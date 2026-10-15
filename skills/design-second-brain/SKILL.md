---
name: design-second-brain
description: "A persistent design second brain for an organization's web properties: canonical design protocols, a per-site design-language registry, a vetted technique arsenal with cost and lock-in tracking, copy standards, an ontology grounding report, and a pre-ship design gate that fails closed. Use before building or redesigning any page or producing promo collateral, and whenever a design-language decision must match the standing house style."
license: MIT
metadata:
  version: 1.0.0
---

# Design Second Brain

## Purpose
The durable design memory of an organization. Load this skill before any web page build/redesign, any promo flyer/collateral job, or any design-language decision on one of its properties. It is the canonical source for: design protocols, per-site design language, the technique arsenal, copy standards, and the pre-ship design gate.

## When to use
- Building or redesigning any page on one of the organization's properties (see `sites/SITE_REGISTRY.md` for the registered set).
- Designing promo flyers, one-pagers, social cards, or other collateral.
- Any question of "what's our design language / palette / motion register / form protocol for X".
- Before shipping any page: run the design gate (see Workflow).

## Structure
| Path | Contents |
|---|---|
| `protocols/PROTOCOLS.md` | The 14 canonical protocols (P1–P14) — single source of truth |
| `protocols/CINEMATIC_HERO_RULE.md` | The cinematic hero rule (ratified doctrine) |
| `sites/SITE_REGISTRY.md` | Per-site design language + status (template + worked examples in this export) |
| `arsenal/ARSENAL.md` | Technique/tool registry with status, cost, lock-in, provenance |
| `arsenal/INGESTION.md` | How arsenal recon reports get ingested (never hand-edited) |
| `arsenal/reference/` | Reference libraries (vendored catalogs, resource lists) — reference only, never design authority |
| `copy/COPY_STANDARDS.md` | Copy rules (structural, numbers, institutional voice) |
| `copy/CIALDINI_BIBLE.md` | The persuasion canon (Cialdini principles operationalized) |
| `ontology/GROUNDING_REPORT.md` + `ontology/design_terms.json` | Term-grounding method + the grounded design vocabulary |
| `workflow/DESIGN_GATE.md` | The pre-ship design gate (fail-closed) |
| `workflow/bin/run_design_gate.py` | The gate runner (deterministic checks + attestation ledger) |
| `workflow/roma_graph.json` | Task-graph template for a gate run |
| `refresh/RECON_BRIEF.md` | The monthly arsenal-recon brief template |

## Workflows
1. **Page build/redesign:** load `protocols/PROTOCOLS.md` + the site's entry in `sites/SITE_REGISTRY.md` → build → run the design gate (below) → ship only on PASS or a waived-with-reason verdict.
2. **Collateral (flyer/one-pager/card):** load PROTOCOLS (P1–P14, esp. P4 register, P5 metaphysics, P6 copy) + `copy/COPY_STANDARDS.md` → design → gate with the collateral job type.
3. **Design-language question:** answer from the site registry + protocols; if the term is a design term, check `ontology/design_terms.json` for its operational grounding.
4. **New technique/tool:** it enters only via the recon → ingestion path (`arsenal/INGESTION.md`), never by hand-editing the arsenal.

## The design gate (mandatory pre-ship)
```
python3 workflow/bin/run_design_gate.py --job manifest.json
```
14 checks mapped to the protocols. P7/P8/P9/P14 fail-closed (a fail blocks the ship decision outright). Waivers require a named reason + approver and are journaled. Full spec: `workflow/DESIGN_GATE.md`.

## Non-negotiables (summary — PROTOCOLS.md is canonical)
1. **Live-asset-first:** open the live page/asset before planning any redesign. Memory is a lead, not a fact.
2. **Zero new subscriptions by default;** vendored over CDN; owned infrastructure over third-party backends.
3. **House form protocol on every form** (owned Worker/database intake, origin-locked, honeypotted, rate-limited, Turnstile-augmented, notify a monitored contact address). Turnstile augments, never replaces, the baseline.
4. **Motion is meaning:** finite, state-driven animation; prefers-reduced-motion honored everywhere (P9).
5. **Copy obeys the standards:** structural rules (written artifact, no fragment bullets), the numbers rule (never invent a figure; every figure traces to a checkable source), institutional voice.
6. **Artifact checks are visual:** open the rendered artifact — the live page, the exported PDF — before claiming done.

## Ontology note
Key design terms were run through an ontology-floor `resolve()` (see `ontology/GROUNDING_REPORT.md`). The floor's regime is hard/rare physical formalisms; design-doctrine terms correctly miss there, so this skill carries its own operational grounding (`ontology/design_terms.json`) and does not rely on the floor for design vocabulary.
