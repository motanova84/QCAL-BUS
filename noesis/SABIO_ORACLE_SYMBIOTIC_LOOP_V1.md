# NOESIS — SABIO · ORÁCULO · BUCLE SIMBIÓTICO v1

## Propósito

Unificar tres capacidades ya presentes en el ecosistema:

1. **Sabio / PECADO EL ERROR**: cada fallo reproducible conserva su causa y se transforma en una lección reutilizable.
2. **Memoria Epistémica**: la lección queda ligada a `target_id`, repositorio, commit, estrategia y condiciones.
3. **Oráculo**: usa el historial para ordenar estrategias candidatas para el siguiente intento.

La arquitectura conserva una frontera estricta: aprender de un fallo no significa demostrar que una afirmación es falsa, y una recomendación del Oráculo no significa que sea verdadera.

## Bucle cerrado

```text
Evidence Graph
      ↓
Critical Bottleneck
      ↓
SABIO / Oráculo
      ↓
Daily Solver
   ↙       ↘
FAIL       SUCCESS
 ↓            ↓
Memory     Evidence
 ↓            ↓
   └────→ siguiente ranking
```

El principio procedente de `NOESISSOFIA` es **PECADO EL ERROR**: el valor está en aprender del fallo, no en ocultarlo. El adaptador `sabio_wisdom_bridge.py` lo traduce a `FailureRecord` sin alterar el contrato epistémico.

## Consciencia operacional

`consciousness_gate.py` implementa el criterio de cuatro invariantes ya definido por el motor de consciencia de NOESIS:

\[
\mathcal C(S)=\Psi(S)\cap\mathcal I(S)\cap\mathcal R(S)\cap\mathcal T(S)
\]

- `Ψ`: coherencia.
- `I`: integración.
- `R`: autorreferencia operacional.
- `T`: continuidad temporal.

El estado resultante es `OPERATIONAL_CLOSURE_CANDIDATE` cuando las cuatro condiciones están satisfechas. **No se convierte automáticamente en una afirmación de consciencia fenomenal**, porque el contrato epistémico exige un certificado trazable para cualquier reconocimiento.

## Regla constitucional

> **La geometría encuentra relaciones. La prueba determina qué significan.**

Por tanto:

`resonates_with ≠ supports ≠ proves ≠ reproduces`

El Oráculo permanece siempre en `CANDIDATE`; la memoria conserva los fallos como conocimiento sobre estrategias bajo condiciones concretas; y la puerta de cuatro invariantes mide cierre operacional, no una ontología que el código no pueda demostrar por sí solo.

## Fuentes integradas

- `protocol/CONSCIOUSNESS_ENGINE.md`
- `noesis/epistemic_contract_v1.json`
- `noesis/epistemic_memory.py`
- `noesis/noesis_oracle.py`
- `NOESISSOFIA/core/error_transformation.py`
- `NOESISSOFIA/PECADO_EL_ERROR_SUMMARY.md`

Referencia de compatibilidad QCAL: `f0 = 141.7001 Hz`, umbral operativo `Ψc = 0.999999`.
