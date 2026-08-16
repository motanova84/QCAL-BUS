from noesis.critical_bottleneck import build_directive, rank_bottlenecks


def graph():
    return {
        "schema": "NOESIS-EVIDENCE-GRAPH/1.0",
        "commit": "abc123",
        "nodes": [
            {"node_id": "n:root", "kind": "proof_obligation", "label": "sorry_root", "repository": "r", "path": "A.lean", "line": 10, "status": "UNRESOLVED"},
            {"node_id": "n:a", "kind": "theorem", "label": "lemma_a", "repository": "r", "path": "A.lean", "line": 20, "status": "FORMALIZED"},
            {"node_id": "n:b", "kind": "theorem", "label": "lemma_b", "repository": "r", "path": "A.lean", "line": 30, "status": "FORMALIZED"},
            {"node_id": "n:c", "kind": "claim", "label": "claim_c", "repository": "r", "path": "claims.json", "line": 1, "status": "SUPPORTED"},
            {"node_id": "n:isolated", "kind": "proof_obligation", "label": "sorry_isolated", "repository": "r", "path": "B.lean", "line": 5, "status": "UNRESOLVED"},
        ],
        "edges": [
            {"source": "n:a", "target": "n:root", "kind": "depends_on"},
            {"source": "n:b", "target": "n:a", "kind": "depends_on"},
            {"source": "n:c", "target": "n:b", "kind": "depends_on"},
        ],
    }


def test_transitive_unlock_is_ranked_above_isolated_obligation():
    ranked = rank_bottlenecks(graph())
    assert ranked[0].node_id == "n:root"
    assert ranked[0].reachable_dependents == 3
    assert ranked[0].score > ranked[-1].score


def test_policy_never_promotes_epistemic_state():
    directive = build_directive(graph())
    assert directive["next_action"]["action"] == "INVESTIGATE"
    assert directive["next_action"]["verification_required"] is True
    assert directive["next_action"]["promotion_allowed"] is False
    assert directive["selection_policy"]["frequency_or_coherence_used"] is False


def test_ties_are_deterministic():
    g = graph()
    g["nodes"][-1]["node_id"] = "n:aaa"
    ranked = rank_bottlenecks(g)
    assert [x.node_id for x in ranked] == sorted(x.node_id for x in ranked)
