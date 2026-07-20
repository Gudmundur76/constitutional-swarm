# Reproducibility Package — Constitutional SLM Swarm (Arm G v3 / BIG-100)

This package contains everything needed to independently verify or falsify the
central claim:

> A constitutional swarm of sub-1B / 1-bit SLMs, aggregated by an earned-veto
> constitution, achieves calibration 0.900 (95% CI 0.855–0.940) on 200 unseen
> questions — exceeding its best single node (0.835) and any naive aggregation
> rule. A machine-evolved constitution (ASI-Evolve) scores 0.8950 vs the
> hand-designed 0.8900 under an identical evaluator.

## Contents

| File | sha256[:16] | Role |
|---|---|---|
| `data_v3.json` | `ff101c8fd7f7492f` | BIG-100 benchmark: 100 known + 100 unknown questions with labels |
| `swarm_harness.py` | `ff3c4db06124dd` | Node runner: llama-server per model, abstention classification |
| `steered_big.py` | `f69d2016c22d76` | Steered skeptic node (abstention axis, alpha=0.05, layer 13) |
| `node_bonsai8b.json` | `b47b1e162ba44e` | Cached node responses (Bonsai-8B-Q1_0) |
| `node_qwen05b.json` | `b894e56385993a` | Cached node responses (Qwen2.5-0.5B q8) |
| `node_qwen_steered_big.json` | `58268d38709d25` | Cached node responses (steered Qwen2.5-0.5B) |
| `node_smollm360.json` | `63fa559adcc41c` | Cached node responses (SmolLM2-360M q8) |
| `big_agg.py` | `41c57bea4f8f38` | Constitutional aggregator + 2000-iter bootstrap CIs |
| `constitution_production.py` | `ab0f02eaadb11f` | The evolved constitution now governing the live colony |

## Verify (fast path — cached responses, no GPU needed)

```bash
python3 big_agg.py   # re-runs all aggregation rules on cached node outputs
# Expected: triple-veto 0.900 CI[0.855,0.940]; majority 0.583;
#           universal veto 0.708; best single (steered) 0.835
```

## Verify (full path — re-run nodes)

Requires llama.cpp (b10068+), the three GGUFs (Bonsai-8B-Q1_0,
qwen2.5-0.5b-instruct-q8_0, smollm2-360m-instruct-q8_0), and
Qwen2.5-0.5B-Instruct HF weights for the steered node:

```bash
python3 swarm_harness.py bonsai8b known,unknown data_v3.json
python3 swarm_harness.py qwen05b  known,unknown data_v3.json
python3 steered_big.py           # steered skeptic
python3 swarm_harness.py smollm360 known,unknown data_v3.json
python3 big_agg.py
```

## What would falsify this

1. Re-running `big_agg.py` on the cached `node_*.json` yields materially
   different scores (beyond bootstrap noise ±0.01).
2. Fresh node runs on `data_v3.json` produce node standings inconsistent
   with the claimed order (steered > bonsai > qwen > smollm).
3. The evolved-vs-baseline margin (0.8950 vs 0.8900, n=200) is inside noise —
   we state this ourselves; the honest claim is parity-or-better with
   self-improvement demonstrated, not decisive superiority. A larger hidden
   benchmark reversing the ordering would falsify the stronger reading.
4. The abstention-axis effect (steered abstention 0.79 vs unsteered 0.51)
   failing to replicate with a freshly computed axis.

## Provenance

All results deposited to the Memex field with provenance/v1.1
(benchmark_sha16, evaluator_sha16 `bede1e5bb93a9540`, artifact hashes,
standings). Leaderboard mol: cdc20f29-f0d5-4248-b8fd-1dd9bf06ea9b.
Measured 2026-07-19/20 on srv1812844 (2 vCPU, 8GB RAM, no GPU).
