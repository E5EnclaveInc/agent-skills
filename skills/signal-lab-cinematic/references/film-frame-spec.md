# Film Frame Spec

The `.film-frame` is the shared framing device for every diagram-as-film. It is a letterboxed panel around an existing SVG schematic. Pure HTML/CSS in Phase 1; the GSAP timeline later plays *inside* it.

## Chrome layout

- **Top-left:** figure title — `FIG.01 — MESH TOPOLOGY`. Tiny mono, low emphasis.
- **Bottom-left:** the bug — `SIMULATED · DESIGNED BEHAVIOR`. Plain HTML overlay. `animation: none !important`. Never fades, never scrolls away, never animates. It must survive screenshots, print, and JS-off. This is the honesty invariant.
- **Top-right:** telemetry stamp — `FRAME 0642 · STATE STABLE`. Instrument grammar: frame counts, link margins, state words. Never a clock time, never "LIVE," never a timecode (timecodes imply a recorded event — banned by the red team).

## Rules

1. The SVG inside the frame is the original schematic, unaltered at rest. Animations are additive layers; the end state equals the static document.
2. The bug is plain DOM text in served bytes — not canvas-drawn, not image-baked, not JS-injected. JS-disabled / no-JS = today's page with the bug.
3. Native controls only for replay machinery: `<input type=range>` labeled `REPLAY SCRUBBER` bound to `timeline.progress(v)`, keyboard-operable, plus play/pause and a `↻ REPLAY` button that appears after the first pass.
4. Frames respect `prefers-reduced-motion` at the door: no init of the timeline, labeled end-state shown, replay button present.
5. Breakpoints: the chrome must not overlap the SVG at 390px width. Figure titles truncate before they collide.
6. Parallax is banned on film frames — decorative layers may drift, but nothing that could separate the honesty bug from its frame.

## Verbatim AgriMesh instance

Top-left `FIG.01 — MESH TOPOLOGY` / `FIG.02 — ROW-LEVEL SENSING` / `FIG.03 — ON-FARM INSIGHT`; bottom-left bug amber, `SIMULATED · DESIGNED BEHAVIOR`; top-right `FRAME 0642 · STATE STABLE`. Dark letterbox on near-black, leaf `#8fc39a` / amber `#d9a441` drafting palette.

## The three words that are never in a frame

**LIVE. NOW. ACTUAL.** Any of these in chrome copy is a ship-gate failure.
