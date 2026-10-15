# Source Prompts — eng_discipline

Distilled from the GrokBot Galaxy 30-prompt set (Ship by Thursday build,
September 15–17, 2026). Provenance: prompts collected from the three builders'
posts and the "30 GROKBOT PROMPTS" card; full text archived with the original source set.

## A02 — Rigorous engineering skill pack
> Install a rigorous engineering skill pack: tests, PR hygiene and
> issue-to-ship loops. Remove everything unnecessary for a 3-day build.

## B08 — Ship-to-main rules
> Write a five-line shipping policy that lets humans and bots move fast,
> deploy directly and recover quickly from mistakes.

## Adaptation notes
- GrokBot "ship directly to main" → a dispatch doctrine: reversible moves
  run act-then-report; production moves need the human's word. The five-line
  policy is where that line is drawn for each build.
- "Remove everything unnecessary for a 3-day build" → the explicit kept/cut
  list: stripping is a written decision, not drift.
- Door-verify is the standing form of "tests that matter": prove the live
  state, never trust the log.
