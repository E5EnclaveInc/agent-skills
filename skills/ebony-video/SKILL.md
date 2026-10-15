---
name: ebony-video
description: "Produce presenter-led video assets with a cloned-voice voiceover and a broadcast-grade generated-video production line: identity-locked body generation, per-chunk pixel and listen checks, template assembly, caption safe zones, word-tail-safe trim discipline, and a human seal before publication. Use for spokesperson or presenter videos where the same on-screen persona must hold across every generated chunk."
license: MIT
metadata:
  version: 1.0.0
---

# Presenter Video

## Purpose
Produce presenter-led video assets at a named quality bar (think festival-craft documentary polish). Two legs: the voice leg runs on a cloned voice from your TTS provider; the picture leg runs the North Star production line (see `references/north-star-grammar.md`). **Raw generations are never the product.**

Set two values per presenter before the first project:

| Variable | Meaning |
|---|---|
| `PRESENTER_VOICE_ID` | The presenter's cloned-voice ID in your TTS library |
| `PRESENTER_ANCHOR_IMAGE` | The approved anchor portrait used as the identity lock |

## Voice leg — cloned voice
- Use the presenter's canonical clone (`PRESENTER_VOICE_ID`), verified in your TTS library at the start of every project; never a premade or stock library voice.
- Script rules: short declaratives, clean full stops. Spoken mottos in the audience's language only; a Latin (or other ceremonial) line stays visual-only on the end card. The presenter does NOT broadcast being AI; never claims to be human.
- Trim discipline: measure speech-end per clip (50ms-window RMS, ambience floor = 10th percentile, threshold = floor×3, min 300); trim to speech-end + 0.3–0.6s air; 80ms micro-fades at every join. Never clip a word tail — transcripts mark word starts, not acoustic decay. Full method in the grammar reference.

## Picture leg — North Star production line
- Body: a video-generation model in quality mode, from the anchor portrait as firstFrameImage + the casting prompt (identity lock). Longer pieces: chain short chunks via the model's extend/continue feature, within its freshness window.
- Per-chunk checks: PIXEL-CHECK (identity by eye) + LISTEN-CHECK (transcribe; word-for-word vs script; phantom words = regenerate).
- Assembly: HyperFrames from `references/flagship-template.html`; then ALWAYS `lint` → `inspect` → `render` (standard for drafts, high for final).
- Smooth motion: gentle continuous push-in + CLEAN CUTS. NEVER cross-dissolve independently-generated takes (it ghosts two faces).
- Full broadcast grammar, caption safe zone, music bed, QR spec, and publish mechanics: `references/north-star-grammar.md`.

## Character-consistency ladder
Character continuity is built from what feeds the model, in rising durability:
prompt baseline → reference anchor → drift judging → trained model. Seeds never
hold identity: leave seed unset across a set (a seed re-rolls one generation
and transfers nothing).

- **Baseline-plus-delta casting prompt.** Write the presenter's identity once as a full must-not-change enumeration: face geometry, hair (cut, color, placement), skin tone, wardrobe, proportions, lighting direction, camera height and angle, subject size and position in frame. Every chunk generation uses the BYTE-IDENTICAL casting prompt; only the final clause changes (the action or scene for that chunk). Never write "same as before" — there is no memory between calls; restate the baseline in full each time.
- **One anchor, every chunk.** The anchor portrait rides as firstFrameImage on every generation, never dropped. On extend chains, judge each new chunk against the written baseline and the anchor — never judge chunk N against chunk N−1 output alone; chaining output-to-output compounds drift. Fix drift by tightening the enumeration, not by chaining outputs.
- **Judge by sub-element, across the whole chunk.** PIXEL-CHECK is not a vibe pass: compare the chunk against the baseline enumeration part by part. A named part gained, lost, recolored, or reshaped is DRIFT. A part that moves with the action (hair swinging, a hand rising) is animation and passes. Sweep mid-chunk frames, not just first/last — drift that fades in late passes a first/last spot check. Phantom-word equivalent: regenerate.
- **Cross-dissolve ban holds**: dissolving independently generated takes ghosts two faces — the same drift-compounding failure mode.
- **Escalation order for stubborn drift:** tighten enumeration → regenerate the baseline hero once and re-anchor the set to it (a wardrobe/haircut change is a new baseline, run once as its own delta, approved, then anchored) → if the presenter recurs at cast scale across campaigns, a trained visual model (LoRA) replaces reference anchoring; prompts do not scale.

## Documentary-evidence story videos
When the piece is a documentary-evidence story (the documents are the hero):
- Evidence on cards: favorable documents on light cards, refusals/denials on dark; reserve red for refusal/admission beats only.
- No faces except the presenter's own presentation segments.
- Criticism targets institutions, never individual support agents or named staff. Characterizations stay attributed ("the founder's characterization"), never stated as legal findings.
- Exact quotation and timestamp fidelity from the source record; never paraphrase evidence on a card.
- A fundraiser URL and QR go on the end card ONLY after the fundraiser is published and the URL is independently verified. No QR on mobile-vertical cuts (dead end — the viewer is holding the phone).
- Deliverables: a 60-second vertical cut for Reels/Shorts; end cards at 1920×1080 and 1080×1920.

## Operating Rules
1. Voice-library check first, every project — the presenter's clone or nothing.
2. Script locked before any generation spend.
3. Word-for-word listen-check on every chunk; phantom words = regenerate.
4. `lint` → `inspect` → `render`, always. A named human's seal is the only path to publication.
5. Never invent URLs, prices, dates, or claims — ground every word in the project record.
