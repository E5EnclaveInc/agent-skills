# Variant Catalog — five shipped variants of Playbook No. 01

The living catalog. Pick per the rotation rule in the workflow; each entry is
one style thesis + its token delta + its contrast verdict. Sources: the project's `variants/` directory (compare: `index.html`;
deltas and method: `MANIFEST.md`; copy freeze: `TEXT_MANIFEST.md` 44/44;
contrast evidence: `qa/contrast.json`).

Every variant keeps body classes, component class API, and copy byte-identical
to the merged build; each is the same HTML fork + one `<style id="variant-tokens">`
delta sheet + a `v-*` class on `<html>`. Shared limitations: newsletter form +
Turnstile omitted by design (comparison pages), worksheet fail-opens to an inert
textarea, nav CTA keeps its frozen internal href.

## 01 — Dawn Atelier (`v01-dawn-atelier.html`)
- **Thesis:** the shipped control. Warm workshop paper (#f4ece4), ledger serif, brass measuring tape. Zero token overrides — the screenshot lane's baseline.
- **Token delta:** none (delta block carries a comment only).
- **Contrast verdict:** PASS. Body 14.85:1 · tape numerals 12.99:1 · CTA 15.88:1. Worst overall 5.32:1 (focus ring, 3.0 threshold). Brand amber #b08d3e appears only here, decorative-only per the AMBER RULE.

## 02 — Midnight Ledger (`v02-midnight-ledger.html`)
- **Thesis:** darkroom inverse. Near-black ink paper (#0e0b09), warm paper-ink text (#f3ead9), moonlit grain blended `screen`, bright-brass (#d4af5f) accents.
- **Token delta:** full dark palette; small-text brass is #e3c47e (10.53:1 on the raised surface); tape fill solid brass, numerals off the fill; grain → screen blend.
- **Contrast verdict:** PASS. Worst required 15.46:1 (tape numerals). Body 16.42:1 · CTA 16.95:1. Worst overall 8.05:1.

## 03 — Newsprint Mono (`v03-newsprint-mono.html`)
- **Thesis:** high-contrast, type-led. Off-white paper (#faf7f1), near-black ink (#141311), NO chromatic accent — the amber family is re-pointed at ink/paper so every rule, underline, and kicker is black/white/gray; display and verdict quote set bolder so type hierarchy carries the design.
- **Token delta:** accent family neutralized (`--ss-amber` → #141311, `--ss-amber-deep` → #1c1a17, `--ss-amber-bright` → #faf7f1); tape fill solid ink; grain 0.35; display/quote weight 700, quote un-italicized.
- **Contrast verdict:** PASS. Worst required 15.35:1 (tape numerals). Body 17.36:1. Worst overall 6.39:1.

## 04 — Verdant Desk (`v04-verdant-desk.html`)
- **Thesis:** deep bottle-green surfaces (#14382c), warm paper text (#f2e9d5), brass accents reserved for decorative + large-display use.
- **Token delta:** full green palette; small brass text uses deep-brass #e0bd76 (5.93:1 on the raised green); tape fill solid brass #c9a24e, numerals off the fill; grain → screen blend.
- **Contrast verdict:** PASS. Worst required 10.66:1 (body text). Tightest pair in the whole set: worksheet label 5.50:1 (self-raised from 4.89:1 during the build — still ≥4.5:1).

## 05 — Cobalt Workshop (`v05-cobalt-workshop.html`)
- **Thesis:** blueprint. Deep cobalt ground (#1a2c66), white line-work, 34px CSS grid-paper motif behind the hero, pale-cyan signal text re-pointed from the amber family.
- **Token delta:** full cobalt palette; `--ss-amber-*` re-pointed at signal cyan (#a8e0ff small text, 8.12:1 on raised cobalt); tape fill solid #8fd8ff, numerals off the fill; focus ring #ffd166 (9.13:1).
- **Contrast verdict:** PASS. Worst required 11.92:1 (body text). CTA 15.89:1. Worst overall 6.16:1.

## Rotation grammar (condensed from `variant-system/VARIANT_GRAMMAR.md`)
- Friday flagship drops rotate A→B→C in order; the pointer lives in `variant-system/rotation-state.json` and is advanced by the pipeline. Milestones are exempt and deliberately chosen; they never consume a rotation slot. Silent overrides are forbidden.
- Daily drops default to A always.
- Brand constants never change: the publication's seal and wordmark, the AMBER RULE, accessibility floors (4.5:1 text, 3:1 UI, ≥48px targets, one polite live region, visible focus ring), the component class API, and vendored-only fonts.
- Forbidden by direction: B never uses the measuring tape; C never uses full-viewport cinematic heroes or the beam; A never inverts to dark. Each direction owns one progress component, one hero register, one atmosphere.
