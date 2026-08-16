import json
from unittest.mock import patch

from noesis.bal003_adapter import BAL003Adapter, F0_QCAL_HZ


PAYLOAD = {
    "node_id": "BAL003",
    "timestamp_utc": "2026-08-16T00:54:39Z",
    "measured_frequency_hz": 141.7001,
    "uncertainty_hz": 0.00005,
    "coherence_psi": 0.999999,
    "hardware_signature": "0x4a8f...b210",
}


def test_measurement_preserves_measured_value_and_hashes_raw_payload():
    raw = json.dumps(PAYLOAD, separators=(",", ":")).encode()
    adapter = BAL003Adapter(bearer_token="test-token")
    with patch.object(adapter, "fetch_raw", return_value=raw):
        measurement = adapter.fetch()

    assert measurement.measured_frequency_hz == 141.7001
    assert measurement.delta_hz == 0.0
    assert measurement.uncertainty_hz == 0.00005
    assert measurement.raw_sha256
    assert measurement.evidence_record()["classification"] == "supports_reference"
    assert F0_QCAL_HZ == 141.7001


def test_drift_is_not_normalized_to_reference():
    payload = dict(PAYLOAD, measured_frequency_hz=141.7002)
    raw = json.dumps(payload, separators=(",", ":")).encode()
    adapter = BAL003Adapter(bearer_token="test-token")
    with patch.object(adapter, "fetch_raw", return_value=raw):
        measurement = adapter.fetch()

    assert measurement.measured_frequency_hz == 141.7002
    assert measurement.delta_hz == 0.0001
    assert measurement.evidence_record()["classification"] == "reproducible_drift"
