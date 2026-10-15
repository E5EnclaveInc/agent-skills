#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selective grounding vs always-grounding vs ungrounded, on the large hard set.

Trigger = UNCERTAINTY via self-consistency: sample the ungrounded answer 3x at
temp 0.7; if >=2 agree the model is CONFIDENT -> keep ungrounded (do NOT ground,
so grounding can't break a right answer); if they disagree it is UNCERTAIN ->
ground once (temp 0) and use that. (Rarity is an additional cheap OR-signal in
prod; here the uncertainty trigger is what we isolate.)

Three cells per task: u (ungrounded temp0), g (always-grounded temp0),
s (selective). Resumable (eval_out/raw_select.jsonl) + wall-clock budget so the
long 8B run completes across invocations. Truths are python-computed. temp 0
for u/g (deterministic). Zero metered cost (Workers AI).
"""
import os, re, json, time, urllib.request
from resolve import resolve, augment_prompt

ACCT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "fd98d813898e36431c9d6af3b0beeb20")
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
MODEL = os.environ.get("ONTOLOGY_EVAL_MODEL", "@cf/meta/llama-3.1-8b-instruct-fp8")
BUDGET = float(os.environ.get("ONTOLOGY_BUDGET_SEC", "50"))
K = 3
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eval_out"); os.makedirs(OUT, exist_ok=True)
RAW = os.path.join(OUT, "raw_select.jsonl")
CORPUS = os.path.join(OUT, "eval_corpus_select.json")
TASKS = [tuple(x) for x in json.load(open(os.path.join(HERE, "tasks_hard.json")))]
INSTR = " Give at most one short line of working, then end with exactly: ANSWER: <number>"


def chat(system, user, temp):
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (ACCT, MODEL)
    body = json.dumps({"messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}],
                       "temperature": temp, "max_tokens": 150}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + TOKEN, "Content-Type": "application/json",
        "User-Agent": "ontology-eval/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return (json.loads(r.read().decode()).get("result") or {}).get("response", "") or ""


def parse_answer(text):
    lines = re.findall(r"ANSWER:\s*(.+)", text, flags=re.IGNORECASE)
    raw = lines[-1] if lines else (text.strip().splitlines()[-1] if text.strip() else "")
    s = raw.strip().lower().replace(",", "").replace("$", "").replace("%", "")
    for u in ["bits","joules","j","meters","m/s","kg","km/h","km","units","degrees","ohm","ohms","mol","l"]:
        s = re.sub(r"\b"+u+r"\b", "", s)
    import math as _m
    s = s.replace("π", "*"+str(_m.pi)).replace("pi", "*"+str(_m.pi))
    s = re.sub(r"(\d)\s*[x×]\s*10\s*\^?\s*([+-]?\d+)", r"\1e\2", s)
    m = re.search(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?", s)
    return float(m.group(0)) if m else None


def correct(pred, truth, tol):
    if pred is None: return False
    if truth == 0: return abs(pred) <= 1e-6
    if tol == 0: return abs(pred-truth) <= 0.005*abs(truth)
    return abs(pred-truth) <= tol*abs(truth)


def consensus(vals):
    for v in vals:
        agree = sum(1 for w in vals if (abs(w-v) <= max(1e-9, 0.01*abs(v))))
        if agree >= 2:
            return v
    return None


def build_corpus():
    recs = [{"term": t[0], "canonical_id": "GR-h-%02d" % i, "tier": 3,
             "root_path": ["E","formal","hard"], "domain": "formal", "math": t[1],
             "proof_kind": "definition", "provenance": "standard",
             "sha256": ("%064d" % i), "verifiable": True} for i, t in enumerate(TASKS)]
    json.dump(recs, open(CORPUS, "w"))


def load_done():
    d = {}
    if os.path.exists(RAW):
        for line in open(RAW):
            try:
                r = json.loads(line)
                if r["model"] == MODEL: d[(r["term"], r["cond"])] = r
            except Exception: pass
    return d


def run():
    build_corpus()
    done = load_done()
    fh = open(RAW, "a")
    start = time.time()
    stopped = False
    for (term, m, q, a, tol) in TASKS:
        if {(term,"u"),(term,"g"),(term,"s")} <= set(done.keys()):
            continue
        if time.time()-start > BUDGET:
            stopped = True; break
        sysu = "You are a careful calculator."
        sysg = "You are a careful calculator. Use the provided grounded formalisms."
        # u
        if (term,"u") not in done:
            p = parse_answer(chat(sysu, q+INSTR, 0.0))
            r = {"model":MODEL,"term":term,"cond":"u","pred":p,"ok":correct(p,a,tol)}
            fh.write(json.dumps(r)+"\n"); fh.flush(); done[(term,"u")]=r
        # g
        if (term,"g") not in done:
            gp = augment_prompt(q, resolve([term], corpus_path=CORPUS))+INSTR
            p = parse_answer(chat(sysg, gp, 0.0))
            r = {"model":MODEL,"term":term,"cond":"g","pred":p,"ok":correct(p,a,tol)}
            fh.write(json.dumps(r)+"\n"); fh.flush(); done[(term,"g")]=r
        # s (selective)
        if (term,"s") not in done:
            samples = [parse_answer(chat(sysu, q+INSTR, 0.7)) for _ in range(K)]
            vals = [v for v in samples if v is not None]
            c = consensus(vals)
            if c is not None:
                pred, uncertain, grounded, calls = c, False, False, K
            else:
                gp = augment_prompt(q, resolve([term], corpus_path=CORPUS))+INSTR
                pred, uncertain, grounded, calls = parse_answer(chat(sysg, gp, 0.0)), True, True, K+1
            r = {"model":MODEL,"term":term,"cond":"s","pred":pred,"ok":correct(pred,a,tol),
                 "uncertain":uncertain,"grounded":grounded,"calls":calls}
            fh.write(json.dumps(r)+"\n"); fh.flush(); done[(term,"s")]=r
    fh.close()
    report(done, stopped)


def _p_mcnemar(b, c):
    if b+c == 0: return 1.0
    import math
    stat = (abs(b-c)-1)**2/(b+c)
    return math.erfc((stat/2)**0.5)


def report(done, stopped):
    n = len(TASKS)
    have = sum(1 for t in TASKS if {(t[0],"u"),(t[0],"g"),(t[0],"s")} <= set(done.keys()))
    if have < n:
        print("PARTIAL: %d/%d tasks complete for %s  (re-run to continue)" % (have, n, MODEL))
        return
    U = {t[0]: done[(t[0],"u")]["ok"] for t in TASKS}
    G = {t[0]: done[(t[0],"g")]["ok"] for t in TASKS}
    S = {t[0]: done[(t[0],"s")]["ok"] for t in TASKS}
    au, ag, as_ = sum(U.values()), sum(G.values()), sum(S.values())
    grounded_n = sum(1 for t in TASKS if done[(t[0],"s")].get("grounded"))
    calls = sum(done[(t[0],"s")].get("calls",0) for t in TASKS)
    def edge(cond):
        broke = sum(1 for t in TASKS if U[t[0]] and not cond[t[0]])
        resc = sum(1 for t in TASKS if not U[t[0]] and cond[t[0]])
        return resc, broke
    rg, bg = edge(G); rs, bs = edge(S)
    print("MODEL %s   N=%d\n" % (MODEL, n))
    print("               acc      halluc")
    print("ungrounded   %3d/%d %3.0f%%   %3.0f%%" % (au,n,100*au/n,100*(1-au/n)))
    print("grounded(all)%3d/%d %3.0f%%   %3.0f%%" % (ag,n,100*ag/n,100*(1-ag/n)))
    print("selective    %3d/%d %3.0f%%   %3.0f%%   (grounded %d/%d tasks; %d model-calls)" %
          (as_,n,100*as_/n,100*(1-as_/n),grounded_n,n,calls))
    print()
    print("vs ungrounded:  always-grounded  %+d pp  (rescued %d, broke %d)  McNemar p=%.3f" %
          (round(100*(ag-au)/n), rg, bg, _p_mcnemar(bg, rg)))
    print("                selective        %+d pp  (rescued %d, broke %d)  McNemar p=%.3f" %
          (round(100*(as_-au)/n), rs, bs, _p_mcnemar(bs, rs)))


if __name__ == "__main__":
    run()
