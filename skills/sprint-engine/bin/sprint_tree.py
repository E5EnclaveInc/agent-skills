#!/usr/bin/env python3
"""
Sprint Engine — tree-recording emitter (Dream-RSI replay substrate).

Appends JSONL branch nodes capturing the dispatcher's exploration decisions
as  alternatives -> choice -> outcome.  This is the future replay substrate
for the harness-refine loop's replay-first adjudication
(design note kept with the adopting team's harness docs).

DESIGN (2026-09-17 Dream-RSI war room, journal/2026-09-17-dream-rsi-war-room.md):
- OBSERVE ONLY. The emitter never alters scheduling, claiming, or execution
  semantics. Every call site wraps emission in try/except: if the emitter
  fails for any reason, the loop proceeds exactly as before.
- APPEND-ONLY. One JSON object per line; the log is never rewritten.
  Removing this file — or setting SPRINT_TREE_OFF=1 — restores the
  pre-instrumentation state completely. Fully reversible.
- STRUCTURE, NOT PROSE. Events record decision structure (which nodes were
  eligible, which was picked, what happened) — never free-text reasoning or
  lesson-style distillations. The paper's negative result (semantic insight
  injection underperforms replay) is why: a replay simulator needs the
  realized decision tree, not summaries of it.

ONTOLOGY (resolved terms — what each field means, nothing invented):
- decision point : one claim_next() call — the dispatcher selects a single
  node from the eligible frontier ("which attempt to continue next").
- alternatives   : EVERY node eligible under the claim predicate at decision
  time (kind='task', status in todo/ready, all depends_on parents done).
  This is the realized search space replay may walk — the choice is always
  one of them, which is what makes replay exact over what happened.
- choice         : the node flipped to 'doing'.
- outcome        : the terminal status + result recorded by complete().
- cut / reopen   : a blocked/proposed transition (cutting a line off) or a
  blocked -> todo/ready transition (reopening it). "When to cut a line off"
  is an exploration decision, so it is recorded too.
- policy         : which exploration policy made the call. claim_next is the
  current default (lowest-id ready). alternatives also carry the
  incumbent basin_score so a future alternative policy can compare its own
  ranking against what the deployed policy assessed.

Node schema (v1) — claim event:
  {"v":1, "ts":<epoch ms>, "db":"graph.db", "run":"<per-process id>",
   "event":"claim", "decision_id":"<uuid>",
   "policy":{"name":"claim_next/lowest-id-ready","basin_scores":true},
   "alternatives":[{"id":12,"kind":"task","title":"...","ctype":"SEARCH",
                    "basin_score":2.31,"basin_rank":1}, ...],
   "choice":{"id":12,"kind":"task","title":"...","ctype":"SEARCH"},
   "note":"..."}
outcome event:
  {"v":1, "ts":..., "db":"graph.db", "run":"...",
   "event":"outcome", "decision_id":"<uuid of the claim>",
   "node":{"id":12,"kind":"task","title":"...","ctype":"SEARCH"},
   "outcome":{"status":"done","result":{...},"latency_ms":45210}}
cut / reopen events:
  {"v":1, "ts":..., "event":"cut", "decision_id":"<uuid>",
   "node":{"id":12,...}, "cut":{"from":"doing","to":"blocked","reason":"dispatcher set_status"}}

Log location: $SPRINT_TREE_LOG, else ~/.sprint-engine/trees/<db>.trees.jsonl
(one log per graph DB, so trees follow the graph they describe).
Kill switch: SPRINT_TREE_OFF=1 disables all emission.
"""
import os
import sys
import json
import time
import uuid

SCHEMA_V = 1

_RUN = uuid.uuid4().hex[:12]


def _default_db_path():
    return os.environ.get("SPRINT_GRAPH_DB") or os.path.join(
        os.path.expanduser("~"), ".sprint-engine", "graph.db")


def log_path(db_path=None):
    """Where this graph's tree log lives. Never raises."""
    try:
        override = os.environ.get("SPRINT_TREE_LOG")
        if override:
            return override
        base = os.path.basename(db_path or _default_db_path()) or "graph.db"
        stem = base[:-3] if base.endswith(".db") else base
        return os.path.join(os.path.expanduser("~"), ".sprint-engine",
                            "trees", stem + ".trees.jsonl")
    except Exception:
        return os.path.join("/tmp", "sprint.trees.jsonl")


def _write(doc, db_path):
    """Append one JSON line. Returns the path, or None on any failure
    (including the kill switch). Never raises."""
    try:
        if os.environ.get("SPRINT_TREE_OFF") == "1":
            return None
        doc = dict(doc)
        doc.setdefault("v", SCHEMA_V)
        doc.setdefault("ts", int(time.time() * 1000))
        doc.setdefault("run", _RUN)
        doc["db"] = os.path.basename(db_path or _default_db_path())
        path = log_path(db_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            f.write(json.dumps(doc, default=str) + "\n")
        return path
    except Exception:
        return None


def _basin_scores(alternatives, edges):
    """Score each alternative with the incumbent basin policy (roma.py).
    Defensive: if roma is unavailable, alternatives ship without scores —
    the claim is still recorded. Never raises."""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import roma
        scored = []
        for a in alternatives:
            node = {"id": a["id"], "kind": a.get("kind"),
                    "title": a.get("title", ""), "ctype": a.get("ctype"),
                    "payload": None, "status": "todo"}
            try:
                s = roma.basin_score(node, edges or [])
            except Exception:
                s = None
            scored.append((s, a))
        # rank deepest-first; None scores sort last
        scored.sort(key=lambda t: (t[0] is None, -(t[0] or 0)))
        out = []
        for rank, (s, a) in enumerate(scored, 1):
            b = dict(a)
            b["basin_score"] = s
            b["basin_rank"] = rank
            out.append(b)
        return out, True
    except Exception:
        return [dict(a) for a in alternatives], False


def _slim(node):
    """Decision-structure view of a graph node: identity only, no payload
    prose (structure, not summaries)."""
    if not node:
        return None
    return {"id": node.get("id"), "kind": node.get("kind"),
            "title": node.get("title"), "ctype": node.get("ctype")}


def emit_claim(db_path, frontier, choice, edges=None):
    """Record a dispatch decision: the eligible frontier and the node picked.
    frontier = list of dicts (id/kind/title/ctype); choice = the claimed node.
    Never raises."""
    try:
        alts, scored = _basin_scores(frontier or [], edges)
        return _write({
            "event": "claim",
            "decision_id": uuid.uuid4().hex,
            "policy": {"name": "claim_next/lowest-id-ready",
                       "basin_scores": scored},
            "alternatives": alts,
            "choice": _slim(choice),
            "note": ("claim_next picked lowest-id ready task; "
                     "%d alternative(s) eligible" % len(alts)),
        }, db_path)
    except Exception:
        return None


def _latest_open_claim(path, node_id):
    """Newest claim for node_id with no later outcome. Never raises."""
    try:
        with open(path) as f:
            lines = f.readlines()
    except Exception:
        return None
    closed = set()
    for line in reversed(lines):
        try:
            d = json.loads(line)
        except Exception:
            continue
        did = d.get("decision_id")
        if d.get("event") == "outcome" and did:
            closed.add(did)
        elif d.get("event") == "claim" and did and did not in closed:
            if (d.get("choice") or {}).get("id") == node_id:
                return d
    return None


def emit_outcome(db_path, node_id, status, result=None):
    """Record the execution outcome for a node, linked to its open claim.
    Never raises."""
    try:
        path = log_path(db_path)
        claim = _latest_open_claim(path, int(node_id))
        latency = None
        if claim:
            try:
                latency = int(time.time() * 1000) - int(claim.get("ts", 0))
            except Exception:
                latency = None
        node = _slim((claim or {}).get("choice")) or {"id": int(node_id)}
        return _write({
            "event": "outcome",
            "decision_id": (claim or {}).get("decision_id"),
            "node": node,
            "outcome": {"status": status, "result": result,
                        "latency_ms": latency},
            "note": ("linked to open claim" if claim
                     else "no open claim observed for this node"),
        }, db_path)
    except Exception:
        return None


def emit_cut(db_path, node_id, old_status, new_status, reason=None):
    """Record a line being cut (blocked/proposed) or reopened. Never raises."""
    try:
        event = "reopen" if (old_status == "blocked"
                             and new_status in ("todo", "ready")) else "cut"
        return _write({
            "event": event,
            "decision_id": uuid.uuid4().hex,
            "node": {"id": int(node_id)},
            event: {"from": old_status, "to": new_status,
                    "reason": reason or "dispatcher set_status"},
        }, db_path)
    except Exception:
        return None
