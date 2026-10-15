#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ontology Floor — INGESTION GATES.

Two checks stand between a freshly-ingested Grounding Record and the trusted
cache. Both must PASS or the record is quarantined (fail-closed). They answer the
two disconfirming findings from the arXiv sweep:

  GATE S  (structural)   -> "Structural Hallucination in LLMs" (arXiv:2603.01341):
                            LLMs keep local facts but distort GRAPH structure.
                            => tier / root_path / edges are validated SYMBOLICALLY,
                               never trusted from the generating model, and each
                               structural edge needs a non-LLM corroborating signal.

  GATE F  (faithfulness) -> the Faithfulness Gap (BPF / roundtrip autoformalization,
                            AAAI/ICML 2026): a formalism can be PROVABLE yet encode
                            a DIFFERENT meaning than the word. Full NL<->formal
                            equivalence is impossible in principle, so we do
                            DRIFT DETECTION (contrastive + roundtrip), not a proof
                            of equivalence.

Promotion:  ingested --GateS--> --GateF--> verified | quarantined
Ethical-domain records carry no math: they skip S/F math checks and are routed to
the governance ceiling (status 'governed'), per the floor's hard rule.

A 'verified' floor record is still a CLAIM the ceiling's Phantom-Aid gate re-checks
(defense in depth). Symbolic authority here is a VETO, not advice
(per the 2026 clinical neuro-symbolic review: gains rise with symbolic authority).

STDLIB ONLY, Python 3.9+. '# PROD:' marks where a real second model / KG plugs in.
"""

import os, sys, json, re, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.environ.get("ONTOLOGY_CORPUS", os.path.join(HERE, "seed_corpus.json"))

PASS, DRIFT, FAIL = "PASS", "DRIFT", "FAIL"
# Calibrated to BGE embeddings, which have a high similarity floor (~0.5 even for
# unrelated short phrases): so thresholds sit well above 0.5. These are
# EMBED_MODEL-specific and empirically set from observed separation.
SEM_PASS = 0.72            # semantic cosine: >= -> PASS-eligible
SEM_DRIFT = 0.60           # [SEM_DRIFT, SEM_PASS) -> DRIFT ; < -> FAIL
CONTRAST_MARGIN = 0.02     # advisory: true binding should beat the best near-miss
STOPWORDS = set("the a an of to and or is are be as in on for with by that this it".split())


# ---------------------------------------------------------------------------
# GATE S -- symbolic structural validation (deterministic; no LLM)
# ---------------------------------------------------------------------------
def build_graph(records):
    """Edges from every record's root_path consecutive pairs -> the committed DAG."""
    edges = set()
    nodes = set()
    for r in records:
        rp = r.get("root_path", [])
        for n in rp:
            nodes.add(n)
        for a, b in zip(rp, rp[1:]):
            edges.add((a, b))
    return nodes, edges


def structural_validate(rec, nodes, edges):
    reasons = []
    rp = rec.get("root_path", [])
    tier = rec.get("tier")

    # 1. rooted at E
    root_ok = bool(rp) and rp[0] == "E"
    if not root_ok:
        reasons.append("root_path does not start at Tier-1 root 'E'")

    # 2. tier == depth (Tier 1 == [E])
    tier_ok = isinstance(tier, int) and tier == len(rp)
    if not tier_ok:
        reasons.append("tier (%s) != len(root_path) (%d)" % (tier, len(rp)))

    # 3. acyclic: no repeated node on the path (simple cycle guard)
    acyclic = len(set(rp)) == len(rp)
    if not acyclic:
        reasons.append("root_path repeats a node (cycle)")

    # 4. connectivity: every edge exists in the committed graph OR is self-declared
    #    by this record's own path (co-ingested). A parent invented out of nowhere
    #    that contradicts the graph is rejected.
    edge_ok = True
    for a, b in zip(rp, rp[1:]):
        if (a, b) not in edges and a not in nodes and a != "E":
            edge_ok = False
            reasons.append("edge %s->%s has no counterpart in the ontology" % (a, b))

    # 5. corroboration: each structural placement needs a NON-LLM signal.
    #    provenance (the source text) counts as one; extra sources add more.
    #    'LLM-asserted' / empty provenance => fabrication risk => fail.
    prov = (rec.get("provenance") or "").strip().lower()
    corr = rec.get("corroboration", [])
    non_llm = 0
    if prov and "llm-asserted" not in prov and "unverified" not in prov:
        non_llm += 1
    non_llm += len([c for c in corr if c.get("kind") != "llm"])
    corr_ok = non_llm >= 1
    if not corr_ok:
        reasons.append("no non-LLM corroboration for structural placement")

    ok = root_ok and tier_ok and acyclic and edge_ok and corr_ok
    return {
        "dag_ok": bool(root_ok and acyclic and edge_ok),
        "tier_consistent": bool(tier_ok),
        "acyclic": bool(acyclic),
        "corroboration_signals": non_llm,
        "status": PASS if ok else FAIL,
        "reasons": reasons,
    }


# ---------------------------------------------------------------------------
# GATE F -- faithfulness of the word->math binding (contrastive + roundtrip)
# ---------------------------------------------------------------------------
def _kw(s):
    toks = re.split(r"[^a-z0-9]+", (s or "").lower())
    return set(t for t in toks if t and t not in STOPWORDS and not t.isdigit())


def _meaningful(kw):
    """Drop short/symbol-like tokens (e, mc2, x) for the meaning comparison;
    symbol fidelity is judged separately by _symbols_grounded."""
    m = set(t for t in kw if len(t) >= 3 and not any(c.isdigit() for c in t))
    return m or kw


# --- back-translation backend (model diversity: a DIFFERENT family than the
#     producer). Real path = Cloudflare Workers AI (Llama), non-metered within the
#     free neuron tier -> honors the zero-recurring-cost mandate. Mock fallback
#     keeps the offline selftest deterministic. ----------------------------------
BACKEND = "workers_ai" if os.environ.get("CLOUDFLARE_API_TOKEN") else "mock"
BT_MODEL = os.environ.get("ONTOLOGY_BT_MODEL", "@cf/meta/llama-3.1-8b-instruct-fp8")
_BT_CACHE = {}

def _mock_back_translate(math):
    m = math or ""
    if "mc^2" in m or "mc2" in m.replace(" ", ""):
        return "mass energy equivalence rest energy"
    if "P(H|E)" in m or "P(E|H)" in m:
        return "conditional probability posterior update bayes"
    if "H(X)" in m and "log" in m:
        return "shannon entropy expected uncertainty information"
    if "H2O" in m:
        return "water molecule two hydrogen one oxygen"
    if "TV(" in m or "Delta/2" in m:
        return "in context learning prompt distribution convergence bound"
    if "2^{aleph_0}" in m or "aleph" in m:
        return "cantor set uncountable cardinality measure zero"
    return "unknown formal statement"

def _workers_ai_translate(math):
    import urllib.request, urllib.error
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "fd98d813898e36431c9d6af3b0beeb20")
    token = os.environ["CLOUDFLARE_API_TOKEN"]
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (acct, BT_MODEL)
    sys_p = ("You are a formal-methods translator. Given ONE mathematical or formal "
             "statement, reply with ONLY a terse lowercase noun phrase (4-10 words) "
             "naming the concept it defines. No punctuation, no preamble, no restating "
             "the formula. If it is meaningless or garbled, reply exactly: garbled.")
    body = json.dumps({"messages": [{"role": "system", "content": sys_p},
                                    {"role": "user", "content": str(math)}],
                       "max_tokens": 32, "temperature": 0.0}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json",
        "User-Agent": "ontology-floor/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        j = json.loads(resp.read().decode("utf-8"))
    out = (j.get("result") or {}).get("response", "")
    return out.strip().lower()

def back_translate(math):
    """math -> NL concept, via a different model family. Fail-safe to mock."""
    if BACKEND == "mock":
        return _mock_back_translate(math)
    if math in _BT_CACHE:
        return _BT_CACHE[math]
    try:
        out = _workers_ai_translate(math) or _mock_back_translate(math)
    except Exception:
        out = _mock_back_translate(math)   # fail-safe: never crash ingestion
    _BT_CACHE[math] = out
    return out


# --- semantic comparator: Workers AI embeddings (BGE) cosine. Lexical overlap is
#     the offline-mock fallback only. This is what makes gravitation~gravitational
#     and "softmax function"~softmax match. --------------------------------------
EMBED_MODEL = os.environ.get("ONTOLOGY_EMBED_MODEL", "@cf/baai/bge-base-en-v1.5")
_EMB_CACHE = {}

def _embed(texts):
    import urllib.request
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "fd98d813898e36431c9d6af3b0beeb20")
    token = os.environ["CLOUDFLARE_API_TOKEN"]
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (acct, EMBED_MODEL)
    body = json.dumps({"text": texts}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json",
        "User-Agent": "ontology-floor/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        j = json.loads(resp.read().decode("utf-8"))
    return (j.get("result") or {}).get("data") or []

def _embed_one(t):
    if t in _EMB_CACHE:
        return _EMB_CACHE[t]
    v = _embed([t])[0]
    _EMB_CACHE[t] = v
    return v

def _cosine(u, v):
    dot = sum(a * b for a, b in zip(u, v))
    nu = sum(a * a for a in u) ** 0.5
    nv = sum(b * b for b in v) ** 0.5
    return dot / (nu * nv) if nu and nv else 0.0

def _lexical_sim(a, b):
    am, bm = _meaningful(_kw(a)), _meaningful(_kw(b))
    return len(am & bm) / max(1, len(am))

def _sem_sim(a, b):
    """Semantic similarity in [0,1]. Embeddings when live, lexical when mock."""
    if BACKEND == "mock":
        return _lexical_sim(a, b)
    try:
        c = _cosine(_embed_one(a), _embed_one(b))
        return max(0.0, min(1.0, c))
    except Exception:
        return _lexical_sim(a, b)   # fail-safe

def _term_text(rec):
    t = rec.get("term", "").replace("_", " ")
    al = [a.replace("_", " ") for a in rec.get("aliases", []) if not any(c.isdigit() for c in a)]
    return (t + " " + " ".join(al[:2])).strip() if al else t


def _symbols_grounded(math, index):
    """Every meaningful identifier in the math should resolve to a cached term or
    be a declared primitive/operator. Returns (fraction_grounded, ungrounded[])."""
    ids = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", math or ""))
    primitives = {"log", "sum", "max", "min", "exp", "int", "lim", "aleph",
                  "union", "open", "measure", "middle", "thirds", "prompt",
                  "delim", "theta", "tau", "probe", "ensemble", "screen"}
    checked, grounded, ungrounded = 0, 0, []
    for tok in ids:
        t = tok.lower()
        if t in primitives:
            continue
        checked += 1
        if t in index or difflib.get_close_matches(t, list(index.keys()), n=1, cutoff=0.9):
            grounded += 1
        else:
            ungrounded.append(tok)
    frac = 1.0 if checked == 0 else grounded / checked
    return frac, ungrounded


def faithfulness_check(rec, index, near_misses=None):
    math = rec.get("math", "")
    term_text = _term_text(rec)

    # (a) roundtrip: math -> NL' (via a DIFFERENT model family), then compare
    #     SEMANTICALLY (embedding cosine) to the term. Drift detection.
    bt = back_translate(math)
    round_sim = _sem_sim(term_text, bt)

    # (b) contrastive: the true binding must beat every near-miss corruption,
    #     now on semantic distance. Easier to detect wrong than prove right (BPF).
    near_misses = near_misses if near_misses is not None else _default_near_misses(math)
    nm_top = 0.0
    for nm in near_misses:
        nm_top = max(nm_top, _sem_sim(term_text, back_translate(nm)))
    beats_all = round_sim > nm_top + CONTRAST_MARGIN

    # (c) symbol grounding
    sym_frac, ungrounded = _symbols_grounded(math, index)

    # Absolute semantic separation is the primary gate (near-miss contrast is noisy
    # in embedding space, so it is reported/advisory, not a hard PASS condition).
    status = PASS if (round_sim >= SEM_PASS and sym_frac >= 0.5) else \
             (DRIFT if round_sim >= SEM_DRIFT else FAIL)
    return {
        "score": round(round_sim, 3),
        "roundtrip_sim": round(round_sim, 3),
        "back_translation": bt,
        "beats_near_misses": beats_all,
        "near_miss_top": round(nm_top, 3),
        "symbols_grounded": round(sym_frac, 3),
        "ungrounded_symbols": ungrounded,
        "comparator": ("embedding-cosine %s" % EMBED_MODEL) if BACKEND != "mock" else "lexical-overlap (mock)",
        "method": "roundtrip+contrastive+symbol-grounding via %s" % (BT_MODEL if BACKEND != "mock" else "mock"),
        "status": status,
    }


def _default_near_misses(math):
    """Cheap corruptions of the math to test the discriminator (generic)."""
    if not math:
        return []
    nm = []
    if "+" in math:
        nm.append(math.replace("+", "-", 1))            # flip an operator
    m2 = re.sub(r"\^?2\b", "3", math, count=1)          # perturb an exponent/number
    if m2 != math:
        nm.append(m2)
    nm.append(math[::-1])                                # reversed -> garbled concept
    # pattern-specific decoys (help when the formula is one of the classics)
    nm.append(re.sub(r"P\(H\|E\)", "P(E|H)", math))
    return [x for x in dict.fromkeys(nm) if x and x != math]


# ---------------------------------------------------------------------------
# Promotion
# ---------------------------------------------------------------------------
def promote(rec, records):
    out = dict(rec)
    if rec.get("domain") == "ethical":
        out["status"] = "governed"
        out["verifiable"] = False
        out["gate_note"] = "value term: skips S/F, routed to governance ceiling"
        return out
    nodes, edges = build_graph(records)
    index = {}
    for r in records:
        for k in [r.get("term", "")] + list(r.get("aliases", [])):
            if k:
                index[k.strip().lower().replace("-", "_").replace(" ", "_")] = r
    s = structural_validate(rec, nodes, edges)
    f = faithfulness_check(rec, index) if s["status"] == PASS else None
    out["structure"] = s
    out["faithfulness"] = f
    verified = (s["status"] == PASS) and (f is not None and f["status"] == PASS)
    out["status"] = "verified" if verified else "quarantined"
    out["verifiable"] = bool(verified)
    if not verified:
        why = list(s.get("reasons", []))
        if f and f["status"] != PASS:
            why.append("faithfulness=%s score=%.2f ungrounded=%s" %
                       (f["status"], f["score"], f["ungrounded_symbols"]))
        out["quarantine_reason"] = "; ".join(why) or "failed gates"
    return out


def _selftest():
    global BACKEND
    BACKEND = "mock"   # deterministic, offline
    base = json.load(open(CORPUS_PATH, "r", encoding="utf-8"))
    cases = []

    # 1. faithful + well-structured -> verified
    energy = next(r for r in base if r["term"] == "energy")
    r1 = promote(energy, base)
    cases.append(("energy -> verified", r1["status"] == "verified"))

    # 2. structural fabrication: bad root + LLM-asserted provenance -> quarantined
    bad = {"term": "phlogiston", "canonical_id": "GR-phlogiston", "tier": 2,
           "root_path": ["information", "fire"], "domain": "physical",
           "math": "Q = phlogiston_released", "proof_kind": "definition",
           "provenance": "LLM-asserted", "sha256": "f"*64, "verifiable": True}
    r2 = promote(bad, base)
    cases.append(("phlogiston -> quarantined (structure)", r2["status"] == "quarantined"
                  and r2["structure"]["status"] == FAIL))

    # 3. unfaithful binding: term 'entropy' bound to Bayes math -> drift/fail
    unfaithful = {"term": "entropy", "canonical_id": "GR-entropy-wrong",
                  "aliases": ["shannon_entropy"], "tier": 3,
                  "root_path": ["E", "information", "uncertainty"], "domain": "formal",
                  "math": "P(H|E) = P(E|H) P(H) / P(E)", "proof_kind": "theorem",
                  "provenance": "arXiv:9999.99999", "sha256": "a"*64, "verifiable": True}
    r3 = promote(unfaithful, base)
    cases.append(("entropy<-bayes -> quarantined (faithfulness)",
                  r3["status"] == "quarantined" and r3["faithfulness"]["status"] != PASS))

    # 4. ethical -> governed (skips math checks)
    love = next(r for r in base if r["term"] == "love")
    r4 = promote(love, base)
    cases.append(("love -> governed (routed to ceiling)", r4["status"] == "governed"))

    ok = all(p for _, p in cases)
    for n, p in cases:
        print("  [%s] %s" % ("PASS" if p else "FAIL", n))
    print("SELFTEST: %d/%d passed" % (sum(1 for _, p in cases if p), len(cases)))
    return 0 if ok else 1


def _demo():
    """Run GATE F on ARBITRARY formulas (not in the mock) via the real backend."""
    print("backend: %s   model: %s\n" % (BACKEND, BT_MODEL if BACKEND != "mock" else "-"))
    base = json.load(open(CORPUS_PATH, "r", encoding="utf-8"))
    index = {}
    for r in base:
        for k in [r.get("term", "")] + list(r.get("aliases", [])):
            if k:
                index[k.strip().lower().replace("-", "_").replace(" ", "_")] = r
    trials = [
        ("softmax",              "sigma(z)_i = exp(z_i) / sum_j exp(z_j)"),
        ("pythagorean_theorem",  "a^2 + b^2 = c^2"),
        ("euler_identity",       "e^(i*pi) + 1 = 0"),
        ("newton_gravitation",   "F = G m1 m2 / r^2"),
        ("standard_deviation",   "sigma = sqrt( (1/N) sum_i (x_i - mu)^2 )"),
        ("WRONG: gravity<-softmax", "sigma(z)_i = exp(z_i) / sum_j exp(z_j)"),
    ]
    print("%-26s %-7s %-6s  %s" % ("term (intended)", "status", "score", "back-translation"))
    print("-" * 92)
    for term, math in trials:
        intended = term.split(":")[-1].split("<-")[0].strip()
        rec = {"term": intended, "math": math, "domain": "formal"}
        f = faithfulness_check(rec, index)
        print("%-26s %-7s %-6.2f  %s" % (term[:25], f["status"], f["score"], f["back_translation"][:44]))
    return 0


def _main(argv):
    if "--selftest" in argv:
        return _selftest()
    if "--demo" in argv:
        return _demo()
    base = json.load(open(CORPUS_PATH, "r", encoding="utf-8"))
    if not argv:
        # promote every seed record, print status table
        print("%-26s %-11s %s" % ("term", "status", "detail"))
        for r in base:
            p = promote(r, base)
            detail = p.get("quarantine_reason", "") or (
                "F=%.2f" % p["faithfulness"]["score"] if p.get("faithfulness") else "")
            print("%-26s %-11s %s" % (r["term"][:25], p["status"], detail))
        return 0
    # promote a record given as a JSON file path
    rec = json.load(open(argv[0], "r", encoding="utf-8"))
    print(json.dumps(promote(rec, base), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
