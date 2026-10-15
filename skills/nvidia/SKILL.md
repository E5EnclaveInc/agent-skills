---
name: nvidia
description: "Run chat completions against NVIDIA NIM hosted models (integrate.api.nvidia.com, OpenAI-compatible), with reasoning-effort control, SSE streaming, and catalog listing. Use when a task involves NVIDIA NIM, build.nvidia.com models, or an nvapi key."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and NVIDIA_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# NVIDIA NIM

Chat completions against NVIDIA's hosted NIM endpoints (`https://integrate.api.nvidia.com/v1`), OpenAI-compatible.

## Credentials

- `NVIDIA_API_KEY` (required) — an `nvapi-...` key from build.nvidia.com, sent as `Authorization: Bearer`.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/nim-chat.py`:
`nim-chat.py --model <id> --system "..." --user "..." [--image page.png] [--max-tokens N] [--timeout S] [--reasoning-effort low|medium|high] [--stream] [--raw] [--list-models]`

### API surface (from NVIDIA's official docs: docs.api.nvidia.com/nim/docs/api-quickstart, docs.api.nvidia.com/nim/reference/llm-apis)

- `POST https://integrate.api.nvidia.com/v1/chat/completions`, `Authorization: Bearer <nvapi-...>`.
- OpenAI-compatible body: model, messages (text + image_url data-URI parts), max_tokens, temperature, stream (SSE), response_format.
- Reasoning models accept top-level `reasoning_effort`; DeepSeek-style `reasoning_content` streams back on delta chunks.
- `GET /v1/models` lists the global catalog — NOT what your key can call.

### Provisioning other models (why a catalog model 404s)

Model availability is PER-ACCOUNT (NVCF routing), not per-catalog:

- `404 "Function '<uuid>': Not found for account"` = that model is not entitled for this key. Fix: while signed in at build.nvidia.com, open the model's page and accept the license once (click "Try API"). Keys minted via "Get API Key" on a model page are usually entitled for that model immediately.
- If the key 404s on EVERYTHING, it was minted without the "Public API Endpoints" scope — regenerate at build.nvidia.com/settings/api-keys with that scope.
- `410 Gone` = model retired (not coming back). `503` = temporarily unavailable, retry later.
- Some catalog entries are self-host-only (container deploy, no hosted endpoint) — 404 is expected there; no browser click fixes it.

### Example probe results (2026-09-25, one key — probe before trusting any ID)

- content (primary): `nvidia/nemotron-3-super-120b-a12b` — 120B reasoning model. Use with --reasoning-effort medium.
- content (fallback): `mistralai/mistral-nemotron`
- style/vision: `meta/llama-3.2-11b-vision-instruct`
- 404 on that key: `nvidia/llama-3.1-nemotron-70b-instruct`, `nvidia/llama-3.1-nemotron-ultra-253b-v1`, `qwen/qwq-32b`, `deepseek-ai/deepseek-v4.1-flash` (read timeout at probe)
- 410 retired: `nvidia/llama-3.3-nemotron-super-49b-v1`, `nvidia/llama-3.3-nemotron-super-49b-v1.5`, `moonshotai/kimi-k2-thinking`
- 503 at probe: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`

## Operating rules

1. Use this skill when the user asks for NVIDIA or this provider's API.
2. Restrict authenticated requests to: integrate.api.nvidia.com.
3. Do not print, log, or persist raw credentials.
4. A 401 or 403 is a question about the request before it is a question about the key: check that `NVIDIA_API_KEY` is set and the model is entitled for the key (see the 404 notes above).
