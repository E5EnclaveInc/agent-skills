#!/usr/bin/env python3
"""BlenderMCP skill CLI — isolated 3D scene control.

Every MCP call spawns the BlenderMCP server as the unprivileged
'blender-mcp' system account (no-login shell, isolated home); Blender itself
runs headless under Xvfb as the same account with its socket bound to
127.0.0.1:9876 only. The wrapper (this process) may run as root, but neither
Blender nor its MCP server ever does.

Server env: telemetry disabled, safe-mode code guard on.
Tool allowlist is enforced here: only local scene tools are reachable.
Asset-download / AI-generation tools (PolyHaven, Sketchfab, Hyper3D, Hunyuan)
are blocked — they need accounts/keys and are out of scope for this pilot.
"""
import argparse
import json
import os
import socket
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _mcp_stdio import call_tool, list_tools, scrubbed_env  # noqa: E402

# Install layout — override any of these via the environment.
VENV_BIN = os.environ.get("BLENDER_MCP_BIN", "/opt/mcp-venvs/blender-mcp/bin/blender-mcp")
BLENDER_BIN = os.environ.get("BLENDER_BIN", "/opt/blender-4.5.0/blender")
BLENDER_USER = os.environ.get("BLENDER_USER", "blender-mcp")
BLENDER_HOME = os.environ.get("BLENDER_HOME", "/home/" + BLENDER_USER)
HOST, PORT = "127.0.0.1", 9876

# Local scene tools only. execute_blender_code is additionally guarded by
# BLENDER_MCP_SAFE_MODE (deny-by-default static validation on the MCP path).
ALLOWLIST = {
    "get_scene_info",
    "get_object_info",
    "get_viewport_screenshot",
    "execute_blender_code",
    "describe_node_type",
    "bpy_api_lookup",
    "export_scene",
}

SERVER_ENV = {
    "BLENDER_MCP_DISABLE_TELEMETRY": "1",
    "BLENDER_MCP_SAFE_MODE": "1",
    "BLENDER_HOST": "localhost",
    "BLENDER_PORT": str(PORT),
    "HOME": BLENDER_HOME,
}


def _guard(tool):
    if tool not in ALLOWLIST:
        sys.exit(f"refusing: tool '{tool}' is not on the blender allowlist")


def _blender_up():
    try:
        socket.create_connection((HOST, PORT), timeout=3).close()
        return True
    except OSError:
        return False


def ensure_blender(timeout=90):
    """Start headless Blender (Xvfb) as the isolated user if not listening."""
    if _blender_up():
        return
    log = os.path.join(BLENDER_HOME, "blender.log")
    with open(log, "ab") as fh:
        subprocess.Popen(
            ["runuser", "-u", BLENDER_USER, "--",
             "xvfb-run", "-a", BLENDER_BIN,
             "--python-expr",
             "import addon_utils; addon_utils.enable('blender_mcp')"],
            stdin=subprocess.DEVNULL, stdout=fh, stderr=subprocess.STDOUT,
            start_new_session=True, cwd=BLENDER_HOME,
        )
    import time
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _blender_up():
            return
        time.sleep(2)
    sys.exit("blender did not come up on 127.0.0.1:9876; see " + log)


def _run(tool, params, timeout=180):
    ensure_blender()
    _guard(tool)
    env = scrubbed_env(SERVER_ENV)
    return call_tool("runuser",
                     ["-u", BLENDER_USER, "--", VENV_BIN],
                     tool, params, timeout=timeout, extra_env=env, cwd=BLENDER_HOME)


def cmd_tools(_a):
    ensure_blender()
    env = scrubbed_env(SERVER_ENV)
    tools = list_tools("runuser", ["-u", BLENDER_USER, "--", VENV_BIN],
                       timeout=90, extra_env=env, cwd=BLENDER_HOME)
    print(json.dumps([t for t in tools if t["name"] in ALLOWLIST], indent=2))


def cmd_scene_info(_a):
    print(json.dumps(_run("get_scene_info",
                          {"user_prompt": "Summarize the current scene."}),
                     indent=2))


def cmd_exec(a):
    code = open(a.code_file).read()
    if len(code) > 20000:
        sys.exit("refusing: code file over 20KB")
    print(json.dumps(_run("execute_blender_code", {"code": code}), indent=2))


def cmd_screenshot(a):
    print(json.dumps(_run("get_viewport_screenshot",
                          {"filepath": a.filepath} if a.filepath else {}),
                     indent=2))


def cmd_export(a):
    print(json.dumps(_run("export_scene",
                          {"filepath": a.filepath,
                           "format": a.format}), indent=2))


def main():
    p = argparse.ArgumentParser(description="Isolated BlenderMCP control")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tools").set_defaults(fn=cmd_tools)
    sub.add_parser("scene-info").set_defaults(fn=cmd_scene_info)
    e = sub.add_parser("exec", help="Run a bpy script file (safe-mode validated)")
    e.add_argument("code_file"); e.set_defaults(fn=cmd_exec)
    s = sub.add_parser("screenshot")
    s.add_argument("--filepath", default=""); s.set_defaults(fn=cmd_screenshot)
    x = sub.add_parser("export")
    x.add_argument("filepath"); x.add_argument("--format", default="glb")
    x.set_defaults(fn=cmd_export)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
