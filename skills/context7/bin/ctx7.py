#!/usr/bin/env python3
"""context7 skill CLI — version-pinned library docs via the Context7 MCP server.

Keyless (no account, no API key). Server: npx @upstash/context7-mcp@4.1.1 (pinned).
Allowlisted tools only; argv is hardcoded; env is scrubbed (see _mcp_stdio).

Usage:
  ctx7.py resolve <library-name>
  ctx7.py docs <context7-library-id> [--topic TOPIC] [--tokens N]
  ctx7.py tools        # list server tools (smoke test)
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _mcp_stdio import call_tool, list_tools  # noqa: E402

NPX = os.environ.get("CTX7_NPX") or __import__("shutil").which("npx") or "npx"
SERVER_ARGS = ["-y", "@upstash/context7-mcp@4.1.1"]
ALLOWLIST = {"resolve-library-id", "query-docs"}


def _guard(tool):
    if tool not in ALLOWLIST:
        raise SystemExit(f"tool {tool!r} not allowlisted")


def _proxy_passthrough():
    """Sandbox egress needs its proxy vars; the CA vars come from scrubbed_env."""
    out = {}
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
                "ALL_PROXY", "all_proxy", "NO_PROXY", "no_proxy"):
        if var in os.environ:
            out[var] = os.environ[var]
    return out


def cmd_resolve(args):
    _guard("resolve-library-id")
    res = call_tool(NPX, SERVER_ARGS, "resolve-library-id",
                    {"query": args.query, "libraryName": args.library_name or args.query},
                    timeout=180, extra_env=_proxy_passthrough())
    print(json.dumps(res, indent=2, ensure_ascii=False))


def cmd_docs(args):
    _guard("query-docs")
    params = {"libraryId": args.library_id, "query": args.query}
    res = call_tool(NPX, SERVER_ARGS, "query-docs", params, timeout=300,
                    extra_env=_proxy_passthrough())
    print(json.dumps(res, indent=2, ensure_ascii=False))


def cmd_tools(_args):
    print(json.dumps(list_tools(NPX, SERVER_ARGS, timeout=180,
                               extra_env=_proxy_passthrough()), indent=2))


def main():
    p = argparse.ArgumentParser(description="Context7 version-pinned docs lookup")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("resolve", help="resolve a library name to a Context7 ID")
    r.add_argument("query", help="What to look up (sent to Context7; no secrets/PII)")
    r.add_argument("--library-name", dest="library_name", default="", help="Official library name (defaults to query)")
    r.set_defaults(fn=cmd_resolve)

    d = sub.add_parser("docs", help="fetch docs for a Context7 library ID")
    d.add_argument("library_id", help="Context7 library ID, e.g. /vercel/next.js")
    d.add_argument("query", help="Single concept to look up (sent to Context7; no secrets/PII)")
    d.set_defaults(fn=cmd_docs)

    t = sub.add_parser("tools", help="list server tools (smoke test)")
    t.set_defaults(fn=cmd_tools)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
