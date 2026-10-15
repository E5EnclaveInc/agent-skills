# Design Arsenal Recon — brief template (monthly refresh)

Run this recon monthly (job: `design-arsenal-refresh`). Same shape as the founding recon's
founding brief. Output: dated entries appended to `arsenal/ARSENAL.md` via the
ingestion step (`arsenal/INGESTION.md`). Idempotent: no new findings → only a
refresh-log line.

## Scope
Leading-edge design technique recon across the four communities (per the
seed-to-forest rule): leading-edge science (perceptual/color science, HCI research),
the hacker community (open-source motion/3D/icon tooling), the nonprofit community
(what mission-driven orgs ship that converts), the astrology/design-culture lane
(visual culture currents). Focus: techniques applicable to the organization's cinematic,
bespoke, motion-rich web properties.

## Constraints (non-negotiable)
- **Revenue-stack independence:** zero new subscriptions, no lock-in, free tiers only.
  Every candidate carries cost verification + lock-in risk or it doesn't enter the registry.
- **Doctrine filter:** candidates contradicting standing doctrine (CDN 3D loaders,
  third-party form backends, ambient motion loops, template grids) are recorded as
  `skipped` with the doctrine citation — recon informs, doctrine decides.
- **Read-only against production:** no merges, no deploys, no touching held PRs.
- **No invented numbers:** every cost/limit figure traced to a checkable source.

## Procedure
1. Survey: web search for current (last ~90 days) developments in web animation,
   WebGL/WebGPU practice, icon systems, design systems, motion accessibility,
   form UX, and nonprofit/campaign design that converts. Prefer primary sources
   (specs, release notes, papers) over listicles.
2. For each candidate technique, record: what it is, evidence pointer (URL + date),
   status recommendation (adopted/trial/skipped), cost verification, lock-in risk,
   integration notes (which house site/repo it would plug into and how).
3. Check candidates against the current registry for duplicates before writing.
4. Append rows + a dated refresh-log entry to `arsenal/ARSENAL.md`.
5. If a candidate would change a protocol (not just the arsenal), flag it in the
   refresh-log as `PROTOCOL-CHANGE-PROPOSAL` — do not edit protocols unilaterally;
   protocol changes need ratification.
6. Journal the run in the team's project journal.

## Output contract
- Findings land in `arsenal/ARSENAL.md` with first-seen date = recon date.
- Refresh-log line even when empty: `YYYY-MM-DD — recon run: no new findings.`
- Never more than one registry write per technique per run (idempotent).
