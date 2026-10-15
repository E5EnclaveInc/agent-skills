---
name: improve-codebase-architecture
description: "Find and rank codebase refactoring targets using dependency, change-pain, and blast-radius evidence, then report them visually. Use when deciding which architecture improvements are worth doing."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Improve Codebase Architecture

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Refactor where it pays, not where it itches.

## Method

1. Map the modules: who depends on whom, where the seams are.
2. Score candidates by: change frequency × pain of change × blast radius
   of getting it wrong.
3. For each candidate: what is wrong structurally (not stylistically),
   what the target shape is, and what the first safe step is.

## Output

A ranked report — module, the structural problem, the target shape, the
first step. No drive-by rewrites: each refactor becomes a ticket with
acceptance criteria.
