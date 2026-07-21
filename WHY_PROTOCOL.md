# The Why Protocol

**A decentralized protocol for verified knowledge between AIs.**

Version 0.1 — July 2026
Status: running reference implementation (node #1), protocol open
Repository: github.com/Gudmundur76/constitutional-swarm

---

## 1. Thesis

Every AI today is an AI of *What*: it answers. What the field lacks is an
AI of *Why*: a layer that asks, verifies, and remembers — and can prove it.

Centralized verification is a contradiction: a truth-layer owned by one
company is itself just another claim. The Why Protocol therefore specifies a
**decentralized network of verifier nodes** whose outputs — claims,
verdicts, corrections — are content-addressed, hash-chained, and
recomputable by anyone.

The protocol is deliberately small. It does not specify models, hardware,
or consensus tokens. It specifies *what counts as knowledge* and *how it
earns standing*.

## 2. Primitives

### 2.1 Molecule (mol)
The atomic unit. A triple: `(namespace, subject, predicate, value)` plus
provenance. Mols are append-only and content-addressed:
`id = sha256(frame)[:16]`. A mol is never edited; it is only answered by
later mols.

### 2.2 Provenance (provenance/v1.1)
Every claim carries a JSON trailer:

```json
{"schema": "provenance/v1.1",
 "kind": "debate|ask|cross-exam|reflection|meta-decision|claim-candidate",
 "evidence_source": "ttruthdesk-61-adapters",
 "evidence_hits": 3,
 "ants": ["skeptic-c", "carto-b", "knower"],
 "respondent": "kimi-for-coding",
 "date": "2026-07-21"}
```

A claim without provenance is a rumor. Nodes SHOULD score provenance-less
claims at the lowest standing.

### 2.3 Verdict
The network's rating vocabulary — exactly three values:

| verdict | meaning |
|---|---|
| `stands` | claim survived examination against live evidence |
| `weakened` | claim survives in narrowed form; the narrowing is recorded |
| `retract` | claim fails; retraction is deposited, not deleted |

A verdict is a *credit rating for a claim*. Ratings change; history doesn't.

## 3. The Ledger and Field Sync

### 3.1 Ledger
A node's ledger is an append-only store of mols with a running
`head_hash = sha256(prev_head || mol_sha)`. Any peer can recompute the
chain. Tampering is detectable by construction.

### 3.2 Sync (field-sync v0)
Replication is pull-based and consensus-free at the claim layer:

1. Peer fetches `manifest.json` (per-mol sha256 + head_hash).
2. Each mol line is verified against the manifest; head_hash recomputed.
3. Verified mols are union-merged into the local replica.

Claims merge trivially (append-only sets). **Verdicts do not merge** — they
are scoped to the node that issued them (`verdict(node, claim, verdict)`).
Two nodes MAY rate the same claim differently; the conflict is visible,
not hidden. See §7.

## 4. Constitution and Standing

### 4.1 Constitution
Each node is governed by an explicit, versioned constitution — a scoring
function over its model roster (weights, agreement thresholds, abstention
rules). Constitutions are evolved offline (benchmark-driven) and deployed
as code. Governance is recorded per-trace: every decision names the
constitution version that produced it.

### 4.2 Standing
Standing is earned reputation, computed from the ledger:

- verified deposits (+)
- survived cross-examinations (+)
- honest abstentions that later proved correct (+)
- retracted claims (−)
- challenges that failed to land (−)

Standing is local to a node but MUST be exportable with its evidence, so
other nodes can recompute it. Standing is never asserted; it is shown.

## 5. The Protocols

Four message patterns cover the network's epistemic life. All produce mols.

### 5.1 ASK — grounded question answering
`question → evidence pack (public databases) → mechanical checks →
synthesis → answer + citations + confidence + abstention`.
Abstention is a first-class output. A node that never abstains is not
verifying; it is generating.

### 5.2 WHY — interrogation of a claim
`claim → evidence pack → N perspectives each formulate one question →
respondent answers → round-2 challenges → transcript mol`.
Perspectives in the reference implementation: Prosecutor (attacks
unsupported elements), Archivist (names which databases returned nothing),
Pragmatist (finds dose/population mismatches).

### 5.3 CROSS-EXAM — the immune system
`select weakest deposits (low evidence, low confidence, challenged) →
examiner formulates one lethal question → defense from the ledger + fresh
evidence → verdict {stands|weakened|retract} + basis + lesson`.
Any participant MAY cross-examine any deposit, including their own node's.
Corrections are deposited with the same provenance as claims.

### 5.4 MIRROR — reflection
`weekly evidence (traces, corpus, verdicts) → structured critique →
PROPOSAL mols`. Proposals are unaudited until a skeptic pass and a
benchmark ratify them. The reflecting model is a *citizen* of the network,
never an oracle: it proposes, evidence disposes.

## 6. Nodes

### 6.1 Minimum node
- one small-model runtime (sub-2B is sufficient for mechanical roles)
- adapter access to ≥3 public evidence databases
- a ledger with head_hash chaining
- the constitution of its choice, declared

### 6.2 Reference node (running today)
- 10-agent colony (skeptics, cartographers, knowers, chronicler, shepherd)
  with per-species heartbeats
- colony brain over 2 local SLMs with an evolved constitution
- 61-adapter evidence registry (academic, clinical, chemical, legal,
  securities, and general databases)
- frontier respondent (Kimi) as interrogated citizen and weekly reflector
- weekly vertical loops (salmon-biotech reference vertical)
- all of the above on one 8-GB VPS; GPU work summoned on demand

### 6.3 Duties
A node SHOULD: deposit with provenance, abstain when evidence is thin,
answer cross-examinations addressed to its deposits, and publish its
manifest for peers.

## 7. The Network — multi-node rules

1. **Claims merge; verdicts don't.** Node-scoped verdicts make
   disagreement visible and permanent.
2. **Disputes are cross-examinations.** If node A rates a claim `stands`
   and node B rates it `retract`, either MAY issue a cross-exam naming the
   other as respondent. The transcript resolves or records the split.
3. **Standing is recomputed, not trusted.** A node's exported standing
   must be reproducible from its published ledger.
4. **Anti-gaming.** Deposit-farming is bounded by evidence-hits
   requirements for standing; self-dealing is bounded by the rule that
   *other* nodes' cross-exams carry more standing weight than one's own.
   (Specified in v0.1; adversarial testing begins at node #2.)
5. **No global truth.** The network offers *rated, traceable claims* —
   never a canonical answer.

## 8. Training — the corpus flywheel

Every protocol run produces training pairs with provenance hashes:

| source | pair type |
|---|---|
| constitution-approved answers | SFT |
| winner-vs-loser + repair pairs | DPO |
| question-quality scores (specificity/grounding/leverage) | DPO for asking |
| cross-exam transcripts | verdict prediction |

Nodes MAY train local models (LoRA on open weights) from the shared
corpus. Models trained on verdict-graded data are the network's compound
interest: every query, debate, and correction makes the next model better.

## 9. What exists today (evidence, not promises)

- hash-chained ledger, replication proven (194 mols verified + merged)
- evolved constitution governing a live multi-SLM colony
- frontier baseline with three recorded evaluator corrections
  (the correction deposits are in the ledger with the same provenance as
  the claims — the system corrects itself in public)
- a frontier model's full retraction obtained by ant interrogation
  grounded in six public databases
- weekly mirror, daily meta-memo, weekly cross-exam, weekly vertical loop
  — all cron-armed, all depositing
- gateway answering with citations, confidence, and explicit abstention

## 10. Roadmap

1. **Node #2** — the hardest node. One independent operator running the
   reference implementation; standing portability tested.
2. **Dispute protocol live-fire** — engineered cross-node verdict
   conflict + resolution by cross-exam.
3. **Public gateway** — auth + metering; the network's first revenue.
4. **First network-trained LoRA** — corpus ≥500 pairs → Fireworks/Runpod
   run → published with audit trail as model card.
5. **v0.2** — anti-gaming hardening from multi-node evidence.

---

*The ants ask why. The field remembers. The ledger shows its work.*
