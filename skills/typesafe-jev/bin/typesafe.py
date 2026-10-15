#!/usr/bin/env python3
"""Thin CLI over jev_client. Never prints credentials."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jev_client import ask_systemone, list_models  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("models", help="GET /v1/models (auth check, no spend)")

    ask = sub.add_parser("ask", help="POST /v1/systemone")
    ask.add_argument("--state-file", required=True)
    ask.add_argument("--questions-file", required=True)
    ask.add_argument("--model", default="jev-latest")
    ask.add_argument("--dry-run", action="store_true",
                     help="print request body; make no call")

    args = ap.parse_args()
    if args.cmd == "models":
        print(json.dumps(list_models(), indent=2))
        return
    state = Path(args.state_file).read_text(encoding="utf-8")
    questions = json.loads(Path(args.questions_file).read_text(encoding="utf-8"))
    body = {"state": state, "model": args.model, "questions": questions}
    if args.dry_run:
        print(json.dumps(body, indent=2, ensure_ascii=False))
        return
    print(json.dumps(ask_systemone(state, questions, args.model),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
