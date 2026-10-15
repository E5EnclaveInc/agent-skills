# REA Usage Policy + Capability Gates
**Authority:** a 2026-10-08 internal review, rulings R1/R4/R5 (record §6, kept with the adopting team's docs). **Standing:** enforced as doctrine; violations are defects, not judgment calls.

## 1. The 894× rule (token cost)
Measured 2026-10-08 (COMPUTED): a 4-file JS fixture (362 bytes of source) returned **323,573 bytes of JSON** — an ~894× verbosity ratio (~80k+ tokens for a trivial app). **Targeted queries only.** Never dump bulk evidence into an agent loop. Ask for the narrow finding; page or filter before ingesting.

## 2. Lane gates
| Lane | Status | Gate |
|---|---|---|
| JS/Electron static | **GREEN** | Pure static; no engine. Freely usable on owned artifacts. |
| Native via Ghidra provider | **GREEN** | Headless, $0. The only authorized native provider. |
| Process capture | **GREEN on owned builds only** | Authority-vs-rebuild comparison for studio regression. `REA_PROCESS_ALLOW_EXTERNAL_NETWORK` defaults **false**; enabling it needs a run charter naming why. |
| Evidence/ledger workflows | **GREEN** | Session, bundles, `verify_reconstruction`. The doctrine lane. |
| Browser-scenario capture | **RED** | Except against **owned fixtures** (e.g. `127.0.0.1` test rigs), behind the safety kernel's ToS capability gate (deny-by-default). Mechanism class: automated access against arbitrary URLs with no origin allowlist — same class as other automated-access ToS gates. |
| Firmware / APK / EVM / recorded crashes / .NET | **NOT WIRED** | Docs vendored; tools unregistered. Revisit only on a named need. |
| Hopper / IDA providers | **NEVER** | Severed per the $0 doctrine. Hopper is macOS-only; IDA tiers are paid. |

## 3. The IP boundary (hard)
- **Owned assets** (studio builds, our fixtures, artifacts we hold rights to analyze): clear.
- **Third-party clients** (any shipped product whose producer has not authorized analysis): **NOT AUTHORIZED.** F-flagged to counsel (DMCA §1201, CFAA, EULA RE clauses — the war room's F-1/F-2/F-3). The repo's entire legal posture is a 3-sentence generic disclaimer with zero statute mentions; its silence is not clearance. This is a human judgment call, never computed by an agent.

## 4. Version discipline
- Pin: `rea-agents@6.0.0` (139 MCP tools / 94 CLI commands, verified live 2026-10-08).
- Mirror: a local mirror of the upstream repo at commit `6fee4268`.
- The vendor supports **latest-only** security fixes: a stale pin is unsupported. The monthly freshness check alerts on drift — **alert, never auto-update**.

## 5. What "wired" means here
- **Agent CLI config** (an `[mcp_servers.rea]` stdio entry in the runtime's MCP config store): registered transactionally, with a backup of the prior config.
- **Skill lane**: this skill + the CLI on PATH + this policy. Where the runtime exposes no separate MCP config surface, the skill is the wiring.
- Full 139-tool surface registers (the vendor removed per-tool permission policies in 4.0.0); **the adopted-lane restriction is enforced by this policy, not by a technical filter.** Treat any call outside §2's GREEN lanes as a policy violation.
