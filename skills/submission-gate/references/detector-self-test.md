# Detector self-test — manual step, intelligence only

## Status

The detector self-test is a **manual, optional step**. It is never automated
in this pipeline and never gates a submission.

## Rationale

- AI detectors are probabilistic signals, not authorship verdicts. Published
  research and vendor disclosures alike document meaningful false-positive
  rates, with elevated risk for formal academic prose — exactly the register
  our manuscripts are written in. A score informs; it never decides.
- Several publishers have quietly reduced or withdrawn detector use for this
  reason. A referee's stylistic suspicion is the real threat surface, and it
  is addressed by the tell-lexicon scan and the author's own voice, not by a
  detector score.
- **Privacy constraint (hard):** never paste an unpublished manuscript into a
  server-side third-party detector. That is an external send of the author's
  unpublished work to a service with unknown retention and training-use
  terms. T&F's own policy bars editors and reviewers from uploading
  unpublished manuscripts into generative AI tools; the same duty of care
  binds us. No subagent may do this on its own authority.

## Privacy-safe option (if the author wants a score)

EyeSift (https://www.eyesift.com/text-analysis/) advertises a no-signup AI
text check that runs **entirely in the browser** (client-side JavaScript, no
upload to their servers) — per the vendor's own page, retrieved 2026-09-18.
This claim has not been independently verified from this environment. If
used, run it in the live browser on an excerpt (never the full manuscript),
and record the tool, date, and score in the manuscript's audit report.

## Recording

If a self-test is run, log: tool name + URL, date, text sampled, score, and
the disposition ("intelligence only — no action taken" or the specific
human-judged follow-up). File it next to the manuscript's audit report.
