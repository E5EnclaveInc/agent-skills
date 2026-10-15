"""Nonprofit 990 lane: IRS tax-exempt standing via two $0 public sources.

Sources:
  A. ProPublica Nonprofit Explorer API v2 (keyless) — live org profile + 990 filing
     metadata.  https://projects.propublica.org/nonprofits/api/v2/
  B. IRS EO Business Master File extract (EO BMF) — monthly CSV; we cache the
     Region-3 extract (eo3.csv, covers FL) locally and grep by EIN.

All HTTP goes through bizintel_common (retries/backoff/timeout/caching).

LIVE TEST RECORD — 2026-09-20 (EDT/UTC-4), executed by the war-room n990 lane.
  Entity: a verified nonprofit test entity (name/EIN withheld in this public copy).
  Endpoints hit:
    GET https://projects.propublica.org/nonprofits/api/v2/organizations/993822441.json
      -> 200, ~3.1s, 1338 bytes. Key raw fields:
        organization.ein=<ein9>, name='<Test Entity>',
        city='Miami', state='FL', ruling_date='2024-07-01', subsection_code=3,
        classification_codes='P99', tax_period=None, latest_object_id=None,
        have_extracts=false, have_pdfs=false, filings_with_data=[]
      (No 990 filed to the IRS on record as of test date — consistent with a
      2024-07 ruling org; PP also carries BMF-derived org fields.)
    GET https://projects.propublica.org/nonprofits/api/v2/organizations/000000000.json
      (deliberate missing-EIN negative case)
      -> 200, ~2.7s. QUIRK: ProPublica returns HTTP 200 for unknown EINs with
        organization={ein:0, id:0, name:"Unknown Organization", ...nulls}.
        No-record detection MUST check org.ein==0/name=="Unknown Organization",
        not the HTTP status.
    IRS page https://www.irs.gov/charities-non-profits/exempt-organizations-
      business-master-file-extract-eo-bmf — read 2026-09-20: data posting date
      9/8/2026, record count 1,964,958. CSVs split by state; Region 3
      (eo3.csv) covers FL.
    HEAD https://www.irs.gov/pub/irs-soi/eo3.csv -> 200, Content-Type: text/csv.
    Downloaded eo3.csv live on 2026-09-20 and grep-verified the test entity's row by EIN.
  Rate limits observed: none surfaced (no Retry-After headers); calls spaced
  >=1s apart. Response latency 2.7-3.1s per call from this VM.

Bulk-vs-targeted recommendation (filed in module): download the regional
extract once (EO BMF is posted monthly), cache it in bizintel_common's .cache
dir, refresh monthly, and grep locally by EIN. This is strictly cheaper and
more reliable than hitting the ProPublica API per entity; ProPublica stays as
the live cross-check (ruling year, subsection, latest 990 metadata).
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bizintel_common import (  # noqa: E402
    CACHE_DIR, cache_get, cache_set, http_get, lane_record, now_iso,
)

PP_BASE = "https://projects.propublica.org/nonprofits/api/v2"
IRS_BMF_PAGE = ("https://www.irs.gov/charities-non-profits/"
                "exempt-organizations-business-master-file-extract-eo-bmf")
# Regional extracts: eo1..eo4.csv. Florida sits in Region 3 (eo3.csv).
IRS_REGION = {"FL": 3, "FL-region-url": "https://www.irs.gov/pub/irs-soi/eo3.csv"}
BMF_CACHE_PREFIX = "eo3_"
PP_CACHE_TTL = 24 * 3600

_LAST = {"t": 0}  # cross-call minimum-interval enforcement for ProPublica


def _ein9(ein: str) -> str:
    digits = re.sub(r"\D", "", ein or "")
    return digits.zfill(9) if digits else ""


def _pp_lookup(ein9: str) -> dict:
    """Live ProPublica v2 org lookup. Returns (status, org_dict, notes)."""
    cache_key = f"n990:pp:v2:{ein9}"
    cached = cache_get(cache_key, ttl=PP_CACHE_TTL)
    notes = []
    if cached is not None:
        notes.append("propublica response served from lane cache")
        return cached["status"], cached["org"], notes
    url = f"{PP_BASE}/organizations/{ein9}.json"
    status, text, _hdrs = http_get(url, last_call=_LAST, min_interval=1.0)
    if status == 404:
        result = ("no_record", {}, notes)
        cache_set(cache_key, {"status": result[0], "org": result[1]})
        return result
    if status != 200 or not text:
        notes.append(f"propublica returned HTTP {status}")
        return ("error", {}, notes)
    try:
        payload = json.loads(text)
    except ValueError:
        notes.append("propublica returned non-JSON body")
        return ("error", {}, notes)
    org = payload.get("organization") or {}
    # ProPublica's no-record quirk: HTTP 200 with a stub org (see docstring).
    if not org.get("ein") or org.get("name") == "Unknown Organization":
        notes.append("propublica returned its 'Unknown Organization' stub: no record")
        result = ("no_record", {}, notes)
        cache_set(cache_key, {"status": result[0], "org": result[1]})
        return result
    result = ("ok", org, notes)
    cache_set(cache_key, {"status": result[0], "org": result[1]})
    return result


def _bmf_lookup(ein9: str) -> dict:
    """Local lookup of the cached EO BMF regional extract for one EIN.

    Prefers the sqlite EIN index (bmf_ein_index.db, built once per cached
    extract — ms per lookup); falls back to the sequential CSV scan (~14s).

    Returns dict(status, row, notes, cache_file). status: ok | no_record |
    parked (file not downloaded yet) | error.
    """
    notes = []
    if not os.path.isdir(CACHE_DIR):
        return {"status": "parked", "row": {}, "notes": [
            "EO BMF extract not cached; run the download step "
            f"(IRS_REGION url -> {CACHE_DIR}) before local lookup"], "cache_file": None}
    idx_path = os.path.join(CACHE_DIR, "bmf_ein_index.db")
    if os.path.isfile(idx_path):
        try:
            import sqlite3
            conn = sqlite3.connect(f"file:{idx_path}?mode=ro", uri=True)
            row = conn.execute(
                "SELECT ein,name,state,subsection,ruling,class,deduct,tax_period,ntee,org,status"
                " FROM bmf WHERE ein=?", (ein9,)).fetchone()
            conn.close()
            if row:
                keys = ["EIN", "NAME", "STATE", "SUBSECTION", "RULING",
                        "CLASSIFICATION", "DEDUCTIBILITY", "TAX_PERIOD",
                        "NTEE_CD", "ORGANIZATION", "STATUS"]
                return {"status": "ok", "row": dict(zip(keys, row)),
                        "notes": notes + ["bmf lookup via sqlite EIN index"],
                        "cache_file": "bmf_ein_index.db"}
            return {"status": "no_record", "row": {},
                    "notes": notes + ["ein not found in cached BMF EIN index"],
                    "cache_file": "bmf_ein_index.db"}
        except Exception as exc:  # fall through to CSV scan
            notes.append(f"sqlite index read failed ({exc}); falling back to CSV scan")
    cands = [f for f in sorted(os.listdir(CACHE_DIR))
             if f.startswith(BMF_CACHE_PREFIX) and f.endswith(".csv")]
    if not cands:
        return {"status": "parked", "row": {}, "notes": [
            "EO BMF extract not cached; run the download step "
            f"(IRS_REGION url -> {CACHE_DIR}) before local lookup"], "cache_file": None}
    path = os.path.join(CACHE_DIR, cands[-1])  # newest posting
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if (row.get("EIN") or "").zfill(9) == ein9:
                    return {"status": "ok", "row": row, "notes": notes,
                            "cache_file": os.path.basename(path)}
    except OSError as exc:
        return {"status": "error", "row": {}, "notes": [f"bmf cache read failed: {exc}"],
                "cache_file": None}
    notes.append(f"ein not found in cached BMF extract {os.path.basename(path)}")
    return {"status": "no_record", "row": {}, "notes": notes,
            "cache_file": os.path.basename(path)}


def _subsection_label(code) -> str:
    try:
        n = int(str(code))
    except (TypeError, ValueError):
        return "unknown"
    return f"501(c)({n})"


def run(entity: dict) -> dict:
    """Run the nonprofit-990 lane for one entity.

    entity keys: legal_name, state, ein, entity_type.
    """
    name = (entity or {}).get("legal_name", "")
    ein = (entity or {}).get("ein", "")
    state = ((entity or {}).get("state") or "FL").upper()
    ein9 = _ein9(ein)
    notes = []
    sources = []

    if not ein9:
        return lane_record(
            "nonprofit_990", "propublica-nonprofit-explorer+irs-eo-bmf",
            "error", {"queried_ein": ein, "legal_name": name},
            sources=sources,
            notes=["no EIN supplied on entity; nothing to look up"])

    # Source A: ProPublica live
    pp_status, org, pp_notes = _pp_lookup(ein9)
    notes.extend(pp_notes)
    sources.append(f"{PP_BASE}/organizations/{ein9}.json")

    # Source B: EO BMF local extract
    bmf = _bmf_lookup(ein9)
    notes.extend(bmf["notes"])
    if bmf["cache_file"]:
        sources.append(f"{IRS_BMF_PAGE} (local cache: {bmf['cache_file']})")

    facts = {"queried_ein": f"{ein9[:2]}-{ein9[2:]}", "legal_name": name,
             "propublica_status": pp_status, "bmf_status": bmf["status"]}

    if pp_status == "ok":
        fils = [f for f in (org.get("filings_with_data") or [])]
        latest = fils[0] if fils else {}
        facts.update({
            "ein": str(org.get("ein")),
            "pp_name": org.get("name"),
            "city": org.get("city"),
            "state": org.get("state"),
            "ruling_date": org.get("ruling_date"),
            "subsection": _subsection_label(org.get("subsection_code")),
            "subsection_code": org.get("subsection_code"),
            "ntee_code": org.get("ntee_code"),
            "exemption_number": org.get("exemption_number"),
            "filings_with_data_count": len(fils),
            "org_tax_period": org.get("tax_period"),
            "latest_filing_tax_period": latest.get("tax_prd") if fils else None,
            "latest_filing_form": latest.get("formtype") if fils else None,
            "latest_filing_object_id": latest.get("object_id") if fils else None,
            "have_pdfs": org.get("have_pdfs"),
        })
    if bmf["status"] == "ok":
        row = bmf["row"]
        facts.update({
            "bmf_name": row.get("NAME"),
            "bmf_city": row.get("CITY"),
            "bmf_state": row.get("STATE"),
            "bmf_ruling": row.get("RULING"),          # YYYYMM
            "bmf_subsection": row.get("SUBSECTION"),  # e.g. '03'
            "bmf_classification": row.get("CLASSIFICATION"),
            "bmf_foundation": row.get("FOUNDATION"),
            "bmf_deductibility": row.get("DEDUCTIBILITY"),
            "bmf_tax_period": row.get("TAX_PERIOD"),
            "bmf_status_code": row.get("STATUS"),
            "bmf_ntee": row.get("NTEE_CD"),
        })

    # Name guard: the two sources must agree with the requested entity; surface
    # any mismatch loudly instead of conflating organizations.
    found_names = [n for n in (facts.get("pp_name"), facts.get("bmf_name")) if n]
    if found_names and name and not any(name.strip().lower() in n.lower()
                                        or n.lower() in name.strip().lower()
                                        for n in found_names):
        notes.append("NAME MISMATCH: EIN resolves to a different organization name "
                     f"({found_names}); do not conflate with '{name}'")

    if pp_status == "ok" or bmf["status"] == "ok":
        status = "ok"
    elif pp_status == "no_record" and bmf["status"] in ("no_record", "parked"):
        status = "no_record"
    elif pp_status == "error" and bmf["status"] != "ok":
        status = "error"
    else:
        status = "parked"

    return lane_record("nonprofit_990",
                       "propublica-nonprofit-explorer+irs-eo-bmf",
                       status, facts, sources=sources, notes=notes)
