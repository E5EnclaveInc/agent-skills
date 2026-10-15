#!/usr/bin/env python3
"""Minimal Codemagic API CLI using the CODEMAGIC_API_KEY environment variable.

Usage:
    cm.py GET /apps
    cm.py POST /builds --data '{"appId":"...","workflowId":"...","branch":"main"}'
    cm.py GET /builds/<build_id> --params '{"x":"y"}'

Paths are appended to https://api.codemagic.io.
Prints the JSON response to stdout. Exits non-zero with the provider's
error message on failure. Never prints the credential.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.codemagic.io"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--data", default=None, help="JSON request body")
    ap.add_argument("--params", default=None, help="JSON query params")
    args = ap.parse_args()

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = args.data.encode("utf-8") if args.data else None
    req = urllib.request.Request(url, data=body, method=args.method.upper())
    req.add_header("Accept", "application/json")
    if body:
        req.add_header("Content-Type", "application/json")

    key = os.environ.get("CODEMAGIC_API_KEY")
    if not key:
        print("codemagic credential error: set the CODEMAGIC_API_KEY "
              "environment variable", file=sys.stderr)
        return 2
    req.add_header("x-api-key", key)

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err = e.read().decode("utf-8", errors="replace")
        except Exception:
            err = str(e)
        print(f"codemagic error: {err[:500]}", file=sys.stderr)
        return 1
    print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
