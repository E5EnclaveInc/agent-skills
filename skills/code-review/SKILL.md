---
name: code-review
description: "Review a diff against its specification and repository standards, naming the evidence for acceptance. Use when checking a branch, pull request, or work in progress before acceptance."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Code Review

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Review the diff, not the author. Two bars: the spec, and the standards.

## Against the spec

- Does every changed line trace to a requirement? Untraced changes are
  questioned, not assumed.
- Do the acceptance criteria pass? Name the evidence (test names, runs).

## Against the standards

- Contracts on boundaries: are inputs validated where they cross?
- Errors: are failures named, or swallowed?
- No dead code, no commented-out code, no TODOs without tickets.

## Output

Findings ordered by severity: blocking (spec or safety), should-fix,
nit. Each finding cites the file and line. Praise is specific or omitted.
