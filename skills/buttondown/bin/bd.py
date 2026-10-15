#!/usr/bin/env python3
"""Buttondown API v1 CLI using the BUTTONDOWN_API_KEY environment variable.

The credential is never printed, logged, or persisted; it is read from
the environment and sent as `Authorization: Token <key>` (Buttondown's
required scheme).

Commands:
    verify                                   Verify the API key (GET /v1/emails)
    config                                   Print newsletter settings
    drafts [--limit N]                       List draft emails
    emails [--status draft|scheduled|sent]    List emails (default: draft)
    get-email <id>                           Fetch one email (metadata only)
    create-draft --file FILE [--subject S]   Create a draft from a Markdown file
    subscribers [--type TYPE]                List subscribers (paginated)
    export-subscribers --out FILE.csv        Export all subscribers to CSV
    import-subscribers --in FILE.csv [--type regular] [--tags a,b]
                                             Import subscribers from CSV

Prints JSON to stdout; exits non-zero with the provider's error message on
failure. Sending is deliberately not wired in — drafts only.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.buttondown.com"
ALLOWED_HOSTS = {"api.buttondown.com"}

# Draft files often carry YAML frontmatter; the API rejects bodies that
# start with `---` unless X-Buttondown-Live-Dangerously is set. Strip it.
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


class CredentialError(RuntimeError):
    """The BUTTONDOWN_API_KEY environment variable is not set."""


class ButtondownError(RuntimeError):
    """Raised for provider-side failures when exit_on_error is False."""


def auth_header() -> dict:
    """Return the Authorization header, built from the environment key."""
    key = os.environ.get("BUTTONDOWN_API_KEY")
    if not key:
        raise CredentialError(
            "set the BUTTONDOWN_API_KEY environment variable")
    return {"Authorization": f"Token {key}"}


def _request_url(method: str, url: str, body: dict | None = None,
                 exit_on_error: bool = True) -> dict:
    host = urllib.parse.urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise ButtondownError(f"refusing to call non-Buttondown host: {host}")
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method.upper())
    req.add_header("Accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    for k, v in auth_header().items():
        req.add_header(k, v)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as exc:
        try:
            err = json.loads(exc.read().decode("utf-8", "replace"))
            msg = err.get("detail") or err.get("message") or str(err)
        except Exception:
            msg = f"HTTP {exc.code}"
        if exit_on_error:
            print(f"buttondown error: {msg}", file=sys.stderr)
            sys.exit(1)
        raise ButtondownError(msg)
    return json.loads(resp.read().decode("utf-8"))


def request(method: str, path: str, params: dict | None = None,
            body: dict | None = None, exit_on_error: bool = True) -> dict:
    url = API + path
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    return _request_url(method, url, body, exit_on_error=exit_on_error)


def paged(path: str, params: dict | None = None):
    """Yield items across DRF-style paginated results."""
    url = API + path
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    while True:
        payload = _request_url("GET", url)
        for item in payload.get("results", []):
            yield item
        url = payload.get("next")
        if not url:
            return


def cmd_verify(_):
    # Buttondown's API v1 has no /config endpoint; a cheap emails list
    # proves the key works (401 here means the key is dead).
    payload = request("GET", "/v1/emails", params={"page_size": 1})
    print(json.dumps({
        "ok": True,
        "total_emails": payload.get("count"),
    }, indent=2))


def cmd_config(_):
    # No settings endpoint exists in API v1; name, description, and custom
    # domain are managed in the Buttondown dashboard.
    print(json.dumps({
        "note": "Buttondown's API v1 exposes no settings endpoint. "
                "Newsletter name, description, and custom domain are "
                "read-only here and managed in the Buttondown dashboard.",
    }, indent=2))


def cmd_drafts(args):
    payload = request("GET", "/v1/emails",
                      params={"status": "draft", "ordering": "-creation_date"})
    rows = [{"id": e["id"], "subject": e.get("subject"),
             "created": e.get("creation_date")}
            for e in payload.get("results", [])[: args.limit]]
    print(json.dumps(rows, indent=2))


def cmd_emails(args):
    params = {"ordering": "-creation_date"}
    if args.status:
        params["status"] = args.status
    payload = request("GET", "/v1/emails", params=params)
    rows = [{"id": e["id"], "subject": e.get("subject"),
             "status": e.get("status"), "created": e.get("creation_date")}
            for e in payload.get("results", [])]
    print(json.dumps(rows, indent=2))


def cmd_get_email(args):
    email = request("GET", f"/v1/emails/{args.id}")
    email.pop("body", None)  # metadata only; fetch body only when needed
    print(json.dumps(email, indent=2))


def load_markdown(path: str) -> tuple[str | None, str]:
    text = open(path, encoding="utf-8").read()
    m = FRONTMATTER_RE.match(text)
    subject = None
    if m:
        fm = m.group(1)
        for key in ("subject", "title"):
            fm_m = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", fm)
            if fm_m:
                subject = fm_m.group(1).strip().strip("\"'")
                break
        text = text[m.end():]
    if not subject:
        # Fallback convention: a "**Recommended subject line:** <subject>"
        # line in the body.
        subj_m = re.search(r"\*\*Recommended subject line:\*\*\s*(.+?)\s*$",
                           text, re.MULTILINE)
        if subj_m:
            subject = subj_m.group(1).strip().strip("\"'")
    return subject, text.strip()


def cmd_create_draft(args):
    fm_subject, body = load_markdown(args.file)
    subject = args.subject or fm_subject
    if not subject:
        print("create-draft: need --subject or a subject/title in frontmatter",
              file=sys.stderr)
        sys.exit(2)
    if not body:
        print("create-draft: empty body after frontmatter strip",
              file=sys.stderr)
        sys.exit(2)
    email = request("POST", "/v1/emails", body={
        "subject": subject,
        "body": body,
        "status": "draft",
    })
    print(json.dumps({"id": email["id"], "subject": email.get("subject"),
                      "status": email.get("status")}, indent=2))


def cmd_subscribers(args):
    params = {}
    if args.type:
        params["type"] = args.type
    out = []
    for s in paged("/v1/subscribers", params):
        out.append({"id": s["id"], "email_address": s.get("email_address"),
                    "type": s.get("type"),
                    "creation_date": s.get("creation_date"),
                    "tags": [t.get("name") for t in s.get("tags", [])]})
        if len(out) >= args.limit:
            break
    print(json.dumps(out, indent=2))


def cmd_export_subscribers(args):
    count = 0
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "email_address", "type", "creation_date", "tags"])
        for s in paged("/v1/subscribers", {"ordering": "creation_date"}):
            w.writerow([s["id"], s.get("email_address"), s.get("type"),
                        s.get("creation_date"),
                        ";".join(t.get("name", "") for t in s.get("tags", []))])
            count += 1
    print(json.dumps({"exported": count, "file": args.out}, indent=2))


def cmd_import_subscribers(args):
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    created, skipped, errors = 0, 0, []
    with open(args.infile, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        cols = {c.lower(): c for c in (reader.fieldnames or [])}
        email_col = cols.get("email") or cols.get("email_address")
        if not email_col:
            print("import-subscribers: CSV needs an 'email' column",
                  file=sys.stderr)
            sys.exit(2)
        for row in reader:
            addr = (row.get(email_col) or "").strip()
            if not addr:
                skipped += 1
                continue
            payload = {"email_address": addr, "type": args.type}
            if tags:
                payload["tags"] = tags
            try:
                request("POST", "/v1/subscribers", body=payload,
                        exit_on_error=False)
                created += 1
            except ButtondownError as exc:
                errors.append({"email": addr, "error": str(exc)})
            time.sleep(0.2)
    print(json.dumps({"created": created, "skipped": skipped,
                      "errors": errors}, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser(prog="bd.py")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    sub.add_parser("config").set_defaults(fn=cmd_config)

    p = sub.add_parser("drafts")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(fn=cmd_drafts)

    p = sub.add_parser("emails")
    p.add_argument("--status", default=None,
                   choices=["draft", "scheduled", "sending", "sent"])
    p.set_defaults(fn=cmd_emails)

    p = sub.add_parser("get-email")
    p.add_argument("id")
    p.set_defaults(fn=cmd_get_email)

    p = sub.add_parser("create-draft")
    p.add_argument("--file", required=True, help="Markdown file for the body")
    p.add_argument("--subject", default=None)
    p.set_defaults(fn=cmd_create_draft)

    p = sub.add_parser("subscribers")
    p.add_argument("--type", default=None)
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(fn=cmd_subscribers)

    p = sub.add_parser("export-subscribers")
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_export_subscribers)

    p = sub.add_parser("import-subscribers")
    p.add_argument("--in", dest="infile", required=True)
    p.add_argument("--type", default="regular",
                   help="'regular' skips double opt-in for imports")
    p.add_argument("--tags", default="")
    p.set_defaults(fn=cmd_import_subscribers)

    args = ap.parse_args()
    try:
        args.fn(args)
    except CredentialError as exc:
        print(f"credential error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
