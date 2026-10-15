# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-15

### Added

- **Wave 2 — 48 new skills (62 total).**
  - Connector set (19): `cloudflare`, `codemagic`, `contrado`, `elevenlabs`,
    `fred`, `github`, `google-ads`, `groq`, `huggingface`, `nvidia`, `prodigi`,
    `buttondown`, `raisely`, `sam-gov`, `simpler-grants-gov`, `stripe`,
    `telegram-bot`, `zeffy`, `zenodo`. Every connector skill reads its
    credential from a documented environment variable — no vault or
    fleet-specific plumbing required.
  - Agent operations: `fleet-doctrine`, `board-of-thirteen`, `writers-war-room`
  - Research & verification: `demand-mining`, `submission-gate`, `paper-foundry`,
    `context7`, `web-fetch`, `phoenix`, `rea`
  - Engineering systems: `eng-discipline`, `prototype-sprint`, `browser-skill`,
    `blender`, `lambda-cloud`, `ontology-floor`
  - Business & growth: `brand-sprint`, `city-map-strategy`, `income-blueprint`,
    `media-company-marketing`, `packaging-lab`, `revenue-wedge`, `minerva`,
    `typesafe-jev`
  - Creative & media: `creative-production` (merges the former creative-studio
    material into one skill), `atelier-character-sheet`, `cinematic-letter-video`,
    `living-mesh-cinematic`, `signal-lab-cinematic`

### Changed

- The skill template moved from `template/SKILL.md` to
  `template/skill-template.md` so installers no longer discover it as an
  installable skill; copy it to `skills/<your-skill>/SKILL.md` to start a
  new skill.
- Marketplace manifest now carries the full 62-skill set in the
  `production-skills` plugin.

## [0.1.0] - 2026-10-15

### Added

- Initial public release: 14 production skills, scrubbed for publication.
  - Agent operations: `subagent-security-brief`, `chief-of-staff`, `agent-spawner`, `war-room`, `war-room-doctrine`
  - Research & verification: `storm-research`, `crucible`, `entity-verification`
  - Engineering systems: `sprint-engine`, `tailscale-admin`
  - Shipping & media: `ios-ship`, `appstore-connect`, `video-learn`, `voice-dna`
- Repo skeleton: README with generated skills index (`scripts/generate-index.py` +
  `skills_index.json`), Claude plugin marketplace manifest, skill template,
  authoring standard in CONTRIBUTING.md, and security policy in SECURITY.md.
- CI: skills-ref validation + index-drift check on skill PRs; gitleaks and
  trufflehog secret scanning on push and pull requests.
