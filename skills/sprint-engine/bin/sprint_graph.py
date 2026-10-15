#!/usr/bin/env python3
"""
Sprint Engine — sqlite-backed graph store (graph engineering substrate).

A dependency-aware task/knowledge graph persisted in local sqlite. Nodes are
goals/tasks/findings/opportunities/capabilities/artifacts; edges carry typed
relations (depends_on / produces / about / blocks). The ready-queue returns the
topological frontier: todo nodes whose every depends_on parent is done. This is
the durable world-model + work-queue an autonomous ROMA loop traverses.

Adapted from an earlier internal edition; the hosted D1 REST layer was replaced
with local sqlite. No credentials required.

DB location: $SPRINT_GRAPH_DB, else ~/.sprint-engine/graph.db.

CLI:
  sprint_graph.py init
  sprint_graph.py add-node --kind task --title "Recon yield endpoints" [--ctype SEARCH] [--status todo] [--payload '{...}']
  sprint_graph.py add-edge --src 5 --dst 3 [--rel depends_on]
  sprint_graph.py ready [--claim]
  sprint_graph.py next
  sprint_graph.py complete --id 5 [--result '{...}']
  sprint_graph.py block --id 5   |   unblock --id 5
  sprint_graph.py dump [--status todo]
All commands print JSON. Importable: init_schema, add_node, add_edge, ready, claim_next, complete, dump.
"""
import os, sys, json, time, argparse, sqlite3

DB_PATH = os.environ.get("SPRINT_GRAPH_DB") or os.path.join(
    os.path.expanduser("~"), ".sprint-engine", "graph.db")

_conn = None

def _db():
    global _conn
    if _conn is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _conn = sqlite3.connect(DB_PATH, timeout=30)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA busy_timeout=15000")
    return _conn

def q(sql, params=None):
    cur = _db().execute(sql, params or [])
    if sql.lstrip().upper().startswith("SELECT"):
        return [dict(r) for r in cur.fetchall()]
    _db().commit()
    return []

def init_schema():
    q("""CREATE TABLE IF NOT EXISTS sprint_nodes (
      id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, title TEXT,
      status TEXT DEFAULT 'todo', ctype TEXT, payload TEXT, provenance TEXT, result TEXT,
      created_at INTEGER, updated_at INTEGER)""")
    q("""CREATE TABLE IF NOT EXISTS sprint_edges (
      id INTEGER PRIMARY KEY AUTOINCREMENT, src INTEGER, dst INTEGER, rel TEXT DEFAULT 'depends_on')""")
    q("CREATE INDEX IF NOT EXISTS idx_sn_status ON sprint_nodes(status)")
    q("CREATE INDEX IF NOT EXISTS idx_se_src ON sprint_edges(src)")
    # migrate pre-provenance DBs (pragma_table_info is a table-valued function)
    cols = [r["name"] for r in q("SELECT name FROM pragma_table_info('sprint_nodes')")]
    if "provenance" not in cols:
        q("ALTER TABLE sprint_nodes ADD COLUMN provenance TEXT")
    return {"ok": True, "schema": "sprint_nodes, sprint_edges", "db": DB_PATH}

def add_node(kind, title, ctype=None, status="todo", payload=None, provenance=None):
    now = int(time.time() * 1000)
    cur = _db().execute(
        "INSERT INTO sprint_nodes (kind,title,status,ctype,payload,provenance,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        [kind, title, status, ctype, json.dumps(payload) if payload is not None else None,
         provenance, now, now])
    _db().commit()
    return {"ok": True, "id": cur.lastrowid, "kind": kind, "title": title, "status": status}

def add_edge(src, dst, rel="depends_on"):
    q("INSERT INTO sprint_edges (src,dst,rel) VALUES (?,?,?)", [int(src), int(dst), rel])
    return {"ok": True, "edge": [int(src), rel, int(dst)]}

def ready(claim=False):
    # todo nodes whose every depends_on parent is done
    rows = q("""SELECT n.id, n.kind, n.title, n.ctype FROM sprint_nodes n
      WHERE n.status='todo' AND NOT EXISTS (
        SELECT 1 FROM sprint_edges e JOIN sprint_nodes p ON p.id=e.dst
        WHERE e.src=n.id AND e.rel='depends_on' AND p.status!='done')
      ORDER BY n.id""")
    if claim and rows:
        ids = ",".join(str(r["id"]) for r in rows)
        q(f"UPDATE sprint_nodes SET status='ready', updated_at={int(time.time()*1000)} WHERE id IN ({ids})")
    return rows

def claim_next():
    """ATOMIC claim. A single BEGIN IMMEDIATE transaction picks the lowest-id
    ready WORK node (kind='task', todo/ready whose every depends_on parent is
    done) and flips it to 'doing' with a status guard. Goals, references,
    findings and observations are not work: the drain never claims them.
    Two concurrent drains cannot claim the same node: the second blocks on
    the reserved lock, then sees the node already 'doing' and moves to the
    next. Double-drain is structurally impossible."""
    # --- tree-recording (Dream-RSI substrate): snapshot the eligible frontier
    # BEFORE the atomic claim. Read-only SELECTs; the claim predicate below is
    # unchanged. Any failure here disables emission for this call only.
    db = _db()
    _tree_frontier, _tree_edges = None, None
    try:
        _rows = db.execute(
            """SELECT n.id, n.kind, n.title, n.ctype FROM sprint_nodes n
               WHERE n.kind='task' AND n.status IN ('todo','ready') AND NOT EXISTS (
                 SELECT 1 FROM sprint_edges e JOIN sprint_nodes p ON p.id=e.dst
                 WHERE e.src=n.id AND e.rel='depends_on' AND p.status!='done')
               ORDER BY n.id""").fetchall()
        _tree_frontier = [dict(r) for r in _rows]
        _tree_edges = [dict(r) for r in db.execute(
            "SELECT src,rel,dst FROM sprint_edges").fetchall()]
    except Exception:
        _tree_frontier, _tree_edges = None, None
    now = int(time.time() * 1000)
    db.execute("BEGIN IMMEDIATE")
    try:
        row = db.execute(
            """SELECT n.id FROM sprint_nodes n
               WHERE n.kind='task' AND n.status IN ('todo','ready') AND NOT EXISTS (
                 SELECT 1 FROM sprint_edges e JOIN sprint_nodes p ON p.id=e.dst
                 WHERE e.src=n.id AND e.rel='depends_on' AND p.status!='done')
               ORDER BY n.id LIMIT 1""").fetchone()
        if not row:
            db.execute("ROLLBACK")
            return None
        nid = row[0]
        cur = db.execute(
            "UPDATE sprint_nodes SET status='doing', updated_at=? WHERE id=? AND status IN ('todo','ready')",
            [now, nid])
        if cur.rowcount != 1:
            db.execute("ROLLBACK")
            return None
        db.execute("COMMIT")
    except Exception:
        try:
            db.execute("ROLLBACK")
        except Exception:
            pass
        raise
    got = q("SELECT id,kind,title,ctype,payload,provenance,status FROM sprint_nodes WHERE id=?", [nid])
    node = got[0] if got else None
    # --- tree-recording: emit the decision AFTER commit. Observe-only:
    # failures are swallowed, the claim result is unaffected.
    if node is not None and _tree_frontier is not None:
        try:
            import sprint_tree
            sprint_tree.emit_claim(DB_PATH, _tree_frontier, node,
                                   edges=_tree_edges)
        except Exception:
            pass
    return node

def complete(nid, result=None):
    q("UPDATE sprint_nodes SET status='done', result=?, updated_at=? WHERE id=?",
      [json.dumps(result) if result is not None else None, int(time.time()*1000), int(nid)])
    # --- tree-recording: outcome edge for the open claim. Observe-only.
    try:
        import sprint_tree
        sprint_tree.emit_outcome(DB_PATH, int(nid), "done", result)
    except Exception:
        pass
    return {"ok": True, "id": int(nid), "status": "done"}

def set_status(nid, status):
    _old = None
    try:
        _r = q("SELECT status FROM sprint_nodes WHERE id=?", [int(nid)])
        _old = _r[0]["status"] if _r else None
    except Exception:
        _old = None
    q("UPDATE sprint_nodes SET status=?, updated_at=? WHERE id=?", [status, int(time.time()*1000), int(nid)])
    # --- tree-recording: cuts (blocked/proposed) and reopens are exploration
    # decisions too. Observe-only.
    try:
        import sprint_tree
        if status in ("blocked", "proposed") or (
                _old == "blocked" and status in ("todo", "ready")):
            sprint_tree.emit_cut(DB_PATH, int(nid), _old, status)
    except Exception:
        pass
    return {"ok": True, "id": int(nid), "status": status}

def dump(status=None):
    cols = "id,kind,title,status,ctype,provenance"
    if status:
        nodes = q(f"SELECT {cols} FROM sprint_nodes WHERE status=? ORDER BY id", [status])
    else:
        nodes = q(f"SELECT {cols} FROM sprint_nodes ORDER BY id")
    edges = q("SELECT src,rel,dst FROM sprint_edges ORDER BY id")
    return {"nodes": nodes, "edges": edges}

def close_out(nid, receipt):
    """ONE close-out write path: graph-complete AND dated journal append in a
    single step, so completion records can never diverge."""
    out = complete(nid, {"receipt": receipt})
    day = time.strftime("%Y-%m-%d")
    line = f"\n## {time.strftime('%H:%M %Z')} — graph close-out: node {nid} done — {receipt}\n"
    logpath = os.path.join(os.path.expanduser("~"), "memory", f"{day}.md")
    with open(logpath, "a") as f:
        f.write(line)
    out["journal"] = logpath
    return out

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    a = sub.add_parser("add-node"); a.add_argument("--kind", required=True); a.add_argument("--title", required=True); a.add_argument("--ctype"); a.add_argument("--status", default="todo"); a.add_argument("--payload"); a.add_argument("--provenance")
    a = sub.add_parser("add-edge"); a.add_argument("--src", required=True); a.add_argument("--dst", required=True); a.add_argument("--rel", default="depends_on")
    a = sub.add_parser("ready"); a.add_argument("--claim", action="store_true")
    sub.add_parser("next")
    sub.add_parser("claim")
    a = sub.add_parser("complete"); a.add_argument("--id", required=True); a.add_argument("--result")
    a = sub.add_parser("close"); a.add_argument("--id", required=True); a.add_argument("--receipt", required=True)
    a = sub.add_parser("block"); a.add_argument("--id", required=True)
    a = sub.add_parser("unblock"); a.add_argument("--id", required=True)
    a = sub.add_parser("dump"); a.add_argument("--status")
    args = p.parse_args()
    if args.cmd == "init": out = init_schema()
    elif args.cmd == "add-node": out = add_node(args.kind, args.title, args.ctype, args.status, json.loads(args.payload) if args.payload else None, args.provenance)
    elif args.cmd == "add-edge": out = add_edge(args.src, args.dst, args.rel)
    elif args.cmd == "ready": out = ready(args.claim)
    elif args.cmd == "next": out = claim_next()
    elif args.cmd == "claim":
        node = claim_next()
        out = {"node": node} if node else {"node": None}
    elif args.cmd == "complete": out = complete(args.id, json.loads(args.result) if args.result else None)
    elif args.cmd == "close": out = close_out(args.id, args.receipt)
    elif args.cmd == "block": out = set_status(args.id, "blocked")
    elif args.cmd == "unblock": out = set_status(args.id, "todo")
    elif args.cmd == "dump": out = dump(args.status)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
