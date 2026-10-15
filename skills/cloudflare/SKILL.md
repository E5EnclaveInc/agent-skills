---
name: cloudflare
description: "Drive the Cloudflare API v4 from the command line: zones, DNS, Workers, R2 object get/put, and any other endpoint, with scoped-token and legacy global-key auth lanes. Use when a task involves Cloudflare or its API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and CLOUDFLARE_API_TOKEN set in the environment (CLOUDFLARE_EMAIL + CLOUDFLARE_GLOBAL_API_KEY for the global-key lane)."
metadata:
  version: 1.0.0
---

# Cloudflare

Scriptable clients for the Cloudflare API v4 (`https://api.cloudflare.com/client/v4`).

## Credentials

- `CLOUDFLARE_API_TOKEN` (primary) — a scoped API token, sent as `Authorization: Bearer`. Create tokens with only the permissions your task needs (dashboard → My Profile → API Tokens). Used by `cf.py`, `cf_auth.py`, `r2get.py`, `r2put.py`.
- Optional per-scope overrides read by `cf_auth.py`: `CLOUDFLARE_API_TOKEN_D1`, `CLOUDFLARE_API_TOKEN_D1W`, `CLOUDFLARE_API_TOKEN_BOTMGMT`, `CLOUDFLARE_API_TOKEN_EMAIL` — each falls back to `CLOUDFLARE_API_TOKEN`.
- `CLOUDFLARE_EMAIL` + `CLOUDFLARE_GLOBAL_API_KEY` (legacy lane, `cf_global.py` only) — the account's Global API Key, sent as `X-Auth-Email` / `X-Auth-Key`. It opens the whole account; use it only for endpoints that reject scoped tokens.

Provide them as environment variables, or through your agent platform's secret store — never print, log, or commit them. Your account ID is a plain identifier (dashboard → Overview) that several calls take as a path segment or argument, e.g. `cf.py GET /accounts/<account_id>/workers/scripts` — it is not a secret, but it is yours; keep it in your own config, not in shared code.

## Usage

- `bin/cf.py` — general CLI (scoped token): `cf.py METHOD /path [--data '{...}'] [--params '{...}']`. Example: `cf.py GET /zones --params '{"name":"example.com"}'`.
- `bin/cf_global.py` — same interface, Global API Key auth, for the endpoints the scoped token cannot reach.
- `bin/cf_auth.py` — shared helper: `auth_header(scope)` / `apply_auth(req, scope)` for your own scripts, with scopes `default`, `d1`, `d1w`, `botmgmt`, `email`.
- `bin/r2get.py <account_id> <bucket> <key> <out_path>` — download an R2 object; prints its sha256.
- `bin/r2put.py <account_id> <bucket> <key> <local_path> [content_type]` — upload a file to R2; prints its sha256.

All CLIs print JSON to stdout and exit non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Cloudflare or this provider's API.
2. Restrict authenticated requests to: api.cloudflare.com.
3. Do not print, log, or persist raw credentials.
4. Prefer the scoped token; reach for the Global Key lane only when an endpoint rejects scoped tokens, and say so when you do.
5. A 401 or 403 is a question about the request before it is a question about the key: check that the token is set and carries the permission the endpoint needs (scoped tokens fail closed, endpoint by endpoint).

## Secrets Store notes (API shape, learned in production)

- Each account has one `default_secrets_store` (beta). Workers read store secrets via `secrets_store_secret` bindings.
- **Create shape:** `POST /accounts/{id}/secrets_store/stores/{store_id}/secrets` takes a **batch array** `[{"name","value","scopes":["workers"],"comment":"..."}]` — a bare object returns `invalid_json_body`.
- **Binding:** wrangler.toml `[[secrets_store_secrets]]` with `binding`, `store_id`, `secret_name`; the runtime API binding type is `secrets_store_secret` with `name`/`store_id`/`secret_name`; code reads via `await env.BINDING.get()`. Binding names must not collide with existing `secret_text` names.
- **Worker re-upload via API** (when wrangler auth isn't available): snapshot `.../workers/scripts/{name}/settings` first; `PUT` multipart with metadata JSON + script part at `Content-Type: application/javascript+module`; re-supply every binding (D1/queues/vars/secrets-store) — anything omitted is wiped; `secret_text` survives only when omitted entirely.
- Turnstile widget secrets are API-readable: `GET /accounts/{id}/challenges/widgets/{sitekey}` returns `secret` — pipe it straight into the store, never display it.
