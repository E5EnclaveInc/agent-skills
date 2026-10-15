---
name: living-mesh-cinematic
description: "Make a page cinematic with a living nodal-network simulation — breathing nodes, pulses routing along edges, circuit traces lighting as current passes, and periodic node failure/rerouting/recovery that teaches the system's story. Use when a page needs continuous ambient motion that demonstrates how something behaves (failover, routing, resilience) rather than a play-once film replay."
license: MIT
metadata:
  version: 1.0.0
---
# Living Mesh Cinematic

## Purpose

Give a page the cinematic register of a **living system**: a continuous ambient
nodal-network simulation where the motion *is* the explanation. Where
signal-lab-cinematic mounts schematics as play-once film replays inside
instrument frames, the living mesh runs a small world that never stops —
nodes breathe, traffic routes, circuits light, and every so often something
fails and the mesh routes around it. The viewer learns the system's behavior
by watching it behave.

The core rule: **the simulation must teach the page's story.** A mesh that
just shimmers is decoration and does not ship. Every behavior in the loop
(node drop → reroute → recovery, pulse routing, trace currents) must map to
something the page claims about how the system works.

## When to trigger

- A page's story is about resilience, routing, failover, coverage, or flow —
  and a static diagram can only assert it, not show it.
- The founder asks for a "nodal network / mesh network" treatment, "bring the
  circuit board to life," or ambient living motion on a dark field.
- A hero or section needs continuous motion that rewards a long look, not a
  4-second show (see failure modes).

**When NOT to trigger:** the story is measurement, evidence, or audit — that's
signal-lab-cinematic's instrument register (play-once labeled replays). The
story is emotional, documentary, or poetic — that's the dawn-film register.
The company has a live system with real data — a simulation would be
vaporware signaling; show the real thing or don't animate.

## Workflow

### Step 1 — Name the story the motion teaches (one sentence)

Before any code: "watching this for 30 seconds teaches the viewer ___."
Examples: "that a dropped node doesn't drop the network," "that current
reaches every trace," "that traffic reroutes around congestion." If the
sentence is "that we're high-tech," stop — that's decoration.

### Step 2 — Build the small world (vanilla canvas, zero CDN)

Construction recipe in `references/technique.md` — the proven build:
deterministic seeded field (mulberry32) so every load composes the same frame;
node count scaled to viewport area (40–96); distance-threshold links; breathing
nodes (sine phase per node); ≤9 pulses random-walking live edges at fixed
px/s with short trails; 4 Manhattan circuit traces with a current head and
Gaussian brightness falloff; a drop cycle every ~11–20s (dropping → down →
reviving with flare → up) that only targets nodes with ≥2 live neighbors so
the mesh never partitions. Pulses whose target goes dark mid-flight reroute
off live edges — the failover story, told by the routing itself.

### Step 3 — Fence it honestly

- **Labels are plain HTML with `animation:none`.** A visible tick states
  `SIMULATED MESH · NN NODES · DESIGNED BEHAVIOR`; during a drop it reads
  `…NODE DOWN · REROUTING…`. A permanent bug reads `AMBIENT SCHEMATIC ·
  ILLUSTRATIVE`. Deduped DOM writes (only update on change).
- **No LIVE grammar.** No pulse beacons implying a live system, no ticking
  counters, no "real-time." Everything simulated is labeled simulated.
- **Screen readers:** the visible tick is `aria-hidden`; a visually-hidden
  live region announces state changes (drop/restore) only — never the
  ambient churn.

### Step 4 — The fallback chain is subtractive

1. **Offscreen:** `IntersectionObserver` (threshold 0) stops the rAF chain;
   resumes on return. Never burn frames nobody sees.
2. **Reduced motion:** the explicit `prefers-reduced-motion` preference — and
   ONLY it — freezes the mesh. It gets one composed frame (the deterministic
   seed drawn once, e.g. t=1.7), the full labeled narrative, never a lesser
   experience. See `references/failure-modes.md` for why heuristics
   (hardwareConcurrency, saveData, play-once-then-freeze) are banned: they
   froze the hero on real iPhones whose owners never asked for stillness.
3. **No JS:** an SVG poster in the same palette, painted under the canvas in
   CSS. The poster IS the composed frame's still.

### Step 5 — Budget it, then verify on a real phone

- Hero mesh JS ≤20KB (proven: 13,231 raw / 4,758 gzip, vanilla canvas).
- Total page motion ≤77KB (proven total: 27,088 raw / 8,483 gzip).
- DPR capped at 2; dt clamped (≤0.05s) so background-tab returns don't jump.
- Verification: headless frame-run (thousands of frames incl. a full
  drop→revive cycle + offscreen pause/resume), served-bytes check for the
  honesty labels, and a real phone (the reviewer's) as final visual authority.

## Output Contract

1. The one-sentence story the motion teaches, agreed before code.
2. The treatment spec: world parameters (node/link/pulse/trace counts,
   timings), label/tick/state strings, fallback states.
3. Measured payload (raw + gzip) against the budgets above.
4. Fallback proof: reduced-motion frame, no-JS poster, offscreen pause —
   each exercised on purpose, not assumed.
5. Honesty proof: simulated-behavior labels present in served bytes at every
   fallback level.

## Operating Rules

1. **Motion teaches or it doesn't ship.** Decoration is never a deliverable.
2. **Continuous ambient, never play-once-then-freeze.** A show with an ending
   guarantees most viewers see only the after-state.
3. **Only the explicit reduced-motion preference freezes motion.** No device,
   core-count, data-saver, or battery heuristics — those are not accessibility
   settings and they misfire on real phones.
4. **Deterministic seed.** The composed field must be identical every load —
   the reduced-motion frame and the no-JS poster are the same composition.
5. **The mesh never partitions.** Drop logic must keep the network connected
   (minimum live-neighbor guard); a dead mesh teaches failure, not resilience.
6. **Vanilla canvas, zero CDN, DPR ≤2, dt clamped.** No framework, no
   network dependency, no background-tab time jumps.
7. **Never the poetic register, never the instrument register.** If a
   sibling page owns dawn-film or signal-lab, this page does not borrow
   their grammar — shared cinematic language blurs entities.
