---
name: setup
description: "Record a repository's conventions once so other engineering skills can operate with context. Use when onboarding a repository to these skills or when its build, test, layout, or conventions change."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Setup

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Before the other skills can work well, they need to know how this repo works.
Run once per repo; re-run when conventions change.

## Record

1. How to build, test, and typecheck (exact commands).
2. Where things live (source, tests, docs, specs) and what each directory is for.
3. The non-negotiables: invariants, red lines, merge policy, who decides what.
4. Live state: what is proven vs claimed right now, and where that is written.

## Output

A short conventions note the invoking agent keeps for the session. Do not
write it into the repo unless asked — conventions live in the repo's own
docs; this is the working copy.
