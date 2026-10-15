#!/usr/bin/env python3
"""ai_tells.py — deterministic AI-suspicion signals for a DOCX manuscript.

Part of the submission-gate AI-suspicion audit module. Reports SIGNALS, not a
verdict: per-hit lexicon matches with locations, em-dash count, sentence-length
statistics (burstiness proxy), and hedging density. A human dispositions every
finding. Nothing here proves or disproves AI involvement.

Usage: python3 bin/ai_tells.py <manuscript.docx>
Exit 0 always (report-only tool); findings go to stdout as text + JSON file
<stem>_ai_tells.json next to the input.

Posture: disclosure, not evasion. This tool helps honest, disclosed
AI-assisted work survive false suspicion. It is never used to launder AI
authorship into fake human authorship.
"""
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# ---------------------------------------------------------------- lexicon ---
# Curated for a humanities register. Two tiers:
#   TIER_A — stock LLM diction, rare in pre-2022 humanities prose. A hit is a
#            genuine flag worth a human look.
#   TIER_B — common academic transitions/connectives. Legitimate authorial
#            style; reported only as frequency counts so an unusual spike can
#            be noticed. Never treated as evidence on their own.
TIER_A = [
    r"\bdelv(?:e|es|ed|ing)\b",
    r"\btapestry\b", r"\btapestries\b",
    r"\brich tapestry\b",
    r"\btestament to\b",
    r"\bsheds? light on\b",
    r"\bintricac(?:y|ies)\b",
    r"\bmultifaceted\b",
    r"\bvibrant\b",
    r"\bholistic\b",
    r"\bleverage[sd]?\b",
    r"\bgroundbreaking\b",
    r"\bgame-?changer\b",
    r"\bseamless(?:ly)?\b",
    r"\bunlock(?:s|ed|ing)?\b",
    r"\bunleash(?:es|ed|ing)?\b",
    r"\bpivotal\b",
    r"\bsteeped in\b",
    r"\ba testament\b",
    r"\bin today's fast-paced\b",
    r"\bever-evolving\b",
    r"\bdive into\b", r"\bdeep dive\b",
    r"\bgrapple with\b",
    r"\bpoised to\b",
    r"\bembark on\b",
    r"\bfoster(?:s|ed|ing)?\b",
    r"\bnuance[sd]?\b",  # 'nuanced' is classic LLM filler; 'nuance' itself is older
    r"\bkaleidoscope\b",
    r"\bmosaic\b",
    r"\blinchpin\b",
    r"\bcornerstone\b",
    r"\bembod(?:y|ies|ied)\b",
    r"\bencapsulat(?:e|es|ed|ing)\b",
    r"\bintricate(?:ly)?\b",
]

TIER_B = [
    r"\bmoreover\b", r"\bfurthermore\b", r"\badditionally\b",
    r"\bconsequently\b", r"\bnevertheless\b", r"\bnonetheless\b",
    r"\bit is worth noting that\b", r"\bit'?s important to note\b",
    r"\bin conclusion\b", r"\bin summary\b",
    r"\bplays? a crucial role\b",
    r"\bcrucial(?:ly)?\b",
    r"\bunderscore[sd]?\b",
    r"\bhighlight[sd]?\b",
]

HEDGES = [
    r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bperhaps\b", r"\bpossibly\b",
    r"\bpotentially\b", r"\barguably\b", r"\bseems?\b", r"\bappears?\b",
    r"\bsuggests?\b", r"\bindicates?\b", r"\blikely\b", r"\btends?\b",
    r"\brelatively\b", r"\bsomewhat\b", r"\bgenerally\b",
]

ABBREV = {"Mr.", "Mrs.", "Ms.", "Dr.", "St.", "e.g.", "i.e.", "vs.", "etc.",
          "Fig.", "fig.", "No.", "no.", "pp.", "p.", "ch.", "Ch.", "ed.",
          "vol.", "Vol.", "ff.", "cf.", "ca.", "Jan.", "Feb.", "Mar.",
          "Apr.", "Jun.", "Jul.", "Aug.", "Sep.", "Sept.", "Oct.", "Nov.",
          "Dec."}


def para_texts(zf, part):
    """Yield (index, text) for each paragraph in a document part."""
    try:
        root = ET.fromstring(zf.read(part))
    except KeyError:
        return
    for i, p in enumerate(root.iter(W + "p")):
        runs = []
        for t in p.iter(W + "t"):
            if t.text:
                runs.append(t.text)
        yield i, "".join(runs)


def sentences(text):
    """Naive sentence splitter that respects common abbreviations."""
    out, buf = [], ""
    for m in re.finditer(r"\S+|\s+", text):
        tok = m.group(0)
        buf += tok
        if tok.strip() and tok.strip()[-1] in ".!?" and not tok.strip().endswith(tuple(ABBREV)):
            s = buf.strip()
            if len(s.split()) >= 3:
                out.append(s)
            buf = ""
    s = buf.strip()
    if len(s.split()) >= 3:
        out.append(s)
    return out


def main():
    if len(sys.argv) != 2:
        print("usage: ai_tells.py <manuscript.docx>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    stem = os.path.splitext(path)[0]

    with zipfile.ZipFile(path) as zf:
        body = [(i, t) for i, t in para_texts(zf, "word/document.xml") if t.strip()]
        notes = [(i, t) for i, t in para_texts(zf, "word/endnotes.xml") if t.strip()]
        try:
            props = ET.fromstring(zf.read("docProps/core.xml"))
            core = {e.tag.split("}")[-1]: (e.text or "") for e in props}
        except KeyError:
            core = {}

    report = {"file": os.path.basename(path), "tier_a_hits": [],
              "tier_b_counts": {}, "hedge_density": {}, "sentence_stats": {},
              "em_dashes": 0, "metadata": {}}

    # --- tier A: per-hit with location -------------------------------------
    for label, paras in (("body", body), ("endnotes", notes)):
        for pi, text in paras:
            for pat in TIER_A:
                for m in re.finditer(pat, text, flags=re.IGNORECASE):
                    s = max(0, m.start() - 60)
                    report["tier_a_hits"].append({
                        "pattern": pat, "where": f"{label} para {pi}",
                        "match": m.group(0),
                        "context": "…" + text[s:m.end() + 60].strip() + "…",
                    })

    # --- tier B: frequency only --------------------------------------------
    all_text = " ".join(t for _, t in body)
    for pat in TIER_B:
        n = len(re.findall(pat, all_text, flags=re.IGNORECASE))
        if n:
            report["tier_b_counts"][pat] = n

    # --- hedging density ----------------------------------------------------
    words = re.findall(r"[A-Za-z']+", all_text)
    n_words = max(1, len(words))
    n_hedge = sum(len(re.findall(p, all_text, flags=re.IGNORECASE)) for p in HEDGES)
    report["hedge_density"] = {
        "hedge_hits": n_hedge, "words": n_words,
        "per_1000_words": round(1000.0 * n_hedge / n_words, 2),
    }

    # --- sentence stats (burstiness proxy) ----------------------------------
    lens = [len(s.split()) for s in sentences(all_text)]
    if lens:
        mean = sum(lens) / len(lens)
        var = sum((x - mean) ** 2 for x in lens) / len(lens)
        band = sum(1 for x in lens if abs(x - mean) <= 3)
        report["sentence_stats"] = {
            "n_sentences": len(lens),
            "mean_words": round(mean, 2),
            "stddev_words": round(var ** 0.5, 2),
            "pct_within_3_of_mean": round(100.0 * band / len(lens), 1),
            "min_words": min(lens), "max_words": max(lens),
        }

    # --- em-dashes -----------------------------------------------------------
    report["em_dashes"] = {
        "body": all_text.count("—"),
        "endnotes": sum(t.count("—") for _, t in notes),
    }

    # Author-identifying tokens to watch for in body + metadata. Configure
    # per author: SUBMISSION_GATE_AUTHOR_TOKENS="surname,given name,..."
    AUTHOR_TOKENS = [tok.strip() for tok in
                     os.environ.get("SUBMISSION_GATE_AUTHOR_TOKENS", "").split(",")
                     if tok.strip()]

    # --- metadata forensics --------------------------------------------------
    report["metadata"] = {
        "creator": core.get("creator", ""),
        "lastModifiedBy": core.get("lastModifiedBy", ""),
        "title": core.get("title", ""),
        "subject": core.get("subject", ""),
        "keywords": core.get("keywords", ""),
        "author_tokens_present": any(
            tok.lower() in all_text.lower() for tok in AUTHOR_TOKENS),
    }

    # --- human-readable ------------------------------------------------------
    print("=" * 70)
    print(f"AI-TELLS REPORT — {report['file']}  (signals, not a verdict)")
    print("=" * 70)
    print(f"\nTIER A (stock LLM diction) hits: {len(report['tier_a_hits'])}")
    for h in report["tier_a_hits"][:50]:
        print(f"  [{h['where']}] /{h['pattern']}/ -> \"{h['match']}\"")
        print(f"      {h['context']}")
    if len(report["tier_a_hits"]) > 50:
        print(f"  … and {len(report['tier_a_hits']) - 50} more (see JSON)")
    print(f"\nTIER B (common transitions — frequency only):")
    if report["tier_b_counts"]:
        for pat, n in sorted(report["tier_b_counts"].items(), key=lambda x: -x[1]):
            print(f"  {pat:45s} {n}")
    else:
        print("  none")
    hd = report["hedge_density"]
    print(f"\nHedging: {hd['hedge_hits']} hits / {hd['words']} words "
          f"= {hd['per_1000_words']} per 1000 words")
    ss = report["sentence_stats"]
    print(f"Sentences: n={ss.get('n_sentences')}, mean={ss.get('mean_words')} words, "
          f"sd={ss.get('stddev_words')}, {ss.get('pct_within_3_of_mean')}% within ±3 "
          f"of mean, range {ss.get('min_words')}–{ss.get('max_words')}")
    print(f"Em-dashes: body={report['em_dashes']['body']}, "
          f"endnotes={report['em_dashes']['endnotes']}")
    md = report["metadata"]
    print(f"Metadata: creator={md['creator']!r} lastModifiedBy={md['lastModifiedBy']!r} "
          f"title={md['title']!r}")
    print(f"Author-name tokens in body text: {md['author_tokens_present']}")
    print("\nDisposition: every Tier A hit is a human decision (fix on a copy if it")
    print("is not the author's voice; keep with a note if it is). Tier B counts,")
    print("hedging, and sentence stats are context only — never evidence alone.")

    with open(stem + "_ai_tells.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nJSON written: {stem}_ai_tells.json")


if __name__ == "__main__":
    main()
