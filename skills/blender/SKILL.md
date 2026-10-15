---
name: blender
description: "Use for 3D scene work in Blender — inspect the scene, run bpy scripts, take viewport screenshots, export scenes. Headless Blender under an isolated unprivileged system account; explicit task-only invocation."
license: MIT
compatibility: "Requires Blender 4.5 + the blender-mcp server installed under an isolated unprivileged account (see SKILL.md isolation controls)."
metadata:
  version: 1.0.0
---
# Blender (isolated)

## Purpose
Programmatic 3D scene control: create/modify/inspect Blender scenes without a GUI. This is arbitrary local-code execution — treat it as such.

## Tooling
CLI: `bin/blender.py` in this skill directory (runs on the isolated venv Python).

```bash
bin/blender.py tools                 # allowlisted tools
bin/blender.py scene-info           # scene summary
bin/blender.py exec /path/code.py   # run a bpy script file
bin/blender.py screenshot --filepath /path/out.png
bin/blender.py export /path/scene.glb --format glb
```

Backend: `blender-mcp==1.9.4` MCP server + headless Blender 4.5.0 (Xvfb), both running as an unprivileged dedicated system account (default name `blender-mcp`, no-login shell, isolated home; override via the `BLENDER_USER` / `BLENDER_HOME` env vars the wrapper reads). The MCP server is spawned per call (no permanent daemon); Blender itself stays up headless and the wrapper restarts it if its socket drops. Addon socket binds **127.0.0.1:9876 only** (verified via `ss`).

Tool allowlist: `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, `execute_blender_code`, `describe_node_type`, `bpy_api_lookup`, `export_scene`. Asset-download and AI-generation tools (PolyHaven, Sketchfab, Hyper3D, Hunyuan) are blocked — they need accounts/keys.

## Isolation controls
- Blender and its MCP server NEVER run as root; wrapper drops privilege via `runuser -u <account>` before spawning the server.
- MCP server env is scrubbed; `BLENDER_MCP_DISABLE_TELEMETRY=1` (no phone-home to vendor Supabase) and `BLENDER_MCP_SAFE_MODE=1` (deny-by-default static validation of `execute_blender_code` on the MCP path).
- The isolated account cannot read the operator's credentials (keys are root-owned mode 600).
- No network egress is configured for the Blender user; the MCP server has no proxy vars in its env.

## Operating Rules
1. Explicit-task-only: run Blender work only when the user (or their delegated task) asked for 3D work. Never idle-drive it.
2. Save `.blend` files before agent-driven sessions (`bpy.ops.wm.save_as_mainfile`) — renders and edits are reproducible from the file.
3. Keep scripts small and idempotent; code files are capped at 20KB per call.
4. Do NOT enable the blocked asset/generator tools or create vendor accounts — that needs the user's word first.
5. Removal: `bin/blender.py` has no uninstaller of its own — full removal is:
   `pkill -u <account>; userdel -r <account>; rm -rf <skill dir> /opt/mcp-venvs/blender-mcp /opt/blender-4.5.0`
