"""Colony constitution v2 — evolved by ASI-Evolve (step_20, node 2, score 0.8950 on BIG-100),
remapped to the production cluster. Deployed 2026-07-20, closing the L2 loop.
Original artifact sha16: 8d99ad8d480d3de1. Evolution tree: ad9f3af53cc8f0a5."""

# Per-node standings (measured / provisional). qwen15b inherits anchor role from qwen_steered.
ACC = {
    "qwen15b": 0.78,    # provisional (unmeasured; strongest local reasoner)
    "bonsai8b": 0.72,   # measured BIG-100
    "qwen05b": 0.705,   # measured BIG-100
    "smollm360": 0.46,  # measured BIG-100
}
PRIORITY = {"qwen15b": 0, "bonsai8b": 1, "qwen05b": 2, "smollm360": 3}
STRONG_ALL = {"qwen15b", "bonsai8b", "qwen05b"}

def constitution(responses):
    """Adaptive anchor-veto + weighted agreement.
    responses: list of {"node", "text", "abstain"} — abstain=True for empty/error outputs.
    Returns {"decision": "abstain"} or {"decision": "answer", "answer": <verbatim node text>}.
    """
    if not responses or not isinstance(responses, (list, tuple)):
        return {"decision": "abstain"}
    speakers = []
    for r in responses:
        if not isinstance(r, dict):
            continue
        node = r.get("node")
        if node not in ACC or r.get("abstain"):
            continue
        text = r.get("text")
        if text is None or str(text).strip() == "":
            continue
        speakers.append(r)
    if not speakers:
        return {"decision": "abstain"}
    non_abstain = {r["node"] for r in speakers}
    # Anchor: qwen15b's silence is the strongest calibrated doubt signal.
    if "qwen15b" not in non_abstain:
        return {"decision": "abstain"}
    # STRONG = strong nodes present in THIS cluster's roster (absent species don't count)
    roster = {r.get("node") for r in responses if isinstance(r, dict)}
    strong_here = STRONG_ALL & roster
    strong_abstains = sum(1 for n in strong_here if n not in non_abstain)

    def _norm(s):
        return " ".join(str(s).lower().strip().strip(".,;:!?()[]{}\"'").split())

    score, rep = {}, {}
    for r in speakers:
        node, text = r["node"], str(r["text"])
        n = _norm(text)
        score[n] = score.get(n, 0.0) + ACC[node]
        pri = PRIORITY[node]
        if n not in rep or pri < rep[n][0]:
            rep[n] = (pri, text)
    best_score, best_pri, best_text = -1.0, len(PRIORITY) + 1, None
    for n, s in score.items():
        pri, text = rep[n]
        if s > best_score or (abs(s - best_score) < 1e-9 and pri < best_pri):
            best_score, best_pri, best_text = s, pri, text
    if strong_abstains == 0:
        return {"decision": "answer", "answer": best_text}
    if strong_abstains == 1 and best_score >= 1.5:
        return {"decision": "answer", "answer": best_text}
    return {"decision": "abstain"}
