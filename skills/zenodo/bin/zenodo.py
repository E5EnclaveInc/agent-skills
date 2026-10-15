#!/usr/bin/env python3
"""Minimal Zenodo API CLI using the ZENODO_ACCESS_TOKEN environment variable.

Usage:
    zenodo.py GET /api/records/{id}
    zenodo.py POST /api/deposit/depositions/{id}/actions/newversion
    zenodo.py DELETE /api/deposit/depositions/{id}/files/{file_id}
    zenodo.py PUT /api/deposit/depositions/{id} --data '{"metadata": {...}}'
    zenodo.py POST /api/deposit/depositions/{id}/actions/publish
    zenodo.py PUT-BUCKET --bucket {links.bucket} --upload-file PATH --upload-name "a/b.zip"

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

API = "https://zenodo.org"


def do_request(req: urllib.request.Request) -> dict:
    token = os.environ.get("ZENODO_ACCESS_TOKEN")
    if not token:
        print("credential error: set the ZENODO_ACCESS_TOKEN environment "
              "variable", file=sys.stderr)
        sys.exit(2)
    req.add_header("Authorization", f"Bearer {token}")
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            msg = err.get("message", str(err))
        except Exception:
            msg = f"HTTP {exc.code}"
        print(f"zenodo error: {msg}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(payload, indent=2))
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("path", nargs="?", default="")
    ap.add_argument("--data", default=None, help="JSON request body")
    ap.add_argument("--params", default=None, help="JSON query params")
    ap.add_argument("--bucket", default=None, help="Bucket URL for PUT-BUCKET")
    ap.add_argument("--upload-file", default=None, help="Local file for PUT-BUCKET")
    ap.add_argument("--upload-name", default=None, help="Remote filename for PUT-BUCKET")
    args = ap.parse_args()

    if args.method.upper() == "PUT-BUCKET":
        if not (args.bucket and args.upload_file and args.upload_name):
            print("PUT-BUCKET needs --bucket, --upload-file, --upload-name", file=sys.stderr)
            return 2
        url = args.bucket.rstrip("/") + "/" + args.upload_name
        with open(args.upload_file, "rb") as fh:
            body = fh.read()
        req = urllib.request.Request(url, data=body, method="PUT")
        req.add_header("Content-Type", "application/octet-stream")
        req.add_header("Content-Length", str(len(body)))
        do_request(req)
        return 0

    url = API + args.path
    if args.params:
        qs = urllib.parse.urlencode(json.loads(args.params))
        url = url + ("&" if "?" in url else "?") + qs

    body = args.data.encode("utf-8") if args.data else None
    req = urllib.request.Request(url, data=body, method=args.method.upper())
    req.add_header("Accept", "application/json")
    if body:
        req.add_header("Content-Type", "application/json")

    do_request(req)
    return 0


if __name__ == "__main__":
    sys.exit(main())
