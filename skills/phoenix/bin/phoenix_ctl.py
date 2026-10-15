#!/usr/bin/env python3
"""phoenix_ctl.py — manage the Arize Phoenix observability pilot server.

Phoenix runs ONLY on 127.0.0.1:6006 (no auth in the self-hosted UI — never
expose it), and ONLY during pilot runs. OTLP receiver: 127.0.0.1:4317.
"""
import argparse
import os
import signal
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
VENV = os.environ.get("PHOENIX_VENV", os.path.expanduser("~/.venvs/phoenix"))
PHOENIX = os.path.join(VENV, "bin", "phoenix")
PIDFILE = os.path.join(HERE, "run", "phoenix.pid")
LOGFILE = os.path.join(HERE, "phoenix.log")
HOST, PORT = "127.0.0.1", 6006


def _pid():
    try:
        with open(PIDFILE) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def _healthy():
    try:
        with urllib.request.urlopen(f"http://{HOST}:{PORT}/", timeout=5) as r:
            return r.status == 200
    except OSError:
        return False


def cmd_start(_a):
    if _pid() and _healthy():
        print(f"phoenix already running (pid {_pid()})")
        return
    if not os.path.exists(PHOENIX):
        sys.exit(f"phoenix binary missing: {PHOENIX} (pip install arize-phoenix)")
    os.makedirs(os.path.dirname(PIDFILE), exist_ok=True)
    logf = open(LOGFILE, "a")
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin",
           "HOME": "/root", "LANG": "C.UTF-8",
           # Short retention for the pilot: trace data can contain task content.
           "PHOENIX_SQL_DATABASE_URL": "sqlite:///" + os.path.join(HERE, "run", "phoenix.db"),
           # No external internet for the pilot: the Mintlify docs MCP server
           # (external docs lookup) breaks startup behind the egress proxy.
           "PHOENIX_ALLOW_EXTERNAL_RESOURCES": "false"}
    p = subprocess.Popen(
        [PHOENIX, "serve", "--host", HOST, "--port", str(PORT)],
        stdout=logf, stderr=subprocess.STDOUT, start_new_session=True, env=env)
    with open(PIDFILE, "w") as f:
        f.write(str(p.pid))
    for _ in range(40):
        time.sleep(2)
        if _healthy():
            print(f"phoenix up on {HOST}:{PORT} (pid {p.pid})")
            return
    print("phoenix failed to become healthy; see phoenix.log", file=sys.stderr)
    sys.exit(1)


def cmd_stop(_a):
    pid = _pid()
    if not pid:
        print("phoenix not running")
        return
    os.kill(pid, signal.SIGTERM)
    for _ in range(15):
        time.sleep(1)
        try:
            os.kill(pid, 0)
        except OSError:
            break
    else:
        os.kill(pid, signal.SIGKILL)
    try:
        os.remove(PIDFILE)
    except OSError:
        pass
    print("phoenix stopped")


def cmd_status(_a):
    print(f"pidfile: {_pid() or 'none'}; healthy: {_healthy()}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("start", cmd_start), ("stop", cmd_stop), ("status", cmd_status)):
        sp = sub.add_parser(name)
        sp.set_defaults(fn=fn)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
