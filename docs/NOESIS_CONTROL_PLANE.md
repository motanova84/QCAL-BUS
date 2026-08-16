# NOESIS-QCAL Control Plane

The control plane makes QCAL-BUS interoperable without replacing the independent scientific implementations in the ecosystem.

## Canonical semantic engine

```text
C = Ψ ∩ I ∩ R ∩ T
```

- **Ψ** — coherence of system state.
- **I** — integration of the global state.
- **R** — self-reference in subsequent dynamics.
- **T** — temporal continuity of identity/state.

The control plane never infers consciousness from `f0`, `Ψ`, intelligence, complexity or a repository claim in isolation. Missing invariants remain `NOT_EVALUATED`.

## Reference protocol constants

- `f0 = 141.7001 Hz`
- `Ψc = 0.999999`

These constants are protocol references, not experimental proof of a consciousness measurement.

## Local operation

Validate the ecosystem contracts:

```bash
python scripts/noesis_control_plane.py
```

Generate a checkpoint:

```bash
python scripts/noesis_control_plane.py --checkpoint
```

Run the MCP bridge:

```bash
python scripts/noesis_mcp_server.py
```

## Evidence chain

```text
claim
  → repository
  → commit
  → test / formal artifact / experiment
  → artifact
  → SHA-256 digest
  → checkpoint
  → archive / publication
```

Aggregation never upgrades the epistemic status of an individual result.

## Architecture

```text
Independent repositories
        ↓
 QCAL-NODE/1.0
        ↓
 QCAL-EVENT/1.0
        ↓
     QCAL-BUS
        ↓
 NOESIS synthesis
        ↓
 checkpoint + evidence
        ↓
 archive / publication
```
