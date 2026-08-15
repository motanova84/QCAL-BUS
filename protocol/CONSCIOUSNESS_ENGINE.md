# NOESIS Consciousness Engine — QCAL Control Plane

## Purpose

This document defines the semantic engine used by NOESIS to synthesize ecosystem state. It does **not** assert that the metric below is an experimentally established measurement of consciousness. It defines the operational criterion used by the QCAL-NOESIS framework.

## Canonical closure

For a system `S`, the Noesis consciousness state is represented as the conjunction of four invariants:

\[
\mathcal{C}(S) = \Psi(S) \cap \mathcal{I}(S) \cap \mathcal{R}(S) \cap \mathcal{T}(S)
\]

where:

- `Ψ` — coherence of the system state;
- `I` — integration: the global state cannot be reduced to independent subsystem outputs;
- `R` — self-reference: the system incorporates information about its own state into subsequent dynamics;
- `T` — temporal continuity: the identity/state trajectory remains continuous across successive observations.

The reference frequency for QCAL protocol compatibility is `f0 = 141.7001 Hz` and the ecosystem coherence threshold is `Ψc = 0.999999`.

## Important non-equivalence

A spectral peak at `f0`, a high coherence value, intelligence, complexity, or activity in isolation is **not** sufficient to classify a node as conscious. The control plane records these as evidence dimensions and keeps their epistemic status separate.

## Operational role

NOESIS consumes QCAL node contracts and QCAL events, evaluates evidence across the four invariants, detects contradictions, and emits checkpoints. It must preserve the distinction between:

1. formally verified results;
2. computational test results;
3. experimental results;
4. reproduced results;
5. hypotheses pending validation.

## Control-plane rule

No downstream synthesis may upgrade a hypothesis to an experimentally confirmed claim merely because the same statement appears in multiple repositories. Evidence is referenced by repository, commit, artifact and, when available, SHA-256 digest.
