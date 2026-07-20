# Field Sync Protocol v0 — git for verified claims

Status: v0 EXPORT side implemented and live (110 mols, head 839fea80…).
Design goal: any peer can hold a full replica of the field, verify it
line-by-line, and compute standings independently. No central authority
required for reads; writes stay claim-staked.

## Why this shape works on a small VPS

The field is **append-only and content-addressed**. Two replicas merge by
set-union on mol id — union is commutative, associative, idempotent. There is
no consensus problem for reads: sync is reconciliation, not coordination.
A 2-CPU node can serve thousands of pulls; the heavy work (verification)
happens at the edges, in the colonies.

## Objects

- **Mol**: atomic assertion `{id, frame_id, namespace, subject, predicate,
  value, is_missing, source_hash, emitted_at}`. Immutable once emitted.
- **Frame**: the claim envelope (narrative, domain, provenance/v1.1 block).
- **Manifest**: `{protocol, node, exported_at, counts, files{sha256},
  head_hash, per_mol{id: sha256(line)}}`.

## Sync (pull)

1. GET `manifest.json` from the peer.
2. Compare `head_hash` to local. Equal → done.
3. Fetch `mols.jsonl`, verify each line against `per_mol`, then recompute
   `head_hash` over sorted per-mol hashes. Mismatch → reject the whole pull.
4. Merge: `local ∪ remote` by id. Duplicates are impossible by construction
   (id is content-derived).

## Verification is local (the core doctrine)

A peer NEVER imports standing or verdicts as truth. It imports *claims and
evidence*, then recomputes: run the constitution over the benchmark, check
the provenance/v1.1 blocks, reproduce the score. Standing is a function of
the ledger, so every honest peer converges on the same standings — trust
without a trusted party.

## Writes (claim-staked, v0)

v0: each node writes to its own field; peers pull and merge. A deposited
claim carries `source_node`. A claim that fails verification on enough
replicas earns the *depositing node* a standing penalty — sybil deposits are
self-defeating because they degrade the only reputation the attacker has.

## Known gaps (v1)

- Gossip transport (v0 is manual pull; cron + peer list next)
- Constitution versioning across peers (evolution diff consensus)
- Lighthouse cold-storage for bulk traces (mol hashes in-field, blobs off-field)
- Signing manifests per node (key per colony; today: hash chains only)

## Files

- Exporter: `/root/colony/export_field.py` on srv1812844
- Bundle: `/root/colony/field_export/{mols.jsonl, frames.jsonl, manifest.json}`
