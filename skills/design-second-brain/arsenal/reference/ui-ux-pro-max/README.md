# ui-ux-pro-max reference catalogs

**Vendored:** 2026-09-20 (ingested from `~/recon/third-party-skills/ui-ux-pro-max-skill/`,
shallow clone of github.com/nextlevelbuilder/ui-ux-pro-max-skill, MIT license).

**Role: REFERENCE ONLY — never an authority.** These catalogs are lookup material
for style/palette/font/pattern searches when the house protocols don't already
answer the question. They do NOT decide design direction. The canonical design
protocols (`protocols/PROTOCOLS.md`), the cinematic hero rule, the per-site
registry (`sites/SITE_REGISTRY.md`), and the design gate decide. Generic
best-practice defaults in these catalogs (e.g. Tailwind-blue "Vibrant &
Block-based" for advocacy pages) are doctrine-rejected aesthetics — consult,
never obey.

## Contents (vendored CSVs, header row + data rows)

| File | Rows | What |
|---|---|---|
| `styles.csv` | 88 | UI style catalog (79 searchable + 9 deprecated legacy names) |
| `colors.csv` | 192 | Industry-aligned color palettes |
| `typography.csv` | 74 | Curated font pairings (Google Fonts; verify OFL/license before vendoring any face — house rule: self-host woff2, never hotlink a font CDN) |
| `google-fonts.csv` | 1934 | Individual Google Fonts catalog |
| `ui-reasoning.csv` | 192 | Product-type → design-system reasoning profiles |
| `products.csv` | 192 | Product type taxonomy backing the reasoning profiles |
| `ux-guidelines.csv` | 119 | UX best practices / anti-patterns |
| `landing.csv` | 34 | Landing-page structure patterns |
| `icons.csv` | 105 | Curated icon recommendations |
| `charts.csv` | 25 | Chart-type recommendations for dashboards |
| `motion.csv` | 17 | GSAP animation presets |
| `stacks/` | — | 22 stack-specific UI guideline files |

**Excluded from ingest:** `phosphor-icons-upstream.json`, `google-font-licenses.json`,
`data-provenance.json`, `catalog-summary.json`, `app-interface.csv`,
`react-performance.csv` — not needed for the reference role; re-vendor on demand.

## How to use
Grep the CSVs directly (e.g. search `styles.csv` for a style keyword, `colors.csv`
for an industry palette). For the original BM25 search machinery, see the source
clone at `~/recon/third-party-skills/ui-ux-pro-max-skill/` —
`scripts/search.py` runs dependency-free against its own data dir.
