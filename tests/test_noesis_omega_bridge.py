import json
from pathlib import Path


MANIFEST = Path(__file__).parents[1] / "audit" / "noesis_omega_bridge.json"


def test_noesis_omega_bridge_is_read_only():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["mode"] == "read-only-evidence-bridge"
    assert data["mutations"] is False
    assert data["exposure"]["audit_ledger"] == "read-only"
    assert data["exposure"]["dependency_graph"] == "read-only"
    assert data["exposure"]["evidence_status"] == "read-only"


def test_reference_contract():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["reference"]["f0_hz"] == 141.7001
    assert data["reference"]["coherence_threshold"] == 0.999999
