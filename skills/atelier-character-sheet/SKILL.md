---
name: atelier-character-sheet
description: "Turn an outfit reference image into a professional Sovereign Couture fashion character sheet: AI-reconstructed garment visualization on black, with crisp HTML-composed callouts, material crops, color palette, and editorial notes written through Black American fashion lineage. Trigger when the user wants a character sheet, design spec board, or outfit breakdown for a garment."
license: MIT
compatibility: "Requires an image-generation tool and a headless Chrome/Chromium for the sheet screenshot."
metadata:
  version: 1.0.0
---
# Atelier Character Sheet

## Purpose
Produce a single polished 4:5 vertical fashion character sheet for any outfit reference: the garment reconstructed with absolute fidelity as a floating-garment visualization on black, surrounded by crisp real-type callouts, true-photograph material crops, an extracted palette, and editorial notes in the house voice. House style throughout — black is the ground, gold is the light — never the ivory default.

## Workflow
1. **Read the reference.** Open the image yourself. Catalog: garment type, silhouette, colors, fabric, prints/motifs, collar/neckline, sleeves/cuffs, closures/hardware, pockets/seams, layering, accessories, distinctive details. Note which parts are obscured.
2. **Generate the hero visualization (ONE image call).** Use your image-generation tool with the output directed to the working directory (a build asset, not a media library). Prompt = the reference image first, then this text:
   > "Reconstruct this exact garment as a premium floating-garment product visualization: invisible-mannequin presentation, full garment visible top to bottom, on a pure black studio ground with a warm gold rim light. Preserve the reference's exact design identity — silhouette, proportions, colors, prints, embroidery, construction, hardware — with zero redesign, zero beautification, zero added elements. Photorealistic fabric behavior, sharp edges, natural shadows. No text, no watermark, no logo, no human model, no background scenery."
   
   If the reference is already a clean isolated garment presentation, the hero may be a fidelity pass on the same presentation rather than a reinvention. Verify the result by reading it before proceeding.
3. **Extract the palette.** Run `bin/sample_palette.py <reference>` for measured dominant colors; assign professional names yourself (Ivory, Charcoal, Burgundy, Olive, Navy, Sand, Black…), 4–7 swatches, only colors actually in the garment.
4. **Write the spec JSON.** Sections per `references/character-sheet-layout.md`. Callout anchors are x/y percentages on the hero. Detail crops are fractional regions of the *source reference* (real photographs — never regenerate close-ups; CSS crops preserve absolute fidelity). Editorial copy (Coordinate Note, Appeal Point, Styling Logic) follows `references/editorial-voice.md`.
5. **Compose.** `python3 bin/compose_sheet.py spec.json sheet.html` — emits one self-contained HTML file (fonts embedded, plus your crest from `assets/crest.webp` if you add one; no network). Then screenshot it: `chrome-headless-shell --headless --screenshot --window-size=1200,1500 sheet.html`, read the screenshot, and fix layout or copy issues (one correction pass; never re-render the hero to fix text).
6. **Deliver.** The sheet.html is the artifact. Present it with a link or path your runtime supports.

## Output Contract
- One self-contained vertical HTML character sheet, 1200px wide: masthead (your crest at `assets/crest.webp`, optional), hero visualization, numbered gold callouts, material/detail crops from the true reference, color palette, Coordinate Note, Appeal Point, Styling Logic, footer with "Nil Satis Nisi Optimum."
- Format note: the board is width-locked at 1200px and extends vertically as the breakdown requires. The source prompt's "4:5" was a constraint of the image-model medium; real type at readable sizes needs real room — never shrink text to force an aspect ratio.
- All annotation type is real HTML text — never rendered by the image model.
- The garment is never redesigned: reference image > creative interpretation.

## Operating Rules
1. **Absolute accuracy rule.** Do not change garment identity, silhouette, color, pattern, proportions, construction, or distinctive details. Reconstruct obscured portions only, staying consistent with the visible design.
2. **Text lives in HTML, never in pixels.** The image model renders the garment only. If the hero comes back with garbled text or watermarks, regenerate the hero — never try to fix type inside the image.
3. **Black American focus, design language not costume.** Editorial sections speak through Black American fashion lineage (see references/editorial-voice.md). Never stereotype. If a human form is needed for presentation, Black models — described with dignity, never exoticized.
4. **Gold is earned (§3.2).** Gold hairlines, numerals, and the crest carry the ceremony; the ground stays black. Never a light/ivory board.
5. **Max one hero generation per sheet** unless the hero is visibly wrong (wrong garment, wrong colors). Copy/layout fixes happen in the HTML, not in re-renders.
6. **Universal adaptation.** Works for menswear, womenswear, childrenswear, unisex, formal, streetwear, uniforms, cultural dress, bridal, fantasy, historical, single garments or full outfits. Include only sections relevant to what's actually present; never invent accessories.
7. `$0. No paid services, no external requests in the artifact.`
