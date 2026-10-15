---
name: prodigi
description: "Work with the Prodigi print-on-demand API v4: products, quotes, and orders — sandbox by default, live only on request. Use when a task involves Prodigi or its print API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and PRODIGI_API_KEY set in the environment (PRODIGI_API_KEY_LIVE for --live)."
metadata:
  version: 1.0.0
---

# Prodigi

A thin, scriptable client for the Prodigi print API v4 (X-API-Key header auth).

## Credentials

- `PRODIGI_API_KEY` (required) — sandbox API key, sent as the `X-API-Key` header.
- `PRODIGI_API_KEY_LIVE` (required only for `--live`) — production API key. Sandbox and Live use **different** keys: a live key will 401 against the sandbox and vice versa.

Provide them as environment variables, or through your agent platform's secret store — never print, log, or commit them.

## Usage

CLI: `bin/prodigi.py` — `prodigi.py METHOD /path [--data '{...}'] [--params '{...}'] [--live]`.
Defaults to the **sandbox** environment (`api.sandbox.prodigi.com`); pass `--live` for production (`api.prodigi.com`).
Examples: `prodigi.py GET /v4.0/Products --params '{"pageSize": 5}'`, `prodigi.py POST /v4.0/Orders --data '{...}' --live`.
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Prodigi or this provider's print API.
2. Restrict authenticated requests to: api.sandbox.prodigi.com, api.prodigi.com.
3. Default to sandbox; never call --live without explicit approval (live orders are produced, shipped, and charged).
4. Do not print, log, or persist raw credentials.
5. A 401 usually means the wrong environment's key — check which of `PRODIGI_API_KEY` / `PRODIGI_API_KEY_LIVE` the call used before assuming a key is dead.
