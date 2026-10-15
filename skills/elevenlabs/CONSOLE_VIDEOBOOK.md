# ElevenLabs Console Videobook

**Method:** 8 tutorial videos analyzed (see Catalog). All 8 received
transcript analysis; 4 received transcript + UI-frame analysis
(official image&video tutorial, official Agent Academy V3 video, Jonas Massie
agent-builder, DGI Kaos 2026 walkthrough). Frame captures: 360p section-cuts
at chapter timestamps, viewed 2026-09-18. Where a step is transcript-only, it
is cited to the video + timestamp anyway — that is the source of record.

**Currency warning:** the console changes fast. Timestamps cite the video's
upload date (in the Catalog). Verify menu names against the live console
before treating any step as production procedure.

---

## 1. Text-to-speech console workflow

**Sources:** Stratvert "How to Use ElevenLabs AI (Complete Beginner Tutorial)"
(50,395 views, up 2026-07-21) · Feisworld "Beginner's Guide 2026" (18,970
views, up 2026-02-04) · DGI Kaos "The Only ElevenLabs Tutorial You'll Need
(2026)" (21,186 views, up 2026-01-16)

**Console map (frame-verified, Jan 2026).** Left nav sections:
- **Creative Platform:** Home, Voices
- **Playground:** Text to Speech, Voice Changer, Sound Effects, Voice Isolator,
  Image & Video *(New)*, Templates
- **Products:** Studio *(New)*, Music, Dubbing, Speech to Text, Audio Native,
  Productions, Developers

Home greets by time of day and shows shortcut cards: Instant speech,
Audiobook, Image & Video, ElevenLabs Agents, Music, Dubbed video; "Latest
from the library" voice cards; **Create or clone a voice** panel (Voice
Design / Clone your Voice). *(DGI Kaos 00:01:24; frame-verified)*

**TTS page (frame-verified):** voice selector, script box with hint *"Type
your text with audio tags like [laughs] to turn into expressive speech…"*,
**+ Add speaker** (multi-speaker), right panel with **Settings / History**
tabs, model selector (shown: **Eleven v3 (alpha)** — labeled a research
preview: "most expressive Text to Speech model but requires more prompt
engineering"), **Stability** slider, **Language Override**.
*(DGI Kaos 00:04:05; frame-verified)*

1. Open **Text to Speech** from the left nav. Paste or type the script.
2. Choose a voice. Filter the library by accent, age, style, use case.
   Saved custom voices consume library slots; default voices do not.
   *(DGI Kaos 00:11:30–00:13:30)*
3. Set voice controls: **speed, stability, similarity, style exaggeration**,
   plus expressiveness on models that expose it.
   *(Stratvert 00:03:21; Feisworld 00:03:17)*
   - Higher stability = more predictable; lower stability = more variation and
     emotion. *(Stratvert 00:03:55)*
   - **Change one setting per generation** so the cause of improvement stays
     measurable. *(Feisworld 00:04:16)*
4. On **V3**, use bracketed performance direction in the script:
   `[whispers]`, `[excited]`, `[long pause]`, `[sigh]`. There is no direct
   speed slider in the V3 interface the creator saw — he returns to V2 when he
   needs speed control. *(DGI Kaos 00:04:10, 00:04:25, 00:05:45)*
5. **Enhance** can auto-suggest directions (thoughtful, long/short pause, sigh,
   whisper); manual direction gives more control. *(DGI Kaos 00:08:12)*
6. Write the script as speech: short sentences, commas at breath points,
   isolate an emphasized phrase on its own line. Script construction and
   punctuation can matter more than slider changes.
   *(Feisworld 00:04:31; Stratvert 00:04:41)*
7. Hit **Generate**. **Regenerating replaces the currently displayed take** —
   download a winning take immediately. Previous generations are usually
   recoverable via **History**, but a deep history is hard to search.
   *(DGI Kaos 00:06:08, 00:06:18, 00:06:56)*
8. Generating re-renders everything in the text box: remove already-approved
   lines or work in smaller segments. *(DGI Kaos 00:07:32)*
9. Export: **WAV** for high-quality video work, **MP3** for web/social.
   *(Feisworld 00:04:47)*

---

## 2. V3 expressive mode + audio tags (Conversational AI agents)

**Source:** Official ElevenLabs Agent Academy, "Give Your Agent Emotional
Intelligence – V3 Expressive Mode & Audio Tags" (4,291 views, up 2026-04-10)

1. Create a **blank agent**. *(00:00:38; frame-verified)*
2. Open the **voice menu**, select **V3 conversational**. Expressive mode turns
   on by default. *(00:00:48; frame-verified)*
3. V3 moves speed/stability adaptation from fixed sliders into the model
   itself. The UI notes: **"Voice settings (Stability, Speed, Similarity) are
   not customizable for v3 models."** *(00:01:13; frame-verified)*
4. Use the **suggested audio tags** or add **custom tags** with a description of
   when the agent should use each one. Frame-verified tag list: Excited,
   Concerned, Patient, Chuckles, Coughs, French accent, US accent, Whispering,
   Sad, Laughing, Angry, Sighs, Disappointed, Enthusiastic, Serious, Singing.
   Tags can appear in the **First message** field itself, e.g.
   `[sighs] Oh no, I'm so sorry to hear your flight was cancelled…`
   *(00:01:24; frame-verified)*
5. ElevenLabs recommends defining tags **through the UI**, not only in the
   system prompt. If tags stay in the system prompt and the agent is later
   switched to an older model, the older model may **speak the tags literally**.
   *(00:01:33, 00:01:39)*
6. Agent builder top tabs (frame-verified): **Agent, Workflow, Branches,
   Knowledge Base, Analysis, Tools, Tests, Widget, Security, Advanced**.
   The Agent tab shows the system-prompt editor (# Role & Persona, Tone,
   Style, Speech), a **Set timezone** button, and the **First message** field
   with an **Interruptible** toggle. *(frame-verified)*
7. In **Advanced settings**, **Speculative turn** is enabled by default: "starts
   generating responses during silence … reducing perceived latency." Related
   controls: **Take turn after silence** (seconds before the agent forces a
   turn; -1 = disabled), **End conversation after silence**, **Max
   conversation duration**. *(00:02:10; frame-verified)*
8. Speculative turn uses Scribe V2 real-time prosody + semantic signals to
   anticipate turn completion and prefetch the response. *(00:02:20)*

---

## 3. Image & Video generation

**Source:** Official ElevenLabs, "Generate Image & Video with ElevenLabs (Full
Tutorial)" (231,974 views — the most-watched video in this set, up 2025-11-18)

1. Open **Image & Video** from the home screen. Header shows the product name
   with a **BETA** tag and **Explore / History** tabs. *(00:00:38; frame-verified)*
2. Enter a prompt, choose the **asset type** (image/video) and the **model**,
   then set model-specific parameters. *(00:00:49)*
3. Image workflow: model, aspect ratio, **1–4 generations**, optional
   **reference images**. Generation cards carry **Upscale** and **4x** buttons.
   *(00:01:11; frame-verified)*
4. Video parameters vary by model: some accept **start/end frames** plus
   references; others accept only a **start frame**. The video panel shows
   "Click to upload, or drag and drop a start frame". Frame-verified model
   list (Nov 2025): **OpenAI Sora 2 Pro, OpenAI Sora 2, Google Veo 3.1,
   Google Veo 3.1 Fast**. *(00:02:12; frame-verified)*
5. Official recommendation: **upscale an image before** turning it into video.
   *(00:03:11)*
6. Open a generated image → **Create video**: select model, resolution,
   duration, audio, negative prompt (where supported), number of variations.
   *(00:04:08)*
7. A generated video's detail panel offers **Use in lip sync**, **Upscale
   video**, **Recreate**, and **Edit in Studio**. *(00:05:52, 00:06:12;
   frame-verified)*
8. **Edit in Studio** imports the video into a Studio project. Studio combines
   video, voiceover, music, sound effects, images, lip-sync, and generation
   history on one timeline. *(00:06:22, 00:06:30)*
9. Explore feed note: "Generations may be shared to Explore page for other
   users to download" (toggleable). *(frame-verified)*

---

## 4. Studio timeline projects

**Sources:** "How to Use ElevenLabs: Create Ultra Realistic AI Voices"
(67,903 views, up 2026-03-09) · DGI Kaos walkthrough (00:26:47) · official
image&video tutorial (00:06:30)

1. Go to elevenlabs.io → **Products → Studio → New project**.
2. The first thing you see is the **timeline**: horizontal tracks stacked
   vertically — **voice track on top, music below, then sound effects and
   video**. Drag and drop; waveforms visible; trim, split, fade in/out.
   *(Ultra Realistic 00:01:53–00:02:25)*
3. Every element on the timeline can be **AI-generated in place** — no need to
   import from elsewhere. *(Ultra Realistic 00:02:27)*
4. Use **New blank project** per client/channel to keep work organized; Studio
   is the same TTS/isolator/changer tools in a project-oriented interface.
   *(DGI Kaos 00:26:47–00:27:33)*
5. Built-in project actions include **remove background noise** (Voice
   Isolator) and **AI soundtrack generator** (Music tool). *(DGI Kaos 00:26:57)*
6. **Studio landing (frame-verified):** Audio cards — *New audiobook* (start
   from scratch or import files), *AI Script Generator* (script from a
   prompt), *Create a podcast* (auto-generate from docs or URLs), *URL to
   audio* (voiceover from any webpage). Video cards — *New video voiceover*,
   *Add SFX and music*, *Remove background noise*, *Fix voiceover mistakes*
   (speech correction), *Add captions*, *AI Soundtrack Generator*. Plus
   **Recent Projects** search and **+ New blank project**.
   *(DGI Kaos 00:26:44; frame-verified)*

---

## 5. Dubbing

**Sources:** Stratvert "BEST AI Dubbing | ElevenLabs" (190,053 views, up
2023-12-06 — oldest video in the set; verify current UI) · Ultra Realistic
(00:07:21)

1. Open **Dubbing → Create new dub**. *(Stratvert 00:01:55)*
2. Add a **title**, source language (or **auto-detect**), and target
   language(s). *(00:02:06)*
3. Upload a local file or choose a supported social source. *(00:02:31)*
4. Advanced settings: **number of speakers**, **output resolution**, and a
   **time range** to dub only part of a longer video. *(00:02:47)*
5. Optional **lip-sync adjustments**. Turnaround observed: ~5 minutes per
   language for a 90-second video. *(Ultra Realistic 00:07:44–00:08:11)*
6. **Preview or download** the dubbed MP4. *(Stratvert 00:03:23)*
7. Mission-critical translations require review by a **fluent human**.
   *(Stratvert 00:03:54)*

---

## 6. Voice Changer (speech-to-speech)

**Sources:** DGI Kaos (00:09:28) · Ultra Realistic (00:08:55)

1. **Drag an MP4 or audio file** into Voice Changer — dropzone reads "Click to
   upload, or drag and drop. Audio or video files up to **50MB** each" — or use
   **Record audio**. *(DGI Kaos 00:09:28; frame-verified)*
2. Choose the **target voice** (right panel: Voice, Model — shown: **Eleven
   Multilingual v2** — Stability, Similarity, Style Exaggeration sliders) and
   hit **Generate speech**. The page shows your credit balance and total
   duration. *(00:09:56; frame-verified)*
3. It preserves much of the source performance's **timing and intonation** —
   all original delivery, timing, and emotions are kept; only the voice is
   swapped. *(00:10:07; Ultra Realistic 00:09:01)*
4. Workflow: a human performs the emotional delivery first, then the
   performance is transferred into the desired ElevenLabs voice.
   *(DGI Kaos 00:10:28)*
5. The tutorial recommends **Multilingual V2** for the transfer because the
   source performance already carries the expressive timing. *(00:10:50)*

**House note:** this is the strongest route for hard comic timing or prophetic
cadence — perform the timing as a human reference, then transfer it into the
canonical voice, rather than asking TTS tags to invent timing.

---

## 7. Voice Design, cloning, library

**Sources:** DGI Kaos (00:11:30–00:17:38) · Ultra Realistic (00:03:17) ·
Feisworld (00:05:00)

- **Create/clone options:** Voice Design, Instant Clone, Professional Clone,
  Voice Remixing. *(DGI Kaos 00:13:30)*
- **Instant Clone:** upload ~1 minute of clean audio (just reading a script);
  ~10 minutes later a synthetic voice ~85% similar. Keep samples clean and
  varied in emotional tone.
  *(Ultra Realistic 00:03:20; Feisworld 00:05:30)*
- **Voice Design workflow:** a modal dialog with a **Prompt** textarea, a
  **Best practices** link, preset chips (shown: *Evil Ogre, Little Mouse,
  Southern Woman*), a **Generate voice** button showing the **−350 credit**
  cost, and **Settings**. At minimum specify **accent, age,
  gender/presentation**. *(00:14:50, 00:15:15; frame-verified)*
  - Demo generation cost **350 credits**; controls include **loudness** and
    **guidance scale**. *(00:16:16, 00:16:28)*
  - **GOTCHA: regenerating Voice Design candidates replaces the current set
    with no history** — unlike regular TTS, discarded designs are
    unrecoverable. Save or favorite a winner before regenerating.
    *(00:17:38)*
- **Library slots:** saved custom voices consume slots; default voices do not.
  Deleting a library voice is recoverable; deleting a uniquely designed voice
  may be difficult to reverse. *(00:12:12)*
- Do not use celebrity-voice cloning as a house practice: the creator's
  suggestion is noted for completeness only. Our rule requires authorization
  and no impersonation.

---

## 8. Voice Isolator

**Sources:** DGI Kaos (00:18:56) · Ultra Realistic (00:06:09)

1. Upload audio/video with background noise or music to **Voice Isolator**.
2. The **Send** button shows the credit cost before you commit (~500 credits
   for a 30-second clip). *(DGI Kaos 00:18:56)*
3. It strips everything except the voice; download the isolated speech.
4. Observed quality: a deliberately noisy coffee-shop recording (chatter,
   clanking dishes) came back "crystal clear" — not studio quality, but
   usable for YouTube/podcast. *(Ultra Realistic 00:06:33–00:07:13)*

---

## 9. Sound Effects + Soundboard

**Source:** DGI Kaos (00:20:24, 00:22:55)

1. **Sound Effects:** search existing effects (filter by most downloaded, most
   recent, trending) or **generate from a text description**.
2. Generation options: **duration** (auto or explicit), **prompt-adherence
   strength**, **loop toggle** (loopable SFX blend end-to-beginning).
   *(00:21:02–00:21:30)*
3. One generation costs **200 credits** and yields **4 candidates**; download
   or favorite winners; generation history is retained. *(00:21:46, 00:22:11)*
4. **Favorites** live on a dedicated tab. *(00:22:24)*
5. **Soundboard** (little-used): load SFX pads for live/DJ use; **Edit mode**
   lets you add your own from a prompt. *(00:22:55–00:23:14)*

---

## 10. Music generation

**Sources:** DGI Kaos (00:23:19) · Ultra Realistic (00:04:14)

1. Open the **Music** tab → **Explore** (filter row: **Genre, Mood, Theme,
   Duration, BPM, Vocals**; **Trending** and **Newest** columns show duration
   and BPM per track) or **Compose**. *(DGI Kaos 00:23:27; frame-verified)*
2. Describe the track ("lofi beat with a dramatic feel, heavy percussions").
   The compose box shows variant count, duration, vocals mode, and the price
   — shown: **1,350 credits/min**. Generation takes ~20–30 seconds.
   *(Ultra Realistic 00:04:50; frame-verified)*
3. Lyrics mode: **Auto** (system decides), **Instrumental only**, or **Custom**
   (type exact lyrics). If you don't want lyrics, explicitly select
   instrumental. *(DGI Kaos 00:24:32–00:25:14)*
4. Set **duration** (or auto) and number of **variants** — more variants cost
   more. Observed: ~1,300–1,350 credits for 30 seconds. *(00:24:08–00:24:27)*
5. If you don't want to spend credits, the preset/explore tracks are usable
   as-is. *(00:25:34)*

---

## 11. Conversational AI agent builder

**Source:** Jonas Massie, "How to Build your First Voice Agent in 1 hour!
(n8n + ElevenLabs)" (5,220 views, up 2026-01-12)

### Create + branches
1. **Agents → Create new agent** (or start from a template: personal
   assistant, business agent). Name it, hit **Create agent**. *(00:27:47)*
2. **Branches** work like GitHub branching: the builder header shows the
   branch name, a **Live 100%** traffic indicator, a branch counter (shown:
   0/6), and **Create branch**. Split traffic (e.g. 50/50) to A/B-test
   branches against live calls; **merge** back to main when done.
   Careful: merging conflicts when settings differ.
   *(00:28:21–00:30:36; frame-verified)*

### Agent-platform map (frame-verified)
Left nav: **Home, History, Agents, Knowledge Base, Tools, Integrations,
Voices** · Monitor: Conversations, Tests · Deploy: Phone Numbers, WhatsApp,
Outbound · Settings · Developers. Builder top tabs: **Agent, Workflow,
Branches, Knowledge Base, Analysis, Tools, Tests, Widget, Security,
Advanced**; top-right: Public/Draft state, **Variables**, **Preview**,
**Publish**. *(frame-verified)*

### System prompt
3. Building blocks: **personality, goal, guardrails, tools, character
   normalization**. A "Generate with AI" button exists; the creator advises
   against it — detail is what makes the prompt good. *(00:30:40–00:31:17)*
4. **Guardrails** = what not to do (e.g. never process refunds outside 30
   days). Tool mapping in the prompt = name, when-to-use description, and
   parameters to collect. *(00:33:15, 00:33:42)*
5. **Character normalization is critical for voice**: define how spoken forms
   ("O R D 1 2 3 4 5 6") convert to written forms (order IDs, emails).
   *(00:35:21–00:35:51)*
6. **Native variables** (`{{system_time}}` etc.) are available without external
   calls — agent ID, caller ID, call duration, time/timezone. Set the
   **timezone** (his example: Australia/Sydney) so the agent is accurate about
   "now". *(00:35:53–00:36:43)*
7. Hit **Publish** to save. **First message** (what the agent says when the
   call answers) has an **interruptible** toggle — checked means the caller
   can cut in during the greeting. *(00:36:51–00:37:24)*

### Voice / LLM
8. Providers: **ElevenLabs, Google, OpenAI, Anthropic, custom LLM**. Model
   select (his build: Gemini 2.5 Flash). *(00:37:32–00:37:46)*
9. **Detailed costs** calculator: enter prompt length + KB pages → estimated
   LLM cost per minute (his example: $0.0035/min on Flash; ~10× on a frontier
   model). *(00:37:49–00:38:40)*
10. **Temperature 0.3–0.5** is the recommended band: lower = deterministic and
    strict to the prompt; higher = creative/hallucination-prone.
    *(00:38:44–00:39:01)*

### Tools (three types)
11. The **Tools** page has three add buttons — **Add webhook tool**, **Add
    client tool**, **Add integration tool** — plus search and a type filter;
    tools list with Name / Description / Created by (shown: cal.com booking
    tools, Twilio SMS send, customer-record lookup). **Integration tools**
    (native: Twilio, SMS send, …) — click to configure; each has Tools/About
    panels. *(00:20:09–00:20:51; frame-verified)*
12. **Client tools** — front-end actions on the caller's side (popups, site
    navigation) driven by voice. *(00:20:59–00:21:38)*
13. **Webhook tools** — collect/submit data to an external service mid-call.
    Define: name, description (when the tool should/shouldn't be called),
    method, and parameters whose values come from an **LLM prompt** or a
    **constant**. *(00:21:50–00:24:46)*

### Knowledge base
14. The **Agent Knowledge Base** page has **Configure RAG** and **Add
    document** buttons; documents list with name, size (his: 1.9 kB),
    creator, last-updated. **Configure RAG** enables retrieval: embedding
    model (English or multilingual), character limit, chunk limit, vector
    distance limit. Advice: leave RAG off unless the KB is hundreds of pages.
    *(00:43:10–00:43:54; frame-verified)*

### Evaluation + data collection
15. **Evaluation criteria**: define success ("call successful if refund issued
    correctly") and failure ("no resolution") in plain language.
    *(00:44:02–00:44:39)*
16. **Data collection**: define values to harvest during the call (like tool
    parameters) — visible at end of call. *(00:44:39–00:45:11)*

### Deployment surface (chapters)
- Platform walkthrough 00:02:16 · agent config 00:04:50 · **WhatsApp**
  00:12:22 · **outbound calling** 00:15:13 · tooling 00:20:52 · knowledge base
  00:24:47 · **n8n custom tools** 00:48:40.

---

## 12. Scribe v2 + Productions (human services)

**Source:** Ultra Realistic (00:09:29, 00:10:06)

- **Scribe V2** (speech-to-text): marketed as "the world's most accurate"
  (their claim); converts interviews, gameplay, messy voice notes into
  transcripts. *(00:09:29–00:09:42)*
- **Productions**: commission **human-edited** dubbing, subtitles, voiceovers,
  and transcripts through the platform — aimed at agencies, brands, and
  high-volume creators. You supply raw assets; their team delivers polished
  files. *(00:10:06–00:10:46)*

---

## 13. Templates (GenAI)

**Source:** DGI Kaos (00:26:00)

- **Templates** combine multiple AI models with pre-tuned prompts ("Get
  started with Gen AI"); includes lip-sync video transforms.
- The **Image & Video explore** feed lets you download, **recreate**, or
  **reference** other users' generations. *(00:26:32)*

---

## Appendix A — Pricing tiers (as stated in videos; verify live)

**Source:** Ultra Realistic 00:10:46 (up 2026-03-09) · DGI Kaos 00:00:24

| Tier | Stated terms |
|---|---|
| Free | 10,000 chars/mo TTS, basic music/SFX access, **no commercial use** |
| Starter $5/mo | 30,000 chars, commercial use, full voice library |
| Creator $22/mo | 100,000 chars, voice cloning, priority generation, commercial rights |
| Pro $99/mo | 500,000 chars, instant voice cloning, API access, projects, team collaboration, priority support |
| Enterprise | Custom |

The creator's own math: replacing ~$105/mo of separate tools (Audition,
Epidemic Sound, Descript, another AI voice tool) with the $22 Creator plan.
*(00:11:47–00:12:16)* — his numbers, not ours; verify before budgeting.

## Appendix B — GOTCHAS (video-sourced)

1. **Voice Design regeneration has no history** — discarded candidates are
   gone. Favorite/save before regenerating. *(DGI Kaos 00:17:38)*
2. **TTS regeneration replaces the current take** — download winners
   immediately; History exists but deep history is unsearchable.
   *(DGI Kaos 00:06:08–00:06:56)*
3. **Generate re-renders the whole text box** — strip approved lines or use
   small segments. *(DGI Kaos 00:07:32)*
4. **Audio tags in the system prompt leak to older models** — define tags in
   the UI; if you switch the agent back to an older model it may speak the
   tags aloud. *(Official Agent Academy 00:01:39)*
5. **No speed slider in the V3 TTS UI the creator saw** — keep a V2 path for
   speed adjustments. *(DGI Kaos 00:04:25)*
6. **Voice Isolator's Send button shows the cost first** — check before
   committing (~500 credits/30s). *(DGI Kaos 00:18:56)*
7. **Music credit cost is duration-driven** — shown only at send time; ~1,350
   credits minimum observed for 30s. *(DGI Kaos 00:24:08)*
8. **Branch merges conflict** when settings differ — reconcile before merging
   to main. *(Jonas Massie 00:30:22)*
9. **RAG stays off** unless the knowledge base is hundreds of pages.
   *(Jonas Massie 00:43:40)*
10. **Dubbing older than the current console** — the 190K-view Stratvert
    dubbing tutorial is from Dec 2023; verify the flow live. *(catalog note)*

---

## Appendix C — Video catalog (measured 2026-09-18 via yt-dlp metadata)

Analysis depth: **T** = full transcript, **T+F** = transcript + UI frames.

| # | Title | Channel | Views | Likes | Dur | Uploaded | Depth |
|---|---|---|---|---|---|---|---|
| 1 | Generate Image & Video with ElevenLabs (Full Tutorial) | ElevenLabs (official) | 231,974 | 2,647 | 7:25 | 2025-11-18 | T+F |
| 2 | BEST AI Dubbing \| ElevenLabs | Kevin Stratvert | 190,053 | 3,409 | 5:07 | 2023-12-06 | T |
| 3 | How to Use ElevenLabs: Create Ultra Realistic AI Voices | (sponsored full-platform guide) | 67,903 | 740 | 13:44 | 2026-03-09 | T |
| 4 | How to Use ElevenLabs AI (Complete Beginner Tutorial) | Kevin Stratvert | 50,395 | 754 | 10:57 | 2026-07-21 | T |
| 5 | The Only ElevenLabs Tutorial You'll Need (2026) | DGI Kaos | 21,186 | 496 | 29:55 | 2026-01-16 | T+F |
| 6 | How to Use ElevenLabs \| Beginner's Guide 2026 | Feisworld Media | 18,970 | 312 | 9:49 | 2026-02-04 | T |
| 7 | How to Build your First Voice Agent in 1 hour! (n8n + ElevenLabs) | Jonas Massie | 5,220 | 133 | 1:15:53 | 2026-01-12 | T+F |
| 8 | Give Your Agent Emotional Intelligence – V3 Expressive Mode & Audio Tags | ElevenLabs Agent Academy (official) | 4,291 | 97 | 4:16 | 2026-04-10 | T+F |

Popularity here is **measured** (view/like counts pulled 2026-09-18), not
search-rank impression. Note the official image&video tutorial dominates;
the most-used dubbing walkthrough is also the stalest (Dec 2023).

### Official channel: lives / streams (cataloged 2026-09-18)
The official channel's streams tab currently lists only:
- "Create faster with Flows Agent" (~1,100 views)
- "Turn Your Workflows into Templates" (~1,000 views)
No large live/tutorial series was found on the streams tab at catalog time.
The official **Agents playlist**
(`http://www.youtube.com/playlist?list=PL0p_X3zznhlNfieOUQnxLMrrRersZBqB-`)
covers: first conversational agent, Twilio telephony, website widget, React
SDK, server webhook tools, signed URLs/allowlists, client tools, MCP tools,
evaluation & success metrics, data extraction, post-call workflows, Shopify,
SIP trunking, scenario/tool simulation testing, V3 expressive mode & audio
tags.

### Official channel: recommended follow-ups (not yet analyzed)
Recent official uploads most relevant to console learning, pulled from the
channel's video tab 2026-09-18:
- "How to Make Your First AI Short Film (Full Tutorial)" — 24,000 views
- "This AI Agent Builds Viral Documentary Videos For You" — 16,000 views
- "Introducing the ElevenLabs MCP, now available in Claude" — 20,000 views
- "Introducing voice, music, image, and video generation in the ElevenLabs console" — 4,200 views
- "ElevenAgents: Configure, Deploy, and Improve AI agents at scale" — 3,400 views
- "Introducing Composer, a section-by-section song editor" — 5,000 views

### Third-party: popularity notes
Third-party ranking above is by measured views. The two Kevin Stratvert
videos and the DGI Kaos 2026 walkthrough are the highest-traction independent
console tutorials found; Feisworld's beginner guide is the most settings-
focused of the beginner set.
