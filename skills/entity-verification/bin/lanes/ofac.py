"""OFAC SDN sanctions screening lane (targeted, $0, no key).

LIVE TEST RECORD (2026-09-20, ~19:20-19:27 EDT, tested live this session):
- Old published endpoint https://sanctionssearch.ofac.treas.gov/api/PublicationPreview/exports/SDN.CSV -> HTTP 404 (1,245-byte error page). That hostname is dead.
- Current endpoint: https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.CSV
  -> HTTP 200, 5,695,725 bytes (5.7 MB), 19,394 rows x 12 cols, download ~11s.
  Redirects to a presigned S3 URL (wc2h-sls-prod-public-published, us-gov-west-1);
  the published bundle is stamped 2026-09-17, i.e. OFAC refreshes this file often.
  First data row: ent 36 "AEROCARIBBEAN AIRLINES", country CUBA, `-0-` placeholders
  in unset columns. Row col index 1 = SDN name, col 3 = country/remarks block.
- DELTA endpoint .../exports/SDN_DELTA.CSV -> HTTP 200 but 0 bytes (empty body) on
  2026-09-20. Treated as unusable; full-file refresh is the working lane.
- Live local lookups on the fetched 19,394-row file for two test entities (names withheld in this public copy),
  "BLACK LIVES MATTER" (substring scan over name column): ZERO hits for all three.
- FEC-style HTTP calls are not used here; this lane is pure bulk-fetch + local match.

Design: fetch-once, cache locally under the skill's .cache dir (raw CSV file, not
the JSON cache wrapper), refresh when the cached copy is older than 7 days (OFAC
updates its lists frequently; Treasury's recommendation is effectively "check
regularly" -- weekly refresh is the floor for any screening use).
Matching is intentionally conservative: token-intersection on the normalized
candidate name. NEVER asserts a positive match -- returns "no_match" or
"candidate_match (needs review)" only, with the raw SDN rows attached for a human.
"""
from __future__ import annotations

import csv
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bizintel_common import CACHE_DIR, cache_get, cache_set, lane_record, now_iso  # noqa: E402

LANE = "ofac_sdn"
SOURCE = "U.S. Treasury OFAC SDN bulk export"

SDN_URL = "https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.CSV"
# Old/dead URL kept for the record (verified 404 live 2026-09-20):
SDN_URL_LEGACY = "https://sanctionssearch.ofac.treas.gov/api/PublicationPreview/exports/SDN.CSV"

CACHE_FILE = os.path.join(CACHE_DIR, "ofac_sdn.csv")
META_KEY = "ofac:snd:meta"
REFRESH_SECONDS = 7 * 24 * 3600  # weekly refresh floor

_LEGAL_SUFFIXES = {
    "INC", "INCORPORATED", "LLC", "LTD", "LIMITED", "CORP", "CORPORATION",
    "COMPANY", "CO", "PLLC", "LP", "LLP", "PA", "DBA", "FKA", "AKA",
    "THE", "OF", "AND", "&",
}


def _tokens(text: str) -> list[str]:
    toks = re.findall(r"[A-Z0-9]+", (text or "").upper())
    return [t for t in toks if t not in _LEGAL_SUFFIXES and len(t) > 1]


def _fetch_sdn_csv(timeout: int = 120) -> tuple[int, bytes]:
    """Download the SDN CSV through the stable endpoint (follows the S3 presign)."""
    req = urllib.request.Request(
        SDN_URL,
        headers={"User-Agent": "EntityVerification/1.0",
                 "Accept": "text/csv, */*"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def ensure_cached(force: bool = False) -> dict:
    """Return {status, rows, bytes, published_note, fetched_live} for the cache."""
    fresh = False
    if os.path.exists(CACHE_FILE) and not force:
        if time.time() - os.path.getmtime(CACHE_FILE) < REFRESH_SECONDS:
            fresh = True
    if not fresh:
        os.makedirs(CACHE_DIR, exist_ok=True)
        status, body = _fetch_sdn_csv()
        if status != 200 or len(body) < 100_000:
            return {"status": "error", "http": status, "bytes": len(body)}
        tmp = CACHE_FILE + ".tmp"
        with open(tmp, "wb") as fh:
            fh.write(body)
        os.replace(tmp, CACHE_FILE)
        cache_set(META_KEY, {"fetched_at": now_iso(), "bytes": len(body),
                             "url": SDN_URL})
    with open(CACHE_FILE, "rb") as fh:
        body = fh.read()
    return {"status": "ok", "rows": body.count(b"\n"), "bytes": len(body),
            "cached_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(
                os.path.getmtime(CACHE_FILE)))}


def _load_rows():
    with open(CACHE_FILE, encoding="utf-8", errors="replace") as fh:
        for row in csv.reader(fh):
            if len(row) >= 2 and row[0].strip().lstrip("-").isdigit():
                yield row


def screen_name(name: str):
    """Return candidate SDN rows where ALL significant name tokens match.

    Returns (status, matches) -- status is "no_match" or "candidate_match".
    A candidate_match is NOT a positive ID; it needs human review.
    """
    want = _tokens(name)
    matches = []
    for row in _load_rows():
        sdn_name = (row[1] or "").upper()
        if want and all(t in sdn_name for t in want):
            matches.append({"sdn_ent": row[0].strip(),
                            "sdn_name": row[1].strip(),
                            "sdn_info": row[3].strip() if len(row) > 3 else ""})
            if len(matches) >= 25:
                break
    return ("candidate_match" if matches else "no_match", matches)


def run(entity: dict) -> dict:
    """Screen one candidate entity. entity: {"name": str, "address": str (opt)}."""
    name = (entity or {}).get("name", "").strip()
    if not name:
        return lane_record(LANE, SOURCE, "error", {}, notes=["no entity name supplied"])
    try:
        cached = ensure_cached()
    except Exception as exc:  # network failure etc. -> parked with evidence
        return lane_record(
            LANE, SOURCE, "parked", {},
            notes=[f"SDN bulk fetch failed live: {exc!r}; lane unusable offline"])
    if cached.get("status") != "ok":
        return lane_record(LANE, SOURCE, "parked", {"fetch": cached},
                           notes=["SDN bulk file unavailable (HTTP/size check failed)"])
    status, matches = screen_name(name)
    facts = {
        "entity_name": name,
        "sdn_file_bytes": cached["bytes"],
        "sdn_file_rows": cached["rows"],
        "sdn_file_cached_at": cached["cached_at"],
        "screening": status,
        "candidate_rows": matches,
    }
    notes = [
        "Targeted screening only: bulk SDN list fetched once and matched locally; "
        "OFAC updates frequently -- refresh this file at least weekly before any reliance.",
        "Local token matching is NOT a compliance-grade determination; a candidate_match "
        "means 'needs human review', never 'sanctioned'.",
        "SDN_DELTA.CSV endpoint returned an empty body on 2026-09-20; full-file refresh is the lane.",
    ]
    return lane_record(LANE, SOURCE, status, facts, notes=notes)


if __name__ == "__main__":  # smoke: python3 ofac.py "NAME TO SCREEN"
    import json
    target = sys.argv[1] if len(sys.argv) > 1 else "ACME COMMUNITY FOUNDATION INC"
    print(json.dumps(run({"name": target}), indent=2))
