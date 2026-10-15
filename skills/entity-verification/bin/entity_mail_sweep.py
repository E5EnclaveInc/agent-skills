#!/usr/bin/env python3
"""Mailbox sweep for the entity-verification skill: searches the business
Outlook mailbox (via a mailbox CLI you configure) for corporate-filing and IRS
correspondence about one entity.

Usage:
    entity_mail_sweep.py --name "LEGAL NAME" [--dba "DBA"] [--doc DOCNUM]
                         [--page-size 15] [--deep]

Read-only. The document-number lane trusts the search match (doc numbers are
unique). Name/DBA lanes filter by entity-token matching on headers; --deep
also checks message bodies, and lists filing-adjacent near-misses whose text
never names the entity (e.g. the pay.gov Form 1024-A receipt, confirmed by
date + form type, not by name) so the agent can correlate by date.
"""
import argparse
import json
import os
import re
import subprocess
import sys

BIZMAIL = os.environ.get("BIZMAIL_CLI", "bizmail.py")  # any mailbox CLI with `search` / `get` subcommands

GENERIC_QUERIES = ["1024", "pay.gov", "sunbiz", "Articles of Incorporation",
                   "annual report", "determination letter", "EIN"]

STOPWORDS = {"THE", "INC", "CORP", "COMPANY", "LLC", "CO", "MIAMI",
             "FLORIDA", "OF", "AND"}


def search(query, page_size):
    out = subprocess.run(
        [BIZMAIL, "search", query, "--page-size", str(page_size)],
        capture_output=True, text=True, timeout=90)
    return json.loads(out.stdout or "{}").get("messages", [])


def entity_tokens(name, dba):
    toks = set()
    for s in filter(None, [name, dba]):
        for w in s.replace(",", " ").split():
            w = w.strip().upper()
            if len(w) >= 4 and w not in STOPWORDS:
                toks.add(w)
    return toks


def headers(msg):
    return " ".join([msg.get("subject", ""), msg.get("preview", ""),
                     msg.get("from_name", "")]).upper()


def get_body_text(msg_id):
    try:
        out = subprocess.run([BIZMAIL, "get", msg_id],
                             capture_output=True, text=True, timeout=60)
        data = json.loads(out.stdout or "{}")
        msg = data.get("message", data)
        for key in ("body", "body_text", "body_html"):
            if msg.get(key):
                return re.sub(r"<[^>]+>", " ", str(msg[key])).upper()
    except Exception:  # noqa: BLE001 - treat as empty, keep sweeping
        pass
    return ""


def token_match(hay, tokens, doc):
    if doc and doc.upper() in hay:
        return True
    hits = [t for t in tokens if t in hay]
    return len(hits) >= 2 or any(len(t) >= 8 for t in hits)


def show(msg):
    print(f"  {msg.get('date', '?')[:10]} | {msg.get('from_name') or msg.get('from')} "
          f"| {msg.get('subject')}")
    pv = (msg.get("preview") or "").replace("\r", " ").replace("\n", " ")[:140]
    if pv:
        print(f"      {pv}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="Exact legal name of the entity")
    ap.add_argument("--dba", default="", help="DBA / trade name")
    ap.add_argument("--doc", default="", help="Known document number (lead)")
    ap.add_argument("--page-size", type=int, default=15)
    ap.add_argument("--deep", action="store_true",
                    help="Also check message bodies on generic lanes (slower)")
    args = ap.parse_args()

    tokens = entity_tokens(args.name, args.dba)
    # Doc-number lane runs first: a doc number is the strongest identifier,
    # so a match there gets the most informative label before dedupe consumes
    # it. Only that lane trusts the raw search match.
    lanes = []
    if args.doc:
        lanes.append(("doc number", args.doc, True))
    lanes.append(("legal name", args.name, False))
    if args.dba:
        lanes.append(("dba", args.dba, False))
    lanes += [("generic", q, False) for q in GENERIC_QUERIES]

    seen = set()
    near = []  # filing-adjacent candidates whose text never names the entity
    for label, query, trust_search in lanes:
        try:
            candidates = [m for m in search(query, args.page_size)
                          if m.get("id") not in seen]
        except Exception as e:  # noqa: BLE001 - report lane, keep sweeping
            print(f"[warn] lane {query!r} failed: {e}", file=sys.stderr)
            continue
        hits = []
        fetched = 0
        for m in candidates:
            hay = headers(m)
            if trust_search or token_match(hay, tokens, args.doc):
                hits.append(m)
            elif args.deep:
                if fetched < 6:
                    fetched += 1
                    if token_match(get_body_text(m.get("id", "")), tokens, args.doc):
                        hits.append(m)
                        continue
                if query.split()[0].upper() in hay:
                    near.append((label, query, m))
        for m in hits:
            seen.add(m.get("id"))
        print(f"\n== {label}: {query} ({len(hits)} relevant) ==")
        for m in sorted(hits, key=lambda m: m.get("date", "")):
            show(m)
    if near:
        print("\n== context: filing-adjacent, entity name not confirmed in message ==")
        for label, query, m in near:
            print(f"  [via {label} '{query}'] ", end="")
            show(m)
    print(f"\n{len(seen)} unique relevant messages. Open full bodies with:")
    print(f"  {BIZMAIL} get <message-id>")


if __name__ == "__main__":
    main()
