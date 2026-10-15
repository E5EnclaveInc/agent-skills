---
name: ios-ship
description: "Use ios-ship to get any app onto a registered iPhone with zero dashboard steps: Codemagic builds, signing groups, the verify_ipa.py ship gate, OTA install pages, and the programmatic App Store submission pipeline."
license: MIT
compatibility: "Requires a Codemagic account for builds and the appstore-connect skill's credentials for App Store Connect operations."
metadata:
  version: 1.0.0
---
# iOS Ship

Get any app onto a registered iPhone with **zero dashboard steps**. Set your Apple Team ID via `ASC_TEAM_ID` and your bundle-ID prefix in your Codemagic variables; examples below use `com.example.*` placeholders.

Works with a Codemagic API skill and this bundle's `appstore-connect` skill — it does not duplicate them.

**Golden rule: never hand a human an INSTALL link until `verify_ipa.py` returns GATE: PASS.**

## Credential topology (reach for these FIRST — do NOT hunt)
- **a Codemagic API client/skill** — drives builds headlessly: `apps`, `start <app_id> <workflow_id> <branch> --instance mac_mini_m2`, `build <id>`, variable groups. 500 free M2 min/mo.
- **appstore-connect skill** (this bundle) — injects `ASC_ISSUER_ID`, `ASC_KEY_ID`, `ASC_PRIVATE_KEY` (the `.p8`), `ASC_TEAM_ID`. Keep the `.p8` in your secret store (mode 600). **This is the App Store Connect API key you sign with.**
- **cloudflare skill** — publishes to the OTA mirror bucket and manages R2 CORS.
- Never print or paste any secret; never hard-code a presigned write URL in a public repo.

## The signing group (the piece that blocks a NEW app)
Codemagic variable groups are **per-app**; secure values cannot be copied app→app via API. A brand-new Codemagic app fails with `unknown variable group(s): appstore_credentials` until populated. Fix, fully agent-side:
1. Compose JSON `{CERTIFICATE_PRIVATE_KEY, APP_STORE_CONNECT_ISSUER_ID, APP_STORE_CONNECT_KEY_IDENTIFIER, APP_STORE_CONNECT_PRIVATE_KEY}` inside a credentialed run (cert from the vault, the 3 ASC values from the appstore-connect skill env). Write to a mode-0600 temp file; never print; shred after.
2. `group-setup <app_id> appstore_credentials --secure <file>` (or `rekey` to replace). The yaml's `groups: [appstore_credentials]` now resolves.

## The gate — bin/verify_ipa.py (mandatory before any human install)
Downloads/opens the IPA and PROVES: bundle id, team, get-task-allow false, **target device in the provisioning profile**, manifest version == IPA version (fix the mirror manifest if not — a mismatch = "unable to install"), and for Capacitor apps web hygiene (no absolute vendor refs, importmap vendored, vendor files present). Exit 0 = ship.

## OTA install page — bin/ota_kit.py
Generates `manifest.plist` (itms-services) + a branded self-arming `install.html` (checks the IPA HEAD, only shows INSTALL once the package exists). Publish both to the mirror BEFORE the build; the link goes hot by itself. On device: Safari → INSTALL → trust your developer profile under Settings → General → VPN & Device Management.

## bin/presign_put.py
Presigned-write helper for publishing build artifacts to the mirror without leaking credentials.

## The autonomous loop, once provisioned (≈4 min/build, zero human steps)
edit web/source → publish to mirror (or git push) → `codemagic start` → watch build → `verify_ipa.py` GATE PASS → hand the user the (unchanging) install link.

## Capacitor web hygiene (boot-stall lessons)
For Capacitor web apps, absolute asset paths **cannot resolve on the `capacitor://` scheme** — they 404 silently and the ES-module chain dies before boot. Rewrite EVERY vendor-path family (CDN and mirror paths) to bundle-relative `./vendor/...`, then **hard-assert** no absolute ref survives. Bundle the whole render stack (three.js module + GLTF/DRACO/KTX2 loaders + wasm) — a missing transitive loader dep also stalls boot. See `references/fetch_assets.ref.sh`, `references/patch_ios.ref.sh`.
An app whose origin differs from the asset host needs **CORS on the R2 bucket** (`PUT /accounts/{acct}/r2/buckets/{bucket}/cors`).

## App Store submission pipeline (proven end-to-end)
1. Confirm the ASC route: `asc.py whoami` (via the appstore-connect skill).
2. App record + bundle id exist. Find/reuse an editable appStoreVersion in PREPARE_FOR_SUBMISSION.
3. Set metadata (name, description, keywords, screenshots), export compliance, build → attach to version.
4. `submit-external` for external review / internal groups for TestFlight-only.
5. Watch the build state to a verdict.

**One human dashboard touch remains: App Privacy** — Apple ships no API for it (verified against Apple's live OpenAPI spec). App record creation is also UI-only (`POST /v1/apps` returns 403; create once in App Store Connect UI). Both are standing one-time steps, never queued as ongoing work.

## Defect log (so the maze is never re-walked)
- Boot stall, empty log → absolute vendor paths → rewrite + hard-assert.
- "Unable to install" → IPA hadn't reached the mirror OR manifest version ≠ IPA version → the gate catches both.
- 403 on r2.dev fetches → send a real User-Agent (Python-urllib is blocked); general rule for all ship tooling.
- Monotonic `CFBundleVersion` (`date +%y%m%d%H%M`) so every OTA reinstall is a clean upgrade.
- `submit_to_testflight: true` in Codemagic creates a betaAppReviewSubmission regardless of group type — for internal-only, export with `testFlightInternalTestingOnly: true`.

## Two one-time human gates (then fully agent-driven)
- GitHub Actions billing for private macOS minutes (only if using the GitHub-Actions/fastlane path).
- The app record (created once in the App Store Connect UI).
