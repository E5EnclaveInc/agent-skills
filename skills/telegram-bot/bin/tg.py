#!/usr/bin/env python3
"""Telegram Bot API CLI using the TELEGRAM_BOT_TOKEN environment variable.

Commands:
    getme                                   Bot identity (proves the token works)
    send --chat <id> --text T [--file F]    Send a message (chunks >4000 chars)
    updates [--offset N] [--timeout S]      getUpdates; prints JSON array

The bot token travels in the request URL path — that is the Telegram Bot
API's own design (https://api.telegram.org/bot<token>/<method>) — so never
log full request URLs. The token itself is never printed.
Prints JSON to stdout; exits non-zero with the provider's error on failure.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.telegram.org/bot{}/"
CHUNK = 4000
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


class TelegramError(RuntimeError):
    pass


class CredentialError(RuntimeError):
    pass


def api_url(method: str) -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise CredentialError(
            "set the TELEGRAM_BOT_TOKEN environment variable "
            "(from @BotFather)")
    return (BASE + method).replace("{}", token.strip(), 1)


def call(method: str, params: dict | None = None,
         body: dict | None = None, timeout: int = 30) -> dict:
    url = api_url(method)
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", UA)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            msg = err.get("description") or str(err)
        except Exception:
            msg = f"HTTP {exc.code}"
        raise TelegramError(f"telegram {method}: {msg}")
    except urllib.error.URLError as exc:
        raise TelegramError(f"telegram {method}: network error: {exc.reason}")
    result = json.loads(resp.read().decode("utf-8"))
    if not result.get("ok"):
        raise TelegramError(
            f"telegram {method}: {result.get('description', 'not ok')}")
    return result["result"]


def chunk(text: str):
    while len(text) > CHUNK:
        cut = text.rfind("\n", 0, CHUNK)
        if cut <= 0:
            cut = CHUNK
        yield text[:cut]
        text = text[cut:].lstrip("\n")
    yield text


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("getme")

    p_send = sub.add_parser("send")
    p_send.add_argument("--chat", required=True)
    g = p_send.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")

    p_upd = sub.add_parser("updates")
    p_upd.add_argument("--offset", type=int, default=0)
    p_upd.add_argument("--timeout", type=int, default=0)

    a = ap.parse_args()
    try:
        if a.cmd == "getme":
            print(json.dumps(call("getMe"), ensure_ascii=False))
        elif a.cmd == "send":
            text = a.text if a.text is not None else open(a.file, encoding="utf-8").read()
            sent = []
            for part in chunk(text):
                r = call("sendMessage",
                         body={"chat_id": a.chat, "text": part})
                sent.append(r["message_id"])
            print(json.dumps({"ok": True, "message_ids": sent}))
        elif a.cmd == "updates":
            ups = call("getUpdates",
                       params={"offset": a.offset, "timeout": a.timeout},
                       timeout=a.timeout + 30)
            print(json.dumps(ups, ensure_ascii=False))
    except (TelegramError, CredentialError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
