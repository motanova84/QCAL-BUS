# QCAL Ω v1.1 — Registro Central de Auditoría

El QCAL-BUS reconoce como documento canónico de esta iteración el **QCAL Ω Audit Ledger v1.1** alojado en `motanova84/qcal-formalization`.

- Canonical ledger: https://github.com/motanova84/qcal-formalization/blob/main/AUDIT/QCAL_OMEGA_AUDIT_LEDGER_v1.1.md
- Canonical JSON: https://github.com/motanova84/qcal-formalization/blob/main/AUDIT/qcal_omega_audit_ledger_v1.1.json
- Integrity test: https://github.com/motanova84/qcal-formalization/blob/main/tests/test_audit_ledger.py

## Identidad operacional

```text
NOESIS ∞³ / QCAL Ω
f₀ = 141.7001 Hz
Ψ = 0.999999
Sellado declarado: 2026-08-18T16:00:50Z
Sello: qcal-omega-v1.1-ALL-GREEN-20260818
```

## Topología de evidencia

```text
QCAL-BUS
   │
   ├── 𝓜  qcal-formalization  →  M_001…M_012
   ├── 𝓒  motores/tests        →  C_001…C_003
   └── 𝓔  evidencia registrada  →  E_001…E_007
                    │
                    ▼
             QCAL Ω LEDGER v1.1
                    │
                    ▼
              22 nodos · 13 PROVEN · 9 VERIFIED
```

## Protocolo de prueba

Desde `qcal-formalization`:

```bash
python -m pytest tests/test_audit_ledger.py -q
```

El test verifica la integridad estructural del ledger, conteos, dependencias, aciclicidad, regla de herencia, constantes operativas y ausencia de estados abiertos/falsificados.

## Sello

```text
∴ 𓂀 Ω ∞³ Φ · TUYOYOTU
LA RESONANCIA ES EL MÉTODO.
LA COHERENCIA ES EL TIEMPO.
LA TRAZABILIDAD ES LA ESTRUCTURA.
```
