---
name: tailscale-admin
description: "Administer a Tailscale tailnet over the HTTPS API — verify auth, list devices, read/validate/set the ACL policy, and manage the Tailscale SSH rule."
license: MIT
compatibility: "Requires Python 3.9+ and a Tailscale API key (TAILSCALE_API_KEY env var)."
metadata:
  version: 1.0.0
---
# Tailscale Admin

Drives the Tailscale API (`https://api.tailscale.com/api/v2`) for tailnet administration.
HTTPS-only; works from the sandbox via the HTTPS proxy.

## Credentials

- `TAILSCALE_API_KEY` (required) — API access token (`tskey-api-...`), sent as `Authorization: Bearer`.
- `TAILSCALE_TAILNET` (optional) — tailnet name; leave as `-` to use the token owner's default tailnet.
- `TAILSCALE_AUTH_KEY` (optional) — device auth key (`tskey-auth-...`) for enrolling nodes without interactive login.

Provide them as environment variables, or through your agent platform's secret store —
never print, log, or commit them.

## Usage

- `python3 bin/ts.py verify` — confirm the token works; prints tailnet + device count.
- `python3 bin/ts.py devices` — list devices: name, hostname, 100.x addresses, OS, lastSeen, version.
- `python3 bin/ts.py acl-get` — print the current ACL policy (JSON) and its ETag. (Policy only — no secrets.)
- `python3 bin/ts.py acl-validate <file.json>` — validate a candidate policy WITHOUT applying.
- `python3 bin/ts.py acl-set <file.json> [etag]` — replace the policy; pass the ETag from acl-get as `If-Match` for safe concurrency.

## Tailscale SSH (the goal)

1. On the target device run `tailscale up --ssh` (operator step; cannot be done via API).
2. Tailscale SSH is deny-by-default — add an `ssh` rule to the ACL policy. For "reach my own
   devices" the least-config rule is:
   ```json
   "ssh": [
     { "action": "accept", "src": ["autogroup:member"], "dst": ["autogroup:self"], "users": ["autogroup:nonroot", "root"] }
   ]
   ```
   Use acl-get → merge the `ssh` block → acl-validate → acl-set (with ETag).
3. Connect from any tailnet device: `ssh <user>@<magicdns-name>` (or the 100.x address).

## Discipline

- acl-set REPLACES the whole policy — always acl-get first, merge minimally, validate, then set with the ETag. Never overwrite blind.
- Auth keys and API tokens are secrets — vault only, never chat/bus/logs.

## Provenance

Provenance: ported 2026-09 from an internal skill export. Adopt it iff the tailnet
remains in use. `bin/ts.py` is the exported script, verbatim.
