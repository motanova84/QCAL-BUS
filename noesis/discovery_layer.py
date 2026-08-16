"""NOESIS read-only discovery for documented BAL003 services.

The discovery layer deliberately has no mutation primitives: HTTP probes use
GET only and network probes only establish a TCP connection. It never sends
credentials, executes remote commands, changes configuration, or writes to
BAL003.

A service is never probed unless it is present in service_registry.json.
"""
from __future__ import annotations

import hashlib
import json
import socket
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT / "service_registry.json"
DEFAULT_TIMEOUT = 5.0


@dataclass(frozen=True)
class ProbeResult:
    service_id: str
    node_id: str
    host: str
    port: int
    role: str
    transport: str
    state: str
    checked_at_utc: str
    endpoint: str | None = None
    http_status: int | None = None
    raw_sha256: str | None = None
    payload: Any = None
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("policy", {}).get("mutations_allowed", True):
        raise ValueError("Discovery registry must explicitly forbid mutations")
    return data


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _raw_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def probe_http(service: dict[str, Any], path: str, timeout: float) -> ProbeResult:
    base = f"{service['transport']}://{service['host']}:{service['port']}"
    endpoint = base + path
    request = Request(endpoint, method="GET", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            content_type = response.headers.get("Content-Type", "")
            try:
                payload: Any = json.loads(raw.decode("utf-8")) if raw else None
            except (UnicodeDecodeError, json.JSONDecodeError):
                payload = {"content_type": content_type, "bytes": len(raw)}
            return ProbeResult(
                service_id=service["id"], node_id=service["node_id"],
                host=service["host"], port=service["port"], role=service["role"],
                transport=service["transport"], state="HEALTHY",
                checked_at_utc=_now(), endpoint=endpoint,
                http_status=getattr(response, "status", None),
                raw_sha256=_raw_hash(raw), payload=payload,
            )
    except HTTPError as exc:
        return ProbeResult(
            service_id=service["id"], node_id=service["node_id"],
            host=service["host"], port=service["port"], role=service["role"],
            transport=service["transport"], state="REACHABLE",
            checked_at_utc=_now(), endpoint=endpoint,
            http_status=exc.code, error="http_error",
        )
    except (URLError, TimeoutError, OSError) as exc:
        return ProbeResult(
            service_id=service["id"], node_id=service["node_id"],
            host=service["host"], port=service["port"], role=service["role"],
            transport=service["transport"], state="UNREACHABLE",
            checked_at_utc=_now(), endpoint=endpoint,
            error=type(exc).__name__,
        )


def probe_tcp(service: dict[str, Any], timeout: float) -> ProbeResult:
    endpoint = f"{service['host']}:{service['port']}"
    try:
        with socket.create_connection((service["host"], service["port"]), timeout=timeout):
            state = "REACHABLE"
            error = None
    except (TimeoutError, OSError) as exc:
        state = "UNREACHABLE"
        error = type(exc).__name__
    return ProbeResult(
        service_id=service["id"], node_id=service["node_id"],
        host=service["host"], port=service["port"], role=service["role"],
        transport=service["transport"], state=state, checked_at_utc=_now(),
        endpoint=endpoint, error=error,
    )


def discover(*, timeout: float = DEFAULT_TIMEOUT, registry_path: Path = REGISTRY_PATH) -> dict[str, Any]:
    """Probe only documented endpoints and return an auditable snapshot.

    No port scan is performed. Each target comes from the checked-in registry.
    """
    registry = load_registry(registry_path)
    results: list[dict[str, Any]] = []
    for service in registry["services"]:
        if service["health_mode"] == "http_get":
            for path in service["paths"]:
                results.append(probe_http(service, path, timeout).as_dict())
        elif service["health_mode"] == "tcp_connect":
            results.append(probe_tcp(service, timeout).as_dict())
        else:
            raise ValueError(f"Unknown health mode: {service['health_mode']}")

    canonical = json.dumps(results, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "schema": "NOESIS-DISCOVERY/1.0",
        "policy": registry["policy"],
        "reference_frequency_hz": registry["policy"]["reference_frequency_hz"],
        "observations": results,
        "snapshot_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(discover(), ensure_ascii=False, indent=2))
