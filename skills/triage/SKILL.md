---
name: triage
description: "Sort raw issues into classified, owned work with a concrete next step. Use when incoming issues need reproduction, clarification, severity, classification, or assignment."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Triage

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Raw issues become work when each one has a next step and an owner.

## Method

1. Reproduce-or-clarify: can the issue be restated as a failing behavior
   or a concrete question? If not, ask for the missing piece.
2. Classify: bug, feature, question, chore. Bugs need severity.
3. Deduplicate against existing issues before creating anything.
4. Each surviving issue gets: a one-line summary, the next step, and a
   suggested owner or lane.

## Output

The sorted list. Issues that cannot be stated concretely go back for
clarification — they do not become tickets.
