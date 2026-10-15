---
name: groq
description: "Call the GroqCloud API (OpenAI-compatible): list models and run chat completions at Groq speed. Use when a task involves Groq, GroqCloud, or its API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and GROQ_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Groq

A thin, scriptable client for the GroqCloud API (`https://api.groq.com`, OpenAI-compatible under `/openai/v1`).

## Credentials

- `GROQ_API_KEY` (required) — a GroqCloud API key (console.groq.com), sent as `Authorization: Bearer`.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/groq.py` —
`groq.py METHOD /openai/v1/path [--data '{...}'] [--params '{...}']`.
Example: `groq.py GET /openai/v1/models`.

## Operating rules

1. Restrict authenticated requests to: api.groq.com.
2. Do not print, log, or persist raw credentials.
3. A 401/403 first means check the request carried the key at all — an unauthenticated request looks identical to a bad key. Check that `GROQ_API_KEY` is set before concluding the key is dead.
4. Watch rate limits: free-tier keys are token-capped per minute; pace batch work and treat 429s as back-off signals, not errors to retry hot.
