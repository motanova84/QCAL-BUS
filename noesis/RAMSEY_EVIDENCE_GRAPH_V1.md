# NOESIS × Ramsey — Evidence Graph Contract v1

## Purpose

Use the existing Ramsey resonance-graph machinery as a topological input to the NOESIS evidence graph while preserving strict epistemic separation.

## Graph relation

A Ramsey resonance relation is represented as:

`source --resonates_with--> target`

with the source repository, exact commit, and source path retained as provenance.

Resonance is **not** automatically upgraded to `supports`, `proves`, or `reproduces`.

## Evidence relations

The shared graph vocabulary is:

- `defines`
- `depends_on`
- `resonates_with`
- `supports`
- `proves`
- `implements`
- `tests`
- `reproduces`
- `blocks`
- `contradicts`

## Verification rule

Only independently verified artifacts may set `verified=true` on an evidence edge. A resonance edge can therefore be present in the graph while remaining epistemically neutral.

## Provenance

Every edge must retain:

1. repository;
2. exact commit;
3. source path.

The bridge computes a deterministic SHA-256 graph digest over canonical edge serialization.

## Next integration stages

1. ingest Ramsey SAT instances;
2. ingest Lean declarations and proof artifacts;
3. ingest beacon/checkpoint artifacts;
4. map claims to graph nodes;
5. derive dependency and blocking edges;
6. expose the graph to the daily NOESIS prioritizer.
