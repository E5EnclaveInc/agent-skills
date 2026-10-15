---
name: scheduled-job-discipline
description: "Author, update, and verify recurring agent jobs so they never silently run stale instructions, die on a helper's timeout, or file run logs nobody can check: scheduler source-of-truth discipline, whole-body updates, timeout budgeting across the whole call path, watermark/diff hygiene, silent-tick semantics, and honesty accounting for run logs. Use when creating or repairing any cron, scheduled worker, watch, or recurring automation."
license: MIT
metadata:
  version: 1.0.0
---
# Scheduled-Job Discipline — recurring jobs that can't lie to you

Recurring agent jobs fail silently in predictable ways: the definition you edited is not the definition that runs, a helper's 30-second timeout strangles a call that legitimately needs 90, a "peek" command quietly eats the events it showed you, a truncated run files a report claiming steps it never took. None of these page anyone. This discipline exists so they can't happen — every rule below is a postmortem that already happened somewhere.

## 1. Know the scheduler's source of truth

- Many schedulers **cache the job definition at load/registration time**. Editing the job's file on disk may change nothing that runs. Treat the scheduler — not the file — as the source of truth.
- Push every change through the scheduler's own update path, then **verify the effective definition** through the scheduler's view/status/runs surfaces. A directory listing can show a job that isn't registered, and hide one that is.
- Corollary: when reality and the file disagree, believe the scheduler and fix the file.

## 2. Updates replace — compose whole bodies

- Scheduler update operations typically **replace the entire job body**; they do not merge or patch. A one-word fix sent as a partial body wipes the job down to that one word.
- Rule: read the current effective body first, compose the complete intended body, send it in one update, verify afterwards. Keep a known-good copy until the new body is verified live.

## 3. Timeout budgeting — audit every timeout on the path

A call chain fails at its **tightest** budget, and the budget that fires is rarely the one you set.

- **Caller ≥ callee.** If job A calls helper B with a 30s timeout, and B's upstream call legitimately takes 60–90s under load, A fails chronically and looks like an upstream outage. The fix is the budget, not the checker. Set each layer's timeout above the worst case of the layer beneath it.
- **Launchers count too.** A launcher's wait budget that is shorter than the bootstrap it launches will kill healthy runs. Audit caller, helper, launcher, and watcher timeouts as one system.
- **Socket timeouts are per-receive inactivity, not deadlines.** A trickling response can hold a "600s timeout" open forever. Long work needs an explicit **wall-clock deadline** per item, measured from the item's start.
- **Calibrate against the slowest real run** — cold cache, loaded box — not the warm demo run.
- **Never recompute huge inputs on a hot path.** Re-hashing or re-parsing multi-hundred-MB inputs every tick will blow any budget eventually. Cache by `(size, mtime)`, or compute once at ingest.
- **Capture exit codes into variables** before composing status lines from them; an echoed-but-never-assigned code reads as success downstream.

## 4. Watermarks and diffs

- Recon-style jobs keep a **watermark**: each run fetches, diffs against the watermark, processes the delta, then advances it. Run sources through a wrapper that does sweep + diff + refresh as one step.
- **Initialize watermarks explicitly before enabling a job.** A dry run may not advance live state — the first live run then re-processes (or re-alerts on) everything the dry run "consumed."
- **Beware reads with side effects.** A digest/peek/summary command that advances a watermark as it reads will consume events nobody else will ever see. Know which of your read paths write.
- **Guard entrypoints.** A script with module-level side effects runs its whole workload on `--help`. Put an argv guard at the top, and call dangerous scripts only through their wrapper.

## 5. Silent-tick semantics

- A tick with nothing to report **emits nothing** — or a single OK line to the run log. Notification noise trains the human to ignore the channel, which is how real failures get missed.
- Report material change, failures, and true gates. Routine state ("still 7 items waiting") is log material, not message material.
- A tick that **could not verify its inputs** says exactly that. It never reports a success it did not earn.

## 6. Run-log honesty

- Every run appends an after-action: what ran, counts from the system of record, what changed, what is next. A truncated run records the truncation — **never claim steps that did not run.**
- Worker self-reports are claims, not facts. A separate closer/auditor step (or the next run) verifies claimed counts against ground truth — queue stats, ledgers, arithmetic (a cost claim is price × uptime, checked, not trusted).
- Distinguish **per-run** numbers from **cumulative** totals when auditing; most "bogus report" alarms are that confusion. Genuinely false reports get quarantined and a failure record gets filed.
- If a run produced no after-action, that absence is itself a recorded gap — covered by the closer, never papered over.

## 7. Failure-proofing the fleet

- **Cache failures as well as successes.** A success-only cache in front of a raising loader makes every caller re-burn the full fetch sequence; a short failure cache makes the component fail fast and closed.
- **Retry the transport layer**, not just HTTP status codes — connection resets and read timeouts are the common case on proxied egress.
- **Debounce state flips.** A health state must hold for N consecutive ticks before it pages anyone; single-tick flaps are weather, not incidents.
- **Long jobs are resumable and idempotent**, owned by the scheduler, so a killed or missed run self-heals on the next tick instead of losing the work.
- **Every watcher gets an independent dead-man check** that probes remote state. The watcher cannot be the only thing standing between a dead run and a meter — or between a dead run and silence.
- **When a shared helper moves, fix every reference in the tree in one pass** — then re-verify the whole changed set (compile, smoke). The next scheduled tick will find the one reference you missed, at 3 a.m.
- **Mass edits preserve per-line structure** (indentation, quoting). A naive find-replace across hundreds of files will break the files whose context differed; validate every changed file afterwards.

## 8. Job-body craft

The body is instructions to a future worker who has none of your context:

- Name exact commands, exact paths, exact done-states. "Check the queue" is not an instruction; the command that lists it is.
- Load deferred tooling **explicitly as step one** if the body uses it — availability in your session is not availability in the worker's.
- Bound output: read large files in pages; never dump them through the job's stdout (it truncates, and the truncation is silent).
- State the hard limits **inside the body** — money, sends, irreversible actions — not in a doctrine doc the worker may never open.
- Give the job a run budget and a "never stop mid-unit" rule: finish the current unit, then stop.

## Pre-flight checklist

- [ ] Effective definition verified through the scheduler after the last edit
- [ ] Body is complete (not a patch), known-good copy kept until verified
- [ ] Every timeout on the path audited; caller budgets exceed callee worst cases
- [ ] Wall-clock deadline on long items; no unbounded socket waits
- [ ] Watermark initialized; side-effecting reads identified
- [ ] Entrypoint argv-guarded; dangerous scripts called via wrappers only
- [ ] Silent-tick contract stated; reporting threshold is material change
- [ ] After-action format stated, with ground-truth counts and honest truncation
- [ ] Failure caching, transport retries, flip debounce in place
- [ ] Resumable/idempotent; independent dead-man check exists
