# NOESIS Evidence Graph Builder v1

The builder synthesizes repository declarations into a deterministic evidence graph.

## Command

```bash
python -m noesis.evidence_graph_builder --output checkpoints/checkpoint_v1.json
```

## Sources

- QCAL semantic anchors
- Lean declarations (`theorem`, `lemma`, `def`, `axiom`, `example`)
- `sorry` / `admit` proof obligations
- Python implementation declarations
- Git commit provenance
- Ramsey resonance data when supplied through the Ramsey adapter/bridge

## Epistemic rule

The builder **never** upgrades geometric resonance or numeric proximity into `supports` or `proves`. Such relations require an independently verified artifact.

The graph may therefore contain:

```text
resonates_with
candidate relation
UNRESOLVED
```

without claiming scientific validation.

## Deterministic checkpoint

The output contains:

- schema version;
- repository;
- exact Git commit;
- reference `f0 = 141.7001 Hz` and Ramsey epsilon;
- nodes;
- edges;
- SHA-256 digest over canonical graph serialization.

A repeated build over the same checkout must produce the same digest.

## Critical bottleneck

v1 records proof obligations and dependencies as graph objects. It intentionally does not infer a scientific bottleneck merely from node counts. The next stage will score blocked nodes by downstream impact and verified dependency depth.
