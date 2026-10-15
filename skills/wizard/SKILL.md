---
name: wizard
description: "Create a step-by-step setup script that walks a human through actions only they can perform, verifying each stage. Use when provisioning, credential setup, migrations, or cutovers need a guided repeatable procedure."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Wizard

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Setup humans can complete without reading the manual.

## Method

1. List the setup steps in order, with what success looks like at each.
2. The script checks preconditions first and says plainly what is missing.
3. Each step: do it, verify it, report it in plain language.
4. On failure: say what failed, what it means, and the exact next action
   — never a bare stack trace.

## Rules

- The wizard never changes anything it has not announced.
- Secrets are never printed, logged, or stored by the wizard.
