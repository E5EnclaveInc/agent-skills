---
name: implement
description: "Build a finished ticket into code test-first, following its acceptance criteria through red, green, and refactor. Use when a ticket is ready to implement."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Implement

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Build the ticket. Test-first, no exceptions.

## Loop

1. Read the ticket and its acceptance criteria. Restate the goal in one
   sentence before touching code.
2. Red: write the failing test that proves the missing behavior.
3. Green: write the smallest code that passes.
4. Refactor while green.
5. Run the repo's full check (build, test, typecheck) before calling done.

## Rules

- The ticket's scope is the scope. Discoveries outside it become new
  tickets, not scope creep.
- Never mark done with failing or skipped checks.
- Reference requirement IDs in commit bodies and test names.
