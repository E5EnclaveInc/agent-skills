#!/usr/bin/env python3
"""Google Ads API CLI using environment-variable credentials.

Credential model (all read from the environment; never printed):
    GOOGLE_ADS_DEVELOPER_TOKEN  developer token (Ads Manager -> Admin ->
                                API Center); sent as the developer-token header
    GOOGLE_ADS_CLIENT_ID        OAuth client ID (Google Cloud Console,
                                Web application client, Google Ads API enabled)
    GOOGLE_ADS_CLIENT_SECRET    OAuth client secret
    GOOGLE_ADS_REFRESH_TOKEN    OAuth refresh token (minted via the user's
                                Google OAuth consent flow)
    GOOGLE_ADS_CUSTOMER_ID      default Ads customer ID, digits only (an
                                account identifier, not a secret); the
                                --customer-id flag overrides it

Usage:
    gads.py [--customer-id ID] [--login-customer-id MGR] METHOD /path [--data '{...}']
    gads.py --setup-check

Examples:
    gads.py POST /v25/customers/1234567890/googleAds:search \
        --data '{"query":"SELECT campaign.name,campaign.status FROM campaign"}'

Paths are appended to https://googleads.googleapis.com.
Prints JSON to stdout. Exits non-zero with the provider's error message.
Never prints raw credentials.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://googleads.googleapis.com"
TOKEN_URL = "https://oauth2.googleapis.com/token"

ENV_DEVTOKEN = "GOOGLE_ADS_DEVELOPER_TOKEN"
ENV_CLIENT_ID = "GOOGLE_ADS_CLIENT_ID"
ENV_CLIENT_SECRET = "GOOGLE_ADS_CLIENT_SECRET"
ENV_REFRESH_TOKEN = "GOOGLE_ADS_REFRESH_TOKEN"
ENV_CUSTOMER_ID = "GOOGLE_ADS_CUSTOMER_ID"


class CredentialError(RuntimeError):
    """A required environment variable is missing."""


# access-token cache: in-process only, fine for short-lived reuse
_TOKEN_CACHE = {"token": None, "exp": 0}


def _env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise CredentialError(f"missing environment variable: {name}")
    return value


def _access_token() -> str:
    now = time.time()
    if _TOKEN_CACHE["token"] and _TOKEN_CACHE["exp"] - now > 120:
        return _TOKEN_CACHE["token"]
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": _env(ENV_REFRESH_TOKEN),
        "client_id": _env(ENV_CLIENT_ID),
        "client_secret": _env(ENV_CLIENT_SECRET),
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        payload = json.loads(
            urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise CredentialError(f"token exchange failed: HTTP {exc.code}")
    _TOKEN_CACHE["token"] = payload["access_token"]
    _TOKEN_CACHE["exp"] = now + int(payload.get("expires_in", 3600))
    return _TOKEN_CACHE["token"]


def api_call(method: str, path: str, body: dict | None,
             login_customer_id: str | None) -> dict:
    token = _access_token()
    url = API + path
    raw = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=raw, method=method.upper())
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("developer-token", _env(ENV_DEVTOKEN))
    # login-customer-id is ONLY for acting through a manager account.
    # Direct access to the target customer must NOT send it.
    if login_customer_id:
        req.add_header("login-customer-id", login_customer_id)
    try:
        return json.loads(
            urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            details = err.get("error", {}).get("details", [])
            msg = "; ".join(
                d.get("errors", [{}])[0].get("message", "") for d in details if d.get("errors")
            ) or err.get("error", {}).get("message", f"HTTP {exc.code}")
        except Exception:
            msg = f"HTTP {exc.code}"
        print(f"google ads error: {msg}", file=sys.stderr)
        sys.exit(1)


def setup_check() -> int:
    missing = [name for name in (ENV_DEVTOKEN, ENV_CLIENT_ID,
                                 ENV_CLIENT_SECRET, ENV_REFRESH_TOKEN)
               if not os.environ.get(name, "").strip()]
    if missing:
        print("missing:", ", ".join(missing))
        return 1
    print("google-ads skill: all credential environment variables present")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--setup-check", action="store_true")
    ap.add_argument("--customer-id", default=None)
    ap.add_argument("--login-customer-id", default=None,
                    help="Manager account to act through. Omit for direct access.")
    ap.add_argument("method", nargs="?")
    ap.add_argument("path", nargs="?")
    ap.add_argument("--data", default=None)
    args = ap.parse_args()

    if args.setup_check:
        return setup_check()
    if not args.method or not args.path:
        ap.error("METHOD and /path are required (or --setup-check)")

    cid = args.customer_id or os.environ.get(ENV_CUSTOMER_ID, "").strip()
    if not cid:
        print("need --customer-id or the GOOGLE_ADS_CUSTOMER_ID environment "
              "variable (Ads customer ID, digits only)", file=sys.stderr)
        return 2
    if "/customers/" not in args.path:
        print("note: path does not embed a customer id; the API expects "
              "/v25/customers/<id>/... — proceeding as given",
              file=sys.stderr)
    body = json.loads(args.data) if args.data else None
    try:
        print(json.dumps(api_call(args.method, args.path, body,
                                  args.login_customer_id), indent=2))
    except CredentialError as exc:
        print(f"credential error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
