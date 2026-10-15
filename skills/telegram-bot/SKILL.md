---
name: telegram-bot
description: "Operate a Telegram bot through the Bot API: verify the bot identity, send (automatically chunked) messages, and poll updates. Use when a task involves a Telegram bot, a @BotFather token, or sending Telegram messages programmatically."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) and TELEGRAM_BOT_TOKEN set in the environment."
metadata:
  version: 1.0.0
---

# Telegram Bot

A small command client for the Telegram Bot API (`https://api.telegram.org`).

## Credentials

- `TELEGRAM_BOT_TOKEN` (required) — the bot token issued by @BotFather. Telegram's API design carries the token in the request URL path (`/bot<token>/<method>`), so never log full request URLs.

Provide it as an environment variable, or through your agent platform's secret store — never print, log, or commit it.

## Usage

CLI: `bin/tg.py` —

- `tg.py getme` — bot identity; proves the token works.
- `tg.py send --chat <id> --text "..."` (or `--file <path>`) — send a message; texts over 4000 chars are chunked automatically.
- `tg.py updates [--offset N] [--timeout S]` — getUpdates; prints the JSON array.

Prints JSON to stdout; exits non-zero with the provider's error message on failure.

## Operating rules

1. Use this skill when the user asks for Telegram Bot or this provider's API.
2. Restrict authenticated requests to: api.telegram.org.
3. Do not print, log, or persist raw credentials — including request URLs, which contain the token.
4. A 401 means the token is wrong or revoked (re-issue via @BotFather); a 404 on a method usually means a malformed token reached the API.
