---
name: phoenix
description: "Use for LLM-observability pilot work — start the local Phoenix server, run the scripted OTel pilot, query traces. Localhost-only, pilot-scoped, short-lived runs."
license: MIT
compatibility: "Requires Python 3 with arize-phoenix installed in a venv (PHOENIX_VENV env var; see SKILL.md)."
metadata:
  version: 1.0.0
---
# Phoenix (observability pilot)

## Purpose
Prove OpenTelemetry → Phoenix trace wiring end-to-end with a scripted pipeline, and query the resulting traces. This is a **pilot**, not fleet-wide instrumentation.

## Tooling
- `bin/phoenix_ctl.py {start|stop|status}` — runs Phoenix (`arize-phoenix==20.12.0`) on **127.0.0.1:6006** only. SQLite store at `bin/run/phoenix.db` (short retention). Sets `PHOENIX_ALLOW_EXTERNAL_RESOURCES=false` so the built-in Mintlify docs MCP server (external internet) doesn't break startup behind a restrictive egress proxy.
- `bin/pilot_run.py` — the full pilot: starts Phoenix → emits OTel spans (canary + scripted sweep iteration) via **OTLP/HTTP** (`POST http://127.0.0.1:6006/v1/traces`) → verifies the canary trace via the project-scoped REST API → checks secret-shaped attributes arrived redacted at span-attribute level → smokes the built-in `/mcp` endpoint → stops Phoenix.

Transport note: in restricted-egress sandboxes the OTLP/gRPC receiver on port 4317 may be **unusable** — grpcio can route it through the sandbox egress proxy regardless of environment, failing the HTTP/2 handshake. OTLP/HTTP on the main port is the working equivalent. If your receiver binds all interfaces, shield port 4317 with a firewall INPUT rule (`! -i lo → DROP`).

```bash
bin/pilot_run.py   # the whole pilot, ~2 minutes
```

## Operating Rules
1. **Localhost only.** Phoenix's self-hosted UI has no auth — never bind it to anything but 127.0.0.1, never proxy it outward.
2. **Short-lived.** Phoenix runs only for the duration of a pilot run, then stops. No permanent daemon.
3. **Trace data is sensitive.** Every span attribute is redacted client-side for secret-shaped values (keys, tokens, long hex) before export; the pilot verifies the redaction by querying Phoenix back.
4. **Scope honesty.** The pilot instruments a *scripted* pipeline, not the live agent loops. True runtime instrumentation of live agent loops needs runtime hooks most agent runtimes don't expose yet — staged as NEXT, not silently claimed.
5. **Removal:** `bin/phoenix_ctl.py stop` and delete this skill directory (+ `pip uninstall arize-phoenix` from the venv if desired).
