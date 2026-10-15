---
name: domain-modeling
description: "Build and sharpen a project domain model and glossary. Use when terminology is ambiguous, one word carries multiple meanings, or load-bearing terms need to be documented."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Domain Modeling

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Confused words make confused software. Sharpen the words first.

## Method

1. List the load-bearing terms — the words decisions turn on.
2. For each: what it means here, what it excludes, and an example.
3. Find the collisions: two meanings wearing one word. Split them —
   one word, one meaning.
4. Write the glossary down where the project keeps its records.

## Rule

A term that cannot be defined with one meaning is not a term — it is a
disagreement waiting to ship. Settle it before it becomes code.
