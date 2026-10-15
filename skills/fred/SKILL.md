---
name: fred
description: "Query the FRED (Federal Reserve Bank of St. Louis) economic data API: fetch series observations and metadata — interest rates, inflation, employment, and thousands of other series. Use when a task needs FRED data or mentions FRED series IDs."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and FRED_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# FRED

A thin, scriptable client for the FRED® API (`https://api.stlouisfed.org`) — for example the effective federal funds rate and the target range (series EFFR, DFEDTARL, DFEDTARU).

## Credentials

- `FRED_API_KEY` (required) — free API key from https://fred.stlouisfed.org/docs/api/api_key.html, sent as the `api_key` query parameter (the way the FRED API reads it).

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/fred.py` —
`fred.py observations SERIES_ID [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--limit N] [--sort-order asc|desc]`
`fred.py series SERIES_ID` (metadata).
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for FRED or this provider's API.
2. Restrict authenticated requests to: api.stlouisfed.org.
3. Do not print, log, or persist raw credentials.
4. Respect FRED's rate limit (120 requests/minute): batch and pace calls, and back off on 429s.
5. A 401 or 403 is a question about the request before it is a question about the key: check that `FRED_API_KEY` is set and the series ID is valid first.
