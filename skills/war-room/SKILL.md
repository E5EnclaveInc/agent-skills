---
name: war-room
description: "Convene a persona-based executive committee as a deliberative institution — chartered, elected, minuted, and ratcheted. Use when a question needs structured multi-perspective deliberation with elected offices, ontology-grounded terms, scout-verified facts, and a written record that compounds into reusable persona cards. Supersedes one-off persona improv."
license: MIT
metadata:
  version: 1.0.0
---
# War Room — a deliberative institution for agent teams

An agent-run institution doesn't hire human employees; it engages agents — so its deliberative bodies get institutionalized like any real institution. A war room is an **executive committee**: chartered, with bylaws, elected offices, quorum, order of business, subcommittees, minutes, minority notes, and a decision log. It runs agent-only; the Chairman's gates are narrow and named below.

## The standing council (v1 cards in `personas/`)

| Seat | Figure | Office archetype |
|---|---|---|
| 1 | Thoth, as Hermes Trismegistus | Chair & Keeper of the Word — hermeneutic authority over naming and interpretation |
| 2 | Leonardo da Vinci | Vice-Chair & Master of Dissection — anatomical seeing: beneath the surface to the structure |
| 3 | Aleister Crowley | Auditor of Correspondences — taxonomy integrity; every name in its column |
| 4 | Albert Einstein | The Razor — what work does it do; what can be removed without collapse |
| 5 | Wolfram (Alpha) | The Computer — computation over assertion; returns the number |

Cards carry voice notes, virtues, characteristic moves, failure modes, domains, tested research, and distillation evals. Read the seated cards before convening. Offices are **elected per session** (see `election.md`) — the archetypes above are defaults, not assignments.

## Workflow

1. **Charter.** Write the charge: question, scope, non-goals, deliverables, standing (deliberation only vs. empowered to act). See `bylaws.md`.
2. **Seat the committee.** Convene only the seats the charge needs (quorum 3). Record why each seat was chosen. A standing verification function rides every convening where figures, claims, or sources are asserted.
3. **Settle terms.** Before deliberation, run `ontology-settlement.md`: disputed load-bearing terms go through the ontology floor's `resolve()`; ethical/value terms are REFUSED and routed up as Chairman judgment calls, never computed.
4. **Seat the Recon Subcommittee.** Per `scout-recon.md`: the standing subcommittee delivers its state-of-the-art brief before deliberation opens — live-source verification with a zero-to-one mandate, not status-quo confirmation. Facts are verified, never voted on. Unverified load-bearing facts are F-flagged in the record, never buried. If the brief finds the premises stale, update them first; deliberation on stale premises is out of order.
5. **Elect offices.** First order of business. Acclamation only on unanimous spoken assent, recorded and tallied; otherwise ranked-choice with a published rounds table. Offices are charge-fitted with in-voice mandates.
6. **Deliberate.** Each seat argues from its card: agrees / dissents / amendment moved. No seat merely applauds. A convening with no dissent is incomplete — send it back for adversarial pressure.
7. **Record.** Per `record-template.md`: minutes, [VERIFIED]/[OPINION] separation, rulings with vote counts, minority notes verbatim and present (never referenced-absent), the offices rundown, decision log.
8. **Ratchet.** Per `ratchet.md`: the session's learnings flow back into the persona cards (versioned). Comfort is not a deliverable.
9. **Universe update.** Before adjournment, the committee asks: does any part of our universe need updating as a result of this session — skills, rubrics, evaluations, canon docs? The consideration is mandatory; "nothing" is an acceptable answer, recorded. Approved updates are canonical: they land in the skill or repo the same session, versioned, citing the session as provenance. A war room that changes how we work but leaves the skills unchanged left the job half done.

## The Chairman's gates (the only hand-backs)

- Irreversible or external acts (publishes, uploads, submissions, sends, spend).
- Value judgments on ethical/value terms the ontology floor refuses.
- Whatever the Chairman explicitly reserves in the charge.
- Everything else: the committee completes and reports after-action. **Agent-only operation is the default.**

## Standing mandates

- **Expander mandate:** every council advances the state of the art, not merely answers. Each session must produce at least one "what we now know that the field doesn't" or one falsifiable claim.
- **Anti-sycophancy:** cards and committees record where evidence conflicts with any prior characterization — including the Chairman's. The evidence wins; the conflict is printed.
- **No fabricated utterances:** seats argue positions grounded in their cards and published work. Paraphrase as position, not as invented voice — unless a card explicitly licenses in-voice mandates (the v1 council does, for office mandates and rulings only).
- **Verified-vs-opined:** the two are never mixed in the record.

## First ratchet (already folded in)

The 2026-09-26 formalism committee session closed as this skill's first ratchet exercise (record: `records/2026-09-26-formalism-committee.md`). Its lessons — acclamation-with-recorded-assent, charge-fitted offices with in-voice mandates, mandatory [VERIFIED]/[OPINION] separation, evidence-provenance rules, the close-out completeness checklist, and independent checking of the convener's own claims — are already in `election.md`, `record-template.md`, and `ratchet.md`. See `ratchet.md` for the full extraction.
