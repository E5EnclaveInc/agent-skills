# Agent Skills — production set

[![skills.sh](https://skills.sh/b/E5EnclaveInc/agent-skills)](https://skills.sh/E5EnclaveInc/agent-skills)

Battle-tested [Agent Skills](https://agentskills.io) from a working agent fleet: delegation safety, deliberation, research, verification, and shipping pipelines. Every skill here runs in production; every skill here has been scrubbed of credentials, personal data, and machine-specific paths before publication (see [SECURITY.md](SECURITY.md)).

## Install

**Agent Skills CLI** (works with Claude Code, Cursor, Codex, and 40+ other agents):

```bash
npx skills add E5EnclaveInc/agent-skills
```

Install a single skill:

```bash
npx skills add E5EnclaveInc/agent-skills --skill war-room
```

**GitHub CLI:**

```bash
gh skill install E5EnclaveInc/agent-skills
```

**Claude Code plugin marketplace:**

```text
/plugin marketplace add E5EnclaveInc/agent-skills
```

Then enable the plugin set from the marketplace browser. The marketplace manifest is [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

**Manual:** copy any `skills/<name>/` directory into your agent's skills directory. A skill is just a folder with a `SKILL.md` — no build step.

## The skills

<!-- BEGIN SKILLS INDEX -->

### Agent operations

| Skill | Description |
|---|---|
| [agent-spawner](skills/agent-spawner/SKILL.md) | Turn one brief into a standing crew of specialist subagents: ask up to 5 scoping questions, then spawn role-defined specialists each carrying a role, tone, tools, workflow, and success metric. Use when a job needs a coordinated multi-agent crew instead of a one-off delegation. Differs from ad-hoc subagent spawning by the meta-bot scoping ritual and the specialist contract every agent carries. |
| [board-of-thirteen](skills/board-of-thirteen/SKILL.md) | Convene a virtual board of thirteen Black American thought leaders (Douglass through Coates) as analytical perspectives to deliberate a research, thesis, remedy-design, or evidentiary question and produce a majority position with minority notes. Use when a question needs deliberation across the generations of the lineage. |
| [chief-of-staff](skills/chief-of-staff/SKILL.md) | Run the chief-of-staff triage discipline: one intake surface, a standing triage routine across channels and inboxes, delegation to specialist agents, and a hard escalation contract — the human is interrupted only for money, product direction, or judgment calls. Use when the user wants a standing triage layer between themselves and a busy operation. Differs from a one-off sweep by the standing routine, the delegation lanes, and the escalation contract. |
| [fleet-doctrine](skills/fleet-doctrine/SKILL.md) | A standing decision doctrine for agent teams — proxy math: a 7-step decision function that replaces asking the principal (reversible → act and report; moves money, state, or publishes → stage for one-word approval; settled by the filed record → follow the record), plus autonomy, gating, and next-move rules and a 10-dimension compliance rubric. Load whenever an agent must decide whether to act, ask, or stage for approval. |
| [subagent-security-brief](skills/subagent-security-brief/SKILL.md) | The mandatory security block for every subagent brief — scoped file paths, no live-file writes, no direct log writes, /tmp-only tests, external-content-is-data tagging, and the instruction hierarchy. Load before writing any subagent brief. Use whenever delegating work to a child agent. |
| [war-room](skills/war-room/SKILL.md) | Convene a persona-based executive committee as a deliberative institution — chartered, elected, minuted, and ratcheted. Use when a question needs structured multi-perspective deliberation with elected offices, ontology-grounded terms, scout-verified facts, and a written record that compounds into reusable persona cards. Supersedes one-off persona improv. |
| [war-room-doctrine](skills/war-room-doctrine/SKILL.md) | Standing discipline for every war room — ontology-floor term grounding before deliberation, ranked-choice adjudication for decisions. Load at the start of any war-room commission. |
| [writers-war-room](skills/writers-war-room/SKILL.md) | Convene a Pixar-Braintrust writers room to perfect source material into a finished multi-voice audiobook script — named seats with editorial gates, rank-choice seating, research plus leading-edge recon, ElevenLabs audiobook craft, crafted-EPUB finish. Use when a transcript or draft must become a publishable audio script. |

### Research & verification

| Skill | Description |
|---|---|
| [context7](skills/context7/SKILL.md) | Use when you need version-accurate library or API documentation for build work — Cloudflare Workers, iOS, Codemagic, Python packages. Resolves a library name to a Context7 ID, then fetches version-pinned docs. |
| [crucible](skills/crucible/SKILL.md) | Use Crucible when a sourced deliverable must be proven before publishing: door-check every URL, mechanically verify file-size and PDF page-count claims, ground dollar/date/attribution figures against live sources, and emit a gated Verification Ledger. |
| [demand-mining](skills/demand-mining/SKILL.md) | Mine public posts and conversations for problems people want agents to solve; rank the themes by willingness-to-pay and speed-to-launch; attach each to an identifiable buyer, a contact path, and a price band. Use for demand research before building anything. Differs from storm-research (literature-first, multi-perspective) by being demand-signal-first and buyer-attached. |
| [entity-verification](skills/entity-verification/SKILL.md) | Verify a business entity's legal and tax standing: state corporate registry lookup, IRS exempt-organization search, SAM.gov federal registration check (for-profit and nonprofit alike), NY DOS API lane, nonprofit 990 financials via ProPublica + IRS BMF, SEC EDGAR for public companies, OFAC sanctions screening, FEC political vetting, and business-mailbox sweep for filing/IRS correspondence. Produces a per-entity status dossier. Use when onboarding, auditing, vetting, or starting up any company or nonprofit. |
| [paper-foundry](skills/paper-foundry/SKILL.md) | Draft and restructure scholarly papers using structural argumentation recipes distilled from the most-cited works in two lanes: reparations economics and Black Atlantic / African diaspora history. Use when drafting a new paper, restructuring a weak one, or strengthening an argument's architecture — 'frame this paper's gap', 'restructure this argument', 'how would the best papers in this lane handle this objection'. The argumentation layer; the submission-gate skill is the verification layer. |
| [phoenix](skills/phoenix/SKILL.md) | Use for LLM-observability pilot work — start the local Phoenix server, run the scripted OTel pilot, query traces. Localhost-only, pilot-scoped, short-lived runs. |
| [rea](skills/rea/SKILL.md) | Use REA (Reverse Engineer Anything) to investigate shipped binaries, apps, and packages: native via Ghidra, JS/Electron static analysis, process capture on owned builds only, and the evidence/ledger contracts. Adopted under per-lane policy gates — read POLICY.md before first use; third-party analysis is not authorized. |
| [storm-research](skills/storm-research/SKILL.md) | Multi-perspective deep research using Stanford OVAL's STORM method (NAACL 2024), adapted for agent search tools. Runs five expert personas, maps their contradictions, synthesizes a sourced briefing, and peer-reviews its own work with confidence scores — the equivalent of ~40 hours of expert reading. Use before any report, decision, investment, competitive analysis, negotiation/interview prep, or presentation where a single-prompt answer would inherit the majority view and miss blind spots. |
| [submission-gate](skills/submission-gate/SKILL.md) | Preflight any scholarly manuscript against the target journal's actual written instructions before submission, so technical returns never happen. Use when preparing, revising, or rechecking a journal submission — 'run the gate', 'preflight this manuscript', 'is this submission-ready', 'cold-review against the journal'. Works from the journal's own author instructions first, encodes every checkable requirement mechanically (including author-anonymization guards), then adversarially reviews what machines cannot check. |
| [web-fetch](skills/web-fetch/SKILL.md) | Use when a subagent needs to read a public web page as markdown without the live-browser path. Fetches a URL and returns markdown (chunked reads supported). Public internet only — internal/private IPs are blocked at the connection layer by a bundled egress proxy. |

### Engineering systems

| Skill | Description |
|---|---|
| [blender](skills/blender/SKILL.md) | Use for 3D scene work in Blender — inspect the scene, run bpy scripts, take viewport screenshots, export scenes. Headless Blender under an isolated unprivileged system account; explicit task-only invocation. |
| [browser-skill](skills/browser-skill/SKILL.md) | Use when the user asks to automate their logged-in Chromium browser: visit and read pages, fill forms, scrape data, click through flows, regression-test a PR's UI, validate a deployed page, or operate a tab they identify. Requires the bsk CLI and browser extension. |
| [eng-discipline](skills/eng-discipline/SKILL.md) | Install the minimum rigorous engineering discipline for a sprint build: the tests that guard the contract, PR hygiene, issue-to-ship loops, and a five-line shipping policy. Use when starting a short build where process must be light but real. Differs from sprint-engine (the task-graph runner) by being the discipline layer inside a build, and from full SDLC process by the explicit strip-to-minimum for a sprint. |
| [lambda-cloud](skills/lambda-cloud/SKILL.md) | Operate Lambda Cloud GPU instances from the CLI: list instance types with live pricing and regional capacity, launch/terminate/restart behind a confirm gate, manage SSH keys and filesystems. Use for evaluation, prototype, or burst GPU work. Credential via the LAMBDA_API_KEY environment variable or ~/.lambda/api_key (mode 600); every mutating command requires --confirm. |
| [ontology-floor](skills/ontology-floor/SKILL.md) | Ground words in math (term → formula + checkable proof) to cut hallucination on hard, rare formalisms: a resolve() lookup, deterministic structural + faithfulness ingestion gates, a self-updating ingest worker, and a Cloudflare R2/D1/Vectorize store layer. Use when a system must compute specialized terms instead of recalling them — and must refuse value/ethical terms rather than ground them. |
| [prototype-sprint](skills/prototype-sprint/SKILL.md) | Ship the thinnest thing that proves the signal today — landing page plus signup, no database — then hand production engineering a clean handoff protocol instead of a pile of prototype. Use when speed-to-signal beats completeness. Differs from a full build by the disposable-first contract and the explicit prototype-to-production handoff. |
| [sprint-engine](skills/sprint-engine/SKILL.md) | Use Sprint Engine to run long-horizon autonomous work as a dependency-aware task graph: sqlite graph store, the ROMA loop (Atomizer to Aggregator), and a mandatory red-team/steel-man self-verification gate before execution. |
| [tailscale-admin](skills/tailscale-admin/SKILL.md) | Administer a Tailscale tailnet over the HTTPS API — verify auth, list devices, read/validate/set the ACL policy, and manage the Tailscale SSH rule. |

### Business & growth

| Skill | Description |
|---|---|
| [brand-sprint](skills/brand-sprint/SKILL.md) | Run a time-boxed naming + visual-direction sprint for a new product or company: generate candidate names, score the best by domain, email format, and company-and-product brand fit, adjudicate by consensus, then ship the visual direction (voice, hero copy, CTAs, palette, logo directions, implementation-ready design brief). Use when a build needs its identity before launch. Differs from a design task by the hard timebox and the scored, decided-not-debated naming. |
| [city-map-strategy](skills/city-map-strategy/SKILL.md) | Use for content strategy and planning a marketing campaign at the quarterly level: build a city-map (Grand Central anchor, max 3 quarterly destinations, signal lines, passengers, format stops, cadence timetable) that works backwards from goals instead of content-first. |
| [income-blueprint](skills/income-blueprint/SKILL.md) | Run the five-step AI income-discovery workshop: super-prompt onboarding, personal intelligence blueprint (resume read as business advisor + gap interview), story repository, ranked income ideas with 90-day probabilities, and a day-one market test. Use when designing a money-making workshop or cohort, validating an offer before building it, or coaching someone from idea to first contact. |
| [media-company-marketing](skills/media-company-marketing/SKILL.md) | Use for content strategy, social media growth, and newsletter growth: plan a marketing campaign like a media company — entertainment-first series, the attention→connection→trust funnel, pre-committed metrics, granular audience targeting, and judging viral content correctly. |
| [minerva](skills/minerva/SKILL.md) | Use Minerva for a paper-first markets desk: market data and execution across Kalshi, Polymarket, and Alpaca paper accounts, with hard guardrails, red-gated live orders, and keyless options-data backtest tooling. Live orders stay disabled unless the operator arms them per session. |
| [packaging-lab](skills/packaging-lab/SKILL.md) | Use for packaging: pre-test titles and thumbnails before publishing, edit for retention first, run outreach as a numbers game, and hold non-negotiable publishing slots — the practical, volume-based discipline for earning viral content without guessing. |
| [revenue-wedge](skills/revenue-wedge/SKILL.md) | Design the fastest path from current assets to the first dollar: the wedge offer, its price, the named first buyer, and the payment method — on the thinnest stack that can accept payment. Use when a project must prove it can take money. Differs from revenue strategy documents by the Day-1 payable constraint: a link, not a billing system. |
| [typesafe-jev](skills/typesafe-jev/SKILL.md) | Call TypeSafe's Jev System One decision model: fast structured Choice/Score/Noul judgments (POST /v1/systemone) and model listing (GET /v1/models). Keyed via the TYPESAFE_API_KEY environment variable. Use for decision/classification/eval-judge tasks where a typed answer with calibrated probabilities beats text generation. |

### Creative & media

| Skill | Description |
|---|---|
| [atelier-character-sheet](skills/atelier-character-sheet/SKILL.md) | Turn an outfit reference image into a professional Sovereign Couture fashion character sheet: AI-reconstructed garment visualization on black, with crisp HTML-composed callouts, material crops, color palette, and editorial notes written through Black American fashion lineage. Trigger when the user wants a character sheet, design spec board, or outfit breakdown for a garment. |
| [cinematic-letter-video](skills/cinematic-letter-video/SKILL.md) | Build a 60-second cinematic documentary-evidence video: a silent AI-presenter body, a cloned voiceover, and the subject's own emails/letters composed as evidence cards in an HTML timeline, rendered to MP4 via HyperFrames. Use when a documented outcome — a dispute, a refusal, a paper trail — needs a video where the evidence is the hero: offers on light cards, denials on dark, red only on refusal beats, no faces. |
| [creative-production](skills/creative-production/SKILL.md) | Produce finished creative assets from reference images: a group portrait with a mandatory face-quality pass, video animation of the verified still, and square icon artwork. Use when a user wants character art, campaign creatives, logos, or animated clips from their own reference images — never for the agent platform's own avatar/self-image pipeline. |
| [living-mesh-cinematic](skills/living-mesh-cinematic/SKILL.md) | Make a page cinematic with a living nodal-network simulation — breathing nodes, pulses routing along edges, circuit traces lighting as current passes, and periodic node failure/rerouting/recovery that teaches the system's story. Use when a page needs continuous ambient motion that demonstrates how something behaves (failover, routing, resilience) rather than a play-once film replay. |
| [signal-lab-cinematic](skills/signal-lab-cinematic/SKILL.md) | Make a technical or corporate page cinematic in the laboratory/instrument register — diagrams become labeled, play-once film replays with permanent honesty bugs, telemetry stamps, and fail-open fallbacks. Use when a site reads as a landing page, when diagrams describe instead of demonstrate, or when asked for cinematic motion that is evidence-grade rather than poetic. |
| [video-learn](skills/video-learn/SKILL.md) | Turn tutorial/how-to videos into durable skill knowledge: download, extract timestamped transcripts and UI frames, analyze the demonstrated workflows, and encode them as click-level documentation. Adapted from the public MIT-licensed claude-watch pattern (yt-dlp + ffmpeg + captions + multimodal analysis). |
| [voice-dna](skills/voice-dna/SKILL.md) | Build a named, recallable writing-style profile (Voice DNA) from three writing samples, saved as ghostwriter rules for a person, brand, or client. Use when ghostwriting, keeping AI output out of AI-slop territory, or maintaining one voice per persona/brand/client. |

### Shipping & distribution

| Skill | Description |
|---|---|
| [appstore-connect](skills/appstore-connect/SKILL.md) | Use App Store Connect when working with Apple's App Store Connect API: ES256-JWT REST client for TestFlight distribution, build compliance, beta groups, testers, and external review submission. |
| [ios-ship](skills/ios-ship/SKILL.md) | Use ios-ship to get any app onto a registered iPhone with zero dashboard steps: Codemagic builds, signing groups, the verify_ipa.py ship gate, OTA install pages, and the programmatic App Store submission pipeline. |

### Connectors & APIs

| Skill | Description |
|---|---|
| [buttondown](skills/buttondown/SKILL.md) | Manage a Buttondown newsletter through API v1: verify the key, list and create draft emails from Markdown files, and import/export subscribers as CSV. Drafts only — sending stays a human action. Use when a task involves Buttondown or its newsletter API. |
| [cloudflare](skills/cloudflare/SKILL.md) | Drive the Cloudflare API v4 from the command line: zones, DNS, Workers, R2 object get/put, and any other endpoint, with scoped-token and legacy global-key auth lanes. Use when a task involves Cloudflare or its API. |
| [codemagic](skills/codemagic/SKILL.md) | Drive the Codemagic CI API from the command line: list apps, trigger and poll builds, and inspect build status. Use when a task involves Codemagic builds, apps, or workflows, or asks about Codemagic or its API. |
| [contrado](skills/contrado/SKILL.md) | Work with the Contrado Helix print-on-demand API: browse stores and products, map variants, create and track orders. Use when a task involves Contrado, Helix, or print-on-demand fulfilment through Contrado. |
| [elevenlabs](skills/elevenlabs/SKILL.md) | Drive the ElevenLabs API: text-to-speech, speech-to-text, sound effects, music, voices, dubbing, and usage — with content-hash idempotency, backoff, and quota preflight built in. Use when a task involves ElevenLabs, voice generation, or its API. |
| [fred](skills/fred/SKILL.md) | Query the FRED (Federal Reserve Bank of St. Louis) economic data API: fetch series observations and metadata — interest rates, inflation, employment, and thousands of other series. Use when a task needs FRED data or mentions FRED series IDs. |
| [github](skills/github/SKILL.md) | Call the GitHub REST API from the command line: repos, contents, issues, pull requests, and any other endpoint. Use when a task involves GitHub or its API and a small scriptable client is handier than a full integration. |
| [google-ads](skills/google-ads/SKILL.md) | Drive a Google Ads account through the Google Ads API: GAQL search, campaign/ad-group/ad/keyword mutations, and ad-strength audits. Use when a task involves Google Ads, Ad Grants, or the Google Ads API. |
| [groq](skills/groq/SKILL.md) | Call the GroqCloud API (OpenAI-compatible): list models and run chat completions at Groq speed. Use when a task involves Groq, GroqCloud, or its API. |
| [huggingface](skills/huggingface/SKILL.md) | Run chat completions through Hugging Face's hosted inference router (OpenAI-compatible), including vision models via image input and SSE streaming. Use when a task needs a Hugging Face model call, an independent second-opinion model lane, or HF Inference. |
| [nvidia](skills/nvidia/SKILL.md) | Run chat completions against NVIDIA NIM hosted models (integrate.api.nvidia.com, OpenAI-compatible), with reasoning-effort control, SSE streaming, and catalog listing. Use when a task involves NVIDIA NIM, build.nvidia.com models, or an nvapi key. |
| [prodigi](skills/prodigi/SKILL.md) | Work with the Prodigi print-on-demand API v4: products, quotes, and orders — sandbox by default, live only on request. Use when a task involves Prodigi or its print API. |
| [raisely](skills/raisely/SKILL.md) | Work with the Raisely fundraising API: campaigns, profiles, donations, teams, and registrations. The campaign key is admin-equivalent, so money-moving calls need explicit confirmation. Use when a task involves Raisely or its API. |
| [sam-gov](skills/sam-gov/SKILL.md) | Query SAM.gov entity registrations (UEI, CAGE, status, NAICS, socioeconomic flags) and search federal contract opportunities. Use when a task asks about SAM.gov, entity standing, or federal opportunities. |
| [simpler-grants-gov](skills/simpler-grants-gov/SKILL.md) | Search and fetch U.S. federal grant opportunities through the Simpler.Grants.gov REST API, plus agency search. Use when a task involves federal grant discovery, funding opportunities, or the Simpler.Grants.gov API. |
| [stripe](skills/stripe/SKILL.md) | Call the Stripe API from the command line: account, payment links, prices, products, charges, and any /v1 endpoint, with automatic form-encoding of request bodies. Use when a task involves Stripe or its API. |
| [telegram-bot](skills/telegram-bot/SKILL.md) | Operate a Telegram bot through the Bot API: verify the bot identity, send (automatically chunked) messages, and poll updates. Use when a task involves a Telegram bot, a @BotFather token, or sending Telegram messages programmatically. |
| [zeffy](skills/zeffy/SKILL.md) | Read the Zeffy API (read-only): payments, contacts, and campaigns with cursor pagination, for reconciliation and reporting. Use when a task involves Zeffy or its API. |
| [zenodo](skills/zenodo/SKILL.md) | Work with the Zenodo API: search and read records, manage draft depositions, upload files via bucket URLs, update metadata, create new versions, and publish. Use when a task involves Zenodo, DOIs, or depositing research outputs. |

<!-- END SKILLS INDEX -->

## Proven in production

These are not demos. They are the working procedures of an agent fleet that ships real
deliverables daily — App Store releases, entity due-diligence dossiers, multi-persona
deliberations, long-horizon autonomous sprints. Where a skill carries an example, the
example is generalized from a real run; names, identifiers, and credentials never ship.

## Read before you install

Skills are code. A `SKILL.md` can instruct your agent and ship executable scripts —
treat installing a skill like installing software from a stranger, including ours.
[SECURITY.md](SECURITY.md) carries the audit checklist we recommend before installing
any skill from anywhere, plus the pre-publication scans this repo runs on itself
(gitleaks + trufflehog in CI, and a manual identifier sweep before every release).

## Contributing

New skills and fixes are welcome. The authoring standard — patterns, the routing
contract, progressive disclosure, and the credential-schema law — is in
[CONTRIBUTING.md](CONTRIBUTING.md). Start from [`template/skill-template.md`](template/skill-template.md).

## License

MIT — see [LICENSE](LICENSE).
