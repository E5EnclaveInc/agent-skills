#!/usr/bin/env python3
"""web-fetch skill CLI — fetch a public URL as markdown via mcp-server-fetch.

SSRF enforcement is CONNECTION-LAYER, not wrapper-level: the server runs with
HTTP_PROXY/HTTPS_PROXY pointed at the validating egress proxy
(bin/egress_proxy.py), which resolves every target host itself at connect time
and blocks all private/loopback/link-local/reserved ranges. The quick check
below is defense-in-depth only.

Usage:
  fetch.py get <url> [--max-length N] [--start-index N] [--raw]
  fetch.py tools      # list server tools (smoke test)
"""
import argparse
import ipaddress
import json
import os
import subprocess
import sys
from urllib.parse import urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _mcp_stdio import call_tool, list_tools  # noqa: E402
from egress_proxy import ip_allowed  # noqa: E402 — same policy as the proxy
import proxy_ctl  # noqa: E402

VENV_PY = os.path.join(os.environ.get("MCP_VENV", os.path.expanduser("~/.venvs/mcp")), "bin", "python")
# NOTE: this server does NOT honor HTTP_PROXY env — the proxy must be passed
# explicitly via --proxy-url (verified in the installed server source).
SERVER_ARGS = ["-m", "mcp_server_fetch", "--proxy-url", "http://127.0.0.1:8899"]
ALLOWLIST = {"fetch"}
PROXY_URL = "http://127.0.0.1:8899"


def _quick_block(host):
    """Defense-in-depth literal check using the SAME policy as the proxy.
    The proxy remains the real enforcement point."""
    try:
        return not ip_allowed(ipaddress.ip_address(host.strip("[]")))
    except ValueError:
        return False  # DNS names are validated by the proxy at connect time


def _ensure_proxy():
    if not proxy_ctl._healthy():
        print("starting egress proxy…", file=sys.stderr)
        subprocess.run([VENV_PY, os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "proxy_ctl.py"), "start"], check=True)


def cmd_get(args):
    parts = urlsplit(args.url)
    if parts.scheme not in ("http", "https"):
        sys.exit(f"refused: only http/https URLs (got {parts.scheme!r})")
    if not parts.hostname or _quick_block(parts.hostname):
        sys.exit(f"refused: blocked target {parts.hostname!r}")
    _ensure_proxy()
    params = {"url": args.url, "max_length": args.max_length,
              "start_index": args.start_index, "raw": args.raw}
    extra = {"HTTP_PROXY": PROXY_URL, "HTTPS_PROXY": PROXY_URL,
             "ALL_PROXY": PROXY_URL, "NO_PROXY": ""}
    res = call_tool(VENV_PY, SERVER_ARGS, "fetch", params,
                    timeout=180, extra_env=extra)
    print(json.dumps(res, indent=2, ensure_ascii=False))


def cmd_tools(_args):
    _ensure_proxy()
    extra = {"HTTP_PROXY": PROXY_URL, "HTTPS_PROXY": PROXY_URL, "NO_PROXY": ""}
    print(json.dumps(list_tools(VENV_PY, SERVER_ARGS, timeout=120,
                               extra_env=extra), indent=2))


def main():
    p = argparse.ArgumentParser(description="Fetch a public URL as markdown")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("get", help="fetch a URL")
    g.add_argument("url")
    g.add_argument("--max-length", type=int, default=5000)
    g.add_argument("--start-index", type=int, default=0)
    g.add_argument("--raw", action="store_true")
    g.set_defaults(fn=cmd_get)
    t = sub.add_parser("tools", help="list server tools (smoke test)")
    t.set_defaults(fn=cmd_tools)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
