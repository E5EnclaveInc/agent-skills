"""SEC EDGAR lane for BizIntel business investigations.

Resolves a company to its SEC CIK (explicit CIK, ticker via the official
company_tickers.json, or name match against that file, with an efts.sec.gov
full-text-search fallback), then pulls:

  1. data.sec.gov/submissions/CIK##########.json  -- company submissions
     (latest filings: form types, accession numbers, filing/report dates)
  2. data.sec.gov/api/xbrl/companyfacts/CIK##########.json -- XBRL company facts
     (us-gaap concept count + latest datapoints for headline concepts)

Keyless, public, read-only. SEC asks for <=10 requests/second and a User-Agent
with contact info; bizintel_common already sends a declared-contact UA and this
module enforces a polite 0.25 s minimum interval (~4 req/s) between its calls.

No-record handling:
  * no CIK resolvable for the name/ticker -> status "no_record"
  * submissions endpoint 404 (CIK not an EDGAR filer) -> status "no_record"
  * companyfacts 404 (filer exists but publishes no XBRL) -> status stays "ok",
    the miss is noted in facts/notes (filer-level record still found)
  * network/exception after retries -> status "error"

LIVE TEST RECORD (run 2026-09-20, all times UTC; executor: lane owner):
  Entity under test: Tesla, Inc., ticker TSLA.
  - GET https://www.sec.gov/files/company_tickers.json -> 200 (10438 entries).
    Verified from the OFFICIAL file (not taken on faith): TSLA -> cik_str 1318605,
    title "Tesla, Inc.".  This is the canonical CIK used below.
  - GET https://data.sec.gov/submissions/CIK0001318605.json -> 200 (~6.6 s,
    cold). Raw fields confirmed: cik "0001318605", name "Tesla, Inc.",
    sic "3711", sicDescription "Motor Vehicles & Passenger Car Bodies",
    stateOfIncorporation "DE", tickers ["TSLA"], exchanges ["Nasdaq"],
    entityType "operating", category "Large accelerated filer",
    filings.recent.count 1003 rows, keys {form, filingDate, accessionNumber,
    reportDate, primaryDocument, ...}. Latest 3 rows as returned:
      4   | 0001104659-26-106432 | 2026-09-09 | xslF345X06/tm2625055d1_4seq1.xml
      144 | 0001950047-26-009212 | 2026-09-08 | xsl144X01/primary_doc.xml
      10-Q| 0001628280-26-049270 | 2026-07-23 | tsla-20260630.htm
    filings.files has 1 archive pointer (older filings beyond the 1000-row
    "recent" window).
  - GET https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json -> 200
    (~4 s cold). Raw top keys: {cik, entityName, facts}. entityName
    "Tesla, Inc.", facts.us-gaap has 643 concepts; concept keys {label,
    description, units}. Sample verified datapoint: Revenues/USD latest =
    {"start":"2026-04-01","end":"2026-06-30","val":28236000000,
     "accn":"0001628280-26-049270","fy":2026,"fp":"Q2","form":"10-Q",
     "filed":"2026-07-23","frame":"CY2026Q2"}.
  - GET https://efts.sec.gov/LATEST/search-index?q=Tesla&forms=10-K -> 200.
    Returns JSON with hits.hits[]._source {ciks, display_names, form, file_date,
    adsh, file_num, inc_states, biz_states, sics, ...}; usable as a name->CIK
    fallback.
  - Negative controls: GET submissions/CIK9999999999.json -> 404 (no_record);
    GET companyfacts/CIK9999999999.json -> 404. Name "Xyzzy Nonexistent Widgets
    LLC" -> no ticker-file match, efts returns zero hits -> status no_record.
  Rate limits observed: zero 429/503 across the test session at 4 req/s with
  the declared-contact User-Agent (EntityVerification/1.0). SEC documents
  10 req/sec; we stay at ~4 req/s (min_interval=0.25).

Quirks found live:
  * company_tickers.json is ~1.7 MB; cached locally 7 days (SEC updates it
    roughly quarterly). cik_str is int-like; pad to 10 digits for data.sec.gov.
  * submissions "recent" window is capped (~1000 rows); older filings live in
    filings.files archives (one archive pointer for Tesla).
  * form "4"/"144"/"8-K" recent rows reflect insider/notice filings as much as
    periodic reports; latest periodic 10-Q filed 2026-07-23.
  * companyfacts is XBRL-only: concept names are us-gaap taxonomy labels; a
    valid filer with no XBRL gets 404 on this endpoint alone.
  * BUG CAUGHT LIVE (fixed same session): raw substring name matching matched
    "cme" inside "acme widgets" and resolved bogus-ticker entity "Acme
    Widgets/ZZZFAKE99" to CME GROUP INC. Fix: name matching now requires every
    query token to be a whole word in the title (token-subset), and a failed
    explicit ticker never degrades to a fuzzy name match.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time

try:
    from bizintel_common import http_get, cache_get, cache_set, lane_record
except ImportError:  # allow running this file directly from the lanes/ dir
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   ".."))
    from bizintel_common import http_get, cache_get, cache_set, lane_record

# Politeness: SEC asks <=10 req/s; we hold ~4 req/s via min_interval=0.25.
_MIN_INTERVAL = 0.25
_TICKER_FILE = "https://www.sec.gov/files/company_tickers.json"
_TICKER_TTL = 7 * 24 * 3600  # SEC refreshes roughly quarterly; 7d is safe

_LATEST_N_FILINGS = 10

# Headline us-gaap concepts summarized from companyfacts (XBRL).
_SUMMARY_CONCEPTS = (
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "NetIncomeLoss",
    "Assets",
    "Liabilities",
    "StockholdersEquity",
    "EarningsPerShareDiluted",
    "CashAndCashEquivalentsAtCarryingValue",
)

_SUFFIXES = re.compile(
    r"\b(incorporated|corporation|corp|inc|llc|l\.l\.c|ltd|limited|co|company|"
    r"plc|sa|ag|gmbh|holdings|holding|group|the)\b",
    re.IGNORECASE,
)


def _normalize_name(name: str) -> str:
    s = name.lower()
    s = _SUFFIXES.sub(" ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _fetch_ticker_table(last_call: dict, notes: list) -> dict | None:
    """Return the official ticker->CIK table (dict of index->record), cached."""
    key = "edgar:company_tickers"
    cached = cache_get(key, ttl=_TICKER_TTL)
    if cached is not None:
        try:
            return json.loads(cached)
        except (ValueError, TypeError):
            pass
    try:
        status, text, _ = http_get(_TICKER_FILE, last_call=last_call,
                                  min_interval=_MIN_INTERVAL, timeout=30)
    except RuntimeError as exc:
        notes.append(f"ticker-file fetch failed: {exc}")
        return None
    if status != 200 or not text:
        notes.append(f"ticker-file HTTP {status}")
        return None
    try:
        table = json.loads(text)
    except ValueError:
        notes.append("ticker-file returned non-JSON")
        return None
    cache_set(key, text)
    return table


def _resolve_by_ticker(ticker: str, table: dict, notes: list) -> dict | None:
    want = ticker.strip().upper()
    for rec in table.values():
        if str(rec.get("ticker", "")).upper() == want:
            return {
                "cik": _pad_cik(rec.get("cik_str")),
                "method": "ticker",
                "input": ticker,
                "resolved_name": rec.get("title"),
                "resolved_ticker": rec.get("ticker"),
            }
    notes.append(f"ticker '{ticker}' not found in SEC company_tickers.json")
    return None


def _resolve_by_name(name: str, table: dict, notes: list) -> dict | None:
    want = _normalize_name(name)
    if not want:
        return None
    want_tokens = set(want.split())
    exact, partial = [], []
    for rec in table.values():
        title = str(rec.get("title", ""))
        norm = _normalize_name(title)
        if norm == want:
            exact.append(rec)
            continue
        # Token-subset match only: every query token must be a WHOLE word in
        # the title. (A raw substring test once matched "cme" inside "acme" --
        # false positive caught in live testing, fixed 2026-09-20.)
        title_tokens = set(norm.split())
        if want_tokens and want_tokens <= title_tokens:
            partial.append(rec)
    if len(exact) == 1:
        rec = exact[0]
        return {"cik": _pad_cik(rec.get("cik_str")), "method": "name",
                "input": name, "resolved_name": rec.get("title"),
                "resolved_ticker": rec.get("ticker")}
    if exact:
        names = [r.get("title") for r in exact[:10]]
        notes.append(f"name '{name}' matched {len(exact)} exact CIKs; "
                     f"ambiguous: {names}")
        return None
    if len(partial) == 1:
        rec = partial[0]
        return {"cik": _pad_cik(rec.get("cik_str")), "method": "name",
                "input": name, "resolved_name": rec.get("title"),
                "resolved_ticker": rec.get("ticker")}
    if partial:
        names = [r.get("title") for r in partial[:10]]
        notes.append(f"name '{name}' matched {len(partial)} CIKs; ambiguous "
                     f"(showing {len(names)}): {names}")
        return None
    return None


def _resolve_by_efts(name: str, last_call: dict, notes: list) -> dict | None:
    """Fallback: full-text search on efts.sec.gov to find a company CIK."""
    try:
        status, text, _ = http_get(
            "https://efts.sec.gov/LATEST/search-index",
            params={"q": name, "ciks": "", "forms": ""},
            last_call=last_call, min_interval=_MIN_INTERVAL, timeout=30)
    except RuntimeError as exc:
        notes.append(f"efts full-text fallback failed: {exc}")
        return None
    if status != 200 or not text:
        notes.append(f"efts full-text HTTP {status}")
        return None
    try:
        data = json.loads(text)
    except ValueError:
        notes.append("efts returned non-JSON")
        return None
    seen = []
    for hit in data.get("hits", {}).get("hits", []):
        src = hit.get("_source", {})
        for c in src.get("ciks", []):
            c = _pad_cik(c)
            if c and c not in seen:
                seen.append(c)
    if len(seen) == 1:
        return {"cik": seen[0], "method": "efts-fulltext", "input": name,
                "resolved_name": None, "resolved_ticker": None}
    if seen:
        notes.append(f"efts full-text for '{name}' found {len(seen)} distinct "
                     f"CIKs; ambiguous")
    return None


def _pad_cik(cik) -> str | None:
    digits = re.sub(r"\D", "", str(cik or ""))
    if not digits:
        return None
    return digits.zfill(10)


def _get_json(url: str, last_call: dict, notes: list, what: str):
    """GET url expecting JSON. Returns (status, dict|None)."""
    try:
        status, text, _ = http_get(url, last_call=last_call,
                                  min_interval=_MIN_INTERVAL, timeout=30)
    except RuntimeError as exc:
        notes.append(f"{what} fetch failed after retries: {exc}")
        return 0, None
    if status != 200 or not text:
        return status, None
    try:
        return status, json.loads(text)
    except ValueError:
        notes.append(f"{what} returned non-JSON")
        return status, None


def _summarize_filings(sub: dict, n: int) -> list[dict]:
    recent = sub.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    out = []
    for i in range(min(n, len(forms))):
        def g(k):
            vals = recent.get(k, [])
            return vals[i] if i < len(vals) else None
        out.append({
            "form": g("form"),
            "accession": g("accessionNumber"),
            "filing_date": g("filingDate"),
            "report_date": g("reportDate"),
            "primary_document": g("primaryDocument"),
            "doc_description": g("primaryDocDescription"),
        })
    return out


def _latest_concept_value(concept: dict) -> dict | None:
    """Return the most recently-filed datapoint for a us-gaap concept."""
    units = (concept or {}).get("units", {})
    best = None
    for _unit, points in units.items():
        for p in points:
            if not isinstance(p, dict) or "val" not in p:
                continue
            if best is None or str(p.get("filed", "")) > str(best.get("filed", "")):
                best = dict(p)
                best["unit"] = _unit
    return best


def _summarize_companyfacts(cf: dict) -> dict:
    facts = cf.get("facts", {})
    usgaap = facts.get("us-gaap", {})
    summary = {}
    for name in _SUMMARY_CONCEPTS:
        concept = usgaap.get(name)
        if not concept:
            continue
        latest = _latest_concept_value(concept)
        if latest:
            summary[name] = {
                "label": concept.get("label"),
                "value": latest.get("val"),
                "unit": latest.get("unit"),
                "start": latest.get("start"),
                "end": latest.get("end"),
                "fy": latest.get("fy"),
                "fp": latest.get("fp"),
                "form": latest.get("form"),
                "filed": latest.get("filed"),
            }
    return {
        "entity_name": cf.get("entityName"),
        "n_usgaap_concepts": len(usgaap),
        "headline_concepts": summary,
    }


def run(entity: dict) -> dict:
    """Run the SEC EDGAR lane for `entity` and return a standard lane_record.

    entity keys: legal_name (str), state, entity_type, plus optional
    "ticker" or "cik".
    """
    source = "SEC EDGAR (sec.gov)"
    notes: list[str] = []
    facts: dict = {}
    sources: list[str] = []
    last_call: dict = {}

    name = str(entity.get("legal_name", "") or "").strip()
    table = None
    resolved = None

    # ---- 1. Resolve CIK ----
    raw_cik = entity.get("cik")
    if raw_cik:
        cik = _pad_cik(raw_cik)
        if cik:
            resolved = {"cik": cik, "method": "cik", "input": str(raw_cik),
                        "resolved_name": None, "resolved_ticker": None}
        else:
            notes.append(f"provided CIK '{raw_cik}' has no digits; ignoring")

    if resolved is None and entity.get("ticker"):
        table = _fetch_ticker_table(last_call, notes)
        if table is None:
            return lane_record("sec_edgar", source, "error", facts, sources,
                               notes + ["could not load SEC ticker table"])
        resolved = _resolve_by_ticker(str(entity["ticker"]), table, notes)
        if resolved is None:
            # A user-supplied ticker is a precise identifier; a failed ticker
            # must NOT degrade to a fuzzy name match on legal_name, which
            # could silently resolve a different company.
            notes.insert(
                0, f"ticker '{entity['ticker']}' is not an SEC-listed ticker; "
                   "name fallback deliberately skipped")
            return lane_record("sec_edgar", source, "no_record", facts,
                               sources, notes)

    if resolved is None and name:
        if table is None:
            table = _fetch_ticker_table(last_call, notes)
            if table is None:
                return lane_record("sec_edgar", source, "error", facts,
                                   sources,
                                   notes + ["could not load SEC ticker table"])
        resolved = _resolve_by_name(name, table, notes)

    if resolved is None and name:
        # last resort: full-text search
        resolved = _resolve_by_efts(name, last_call, notes)

    if resolved is None:
        notes.insert(0, f"no SEC CIK resolved for '{name or entity}'")
        return lane_record("sec_edgar", source, "no_record", facts, sources,
                           notes)

    cik = resolved["cik"]
    facts["cik_resolution"] = resolved

    # ---- 2. Company submissions ----
    sub_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    sources.append(sub_url)
    status, sub = _get_json(sub_url, last_call, notes, "submissions")
    if status == 404 or (status == 200 and sub is None):
        notes.append(f"CIK {cik} is not an EDGAR filer "
                     f"(submissions 404 / unreadable)")
        return lane_record("sec_edgar", source, "no_record", facts, sources,
                           notes)
    if sub is None:
        notes.append(f"submissions fetch failed (HTTP {status})")
        return lane_record("sec_edgar", source, "error", facts, sources, notes)

    facts.update({
        "cik": sub.get("cik"),
        "company_name": sub.get("name"),
        "sic": sub.get("sic"),
        "sic_description": sub.get("sicDescription"),
        "state_of_incorporation": sub.get("stateOfIncorporation"),
        "state_of_incorporation_description":
            sub.get("stateOfIncorporationDescription"),
        "tickers": sub.get("tickers"),
        "exchanges": sub.get("exchanges"),
        "entity_type": sub.get("entityType"),
        "filer_category": sub.get("category"),
        "fiscal_year_end": sub.get("fiscalYearEnd"),
        "ein": sub.get("ein"),
        "phone": sub.get("phone"),
        "website": sub.get("website"),
        "investor_website": sub.get("investorWebsite"),
        "addresses": sub.get("addresses"),
        "flags": sub.get("flags"),
        "owner_org": sub.get("ownerOrg"),
        "former_names": sub.get("formerNames"),
    })
    recent = sub.get("filings", {}).get("recent", {})
    facts["filings_recent_count"] = len(recent.get("form", []))
    facts["filings_latest"] = _summarize_filings(sub, _LATEST_N_FILINGS)
    facts["filings_archives"] = len(sub.get("filings", {}).get("files", []))
    if sub.get("insiderTransactionForOwnerExists"):
        notes.append("insider transactions exist for owners of this issuer")

    # ---- 3. XBRL company facts ----
    cf_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    sources.append(cf_url)
    cf_status, cf = _get_json(cf_url, last_call, notes, "companyfacts")
    if cf_status == 404 or cf is None:
        facts["companyfacts"] = None
        notes.append("no XBRL company facts for this CIK "
                     f"(HTTP {cf_status}); filer may not publish XBRL")
    else:
        facts["companyfacts"] = _summarize_companyfacts(cf)

    return lane_record("sec_edgar", source, "ok", facts, sources, notes)


if __name__ == "__main__":
    import sys
    print(json.dumps(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}),
                     indent=1))
