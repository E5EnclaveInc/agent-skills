#!/usr/bin/env python3
"""BizIntel — unified business-investigation CLI.

Runs one entity through every BizIntel lane and emits a single
per-entity dossier: a JSON record plus a human-readable summary.

API lanes are self-contained modules in lanes/ (they share the hardened
transport in bizintel_common.py). The two pre-existing arsenal tools are
reused BY REFERENCE (subprocess, never copied):
  - SAM.gov:  $SAM_GOV_CLI (a SAM.gov API client you provide; env var)
  - mailbox:  this skill's bin/entity_mail_sweep.py

Read-only. No filings, no payments, no amendments, no outside contact.
$0: every lane is keyless, free-keyed-with-DEMO_KEY, or cached bulk.

Usage:
  bizintel.py --name "ACME COMMUNITY FOUNDATION INC" --state FL --type nonprofit --ein <EIN>
  bizintel.py --name "TESLA, INC." --type for-profit --ticker TSLA
  bizintel.py --name "RIVERBEND COMMUNITY ALLIANCE INC" --lanes n990,ofac,mailbox
  bizintel.py --entity-json entity.json --out dossier.json
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from bizintel_common import now_iso  # noqa: E402

SAM_PY = os.environ.get("SAM_GOV_CLI", "")  # path to a SAM.gov API client (optional lane)
MAIL_SWEEP = os.path.join(HERE, "entity_mail_sweep.py")

API_LANES = ["n990", "edgar", "ofac", "fec", "nydos"]
LANE_TIMEOUT_S = 180  # a flaky endpoint must never stall the whole dossier


class _LaneTimeout(Exception):
    pass


def _with_timeout(fn, entity, seconds=LANE_TIMEOUT_S):
    def _raise(signum, frame):
        raise _LaneTimeout(f"lane exceeded {seconds}s budget")
    prev = signal.signal(signal.SIGALRM, _raise)
    signal.alarm(seconds)
    try:
        return fn(entity)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, prev)


def _run_api_lane(lane: str, entity: dict) -> dict:
    mod = importlib.import_module(f"lanes.{lane}")
    return mod.run(entity)


def _run_sam(entity: dict) -> dict:
    """Lane D — reuse an external SAM.gov client by reference (subprocess)."""
    if not SAM_PY or not os.path.exists(SAM_PY):
        return {"lane": "sam", "source": "https://api.sam.gov",
                "retrieved_at": now_iso(), "status": "error",
                "facts": {}, "sources": ["https://api.sam.gov"],
                "notes": ["SAM_GOV_CLI is not set (or the path does not exist) — Lane D skipped."]}
    started = time.time()
    params: dict = {}
    if entity.get("uei"):
        params["ueiSAM"] = entity["uei"]
    else:
        params["legalBusinessName"] = entity["legal_name"]
    cmd = [sys.executable, SAM_PY, "GET", "/entity-information/v3/entities",
           "--params", json.dumps(params)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return {"lane": "sam", "source": "https://api.sam.gov",
                "retrieved_at": now_iso(), "status": "error",
                "facts": {}, "sources": ["https://api.sam.gov"],
                "notes": [f"sam.py did not run: {exc}"]}
    try:
        payload = json.loads(out.stdout or "{}")
    except json.JSONDecodeError:
        return {"lane": "sam", "source": "https://api.sam.gov",
                "retrieved_at": now_iso(), "status": "error",
                "facts": {}, "sources": ["https://api.sam.gov"],
                "notes": [f"sam.py output was not JSON (stderr: {out.stderr[:300]})"]}
    entities = (payload.get("entityData") or [])
    if not entities:
        return {"lane": "sam", "source": "https://api.sam.gov",
                "retrieved_at": now_iso(), "status": "no_record",
                "facts": {"duration_s": round(time.time() - started, 1)},
                "sources": ["https://api.sam.gov"],
                "notes": ["No SAM.gov entity matched the lookup."]}
    reg = entities[0].get("entityRegistration", {})
    assertions = entities[0].get("assertions", {}).get("goodsAndServices", {})
    return {"lane": "sam", "source": "https://api.sam.gov",
            "retrieved_at": now_iso(), "status": "ok",
            "facts": {
                "legal_name": reg.get("legalBusinessName"),
                "uei": reg.get("ueiSAM"),
                "cage": reg.get("cageCode"),
                "registration_status": reg.get("registrationStatus"),
                "activation_date": reg.get("activationDate"),
                "expiration_date": reg.get("expirationDate"),
                "last_update": reg.get("lastUpdateDate"),
                "primary_naics": assertions.get("primaryNaics"),
                "duration_s": round(time.time() - started, 1),
            },
            "sources": ["https://api.sam.gov"],
            "notes": ["Reuse-by-reference: external SAM.gov client (not copied)."]}


def _run_mailbox(entity: dict) -> dict:
    """Lane C — reuse this skill's entity_mail_sweep.py by reference."""
    started = time.time()
    cmd = [sys.executable, MAIL_SWEEP, "--name", entity["legal_name"]]
    if entity.get("dba"):
        cmd += ["--dba", entity["dba"]]
    if entity.get("doc_number"):
        cmd += ["--doc", entity["doc_number"]]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except Exception as exc:
        return {"lane": "mailbox", "source": "business mailbox (Graph)",
                "retrieved_at": now_iso(), "status": "error",
                "facts": {}, "sources": [],
                "notes": [f"entity_mail_sweep.py did not run: {exc}"]}
    text = out.stdout or ""
    # entity_mail_sweep.py emits human-readable text; parse the totals line.
    import re as _re
    hits = 0
    m = _re.search(r"(\d+)\s+unique relevant messages", text)
    if m:
        hits = int(m.group(1))
    facts = {
        "hits_found": hits,
        "duration_s": round(time.time() - started, 1),
        "output_tail": text[-800:] if text else "",
    }
    if out.returncode != 0 and not text.strip():
        return {"lane": "mailbox", "source": "business mailbox (Graph)",
                "retrieved_at": now_iso(), "status": "error",
                "facts": facts, "sources": [],
                "notes": [f"sweep exited {out.returncode}; stderr: {out.stderr[:300]}"]}
    return {"lane": "mailbox", "source": "business mailbox (Graph)",
            "retrieved_at": now_iso(),
            "status": "ok" if hits else "no_record",
            "facts": facts, "sources": [],
            "notes": ["Reuse-by-reference: bin/entity_mail_sweep.py (not copied)."]}


LANE_RUNNERS = {
    "sam": _run_sam,
    "mailbox": _run_mailbox,
}


def run_all(entity: dict, lanes: list | None = None) -> dict:
    lanes = lanes or (API_LANES + ["sam", "mailbox"])
    # Lane modules were written against slightly different key names
    # ("name" vs "legal_name"); normalize once so every lane sees both.
    ent = dict(entity or {})
    ent.setdefault("name", ent.get("legal_name", ""))
    ent.setdefault("legal_name", ent.get("name", ""))
    lane_records = []
    for lane in lanes:
        t0 = time.time()
        try:
            if lane in API_LANES:
                rec = _with_timeout(lambda e: _run_api_lane(lane, e), ent)
            elif lane in LANE_RUNNERS:
                rec = _with_timeout(LANE_RUNNERS[lane], ent)
            else:
                rec = {"lane": lane, "source": "", "retrieved_at": now_iso(),
                       "status": "error", "facts": {},
                       "sources": [], "notes": [f"Unknown lane '{lane}'."]}
        except _LaneTimeout as exc:
            rec = {"lane": lane, "source": "", "retrieved_at": now_iso(),
                   "status": "parked", "facts": {},
                   "sources": [],
                   "notes": [f"{exc} — parked; retry the lane standalone later."]}
        except Exception as exc:  # a lane must never kill the dossier
            rec = {"lane": lane, "source": "", "retrieved_at": now_iso(),
                   "status": "error", "facts": {},
                   "sources": [],
                   "notes": [f"Lane raised: {type(exc).__name__}: {exc}"]}
        rec.setdefault("facts", {})["duration_s"] = rec.get("facts", {}).get(
            "duration_s", round(time.time() - t0, 1))
        lane_records.append(rec)
    dossier = {
        "entity": entity,
        "run_at": now_iso(),
        "tool": "bizintel.py (entity-verification BizIntel suite)",
        "lanes": lane_records,
        "verification_ledger": [
            {"lane": r["lane"], "source": r.get("source", ""),
             "retrieved_at": r.get("retrieved_at", ""),
             "status": r.get("status", "")}
            for r in lane_records
        ],
    }
    return dossier


def summarize(dossier: dict) -> str:
    lines = [f"BizIntel dossier — {dossier['entity']['legal_name']} "
             f"(run {dossier['run_at'][:19]}Z)"]
    for r in dossier["lanes"]:
        f, n = r.get("facts", {}), r.get("status", "?")
        if r["lane"] == "n990":
            lines.append(f"- 990/financials [{n}]: {f.get('subsection_label', '?')}, "
                         f"ruling {f.get('ruling_date', '?')}, "
                         f"latest 990 {f.get('latest_filing_period', 'none on record')}")
        elif r["lane"] == "edgar":
            latest = f.get("filings_latest") or []
            forms = ", ".join(x.get("form", "?") for x in latest[:3]) or "?"
            lines.append(f"- SEC EDGAR [{n}]: {f.get('company_name', '?')}, CIK {f.get('cik', '?')}, "
                         f"SIC {f.get('sic', '?')}, "
                         f"{f.get('filings_recent_count', 0)} recent filings (latest: {forms})")
        elif r["lane"].startswith("ofac"):
            lines.append(f"- Sanctions [{n}]: {f.get('match_summary', f.get('match', '?'))}")
        elif r["lane"].startswith("fec"):
            lines.append(f"- FEC [{n}]: {f.get('committee_count', f.get('count', 0))} committee hit(s)")
        elif r["lane"].startswith("ny") or r["lane"] == "nydos":
            lines.append(f"- NY DOS [{n}]: {f.get('entity_name', f.get('match_summary', '?'))}, "
                         f"status {f.get('status', '?')}")
        elif r["lane"] == "sam":
            lines.append(f"- SAM.gov [{n}]: UEI {f.get('uei', '?')}, "
                         f"CAGE {f.get('cage', '?')}, status {f.get('registration_status', '?')}")
        elif r["lane"] == "mailbox":
            lines.append(f"- Mailbox [{n}]: {f.get('hits_found', f.get('hit_count', '?'))} relevant item(s)")
        else:
            lines.append(f"- {r['lane']} [{n}]")
        for note in (r.get("notes") or [])[:2]:
            lines.append(f"    note: {note[:140]}")
    return "\n".join(lines)


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="BizIntel unified entity investigation.")
    ap.add_argument("--name", required=True, help="Exact legal name of the entity")
    ap.add_argument("--ein", default="", help="EIN (nn-nnnnnnn)")
    ap.add_argument("--state", default="", help="State of formation, e.g. FL")
    ap.add_argument("--type", default="unknown", choices=["nonprofit", "for-profit", "unknown"],
                    help="Entity type")
    ap.add_argument("--ticker", default="", help="Stock ticker (EDGAR lane)")
    ap.add_argument("--cik", default="", help="SEC CIK (EDGAR lane)")
    ap.add_argument("--uei", default="", help="SAM UEI (SAM lane)")
    ap.add_argument("--dos-id", default="", help="NY DOS ID (nydos lane)")
    ap.add_argument("--dba", default="", help="DBA / assumed name")
    ap.add_argument("--doc", default="", dest="doc_number", help="State doc number (lead only)")
    ap.add_argument("--lanes", default=",".join(API_LANES + ["sam", "mailbox"]),
                    help="Comma-separated lane list")
    ap.add_argument("--out", default="", help="Write dossier JSON to this path")
    ap.add_argument("--entity-json", default="", help="Load entity dict from JSON file instead")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.entity_json:
        with open(args.entity_json, encoding="utf-8") as fh:
            entity = json.load(fh)
    else:
        entity = {"legal_name": args.name, "state": args.state, "ein": args.ein,
                  "entity_type": args.type, "ticker": args.ticker, "cik": args.cik,
                  "uei": args.uei, "dos_id": args.dos_id, "dba": args.dba,
                  "doc_number": args.doc_number}
    lanes = [l.strip() for l in args.lanes.split(",") if l.strip()]
    dossier = run_all(entity, lanes)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(dossier, fh, indent=2)
        print(f"Wrote dossier: {args.out}")
    print(summarize(dossier))
    print("\nVerification ledger:")
    for entry in dossier["verification_ledger"]:
        print(f"  {entry['lane']:10s} {entry['status']:10s} {entry['source']} @ {entry['retrieved_at'][:19]}Z")


if __name__ == "__main__":
    main()
