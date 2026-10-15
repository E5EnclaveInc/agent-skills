#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOVE #1 -- The Proof. Measure the hallucination delta the ontology floor buys.

For each task, ask a SMALL model (where grounding is claimed to help most) the
SAME question in two conditions:
  UNGROUNDED : question only.
  GROUNDED   : question + resolve()-injected formalism (math + proof pointer).
Both end with 'ANSWER: <number>'. We parse that number and score it against a
known ground truth (KGHaluBench-style fact-level check). Hallucination = wrong or
missing answer. Delta = ungrounded_halluc - grounded_halluc.

Model diversity: producer under test = Llama (Workers AI); this is a different
family than the orchestrator. Deterministic (temperature 0). Zero metered cost.
"""
import os, re, json, urllib.request
from resolve import resolve, augment_prompt

ACCT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "fd98d813898e36431c9d6af3b0beeb20")
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
MODEL = os.environ.get("ONTOLOGY_EVAL_MODEL", "@cf/meta/llama-3.2-3b-instruct")
PI = 3.141592653589793

# term must exist in the cache so resolve() can ground it.
TASKS = [
    {"term": "energy", "answer": 2.7e17, "tol": 0.02,
     "q": "Using the mass-energy equivalence, compute the energy (in joules) of a mass of 3 kg. Use c = 3e8 m/s."},
    {"term": "bayes", "answer": 0.18, "tol": 0.02,
     "q": "Given P(E|H)=0.9, P(H)=0.01, P(E)=0.05, compute the posterior P(H|E)."},
    {"term": "shannon_entropy", "answer": 2.0, "tol": 0.0,
     "q": "What is the Shannon entropy, in bits, of a source with 4 equally likely symbols?"},
    {"term": "cantor_set", "answer": 0.0, "tol": 0.0,
     "q": "What is the Lebesgue measure of the standard Cantor set? Give the number."},
    {"term": "pythagorean_theorem", "answer": 5.0, "tol": 0.0,
     "q": "A right triangle has legs a=3 and b=4. What is the length of the hypotenuse?"},
    {"term": "softmax", "answer": 0.5, "tol": 0.0,
     "q": "For the input vector [2, 2], what is the first component of its softmax?"},
    {"term": "standard_deviation", "answer": 2.0, "tol": 0.0,
     "q": "Compute the POPULATION standard deviation of [2,4,4,4,5,5,7,9]."},
    {"term": "quadratic_formula", "answer": 3.0, "tol": 0.0,
     "q": "What is the larger root of x^2 - 5x + 6 = 0?"},
    {"term": "circle_area", "answer": 4 * PI, "tol": 0.02,
     "q": "What is the area of a circle with radius 2? Give a decimal."},
]

INSTR = " Show your reasoning briefly, then end with a line formatted exactly: ANSWER: <number>"


def chat(system, user):
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (ACCT, MODEL)
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    body = json.dumps({"messages": msgs, "temperature": 0.0, "max_tokens": 400}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + TOKEN, "Content-Type": "application/json",
        "User-Agent": "ontology-eval/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        j = json.loads(r.read().decode())
    return (j.get("result") or {}).get("response", "") or ""


def parse_answer(text):
    lines = re.findall(r"ANSWER:\s*(.+)", text, flags=re.IGNORECASE)
    raw = lines[-1] if lines else text.strip().splitlines()[-1] if text.strip() else ""
    s = raw.strip().lower()
    s = s.replace(",", "").replace("$", "").replace("j", "").replace("bits", "").replace("units", "")
    s = s.replace("π", "*"+str(PI)).replace("pi", "*"+str(PI))
    s = re.sub(r"(\d)\s*[x×]\s*10\s*\^?\s*([+-]?\d+)", r"\1e\2", s)   # 2.7 x 10^17 -> 2.7e17
    s = s.replace("^", "**")
    m = re.search(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?(?:\s*\*\s*[-+]?\d*\.?\d+(?:e[-+]?\d+)?)*", s)
    if not m:
        return None
    expr = m.group(0)
    try:
        return float(eval(expr, {"__builtins__": {}}, {}))
    except Exception:
        try:
            return float(re.search(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?", expr).group(0))
        except Exception:
            return None


def correct(pred, truth, tol):
    if pred is None:
        return False
    if tol == 0.0:
        return abs(pred - truth) < 1e-6 or (truth != 0 and abs(pred - truth) <= 0.001 * abs(truth))
    return abs(pred - truth) <= tol * abs(truth) if truth != 0 else abs(pred) <= tol


def run():
    print("model under test: %s   N=%d   (deterministic, temp 0)\n" % (MODEL, len(TASKS)))
    print("%-22s %-10s %-10s %s" % ("term", "ungrounded", "grounded", "truth"))
    print("-" * 70)
    ok_u = ok_g = 0
    for t in TASKS:
        gs = resolve([t["term"]])
        grounded_prompt = augment_prompt(t["q"], gs) + INSTR
        u = parse_answer(chat("You are a careful calculator.", t["q"] + INSTR))
        g = parse_answer(chat("You are a careful calculator. Use the provided grounded formalisms.", grounded_prompt))
        cu, cg = correct(u, t["answer"], t["tol"]), correct(g, t["answer"], t["tol"])
        ok_u += cu; ok_g += cg
        print("%-22s %-10s %-10s %s" % (
            t["term"][:21],
            ("OK  " if cu else "MISS") + " " + _fmt(u),
            ("OK  " if cg else "MISS") + " " + _fmt(g),
            _fmt(t["answer"])))
    n = len(TASKS)
    hu, hg = 1 - ok_u / n, 1 - ok_g / n
    print("-" * 70)
    print("ungrounded: acc %d/%d = %.0f%%   hallucination %.0f%%" % (ok_u, n, 100*ok_u/n, 100*hu))
    print("grounded:   acc %d/%d = %.0f%%   hallucination %.0f%%" % (ok_g, n, 100*ok_g/n, 100*hg))
    print("")
    print(">>> HALLUCINATION DELTA (reduction): %.0f percentage points  (%.0f%% -> %.0f%%)"
          % (100*(hu - hg), 100*hu, 100*hg))
    print(">>> accuracy lift: %+.0f percentage points" % (100*(ok_g - ok_u)/n))


def _fmt(x):
    if x is None:
        return "(none)"
    if abs(x) >= 1e4 or (x != 0 and abs(x) < 1e-3):
        return "%.2e" % x
    return ("%.3f" % x).rstrip("0").rstrip(".")


if __name__ == "__main__":
    run()
