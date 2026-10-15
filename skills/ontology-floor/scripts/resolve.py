#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ontology Floor — resolve() lookup.

The single up-call every fleet agent makes BEFORE it reasons: bind each term to
its grounding math + proof so inference becomes computation, not confabulation.

HARD RULE (the Abu-Heru boundary): physical/formal terms are grounded (Heru);
ethical/value terms are REFUSED here and routed up to the governance ceiling to
be governed by wisdom (Abu). The floor never computes a value.

STUB SCOPE: this reference implementation reads Grounding Records from a local
JSON corpus (seed_corpus.json) and does exact + alias + fuzzy matching with the
Python stdlib only (no deps, Python 3.9+). The production floor swaps the
`_load_corpus` / `_lookup` internals for Cloudflare D1 (index) + Vectorize
(semantic) + R2 (proof bytes) behind the SAME return contract -- callers do not
change. Search for "# PROD:" markers for the swap points.

Contract (GroundingSet):
{
  "grounded":        [GroundingRecord, ...],   # term carried WITH its math+proof
  "ungrounded":      [term, ...],              # no canonical record -> flag, never fake
  "refused_ethical": [term, ...],              # value terms -> govern at ceiling
  "confidence":      float                     # 0..1 over the requested terms
}

CLI:
  python3 resolve.py energy bayes love water quark
  python3 resolve.py --json in_context_learning honesty
  python3 resolve.py --selftest
"""

import os
import sys
import json
import difflib

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.environ.get("ONTOLOGY_CORPUS", os.path.join(HERE, "seed_corpus.json"))

ETHICAL_DOMAIN = "ethical"
FUZZY_CUTOFF = 0.82  # conservative: a miss is surfaced, never faked


def _norm(term):
    """Canonical surface form for matching."""
    return term.strip().lower().replace("-", "_").replace(" ", "_")


def _load_corpus(path=CORPUS_PATH):
    # PROD: replace with D1 SELECT + Vectorize handle; keep the record shape.
    with open(path, "r", encoding="utf-8") as fh:
        records = json.load(fh)
    index = {}
    for rec in records:
        keys = [rec.get("term", "")] + list(rec.get("aliases", []))
        for k in keys:
            nk = _norm(k)
            if nk:
                index[nk] = rec
    return records, index


def _lookup(term, records, index):
    """Return (record_or_None, match_kind). match_kind in exact|fuzzy|miss."""
    nt = _norm(term)
    if nt in index:
        return index[nt], "exact"
    # PROD: replace fuzzy with Vectorize nearest-neighbour over embeddings.
    candidates = difflib.get_close_matches(nt, list(index.keys()), n=1, cutoff=FUZZY_CUTOFF)
    if candidates:
        return index[candidates[0]], "fuzzy"
    return None, "miss"


def resolve(terms, corpus_path=CORPUS_PATH):
    """Resolve a list of terms into a GroundingSet. Pure, side-effect free."""
    records, index = _load_corpus(corpus_path)

    grounded = []
    ungrounded = []
    refused_ethical = []
    seen_conf = []

    for term in terms:
        rec, kind = _lookup(term, records, index)
        if rec is None:
            ungrounded.append(term)
            seen_conf.append(0.0)
            continue
        # HARD RULE: value/ethical terms are never floor-grounded.
        if rec.get("domain") == ETHICAL_DOMAIN:
            refused_ethical.append(term)
            seen_conf.append(0.0)
            continue
        grounded.append(rec)
        seen_conf.append(1.0 if kind == "exact" else 0.85)

    confidence = round(sum(seen_conf) / len(terms), 4) if terms else 0.0
    return {
        "grounded": grounded,
        "ungrounded": ungrounded,
        "refused_ethical": refused_ethical,
        "confidence": confidence,
    }


def augment_prompt(base_prompt, grounding_set):
    """Convenience: fold grounded math+proof into an agent prompt so the term
    arrives carrying its formalism. Ethical terms are flagged for the ceiling,
    not injected as fact."""
    lines = [base_prompt, "", "--- GROUNDED FORMALISMS (compute, do not guess) ---"]
    for rec in grounding_set["grounded"]:
        lines.append("- {term} := {math}   [proof: {pk} @ {ref}]".format(
            term=rec["term"], math=rec.get("math", ""),
            pk=rec.get("proof_kind", "none"), ref=rec.get("proof_ref", "")))
    if grounding_set["refused_ethical"]:
        lines.append("")
        lines.append("--- VALUE TERMS (route to governance ceiling; do NOT compute) ---")
        for t in grounding_set["refused_ethical"]:
            lines.append("- {t}".format(t=t))
    if grounding_set["ungrounded"]:
        lines.append("")
        lines.append("--- UNGROUNDED (no canonical record; flag, do not fabricate) ---")
        for t in grounding_set["ungrounded"]:
            lines.append("- {t}".format(t=t))
    return "\n".join(lines)


def _selftest():
    checks = []
    gs = resolve(["energy", "bayes", "love", "water", "quark", "in-context learning", "honesty"])
    checks.append(("energy grounded", any(r["term"] == "energy" for r in gs["grounded"])))
    checks.append(("bayes grounded", any(r["canonical_id"] == "GR-bayes-theorem" for r in gs["grounded"])))
    checks.append(("love refused (ethical)", "love" in gs["refused_ethical"]))
    checks.append(("honesty refused (ethical)", "honesty" in gs["refused_ethical"]))
    checks.append(("quark ungrounded (not faked)", "quark" in gs["ungrounded"]))
    checks.append(("icl fuzzy/alias resolved", any(r["canonical_id"] == "GR-bayes-implicit-icl" for r in gs["grounded"])))
    checks.append(("no ethical record leaked into grounded",
                   all(r.get("domain") != ETHICAL_DOMAIN for r in gs["grounded"])))
    ok = all(p for _, p in checks)
    for name, p in checks:
        print("  [{}] {}".format("PASS" if p else "FAIL", name))
    print("SELFTEST: {}/{} passed".format(sum(1 for _, p in checks if p), len(checks)))
    return 0 if ok else 1


def _main(argv):
    args = list(argv)
    as_json = False
    if "--json" in args:
        as_json = True
        args.remove("--json")
    if "--selftest" in args:
        return _selftest()
    if not args:
        print(__doc__)
        return 0
    gs = resolve(args)
    if as_json:
        print(json.dumps(gs, indent=2))
        return 0
    print("confidence: {}".format(gs["confidence"]))
    print("grounded ({}):".format(len(gs["grounded"])))
    for rec in gs["grounded"]:
        print("  {:<22} {:<8} {} := {}".format(
            rec["term"], rec.get("domain", ""), rec["canonical_id"], rec.get("math", "")))
    print("refused_ethical ({}): {}".format(len(gs["refused_ethical"]), ", ".join(gs["refused_ethical"]) or "-"))
    print("ungrounded ({}): {}".format(len(gs["ungrounded"]), ", ".join(gs["ungrounded"]) or "-"))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
