# Ratchet — every session compounds

**EMIT → EXTRACT → ENDORSE → INDEX → CONSTRAIN.** A session's learnings are emitted in its record, extracted here, endorsed by the Chairman's standing doctrine (or their explicit word), indexed into the cards and protocol files, and constrain future sessions.

## The loop

1. **EMIT** — the record carries a "ratchet candidates" pass: what did this session teach about elections, record format, card design, or protocol?
2. **EXTRACT** — the convener distills candidates into discrete, testable lessons.
3. **ENDORSE** — a lesson enters the canon only if it coheres with standing doctrine or the Chairman explicitly endorses it. Rejected lessons are logged with the reason, not silently dropped.
4. **INDEX** — endorsed lessons land in the right file: card design → `personas/<name>.md`; elections → `election.md`; record → `record-template.md`; protocol → `SKILL.md`/`bylaws.md`. Cards are **versioned** (`version: 1`, changelog at the card's foot).
5. **CONSTRAIN** — the next session's charge cites the constraints it inherits. Nothing breaks twice.

## First exercise — the 2026-09-26 formalism committee close (extracted)

1. **Acclamation with recorded spoken assent** is a valid election procedure when unanimous; RCV is mandatory when contested. → `election.md`
2. **Charge-fitted offices with in-voice mandates** outperform generic titles; the rundown table is a required record element. → `election.md`, `record-template.md`
3. **Mandatory [VERIFIED]/[OPINION] separation** — the single highest-value record discipline observed. → `record-template.md`
4. **Evidence provenance rules** — state the form of evidence; screenshot-as-source is unfit for audit; transcriptions get an independent check. → `scout-recon.md`, `record-template.md`
5. **Close-out completeness checklist** — the formalism record closed without its taxonomy/fitness/gaps/recommendations sections and with dangling minority-note pointers; the checklist now gates adjournment. → `record-template.md`
6. **The convener is checkable too** — Wolfram corrected the convener's collision count (3→2). Verification rides the convener. → `ontology-settlement.md`, `scout-recon.md`
7. **Rulings carry vote counts and named dissenters; minority notes must be present verbatim**, not referenced-absent. → `record-template.md`
8. **Card-design lesson:** the session showed what cards must support — in-voice mandates, dissent in character, quantitative correction of the convener, and the discipline to mark opinion as opinion. The v1 cards' scenario evals encode these behaviors. → `personas/`

## Amendment-execution session — the 2026-09-26 A1–A7 execution (fifth live exercise)

Record: `records/2026-09-26-amendment-execution.md`. The Chairman tapped the staged packet; the committee executed under the sequencing law. (The fourth live exercise, the Jev-improvement war room, ratcheted crowley.md/wolfram.md to v3 with the badge-vs-file license rule and the release-notes check.)

1. **The sequencing law's first live precedent** — the audit didn't just amend the packet, it vacated five of seven items' preconditions: the 628-entry cache was in none of the three remote stores. A2–A6 suspended as unmet-precondition, re-pointed at the cache when located. The audit earned zero writes. → `record-template.md` (new subject-verification rule in the staged-packet section)
2. **Negative results are deliverables** — the A1 audit's headline was an absence (0/4 collision keys, 0 GOD keys, cache not in store), ruled on with receipts rather than treated as inconclusive. → `scout-recon.md`
3. **Credential-path provenance** — dead scoped token → Global-key surrogate per the skill's Auth section; the record names the path used. → `scout-recon.md`
4. **Mid-session doctrine arrival** — the standing Recon Subcommittee was chartered during A1; the session already matched the new order of business in substance (recon before deliberation), so the record noted the arrival point and the substantive compliance, and seated the subcommittee formally for the re-execution. → noted here; future sessions follow the new Art. IV order natively.
5. **Card-header hygiene** — the Jev session entered v3 in crowley/wolfram changelogs without bumping the version headers; corrected to v4 with the correction noted. Ratchet edits bump the header and the changelog together.
6. **Card deltas → v3/v4** — Thoth v3 (naming-as-law applied to execution scope); da Vinci v3 (wrong-store surgery refused; three bodies); Einstein v3 (the razor applied to the packet itself); Crowley v4 (census-as-baseline; LOCATE THE CACHE); Wolfram v4 (threshold-granularity catch; full-census COMPUTED receipts).

## Pending

The formalism committee's unanswered charge items (taxonomy, fitness-for-arcade, gaps, recommendations) are open work — labeled, not absorbed. A follow-up session may take them up; the protocol does not pretend they were done.

## Second exercise — the 2026-09-26 domain-governance session (extracted)

Records: `records/2026-09-26-formalism-domain-governance.md` (Phase 1) + `records/2026-09-26-prometheus-os-review.md` (Phase 2). The committee took jurisdiction over the formalism lineage and applied R1–R9 against the live system.

1. **Committee operational definitions** — institutional terms return ungrounded from the floor; that is expected. Define them on the record, marked committee-defined. → `ontology-settlement.md`
2. **Read the subject's own Open ledger** as standard scout reading; cite scout files as evidence provenance. → `scout-recon.md`
3. **Diff vendored copies against live sources as standard** — "no conflict" must still pass the Razor. → `scout-recon.md`
4. **Sequencing law** — never specify a store migration before reading the store; amendment packets carry their own execution order. → `record-template.md` (new staged-packet section)
5. **The Auditor may amend taxonomies mid-deliberation** (kind-as-set precedent). → `bylaws.md` Art. V
6. **Card deltas → v2** — all five cards bumped with session lessons (Thoth: operative register on custody rulings; da Vinci: three-system separation; Einstein: sequencing amendment + live R2 catch + sustained GOD-tier dissent; Crowley: kind-as-set + consultable annex; Wolfram: COMPUTED/ATTESTED tiering + 0.82-calibration flag).

## Sixth live exercise — the 2026-09-26 sprint-operations war room (extracted)

Record: `records/2026-09-26-sprint-operations-war-room.md`. The Chairman's commission: run the war-room protocol, reach consensus on a sprint operating doctrine, and execute the first sprint hardening. (The fifth live exercise, the amendment-execution session, ratcheted above; the Jev-improvement war room, the fourth, is noted there.)

1. **Brief premises are claims** — the convener's brief carried two stale premises ("all cards v3"; "two failed watchers"); the verification function caught both before deliberation. A brief is checked like any other claim. → `scout-recon.md` (the Recon Subcommittee checks the brief first)
2. **Fail-closed as a first-class done-state value** — a run that stops before committing damage is a verdict, not an error; done-state schemas enumerate it alongside success and name the failed gate. → `record-template.md` (done-state section)
3. **The live-tissue rule** — healthy lanes are not experiment sites; repair targets are the failed, the stale, the recoverable. The intention-lab tick was verified healthy and deliberately left uncut. → `scout-recon.md` (target selection)
4. **Scheduler-body primacy** — `cron.view` outranks `cron.d/` mirrors; a mirror's absence is cosmetic, the scheduler's body is the law. → `scout-recon.md` (evidence provenance)
5. **Stop-condition independence** — a bounded run whose stop depends on the frontier draining will not stop when work regenerates; the stop must be independent of the work-frontier. → `ontology-settlement.md` (constraint on the committee-defined `sprint`)
6. **Card deltas → v5/v6** — Thoth v5 (brief-as-claim); da Vinci v5 (live-tissue rule); Einstein v5 (stop-condition independence; the label-does-no-work dissent); Crowley v6 (fail-closed as first-class done-state; scheduler-body primacy); Wolfram v6 (done-state schemas specified exactly and machine-checkable).
