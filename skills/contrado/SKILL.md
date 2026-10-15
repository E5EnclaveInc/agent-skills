---
name: contrado
description: "Work with the Contrado Helix print-on-demand API: browse stores and products, map variants, create and track orders. Use when a task involves Contrado, Helix, or print-on-demand fulfilment through Contrado."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and CONTRADO_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Contrado

A thin, scriptable client for the Contrado Helix print-on-demand API (`https://api.contrado.app/helix/v1`).

## Credentials

- `CONTRADO_API_KEY` (required) — Helix API key, sent as the `x-api-key` header.
- `CONTRADO_STORE_ID` (optional) — store scoping, sent as the `X-Store-Id` header.

Provide them as environment variables, or through your agent platform's secret store — never print, log, or commit them.

## Usage

CLI: `bin/contrado.py` — `contrado.py METHOD /path [--data '{...}'] [--params '{...}']`.
Base URL is fixed: `https://api.contrado.app/helix/v1` (no sandbox is publicly documented; credential checks validate credentials only).
Examples: `contrado.py GET /products --params '{"limit": 1}'`, `contrado.py POST /orders --data '{...}'`.
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Auth placement (verified 2026-09-12 from the provider's own plugin source)

The API key goes in the `x-api-key` header (case-insensitive per HTTP), per the official WordPress plugin's `headers()` implementation. Optional sibling headers: `X-Store-Id` (store scoping), `X-Culture-Code` (e.g. `en-US`). An earlier round of 404s turned out to be wrong paths, not auth — `/` and `/products` are not Helix routes.

## Verified contract (2026-09, from the wordpress.org plugin SVN trunk + live probes)

- Base URL: `https://api.contrado.app/helix/v1` (entered by the store owner in plugin settings, not hardcoded — the base was never the failure).
- Test Connection probe (the plugin's own): `GET /stores` → `200 {"success": true, "data": [...]}`.
- Response envelope: JSON with `success` (bool), `data` (payload), `message` (error detail); HTTP ≥400 → error path.
- Read-only GET inventory: `stores/products` (PageNumber/PageSize), `stores/products/{id}`, `stores/products/{id}/option-variants`, `shipping/{culture_code}`, `orders/{id}`, `orders/{id}/shipment/status`, `orders/by-reference/{ref}/status`. Note: `stores/products` on an empty store returns HTTP 200 with `success:false` and message "No Store Products Found , Please check your details or token." — SKU mapping needs products attached in the Contrado dashboard first.
- Webhook auth: NO HMAC signing — shared-secret token as `X-Webhook-Secret` header or `?wh_secret=<secret>` on the callback URL, compared with a timing-safe `hash_equals`.
- Order creation (verified against the plugin's order-sync code): `POST {base}/orders/create`. Full body:
  `{externalReferenceId, recipient, lineItem, totalAmount, currencyCode, forceInsert, cultureCode}`.
  Recipient: `{name, company, address1, address2, city, stateCode, stateName, countryCode, country, postCode, phone, mobile, recipientPhone, email, taxNumber, ssn}` (shipping preferred, billing fallback; full country/state names, not just codes).
  Line item: `{storeProductId (int, from stores/products), externalReferenceId, variantId (string, from stores/products/{id}/option-variants), selectedOptions: [{optionId, optionValueId, optionName, optionValueName}], quantity, price (unit)}`.
  totalAmount = sum(price*quantity), rounded to 2dp. forceInsert: false (block duplicates).
  IMPORTANT: Helix can return HTTP 200 with `success:false` — always check the `success` field, not the status code. Success data: `referenceId`, `status` (or `reference_id`/`orderStatus`).
  Status tracking: `GET orders/by-reference/{ref}/status`, `GET orders/{id}`, `GET orders/{id}/shipment/status`.
  Order flow: `stores/products/{id}` → `stores/products/{id}/option-variants` (variantId + optionId/optionValueId) → `orders/create` → `orders/by-reference/{ref}/status`.

## Operating rules

1. Use this skill when the user asks for Contrado or its Helix print API.
2. Restrict authenticated requests to: api.contrado.app.
3. No sandbox exists publicly — treat every call as production-adjacent. Never POST an order without explicit approval (orders are produced, shipped, and charged).
4. Do not print, log, or persist raw credentials.
