# Cinematic Letter Video — Pipeline README

**One-liner:** a silent AI-presenter body + cloned voiceover + the campaign's
own emails/letters composed as documentary evidence cards in an HTML timeline,
rendered to MP4 via HyperFrames. Generalized from a complete production build;
the worked example is a fictionalized dispute in the same form.

## The five stages

```
1. LOCK        evidence record + locked script (beats) + presenter identity
2. VOICE       ElevenLabs cloned voice → per-beat trims → Scribe word timings
3. BODY        silent ~8–10s talking-head clips (beats 1 & 5) → pixel-check
4. ASSEMBLE    HyperFrames: retimed index.html, cards anchored to word timings
5. FINALIZE    loudnorm −16 LUFS, provenance metadata, transport copies
```

## The beats (60s, 5-beat form)

1. **Presenter on camera** — cold open, hook first; never a logo intro card.
2. **The offer (light cards)** — campaign's own emails/letters, verbatim.
3. **The refusal (dark cards)** — red only on the refusal/admission phrase.
4. **The demand + the silence** — close the middle on an empty-inbox glyph.
5. **Presenter closes** — then the end card (seal, motto, campaign URL).

## The art direction (non-negotiable)

- No faces except the presenter's own on-camera beats.
- Offers/asks on **light cards** `#f4f0e5`; denials/refusals on **dark cards** `#17171b`.
- Red `#d43d2a` ONLY on refusal/admission beats.
- Timestamps in letterspaced mono; bodies in Source Serif, verbatim.
- Criticism targets institutions, never individual support agents.

## The quality gates

- Voice-library check first; script locked before any generation spend.
- PIXEL-CHECK every on-camera take (identity masters).
- LISTEN-CHECK every beat, Scribe word-for-word; phantom words = regenerate.
- `lint` → `inspect` → `render` (standard draft, high final).
- Frame-verify the render firsthand before anything ships.
- **The principal's sign-off is the only path to publication.**

## The honest notes

- This lane is **silent-body + dubbed voiceover by design** — no true
  audio-driven lip-sync (owned openly). A lip-sync A/B was scoped and parked;
  it is not part of this lane.
- Voice leg: $0 observed on a nonprofit program tier of the voice provider
  (your cost depends on your own plan).
- Picture-leg generation cost and HyperFrames render pricing are **not in the
  trail** — price them before spending; script/TPS discipline applies.
- Music beds must be rights-documented; never license-encumbered recordings.

## Where this came from

Reconstructed from a complete production build trail (script, staged plan,
lip-sync recon, timing builder, finalize script, the shipped card-system
HTML) and a companion presenter-video skill's production grammar. Full
provenance lives in `SKILL.md`.
