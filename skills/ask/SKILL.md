---
name: ask
description: "Route an engineering situation to the right skill or flow. Use when the user is unsure which engineering skill applies or where to start."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# Ask

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

You describe the situation; this skill names the skill.

## Route

- "I have a rough idea" → grill-me, then to-spec.
- "We agreed on something in chat" → to-spec.
- "I have a spec" → to-tickets, then implement (or implement-spec).
- "Something is broken" → diagnosing-bugs.
- "Review this" → code-review.
- "I need to understand a codebase" → research, then improve-codebase-architecture.
- "Hand this to someone else" → handoff.
- "This is a big messy effort" → wayfinder.
- "Am I sure about this design?" → prototype, or grill-with-docs.
- "Write this up for a human" → to-questionnaire, wizard, or pr.

If none fits, say so plainly instead of forcing a skill.
