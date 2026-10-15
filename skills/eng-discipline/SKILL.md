---
name: eng-discipline
description: "Install the minimum rigorous engineering discipline for a sprint build: the tests that guard the contract, PR hygiene, issue-to-ship loops, and a five-line shipping policy. Use when starting a short build where process must be light but real. Differs from sprint-engine (the task-graph runner) by being the discipline layer inside a build, and from full SDLC process by the explicit strip-to-minimum for a sprint."
license: MIT
metadata:
  version: 1.0.0
---
# Engineering Discipline

## Purpose
A short build needs rigor without ceremony: enough process that nothing ships
broken, little enough that the build still ships. Install the pack, strip the
rest — explicitly.

## Workflow
1. Define "done" for the build in one paragraph before any code is written.
2. Install the skill pack:
   - The tests that guard the contract (not exhaustive coverage — the tests
     that would catch a real regression of the done-definition).
   - PR/change hygiene: small diffs, one concern per change, every change
     traces to an issue or task.
   - Issue-to-ship loop: issue → change → verify → merge, no orphan commits.
3. Write the five-line shipping policy on an index card. Example shape:
   small diffs only; staging first, production on approval; every change
   verified live; broken main reverted fast, not debated; decisions logged in
   one line.
4. Strip for the sprint: name what's cut (heavy test matrices, formal reviews,
   ceremony) and what's kept — in writing, so the cut is a decision, not drift.
5. Set ship-to-main rules: who can merge, what verification precedes the merge,
   and exactly how a bad merge is reverted.
6. Close the loop: after the sprint, one retro line per rule — kept, fixed,
   or dropped.

## Output Contract
The done-definition, the installed pack (kept list + cut list), the five-line
shipping policy, and the ship-to-main rules.

## Operating Rules
1. Tests guard the contract, not the codebase. A test that can't fail on a real
   regression is deleted.
2. One concern per change. A change that can't be described in one line is split.
3. Verification is live state, not green logs (door-verify: prove the deploy,
   the hash, the artifact — never trust a green log).
4. Revert beats debate. A broken main is reverted first and discussed after.
5. The policy fits on an index card or it isn't the policy.
6. Nothing breaks twice: every failure becomes a rule, a test, or a doc entry.
