# DocJev — independent Jev benchmark reference (2026-09-20)

Source: https://github.com/jerryjliu/docjev (Jerry Liu, LlamaIndex co-founder).
Apache 2.0. Evaluated hands-on 2026-09-20: cloned, installed in a venv,
`docjev doctor --smoke` passed keyless, local LiteParse OCR parsed a real
10-page BEA PDF (10 pages, exit 0), and their benchmark claims were checked
against their recorded `benchmarks/results/*/metrics.csv` — all verified
byte-for-byte (see below).

## What it is
Document classification (one doc → one category) and splitting (one packet →
ordered category/page ranges, optional per-document PDF export) over Jev,
with local LiteParse OCR (default, no API fee) and optional LlamaParse cloud
OCR tiers. Independent of LlamaIndex's hosted Classify/Split APIs. Thin,
well-engineered Python (~5.5k lines incl. tests): official `typesafe-sdk`,
Choice + Noul questions, preflight that validates request construction without
a key, per-call request records with input tokens and cost at $0.042/MTok,
no provider bodies in logs.

## Measured results (their 40-doc / 8-packet benchmark, reproduced from CSV)
- Classify: Jev **40/40** correct, p50 **138.6 ms**; GPT-5.6 Luna 40/40, p50
  794.3 ms → Jev **5.73×** faster.
- Split: Jev **7/8** exact packets, p50 **209.6 ms**; Luna 8/8, p50 1352.3 ms
  → Jev **6.45×** faster. Jev's one miss: an extra boundary before a Federal
  Reserve statement's implementation attachment (frozen rules treat it as part
  of the original publication).
- Both found all 32 true boundaries, including adjacent same-category
  boundaries; all 116 packet pages labeled correctly.
- Cost: **$0.011663** Jev vs **$0.046894** Luna for the measured decisions
  (~4× cheaper).
- Honest caveats stated in-repo: Jev's probabilities are NOT claimed to be
  calibrated; small convenience sample; no inferential confidence intervals.
  Trust the honesty more than the headline numbers.

## Live lane confirmed 2026-09-20
One Jev call via this skill against DocJev's own real rules on the BEA
release page-1 text: model `jev-1.13.0`, answer `press_release` (their
ground truth), p=0.98, confidence 0.97, 953 input tokens ≈ $0.00004.

## What to reuse from them
- Methodology: frozen dataset + shared OCR + preflight-without-key + honest
  caveats. Any local judge head-to-head should copy this discipline.
- Their per-call request-record pattern (elapsed_ms, input_tokens, cost_usd
  estimated vs unknown) is the right shape for our eval receipts.
- Engine code is Apache 2.0 — reusable if we ever need document split logic.

## Verdict: REFERENCE, not adopt
DocJev is a document-pipeline product; we have no standing document-pipeline
need, and this skill already covers Jev decision calls. Its value to us is
independent evidence (methodology + measured latency/cost/accuracy) for
Jev-as-judge, and its harness discipline for our own evals.
