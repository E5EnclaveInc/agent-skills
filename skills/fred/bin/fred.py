#!/usr/bin/env python3
"""Minimal FRED API CLI using the FRED_API_KEY environment variable.

Usage:
    fred.py observations SERIES_ID [--start YYYY-MM-DD] [--end YYYY-MM-DD]
                                   [--limit N] [--sort-order asc|desc]
    fred.py series SERIES_ID

Prints the JSON response to stdout. Exits non-zero with the provider's
error message on failure. Never prints the credential.

The API key is sent as the `api_key` query parameter, which is how the
FRED API reads it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.stlouisfed.org"


def call(path: str, params: dict) -> dict:
    key = os.environ.get("FRED_API_KEY")
    if not key:
        print("credential error: set the FRED_API_KEY environment variable",
              file=sys.stderr)
        sys.exit(2)
    params = {**params, "api_key": key}
    url = API + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    req.add_header("Accept", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        print(f"FRED HTTP {exc.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001 - transport failure
        print(f"FRED transport error: {exc}", file=sys.stderr)
        sys.exit(1)
    raw = resp.read()
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        print("FRED response was not valid JSON", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ob = sub.add_parser("observations")
    ob.add_argument("series_id")
    ob.add_argument("--start", default=None)
    ob.add_argument("--end", default=None)
    ob.add_argument("--limit", default=None)
    ob.add_argument("--sort-order", default="desc",
                    choices=["asc", "desc"])

    se = sub.add_parser("series")
    se.add_argument("series_id")

    args = ap.parse_args()
    if args.cmd == "observations":
        params = {"series_id": args.series_id, "file_type": "json",
                  "sort_order": args.sort_order}
        if args.start:
            params["observation_start"] = args.start
        if args.end:
            params["observation_end"] = args.end
        if args.limit:
            params["limit"] = args.limit
        payload = call("/fred/series/observations", params)
    else:
        payload = call("/fred/series",
                       {"series_id": args.series_id, "file_type": "json"})
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
