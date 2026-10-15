# Scout recon — facts are verified, never voted on

Every deliberation seats the **standing Recon Subcommittee** before debate opens. A war room without recon is untrusted; a war room that deliberates on stale premises is out of order.

## Standing sub-charter

The subcommittee exists for one reason: the committee must have the latest information to make the best judgment. This is not about the status quo. The members were chosen to always fully understand 100% of the state of the art — so the institution can always move zero to one.

- **Seated automatically** at every convening (bylaws Art. VI §4); no formation vote. It fans out scout agents as needed; scouts measure, they do not deliberate or vote.
- **Reports before deliberation opens** (order of business step 4). No seat argues until the brief is delivered.
- **The brief covers:** what is newest (roughly the last 90 days), what shipped vs what is proposal or marketing, what the field doesn't know, and where the status quo is wrong. Every brief ends with the zero-to-one question: *what would we do differently if we started today?*
- **Premise check:** if the brief finds the committee's premises predate the state of the art, the premises are updated first — deliberation on stale premises is out of order. A corrected premise that dominates a prior verdict takes an **amendment**, not a re-vote.
- **The Computer holds the standing verification function** over the subcommittee's numbers: the convener's counts are re-derived, not trusted.

## Commissioning

1. At the order of business, the committee charters scout work: the market/empirical facts the decision turns on, checked against **live sources** (official docs, primary texts, repos, registries, measured runs) — never from the model's memory, never by vote.
2. Scouts report: VERIFIED (primary source cited) vs. F-FLAGGED (unverifiable — named in the record, not buried).
3. **F-flag rule:** an unverified load-bearing fact is named explicitly with who must close it and how. A ruling that depends on an F-flagged fact says so on its face.
4. **Dead-lane rule:** when a recon scout lane dies mid-session (infra restart, no findings, no file), the convener re-dispatches with identical briefs; the committee does not deliberate on partial recon and does not treat the dead lane as a negative result — a lane that never reported is not an absence finding. (Precedent: 2026-10-06 video-product session — 4/4 lanes lost, 4/4 re-dispatched, full brief delivered.)

## Evidence provenance

- The record states what was examined and in what form. **Screenshot-as-source is unfit for audit** (precedent: the 2026-09-26 committee transcribed 628 entries from pixels, dropped two, caught them on re-read — and ruled the registry must never be audited from pixels again).
- Transcriptions and counts are checkable work: an independent pass verifies the convener's numbers before rulings cite them.
- **Read the subject's own Open ledger first.** A system's self-declared risks and honest ledgers are standard scout reading — they produced the 2026-09-26 classifier-upstream-of-gates finding, the session's expander contribution. Scout for what the builders admit before hunting what they hide.
- **Diff vendored copies against live sources as standard.** A "no conflict" finding still passes the Razor: a 2026-09-26 system review found the vendored floor stale (2026-07-20 snapshot; text narrating code it doesn't have) only because the byte-diff was demanded.
- **Licenses are identified from the LICENSE file, never the badge.** Precedent: 2026-09-26, Unsloth's badge read Apache-2.0 while the LICENSE file split `unsloth/`/`tests/`/`scripts/` = Apache-2.0 vs `studio/`/`unsloth_cli/` = AGPLv3 — the file wins, and anything AGPL-tainted stays out until resolved.
- Scout reports are filed (e.g. `/tmp/<lane>.md`) and cited in the record as evidence provenance — the record never floats a number the scout file doesn't carry.

## What scouts don't do

Scouts don't deliberate and don't vote. They return evidence with provenance. The committee judges; the scouts measure. When a corrected fact dominates a prior verdict, the record takes an **amendment**, not a re-vote.

## Negative results are deliverables

An audit that finds the subject absent is a complete result, not a failed probe. Zero-collisions, zero-keys, and subject-not-in-store are findings with receipts — the committee rules on the absence (suspend, re-point, re-stage) rather than treating the probe as inconclusive. (Precedent: 2026-09-26 execution — the A1 audit's headline was the cache's absence from all three remote stores; five amendments suspended on it.)

## Credential-path provenance

When a skill offers more than one credential path and one is dead, the record names which path was used and why the other failed. A 401/403 on the first path is a question about the path before it is a question about the key. (Precedent: 2026-09-26 execution — the scoped token returned Authentication error; the global-key path per the skill's Auth section succeeded; no raw secrets handled.)

## Substitute audits are verified interim

When the native audit endpoint is blocked (sandbox egress, policy), a read-only advisory-graph sweep over the same source is a verified interim — not a workaround wearing verification's clothes. The record states the substitution, names the blocked call, and keeps the F-flag until a native audit runs on an unrestricted host. (Precedent: 2026-10-08 REA session — the sandbox denied POST to the npm security endpoint; all 549 transitive name@version pins were swept against deps.dev's `advisoryKeys`, the same OSV/GitHub-Advisory source `npm audit` draws on, zero advisories; F-DEP-1 kept as formality.)
