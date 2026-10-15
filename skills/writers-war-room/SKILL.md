---
name: writers-war-room
description: "Convene a Pixar-Braintrust writers room to perfect source material into a finished multi-voice audiobook script — named seats with editorial gates, rank-choice seating, research plus leading-edge recon, ElevenLabs audiobook craft, crafted-EPUB finish. Use when a transcript or draft must become a publishable audio script."
license: MIT
metadata:
  version: 1.0.0
---
# Writers War Room

## Purpose

Turn source material (a transcript, a draft, a brief) into a perfected script for a multi-voice audio production, through the Pixar Braintrust method: candid notes on the work, never the person; the head writer revises; iterate until the chairs pass it. Ends in a crafted EPUB by default. Reusable across productions — first proven on a full-length multi-voice audiobook production, which was the first instance, not the template.

## Inputs (parameterize every run)

- **Source material**: the transcript/draft, with word/turn counts and speaker structure.
- **Voice/cast spec**: the voice IDs and their dramatic assignments (e.g., lead vs interlocutor).
- **Output format**: default = crafted EPUB; name any alternative explicitly.
- **Canon constraints**: the non-negotiable facts, attributions, and prohibitions the room may not vote away. List them in the charter.
- **Named seats** (optional): the commissioner may name any seat outright; unnamed seats are rank-choice seated.

## Workflow

1. **Charter.** Write the charge in the commissioner's words: what the script must become, scope, non-goals, deliverables, canon constraints, standing (the room OWNS the script). Canon constraints are binding — the room does not vote them away.
2. **Seat the room.** Named seats take their offices directly (no election):
   - **Co-chairs** — the FINAL editorial gate. Nothing ships without both passing it. (Archetype: one moral/prophetic voice, one dramatic-structure voice.)
   - **Co-vice chairs** — copy editors. One owns persuasion architecture, one owns clarity and style.
   - **Head writer** — drafts the script, and is the FIRST editorial gate.
   - **Research head** — owns extensive research plus leading-edge recon.
   - **Named specialists** — seated directly (archetypes: power/strategy, pitch).
   
   Then **rank-choice the remaining personnel**: the named seats propose a candidate slate covering dialogue polish, audiobook craft, fact-check rigor, and lineage voice. Run ranked-choice with a published rounds table; seat the winners.
3. **Persona cards.** One per seat, grounded in their published work — positions paraphrased from what they actually made, never fabricated utterances. Record why each seat was chosen.
4. **Research (research head leads; recon lane in parallel).** Verify every factual claim in the source against current sources; recon the latest information so the script sits at the leading edge. Mark claims `[VERIFIED]` / `[CONTESTED]` / `[UNVERIFIED]` with sources. **ElevenLabs audiobook best practices** are a defined research step — chapter architecture, pacing, pronunciation consistency, dialogue-vs-narration handling, per-turn segmentation, listener retention — applied to the draft, not admired from a distance.
5. **Draft (Braintrust).** The head writer drafts. The room gives candid notes on the work, never the person. The head writer revises. The vice chairs copy-edit each revision. Iterate until excellent. Real dissent is mandatory — a pass with no dissent is incomplete.
6. **Gates.** Head writer = first gate. Co-chairs = final gate (both must pass). Record every gate decision; a failed gate returns the draft with notes, never a silent rewrite.
7. **Craft the EPUB.** A single craftsman builds the final EPUB — beautiful, anatomical, structured. One hand, not a committee. Default palette and register come from the commissioner's canon.
8. **Record.** Minutes with `[VERIFIED]`/`[OPINION]` separation, the RCV rounds table, persona cards, research findings with sources, revision history, gate decisions, minority notes verbatim, decision log. Write to `records/war-rooms/<YYYY-MM-DD>-writers-war-room.md` in your workspace.

## Output Contract

- The perfected script file.
- The crafted EPUB (default: `<project>/<title>.audiobook-script.epub`).
- The war-room record, naming what changed vs the source and what the research updated.

## Operating Rules

1. The transcript is the source of truth, not a cage — meaning preserved, never rewritten into fiction.
2. Canon constraints are binding; the room rules craft, not facts.
3. No audio renders inside this commission — the render lane runs after, on the perfected script, under the production's ear gates.
4. Default cost $0; research uses free sources.
5. Never invent experience, figures, metrics, dates, credentials, or outcomes.
6. The craftsman owns the EPUB's design; the room owns the words.
7. A war room the commissioner names starts and runs the same turn — never staged back as a plan.
