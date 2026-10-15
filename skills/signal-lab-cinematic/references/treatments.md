# Diagram-to-Film Treatments

Three canonical treatments, derived from the AgriMesh Signal Lab. Each is a GSAP-timeline animation of an existing SVG schematic inside a `.film-frame` (see `film-frame-spec.md`). 7–9s, play-once on scroll-entry (IntersectionObserver), ≤160 animated DOM nodes, `transform`+`opacity` only, easings `power2.inOut` / `expo` (never elastic, back, bounce, float, spring, marquee). Adapt the beats; keep the structure.

## Treatment 1 — "OPS REPLAY" (failure-and-recovery)

For any self-healing / redundancy / failover diagram. One 8.4s pass with a native scrubber:

1. **0.0–1.5s — Steady state.** All nodes breathe (scale/opacity stagger, yoyo); links hold.
2. **1.5s — Failure.** One node fails: amber X draws on, node dims, its links grey out. Ticker: `T+00:01.5 — NODE-09 LOST · 3 LINKS DOWN`.
3. **1.9–2.5s — The honest gap.** Nothing happens for 600ms. Detection takes time; the pause is the story of failover cost. Ticker: `RECOMPUTING ROUTE…`.
4. **2.5–5.5s — Reroute.** Packet dots (≤8) travel dashed reroute paths via `getPointAtLength` on a shared rAF ticker; links along the path light amber. Ticker: `REROUTE VIA <coords> · 0 PACKETS LOST (DESIGNED)` — the `(DESIGNED)` tag is mandatory: zero-loss is a design target, never a measurement.
5. **5.5–7s — Settle.** Nodes return to breathing green. Ticker: `MESH STABLE · NO SINGLE POINT OF FAILURE`.
6. **7–8.4s — Idle. No loop.** A `↻ REPLAY` button appears in the chrome.

## Treatment 2 — "TRANSECT SCAN" (survey / sensing sweep)

For any row-level sensing, scanning, or survey diagram. A scan is a sweep, not a timeline — no scrubber. One 7s pass:

1. A horizontal scanline (thin amber, soft gradient trail) descends from the hub toward the rows over 0–2s.
2. As it passes each sensor's y-coordinate, the dot flashes and fires its dotted reporting line to the hub (stroke-dashoffset draw).
3. Readout rows fill in mono DOM text beneath the frame: `ROW A · 23.4% VWC · 21.6°C · SYNTH` — **every synthetic value carries a `SYNTH` tag.** Satisfies curiosity without fabricating data.
4. **6–7s:** hub pulses twice; ticker: `AGGREGATED ON LOCAL HUB · UPLINK NOT REQUIRED`.

## Treatment 3 — "EDGE LOOP" (on-device / local-first intelligence)

For any edge-compute, local-inference, or offline-first diagram. One 9s pass:

1. Dots flow FIELD → ON-DEVICE along the input lines.
2. The device box shows a processing pulse (inset rect strobing 3× at 300ms) with ticker `INTERPRETING (DESIGNED)` — drafting-register pulse, never an "AI thinking" brain icon.
3. Dots flow ON-DEVICE → USER along the guidance line; the user glyph receives them (single expanding ring).
4. The severed uplink: the dashed cloud link flickers once, an amber X marks it; ticker: `UPLINK ATTEMPT — NOT REQUIRED · DROPPED BY DESIGN`. Dramatizes "optional, never required" without claiming unmeasured behavior.
5. Settle to the static end state — identical to the original SVG.

## Beat rules shared by all treatments

- The honesty bug never participates in the animation.
- The honest gap (a beat of nothing during failover/detection) is required wherever recovery is shown.
- All outcome claims carry `(DESIGNED)` or `SYNTH` tags — dramatize *designed behavior*, never documented performance.
- Re-entry resumes; only the replay button restarts.
