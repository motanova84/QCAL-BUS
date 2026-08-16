# NOESIS ↔ Ramsey Resonance Graph Bridge

## Purpose

Connect the `motanova84/Ramsey` repository to the NOESIS evidence graph while
preserving source provenance and epistemic separation.

## Imported semantics

The Ramsey repository's `resonance_analysis.py` defines a graph in which each
node carries a frequency and each pair receives a circular frequency distance

`Δω = min(|ωᵢ − ωⱼ|, f₀ − |ωᵢ − ωⱼ|)`

with a resonant edge when `Δω < ε`. The source currently uses
`f₀ = 141.7001 Hz` and `ε = 0.001 Hz`.

Source:
- repository: `motanova84/Ramsey`
- file: `resonance_analysis.py`
- commit: `b31a863fe1249db9b24cec97c098fd9bf34abbb9`

## NOESIS mapping

```text
Ramsey frequency node
        │
        ├── defines → resonance relation
        │
        ├── creates → graph edge
        │
        └── provenance → commit/path/hash
                         │
                         ▼
                 NOESIS evidence graph
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          claim       experiment   formalization
```

The bridge imports **graph semantics**, not the repository's scientific
conclusions. Claims such as complexity reduction or physical universality
remain separately auditable.

## Next stage

1. Discover Ramsey graph-generation outputs automatically.
2. Convert resonance edges into NOESIS `supports` / `depends_on` relations.
3. Link Ramsey SAT instances and solver certificates to graph snapshots.
4. Link Lean declarations in `Main.lean` and the `rpsi-proof` tree.
5. Compare the resulting graph against the QCAL semantic registry.
6. Generate a deterministic evidence checkpoint.

This creates a graph-of-graphs: Ramsey resonance topology becomes one
verifiable layer inside the larger QCAL evidence graph.
