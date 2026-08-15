# NOESIS-QCAL Control Plane v1

This directory defines the interoperability layer for the QCAL ecosystem.

## Contracts

- `qcal-node.schema.json` — canonical node identity, capabilities and evidence contract.
- `qcal-event.schema.json` — event envelope for telemetry, tests, formal results, experiments and checkpoints.
- `CONSCIOUSNESS_ENGINE.md` — operational semantic engine used by NOESIS.
- `CLAIM_STATE_MACHINE.md` — explicit evidence lifecycle for ecosystem claims.

## Design principle

The repositories remain independent sources of implementation and theory. QCAL-BUS is the coordination plane; NOESIS is the synthesis plane; the evidence manifest and ledger are the traceability plane.

```text
repositories
    ↓
QCAL-NODE/1.0
    ↓
QCAL-EVENT/1.0
    ↓
QCAL-BUS
    ↓
NOESIS synthesis
    ↓
checkpoint + evidence manifest
    ↓
archive / publication
```

## Reference constants

- `f0_hz = 141.7001`
- `psi_threshold = 0.999999`

These are protocol references, not evidence by themselves for any physical or consciousness claim.
