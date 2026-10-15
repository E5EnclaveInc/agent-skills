---
name: public-export
description: "Export internal agent skills to a public repository without leaking anything and without breaking CI: forensic inventory first, identifier scrub battery, spec conformance, skills-ref validation, credential generalization to environment variables, single-commit pushes through the Git data API, CI-green verification after every push, and directory/discovery submissions. Use whenever publishing, open-sourcing, or updating a public skills/code repo from private sources."
license: MIT
metadata:
  version: 1.0.0
---

# Public export — shipping private skills to a public repo

Born 2026-10-15, from a production public launch (two waves, 62 skills) and its failures. The failures are the curriculum: an EIN found verbatim in private files at audit time, a real Cloudflare account ID riding in a production source, an authoring template registering as an installable skill, a CI workflow that failed on every push for a licensing reason nobody saw because nobody checked Actions, and a per-file push pattern that turned that failure into ~200 phone notifications.

## The pipeline (in order — no step skips)

1. **Forensic inventory before touching anything.** Index the full corpus (every tree the material lives in), dedupe by content, count licenses. Classify each item: original / adapted (attribution travels in the file) / vendored third-party (never launches under our name) / hold. The decision list for the human is short and explicit; everything else moves.
2. **Stage fresh, never edit production.** Build the export tree from scrubbed copies in a staging directory. Production sources stay untouched unless the human rules on a production-side scrub separately.
3. **Scrub in the export, with a named-scrub list.** Generic patterns are not enough: keep a per-skill list of the specific identifiers known to live in that source (account IDs, example entities, real addresses, internal hostnames, path prefixes, credential-plumbing imports) and verify each one is gone or parameterized.
4. **Credential generalization.** Anything that read fleet/private credential plumbing is rewritten to documented environment variables (`<SERVICE>_API_KEY` etc.), with a per-skill setup table in the SKILL.md. If a source calls an endpoint that cannot be verified against current public docs, remove the unverifiable part rather than shipping a guess.
5. **Conform + validate.** SKILL.md frontmatter to the agentskills.io spec (name matches directory, description ≤1024 chars and says what + when). Validate EVERY skill with skills-ref; zero failures is the gate, not a sample.
6. **Identifier battery on the full staged tree.** Grep for: tax IDs, phone numbers, entity identifiers (UEI/CAGE), internal domains and hostnames, home-directory paths, private package names, key shapes, session/credential markers, and the principal's public handles (which never appear — the institution is the only voice). Zero hits is the gate. Verify any remaining hit by reading it (formatting strings and detector examples are not leaks; document them in SECURITY.md).
7. **Repo skeleton.** Install-first README with a generated skill index (script generates it — never hand-maintain the table), CHANGELOG, CONTRIBUTING, SECURITY.md, license, marketplace/plugin manifest if the ecosystem has one, CI (validation + secret scan).
8. **Push as ONE commit.** Use the Git data API (blobs → tree → commit → ref update) or a real git push. NEVER push file-by-file through the Contents API: every commit fires CI, and N files = N runs = N notifications. Blobs are content-addressed, so re-running a sync is idempotent and resumes after network drops; add retry-with-backoff around every API call (sandbox egress drops connections under load).
9. **Verify CI green — actually look.** After the push, read the Actions runs for the new HEAD and confirm success before reporting anything. A pushed tree is not a shipped tree. (Wave 1 verified contents and missed that every CI run had failed.)
10. **Verify the consumer path.** Fresh scratch install with the ecosystem's installer (`npx skills add <owner>/<repo> -s '*' -a '*' -y`): count what lands, confirm non-skills (templates!) are not detected as skills. A `template/SKILL.md` WILL be discovered as a skill by directory scanners — name templates `skill-template.md`, never `SKILL.md`, outside `skills/`.
11. **Discovery submissions.** File the index request with the ecosystem directory (skills.sh indexes GitHub repos automatically — the badge resolves once the repo is public; a real install seeds their audit). Submit to the curated lists (VoltAgent, Composio) following each repo's own contribution format exactly. Public text is institutional voice only.
12. **Release.** Tag + GitHub release with notes from the CHANGELOG once CI is green and the install test passes.

## CI secret-scan doctrine

- **The gitleaks GitHub Action (gitleaks/gitleaks-action@v2) now requires a paid GITLEAKS_LICENSE for organization-owned repos and hard-fails without one** — the run dies before scanning, which looks identical to a leak failure in notifications. Run the gitleaks CLI directly in the workflow (install the release binary, `gitleaks detect --source . --redact`) — same scanner, no license gate. Trufflehog's action has no such gate.
- **False positives are handled with a scoped `.gitleaks.toml` allowlist** (rule + path, with a comment saying why) — never by disabling the scan, and never by mangling readable code. Formatting constants (e.g. PEM header strings in key-formatting code) are the classic case.
- Reproduce CI failures locally with the same tool/version before changing anything: the log is the ground truth (Actions job logs via the API — the logs endpoint redirects to a signed URL; fetch it WITHOUT forwarding the auth header).

## Hard rules

- Zero-hit battery and 100% validation before any push. No exceptions for "just docs."
- One commit per wave. If a push script dies mid-run, check remote state before rerunning; blob/tree syncs are idempotent, per-file pushes are not resumable.
- Attribution for adapted work travels in the file (`adapted-from`), prominently. Vendored third-party work does not ship under our name at all.
- Held items stay held on their stated condition (authorship unconfirmed, decision pending) — a wave shipping is not implied consent to include them.
