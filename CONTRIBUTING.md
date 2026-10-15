# Contributing — the skill authoring standard

How skills in this repo are authored, edited, reviewed, and debugged. Read it before
creating or changing any skill. New skills start from [`template/skill-template.md`](template/skill-template.md).

> Methodology adapted from David Ondrej's `effective-agent-skills` (Agent Skills, MIT).
> The craft is his; the credential law (§7a) and the audit discipline are this repo's.

---

## 1. What a skill is

A directory containing a `SKILL.md`: YAML frontmatter (**name**, **description** —
the routing contract), a markdown **body** (loaded only when the skill activates),
optional **scripts** under `bin/`, and optional **reference** material the body
points at. Per the [Agent Skills specification](https://agentskills.io/specification),
frontmatter may carry only `name`, `description`, `license`, `compatibility`,
`metadata`, and `allowed-tools`; `name` must equal the directory name; `description`
is capped at 1024 characters.

Skills earn their keep two ways: instructions load only when relevant (context
efficiency), and multi-step procedures become auditable, repeatable, composable
workflows.

## 2. Two patterns — name which one you are building

- **Pattern A — Capability primitive.** A thin wrapper over a deterministic
  script/CLI/API. Logic lives in code; the documentation teaches the agent how to
  invoke it. Reliability comes from the script, not the prose. Use when the
  bottleneck is "the agent can't do X."
- **Pattern B — Process primitive.** A methodology the agent follows. Pure
  documentation, no scripts. Reliability comes from explicit procedure +
  checklists. Use when the bottleneck is "the agent's process/output quality is bad."

A mature set uses both. Never weld a capability and a discipline into one skill.

## 3. The routing contract — the description

Before loading anything, the agent sees only `name` + `description`. **If a skill
does not fire, the description is wrong 95% of the time — not the body.**

Include three elements:

1. **What** it does (one phrase).
2. **When** to use it (trigger phrases / situations).
3. **Differentiator** vs sibling skills (prevents routing conflicts).

**Never summarize the *how* in the description.** A step-by-step summary makes the
agent follow the summary and skip loading the body. Describe *what* + *when*, never
*how*. Avoid `<` and `>` in name/description (injection risk). Keep the name short
and unique.

## 4. Progressive disclosure

Three stages, each cheaper the earlier it stops:

- **Discovery** — name + description, surfaced by skill search. Cheap; you can
  carry dozens of skills.
- **Activation** — the full body, loaded only on a match.
- **Execution** — scripts and reference material, pulled only when needed. Scripts
  run without their source bloating context.

Consequence: push rarely-needed detail out of the body into scripts or
clearly-pointed reference files. Keep the body lean (under 500 lines).

## 5. Do this

- **Draft the description first.** Read it back: would an agent know exactly when
  to fire it?
- **Keep the documentation lean.** Past a point, you are encoding logic that
  belongs in a script.
- **stdlib/curl-first, prose-second.** Show concrete commands with inline comments;
  the agent pattern-matches on syntax.
- **Push determinism into scripts.** Anything fragile, repetitive, or where
  variation is a bug → a script. Prose only for judgment.
- **Match strictness to fragility.** Loose heuristics when many approaches are
  valid; templates when there is a preferred shape; exact scripts + strict step
  lists when a wrong move is costly (deploys, migrations, signing).
- **Build validation loops.** State an explicit verify → fix → re-verify: prove
  the deploy/hash/artifact/live-state, never trust a green log or a peer's
  narration.
- **State-check before action.** Verify setup, then branch (e.g. "confirm the
  profile exists via GET …; if not, create it").
- **One skill, one concern.** Compose at runtime; do not bundle "the X workflow."
- **Persistent artifacts for memory.** Skills that write durable outputs give
  future sessions continuity.
- **Cite the methodology** when you encode a known discipline (STORM, red-team,
  TDD) — it gives the agent a coherent model to align with.
- **Keep documentation in sync with scripts.** On ANY script change, update the
  documentation to match — stale docs are the #1 cause of skill failure on later
  runs.

## 6. Runtime gotchas (hard-won — encode these)

- **Do not assume `requests`/`pip`.** Agent sandboxes often lack both. Prefer
  stdlib (`urllib`) or `curl`; for signing, `openssl` is usually present,
  `cryptography` often is not — say so in `compatibility:` when you need it.
- **Target Python 3.9** for skill scripts unless you control the runtime (no
  PEP-604 `X | None`, no `match`).
- **Secrets are env vars, never args.** Read from the environment or your
  platform's credential store; never pass a secret as a CLI argument that lands
  in logs.
- **Resolve credentials at run time, from the store — every run.** Do not cache
  secret values in files, and never ask the user for a credential that already
  exists in their store.

## 7. Credentials & security — the guardrail

- **Store only.** Secrets live in your platform's credential store / secret
  manager, entered by the owner, injected at runtime. NEVER put a secret in chat,
  documentation, a script literal, a log, or a public URL.
- **Fail closed.** If a required secret is unset, stop — never hardcode a fallback
  secret in an `os.getenv(..., default)`. (A real production leak came from
  exactly this pattern.)
- **One skill per provider rail.** Credential isolation, not one mega-skill
  holding every secret.
- **Prefer first-party APIs** and infrastructure you control over metered
  third-party services that add recurring cost and another trust surface.
- **Audit before import.** For any outside skill: read every file, audit `bin/`
  for network calls / file access / injection, watch for typosquatting, pin to a
  commit. Pure-prose Pattern-B skills carry near-zero import risk — no code to run.

### 7a. THE CREDENTIAL-SCHEMA LAW

Where your platform lets a skill declare credential fields (a `credentialSchema`
or equivalent), every declaration must satisfy ALL of these — no exceptions:

1. **Nothing mandatory.** Every field is `required: false`, always. The skill must
   fully function on its keyless/public lane with an empty vault; credentials only
   ADD capability. A `required: true` field is a law violation on sight.
2. **Minimum fields — nothing derivable.** Never declare a field whose value
   derives from another field (wallet address from private key, account SID from
   an API-key probe, fingerprint from a key, endpoint from an account id) or whose
   value already lives in the platform vault. Scripts compute derived values; the
   vault holds only irreducible secrets. A vault-held value may appear ONLY as an
   explicitly-labeled optional standalone override.
3. **No cross-rail clutter.** A skill declares only the fields of ITS OWN rail.
   Never duplicate a sibling skill's credentials "for convenience" — that creates
   a second collection surface for the same secret. Borrow at runtime via the
   documented multi-skill pipeline (run each leg under the skill that holds the
   credential) or via the vault.
4. **Hints short and honest.** Under ~120 characters, no example-URL clutter, no
   phantom-field noise. For multi-line secrets (PEM blocks): masked fields fight
   newlines, so the script must accept a **single-line base64** of the file as an
   alternate paste format (and auto-repair flattened PEMs); say so in the hint.
5. **Retired skills shed their schemas — and get DELETED.** A retired/superseded/
   do-not-use skill must not declare credential fields. And know the limit of a
   schema edit:

> **SCHEMA-STRIP ≠ VALUE-PURGE.** Removing a field from a credential schema stops
> RE-ENTRY (the prompt no longer shows it) but does NOT purge an already-stored
> value, and for proxy-delivered credentials the injection at the bound host
> REMAINS ACTIVE. The only true purges are a platform-level credential clear or
> **deleting the skill**. Consequence: when retiring a skill that holds stored
> secrets, schema-strip it for hygiene, then DELETE the skill — never assume the
> strip cleared the secret, and never leave an account-scoped token stored on a
> "do-not-use" pointer.

## 8. Do not do this (anti-patterns)

- Do not re-teach what the model knows (no language tutorials).
- Do not put human-facing docs (README/CHANGELOG) inside the skill.
- Do not write vague descriptions ("a helpful skill for docs").
- Do not build monolithic mega-skills (design + plan + build + ship = a framework,
  not a skill).
- Do not assume the agent will infer — be explicit about steps that matter.
- Do not ship style-only variants (tone/format belongs in a prompt/preference).
- Do not ignore failure modes — for every step that can fail, say what failure
  looks like and what to do.
- Do not bake in time-sensitive info ("as of Q3 2026…") — fetch live or omit.
- Do not use absolute paths; relative + forward slashes. Never commit a path from
  your own machine.
- Do not declare `required: true` credential fields, derivable fields, or another
  rail's credentials (the schema law, §7a).
- Do not treat a schema edit as a secret purge — stored values and proxy injection
  survive field removal (§7a.5).

## 9. Authoring workflow

1. **Find the gap** — where the agent repeatedly fails or needs re-prompting.
2. **Pick the pattern** — A (need a tool) or B (need a method).
3. **Draft the description first** — what + when + differentiator.
4. **Write the smallest body that works;** add only when testing reveals gaps.
5. **Move detail to scripts / reference sections** once the body grows.
6. **Test triggering** — does skill search surface it on a natural request? If
   not, fix the description.
7. **Test execution** — run it; if output is wrong, fix the body/script.
8. **Adversarial test** — have another model ask "what edge cases break this?"
   Patch the gaps.
9. **Version it** — skills are code; bump `metadata.version`, and update
   documentation with every script change.

## 10. Ship checklist

- [ ] Description = what + when + differentiator, with real trigger phrases; no
      *how*-summary; ≤1024 chars
- [ ] Pattern named (A capability / B process)
- [ ] Body lean (<500 lines); rarely-needed detail pushed to scripts/reference
- [ ] Determinism in scripts; judgment in prose; strictness matches fragility
- [ ] Validation / verify loop stated
- [ ] State-check before action where relevant
- [ ] Failure modes documented
- [ ] Secrets only via the credential store; fail-closed; nothing in docs/logs
- [ ] **Schema law (§7a): every field `required: false`; no derivable fields; no
      cross-rail fields; vault-held values only as labeled optional overrides**
- [ ] **Hints <120 chars; multi-line/PEM secrets accept single-line base64 (and
      the script repairs flattened PEMs)**
- [ ] **Keyless lane works with an empty vault (credentials only add capability)**
- [ ] **If this ships as a replacement for an old skill: schema-strip AND delete
      the old one — schema-strip alone does not purge stored secrets (§7a.5)**
- [ ] stdlib/curl-first; Python 3.9-safe
- [ ] One concern; composes with siblings
- [ ] Documentation matches current scripts
- [ ] No human-facing docs, no time-sensitive info, relative paths only
- [ ] Ran the identifier sweep (names, emails, phone numbers, account/team IDs,
      absolute home paths, key-shaped strings) over the whole skill directory

## 11. First principles, compressed

1. The description routes; the body executes. Get both right independently.
2. Tokens are scarce; scripts/references are cheap. Defer detail until needed.
3. Determinism from code; judgment from prose.
4. One skill, one concern. Composition beats bundling.
5. Agents forget; persistent artifacts are their memory.
6. The model knows a lot — only add what is missing.
7. Verify before you enshrine.
8. Secrets live in the vault, and only there — optional, minimal, on-rail (§7a).
9. Prefer infrastructure you control over metered SaaS.
10. A removed field is not a removed secret. Deletion purges; edits don't.

---

> Provenance: methodology adapted from David Ondrej's `effective-agent-skills`
> (MIT). §7a codifies a standing credential-schema law and the schema-strip ≠
> value-purge finding, verified live in a 113-skill fleet audit.
