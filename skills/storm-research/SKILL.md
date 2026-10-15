---
name: storm-research
description: "Multi-perspective deep research using Stanford OVAL's STORM method (NAACL 2024), adapted for agent search tools. Runs five expert personas, maps their contradictions, synthesizes a sourced briefing, and peer-reviews its own work with confidence scores — the equivalent of ~40 hours of expert reading. Use before any report, decision, investment, competitive analysis, negotiation/interview prep, or presentation where a single-prompt answer would inherit the majority view and miss blind spots."
license: MIT
metadata:
  version: 1.0.0
---
# STORM Research — multi-perspective deep research

Stanford OVAL's **STORM** method (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking, NAACL 2024), adapted for agent use. Four phases turn a single question into a sourced, contradiction-mapped, self-reviewed briefing — comparable to ~40 hours of expert reading, and measured ~25% more organized / ~10% broader than single-prompt research.

## When to use
Before any report, article, strategic decision, investment, competitive/landscape analysis, negotiation or interview prep, or presentation — anywhere a one-shot answer would inherit the majority framing and miss blind spots. The default tool when the Chairman says "research X" and means it.

## Core principle
One prompt returns the most common view. Five perspectives return what each other misses. Run all four phases **in order** — the contradiction map (Phase 2) and the peer review (Phase 4) are what separate real expertise from a confident summary. Never skip them.

## Sourcing discipline (this is what makes it trustworthy)
STORM's one documented weakness is source bias and fact misassociation, so in this set **ground every phase in real retrieval**:
- Use ExaSearch / ExaAnswer / ExaContents (or WebSearch) to source each perspective's strongest evidence and every Phase-3 finding.
- Cite inline. Mark any claim you cannot source as **UNVERIFIED**. Never assert a figure, date, or name from memory — verify it (the kingdom's factual-integrity bar).
- The **Skeptic** persona (1.3) and the Phase-4 bias check operationalize the disconfirming search: actively try to kill the thesis, name competitors and counter-evidence, before relying on it.

## Phase 1 — Multi-perspective scan
Simulate 5 experts on the TOPIC. For each: core position (2 sentences), strongest **sourced** evidence, and the one thing only they would say.
1. **Practitioner** — works with it daily; what academics miss; ignored practical realities.
2. **Academic** — what peer-reviewed evidence actually says; where it contradicts popular belief.
3. **Skeptic** — strongest counterargument; evidence proponents ignore.
4. **Economist** — who profits; what incentives shape the narrative.
5. **Historian** — parallels and how they played out.

## Phase 2 — Contradiction map
(1) Where two+ perspectives directly clash — name the claims. (2) Strongest vs weakest evidence, and why. (3) The one question that resolves the biggest contradiction. (4) What EVERY perspective agrees on (likely true). (5) What NONE addressed — the field's blind spot, often the most valuable finding.

## Phase 3 — Synthesis briefing
(1) One-paragraph summary for a CEO with 60 seconds who needs nuance. (2) 5 key findings ranked by reliability, each noting who supports/challenges it. (3) The hidden connection visible only across all five. (4) The actionable insight — what someone in the user's ROLE should DO differently, specific. (5) The frontier question that would change everything.

## Phase 4 — Peer review (STORM's built-in fix for its own weakness)
(1) Confidence 1–10 per finding, with reasons. (2) Weakest link + exactly what would verify it. (3) Bias check — which perspective dominated. (4) Missing 6th perspective that would change conclusions. (5) Overall grade a domain expert would give, and what to fix.

## Output
Lead with the Phase-3 one-paragraph summary + the actionable insight; attach the contradiction map and the Phase-4 confidence table; cite sources inline; flag unverified claims. Keep it a decision instrument, not an essay. For a richer deliverable, render the briefing as a webpage, doc, or comparison table.

## Scaling (optional)
For breadth or speed, dispatch the five personas as parallel subagents (each does its own ExaSearch sourcing), then synthesize their returns — this collapses wall-clock time. Use sonnet per persona; reserve opus for the synthesis when stakes are high.

## Provenance
Stanford OVAL STORM — live tool storm.genie.stanford.edu, code github.com/stanford-oval/storm (MIT). This skill is the method, not the software; no install or credentials required.
