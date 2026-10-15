---
name: agent-spawner
description: "Turn one brief into a standing crew of specialist subagents: ask up to 5 scoping questions, then spawn role-defined specialists each carrying a role, tone, tools, workflow, and success metric. Use when a job needs a coordinated multi-agent crew instead of a one-off delegation. Differs from ad-hoc subagent spawning by the meta-bot scoping ritual and the specialist contract every agent carries."
license: MIT
metadata:
  version: 1.0.0
---
# Agent Spawner

## Purpose
The meta-bot pattern: one scoping pass, then a roster of specialist subagents —
each with a written contract — working in parallel through a shared surface,
so the human is never the router.

## Workflow
1. Scope with at most 5 questions: mission, lanes, tools/surfaces allowed, what
   "done" looks like, and the human gates. Never more than 5 before the first
   spawn; refine after, not before.
2. Draft the roster: 3–7 specialists, one sentence each — job, first task, and
   what success looks like today.
3. Cut friction: remove any specialist whose first task duplicates another's.
   Merge, don't accumulate.
4. Write the specialist contract for each agent:
   - Role (one line) and tone (one line)
   - Tools/surfaces allowed (explicit; nothing assumed)
   - Workflow (numbered steps)
   - Success metric (measurable, checkable on disk or live)
   - Escalation rule (exactly when it pulls the human in)
5. Spawn with one self-contained brief per agent carrying its contract. Truly
   separate lanes spawn in the same turn — parallel, not sequential.
6. Stand up the coordination surface: one shared thread, channel, or directory
   per lane. Specialists report completion and blockers there, never to the
   human directly.
7. Re-verify on completion: check artifacts on disk or live state — never trust
   a completion report in chat (door-verify).

## Output Contract
The 5 scoping answers, a roster table (agent, job, first task, success metric),
the named coordination surface, and each agent's escalation rule.

## Operating Rules
1. Five questions max before the first spawn. A sixth question is procrastination.
2. No agent without a written success metric. A vague agent is a vague outcome.
3. Specialists coordinate through the shared surface; the human is not the router.
4. Human interruption only for money/state moves, irreversible acts, or genuine
   ambiguity — everything else the crew resolves between itself.
5. Verify artifacts, never narration. A report of done is not done.
6. Kill a specialist that creates friction: merge it or delete it the same turn.
