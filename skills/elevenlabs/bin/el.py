#!/usr/bin/env python3
"""ElevenLabs API CLI using the ELEVENLABS_API_KEY environment variable.

Usage:
    el.py GET /v1/voices
    el.py POST /v1/text-to-speech/{voice_id} --data '{"text":"hello"}' --out voice.mp3
    el.py POST /v1/speech-to-text --file file=/tmp/a.wav --data '{"model_id":"scribe_v2"}'
    el.py GET /v1/user --params '{"x":"y"}'

Paths are appended to https://api.elevenlabs.io.
JSON responses print to stdout; binary responses (audio) need --out FILE.
Exits non-zero with the provider's error message on failure.
Never prints the credential.

Spend discipline (encoded, not advisory):
  --idempotent      content-hash cache (method+path+body) under the
                    scratch dir (EL_SCRATCH_DIR, default /tmp/elevenlabs/);
                    a cache hit performs NO api call. Default ON for POST
                    /v1/text-to-speech/* (the pay-per-character lane).
  Retries: exponential backoff (1s/2s/4s, max 3) on 408/409/429/5xx and
  network errors. Never hot-loops on 429.
  Usage: every call appends one JSONL line to usage.jsonl in the scratch
         dir (unit-labeled, so spend can be audited offline).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://api.elevenlabs.io"
# Contract: machine state (cache, usage logs) lives ONLY under the scratch
# dir — never inside the skill dir. Relocate via EL_SCRATCH_DIR.
SCRATCH = os.environ.get("EL_SCRATCH_DIR", "/tmp/elevenlabs")
CACHE_DIR = os.path.join(SCRATCH, "cache")
USAGE_LOG = os.path.join(SCRATCH, "usage.jsonl")

RETRYABLE = {408, 409, 429} | set(range(500, 600))
MAX_RETRIES = 3


class CredentialError(RuntimeError):
    """The ELEVENLABS_API_KEY environment variable is not set."""


def log_usage(entry: dict) -> None:
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **entry}
    try:
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        print(f"usage-log warning: {e}", file=sys.stderr)


def product_of(path: str) -> str:
    if path.startswith("/v1/text-to-speech"):
        return "tts"
    if path.startswith("/v1/speech-to-text"):
        return "stt"
    if path.startswith("/v1/sound-generation") or path.startswith("/v1/text-to-sound-effects"):
        return "sfx"
    if path.startswith("/v1/music"):
        return "music"
    if path.startswith("/v1/user"):
        return "account"
    return "other"


def cache_key(method: str, path: str, body: bytes | None) -> str:
    h = hashlib.sha256()
    h.update(method.upper().encode())
    h.update(b"\x00" + path.encode())
    h.update(b"\x00" + (body or b""))
    return h.hexdigest()


def encode_multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    """Build a multipart/form-data body.

    fields: {name: text_value} — plain text parts.
    files: {name: path} — file parts; the part Content-Type is guessed from the
    file extension (ElevenLabs rejects application/octet-stream on KB upload).
    """
    boundary = uuid.uuid4().hex
    buf = io.BytesIO()
    for k, v in fields.items():
        buf.write(f"--{boundary}\r\n".encode())
        buf.write(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode())
        buf.write(str(v).encode() + b"\r\n")
    for k, p in files.items():
        fname = os.path.basename(p)
        ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
        buf.write(f"--{boundary}\r\n".encode())
        buf.write(
            f'Content-Disposition: form-data; name="{k}"; filename="{fname}"\r\n'.encode()
        )
        buf.write(f"Content-Type: {ctype}\r\n\r\n".encode())
        with open(p, "rb") as f:
            buf.write(f.read())
        buf.write(b"\r\n")
    buf.write(f"--{boundary}--\r\n".encode())
    return buf.getvalue(), f"multipart/form-data; boundary={boundary}"


def do_request(url: str, body: bytes | None, content_type: str | None, method: str):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise CredentialError(
            "set the ELEVENLABS_API_KEY environment variable")
    req = urllib.request.Request(url, data=body, method=method.upper())
    req.add_header("Accept", "*/*")
    if content_type:
        req.add_header("Content-Type", content_type)
    req.add_header("xi-api-key", key)
    return urllib.request.urlopen(req)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--data", default=None, help="JSON request body")
    ap.add_argument("--params", default=None, help="JSON query params")
    ap.add_argument("--file", action="append", default=[],
                    help="multipart part: name=/path for a file, or name=text for a "
                         "plain text field (repeatable)")
    ap.add_argument("--out", default=None, help="write binary response to FILE")
    ap.add_argument("--idempotent", dest="idempotent", action="store_true", default=None,
                    help="enable content-hash cache (default ON for TTS POST)")
    ap.add_argument("--no-idempotent", dest="idempotent", action="store_false",
                    help="disable content-hash cache")
    args = ap.parse_args()

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    data_obj = json.loads(args.data) if args.data else {}
    files = {}
    for spec in args.file:
        name, _, val = spec.partition("=")
        if not name or not val:
            print(f"bad --file spec (want name=/path or name=text): {spec}", file=sys.stderr)
            return 2
        if os.path.isfile(val):
            files[name] = val
        else:
            data_obj[name] = val  # plain text part, not a file

    body: bytes | None
    content_type: str | None
    if files:
        body, content_type = encode_multipart(data_obj, files)
    elif args.method.upper() in ("POST", "PUT", "PATCH"):
        body = json.dumps(data_obj).encode("utf-8")
        content_type = "application/json"
    else:
        body, content_type = None, None

    product = product_of(args.path)
    idempotent = args.idempotent
    if idempotent is None:
        idempotent = args.method.upper() == "POST" and args.path.startswith(
            "/v1/text-to-speech"
        )

    # ---- content-hash idempotency ----
    ckey = cache_key(args.method, url, body) if idempotent else None
    if ckey:
        os.makedirs(CACHE_DIR, exist_ok=True)
        hit = os.path.join(CACHE_DIR, ckey + ".bin")
        meta_p = os.path.join(CACHE_DIR, ckey + ".json")
        if os.path.exists(hit):
            meta = {}
            if os.path.exists(meta_p):
                meta = json.load(open(meta_p))
            if args.out:
                with open(hit, "rb") as src, open(args.out, "wb") as dst:
                    dst.write(src.read())
                print(f"idempotency cache HIT ({ckey[:12]}): no API call, wrote {args.out}")
            else:
                ctype = meta.get("content_type", "")
                if ctype.startswith("application/json"):
                    print(open(hit).read())
                else:
                    print(f"idempotency cache HIT ({ckey[:12]}): binary, pass --out to restore")
            log_usage({"endpoint": args.path, "method": args.method.upper(),
                       "product": product, "cache_hit": True, "status": "ok"})
            return 0

    # ---- request with exponential backoff (never hot-loop) ----
    t0 = time.time()
    retries = 0
    last_err = ""
    resp = None
    while True:
        try:
            resp = do_request(url, body, content_type, args.method)
            break
        except urllib.error.HTTPError as e:
            try:
                last_err = e.read().decode("utf-8", errors="replace")[:500]
            except Exception:
                last_err = str(e)
            if e.code in RETRYABLE and retries < MAX_RETRIES:
                wait = 2 ** retries
                print(f"HTTP {e.code}, backing off {wait}s (retry {retries+1}/{MAX_RETRIES})",
                      file=sys.stderr)
                time.sleep(wait)
                retries += 1
                continue
            print(f"elevenlabs error: {last_err}", file=sys.stderr)
            log_usage({"endpoint": args.path, "method": args.method.upper(),
                       "product": product, "cache_hit": False, "retries": retries,
                       "latency_ms": int((time.time() - t0) * 1000),
                       "status": f"http_{e.code}", "error": last_err[:200]})
            return 1
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = str(e)[:200]
            if retries < MAX_RETRIES:
                wait = 2 ** retries
                print(f"network error ({last_err}), backing off {wait}s "
                      f"(retry {retries+1}/{MAX_RETRIES})", file=sys.stderr)
                time.sleep(wait)
                retries += 1
                continue
            print(f"elevenlabs network error: {last_err}", file=sys.stderr)
            log_usage({"endpoint": args.path, "method": args.method.upper(),
                       "product": product, "cache_hit": False, "retries": retries,
                       "latency_ms": int((time.time() - t0) * 1000),
                       "status": "network_error", "error": last_err[:200]})
            return 1
        except CredentialError as e:
            print(f"elevenlabs credential error: {e}", file=sys.stderr)
            return 2

    latency_ms = int((time.time() - t0) * 1000)
    ctype = resp.headers.get("Content-Type", "")
    raw = resp.read()
    resp.close()

    # ---- usage logging (unit-labeled) ----
    entry: dict = {"endpoint": args.path, "method": args.method.upper(),
                   "product": product, "cache_hit": False, "retries": retries,
                   "latency_ms": latency_ms, "status": "ok",
                   "response_bytes": len(raw)}
    if product == "tts" and isinstance(data_obj, dict) and "text" in data_obj:
        entry["characters"] = len(data_obj["text"])
        entry["model"] = data_obj.get("model_id")
        entry["voice_id"] = args.path.rstrip("/").split("/")[-1]
    if product == "music":
        entry["model"] = data_obj.get("model_id") if isinstance(data_obj, dict) else None
    if product == "stt":
        entry["model"] = data_obj.get("model_id") if isinstance(data_obj, dict) else None
    log_usage(entry)

    # ---- cache the result for idempotent POSTs ----
    if ckey:
        with open(os.path.join(CACHE_DIR, ckey + ".bin"), "wb") as f:
            f.write(raw)
        json.dump({"content_type": ctype, "product": product,
                   "endpoint": args.path},
                  open(os.path.join(CACHE_DIR, ckey + ".json"), "w"))

    if ctype.startswith("application/json") or raw[:1] in (b"{", b"["):
        text = raw.decode("utf-8", errors="replace")
        print(text[:20000])
    else:
        if args.out:
            with open(args.out, "wb") as f:
                f.write(raw)
            print(f"wrote {len(raw)} bytes to {args.out} ({ctype or 'binary'})")
        else:
            sys.stdout.buffer.write(raw)
    return 0


if __name__ == "__main__":
    sys.exit(main())
