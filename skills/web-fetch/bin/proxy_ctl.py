#!/usr/bin/env python3
"""proxy_ctl.py — manage the web-fetch validating egress proxy daemon."""
import argparse
import os
import signal
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(os.environ.get("MCP_VENV", os.path.expanduser("~/.venvs/mcp")), "bin", "python")
PROXY = os.path.join(HERE, "egress_proxy.py")
PIDFILE = os.path.join(HERE, "run", "proxy.pid")
LOGFILE = os.path.join(os.path.dirname(HERE), "proxy.log")
HOST, PORT = "127.0.0.1", 8899


def _pid():
    try:
        with open(PIDFILE) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def _healthy():
    # The proxy only speaks proxy protocol; a TCP connect proves liveness.
    import socket
    try:
        s = socket.create_connection((HOST, PORT), timeout=3)
        s.close()
        return True
    except OSError:
        return False


def cmd_start(_a):
    if _pid() and _healthy():
        print(f"proxy already running (pid {_pid()})")
        return
    os.makedirs(os.path.dirname(PIDFILE), exist_ok=True)
    logf = open(LOGFILE, "a")
    # The daemon needs the sandbox egress vars to chain upstream; nothing else.
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/root",
           "LANG": "C.UTF-8"}
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
                "ALL_PROXY", "all_proxy", "NO_PROXY", "no_proxy"):
        if var in os.environ:
            env[var] = os.environ[var]
    p = subprocess.Popen([VENV_PY, PROXY], stdout=logf, stderr=subprocess.STDOUT,
                         start_new_session=True, env=env)
    with open(PIDFILE, "w") as f:
        f.write(str(p.pid))
    time.sleep(1.5)
    if _healthy():
        print(f"proxy started (pid {p.pid}) on {HOST}:{PORT}")
    else:
        print("proxy failed to become healthy; see proxy.log", file=sys.stderr)
        sys.exit(1)


def cmd_stop(_a):
    pid = _pid()
    if not pid:
        print("proxy not running")
        return
    os.kill(pid, signal.SIGTERM)
    time.sleep(1)
    try:
        os.kill(pid, 0)
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass
    try:
        os.remove(PIDFILE)
    except OSError:
        pass
    print("proxy stopped")


def cmd_status(_a):
    pid = _pid()
    print(f"pidfile: {pid or 'none'}; healthy: {_healthy()}")


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
