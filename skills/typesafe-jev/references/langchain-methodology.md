# LangChain "Jev-as-a-Judge" methodology — extracted 2026-09-20

Source: "Can Jev Be a Better Agent Evaluator?" (Daniel Shea, Seán Roche),
https://www.langchain.com/blog/jev-agent-evals-langsmith, announced
https://x.com/LangChain/status/2101454284927959080 (7:31 PM Sep 19, 2026).
Methodology below is extracted from the article text; numbers are theirs.

## Experimental design
- **Target:** a weather agent built with Deep Agents (their open-source harness).
- **Fixed set:** 5 weather requests; the agent's full output for each was
  captured and stored as a *fixed example* in a LangSmith dataset. Every judge
  evaluated the same 5 fixed runs — agent behavior, retrieved data, and trace
  context were frozen, so judges were compared on identical inputs.
- **Two signals per judgment:** `quality` (continuous score) and `does_pass`
  (binary pass/fail decision).
- **Oracle:** a human reviewer labeled each fixed response against the same
  rubric. Correctness (vs oracle) was measured separately from repeatability.
- **Repetition:** each judge evaluated each fixed case **100 times** →
  5 × 100 = **500 decisions per judge**. Comparators: GPT-5.6 Luna, GPT-5.6
  Terra, Claude Sonnet 4.6 (run through LangSmith Gateway, provider defaults —
  no temperature/top-p/seed/max-tokens set). Jev via `langchain-typesafe==0.0.1a2`
  (Jev service version not recorded in their metadata).

## Metrics
- **Accuracy** = agreement with the human oracle on binary `does_pass`.
  Reported: Jev 500/500 (100%), Terra 99.8%, Luna 96.4%, Claude Sonnet 4.6 80.0%.
- **Precision (repeatability)** = observed variance of the judge's scores
  across the 100 repetitions of identical input. Lower variance = same judgment
  on unchanged behavior. Reported mean per-case variance of quality scores:
  Jev **0.0000149**; Luna 433× higher; Terra 913× higher; Claude 92× higher.
  Their note: low variance ≠ accuracy — a judge can be consistently wrong; but
  when accurate, low variance makes the accuracy dependable in production.
- **Signal value** = (binary oracle agreement) × (binary repeatability), where
  repeatability = probability two independent calls on the same trace return
  the same verdict. Rewards accurate+stable; penalizes consistently wrong.
- **Cost:** Jev **$0.00035/call** observed in the experiment ($0.34 total for
  their 500-call Jev run vs $28.17 for Claude).
- **Latency:** Jev mean **0.44 s** in the experiment (vendor claims 70–500 ms).

## Their caveats (restate with every result)
1. Only **five fixed examples** — a narrow benchmark; carry-over to other
   agents and production workflows is unproven.
2. **Low cost can amplify mistakes** — a consistently wrong evaluator produces
   bad feedback at scale. Cheap ≠ safe.
3. **Human review and judge alignment remain necessary** in the workflow.
4. The variance result is **observational** — they could not attribute it to
   Jev's training objective; it may come from decision-first vs
   token-generation output design.

## How our test folds this in (`jev_repeat_test.py`)
| LangChain element | Our mapping |
|---|---|
| 5 fixed examples × 100 repeats (500 calls) | **20 fixed Judge-A pairs × 25 repeats (500 calls)** — fixed set frozen across repeats; 20 items give verdict-class coverage (10 KEEP / 10 REJECT) |
| Human reviewer oracle | **Completed Judge-A adjudications** (`judge-a-labels.jsonl`, 206 records): original verdict KEEP/REJECT from the pinned Llama-3.3-70B judge. The ONLY oracle — never invented |
| Binary `does_pass` accuracy vs oracle | Jev's selected Choice (KEEP/REJECT) vs original verdict, N=500 |
| Quality-score variance across repeats | Variance of **P(KEEP)** across the 25 repeats per item; mean per-case variance reported in the same units as their 0.0000149 |
| Decision-flip rate | Fraction of items whose 25 repeats disagree (binary instability) |
| Signal value | Oracle agreement × pairwise repeat-agreement per item |
| Latency | Per-call wall time: mean, p50, p95 (theirs: mean 0.44 s) |
| Cost | `usage.input_tokens` × $0.042/1M per call; total (theirs: $0.00035/call) |
| Fixed behavior across repeats | Same state bytes, same question, same model on every repeat — only the service's own sampling varies |

## Question design (one Jev Choice)
Mirrors the original Judge-A instrument (`JUDGE_A_USER`): the state carries
tier, the decoration-risk flag line ("the flag may be wrong — judge the text,
not the flag"), the lesson prompt, and the local judge's reply. The Choice asks
KEEP vs REJECT with the original definitions verbatim. Jev returns the
selection, per-option probabilities, and confidence — so one call yields both
the binary decision (accuracy) and the continuous score P(KEEP) (variance).
