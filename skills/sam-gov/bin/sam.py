#!/usr/bin/env python3
"""Thin SAM.gov API CLI using the SAM_GOV_API_KEY environment variable
(an api.data.gov key, sent as the X-Api-Key header).

Usage:
    sam.py GET /entity-information/v3/entities --params '{"ueiSAM":"..."}'
    sam.py GET /opportunities/v2/search --params '{"limit":1}'

Paths are appended to https://api.sam.gov. Prints the JSON response to stdout.
Exits non-zero with the provider's error message on failure.
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

API = "https://api.sam.gov"


class SamApiError(RuntimeError):
    """The provider answered with a non-2xx status."""


class CredentialError(RuntimeError):
    """The API key environment variable is not set."""


def _provider_message(payload_text: str, code: int) -> str:
    try:
        err = json.loads(payload_text)
        return err.get("errorMessage") or err.get("message") or f"HTTP {code}"
    except json.JSONDecodeError:
        return payload_text[:200] or f"HTTP {code}"


def _request(method: str, url: str, body: bytes | None) -> dict:
    key = os.environ.get("SAM_GOV_API_KEY")
    if not key:
        raise CredentialError(
            "set the SAM_GOV_API_KEY environment variable (an api.data.gov "
            "key)")
    req = urllib.request.Request(url, data=body, method=method.upper())
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("X-Api-Key", key)
    try:
        resp = urllib.request.urlopen(req, timeout=45)
    except urllib.error.HTTPError as exc:
        raise SamApiError(
            f"sam.gov error: {_provider_message(exc.read().decode('utf-8', 'replace'), exc.code)}"
        ) from exc
    return json.loads(resp.read().decode("utf-8"))


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

    try:
        payload = _request(args.method, url, body)
    except SamApiError as exc:
        print(exc, file=sys.stderr)
        return 1
    except CredentialError as exc:
        print(f"credential error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
