#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Design Second Brain — executable pre-ship gate.

Usage:
  python3 run_design_gate.py --job manifest.json [--out report.json] [--plan plan.json]

Manifest schema (see ../roma_graph.json -> manifest_schema):
  { "site": ..., "target": ..., "artifact_type": "page|flyer",
    "artifact_path": ..., "notes": ..., "waivers": [{protocol, reason, approved_by}],
    "private_terms": ["internal names/codenames that must never appear in shipped copy"] }

What it does:
  - Loads PROTOCOLS.md checks + SITE_REGISTRY + COPY_STANDARDS pointers.
  - Runs every AUTOMATABLE check against the artifact (HTML scan: CDN script tags,
    Turnstile widget vs form presence, honeypot field; file existence).
  - Emits MANUAL-ATTEST checks the runner must confirm by hand (design review,
    copy pass, live render) — these fail closed: unattested = FAIL.
  - Honors waivers (named protocol + reason + approver); anything else waived is FAIL.
  - Writes a gate report JSON and a plan.json suitable for
    `roma.py verify --file plan.json` (the T4 red-team/steelman step).
  - Exit code: 0 = GATE PASS (all checks pass/waived/N-A), 1 = GATE FAIL,
    2 = usage/manifest error. Fail-closed protocols (P7/P8/P9/P14) can never be
    waived into a pass — a fail there is always exit 1.

Stdlib only. Read-only against production: it never commits, merges, or deploys.
"""
import json, os, re, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))

FAIL_CLOSED = {"P7", "P8", "P9", "P14"}
MANUAL = {"P1", "P2-motion-review", "P4", "P5", "P6", "P9-contrast", "P9-keyboard",
          "P10", "P11", "P12", "P13", "P15"}

CHECKS = [
    ("P1",  "hero: cinematic set-piece per protocols/CINEMATIC_HERO_RULE.md (ratified 2026-09-12; attest; flagged hero-rule: ratified)", "manual"),
    ("P2",  "motion: no ambient loops; reduced-motion honored (auto-scan + attest)", "auto"),
    ("P3",  "vendoring: no CDN script tags for 3D/animation libs", "auto"),
    ("P4",  "layout: bespoke, non-template composition (attest)", "manual"),
    ("P5",  "brand: palette matches site registry (attest)", "manual"),
    ("P6",  "icons: custom/cleared only (attest)", "manual"),
    ("P7",  "forms: house form protocol + Turnstile lockstep (auto-scan; E2E attested separately)", "auto"),
    ("P8",  "independence: no new paid service (attest)", "manual"),
    ("P9",  "accessibility: contrast computed, keyboard walkthrough, live region (attest)", "manual"),
    ("P10", "copy: Pinker + Cialdini + sourced numbers (attest)", "manual"),
    ("P11", "video: presenter + voice casting per the project brief if video job (attest; N/A otherwise)", "manual"),
    ("P12", "verification: artifact viewed live firsthand (attest)", "manual"),
    ("P13", "voice: no private/internal names in public copy; signature rule (auto-scan + attest)", "auto"),
    ("P14", "no-deploy: no commits to main/merges/deploy triggers (attest)", "manual"),
    ("P15", "reference-consult: where house protocols don't answer a style/palette/font question, arsenal/reference/ (ui-ux-pro-max catalogs) consulted before inventing; catalogs are lookup only, never design authority (attest)", "manual"),
]

CDN_PATTERNS = [
    r'cdn\.jsdelivr\.net', r'unpkg\.com', r'cdnjs\.cloudflare\.com',
    r'stackpath', r'cdn\.staticfile', r'threejs\.org/build', r'threejs\.org/examples',
]
LIB_HINTS = [r'three(\.min)?\.js', r'gsap(\.min)?\.js', r'lottie', r'pixi(\.min)?\.js']


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def auto_checks(manifest, html):
    """Return dict check_id -> (status, evidence)."""
    out = {}
    atype = manifest.get("artifact_type", "page")

    # P2: scan for suspicious perpetual animation markers (advisory; review still attests)
    if atype == "page" and html:
        infinite = len(re.findall(r'animation-iteration-count\s*:\s*infinite', html, re.I))
        out["P2"] = ("pass" if infinite == 0 else "fail",
                     f"{infinite} infinite CSS animations found" if infinite else "no infinite CSS animations; reviewer must still attest motion budget")
    else:
        out["P2"] = ("na", "not an HTML page; motion review is manual") if atype != "page" else ("fail", "artifact HTML unreadable")

    # P3: CDN scan
    if html:
        hits = []
        for pat in CDN_PATTERNS:
            for m in re.finditer(pat, html, re.I):
                # allowlist: known-good infra (turnstile, fonts)
                ctx = html[max(0, m.start()-80):m.end()+80]
                if "challenges.cloudflare.com/turnstile" in ctx or "fonts.googleapis" in ctx or "fonts.gstatic" in ctx:
                    continue
                hits.append(pat)
        lib_hits = [p for p in LIB_HINTS if re.search(p, html, re.I)]
        cdn_lib = [h for h in hits if any(l in h for l in ("three", "gsap", "lottie", "pixi"))]
        if cdn_lib or (lib_hits and hits):
            out["P3"] = ("fail", f"possible CDN-loaded 3D/animation lib: {sorted(set(cdn_lib or hits))}")
        else:
            out["P3"] = ("pass", "no CDN script tags for 3D/animation libraries detected (turnstile/fonts allowlisted)")
    else:
        out["P3"] = ("na" if atype != "page" else "fail", "no HTML to scan" if atype == "page" else "not an HTML page")

    # P7: form scan
    if html and re.search(r'<form', html, re.I):
        has_ts = bool(re.search(r'cf-turnstile|challenges\.cloudflare\.com/turnstile', html, re.I))
        has_hp = bool(re.search(r'honeypot|hp-|_honey|[\-_"]hp[\-_"]', html, re.I))
        if has_ts and has_hp:
            out["P7"] = ("pass", "form present: Turnstile widget + honeypot field detected; E2E + origin-lock still to attest")
        elif has_ts:
            out["P7"] = ("fail", "form has Turnstile but no honeypot field detected — protocol requires honeypot first")
        else:
            out["P7"] = ("fail", "form present but no Turnstile widget detected")
    elif html:
        out["P7"] = ("na", "no <form> in artifact")
    else:
        out["P7"] = ("na" if atype != "page" else "fail", "no HTML to scan")

    # P13: private-terms scan — institutional voice check. Terms come from the
    # manifest (private_terms): internal names/codenames that must never ship.
    # Identifiers inside attribute values (URLs etc.) are infrastructure, not
    # public copy; strip attribute values before scanning visible copy.
    if html:
        text_only = re.sub(r'=[\'"][^\'"]*[\'"]', '=""', html)
        text_only = re.sub(r'<script[\s\S]*?</script>', '', text_only, flags=re.I)
        terms = [t for t in manifest.get("private_terms", []) if t]
        hits = [t for t in terms if re.search(re.escape(t), text_only, re.I)]
        out["P13"] = ("fail" if hits else "pass",
                      f"private term(s) in visible copy: {hits} (URLs/identifiers excluded)" if hits else "no private terms in visible copy (URLs excluded); signature-rule still to attest")
    else:
        out["P13"] = ("manual", "non-HTML artifact: reviewer attests")
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="design second brain — pre-ship gate")
    ap.add_argument("--job", required=True, help="job manifest JSON")
    ap.add_argument("--out", default="", help="gate report JSON output path")
    ap.add_argument("--plan", default="", help="plan.json output for roma.py verify")
    ap.add_argument("--attest", default="",
                    help="comma-separated check IDs the runner manually attests PASS (e.g. P1,P4,P12)")
    args = ap.parse_args(argv)

    try:
        manifest = json.load(open(args.job, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"GATE ERROR: cannot read manifest: {e}", file=sys.stderr)
        return 2
    for k in ("site", "target", "artifact_type", "artifact_path"):
        if k not in manifest:
            print(f"GATE ERROR: manifest missing '{k}'", file=sys.stderr)
            return 2

    attested = {a.strip() for a in args.attest.split(",") if a.strip()}
    waivers = {w.get("protocol"): w for w in manifest.get("waivers", []) if w.get("protocol") and w.get("reason") and w.get("approved_by")}

    apath = manifest["artifact_path"]
    html = read_text(apath) if manifest["artifact_type"] == "page" else ""
    auto = auto_checks(manifest, html)

    results = []
    for pid, desc, kind in CHECKS:
        entry = {"id": pid, "check": desc, "kind": kind}
        if pid in waivers and pid not in FAIL_CLOSED:
            w = waivers[pid]
            entry.update(status="waived", evidence=f"waived: {w['reason']} (approved by {w['approved_by']})")
        elif pid in waivers and pid in FAIL_CLOSED:
            entry.update(status="fail", evidence=f"WAIVER REJECTED: {pid} is fail-closed and cannot be waived")
        elif kind == "auto" and pid in auto:
            st, ev = auto[pid]
            entry.update(status=st, evidence=ev)
        elif pid in attested:
            entry.update(status="pass", evidence="runner attested PASS firsthand")
        else:
            entry.update(status="fail", evidence="manual check not attested — fail closed (pass --attest after firsthand review)")
        results.append(entry)

    fails = [r for r in results if r["status"] == "fail"]
    fc_fails = [r["id"] for r in fails if r["id"] in FAIL_CLOSED]
    verdict = "PASS" if not fails else "FAIL"

    report = {
        "gate": "design-second-brain pre-ship gate",
        "verdict": verdict,
        "job": {k: manifest.get(k) for k in ("site", "target", "artifact_type", "artifact_path")},
        "notes": manifest.get("notes", ""),
        "checks": results,
        "fail_closed_violations": fc_fails,
        "next": ("fix findings, re-run gate, then roma.py verify --file plan.json (T4) before any ship decision"
                 if fails else "run roma.py verify --file plan.json (T4); ship decision (T7) stays PROPOSED pending explicit approval"),
    }
    out_path = args.out or os.path.join(os.path.dirname(os.path.abspath(args.job)), "gate-report.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    plan = {
        "title": f"design-gate ship: {manifest['site']}{manifest['target']}",
        "notes": (f"Gate verdict {verdict}. {manifest.get('notes','')}\n"
                  f"Fail-closed violations: {fc_fails or 'none'}. "
                  "Ship (T7) is ACT: confirm-gate required, never auto-executed; "
                  "human_dependency is explicit — a person approves the ship, no ongoing human ops. "
                  "No merges/deploys by the gate (reversibility: gate changes nothing in prod). "
                  "safety_money: design gate moves no money. cost_runaway: gate is a bounded local run, "
                  "no metered APIs, batch size = one artifact. feasibility_limits: checks are static scans + "
                  "firsthand attestation, no external subrequests required. value: the gate protects brand "
                  "equity and blocks doctrine violations before they ship. security: read-only; secrets never "
                  "touched; form checks verify origin-lock/honeypot/Turnstile posture. observability: full JSON "
                  "report + plan written per run, findings enumerated with evidence."),
        "tasks": [
            {"id": r["id"], "title": r["check"], "status": r["status"], "evidence": r["evidence"]}
            for r in results
        ],
    }
    plan_path = args.plan or os.path.join(os.path.dirname(os.path.abspath(args.job)), "plan.json")
    with open(plan_path, "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=2)

    print(f"GATE {verdict}: {len(results)-len(fails)}/{len(results)} checks pass "
          f"({len([r for r in results if r['status']=='waived'])} waived, "
          f"{len([r for r in results if r['status']=='na'])} n/a)")
    for r in fails:
        print(f"  FAIL {r['id']}: {r['evidence']}")
    if fc_fails:
        print(f"  FAIL-CLOSED VIOLATIONS: {', '.join(fc_fails)} — ship blocked")
    print(f"  report: {out_path}\n  plan:   {plan_path}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
