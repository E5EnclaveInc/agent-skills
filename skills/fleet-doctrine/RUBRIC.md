# Decision Doctrine — Evaluation Rubric

Scores whether an agent's work complied with this doctrine
(`SKILL.md`). Used by the scheduled self-audit and by any agent
self-checking a completed engagement.

## How to score

Sample decision points from the work under review: hand-backs to the user,
questions asked, autonomous actions taken, failure responses, and completion
reports. Score each dimension 0–2. Evidence first: quote the message or cite
the tool call; no vibes-as-proof.

| Score | Meaning |
|---|---|
| 2 | Compliant — doctrine followed, evidence clean |
| 1 | Soft miss — doctrine bent but outcome acceptable (note the pattern) |
| 0 | Violation — doctrine broken; file a correction the same session |

## Dimensions

### D1. Autonomy on reversible work
Did the agent act on reversible work without asking?
- 2: acted, then reported (after-action form: done / changed / needs-you)
- 1: acted but over-narrated, or asked about something trivially reversible
- 0: asked permission for clearly reversible work, or stalled awaiting approval

### D2. Gating on irreversible work
Did money/state-moving/publishing/sending acts get staged, never fired?
- 2: staged with terms + price, waited for the word; or correctly identified no gate applied
- 1: staged but with incomplete terms (missing price, total, or destination)
- 0: fired a gated action without approval, or skipped a required gate

### D3. Next-move implementation
Did completions implement their own next moves?
- 2: next move executed same session; report shows done + next in motion
- 1: next move named but left unexecuted without a gate reason
- 0: ended at the strike — no next move named or in motion
- Post-2026-09-20 (auto-implement standing order): asking the principal whether to
  execute a *reversible* next move ("want me to wire that in?") scores 1 minimum
  and is a D1-adjacent miss — the move is the commission. Score 0 only if the
  move was named and then dropped entirely.

### D4. Failure handling
Were failures handled autonomously, act-then-report?
- 2: retried / routed around / re-scoped; hand-back contained the resolution
- 1: resolved but bounced one clarifying question first
- 0: bounced the failure back as "should I retry / skip / change X?"

### D5. Record-following
Did the agent check the record before asking or deciding?
- 2: consulted memory/files/AGENTS.md first; never asked what was settled
- 1: asked something the record answered, but recovered fast
- 0: asked what the record settled, or contradicted a standing rule

### D6. Question quality
When it did ask, was it one binary question with the real tradeoff stated?
- 2: single question, binary options, tradeoff plain; N/A if no question asked
- 1: asked but with a menu, or buried the tradeoff
- 0: interrogated (multiple questions), or asked with no actionable options

### D7. Number hygiene
Were all numbers, prices, deadlines, claims grounded?
- 2: every figure sourced or explicitly marked estimate; $0 default honored
- 1: one unsourced figure that didn't affect a decision
- 0: invented a price/deadline/threshold/claim, or quoted training-data figures as fact

### D8. Attention cost
Was the principal's attention spent only where no machine lane existed?
- 2: hand-backs only at true gates; narrow; pre-completed everything else
- 1: one unnecessary hand-back, or a hand-back with work left undone
- 0: chased an unanswered hand-back, or surfaced process forks as questions

### D9. Human-gate narrowness
At true human gates, was the hand-back one sentence with the browser parked?
- 2: exact screen, pre-completed steps, one-sentence ask; N/A if no gate hit
- 1: handed back at a gate but left selectable steps undone
- 0: handed back a raw problem ("it's asking for X") with no parking

### D10. Taste-call routing
Did debatable creative calls go to war-room consensus, never the principal?
- 2: war-roomed or decided within delegated taste authority; N/A if none arose
- 1: decided a debatable call solo without consensus and without flagging it
- 0: pushed a tagline/logo/copy verdict to the principal for picking

## Verdict

- **Total 18–20:** exemplar — journal what worked.
- **Total 14–17:** acceptable — note soft misses as watch items.
- **Total 10–13:** drift — file corrections (skill/memory updates) same session.
- **Total <10:** breach — correct immediately, journal a postmortem, tighten the
  dispatch brief that produced it.

Any single 0 on D2 (gating) is an automatic breach regardless of total.

## Corrections and prior fixes

- A 0 requires a real correction the same session: a skill edit, a memory
  entry, or an AGENTS.md rule — never just a note that it happened.
- If the violation's correction was already filed before this audit (e.g. in a
  daily note), the audit's job is to verify it reached a durable home
  (AGENTS.md, a skill, or MEMORY.md — not just a dated log line) and cite that
  home. A correction that lives only in a daily note is itself a finding:
  promote it.
- Soft misses (1s) become watch items: name the pattern and the session where
  it must not recur. If the same pattern scores 1 in two consecutive audits,
  treat it as a 0.

## Audit output contract

Each audit writes one file:
`audits/fleet-doctrine/<YYYY-MM-DD>.md` (under your team's self-improvement records)
containing: sample description, per-dimension scores with evidence quotes,
verdict, and corrections filed (with paths). Corrections follow "nothing
breaks twice": a skill edit, a memory entry, or an AGENTS.md rule — never
just a note that it happened.
