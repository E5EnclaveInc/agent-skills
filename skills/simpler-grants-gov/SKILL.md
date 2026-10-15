---
name: simpler-grants-gov
description: "Search and fetch U.S. federal grant opportunities through the Simpler.Grants.gov REST API, plus agency search. Use when a task involves federal grant discovery, funding opportunities, or the Simpler.Grants.gov API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and SIMPLER_GRANTS_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Simpler.Grants.gov

A purpose-built client for the Simpler.Grants.gov REST API (`https://api.simpler.grants.gov`).

## Credentials

- `SIMPLER_GRANTS_API_KEY` (required) — API key from Simpler.Grants.gov, sent as the `X-API-Key` header.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/sg.py` —

- `sg.py health` — service health check.
- `sg.py search --query "nonprofit" [--page 1] [--page-size 25] [--filters '{"opportunity_status":{"one_of":["posted"]}}']` — POST /v1/opportunities/search.
- `sg.py get <legacy_opportunity_id>` — fetch one opportunity.
- `sg.py agencies [--query "health"] [--page-size 25] [--data '{...}']` — POST /v1/agencies/search.

Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Simpler.Grants.gov or this provider's API.
2. Restrict authenticated requests to: api.simpler.grants.gov.
3. Do not print, log, or persist raw credentials.
4. A 401 or 403 is a question about the request before it is a question about the key: check that `SIMPLER_GRANTS_API_KEY` is set first.
