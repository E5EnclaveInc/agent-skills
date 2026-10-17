# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-10-17

### Added

- **`first-orchestration`** (112 total) — the designated first skill for
  newcomers adopting this library: a one-time onboarding sequence that runs
  a forensic review of the imported library (Adopt / Adapt / Park), convenes
  a war room to charter the agent as chief of staff, performs read-only
  email/calendar recon plus fresh world recon (unknown unknowns included),
  and stands up SMART goals with the standing `chief-of-staff` routine.
  Agent-only and accessibility-first by design: one question at a time,
  one-word answers, digest-first reporting, money/sends/publishing staged
  for approval.

## [0.3.0] - 2026-10-15

### Added

- **Wave 3 — 49 new skills (111 total).**
  - Scenario suite (10): `scenario`, `scenario-consistency`,
    `scenario-identity-library`, `scenario-model-training`,
    `scenario-quality-gate`, `scenario-refine-loop`, `scenario-storyboards`,
    `scenario-text-overlay`, `scenario-video-ads`, `scenario-video-assembly` —
    the full Scenario MCP creative pipeline: generation, consistency,
    identities, model training, quality gates, refinement, storyboards,
    text overlay, video ads, and assembly.
  - Creative & design: `design-second-brain`, `sawdust-cinematic`,
    `ebony-video`, `anatomy` (interactive isometric SVG explainers).
  - Operations & analytics: `fleet-atlas`, `google-analytics`,
    `job-application-filing` (method only — ships with a blank
    canonical-answers template).
  - Newly authored: `scheduled-job-discipline`, `grant-ops`,
    `eval-battery`, `secret-sweep`, `public-export`.
  - **Adapted engineering set (27)** — `ask`, `code-review`,
    `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grill-me`,
    `grill-with-docs`, `grilling`, `handoff`, `implement`, `implement-spec`,
    `improve-codebase-architecture`, `pr`, `prototype`, `research`, `retro`,
    `setup`, `tdd`, `teach`, `to-questionnaire`, `to-spec`, `to-tickets`,
    `triage`, `wait-what`, `wayfinder`, `wizard`, `writing-for-agents`.
    Adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
    (MIT) — upstream is canonical; each skill carries its attribution and the
    upstream license. See `skills/<name>/LICENSE`.

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
