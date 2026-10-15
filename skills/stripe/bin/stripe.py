#!/usr/bin/env python3
"""Minimal Stripe API CLI using the STRIPE_API_KEY environment variable.

Usage:
    stripe.py GET /v1/account
    stripe.py GET /v1/payment_links --params '{"limit":"3"}'
    stripe.py POST /v1/payment_links --data '{"line_items":[...],"metadata":{...}}'

The Stripe API takes form-encoded bodies; --data accepts a JSON object that
is flattened to Stripe's bracket notation. Prints the JSON response to
stdout. Exits non-zero with the provider's error message on failure.
Never prints the credential. Use a restricted key with only the scopes
you need.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.stripe.com"


def flatten(obj, prefix=""):
    """Flatten nested dicts/lists to Stripe bracket-notation pairs."""
    pairs = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}[{k}]" if prefix else str(k)
            pairs.extend(flatten(v, key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            pairs.extend(flatten(v, f"{prefix}[{i}]"))
    else:
        pairs.append((prefix, "" if obj is None else str(obj)))
    return pairs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path")
    ap.add_argument("--data", default=None, help="JSON object, flattened to form-encoding")
    ap.add_argument("--params", default=None, help="JSON query params")
    args = ap.parse_args()

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = None
    if args.data:
        pairs = flatten(json.loads(args.data))
        body = urllib.parse.urlencode(pairs).encode("utf-8")

    req = urllib.request.Request(url, data=body, method=args.method.upper())
    req.add_header("Stripe-Version", "2025-08-27.basil")
    if body:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

    key = os.environ.get("STRIPE_API_KEY")
    if not key:
        print("credential error: set the STRIPE_API_KEY environment "
              "variable", file=sys.stderr)
        return 2
    req.add_header("Authorization", f"Bearer {key}")

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            msg = err.get("error", {}).get("message", str(err))
        except Exception:
            msg = f"HTTP {exc.code}"
        print(f"stripe error: {msg}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
