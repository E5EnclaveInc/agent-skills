# Vibe-coding design resources (user-kept list, 2026-09-25)

The approver's kept list of 28 vibe-coding resources, grouped by what you're stuck on (their framing). Source: their 2026-09-25 share ("tested every vibe coding resource I could find this year"). Liveness verified 2026-09-25 by HTTP check from the fleet box (28/29 live; AppShot timed out twice — flagged, not declared dead).

**Doctrine status: reference library, never design authority** — same standing as the ui-ux-pro-max vendored catalogs. House protocols decide every design; these are lookup material for agents and designers.

## Full-build prompts (stuck on the whole page)
| Resource | What | Note |
|---|---|---|
| [scrolltide.co](https://scrolltide.co) | 200+ full build prompts for 3D and scroll-driven sites — complete design briefs, not drop-in components | LIVE 200. Directly aligned with the cinematic-hero rule — prompt library for agents |

## Inspiration galleries (stuck on "what good looks like")
| Resource | What | Note |
|---|---|---|
| [minimal.gallery](https://minimal.gallery) | Curated high-end sites to feed your agent | LIVE 200 |
| [kage.design](https://kage.design) | Real UI inspiration mapped straight to prompts | LIVE 200 |
| [styles.refero.design](https://styles.refero.design) | 2,000+ real product styles with typography | LIVE 200 |
| [component.gallery](https://component.gallery) | 2,600+ examples of how top design systems solve the same element | LIVE 200 |
| [appshot.gallery](https://appshot.gallery) | Real app screenshots for mobile | TIMEOUT from fleet box 2026-09-25 (twice) — may be geo/CDN; re-verify before use |
| [navbar.gallery](https://navbar.gallery) | Navbar patterns | LIVE 200 |
| [footer.design](https://footer.design) | Footer patterns | LIVE 200 |
| [cta.gallery](https://cta.gallery) | Conversion-tested forms, popups, buttons | LIVE 200 |
| [404s.design](https://404s.design) | 404 page patterns | LIVE 200 |

## Agent-readable design systems (stuck on agent output quality)
| Resource | What | Note |
|---|---|---|
| [designmd.ai](https://designmd.ai) | Design systems as markdown your agent can read (DESIGN.md files for Cursor/Claude Code) | LIVE 200. **Strongest glean: author per-property DESIGN.md files from our SITE_REGISTRY.md so agents building on house properties read the design language in markdown** |
| [vibeprompts.dev](https://vibeprompts.dev) | Ready-made prompts for dashboards and landing pages | LIVE 200 |

## Component registries (stuck on building it)
| Resource | What | Note |
|---|---|---|
| [21st.dev](https://21st.dev) | 12,000+ hand-crafted React/Tailwind components, templates, shadcn themes; installs via MCP | LIVE 200. **Glean: MCP-pluggable into agent workflows — but verify license PER COMPONENT (many are pro); vendored only, never CDN, per doctrine** |
| [ui.shadcn.com](https://ui.shadcn.com) | shadcn/ui — the gold standard | LIVE 200 |
| [ui.aceternity.com](https://ui.aceternity.com) | 200+ animated React/Tailwind components | LIVE 200 |
| [magicui.design](https://magicui.design) | Animated components | LIVE 200 |
| [motion-primitives.com](https://motion-primitives.com) | Motion primitives | LIVE 200 |
| [uiverse.io](https://uiverse.io) | Community UI elements | LIVE 200 |
| [uiable.com](https://uiable.com) | UI components | LIVE 200 |
| [mapcn.dev](https://mapcn.dev) | Map components — markers, routes, popups | LIVE 200. Note: our adopted map stack is vendored MapLibre; mapcn is React/Tailwind component reference only |

## Motion (stuck on making it move)
| Resource | What | Note |
|---|---|---|
| [kinetics.colorion.co](https://kinetics.colorion.co) | 150+ motion effects with React code and prompts; spring-physics micro-interactions, copyable CSS/React | LIVE 200. **Glean: spring-physics tuning complements our motion arsenal (GSAP vendored, Lenis)** |
| [animejs.com](https://animejs.com) | Anime.js animation library | LIVE 200 |

## Micro-interactions and details
| Resource | What | Note |
|---|---|---|
| [microkit.co](https://microkit.co) | Micro-interactions | LIVE 200 |
| [glass.samasante.com](https://glass.samasante.com) | Liquid Glass refraction components | LIVE 200 |
| [text-effects.colorion.co](https://text-effects.colorion.co) | CSS text effects | LIVE 200 |
| [circleloaders.dominikakissi.com](https://circleloaders.dominikakissi.com) | Circle loaders | LIVE 200 |
| [gradientbuttons.colorion.co](https://gradientbuttons.colorion.co) | Gradient buttons | LIVE 200 |

## Illustration and 3D assets
| Resource | What | Note |
|---|---|---|
| [kitbitz.art](https://kitbitz.art) | 2,000+ hand-drawn illustrations | LIVE 200 |
| [3dicons.co](https://3dicons.co) | 3D icons | LIVE 200 |

## Standing rules for anything pulled from this list
1. **License first:** verify the license per asset/component before vendoring (community registries mix MIT with commercial/pro).
2. **Vendored, never CDN:** anything shipped in shipped HTML is copied into the repo; no runtime dependency on these domains.
3. **Reference, not authority:** house protocols and the per-site design language decide; these inform, never dictate.
4. The list is their kept set as of 2026-09-25 — new entries come from them, not from recon.
