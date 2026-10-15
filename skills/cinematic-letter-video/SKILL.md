---
name: cinematic-letter-video
description: "Build a 60-second cinematic documentary-evidence video: a silent AI-presenter body, a cloned voiceover, and the subject's own emails/letters composed as evidence cards in an HTML timeline, rendered to MP4 via HyperFrames. Use when a documented outcome — a dispute, a refusal, a paper trail — needs a video where the evidence is the hero: offers on light cards, denials on dark, red only on refusal beats, no faces."
license: MIT
compatibility: "Requires HyperFrames, an ElevenLabs (or equivalent) voice account, and a video-generation tool for the presenter body."
metadata:
  version: 1.0.0
---
# Cinematic Letter Video

## Purpose
Build a 60-second cinematic documentary-evidence video in the reference form:
a silent AI-presenter body, a cloned voiceover, and the campaign's own emails
or letters composed as evidence cards inside an HTML timeline, rendered to MP4
via HyperFrames. Raw generations are never the product. (The worked example in
`references/card-system.md` is a fictionalized billing dispute in this form —
the grammar is the asset, not any one case.)

## Workflow

### 0. Intake — lock the inputs before any spend
- **Evidence record** — the campaign's own emails/letters: exact quotations and
  exact timestamps. Nothing quoted or timestamped enters the video without a
  source in the campaign record.
- **Locked script** — short declaratives, clean full stops; ~136 words / 5 beats
  for the 60s form. Script is locked BEFORE any generation spend.
- **Presenter** — who presents (your named presenter persona); kit portrait /
  identity photo; canonical cloned voice ID **library-verified** (check the
  voice library first, every project — never a premade or random voice).
- **House assets** — your brand seal/logo (transparent), music bed with documented rights
  (see Cost), fonts (Bodoni Moda, Source Serif 4, Inter — fetched locally for
  deterministic renders).

### 1. Voice leg — cloned voiceover, per beat
- Render each beat with the canonical cloned voice. Reference settings from the
  proof lane: ElevenLabs `eleven_multilingual_v2`, stability 0.75,
  similarity_boost 0.75, style 0.0, speaker_boost on, speed 1.15, mp3_44100_128.
- **Trim discipline:** measure speech-end per clip (50ms-window RMS; ambience
  floor = 10th percentile; threshold = floor×3, min 300). Trim to speech-end +
  0.3–0.6s air; ~0.25s head-room; 80ms micro-fades at every join. Transcripts
  mark word starts, not acoustic decay — never clip a word tail.
- **Listen-check:** ElevenLabs Scribe word-for-word against the locked script.
  Phantom words or missing words = regenerate that beat (the reference build
  regenerated two beats over an amount-pronunciation ambiguity).

### 2. Picture leg — silent on-camera body
- Generate silent ~8–10s talking-head clips for the on-camera beats (proof lane:
  beats 1 and 5 only; beats 2–4 run voiceover under evidence cards). From the
  kit portrait / identity photo as firstFrameImage + casting prompt (identity
  lock); gentle continuous push-in, clean cuts — NEVER cross-dissolve between
  independently-generated takes (ghosts two faces).
- **PIXEL-CHECK each take:** extract frames at 1s and 5s; same face, haircut,
  features as the identity master; no morphing, no distortion.
- Crop baked film borders to full-bleed 1080×1920 BEFORE composition.

### 3. Evidence cards — the documentary art direction
Build the cards per `references/card-system.md`: the emails/letters are the
hero. Offers and asks go on light cards (`#f4f0e5`); denials and refusals go on
dark cards (`#17171b`); red (`#d43d2a`) appears ONLY on refusal/admission beats;
timestamps are letterspaced mono. **No faces anywhere except the presenter's
own on-camera beats.** Do not invent quotes, timestamps, case IDs, or amounts.

### 4. Assembly — HyperFrames timeline
- Scaffold from the proof lane's pattern: a retimed `index.html` where card
  timings are anchored to Scribe word timestamps (a builder like
  `build/generate_cut.py` computes them from the beat transcripts — see
  references).
- Structure: `<video muted>` body clip + separate `<audio>` per beat;
  on-camera beats (1 & 5) full-frame; voiceover beats (2–4) under the evidence
  cards with a mono slug line (case ID / campaign identifier).
- Burned-in captions: Inter 800 ~64px, 2–5 words per screen, center at ~55% of
  frame height (y≈1050 on 1080×1920), **hard floor y1150 — nothing below it**,
  right ~180px clear of UI icon columns.
- Corner bug: brand seal, upper-left, ~10% frame width, ~70% opacity, from ~0.15s.
- Lower-third (~0.9–4.3s): presenter name (Bodoni, gold) / organization (Inter,
  tracked, ivory), gold rule above.
- Music bed at data-volume ~0.14 (−18 to −25 dB under voice); reads up on the
  end card. Never license-encumbered recordings — recon licensing first.
- Watermark: "© YOUR ORGANIZATION", Inter semi-bold tracked caps, ivory
  ~41% opacity, top-right; fades out at the end-card crossfade.

### 5. QA gates — before render
1. Voice-library check passed; script locked; no invented quotes/timestamps.
2. PIXEL-CHECK: identity holds on every on-camera take.
3. LISTEN-CHECK: Scribe word-for-word vs locked script on every beat.
4. Card timings anchored to actual word timestamps (not guesses).
5. Caption safe zone respected (floor y1150, right clear).
6. `lint` → `inspect` → `render` (`--quality standard` for drafts, `high` for
   final). Fix all errors; review warnings.
7. Frame-verify the render firsthand: extract frames at beats boundaries and
   read them — a successful render proves files exist, not how they look.

### 6. Finalize
- Two-pass ffmpeg loudnorm to **−16 LUFS** / −3.0 dBTP / LRA 11 (measure first,
  apply with measured values, linear=true); AAC 192k; `+faststart`.
- Embed provenance metadata: title, artist (presenter + your organization),
  copyright "© <year> <your organization>", comment with the AI-presenter disclosure
  (voice: ElevenLabs cloned voice; likeness: AI-generated imagery).
- X/Twitter transport: the ~3.8MB wall counts the **base64** payload — keep raw
  ≤ ~2.8MB (720×1280 crf25, re-encode audio at 96k if needed), md5-verify audio
  unchanged, pixel-check a mid-clip frame before upload.

## Output Contract
- **60s cut** MP4 for Reels/Shorts (+ a 720×1280 transport copy when posting to X).
- **End cards:** 1920×1080 and 1080×1920 PNGs. Fundraiser/campaign QR goes on
  the end card ONLY after the target URL is live and independently verified.
  NO QR on mobile-vertical cuts — the viewer is holding the phone.
- All beats word-verified, identity pixel-verified, loudness-normalized, with
  embedded provenance. **The principal's sign-off is the only path to publication.**

## Operating Rules
1. Script locked before any generation spend. Raw generations are never the product.
2. Voice-library check first, every project — the presenter's canonical clone or nothing.
3. Word-for-word listen-check on every beat; phantom words = regenerate.
4. Every timed element carries `data-start` and a duration; deterministic logic only
   (no `Date.now()`, no `Math.random()`, no network fetches).
5. The evidence art direction is non-negotiable: light = offers/asks, dark =
   denials/refusals, red only on refusal/admission beats, mono timestamps,
   no faces. Criticism targets institutions, never individual support agents.
6. Never invent fundraiser URLs, prices, dates, case IDs, or claims — ground
   every word in the campaign record.

## Cost (the $0-default discipline; honest notes)
- **Voice leg: $0 observed** on a nonprofit program tier of the voice provider
  (your cost depends on your own plan). Trim/listen-check are local Python
  (wave + audioop) — $0.
- **Picture leg: spend UNVERIFIED.** The trail names text-to-video generation
  (Veo-class, delivered via media CDN) but records no cost per cut. Get a price
  in front of the principal before regenerating; script/TPS cost discipline
  applies.
- **HyperFrames assembly/render: $0 observed; CLI pricing UNVERIFIED.** The
  build dirs show local renders (`render-hi.mp4` produced on-box); no render
  bill appears in the trail. If HyperFrames moves to a hosted render service,
  price it before shipping.
- **Lip-sync is NOT part of this lane.** By design the pipeline is silent-body
  + dubbed voiceover — the honest note: "no true audio-driven lip-sync ever."
  A lip-sync A/B (sync-3/Hedra/LatentSync class tools) was scoped and parked.
  Only add it via that recon; the lane ships without it.
- **Music bed: rights-first.** Never a license-encumbered recording. The proof
  lane used a rights-documented WAV (license file in assets).

## Provenance
Reconstructed from a complete production build trail — locked script, staged
plan, lip-sync recon, the timing builder and finalize scripts, and the shipped
card-system HTML — plus a companion presenter-video skill's production grammar.
The case behind that build is not reproduced here; the worked example in
`references/card-system.md` is a fictionalized dispute in the same form.
