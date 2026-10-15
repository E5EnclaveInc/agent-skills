"""NY Department of State, Division of Corporations — API lane.

Settled 2026-09-20 (war-room lane, firsthand evidence):
  Source: data.ny.gov Socrata dataset "Active Corporations: Beginning 1800",
  dataset id n9v6-gdp6 (replaces the older view exzd-3inm).
  Measured live: 4,283,693 active rows; X-SODA2-Data-Out-Of-Date: false;
  dataset truth last modified 2026-09-20 11:30 GMT; latest initial filing
  date in the data 2026-09-18. Queries (exact DOS ID, SoQL name search) all
  returned HTTP 200 in seconds; no throttling observed across back-to-back
  requests. Covers business corporations, LLCs, LPs, LLPs, not-for-profits
  and misc entities — INCLUDING for-profit corporations.

  Known limits (why the browser lane still exists):
  - Dataset holds ACTIVE entities only. Inactive / suspended / dissolved
    entities are not in it — those go to the browser lane (official public
    inquiry site allows an Entity Status filter: active, inactive,
    suspended, or all).
  - No assumed-name (DBA) linkage in the dataset; assumed-name certificate
    search lives only on the official public-inquiry form.
  - Status field is implied "Active" by membership in the dataset.

Usage:
  from lanes.nydos import run
  run({"dos_id": "5795922"})
  run({"name": "BLACK LIVES MATTER GRASSROOTS - BUFFALO CHAPTER INC."})
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bizintel_common import http_get, lane_record, cache_get, cache_set  # noqa: E402

DATASET_ID = "n9v6-gdp6"
DATASET_URL = f"https://data.ny.gov/resource/{DATASET_ID}.json"
DATASET_PAGE = "https://data.ny.gov/Business-Enterprise/Active-Corporations-Beginning-1800/n9v6-gdp6"
OFFICIAL_SEARCH = "https://www.dos.ny.gov/corps/bus_entity_search.html"
PUBLIC_INQUIRY = "https://apps.dos.ny.gov/publicInquiry/"

SOURCE = f"NY DOS Division of Corporations via data.ny.gov Socrata API ({DATASET_ID})"

_rate: dict = {}


def _query(params: dict) -> list:
    """Run a SoQL query against the dataset with the hardened transport."""
    cache_key = "nydos:" + "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    cached = cache_get(cache_key, ttl=6 * 3600)
    if cached is not None:
        return cached
    status, text, _ = http_get(DATASET_URL, params=params, min_interval=0.6,
                              last_call=_rate)
    if status != 200:
        raise RuntimeError(f"data.ny.gov returned HTTP {status} for {params}")
    import json
    rows = json.loads(text)
    cache_set(cache_key, rows)
    return rows


def _clean(value):
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def _facts(row: dict) -> dict:
    def addr(prefix: str) -> str | None:
        parts = [row.get(f"{prefix}_{k}") for k in
                 ("name", "address_1", "address_2", "city", "state", "zip")]
        parts = [p for p in (_clean(p) for p in parts) if p]
        return ", ".join(parts) if parts else None

    return {
        "dos_id": _clean(row.get("dos_id")),
        "entity_name": _clean(row.get("current_entity_name")),
        # Dataset membership implies active; the dataset itself is "Active Corporations".
        "status": "Active (dataset membership — active entities only)",
        "entity_type": _clean(row.get("entity_type")),
        "jurisdiction": _clean(row.get("jurisdiction")),
        "county": _clean(row.get("county")),
        "initial_dos_filing_date": _clean(row.get("initial_dos_filing_date")),
        "dos_process": addr("dos_process"),
        "registered_agent": addr("registered_agent"),
        "location": addr("location"),
        "chairman": addr("chairman"),
        "record_url": f"{PUBLIC_INQUIRY} (official) / dataset {DATASET_URL}",
    }


def run(entity: dict) -> dict:
    """Look up a NY entity. entity may carry 'dos_id' and/or 'name'."""
    dos_id = str(entity.get("dos_id", "") or "").strip()
    name = str(entity.get("name", "") or entity.get("legal_name", "") or "").strip()
    notes = [
        "Dataset 'Active Corporations: Beginning 1800' (n9v6-gdp6) holds "
        "ACTIVE entities only; a no_record here does not prove the entity "
        "never existed in NY — route inactive/dissolved lookups and "
        "assumed-name (DBA) searches to the browser lane "
        f"({PUBLIC_INQUIRY}).",
    ]
    sources = [SOURCE, DATASET_PAGE]

    try:
        if dos_id:
            rows = _query({"dos_id": dos_id, "$limit": "5"})
            if not rows:
                return lane_record("ny_dos", SOURCE, "no_record", {},
                                   sources,
                                   notes + [f"No active NY entity with DOS ID {dos_id}."])
            row = rows[0]
            return lane_record("ny_dos", SOURCE, "ok", _facts(row), sources,
                               notes + [f"Exact DOS ID match: {dos_id}."])

        if not name:
            return lane_record("ny_dos", SOURCE, "error", {},
                               sources, ["run() needs 'dos_id' or 'name'."])

        upper = name.upper().replace("'", "''")
        # Exact match first.
        rows = _query({"$where": f"upper(current_entity_name)='{upper}'",
                       "$limit": "11"})
        if len(rows) == 1:
            return lane_record("ny_dos", SOURCE, "ok", _facts(rows[0]),
                               sources, notes + ["Exact name match."])
        if len(rows) > 1:
            return lane_record(
                "ny_dos", SOURCE, "ok",
                {"candidates": [_facts(r) for r in rows[:10]],
                 "matches_shown": len(rows[:10]),
                 "result_capped": len(rows) > 10},
                sources, notes + [
                    f"Exact-name search returned {len(rows)}+ active NY "
                    "entities (results capped at 10) — disambiguate by DOS ID "
                    "before relying on one."])
        # Fuzzy fallback.
        rows = _query({"$where": f"upper(current_entity_name) like '%{upper}%'",
                       "$limit": "11"})
        if not rows:
            return lane_record("ny_dos", SOURCE, "no_record", {},
                               sources,
                               notes + [f"No active NY entity matching '{name}'."])
        if len(rows) == 1:
            return lane_record(
                "ny_dos", SOURCE, "ok", _facts(rows[0]), sources,
                notes + [f"Single fuzzy match for '{name}' — confirm it is the "
                         "intended entity by DOS ID."])
        return lane_record(
            "ny_dos", SOURCE, "ok",
            {"candidates": [_facts(r) for r in rows[:10]],
             "matches_shown": len(rows[:10]),
             "result_capped": len(rows) > 10},
            sources, notes + [
                f"Fuzzy match for '{name}' returned {len(rows)}+ candidates "
                "(capped at 10) — disambiguate by DOS ID before relying on "
                "one."])

    except Exception as exc:  # transport failure after retries
        return lane_record("ny_dos", SOURCE, "error", {},
                           sources,
                           notes + [f"API query failed: {exc}; route to the "
                                    f"browser lane ({PUBLIC_INQUIRY})."])


if __name__ == "__main__":
    import json
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    ent = {"dos_id": arg} if arg.isdigit() else {"name": arg}
    print(json.dumps(run(ent), indent=2))
