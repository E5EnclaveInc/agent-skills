# Living-mesh failure modes (solved — do not reintroduce)

Two real failures from the services hero lineage, documented so no future
build repeats them. Both are *design* failures, not code bugs: each was
working as written.

## 1. The play-once freeze (CERTAIN cause of "still not moving")

**What shipped (PR #66):** a ~4-second "ignition" show ending in a
permanently frozen frame — by design. The script was defer-loaded, so the
show played during page load, while the viewer was watching the URL bar /
the page settle.

**Why it failed:** anyone who missed the first seconds saw only the
after-state. On both of the reviewer's phone viewings they were looking at a
frozen frame. A show with an ending guarantees most viewers see only the
ending.

**The fix (PR #68):** continuous ambient loop — nothing to miss, no
after-state. There is no "final frame" because the mesh never finishes.

**Rule:** living-mesh treatments are ambient loops, never play-once shows.
(Play-once belongs to signal-lab-cinematic's instrument register, where the
replay console makes the ending explicit and re-runnable.)

## 2. The phantom freeze heuristic (LIKELY contributor)

**What shipped (PR #66):** the hero froze when
`(navigator.hardwareConcurrency <= 4) || navigator.connection.saveData`.

**Why it failed:** neither condition requires an accessibility setting. iOS
Safari reports `navigator.connection.saveData = true` when Low Data Mode is
on — a cellular/Wi-Fi setting, not accessibility. Low core counts are
reported by real phones in low-power states. The reviewer had no
accessibility settings on; the heuristic froze his hero anyway. Device and
network heuristics are not accessibility settings and they misfire on real
hardware.

**The fix (PR #68):** `still` honors ONLY the explicit
`prefers-reduced-motion` preference. Everything else — low cores, data
saver, old devices — gets the full ambient mesh (the mesh is cheap:
≤96 nodes, DPR ≤2, offscreen pause).

**Rule:** no heuristics. `matchMedia('(prefers-reduced-motion: reduce)')`
is the single gate. If motion is too heavy for a weak device, make the
motion cheaper — never silently still it.

## 3. Watch-list (not yet bitten, guard anyway)

- **Tick spam:** writing the tick/status DOM every frame costs layout and
  can spam screen readers. Dedupe writes; announce state changes only.
- **Unseeded randomness:** `Math.random()` in layout means the composed
  frame differs per load — the reduced-motion frame and no-JS poster stop
  matching. Seed layout randomness (mulberry32); `Math.random()` is fine
  for ongoing behavior (drop timing, pulse routing).
- **Partitioning the mesh:** a drop that isolates nodes teaches failure,
  not resilience. Always guard drop targets (≥2 live neighbors) and reroute
  pulses off live edges only.
- **Background-tab time jump:** without dt clamping, a tab returning after
  minutes teleports the simulation. Clamp dt (≤0.05s).
- **Offscreen burn:** rAF running while scrolled past wastes battery and can
  throttle the visible page. IntersectionObserver start/stop is mandatory.
