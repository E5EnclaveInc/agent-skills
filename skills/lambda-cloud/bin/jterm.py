#!/usr/bin/env python3
"""Run a bash command on a Lambda instance via its JupyterLab terminal.

Usage: jterm.py <instance-id> "<command>" [--timeout SEC]

Opens a Jupyter terminal, runs the command, waits for a completion marker,
prints combined stdout/stderr, exits with the remote command's exit code.

Never prints the API key or Jupyter token.
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jcommon import jupyter  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
MARK = "__JTERM_DONE__"


def rest(base: str, token: str, method: str, path: str, body=None):
    """REST call via curl — urllib hits intermittent RemoteDisconnected on
    this host (2026-09-15), while curl stays solid."""
    import random
    import subprocess
    url = f"{base}{path}?token={token}"
    last = None
    for i in range(6):
        cmd = ["curl", "-s", "--max-time", "30", "-A", UA, "-X", method, url,
               "-H", "Content-Type: application/json"]
        if body is not None:
            cmd += ["-d", json.dumps(body)]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if p.returncode == 0 and (p.stdout.strip() or method == "DELETE"):
            raw = p.stdout.strip()
            return json.loads(raw) if raw else {}
        last = f"rc={p.returncode} stderr={p.stderr[:80]}"
        time.sleep(min(20, 2 ** i) + random.uniform(0, 1))
    raise RuntimeError(f"terminal REST {method} {path} failed: {last}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--timeout")]
    timeout = 300
    for a in sys.argv[1:]:
        if a.startswith("--timeout"):
            timeout = int(a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a) + 1])
    if len(args) < 2:
        sys.exit('usage: jterm.py <instance-id> "<command>" [--timeout SEC]')
    iid, cmd = args[0], args[1]

    import websocket  # websocket-client

    base, token = jupyter(iid)
    term = rest(base, token, "POST", "/api/terminals", {"cwd": ""})
    name = term["name"]
    ws_url = base.replace("https://", "wss://").replace("http://", "ws://")
    try:
        ws = websocket.create_connection(
            f"{ws_url}/terminals/websocket/{name}?token={token}",
            header=[f"User-Agent: {UA}"], timeout=30)
        ws.send(json.dumps(["stdin", cmd.rstrip("\n") + f"\necho {MARK}:$?\n"]))
        out, exit_code, deadline = [], None, time.time() + timeout
        # NOTE: match the marker result WITHOUT a ^ anchor. The pty emits
        # bracketed-paste escapes (\x1b[?2004l) and \r at line starts, so the
        # result line rarely begins cleanly with the marker. The echoed INPUT
        # line is `echo __JTERM_DONE__:$?` (literal $? — not digits), so
        # requiring (\d+) after the colon safely excludes it.
        marker_re = re.compile(rf"{MARK}:(\d+)")
        while time.time() < deadline:
            try:
                msg = json.loads(ws.recv())
            except Exception:
                break
            if not isinstance(msg, list) or len(msg) < 2:
                continue
            kind, data = msg[0], msg[1]
            if kind in ("stdout", "stderr"):
                out.append(data)
                clean = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07|\r", "", "".join(out))
                matches = marker_re.findall(clean)
                if matches:
                    exit_code = int(matches[-1])
                    break
        ws.close()
        text = "".join(out)
        # strip ANSI escape sequences and our marker line from visible output
        text = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07", "", text)
        text = "\n".join(l for l in text.splitlines() if MARK not in l)
        print(text)
        sys.exit(exit_code if exit_code is not None else 124)
    finally:
        try:
            rest(base, token, "DELETE", f"/api/terminals/{name}")
        except Exception:
            pass


if __name__ == "__main__":
    main()
