---
name: prototype-sprint
description: "Ship the thinnest thing that proves the signal today — landing page plus signup, no database — then hand production engineering a clean handoff protocol instead of a pile of prototype. Use when speed-to-signal beats completeness. Differs from a full build by the disposable-first contract and the explicit prototype-to-production handoff."
license: MIT
metadata:
  version: 1.0.0
---
# Prototype Sprint

## Purpose
Prove the signal fast with the thinnest shippable thing, then hand production
a protocol — not a codebase to inherit by accident.

## Workflow
1. State the one signal the prototype must produce (e.g. "will anyone sign
   up"). One sentence. If it doesn't serve the signal, it isn't built today.
2. Cut the stack to the thinnest shape: landing page + signup; no database, no
   auth, no infrastructure beyond the thinnest host. Write the built-vs-faked
   list explicitly — faked is a strategy, not a shame.
3. Build disposable: single-file or minimal static where possible. Speed over
   structure; this code is allowed to die.
4. Ship to staging first. Verify live yourself: open the page, submit the form,
   confirm the data lands where it should. Screenshots of forms, not claims
   of forms.
5. Write the handoff protocol before the prototype ships, not after:
   - What graduates to production (files, specs, data, copy)
   - What gets thrown away
   - Who owns the first production task
   - What the production builder must verify before building on any of it
6. Sunset the prototype: it never becomes production by drift. Production is
   rebuilt from the handoff — or the handoff explicitly blesses the
   prototype's promotion, in writing.

## Output Contract
The signal statement, the built-vs-faked stack list, the live staging URL with
verification evidence, and the handoff protocol.

## Operating Rules
1. One signal. A prototype with two signals is two prototypes.
2. No database until the signal says someone wants the thing.
3. Prototype and production are different artifacts; the handoff is the bridge,
   never the code.
4. Verify the live page yourself — open it, click it, submit it.
5. Manual behind the curtain is allowed, but it's written down.
6. The handoff protocol exists before the prototype ships. No protocol, no ship.
