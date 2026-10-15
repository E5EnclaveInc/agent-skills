---
name: huggingface
description: "Run chat completions through Hugging Face's hosted inference router (OpenAI-compatible), including vision models via image input and SSE streaming. Use when a task needs a Hugging Face model call, an independent second-opinion model lane, or HF Inference."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and HF_TOKEN set in the environment."
metadata:
  version: 1.0.0
---

# Hugging Face

Chat completions through Hugging Face's OpenAI-compatible router (`https://router.huggingface.co/v1`).

## Credentials

- `HF_TOKEN` (required) — a Hugging Face access token (huggingface.co → Settings → Access Tokens), sent as `Authorization: Bearer`. `HUGGINGFACE_API_KEY` is accepted as a fallback name.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/hf-chat.py` — OpenAI-compatible chat completions:
`hf-chat.py --model <id> --system "..." --user "..." [--image page.png] [--max-tokens N] [--timeout S] [--stream] [--raw]`
Image input is sent as a data-URI inside the user message, for vision models.

## Second-opinion judge lane (pattern)

HF models make a good *independent* second lane next to another provider's lane when reviewing generated work — pick models from a different family than your primary lane, and show them only the artifact and the rubric, never the first lane's rationale or review history. Two picks that work well:

- Content/reasoning: `deepseek-ai/DeepSeek-R1` — recomputes numbers, reasoning trace auditable.
- Page/visual style: `Qwen/Qwen2.5-VL-72B-Instruct` — typography, layout, hierarchy from rendered page images.

## Operating rules

1. Use this skill when the user asks for Hugging Face or this provider's API.
2. Restrict authenticated requests to: router.huggingface.co, api-inference.huggingface.co.
3. Do not print, log, or persist raw credentials.
4. A 401 or 403 is a question about the request before it is a question about the key: check that `HF_TOKEN` is set and the token carries Inference permissions first.
