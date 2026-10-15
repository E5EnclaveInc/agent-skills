---
name: submission-gate
description: "Preflight any scholarly manuscript against the target journal's actual written instructions before submission, so technical returns never happen. Use when preparing, revising, or rechecking a journal submission — 'run the gate', 'preflight this manuscript', 'is this submission-ready', 'cold-review against the journal'. Works from the journal's own author instructions first, encodes every checkable requirement mechanically (including author-anonymization guards), then adversarially reviews what machines cannot check."
license: MIT
compatibility: "Requires Python 3 (python-docx not needed; scripts work on raw OOXML via stdlib)."
metadata:
  version: 1.0.0
---
# Submission Gate

## What this is

Pattern B (process primitive) with Pattern A scripts for the deterministic checks: instructions live here, mechanics live in code. The doctrine:

1. Retrieve the current target-journal instructions and style sheet (the live source of truth, never memory).
2. Encode every deterministic requirement as machine checks and run the manuscript until all pass.
3. Perform an independent source-instructions-first cold review of the full package.
4. Simulate the journal's technical editorial assistant (what they will bounce on).
5. Verify venue fit, article type, anonymity, AI-use policy, and declarations.
6. Add every newly discovered failure mode to this gate permanently.

No submission goes out until steps 1-5 are green. No file is replaced externally without the user's exact authorization.

## Hard rules

- **Source instructions first.** The journal's author guidelines and style sheet are the spec. Before any check runs, fetch or re-read the current versions. Memory of "what the journal wants" is not evidence.
- **Nothing invented.** No invented citations, editions, page numbers, DOIs, or bibliographic data. A check that cannot be sourced is left as an open question for the user, not filled in.
- **Anonymity holds** until the submission system says otherwise. Metadata, headers, running heads, acknowledgments, and file properties get scrubbed.
- **Act-then-report within the manuscript; external acts need the word.** Rewriting the DOCX is reversible work — do it, then report. Submitting, replacing a file in Editorial Manager, or contacting an editor is never done without exact authorization.

## Scripts (bin/)

- `bin/verify_chicago.py` — hardened verifier for Chicago Humanities / Atlantic Studies-style manuscripts. Checks: Normal-style font/size/spacing, docDefaults alignment, abstract word cap, keyword cap, endnote count and clustering, Reference list completeness, style-sheet conformance (sentence-case headings, spaced en-dashes, access-date format, hanging indents), no "U.S." with periods (body and endnotes), References alphabetical with Chicago sort key (leading punctuation ignored). Always emits a "(see note N)" cross-reference audit table (WARN level) resolving each manual cross-reference against rendered note numbering — review it after every note merge/add/delete.
- The manuscript builder (pattern, not shipped): in production this gate pairs the verifier with a per-manuscript builder script that rebuilds the DOCX programmatically — title page, abstract, heading map, and endnote scaffolding generated from the manuscript's own structured text rather than hand-edited XML. The builder is intentionally not shipped here because a real one embeds its manuscript's actual title, abstract, and section map; write one per manuscript following the verifier's contract, and rebuild through it rather than hand-editing XML whenever a change is mechanical and repeatable.

Keep documentation in sync with scripts: any script change updates this file the same session.

## The attribution test (learned from Meta Engineering, 2026-09)

When anything in this gate fails — a verifier flag, a cold-review finding, an actual journal return — run the root-cause attribution test before fixing. Meta's team found the obvious heuristic wrong (information correction is not automatically a knowledge gap; a redirect is not automatically a procedure flaw). Use the single question:

> **Could the agent have reached the correct conclusion from the materials it had?**

- If yes, but it still erred: **procedure flaw.** Fix the process — the check, the builder step, the review protocol. Do not touch the knowledge.
- If no, the materials were insufficient: **knowledge gap.** Fix the knowledge — the style-sheet encoding, the journal instructions snapshot, the checklist. Do not touch the procedure.
- If experts (or the style sheet, or the instructions) themselves disagree or are silent: **genuine ambiguity.** Flag it to the user as an open decision, never guess.

Each class lands in a different place. A procedure flaw that gets "fixed" by adding a checklist entry is a fix in the wrong layer and will recur. A knowledge gap "fixed" by editing the verifier's thresholds is the same error in reverse. Attribute first, edit second.

## Fresh-context adversarial review (learned from Meta Engineering, 2026-09)

The gate's cold review is this gate's version of Meta's independent adversarial review. Run it with the discipline that makes it adversarial rather than ceremonial:

- **Fresh context.** The reviewing subagent starts from the journal's instructions and style sheet plus the manuscript package. It must NOT inherit the proposing agent's rationale, fix history, or confidence. Pass it the artifact, not the story.
- **Artifact-only scope.** It receives the manuscript and the source instructions. Its job is to find problems the proposer is blind to: contradictions introduced by fixes, checks the verifier cannot run, venue-fit risks, anything the builder might have broken while fixing.
- **Blind replay where possible.** When the verifier says green, the cold reviewer re-derives the verdict from the instructions independently rather than spot-checking the verifier's report. It asks "does this satisfy the style sheet?" — not "did the verifier miss anything?"
- **Every finding dispositioned.** Each cold-review finding ends in one of three states: fixed and re-verified, proven false positive (with evidence), or logged as an open scholarly choice for the user. "Addressed" without evidence is not a state.

A review that had access to the fix rationale shares the fixer's blind spots. Keep the reviewer blind to the rationale and pointed at the instructions.

## Verification loop (door-verify)

1. Run `bin/verify_chicago.py` on the rebuilt manuscript. All deterministic checks green or explicitly dispositioned.
2. Render or open the actual manuscript and visually confirm effective font, size, spacing, endnotes, References, and pagination. Inherited XML defaults (docDefaults) lie; the rendered page does not.
3. Run the fresh-context adversarial cold review (above).
4. Run the journal-assistant simulation: read the package as the technical editor who returned it last time and try to find a bounce.
5. Surface the cleared manuscript plus any genuinely open scholarly decisions to the user. Do not submit.

## AI-suspicion audit module (added 2026-09-18)

The gate verifies the manuscript obeys the style sheet. This module verifies
it survives AI-suspicion: the referee's eye, software forensics, and the
venue's actual AI policy. Posture throughout is **disclosure, not evasion**:
the audit protects honest, disclosed AI-assisted work from false suspicion.
It is never used to launder AI authorship into fake human authorship.

### When it runs

After the verification loop is green, before any submission or file
transmission. It runs on the final candidate file (e.g. v17), not on every
intermediate.

### What it checks

1. **Tell-lexicon scan** — `bin/ai_tells.py <manuscript.docx>` (deterministic,
   report-only, exit 0 always). Reports: Tier A hits (stock LLM diction:
   delve/tapestry/testament-to/sheds-light-on and kin — curated for a
   humanities register) with per-hit locations and context; Tier B frequency
   counts (common transitions like moreover/furthermore — context only, never
   evidence); hedging density per 1000 words; sentence-length mean/stddev and
   the share within ±3 words of the mean (burstiness proxy); em-dash count;
   document metadata (creator, lastModifiedBy, title) and author-name tokens
   in body text. Emits a human-readable report plus `<stem>_ai_tells.json`.
   Output is signals, never a verdict.
2. **Metadata forensics** — blank creator/lastModifiedBy/title/subject,
   no author tokens in body/notes/references text, no AI-service fingerprints.
   (Author tokens are configured per author via the `SUBMISSION_GATE_AUTHOR_TOKENS`
   env var — `verify_chicago.py` and `ai_tells.py` read it; never hardcode a name.)
   (Covered by ai_tells.py; re-verify after any rebuild.)
3. **Venue AI-policy check** — against `references/ai-policy-matrix.md`
   (official publisher pages, retrieved 2026-09-18, re-fetch when stale).
   Confirm: no AI listed as author; the venue's required disclosure elements
   are present (T&F: tool name + version, how used, reason — "a specific
   statement of AI usage disclosure must be included" for articles; Sage:
   generative use disclosed in methods or acknowledgements with tool, use,
   and rationale); no prohibited uses (text generation without rigorous
   revision, synthetic data, AI-generated research images).
4. **Provenance log** — `references/provenance-log-<slug>.md` (template:
   `references/provenance-log-TEMPLATE.md`). Per-version record of human
   author vs. agent revision, human-reserved decisions, and negative
   attestations (no AI images, no AI-generated citations, no synthetic data,
   no pasting into third-party AI services, human retains final sign-off).
   The log is the evidence behind the disclosure statement. State only what
   files, hashes, and dated records evidence.
5. **Detector self-test** — manual, optional, intelligence only. See
   `references/detector-self-test.md`. Never automated, never a gate, never
   a server-side third-party upload of an unpublished manuscript.

### How findings are dispositioned

- **Unambiguous mechanical marker** (e.g. a Tier A phrase that is not the
  author's voice, a stray em-dash): fix on a NEW copy, re-verify at XML
  level. Never silently wholesale-rephrase the author's prose or voice.
- **Stylistic query** (a Tier A hit that may be legitimate authorial diction,
  an unusual Tier B spike): flag with location and context for the human
  author. Their call.
- **Policy gap** (e.g. missing required disclosure statement): draft the
  venue-compliant wording from the provenance log, but the human author
  finalizes it — a disclosure statement is their signed declaration.
- **Detector score** (if the manual step was run): intelligence only. A high
  score on honest work is a data point about the tool, not about the work.

### Failure modes this module has already learned

- v17 carried no AI-usage disclosure statement at all (found 2026-09-18):
  its "Disclosure statement" section held only the style sheet's
  conflict-of-interest model text, while T&F's policy requires "a specific
  statement of AI usage disclosure" naming tool + version, how used, and
  reason for use. A conflict-of-interest disclosure is not an AI disclosure.
  The gate now checks for the venue's required disclosure elements as a
  distinct item, not as "a disclosure section exists."

## Failure modes this gate has already learned (each was a real miss)

- A verifier that only reads declared styles while the document renders from inherited defaults → align docDefaults AND styles explicitly, then verify by rendering.
- Reading only the first paragraph of a multi-paragraph abstract → count all abstract paragraphs against the word cap.
- Treating Word's `continuationSeparator` endnote (ID 1) as a substantive orphan note → it is infrastructure, never delete it.
- Over-merging endnotes: multiple notes attached to separate claims in one paragraph are usually correct; consolidate only when one note clearly serves one claim.
- US-order access dates where the journal wants day-month-year → encode the exact format.
- Em-dashes where the style sheet wants spaced en-dashes; title-case headings where it wants sentence case.
- Second-hand citations (X citing Y) and incomplete edition data are scholarly questions, not machine-fixable → disposition via sources, never invention.
- Manual "(see note N)" cross-references go stale silently when notes merge or renumber → the verifier now resolves each one against rendered numbering and forces a human audit every run.
- Fix scripts that only scan document.xml miss endnotes.xml ("U.S." survived in a note after the body was fixed) → full-text checks must cover body AND endnotes.
- ET.tostring uses ns0: prefixes, so literal "<w:b" substring checks never match → bold/italic detection must be namespace-agnostic.
- A digit-anywhere guard on the title-case heuristic skips headings containing years ("After 1492: ...") → guard only on leading digits.
- Alphabetical check on raw first characters false-fails title-first entries ("PORTUGAL") → Chicago sort key ignores leading punctuation.
- APA §9.47 same-first-author rule (learned 2026-09-18, RBPE pass): same first author orders by the SECOND author's surname (then third, …), not by year — year-ordering applies only to identical author lists. An agent-encoded "same author → chronological" rule silently misordered Aladangady (2023) after Aladangady & Forde (2021); the correct order is Chang (2023) before Forde (2021). Verify the rule against an authoritative APA source before encoding it.
- Abstract word caps are counter-dependent (learned 2026-09-18): "Black–White" counts as 1 or 2 words depending on whether the counter splits en-dashes; hyphenated compounds vary too. Verify under the strictest plausible counter (Word-style: en/em dash splits, hyphen does not) and trim to clear the cap by margin, never to the edge.
- Cover-letter figures go stale on rebuild (learned 2026-09-18): word count, abstract words, and table/figure counts asserted in the cover letter must be re-synced from the rebuilt manuscript every run.
- Verifier regexes must be tested against the data's own characters (learned 2026-09-18): a "trailing period after DOI" check using `\S+\.` false-flagged every entry because DOIs contain periods — inspect the final token only.
- Rebuilds drop title-page fields silently (learned 2026-09-18, RBPE v0.5→v0.6): regenerating the title page from the master source lost the corresponding-author phone/address line that the prior version carried — the likeliest technical-return item. On every rebuild, diff the new title page's identifying block against the prior version's before accepting it.
- Cold reviewers must resolve "(see note N)" against DISPLAY order, never raw w:id (learned 2026-09-18, v14 cold review): Word numbers endnotes sequentially by document order; raw w:id gaps (deleted/merged notes, infrastructure ID 1, inserted out-of-order IDs) are invisible to readers. A reviewer that treats w:id as the displayed number will report every cross-reference broken when all are correct. LibreOffice additionally renders endnote marks as lowercase roman by default (Word shows arabic) — never infer the reader's numbering from a renderer's default.
- Cold reviewers must quote exact manuscript text for every finding (learned 2026-09-18, v14 cold review): the reviewer hallucinated a References entry ("Pike's 'Black Society in Spain'") that does not exist in the manuscript and misattributed the Santos Silva & Tavares title. A finding without a verbatim manuscript quote is not a finding.
- String-op OOXML builds must assert well-formedness after every run (learned 2026-09-18, v14→v15): a `w:t` regex that also matched self-closing `<w:t .../>` tags glommed across runs and curled attribute quotes, producing unparseable XML. The verifier now fails on malformed document.xml/endnotes.xml before any other check. Related: `<w:t[^>]*>` matches `<w:tabs>`, `<w:tab/>`, `<w:tr>` — always anchor the tag name with `[\s>]`.
- Style-sheet punctuation classes need dedicated raw-XML scans (learned 2026-09-18, v15→v16 blind review): bare author-inserted ellipses (sheet wants `[…]`), endnote numbers preceding punctuation (sheet: number follows punctuation except before a dash), and abbreviated page/date ranges (sheet: all digits, unspaced en-dash) all survived multiple earlier passes because no check encoded them. `verify_chicago.py` now carries: a bare-ellipsis FAIL, an endnote-before-punctuation FAIL (raw-XML scan, covers body and notes), an abbreviated-range WARN (human-dispositioned, since published titles must be quoted faithfully even when they abbreviate), a series-comma census WARN (Oxford vs UK counts; known regex false positives: number phrases like "three and a half", two-item pairs, and the tail of a long Oxford series), and a container-title-italics WARN for References chapter entries. The same pass caught one additional instance the review missed (note 16 before a comma) — the new scan class pays for itself immediately.
- Blind-review misreads of the sheet must be re-verified against the sheet itself (learned 2026-09-18, v16 fix-up): the v15 cold review reported the sheet's edition model as "2 ed." when the sheet actually prints "2nd ed." — which made the manuscript's "3rd ed." compliant, not deviant. Treat every reviewer-cited sheet rule as a claim to check against the PDF, not as fact.

- Series-comma census regexes must allow multi-word items (learned 2026-09-18, v16→v17): the v16 census pattern only matched single-word items (`\w+`), so "Sierra Leone and the Rio Nunez" — a genuine UK-style no-comma series — passed as clean and the log wrongly concluded "Oxford 16, UK 0". The corrected census allows up to 3 words per item and found 22 candidates; all remaining ones are two-item pairs, author pairs, or a published title (never altered). A census that cannot match the manuscript's own noun phrases is not a census.
- LibreOffice does not honor `w:endnotePr w:pos="sectEnd"` (learned 2026-09-18, v17): endnotes render at document end regardless of section-end positioning. Endnote-placement fixes can only be XML-verified (schema-ordered sectPr: footerReference, endnotePr, type, pgSz, pgMar) plus render-verified for no-layout-regression; true placement verification needs Word. Never declare a placement fix "render-verified" from LibreOffice alone.
- Paragraph-level sectPr elements must follow CT_SectPr schema order (learned 2026-09-18, v17): footerReference, footnotePr, endnotePr, type, pgSz, pgMar, … — Word tolerates out-of-order elements but strict readers may not; the fix script now asserts the order by regex.
- w:id gaps and out-of-order ids in endnotes.xml are benign Word renumbering artifacts (learned 2026-09-18, v17): v17 has no w:id 23 and w:id 49 sorts before 45 in file order, yet all 47 endnoteReferences resolve 1–47 in document order. Verify by reference order, never by id sequence; a reviewer flagging "missing note 23" from raw ids is reporting an artifact, not a defect.
- References italics need a run-level audit the verifier never ran (learned 2026-09-18, v18→v19): Chicago 16th bibliography styling is per-run — author names roman, book/journal titles italic, article/chapter titles roman inside quotation marks, place/publisher/year/edition roman. `verify_chicago.py` checked none of this. Audit every References entry's runs mechanically against that mapping before submission.
- `<w:i w:val="0"/>` is explicitly NOT italic (learned 2026-09-18, v18→v19): a naive grep for `<w:i` false-flagged 20 References entries' author-name runs as italic when the XML actually carried `<w:i w:val="0"/>` (italic off) — confirmed by the LibreOffice render showing roman author names. The v18 blind review's DEFECT-1 ("italic author names, confirmed in raw XML") was this misread. Any italics check must parse the val attribute: absent/`1`/`true`/`on` = on; `0`/`false`/`off` = off; no element = off (absent a style default). A finding that quotes `<w:i` without the val is not a finding.
- Endnote w:numFmt must be decimal-family, asserted in the XML (learned 2026-09-18, v18→v19): with no `<w:numFmt/>` in w:endnotePr, Word defaults endnote numbers to lowercase roman (i, ii, iii) even though the style sheet's model is Arabic ("16."). LibreOffice also renders endnotes as lowercase roman by default, so the LO render masks the defect instead of revealing it. Fix: `<w:endnotePr><w:pos w:val="sectEnd"/><w:numFmt w:val="decimalEnclosedFullstop"/></w:endnotePr>` — renders "1." per the sheet; a renderer that ignores the value falls back to decimal, still strictly better than roman. Verify in the XML; the LO render cannot confirm it.
- LibreOffice render artifacts are not DOCX defects (learned 2026-09-18, v18→v19): LO ignores `w:endnotePr w:pos="sectEnd"`, so endnote text renders at document end (after References) regardless of the XML's section-end positioning — the v18 blind review's DEFECT-4 ("notes print after References") was an LO artifact; the XML proves Word order (body → continuous section break → Disclosure → References, endnote text at end of section 1). LO likewise cannot verify endnote numbering format. Render-verify layout only; verify order/numbering against the XML.

Add each new miss here the session it is found, with what actually happened. Nothing breaks twice.
