---
name: to-tickets
description: "Split a specification into small, independently buildable tickets with explicit dependencies. Use when a settled spec is ready to become an execution plan."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# To Tickets

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

A spec becomes tickets when each ticket is buildable alone.

## Rules

1. One ticket = one requirement (or a coherent slice), buildable and
   testable in isolation.
2. Order by dependency: each ticket lists what it needs from earlier ones.
3. Size: if a ticket needs more than a few focused work sessions, split it.
4. Each ticket states its acceptance criteria — copied from the spec,
   never paraphrased into vagueness.
5. The last ticket is verification: run the full acceptance list.

## Output

Numbered tickets with title, requirement refs, dependencies, acceptance
criteria, and rough size. Ready for implement or implement-spec.
