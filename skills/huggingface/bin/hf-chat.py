#!/usr/bin/env python3
"""Chat-completions call to Hugging Face Inference using the HF_TOKEN
environment variable (falls back to HUGGINGFACE_API_KEY).

Usage:
  hf-chat.py --model deepseek-ai/DeepSeek-R1 --system "..." --user "..." [--image page.png]
             [--max-tokens 2000] [--timeout 300] [--raw]
Prints the assistant message text (plus a JSON envelope with --raw).
"""
import argparse, base64, json, os, sys, urllib.request


def _auth(req):
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_KEY")
    if not token:
        print("credential error: set the HF_TOKEN environment variable",
              file=sys.stderr)
        sys.exit(2)
    req.add_header("Authorization", f"Bearer {token}")
    return req


def _read_json(resp):
    return json.loads(resp.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--system", default="")
    ap.add_argument("--user", default="")
    ap.add_argument("--messages-json", default="")
    ap.add_argument("--image", default="")
    ap.add_argument("--max-tokens", type=int, default=2000)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--raw", action="store_true")
    ap.add_argument("--stream", action="store_true",
                    help="Use SSE streaming (avoids gateway timeouts on long generations).")
    a = ap.parse_args()

    if a.messages_json:
        messages = json.loads(a.messages_json)
    else:
        messages = []
        if a.system:
            messages.append({"role": "system", "content": a.system})
        if a.image:
            b64 = base64.b64encode(open(a.image, "rb").read()).decode()
            messages.append({"role": "user", "content": [
                {"type": "text", "text": a.user},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
            ]})
        else:
            messages.append({"role": "user", "content": a.user})

    body = {"model": a.model, "messages": messages, "max_tokens": a.max_tokens}
    if a.stream:
        body["stream"] = True
        req = urllib.request.Request("https://router.huggingface.co/v1/chat/completions",
                                     data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", "Accept": "text/event-stream"})
        _auth(req)
        full, reasoning = "", ""
        with urllib.request.urlopen(req, timeout=a.timeout) as r:
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
            print(json.dumps({"content": full, "reasoning_content": reasoning})[:4000])
            return
        print(full)
        return
    req = urllib.request.Request("https://router.huggingface.co/v1/chat/completions",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    _auth(req)
    with urllib.request.urlopen(req, timeout=a.timeout) as r:
        resp = _read_json(r)
    if a.raw:
        print(json.dumps(resp, indent=1)[:4000])
        return
    try:
        msg = resp["choices"][0]["message"]
    except (KeyError, IndexError):
        print(json.dumps(resp)[:2000], file=sys.stderr)
        sys.exit(1)
    if msg.get("reasoning_content"):
        print("=== reasoning (truncated) ===")
        print(msg["reasoning_content"][:1500])
        print("=== answer ===")
    print(msg.get("content", ""))

if __name__ == "__main__":
    main()
