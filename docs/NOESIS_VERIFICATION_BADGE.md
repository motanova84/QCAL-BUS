# NOESIS Verification Badge

The verification badge is intentionally tied to the repository's GitHub Actions workflow rather than a manually asserted status.

[![NOESIS CI](https://github.com/motanova84/QCAL-BUS/actions/workflows/noesis-validation.yml/badge.svg)](https://github.com/motanova84/QCAL-BUS/actions/workflows/noesis-validation.yml)

## Evidence rule

A green badge means GitHub Actions reports the `noesis-validation.yml` workflow as successful for the selected branch/workflow view. It is not a claim that BAL003 has produced a physical measurement of 141.7001 Hz.

Physical observations must remain separately attributable to BAL003, with timestamp, raw payload hash, uncertainty and provenance.

Reference frequency used by the software invariants:

```text
f0 = 141.7001 Hz
```

## README snippet

```markdown
[![NOESIS CI](https://github.com/motanova84/QCAL-BUS/actions/workflows/noesis-validation.yml/badge.svg)](https://github.com/motanova84/QCAL-BUS/actions/workflows/noesis-validation.yml)
```
