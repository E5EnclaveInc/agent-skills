---
name: typesafe-jev
description: "Call TypeSafe's Jev System One decision model: fast structured Choice/Score/Noul judgments (POST /v1/systemone) and model listing (GET /v1/models). Keyed via the TYPESAFE_API_KEY environment variable. Use for decision/classification/eval-judge tasks where a typed answer with calibrated probabilities beats text generation."
license: MIT
compatibility: "Requires a TypeSafe API key in the TYPESAFE_API_KEY environment variable."
metadata:
  version: 1.0.0
---
# TypeSafe / Jev

## Purpose
Call Jev (`jev-latest`), TypeSafe's System One decision model, over HTTPS.
Jev does not generate text: it evaluates typed **questions** (Choice / Score /
Noul) against a **state** string and returns typed answers with probabilities
and confidence. Intended for classification, routing, and evaluator/judge
workloads — not for prose, code, or conversation.

## Tooling
- `bin/jev_client.py` — importable client: `list_models()`,
  `ask_systemone(state, questions, model="jev-latest")`. Uses only stdlib
  (`urllib`); the API key comes from the `TYPESAFE_API_KEY` env var. Import it from experiment
  scripts; do not shell out per call.
- `bin/typesafe.py` — thin CLI over the client:
  - `python3 bin/typesafe.py models` → GET /v1/models (auth check; no spend)
  - `python3 bin/typesafe.py ask --state-file S --questions-file Q [--model jev-latest] [--dry-run]`
    → POST /v1/systemone; prints the raw JSON response. `--dry-run` prints
    the request body and makes no call.
- Question JSON shape (per official docs):
  `{"<key>": {"type": "choice"|"score"|"noul", "instructions": "...", "criteria": {...}}}`
  - choice: `criteria` = object mapping each option name → description.
  - score: `criteria` = ordered list of rubric level descriptions.
  - noul: `criteria` omitted; `instructions` states the yes/no proposition.
- Response: `answers.<key>` carries `choice`/`score`/`noul` plus
  `probabilities` and `confidence` (choice/score); top-level `model` (resolved
  version, e.g. `jev-1.13.0`) and `usage: {input_tokens, output_tokens}`.
  Always record `usage.input_tokens` — it is the billing basis.

## Auth
Set your TypeSafe API key in the environment: `export TYPESAFE_API_KEY=<your key>`.
The client (`bin/jev_client.py`) reads it per request and sends it as an
`Authorization: Bearer` header to `api.typesafe.ai` only. Never print, log, or
persist the key; never pass it as a CLI flag or write it to an auth file.
A 401/403 is a question about the request before it is a question about the
key — verify the header was attached and the key is current before assuming
the credential is bad.

## API surface (grounded in https://docs.typesafe.ai/introduction/quickstart)
| Operation | Method + path |
|---|---|
| List models / auth check | `GET https://api.typesafe.ai/v1/models` |
| Ask Jev | `POST https://api.typesafe.ai/v1/systemone` |

- Request body: `{"state": str, "model": "jev-latest", "questions": {...}}`.
  Multiple questions in one call are evaluated in parallel against the same
  state; adding questions barely changes latency.
- Vendor pricing (stated, not independently verified): **$0.042 / MTok input,
  outputs free**. Cost per call = `usage.input_tokens / 1e6 * 0.042`.
  LangChain's observed cost in their eval experiment: **$0.00035/call**.
- Vendor latency claim: 70–500 ms end-to-end. LangChain observed mean 0.44 s.

## Operating Rules
1. Authenticated requests go only to `api.typesafe.ai`.
2. Do not print, log, or persist raw credentials.
3. Every evaluation use must carry a spend cap: estimate input tokens
   (state chars / 4) × calls × $0.042/1e6 before running; refuse to start if
   the projection exceeds the approved cap.
4. Record per call: model version returned, selected answer, probabilities,
   confidence, wall-clock latency, `usage.input_tokens`.
5. Jev is early-access and calls leave our infra. Type-safety ("can't
   hallucinate") is not judgment quality — any pipeline-swap decision needs a
   head-to-head validation against a held-out oracle first (see
   `references/langchain-methodology.md`).
6. Never invent oracle labels. The oracle is a stored artifact (e.g. a completed,
   human-reviewed adjudication set); Jev's answers are measured against it,
   never the reverse.
