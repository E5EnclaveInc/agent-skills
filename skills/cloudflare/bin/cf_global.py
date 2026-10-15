#!/usr/bin/env python3
"""Cloudflare API CLI using the legacy Global API Key.

Same interface as cf.py (METHOD path [--data JSON] [--params JSON]) but
authenticates with the account's Global API Key (X-Auth-Email +
X-Auth-Key headers, from the CLOUDFLARE_EMAIL and
CLOUDFLARE_GLOBAL_API_KEY environment variables). Use it only for
endpoints a scoped token cannot reach (some DNS, speed settings, R2,
DNSSEC reads, worker domains/routes) — the Global Key opens the whole
account, so prefer cf.py's scoped token everywhere else.

Never prints the credential.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.cloudflare.com/client/v4"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--data", default=None)
    ap.add_argument("--params", default=None)
    args = ap.parse_args()

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = args.data.encode("utf-8") if args.data else None
    req = urllib.request.Request(url, data=body, method=args.method.upper())
    req.add_header("Content-Type", "application/json")

    email = os.environ.get("CLOUDFLARE_EMAIL")
    key = os.environ.get("CLOUDFLARE_GLOBAL_API_KEY")
    if not email or not key:
        print("credential error: set CLOUDFLARE_EMAIL and "
              "CLOUDFLARE_GLOBAL_API_KEY", file=sys.stderr)
        return 2
    req.add_header("X-Auth-Email", email)
    req.add_header("X-Auth-Key", key)

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            errs = err.get("errors") or []
            msg = "; ".join(e.get("message", str(e)) for e in errs) or f"HTTP {exc.code}"
        except Exception:
            msg = f"HTTP {exc.code}"
        print(f"cloudflare error: {msg}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
