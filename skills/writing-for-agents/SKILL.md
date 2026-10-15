---
name: writing-for-agents
description: "Write skills and documents that agents can actually follow. Use when drafting or revising agent instructions that need specific imperatives, correct order, and explicit done-states."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Writing for Agents

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Agents follow writing that is specific, ordered, and checkable.

## Rules

1. Imperatives, not observations: "run the tests" beats "tests are important."
2. Order is meaning: put steps in the order they happen.
3. Name the done-state: how does the agent know the step worked?
4. One method per document. A skill that does three things does none.
5. Keep it short: every sentence must earn its place. Cut throat-clearing.
6. Frontmatter carries the facts (name, version, attribution); the body
   carries the method.

## Test

Hand it to an agent cold. Where it hesitates, the writing failed — fix
the writing, not the agent.
