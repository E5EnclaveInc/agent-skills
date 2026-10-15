---
name: google-ads
description: "Drive a Google Ads account through the Google Ads API: GAQL search, campaign/ad-group/ad/keyword mutations, and ad-strength audits. Use when a task involves Google Ads, Ad Grants, or the Google Ads API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and the GOOGLE_ADS_* credential environment variables (see Credentials)."
metadata:
  version: 1.0.0
---

# Google Ads

Drive a Google Ads account (including Ad Grant accounts) via the Google Ads API: campaign/ad-group/ad/keyword search and mutate, plus ad-strength audits.

## Credentials

All read from the environment — never print, log, or commit them:

- `GOOGLE_ADS_DEVELOPER_TOKEN` — from Ads Manager → Admin → API Center.
- `GOOGLE_ADS_CLIENT_ID` / `GOOGLE_ADS_CLIENT_SECRET` — a Google Cloud OAuth client (Web application type) with the Google Ads API enabled.
- `GOOGLE_ADS_REFRESH_TOKEN` — minted via the account owner's Google OAuth consent flow.
- `GOOGLE_ADS_CUSTOMER_ID` — the Ads customer ID, digits only. An account identifier, not a secret; `--customer-id` overrides it.

The CLI exchanges the refresh token for an access token at oauth2.googleapis.com, then calls googleads.googleapis.com with `Authorization: Bearer` + the `developer-token` header.

`gads.py --setup-check` verifies the credential variables exist (no API call).

## Usage

CLI: `bin/gads.py` — `gads.py [--customer-id ID] [--login-customer-id MGR] METHOD /path [--data '{...}']`.
Examples:
  `gads.py POST /v25/customers/1234567890/googleAds:search --data '{"query":"SELECT campaign.name FROM campaign"}'`
  `gads.py POST /v25/customers/1234567890/googleAds:mutate --data '{"operations":[...]}'`
Paths are appended to https://googleads.googleapis.com. Prints JSON to stdout; exits non-zero with the provider's error message on failure.

Use `--login-customer-id` ONLY when acting through a manager account; accounts with direct access omit it.

## Operating rules

1. Use this skill when the user asks for Google Ads or this provider's API.
2. Restrict authenticated requests to: googleads.googleapis.com, oauth2.googleapis.com.
3. Do not print, log, or persist raw credentials.
4. Mutations (campaign/ad/keyword create, pause, budget changes) are state-moving: narrate before firing on anything irreversible or spend-adjacent. Ad Grant accounts have no spend, but pausing/launching campaigns is still consequential: confirm with the user first.
5. Ad-strength standard ("EXCELLENT" protocol): every responsive search ad composed should target the top strength rating — 15 headlines across 7 intent categories, 4 descriptions ≤90 chars, 6+ sitelinks at account/campaign level. Audit existing ads against it before writing new ones.
6. A 401/403 is a question about the request before it is about the credentials: check the developer token's access level, the OAuth client's project, and that the refresh token hasn't been revoked before re-minting anything.
