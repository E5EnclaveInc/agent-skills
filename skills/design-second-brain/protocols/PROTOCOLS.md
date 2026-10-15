# Design Protocols — canonical rules

Source: standing doctrine (ratified by the user across 2026-09-10 → 2026-09-12) plus the
cinematic-hero rule (`protocols/CINEMATIC_HERO_RULE.md` — `status: ratified`,
RATIFIED by the user 2026-09-12; verified doctrine).
Every rule below is enforceable: each carries a check so a gate runner can pass/fail it.

## P1 — Cinematic heroes go all out
Heroes get cinematic hero sections: real motion, custom icons, 3D where it serves,
gold leaf where it fits the brand. Always the best foot forward, heroes in particular.
*Check: the hero is a designed set-piece, not a headline + stock image. It reads as
cinematic at first paint, with motion that starts on view. Full enforceable
criteria: `protocols/CINEMATIC_HERO_RULE.md` (ratified by the user 2026-09-12 —
canonical doctrine).*

## P2 — Real motion only, honest budgets
Motion is real (GSAP-directed, DOM-first) and budgeted: ~zero ambient motion except
honest progress indicators (e.g. the sending-progress sweep, visible only while a real
request is in flight). Respect `prefers-reduced-motion`; solid surfaces under
`prefers-reduced-transparency`.
*Check: no perpetual ambient loops; every animation has a start, a purpose, and an end.
Frame work fits the motion budget (see `ontology/design_terms.json`: frame_budget).*

## P3 — 3D vendored, never CDN
Three.js is vendored into the repo, never loaded from a CDN. WebGL is focal,
WebGPU is progressive, layers are capability-gated and disposable; the semantic
document stays authoritative without them.
*Check: no third-party script tags for 3D/animation libraries in shipped HTML.*

## P4 — Bespoke layouts, never template grids
The user hates square template layouts where everything is the same measurement.
Every design is masterful, high-level, elegant, bespoke — never a generic grid.
*Check: the layout has deliberate asymmetry, varied rhythm, custom composition.
"The current best is the floor" — a launch that merely matches the last good design can miss.*

## P5 — Gold leaf, brand colors honored
The house loves gold leaf. A manifesto campaign may lead with BLACK, RED, and GOLD —
the manifesto colors, never the quiet ivory/black museum look (rejected outright).
Supplied dragon artwork is the foundation for that campaign (see site registry).
*Check: campaign palettes match the registered brand; never substitute a quieter palette unasked.*

## P6 — Custom icons
Icons are custom-drawn for the brand, not stock icon fonts. Upscale rules in the
ontology file (icon_upscale) apply when raster assets are involved.
*Check: every icon in the design is bespoke or brand-cleared.*

## P7 — House form protocol, Turnstile-augmented
Every form on every house site: owned Worker/D1 intake, origin-locked, honeypotted,
rate-limited, notification to contact@example.com. No third-party form backends, no
exceptions. Turnstile augments the protocol, never replaces it; server-side Siteverify
fails closed. Frontend and backend ship in lockstep — a backend that rejects missing
tokens only goes live when every form posting to it already renders the widget and
sends the token.
*Check: submit a form end-to-end; verify honeypot-first pipeline, origin lock, and
notification delivery.*

## P8 — Revenue-stack independence
Zero new subscriptions. Minimal dependence on external services; free tiers without
lock-in only. Every technique adopted into the arsenal carries cost verification and
lock-in risk (see `arsenal/ARSENAL.md`).
*Check: the design introduces no paid service, no account the fleet doesn't already own.*

## P9 — Accessibility is a gate, not a polish pass
WCAG 2.1 AA contrast minimum (4.5:1 body text, 3:1 large text/UI), keyboard-operable
everything, visible focus, semantic HTML, single polite live region for dynamic status.
*Check: contrast ratios computed, keyboard walkthrough passes, no keyboard traps.*

## P10 — Copy: Pinker clarity, Cialdini persuasion, verified numbers
All copy passes the copy standards (`copy/COPY_STANDARDS.md`): Pinker's classic style
(concrete, coherent, no zombie nouns), Cialdini's levers used honestly, and every
figure grounded in a checkable source — never invented, never from training data.
*Check: each number on the page traces to a source; each Cialdini lever is honest,
not manipulative.*

## P11 — Standing video formula
Anything requiring a video uses the standing presenter persona as on-screen MC + the standing voice persona as master voiceover
(the voice persona is voice-only, no body). Scripts are built in the founder's first-person voice.
*Check: video jobs cast the standing presenter/voice pair unless the user directs otherwise.*

## P12 — Verify the artifact firsthand
The approver's standing order: "Always view the artifact live when I send you."
Never hand over a deliverable on a subagent's report alone — watch the video, open the
file, check the render. Simple questions answerable from his own filed materials are a
bother; use the wealth of resources first.
*Check: the gate runner has opened the built artifact in a browser/viewer and confirmed
it renders as designed.*

## P13 — Institution voice
The organization is the sole institutional voice; internal codenames never appear publicly.
The user's name, when it appears, is always the full three-name form
The founder's name — full form only, sparingly, only where a signature belongs.
*Check: no internal-codename mentions in public copy; name usage follows the signature rule.*

## P14 — Nothing here deploys
Design work never merges or deploys on its own. PRs held (e.g. PR #54) are not to be
touched. Production deploys follow the repo's own pipeline after explicit approval.
*Check: the job produced no commits to main, no merges, no deploy triggers.*

## P15 — Founder-on-device is the final gate
Headless verification is necessary but never sufficient. Staging ships to a URL the
founder opens on his own phone; his eyes catch what automation misses — a page that
passed every check rendered blank below the hero on iPhone Safari (a CSS specificity
bug no headless run surfaced), and an auto-laid-out constellation showed colliding
labels only on the real 390px viewport. The loop is: staging URL → his eyes →
screenshot feedback → targeted rebuild, same session. Never dismiss his screenshot
as caching until the served bytes prove it.
*Check: the founder has viewed the staging URL on his own device and confirmed, or a
screenshot of the failure is in hand and the rebuild targets exactly what it shows.*

## P16 — Enhancement layers are isolated and fail-open
Motion, 3D, and interactive maps live in their own files and never touch the content
visibility system. The semantic document is complete with JS disabled, WebGL absent,
and tiles failed: the reveal system fails open (the winning rule plus an unconditional
watchdog), motion.js never touches reveals, map pages read as full articles when the
canvas can't init. An enhancement layer must be removable without losing a word.
*Check: disable JS and block the 3D/map scripts — the page still reads whole, nothing
hidden, nothing broken.*

## P17 — Bespoke placement, machine verification
When precision matters, place by hand and verify by machine — not the reverse. The
Ground constellation that earned "absolutely beautiful" was hand-built SVG: every node
and label coordinate placed deliberately, separate phone and desktop layouts, with a
programmatic label-collision check (zero cross-landmark collisions) as the verifier.
Auto-layout is a sketching tool; the shipped artifact is drawn.
*Check: hand-placed compositions carry a machine check (collision, contrast, overlap)
with a recorded pass; algorithmic layouts are never shipped unverified on the
founder's viewport sizes.*

(Process provenance: these three protocols were earned on a chapter-site overhaul,
2026-09-14 → 2026-09-15 — the reveal-specificity blank-page fix, the gold-dust hero
and pillar-sweep motion layer, the vendored MapLibre /map/ migration, and the
hand-drawn constellation rebuild after the founder's iPhone screenshot.)
