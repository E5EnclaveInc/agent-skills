#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Verification Gate — EXA-GROUNDED FIGURE CHECK
For the claims a machine cannot settle (dollar amounts, dates, attributions, "who said it"),
ask Exa's /answer endpoint for a SOURCED verdict and return it with citations. This is the
disconfirming pass made mechanical: it queries the live web, not the agent's memory.

Requires EXA_API_KEY (https://dashboard.exa.ai/api-keys). Injected as an env var at runtime.

USAGE
  python3 verify_figure_exa.py --query "Is the $51 trillion racial-inequality cost figure
        from the San Francisco Federal Reserve (Buckman, Daly et al., 2021), not the WEF?"
  python3 verify_figure_exa.py --query "..." --expected "SF Federal Reserve, 2021"
  python3 verify_figure_exa.py --claims claims.json   # [{"query":"...","expected":"..."}]
Emits a JSON array of ledger entries to --out (default exa_ledger.json) + a console summary.
Status: SUPPORTED | CONTRADICTED | UNCLEAR | ERROR
"""
import sys, os, json, argparse, urllib.request, urllib.error

API = "https://api.exa.ai/answer"

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "supported": {"type": "boolean",
                      "description": "true if live sources corroborate the claim/expected value"},
        "found_value": {"type": "string",
                        "description": "the exact value/attribution the sources state"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "note": {"type": "string", "description": "one sentence on what the sources say"},
    },
    "required": ["supported", "found_value", "confidence", "note"],
}


def ask(query, expected=None, timeout=90):
    key = os.environ.get("EXA_API_KEY")
    if not key:
        return {"status": "ERROR", "detail": "EXA_API_KEY not set — enter it on the skill credential card"}
    q = query
    if expected:
        q += "\n\nThe claim to verify states: %r. Judge whether live, citable sources support it." % expected
    body = json.dumps({"query": q, "text": True, "outputSchema": OUTPUT_SCHEMA}).encode()
    req = urllib.request.Request(API, data=body, method="POST",
                                 headers={"x-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as ex:
        return {"status": "ERROR", "detail": "Exa HTTP %s: %s" % (ex.code, ex.read()[:200])}
    except Exception as ex:
        return {"status": "ERROR", "detail": "Exa request failed: %s" % ex}

    ans = data.get("answer")
    if isinstance(ans, str):
        try:
            ans = json.loads(ans)
        except Exception:
            ans = {"supported": None, "found_value": ans, "confidence": "low", "note": ans[:300]}
    cites = data.get("citations") or data.get("sources") or []
    srcs = [{"title": c.get("title"), "url": c.get("url")} for c in cites][:6]
    if not isinstance(ans, dict):
        return {"status": "UNCLEAR", "detail": str(ans)[:300], "sources": srcs}
    sup = ans.get("supported")
    status = "SUPPORTED" if sup is True else ("CONTRADICTED" if sup is False else "UNCLEAR")
    detail = "%s | found: %s | conf: %s | %s" % (status, ans.get("found_value", "?"),
                                                 ans.get("confidence", "?"), ans.get("note", ""))
    return {"status": status, "detail": detail, "found_value": ans.get("found_value"),
            "confidence": ans.get("confidence"), "sources": srcs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query")
    ap.add_argument("--expected")
    ap.add_argument("--claims", help="JSON [{query, expected}]")
    ap.add_argument("--out", default="exa_ledger.json")
    a = ap.parse_args()

    todo = []
    if a.claims:
        todo = json.load(open(a.claims))
    elif a.query:
        todo = [{"query": a.query, "expected": a.expected}]
    else:
        print("Pass --query \"...\" or --claims claims.json"); sys.exit(1)

    entries = []
    for c in todo:
        res = ask(c["query"], c.get("expected"))
        e = {"kind": "figure-exa", "claim": c["query"], "expected": c.get("expected")}
        e.update(res)
        entries.append(e)
        print("[%s] %s\n        %s" % (e["status"], c["query"][:90], e.get("detail", "")))
        for s in e.get("sources", []):
            print("          - %s  %s" % (s.get("title", "")[:60], s.get("url", "")))
    with open(a.out, "w") as f:
        json.dump(entries, f, indent=2)
    print("\nEXA FIGURE GATE -> %s" % a.out)


if __name__ == "__main__":
    main()
