#!/usr/bin/env python3
"""Download files/dirs from a Lambda instance via its JupyterLab contents API.

Usage:
  jfile.py <instance-id> <remote-path> <local-dest> [--text]
  jfile.py <instance-id> --ls <remote-path>

<remote-path> is RELATIVE to the Jupyter root (/home/ubuntu) — absolute
instance paths (e.g. /lambda/nfs/...) are NOT reachable here. Stage them
first with jterm, e.g.:
  jterm.py <id> "tar czf ~/artifacts.tar.gz -C /lambda/nfs/my-fs runs/shakedown-02"
  jfile.py <id> artifacts.tar.gz /local/dest.tar.gz

Directories are downloaded recursively. Binary-safe (base64); --text forces
text mode (useful for logs you want to read raw).

Never prints the API key or Jupyter token.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jcommon import api_key, jupyter  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def curl_json(url: str, attempts: int = 8) -> dict:
    """GET JSON via requests (2026-09-17: this sandbox's egress proxy returns
    EMPTY bodies for curl on the chunked /api/contents endpoint — every call
    failed 8/8 with 'Expecting value: line 1 column 1 (char 0)', while
    requests gets STATUS 200 first try. Same transport lesson as jcommon:
    requests handles the proxy's chunked responses, curl/urllib do not).
    Backs off generously; this endpoint sometimes blackholes in bursts."""
    import random
    import requests
    last = None
    for i in range(attempts):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=120)
            if r.status_code in (400, 404):
                # Deterministic client errors: 400 = wrong node type for the
                # requested type= (caller falls back); 404 = not present.
                # Never worth retrying.
                r.raise_for_status()
            r.raise_for_status()
            if r.text.strip():
                return r.json()
            last = RuntimeError("empty body")
        except Exception as e:
            last = e
            s = str(e)
            if " 400 " in f" {s} " or " 404 " in f" {s} ":
                break
        time.sleep(min(30, 2 ** i) + random.uniform(0, 2))
    raise RuntimeError(f"contents API failed after {attempts} attempts: {last}")


def api_get(base: str, token: str, path: str, **params):
    q = "&".join(f"{k}={quote(str(v), safe='')}" for k, v in params.items())
    # (postmortem note): remote paths are relative
    # (e.g. "bench-02-artifacts.tar.gz", or "path" from the API's
    # directory listings — no leading slash). Concatenating such a path
    # straight onto "/api/contents" produced
    # ".../api/contentsbench-02-artifacts.tar.gz" (missing separator
    # -> 404), which is why the artifact tarball was never retrievable.
    # Normalize the separating slash here so every caller is safe.
    if not path.startswith("/"):
        path = "/" + path
    url = f"{base}/api/contents{quote(path, safe='/')}?token={quote(token)}&{q}"
    return curl_json(url)


def _is_400(exc):
    s = str(exc)
    return " 400 " in f" {s} " or "400 Client Error" in s


def download(base, token, remote, local, text):
    """Pull one remote path (file or directory tree) to a local path.

    Tries a file fetch first; the Jupyter contents API answers HTTP 400
    when a directory is queried with type=file, so on a 400 the target is
    re-fetched as a directory and recursed. (2026-09-19: the old code
    queried every target with type=file and died on directories.)
    """
    try:
        meta = api_get(base, token, remote, type="file",
                       format="text" if text else "base64", content=1)
    except RuntimeError as e:
        if not _is_400(e):
            raise
        meta = api_get(base, token, remote, type="directory", content=1)
    if meta.get("type") == "directory":
        for ch in meta.get("content", []) or []:
            download(base, token, remote.rstrip("/") + "/" + ch["name"],
                     os.path.join(local, ch["name"]), text)
        return
    content = meta.get("content", "")
    data = content.encode() if text else base64.b64decode(content)
    Path(local).parent.mkdir(parents=True, exist_ok=True)
    Path(local).write_bytes(data)
    print(f"pulled {remote} -> {local} ({len(data)} bytes)")


def ls(base, token, remote):
    meta = api_get(base, token, remote, type="directory", content=1)
    for ch in meta.get("content", []) or []:
        print(ch.get("type"), ch.get("name"), ch.get("size", ""))


def main():
    ap = argparse.ArgumentParser(description="Pull files/dirs from a Lambda box.")
    ap.add_argument("iid")
    ap.add_argument("--ls", action="store_true",
                    help="list remote directory instead of downloading")
    ap.add_argument("remote")
    ap.add_argument("local", nargs="?")
    ap.add_argument("--text", action="store_true")
    a = ap.parse_args()
    base, token = jupyter(a.iid)
    if a.ls:
        ls(base, token, a.remote)
    else:
        if not a.local:
            ap.error("local destination required (or use --ls)")
        download(base, token, a.remote, a.local, a.text)


if __name__ == "__main__":
    main()
