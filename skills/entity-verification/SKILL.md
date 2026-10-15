---
name: entity-verification
description: "Verify a business entity's legal and tax standing: state corporate registry lookup, IRS exempt-organization search, SAM.gov federal registration check (for-profit and nonprofit alike), NY DOS API lane, nonprofit 990 financials via ProPublica + IRS BMF, SEC EDGAR for public companies, OFAC sanctions screening, FEC political vetting, and business-mailbox sweep for filing/IRS correspondence. Produces a per-entity status dossier. Use when onboarding, auditing, vetting, or starting up any company or nonprofit."
license: MIT
compatibility: "Requires Python 3.9+. Most lanes are keyless; the SAM.gov lane needs a SAM.gov API client (SAM_GOV_CLI) and the mailbox lane a mailbox CLI (BIZMAIL_CLI). Bulk datasets are downloaded at runtime into a local cache."
metadata:
  version: 1.0.0
---
# Entity Verification (BizIntel suite)

## Purpose
Confirm what a business legally is right now: active with the state or not, what's filed, officers and registered agent, whether tax-exempt status was granted or is pending, and what the paper trail in the business mailbox shows. Read-only — never files, pays, amends, or contacts anyone.

## Orchestrator
`bin/bizintel.py` runs one entity through every lane and emits a single dossier (JSON + human summary + verification ledger). It imports the five API lanes from `bin/lanes/` (`n990`, `edgar`, `ofac`, `fec`, `nydos`) and reuses two external tools **by reference** (subprocess, never copied): a SAM.gov API client you provide via the `SAM_GOV_CLI` env var (Lane D) and `bin/entity_mail_sweep.py` (Lane C). A failing lane never kills the dossier — its record carries `status: error` with the reason, and the other lanes still complete.

```bash
bin/bizintel.py --name "ACME COMMUNITY FOUNDATION INC" --state FL --type nonprofit --ein <EIN>
bin/bizintel.py --name "TESLA, INC." --type for-profit --ticker TSLA
bin/bizintel.py --name "RIVERBEND COMMUNITY ALLIANCE INC" --lanes n990,ofac,mailbox
bin/bizintel.py --entity-json /tmp/entity.json --out /tmp/dossier.json
```

All lanes share the hardened transport in `bin/bizintel_common.py`: retries with exponential backoff (honoring `Retry-After`), request timeouts, polite minimum request intervals per provider, response caching under `bin/.cache/`, and a declared-contact `User-Agent` where providers require one. No invented numbers anywhere: every claimed fact cites its live source + `retrieved_at` timestamp in the verification ledger.

## Workflow
1. **Collect inputs:** exact legal name, state of formation, entity type (nonprofit / for-profit), optional DBA, known document number (a lead, not a fact).
2. **Lane A — state registry** (live browser task, read-only): spawn with the brief in `assets/browser-brief-template.md`, substituting the entity's details. For Florida use search.sunbiz.org; other states see `references/state-registries.md`. Record: status, document number, date filed / effective date, entity type, registered agent, principal + mailing address, officers/directors with titles, annual report status, EIN if shown.
3. **Lane B — IRS Tax Exempt Organization Search** (same browser task): https://apps.irs.gov/app/eos. Record: appears or not, EIN, determination date, subsection, Publication 78 listing / deductibility code, most recent Form 990 and tax period. Absence is the expected result for a pending application — report it exactly, never as a denial.
4. **Lane C — mailbox sweep:** run `bin/entity_mail_sweep.py --name "LEGAL NAME" [--dba "DBA"] [--doc DOCNUM]`. It searches your business mailbox for state filing confirmations, IRS letters, 1024/1024-A filings, EIN notices, and pay.gov receipts, filtered to the entity. Set `BIZMAIL_CLI` to a mailbox CLI with `search` / `get` subcommands; open the full bodies of the hits that matter with its `get`.
5. **Lane D — SAM.gov federal registration** (API, read-only, no browser): run `$SAM_GOV_CLI GET /entity-information/v3/entities --params '{"legalBusinessName":"LEGAL NAME"}'` (any SAM.gov API client with that CLI shape works; a SAM.gov API key is required). SAM.gov is the federal registry for any organization doing business with the government, so this lane covers for-profit entities that have no IRS exempt-org footprint. Record: UEI, CAGE code, registration status (Active is the minimum for federal awards), activation / expiration / last-update dates, primary NAICS.
6. **Lane E — nonprofit 990s / financials** (API, no key): the `n990` lane queries ProPublica Nonprofit Explorer v2 by EIN (org profile, ruling date, subsection, latest 990 filing metadata) and cross-checks the locally cached IRS Exempt Organizations Business Master File extract by EIN (ruling, subsection, classification, tax period, NTEE) — download the regional extract once per month into `bin/.cache/`, build the sqlite EIN index once (`bmf_ein_index.db`), then lookups are local and instant. ProPublica never 404s on unknown EINs — it returns an "Unknown Organization" stub, so no-record detection reads the body. If the EIN resolves to a different organization name, surface the NAME MISMATCH and do not attribute its numbers to the entity.
7. **Lane F — SEC EDGAR** (API, keyless, declared-contact User-Agent): the `edgar` lane is the for-profit analog of 990s for **public companies**: CIK resolution (explicit CIK → official `company_tickers.json` → legal-name token match → `efts.sec.gov` full-text fallback), submissions JSON (latest filings: form, accession, dates), XBRL `companyfacts` (headline us-gaap datapoints), SIC, state of incorporation, addresses. Name matching requires whole-word token subsets — substring matches cause silent misattribution (caught live: "acme widgets" → CME GROUP INC). Skip this lane for private entities; `no_record` is normal there.
8. **Lane G — OFAC sanctions screening** (bulk CSV, no key): the `ofac` lane fetches the SDN bulk file from the current OFAC sanctions-list-service host once, caches it in `bin/.cache/` with a weekly refresh floor, and screens the entity's name locally. Returns `no_match` or `candidate_match` — a candidate is a flag for human review, never a positive assertion. Note the old `sanctionssearch.ofac.treas.gov/.../SDN.CSV` endpoint is dead (HTTP 404 as of 2026-09-20); the module knows the current host.
9. **Lane H — FEC political vetting** (OpenFEC, free; `DEMO_KEY` works at ~40/hr for one-off checks, set `OPENFEC_API_KEY` for the free personal key at 1,000/hr): the `fec` lane searches committees by name and returns committee ID, type, designation, party, treasurer, first/last filing dates. Scope this lane to political/527-adjacent vetting — a hit doesn't make the entity political, a miss doesn't clear it. Federal law restricts commercial use of contributor data; review terms before any bulk use.
10. **Lane I — NY DOS API** (keyless Socrata): the `nydos` lane queries the live NY Department of State dataset `n9v6-gdp6` ("Active Corporations: Beginning 1800", 4.28M rows, refreshed same-day as of 2026-09-20) by exact DOS ID, exact name, or fuzzy name — it covers for-profit corporations, LLCs, LPs, LLPs, and not-for-profits. Dataset holds **active** entities only; for inactive/suspended/dissolved entities or assumed-name (DBA) certificate details, escalate to the browser lane using `assets/ny-browser-brief.md`.
11. **Reconcile and report** per the Output Contract. Flag gaps explicitly: missing EIN, DBA not registered with the state, typos in state records, document numbers in the user's files that don't match the registry.

## Fallback cascade
Per lane, in order: **live API → cached response (within TTL) → browser lane (where one exists: Lane A state registries, Lane B TEOS, Lane I NY DBA/inactive) → parked with a dated note.** Parking is a result, not a failure: record what was tried, the exact error/evidence, and what would unpark it. Never grind a failing endpoint more than the lane's retry budget; never route around a CAPTCHA.

## Output Contract
One status block per entity, plain language, phone-screenable: legal name | state status | doc # | filed / effective | type | EIN (or NONE) | registered agent | officers | annual reports | IRS status (granted with date + subsection, pending, or n/a) | **990s (ruling date, subsection, latest 990 period/form — nonprofit lane)** | **EDGAR (CIK, SIC, latest filings — public-company lane)** | **sanctions (no_match / candidate_match)** | **FEC (committee hits)** | **NY DOS (status, DOS ID, entity type)** | SAM.gov (UEI, CAGE, status, activated / expires, primary NAICS — for-profit and nonprofit alike) | mailbox evidence (dates + senders) | gaps and flags. End with what "starting" the entity still requires. `bin/bizintel.py` emits the full machine-readable dossier plus a verification ledger (lane, source, retrieved_at, status for every lane run).

## Operating Rules
1. Read-only: no forms, no filings, no payments, no amendments, no outside contact — ever.
2. A document number found in the user's files is a lead, not a fact: verify it with a registry document-number lookup. (A document number found in the user's files once turned out to belong to a different company entirely.)
3. EIN applications require the responsible party's SSN — that's the user's personal step. Never attempt it on their behalf.
4. Pending IRS applications do not appear in TEOS. Say "pending — not listed," never imply a grant or a denial.
5. Record the source URL of every registry and IRS detail page; the user may need them later.
6. If a CAPTCHA appears in the browser lane, park and hand back — never route around it.
7. SAM.gov name searches are exact-ish: one looser retry on zero results, then park and document. A `CAGEREVIEW@DLA.MIL` "verification needed" email verifies the UEI ↔ legal-name ↔ address triple — it is a verification *request*, not a confirmation. The confirmation is an Active SAM.gov record with the CAGE code on it.
8. Names travel with their cited sources and are never relabeled. The `n990` lane surfaces a NAME MISMATCH when an EIN resolves to a different organization — it never attributes another org's numbers to the entity. Never conflate similarly named organizations (e.g. a national foundation and an independent local chapter that shares part of its name) anywhere in outputs.
9. An OFAC `candidate_match` is a flag for human review, never a positive sanction assertion.
10. The API lane is tried before the browser lane whenever both exist (NY DOS). Bulk-first, live-cross-checked: download bulk extracts once (EO BMF monthly, OFAC SDN weekly), build the local index once, serve lookups locally; use the live API as the cross-check. Rate limits are respected by construction (polite intervals, `Retry-After` honored, caches keyed per query).
11. No API enters a lane without a live verified response this session — verify before you spec, measured not assumed. Each lane module's docstring carries its live test record.
