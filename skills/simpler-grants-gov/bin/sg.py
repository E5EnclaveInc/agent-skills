#!/usr/bin/env python3
"""Simpler.Grants.gov REST API CLI using the SIMPLER_GRANTS_API_KEY
environment variable.

Usage:
    sg.py health
    sg.py search --query "nonprofit" [--page 1] [--page-size 25] [--filters '{"opportunity_status":{"one_of":["posted"]}}']
    sg.py get <legacy_opportunity_id>
    sg.py agencies [--query "health"] [--page-size 25] [--data '{...}']

Prints the JSON response to stdout. Exits non-zero with the provider's
error message on failure. Never prints the credential.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.simpler.grants.gov"


def _req(method: str, path: str, body: dict | None = None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "GrantsSearch/1.0")
    if data:
        req.add_header("Content-Type", "application/json")
    key = os.environ.get("SIMPLER_GRANTS_API_KEY")
    if not key:
        print("credential error: set the SIMPLER_GRANTS_API_KEY environment "
              "variable", file=sys.stderr)
        sys.exit(2)
    req.add_header("X-API-Key", key)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            msg = err.get("message") or err.get("detail") or str(err)
        except Exception:
            msg = f"HTTP {exc.code}"
        print(f"simpler-grants-gov error: {msg}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("health")

    sp = sub.add_parser("search")
    sp.add_argument("--query", default=None)
    sp.add_argument("--page", type=int, default=1)
    sp.add_argument("--page-size", type=int, default=25)
    sp.add_argument("--filters", default=None, help="JSON filters object")

    gp = sub.add_parser("get")
    gp.add_argument("opportunity_id")

    apg = sub.add_parser("agencies")
    apg.add_argument("--query", default=None)
    apg.add_argument("--page-size", type=int, default=25)
    apg.add_argument("--data", default=None, help="raw JSON body override")

    args = ap.parse_args()

    if args.cmd == "health":
        print(json.dumps(_req("GET", "/health"), indent=2))
    elif args.cmd == "search":
        body = {"pagination": {"page_offset": args.page,
                               "page_size": args.page_size}}
        if args.query:
            body["query"] = args.query
        if args.filters:
            body["filters"] = json.loads(args.filters)
        print(json.dumps(_req("POST", "/v1/opportunities/search", body),
                         indent=2))
    elif args.cmd == "get":
        print(json.dumps(
            _req("GET", f"/v1/opportunities/{args.opportunity_id}"), indent=2))
    elif args.cmd == "agencies":
        if args.data:
            body = json.loads(args.data)
        else:
            body = {"pagination": {"page_offset": 1,
                                   "page_size": args.page_size}}
            if args.query:
                body["query"] = args.query
        print(json.dumps(_req("POST", "/v1/agencies/search", body), indent=2))


if __name__ == "__main__":
    main()
