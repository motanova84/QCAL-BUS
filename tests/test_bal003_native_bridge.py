import json
from noesis.bal003_adapter import BAL003Adapter


def test_reactor_observation_preserves_measured_value_and_hash(monkeypatch):
    adapter = BAL003Adapter(host="127.0.0.1")
    raw = json.dumps({
        "success": True,
        "reactor": {
            "frecuencia": 141.7002,
            "coherencia": 0.9999,
            "estado": "online",
        },
    }).encode()

    def fake_get(port, path):
        return (
            f"http://127.0.0.1:{port}{path}",
            raw,
            {"sha256": __import__("hashlib").sha256(raw).hexdigest(), "payload": json.loads(raw)},
        )

    monkeypatch.setattr(adapter, "_get", fake_get)
    observation = adapter.reactor()

    assert observation.measured_frequency_hz == 141.7002
    assert observation.delta_hz == 0.0001
    assert observation.raw_sha256 == __import__("hashlib").sha256(raw).hexdigest()
    assert observation.evidence_record()["classification"] == "reproducible_drift"
