"""OpenFEC committee screening lane (free, API-key via api.data.gov).

LIVE TEST RECORD (2026-09-20, ~19:20-19:28 EDT, tested live this session):
- Base: https://api.open.fec.gov/v1 ; DEMO_KEY worked without registration.
- GET /committees/?q=ACTBLUE&api_key=DEMO_KEY -> HTTP 200, 1 result (pagination.count=1):
  committee_id C00401224, name "ACTBLUE", committee_type "V",
  committee_type_full "Hybrid PAC (with Non-Contribution Account) - Nonqualified",
  designation "U", designation_full "Unauthorized", filing_frequency "M",
  state "MA", treasurer_name "GILMER, GEORGE", cycles [2004..2026],
  first_file_date "2004-05-17", last_file_date "2026-08-20",
  party/party_full null, organization_type null.
- GET /committees/?q=<ENTITY>&api_key=DEMO_KEY -> HTTP 200, pagination.count=0,
  results []. (No committee registered under that name -- expected for a nonprofit.)
- GET /schedules/schedule_a/?committee_id=C00401224&per_page=1&api_key=DEMO_KEY
  -> HTTP 200; ~553M receipts in the index; first result fields include
  amendment_indicator, candidate_* (null for this row), contributor info fields.
  Receipt/disbursement totals for a committee come cheaper from /committee/{id}/totals/.
- Rate-limit headers MEASURED on live responses (not from docs):
  X-Ratelimit-Limit: 10, X-Ratelimit-Remaining: 9.
  (This is a short-window bucket; DEMO_KEY is documented at ~40 requests/hour --
  fine for one-off vetting, not for bulk sweeps.)

Free-key upgrade path: request a free personal key at https://api.data.gov/signup/
(email only, no signup for DEMO_KEY needed to test). Then pass api_key to run()
or set env OPENFEC_API_KEY.

Scope: this lane is political/527-adjacent vetting ONLY -- it answers "does an
FEC-registered committee exist under/near this name" plus basic committee facts.
A hit does NOT mean the entity itself is political, and a miss does NOT clear it.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bizintel_common import cache_get, cache_set, http_get, lane_record, now_iso  # noqa: E402

LANE = "fec_committees"
SOURCE = "FEC OpenFEC API (api.open.fec.gov)"

BASE = "https://api.open.fec.gov/v1"
DEMO_KEY = "DEMO_KEY"

_committee_fields = (
    "committee_id", "name", "designation", "designation_full",
    "committee_type", "committee_type_full", "party", "party_full",
    "treasurer_name", "state", "cycles", "filing_frequency",
    "organization_type", "organization_type_full",
    "first_file_date", "last_file_date",
)


def _key(api_key: str | None) -> str:
    return api_key or os.environ.get("OPENFEC_API_KEY") or DEMO_KEY


def _slim_committee(raw: dict) -> dict:
    return {k: raw.get(k) for k in _committee_fields}


def committee_search(query: str, api_key: str | None = None, per_page: int = 20):
    """Name search; returns (status, text, headers, parsed). Cached 24h per query."""
    key = _key(api_key)
    cache_key = f"fec:committees:q={query}:pp={per_page}"
    hit = cache_get(cache_key)
    if hit is not None:
        return 200, json.dumps(hit), {}, hit
    status, text, headers = http_get(
        f"{BASE}/committees/",
        params={"q": query, "per_page": per_page, "api_key": key},
        min_interval=1.0, last_call=_throttle)
    if status != 200:
        return status, text, headers, None
    try:
        parsed = json.loads(text)
    except ValueError:
        return status, text, headers, None
    cache_set(cache_key, parsed)
    return status, text, headers, parsed


def committee_totals(committee_id: str, cycle: int = 2026, api_key: str | None = None):
    """Cheap money-in/out summary for a committee. Returns parsed dict or None."""
    key = _key(api_key)
    status, text, _ = http_get(
        f"{BASE}/committee/{committee_id}/totals/",
        params={"cycle": cycle, "full_election": "true", "api_key": key},
        min_interval=1.0, last_call=_throttle)
    if status != 200:
        return None
    try:
        return json.loads(text)
    except ValueError:
        return None


_throttle: dict = {}


def run(entity: dict) -> dict:
    """Look up FEC-registered committees near the entity name.

    entity: {"name": str, "api_key": str (opt)}. Returns standard lane_record.
    """
    name = (entity or {}).get("name", "").strip()
    if not name:
        return lane_record(LANE, SOURCE, "error", {}, notes=["no entity name supplied"])
    key_used = "provided/env" if (entity.get("api_key") or os.environ.get("OPENFEC_API_KEY")) else "DEMO_KEY"
    try:
        status, text, headers, parsed = committee_search(name, entity.get("api_key"))
    except Exception as exc:
        return lane_record(LANE, SOURCE, "parked", {},
                           notes=[f"OpenFEC request failed live: {exc!r}"])
    rate_info = {k: v for k, v in headers.items()
                 if "ratelimit" in k.lower() or "rate" in k.lower()}
    if status != 200 or parsed is None:
        return lane_record(
            LANE, SOURCE, "error",
            {"http_status": status, "rate_limit_headers": rate_info, "key_used": key_used},
            notes=["OpenFEC committee search failed; check rate limits or key"])
    results = parsed.get("results", []) or []
    pagination = parsed.get("pagination", {}) or {}
    committees = [_slim_committee(r) for r in results]
    facts = {
        "entity_name": name,
        "key_used": key_used,
        "result_count": pagination.get("count", len(results)),
        "committees": committees,
        "rate_limit_headers": rate_info,
    }
    notes = [
        "Scoped to political/527-adjacent vetting: answers only whether an "
        "FEC-registered committee exists under/near this name. A hit does not "
        "mean the entity is political; a miss does not clear it.",
        f"Free-key upgrade path: request a free key at https://api.data.gov/signup/ "
        f"and set OPENFEC_API_KEY (or pass api_key). DEMO_KEY is rate-capped "
        f"(measured X-Ratelimit-Limit: 10 per short window, documented ~40/hr).",
        "For money-in/out totals use /committee/{id}/totals/; receipts detail via "
        "/schedules/schedule_a/ (553M+ rows -- keep per_page small).",
    ]
    return lane_record(LANE, SOURCE,
                       "ok" if committees else "no_record", facts, notes=notes)


if __name__ == "__main__":  # smoke: python3 fec.py "NAME TO SEARCH"
    query = sys.argv[1] if len(sys.argv) > 1 else "ACTBLUE"
    print(json.dumps(run({"name": query}), indent=2))
