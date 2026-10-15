---
name: raisely
description: "Work with the Raisely fundraising API: campaigns, profiles, donations, teams, and registrations. The campaign key is admin-equivalent, so money-moving calls need explicit confirmation. Use when a task involves Raisely or its API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and RAISELY_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Raisely

Work with the Raisely fundraising API (`https://api.raisely.com/v3`).

## Credentials

- `RAISELY_API_KEY` (required) — the per-campaign private key (campaign admin → Settings → Developers / API & Webhooks), sent as `Authorization: Bearer`. The key acts as the organisation's first admin (**ORG_ADMIN**) — it is powerful, guard it accordingly.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## What the API actually is (verified 2026-09)

- **Capabilities:** full CRUD on campaigns, profiles, donations, teams — including creating donations and registering fundraisers (e.g. `POST /v3/campaigns/{uuid}/register`). Unlike read-only fundraising APIs, this API can *write*.
- **Money-moving actions stay gated:** creating donations, issuing refunds, or changing anything financial requires the user's explicit confirmation first. Reads and dry-runs are autonomous.
- **Webhooks:** Raisely supports outbound webhooks (configured in the admin panel). A sound pattern for donation events: webhook → your own endpoint/worker → your database → notify your ops address, with origin checks and rate limiting on the receiver.

Architecture implication: Raisely is a candidate *capture* surface (hosted campaign pages, peer-to-peer fundraising); keep your own wiring *downstream* — webhooks in, API reads for reconciliation.

## Usage

CLI: `bin/raisely.py` — `raisely.py GET /v3/campaigns/{uuid}` / `raisely.py POST /v3/... --data '{...}'`.
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Raisely or this provider's API.
2. Restrict authenticated requests to: api.raisely.com.
3. Do not print, log, or persist raw credentials.
4. The private key is ORG_ADMIN-equivalent: reads are autonomous; anything that moves money or mutates campaign state needs explicit user confirmation.
5. A 401 `invalid token` means the stored key does not match the campaign's current key — re-copy it from the campaign admin (Settings → Developers / API & Webhooks) rather than retrying.
