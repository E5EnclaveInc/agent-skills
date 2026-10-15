---
name: signal-lab-cinematic
description: "Make a technical or corporate page cinematic in the laboratory/instrument register — diagrams become labeled, play-once film replays with permanent honesty bugs, telemetry stamps, and fail-open fallbacks. Use when a site reads as a landing page, when diagrams describe instead of demonstrate, or when asked for cinematic motion that is evidence-grade rather than poetic."
license: MIT
metadata:
  version: 1.0.0
---
# Signal Lab Cinematic

## Purpose

Give a technical corporate page the cinematic register of a **high-technology laboratory**: motion as *measurement*, not poetry. The page stops reading as a landing page when it stops selling and starts *demonstrating* — schematics become short, labeled, play-once film sequences inside instrument frames.

The core rule: **if a motion can't carry a label, it doesn't ship.** Every animation must teach the reviewer something the static version cannot.

## When to trigger

- A corporate/technical page reads as a landing page (conversion scaffolding, static schematics, one flat palette, zero motion).
- "Bring the diagrams to life through video" — but do it code-regenerably (GSAP-timeline SVG), never baked video.
- A site must look cinematic without copying a sibling site's poetic/documentary treatment (the entity-blur problem).
- Anything pre-revenue where autoplay loops would imply a live system (vaporware signaling).

**When NOT to trigger:** the ask is documentary, emotional, or poetic motion — that's the dawn-film register, a different skill. When the company has a live system with real data to show (different honesty posture).

## Workflow

### Step 1 — Diagnose like a red team

Score the live page against these landing-page tells: conversion scaffolding (dual CTAs, badge strips, card grids, FAQ, newsletter footer) instead of editorial architecture; static schematics identical in visual weight (describe, not demonstrate); one palette/temperature/rhythm from hero to footer (attention never resets); hero with more than one thing competing in the eyeline; zero state changes; backstory openings (who we are before the strongest moment). Record which tells are present — they are the redesign's brief.

### Step 2 — Fix the register, not the palette

Choose instrument grammar over poetry grammar:

| Poetic register (don't reach for this here) | Instrument register (this skill) |
|---|---|
| Lyric hero fragments | Section codes (§01, §02…) |
| Film timecodes (imply a recording) | Telemetry stamps (`FRAME 0642 · LINK −3 dB`) |
| Chapter kickers | Figure titles (`FIG.01 — MESH TOPOLOGY`) |
| Mood light | Per-section color temperature (cold evidence → warm document → human night) |
| Free-play simulation | Fenced, play-once replay console |
| Present-tense claims | Conditional/fenced verbs: designed, proposed, under development |

Light carries classification. Motion carries mechanism.

### Step 3 — Frame every diagram as film

Mount each SVG schematic in a **`.film-frame`** — a letterboxed panel with permanent, non-animated, in-frame chrome:

- **Top-left:** the figure title.
- **Bottom-left:** the bug `SIMULATED · DESIGNED BEHAVIOR` — plain HTML overlay, `animation:none`, never fading, never scrolling away, must survive screenshots and JS-off.
- **Top-right:** a telemetry stamp in instrument grammar — never a clock time, never "LIVE."

The fallback chain is *subtractive*: kill the animation → the static schematic plus the bug is today's honest page. See `references/film-frame-spec.md`.

### Step 4 — Animate the schematics themselves

The SVGs *are* the films. GSAP-timeline DOM animation only — text stays text (selectable, zoomable, screen-reader-legible). Three canonical treatments (beat structures in `references/treatments.md`): **OPS REPLAY** (failure → honest gap → reroute → settle → replay button), **TRANSECT SCAN** (survey sweep, synthetic values tagged `SYNTH`), **EDGE LOOP** (processing pulse, severed-cloud flicker). Each 7–9s, play-once on scroll-entry, ≤160 animated DOM nodes, `transform`+`opacity` only. The 600ms honest gap (detection takes time) is a required beat wherever failover is shown.

### Step 5 — Budget every motion, gate every phase

Phases are independently shippable and killable: **0 guards** (copy lint, identifiers, no live grammar, frozen baseline) → **1 frames** (chrome as pure HTML/CSS, zero new media) → **2–3 treatments** (each validated on a real phone before proceeding) → **4 hero motion** (poster-first canvas instrument layer) → **5 polish** → **6 measure** (pre-committed falsifiable metric before code). Full budgets and the gate table are in `references/budgets-and-gates.md`. If a phase fails its gate, it ships never — the page is a complete honest document at every phase boundary.

## Output Contract

Any agent running this skill must deliver, per phase:

1. A diff of what changed (file → change).
2. A per-gate verification table with **measured** numbers (fps, init ms, fallback states exercised on purpose — kill GSAP, disable JS, enable reduced-motion), not vibes.
3. Proof of the honesty invariant: the bug present at every fallback level, in served bytes.
4. A staging URL and a one-screen human review brief (what to look at, what is intentionally static, what question the reviewer must answer).
5. Production untouched until the human's word.

## Operating Rules

1. **No LIVE grammar.** Pulse beacons, ticking counters, dashboard chrome, autoplay loops, and timecodes are banned — a company with no deployed system must not imply one.
2. **No present-tense capability claims.** Everything conditional or fenced; diff capability copy against a frozen baseline each phase.
3. **Nothing bakes mutable facts.** Status, dates, identifiers stay as DOM text; motion must be code-regenerable, never baked video.
4. **Reduced-motion parity.** Reduced-motion users get the complete labeled narrative — never a lesser experience; the bug is the one element on the page with zero motion.
5. **Budgets are load-bearing.** Total motion payload ≤80KB; per film ≤15MB memory, <120ms init on iPhone 12-class, 60fps desktop / ≥30fps iPhone; hero canvas ≤20KB JS, poster stays LCP.
6. **Never conflation.** If a sibling site owns the poetic/dawn register, this one does not borrow it — shared cinematic language blurs entities.
7. **One human review pass per phase, timeboxed** — a real phone is the final visual authority.
8. Work from the canonical build; never from stale iterations (tag stale dirs `DO_NOT_SHIP` rather than deleting evidence).
