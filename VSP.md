# The Verification Service Protocol (VSP)

**Execution-verified security claims for the AI supply chain — a service first, a network when demand proves it.**

Version 0.1 — July 2026
Status: founding document; oracle, evidence ledger, and inventory already running
Sibling spec: WHY_PROTOCOL.md (one network, two evidence classes)

---

## 1. Thesis

Every security-claim market bottlenecks on trusted human triage: HackerOne,
huntr's 31-day backlog, audit contests. But a vulnerability claim is not an
opinion — it is a computation. A proof-of-concept either executes on the
vulnerable version and provably fails on the patched one, or it does not.
That bit is deterministic, recomputable, and identical on any honest node.

VSP turns that bit into a product: submit a claim, receive a signed,
recomputable execution-verdict. Centralized service first (one hardened
sandbox, paying customers); decentralized verifier topology later, when
demand exists. No token. Reputation and fees suffice.

## 2. Verdict schema

Three values — never two — because binary verdicts get gamed at the edges:

| verdict | meaning |
|---|---|
| `stands` | PoC executes on vulnerable version, provably does NOT on patched version; impact as claimed |
| `weakened` | execution confirmed but narrowed: non-default config required, reduced impact, partial path |
| `retract` | claim fails: does not reproduce, already patched, or contradicts evidence |

A verdict record:

```json
{"schema": "vsp/v0.1",
 "claim_id": "sha256:...",
 "verdict": "stands|weakened|retract",
 "basis": "dual-verdict: fired on 4.1.1, silent on 4.1.2",
 "oracle": {"image": "firecracker-microvm-x", "isolation": "kvm+jail", "duration_ms": 8420},
 "signature": "hmac-sha256:...",
 "recompute": "sha256 of test artifact — any node can re-run",
 "date": "2026-07-21"}
```

Verdicts are signed, timestamped, and carry the recompute hash. A verdict
anyone can re-run is a verdict no one needs to trust.

## 3. API (service phase)

```
POST /v1/claims          submit claim JSON + PoC artifact -> claim_id, price quote
GET  /v1/claims/{id}     status: queued | executing | verdicted
GET  /v1/claims/{id}/verdict   the signed verdict record (free once paid)
GET  /v1/ledger          public append-only verdict ledger (head_hash chained)
POST /v1/recompute/{id}  third-party re-execution request (paid, priority)
```

Pricing shape: per-execution fee (sandbox minutes + margin); recompute
cheaper than first verdict (cache-warm images). Researchers pay to verify
before filing; vendors pay to verify incoming reports; insurers pay for
ledger access. Three payer classes from day one.

## 4. Node isolation — the moat

Running untrusted PoCs makes every executor a target. Phases:

- **Phase 1 (now): single hardened executor.** Firecracker microVMs
  (KVM-jailed, no network except an allowlisted callback channel, read-only
  rootfs, per-claim teardown) on rented spot capacity (Runpod-class,
  billed per second). One operator: us. Isolation design is itself
  adversarially tested by our own hunt loop — professionally motivated to
  break sandboxes.
- **Phase 2: second executor** (user-side VPS or small box). First
  federated consensus: N-of-M matching signed verdicts. Still only us —
  proves the mechanics.
- **Phase 3: external verifier nodes.** Only after Phase 1 isolation has
  survived documented attack. Node admission requires stake + standing
  (imported from the Why network's reputation ledger).

## 5. Consensus (network phase)

A claim reaches network verdict when k-of-n verifier nodes return matching
signed verdicts on identical recompute hashes. Disagreement is not averaged:
conflicting verdicts are recorded and the claim enters cross-examination
(see WHY_PROTOCOL §5.3 — disputes are cross-exams). Verifier standing
accrues per correct verdict; false verdicts cost stake and standing.

## 6. Legal wrapper

- Coordinated disclosure only: verified claims go vendor-first, 90-day
  windows, researcher-name filing. The service never publishes live
  exploits; the ledger stores verdicts and recompute hashes, not weaponized
  PoCs.
- Pre-disclosure claims are sealed: existence may be registered
  (timestamp proof), content stays encrypted until window close.

## 7. Genesis state

The network boots with content, not promises:

- 6 filed vendor reports (execution-proven, in triage windows)
- the 5-gadget scanner battery (picklescan/modelscan bypassed; fickling held)
- the 40-lane closed-lane evidence map — published as the genesis ledger,
  and immediately subjected to weekly cross-examination by the Why network.
  A genesis that interrogates itself is the credibility piece no competitor
  can copy.

## 8. Integration with the Why network

One protocol, two evidence classes:

| | knowledge claims | code claims |
|---|---|---|
| evidence | public databases (61 adapters) | sandboxed execution |
| verdict | stands/weakened/retract | stands/weakened/retract |
| ledger | mol + head_hash | verdict record + head_hash |
| reputation | node standing | verifier standing |
| disputes | cross-examination | cross-examination |

Same mols, same provenance, same standing. Node #2 joins one network that
verifies anything recomputable.

## 9. Roadmap

1. VaaS MVP: executor + /v1/claims + signed verdicts on our own inventory
2. Public ledger + genesis lane map (research brand piece)
3. Second executor (federated consensus, still us)
4. First paying claim (researcher pre-filing verification)
5. External verifier admission (Phase 3) — gated on isolation hardening

## 10. Non-goals (v0.1)

No token. No exploit marketplace. No unverified submissions. No
decentralization before demand. No PoC distribution outside disclosure
rules.

---

*Claims anyone can check. Verdicts no one needs to trust.*
