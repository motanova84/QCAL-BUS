"""BAL003 telemetry adapter for the NOESIS evidence graph.

The adapter records the payload received from BAL003 without rewriting the
measurement. Authentication is supplied only through the environment; no
credential is stored in source control.

Required environment variables:
    BAL003_BEARER_TOKEN

Optional:
    BAL003_HOST (default: 195.201.219.237)
    BAL003_PORT (default: 8443)
    BAL003_PATH (default: /api/v1/telemetry/frequency)
    BAL003_TIMEOUT_S (default: 10)
    BAL003_CA_BUNDLE (optional CA bundle path)
    BAL003_VERIFY_TLS (default: true; set false only for controlled testing)
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

F0_QCAL_HZ = 141.7001


class BAL003Error(RuntimeError):
    """Base error for BAL003 acquisition failures."""


class BAL003ConfigurationError(BAL003Error):
    """Raised when required connection configuration is missing or invalid."""


class BAL003ProtocolError(BAL003Error):
    """Raised when BAL003 returns an invalid telemetry document."""


@dataclass(frozen=True)
class BAL003Measurement:
    node_id: str
    timestamp_utc: str
    measured_frequency_hz: float
    uncertainty_hz: float | None
    coherence_psi: float | None
    hardware_signature: str | None
    raw_sha256: str
    endpoint: str

    @property
    def delta_hz(self) -> float:
        return self.measured_frequency_hz - F0_QCAL_HZ

    def evidence_record(self) -> dict[str, Any]:
        """Return a derived record while retaining the measured value verbatim."""
        record = asdict(self)
        record.update(
            {
                "reference_frequency_hz": F0_QCAL_HZ,
                "delta_hz": self.delta_hz,
                "classification": (
                    "supports_reference"
                    if self.delta_hz == 0.0
                    else "reproducible_drift"
                ),
            }
        )
        return record


class BAL003Adapter:
    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        path: str | None = None,
        timeout_s: float | None = None,
        bearer_token: str | None = None,
        verify_tls: bool | None = None,
        ca_bundle: str | None = None,
    ) -> None:
        self.host = host or os.getenv("BAL003_HOST", "195.201.219.237")
        self.port = int(port or os.getenv("BAL003_PORT", "8443"))
        self.path = path or os.getenv("BAL003_PATH", "/api/v1/telemetry/frequency")
        self.timeout_s = float(timeout_s or os.getenv("BAL003_TIMEOUT_S", "10"))
        self.bearer_token = bearer_token or os.getenv("BAL003_BEARER_TOKEN")
        verify_value = os.getenv("BAL003_VERIFY_TLS", "true") if verify_tls is None else str(verify_tls)
        self.verify_tls = verify_value.lower() not in {"0", "false", "no"}
        self.ca_bundle = ca_bundle or os.getenv("BAL003_CA_BUNDLE")

        if not self.bearer_token:
            raise BAL003ConfigurationError("BAL003_BEARER_TOKEN is required")
        if not self.path.startswith("/"):
            raise BAL003ConfigurationError("BAL003_PATH must start with '/'")

    @property
    def url(self) -> str:
        return f"https://{self.host}:{self.port}{self.path}"

    def fetch_raw(self) -> bytes:
        request = Request(
            self.url,
            headers={
                "Authorization": f"Bearer {self.bearer_token}",
                "Accept": "application/json",
                "User-Agent": "NOESIS-BAL003/1.0",
            },
            method="GET",
        )
        # urllib uses the platform trust store by default. A custom CA bundle
        # is opt-in. We intentionally never disable TLS verification by default.
        context = None
        if self.url.startswith("https://"):
            import ssl
            context = ssl.create_default_context(cafile=self.ca_bundle) if self.ca_bundle else ssl.create_default_context()
            if not self.verify_tls:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
        try:
            with urlopen(request, timeout=self.timeout_s, context=context) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            raise BAL003Error(f"BAL003 acquisition failed: {exc}") from exc

    def fetch(self) -> BAL003Measurement:
        raw = self.fetch_raw()
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BAL003ProtocolError("BAL003 response is not valid UTF-8 JSON") from exc
        if not isinstance(payload, dict):
            raise BAL003ProtocolError("BAL003 payload must be a JSON object")

        required = {"node_id", "timestamp_utc", "measured_frequency_hz"}
        missing = sorted(required - payload.keys())
        if missing:
            raise BAL003ProtocolError(f"BAL003 payload missing fields: {', '.join(missing)}")
        if payload["node_id"] != "BAL003":
            raise BAL003ProtocolError(f"unexpected node_id: {payload['node_id']!r}")

        try:
            measured = float(payload["measured_frequency_hz"])
            uncertainty = payload.get("uncertainty_hz")
            coherence = payload.get("coherence_psi")
            uncertainty = None if uncertainty is None else float(uncertainty)
            coherence = None if coherence is None else float(coherence)
        except (TypeError, ValueError) as exc:
            raise BAL003ProtocolError("BAL003 numeric telemetry field is invalid") from exc

        return BAL003Measurement(
            node_id="BAL003",
            timestamp_utc=str(payload["timestamp_utc"]),
            measured_frequency_hz=measured,
            uncertainty_hz=uncertainty,
            coherence_psi=coherence,
            hardware_signature=payload.get("hardware_signature"),
            raw_sha256=hashlib.sha256(raw).hexdigest(),
            endpoint=self.url,
        )


def fetch_bal003() -> dict[str, Any]:
    """Fetch one BAL003 observation and return its evidence record."""
    return BAL003Adapter().fetch().evidence_record()


if __name__ == "__main__":
    print(json.dumps(fetch_bal003(), indent=2, sort_keys=True))
