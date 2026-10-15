# Buttondown API notes

Base URL: `https://api.buttondown.com`. Auth on every request:
`Authorization: Token <api_key>`. Key found in the Buttondown dashboard under
Settings → API. Pagination on list endpoints is DRF-style:
`{count, next, previous, results}` — follow `next`.

## Emails
- `POST /v1/emails` — create. Body fields: `subject`, `body`, `status`
  (`draft` default; never set `sending`/`sent` from automation).
  The API auto-detects Markdown; prefix the body with
  `<!-- buttondown-editor-mode: plaintext -->` or `<!-- buttondown-editor-mode: fancy -->`
  to force a mode. Bodies starting with YAML frontmatter (`---`) are rejected
  unless the `X-Buttondown-Live-Dangerously: true` header is set — strip
  frontmatter instead.
- `GET /v1/emails?status=draft|scheduled|sending|sent` — list, `ordering=-creation_date`.
- `GET /v1/emails/{id}`, `PATCH /v1/emails/{id}` (update subject/body,
  schedule via `scheduled_for` + `status: scheduled`), `DELETE /v1/emails/{id}`.
- Sending is `POST /v1/emails/{id}/send-draft` — deliberately not wired into
  `bd.py`; sending stays a human click.

## Config (settings)
- `GET /v1/config` — read-only. Newsletter name, username, description,
  timezone, custom domain. There is no documented v1 write endpoint; changes
  go through the dashboard (Settings → Newsletter / Domains).

## Subscribers
- `GET /v1/subscribers` — params: `type`, `tag`, `ordering`.
- `POST /v1/subscribers` — `{email_address, type, tags[], metadata{}, notes}`.
  `type: "regular"` skips double opt-in (use only for consented lists).
- `GET|PATCH|DELETE /v1/subscribers/{id_or_email}`.
- No native bulk CSV export/import endpoints in v1: `export-subscribers`
  paginates the list into CSV; `import-subscribers` POSTs one row at a time
  (~0.2s apart) and reports created/skipped/errors.

## Limits (as of last check)
Free tier covers up to 100 subscribers; custom sending domain is included on
the free plan; the API is available on free accounts. Verify current pricing
at buttondown.com if it matters for a decision.
