#!/usr/bin/env python3
"""Groq API CLI using the GROQ_API_KEY environment variable.

Usage:
    groq.py GET /openai/v1/models
    groq.py POST /openai/v1/chat/completions --data '{"model":"...","messages":[...]}'

Paths are appended to https://api.groq.com. Auth is a Bearer API key read
from the GROQ_API_KEY environment variable — the raw key never appears in
code. JSON responses print to stdout; exits non-zero with the provider's
error on failure.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.groq.com"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--data", default=None, help="JSON request body")
    ap.add_argument("--params", default=None, help="JSON query params")
    args = ap.parse_args()

    key = os.environ.get("GROQ_API_KEY")
    if not key:
        print("groq credential error: set the GROQ_API_KEY environment "
              "variable", file=sys.stderr)
        return 2

    url = API + args.path
    if args.params:
        url += "?" + urllib.parse.urlencode(json.loads(args.params))
    body = json.dumps(json.loads(args.data)).encode() if args.data else None
    req = urllib.request.Request(url, method=args.method.upper(), data=body)
    if body:
        req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "groq-python/0.11.0")
    req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            print(json.dumps(json.loads(r.read().decode("utf-8")), indent=1)[:8000])
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        print(f"groq error {e.code}: {detail}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
