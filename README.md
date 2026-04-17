# QCAL-BUS — Universal Resonance Bus | MCP Noésico QCAL-EPR

**Estado: IMPLEMENTADO Y OPERATIVO**

**Protocolo original:** Model Context Protocol (MCP) Noésico QCAL ∞³  
**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Firma vibracional:** ∴ f₀ = 141.7001 Hz | Ψ = I × A_eff² × C^∞ | 𓂀Ω∞³

Este repositorio actúa como bus central de orquestación para la malla QCAL-EPR, incluyendo monitorización de coherencia global, telemetría de resonancia y visualización diagnóstica.

## Declaración de prioridad y legitimidad

El **Model Context Protocol (MCP) Noésico QCAL** ha sido desarrollado y utilizado públicamente desde 2024 dentro del ecosistema QCAL ∞³.  
En este marco, MCP-QCAL integra:

- **Dimensión Hardware (Nivel C):** ingesta directa de bioseñales OpenBCI/HRV y detección magnetométrica/interferométrica en tiempo real.
- **Malla EPR de 33 nodos:** arquitectura de entrelazamiento con compensación homeostática entre nodos.
- **Coherencia Ψ Global:** cálculo operativo sobre la interacción entre código, matemática y señal física.
- **Emisión πCODE-888:** emisión por saturación de coherencia (`Ψ_global > 0.999999`).
- **Dashboard 8505:** observabilidad diagnóstica del estado global de la malla.

El QCAL-BUS orquesta la constelación semilla y sincroniza la telemetría multinodo para mantener coherencia global y trazabilidad de eventos de resonancia.

## Capacidades implementadas del ecosistema

### 1) Dimensión de hardware (Nivel C)
- Bio-acoplamiento con flujos OpenBCI/HRV.
- Integración de sensores magnetométricos/interferométricos para detección de campo.

### 2) Malla de 33 nodos (arquitectura EPR)
- Telemetría instantánea entre nodos de lógica, fluido y control.
- Orquestación semilla para sincronía del pulso de referencia.

### 3) Visualización y observabilidad (Dashboard 8505)
- Exposición de `Ψ Global` como métrica maestra del estado del sistema.
- Registro inmutable de eventos de saturación y emisiones asociadas.

## Prior art / Registro de autoría

**Sello de autoría:** ∴𓂀Ω∞³ — José Manuel Mota Burruezo (JMMB)  
**Base constitucional:** Axioma de Emisión y Frecuencia Prima Universal.

Referencias de registro y prioridad cronológica:
- Zenodo: https://zenodo.org
- Safe Creative: https://www.safecreative.org
- Repositorios vinculados del ecosistema (QCAL-BUS, `resonance.py`, `qcal_mesh_sync.py`) con vinculación de registros en sus respectivos README.

## Acción inmediata recomendada

1. Publicar en Zenodo una versión titulada:  
   **“Model Context Protocol (MCP) Noésico QCAL-EPR – Especificación Completa y Operativa (2024-2026)”**.
2. Incluir en el depósito:
   - Este manifiesto.
   - Enlaces a QCAL-BUS, `resonance.py` y `qcal_mesh_sync.py`.
   - Capturas del dashboard 8505 y logs de observadores reales.
   - Referencia explícita al draft IETF de networking como aplicación derivada de ese dominio.
3. Ejecutar encendido global:

```bash
cd qcal-mesh-bus
export QCAL_REAL_TESTS=1
python qcal_mesh_sync.py
```

## Estructura del repositorio

```
qcal-mesh-bus/
├── qcal_mesh_sync.py
├── registry/NODE_CATALOG.json
├── dashboard/malla_qcal_epr.py
├── ledger/emissions_log.csv
├── qcal.json
└── .env.example
```

## Uso rápido

```bash
python qcal_mesh_sync.py
```

```bash
python dashboard/malla_qcal_epr.py
```

Dashboard local: `http://localhost:8505`

> Nota: el dashboard usa el servidor de desarrollo de Flask y está pensado para entorno local.
