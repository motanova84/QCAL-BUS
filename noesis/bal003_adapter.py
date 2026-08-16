"""Native BAL-003 bridge for the NOESIS evidence graph.

This adapter consumes the already documented BAL-003 public interfaces:

* PayGate / QCAL-SYMBIO-BRIDGE: http://195.201.219.237:8844/reactor
* Ecosystem proxy:              http://195.201.219.237:8844/ecosistema
* Monitor health:               http://195.201.219.237:5050/health
* Monitor status:               http://195.201.219.237:5050/status
* Monitor ecosystem:            http://195.201.219.237:5050/ecosystem

No credential is required by the documented read-only endpoints. The adapter
never manufactures a measurement: it records the raw response hash and only
extracts fields actually returned by BAL-003.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

F0_QCAL_HZ = 141.7001
DEFAULT_HOST = "195.201.219.237"
DEFAULT_PAYGATE_PORT = 8844
DEFAULT_MONITOR_PORT = 5050


class BAL003Error(RuntimeError):
    """Base error for BAL-003 acquisition failures."""


class BAL003ProtocolError(BAL003Error):
    """Raised when a BAL-003 response is not valid for the selected endpoint."""


@dataclass(frozen=True)
class BAL003Observation:
    source: str
    endpoint: str
    timestamp_utc: str | None
    measured_frequency_hz: float | None
    coherence_psi: float | None
    raw_sha256: str
    payload: dict[str, Any]

    @property
    def delta_hz(self) -> float | None:
        if self.measured_frequency_hz is None:
            return None
        return self.measured_frequency_hz - F0_QCAL_HZ

    def evidence_record(self) -> dict[str, Any]:
        record = asdict(self)
        record.update(
            {
                "reference_frequency_hz": F0_QCAL_HZ,
                "delta_hz": self.delta_hz,
                "classification": (
                    "supports_reference"
                    if self.delta_hz == 0.0
                    else "reproducible_drift"
                    if self.delta_hz is not None
                    else "no_frequency_observed"
                ),
            }
        )
        return record


class BAL003Adapter:
    """Read-only client for the documented BAL-003 bridge and monitor."""

    def __init__(
        self,
        host: str | None = None,
        timeout_s: float | None = None,
        verify_tls: bool = True,
    ) -> None:
        self.host = host or os.getenv("BAL003_HOST", DEFAULT_HOST)
        self.timeout_s = float(timeout_s or os.getenv("BAL003_TIMEOUT_S", "10"))
        self.verify_tls = verify_tls

    def _get(self, port: int, path: str) -> tuple[str, bytes, dict[str, Any]]:
        url = f"http://{self.host}:{port}{path}"
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "NOESIS-BAL003/2.0"})
        try:
            with urlopen(request, timeout=self.timeout_s) as response:
                raw = response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            raise BAL003Error(f"BAL003 acquisition failed at {url}: {exc}") from exc

        digest = hashlib.sha256(raw).hexdigest()
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BAL003ProtocolError(f"BAL003 endpoint {url} did not return UTF-8 JSON") from exc
        if not isinstance(payload, dict):
            raise BAL003ProtocolError(f"BAL003 endpoint {url} must return a JSON object")
        return url, raw, {"sha256": digest, "payload": payload}

    @staticmethod
    def _reactor_frequency(payload: dict[str, Any]) -> tuple[float | None, float | None, str | None]:
        reactor = payload.get("reactor")
        if not isinstance(reactor, dict):
            return None, None, None
        frequency = reactor.get("frecuencia")
        coherence = reactor.get("coherencia")
        try:
            frequency = None if frequency is None else float(frequency)
            coherence = None if coherence is None else float(coherence)
        except (TypeError, ValueError) as exc:
            raise BAL003ProtocolError("BAL-003 reactor contains non-numeric frequency/coherence") from exc
        timestamp = reactor.get("timestamp_utc") or payload.get("timestamp_utc")
        return frequency, coherence, None if timestamp is None else str(timestamp)

    def reactor(self) -> BAL003Observation:
        url, _raw, result = self._get(DEFAULT_PAYGATE_PORT, "/reactor")
        payload = result["payload"]
        frequency, coherence, timestamp = self._reactor_frequency(payload)
        return BAL003Observation("BAL003", url, timestamp, frequency, coherence, result["sha256"], payload)

    def ecosystem(self) -> BAL003Observation:
        url, _raw, result = self._get(DEFAULT_PAYGATE_PORT, "/ecosistema")
        payload = result["payload"]
        frequency = payload.get("frecuencia")
        coherence = payload.get("coherencia")
        try:
            frequency = None if frequency is None else float(frequency)
            coherence = None if coherence is None else float(coherence)
        except (TypeError, ValueError) as exc:
            raise BAL003ProtocolError("BAL-003 ecosystem contains non-numeric frequency/coherence") from exc
        timestamp = payload.get("timestamp_utc")
        return BAL003Observation("BAL003", url, None if timestamp is None else str(timestamp), frequency, coherence, result["sha256"], payload)

    def monitor(self, path: str = "/health") -> BAL003Observation:
        if path not in {"/health", "/status", "/ecosystem"}:
            raise ValueError("monitor path must be /health, /status or /ecosystem")
        url, _raw, result = self._get(DEFAULT_MONITOR_PORT, path)
        return BAL003Observation("BAL003-monitor", url, None, None, None, result["sha256"], result["payload"])

    def acquire(self) -> dict[str, Any]:
        """Collect read-only reactor + monitor evidence without synthesizing data."""
        reactor = self.reactor()
        monitor = self.monitor("/health")
        return {
            "node_id": "BAL003",
            "reference_frequency_hz": F0_QCAL_HZ,
            "reactor": reactor.evidence_record(),
            "monitor_health": monitor.evidence_record(),
        }


def fetch_bal003() -> dict[str, Any]:
    return BAL003Adapter().acquire()


if __name__ == "__main__":
    print(json.dumps(fetch_bal003(), indent=2, sort_keys=True))
