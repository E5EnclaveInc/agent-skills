#!/usr/bin/env python3
"""Minimal GitHub API CLI using the GITHUB_TOKEN environment variable.

Usage:
    gh.py GET /repos/{owner}/{repo}
    gh.py GET /repos/{owner}/{repo}/contents/{path} --params '{"ref":"main"}'
    gh.py POST /repos/{owner}/{repo}/issues --data '{"title":"...","body":"..."}'
    gh.py PUT /repos/{owner}/{repo}/contents/{path} --data '{...}'

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

API = "https://api.github.com"


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
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if body:
        req.add_header("Content-Type", "application/json")

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("github credential error: set the GITHUB_TOKEN environment "
              "variable", file=sys.stderr)
        return 2
    req.add_header("Authorization", f"Bearer {token}")

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            msg = err.get("message", str(err))
        except Exception:
            msg = f"HTTP {exc.code}"
        print(f"github error: {msg}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
