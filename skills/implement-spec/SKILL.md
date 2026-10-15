---
name: implement-spec
description: "Build an entire specification through dependency-ordered tickets, using parallel subagents where tickets are independent. Use when a whole spec is ready and should be implemented as one coordinated effort."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Implement Spec

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

A whole spec, built in parallel where the tickets allow.

## Method

1. to-tickets first: the spec becomes ordered, dependency-mapped tickets.
2. Independent tickets go to parallel subagents; each carries its ticket,
   its acceptance criteria, and nothing else.
3. Each subagent works the implement loop (test-first) on its ticket.
4. Integration order follows the dependency map; the final ticket runs
   the full acceptance list.

## Rules

- Subagents never share mutable state; they meet at ticket boundaries.
- A ticket that reveals a spec gap stops and reports — it does not
  redesign the spec mid-flight.
- The build is done when the acceptance list passes, not when the
  tickets close.
