# Security Policy

## Reporting a vulnerability

Email **security@e5enclave.com** with the skill name, the file and line, and what
you found. Please do not open a public issue for a suspected credential or personal
data exposure. We aim to acknowledge within two business days.

## Before you install any skill (ours included)

Skills are code: a `SKILL.md` instructs your agent, and `bin/` scripts execute with
your agent's permissions. Audit before installing:

1. **Read the whole `SKILL.md`.** Look for instructions that reach outside the
   skill's stated job — exfiltration, persistence, or "ignore previous instructions"
   aimed at your agent.
2. **Read every script in `bin/` and any referenced files.** Check network calls
   (where do they go?), file access (what paths?), and shell invocations.
3. **Check how credentials are handled.** Secrets must arrive via environment
   variables or your platform's credential store — never literals in code or docs,
   never CLI arguments that land in logs. If a skill asks you to paste a key into a
   file inside the repo, stop.
4. **Pin what you install.** Install from a commit or release tag you audited, not
   a moving branch.
5. **Run it least-privilege first.** Give a new skill the smallest workspace and
   credential scope that lets it do its job; widen only on evidence.

## How this repo audits itself

- **CI secret scanning:** gitleaks and trufflehog run over the worktree and git
  history on every push and pull request (`.github/workflows/security-scan.yml`).
- **Pre-publication scrub:** before this release, every skill passed a manual
  identifier sweep — personal names, phone numbers, email addresses, tax IDs,
  account/team IDs, bundle identifiers, absolute home paths, and key-shaped
  strings — plus a file-by-file read of everything under `skills/`.
- **No live credentials ship.** Configuration examples use placeholders; real
  values belong in your environment or secret store.

## Known false positives

- **`skills/appstore-connect/bin/asc.py`** contains PEM *formatting* code — the
  literal `-----BEGIN PRIVATE KEY-----` / `-----END PRIVATE KEY-----` marker
  strings used to wrap a key loaded from the environment or a local file at
  runtime. There is no key material in the file; secret scanners flag the markers.
- **`skills/entity-verification/bin/lanes/fec.py`** mentions the FEC API's public
  `DEMO_KEY` placeholder in its design notes. It is the API provider's published
  demo credential, not a real key.
