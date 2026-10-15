---
name: diagnosing-bugs
description: "Diagnose a hard bug from a reliably failing reproduction, isolate its mechanism, and lock it down with a regression test. Use when behavior is broken, throwing, failing, or unexpectedly slow."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Diagnosing Bugs

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

No repro, no diagnosis. The failing repro is the ground truth.

## Method

1. Write the smallest repro that fails reliably. If it is flaky, fix the
   flakiness first — a flaky repro diagnoses nothing.
2. Narrow: bisect the code path until the failure moves with one change.
3. State the mechanism: what exactly goes wrong, in what order.
4. Fix the mechanism, not the symptom. The repro becomes the regression
   test.

## Rules

- Never "fix" by making the repro pass without understanding the
  mechanism.
- If the mechanism implicates a dependency or platform, verify against
  its source before blaming it.
