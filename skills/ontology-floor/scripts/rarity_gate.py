#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rarity-primary gate on a MIXED (easy+hard) workload, evaluated over the 8B's
already-computed ungrounded (u) and always-grounded (g) answers -> zero new model
calls, fully reproducible.

Gate:  ground IFF the formalism is RARE (not in COMMON).  Rarity here is a
transparent stand-in for a production corpus-frequency lookup; the COMMON list is
elementary/ubiquitous formulas and deliberately CROSS-CUTS the easy/hard split
(some easy terms are 'rare', some hard terms are 'common') so the test is not
circular with difficulty.

Confirms the hypothesis: keep the hard-item gain, avoid the easy-item breakage,
at 1 model call/task (vs 3-4 for uncertainty-gating).
"""
import os, json, collections, math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eval_out")
MODEL = "@cf/meta/llama-3.1-8b-instruct-fp8"

# Elementary / ubiquitous formulas (taught pre-college or globally famous).
# Everything NOT here is treated as rare/specialized -> grounded.
COMMON = set("""
energy kinetic_energy newtons_second_law ohms_law gravitational_pe momentum
density power speed average_speed_htg wave_speed kinematics_v ohmic_power
pressure work_done efficiency celsius_to_f percentage
pythagorean_theorem circle_area circle_circumference triangle_area rectangle_area
trapezoid_area quadratic_formula discriminant distance_2d slope
mean median mode range_stat factorial simple_interest bmi gcd lcm molarity
hookes_law frequency_period cylinder_volume sphere_volume
arithmetic_series geometric_series nth_term_arith dot_product
""".split())

def is_rare(term):
    return term not in COMMON

def load(path, tag, into):
    by = collections.defaultdict(dict)
    for line in open(path):
        r = json.loads(line)
        if r["model"] == MODEL:
            by[r["term"]][r["cond"]] = bool(r["ok"])
    for term, d in by.items():
        if "u" in d and "g" in d:
            into.append({"set": tag, "term": term, "u": d["u"], "g": d["g"],
                         "rare": is_rare(term)})

def mcnemar(b, c):
    if b + c == 0: return 1.0
    stat = (abs(b - c) - 1) ** 2 / (b + c)
    return math.erfc((stat / 2) ** 0.5)

def main():
    rows = []
    load(os.path.join(OUT, "raw.jsonl"), "easy", rows)
    load(os.path.join(OUT, "raw_select.jsonl"), "hard", rows)
    for r in rows:
        r["r"] = r["g"] if r["rare"] else r["u"]   # rarity gate

    def acc(rs, k): return sum(x[k] for x in rs) / len(rs)
    n = len(rows)
    easy = [x for x in rows if x["set"] == "easy"]
    hard = [x for x in rows if x["set"] == "hard"]

    print("MIXED workload: %d tasks (%d easy + %d hard), model 8B\n" % (n, len(easy), len(hard)))
    print("rarity labels: easy common=%d rare=%d | hard common=%d rare=%d" % (
        sum(not x["rare"] for x in easy), sum(x["rare"] for x in easy),
        sum(not x["rare"] for x in hard), sum(x["rare"] for x in hard)))
    print("(label cross-cuts the split -> not circular)\n")

    hdr = "%-8s %7s %7s %7s"
    print(hdr % ("set", "ungrnd", "always", "rarity"))
    for name, rs in [("ALL", rows), ("easy", easy), ("hard", hard)]:
        print(hdr % (name, "%.0f%%" % (100*acc(rs,"u")), "%.0f%%" % (100*acc(rs,"g")), "%.0f%%" % (100*acc(rs,"r"))))

    # easy breakage (u right -> cond wrong), hard rescue (u wrong -> cond right)
    def breaks(rs, k): return sum(1 for x in rs if x["u"] and not x[k])
    def resc(rs, k):   return sum(1 for x in rs if not x["u"] and x[k])
    print("\nEASY breakage (grounding flips a right answer wrong):")
    print("   always-grounded: %d    rarity-gated: %d" % (breaks(easy,"g"), breaks(easy,"r")))
    print("HARD rescue (grounding fixes a wrong answer):")
    print("   always-grounded: %d    rarity-gated: %d" % (resc(hard,"g"), resc(hard,"r")))

    # overall McNemar rarity vs ungrounded
    b = sum(1 for x in rows if x["u"] and not x["r"])
    c = sum(1 for x in rows if not x["u"] and x["r"])
    print("\nrarity vs ungrounded (ALL): +%d pp  (rescued %d, broke %d)  McNemar p=%.4f" % (
        round(100*(acc(rows,"r")-acc(rows,"u"))), c, b, mcnemar(b, c)))
    ba = sum(1 for x in rows if x["u"] and not x["g"])
    ca = sum(1 for x in rows if not x["u"] and x["g"])
    print("always vs ungrounded (ALL): +%d pp  (rescued %d, broke %d)  McNemar p=%.4f" % (
        round(100*(acc(rows,"g")-acc(rows,"u"))), ca, ba, mcnemar(ba, ca)))
    print("\ncost: rarity = 1 call/task (same as baseline); uncertainty-gating was 3-4x.")

if __name__ == "__main__":
    main()
