#!/usr/bin/env python3
"""FLEET ATLAS recon — inventory a Cloudflare estate into a typed index + gaps.

Usage:
  CLOUDFLARE_API_TOKEN=<token> CLOUDFLARE_ACCOUNT_ID=<account-id> \
    python3 bin/atlas_recon.py

The token needs read scope on Workers scripts and zones. Writes the index to
$FLEET_ATLAS_DIR/index.json (default ./fleet-atlas/index.json). If an
agents.json roster exists in the working directory it is folded in and
duplicate agent names are reported as a gap.

Workers are grouped into subsystems by the prefix before the first "-" in
their name (names without a prefix land in UNCLASSIFIED) — rename the
grouping function if your estate uses a different convention.
"""
import json, os, urllib.request, datetime, sys

ACCT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
TOK = os.environ.get("CLOUDFLARE_API_TOKEN", "")
OUT_DIR = os.environ.get("FLEET_ATLAS_DIR", os.path.join(os.getcwd(), "fleet-atlas"))

def api(path):
    r = urllib.request.Request(f"https://api.cloudflare.com/client/v4{path}", headers={"Authorization": "Bearer " + TOK})
    return json.loads(urllib.request.urlopen(r, timeout=40).read())

def subsystem(w):
    return w.split("-")[0].upper() if "-" in w else "UNCLASSIFIED"

ONTOLOGY = {"node_types": ["Agent", "Worker", "App", "Skill", "Schedule", "Credential", "REDGate", "LiveSurface", "Zone", "Lane", "Sprint"],
  "edge_types": ["owns", "exposes", "depends_on", "monitors", "gates", "supersedes", "spawned_by", "houses"],
  "node_fields": ["id", "type", "owner", "subsystem", "status", "last_seen", "health_probe", "provenance"]}

def main():
    if not ACCT or not TOK:
        print("error: set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN in the environment", file=sys.stderr)
        return 2
    workers = sorted(s["id"] for s in (api(f"/accounts/{ACCT}/workers/scripts").get("result") or []))
    zones = sorted(z["name"] for z in (api("/zones").get("result") or []))
    clusters = {}
    for w in workers: clusters.setdefault(subsystem(w), []).append(w)
    agents = json.load(open("agents.json")) if os.path.exists("agents.json") else []
    names = [a.get("name") for a in agents]
    dups = sorted({n for n in names if names.count(n) > 1})
    idx = {"atlas_version": "v0", "generated": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
      "counts": {"workers": len(workers), "zones": len(zones), "agents": len(agents), "subsystems": len(clusters)},
      "ontology": ONTOLOGY,
      "subsystems": {k: sorted(v) for k, v in sorted(clusters.items(), key=lambda x: -len(x[1]))},
      "zones": zones, "agents": agents,
      "gaps": {"duplicate_agents": dups, "unclassified_workers": clusters.get("UNCLASSIFIED", []),
              "note": "per-worker monitor coverage is UNKNOWN until the Warden probes each node"}}
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "index.json")
    json.dump(idx, open(out, "w"), indent=1)
    print(f"index written: {out} ({len(workers)} workers, {len(zones)} zones)")

if __name__ == "__main__":
    sys.exit(main())
