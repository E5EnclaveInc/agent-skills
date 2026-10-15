---
name: stripe
description: "Call the Stripe API from the command line: account, payment links, prices, products, charges, and any /v1 endpoint, with automatic form-encoding of request bodies. Use when a task involves Stripe or its API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and STRIPE_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Stripe

A thin, scriptable client for the Stripe API (`https://api.stripe.com`).

## Credentials

- `STRIPE_API_KEY` (required) — a Stripe secret key, sent as `Authorization: Bearer`. Prefer a **restricted key** with only the scopes the task needs.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/stripe.py` — `stripe.py METHOD /v1/path [--data '{...}'] [--params '{...}']`.
The Stripe API takes **form-encoded** bodies; `--data` accepts a JSON object that is flattened to Stripe's bracket notation automatically.

Examples:
- `stripe.py GET /v1/account`
- `stripe.py GET /v1/payment_links --params '{"limit":"3"}'`
- `stripe.py POST /v1/payment_links --data '{"line_items":[{"price_data":{"currency":"usd","unit_amount":2500,"recurring":{"interval":"month"},"product_data":{"name":"Example Org — Supporter Monthly $25"}},"quantity":1}],"metadata":{"plan":"supporter_monthly"}}'`

Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Stripe or this provider's API.
2. Restrict authenticated requests to: api.stripe.com.
3. Do not print, log, or persist raw credentials.
4. Creating payment links, prices, or products is configuration, not a charge — but anything that moves money (refunds, payouts, transfers) needs the user's explicit confirmation first.
5. A 401 or 403 is a question about the request before it is a question about the key: check that `STRIPE_API_KEY` is set and the (restricted) key carries the needed scope first.
