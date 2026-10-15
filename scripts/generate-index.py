#!/usr/bin/env python3
"""Regenerate the README skills index and skills_index.json from SKILL.md frontmatter.

Stdlib only. Run from anywhere:

    python3 scripts/generate-index.py

The README region between <!-- BEGIN SKILLS INDEX --> and <!-- END SKILLS INDEX -->
is rewritten in place; skills not listed in CATEGORIES fall under "Other".
CI runs this script and fails the PR if README.md or skills_index.json drift.
"""
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
README = os.path.join(REPO_ROOT, "README.md")
INDEX_JSON = os.path.join(REPO_ROOT, "skills_index.json")
BEGIN = "<!-- BEGIN SKILLS INDEX -->"
END = "<!-- END SKILLS INDEX -->"

CATEGORIES = [
    ("Agent operations", [
        "subagent-security-brief", "chief-of-staff", "agent-spawner",
        "war-room", "war-room-doctrine", "fleet-doctrine",
        "board-of-thirteen", "writers-war-room",
    ]),
    ("Research & verification", [
        "storm-research", "crucible", "entity-verification",
        "demand-mining", "submission-gate", "paper-foundry",
        "context7", "web-fetch", "phoenix", "rea",
    ]),
    ("Engineering systems", [
        "sprint-engine", "eng-discipline", "prototype-sprint",
        "tailscale-admin", "browser-skill", "blender",
        "lambda-cloud", "ontology-floor",
    ]),
    ("Business & growth", [
        "brand-sprint", "city-map-strategy", "income-blueprint",
        "media-company-marketing", "packaging-lab", "revenue-wedge",
        "minerva", "typesafe-jev",
    ]),
    ("Creative & media", [
        "creative-production", "atelier-character-sheet",
        "cinematic-letter-video", "living-mesh-cinematic",
        "signal-lab-cinematic", "video-learn", "voice-dna",
    ]),
    ("Shipping & distribution", [
        "ios-ship", "appstore-connect",
    ]),
    ("Connectors & APIs", [
        "cloudflare", "codemagic", "contrado", "elevenlabs", "fred",
        "github", "google-ads", "groq", "huggingface", "nvidia",
        "prodigi", "buttondown", "raisely", "sam-gov",
        "simpler-grants-gov", "stripe", "telegram-bot", "zeffy",
        "zenodo",
    ]),
]


def parse_frontmatter(path):
    """Minimal frontmatter reader: top-level `key: value` pairs (quoted or plain)."""
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        raise ValueError(f"{path}: missing frontmatter")
    block = text.split("---", 2)[1]
    meta = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
            try:
                val = json.loads(val)
            except Exception:
                val = val[1:-1]
        meta[key] = val
    return meta


def main():
    skills = []
    for name in sorted(os.listdir(SKILLS_DIR)):
        skill_md = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        meta = parse_frontmatter(skill_md)
        if meta.get("name") != name:
            print(f"warning: {name}: frontmatter name is {meta.get('name')!r}", file=sys.stderr)
        skills.append({
            "name": name,
            "description": meta.get("description", ""),
            "path": f"skills/{name}",
        })

    cat_of = {}
    for cat, members in CATEGORIES:
        for m in members:
            cat_of[m] = cat
    for s in skills:
        s["category"] = cat_of.get(s["name"], "Other")

    # README region
    by_cat = {}
    for s in skills:
        by_cat.setdefault(s["category"], []).append(s)
    ordered_cats = [c for c, _ in CATEGORIES if c in by_cat]
    if "Other" in by_cat:
        ordered_cats.append("Other")
    out = []
    for cat in ordered_cats:
        out.append(f"### {cat}")
        out.append("")
        out.append("| Skill | Description |")
        out.append("|---|---|")
        for s in sorted(by_cat[cat], key=lambda x: x["name"]):
            desc = s["description"].replace("|", "\\|")
            out.append(f"| [{s['name']}](skills/{s['name']}/SKILL.md) | {desc} |")
        out.append("")
    region = "\n".join(out).rstrip() + "\n"

    readme = open(README, encoding="utf-8").read()
    if BEGIN not in readme or END not in readme:
        print(f"error: README.md is missing the {BEGIN} / {END} markers", file=sys.stderr)
        return 1
    new_readme = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        BEGIN + "\n\n" + region + "\n" + END,
        readme, flags=re.S)
    if new_readme != readme:
        open(README, "w", encoding="utf-8").write(new_readme)
        print("README.md index region updated")
    else:
        print("README.md index region already current")

    payload = {"skills": [
        {"name": s["name"], "description": s["description"],
         "path": s["path"], "category": s["category"]}
        for s in sorted(skills, key=lambda x: x["name"])
    ]}
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if not os.path.exists(INDEX_JSON) or open(INDEX_JSON, encoding="utf-8").read() != rendered:
        open(INDEX_JSON, "w", encoding="utf-8").write(rendered)
        print("skills_index.json updated")
    else:
        print("skills_index.json already current")
    print(f"{len(skills)} skills indexed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
