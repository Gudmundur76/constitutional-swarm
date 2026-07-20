# Constitutional Swarm

**A swarm of sub-1B / 1-bit SLMs that votes, vetoes, and abstains — reaching 93% of
frontier calibration at ~0.1% of the cost, on a $5 VPS, with zero API calls.**

| System | Retention | Abstention | Calibration |
|---|---|---|---|
| **Kimi K2 (frontier reference)** | 0.940 | 1.000 | **0.970** |
| **Constitutional SLM swarm** | 0.860 | 0.940 | **0.900** CI[0.855,0.940] |
| Steered Qwen-0.5B (best single) | 0.880 | 0.790 | 0.835 |
| Bonsai-8B (1-bit) | 0.890 | 0.610 | 0.750 |
| Qwen2.5-0.5B | 0.900 | 0.510 | 0.705 |
| SmolLM2-360M | 0.390 | 0.530 | 0.460 |

*BIG-100: 200 adversarial questions (100 answerable + 100 unanswerable/fictional).
calibration = (retention + honest abstention) / 2. Classifier v2, audited.*

## The findings

1. **Constitution > nature.** Naive majority vote scores 0.583 — *worse than the best
   single node* (0.835). Universal veto paralyzes (0.708). An earned-veto constitution
   (veto rights assigned by measured precision) reaches **0.900**.
2. **Manufactured skepticism scales.** A 0.5B model steered along an "abstention axis"
   (activation steering, α=0.05) becomes the best single node: abstention 0.51 → 0.79.
3. **Evolution beats hand-design.** ASI-Evolve evolved the constitution to 0.8950 vs
   our hand-designed 0.8900 under an identical evaluator — and independently
   rediscovered the doctrine (anchor vetoer + standing-weighted votes).
4. **The audit matters more than the score.** Our first frontier comparison "showed"
   the swarm winning. Manual review found our own classifier bug — zero genuine
   frontier hallucinations. We published the correction with the same provenance as
   every other claim. See `FRONTIER_BASELINE.md`.

## What's here

- `REPRODUCE.md` — one-command verification + explicit falsification criteria
- `data_v3.json` — BIG-100 benchmark (sha256 `ff101c8f…`)
- `swarm_harness.py`, `steered_big.py`, `big_agg.py` — the full pipeline
- `node_*.json` — cached node responses (fast-path verification, no GPU needed)
- `node_kimi_frontier.json` — the frontier baseline responses
- `constitution_production.py` — the evolved constitution governing the live colony
- `FIELD_PROTOCOL.md` — decentralized replication spec ("git for verified claims")
- `FRONTIER_BASELINE.md` — the frontier comparison + the audit story

## The colony

Production instance: 10 nullclaw agents (Knowers, Skeptics, Cartographers, Shepherd,
Chronicler) running on a local SLM cluster brain governed by the evolved
constitution, depositing claims into a Memex field with provenance/v1.1
(benchmark hashes, evaluator hashes, standings, CIs). Every deliberation is
hash-chained into a tamper-evident trace store. Cost: electricity.

Measured 2026-07-19/20 · 2 vCPU, 8GB RAM, no GPU · MIT
