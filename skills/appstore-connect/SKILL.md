---
name: appstore-connect
description: "Use App Store Connect when working with Apple's App Store Connect API: ES256-JWT REST client for TestFlight distribution, build compliance, beta groups, testers, and external review submission."
license: MIT
compatibility: "Requires Python 3.9+ and the cryptography package (or pycryptodome); an App Store Connect API key supplied via env vars or a local .asc_config."
metadata:
  version: 1.0.0
---
# App Store Connect — Canonical Distribution Client

ES256-JWT REST client for App Store Connect. Works for any Apple Developer team — set `ASC_TEAM_ID` to yours. Drives the entire TestFlight distribution flow by API — no Mac, no Xcode GUI. (Supersedes the standalone "ASC API Client" draft; merged here.)

## Credentials
- `ASC_ISSUER_ID` (fallback `APP_STORE_CONNECT_ISSUER_ID`), `ASC_KEY_ID` (fallback `APP_STORE_CONNECT_KEY_IDENTIFIER`), `ASC_PRIVATE_KEY` (fallback `APP_STORE_CONNECT_PRIVATE_KEY` — full `.p8`, single-line OK; the client rebuilds the PEM), `ASC_TEAM_ID` (optional).
- **Config file (optional): `bin/asc.py` loads `.asc_config` (KEY=VALUE lines) from the skill root at startup if present** — copy `.asc_config.example` and fill in your Issuer ID, Key ID, Team ID, and `.p8` path. Env vars override file values. Never commit a filled `.asc_config`.
- Keep the `.p8` outside the repo (mode 600): either export the env vars or set `ASC_P8_PATH` to that file.
- Never print, log, or paste key material. Each JWT is minted fresh per call (18-min expiry, aud appstoreconnect-v1).

## Run
```
pip install cryptography --quiet   # or the pycryptodome fallback
python3 bin/asc.py <subcommand>
```

## Subcommands (door-tested live 2026-06-30)
- `whoami` · `apps [--bundle ...]` · `builds --app <id> [--limit N]` · `build-get --build <ID>`
- `set-compliance --build <ID> [--exempt false]` — PATCH usesNonExemptEncryption (clears MISSING_EXPORT_COMPLIANCE).
- `groups --app <id>` · `group-create --app <id> --name "X" [--internal]` · `group-add-build --group <GID> --build <BID>`
- `tester-add --group <GID> --email a@b.com --first F --last L` (internal testers must be ASC Users; 409 if already present).
- `set-feedback-email --app <id> --email ...` · `set-review-detail --app <id> --first F --last L --phone "+1.." --email ...` (external requirements).
- `submit-external --build <ID> --group <GID>` (external only) · `raw --method GET/PATCH --path "/v1/..." [--body '{...}']` (e.g. set betaAppLocalizations.description; read buildBetaDetail → internal/externalBuildState).

## ES256 signing
`make_jwt()` signs with `cryptography` when present, else falls back to **pycryptodome** (`Crypto.PublicKey.ECC` + `Crypto.Signature.DSS` in `fips-186-3` mode, emitting the raw r‖s 64-byte signature = exactly JWT ES256). `whoami` verifies the path (expect 200).

## Operating model (free, testing-only)
### Internal TestFlight — default, fully agent-only, NO gates
No Paid Apps Agreement, no Beta App Review, no banking. A build reaches `internalBuildState=IN_BETA_TESTING` with the beta contract still missing. Internal testers = ASC **Users** (Users & Access), up to **100**. Flow: upload → compliance (or born compliant) → `group-add-build` to internal group → testers install. Your internal group (e.g. **"Internal"**) — NOTE: group IDs are per-app, and a same-named group on another app is a different group. Always resolve the group under the target app (`/v1/betaGroups?filter[app]=<appId>`) before adding builds — a same-named group on another app silently misroutes the build.
### External / Public — only for non-ASC-user / public / >100 testers
Needs: feedback email + review contact + Beta App **description** + build in an external group + `submit-external` + the **Paid Apps Agreement ACTIVE** (Apple requires it for external even for FREE apps; activating needs **bank + tax** — a setup, not a click). Then async Apple Beta App Review. A 2026 Apple backend bug can throw BETA_CONTRACT_MISSING even when agreements are Active → Apple Developer Support case.

## Troubleshooting
- **422 BETA_CONTRACT_MISSING** → external-only gate (Paid Apps Agreement not Active, or Apple backend bug). Internal is unaffected. **On Codemagic:** `submit_to_testflight: true` creates a betaAppReviewSubmission **regardless of beta-group type** — for internal-only builds export with `testFlightInternalTestingOnly: true` in the export options so no submission is created.
- **MISSING_EXPORT_COMPLIANCE** → `set-compliance --exempt false`, or bake `INFOPLIST_KEY_ITSAppUsesNonExemptEncryption: "NO"` into the XcodeGen `project.yml` so builds are born compliant.
- **409 STATE_ERROR adding internal tester** → already in group, or email isn't an ASC User.
- **Beta App Description missing (422)** → set betaAppLocalizations.description via `raw PATCH` (external only).

## Standing human steps (one-time, never queued as ongoing work)
- Creating a NEW app record is NOT possible via API (`POST /v1/apps` → 403). Create once in the App Store Connect UI (My Apps → + → New App). The Bundle ID itself IS created automatically by Codemagic's `fetch-signing-files --create`.
- App Privacy answers — Apple ships no API for them.
