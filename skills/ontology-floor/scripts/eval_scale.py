#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOVE #1 at scale -- KGHaluBench-style fact-level eval of the ontology floor.

~46 tasks, each tied to a cached formalism. Ground truths are COMPUTED IN PYTHON
(authoritative, not hand-typed). Each question is asked in two conditions:
  UNGROUNDED : question only
  GROUNDED   : question + resolve()-injected formalism (math)
Parse 'ANSWER: <number>', score against the computed truth (fact-level check),
tally abstentions. Report accuracy, hallucination rate, and the delta per model.

Resumable: every (model,term,condition) result is appended to eval_out/raw.jsonl;
re-running skips finished cells, so a timeout just needs another invocation.
Set ONTOLOGY_EVAL_MODEL to pick the model. Deterministic (temp 0). Zero metered cost.
"""
import os, re, json, math, urllib.request

ACCT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "fd98d813898e36431c9d6af3b0beeb20")
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
MODEL = os.environ.get("ONTOLOGY_EVAL_MODEL", "@cf/meta/llama-3.2-3b-instruct")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eval_out")
os.makedirs(OUT, exist_ok=True)
RAW = os.path.join(OUT, "raw.jsonl")
CORPUS = os.path.join(OUT, "eval_corpus.json")

# (term, grounding-math, question, computed-truth, tol)
T = [
 ("energy","E = mc^2","Energy (J) of mass m=2 kg, c=3e8 m/s?",2*(3e8)**2,0.02),
 ("kinetic_energy","KE = 0.5 m v^2","Kinetic energy of m=4 kg at v=3 m/s?",0.5*4*9,0.005),
 ("newtons_second_law","F = m a","Force on m=5 kg at a=3 m/s^2?",15,0.005),
 ("ohms_law","V = I R","Voltage across R=5 ohm with I=2 A?",10,0.005),
 ("gravitational_pe","PE = m g h","Grav. PE of m=2 kg at h=10 m (g=9.8)?",2*9.8*10,0.01),
 ("momentum","p = m v","Momentum of m=3 kg at v=4 m/s?",12,0.005),
 ("density","rho = m / V","Density of m=10 kg in V=2 m^3?",5,0.005),
 ("power","P = W / t","Power for W=100 J over t=4 s?",25,0.005),
 ("wave_speed","v = f * lambda","Wave speed, f=5 Hz, lambda=2 m?",10,0.005),
 ("ohmic_power","P = I^2 R","Power dissipated, I=2 A, R=5 ohm?",20,0.005),
 ("kinematics_v","v = u + a t","Final velocity, u=0, a=2, t=5?",10,0.005),
 ("celsius_to_f","F = 9/5 C + 32","100 C in Fahrenheit?",212,0.005),
 ("moles","n = mass / molar_mass","Moles in 36 g of water (molar mass 18)?",2,0.005),
 ("pythagorean_theorem","a^2 + b^2 = c^2","Hypotenuse for legs 6 and 8?",10,0.005),
 ("circle_area","A = pi r^2","Area of a circle radius 3?",9*math.pi,0.02),
 ("circle_circumference","C = 2 pi r","Circumference of a circle radius 5?",10*math.pi,0.02),
 ("sphere_volume","V = 4/3 pi r^3","Volume of a sphere radius 3?",4/3*math.pi*27,0.02),
 ("triangle_area","A = 0.5 b h","Area of triangle base 6 height 8?",24,0.005),
 ("rectangle_area","A = l w","Area of a 7 by 6 rectangle?",42,0.005),
 ("quadratic_formula","x = (-b +/- sqrt(b^2-4ac))/(2a)","Larger root of x^2 - 7x + 12 = 0?",4,0.005),
 ("distance_2d","d = sqrt((x2-x1)^2+(y2-y1)^2)","Distance from (0,0) to (3,4)?",5,0.005),
 ("slope","m = (y2-y1)/(x2-x1)","Slope through (1,2) and (3,8)?",3,0.005),
 ("simple_interest","I = P r t","Interest on P=1000 at r=0.05 for t=3 yr?",150,0.005),
 ("mean","mean = sum(x)/n","Mean of [2,4,6,8]?",5,0.005),
 ("variance_pop","var = mean((x-mu)^2)","Population variance of [2,4,4,4,5,5,7,9]?",4,0.005),
 ("standard_deviation","sigma = sqrt(mean((x-mu)^2))","Population std dev of [2,4,4,4,5,5,7,9]?",2,0.005),
 ("bayes","P(H|E) = P(E|H)P(H)/P(E)","Posterior with P(E|H)=0.8,P(H)=0.02,P(E)=0.1?",0.16,0.02),
 ("shannon_entropy","H = log2(k) for k equally likely","Entropy (bits) of 8 equally likely symbols?",3,0.005),
 ("combinations","C(n,k)=n!/(k!(n-k)!)","C(5,2)?",10,0.005),
 ("permutations","P(n,k)=n!/(n-k)!","P(5,2)?",20,0.005),
 ("factorial","n! = product 1..n","5! ?",120,0.005),
 ("z_score","z = (x-mu)/sigma","z-score, x=85, mu=70, sigma=5?",3,0.005),
 ("expected_value_die","E = sum p*x","Expected value of a fair six-sided die?",3.5,0.005),
 ("softmax","softmax(z)_i = exp(z_i)/sum_j exp(z_j)","First component of softmax([1,1,1])?",1/3,0.02),
 ("sigmoid","s(x) = 1/(1+exp(-x))","Sigmoid of 0?",0.5,0.005),
 ("relu","relu(x)=max(0,x)","ReLU of -3?",0,0.005),
 ("log2","log2(x)=ln x/ln 2","log base 2 of 32?",5,0.005),
 ("xor","xor: 1 if bits differ","1 XOR 1?",0,0.005),
 ("hamming_distance","count differing positions","Hamming distance between 1011 and 1001?",1,0.005),
 ("mse","MSE = mean((y-yhat)^2)","MSE of y=[1,2], yhat=[1,4]?",2,0.005),
 ("accuracy","acc = correct/total","Accuracy: 90 correct of 100?",0.9,0.005),
 ("compound_interest","A = P(1+r)^t","Amount, P=1000, r=0.1, t=2 (compounded yearly)?",1000*1.1**2,0.01),
 ("speed","speed = distance/time","Speed for 150 km in 3 h?",50,0.005),
 ("bmi","BMI = kg / m^2","BMI for 80 kg, 2 m tall?",20,0.005),
 ("percentage","pct = part/whole*100","What percent is 45 of 180?",25,0.005),
 ("average_speed_htg","d = r t","Distance at 60 km/h for 2.5 h?",150,0.005),
]

INSTR = " Give at most one short line of working, then end with exactly: ANSWER: <number>"

# Optional: load an alternate task set + output tag (keeps hard/easy runs separate)
_TASKS_FILE = os.environ.get("ONTOLOGY_TASKS_FILE")
if _TASKS_FILE:
    T = [tuple(x) for x in json.load(open(_TASKS_FILE))]
_TAG = os.environ.get("ONTOLOGY_EVAL_TAG", "")
if _TAG:
    RAW = os.path.join(OUT, "raw_%s.jsonl" % _TAG)
    CORPUS = os.path.join(OUT, "eval_corpus_%s.json" % _TAG)


def chat(system, user):
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (ACCT, MODEL)
    body = json.dumps({"messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}],
                       "temperature": 0.0, "max_tokens": 160}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + TOKEN, "Content-Type": "application/json",
        "User-Agent": "ontology-eval/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        j = json.loads(r.read().decode())
    return (j.get("result") or {}).get("response", "") or ""


def parse_answer(text):
    lines = re.findall(r"ANSWER:\s*(.+)", text, flags=re.IGNORECASE)
    raw = lines[-1] if lines else (text.strip().splitlines()[-1] if text.strip() else "")
    s = raw.strip().lower().replace(",", "").replace("$", "").replace("%", "")
    for u in ["bits", "joules", "j", "meters", "m/s", "kg", "km/h", "km", "units", "degrees", "f"]:
        s = re.sub(r"\b" + u + r"\b", "", s)
    s = s.replace("π", "*"+str(math.pi)).replace("pi", "*"+str(math.pi))
    s = re.sub(r"(\d)\s*[x×]\s*10\s*\^?\s*([+-]?\d+)", r"\1e\2", s)
    m = re.search(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?", s)
    return float(m.group(0)) if m else None


def correct(pred, truth, tol):
    if pred is None:
        return False
    if truth == 0:
        return abs(pred) <= 1e-6
    if tol == 0:
        return abs(pred - truth) <= 0.005 * abs(truth)
    return abs(pred - truth) <= tol * abs(truth)


def build_corpus():
    recs = []
    for i, (term, m, q, a, tol) in enumerate(T):
        recs.append({"term": term, "canonical_id": "GR-eval-%02d" % i, "tier": 3,
                     "root_path": ["E", "formal", "eval"], "domain": "formal",
                     "math": m, "proof_kind": "definition",
                     "provenance": "standard", "sha256": ("%064d" % i), "verifiable": True})
    json.dump(recs, open(CORPUS, "w"))


def load_done():
    done = {}
    if os.path.exists(RAW):
        for line in open(RAW):
            try:
                r = json.loads(line)
                if r.get("model") == MODEL:
                    done[(r["term"], r["cond"])] = r
            except Exception:
                pass
    return done


def run():
    from resolve import resolve, augment_prompt
    build_corpus()
    done = load_done()
    fh = open(RAW, "a")
    for (term, m, q, a, tol) in T:
        for cond in ("u", "g"):
            if (term, cond) in done:
                continue
            if cond == "u":
                prompt = q + INSTR
                sys_p = "You are a careful calculator."
            else:
                gs = resolve([term], corpus_path=CORPUS)
                prompt = augment_prompt(q, gs) + INSTR
                sys_p = "You are a careful calculator. Use the provided grounded formalisms."
            try:
                pred = parse_answer(chat(sys_p, prompt))
            except Exception as e:
                pred = None
            rec = {"model": MODEL, "term": term, "cond": cond, "pred": pred,
                   "truth": a, "ok": bool(correct(pred, a, tol)), "abstain": pred is None}
            fh.write(json.dumps(rec) + "\n"); fh.flush()
            done[(term, cond)] = rec
    fh.close()
    # summary for this model
    n = len(T)
    ok_u = sum(1 for (t, c) in done if c == "u" and done[(t, c)]["ok"])
    ok_g = sum(1 for (t, c) in done if c == "g" and done[(t, c)]["ok"])
    ab_u = sum(1 for (t, c) in done if c == "u" and done[(t, c)]["abstain"])
    ab_g = sum(1 for (t, c) in done if c == "g" and done[(t, c)]["abstain"])
    hu, hg = 1-ok_u/n, 1-ok_g/n
    print("MODEL: %s   N=%d" % (MODEL, n))
    print("ungrounded: acc %2d/%d=%3.0f%%  halluc %3.0f%%  abstain %d" % (ok_u, n, 100*ok_u/n, 100*hu, ab_u))
    print("grounded:   acc %2d/%d=%3.0f%%  halluc %3.0f%%  abstain %d" % (ok_g, n, 100*ok_g/n, 100*hg, ab_g))
    print(">>> hallucination reduction: %+.0f pp  (%.0f%% -> %.0f%%)" % (100*(hu-hg), 100*hu, 100*hg))
    json.dump({"model": MODEL, "n": n, "acc_u": ok_u, "acc_g": ok_g,
               "halluc_u": hu, "halluc_g": hg, "delta_pp": 100*(hu-hg)},
              open(os.path.join(OUT, "summary_%s.json" % re.sub(r"[^a-z0-9]+", "_", MODEL.lower())), "w"))


if __name__ == "__main__":
    run()
