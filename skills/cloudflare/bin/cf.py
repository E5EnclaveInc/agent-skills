#!/usr/bin/env python3
"""Minimal Cloudflare API CLI using the CLOUDFLARE_API_TOKEN environment
variable (a scoped API token, sent as a Bearer token).

Usage:
    cf.py GET /zones --params '{"name":"example.com"}'
    cf.py POST /zones/{zone_id}/dns_records --data '{"type":"TXT","name":"_x","content":"y"}'
    cf.py PATCH /zones/{zone_id}/email/routing/rules/{rule_id} --data '{...}'
    cf.py DELETE /zones/{zone_id}/dns_records/{record_id}

Paths are appended to https://api.cloudflare.com/client/v4.
Prints the JSON response to stdout. Exits non-zero with the provider's
error message on failure. Never prints the credential.

Prefer a scoped token with only the permissions your task needs. A small
number of endpoints reject scoped tokens; cf_global.py covers those with
the legacy Global API Key instead.
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
    ap.add_argument("--data", default=None, help="JSON request body")
    ap.add_argument("--params", default=None, help="JSON query params")
    args = ap.parse_args()

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = args.data.encode("utf-8") if args.data else None
    req = urllib.request.Request(url, data=body, method=args.method.upper())
    req.add_header("Content-Type", "application/json")

    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        print("credential error: set the CLOUDFLARE_API_TOKEN environment "
              "variable", file=sys.stderr)
        return 2
    req.add_header("Authorization", f"Bearer {token}")

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
