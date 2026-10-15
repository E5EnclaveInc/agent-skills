#!/usr/bin/env python3
"""Minimal Raisely API CLI using the RAISELY_API_KEY environment variable.

Usage:
    raisely.py GET /v3/campaigns/{uuid}
    raisely.py GET /v3/campaigns/{uuid}/donations --params '{"limit":"50"}'
    raisely.py POST /v3/campaigns/{uuid}/register --data '{...}'

Auth is the campaign private key as a Bearer token (ORG_ADMIN equivalent).
Reads are autonomous; anything that moves money or mutates campaign state
requires the user's explicit confirmation first. Prints the JSON response to
stdout. Exits non-zero with the provider's error message on failure.
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

API = "https://api.raisely.com"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--params", default=None, help="JSON query params")
    ap.add_argument("--data", default=None, help="JSON request body (POST/PUT/PATCH)")
    args = ap.parse_args()

    method = args.method.upper()
    if method not in ("GET", "POST", "PUT", "PATCH"):
        print("raisely error: only GET/POST/PUT/PATCH are supported", file=sys.stderr)
        return 2

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = args.data.encode("utf-8") if args.data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Accept", "application/json")
    if body:
        req.add_header("Content-Type", "application/json")

    key = os.environ.get("RAISELY_API_KEY")
    if not key:
        print("credential error: set the RAISELY_API_KEY environment "
              "variable", file=sys.stderr)
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
        print(f"raisely error: {msg}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
