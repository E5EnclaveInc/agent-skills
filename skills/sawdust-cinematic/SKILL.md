---
name: sawdust-cinematic
description: "Take a publication's frozen text and build a cinematic, gate-passing HTML page in the Atelier Ledger register or a named design variant, styling by token-delta only and never rewording the copy. Use when a new issue or drop page needs styling from finalized text, when a variant is commissioned, or when copy-freeze, computed-contrast, and visual-evidence gates must all pass before the page is staged for approval."
license: MIT
metadata:
  version: 1.0.0
---

# Sawdust Cinematic

## Purpose
Turn frozen playbook copy into a cinematic, evidence-gated HTML page built only from the canonical Atelier Ledger design system plus a token-delta layer — nothing forked, nothing eyeballed, nothing deployed without approval.

## Trigger conditions
Load this skill when: a new playbook issue needs styling from its frozen text; a variant commission lands (Friday rotation, milestone); or a Friday/daily drop needs the cinematic page treatment. Always load `design-second-brain` alongside it — its 14-point gate is step 7 below.

## Workflow
1. **Ingest frozen copy.** Read the issue's frozen source text. It is already finalized — do not reword, reorder, or "improve" a single block.
2. **Select direction.** Consult `variant-system/rotation-state.json` (see references) for the rotation rule: Friday drops rotate A→B→C; dailies default to A; milestones are exempt and deliberately chosen. Then pick from the shipped catalog in `references/VARIANT_CATALOG.md`.
3. **Build the page from the canonical system via token-delta only.** Copy the shipped merged build, apply `<style id="variant-tokens">` token overrides plus a `v-*` class on `<html>`. Never fork `system/` CSS, never rename component classes, never add fonts or scripts, never touch copy.
4. **Computed contrast gate.** Run the WCAG computation (method + paste-ready snippet in `references/CONTRAST_METHOD.md`): body text ≥4.5:1 (target 7:1), tape numerals ≥4.5:1 on their track, CTA ≥4.5:1. Any failure is a fix, not a judgment call.
5. **Visual evidence.** Render virtual-iPhone 390px WebKit + desktop screenshots with a console-error count of 0. Record what was actually rendered — no invented evidence.
6. **Firsthand visual review loop.** Look at the screenshots. Fix what your eye catches (tape numeral placement, dead voids, clipping) and re-run steps 4–5 until clean.
7. **design-second-brain 14-point gate.** Invoke that skill's gate script (`workflow/bin/run_design_gate.py` in design-second-brain) — do not duplicate its checks. Its PASS plus this skill's cinematic gates (copy-freeze, computed contrast, zero console errors) is the complete verdict.
8. **Stage the approval packet and STOP.** Output contract below. No deploy, no newsletter send — publishing is the approver's explicit word only.

## Output Contract
- **Page artifact:** single HTML file + vendored `fonts/` (woff2 + OFL.txt), all assets same-origin. No CDN references anywhere.
- **Gate report** (`gate-report.json`): design-gate verdict, copy-freeze result (blocks counted), contrast results (worst required pair + body/display/CTA), screenshot inventory with console-error count, and the frozen-copy source path.
- **Evidence directory** (`qa/`): screenshots, `contrast.json` (per-pair fg/bg/ratio/threshold/pass), copy-freeze log output.
- **Attestation manifest:** artifact hash list ready for the deploy lane's admission gate. The skill stops here — deployment funnels through `deploy_site.py` and `deploy_gate.py` only on the approver's explicit word.

## Operating Rules
1. Copy freeze: included text is byte-identical to the frozen source, verified by `bin/verify_copy.py`. A single word change fails the gate.
2. Delta layers only: variant styling is a token-delta sheet; `system/` CSS is never forked and component classes are never renamed.
3. Contrast is computed, never eyeballed — WCAG relative-luminance math, stdlib Python.
4. AMBER RULE: brand amber `#b08d3e` is decorative/UI-only; amber text only via the approved deep/bright variants at ≥4.5:1 (see `system/tokens.css`).
5. Fonts vendored same-origin (woff2). No Google Fonts CDN, no external requests.
6. Honor `prefers-reduced-motion` and `prefers-reduced-transparency`; direction-level motion overrides live inside `@media (prefers-reduced-motion: no-preference)`.
7. Fail-open: the page reads whole with no JS — reveals visible, motes absent, tape at final state.
8. $0 new spend. Nothing publishes or sends without the Chairman's explicit word.