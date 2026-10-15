---
name: zeffy
description: "Read the Zeffy API (read-only): payments, contacts, and campaigns with cursor pagination, for reconciliation and reporting. Use when a task involves Zeffy or its API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and ZEFFY_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Zeffy

Read the Zeffy API (`https://api.zeffy.com/api/v1`) — payments, contacts, campaigns — for reconciliation and reporting.

## Credentials

- `ZEFFY_API_KEY` (required) — the per-organization API key (Zeffy → Settings → Integrations), sent as `Authorization: Bearer`.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## What the API actually is (verified 2026-09)

- **Read-only:** `GET /payments`, `GET /contacts`, `GET /campaigns` (cursor-based pagination: `has_more`, `next_cursor`). You can pull data out; you **cannot** create donations, contacts, or campaigns through the API.
- **Rate limit:** 100 requests/minute per key (HTTP 429 on exceed). HTTPS only.
- **Webhooks:** outbound POSTs to a configured URL when a payment completes (also on contact/campaign changes). This is the real-time path — put the receiver on infrastructure you own, verify the webhook signature per Zeffy's docs before trusting any payload, and apply origin checks + rate limiting before notifying your ops address.

Architecture implication: donation *capture* stays on Zeffy's hosted/embed form (their checkout, their PCI scope, $0 fees). Your wiring lives *downstream*: webhooks → your receiver → your records, plus read-API reconciliation.

## Usage

CLI: `bin/zeffy.py` — `zeffy.py GET /v1/payments [--params '{...}']`.
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Zeffy or this provider's API.
2. Restrict authenticated requests to: api.zeffy.com.
3. Do not print, log, or persist raw credentials.
4. The API is read-only: never attempt to POST a donation through it. Capture happens on Zeffy's form; your side receives via webhooks.
5. A 401 means the key is wrong, revoked, or for a different organization — re-issue it under Settings → Integrations.
