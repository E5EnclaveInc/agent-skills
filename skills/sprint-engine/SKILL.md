---
name: sprint-engine
description: "Use Sprint Engine to run long-horizon autonomous work as a dependency-aware task graph: sqlite graph store, the ROMA loop (Atomizer to Aggregator), and a mandatory red-team/steel-man self-verification gate before execution."
license: MIT
metadata:
  version: 1.0.0
---
# Sprint Engine — ROMA Graph Orchestration

Methodology **and** toolkit for running long-horizon, autonomous work as a dependency-aware task graph: **graph engineering** (a persistent local-sqlite graph), the **ROMA loop** (Atomizer→Planner→Executor→Aggregator; ROMA arXiv 2602.01848, WriteHERE arXiv 2503.08275), and a **mandatory self-verification gate** (red-team + steel-man any plan before executing it).

Adapted from an earlier internal edition: the hosted graph store was replaced with local sqlite, and hosted credential machinery was removed — credentials come from your environment or secret store, never from skill files.

## Core doctrine
- **Verify before you bet.** No plan executes until `roma.red_team_steelman()` returns `approve` (all 8 lenses addressed); a weak plan returns `revise` + specific findings.
- **Split cognition from execution.** High-quality PLANNING in the agent's reasoning; bounded DETERMINISTIC executors. Both read/write the same graph.
- **Gate every side effect.** Nodes carry a cognitive type (THINK / SEARCH / WRITE / ACT). ACT = money/state-moving; the loop NEVER auto-executes ACT — it marks it `proposed` for the confirm-gate.
- **Stay autonomous.** Cut human dependencies; anything irreducibly human is handed off as an exact one-time click, never queued as ongoing work.

## Credential rule — never ask twice
1. Never ask the user to re-enter, re-paste, or re-authorize a secret already on file in any connected skill, native integration, or credential store.
2. Before surfacing any credential card, search available skills and integrations for an equivalent route.
3. Only after programmatic discovery proves the credential is genuinely absent may an agent surface **one** masked credential card identifying the exact missing field. Never request plaintext in conversation.

## Graph substrate — bin/sprint_graph.py (sqlite)
Tables `sprint_nodes(id,kind,title,status,ctype,payload,result,created_at,updated_at)` and `sprint_edges(id,src,dst,rel)`.
- `kind`: goal / task / finding / opportunity / capability / artifact. `status`: todo→ready→doing→done (+ blocked, proposed). `rel`: depends_on / produces / about / blocks.
- DB: `$SPRINT_GRAPH_DB`, else `~/.sprint-engine/graph.db`. No credentials, no network.
- **Ready-queue** = todo nodes whose EVERY `depends_on` parent is `done` (topological frontier).
```
python3 bin/sprint_graph.py init
python3 bin/sprint_graph.py add-node --kind task --title "..." --ctype SEARCH
python3 bin/sprint_graph.py add-edge --src 5 --dst 3
python3 bin/sprint_graph.py ready [--claim]
python3 bin/sprint_graph.py next
python3 bin/sprint_graph.py complete --id 5 --result '{...}'
python3 bin/sprint_graph.py block --id 5 | unblock --id 5
python3 bin/sprint_graph.py dump [--status todo]
```
Importable: `init_schema, add_node, add_edge, ready, claim_next, complete, set_status, dump`.

## Tree-recording — bin/sprint_tree.py (Dream-RSI replay substrate, 2026-09-17)
Append-only JSONL branch nodes capturing dispatcher exploration decisions as
**alternatives → choice → outcome** — the future replay substrate for the
harness-refine loop's replay-first adjudication. `claim_next()` snapshots the
eligible frontier before the atomic claim and emits a `claim` event (every
alternative carries its incumbent `basin_score`/`basin_rank`); `complete()`
emits the linked `outcome` (status + result + latency); `set_status()` emits
`cut`/`reopen` for blocked/proposed transitions. Observe-only: all emission is
post-commit and exception-swallowed — the loop behaves identically with the
emitter broken or removed. Log: `$SPRINT_TREE_LOG`, else
`~/.sprint-engine/trees/<db>.trees.jsonl` (one log per graph). Kill switch:
`SPRINT_TREE_OFF=1`. Reversal: delete `sprint_tree.py`, or just set the kill switch. Records
decision structure only, never free-text reasoning (per the paper's negative
result: replay needs the realized tree, not summaries).

## ROMA + self-verification — bin/roma.py
- `red_team_steelman(title, notes, tasks=None)` → `{verdict, coverage, findings, steelman, lenses_passed}` over 8 lenses: safety_money, cost_runaway, feasibility_limits, value, security, reversibility, human_dependency, observability. CLI: `roma.py verify --file plan.json` (runs offline, no creds).
- `tick(executor, max_ticks)` pulls the ready frontier and runs each node; ACT held `proposed`. `demo()` seeds a graph, gates it, ticks through.

## Basin model — continuous sprints, no menus
Route by steepest value-gradient toward the goal attractor instead of presenting a menu of options. Each cycle: `rank_basin(dump())` scores the READY frontier — value (goal-term pull) + unblock_power (downstream nodes freed) + feasibility (ctype×kind) − dead-end penalty (unwired route / no live target / greenfield) — then DESCEND the deepest basin: execute it, re-score, flow node→node. Refactor mid-sprint when a node reveals new info. Stop only at a REAL gate: a money/ACT node (prepare→propose for one-tap), an external human step, or a flat gradient. CLI: `roma.py basin` ranks the live frontier.

## Guardrails to enforce in your executor
Money/ACT: confirm-gate + per-action and daily caps + kill switch; re-verify freshness at execute; reversible where possible. Cost: bounded ticks, cheap default model, bounded aggregation. Security: secrets only through your secret store or connected integrations, never logged and never requested again when already present. Observability: audit-log every action; alert + auto-pause on auth failure.

## Failure-mining (adapted pattern)
Run a periodic sweep over failed/rejected/skipped actions + blocked/superseded graph nodes. Write ONE dated finding node per sweep; queue fix tasks in the graph — never patch ad hoc mid-sweep. Mined classes to date (generic, from production use): **a 100%-failure action is a schema bug, not market conditions** (detect via per-action success ratio; fix the param map); **failed targets need a cooldown** (re-burned targets waste cycles); **reason-tagged synthetic rejections are healthy** (exclude from failure metrics); **time-gated probes need explicitly past windows** (pre-window 200/empty responses burn probes).

## References
ROMA (arXiv 2602.01848); WriteHERE heterogeneous recursive planning (arXiv 2503.08275).
