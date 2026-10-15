---
name: war-room-doctrine
description: "Standing discipline for every war room — ontology-floor term grounding before deliberation, ranked-choice adjudication for decisions. Load at the start of any war-room commission."
license: MIT
metadata:
  version: 1.0.0
---
# War-Room Doctrine

Three standing rules for every war room. No exceptions, no re-asking.

## 0. Scouts do recon (market verification)

A war room without scout recon is untrusted. Alongside deliberation, the
market facts the decision turns on are checked against live sources
(official docs, pricing pages, repos, registries) — by scouts (subagents)
or by the runner directly when running solo. Facts are verified, never
voted on, and never merely assumed.

- The verdict separates **verified facts** from **flagged-unverified** ones.
  Unverified load-bearing facts are named in the record, not buried.
- When a corrected fact dominates the decision, the honest fix is an
  **amendment**, not a re-vote. Record what was wrong, what the recon
  found, and what changes.
- (2026-09-26: the Slack war room ran full doctrine on an unverified
  premise — "Claude tags" misread as the Claude app. Same-night recon
  corrected it to Claude Tag and overturned the winner via amendment.)

## 1. Ground the terms first (ontology floor)

Before any perspective speaks, ground the war room's **load-bearing terms**
(the 3–7 words the decision turns on) with an ontology floor
(`resolve()` in your ontology-floor skill): word →
formula + checkable proof, so the room computes instead of recalling.

- Ground **physical/formal terms** (metrics, mechanisms, quantities, named
  methods). Record each grounding in the war-room file: term, formula,
  proof sketch, source.
- **REFUSE ethical/value terms** — justice, fairness, right, should. Route
  them up to the perspectives as judgment calls, never computed. Record the
  refusal alongside the groundings.
- The war-room report opens with the grounding table. A verdict that rests
  on an ungrounded load-bearing term is flagged, not hidden.

## 2. Adjudicate by ranked choice (RCV)

When the room must **choose** (names, directions, verdicts, ship/no-ship):

1. Each perspective submits a **ranked ballot** over the live options
   (full ranking; ties broken by stated reason, never silently).
2. **Instant runoff:** count first choices; if no option holds a majority,
   eliminate the weakest and redistribute its ballots to next choices.
   Repeat until one option holds a majority.
3. Publish the **rounds table** (votes per option per round) in the report.
4. The winner is the decision. **Minority notes are preserved verbatim** —
   RCV picks the winner; it never erases the dissent.

RCV applies to choices, not to findings of fact. Facts are verified
(Crucible / door-checks), never voted on.

## What changes in existing skills

- **board-of-thirteen:** majority position now means RCV majority; keep the
  minority notes.
- **brand-sprint:** name adjudication runs RCV over the scored shortlist.
- **storm-research:** contradictions are mapped as facts; the synthesis
  recommendation (if one is made) is RCV-adjudicated across personas.
