---
name: ontology-floor
description: "Ground words in math (term → formula + checkable proof) to cut hallucination on hard, rare formalisms: a resolve() lookup, deterministic structural + faithfulness ingestion gates, a self-updating ingest worker, and a Cloudflare R2/D1/Vectorize store layer. Use when a system must compute specialized terms instead of recalling them — and must refuse value/ethical terms rather than ground them."
license: MIT
compatibility: "The offline resolve() path needs only Python 3 stdlib; the store/ingest layer needs a Cloudflare account (Workers AI, R2, D1, Vectorize) via CLOUDFLARE_API_TOKEN / CLOUDFLARE_ACCOUNT_ID."
metadata:
  version: 1.0.0
---
# Ontology Floor (full loop)

Grounds a term in its **math + checkable proof** so a model computes instead of recalling. Epistemic floor of a composed stack (floor grounds; an output-verification ceiling layer verifies).

## Proven (honest, measured — Workers AI Llama, python-computed truths)
- **Hard/rare formalisms, 8B: +18pp hallucination reduction** (64%→82%, N=84, McNemar **p=0.002**); +19pp at N=31.
- Mixed workload +14pp (p=0.001). Easy classics: a wash. **Value is regime-dependent** — helps on specialized recall, not common knowledge.
- Trigger study: **always-ground rare-domain wins**; don't build a trigger; residual item-specific backfire belongs at the output-verification/ceiling layer.

## Components
- **resolve.py** — `resolve(terms)` grounds physical/formal terms (math+proof), REFUSES ethical/value terms (routed up, never computed). `augment_prompt()` folds math into a prompt. Stdlib, zero creds offline.
- **ingest_gate.py** — GATE S (deterministic structural: tier/DAG + non-LLM corroboration) + GATE F (faithfulness: Workers AI Llama back-translation + BGE embedding cosine + contrastive + symbol-grounding). Fail-closed. `promote(rec, corpus)` runs both.
- **ingest_worker.py** — the self-updating INGEST loop: SOURCE (arXiv + reference) → EXTRACT (Llama → draft record) → `promote()` → PROMOTE(write) / QUARANTINE(reason) → append-only audit → watermark. `INGEST_DRY=1` = dry run (no writes); `INGEST_DRY=0` = live persist. `INGEST_CAP` bounds candidates/run.
- **cf_stores.py** — the write layer. Idempotently provisions and writes to owned Cloudflare: **R2** `ontology-floor` (record JSON), **D1** `ontology` (index row resolve() reads), **Vectorize** `ontology-floor-canon` (768-d BGE embedding). `--writetest` writes one record + reads it back.
- **seed_corpus.json** + **JSON schemas** in `scripts/` (grounding_record · claim_envelope · coherence_verdict).
- **Eval harness** (reproducible): gen_hard_tasks.py, eval_scale.py, eval_select.py, rarity_gate.py, eval_proof.py.

## Run it
- Offline: `python3 scripts/resolve.py` grounds terms from the local seed corpus — no credentials needed.
- Live model calls need Workers AI on your own Cloudflare account. Set the env
  (below) and run the worker directly:
  `INGEST_DRY=0 INGEST_CAP=12 python3 scripts/ingest_worker.py`
  (`INGEST_DRY=1` = dry run, no writes). Schedule it with your own scheduler
  (cron, a task runner) if you want daily ingest.
- Env: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY. Models: `@cf/meta/llama-3.1-8b-instruct-fp8`, `@cf/baai/bge-base-en-v1.5`. **Zero recurring cost** at Workers AI free/paid tier rates for this volume.

## Honest limits
- **Watermark is currently local per-run** — a fresh scheduled thread re-scans recent sources (writes are idempotent: D1 ON CONFLICT, R2 same-key overwrite, so safe but mildly wasteful). Move the watermark to R2 to dedup across days.
- **arXiv abstracts are low-yield** (rarely contain a clean formula) — feed formula-reference/full-text sources for faster coverage.
- **Gates are high-precision / low-recall** (verification-strict thresholds; legit formulas like gini/CAGR can quarantine at ~0.55). Safe default; add a dedicated ingestion threshold + broader symbol set for more throughput.
- Fail-closed everywhere: a record reaches the cache only on S∧F PASS; ethical terms never grounded; relay untrusted, verify on read.



## Update — watermark moved to R2 (cross-day dedup)
The ingest watermark moved from a local file to R2 (`state/watermark.json`, via `cf_stores.load_watermark`/`save_watermark`). LIVE runs now dedup across days and fresh scheduled threads; DRY runs still use the local file. Door-tested: a repeat LIVE run deduped 9 already-seen sources, processed 0, in ~1.3s (vs ~12s for the first run) — the compute win is real. `ingest_worker.py` also reports a `deduped(already-seen)` count.## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
