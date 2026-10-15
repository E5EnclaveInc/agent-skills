# Character Sheet Layout — Sovereign Couture Atelier Document

The composed sheet is a single 4:5 vertical board (1200×1500). Black ground
(#0a0a0a), gold light (#d6a84b / #ecd9a4). This is the section-by-section
spec the spec-JSON must fill. Adapted from a source prompt; every
section below is mandatory unless the garment genuinely lacks the subject.

## 1. Masthead
- Atelier crest (small, left — your own mark at `assets/crest.webp`; omit if none), eyebrow `ATELIER SOVEREIGN · CHARACTER SHEET` in
  Plex Mono caps, sheet title in Cormorant Garamond (the garment's name),
  one-line house descriptor, thin gold hairline rule.
- The crest is the document's authority mark — this is a technical atelier
  document, not a volume; the masthead seal is correct here.

## 2. Hero visualization
- The AI-reconstructed floating garment / invisible-mannequin presentation,
  full garment top to bottom, on black. Numbered gold markers (01–NN) pinned
  at the callout anchor coordinates.
- The markers are the only overlay on the hero. No captions on the image.

## 3. Design breakdown (callouts)
- 6–10 numbered callouts, gold numerals, Plex Sans body. Each: a tight
  technical identification + one line of construction/fabric reading.
- Use only categories actually present: main garment · collar/neckline ·
  sleeve/cuff · fabric & texture · pattern/print/embroidery · closure/hardware
  · lower garment · accessories/footwear · distinctive detail.
- Callout text is specification, not marketing. Name what is there.

## 4. Material & detail panel
- 3–5 crops of the SOURCE REFERENCE (real photographs via CSS crops —
  never regenerated close-ups): fabric texture, stitching, embroidery,
  buttons/hardware, print, seams, trims.
- Small numbered labels beneath each crop. These are evidence, not art.

## 5. Color palette
- 4–7 circular swatches with professional names (Ivory, Charcoal, Burgundy,
  Olive, Navy, Sand, Black…). Only colors in the garment. Hexes measured
  from the reference via `bin/sample_palette.py`; names assigned by the
  atelier, never invented.

## 6. Coordinate Note
- 3–5 sentences: styling direction, silhouette, layering, visual balance,
  the relationship between pieces, the distinctive design language.
- Written through Black American fashion lineage — see
  `references/editorial-voice.md`. Editorial, concise, reverent.

## 7. Appeal Point
- 4–6 short design highlights: what makes the garment visually distinctive
  (silhouette, contrast detailing, tailoring, hardware, pattern placement,
  proportion, finishing). Grounded in the actual reference.

## 8. Styling Logic
- 2–4 sentences: how the pieces work together visually and why the
  combination creates the look. Fashion-editorial register.

## 9. Typography & graphic discipline
- Display: Cormorant Garamond (self-hosted woff2, embedded). Body: IBM Plex
  Sans. Labels/eyebrows: IBM Plex Mono caps. Thin gold hairline dividers,
  generous negative space, strict hierarchy. Never hotlink a font CDN.

## 10. Footer
- Gold hairline, the crest small, `NIL SATIS NISI OPTIMUM` in tracked caps,
  provenance line: `Reference image > creative interpretation · Reconstructed
  with fidelity · Atelier Sovereign`.

## Spec JSON shape
```json
{
  "title": "The Pegasus Bomber",
  "house_line": "A black satin bomber carrying the winged guardian in gold thread.",
  "hero": "/abs/path/hero.webp",
  "reference": "/abs/path/reference.webp",
  "callouts": [{"n":"01","title":"Main garment","body":"…","x":50,"y":30}],
  "details": [{"label":"Embroidery","caption":"…","x":0.30,"y":0.35,"w":0.25,"h":0.20}],
  "palette": [{"name":"Obsidian","hex":"#0b0b0c"}],
  "coordinate_note": "…",
  "appeal_points": ["…"],
  "styling_logic": "…"
}
```
- Callout `x`,`y` are percentages on the hero. Detail `x`,`y`,`w`,`h` are
  fractions of the reference image. Compose with
  `python3 bin/compose_sheet.py spec.json sheet.html`.
