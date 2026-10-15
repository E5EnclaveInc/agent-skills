---
name: github
description: "Call the GitHub REST API from the command line: repos, contents, issues, pull requests, and any other endpoint. Use when a task involves GitHub or its API and a small scriptable client is handier than a full integration."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and GITHUB_TOKEN set in the environment."
metadata:
  version: 1.0.0
---

# GitHub

A thin, scriptable client for the GitHub REST API (`https://api.github.com`).

## Credentials

- `GITHUB_TOKEN` (required) — a GitHub personal access token (fine-grained or classic) with only the scopes the task needs, sent as `Authorization: Bearer`.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/gh.py` — `gh.py METHOD /path [--data '{...}'] [--params '{...}']`.
Examples: `gh.py GET /repos/{owner}/{repo}`, `gh.py GET /repos/{owner}/{repo}/contents/{path} --params '{"ref":"main"}'`.
Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for GitHub or this provider's API.
2. Restrict authenticated requests to: api.github.com.
3. Do not print, log, or persist raw credentials.
4. A 401 or 403 is a question about the request before it is a question about the key: check that `GITHUB_TOKEN` is set, unexpired, and scoped for the repo before assuming the token is dead.
