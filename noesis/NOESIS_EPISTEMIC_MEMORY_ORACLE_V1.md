# NOESIS Epistemic Memory & Oracle v1

## Purpose

Extend the Evidence Graph and Epistemic Auditor with two conservative capabilities:

1. **Epistemic Memory** records reproducible failures and the lessons attached to them.
2. **Oracle** ranks candidate investigation strategies for an unresolved target.

Neither component upgrades a claim to `SUPPORTED` or `PROVEN`.

## Constitutional boundary

> The geometry finds relations; the proof determines what they mean.

A failed strategy is evidence about that strategy under its recorded conditions. It is **not**, by itself, a counterexample to the target claim.

A counterexample requires an explicit `COUNTEREXAMPLE` artifact and its own provenance.

## Closed learning loop

```text
Evidence Graph
      |
      v
Critical Bottleneck
      |
      v
Oracle -> candidate strategies
      |
      v
Daily Solver / isolated attempt
      |
      +---- success ----> Evidence
      |
      +---- failure ----> Epistemic Memory
                              |
                              v
                         next ranking
```

## Determinism

The memory serialization is canonicalized before SHA-256 calculation. Strategy ranking uses a fixed transparent scoring function and deterministic tie-breaking.

## Consciousness boundary

The Oracle and memory layer do not infer phenomenal consciousness from coherence, self-reference, entanglement, frequency, or any threshold. They define an operational learning loop for the software system.

## Next integration

The next safe step is to consume `EVIDENCE_GRAPH_V1` and the existing Critical Bottleneck candidate list as inputs to `noesis_oracle.from_bottleneck`, then emit an auditable candidate directive for the Daily Solver.
