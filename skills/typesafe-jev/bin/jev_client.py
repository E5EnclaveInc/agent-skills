#!/usr/bin/env python3
"""Importable TypeSafe/Jev client (stdlib only).

Auth: the API key is read from the ``TYPESAFE_API_KEY`` environment variable
and sent as an ``Authorization: Bearer`` header. The key is never printed,
logged, or persisted by this module.

Usage:
    from jev_client import list_models, ask_systemone
    models = list_models()
    resp = ask_systemone(state="...", questions={
        "admit": {"type": "choice",
                  "instructions": "Should this row be KEPT or REJECTED?",
                  "criteria": {"KEEP": "...", "REJECT": "..."}}})
"""

from __future__ import annotations

import json
import os
import urllib.request

BASE = "https://api.typesafe.ai"
ALLOWED_HOSTS = ["api.typesafe.ai"]
API_KEY_ENV = "TYPESAFE_API_KEY"
DEFAULT_MODEL = "jev-latest"


class JevError(RuntimeError):
    """Raised on transport or API-level failure."""


def _request(method: str, path: str, body: dict | None = None) -> dict:
    url = BASE + path
    data = None
    req = urllib.request.Request(url, method=method)
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
    key = os.environ.get(API_KEY_ENV)
    if not key:
        raise JevError(f"{API_KEY_ENV} is not set — export your TypeSafe API key first")
    req.add_header("Authorization", f"Bearer {key}")
    try:
        resp = urllib.request.urlopen(req, timeout=60)
    except Exception as exc:  # noqa: BLE001
        raise JevError(f"{method} {path} transport failure: {type(exc).__name__}: {exc}")
    try:
        payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise JevError(f"{method} {path}: unreadable response: {exc}")
    if isinstance(payload, dict) and "error" in payload:
        raise JevError(f"{method} {path} API error: {payload['error']}")
    return payload


def list_models() -> dict:
    """GET /v1/models. Read-only auth check; no spend."""
    return _request("GET", "/v1/models")


def ask_systemone(
    state: str,
    questions: dict,
    model: str = DEFAULT_MODEL,
) -> dict:
    """POST /v1/systemone. Returns the parsed JSON response dict.

    Response shape (per official docs): {"model": str, "answers": {...},
    "usage": {"input_tokens": int, "output_tokens": int}}.
    """
    if not state or not questions:
        raise JevError("ask_systemone requires non-empty state and questions")
    return _request(
        "POST", "/v1/systemone",
        {"state": state, "model": model, "questions": questions},
    )


def estimate_input_tokens(text: str) -> int:
    """Rough token estimate for spend-cap math: ~4 chars per token."""
    return max(1, len(text) // 4)


def call_cost_usd(input_tokens: int, price_per_mtok: float = 0.042) -> float:
    """Vendor-stated pricing: $0.042/MTok input, outputs free."""
    return input_tokens / 1_000_000 * price_per_mtok
