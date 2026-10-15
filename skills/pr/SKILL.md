---
name: pr
description: "Shape a pull request body that lets a reviewer decide quickly. Use when preparing or revising a pull request description with the change, reason, evidence, and risks."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# PR

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

A pull request body that lets a reviewer decide in minutes.

## Shape

1. What changed, in one paragraph — the user-visible or behavior
   difference.
2. Why — the requirement or decision behind it, with refs.
3. How to verify — the exact commands or steps, and what green looks like.
4. Risk and rollback — what could break, and how to undo it.

## Rules

- The diff shows the how; the body explains the why. Never narrate the
  diff line by line.
- Breaking changes and migration steps go at the top, not the bottom.
- Requirement IDs in the body, matching the commits.
