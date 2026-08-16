# BAL003 → NOESIS Evidence Bridge

BAL003 is the physical observation node for the NOESIS evidence layer.

## Endpoint

- Host: `195.201.219.237`
- Port: `8443`
- Transport: HTTPS
- Path: `/api/v1/telemetry/frequency`
- Authentication: `Authorization: Bearer <JWT>` supplied at runtime

No credential is committed to this repository.

## Raw-data rule

The adapter preserves the received measurement exactly as a numeric value and
computes the SHA-256 digest of the raw response bytes. The QCAL reference
`141.7001 Hz` is used only for a derived comparison. A non-matching physical
measurement is never rounded, replaced, or coerced to the reference.

## Evidence classification

- `supports_reference`: measured frequency is exactly equal to the configured
  reference in the parsed numeric representation.
- `reproducible_drift`: measured frequency differs from the reference.

This classification is descriptive. It does not by itself establish physical
causality or scientific validity.

## Runtime

```bash
export BAL003_BEARER_TOKEN='...'
python -m noesis.bal003_adapter
```

Optional configuration:

```text
BAL003_HOST
BAL003_PORT
BAL003_PATH
BAL003_TIMEOUT_S
BAL003_CA_BUNDLE
BAL003_VERIFY_TLS
```

TLS verification is enabled by default. Use a custom CA bundle when BAL003
uses a private CA. Disabling TLS verification is supported only for controlled
testing and must not be used for production evidence collection.

## Evidence graph integration

The adapter returns an evidence-ready record containing:

- node ID;
- source timestamp;
- measured frequency;
- uncertainty, when supplied;
- coherence, when supplied;
- hardware signature, when supplied;
- raw response SHA-256;
- endpoint;
- reference frequency;
- derived frequency delta;
- classification.

A downstream evidence-graph writer can persist this record without altering the
raw observation.
