# Ontology Grounding Report — 2026-09-12

**Method:** key design terms run through the house Ontology Floor's `resolve()`
(your ontology-floor skill's `scripts/resolve.py`) against the live
`seed_corpus.json` (16 records).

**Result: 10/10 missed, 0 refused, confidence 0.0.**
Terms tested: `cinematic hero`, `motion budget`, `icon upscale`, `gold leaf`,
`three js`, `turnstile`, `landing page`, `color contrast`, `hero section`, `call to action`.

**Interpretation (fail-closed):** the floor's proven regime is hard/rare physical
formalisms (measured +18pp hallucination reduction there, p=0.002; "a wash" on easy
classics). Design-doctrine terms are not in that regime — they carry no mathematical
proof object the floor could verify, and attempting to force them through the ingest
gates would game the gates, not ground the terms. So per the fail-closed doctrine,
these terms are **marked, not asserted**:

1. **Marked as floor-misses** — no claim of ontology-floor grounding is made anywhere
   in this skill.
2. **Grounded operationally in-skill** — `ontology/design_terms.json` gives each term
   a checkable definition + measurement method + pass/fail thresholds. A definition
   you can test is worth more than a vibe you can't.
3. **Math-bearing terms formally specified in-skill** — `contrast_ratio` (WCAG 2.1
   formula) and `motion_budget`/`icon_upscale` (frame-budget and DPR scaling math)
   carry the actual formula and its standard reference, marked **skill-local** rather
   than floor-grounded. Honest about the boundary.
4. **Aesthetic terms stay aesthetic** — `gold_leaf`, `bespoke_layout`,
   `cinematic_hero` are doctrine, checkable via design review, never computed.
   The floor's Abu-Heru boundary (never compute a value) is respected by analogy:
   taste is not a formula.

**Re-check trigger:** if the floor's corpus later gains design-relevant formal records
(e.g. a color-science or perceptual-motion record via the daily ingest), re-run
`resolve()` and promote any exact matches. Until then, this report stands.
