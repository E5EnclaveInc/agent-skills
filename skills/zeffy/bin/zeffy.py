#!/usr/bin/env python3
"""Minimal Zeffy API CLI using the ZEFFY_API_KEY environment variable.

Usage:
    zeffy.py GET /v1/payments
    zeffy.py GET /v1/contacts --params '{"limit":"50"}'
    zeffy.py GET /v1/campaigns --params '{"next_cursor":"..."}'

The Zeffy API is read-only (payments, contacts, campaigns). Prints the JSON
response to stdout. Exits non-zero with the provider's error message on
failure. Never prints the credential.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.zeffy.com"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--params", default=None, help="JSON query params")
    args = ap.parse_args()

    if args.method.upper() != "GET":
        print("zeffy error: API is read-only; only GET is supported", file=sys.stderr)
        return 2

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    req = urllib.request.Request(url, method="GET")
    req.add_header("Accept", "application/json")

    key = os.environ.get("ZEFFY_API_KEY")
    if not key:
        print("credential error: set the ZEFFY_API_KEY environment variable",
              file=sys.stderr)
        return 2
    req.add_header("Authorization", f"Bearer {key}")

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            msg = err.get("message", str(err))
        except Exception:
            msg = f"HTTP {exc.code}"
        print(f"zeffy error: {msg}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
