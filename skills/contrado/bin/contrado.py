#!/usr/bin/env python3
"""Minimal Contrado Helix API CLI using the CONTRADO_API_KEY environment variable.

Usage:
    contrado.py GET /products --params '{"limit": 1}'
    contrado.py POST /orders --data '{...}'

Base URL is fixed: https://api.contrado.app/helix/v1. No sandbox is publicly
documented, so treat every call as production-adjacent: never POST an order
without explicit approval.

Auth placement (x-api-key header) was verified against the provider's own
WordPress plugin source — see SKILL.md. If a credential-carrying request
401s/403s, suspect the header name first.

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

BASE = "https://api.contrado.app/helix/v1"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--data", default=None, help="JSON request body")
    ap.add_argument("--params", default=None, help="JSON query params")
    args = ap.parse_args()

    url = BASE + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = args.data.encode("utf-8") if args.data else None
    req = urllib.request.Request(url, data=body, method=args.method.upper())
    req.add_header("Accept", "application/json")
    if body:
        req.add_header("Content-Type", "application/json")

    key = os.environ.get("CONTRADO_API_KEY")
    if not key:
        print("credential error: set the CONTRADO_API_KEY environment "
              "variable", file=sys.stderr)
        return 2
    req.add_header("x-api-key", key)
    store = os.environ.get("CONTRADO_STORE_ID")
    if store:
        req.add_header("X-Store-Id", store)

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        payload = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(payload, indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8", "replace"))
            detail = json.dumps(payload)
        except Exception:
            detail = f"HTTP {exc.code}"
        print(f"HTTP {exc.code}: {detail}", file=sys.stderr)
        return 1
    except Exception as exc:  # network-level failures
        print(f"request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
