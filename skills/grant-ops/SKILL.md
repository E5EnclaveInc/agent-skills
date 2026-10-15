---
name: grant-ops
description: "Run grant and funding-opportunity work as a continuously operating department instead of a batch chore: an event queue as the only work list, a dispatcher that drains the frontier and a closer that owns settlement, learning, and honesty accounting, watermarked recon, disqualify-first vetting against an encoded rubric, drafting only from grounded material, staged packages with explicit human gates, and firing under a standing authorization. Use when building or running a grants pipeline for any organization."
license: MIT
metadata:
  version: 1.0.0
---
# Grant Ops — the department pattern

A grants operation run as a **department**, not a batch worker. Work triggers on opportunity availability + eligibility — never on clock slots. There are no quiet hours and no one-stage-per-tick limits: the moment a real opportunity exists and the organization is eligible, the department moves. The pattern below is role-generic: the **principal** is the human who owns the organization and its attestations; everything else is machinery.

## The queue is the only work list

```
                    EVENT QUEUE (the single source of truth)
        states: queued → vetted → drafting → staged → fired
                terminal: disqualified / struck
                              │
        ┌─────────────────────┼─────────────────────┐
   RECON desk           DRAFTING desks           FIRE desk
   (watermarked,        (quality gates           (standing
    when-due)            intact)                  authorization)
                              ▼
              SETTLEMENT + LEARNING (every run, closer-owned)
```

- **No one-stage-per-tick.** Each dispatcher run drains the ready frontier back-to-back: every queued item vetted, every vetted item drafted, every drafted item staged, every cleared staged package fired — bounded only by a run budget. Never stop mid-package.
- **Events, not clocks.** Recon runs when its watermark is stale, not at a fixed hour. A new eligible opportunity is vetted in the same run that finds it.

## The dispatcher / closer split

Truncated runs are inevitable; losing the tail is optional. Split the job in two:

- **Dispatcher** owns the frontier: edge intake, watermarked recon, the vetting/drafting/staging desks, firing.
- **Closer** runs minutes later and owns the tail: settlement ingest, the learning block, the after-action report, and **honesty accounting** over the dispatcher's report (below). If the dispatcher finished early it may run tail steps too — but the closer guarantees them either way.

## Pipeline

1. **RECON** — sweep funder postings, aggregators, newsletters, filings data. Every candidate enters the queue as `queued` with a source reference. Struck sources are never re-added.
2. **VET** — apply the fit rubric (below) without asking the principal. Output per item: `vetted`, `blocked` (named human gate), or struck with a reason.
3. **DRAFT** — assemble the application **only** from a library of grounded narrative blocks (verified organizational material) plus opportunity-specific tailoring. No invented numbers, budgets, dates, counts, or outcomes. Unverifiable fields are marked `[CONFIRM]`, never filled.
4. **STAGE** — the package is a fixed set of files: `requirements` (what is asked, with sources), `draft` (the narrative), `gates` (the exact human inputs still needed), `package` (a one-screen fire checklist: what fires, where, cost, what happens after).
5. **FIRE** — submit only under the standing authorization (below), only when every genuine gate is cleared. Log every submission in the canonical submission log the same run. Never submit twice for the same program + cycle.
6. **SETTLE + LEARN** — outcomes ingested every run; the learning machinery (below) updates calibration, source scores, and rule proposals.

## Disqualify-first vetting

Encode the principal's actual decisions as a rubric, and run the rejects before the scoring — most candidates should die cheap:

- **Ineligible entity** — wrong organization type for the funder (route it to the right entity if one exists; re-homing is not rejection).
- **Wrong geography** — service territory doesn't include yours.
- **Closed cycle, no announced next round** — watchlist at best; spend no effort.
- **Invitation-only with no relationship path** — relationship lane only, never a cold draft.
- **Requires evidence you don't have** — the hard rule. If honest materials can't support the application, it is a skip, not a stretch.
- **Founder-time traps** — commitments (board seats, full-time fellowships, diligence marathons) whose cost exceeds the award's value.
- **One-shot-per-cycle funders** — never rush a weak draft; a weak submission burns the cycle.

Score survivors by **window nearness × award size relative to effort × thematic fit**, in that order. Every vetted prospect gets a one-line verdict with its reason. No prospect sits unvetted longer than one run.

The **struck list is permanent**: an item leaves it only on the principal's explicit word naming it. A principal override can promote a struck item to drafting — never straight to fired — and the caveat travels with the package.

## Founder gates — the honest human list

A gate is a fact or act only the principal can supply. Audit gates periodically: in the reference deployment's first audit, roughly a third of "human" gates turned out to be machine-resolvable and were removed. The gates that are genuinely human:

- **Legal attestations and certifications** — never auto-checked, under any standing approval. The exact text is captured and staged for explicit per-package sign-off.
- Banking details, tax filings.
- Identity-bound sign-ins and account creation.
- Other people's consent.
- Unresolved factual conflicts (two records disagree on a number — the principal's knowledge wins, and the correction is recorded).
- Unsettled strategy, money, scale, or scope commitments.

## Firing under a standing authorization

Define it in writing, with its exclusions, before the first fire: which states may fire, what the approval never covers (legal attestations, spending, external sends without exact-text approval), and what still needs a fresh tap. The authorization speeds up packages whose gates are **cleared** — it never invents or assumes the facts the gates exist to supply. Reversibility is the master variable: reversible = act and report; irreversible-and-consequential = the principal's word first.

## Settlement and learning — the tail that compounds

- **Settlement ledger.** Every fire records fit score, rubric version, funder, program, cycle, ask, date, outcome, evidence. Outcome ingest is idempotent. **Pending outcomes never count toward calibration.**
- **Fit-score calibration.** Per (funder, rubric version): a proper scoring rule (Brier), binned calibration error, bias, n. Shrink predictions toward the base rate until n is meaningful (e.g. full shrinkage at n<10, easing as n grows). Every bucket is labeled **UNCALIBRATED** until it earns the label.
- **Source-yield scoring.** Track yield per recon source. Prune thresholds are **provisional observations, not automatic policy** — a floor is a starting observation to revisit against evidence, never an auto-prune. A pruned source revives only on the principal's explicit word.
- **Rule evolution.** Rubric changes flow: propose → adversarial review (red-team/steel-man) → apply as a **new rubric version** (never edit in place). Evidence bar: a calibration floor (n≥10) or two independent confirming signals. A small set of **guarded rules** the department can never change itself: the fire gate, human-only legal attestations, $0 default, no invented numbers, struck stays struck.
- **Failure ledger.** Every failure recorded with cause and fix. Nothing breaks twice. Open failures surface in every learning block.

## Honesty accounting

The closer verifies the dispatcher's after-action against the system of record:

- Counts in the report must match queue stats exactly; claims about fires must match the submission ledger.
- **Per-run claims are not cumulative totals.** A report saying "fired: none" describes that run. Most false alarms in the reference deployment were exactly this confusion — re-read before quarantining.
- A genuinely false report is quarantined and a failure record filed. A missing report is recorded as a gap — and the closer covers settlement + learning anyway, noting the gap honestly.

## Hard limits (adopt and fill in)

- Never submit outside the standing authorization. Never create a portal account without the principal.
- Never touch banking, tax, or legal certifications — stage them for the principal's word.
- Never send external email or portal messages without exact-text approval.
- Never invent a number. Default cost $0. Struck stays struck.
