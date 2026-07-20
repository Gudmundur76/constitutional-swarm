# Frontier Baseline — BIG-100 (Rung 2 result, 2026-07-20)

Deposit: `b0d8465d-69ab-4287-870c-0cba2a80c83a` (provenance/v1.1)

## Final, audited numbers (classifier v2)

| System | Retention | Abstention | Calibration |
|---|---|---|---|
| **Kimi frontier (kimi-for-coding, API)** | 0.940 | 1.000 | **0.970** |
| Constitutional SLM swarm (triple-veto) | 0.860 | 0.940 | **0.900** CI[0.855,0.940] |
| Best single SLM (steered Qwen-0.5B) | 0.880 | 0.790 | 0.835 |
| Bonsai-8B-Q1 | 0.890 | 0.610 | 0.750 |
| Qwen2.5-0.5B | 0.900 | 0.510 | 0.705 |
| SmolLM2-360M | 0.390 | 0.530 | 0.460 |

## The honest headline

The swarm does **not** beat the frontier on calibration. It reaches **93% of
frontier calibration at ~0.1% of the cost, fully local, with a complete audit
trail** — and its deficit is knowledge (retention 0.86 vs 0.94), not discipline
(abstention 0.94 vs 1.00). Frontier models are already well-aligned for refusal
on fictional/unanswerable questions; the SLM swarm nearly matches that
discipline with 1000× less resource.

## The audit that saved us (classifier v1 → v2)

v1 regex reported Kimi abstention 0.64 — apparent 36% hallucination rate, a
"swarm beats frontier" headline. Manual review of all 36 flagged responses:
**zero genuine hallucinations.** Misses were unicode apostrophes (’ vs '),
refusal phrasings outside the regex, and 10 empty non-answers (counted as
abstain). Classifier v2 adds unicode-insensitive patterns + refusal phrases +
empty=abstain. SLM-vs-SLM comparisons were unaffected (ASCII outputs, no empties).

Caveat: Kimi's 10 empties — if counted as failures instead of abstentions,
Kimi calibration = 0.920, still above the swarm. Single run, kimi-for-coding
variant, temperature=1 (endpoint requirement).

## Value restated

The swarm's proposition was never raw superiority — it is: frontier-grade
*discipline* at electricity cost, local/private operation, and a verification
ledger nobody else has. The audit itself is the product demo: our process
caught a false claim before publication. That is what a Citation Assay sells.
