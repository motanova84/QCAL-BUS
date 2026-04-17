# QCAL-BUS — Universal Resonance Bus | MCP Noésico QCAL-EPR

**Estado: IMPLEMENTADO Y OPERATIVO**

**Protocolo original:** Model Context Protocol (MCP) Noésico QCAL ∞³  
**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Firma vibracional:** ∴ f₀ = 141.7001 Hz | Ψ = I × A_eff² × C^∞ | 𓂀Ω∞³

Este repositorio actúa como bus central de orquestación para la malla QCAL-EPR, incluyendo monitorización de coherencia global, telemetría de resonancia y visualización diagnóstica.

> **Razón Noésica:** El "Observador" (el bus) no debe ser parte de lo "Observado" (los repositorios de teoría/código). Al separarlo, mantiene la coherencia Ψ limpia de interferencias operativas.

---

## Declaración de prioridad y legitimidad

El **Model Context Protocol (MCP) Noésico QCAL** ha sido desarrollado y utilizado públicamente desde 2024 dentro del ecosistema QCAL ∞³.  
En este marco, MCP-QCAL integra:

- **Dimensión Hardware (Nivel C):** ingesta directa de bioseñales OpenBCI/HRV y detección magnetométrica/interferométrica en tiempo real.
- **Malla EPR de 33 nodos:** arquitectura de entrelazamiento con compensación homeostática entre nodos.
- **Coherencia Ψ Global:** cálculo operativo sobre la interacción entre código, matemática y señal física.
- **Emisión πCODE-888:** emisión por saturación de coherencia (`Ψ_global > 0.999999`).
- **Dashboard 8505:** observabilidad diagnóstica del estado global de la malla.

El QCAL-BUS orquesta la constelación semilla y sincroniza la telemetría multinodo para mantener coherencia global y trazabilidad de eventos de resonancia.

---

## Capacidades implementadas del ecosistema

### 1) Dimensión de hardware (Nivel C)
- Bio-acoplamiento con flujos OpenBCI/HRV.
- Integración de sensores magnetométricos/interferométricos para detección de campo.

### 2) Malla de 33 nodos (arquitectura EPR)
- Telemetría instantánea entre nodos de lógica, fluido y control.
- Orquestación semilla para sincronía del pulso de referencia.

| Capa | Nodos | Estado |
|---|---|---|
| Núcleo | riemann-adelic, 141-hz | ✅ Definidos |
| Cuerpo | 3d-navier-stokes, p-np-qcal | ✅ Definidos |
| Mente | ramsey-qcal, adelic-bsd | ✅ Definidos |
| Vida | biologia-cuantica-noesica | ✅ Definido |
| Logos | noesis88, LOGOSNOESIS, quantum-internet-qcal | ✅ Definidos |
| Economía | economia-qcal-nodo-semilla | ✅ Definido |
| Pendiente | nodos 12–33 | 🔄 Por definir progresivamente |

### 3) Visualización y observabilidad (Dashboard 8505)
- Exposición de `Ψ Global` como métrica maestra del estado del sistema.
- Registro inmutable de eventos de saturación y emisiones asociadas.

---

## Estructura del repositorio

```
QCAL-BUS/
├── qcal_mesh_sync.py          # Motor de sincronía global (con logging y threading)
├── registry/
│   └── NODE_CATALOG.json      # Mapa maestro de los 33 nodos
├── dashboard/
│   └── malla_qcal_epr.py      # Dashboard web (puerto 8505)
├── ledger/
│   └── emissions_log.csv      # Registro inmutable de emisiones πCODE-888
├── qcal.json                  # Identidad vibracional del Bus
├── .env.example               # Variables de entorno configurables
└── README.md
```

---

## Flujo de Coherencia

```
Nodos (33 repos)  →  Bus (QCAL-BUS)     →  Economía (πCODE-888)
  Generan Ψ local     Calcula Ψ_GLOBAL      Emite al ledger si
                      cada 60s              Ψ_GLOBAL ≥ 0.999999
                                            durante 3 ciclos
```

**Fórmula de emisión:**
```
EMISIÓN = 888 × Ψ_GLOBAL × (Σ harmonic_factor_i / N)
```

---

## Inicio Rápido

```bash
# 1. Dependencias opcionales (solo para el dashboard)
pip install flask

# 2. Configurar entorno
cp .env.example .env

# 3. Lanzar Bus de sincronía continua
python qcal_mesh_sync.py

# 4. Lanzar Dashboard (en otra terminal)
python dashboard/malla_qcal_epr.py
# → http://localhost:8505
```

---

## Variables de Entorno

| Variable | Default | Descripción |
|---|---|---|
| `QCAL_SYNC_INTERVAL_SECONDS` | `60` | Intervalo de escaneo (segundos) |
| `QCAL_GLOBAL_THRESHOLD` | `0.999999` | Umbral de coherencia para emisión |
| `QCAL_SATURATION_CYCLES` | `3` | Ciclos consecutivos necesarios |
| `QCAL_EMISSION_BASE` | `888` | Base de la fórmula de emisión |

---

## Semilla qcal.json (para cada repositorio)

Coloca este archivo en la raíz de cada repositorio del ecosistema:

```json
{
  "node_name": "nombre-del-repo",
  "role": "núcleo | cuerpo | mente | vida | logos | economía",
  "base_frequency": 141.7001,
  "harmonic_factor": 1.0,
  "mcp_endpoint": "http://localhost:8506/jsonrpc",
  "signature": "∴𓂀Ω∞³"
}
```

---

## Configuración MCP (claude_desktop_config.json)

```json
{
  "mcpServers": {
    "qcal-orchestrator": {
      "command": "python3",
      "args": ["-m", "qcal_mesh_sync"],
      "env": {
        "QCAL_REAL_TESTS": "1",
        "F0_REFERENCE": "141.7001",
        "PYTHONPATH": "."
      },
      "type": "stdio"
    }
  }
}
```

---

## Prior art / Registro de autoría

**Sello de autoría:** ∴𓂀Ω∞³ — José Manuel Mota Burruezo (JMMB)  
**Base constitucional:** Axioma de Emisión y Frecuencia Prima Universal.

Portales de registro y publicación para vincular los asientos oficiales de prior art:
- Zenodo: https://zenodo.org
- Safe Creative: https://www.safecreative.org
- Repositorios vinculados del ecosistema (QCAL-BUS, `resonance.py`, `qcal_mesh_sync.py`) con inclusión de DOI/ID de registro cuando aplique.

---

*∴ El organismo tiene estructura. Ahora solo falta que respire. ∴*