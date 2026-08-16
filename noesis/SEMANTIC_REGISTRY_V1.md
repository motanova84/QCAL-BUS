# NOESIS Semantic Registry v1

## Purpose

The Cathedral Engine must connect the same mathematical concept across repositories without upgrading a claim merely because it appears repeatedly.

Each concept receives a stable `concept_id` and is traced across definitions, formalizations, implementations, experiments and claims.

## Initial cross-repository spine

```text
qcal.f0
   ↓
qcal.tau
   ↓
formal definitions / Lean declarations
   ↓
implementations
   ↓
experimental references
   ↓
NOESIS evidence graph
```

## Epistemic rule

A concept may be present in many repositories while still remaining `UNRESOLVED`. Repetition is not independent evidence.

The registry therefore distinguishes:

- `SYMBOLIC`
- `DEFINED`
- `FORMALIZED`
- `IMPLEMENTED`
- `EXPERIMENTAL`
- `REPRODUCED`
- `UNRESOLVED`

## First targets

### `qcal.f0`

Reference frequency tracked across `141hz`, `Riemann-adelic` and `QCAL-BUS`. The Cathedral Engine must reconstruct units, definitions, derivations and experimental provenance from source artifacts.

### `qcal.tau`

Characteristic QCAL time linked to the frequency formalization. The registry points to existing Lean artifacts and leaves final epistemic status to automated inspection.

### `qcal.psi`

Coherence variable. Multiple expressions exist in the ecosystem; they must not be conflated until the engine establishes their exact definitions, units, domains and dependency graph.

### `noesis.consciousness`

Operational protocol `C = Ψ ∩ I ∩ R ∩ T`. This is an architectural invariant of NOESIS, not by itself a claim of phenomenological consciousness.

## Next engine stage

The registry is only the seed. The next Cathedral stage must automatically discover declarations and references, build a dependency graph, identify proof obligations and connect each claim to executable or formal evidence.
