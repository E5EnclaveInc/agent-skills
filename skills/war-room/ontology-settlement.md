# Ontology settlement — terms before deliberation

Disputes about words are settled before disputes about the world. The ontology floor is the agreement mechanism.

## Procedure

1. The convener lists the **load-bearing terms** (the 3–7 words the decision turns on) in the charge.
2. Each term goes through the ontology floor's `resolve()` (see `your ontology-floor skill`): word → formula + checkable proof. Grounded terms enter the record with their grounding; deliberation proceeds on the math, not the vibes.
3. **Refused terms:** ethical/value terms are REFUSED by the floor and routed up as **Chairman judgment calls** — never computed, never voted on by the committee. The refusal is recorded.
4. Terms the floor cannot ground (no record, quarantine) are F-flagged: deliberation may proceed around them, but no ruling may depend on them silently.
5. **Committee operational definitions:** institutional/governance terms (jurisdiction, canonical-as-policy, ratification, consumer, conformance) will routinely return ungrounded — that is expected, not a failure. The committee then enters an explicit operational definition, marked **committee-defined, never floor-grounded**, and rulings cite the definition, not the floor. (Precedent: 2026-09-26 domain-governance session — "formalism," "canonical," "jurisdiction" all ungrounded; defined operationally on the record.)

## The Keeper's role

The Chair (as Keeper of the Word, in the v1 council: Thoth) rules on naming disputes *after* the floor has spoken. "Two names that normalize to one name are one entry wearing two masks" — the floor's canonicalizer is the law of identity the committee keeps.

## Ratchet note (2026-09-26)

The formalism committee's core integrity work was applying the floor's own canonicalizer (`resolve.py`: lowercase, hyphens→underscores, spaces→underscores) to the evidence — and it caught the convener's own miscount (3 suspected collisions → 2 real; `LMcCache`/`LMCACHE` normalize distinctly). Lesson institutionalized: **the convener's claims are subject to the same settlement as anyone's.** Verification rides the convener too.
