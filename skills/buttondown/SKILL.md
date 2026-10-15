---
name: buttondown
description: "Manage a Buttondown newsletter through API v1: verify the key, list and create draft emails from Markdown files, and import/export subscribers as CSV. Drafts only — sending stays a human action. Use when a task involves Buttondown or its newsletter API."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and BUTTONDOWN_API_KEY set in the environment."
metadata:
  version: 1.0.0
---

# Buttondown

Drive the Buttondown API v1 for a newsletter: verify the key, create draft emails from Markdown files, list drafts, and import/export subscribers as CSV. Sending stays a human click; this skill never sends.

## Credentials

- `BUTTONDOWN_API_KEY` (required) — API key from the Buttondown dashboard (Settings → API), sent as `Authorization: Token <key>` (Buttondown's required scheme).

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/bd.py <command>` — see `bd.py --help`. Prints JSON to stdout; exits non-zero with the provider's error message on failure.

- `verify` — check the key against the live API (`GET /v1/emails`)
- `config` — note that newsletter settings live in the Buttondown dashboard (API v1 has no settings endpoint)
- `drafts [--limit N]` — list draft emails
- `emails [--status draft|scheduled|sending|sent]` — list emails
- `get-email <id>` — fetch one email's metadata (body excluded)
- `create-draft --file FILE.md [--subject S]` — create a draft from Markdown. Subject comes from `--subject`, else the file's `subject:`/`title:` frontmatter. Frontmatter is stripped (the API rejects bodies starting with `---`).
- `subscribers [--type TYPE] [--limit N]` — list subscribers
- `export-subscribers --out FILE.csv` — export every subscriber to CSV
- `import-subscribers --in FILE.csv [--type regular] [--tags a,b]` — import from a CSV with an `email` column. `regular` type skips double opt-in — use only for consented lists.

See `references/api-notes.md` for the endpoint-level contract (envelope, pagination, limits).

## Operating rules

1. Use this skill when the user asks for Buttondown or its newsletter API.
2. Restrict authenticated requests to: api.buttondown.com.
3. Never create, schedule, or send an email without the user's explicit go-ahead for that specific issue. `create-draft` is preparation, not sending — and `bd.py` deliberately has no send command.
4. Do not print, log, or persist raw credentials.
5. The API v1 has no settings endpoint; the newsletter name, description, and custom domain are managed in the Buttondown dashboard.
6. A 401 or 403 is a question about the request before it is a question about the key: check that `BUTTONDOWN_API_KEY` is set and current in the dashboard first.
