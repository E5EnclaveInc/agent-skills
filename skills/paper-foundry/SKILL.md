---
name: paper-foundry
description: "Draft and restructure scholarly papers using structural argumentation recipes distilled from the most-cited works in two lanes: reparations economics and Black Atlantic / African diaspora history. Use when drafting a new paper, restructuring a weak one, or strengthening an argument's architecture — 'frame this paper's gap', 'restructure this argument', 'how would the best papers in this lane handle this objection'. The argumentation layer; the submission-gate skill is the verification layer."
license: MIT
metadata:
  version: 1.0.0
---
# Paper Foundry

## What this is

Pattern B (process primitive). Reliability comes from explicit procedure + checklists, and from the fact that every recipe below cites real, API-verified exemplars — never vibes, never memory, never prose templates. We distill structural DNA (how the best papers argue), not prose style (today's base models already write better than most PhDs; prose was never the bottleneck).

Exemplar keys used across this skill: **L1-En** = lane 1 (reparations economics) exemplar n; **L2-En** = lane 2 (Black Atlantic / African diaspora history) exemplar n. Full registry: `references/exemplars.md`. Working evidence: `work/lane1-reparations-economics.md`, `work/lane2-black-atlantic.md`. All citation counts are OpenAlex `cited_by_count` as of 2026-09-18, spot-checked against Crossref with zero mismatches.

## How Foundry composes with Submission Gate (read this before using either)

- **Foundry is the proposal layer.** It runs during drafting and revision: gap-framing, claim architecture, evidence weaving, objection handling, intro/conclusion, literature positioning. Its output is an argument structure with exemplar-backed moves.
- **Submission Gate is the disposal layer** (the companion `submission-gate` skill). It runs after drafting, before submission: journal instructions, mechanical checks, cold review, venue fit, declarations. Its output is green/amber/red on compliance.
- **Pipeline order:** Foundry first, Gate second. Never submit a Foundry-drafted paper without the Gate pass. Never use Gate findings to quietly rewrite Foundry recipes — route Gate failures through the attribution test.
- **The attribution test applies across the boundary.** When a Foundry-drafted paper fails — a weak review, a Gate flag, a journal return — ask: *could the agent have reached the correct argument from the materials it had?* If the recipe was wrong, fix the recipe file (procedure flaw). If the exemplar evidence was thin, mark or replace the exemplar (knowledge gap). If the field itself disagrees, open it to the user (genuine ambiguity). Never fix in the wrong layer.

## Hard rules

- **$0, no subscriptions, no accounts.** All evidence comes from free public APIs (OpenAlex, Crossref). No fine-tuning — ever. This is doctrine, not a suggestion: recipes live in text files a human can review in 30 seconds, not in weights that cannot be audited or retracted. (Rationale: Meta Engineering's "Organizational Second Brain," 2026-09.)
- **Nothing invented.** No invented citations, quotes, page numbers, DOIs, or citation counts. A recipe section whose evidence is thin says so inline ("abstract-only evidence," "inferred, unverified") — the confidence annotations in the exemplar registry are load-bearing, not decorative.
- **Structure, not style.** These recipes teach argumentative moves. They never teach voice, diction, or sentence rhythm. If a draft reads like a pastiche of an exemplar, the recipe was misapplied.
- **The human keeps three things.** The thesis, the taste, and the judgment calls where evidence genuinely cuts two ways. Everything machine-checkable belongs to the machine.

## Recipe index (load the file when its phase runs; don't preload)

1. `recipes/recipe-gap-framing.md` — name the gap so the paper has a reason to exist. Fourteen named gap moves with exemplar citations.
2. `recipes/recipe-contribution-claim.md` — architect the thesis: single-pivot, stacked, triangulated, or comparative. Pick the architecture the venue rewards.
3. `recipes/recipe-evidence-weave.md` — set evidence-to-claim density: how close each claim sits to its evidence, by genre.
4. `recipes/recipe-objection-handling.md` — name the strongest objection early and answer it with the method, not with rhetoric.
5. `recipes/recipe-intro-conclusion.md` — opening and closing moves: paradox, vignette, inventory, diagnosis, taxonomy; and how to land without overclaiming.
6. `recipes/recipe-lit-review-positioning.md` — make room for the contribution: credit, group, delimit, reclassify, affiliate.
7. `recipes/recipe-venue-calibration.md` — economics journals vs. history journals vs. field journals: which architectures each venue's exemplars reward, and what to change when retargeting.

## Drafting loop (door-verify)

1. **Frame:** run recipe 1 on the paper's core question. Write the gap as one sentence before drafting anything else. If the gap sentence can't name the consensus it displaces, the paper isn't ready to draft.
2. **Architect:** run recipe 2, then recipe 7 — pick the claim architecture the target venue rewards. One paper, one architecture; don't blend.
3. **Weave:** run recipe 3 claim by claim. Every substantive claim gets its evidence attached in the same paragraph. No floating claims.
4. **Fortify:** run recipe 4. Name the single strongest objection to the thesis and check the method answers it. If the answer is only rhetorical, the design is incomplete.
5. **Position:** run recipe 6. Every cited predecessor is credited by name and delimited by scope. No predecessor is a straw man.
6. **Open and close:** run recipe 5 last, not first. The opening must earn the thesis; the closing must not introduce new claims.
7. **Verify:** hand the draft to submission-gate. Foundry's job ends where Gate's begins.
8. **Attribute:** if the draft fails anywhere, run the attribution test (above) before editing anything.

## Evidence quality and known gaps (read before trusting a recipe)

- Most distillations are **abstract-level**: gap-framing and claim architecture read clearly in abstracts; objection handling, intro/conclusion microstructure, and lit-review mechanics often do not. Recipes flag these sections inline.
- OpenAlex systematically undercounts pre-2000 monographs in the history lane and merges book citations into review records. One record (L2-E1, 7,562 citations) is a review-proxy merge artifact — it is documented as such and never cited as evidence of the review's own influence. One record (a *Black Jacobins* entry) misattributes authorship and is banned from citation entirely.
- Priority full-text acquisitions for future recipe upgrades: Patterson & Kelley "Unfinished Migrations" (2000), Morgan *Laboring Women* (2004), Baucom *Specters of the Atlantic* (2005), Edwards *The Practice of Diaspora* (2003).
- When new exemplars are verified or new misses found, update the recipe files and the registry the same session. Nothing breaks twice.
