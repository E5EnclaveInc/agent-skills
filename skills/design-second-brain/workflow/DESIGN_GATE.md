# The Mandated Design Gate

**Rule: every web page build/redesign AND every promo flyer/collateral job for the
House sites must pass the second brain's protocol checklist before shipping.**
No exceptions, no "small change" waivers — small changes are where doctrine dies.

## How a gate run works (ROMA shape)

The gate is a dependency-aware task graph executed in ROMA order
(Atomizer → Planner → Executor → Aggregator), with the sprint-engine's mandatory
red-team/steel-man self-verification before the ship decision. The executable form
is `workflow/bin/run_design_gate.py`; the graph template is `workflow/roma_graph.json`.

```
GOAL: ship <page|flyer> for <site> to <standard>
 ├─ T1 protocol-checklist      [THINK]  run run_design_gate.py --job manifest.json
 │    └─ findings: per-protocol PASS/FAIL (+ evidence)
 ├─ T2 design-review            [THINK]  depends_on T1 — human-eye review against
 │                                        SITE_REGISTRY language + PROTOCOLS (P1–P6, P12:
 │                                        view the artifact live, firsthand)
 ├─ T3 copy-check               [THINK]  depends_on T1 — COPY_STANDARDS pass/fail per line
 ├─ T4 red-team/steelman        [THINK]  depends_on T2,T3 — roma.py verify over the 8
 │                                        lenses (safety_money, cost_runaway,
 │                                        feasibility_limits, value, security,
 │                                        reversibility, human_dependency, observability);
 │                                        verdict must be `approve`, else revise + re-gate
 ├─ T5 build/finalize           [WRITE]  depends_on T4 — apply fixes, rebuild artifact
 ├─ T6 artifact-verification    [THINK]  depends_on T5 — open the artifact live;
 │                                        re-run failing checks; confirm render
 └─ T7 ship-decision            [ACT]    depends_on T6 — NEVER auto-executed.
                                          Marked `proposed`; the ship (merge/deploy/
                                          publish) needs explicit approval per the
                                          tiered-gating doctrine. The gate does not deploy.
```

## Checklist mapping (protocols → gate checks)

The gate script evaluates, at minimum:
- **P1 hero** — cinematic hero present & canonical (or `hero-rule: interim` flagged)
- **P2 motion** — no ambient loops; reduced-motion honored; frame budget respected
- **P3 vendoring** — no CDN script tags for 3D/animation
- **P4 layout** — bespoke composition declared (reviewer attests)
- **P5 brand** — palette matches SITE_REGISTRY for the target site
- **P6 icons** — custom/cleared icons only
- **P7 forms** — if the artifact has a form: house form protocol + Turnstile lockstep
- **P8 independence** — no new paid service introduced
- **P9 accessibility** — contrast ratios computed; keyboard walkthrough; live region
- **P10 copy** — numbers sourced; Cialdini levers honest; Pinker checks
- **P11 video** — if video: the standing presenter/voice casting per the project brief
- **P12 verification** — artifact viewed live firsthand by the gate runner
- **P13 voice** — no private/internal names in public copy; signature rule respected
- **P14 no-deploy** — job produced no commits to main, no merges, no deploy triggers
- **P15 reference-consult** — where house protocols don't answer a style/palette/font question, `arsenal/reference/` (ui-ux-pro-max catalogs) consulted before inventing anything new. Catalogs are lookup material only — never design authority; generic defaults that clash with the house register stay rejected.

Checks are `pass` / `fail` / `waived` (waiver requires a named reason + who approved;
waivers are journaled). A `fail` on P7/P8/P9/P14 blocks the ship decision outright —
these are fail-closed protocols.

## Flyer/collateral jobs
Same gate, page-specific checks (P1 hero, P3 vendoring, P7 forms) marked N/A with
reason; P4/P5/P6/P10/P13 carry the weight. Output is a print/digital file — P12 means
opening the actual exported file, not the design tool's preview.

## Running it
```bash
# 1. write a job manifest (see roma_graph.json -> manifest schema)
python3 ~/design-second-brain/workflow/bin/run_design_gate.py --job manifest.json
# 2. red-team the plan before the ship decision
python3 ~/sprint-engine/bin/roma.py verify --file plan.json
# 3. record the run in the sprint graph (optional but recommended)
python3 ~/sprint-engine/bin/sprint_graph.py add-node --kind artifact --title "design-gate: <page> <verdict>"
```
