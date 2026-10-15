# The Evidence Card System

Recovered from the reference build's shipped card-system HTML. Canvas is
1080×1920; fonts bundled locally as `@font-face` (Bodoni Moda, Source Serif 4,
Inter). The example exchange below is fictionalized — a software vendor's
billing dispute standing in for any documented offer/refusal paper trail.

## Palette

| Role | Value | Notes |
|---|---|---|
| Card, light (offers/asks) | `#f4f0e5` | Cream; border `#d9cfae`; dark body text `#191914` |
| Card, dark (denials/refusals) | `#17171b` | Near-black; border `#33333b`; ivory body text `#f2efe6` |
| Red (refusal/admission ONLY) | `#d43d2a` | `span.red` around the refusal phrase, bold |
| Gold accent | `#d8b36a` | Lower-third rule, name |
| Timestamp, light card | `#8a7648` | Mono, letterspaced |
| Timestamp, dark card | `#9a917e` | Mono, letterspaced |
| Slug line (case identifier) | `#b9ac7f` | Mono, tracked, centered |

## Card CSS (as shipped)

```css
.card { position: absolute; left: 100px; top: 470px; width: 880px; padding: 52px 58px; }
.card-light { background: #f4f0e5; border: 1px solid #d9cfae; box-shadow: 0 18px 60px rgba(0,0,0,0.55); }
.card-dark   { background: #17171b; border: 1px solid #33333b; box-shadow: 0 18px 60px rgba(0,0,0,0.65); }
.card .ts {
  font-family: ui-monospace, Menlo, monospace;
  font-size: 29px; letter-spacing: 0.22em; margin-bottom: 26px;
}
.card-light .ts { color: #8a7648; }
.card-dark  .ts { color: #9a917e; }
.card .cbody { font-family: "Source Serif 4", serif; font-size: 50px; line-height: 1.38; }
.card-light .cbody { color: #191914; }
.card-dark  .cbody { color: #f2efe6; }
.red { color: #d43d2a; }
```

## Card semantics — the grammar

- **Light card** = an offer, an ask, a confirmation, the campaign's own voice:
  `SEP 9 · 5:09 AM ET` / "The vendor offers: confirm, and they will cancel the
  seat and refund the **$250**."
- **Dark card** = a denial, a refusal, an admission, the opponent's voice:
  `SEP 10 · 11:58 AM` / "The vendor's answer: <span class=red>**no refund.**</span>"
- **Red appears exactly twice in the 60s reference build** — on the two refusal beats
  ("no refund.", "And still say no." on the admission). Nowhere else. That
  restraint is the point.
- Body quotes are **verbatim** from the campaign record, including the user's
  own exact wording ("yes a downgrade and refund please." — lowercase, as sent).
- **Silence is a card too:** the reference build closed beat 4 with an empty inbox
  glyph — a bordered rectangle with three hairline dividers, no text — under
  the line about the unanswered demand. The absence is the evidence.

## Beat map (reference build, 60s, 5 beats)

| Beat | Range | Visual | Audio |
|---|---|---|---|
| 1 | 0–6.1s | Presenter on camera (silent body clip) | Beat-1 VO |
| 2 | 6.5–25.2s | Slug line + cards A–D (light): offer → reply → ask-again → confirmed | Beat-2 VO |
| 3 | 25.6–36.8s | Cards E–F (dark): refusal → admission of acceptance + still no | Beat-3 VO |
| 4 | 37.2–48.5s | Cards G–H (dark): formal demand → promise; then the empty-inbox glyph | Beat-4 VO |
| 5 | 48.9–58.3s | Presenter back on camera | Beat-5 VO |
| End card | ~58.3–61s | Brand seal, motto, campaign URL; QR only when URL verified | Music reads up |

## Timing mechanics

Card in/out points are computed from **Scribe word timestamps**, not guessed:
a builder script walks the beat transcripts, finds anchor words (timestamps
spoken in the VO — "6:43", "6:55", "7:21", "September", "silence"), and backs
each card's start 0.08s before its first word, floor-clamped to the previous
card's end + 0.1s. (The reference build's timing script was `generate_cut.py`.)

## Adaptation rule for new campaigns

Map the campaign's document timeline onto the 5 beats: **opening → the offer
(light cards) → the refusal (dark cards) → the demand + silence → close.**
The presenter anchors beats 1 and 5; the evidence owns the middle. If the
campaign's timeline doesn't fit that arc, the script doesn't fit the lane —
rework the script, not the card grammar.
