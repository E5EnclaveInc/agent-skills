---
name: codebase-design
description: "Design deep modules with shared vocabulary for contracts, invariants, and seams. Use when designing or restructuring a code interface, boundary, or module."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Codebase Design

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Deep modules are designed with words before code.

## Vocabulary

- **Boundary:** what crosses in and out, and in what shape (contracts).
- **Invariant:** what is always true inside, and who enforces it.
- **Seam:** where the module can be split later without redesign.
- **Owner:** who decides changes to the boundary.

## Method

1. Name the module's single responsibility in one sentence.
2. Draw the boundary: inputs, outputs, and their contracts.
3. State the invariants and where they are enforced.
4. Name the seams — the future splits you are preserving.

A module you cannot describe this way is not designed yet.
