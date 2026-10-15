---
name: sam-gov
description: "Query SAM.gov entity registrations (UEI, CAGE, status, NAICS, socioeconomic flags) and search federal contract opportunities. Use when a task asks about SAM.gov, entity standing, or federal opportunities."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and SAM_GOV_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# SAM.gov

Query SAM.gov entity registrations and federal contract opportunities. Primary jobs: (1) snapshot an entity's grant/contract readiness (registration status, UEI, CAGE, NAICS, SBA flags); (2) search posted federal opportunities.

## Credentials

- `SAM_GOV_API_KEY` (required) — an api.data.gov API key, sent as the `X-Api-Key` header.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/sam.py` — thin passthrough. Paths append to `https://api.sam.gov`.

```bash
# Entity lookup by legal name (fictional example)
bin/sam.py GET /entity-information/v3/entities \
  --params '{"legalBusinessName":"EXAMPLE LOGISTICS LLC"}'

# Entity lookup by UEI (fictional example — not a real registration)
bin/sam.py GET /entity-information/v3/entities \
  --params '{"ueiSAM":"EXAMPLEUEI12"}'

# Opportunity search (postedFrom/postedTo are mandatory)
bin/sam.py GET /opportunities/v2/search \
  --params '{"postedFrom":"01/01/2026","postedTo":"02/01/2026","limit":5}'
```

Key response fields: `entityData[].entityRegistration` (legalBusinessName, ueiSAM, cageCode, registrationStatus, activationDate, lastUpdateDate), `assertions.goodsAndServices` (primaryNaics, naicsList), `pointsOfContact`.
Grant-readiness rule: `registrationStatus == "Active"` is the minimum for federal awards; expired or missing registrations block submissions.

## Operating rules

1. Use this skill when the user asks for SAM.gov, entity standing, or federal opportunities, or when a filing checklist needs an entity readiness check.
2. Restrict authenticated requests to: api.sam.gov.
3. Do not print, log, or persist raw credentials.
4. A 401 or 403 is a question about the request before it is a question about the key: check that `SAM_GOV_API_KEY` is set and valid for api.data.gov first.
5. Name searches are exact-ish: a zero-result lookup gets one looser retry, then park-and-document (don't grind).
