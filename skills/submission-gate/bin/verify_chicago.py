#!/usr/bin/env python3
"""Chicago Humanities (Atlantic Studies / RJAS style sheet) pre-flight verifier.

Machine-checkable subset of the RJAS style sheet, HARDENED 2026-09-18 after a
cold adversarial review caught false greens in v1 (font/size/spacing were only
checked on the Normal style, not the effective document defaults; orphan notes,
meta-text, note clusters, and cited-but-missing references were unchecked).

FAIL = blocks submission. WARN = heuristic, must be dispositioned by a human.
Exit 0 = no FAILs. Exit 1 = failures present.
"""
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
EM_DASH = "\u2014"
MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")


def text_of(root):
    return "".join(t.text or "" for t in root.iter(f"{{{W}}}t"))


def raw_paras(doc_root):
    """List of (xml_string, text) per paragraph."""
    out = []
    for p in doc_root.iter(f"{{{W}}}p"):
        xml = ET.tostring(p, encoding="unicode")
        out.append((xml, text_of(p)))
    return out


def main(path):
    z = zipfile.ZipFile(path)
    raw_doc = z.read("word/document.xml").decode("utf-8")
    raw_en = z.read("word/endnotes.xml").decode("utf-8")
    fails, warns = [], []

    def check(name, ok, detail=""):
        fails.append((name, ok, detail))

    def warn(name, detail=""):
        warns.append((name, detail))

    # ---- 0. OOXML well-formedness (guards string-op build corruption) ----
    # Added 2026-09-18: a v15 fix script curled attribute quotes via a bad
    # w:t regex and produced unparseable XML; nothing downstream can be trusted
    # if the parts don't parse, so this fails first and loud.
    try:
        doc = ET.fromstring(raw_doc)
        check("document.xml well-formed", True)
    except ET.ParseError as e:
        check("document.xml well-formed", False, f"parse error: {e}")
        doc = None
    try:
        ET.fromstring(raw_en)
        check("endnotes.xml well-formed", True)
    except ET.ParseError as e:
        check("endnotes.xml well-formed", False, f"parse error: {e}")
    if doc is None:
        print_report(fails, warns)
        return 1
    paras = raw_paras(doc)
    texts = [t for _, t in paras]
    full = "\n".join(texts)

    # ---- 1. References heading ----
    has_refs = any(t.strip().lower() == "references" for t in texts)
    has_bib = any(t.strip().lower() == "bibliography" for t in texts)
    check("Heading is 'References'", has_refs, "no References heading" if not has_refs else "")
    check("No 'Bibliography' heading", not has_bib, "rename to 'References'" if has_bib else "")

    # ---- 2. Endnotes: present, non-empty, referenced, no orphans ----
    en = ET.fromstring(z.read("word/endnotes.xml"))
    notes = {}
    for e in en.iter(f"{{{W}}}endnote"):
        if e.get(f"{{{W}}}type") in ("separator", "continuationSeparator", "continuationNotice"):
            continue
        notes[int(e.get(f"{{{W}}}id"))] = text_of(e).strip()
    n_real = sum(1 for v in notes.values() if v)
    check("Endnotes present (>=10)", n_real >= 10, f"found {n_real}")
    empty_ids = sorted(k for k, v in notes.items() if not v)
    check("No empty orphan endnotes", not empty_ids, f"empty note ids: {empty_ids}" if empty_ids else "")

    ref_ids = [int(x) for x in re.findall(r'<\w+:endnoteReference\b[^>]*?\bid="(\d+)"', raw_doc)]
    # fallback for non-prefixed serialization
    if not ref_ids:
        ref_ids = [int(x) for x in re.findall(r'endnoteReference[^>]*?id="(\d+)"', raw_doc)]
    unrefed = sorted(set(notes) - set(ref_ids) - {0})
    check("Every endnote referenced in body", not unrefed, f"unreferenced: {unrefed}" if unrefed else "")
    dangling = sorted(set(ref_ids) - set(notes))
    check("Every body reference resolves", not dangling, f"dangling refs: {dangling}" if dangling else "")

    # ---- 3. No multi-note clusters (sheet: avoid >1 ref at one location) ----
    clusters = 0
    for xml, _ in paras:
        # ET re-serializes prefixes; match on local name in the raw paragraph xml
        tags = re.findall(r'<\w*:endnoteReference\b[^>]*?/>', xml)
        if len(tags) < 2:
            continue
        segs = re.split(r'<\w*:endnoteReference\b[^>]*?/>', xml)
        for g in segs[1:-1]:
            if len(re.sub(r'<[^>]+>', '', g).strip()) < 30:
                clusters += 1
                break
    check("No multi-note clusters", clusters == 0, f"{clusters} paragraphs with clustered refs" if clusters else "")

    # ---- 4. Em-dashes ----
    en_text = text_of(en)
    em = full.count(EM_DASH) + en_text.count(EM_DASH)
    check("Zero em-dashes", em == 0, f"{em} found — use ' – '" if em else "")

    # ---- 5. Disclosure ----
    check("Disclosure present",
          "no potential conflict was reported by the author" in full.lower())

    # ---- 6. Abstract (may span several paragraphs) / keywords ----
    HEADS = {"abstract", "keywords", "notes", "references", "disclosure",
             "acknowledgements", "acknowledgments", "notes on contributors"}
    abstract_parts = []
    for i, t in enumerate(texts):
        if t.strip().lower() == "abstract":
            for u in texts[i + 1:]:
                if u.strip().lower() in HEADS:
                    break
                if u.strip():
                    abstract_parts.append(u.strip())
            break
    abstract = " ".join(abstract_parts)
    aw = len(abstract.split())
    check("Abstract <= 150 words", 0 < aw <= 150, f"{aw} words")
    kws = next((texts[i + 1] for i, t in enumerate(texts)
                if t.strip().lower() == "keywords" and i + 1 < len(texts)), "")
    nk = len([k for k in kws.split(";") if k.strip()])
    check("Keywords <= 6", 0 < nk <= 6, f"{nk} found")

    # ---- 7. Section order ----
    low = [t.strip().lower() for t in texts]
    i_notes = low.index("notes") if "notes" in low else -1
    i_refs = low.index("references") if "references" in low else -1
    check("Notes precedes References", -1 < i_notes < i_refs, f"notes@{i_notes} refs@{i_refs}")

    # ---- 8. Anonymity ----
    # Author-identifying tokens are configured per author, never hardcoded:
    # SUBMISSION_GATE_AUTHOR_TOKENS="surname,given name,..."
    _tokens = [tok.strip().lower() for tok in
               os.environ.get("SUBMISSION_GATE_AUTHOR_TOKENS", "").split(",")
               if tok.strip()]
    _core = z.read("docProps/core.xml").decode("utf-8", "ignore").lower()
    check("Anonymous body/metadata",
          all(tok not in full.lower() and tok not in _core for tok in _tokens),
          "tokens from SUBMISSION_GATE_AUTHOR_TOKENS"
          if _tokens else "no author tokens configured")

    # ---- 9. EFFECTIVE font/size/spacing: docDefaults (the false-green fix) ----
    styles = ET.fromstring(z.read("word/styles.xml"))
    dd = styles.find("w:docDefaults", {"w": W})
    dd_font = dd_sz = dd_line = False
    if dd is not None:
        rpr = dd.find("w:rPrDefault/w:rPr", {"w": W})
        if rpr is not None:
            rf = rpr.find("w:rFonts", {"w": W})
            if rf is not None:
                a = (rf.get(f"{{{W}}}ascii") or "")
                dd_font = a.lower() == "times new roman" or "theme" not in (rf.get(f"{{{W}}}asciiTheme") or "").lower() and a == ""
                # explicit non-theme TNR required
                dd_font = a.lower() == "times new roman"
            szv = rpr.find("w:sz", {"w": W})
            dd_sz = szv is not None and szv.get(f"{{{W}}}val") == "24"
        ppr = dd.find("w:pPrDefault/w:pPr", {"w": W})
        if ppr is not None:
            sp = ppr.find("w:spacing", {"w": W})
            dd_line = sp is not None and sp.get(f"{{{W}}}line") == "480"
    check("docDefaults: Times New Roman (effective font)", dd_font,
          "theme font inherits (renders wrong for unstyled text)" if not dd_font else "")
    check("docDefaults: 12pt", dd_sz, "" if dd_sz else "")
    check("docDefaults: double-spaced", dd_line, "" if dd_line else "")

    # ---- 10. References alphabetical (Chicago ignores leading punctuation) ----
    def sort_key(t):
        return re.sub(r"^[^\w]+", "", t.strip()).lower()
    alpha_ok, alpha_detail = True, ""
    if i_refs != -1:
        refs = [t for t in texts[i_refs + 1:] if t.strip()]
        keys = [sort_key(t)[0] for t in refs if sort_key(t)]
        for a, b in zip(keys, keys[1:]):
            if b < a:
                alpha_ok, alpha_detail = False, f"break '{a}'->'{b}'"
                break
    check("References alphabetical", alpha_ok, alpha_detail)

    # ---- 10b. No "U.S." with periods (sheet wants "US"; scan body AND endnotes) ----
    en_text_all = " ".join(v for v in notes.values())
    check("No 'U.S.' with periods", "U.S." not in full and "U.S." not in en_text_all,
          "found 'U.S.' — use 'US'" if ("U.S." in full or "U.S." in en_text_all) else "")

    # ---- 10c. Style-sheet punctuation guards (added 2026-09-18, v16 fix-up) ----
    # Bare author-inserted ellipses: the sheet requires square brackets ('[…]').
    def bare_ell(x):
        return [m for m in re.finditer("\u2026", x)
                if not (m.start() > 0 and x[m.start() - 1] == "[" and
                        m.end() < len(x) and x[m.end()] == "]")]
    n_bare = len(bare_ell(raw_doc)) + len(bare_ell(raw_en))
    check("No bare ellipses (sheet: '[…]')", n_bare == 0,
          f"{n_bare} bare '…' found — bracket them" if n_bare else "")

    # Endnote number before punctuation: sheet says the number follows any
    # punctuation mark (except a dash). Scan the raw XML so runs don't hide it.
    def note_before_punct(x):
        hits = []
        for m in re.finditer(r"<\w*:endnoteReference\b[^>]*?/>", x):
            after = x[m.end():m.end() + 600]
            t = re.search(r"<\w*:t[^>]*>(.*?)</\w*:t>", after)
            if t and t.group(1) and t.group(1)[0] in ".,;:":
                wid = re.search(r'id="(\d+)"', m.group(0))
                hits.append(f"note w:id={wid.group(1) if wid else '?'} before '{t.group(1)[:16]}'")
        return hits
    nbp = note_before_punct(raw_doc) + note_before_punct(raw_en)
    check("Endnote numbers follow punctuation", not nbp,
          "; ".join(nbp[:4]) if nbp else "")

    # Abbreviated ranges (sheet: "Page ranges are not abbreviated", "All digits
    # using an en-dash"): warn for human disposition, because published titles
    # must be quoted faithfully even when they abbreviate (e.g. "1644–45").
    abbr = []
    for x in (raw_doc, raw_en):
        for m in re.finditer(r"(\d{2,4})\s*[–—-]\s*(\d{1,4})", re.sub(r"<[^>]+>", " ", x)):
            a, b = m.group(1), m.group(2)
            if len(b) < len(a):
                abbr.append(m.group(0))
    abbr = sorted(set(abbr))
    for a in abbr:
        warn("Abbreviated range (sheet wants all digits; skip if a published title)", a)

    # Series-comma census (sheet: US or UK acceptable if consistent). Strict
    # patterns; known false positives: number phrases ("three and a half"),
    # two-item pairs, and the tail of a long Oxford series. Both styles present
    # at nonzero counts = human audit.
    body_txt = "\n".join(texts[:i_notes] if i_notes > 0 else texts)
    ox = set()
    for m in re.finditer(r"\b[\w'’\-]+(?:,\s+[\w'’\-]+){1,},\s+and\s+[\w'’\-]+", body_txt, re.I):
        ox.add(" ".join(m.group(0).split()).lower())
    uk = set()
    for m in re.finditer(r"\b[\w'’\-]+(?:,\s+[\w'’\-]+)+\s+and\s+[\w'’\-]+", body_txt, re.I):
        s = " ".join(m.group(0).split()).lower()
        if not re.search(r",\s+and\s", s):
            uk.add(s)
    warn("Series-comma census", f"Oxford-style: {len(ox)}, UK-style: {len(uk)} "
         f"(sheet allows either if consistent; inspect UK hits for false positives)")

    # Container title italics in References: the sheet's chapter-in-book model
    # italicizes the containing work. Targeted guard (added for the
    # PORTUGAL./Jewish Encyclopedia miss).
    if "The Jewish Encyclopedia" in raw_doc:
        italic_hits = re.findall(
            r'<w:rPr>.*?w:i(?: w:val="(?:1|true)")?.*?</w:rPr>\s*<w:t[^>]*>The Jewish Encyclopedia</w:t>',
            raw_doc)
        plain_hits = len(re.findall(r">The Jewish Encyclopedia</w:t>", raw_doc))
        if len(italic_hits) < plain_hits:
            warn("Container title may not be italicized",
                 f"'The Jewish Encyclopedia': {len(italic_hits)}/{plain_hits} italic")

    # ---- 11. No production meta-text inside manuscript ----
    check("No 'Submission note' meta-text", "submission note" not in full.lower(),
          "remove before submission" if "submission note" in full.lower() else "")

    # ---- 12. Access-date format: 'Accessed D Month Year' ----
    bad_dates = re.findall(rf"Accessed\s+(?:{MONTHS})\s+\d{{1,2}},\s+\d{{4}}", full)
    check("Access dates 'D Month Year'", not bad_dates, f"US-format dates: {bad_dates[:3]}" if bad_dates else "")

    # ---- 13. Every work cited in notes appears in References (Albacete rule) ----
    refs_text = " ".join(texts[i_refs + 1:]).lower() if i_refs != -1 else ""
    missing = []
    for nid, ntext in sorted(notes.items()):
        if not ntext or nid == 0:
            continue
        m = re.match(r"\s*([A-ZÀ-Ž][\w'’\-\.]+)", ntext)
        if not m:
            continue
        surname = m.group(1).strip(".'").lower()
        if len(surname) < 3:
            continue
        if surname not in refs_text:
            missing.append(f"n{nid}:{m.group(1)}")
    check("All cited works in References", not missing, f"missing: {missing[:5]}" if missing else "")
    # embedded second-hand citations: "citing X", "quoted in X"
    for nid, ntext in sorted(notes.items()):
        if not ntext or nid == 0:
            continue
        for m2 in re.finditer(r"(?:citing|quoted in|cited in|see also)\s+([A-ZÀ-Þ][\w'’\-]+)", ntext):
            if m2.group(1).lower() not in refs_text:
                warn("Second-hand citation not in References", f"n{nid}: '{m2.group(1)}' via '{m2.group(0)[:40]}'")

    # ---- WARNINGS (heuristic, human-dispositioned) ----
    # journal entries without page ranges
    if i_refs != -1:
        for t in texts[i_refs + 1:]:
            if not t.strip():
                continue
            if re.search(r"no\.\s*\d+|\(\w+ \d{4}\)", t) and "http" not in t \
               and not re.search(r":\s*\d+\s*[–-]\s*\d+", t) and "Vol" not in t:
                warn("Reference may lack page range", t[:90])
    # subheading sentence case: short bold paras
    # (bold detection is namespace-agnostic: ET.tostring uses ns0: prefixes)
    for xml, t in paras:
        s = t.strip()
        if 0 < len(s) < 90 and s.lower() not in ("abstract", "keywords", "notes", "references", "disclosure"):
            if re.search(r"<\w+:b[\s>/]", xml) and not s.endswith((".", ":", ";")):
                words = re.findall(r"[A-Za-zÀ-ž']+", s)
                caps = [w for w in words[1:] if w[0].isupper()]
                if len(caps) >= 2 and not re.match(r"\d", s):
                    warn("Possible Title-Case subheading", s[:70])

    # manual "(see note N)" cross-references: resolve against rendered numbering
    # and force human review — any note merge/add/delete silently breaks these
    if ref_ids:
        rendered_ids = [i for i in ref_ids if i in notes]
        for xml, t in paras:
            for m in re.finditer(r"\(see note (\d+)\)", t):
                n = int(m.group(1))
                if 1 <= n <= len(rendered_ids):
                    target = notes.get(rendered_ids[n - 1], "")[:60]
                    warn("Cross-ref audit", f"'(see note {n})' -> note {n} ({target}...)")
                else:
                    warn("Cross-ref audit", f"'(see note {n})' OUT OF RANGE (1-{len(rendered_ids)})")

    # ---- report ----
    print_report(fails, warns)
    return 1 if any(not ok for _, ok, _ in fails) else 0


def print_report(fails, warns):
    width = max([len(n) for n, _, _ in fails] + [0])
    nfail = 0
    for name, ok, detail in fails:
        if not ok:
            nfail += 1
            print(f"[FAIL] {name:<{width}} {detail}")
        else:
            print(f"[PASS] {name:<{width}} {detail}")
    for name, detail in warns:
        print(f"[WARN] {name}: {detail}")
    print(f"\n{len(fails) - nfail}/{len(fails)} checks green, {len(warns)} warnings")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
