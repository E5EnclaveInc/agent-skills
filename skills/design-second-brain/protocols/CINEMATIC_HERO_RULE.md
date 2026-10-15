# Cinematic Hero Rule — Design Program

**Status: `ratified` — RATIFIED by the approver 2026-09-12 (verbal order; recorded here 2026-09-12).**

**Ratification provenance:** authored by the design program (2026-09-12);
ingested into this skill 2026-09-12. **RATIFIED by the user 2026-09-12** —
ratification instruction: "Approve, consider ratified." Per the 2026-09-12
ratification-provenance doctrine, this is now verified doctrine: cite it as
ratified, treat it as settled canon. Work shipped under this rule is flagged
`hero-rule: ratified` (replacing the earlier `hero-rule: draft` flag).
Doctrine changelog: draft 2026-09-12 (the design program) → ratified 2026-09-12 (approver).
Canonical statement also recorded in `~/AGENTS.md` ("Cinematic hero rule
(2026-09-12, RATIFIED by the approver)"). Amendments require the approver's order.

**Source:** the design program's doctrine directory · ingested
2026-09-12 · normative text below is verbatim from the design program's file.

---

# CINEMATIC HERO RULE
**Status:** canonical doctrine — the design program, ordered 2026-09-12.
**Scope:** every hero section on every house surface (the flagship site, the publication site, campaign sites, app landing pages, paid-landing pages).
**Intent:** every first viewport is a cinematic frame optimized jointly for **visual supremacy** and **conversion**. Beauty that doesn't convert is decoration; conversion that isn't beautiful is beneath the brand.

Institutional voice rule: heroes speak as the organization Internal codenames never appear in heroes. The founder's name appears only in full three-name signature form and only where a signature belongs — never in hero copy.

---

## 1. Composition — the layout grammar

1.1. **Element hierarchy (strict order of visual weight):** (1) one dominant visual field (cinematic image, 3D scene, or full-bleed media) → (2) the headline → (3) one proof element (stat, quote, or trust marker) → (4) the CTA cluster → (5) a single subhead or mission line. No element may out-weigh its predecessor in contrast, size, or motion except the CTA cluster, which is permitted to pulse once on load (see §2).

1.2. **Asymmetry is mandatory.** The headline's vertical center must sit off the viewport's vertical center by ≥8% of viewport height; the primary optical mass must be off horizontal center by ≥6%. A hero that could be mirrored horizontally and still look identical FAILS.

1.3. **The "no generic grid" test (pre-ship gate):** cover the logo and brand colors. If a stranger could mistake the hero for a template (centered headline, centered buttons, blurred blob background), it ships nowhere. Redesign until unmistakable.

1.4. **Depth over flatness:** at least two of {parallax layer, 3D geometry, cinematic grain/vignette, volumetric light, particle field} must be present — unless performance or reduced-motion conditions suppress them, in which case the static fallback (see §2.7) must itself pass 1.3.

1.5. **Gold is earned, not wallpapered.** Gold leaf / gold accents are a reserved signal: permitted in heroes only where the content warrants reverence or achievement (manifesto, milestone, lineage). Routine heroes use it sparingly or not at all — scarcity is what makes it land.

1.6. **One hero per viewport, one promise per hero.** No carousel, no rotating headlines, no tabbed hero. If there are two messages, build two pages or pick one.

---

## 2. Motion budget

2.1. **What may move:** the background field (WebGL/Three.js scene, video, or animated canvas), ONE entrance choreography on load (elements arrive in hierarchy order, ≤900ms total, staggered ≤120ms), scroll-linked parallax on decorative layers only (never on the CTA cluster or headline legibility), and ONE ambient loop (particles, light drift, or slow camera dolly). Everything else is static.

2.2. **What may never move:** body copy, CTA labels, prices, dates, legal text. Motion must never carry meaning — if removing the motion removes information, the design is broken.

2.3. **Frame-rate floor:** sustained ≥55fps on a 2022-class mid-range device (target: Pixel 6a / iPhone 12 class) during the first 10 seconds. Measured with the actual vendored build, not dev-mode. If it can't hold 55, cut a layer — visual supremacy includes smoothness.

2.4. **prefers-reduced-motion (mandatory, no exceptions):** when the media query matches: (a) the entrance choreography becomes an instant state (no fade/slide — elements simply appear), (b) all ambient loops freeze on a composed frame, (c) parallax is disabled, (d) the single CTA pulse becomes a static outline. The frozen composition must still pass the no-generic-grid test (§1.3).

2.5. **Three.js vendored, never CDN.** The Three.js runtime is vendored into the site build (self-hosted), pinned to an exact version, loaded async/defer after first paint. No CDN script tags. Failure to load WebGL degrades to the §2.7 fallback — never a blank hero, never a console-error void.

2.6. **Video backgrounds:** permitted only if ≤2.5MB, ≤10s loop, no audio track, muted+playsinline, poster frame mandatory. If the video fails or is data-saver-blocked, the poster frame is the hero — it must be composed to carry the section alone.

2.7. **No-JS fallback (required):** with JavaScript disabled, the hero renders a fully legible composed frame — headline, proof, CTA, background image/gradient — with no layout breakage. Tested by disabling JS, not by assumption.

---

## 3. Performance budgets (mobile 4G, mid-range device — the floor, not the lab)

3.1. **Core Web Vitals:** LCP ≤ 2.5s, CLS ≤ 0.05, INP ≤ 200ms. Hero images are `fetchpriority="high"`, preloaded, and sized to the rendered slot — no 3000px sources served to a 390px screen.

3.2. **Hero asset weight caps:** total hero-blocking weight ≤ 400KB; hero image ≤ 250KB (WebP/AVIF, both offered via `<picture>`); the vendored Three.js hero module ≤ 150KB gzipped (import only the modules used — tree-shaken, never the full build); custom fonts ≤ 100KB total for hero-critical faces. Video heroes: total hero weight ≤ 2.8MB including poster.

3.3. **Vendored/self-hosted only.** Every hero asset — images, fonts, 3D runtime, icon sprites — is served from owned infrastructure (the site's own CDN/edge). Zero third-party requests in the hero critical path: no Google Fonts, no CDN libraries, no external trackers firing before the conversion event. (Instrumentation fires per §8 — asynchronously, after interaction or after LCP, never blocking.)

3.4. **Render rule:** no render-blocking JS for the hero; CSS for the first viewport is inlined or <14KB. The CTA must be interactive within 1s of first paint on repeat visit (cached).

---

## 4. CTA architecture

4.1. **Conversion goal declaration (required, in the page's build notes):** every hero declares exactly one primary conversion goal, chosen from the taxonomy: `donate | subscribe | sign | apply | buy | book | share | contact`. Secondary goals are permitted only as secondary CTAs. A hero without a declared goal does not ship.

4.2. **Placement:** the primary CTA cluster sits within the first viewport on all breakpoints, after the headline in reading order (or beside it on wide screens — never above it). Minimum one primary CTA visible without scrolling on 360×640.

4.3. **Hierarchy:** exactly ONE primary CTA (filled, highest contrast), up to TWO secondary CTAs (ghost/outline or text-link). The primary CTA's label is a verb phrase promising the outcome ("Fund the mission," "Get the playbook"), never a dead-end verb ("Submit," "Click here," "Learn more" as the primary is banned — see §5.5).

4.4. **Friction rules:** primary CTA reaches the conversion instrument in ≤2 clicks from the hero (hero click → instrument, e.g. the form/checkout/subscribe widget — one intermediate step maximum, and that step must be pre-loaded or instant). No interstitial modal before the instrument except where legally required. Every form behind a hero CTA follows the house form protocol (owned Worker/D1 intake, origin-locked, honeypotted, rate-limited, notify contact@example.com) with Turnstile on submit.

4.5. **Nonprofit vs. business calibration:** nonprofit heroes (the flagship, campaign sites) default the primary CTA to the mission action (donate/sign/subscribe); business heroes (the publication site) default to the value action (subscribe/buy/book). The proof element (§1.1-3) must match the lane: nonprofit = impact evidence; business = outcome evidence. Never a donate CTA on a business hero, never a buy CTA on a nonprofit hero.

---

## 5. Copy constraints

5.1. **Word-count ceilings:** headline ≤ 12 words (target ≤ 8); subhead ≤ 25 words; CTA label ≤ 5 words; proof element ≤ 15 words. Every word over ceiling needs a written justification in the build notes.

5.2. **Pinker rules (applied to hero copy):** concrete over abstract (name the thing: "fund 50 STEAM academies," not "empower the future"); active verbs, human subjects; kill zombie nouns ("utilization," "facilitation," "empowerment" — rewrite or strike); no hedging ("maybe," "could possibly," "we hope to"); the headline must survive the "so what?" test — a stranger reads it and can state what the page wants them to do.

5.3. **Cialdini moves — required:** at least ONE of {authority-by-attribution (named source, cited credential), social proof (a number with a source: members, dollars, families served), unity (shared identity language — "we," the lineage, the mission)} must be present in the proof element. Commitment/consistency may appear in the secondary CTA ("Continue your support") but never in the primary — the primary is the commitment, not the reminder of one.

5.4. **Cialdini moves — permitted but policed:** scarcity and urgency only with a real, verifiable constraint (a deadline that exists, seats that are counted). Fabricated urgency is banned outright — it burns the trust the brand is built on.

5.5. **Banned in heroes:** hype adjectives with no evidence ("revolutionary," "game-changing," "world-class" — unless a third party said it, attributed); vague claims ("best," "leading" without a frame); "Learn more" as the primary CTA; exclamation points in headlines (max one per hero, and it had better be earned); the founder's name in hero copy (signature belongs at the sign-off, not the masthead); anything that would fail the house comms-law voice (institutional "we" of the organization).

---

## 6. Icon standards — the ICON UPSCALE PIPELINE

6.1. **Every icon in a hero is custom.** Custom-drawn (original vector work in the house icon language) or custom-composed (built from licensed primitives, re-drawn and re-weighted into a single coherent set). Stock icon sets, default emoji-as-icon, and unmodified template glyphs are banned from heroes.

6.2. **Premium bar:** icons must read as jewelry, not signage — consistent 2px optical stroke (or filled equivalent), rounded joins, drawn on a shared grid, with the gold accent reserved per §1.5. A hero icon set is reviewed at 4× zoom; any jag, inconsistency, or stock echo fails it.

6.3. **When animation pays:** animate an icon only when the motion explains the action (a pen signing for "sign," a seed sprouting for "grow") — the animation must complete in ≤1.2s and settle to a clean static state. Decorative perpetual icon animation (spinning, bouncing badges) is banned.

6.4. **When static wins:** proof-adjacent icons (trust markers, stat icons), secondary CTAs, and anything inside the conversion path stay static — motion there is distraction, and distraction is friction.

6.5. **Format/delivery:** SVG only, inline or sprited (never icon fonts); `aria-hidden="true"` on purely decorative icons; meaningful icons get `<title>` or an `aria-label`; icons theme via `currentColor` so they inherit context; a dark/light or brand-context variant is supplied wherever the hero background demands it.

---

## 7. Accessibility floor

7.1. **Contrast:** headline and CTA text ≥ 7:1 against their immediate background (AAA for the two elements that matter most); subhead and proof ≥ 4.5:1. Tested against the actual rendered frame — including over the brightest video frame or 3D state — not against a flat mockup.

7.2. **Keyboard:** every CTA and interactive hero element is reachable and operable by keyboard; visible focus indicator (never `outline: none` without a replacement); focus order follows the hierarchy in §1.1.

7.3. **Screen readers:** decorative canvas/WebGL/video is `aria-hidden="true"` with no focusable children; the hero carries one `<h1>` (the headline — exactly one per page); the proof element is real text, not baked into an image; CTA labels are self-describing out of context ("Donate to the organization," not "Donate" where ambiguity exists).

7.4. **Motion sensitivity:** §2.4 is the floor. Additionally, no auto-playing motion may exceed 5 seconds without a user-accessible pause control (video backgrounds loop silently — they are exempt only if ≤10s, muted, and non-essential per §2.6; anything longer gets a pause button).

---

## 8. Instrumentation — the hero event taxonomy

Every hero emits these events to the site's analytics (async, non-blocking, after LCP):

- `hero_view` — hero entered viewport (once per pageview). Properties: `page`, `hero_id`, `variant`, `goal` (from §4.1).
- `hero_cta_impression` — CTA cluster rendered interactively. Properties: `cta_id`, `position` (primary/secondary-N).
- `hero_cta_click` — any hero CTA clicked. Properties: `cta_id`, `label`, `destination`, `position`.
- `hero_goal_start` — conversion instrument opened from hero (form/checkout rendered). Properties: `goal`, `cta_id`.
- `hero_goal_complete` — conversion completed. Properties: `goal`, `cta_id`, `value` (where applicable).
- `hero_media_state` — fallback engaged: `fallback` ∈ {no-js, reduced-motion, webgl-fail, video-fail, data-saver}. Fires once per session per hero.

8.1. **Attribution rule:** `hero_goal_complete` must carry the originating `cta_id` and `hero_id` so conversion rate is measurable per hero and per CTA — heroes are A/B-able units, not vibes.

8.2. **No event may carry PII.** Labels, emails, and form contents are never event properties.

8.3. **Dashboard requirement:** each site's hero set has a standing view showing, per `hero_id`: views → CTA clicks → goal starts → goal completes (the funnel), plus fallback-engagement rate. A hero with no measurable funnel is undecorated work — pretty, but not doctrine.

---

## 9. Enforcement — pre-ship checklist

Every page build or redesign must check every box before merge/deploy. One unchecked box = does not ship.

**Composition**
- [ ] Hierarchy follows §1.1 order (visual → headline → proof → CTA → subhead)
- [ ] Asymmetry measured: headline ≥8% off vertical center, mass ≥6% off horizontal center
- [ ] Passes the no-generic-grid test (§1.3) — documented with a one-line verdict in build notes
- [ ] Gold usage justified or absent (§1.5)
- [ ] Exactly one promise; no carousel/rotator/tabbed hero

**Motion**
- [ ] Motion inventory listed: ambient loop (1 max), entrance (≤900ms), parallax (decorative only)
- [ ] Sustained ≥55fps on target mid-range device, first 10s, measured on the vendored build
- [ ] prefers-reduced-motion renders the frozen composed frame; frozen frame passes §1.3
- [ ] Three.js vendored + pinned, async/defer; WebGL failure shows composed fallback (tested)
- [ ] Video (if any): ≤2.5MB, ≤10s, muted/playsinline, poster carries the hero alone
- [ ] No-JS render tested: headline, proof, CTA, background all legible, no breakage

**Performance**
- [ ] LCP ≤ 2.5s, CLS ≤ 0.05, INP ≤ 200ms (mobile 4G, mid-range)
- [ ] Hero-blocking weight ≤ 400KB; hero image ≤ 250KB (WebP/AVIF via `<picture>`); Three.js module ≤ 150KB gz; fonts ≤ 100KB
- [ ] Zero third-party requests in the hero critical path (fonts, libs, trackers all self-hosted or deferred)
- [ ] CTA interactive ≤1s after first paint on repeat visit

**CTA**
- [ ] Conversion goal declared in build notes (`donate|subscribe|sign|apply|buy|book|share|contact`)
- [ ] One primary CTA, ≤2 secondary; primary is a verb phrase promising the outcome
- [ ] Primary CTA → conversion instrument in ≤2 clicks; instrument follows the house form protocol + Turnstile
- [ ] Lane-correct: nonprofit heroes carry mission CTAs, business heroes carry value CTAs (§4.5)

**Copy**
- [ ] Word ceilings met: headline ≤12, subhead ≤25, CTA ≤5, proof ≤15 (overages justified in notes)
- [ ] Pinker pass: concrete, active, zero zombie nouns, no hedging, survives "so what?"
- [ ] ≥1 required Cialdini move present in proof (authority-by-attribution, social proof, or unity)
- [ ] No banned items: hype adjectives without attribution, vague superlatives, "Learn more" as primary, founder's name in hero copy

**Icons**
- [ ] All hero icons custom-drawn or custom-composed; no stock sets, no icon fonts
- [ ] 4× zoom review passed; gold used per §1.5
- [ ] Icon animation (if any) ≤1.2s, settles static, explains the action; conversion-path icons static
- [ ] SVG only, `currentColor`-themed, decorative icons `aria-hidden`, meaningful icons labelled

**Accessibility**
- [ ] Headline + CTA ≥7:1 contrast; subhead + proof ≥4.5:1 — tested on the rendered frame
- [ ] Full keyboard operability; visible focus; focus order matches §1.1
- [ ] Decorative canvas `aria-hidden`; exactly one `<h1>`; proof is real text; CTA labels self-describing
- [ ] Motion >5s has a pause control (or qualifies for the §2.6 exemption)

**Instrumentation**
- [ ] All six events (§8) implemented: `hero_view`, `hero_cta_impression`, `hero_cta_click`, `hero_goal_start`, `hero_goal_complete`, `hero_media_state`
- [ ] `hero_goal_complete` carries `hero_id` + `cta_id` for per-hero/per-CTA attribution
- [ ] No PII in event properties
- [ ] Funnel view exists or is specified for this hero (views → clicks → starts → completes)

**Doctrine**
- [ ] Build notes record: goal, motion inventory, weight audit, grid-test verdict, copy ceilings, icon provenance
- [ ] PR #54 untouched; no merge/deploy performed by this change (standing hold)

---

*Doctrine changelog (from source): created 2026-09-12 (the design program, the design program). Source self-styles "Canonical" — recorded in this skill as **DRAFT pending user ratification (2026-09-12)**. Amendments require the approver's order.*
