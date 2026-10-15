# Budgets and Phase Gates

Every figure below was set by the AgriMesh Signal Lab war room and is load-bearing. Numbers survive only with their kill reasoning attached — see the War Room Log for why each exists.

## Motion payload budgets

- Total motion payload (film JS + hero canvas JS): **≤80KB**.
- GSAP vendored (never CDN at runtime). Zero external runtime loads except the site's existing ones (e.g., Turnstile).
- Per film: **≤160 animated DOM nodes**, `transform`+`opacity` only, **≤15MB** memory, **<120ms** init on iPhone 12-class, 60fps desktop / ≥30fps iPhone.
- Hero canvas: ≤960×540 backing store (DPR 1, CSS-scaled), 30fps cap → 15fps after 60s on-screen, ~25MB total including the poster; JS ≤20KB. Poster remains the LCP element; mobile shows poster-first on throttled connections.
- Grain: tiled PNG ≤3KB, `mix-blend-mode: overlay`, opacity ~.05 — never full-frame canvas grain.
- All films gated on visibility (IntersectionObserver, threshold 0.2, 200px prefetch margin) and `document.hidden`; one shared rAF ticker for packet dots; init deferred to `requestIdleCallback` where available. A 2500ms watchdog must confirm first-frame-rendered.

## Fail-open chain (top-down)

```
FILM (GSAP-timeline SVG in .film-frame)
  → STATIC SVG + in-frame bug (reduced-motion, GSAP absent, init throws, watchdog fires)
    → CAPTION-ONLY (SVG asset fails — <figure> keeps figcaption + honest label)
```

`prefers-reduced-motion` gates init at the door; feature gate (`window.gsap` + `IntersectionObserver`); try/catch on init with `.film-static` class fallback; `<img>` error handlers preserving the caption; `noscript` = today's page.

## Copy lint (blocking gate, every phase)

- Every capability sentence carries proposed / designed / under development, or a conditional verb.
- Freeze the fenced copy as a diff baseline in Phase 0; zero drift thereafter.
- No "live" grammar anywhere (pulse beacons, ticking counters, dashboard chrome, status dots).
- No third-party stat that collapses in View Source — rewrite honestly or remove.
- Federal identifiers (where applicable) present and verified against the source of truth.

## Phases (each independently shippable and killable)

| Phase | Scope | Ship gate (all must pass) |
|---|---|---|
| **0 — Guards first** | Copy lint, identifiers, no live grammar, frozen copy baseline | Copy diff clean; identifiers present; reviewer phone visual check |
| **1 — Film frames** | `.film-frame` chrome as pure HTML/CSS; CSS-only hero entrance | Zero bytes of new media; reduced-motion shows labeled end-state |
| **2 — OPS REPLAY** | First timeline + scrubber + replay, iPhone-validated before proceeding | ≥30fps iPhone; <120ms init; watchdog green; fallback chain exercised on purpose (kill GSAP → static + bug) |
| **3 — Scan + edge** | Treatments 2+3 as variations on the same module | Same gates; all films stay under per-film budgets |
| **4 — Hero motion** | Instrument canvas + telemetry rail + grain; single CTA; badges moved to evidence | Hero budget met; LCP still poster; mobile poster-first on throttled connections |
| **5 — Section polish** | §-coded eyebrows, temperature-graded bands, evidence-desk, honest confessional chapter | Palette temperatures verified; chapter indicator present; red lines re-checked |
| **6 — Measure** | Pre-committed falsifiable metric, cohort comparison, 90-day clock | Baseline captured; falsification thresholds armed |

**Verification ritual, every phase:** budgets measured on the reviewer's phone (final visual authority); reduced-motion confirmed; honesty labels confirmed at every fallback level; red lines re-run as blocking checks. A failed phase ships never — the page is a complete honest document at every phase boundary.

## Red lines (blocking ship-gate checks)

No autoplay video anywhere; no video asset over 2.5MB/10s; no photorealistic renders of nonexistent hardware; no timecode grammar; no live-system grammar; no present-tense capability claims; no motion whose honesty label lives only in surrounding copy; no dawn film on the instrument register; no baked mutable facts; no perpetual ambient loops; no scroll-jacking; no third-party media embeds; no removal of the identifiers table.
