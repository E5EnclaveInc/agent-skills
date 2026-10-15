#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Verification Gate — THE LEDGER
Merge the JSON ledger outputs from the link / figure / exa gates into one
append-only Verification Ledger: a machine-readable ledger.json AND a styled
HTML report (sovereign institutional register) — the gate, made visible.

USAGE
  python3 verify_ledger.py link_ledger.json figure_ledger.json exa_ledger.json \
      --title "Reparations Archive — Verification Ledger" --out ledger
  -> writes ledger.json and ledger.html
No credentials required.
"""
import sys, json, argparse, html, datetime

OK = {"PASS", "MATCH", "SUPPORTED"}
BAD = {"BROKEN", "MISMATCH", "CONTRADICTED", "ERROR"}
HOLD = {"NEEDS_EYES", "UNVERIFIABLE", "NEEDS_SOURCE_CHECK", "UNCLEAR"}


def cls(s):
    return "ok" if s in OK else ("bad" if s in BAD else "hold")


CSS = """
:root{--bg:#0a1226;--panel:#0e1830;--gold:#c9a84c;--gold-bright:#e6cd86;--ivory:#f3eee2;
--muted:#9aa6bd;--ok:#9fd4ad;--bad:#d98a86;--hold:#e6cd86;--line:rgba(201,168,76,.22)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ivory);font-family:'Inter',-apple-system,system-ui,sans-serif;line-height:1.5;padding:48px 5vw}
h1{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:clamp(2rem,4vw,3rem);letter-spacing:-.01em}
.sub{color:var(--muted);font-size:.9rem;margin-top:8px;font-family:ui-monospace,monospace;letter-spacing:.04em}
.tally{display:flex;gap:1px;background:var(--line);border:1px solid var(--line);margin:30px 0;flex-wrap:wrap}
.t{background:var(--bg);padding:18px 26px;flex:1;min-width:120px}
.t .n{font-family:'Cormorant Garamond',Georgia,serif;font-size:2.2rem;font-weight:600}
.t .l{font-family:ui-monospace,monospace;font-size:.62rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-top:4px}
table{width:100%;border-collapse:collapse;margin-top:18px}
th{font-family:ui-monospace,monospace;font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}
td{padding:12px;border-bottom:1px solid rgba(255,255,255,.06);font-size:.85rem;vertical-align:top}
td a{color:var(--gold-bright);text-decoration:none;word-break:break-all}
.badge{font-family:ui-monospace,monospace;font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;padding:4px 9px;border-radius:999px;white-space:nowrap}
.badge.ok{color:var(--ok);border:1px solid rgba(46,107,62,.5)}
.badge.bad{color:var(--bad);border:1px solid rgba(180,70,66,.5)}
.badge.hold{color:var(--hold);border:1px solid var(--line)}
.det{color:var(--muted);font-size:.8rem}
.foot{margin-top:34px;font-family:ui-monospace,monospace;font-size:.6rem;letter-spacing:.1em;color:var(--muted)}
"""


def render_html(entries, title):
    tally = {}
    for e in entries:
        tally[e.get("status", "?")] = tally.get(e.get("status", "?"), 0) + 1
    nbad = sum(v for k, v in tally.items() if k in BAD)
    rows = []
    for e in entries:
        s = e.get("status", "?")
        claim = e.get("claim") or e.get("target_url") or e.get("id") or ""
        url = e.get("target_url") or ""
        link = '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (html.escape(url), html.escape(url)) if url else ""
        rows.append(
            "<tr><td><span class='badge %s'>%s</span></td><td>%s%s</td><td class='det'>%s</td><td class='det'>%s</td></tr>"
            % (cls(s), html.escape(s), html.escape(str(claim)),
               ("<br>" + link) if (url and url != claim) else "",
               html.escape(str(e.get("detail", ""))), html.escape(str(e.get("source", "")))))
    tcells = "".join("<div class='t'><div class='n %s'>%d</div><div class='l'>%s</div></div>"
                     % (cls(k), v, html.escape(k)) for k, v in sorted(tally.items()))
    verdict = "GATE CLEAN — nothing failed verification" if nbad == 0 else ("%d ITEM(S) FAILED — reject + requeue" % nbad)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>%s</title>"
            "<link href='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap' rel='stylesheet'>"
            "<style>%s</style></head><body>"
            "<h1>%s</h1><div class='sub'>Crucible Verification Ledger · %s · %s</div>"
            "<div class='tally'>%s</div>"
            "<table><thead><tr><th>Status</th><th>Claim / Source</th><th>Detail</th><th>Cited</th></tr></thead><tbody>%s</tbody></table>"
            "<div class='foot'>Verify against the source, never the author's confidence. Nil satis nisi optimum.</div>"
            "</body></html>"
            % (html.escape(title), CSS, html.escape(title), html.escape(verdict), now, tcells, "".join(rows)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="one or more *_ledger.json files")
    ap.add_argument("--title", default="Verification Ledger")
    ap.add_argument("--out", default="ledger", help="output basename (writes .json and .html)")
    a = ap.parse_args()

    entries = []
    for p in a.inputs:
        try:
            data = json.load(open(p))
            entries += data if isinstance(data, list) else [data]
        except Exception as ex:
            print("skip %s: %s" % (p, ex))
    json.dump(entries, open(a.out + ".json", "w"), indent=2)
    open(a.out + ".html", "w").write(render_html(entries, a.title))

    tally = {}
    for e in entries:
        tally[e.get("status", "?")] = tally.get(e.get("status", "?"), 0) + 1
    nbad = sum(v for k, v in tally.items() if k in BAD)
    print("LEDGER: %d entries · %s" % (len(entries), " · ".join("%d %s" % (v, k) for k, v in sorted(tally.items()))))
    print("-> %s.json  %s.html" % (a.out, a.out))
    print("VERDICT: " + ("GATE CLEAN" if nbad == 0 else "%d FAILED — reject + requeue" % nbad))
    sys.exit(2 if nbad else 0)


if __name__ == "__main__":
    main()
