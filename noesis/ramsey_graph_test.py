from noesis.ramsey_resonance_adapter import pairwise_resonance_graph


def test_resonance_edge_and_provenance():
    graph = pairwise_resonance_graph([0.0, 0.0005, 1.0])
    assert len(graph["nodes"]) == 3
    assert len(graph["edges"]) == 3
    first = graph["edges"][0]
    assert first["resonant"] is True
    assert first["delta_hz"] == 0.0005
    assert graph["provenance"]["repository"] == "motanova84/Ramsey"
    assert graph["provenance"]["commit"] == "b31a863fe1249db9b24cec97c098fd9bf34abbb9"


def test_circular_distance():
    # Frequencies near opposite ends of the [0, f0) interval are close on the
    # circle, matching the Ramsey modulo-f0 construction.
    f0 = 141.7001
    graph = pairwise_resonance_graph([0.0002, f0 - 0.0002])
    edge = graph["edges"][0]
    assert edge["delta_hz"] == 0.0004
    assert edge["resonant"] is True
