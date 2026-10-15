---
name: rea
description: "Use REA (Reverse Engineer Anything) to investigate shipped binaries, apps, and packages: native via Ghidra, JS/Electron static analysis, process capture on owned builds only, and the evidence/ledger contracts. Adopted under per-lane policy gates — read POLICY.md before first use; third-party analysis is not authorized."
license: MIT
compatibility: "Requires the rea-agents CLI (pinned 6.0.0) installed locally; Ghidra for the native lane."
metadata:
  version: 1.0.0
---
# REA — Reverse Engineer Anything (adoption profile, pinned 6.0.0)

## Purpose
Agent-driven investigation of **shipped artifacts** — recover mechanism (pseudocode, IPC routes, module graphs, protocols) from the artifact itself, without the producer's source. Complements a video-first skill-acquisition lane with ground-truth internals; serves a studio build lane as build-regression (authority vs rebuild comparison).

Adopted 2026-10-08 under a recorded internal review (record kept with the adopting team's docs), standing **ADOPT-SCOPED, per-lane**. The full vendor surface is 139 MCP tools / 94 CLI commands — the fleet adopts the lanes below, not the blob. Read `POLICY.md` before first use.

## Tooling
- CLI: `rea` on PATH from your local install (pinned `rea-agents@6.0.0`; `rea --help` lists 94 commands). No registration needed for CLI use.
- MCP server: `rea --mcp` over stdio (139 tools, verified live 2026-10-08). Register it in your agent runtime's MCP config (e.g. a `[mcp_servers.rea]` stdio entry).
- Vendored guides: `references/` — the 5 upstream playbooks (native-and-artifacts, javascript-applications, android-applications, runtime-observation, evidence-workflows), MIT, verbatim from the pinned 6.0.0 tree.

## The evidence contract (adoption doctrine)
Every REA conclusion must distinguish **observations, inferences, and unknowns** — never imply that static analysis observed execution. Cite Evidence IDs. Static tools parse the artifact as inert text ("parsed as inert text; never executed"); runtime tools are explicitly marked. This discipline is the primary thing this adoption takes from the tool.

## Adopted lanes (the only authorized surface)
1. **JS/Electron static analysis** — `analyze-javascript-application` and kin. Pure static, no engine, safest surface.
2. **Native analysis via the Ghidra provider only** — headless, $0. Hopper/IDA providers: never enabled (severed per the $0 doctrine).
3. **Process capture on owned builds only** — authority-vs-rebuild comparison (`compare-process-captures`) for studio build-regression. `REA_PROCESS_ALLOW_EXTERNAL_NETWORK` stays false unless a run's charter explicitly sets it.
4. **Evidence/ledger workflows** — session lifecycle, `export_evidence_bundle`, `verify_reconstruction`.

## Operating Rules
1. Use this skill when a claim depends on a shipped binary or package your team owns or holds analysis rights over. For ordinary source-repository analysis, use normal repo tools — do not run REA.
2. **POLICY.md is mandatory reading** — it carries the lane gates (browser-scenario RED, third-party analysis NOT authorized, the 894× token rule).
3. Prefer targeted queries; never dump bulk evidence into an agent loop (see the 894× rule in POLICY.md).
4. Static first: reach for a runtime tool only when the question cannot be answered statically, and say so in the record.
5. Version pin: `rea-agents@6.0.0`, mirrored from upstream at commit `6fee4268`. Never auto-update; a monthly freshness check alerts on drift (latest-only security support).
