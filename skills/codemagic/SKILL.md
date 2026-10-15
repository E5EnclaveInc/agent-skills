---
name: codemagic
description: "Drive the Codemagic CI API from the command line: list apps, trigger and poll builds, and inspect build status. Use when a task involves Codemagic builds, apps, or workflows, or asks about Codemagic or its API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and CODEMAGIC_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Codemagic

A thin, scriptable client for the Codemagic API (`https://api.codemagic.io`).

## Credentials

- `CODEMAGIC_API_KEY` (required) — Codemagic API token (Codemagic → Teams/User settings → Integrations → Codemagic API), sent as the `x-api-key` header.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/cm.py` — `cm.py METHOD /path [--data '{...}'] [--params '{...}']`.
Examples: `cm.py GET /apps`, `cm.py POST /builds --data '{"appId":"...","workflowId":"...","branch":"main"}'`, `cm.py GET /builds/<build_id>`.
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Codemagic or this provider's API.
2. Restrict authenticated requests to: api.codemagic.io.
3. Do not print, log, or persist raw credentials.
4. A 401 or 403 is a question about the request before it is a question about the key: check that `CODEMAGIC_API_KEY` is set and the token has the needed scope before assuming the key is dead.
