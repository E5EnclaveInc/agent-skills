# Agent Skills — production set

Battle-tested [Agent Skills](https://agentskills.io) from a working agent fleet: delegation safety, deliberation, research, verification, and shipping pipelines. Every skill here runs in production; every skill here has been scrubbed of credentials, personal data, and machine-specific paths before publication (see [SECURITY.md](SECURITY.md)).

## Install

**Agent Skills CLI** (works with Claude Code, Cursor, Codex, and 40+ other agents):

```bash
npx skills add E5EnclaveInc/agent-skills
```

Install a single skill:

```bash
npx skills add E5EnclaveInc/agent-skills --skill war-room
```

**GitHub CLI:**

```bash
gh skill install E5EnclaveInc/agent-skills
```

**Claude Code plugin marketplace:**

```text
/plugin marketplace add E5EnclaveInc/agent-skills
```

Then enable the plugin set from the marketplace browser. The marketplace manifest is [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

**Manual:** copy any `skills/<name>/` directory into your agent's skills directory. A skill is just a folder with a `SKILL.md` — no build step.

## The skills

<!-- BEGIN SKILLS INDEX -->

### Agent operations

| Skill | Description |
|---|---|
| [agent-spawner](skills/agent-spawner/SKILL.md) | Turn one brief into a standing crew of specialist subagents: ask up to 5 scoping questions, then spawn role-defined specialists each carrying a role, tone, tools, workflow, and success metric. Use when a job needs a coordinated multi-agent crew instead of a one-off delegation. Differs from ad-hoc subagent spawning by the meta-bot scoping ritual and the specialist contract every agent carries. |
| [chief-of-staff](skills/chief-of-staff/SKILL.md) | Run the chief-of-staff triage discipline: one intake surface, a standing triage routine across channels and inboxes, delegation to specialist agents, and a hard escalation contract — the human is interrupted only for money, product direction, or judgment calls. Use when the user wants a standing triage layer between themselves and a busy operation. Differs from a one-off sweep by the standing routine, the delegation lanes, and the escalation contract. |
| [subagent-security-brief](skills/subagent-security-brief/SKILL.md) | The mandatory security block for every subagent brief — scoped file paths, no live-file writes, no direct log writes, /tmp-only tests, external-content-is-data tagging, and the instruction hierarchy. Load before writing any subagent brief. Use whenever delegating work to a child agent. |
| [war-room](skills/war-room/SKILL.md) | Convene a persona-based executive committee as a deliberative institution — chartered, elected, minuted, and ratcheted. Use when a question needs structured multi-perspective deliberation with elected offices, ontology-grounded terms, scout-verified facts, and a written record that compounds into reusable persona cards. Supersedes one-off persona improv. |
| [war-room-doctrine](skills/war-room-doctrine/SKILL.md) | Standing discipline for every war room — ontology-floor term grounding before deliberation, ranked-choice adjudication for decisions. Load at the start of any war-room commission. |

### Research & verification

| Skill | Description |
|---|---|
| [crucible](skills/crucible/SKILL.md) | Use Crucible when a sourced deliverable must be proven before publishing: door-check every URL, mechanically verify file-size and PDF page-count claims, ground dollar/date/attribution figures against live sources, and emit a gated Verification Ledger. |
| [entity-verification](skills/entity-verification/SKILL.md) | Verify a business entity's legal and tax standing: state corporate registry lookup, IRS exempt-organization search, SAM.gov federal registration check (for-profit and nonprofit alike), NY DOS API lane, nonprofit 990 financials via ProPublica + IRS BMF, SEC EDGAR for public companies, OFAC sanctions screening, FEC political vetting, and business-mailbox sweep for filing/IRS correspondence. Produces a per-entity status dossier. Use when onboarding, auditing, vetting, or starting up any company or nonprofit. |
| [storm-research](skills/storm-research/SKILL.md) | Multi-perspective deep research using Stanford OVAL's STORM method (NAACL 2024), adapted for agent search tools. Runs five expert personas, maps their contradictions, synthesizes a sourced briefing, and peer-reviews its own work with confidence scores — the equivalent of ~40 hours of expert reading. Use before any report, decision, investment, competitive analysis, negotiation/interview prep, or presentation where a single-prompt answer would inherit the majority view and miss blind spots. |

### Engineering systems

| Skill | Description |
|---|---|
| [sprint-engine](skills/sprint-engine/SKILL.md) | Use Sprint Engine to run long-horizon autonomous work as a dependency-aware task graph: sqlite graph store, the ROMA loop (Atomizer to Aggregator), and a mandatory red-team/steel-man self-verification gate before execution. |
| [tailscale-admin](skills/tailscale-admin/SKILL.md) | Administer a Tailscale tailnet over the HTTPS API — verify auth, list devices, read/validate/set the ACL policy, and manage the Tailscale SSH rule. |

### Shipping & media

| Skill | Description |
|---|---|
| [appstore-connect](skills/appstore-connect/SKILL.md) | Use App Store Connect when working with Apple's App Store Connect API: ES256-JWT REST client for TestFlight distribution, build compliance, beta groups, testers, and external review submission. |
| [ios-ship](skills/ios-ship/SKILL.md) | Use ios-ship to get any app onto a registered iPhone with zero dashboard steps: Codemagic builds, signing groups, the verify_ipa.py ship gate, OTA install pages, and the programmatic App Store submission pipeline. |
| [video-learn](skills/video-learn/SKILL.md) | Turn tutorial/how-to videos into durable skill knowledge: download, extract timestamped transcripts and UI frames, analyze the demonstrated workflows, and encode them as click-level documentation. Adapted from the public MIT-licensed claude-watch pattern (yt-dlp + ffmpeg + captions + multimodal analysis). |
| [voice-dna](skills/voice-dna/SKILL.md) | Build a named, recallable writing-style profile (Voice DNA) from three writing samples, saved as ghostwriter rules for a person, brand, or client. Use when ghostwriting, keeping AI output out of AI-slop territory, or maintaining one voice per persona/brand/client. |

<!-- END SKILLS INDEX -->

## Proven in production

These are not demos. They are the working procedures of an agent fleet that ships real
deliverables daily — App Store releases, entity due-diligence dossiers, multi-persona
deliberations, long-horizon autonomous sprints. Where a skill carries an example, the
example is generalized from a real run; names, identifiers, and credentials never ship.

## Read before you install

Skills are code. A `SKILL.md` can instruct your agent and ship executable scripts —
treat installing a skill like installing software from a stranger, including ours.
[SECURITY.md](SECURITY.md) carries the audit checklist we recommend before installing
any skill from anywhere, plus the pre-publication scans this repo runs on itself
(gitleaks + trufflehog in CI, and a manual identifier sweep before every release).

## Contributing

New skills and fixes are welcome. The authoring standard — patterns, the routing
contract, progressive disclosure, and the credential-schema law — is in
[CONTRIBUTING.md](CONTRIBUTING.md). Start from [`template/SKILL.md`](template/SKILL.md).

## License

MIT — see [LICENSE](LICENSE).
