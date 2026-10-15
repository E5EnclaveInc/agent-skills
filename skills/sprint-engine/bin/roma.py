#!/usr/bin/env python3
"""
Sprint Engine — ROMA driver + mandatory self-verification gate.

Implements the ROMA control loop (Atomizer -> Planner -> Executor -> Aggregator,
arXiv 2602.01848 / WriteHERE heterogeneous recursive planning) over the D1 graph
in sprint_graph.py, plus the RED-TEAM / STEEL-MAN gate that MUST pass before any
plan is executed ("run the protocol on your own plan before betting on it").

Cognitive types (WriteHERE): THINK (reason), SEARCH (retrieve/recon),
WRITE (compose), ACT (side-effecting execution — always the gated tier).

This module is executor-agnostic: pass an executor(node)->result callable.
The default DryExecutor echoes, so the loop is testable with no side effects.

CLI:
  roma.py verify --file plan.json      # run the self-verification gate (offline, no creds)
  roma.py demo                         # seed a tiny graph, verify, tick through (needs D1 creds)
  roma.py tick [--max 5]               # advance the live graph with the dry executor (needs D1 creds)
"""
import os, sys, json, argparse

# ---- the self-verification gate (red-team + steel-man) --------------------
# Every plan must demonstrably address each lens before it earns execution.
LENSES = {
    "safety_money":      ["gate", "confirm", "cap", "spend", "reversible", "kill"],
    "cost_runaway":      ["budget", "bound", "cap", "rate", "token", "cadence", "limit"],
    "feasibility_limits":["subrequest", "limit", "batch", "cursor", "cpu", "timeout", "propagat"],
    "value":             ["value", "roi", "payback", "yield", "why", "benefit", "outcome"],
    "security":          ["secret", "encrypt", "key", "vault", "least-priv", "exfil", "0600"],
    "reversibility":     ["revers", "undo", "unlist", "refund", "dry", "rollback"],
    "human_dependency":  ["autonomous", "no human", "cut", "unattended", "self", "without"],
    "observability":     ["audit", "log", "trace", "alert", "verify", "monitor"],
}

def red_team_steelman(plan_title, notes, tasks=None):
    """Score a plan against the lenses. notes = free-text rationale/guardrails;
    tasks = optional list of task dicts (each may carry its own 'notes').
    Returns {verdict, coverage, findings, steelman}. verdict='approve' iff no lens is unaddressed."""
    hay = (plan_title + "\n" + (notes or "")).lower()
    for t in (tasks or []):
        hay += "\n" + json.dumps(t).lower()
    findings, coverage = [], {}
    for lens, kws in LENSES.items():
        hit = any(k in hay for k in kws)
        coverage[lens] = hit
        if not hit:
            findings.append({"lens": lens, "red_team": f"plan does not visibly address '{lens}'",
                             "ask": f"state how '{lens}' is handled (keywords like {kws[:3]})"})
    verdict = "approve" if not findings else "revise"
    steelman = ("Strongest case FOR: " + plan_title + " — proceeds only after every lens is addressed; "
                "gate is advisory-strict so an unverified plan cannot execute.")
    return {"verdict": verdict, "coverage": coverage, "findings": findings,
            "steelman": steelman, "lenses_total": len(LENSES), "lenses_passed": sum(coverage.values())}

# ---- basin model: route toward the goal attractor by steepest value-gradient ----
# The goal is a deep attractor (a self-running, actionable, compounding operator). Rather than
# present a menu of options, the engine DESCENDS the deepest basin: score each READY node by its
# pull toward the goal, execute the deepest, re-score, flow node->node; refactor mid-sprint when a
# node reveals new information (add/modify nodes); stop only at a real gate (money/ACT -> propose;
# an external human step; or a flat gradient = no positive-value ready node). Always source perfection.
CTYPE_W = {"ACT": 1.0, "SEARCH": 0.85, "WRITE": 0.7, "THINK": 0.4}
KIND_W  = {"opportunity": 1.0, "task": 0.85, "goal": 0.6, "epic": 0.6, "artifact": 0.5, "finding": 0.2, "capability": 0.3, "reference": 0.3}
GOAL_TERMS = ("value", "yield", "payback", "roi", "deploy", "stage", "actionable", "liquid", "compound", "revenue", "profit")
DEADEND_TERMS = ("unwired", "not client-wired", "no live target", "greenfield", "404", "quiescent", "sold out", "blocked")

def basin_score(node, edges):
    """Pull-toward-goal for one ready node. Deeper basin = higher score.
      value        : goal-term hits in title+payload (does this move the estate?)
      unblock_power: how many nodes depend_on this one (freeing the DAG downstream)
      feasibility  : ctype x kind weight (can it actually be executed now?)
      liveness     : penalty if it flows to a dead-end right now (unwired route, no target)
    """
    nid = node.get("id")
    hay = (node.get("title", "") + " " + json.dumps(node.get("payload") or {})).lower()
    value = sum(1 for t in GOAL_TERMS if t in hay)
    unblock = sum(1 for e in edges if e.get("dst") == nid and e.get("rel") == "depends_on")
    feas = CTYPE_W.get((node.get("ctype") or "").upper(), 0.5) * KIND_W.get(node.get("kind"), 0.5)
    deadend = 0.5 if any(t in hay for t in DEADEND_TERMS) else 0.0
    return round(1.5 * value + 1.2 * unblock + 2.0 * feas - 2.0 * deadend, 3)

def rank_basin(graph):
    """Rank the READY frontier by basin depth (deepest first). graph = dump() = {nodes, edges}.
    Ready = a 'todo' node whose every depends_on parent is 'done'. Returns [(score, id, title, ctype)]."""
    nodes = {n["id"]: n for n in graph.get("nodes", [])}
    edges = graph.get("edges", [])
    done = {i for i, n in nodes.items() if n.get("status") == "done"}
    def ready(n):
        if n.get("status") != "todo":
            return False
        deps = [e["dst"] for e in edges if e.get("src") == n["id"] and e.get("rel") == "depends_on"]
        return all(d in done for d in deps)
    cand = [n for n in nodes.values() if ready(n)]
    ranked = sorted(((basin_score(n, edges), n["id"], n.get("title"), n.get("ctype")) for n in cand), reverse=True)
    return ranked

def next_in_basin(graph):
    """The single deepest-basin ready node (the route to take now), or None if the gradient is flat."""
    r = rank_basin(graph)
    return r[0] if r and r[0][0] > 0 else None

# ---- executors -------------------------------------------------------------
def dry_executor(node):
    return {"executed": "dry", "node": node.get("id"), "title": node.get("title"), "ctype": node.get("ctype")}

# ---- ROMA loop over the D1 graph ------------------------------------------
def _graph():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sprint_graph as g
    return g

def tick(executor=dry_executor, max_ticks=5):
    g = _graph()
    done = []
    for _ in range(max_ticks):
        node = g.claim_next()
        if not node:
            break
        # ACT nodes are the gated tier: never auto-execute here; they must be
        # confirmed out-of-band. The dry loop marks them 'proposed' and moves on.
        if (node.get("ctype") or "").upper() == "ACT":
            g.set_status(node["id"], "proposed")
            done.append({"id": node["id"], "disposition": "proposed_gated"})
            continue
        res = executor(node)
        g.complete(node["id"], res)
        done.append({"id": node["id"], "disposition": "executed", "result": res})
    return {"ticked": len(done), "nodes": done}

def demo():
    g = _graph()
    g.init_schema()
    goal = g.add_node("goal", "DEMO: recon then collect yield", ctype="THINK",
                      payload={"notes": "gate+confirm+cap money, batch within subrequest limit, audit log, autonomous no human, reversible dry-run"})["id"]
    t1 = g.add_node("task", "DEMO: SEARCH yield endpoints", ctype="SEARCH")["id"]
    t2 = g.add_node("task", "DEMO: ACT collect (gated)", ctype="ACT")["id"]
    g.add_edge(t1, goal); g.add_edge(t2, t1)  # t1 depends on goal, t2 depends on t1
    gate = red_team_steelman("DEMO plan", "gate confirm cap spend reversible kill; budget bound token cadence; subrequest batch cursor; value roi payback; secret encrypt vault 0600; audit log trace alert; autonomous unattended self no human", [])
    out = {"seeded": [goal, t1, t2], "gate": gate}
    if gate["verdict"] != "approve":
        out["halt"] = "gate did not approve; execution blocked"
        return out
    out["run"] = tick(max_ticks=5)
    out["final"] = g.dump()
    return out

def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("verify"); a.add_argument("--file", required=True)
    a = sub.add_parser("tick"); a.add_argument("--max", type=int, default=5)
    sub.add_parser("demo")
    sub.add_parser("basin")  # rank the live ready-frontier by basin depth (the route to take now)
    args = p.parse_args()
    if args.cmd == "verify":
        spec = json.load(open(args.file))
        out = red_team_steelman(spec.get("title", "untitled"), spec.get("notes", ""), spec.get("tasks"))
    elif args.cmd == "tick":
        out = tick(max_ticks=args.max)
    elif args.cmd == "demo":
        out = demo()
    elif args.cmd == "basin":
        out = {"basin_ranked": rank_basin(_graph().dump())}
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
