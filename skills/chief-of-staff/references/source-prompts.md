# Source Prompts — chief_of_staff

Distilled from the GrokBot Galaxy 30-prompt set (Ship by Thursday build,
September 15–17, 2026). Provenance: prompts collected from the three builders'
posts and the "30 GROKBOT PROMPTS" card; full text archived with the original source set.

## A03 — Steve → Chief of Staff
> Turn a general bot into a Chief of Staff that triages Slack, delegates work
> and only interrupts you for money or product decisions.

## B01 — Slack as control plane
> Set up Slack as our control plane: create channels for #build, #bots,
> #prospecting, #signups. Propose bot mentions and what each channel is for.
> No fluff — ship the structure now.

## C07 — Divide and conquer
> Divide the next 24 hours across three humans and their bots, with one owner
> and a clear definition of "done" for every workstream.

## Adaptation notes
- GrokBot "Slack channels" → your team's side chats, feeds, and goal lanes;
  the CoS pattern works on any intake surface.
- "Only interrupt for money or product decisions" → tiered gating:
  money/state-moving and irreversible acts are human-gated; everything
  reversible runs act-then-report.
- The standing routine maps to scheduled cron sweeps with a human-gate digest;
  the digest discipline (one screen per cycle) is the point, not the schedule.
