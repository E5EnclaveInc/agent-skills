# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
