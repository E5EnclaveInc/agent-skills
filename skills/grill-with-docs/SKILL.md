---
name: grill-with-docs
description: "Interview a plan against project documentation and record resulting decisions. Use when a proposed plan must be checked against specs, docs, or ADRs before it becomes a specification."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Grill With Docs

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

A plan interviewed against the written record before it becomes a spec.

## Method

1. The agent asks pointed questions about the plan — one at a time.
2. Every answer is checked against the repo's docs, specs, and ADRs.
   When the docs contradict the plan, the docs win until amended.
3. Open decisions are recorded with options, trade-offs, and a
   recommendation — never decided silently.

## Output

A decision log: each decision, the options considered, what was chosen,
and why. This feeds to-spec directly.
