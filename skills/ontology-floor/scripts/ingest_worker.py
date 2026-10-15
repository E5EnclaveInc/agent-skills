#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INGEST worker (path A) — self-updating floor, agent-only.

Per run: SOURCE (arXiv + any parseable reference source) -> EXTRACT (Workers AI
Llama -> draft Grounding Record) -> GATE S + GATE F via the existing
ingest_gate.promote() -> PROMOTE (write to R2/D1/Vectorize) or QUARANTINE (reason)
-> AUDIT (append-only) -> advance watermark. Fail-closed: default is quarantine.

DRY RUN (INGEST_DRY=1, default): runs SOURCE->EXTRACT->GATES and prints the
promote/quarantine verdict per candidate; the R2/D1/Vectorize writes are described
("would write"), not executed. Live model calls (extract + gates) use Workers AI,
so run via the Cloudflare (Global) skill. Set INGEST_DRY=0 to actually write.
"""
import os, re, json, time, hashlib, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import ingest_gate as ig
from ingest_gate import promote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eval_out"); os.makedirs(OUT, exist_ok=True)
SEED = json.load(open(os.path.join(HERE, "seed_corpus.json")))
ACCT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "fd98d813898e36431c9d6af3b0beeb20")
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
MODEL = os.environ.get("ONTOLOGY_EVAL_MODEL", "@cf/meta/llama-3.1-8b-instruct-fp8")
CAP = int(os.environ.get("INGEST_CAP", "5"))
DRY = os.environ.get("INGEST_DRY", "1") == "1"
WATERMARK = os.path.join(OUT, "ingest_watermark.json")
AUDIT = os.path.join(OUT, "ingest_audit.jsonl")

# domain -> an EXISTING parent node in the seed graph (keeps GATE S connectivity valid;
# shallow auto-placement, tier 2). Schema domain must be physical|formal|ethical.
DOMAIN_PARENT = {"physical": "matter", "formal": "formal", "information": "information"}
DOMAIN_OUT = {"physical": "physical", "formal": "formal", "information": "formal"}

# --- SOURCE ------------------------------------------------------------------
def fetch_arxiv(cats, n):
    q = "https://export.arxiv.org/api/query?search_query=%s&sortBy=submittedDate&sortOrder=descending&max_results=%d" % (
        "+OR+".join("cat:" + c for c in cats), n)
    req = urllib.request.Request(q, headers={"User-Agent": "ontology-ingest/1.0"})
    xml = urllib.request.urlopen(req, timeout=30).read()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(xml).findall("a:entry", ns):
        out.append({"origin": "arxiv",
                    "id": e.findtext("a:id", "", ns).strip().split("/")[-1],
                    "title": " ".join(e.findtext("a:title", "", ns).split()),
                    "abstract": " ".join(e.findtext("a:summary", "", ns).split())})
    return out

# "any parseable source" — a couple of clean formula-reference snippets (the non-arXiv
# branch), to exercise the PROMOTE path honestly alongside messy abstracts.
REFERENCE_SOURCES = [
    {"origin": "ref", "id": "ref:gini",
     "title": "Gini coefficient (inequality measure)",
     "abstract": "The Gini coefficient is defined as G = (sum_i sum_j |x_i - x_j|) / (2 n^2 mu), where mu is the mean; 0 = perfect equality, 1 = maximal inequality."},
    {"origin": "ref", "id": "ref:cagr",
     "title": "Compound annual growth rate",
     "abstract": "CAGR = (ending_value / beginning_value)^(1/years) - 1, the smoothed annualized growth rate over a period."},
    {"origin": "ref", "id": "ref:ke",
     "title": "Kinetic energy",
     "abstract": "Kinetic energy is KE = 1/2 m v^2, the energy of a mass m moving at speed v."},
    {"origin": "ref", "id": "ref:newton2",
     "title": "Newton's second law",
     "abstract": "Newton's second law states F = m a: force equals mass times acceleration."},
]

# --- EXTRACT (LLM -> draft record) ------------------------------------------
def chat(system, user):
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (ACCT, MODEL)
    body = json.dumps({"messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}],
                       "temperature": 0.0, "max_tokens": 200}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + TOKEN, "Content-Type": "application/json",
        "User-Agent": "ontology-ingest/1.0"})
    try:
        raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    except Exception as e:
        try:
            raw = e.read().decode("utf-8", "replace")   # HTTPError body
        except Exception:
            raw = '{"error":"%s"}' % e
    try:
        j = json.loads(raw)
    except Exception:
        return ""
    res = j.get("result") or {}
    resp = res.get("response")
    if isinstance(resp, str) and resp.strip():
        return resp
    if isinstance(resp, (dict, list)):          # some models return parsed JSON here
        return json.dumps(resp)
    try:                                         # OpenAI-style choices fallback
        c = res["choices"][0]["message"]["content"]
        if isinstance(c, str) and c.strip():
            return c
    except Exception:
        pass
    if not j.get("success", True):
        print("   [chat error] " + raw[:160])
    return ""

def extract(src):
    sysp = ("You extract ONE named formalism from a title+abstract. If it centers on a "
            "NAMED formula/metric/law with EXPLICIT math, output compact JSON: "
            '{"term":"snake_case_name","math":"the equation","domain":"physical|formal|information"}. '
            'If there is no explicit named formula, output {"none":true}. Output ONLY JSON.')
    txt = chat(sysp, (src["title"] + ". " + src["abstract"])[:1200]) or ""
    m = re.search(r"\{.*\}", txt, re.DOTALL)
    if not m:
        return None
    try:
        j = json.loads(m.group(0))
    except Exception:
        return None
    if j.get("none") or not j.get("term") or not j.get("math"):
        return None
    return j

def draft_record(j, src):
    dom_in = (j.get("domain") or "formal").lower()
    if dom_in not in DOMAIN_PARENT:
        dom_in = "formal"
    parent = DOMAIN_PARENT[dom_in]
    term = re.sub(r"[^a-z0-9_]+", "_", j["term"].strip().lower()).strip("_") or "unnamed"
    h = hashlib.sha256((term + j["math"]).encode()).hexdigest()
    return {"term": term, "canonical_id": "GR-ing-" + h[:10],
            "tier": 2, "root_path": ["E", parent], "domain": DOMAIN_OUT[dom_in],
            "math": j["math"], "proof_kind": "definition",
            "provenance": src["origin"] + ":" + src["id"],
            "corroboration": [{"source": src["id"], "kind": "source_text"}],
            "sha256": h, "verifiable": False}

# --- WRITE LAYER (R2 / D1 / Vectorize) — executed only when not DRY ----------
def write_stores(rec):
    # Live persistence to owned Cloudflare: R2 (record) + D1 (index) + Vectorize (embedding).
    try:
        import cf_stores
        res = cf_stores.write_record(rec)
        return "R2 %s · D1 %s · Vec %s" % (res["r2"], res["d1"], res["vectorize"])
    except Exception as e:
        return "write error: %s" % e

def load_watermark():
    # LIVE runs use the shared R2 watermark (dedups across days / fresh threads);
    # DRY runs use a local file so they never touch shared state.
    if not DRY:
        try:
            import cf_stores
            return cf_stores.load_watermark()
        except Exception:
            pass
    if os.path.exists(WATERMARK):
        return json.load(open(WATERMARK))
    return {"seen": []}

def run():
    print("INGEST worker  | model=%s | cap=%d | mode=%s\n" % (MODEL, CAP, "DRY" if DRY else "LIVE"))
    wm = load_watermark(); seen = set(wm.get("seen", []))
    sources = REFERENCE_SOURCES + fetch_arxiv(["math.HO", "stat.ML", "cs.LG"], 8)
    audit = open(AUDIT, "a")
    processed = promoted = quarantined = skipped = deduped = 0
    print("%-22s %-7s %-11s %s" % ("term", "origin", "verdict", "detail"))
    print("-" * 78)
    for src in sources:
        if processed >= CAP:
            break
        if src["id"] in seen:
            deduped += 1
            continue
        j = extract(src)
        if not j:
            skipped += 1
            seen.add(src["id"])   # mark seen so we don't re-extract it every run
            continue
        rec = draft_record(j, src)
        out = promote(rec, SEED)          # GATE S -> GATE F, fail-closed
        processed += 1
        verified = out["status"] == "verified"
        if verified:
            promoted += 1
            detail = write_stores(out) if not DRY else "would write to R2/D1/Vectorize"
        else:
            quarantined += 1
            detail = out.get("quarantine_reason", "")[:46]
        seen.add(src["id"])
        audit.write(json.dumps({"ts": time.time(), "src": src["id"], "term": rec["term"],
                                "status": out["status"], "reason": out.get("quarantine_reason", "")}) + "\n")
        print("%-22s %-7s %-11s %s" % (rec["term"][:21], src["origin"], out["status"], detail))
    audit.close()
    wm_where = WATERMARK + "  [dry: local]"
    if not DRY:
        try:
            import cf_stores
            st = cf_stores.save_watermark({"seen": sorted(seen)})
            wm_where = "R2 %s (HTTP %s)" % (cf_stores.WM_KEY, st)
        except Exception as e:
            wm_where = "R2 save FAILED: %s" % e
    print("-" * 78)
    print("processed %d | promoted %d | quarantined %d | skipped(no-formula) %d | deduped(already-seen) %d" %
          (processed, promoted, quarantined, skipped, deduped))
    print("watermark: %s (%d seen)" % (wm_where, len(seen)))


if __name__ == "__main__":
    run()
