# NOESIS Discovery Layer v1

## Purpose

NOESIS Discovery converts the documented BAL003 topology into an auditable,
read-only observation layer. It does not replace `templo_core/noesis_live.py`
and it does not invoke its production/autopoietic execution loop.

`noesis_live.py` is a production loop that calls `BucleNoetico(dry_run=False)`
and can execute existing operational motors. Discovery intentionally stays on
the observation side of that boundary. The source implementation is in the
`141hz` repository.

## Lifecycle

```text
DISCOVERED -> DOCUMENTED -> REACHABLE -> HEALTHY -> OBSERVING
```

A service may stop at any stage. `REACHABLE` means network connectivity; it is
not proof that the application protocol is healthy. `HEALTHY` is reserved for
successful documented HTTP GET observations.

## Safety contract

* Only services declared in `noesis/service_registry.json` are probed.
* HTTP probes use `GET` only.
* TCP services use connection establishment only.
* No SSH authentication or remote command execution occurs.
* No credentials are sent by the discovery layer.
* No configuration, ledger, channel, wallet, or service state is mutated.
* Unknown ports are not scanned.
* Raw HTTP response bytes are hashed with SHA-256 before parsing.

## BAL003 registry

The initial registry is deliberately limited to interfaces already documented
in the ecosystem:

| Service | Endpoint | Probe | Access |
|---|---|---|---|
| QCAL-SYMBIO | `195.201.219.237:8844` | documented HTTP GET paths | read-only |
| Monitor | `195.201.219.237:5050` | documented HTTP GET paths | read-only |
| LNDHub | `195.201.219.237:8000` | TCP connect | read-only |
| Bitcoin Core | `195.201.219.237:8505` | TCP connect | read-only |
| LND | `195.201.219.237:9735` | TCP connect | read-only |
| SSH | `195.201.219.237:22` | TCP connect only | read-only |

Reachability is not treated as evidence of a physical frequency measurement.

## Evidence boundary

`f0 = 141.7001 Hz` is the ecosystem reference value. Discovery never rewrites
an observed value to that reference. Any future BAL003 measurement adapter must
preserve the original payload, timestamp, uncertainty and provenance and derive
`delta_hz = measured_frequency_hz - 141.7001` without correction.

## Snapshot

`noesis/snapshot.py` converts discovery observations into a canonical snapshot
with a SHA-256 digest. The generated timestamp is metadata; the digest is over
the canonical snapshot body before the timestamp is appended.
