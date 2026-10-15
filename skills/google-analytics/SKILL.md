---
name: google-analytics
description: "Use Google Analytics 4 when a user asks for GA4, Analytics, or measurement: onboard properties and web data streams via the Admin API, link Google Ads, wire key events, and verify data flow per stream with the Data API. Covers OAuth scope separation between the Admin and Data APIs and the scope-403 diagnosis."
license: MIT
compatibility: "Requires Python 3.10+ (stdlib only) and OAuth client credentials plus a refresh token supplied through environment variables (see SKILL.md)."
metadata:
  version: 1.0.0
---

# Google Analytics 4

## Purpose
Manage a GA4 estate via the Analytics Admin API and Data API: create properties and web data streams, link Google Ads, wire key events, and verify measurement.

## Tooling
CLI: `bin/ga_onboard.py` — onboard a new site to GA4 via API.

Usage:
```
ga_onboard.py "Site Name" https://example.com --account accounts/123456789 [--link-ads --ads-customer 1234567890] [--time-zone America/New_York] [--currency USD]
```

Creates a property under the given Analytics account plus a web data stream for the site. With `--link-ads`, links the property to the given Google Ads customer (the API takes the bare ten-digit customer ID).

## Auth
All credentials come from the environment; nothing is read from disk and nothing is printed or logged:

| Variable | Meaning |
|---|---|
| `GOOGLE_OAUTH_CLIENT_ID` | OAuth client ID (Web or Desktop app) |
| `GOOGLE_OAUTH_CLIENT_SECRET` | OAuth client secret |
| `GOOGLE_ANALYTICS_REFRESH_TOKEN` | Refresh token for the API work (scope below) |
| `GOOGLE_ADS_CUSTOMER_ID` | Optional default for `--ads-customer` |

The Analytics Admin API must be enabled on the Google Cloud project that owns the OAuth client.

## Auth scopes — the expensive lesson
- An `analytics.edit` refresh token covers the **Admin API** (create properties/streams/secrets, link Ads).
- It does **NOT** cover the **Data API** (`runRealtimeReport`, `runReport`): those return HTTP 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT`. The Data API needs `https://www.googleapis.com/auth/analytics.readonly` — keep a **separate readonly refresh token** for Data API calls; never reuse the edit-scoped token there.
- A 403 from the Data API is a **scope problem, not an enablement or property-access problem** — unless the reason is `SERVICE_DISABLED`, which means the Data API itself isn't enabled on the Cloud project (enable it in the console; reversible). Do not re-diagnose a scope 403 as anything else.

## Operating Rules
1. Use this skill when the user asks for GA4, Analytics, or measurement setup.
2. Restrict authenticated requests to: analyticsadmin.googleapis.com, analyticsdata.googleapis.com, oauth2.googleapis.com.
3. Do not print, log, or persist raw credentials or refresh tokens.
4. Decide the property layout deliberately: additional sites usually become additional data streams on the organization's canonical property; create a new property only when the user explicitly asks.
5. Verify tags are live in the served HTML before claiming measurement success.
6. **Never infer per-stream event success from aggregate `page_view`.** Prove genuine events per stream via the Data API or Realtime/DebugView. "Events flowing" means named events on the named stream, not a property-wide page_view count.
7. Keep GA4 `purchase` as a Secondary conversion in Google Ads until verified purchase events exist in GA4 — promoting it earlier inflates Smart Bidding on zero data.
8. GA4 Measurement Protocol secrets: name them after their consumer, create them via the Admin API, and audit for duplicates after any partially-failed run (a retry can mint a second secret). Never print or save secret values.
