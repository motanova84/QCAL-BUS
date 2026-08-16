"""Build a canonical NOESIS ecosystem snapshot from discovery observations."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

REFERENCE_FREQUENCY_HZ = 141.7001


def build_snapshot(discovery: dict[str, Any], *, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    observations = discovery.get("observations", [])
    states: dict[str, str] = {}
    for item in observations:
        service = item["service_id"]
        current = states.get(service)
        state = item["state"]
        rank = {"HEALTHY": 3, "REACHABLE": 2, "UNREACHABLE": 1}.get(state, 0)
        previous_rank = {"HEALTHY": 3, "REACHABLE": 2, "UNREACHABLE": 1}.get(current or "", 0)
        if current is None or rank > previous_rank:
            states[service] = state

    body: dict[str, Any] = {
        "schema": "NOESIS-SNAPSHOT/1.0",
        "reference_frequency_hz": REFERENCE_FREQUENCY_HZ,
        "node": "BAL003",
        "services": dict(sorted(states.items())),
        "evidence_graph": evidence or {"status": "NOT_PROVIDED"},
        "discovery_sha256": discovery.get("snapshot_sha256"),
    }
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    body["snapshot_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    body["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    return body


def main() -> None:
    from .discovery_layer import discover
    snapshot = build_snapshot(discover())
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
