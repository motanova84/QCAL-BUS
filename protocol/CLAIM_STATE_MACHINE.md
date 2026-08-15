# QCAL Claim State Machine v1

A claim in the ecosystem progresses through explicit evidence states:

```text
PROPOSED
   ↓
DEFINED
   ↓
IMPLEMENTED
   ↓
FORMAL_PASS ───────┐
   ↓               │
EXPERIMENTAL_PASS  │
   ↓               │
REPRODUCED        │
   ↓               │
REVIEW            │
   ↓               │
ARCHIVED ◄────────┘
```

`FAIL` is a terminal result for the current evidence run and may be reopened only by a new, traceable claim update.

## Epistemic separation

- `FORMAL_PASS` means the declared formal artifact passed its formal verification process.
- `EXPERIMENTAL_PASS` means the declared experiment passed its declared analysis criteria.
- `REPRODUCED` means the result was reproduced under the declared reproduction protocol.
- `REVIEW` means human or independent review is pending or has identified an issue.
- `ARCHIVED` means the exact state and evidence have been immutably recorded.

No transition may infer physical truth solely from a formal result. No transition may infer consciousness solely from `f0` or `Ψ`.
