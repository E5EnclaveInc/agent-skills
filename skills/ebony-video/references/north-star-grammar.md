# North Star Production Line

The proven pipeline for presenter-led spokesperson pieces at a festival-craft quality bar. **Raw generations are never the product.**

## The line, end to end
1. **Script** — short declaratives, clean full stops. Keep a written canon of approved and struck phrases for the presenter; struck phrases never reappear in copy, filenames, or prompts. Disclosure: the presenter does NOT broadcast being AI; never claims to be human.
2. **Body (video model, quality mode)** — generate from the anchor portrait as firstFrameImage + the casting prompt (identity lock). Longer pieces: chain short chunks via the model's extend/continue feature (motion and audio continuous, within the model's freshness window); for older sources, extract the last frame (`ffmpeg -sseof -0.1 -i in.mp4 -update 1 -q:v 2 last.jpg`) → firstFrameImage.
3. **Checks per chunk** — PIXEL-CHECK (identity by eye) + LISTEN-CHECK (transcribe; word-for-word vs script; phantom words = regenerate).
4. **Assembly (HyperFrames)** — scaffold from `flagship-template.html`. Then ALWAYS: `lint` → `inspect` → `render --quality standard` (draft for iteration, high for final).

## The broadcast grammar
- **Cold open, hook-first** — NEVER a logo intro card; the first 2–3 seconds decide reach. Brand = corner bug + lower-third.
- **Corner bug**: your seal/logo (transparent version), upper-left, ~10% frame width, ~70% opacity, static.
- **Lower-third** (~0.9–4.3s): presenter name (display serif, brand accent) / organization (sans, tracked, ivory), accent rule above.
- **Captions**: burned-in, 2–5 words/screen, in the CAPTION SAFE ZONE below, bold sans ~64px on 1080×1920, white + accent words, small y-pop per phrase. ~85% of viewers watch muted. Keep the right ~180px clear (platform icon columns).
- **Music bed**: a warm, era-styled instrumental bed (public-domain-era recordings or generated in-style — verify licensing before first use; never license-encumbered recordings). Data-volume ~0.14 under voice (≈ −18 to −25 dB), reads up on the end card.
- **End card** (3–5s): dark ground, accent radial glow, seal, motto in small caps, organization URL, signature. **NO QR on mobile vertical** (dead end — the viewer is holding the phone); QR is for print/CTV.
- Timing anchors from ffmpeg silencedetect (`-af silencedetect=noise=-30dB:d=0.25`) when no word-level transcript exists.

## Brand assets
Keep in a versioned brand kit: seal (original + transparent derivative — recreate transparency via edge flood-fill: only edge-connected white → alpha 0; interior white lettering preserved), signature, credo/brand document, presenter portraits, the presenter's canonical voice reference. **When a versioned brand kit lands, its pinned values always win** — logo variants, seal, signature, fonts, palettes, lower-third/caption templates supersede this grammar's defaults wherever they conflict. Fetch fonts locally per project for deterministic renders.

## Gotchas (paid for)
- Generated sources may carry a baked film border — `cropdetect`, then crop/scale to full-bleed BEFORE composition.
- White-box logos on dark cards = amateur hour; flood-fill transparency first, verify composited on the dark ground by eye.
- Decorative oversized elements: mark `data-layout-ignore` or the inspector fails.
- Assembly needs a current Node + ffmpeg; without a local transcriber, use silencedetect or a transcription tool for timings.
- Some platforms' video uploads die above a size ceiling that counts the BASE64 payload, not the raw file (raw × 1.33): budget the raw file at roughly ¾ of the stated ceiling. Prefer `-c:a copy` when it fits; md5-verify the audio is unchanged after any transcode.

## Smooth motion + multi-location journeys
**Smooth motion (fixes "choppy transitions"):** NEVER cross-dissolve between independently generated takes — it ghosts two different faces/poses (double-exposure). Use a gentle continuous/per-shot PUSH-IN (scale up over time, then crop to constant output size) + CLEAN CUTS. Within one continuous scene, use a single global slow push so scale matches at cuts; across different locations, per-shot push + hard cuts read as natural scene changes.

**Placing the presenter in DIFFERENT real locations (identity-locked):**
1. Ground each location in a REAL photo (image search) — never imagine a real place.
2. Build a still per location with an image model: inputs = [the exact presenter face + wardrobe reference, a second canonical identity reference, the real location photo]; the prompt names identity + wardrobe explicitly and places the subject "in the location in the THIRD reference." DUAL identity refs + naming the wardrobe hold the face; a single canonical ref drifts identity and defaults to the wrong wardrobe.
3. PIXEL-VERIFY each still against the references before spending video.
4. Animate each still (firstFrameImage = the still) with the presenter's line; pixel + listen check each.
5. Assemble per the smooth-motion rule; keep one wardrobe across the piece for one-journey continuity.

**More gotchas:**
- Video models tend to SING a closing motto at a hopeful close (transcriber flags "Singer" / 2 speakers) — direct "spoken plainly, NO singing, flat measured cadence," drop any "smile" cue, and re-verify the transcript shows a single spoken speaker.
- A firstFrameImage whose backdrop contains depicted human figures (e.g. a mural of people) can make generation fail — swap to a people-free backdrop.
- Don't auto-trim trailing silence on lines with internal pauses (silencedetect grabs a mid-line pause and clips the rest) — use fixed transcript-informed trim windows; always re-transcribe the assembled body to confirm the full word count.
- Cloud platforms generally have NO video frame-interpolation or upscaling — motion smoothing is editorial, not a platform capability.

## TRIM DISCIPLINE — NEVER CLIP A WORD TAIL
- Transcript timings mark word STARTS, not acoustic decay — trim windows set from them CLIP the final word's tail. A clipped tail can still transcribe 95/95, so the transcript alone will NOT catch it.
- MEASURE, don't guess: extract mono 16k WAV per clip, compute 50ms-window RMS, ambience floor = 10th percentile, speech threshold = floor×3 (min 300); speech-end = last window above threshold. Trim to speech-end + 0.3–0.6s air minimum; head-room ~0.2–0.35s; 80ms audio micro-fades at every join.
- If speech runs to the source's final frame (no air left), add a freeze-frame hold (`tpad=stop_mode=clone:stop_duration=0.45` + `apad`) — the music bed masks the ambience pad.
- The end-card crossfade must start only AFTER verified speech-end + air on the closing clip, or it eats the closing line.
- VERIFY boundaries objectively: re-run the RMS check on the trimmed clips (per-clip, pre-assembly — the assembled mix's bed contaminates a global threshold) + independently transcribe the close window and confirm the final words complete.

## Styled QR spec (decode-proven)
Dark-on-light ONLY — never an accent-on-dark inversion (fails ~30% of scanners). Build: rounded dark modules (radius ~0.9) on a light plate, accent hairline frame inside the plate edge, centered brand disc with monogram, EC level H with logo ≤ ~7.5% coverage (≤20% is the ceiling), finder eyes untouched, quiet zone preserved, built at 4× supersample then downscaled. VERIFY from RENDERED pixels (a QR detector) at multiple scales — parity baseline: a plain black QR of the same version also fails below a minimum frame width, so match that, don't beat it. Always decode the OLD QR first to recover the exact target URL before touching an end card.

## Publish discipline
- **Approved ≠ sealed, ever.** Each sealed package publishes immediately on its rail when the workflow is publish-on-seal; record the live URL returned by the platform, then door-check it.
- An asset's body IS the public post text. Never let internal production/salvage notes live in a body field — they will reach a public timeline the moment the row seals. If a sealed body carries internal notes (or exceeds a platform limit): HOLD, never silently edit sealed copy; run revise → re-gate → fresh QC → re-seal.
- Platform mechanics vary: containers for long Reels need processing time (retry with the same creation id on IN_PROGRESS), scheduled-post APIs want ISO dates with offsets, and upload ceilings may count base64 (see Gotchas).

## Polish pass recipe
Two-pass loudnorm to **−14 LUFS / ≤ −1.35 dBTP** (measure first, apply with measured values + linear=true) — one house target; older −16 LUFS notes are superseded. Visible watermark: organization name in tracked caps, ivory ~41% opacity + soft shadow, top-right (clear of bug/captions/lower-third), fading out at the end-card crossfade. Embed provenance in the container metadata (title/artist/copyright/comment, including the AI-spokesperson disclosure). If two file copies of a supplied asset exist, md5 both before reconciling "two versions."

## CAPTION SAFE ZONE — supersedes any lower-center spec
Platform UI overlays eat the bottom of the frame (one major Shorts app covers the bottom ~400px with its description overlay; Reels/TikTok-class UIs eat ~350–420px plus the right icon column), and mid-screen captions carry a documented retention gain. **Rule (one master must clear ALL rails):** burned-in captions center at ~55% of frame height (center ≈ y 1050 on 1080×1920), **HARD floor y 1150 — nothing below it, ever**; keep the right ~180px clear of caption overflow. Lower-thirds (the presenter's name card, ~0.9–4.3s) stay where they are — they're brief and early; the standing captions are what live in the danger zone.
