# Worked Example — the No. 01 Merged Build

The skill's first run: Playbook No. 01 ("The skeptic's audit"), 2026-09-19.
This is what the workflow looks like when followed end to end.

## What was chosen
- **Foundation:** Direction A (Atelier Ledger) — warm workshop paper, ledger serif, brass measuring tape.
- **Adopted from B:** the 48px scroll cue, with B's war-room corrections (real 48px touch target, aria-label, real anchor, arrow SVG inlined — never `<use href="icons.svg#…">` — curly quotes normalized to straight).
- **Adopted from C:** the measuring-tape scroll-progress timeline, contrast-corrected.
- The approver's verdict on the shipped result: "Absolutely beautiful."
- Shipped live as the publication's Issue No. 01 page (attestation sequence 111), 14/14 design-gate pass, 32/32 frozen blocks byte-identical, 22 virtual-iPhone screenshots all green, zero console errors, $0 spend.

## Defects caught and fixed (do not reintroduce)
1. **Tape numerals 2.60:1 → 12.99:1.** C's numerals sat *on* the advancing fill; ink on the amber-deep gradient end measured 2.60:1 — a WCAG failure. Two independent guarantees now: the advancing fill is a solid `--ss-tape-fill` (never the gradient), and the fill is confined to the 14px tick band while numerals live in their own 24px band on the paper-deep track — the fill can never slide under the numerals by construction. Tape numerals always read ≥4.5:1 on their track (12.99:1 in the merged build; 12.39–15.46:1 across the variants).
2. **Reduced-motion cascade guard.** A direction-level reveal override sat after the system's reduced-motion `transition: none` at equal specificity, re-enabling transitions under `prefers-reduced-motion`. Rule, now canonical: direction-level reveal overrides, if any, live inside `@media (prefers-reduced-motion: no-preference)`; the merged build carries none at all. Motion essentials: `data-reveal` IntersectionObserver reveals, `sawdust-motes` canvas (never starts under reduced-motion), tape advance jumps with no animation under reduced-motion, anchors jump natively.
3. **Fonts vendored same-origin.** CDN-loaded Google Fonts (measured ~613KB served) replaced with 4 vendored woff2 + OFL.txt (measured ~53KB served). No Google Fonts CDN anywhere — the merge gate fails any external font request.
4. **Contrast parser defects** (from the variant build that followed): a `[data-theme="dark"]` string inside a CSS *comment* truncated naive token parsing — parse the first top-level `:root { … }` with a regex. Copy verifier confused identical strings across removed sections ("Where does our data go?" appears twice) — position-based exclusion using source character offsets, not multiset subtraction.

## Evidence layout (verify before citing)
In the project's design-system working directory, the merged build keeps:
the page (`no-01.html`) and its motion fork (`no-01-motion.js`); the gate
report (`gate-report.json` — 14/14, verdict PASS, zero fail-closed
violations); screenshots under `qa/` (22 PNGs — motion-on, reduced-motion,
reduced-transparency-emulation-unsupported, no-JS rungs — plus a run-meta.json
console log); and the fix log (`FIXES.md`) and copy diff (`TEXT_DIFF.md`,
32/32 byte-identical) beside the build.

## The five-variant proof set
The same recipe then produced five rendered variants from the merged build — the skill's standing proof that the token-delta method yields distinct, gate-passing designs. Cataloged in `VARIANT_CATALOG.md`; sources in the project's design-system variants directory with `index.html` comparison, `TEXT_MANIFEST.md` (44/44 copy-freeze per variant), `qa/contrast.json`, and `qa-shots/` (28 PNGs: virtual-iPhone 390px + desktop, 0 console errors, firsthand-reviewed 2026-09-19). The v05 phone-hero capture was corrupted by a dying WebKit lane and re-shot clean via Chromium — recorded in `qa-shots/SHOT_LOG.md`. Lesson carried forward: never cite contrast from the catalog as screenshots for a new build — new variants still run step 5 fresh.
