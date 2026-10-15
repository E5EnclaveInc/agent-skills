---
name: elevenlabs
description: "Drive the ElevenLabs API: text-to-speech, speech-to-text, sound effects, music, voices, dubbing, and usage — with content-hash idempotency, backoff, and quota preflight built in. Use when a task involves ElevenLabs, voice generation, or its API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and ELEVENLABS_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# ElevenLabs — capability router

## Lanes

- **Hosted MCP** (`https://api.elevenlabs.io/v1/mcp`, OAuth 2.x, workspace-scoped): the vendor's forward direction — the local MCP server package is archived; do not build on it. Use it where it has the tool (notably image/video generation).
- **API-key REST lane** (`bin/el.py`): live for everything below, and the only lane for the REST-only rows. This skill's CLI drives this lane.

## Credentials

- `ELEVENLABS_API_KEY` (required) — an ElevenLabs API key, sent as the `xi-api-key` header.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Lane table

| Capability | MCP (hosted) | REST (`el.py`) | Console-only |
|---|---|---|---|
| TTS (incl. v3, dialogue) | `creative_generate_speech` | ✅ full — v3, `/stream`, text-to-dialogue | — |
| TTS — `eleven_v4` (expressive) | hosted tools | ✅ full | Studio |
| TTS — `eleven_v4_turbo` (real-time ~100ms) | hosted tools | ✅ full | Studio |
| STT (Scribe) | ✅ | ✅ | — |
| SFX | ✅ | ✅ | — |
| Music | ✅ | ✅ full suite (compose, stems, inpaint) | — |
| Image / video gen, edit, animate, lip-sync | ✅ **only programmatic lane** | — | enterprise API on request |
| Agents platform | ✅ create/update/list/duplicate, conversations, outbound, KB, cost estimate | — | Studio Agent (web-only) |
| Pronunciation dictionaries (full CRUD) | — | ✅ **REST-only** | — |
| Forced alignment | — | ✅ **REST-only** | — |
| History (per-generation audit) | — | ✅ **REST-only** | — |
| Voice design / IVC / library | — | ✅ | — |
| Dubbing | ✅ | ✅ project endpoints + v2 API | Dubbing Studio manual edit |
| Long-form Projects / Studio timeline | — | ✅ project endpoints | Studio 4.0 agentic editor (console-only; the Projects/Studio API requires explicit whitelisting by ElevenLabs sales) |
| Seats / billing | — | usage endpoints (read) | ✅ |

**Layering rule:** MCP-native chaining where the MCP has the tool; `el.py` for the REST-only rows. Never build on the archived local MCP package or the outdated npm `elevenlabs` package.

## Spend gates (mandatory before every real call)

1. **Estimate-first:** quote the cost before generating. On REST, one call = one generation.
2. **Idempotency:** content-hash cache (method+path+body) in the scratch dir (`EL_SCRATCH_DIR`, default `/tmp/elevenlabs/`; never writes machine state into the skill dir) — never pay twice for the same render; `el.py` enables it by default on TTS POSTs.
3. **Quota preflight:** `GET /v1/user` before a batch; abort if headroom < planned spend.
4. **Backoff:** exponential backoff on 408/409/429/5xx (built into `el.py`); never hot-loop on 429.
5. **No verification burns:** every API call is substance. Read headroom from usage data, never from a dedicated check-call.
6. **Image/video: expensive-until-measured** — estimate-first gates stay until you have measured real burn.

## Usage

CLI: `bin/el.py` — `el.py METHOD /v1/path [--data '{...}'] [--params '{...}'] [--file name=/path] [--out file] [--idempotent/--no-idempotent]`.
Examples: `el.py GET /v1/voices`, `el.py POST /v1/text-to-speech/{voice_id} --data '{"text":"..."}' --out voice.mp3`.
Binary responses need `--out FILE`. Every call appends one unit-labeled JSONL line to `usage.jsonl` in the scratch dir, so spend can be audited offline.

**Full playbook:** `PLAYBOOK.md` in this skill — a durable reference for models, voice settings, v3 tags, streaming, the agents platform, dubbing/SFX/music, API best practices, and billing. Consult it before speccing any new ElevenLabs build; re-verify dated prices/limits against `https://elevenlabs.io/docs/llms.txt`. `CONSOLE_VIDEOBOOK.md` covers console-only workflows (Studio timeline, agent builder, credit-cost displays).

## QC gates (no output skips local gates)

Every chained or generated output passes: listen-check (Scribe round-trip, word-for-word, ≥92%), caption safe zone (y-center ≈1050, hard floor 1150 on 1080×1920), identity lock (use your canonical clone voices — enumerate your library first with `GET /v1/voices`, which returns the whole library at once; never substitute a premade voice when a canonical clone exists).

## v4 TTS lane (verified 2026-10)

New TTS renders use `eleven_v4` (expressive) / `eleven_v4_turbo` (real-time ~100ms). Migrated recipe: stability **0.55** / similarity_boost **0.75** / speed **1.0**. `style` and `use_speaker_boost` are **struck on v4** — rejected per the live `/v1/models` flags (`can_use_style:false`, `can_use_speaker_boost:false`). Already-baked audio beds are model-agnostic files: never re-render them just to prove a migration. Python SDK: pin ≥ **2.71.0** (`model_id` is a plain string, no SDK gate).

## Long-form audiobook precedent

For long-form batch renders, `eleven_v4` (non-turbo) is the right default — turbo's virtue is latency, which a batch doesn't spend; turbo remains the lane for short-form interactive work. Method: per-speaker-turn segmentation with per-turn retry (never re-render the whole batch); inter-turn pauses derived from the source's word timings (timing-derived assemblies rate more natural than uniform-gap in blind A/B); chapter markers at content beats; render-verified vs ear-verified tiering with numbered ear gates (first-60s identity, pilot-chapter direction/pacing, post-assembly spot-listen of a sample of turns + the longest turn, words verified against transcript).

## Operating rules

1. Use this skill when the user asks for ElevenLabs or this provider's API.
2. Restrict authenticated requests to: api.elevenlabs.io.
3. Do not print, log, or persist raw credentials.
4. If auth is missing or rejected, check that `ELEVENLABS_API_KEY` is set and scoped for the endpoint before assuming the key is dead.
