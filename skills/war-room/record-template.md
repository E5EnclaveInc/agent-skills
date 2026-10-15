# Record template — a session that leaves no record did not happen

Every convening produces one record file: `records/<date>-<slug>.md`.

## Required sections

1. **Header:** date, commissioned by, charge (question/scope/non-goals/deliverables), protocol source, standing (deliberative vs. empowered).
2. **Election of offices** — the rundown table (office / holder / mandate in own voice), procedure used (acclamation with spoken assents, or RCV rounds table).
3. **Evidence and method** — what was examined, in what form, provenance; transcription method and its independent check.
4. **Ontology settlement** — load-bearing terms, grounded / refused / F-flagged.
5. **Findings** — every claim tagged **[VERIFIED]** (checked by computation or primary source) or **[OPINION]** (committee judgment). The two are never mixed. A [VERIFIED] tag must name the specific check performed or the primary source examined — "per <document>" without a named check is **[ATTESTED]**, never [VERIFIED]. (Ratified 2026-10-01, production war room: citation wearing verification's clothes.)
6. **Rulings** — each with the vote count and named dissenters.
7. **Minority notes — verbatim and present.** Stated in the dissenter's own terms, never paraphrased away, never referenced-absent. A "see Minority Notes" pointer with no such section is a defective record.
8. **Decision log** — what was decided, by whom, on what evidence. Every decision-log row carries a **verdict-state-history** column (active | amended | retired-by-amendment, naming the amending instrument) — a record must never show a retired ruling as live. (Precedent: the 2026-09-26 Whiteboard war room, where a typed "R5 — 5–0" rendered after §17's retirement would read as an active verdict.)
9. **Staged amendment packet (if any)** — consequential changes specified exactly and staged for the Chairman's one-tap, never executed by the committee. Each item: exact spec, preconditions, and its place in the packet's execution order. **Sequencing law:** never specify a store migration before reading the store — the packet carries its own order, and items specified before the audit returns are marked amendable-by-audit. (Precedent: 2026-09-26 domain-governance A1–A7.) **Subject-verification rule:** each item's preconditions must name the store they act on, and the audit must confirm the packet's subject IS that store before any write executes — an audit that finds the subject absent suspends the item back to STAGED (re-pointed), it does not fail the session. (Precedent: 2026-09-26 execution — A2–A6 suspended when the 628-entry cache was absent from the remote store; the absence was ruled on, with receipts.)
10. **The offices rundown** (repeated at close if offices changed mid-session).

## Close-out checklist (the minutes-taker verifies before adjournment)

- [ ] Every charge item has a section or an explicit deferral with owner and date.
- [ ] No dangling cross-references (every "see §X" resolves).
- [ ] Every [VERIFIED] claim names its check; every [OPINION] is labeled.
- [ ] Minority notes are present verbatim, not merely referenced.
- [ ] The convener's own counts were independently checked.
- [ ] F-flagged items name who closes them and how.

*Precedent for this checklist: the 2026-09-26 formalism record closed with integrity findings only — taxonomy, fitness, gaps, and recommendations sections from its charge were never written, and its "see Minority Notes" pointers dangle. The checklist exists so the next committee cannot close that way.*
