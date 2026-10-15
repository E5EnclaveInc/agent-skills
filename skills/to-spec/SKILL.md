---
name: to-spec
description: "Turn an agreed conversation into a written specification an agent can build from. Use when discussion has settled the goal, scope, exclusions, and acceptance criteria."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# To Spec

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Convert agreement into a spec an agent can build from without asking
questions.

## The spec contains

1. Goal in one paragraph — what changes for the user.
2. Non-goals — what this explicitly does not do.
3. Requirements, numbered (REQ-1…), each testable.
4. Interfaces and data shapes involved.
5. Acceptance criteria — how done is verified.
6. Open questions — anything still undecided, with owners.

## Rules

- No implementation details disguised as requirements.
- Every requirement traceable: reference the conversation or decision
  that produced it.
- If the conversation never settled something, it goes in open
  questions — never invented.
