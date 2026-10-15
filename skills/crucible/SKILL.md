---
name: crucible
description: "Use Crucible when a sourced deliverable must be proven before publishing: door-check every URL, mechanically verify file-size and PDF page-count claims, ground dollar/date/attribution figures against live sources, and emit a gated Verification Ledger."
license: MIT
metadata:
  version: 1.0.0
---
# Crucible Verification Gate

The portable verification gate: fire raw source material at the gate until only verified truth survives. Use it before publishing or enshrining ANY sourced deliverable — an archive, catalogue, research report, or page with external links and figures — and to vet untrusted source material before incorporating it.

This is the executable form of a door-verification doctrine: nothing ships on confidence — only on checks.

> Core rule: **verify against the source, never against the author's (or a sub-agent's) confidence.** Quality equals the checklist, not the model's mood.

## The loop
1. **SPEC** — list the source(s): an HTML file, a URL list, and/or a `claims.json` of figures to check.
2. **LINK GATE** — `verify_link_gate.py` probes every URL for liveness + real content.
3. **FIGURE GATE (mechanical)** — `verify_figure_check.py` settles size/page-count claims against the cited file.
4. **FIGURE GATE (grounded)** — `verify_figure_exa.py` checks dollar/date/attribution claims against live sources via Exa.
5. **LEDGER** — `verify_ledger.py` merges every result into `ledger.json` + a styled `ledger.html`.
6. **PROMOTE / REJECT** — PASS/MATCH/SUPPORTED ship. Anything BROKEN/MISMATCH/CONTRADICTED is rejected, the reason attached, and requeued (fix the figure, replace the link) — or cut. NEEDS_EYES / NEEDS_SOURCE_CHECK / UNVERIFIABLE await a human/agent decision.

## Status taxonomy
- **PASS / MATCH / SUPPORTED** — verified; eligible to ship.
- **BROKEN / MISMATCH / CONTRADICTED / ERROR** — failed; reject + requeue (gate is not clean).
- **NEEDS_EYES** — a 200 that reads like an error/login/parked page, OR a 401/403 that is likely a datacenter bot-block on a real page (verify in a real browser; legitimate to keep if browser-confirmed).
- **UNVERIFIABLE** — could not settle mechanically (e.g. no Content-Length and file too large to measure).
- **NEEDS_SOURCE_CHECK** — not mechanically checkable (a dollar amount, date, attribution); hand to `verify_figure_exa.py` or agent judgment.

## Scripts (`bin/`)

### 1. verify_link_gate.py (no credentials)
```
python3 bin/verify_link_gate.py page.html                 # extract + probe every http(s) link
python3 bin/verify_link_gate.py --urls urls.txt           # one URL per line
python3 bin/verify_link_gate.py --url https://a https://b
python3 bin/verify_link_gate.py page.html --out link_ledger.json
```
Catches dead links (4xx/5xx), **soft-404s where a `.pdf` URL actually returns an HTML shell**, parked/login/error pages, and bot-blocks (flagged NEEDS_EYES, not falsely killed). Skips Google-Fonts noise. Exit code 2 if any BROKEN.

### 2. verify_figure_check.py (no credentials; uses poppler `pdfinfo`, falls back to `pypdf`)
```
python3 bin/verify_figure_check.py --claims claims.json
python3 bin/verify_figure_check.py --from-html page.html
python3 bin/verify_figure_check.py --claims claims.json --tol 0.18
```
`claims.json` schema:
```json
[
  {"id":"ca-full","type":"filesize","url":"https://.../full.pdf","expected":"86 MB"},
  {"id":"fulton","type":"pagecount","url":"https://.../report.pdf","expected":"636"},
  {"id":"citi","type":"figure","claim":"$16T lost GDP 2000-2020","source":"Citi GPS 2020"}
]
```
- `filesize` → compares the server's Content-Length to the claim within `--tol` (default 18%); streams the file (capped ~60 MB) if Content-Length is absent.
- `pagecount` → downloads the PDF (capped ~170 MB) and counts pages via `pdfinfo`/`pypdf`.
- `figure` (anything else) → `NEEDS_SOURCE_CHECK`. Exit code 2 if any MISMATCH.

### 3. verify_figure_exa.py (requires EXA_API_KEY)
```
python3 bin/verify_figure_exa.py --query "Is the $51T figure from the SF Fed (Daly et al., 2021)?" --expected "SF Federal Reserve, 2021"
python3 bin/verify_figure_exa.py --claims claims.json
```
POSTs to `https://api.exa.ai/answer` (header `x-api-key`) with a structured output schema returning `{supported, found_value, confidence, note}` plus citations. Without a key it exits gracefully telling you to set it.

### 4. verify_ledger.py (no credentials)
```
python3 bin/verify_ledger.py link_ledger.json figure_ledger.json exa_ledger.json \
    --title "<Project> — Verification Ledger" --out ledger
```
Merges all entries, tallies by status, prints the verdict (**GATE CLEAN** vs **N FAILED — reject + requeue**), and renders the ledger as a publishable HTML report. Exit code 2 if anything failed.

## Doctrine baked in
- **Verify against the source, never the author's confidence.**
- **Empirical, not comfort-based, exclusion.** Keep what survives verification; exclude only what fails the evidence test — not what is merely unfavorable.
- **A failure is rejected, not flagged-for-later.** Attach the reason, requeue, re-run the gate. Ship only when nothing fails.
- **The ledger is append-only.** Keep `ledger.json` as the receipt of what was checked and what was caught.

## Dependencies
- `requests` auto-installed by the scripts if missing. `verify_figure_check.py` uses poppler `pdfinfo`, falls back to `pypdf` (`pip install pypdf`).
- Scripts send a real browser User-Agent (many sites 403 a default Python UA — that is a bot-block, not a dead link).
- Python 3.9-compatible.
