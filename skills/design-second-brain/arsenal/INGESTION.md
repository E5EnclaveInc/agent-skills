# Arsenal Ingestion — from recon brief to registry

**Status (2026-09-12): the founding recon's recon brief not yet delivered — registry is seeded
from verified estate observations (see ARSENAL.md). This document defines the
ingestion step so the brief lands cleanly when it arrives.**

## Source
the recon team (leading-edge recon) writes:
```
~/design-program/arsenal/ARSENAL_RECON.md
```
If the file does not exist yet, the registry stays in seed mode — do not invent
recon findings.

## Ingestion step
1. Read `~/design-program/arsenal/ARSENAL_RECON.md`.
2. For each technique it recommends, check the registry for duplicates (technique
   identity = normalized name + integration surface).
3. Apply the revenue-stack independence doctrine **before** adopting: zero new
   subscriptions; free tiers without lock-in; every external dependency justified or
   eliminated. Anything requiring a paid tier → `skipped` with the cost reason, or
   `trial` only if a free path is verified.
4. Write new rows in the appropriate table (`adopted` / `trial` / `skipped`) with:
   technique, status, **cost verification** (verified $0 / free-tier name / rejected-with-cost),
   **lock-in risk** (none / low / medium / high + one-line justification),
   **integration notes** (how it plugs into the estate: which site, which repo path,
   which worker), first-seen date, and the recon brief's evidence pointer.
5. Append a dated entry to the Refresh log.
6. If a brief recommendation contradicts standing doctrine (e.g. proposes a CDN 3D
   loader or a third-party form backend), mark it `skipped` with the doctrine
   citation — recon informs, doctrine decides.
7. Journal the ingest in the GitHub hallways-boardroom journal (canonical journaling).

## Monthly refresh
The scheduled job `design-arsenal-refresh` (monthly, see `refresh/RECON_BRIEF.md`
and `refresh/job-body.md`) re-runs the leading-edge recon in the same shape as
the founding recon's brief and ingests via this step. Idempotent: re-running with no new
findings appends only a refresh-log line.
