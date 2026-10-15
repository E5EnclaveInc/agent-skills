# Source Prompts — agent_spawner

Distilled from the GrokBot Galaxy 30-prompt set (Ship by Thursday build,
September 15–17, 2026). Provenance: prompts collected from the three builders'
posts and the "30 GROKBOT PROMPTS" card; full text archived with the original source set.

## A01 — Install a meta-bot (Dr. Eggbot pattern)
> Turn one general assistant into a meta-bot. Ask me 5 questions about the
> company, then create the first 3 specialist bots with memory, skills and
> initial tasks.

## A05 — Chat-first bot customization
> Transform a generic bot into a specialist through chat alone: define its
> role, tone, tools, workflow and success metric.

## A07 — Cracked engineer bot (Tater pattern)
> Create a "cracked engineer" bot that owns the repository, ships directly to
> main, writes minimal tests and never bikesheds.

## B03 — Hire bots as employees
> Start with zero employees and 72 hours. Design a minimal bot organization
> covering research, prospecting, engineering, operations and creative. For each
> bot: one-sentence job, first task, and what success looks like today.

## B07 — Ops + Creative Director bots
> Create two bots: (1) Ops — domains, hosting, repo hygiene; (2) Creative
> Director — brand voice, landing copy, visual direction. Each gets a standing
> routine and an escalation rule for when they need a human.

## A08 — Marketplace discoverability
> Find the best marketplace bots for research, outbound, inbox, engineering and
> design. Define the first task for each and remove any that create friction.

## Adaptation notes
- GrokBot "bots" → subagents, each with a self-contained brief
  (subagents don't inherit context).
- GrokBot "memory" → the skill's standing files and the coordination surface;
  write contracts down, don't rely on chat history.
- GrokBot "skills" → workspace skills attached by reference in the brief.
- The "remove any that create friction" rule maps to Operating Rule 6.
