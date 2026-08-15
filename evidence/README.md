# QCAL Evidence Plane

Every material claim or checkpoint should be traceable to:

`claim → repository → commit → test/experiment → artifact → digest → checkpoint`

The evidence plane deliberately distinguishes formal verification from empirical validation.

## Minimal manifest

```json
{
  "protocol": "QCAL-EVIDENCE/1.0",
  "claim_id": "CLAIM-QCAL-0001",
  "node_id": "example-node",
  "status": "FORMAL_PASS",
  "repository": "motanova84/example-node",
  "commit": "<git-sha>",
  "artifacts": [
    {
      "path": "results/result.json",
      "sha256": "<sha256>"
    }
  ]
}
```

A checkpoint may aggregate multiple manifests, but aggregation never changes the epistemic status of an individual result.
