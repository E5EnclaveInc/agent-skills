"""Shared auth helper for Cloudflare scoped API tokens.

Returns an Authorization header dict for a named token scope. Each scope
reads its own environment variable and falls back to the base
CLOUDFLARE_API_TOKEN, so a single-token setup works everywhere and
least-privilege setups can mint one token per scope:

    "default"  - CLOUDFLARE_API_TOKEN (general work: Workers, KV, zone
                 routes, Email Routing, AI Gateway, Queues, Vectorize,
                 Turnstile, Access, Workers AI)
    "d1"       - CLOUDFLARE_API_TOKEN_D1 (D1 metadata + data reads)
    "d1w"      - CLOUDFLARE_API_TOKEN_D1W (D1 writes)
    "botmgmt"  - CLOUDFLARE_API_TOKEN_BOTMGMT (Bot Management writes)
    "email"    - CLOUDFLARE_API_TOKEN_EMAIL (Email Sending writes)

Usage:
    from cf_auth import auth_header, apply_auth
    for k, v in auth_header("d1").items():
        req.add_header(k, v)
    # or simply:
    apply_auth(req, "d1")

Never prints the token value.
"""
from __future__ import annotations

import os

TOKEN_ENVS = {
    "default": "CLOUDFLARE_API_TOKEN",
    "d1": "CLOUDFLARE_API_TOKEN_D1",
    "d1w": "CLOUDFLARE_API_TOKEN_D1W",
    "botmgmt": "CLOUDFLARE_API_TOKEN_BOTMGMT",
    "email": "CLOUDFLARE_API_TOKEN_EMAIL",
}


def auth_header(scope: str = "default") -> dict:
    """Return {"Authorization": "Bearer <token>"} for the named scope."""
    if scope not in TOKEN_ENVS:
        raise ValueError(
            f"unknown cloudflare token scope {scope!r}; "
            f"expected one of {sorted(TOKEN_ENVS)}"
        )
    token = os.environ.get(TOKEN_ENVS[scope]) or os.environ.get(
        "CLOUDFLARE_API_TOKEN")
    if not token:
        raise RuntimeError(
            f"cloudflare token missing for scope {scope!r}: set "
            f"{TOKEN_ENVS[scope]} (or CLOUDFLARE_API_TOKEN)"
        )
    return {"Authorization": f"Bearer {token}"}


def apply_auth(req, scope: str = "default") -> None:
    """Apply the scoped-token Authorization header to a urllib Request."""
    for k, v in auth_header(scope).items():
        req.add_header(k, v)
