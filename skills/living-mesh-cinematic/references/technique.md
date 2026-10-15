# Living-mesh technique reference

Extracted from the proven build: `svc-hero.js` (13,231 bytes raw),
a production services-page hero (2026). Vanilla canvas, zero CDN.

## Palette

- Blue: `56,189,248` (electric blue) — 55% of nodes, links, traces.
- Green: `52,211,153` — 45% of nodes, 60% of pulses.
- Ink: `6,10,18` — dark field. Pulse head highlight: `190,230,255`;
  revive flare: `235,242,255`.

## World construction

- **Deterministic PRNG:** mulberry32, seed `0xE5E5`, reset on every seed.
  The initial field is identical on every load — this is what makes the
  reduced-motion frame and the no-JS poster the *same* composition.
- **Nodes:** count = `clamp(40, 96, floor(W*H/24000))` — scales with viewport
  area. Each: random pos, radius 1.6–4.0, random phase, blue/green coin flip,
  state `up`.
- **Links:** all pairs within `linkDist = clamp(120, 190, W/8)` px.
  Drawn with alpha `(1 - d/linkDist) * (0.04 + 0.30 * min(endpoint health))` —
  links fade near a dying node before it drops.
- **Breathing:** per frame, `br = 0.5 + 0.5*sin(t*0.9 + phase)`; radius ×
  `(0.8 + 0.4*br)`, alpha `(0.25 + 0.65*(0.45 + 0.55*br)) * health`, plus a
  halo ring at `r + 5 + 2*sin(...)`. Slow (0.9 rad/s) — calm, not frantic.

## Pulses (traffic)

- Cap `PULSE_N = 9`; spawner ticks every 0.5s and tops up only below cap.
- Speed fixed at `PULSE_PX = 170` px/s — `p.t += dt * 170 / edgeLength`, so
  pulses move at constant *speed*, not constant *progress* (long edges take
  longer; this reads as physical).
- Trails: draw segment from `t-0.07` to `t` (3px, alpha .35) + head dot
  (2.2px, alpha .95).
- Routing: random walk over *live* neighbors. On arrival at node B: if B went
  dark mid-flight, pick another live neighbor of A and restart the edge;
  else continue from B to a random live neighbor. Dead end (no live
  neighbors) → despawn. **The reroute is the failover story** — no separate
  "rerouting" animation needed; the traffic visibly goes around the hole.

## Circuit traces (the circuit board coming to life)

- 4 traces; each a Manhattan (right-angle) polyline: 4–7 segments,
  50–180px each, alternating axis, clamped inside the field.
- A current head travels each trace at 240–360 px/s. Segment brightness gets
  a Gaussian boost around the head: `exp(-((m - head)^2) / 9800)` on top of a
  0.08 dim baseline; segments near the head also go 2px wide.
- Head dot (2.6px, near-white) + halo (7px, blue .28).
- After the head clears the trace (+140px overshoot), the trace rests 5–13s
  before the next current. Traces are drawn *under* the mesh.

## Drop cycle (the story beat)

- Timer: first drop at 8–16s, then every 11–20s (`t + 11 + rnd*9`).
- Target selection: random node with state `up` AND ≥2 live neighbors —
  **the mesh never partitions** (20 tries, else retry in 6s).
- States: `dropping` (0.9s, health → 0.06) → `down` (2.6–4.6s, health 0.06,
  links faded) → `reviving` (1.1s, health → 1, flare 1 → 0, expanding ring)
  → `up`.
- Tick + live region update on drop ("A node dropped. Traffic rerouted.
  Simulated.") and restore ("Node restored. Mesh whole. Simulated.").

## Honesty architecture

- Tick element: `SIMULATED MESH · {NN} NODES · DESIGNED BEHAVIOR`, or
  `SIMULATED MESH · NODE DOWN · REROUTING · DESIGNED BEHAVIOR` during a drop.
  Deduped writes (update only on change). `aria-hidden="true"`.
- Separate visually-hidden live region announces drop/restore only.
- Permanent bug (plain HTML, `animation:none`): `AMBIENT SCHEMATIC ·
  ILLUSTRATIVE`.
- Reduced-motion: tick `SIMULATED MESH · DESIGNED BEHAVIOR`, status
  "Mesh schematic. Motion off. Simulated."

## Loop hygiene

- `dt = min(0.05, (ts - lastTs)/1000)` — clamps background-tab returns.
- `IntersectionObserver` threshold 0: `isIntersecting ? start() : stop()`.
  No fallback → start (fail toward motion, not stillness).
- `resize`: DPR capped at 2 (`Math.min(2, devicePixelRatio)`); node positions
  scale proportionally; links/traces rebuilt; pulses cleared.
- Reduced-motion: `still` drawn once at `t = 1.7` (a lively but composed
  moment), no rAF chain at all.

## Kinetic type (optional companion)

Staggered word-ramp on the H1: split words into spans, `transition-delay:
ix*90 + 900ms`, add class on double-rAF. Under reduced-motion, apply the
final class immediately (no stagger).
