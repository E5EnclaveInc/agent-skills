# THE WARDEN SWEEP — Fleet Atlas.
# Walk every indexed worker, probe it, write warden_status.json next to the index.
# READ-ONLY surveillance: never mutates what it watches, never arms anything.
# Run: python3 bin/warden_sweep.py
# The index is rebuilt with bin/atlas_recon.py (needs CLOUDFLARE_API_TOKEN).
#
# Estate-specific probe configuration lives in $FLEET_ATLAS_DIR/warden_config.json
# (all keys optional):
#   {
#     "rich_probes":   {"my-worker": "/health", ...},
#     "url_overrides": {"custom-only-worker": "https://example.com/", ...},
#     "red_gates":     [{"worker": "my-worker", "method": "GET",
#                        "path": "/api/live/probe", "expect": 403}, ...]
#   }
# Generic probes are built as https://<worker>.<WORKERS_DEV_SUBDOMAIN><path>;
# set WORKERS_DEV_SUBDOMAIN in the environment (e.g. "myteam.workers.dev").
import json, os, sys, time, datetime, hashlib, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

ATLAS_DIR = os.environ.get("FLEET_ATLAS_DIR", os.path.join(os.getcwd(), "fleet-atlas"))
INDEX_PATH = os.path.join(ATLAS_DIR, "index.json")
STATUS_PATH = os.path.join(ATLAS_DIR, "warden_status.json")
CONFIG_PATH = os.path.join(ATLAS_DIR, "warden_config.json")

SUBDOMAIN = os.environ.get("WORKERS_DEV_SUBDOMAIN", "")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) FleetAtlas-Warden/1.1"
TIMEOUT = 12

def _load_config():
    try:
        with open(CONFIG_PATH) as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}

_CONFIG = _load_config()
# RICH probes — workers with REAL JSON health surfaces. A rich probe demands a
# parsing JSON answer with truthful fields; a 200 alone is not health (the
# SPA-fallback trap). Generic liveness covers everything not listed here.
RICH = _CONFIG.get("rich_probes", {})
# Workers that only serve on a custom domain (workers.dev root is route-scoped).
URL_OVERRIDE = _CONFIG.get("url_overrides", {})
# RED-gate invariants the Warden verifies EXTERNALLY every sweep (the worker
# cannot self-probe its own origin). Wrong answer here is an automatic ALARM.
# RED-gate invariants the Warden verifies EXTERNALLY every sweep (the worker
# cannot self-probe its own origin). Configured per estate in warden_config.json
# as {"worker", "method", "path", "expect"} entries; empty by default.
RED_GATES = [
    (g["worker"], g.get("method", "GET"), g["path"], g["expect"])
    for g in _CONFIG.get("red_gates", [])
]

def fetch(url, method="GET"):
    req = urllib.request.Request(url, method=method)
    req.add_header("User-Agent", UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read()[:4096]
    except urllib.error.HTTPError as e:
        return e.code, (e.read()[:4096] if e.fp else b"")
    except Exception as e:
        return None, str(e)[:160].encode()

def classify_liveness(code):
    """Any HTTP answer = alive; 4xx = gated/no public route (a healthy gate)."""
    if code is None: return "unknown"
    if code >= 500: return "down"
    return "ok"

def judge_health_json(j):
    """Truthful-field interpretation of a rich health payload."""
    if "overall" in j:                       # AUGUR-style aggregate
        return ("ok" if j["overall"] == "HEALTHY" else "warn"), j.get("overall")
    if "ok" in j:
        return ("ok" if j["ok"] is True else "warn"), None
    s = str(j.get("status", "")).lower()
    if s in ("ok", "online", "healthy", "up"):
        return "ok", None
    if s:
        return "warn", s
    return "ok", None                        # version-only health page: parses = serving

def probe(name):
    t0 = time.time()
    rich = name in RICH
    if name in URL_OVERRIDE:
        url, path = URL_OVERRIDE[name], URL_OVERRIDE[name]
    elif not SUBDOMAIN:
        return name, {"status": "unknown", "http": None, "probe": RICH.get(name, "/"),
                      "ms": 0, "rich": rich,
                      "note": "WORKERS_DEV_SUBDOMAIN not set and no url_overrides entry — cannot build a probe URL"}
    else:
        path = RICH.get(name, "/")
        url = f"https://{name}.{SUBDOMAIN}{path}"
    code, body = fetch(url)
    ms = int((time.time() - t0) * 1000)
    node = {"status": classify_liveness(code), "http": code, "probe": path, "ms": ms, "rich": rich}
    if rich:
        healthy_json = False
        if code == 200:
            try:
                j = json.loads(body)
                if isinstance(j, dict):
                    node["status"], extra = judge_health_json(j)
                    if extra: node["overall"] = extra
                    if "alarm_count" in j: node["alarms"] = j["alarm_count"]
                    if "version" in j: node["v"] = str(j["version"])[:24]
                    healthy_json = True
            except Exception:
                pass
        if not healthy_json:
            # A declared health endpoint that stops answering truthfully is WARN even if
            # the origin still serves bytes — the surface regressed. Silence stays unknown.
            node["status"] = "warn" if code is not None else "unknown"
            node["note"] = f"rich health endpoint {path} not serving JSON (http {code})"
    elif code is None:
        node["note"] = body.decode(errors="replace")
    return name, node

def main():
    assert os.path.exists(INDEX_PATH), f"atlas index missing: {INDEX_PATH} — run bin/atlas_recon.py first"
    atlas = json.load(open(INDEX_PATH))
    workers = sorted({w for names in atlas["subsystems"].values() for w in names})
    print(f"warden sweep: {len(workers)} indexed workers · {len(RICH)} rich probes", flush=True)

    t0 = time.time()
    nodes = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        for name, node in ex.map(probe, workers):
            nodes[name] = node

    # RED-gate external verification (a LiveSurface gate that moves is P0)
    red = []
    for wname, method, path, want in RED_GATES:
        if wname in URL_OVERRIDE:
            base = URL_OVERRIDE[wname].rstrip("/")
            code, _ = fetch(base + path, method=method)
            holds = (code == want)
        elif SUBDOMAIN:
            code, _ = fetch(f"https://{wname}.{SUBDOMAIN}{path}", method=method)
            holds = (code == want)
        else:
            code, holds = None, None  # no probe URL can be built — not verifiable
        red.append({"worker": wname, "path": path, "expect": want, "got": code, "holds": holds})
        if holds is False and wname in nodes:
            nodes[wname]["status"] = "down"
            nodes[wname]["note"] = f"RED GATE MOVED: {path} returned {code}, expected {want}"

    tally = {"ok": 0, "warn": 0, "down": 0, "unknown": 0}
    for n in nodes.values(): tally[n["status"]] += 1
    attention = sorted([f"{k}: {v['status']} (http {v.get('http')})" + (f" — {v['note']}" if v.get("note") else "")
                        for k, v in nodes.items() if v["status"] in ("down", "warn")])

    status = {
        "swept_at": datetime.datetime.utcnow().isoformat() + "Z",
        "warden": "Fleet Atlas Warden",
        "atlas_version": atlas.get("atlas_version"),
        "workers_indexed": len(workers),
        "rich_probes": len(RICH),
        "sweep_seconds": round(time.time() - t0, 1),
        "tallies": tally,
        "red_gates": red,
        "attention": attention,
        "nodes": nodes,
        "law": "Read-only surveillance. Unknown is reported as unknown — never faked green.",
    }
    os.makedirs(ATLAS_DIR, exist_ok=True)
    payload = json.dumps(status, indent=1).encode()
    with open(STATUS_PATH, "wb") as f:
        f.write(payload)
    back = open(STATUS_PATH, "rb").read()
    ok = hashlib.sha256(back).hexdigest() == hashlib.sha256(payload).hexdigest()
    print(f"status write byte-verified: {ok} -> {STATUS_PATH}", flush=True)

    print(json.dumps({"tallies": tally, "red_gates_hold": not any(r["holds"] is False for r in red),
                      "attention": attention[:20]}, indent=1), flush=True)
    # Alert law: silent when clean; this exit signal is the trouble flag.
    trouble = tally["down"] > 0 or any(r["holds"] is False for r in red)
    print("SWEEP-VERDICT:", "TROUBLE — alert the operator" if trouble else "CLEAN — stay silent", flush=True)

if __name__ == "__main__":
    main()
