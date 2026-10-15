# ElevenLabs Playbook

**Purpose:** the durable, practical reference for production use of ElevenLabs — which model, which settings, which product, what it costs, and what actually works vs what's marketing. Compiled 2026-09-18 from official docs (via the official docs GitHub repo + official skills repo, since docs.elevenlabs.io was unreachable during research), the developer community (GitHub production skill repos, HN, long-form reviews), and measured benchmarks.

**Freshness rule:** model IDs, prices, plan limits, and feature availability are volatile. Before quoting numbers or speccing a build, re-verify against `https://elevenlabs.io/docs/llms.txt` (the community's favorite freshness trick) and the live pricing page. Dated claims below carry their verification date.

**House practice this playbook serves:**
- Library-first, always: enumerate the full voice library before any generation; never a premade/random voice when a canonical clone exists.
- Auth: `ELEVENLABS_API_KEY` environment variable, `xi-api-key` header, `bin/el.py` CLI. Never paste keys in chat or bake them into code — public repos actively leak keys; don't imitate them.
- Prefer covered usage on capped plans and watch consumption against the live account numbers (`GET /v1/user`), not against any recorded figure.

---

## 1. TTS models — which one, when

**Official model matrix** (from `elevenlabs/elevenlabs-docs` `fern/snippets/tts-models.mdx` — the Models docs page source, verified 2026-09-18):

| Model | Official description | Languages | Char limit / request | Latency | Cost |
|---|---|---|---|---|---|
| `eleven_v3` (Alpha) | Most emotionally rich; dramatic delivery, natural multi-speaker dialogue | 70+ | 10,000 (one community source says 3,000 — discrepancy flagged, don't hard-code) | — | — |
| `eleven_multilingual_v2` | Lifelike, consistent; most stable on long-form; "recommended for most use cases" | 29 | 10,000 | — | higher price/char |
| `eleven_flash_v2_5` | Fast, affordable; ultra-low latency | 32 | 40,000 | ~75ms | 50% lower price/char |
| `eleven_turbo_v2_5` | High quality, low latency; good balance | 32 | 40,000 | ~250–300ms | 50% lower price/char |

Latency figures are model-only, never SLAs — quote end-to-end in production.

**Best usage (community-converged, validated):**
| Workload | Model | Why |
|---|---|---|
| Narration / long-form / stage beats | `eleven_multilingual_v2` | Best quality; the only model that preserves cloned voices faithfully |
| Real-time / agents / live loop | `eleven_flash_v2_5` | ~75ms model latency, ~135ms end-to-end; ~50% cheaper; the agents skill's explicit default |
| Expressive character work | `eleven_v3` (aka eleven_v3) | Direction tags, dramatic range — but alpha-flaky, 2× credit cost, NOT for narration or latency paths |
| Balanced middle | `eleven_turbo_v2_5` | Between flash and multilingual; largely superseded by flash for latency, v2 for quality |

**Key facts:**
- Credit cost roughly doubles on the quality tier: Multilingual v2/v3 ≈ $0.10/1k chars ($100/1M); Flash/Turbo ≈ $0.05/1k ($50/1M). ~1,000 chars ≈ 1 minute of audio. (July 2026 public rates — verify.)
- Text-to-dialogue: `POST /v1/text-to-dialogue` (v3, ≤10 voices) → 200 audio — verified live 2026-10-07.
- Blind quality arena (Artificial Analysis, Aug 2026): Flash v2.5 scored 1,083 Elo vs Cartesia Sonic 3.6 at 1,288 — the low-latency tier trades real quality for speed. Multilingual v2/v3 close the gap.
- Professional Voice Clones are **not yet fully optimized for v3** — for v3 work prefer Instant Voice Clones or designed voices; test every voice on v3 before migrating a pipeline. (Community + docs mirror.)
- Never run v3 or multilingual on the latency path.

---

## 1A. Models: Eleven v4 generation

> Authored from vendor docs 2026-10-01; the vendor plugin repo is frozen pre-v4 (1c5f1de, 2026-09-07) — do not source v4 doctrine from it.

**Launch:** v4 generation launched 2026-09-28 (vendor). Python SDK v2.70.0 published the same day; `model_id` is a plain `str` on every TTS surface (no enum gate — v4 IDs pass straight through) — pin pipeline code to **SDK ≥ v2.70.0**. v4 support is decided server-side, not SDK-side. No v4-specific SDK feature was added in v2.70.0 (routine Fern regeneration).

**Model IDs** (verified live via `GET /v1/models`, 2026-10-01):

| Model | Role | Notes |
|---|---|---|
| `eleven_v4` | Expressive TTS | Public (no alpha gate); token cost 1.0 — same per-char price as v3; our new expressive default |
| `eleven_v4_turbo` | Real-time TTS / agents | ~100ms median inference, ~150ms first-speech; the latency twin for live loops and agent turns |

- **90+ languages** (up from 70+ on v3).
- **Control mechanism: inline `[...]` audio tags.** SSML is **disabled on v4** — `<break>` and other SSML tags no longer work; control is natural-language inline tags: `[laughs]`, `[sighs]`, `[pause]`, `[long-pause]`, `[excited]`, `[said angrily in French accent]`, environmental cues like `[light rain]`. Any existing script pipeline using SSML must be rewritten.
- **Per-request limit: 10,000 chars** (~10 min audio), up from 5k on v3 — long-form needs half as many chunks. (v3-era quirk on record: the API enforced 500 chars/request for a cloned voice 2026-09-18 — see Appendix B; v4 not yet measured against this surface.)
- **`voice_settings` surface on v4 = stability, similarity_boost, speed ONLY.** `/v1/models` flags: `can_use_style:false`, `can_use_speaker_boost:false` on both v4 models. Pass only the three supported knobs; `style` and `use_speaker_boost` are STRUCK on v4.
- **Freshness 2026-10-07:** `/v1/models` now also reports `can_use_style:false` on `eleven_v3` (previously documented style modes) — re-verify before any v3 `style` use; the v3 style discussion below needs a freshness check before production use.
- **v4 recipe (verified 2026-10-01):** stability **0.55** / similarity_boost **0.75** / speed **1.0**.
- **No `eleven_v4_conversational` exists** — the only conversational-flagged v3+ model is `eleven_v3_conversational`. Switching a ConvAI agent to `eleven_v4_turbo` is **conditional**: config exposes `tts.model_id` as a settable string and v4_turbo is account-available (no alpha gate), but runtime acceptance of a non-`_conversational` model id is unverified — needs a console check or throwaway-agent PATCH, not a production edit.
- **Professional Voice Clones not served by v4:** `/v1/models` reports `serves_pro_voices:false` on v4 — **CLAIMED conflict** with vendor docs coverage that "PVCs [are] fully supported on v4." Instant (`cloned`) voices are not PVCs — and IVCs do render on v4 in practice (see the clone-carry finding below).
- **Clone-carry finding (falsifiable, n=2):** two production clones — one on `eleven_v4`, one on `eleven_v4_turbo` — each rendered first-try on 2026-10-01 with the migrated recipe (47-char lines, no errors, zero retraining-required signals). Working rule: no retraining for established clone voices; a future render emitting a retraining-required signal re-opens the question.
- **Launch pricing (informational only, promo through 2026-10-12):** v4 $80/1M list → $22/1M; Turbo $40/1M → $11/1M (72% off, vendor-published). If your plan bills from a character pool, list pricing never enters budgeting — watch the pool instead.
- **Tag status:** `[laughs]` RENDER-VERIFIED on `eleven_v4` (49-char render ran 4.16s vs the 3.60s no-tag baseline — the tag inserts audio), **EAR-UNVERIFIED** — acoustic listen-check open as F6. Inline-tag script markup stays CONDITIONAL until F6 closes.

---

## 2. Voice settings — the four knobs

**Officially verified mechanics:**
- **v3 stability modes** (official v3 prompting guide): **Creative** (more expressive, more hallucination-prone) · **Natural** (closest to reference, balanced) · **Robust** (most consistent, least responsive to direction). Use Creative or Natural for maximum tag expressiveness.
- **WebSocket guide example settings:** `stability: 0.5, similarity_boost: 0.8, use_speaker_boost: false` — a sane official baseline.
- Field names: `stability`, `similarity_boost`, `use_speaker_boost`, `style`, `speed`.
- **If `voice_settings` is omitted, the voice's saved defaults apply** — official TTS guide recommends starting from defaults before experimenting.
- Numeric ranges/defaults beyond this are **not** verified in official docs — treat community ranges below as inference.

**What each knob does (community-tested understanding):**
- **stability** — low = more expressive/variable, high = more monotone/consistent. Too low hallucinates words and drifts tone; too high sounds flat. This is the primary "yelling vs. moving" lever.
- **similarity_boost** — how hard the output clings to the source voice. Too high on clones distorts (0.85–0.90 reported as distortion territory).
- **style (exaggeration)** — how much the model leans into stylistic delivery. **On cloned voices, style > 0 causes inconsistent speed, mispronunciation, and extra sounds** (documented); one operator tested 0.25/0.40/0.65 and all artifacted. Keep at **0.0 for clones**.
- **use_speaker_boost** — clarity lift; leave on for production.

**Battle-tested starting recipes (single-operator, validate on our voices before standardizing):**
- Cloned-voice production: stability **0.55**, similarity **0.75**, style **0.0**, speaker boost on.
- By content type: solemn narration 0.55–0.65 (grounded conviction); energetic/hype 0.45–0.50 (test first — goes loose); conversational agents moderate (very low stability = jarring emotional swings between turns).
- Retry ladder: bump stability +0.05 per retry, max 0.75.
- Web folklore: style exaggeration ~3–5% (not 100%) for non-clone expressive work; always generate **full paragraphs**, never single sentences (singles generate flat).

**Console-operator notes (video-sourced, CONSOLE_VIDEOBOOK.md §1):**
- Change **one setting per generation** — otherwise the cause of improvement is unmeasurable.
- **Regenerating a TTS take replaces the displayed take** — download a winner immediately (History exists but deep history is hard to search).
- Generating re-renders the whole text box — strip approved lines or work in small segments.
- Script construction matters as much as sliders: short sentences, commas at breath points, an emphasized phrase isolated on its own line.

---

## 3. v3 audio / direction tags

**Verified official tag list** (official v3 prompting guide, 2026-09-18 — copy strings verbatim; forms are **plural**):
- Voice/delivery: `[laughs]` `[laughs harder]` `[starts laughing]` `[wheezing]` `[whispers]` `[sighs]` `[exhales]` `[sarcastic]` `[curious]` `[excited]` `[crying]` `[snorts]` `[mischievously]`
- Effects: `[gunshot]` `[applause]` `[clapping]` `[explosion]` `[swallows]` `[gulps]`
- Experimental: `[strong X accent]` `[sings]` `[woo]` `[fart]`
- Also appearing in official guide examples (not the formal list): `[frustrated sigh]` `[happy gasp]` `[excitedly]` `[curiously]` `[impressed]` `[dramatically]` `[giggling]` `[with genuine belly laugh]` `[delighted]` `[amazed]` `[warmly]`
- **NOT official — do not encode as documented:** `[chuckle]`/`[chuckles]`, `[pause]`, `[shout]` (`[shout]` appears only as a counterexample: "don't expect a whispering voice to suddenly shout"). `[pause]` is a *client* convention (some clients map SSML `<break>` → `[pause]`), not official docs.
- Tags are **model-interpreted directions, not a closed schema** — the guide says more effective tags likely exist beyond the list.
- **Official punctuation control (v3):** ellipses add pauses and weight; capitalization = emphasis; normal punctuation supplies rhythm. (One community skill warns ellipses can be vocalized — contradicts the official guide; follow the official guide for v3.)

**Cloning note (official):** PVCs are "not fully optimized" for v3 — use an Instant Voice Clone or designed voice when v3 features are required. Tags work with cloned voices, but the voice must be able to perform the behavior: a soft gentle voice won't shout.

**What works in practice:**
- Match the tag to the voice — a somber narrator won't do `[giggles]`; a shouting voice won't do `[whispering]`. Tags behave differently per voice; always pilot. Tags can combine (`[laughs][sarcastic]`).
- Write like a screenwriter, not a programmer: `[laughs]`, `[sighs]`, `[warmly]`, `[dramatically]`. (Community pilots also try non-listed tags like `[chuckle]` or `[softly]` — tags are model-interpreted, so piloting is legitimate, but never encode non-listed tags as officially documented.)
- v3 needs prompts **>250 chars** for consistent output; very short prompts produce inconsistent takes.
- v3 does **NOT** support SSML `<break>` — use audio tags, punctuation, ellipses, and text structure for pacing. Overusing break-style tags causes instability (model speeds up or injects artifacts).
- v3 natively reads IPA in `/slashes/`: `"/ˌbaɪoʊˈkemɪstri/"` at 80–90% consistency — include stress markers, apply selectively, QC single generations when pronunciation is critical.
- A global tone tag as plain prepended text (no brackets, e.g. "warm cheerfulness") can set a default personality across generations without per-line typing (AAC community trick).
- For **v2 models**, emotion works better as narrative context ("she asked, her voice trembling") than as tags — but the model may speak the guidance aloud, so strip it in post.

**Honest caveats:** tags get spoken aloud or silently ignored depending on voice — treat as an assist, not a guarantee. v3's dramatic style can read as "exaggerated yet monotonous" over long sessions (HN). v3 is for character/expressive work, not the narration default.
- **Official Agent Academy tag list (video-sourced):** Excited, Concerned, Patient, Chuckles, Coughs, French/US accent, Whispering, Sad, Laughing, Angry, Sighs, Disappointed, Enthusiastic, Serious, Singing. Tags can appear in the agent's **First message** itself (e.g. `[sighs] Oh no, I'm so sorry…`).
- **Tag-leak gotcha (official):** define tags through the agent-builder UI, not only in the system prompt — if the agent is later switched to an older model, the older model may **speak the tags literally**.
- **Measured (A/B, 2026-09-18):** v3 tags on a cloned voice measured active, not placebo — identical text ran 13–20% longer on v3 than v2 and loudness range doubled (LRA 4.1–4.8 vs 1.9–2.6 LU). Sparse conventional tags only: `[chuckles]` *before* the punchline, never after.

---

## 4. Script preprocessing — the converged pipeline

Run every script through this before it hits the API (converged across creators + production skill repos):
1. Em-dashes (— –) → commas (multilingual model chokes on them).
2. ALL CAPS → Title Case (caps create unnatural emphasis artifacts).
3. Numbers written out ("twelve", not "12"; "five figure", not "5-figure"). Money/phone patterns → words in code (`$1,234.56` → "one thousand two hundred thirty-four dollars and fifty-six cents").
4. Expand contractions ("do not", "cannot" — contractions get misread as other languages on multilingual models).
5. No mid-sentence ellipsis, semicolons, or colons.
6. One idea per short sentence for natural pacing.
7. **Pauses are placed deliberately:** paragraph breaks and ellipses create pauses; for v3 use `[pause]` tags. Map dramatic pauses to the script text (peroration beats get 1–2s of air before the landing line).

---

## 5. Long-form: chunking recipe + Projects/Studio

**Chunking (the community's most-agreed recipe):**
- Split on **sentence boundaries only**, ≤700 chars/chunk.
- Context-seed each chunk after the first with the previous chunk's last sentence so the model warms up on the established tone (prevents drift); trim the seed out afterward using STT word-timestamps.
- Stitch with a **150ms triangular crossfade** (not silence gaps — those read as audible pauses); trim ~0.1s off the very end (a 0.4s trim was reported to cut the last word).
- QC loop: transcribe back with Scribe, diff against script, 92% similarity gate, auto-retry with stability +0.05 (max 3 retries). Caveat: STT transcribes written-out numbers back as digits — listen before re-burning credits on those false alarms.

**Projects / Studio:** the long-form workflow — text organized into **chapters**, each with its own voice and model assignment, rendered into a full audio project with per-chapter snapshots. Full Studio API exists (create/manage/render projects and chapters programmatically). Best for audiobooks, podcast series, course narration. **Single-shot TTS is better for short clips and real-time.** Limitation: regeneration granularity is chapter/chunk-level — one misread word costs a re-convert of the chunk (generate in 150–300 word chunks). Community note: Studio renders can sound flatter than hand-tuned single-shot pipelines.

**Console Studio timeline (video-sourced, CONSOLE_VIDEOBOOK.md §4):** the console's Studio is a multi-track editor — **voice track on top, music below, then SFX and video** — with trim/split/fade in/out and visible waveforms. Every element can be **AI-generated in place** (no imports needed). Built-in actions: remove background noise (Isolator), AI soundtrack generator, video voiceover, fix-voiceover-mistakes (speech correction), captions, podcast/URL-to-audio generators. **Edit in Studio** imports Image & Video generations straight into a project.

---

## 6. Pronunciation dictionaries — the determinism tool

- PLS/XML upload; usable in Studio, Dubbing Studio, and the Speech Synthesis API; referenced in TTS requests.
- Create paths (verified 2026-10-07): `add-from-rules` (JSON body) / `add-from-file` (multipart). `add-from-xml` does not exist (405).
- No DELETE on dictionaries (405) — archive via `PATCH {"archived": true}`.
- Grapheme→phoneme or grapheme→alias pairs. **Matching is case-sensitive and first-match-wins — order matters.**
- Alias tricks: `URL` → `U R L`, `UN` → `United Nations`.
- **Best usage:** brand names, acronyms, proper nouns that must be right every time. Boring, old-tech, and more dependable than v3 tags for determinism.
- v3 spot-fix alternative: IPA in `/slashes/` inline (see §3).

---

## 7. Streaming & real-time TTS

**Official WebSocket guide** (verified 2026-09-18):
- Endpoint: `wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model_id}`
- Flow: init with `{"text": " "}` (single space) → set `voice_settings` + `generation_config.chunk_length_schedule` in the init message → stream text chunks → `""` (empty string) closes. Responses: base64 audio chunks + `isFinal`.
- **Default chunk schedule:** `[120, 160, 250, 290]` (character thresholds before generation starts). Official best practice: start with defaults; reduce only if latency is inadequate.
- **`flush: true`** forces generation of buffered text — recommended at the end of each conversational turn; closing the socket auto-flushes.
- **Keepalive:** connection closes after 20s inactivity (`inactivity_timeout`, default 20) — send `" "` to keep alive; `""` closes.
- **Pronunciation dictionaries** go in the **init** message (`pronunciation_dictionary_locators`).
- Query params: `enable_ssml_parsing` (default **false** — SSML is opt-in); `optimize_streaming_latency` is **DEPRECATED**; `auto_mode` (full sentences only — partial phrases get "highly reduced quality"); `sync_alignment` (character timing per chunk); `language_code` **only on Turbo/Flash v2.5**; `output_format` default `mp3_44100`.
- **No official guaranteed TTFB** — the guide defines TTFB and points to the `elevenlabs-latency` tool for measurement. Never promise latency as an SLA.

**Measured reality (community benchmarks):**
- Flash v2.5: ~75ms model-only, ~135ms end-to-end same-region; network typically adds 20–200ms; audio players commonly buffer ~500ms before playback.
- Community voice pipeline (Deepgram + GPT-4.1-mini + ElevenLabs): TTS TTFB 0.35–0.46s; first-byte end-to-end 0.7–2.1s.
- **Always stream for real-time** (`convert_as_stream` / WebSocket `streamInput`); non-streaming adds full-file latency.
- Quote end-to-end, never model-only. In agent loops ElevenLabs TTS is ~135ms of a ~1.7s median turn — the LLM first-token and telephony hops are the fat; optimizing TTS below Flash is wasted effort.
- WebSocket hygiene: the JS SDK distinguishes `disconnected` (dropped) from `error` (protocol) — handle both; always `end_session()` to close sockets (leaked sessions are a known pitfall); SDK auto-retries 408/409/429/5xx with exponential backoff (default maxRetries=2 — tune per workload); 429s are real on high-volume endpoints — back off, never hot-loop.

---

## 8. Conversational AI — the agents platform

### Architecture (official)
Managed STT → LLM → TTS → turn-taking pipeline. Four building blocks: fine-tuned ASR (Scribe family); LLM of choice (Gemini, Claude, OpenAI, or BYO server-side custom LLM); low-latency TTS across 5k+ voices and 31 languages; custom **turn-taking model** (ConvAI 2.0) that reads hesitations and filler words in real time. ElevenLabs' own team confirms turn-taking/interruption was the hardest problem they solved.

### Agent configuration
- First message (adjustable pre-greeting delay), system prompt, LLM choice + temperature + token limit, voice + TTS model, primary language, auth criteria, max conversation length. Preset templates exist; blank agents start empty.
- **Per-call overrides:** `conversation_initiation_client_data` injects `dynamic_variables` (prompt context) and `conversation_config_override` (e.g. override `first_message`, `language`, `tts.voice_id` per call) — per-caller personalization without cloning agents.
- **Tools (four types):** client tools (execute on user's device via WebSocket), server tools (your backend webhook — CRM, orders, payments), system tools (`end_call`, `language_detection`, `agent_transfer`, `transfer_to_number`, `skip_turn`, `voicemail_detection`), MCP tools (external MCP server with approval policies).

### Knowledge base / RAG mechanics
- Document types: file (PDF/TXT/DOCX), URL (**with `enable_auto_sync`** for living content), text blocks.
- **Explicit two-step indexing:** upload (`POST /v1/convai/knowledge-base/url` or `/file`), then trigger embedding (`POST /v1/convai/knowledge-base/{doc_id}/rag-index`, model `e5_mistral_7b_instruct` or `multilingual_e5_large`). Async: typically 30–90s/doc, minutes for large docs.
- Attach doc IDs in `conversation_config.agent.prompt.knowledge_base` (`{id, name, type, usage_mode}`); `prompt.rag.enabled` toggles retrieval; configurable `max_chunks`, `vector_distance_threshold`.
- Gotchas (community): **21 MB/file upload max; account cap ~20 MB / 300k chars** (non-enterprise); **URL import fetches one page — it does not crawl**; RAG adds ~500ms latency; chunking/embedding internals unpublished.
- Production pattern: split manuals into focused docs, keep them current, mine transcripts for unanswered questions; keep per-user data in dynamic variables/server tools — **never in the KB**.
- Structured extraction: data-collection fields return in `analysis.data_collection_results` as `{value, rationale}`; per-call RAG usage visible on `GET /v1/convai/conversations/{id}`.

### Token / credit mechanics (playbook-critical)
- **Agents bill per-MINUTE, all-inclusive** — not per token or per character. Official: 13,750 minutes on Business at **$0.08/min**; setup/prompt testing at half cost.
- The **LLM is bundled** — GPT-4o vs GPT-4o-mini doesn't change the ElevenLabs meter. But per community verification, LLM and telephony may bill **on top** of the minute rate on some plans — verify on the live pricing page before budgeting.
- Billing units: **TTS = per character; STT = per minute; agents = per minute** (separate from the shared TTS credit pool).
- Consequence: budget conversations in **minutes, not tokens**; silence and long caller monologues still cost; concurrency caps (Free 4 → Business 40) matter more than monthly minutes — burst overage ~$0.16/min (2×). **Size plans to busy-hour simultaneous calls, not monthly minutes.**

### Latency knobs (in impact order)
1. **LLM first-token is the biggest, most variable slice** (Gemini Flash <350ms vs GPT-4-class/Claude Sonnet 700–1000ms). Dropping to a Flash/Haiku-tier model saves 400–700ms/turn — the single highest-impact lever. (But ElevenLabs' own guidance warns the weakest Flash models misfire tools — test tool reliability per model.)
2. TTS model: Flash v2.5 (agents default) → Turbo → Multilingual v2 → v3 Conversational (most natural, alpha, highest latency).
3. Interruption handling toggle; stability moderate (not maxed); conversational-tuned voice (not a narration voice); small first-message delay; streaming throughout.
4. Real-world medians (independent monitoring, 2026): agent turn **~1.7s median, P95 ~3.2s** — sub-500ms is best-case marketing. <700ms end-to-end is the bar for natural-feeling phone conversation; most platforms exceed it. Telephony adds ~500ms+.

### Telephony / WebRTC / WebSocket
- **WebRTC (browser):** short-lived conversation token (`GET /v1/convai/conversation/token`); official SDKs for React/client/React Native/Swift/Kotlin. Never expose `xi-api-key` in the browser.
- **WebSocket:** `wss://api.elevenlabs.io/v1/convai/conversation?agent_id=...` with signed URLs (`get-signed-url`); events: `user_audio_chunk`, `audio`, `agent_response`, `user_transcript`, `interruption`, `agent_response_correction`, `ping/pong`, `client_tool_call`.
- **Telephony:** native Twilio integration (import numbers in dashboard; outbound via `POST /v1/convai/twilio/outbound-call` or register-call flow returning TwiML); SIP trunking as enterprise alternative; **batch calling** campaigns with per-recipient dynamic variables.
- Security: server mints **signed URLs (~15min expiry)** or conversation tokens; gate minting behind your own auth; unauthenticated agent IDs get mined (community's most-repeated anti-pattern is keys in client code).

### Webhooks
- Settings > Webhooks or per-agent; HTTPS; **HMAC-SHA256** in `ElevenLabs-Signature` (`t=<ts>,v1=<hex>` over `<timestamp>.<raw_body>`); SDK helper `elevenlabs.webhooks.constructEvent`.
- Events: `post_call_transcription` (transcript + metadata/timing/cost + analysis), `post_call_audio` (base64 full-call audio, recording must be enabled), `call_initiation_failure`, `speech_to_text.completed`.

### Production hardening (community)
- Barge-in: VAD false-triggers in noise (HVAC, cross-talk) — **test interruption on real telephony audio**, not a quiet office mic; Patient mode for support/elderly/noisy lines, Eager for transactional flows.
- Echo: agent with open mic hears itself — client-side acoustic echo cancellation is your bug, not the model's.
- Tool calls: strong LLM + crisp descriptions; for costly tools (payments, cancellations): higher-intelligence LLM + tool-call tests + idempotent tools + spoken filler to mask tool latency ("Let me pull that up…").
- Keep **LLM cascading ON** but ensure every model in the chain is fast enough that a fallback doesn't wreck the call.
- Agent prompt recipe: force brevity (1–3 sentences/turn); ban markdown/bullets/emojis/URLs (read aloud literally); spell out numbers; persona + scope + explicit "don't know → say so and offer transfer"; script the edges (first message, interruptions, silence, hostiles). Prefer several small subagents over one giant prompt.
- Compliance is a config item: AI disclosure in first message (EU AI Act Art. 52); TCPA consent + 8am–9pm windows + DNC scrubbing (US); voice = biometric data under GDPR.
- Testing: use the platform's production test suite — scenario/LLM-eval, tool-call tests, simulation with tool mocking, probabilistic repeats (green 100%/amber ≥80%/red), "create test from conversation" regression capture. Single-run "worked once" is not a pass.

### Verified API notes (2026-10-07, live probes)
- **Agent create = `POST /v1/convai/agents/create`** — bare `POST /v1/convai/agents` returns 405.
- **PATCH is a deep merge** — partial updates are safe. Round-trip gotcha: GET state carries both `prompt.tools` and `prompt.tool_ids` → 400 `both_tools_and_tool_ids_provided`; strip `tools`, keep `tool_ids`.
- **Webhook tool registration:** every `request_body_schema` property needs a `description` or the create 422s.
- **DELETE semantics:** agents, tools, KB docs → 204 empty body (parse-tolerant clients only).
- **Session lane is API-drivable:** `GET /v1/convai/conversation/token` and `/get-signed-url` both 200.
- **Telephony:** `GET /v1/convai/phone-numbers` → 200 `[]` on the probed account — no numbers provisioned; outbound-call ambitions need provisioning first.
- **KB upload:** the multipart file part MUST carry a real content type (`application/octet-stream` → 422); `el.py` guesses it from the extension (fixed 2026-10-07). RAG status key is `indexes`, not `rag_indexes`.

### Takeaways for a production conversational agent
1. Cost is forecastable: minutes × $0.08 (Business), testing at half. No separate LLM line item on the ElevenLabs meter.
2. KB refresh is automatable: URL docs with `enable_auto_sync` + scripted upload → rag-index → attach.
3. `conversation_initiation_client_data` gives per-caller dynamic context without cloning agents — the personalization lane.

### Console agent builder (video-sourced, CONSOLE_VIDEOBOOK.md §2/§11)
- **V3 conversational** is selected per-agent in the voice menu; the UI notes stability/speed/similarity are not customizable on v3 models (the model adapts them).
- **Branches** work like git branches with **traffic splitting** (e.g. 50/50) for A/B-testing live calls; merge back to main — **merges conflict when settings differ**, reconcile first.
- Builder tabs: Agent, Workflow, Branches, Knowledge Base, Analysis, Tools, Tests, Widget, Security, Advanced. System-prompt blocks: personality, goal, guardrails, tools, **character normalization** (how spoken forms map to written forms — critical for voice).
- **Speculative turn** (on by default) prefetches responses during silence; related controls: take-turn-after-silence, end-conversation-after-silence, max conversation duration.
- **Detailed costs** calculator: prompt length + KB pages → estimated per-minute LLM cost. Community temperature band: **0.3–0.5**.
- **Evaluation:** define success/failure in plain language; **data collection** harvests named values per call. **RAG: leave off unless the KB is hundreds of pages.**

---

## 9. Dubbing Studio

- End-to-end localization: upload audio/video → dubbed into **29 languages** with the original speaker's voice preserved; auto speaker separation (up to 32 speakers); background-audio mix handling; transcript timing preserved. BCP-47 regional identifiers accepted (`es-ES` vs `es-419`, `pt-BR`).
- **Dubbing API** (public since ~Aug 2026): up to **3 GB** source files (vs 1 GB in app UI); transcript review; segment-level regeneration; model selection; up to 3 concurrent jobs self-serve (10 enterprise).
- **Dubbing v2 is the default** (emotional fidelity, automatic); legacy **v1** remains for cost-sensitive batch work — but the editable legacy Studio is reportedly in maintenance mode, so v2 = quality without granular correction tools. Pick per workload.
- Credit heuristic: ~1 minute of dubbing ≈ 3,000 characters (old figure — verify current).
- Caveats: free-tier dubs are watermarked with no commercial license; pronunciation/accent/cross-language identity need human review. Best for creator/podcast/game localization at scale.

**Console dubbing workflow (video-sourced, CONSOLE_VIDEOBOOK.md §5):** Dubbing → Create new dub → title + source language (or auto-detect) + target language(s) → upload file or social URL → advanced: number of speakers, output resolution, time-range for partial dubs → optional lip-sync adjustments → preview/download MP4. Observed: ~5 min/language for a 90-second video. Mission-critical translations need a **fluent human** review. (The most-watched walkthrough is Dec 2023 — verify the flow live.)

---

## 10. Sound Effects API

- `POST /v1/sound-generation`: `text` (prompt), `duration_seconds` (0.5–22s; model picks if omitted), `prompt_influence` (0–1, default 0.3; higher = more literal), `loop` (seamless loop), `output_format`, model `eleven_text_to_sound_v2`.
- Billing: **100 characters per generation** (auto duration) or **25 chars/second** (set duration). **Measured 2026-09-26:** a 3 s generation with duration set consumed 75 characters, matching the documented rule.
- Best usage: foley, ambiences, UI/game one-shots, stingers. Generate variations and pick takes; 1–4s for one-shots, 3–8s for loops/beds.
- Limitations: max 22s per generation — not music, not speech. **Prohibited Use Policy restricts selling generated SFX as standalone files/sample packs/sound libraries.** Community reviewers rate SFX quality as sub-par/non-immersive — pilot before depending on it.

**Console SFX (video-sourced):** one generation = **200 credits → 4 candidates**; options: duration (auto/explicit), prompt-adherence strength, **loop toggle** (seamless loops). Favorites tab; history retained. **Soundboard** mode for live/DJ pads with an edit mode for custom prompts.

---

## 11. Music (Eleven Music)

- Prompt-driven music generation (any genre, vocals or instrumental); trained on **licensed** production music (Merlin + Kobalt deals).
- **Public API, paid plans only:** `POST /v1/music` (compose), `/v1/music/detailed` (audio + composition plan + metadata), composition-plan endpoint (plan without generation cost), `video_to_music`, upload, inpainting, stem separation. Set `model_id` explicitly (`music_v1` API default; `music_v2` UI default during transition). `music_length_ms` 3,000–600,000 (~10 min max per prompt; overview pages also cite 5 min — flagged inconsistency, verify live).
- Pricing: documented **$0.15/minute** (third-party, July 2026 — verify). **Measured 2026-09-26:** a 30 s `music_v2` generation moved the account's character counter by ≈157 characters (derived residual) — ≈314 chars/min. Treat as an estimate until a dedicated measurement; the no-cost `composition-plan` endpoint does not exist on this API surface (404 on both `/v1/music/composition-plan` and `/v1/music/composition_plan`) — estimates fall back to documented rates.
- **Commercial rights (self-serve):** broad online/offline commercial use **except film, TV, radio, and studio games**; full broadcast rights are Enterprise. Hard restrictions: no commercial music libraries; no arms/tobacco/pharma/adult/religious/political use; no artist/songwriter names, song/album titles, lyric excerpts, or label names in prompts.
- Best usage: background/cue music, ad spots, game loops, instrumental beds. Reproducibility via seed is approximate.

**Console music (video-sourced):** Compose shows **~1,350 credits/min** (≈1,300–1,350 for 30s), ~20–30s generation time. Lyrics mode: **Auto / Instrumental only / Custom lyrics** — explicitly select instrumental if no vocals wanted. The Explore tab's preset tracks are usable as-is at zero generation cost.

---

## 12. Voices: Design, Cloning, Changer

**Voice Design** — brand-new voice from a text description. Two-step API: `POST /v1/text-to-voice/design` → previews (each with `generated_voice_id` + audio); listen, pick, then `POST /v1/text-to-voice` to create. Models: `eleven_ttv_v3`, `eleven_multilingual_ttv_v2`. Best for invented characters/NPCs/prototypes without booth time. Inherently nondeterministic — you choose from previews.

**Voice cloning hygiene:**
- Record all samples in the same room, same mic, consistent tone/energy — the AI clones the noise too. Longer continuous samples beat chopped ones.
- **The sample's tone must match the target use** — a clone built from excited podcast audio reading solemn copy was unusable until re-recorded (Platformer test).
- Instant Voice Clone works from ~1 min; Professional Voice Clone ≈ 3 hours of clean audio, tiered quality.

**Voice Changer / Speech-to-Speech** — transform a recording into another voice while **preserving the original performance** (emotion, timing, delivery); also the engine behind Dubbing v2.
- `POST /v1/speech-to-speech/{voice_id}` (multipart; `voice_settings` must be a **JSON-encoded string**); streaming variant available; `remove_background_noise` runs audio isolation first; `file_format: pcm_s16le_16` for lower latency.
- Model must have `can_do_voice_conversion: true` (check `GET /v1/models`).
- Best usage: re-voicing ADR, translating a performance while keeping acting nuance, voice anonymization, consistent character voices from scratch recordings. **When a performance exists (pause, laugh, hesitation), conversion preserves delivery better than any text prompt can direct it** — underrated.
- Limitation: output bounded by input quality; batch conversion API, not a real-time voice-changer product.

**Console gotchas (video-sourced):**
- **Voice Design regeneration has no history** — discarded candidates are unrecoverable. Favorite/save a winner before regenerating. Demo generation costs **350 credits**; specify accent/age/gender at minimum.
- Saved custom voices consume library slots; default voices do not.
- **Voice Isolator:** the Send button shows the credit cost before committing (~500 credits/30s).
- **House note:** for hard comic timing or prophetic cadence, the strongest route is human-performs-reference → Voice Changer transfer into the canonical voice — the transfer preserves timing better than tags can invent it.

---

## 13. API best practices

**Officially verified reliability mechanics:**
- **SDK retries (official):** exponential backoff, default max **2 retries**, on 408/409/429/5xx; default SDK timeout 60s (`maxRetries`/`timeoutInSeconds` tunable).
- **Rate limits are concurrency-based, not RPM** (official Help Center): exceeding concurrent requests → HTTP 429 with `"too_many_concurrent_requests"`. 429 body shape: `{"detail": {"status": "rate_limit_exceeded" | "quota_exceeded" | "concurrent_limit_exceeded", "message": "..."}}`. Never hot-loop on 429 — failed requests count against limits.
- **Two 429 variants (observed 2026-10-07):** `too_many_concurrent_requests` → queue the request (do not backoff); `system_busy` → backoff. Blanket backoff on every 429 is half-wrong. No rate-limit response headers observed.
- **No native idempotency key** in official docs — house rule, implemented in `el.py`: content-hash cache (sha256 of method+path+body) under the scratch dir; demonstrated 2026-09-26 (re-request returned byte-identical MP3 in 0.26 s, zero API call). Never retry blind on 5xx without it.
- **Usage endpoints (official changelog):** `GET /v1/user/subscription` (balance/limits, reset times — read this on the live account instead of quoting any plan numbers); `GET /v1/usage/character-stats` (time-series metrics; `start_unix`/`end_unix` are unix **milliseconds**); `GET /v1/history` (per-generation audit trail).
- **Webhooks:** three families — Agents post-call (`ElevenLabs-Signature` HMAC, verify with `elevenlabs.webhooks.constructEvent`), STT async webhooks, workspace webhook CRUD (`POST/GET/PATCH /v1/workspace/webhooks`, `auth_type: hmac`, persist the returned secret immediately). Don't conflate the families.
- **Keys:** never in client code — server mints signed URLs / conversation tokens behind your own auth.
- **Cost:** corrections cost full-block credits; credits are deducted even when generation fails; credits reset monthly, no rollover.
- **Freshness:** re-verify model IDs, prices, plan limits against `elevenlabs.io/docs/llms.txt` before building or quoting. Never state a price from training data or infer one from a plan label.

- **Retries:** SDK auto-retries 408/409/429/5xx with exponential backoff (default maxRetries=2 in elevenlabs-js — tune per workload). Implement exponential backoff yourself on other stacks; never hot-loop on 429 (failed requests count against limits).
- **Keys:** never in client code. Server mints signed URLs / conversation tokens behind your own auth.
- **Webhooks:** HMAC-SHA256 verification (`ElevenLabs-Signature`); use SDK `constructEvent` helper.
- **Idempotency & cost:** corrections cost full-block credits — batch script QA before generating; credits are deducted even when a generation fails or glitches; credits reset monthly, no rollover.
- **Freshness:** re-verify model IDs, prices, plan limits against `elevenlabs.io/docs/llms.txt` before building or quoting.

---

## 14. Billing, quotas, cost discipline

**Public plan ladder (mid-2026, verify live):** Free $0/10k credits · Starter $6/30k · Creator $22/121k · Pro $99/600k · Scale $299/1.8M · Business $990/6M.
**Agent minutes (verified 2026-07-10, volatile):** Free 15 min/4 concurrent · Starter 75/6 · Creator 275/10 · Pro 1,238/20 · Scale 3,738/30 · Business 12,375/40. Overage $0.08/min standard, $0.16/min burst.
**Cost units:** TTS Multilingual $100/1M chars; Flash/Turbo $50/1M; Music $0.15/min; agents $0.08/min (Business). Comparables: Google WaveNet $4/1M, Azure Neural $16/1M — a 25× spread top-to-bottom; always compute in $/1M chars.

**Cost-discipline rules:**
1. Draft on Flash (0.5 credits/char), final renders on Multilingual.
2. Cache repeated phrases; monitor usage — conversational agents flip the bill from char-based to minute-based, which teams consistently underestimate.
3. One misread word costs the whole block's characters again — batch script QA before generating.
4. Regeneration habits are the silent budget killer (one reviewer's 3 min of audio + 1 agent burned 6,088/10,000 free credits, mostly trial-and-error).
5. Credits never roll over; failed generations still deduct.

---

## 15. Impact Program nonprofit lane

**What is officially established (2026-09-18):**
- The Impact Program is an **accessibility initiative for individuals with permanent voice loss**, run through nonprofit partners (~7,000 individuals, 800+ nonprofit partners across 49 countries as of March 2026). Eligible users receive a free license (official tutorial: five-year renewable Pro through nonprofit partners; March 2026 PR: "free license for life"). Nonprofits partner via elevenlabs.io/impact-program.
- A general **501(c)(3) discount/credit lane with a named credit allowance is NOT verifiable in official material** — coupon-site claims to that effect are unverified. Exact credit allowances, included/excluded products, API scope, and renewal terms are not in public official docs.

**Working rules:**
- The official public description (voice-loss accessibility) does not on its face describe a general nonprofit credit lane — any membership terms live in-account. **Do not assume coverage of agents' per-minute billing or Music until verified in your own account.**
- Prefer covered usage and watch consumption; read live headroom from `GET /v1/user/subscription` on the account rather than quoting any public price or quota; never infer a paid plan price from a plan label.

---

## 16. House TTS recipe — stage audio (worked example)

> **Ear-checked 2026-09-18:** the v3 expressive lane won the A/B — the comic direction (chuckle before the punchline, deadpan line) and the emotional peroration both kept the narrator's voice identity.

**Primary narrator — all stage beats:**
- Model `eleven_v3`, your cloned narrator voice, `stability: 0.55`, `similarity_boost: 0.75`, style **0.0** (clone rule — never > 0 on clones), no speaker boost (unsupported on v3).
- **v3 hard limit: 500 chars/request** — chunk beats at paragraph boundaries (≤450 raw chars to leave tag headroom), render each, `atempo=0.9` per chunk, concatenate. Production pattern: load verbatim text from a beats file, apply markup programmatically, and run a verbatim-integrity check before any API call.
- **Markup conventions (sparse, conventional tags only):** `[warmly]` on warm opens; `[pause]` before punchlines and section turns; `[chuckles]` *before* the laugh line, never after (never laugh at your own punchline); `[deadpan]` on the ketchup line; `[solemnly]` on the witness sentence with the longest hold in the speech; `[warmly]` on the hands passage; `[softly]` on the final question, standing alone, no fade trick. Punctuation does half the work: `...` = real hesitation, em-dash = mid-sentence catch, paragraph break = longest natural pause.
- **Pause map:** keep a written pause map per beat (scored pauses; the same sensibility extended across beats).
- Post: `atempo=0.9`, mono 44.1 kHz, MP3 96 kbps. Keep output filenames stable across re-renders so downstream pages don't change; preserve baselines before any migration.

**Fallback (documented, not current):** `eleven_multilingual_v2`, stability 0.80–0.85, style 0.15, speaker boost on, `...`/em-dash/paragraph-break markup. Pauses yes, directed emotion no; zero voice-identity risk, single-request renders.

**Second voice (unchanged):** `eleven_multilingual_v2`, stability 0.75 / similarity 0.85, speaker boost on, `atempo=0.9`. A voice moves to v3 only on a separate decision.

**Rules that never change:** script preprocessing per §4 before every render; style 0.0 on every clone; never quote a plan price from a plan label; watch consumption against the live account numbers.

---

## 17. Hype vs reality scorecard

**Marketed hard, underdelivers:**
1. **v3 expressiveness** — demo reels are dramatic; production reports cite sing-song delivery, artifacts, credit-burning regen loops. Right model for character work, not the narration default.
2. **Audio tags as a control surface** — tags get spoken aloud or ignored depending on voice; alpha-flaky. An assist, not a guarantee.
3. **v3 "symbol intelligence"** — phone-number digit-group reading fixed "in 72% of cases" per vendor claim — i.e., nearly a third still wrong. Pre-normalize numbers anyway.
4. **Sub-500ms agent turns** — best-case for ElevenLabs-controlled stages; median real turn ~1.7s, P95 ~3.2s.
5. **Sound effects quality** — reviewers call them sub-par; pilot before depending on them.
6. **"Director's Mode"** — announced as the coming fix for fine-grained control; treat as roadmap, not capability.

**Underrated, punches above its weight:**
1. **Instant Voice Cloning** — one minute of well-recorded, tone-matched audio beats the state of the art of a few years prior.
2. **Flash v2.5 as the agent default** — ~50% cheaper, ~135ms end-to-end, the agents skill's explicit recommendation.
3. **Scribe/STT in the QC loop** — cheapest automated QC in the ecosystem (with the numbers-transcribe-back-as-digits caveat).
4. **Pronunciation dictionaries + alias tricks** — the only reliable determinism tool for brand names/acronyms.
5. **Voice Changer (STS)** — when a performance exists, conversion preserves delivery better than any text prompt.
6. **`llms.txt` docs index** — point agents at `elevenlabs.io/docs/llms.txt` for current-API codegen.

---

## 18. Console creative products (video-sourced)

> From `CONSOLE_VIDEOBOOK.md` (video-learned 2026-09-18; full video+timestamp citations there). Currency warning: the console changes fast — verify menu names live before treating any step as production procedure.

### Image & Video generation
- **Image & Video** (BETA at capture): prompt → asset type (image/video) + model. Frame-verified model list (Nov 2025): OpenAI Sora 2 Pro, Sora 2, Google Veo 3.1, Veo 3.1 Fast. Video params vary by model (start/end frames, resolution, duration, audio, negative prompt).
- Image workflow: 1–4 generations, reference images, Upscale/4x on cards. Official tip: **upscale the image before** turning it into video.
- Video detail panel: **Use in lip sync**, **Upscale video**, **Recreate**, **Edit in Studio** (imports into a Studio project — video + voiceover + music + SFX + lip-sync on one timeline).
- Explore feed: generations may be shared publicly (toggleable).

### Scribe v2 + Productions
- **Scribe v2** STT — also the QC-loop transcriber (§5/§17). **Productions:** commission human-edited dubbing/subtitles/voiceovers/transcripts — the finishing layer for client deliverables.

### Templates
- One-click creative workflows: UGC videos (product photo → talking creator), explainer videos, graphic recordings (topic → 30s narrated animation), compare-voices (one script across voices). **Fastest path from a script to a finished short.**

---

## Appendix A — key sources

- Official docs source repo (docs.elevenlabs.io published source): https://github.com/elevenlabs/elevenlabs-docs
- Official skills repo (agents + music API references): https://github.com/elevenlabs/skills
- Official docs mirrors: https://github.com/braydoncoyer/elevenlabs-docs · https://github.com/letsgititbby/elevenlabs-docs
- Docs freshness index: https://elevenlabs.io/docs/llms.txt
- Community production skills: https://github.com/calesthio/generative-media-skills · https://github.com/dreydrey9000/claude-skills (clone-production recipe) · https://github.com/hiteshshimpi-55/kahani-studio (best-practices)
- Latency benchmark: https://github.com/cloudx-labs/posts (voice-pipelines-latency) · https://www.marktechpost.com/2026/08/30/lowest-latency-inference-apis-for-voice-and-realtime-agents-a-time-to-first-token-ttft-first-benchmark/
- Cost spread analysis: https://forasoft.medium.com/your-text-to-speech-bill-has-a-25-spread-hiding-in-it-44ecc6f279fb
- Platformer voice-clone test: https://www.platformer.news/platformer-voice-clone-elevenlabs/
- Voice-changer evaluation protocol: https://queststudio.io/blog/elevenlabs-voice-changer-performance-guide
- v3 tag piloting: https://www.theaivideocreator.ai/p/eleven-v3 · https://spokenaac.com/blog/elevenlabs-audio-tags-in-aac/
- Video-learned console operations (8 tutorials, 2026-09-18): `CONSOLE_VIDEOBOOK.md` (this skill) — console-only behaviors (Studio timeline, Image & Video, agent-builder branches/cost calculator, credit-cost displays, voice-design gotchas); folded into this playbook per its merge note.

## Appendix B — remaining open items

- **Live-verification gaps** (need a working docs.elevenlabs.io read or read-only API introspection — `GET /v1/models`, `GET /v1/user/subscription`): exact per-model language names; v3's WebSocket input-streaming status; v3 per-request char limit (official card says 10,000, one community source says 3,000 — the API enforced 500 on TTS text for a cloned voice 2026-09-18); numeric voice-setting ranges/defaults in the API reference; official SSML support page; current Help Center rate limits + pricing page; official webhook event catalog; Impact Program entitlement terms (likely in-account only); console menu names from the videobook fold-in (the console changes fast).
- Never encode as fact: `[chuckle]`/`[pause]`/`[shout]` as official tags; numeric voice-setting defaults beyond the WS example; plan prices/quotas; a native idempotency key; any Impact Program credit allowance beyond your own measured usage.

---

*Playbook compiled 2026-09-18; §16 carries the v3 house recipe and the CONSOLE_VIDEOBOOK.md material is folded in. Next refresh: any dated price/plan/limit quoted in a build, or a console UI change that breaks a videobook workflow.*
