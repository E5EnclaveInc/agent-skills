# Source Prompts — prototype_sprint

Distilled from the GrokBot Galaxy 30-prompt set (Ship by Thursday build,
September 15–17, 2026). Provenance: prompts collected from the three builders'
posts and the "30 GROKBOT PROMPTS" card; full text archived with the original source set.

## A04 — Prototype engineer, landing first
> Create a prototype engineer that ships a simple landing page with email
> signup today — no database or unnecessary infrastructure.

## A06 — Prototypes vs production split
> Use GrokBot for research and disposable prototypes, then create a clear
> handoff protocol for production engineering.

## B06 — Landing page signup to Notion
> Connect the landing-page signup form to a Notion database and define its
> fields, workflow and customer confirmation message.

## B09 — Deploy path
> Connect the product repository to Vercel and create the complete deployment
> path from first preview to custom domain.

## Visual direction → brand_sprint (re-homed)
Naming, visual direction, and the design brief now live in the `brand_sprint`
skill (A09, C08). Prototype-sprint owns the thinnest shippable thing and its
handoff; the identity it ships with is decided by brand_sprint.

## Adaptation notes
- GrokBot "disposable prototypes" → your staging lanes (any static host's
  staging/preview deploys, verified live before any production word).
- "Handoff protocol for production engineering" → production gates: nothing
  graduates without the handoff's verification checklist, and a human's word
  moves production.
- B06's Notion-DB signup → any thinnest capture you own (an owned form, a
  spreadsheet, a tiny key-value store); the point is capture without
  infrastructure, not the specific tool.
