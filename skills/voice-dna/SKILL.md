---
name: voice-dna
description: "Build a named, recallable writing-style profile (Voice DNA) from three writing samples, saved as ghostwriter rules for a person, brand, or client. Use when ghostwriting, keeping AI output out of AI-slop territory, or maintaining one voice per persona/brand/client."
license: MIT
metadata:
  version: 1.0.0
---
# Voice DNA

## Purpose
Turn how someone actually writes into a saved, reusable profile the AI can recall by name —
so every draft sounds like *them*, not like a model. Pattern B (process primitive); the
procedure is the skill.

## When it fires
- Writing for a persona with a distinct voice (a named persona, a client, a brand).
- Client ghostwriting work: one profile per client/brand, workspace recalls which is which.
- Any output that must not read as AI-written (marketing, newsletters, proposals, posts).
- NOT for voice cloning/audio — that's the `elevenlabs` skill. Voice DNA is writing style.

## Procedure

### 1. Collect three samples
Get three real writing samples from the person/brand (emails, posts, pages — their words,
unedited). Dictation counts if it's how they naturally speak-write.

### 2. Build the profile (one prompt)
Feed the samples and ask for the profile **as a set of rules a ghostwriter would follow**:
- Sentence length and rhythm; words they reach for; words they never use.
- Formality level, humor, directness, how they open and close.
- **The don't-list matters more than the do-list:** never-use words (e.g. leverage, utilize),
  never-use closers ("in conclusion"), never-use AI tells (em-dashes, emoji-led headers).
  To find the AI tells: ask the tool "what marks writing as AI-written?" and fold the
  answer into the don't-list.

### 3. Name and save it
Save it under a person/brand name ("Client A — voice DNA"). In a workspace with memory,
the name is the recall handle. Multiple profiles can coexist — one per person or client.

### 4. Test it
Run a test prompt: write a short piece in their voice. If it reads as generic, add
constraint rules and re-save. Iterate until a blind reader would attribute it to them.

### 5. Use it
Every writing task starts by invoking the profile by name: "write this using X's voice DNA."
For client work, confirm the profile with the client before using it on live copy.

## Files
- `profiles/_template.md` — the blank profile template. Save each built profile as
  `profiles/<name>.md`, one per person, brand, or client.

## Operating rules
- Samples must be real, not aspirational — the profile captures how they write, not how
  they wish they wrote.
- Refresh when the voice evolves (new samples in, re-profile). Quarterly is plenty.
- Privacy: samples may contain sensitive client material — never put them where they
  train anything. State that to the client up front.
- Pairing: Voice DNA (style) + a voice clone (audio) = a complete spokesperson
  identity per persona.
