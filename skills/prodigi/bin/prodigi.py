#!/usr/bin/env python3
"""Minimal Prodigi Print API v4 CLI using environment-variable API keys.

Usage:
    prodigi.py GET /v4.0/Products --params '{"pageSize": 5}'
    prodigi.py POST /v4.0/Orders --data '{...}' --live

Defaults to the sandbox environment (api.sandbox.prodigi.com), keyed by
PRODIGI_API_KEY. Pass --live for production (api.prodigi.com), keyed by
PRODIGI_API_KEY_LIVE — sandbox and live use different keys. Live orders
are produced, shipped and charged, so never use --live without explicit
approval.

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

SANDBOX = "https://api.sandbox.prodigi.com"
LIVE = "https://api.prodigi.com"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--data", default=None, help="JSON request body")
    ap.add_argument("--params", default=None, help="JSON query params")
    ap.add_argument("--live", action="store_true", help="use production API")
    args = ap.parse_args()

    url = (LIVE if args.live else SANDBOX) + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = args.data.encode("utf-8") if args.data else None
    req = urllib.request.Request(url, data=body, method=args.method.upper())
    req.add_header("Accept", "application/json")
    if body:
        req.add_header("Content-Type", "application/json")

    env_name = "PRODIGI_API_KEY_LIVE" if args.live else "PRODIGI_API_KEY"
    key = os.environ.get(env_name)
    if not key:
        print(f"credential error: set the {env_name} environment variable",
              file=sys.stderr)
        return 2
    req.add_header("X-API-Key", key)

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
