---
name: zenodo
description: "Work with the Zenodo API: search and read records, manage draft depositions, upload files via bucket URLs, update metadata, create new versions, and publish. Use when a task involves Zenodo, DOIs, or depositing research outputs."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and ZENODO_ACCESS_TOKEN set in the environment."
metadata:
  version: 1.0.0
---

# Zenodo

A thin, scriptable client for the Zenodo API (`https://zenodo.org`).

## Credentials

- `ZENODO_ACCESS_TOKEN` (required) — a Zenodo personal access token (zenodo.org → Applications → Personal access tokens), sent as `Authorization: Bearer`. Scope the token to deposits unless you need more.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/zenodo.py` —
`zenodo.py METHOD /path [--data '{...}'] [--params '{...}'] [--upload-file PATH --upload-name NAME --bucket URL]`.
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

Common flows:
- New version draft: `zenodo.py POST /api/deposit/depositions/{id}/actions/newversion`
- Delete a draft file: `zenodo.py DELETE /api/deposit/depositions/{id}/files/{file_id}`
- Upload a file to a draft: `zenodo.py PUT-BUCKET --bucket {links.bucket} --upload-file PATH --upload-name "a/b.zip"` (PUT to `{bucket}/{name}`)
- Update metadata: `zenodo.py PUT /api/deposit/depositions/{id} --data '{"metadata": {...}}'`
- Publish: `zenodo.py POST /api/deposit/depositions/{id}/actions/publish`
- Public record: `zenodo.py GET /api/records/{id}` (no auth needed, but auth works too)

## Operating rules

1. Use this skill when the user asks for Zenodo or this provider's API.
2. Restrict authenticated requests to: zenodo.org.
3. Do not print, log, or persist raw credentials.
4. Publishing is irreversible in effect (a published record gets a DOI) — confirm with the user before `actions/publish`.
5. Never create a GitHub Release to trigger the GitHub–Zenodo auto-integration without explicit user approval; prefer explicit versioned API deposits.
