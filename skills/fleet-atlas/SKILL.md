---
name: fleet-atlas
description: "Map a Cloudflare-backed fleet into a typed index of workers, zones, apps, skills, and schedules; find orphans and double-builds; and run a read-only Warden sweep that answers what exists, how it connects, and whether it is healthy. Use when inventorying an estate, after adding or retiring services, or when a health verdict must distinguish a real outage from a gated, unknown, or silently-degraded surface."
license: MIT
compatibility: "Requires Python 3.10+ (stdlib only) and CLOUDFLARE_API_TOKEN plus CLOUDFLARE_ACCOUNT_ID in the environment for recon."
metadata:
  version: 1.0.0
---

# Fleet Atlas

The single map of a whole fleet, and the caretaker that watches it. Answers "what exists, how does it connect, and is it healthy?"

The skill consumes an estate's existing monitors and surfaces — it does not replace them. All estate-specific values (account, probe maps, gate invariants) arrive through environment variables and one local config file; nothing about a specific fleet is baked into the code.

## Configuration

| Variable | Used by | Meaning |
|---|---|---|
| `CLOUDFLARE_API_TOKEN` | recon | Token with read scope on Workers scripts and zones |
| `CLOUDFLARE_ACCOUNT_ID` | recon | The account to inventory |
| `FLEET_ATLAS_DIR` | both | Where `index.json`, `warden_status.json`, and `warden_config.json` live (default `./fleet-atlas`) |
| `WORKERS_DEV_SUBDOMAIN` | sweep | Your workers.dev subdomain, e.g. `myteam.workers.dev`, for building probe URLs |

`warden_config.json` (in `FLEET_ATLAS_DIR`, all keys optional) carries the per-estate probe knowledge:

```json
{
  "rich_probes":   {"my-worker": "/health"},
  "url_overrides": {"custom-domain-only": "https://example.com/"},
  "red_gates":     [{"worker": "my-worker", "method": "GET", "path": "/api/live/probe", "expect": 403}]
}
```

## The ontology (schema)
NODE TYPES: Agent, Worker, App, Skill, Schedule, Credential, REDGate, LiveSurface, Zone, Lane, Sprint. Each node: id · type · owner · subsystem · status · last_seen · health_probe · provenance.
EDGE TYPES: owns, exposes, depends_on, monitors, gates, supersedes, spawned_by, houses.
The graph lets the Warden answer: if this worker dies what goes dark (depends_on)? what has no monitor (missing `monitors` edge = orphan)? what is a stale duplicate (supersedes)? which live surface is ungated (LiveSurface with no REDGate)?

## Recon — bin/atlas_recon.py
Inventories workers + zones into a typed index.
```
CLOUDFLARE_API_TOKEN=<token> CLOUDFLARE_ACCOUNT_ID=<account-id> python3 bin/atlas_recon.py
```
The token needs read scope on workers/zones. Workers are grouped into subsystems by the prefix before the first `-` in the name (edit the classifier if your estate groups differently). An index is a snapshot: run a fresh recon before trusting any sweep built on an old one.

## The Warden — bin/warden_sweep.py (read-only surveillance)
Each cycle:
```
python3 bin/warden_sweep.py   # reads index.json, writes warden_status.json (byte-verified after write)
```
What one sweep does (never mutates what it watches, never arms anything):
1. Loads the index and walks EVERY indexed worker.
2. RICH probes (workers listed in `rich_probes`): each has a REAL JSON health surface. Judgment: `overall` HEALTHY→ok else warn · `ok` true→ok false→warn · `status` ok/online/healthy→ok · version-only page→ok. **A declared health endpoint that stops serving truthful JSON grades WARN even if bytes still flow — a 200 alone is never health** (the SPA-fallback trap).
3. GENERIC liveness for everything else: any HTTP answer = alive (4xx = healthy gate), 5xx = down, silence = unknown — never faked green.
4. URL overrides for custom-domain-only workers.
5. Verifies RED-GATE invariants EXTERNALLY (from `red_gates` in the config): a gated endpoint must keep returning its expected status. A moved gate marks the node down — automatic P0.
6. Prints `SWEEP-VERDICT: CLEAN — stay silent` or `TROUBLE — alert the operator`.

Alert law: silent on clean; surface only down nodes, moved RED gates, or a failed status write.

## Growing the map
Add rich probes, URL overrides, and RED gates to `warden_config.json`; re-run recon to refresh the index when workers are added or retired (the sweep follows the index automatically).

## Operating rules
- The index is the source of truth the sweep follows. Re-run recon after any estate change (new worker, retired worker, new zone).
- A sweep is read-only. It never deploys, never flips a gate, never arms anything.
- Unknown is reported as unknown — never faked green.
