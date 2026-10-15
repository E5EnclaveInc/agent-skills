#!/usr/bin/env python3
"""Chat-completions call to NVIDIA NIM using the NVIDIA_API_KEY
environment variable.

Usage:
  nim-chat.py --model <nim-id> --system "..." --user "..." [--image page.png]
              [--max-tokens N] [--timeout S] [--reasoning-effort low|medium|high]
              [--stream] [--raw] [--list-models]
Model IDs rotate on the NIM catalog; prefer IDs confirmed by --list-models.
"""
import argparse, base64, json, os, sys, urllib.request

BASE = "https://integrate.api.nvidia.com/v1"

def authed(method, path, body=None, stream=False):
    headers = {"Content-Type": "application/json"}
    if stream: headers["Accept"] = "text/event-stream"
    req = urllib.request.Request(BASE + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 method=method, headers=headers)
    key = os.environ.get("NVIDIA_API_KEY")
    if not key:
        print("credential error: set the NVIDIA_API_KEY environment variable",
              file=sys.stderr)
        sys.exit(2)
    req.add_header("Authorization", f"Bearer {key}")
    return req

def _read_json(resp):
    return json.loads(resp.read().decode("utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="")
    ap.add_argument("--system", default="")
    ap.add_argument("--user", default="")
    ap.add_argument("--messages-json", default="")
    ap.add_argument("--image", default="")
    ap.add_argument("--max-tokens", type=int, default=2000)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--reasoning-effort", default="", choices=["", "low", "medium", "high"])
    ap.add_argument("--stream", action="store_true")
    ap.add_argument("--raw", action="store_true")
    ap.add_argument("--list-models", action="store_true")
    a = ap.parse_args()

    if a.list_models:
        with urllib.request.urlopen(authed("GET", "/models"), timeout=60) as r:
            d = _read_json(r)
        ids = sorted(m.get("id", "") for m in d.get("data", []))
        print("\n".join(ids)); return

    if a.messages_json:
        messages = json.loads(a.messages_json)
    else:
        messages = []
        if a.system: messages.append({"role": "system", "content": a.system})
        if a.image:
            b64 = base64.b64encode(open(a.image, "rb").read()).decode()
            messages.append({"role": "user", "content": [
                {"type": "text", "text": a.user},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}}]})
        else:
            messages.append({"role": "user", "content": a.user})

    body = {"model": a.model, "messages": messages, "max_tokens": a.max_tokens}
    if a.reasoning_effort: body["reasoning_effort"] = a.reasoning_effort
    if a.stream:
        body["stream"] = True
        full, reasoning = "", ""
        with urllib.request.urlopen(authed("POST", "/chat/completions", body, stream=True),
                                    timeout=a.timeout) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"): continue
                payload = line[5:].strip()
                if payload == "[DONE]": break
                try: d = json.loads(payload)
                except json.JSONDecodeError: continue
                try: delta = d["choices"][0]["delta"]
                except (KeyError, IndexError): continue
                full += delta.get("content") or ""
                reasoning += delta.get("reasoning_content") or ""
        if a.raw:
            print(json.dumps({"content": full, "reasoning_content": reasoning})[:4000]); return
        print(full); return

    with urllib.request.urlopen(authed("POST", "/chat/completions", body),
                                timeout=a.timeout) as r:
        resp = _read_json(r)
    if a.raw:
        print(json.dumps(resp)[:4000]); return
    try: msg = resp["choices"][0]["message"]
    except (KeyError, IndexError):
        print(json.dumps(resp)[:2000], file=sys.stderr); sys.exit(1)
    print(msg.get("content", ""))

if __name__ == "__main__":
    main()
