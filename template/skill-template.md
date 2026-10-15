---
name: my-skill
description: "What this skill does, in one phrase — plus when to use it: the trigger situations or phrases an agent should match, and how it differs from sibling skills. Never summarize the steps here."
license: MIT
metadata:
  version: 1.0.0
---

# My Skill

One short paragraph: what this skill is and the outcome it produces.

## When to use

- The situations that should trigger this skill.
- The situations that should NOT (point at the sibling skill instead).

## Procedure

1. State-check first: verify the setup this skill assumes, then branch.
2. Do the work. Push anything deterministic, fragile, or repetitive into a
   script under `bin/` and call it from here — prose is for judgment.
3. Verify before you finish: state the check, run it, fix, re-verify.

## Failure modes

- For every step that can fail: what failure looks like and what to do.

## Files

- `bin/` — scripts (optional; Pattern A capability skills).
- `references/` — detail the body points at but does not inline (optional).

<!-- Authoring rules: description = what + when + differentiator, ≤1024 chars;
     body < 500 lines; secrets only via env vars or your platform's credential
     schema, never literals; relative paths only. See CONTRIBUTING.md. -->
