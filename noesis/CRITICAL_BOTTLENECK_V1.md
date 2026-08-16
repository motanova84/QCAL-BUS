# NOESIS Critical Bottleneck v1

## Purpose
Rank unresolved graph objects by potential downstream impact so the Daily Solver has a reproducible candidate priority.

## Rule
`CANDIDATE` is a scheduling state, not a theorem, claim validation, or scientific conclusion.

## v1 score

`score(v) = 10 * downstream_degree(v) + upstream_degree(v)`

The score is intentionally transparent and deterministic. Later versions may incorporate transitive reachability, dependency depth and verified resolution cost, but any change must version the ranking schema.

## Output

```bash
python -m noesis.critical_bottleneck --graph checkpoints/checkpoint_v1.json --output checkpoints/bottleneck_v1.json
```

The output retains the source graph digest and lists candidates in deterministic order.

## Epistemic boundary

A high score means only that resolving the node may affect many currently connected graph objects. It does not mean the node is true, fundamental, or scientifically important.
