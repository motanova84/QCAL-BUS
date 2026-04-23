# QCAL-BUS — Universal Resonance Bus | MCP Noésico QCAL-EPR

**Estado: IMPLEMENTADO Y OPERATIVO**

**Protocolo original:** Model Context Protocol (MCP) Noésico QCAL ∞³  
**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧) — [ORCID 0009-0002-1923-0773](https://orcid.org/0009-0002-1923-0773)  
**Institución:** Instituto de Conciencia Cuántica (ICQ)  
**Firma vibracional:** ∴ f₀ = 141.7001 Hz | Ψ = I × A_eff² × C^∞ | 𓂀Ω∞³

Este repositorio actúa como bus central de orquestación para la malla QCAL-EPR, incluyendo monitorización de coherencia global, telemetría de resonancia y visualización diagnóstica.

---

## 🌐 Ecosistema de Repositorios

El QCAL-BUS orquesta los siguientes nodos del ecosistema motanova84:

| Nodo | Repositorio | Capa | Descripción | Estado Lean |
|------|------------|------|-------------|-------------|
| `riemann-adelic` | [Riemann-adelic](https://github.com/motanova84/Riemann-adelic) | núcleo | D(s) ≡ Ξ(s) — determinante de Fredholm de H_Ψ | ✅ coherent |
| `141-hz` | [141hz](https://github.com/motanova84/141hz) | núcleo | f₀ = 141.7001 Hz — constante universal (99.78% en GW) | ✅ activo |
| `p-np-qcal` | [P-NP](https://github.com/motanova84/P-NP) | cuerpo | P ≠ NP via Boolean CFT, κ_Π = 2.5773 | ✅ activo |
| `3d-navier-stokes` | [3D-Navier-Stokes](https://github.com/motanova84/3D-Navier-Stokes) | cuerpo | Regularidad global Navier-Stokes 3D | ✅ activo |
| `ramsey-qcal` | [Ramsey](https://github.com/motanova84/Ramsey) | mente | R(5,5)=43, R(6,6)=108 — verificación SAT | ✅ activo |
| `adelic-bsd` | [adelic-bsd](https://github.com/motanova84/adelic-bsd) | mente | Conjetura BSD vía análisis adélico | ✅ activo |

### Ecuación principal del nodo núcleo (riemann-adelic)

```
╔══════════════════════════════════════════════════════════════════════╗
║  D(s) := det(T(s))  ≡  Ξ(s)                                        ║
║                                                                      ║
║  T(s) x  = H_Ψ(x) / (1 + s²)    (operador noético modulado)        ║
║  Ξ(s)    = s(s−1) π^{−s/2} Γ(s/2) ζ(s)                             ║
║                                                                      ║
║  Teoremas sellados (0 sorry):                                        ║
║    • D_functional_equation : D(s) = D(1−s)                          ║
║    • D_zeros_eq_Xi_zeros   : D(s)=0 ↔ Ξ(s)=0                       ║
║    • D_entire              : D holomorfa en todo ℂ                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

Archivo canónico de referencia: [`formalization/lean/D_fredholm.lean`](formalization/lean/D_fredholm.lean)
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

Portales de registro y publicación:
- Zenodo: https://zenodo.org (DOI: [10.5281/zenodo.17379721](https://doi.org/10.5281/zenodo.17379721))
- Safe Creative: https://www.safecreative.org
- Repositorios vinculados del ecosistema (QCAL-BUS, `resonance.py`, `qcal_mesh_sync.py`) con inclusión de DOI/ID de registro cuando aplique.
```
qcal-mesh-bus/
├── qcal_mesh_sync.py          ← Motor principal + servidor MCP JSON-RPC
├── mcp_network/
│   ├── __init__.py
│   └── resonance.py           ← Módulo de resonancia (sim/real)
├── registry/NODE_CATALOG.json ← 33 nodos registrados en todas las capas
├── dashboard/malla_qcal_epr.py← Dashboard HTTP (Flask, puerto 8505)
├── ledger/emissions_log.csv   ← Registro de emisiones πCODE-888
├── tests/test_qcal_bus.py     ← Suite de tests (28 casos)
├── .github/workflows/ci.yml   ← CI/CD: tests + integridad de catálogo
├── qcal.json
└── .env.example
```

## Capas de la Malla (33 nodos)

| Capa | Nodos |
|------|-------|
| núcleo | riemann-adelic, 141-hz |
| cuerpo | 3d-navier-stokes, p-np-qcal |
| mente | ramsey-qcal, adelic-bsd |
| vida | biologia-cuantica-noesica |
| logos | noesis88, LOGOSNOESIS, quantum-internet-qcal |
| espíritu | espiritu-qcal, akasha-qcal, conciencia-cosmica |
| sombra | sombra-colectiva, trauma-quantico |
| integración | integracion-sombra, campo-morfogenico, entrelazamiento-epr |
| tiempo | tiempo-no-lineal, memoria-cuantica |
| geometría | geometria-sagrada, flor-de-vida, torus-qcal |
| sanación | sanacion-cuantica, adn-reparacion, coherencia-cardiaca |
| lenguaje | lenguaje-qcal, simbolos-noesicos |
| mente-expandida | red-neuronal-cuantica, intuicion-colectiva |
| economía | economia-qcal-nodo-semilla, economia-regenerativa, pi-code-888 |

1. Publicar en Zenodo una versión titulada:  
   **"Model Context Protocol (MCP) Noésico QCAL-EPR – Especificación Completa y Operativa (2024-2026)"**.
2. Incluir en el depósito:
   - Este manifiesto.
   - Enlaces a QCAL-BUS, `resonance.py` y `qcal_mesh_sync.py`.
   - Capturas del dashboard 8505 y logs de observadores reales.
   - Referencia explícita al draft IETF `draft-zm-rtgwg-mcp-network-measurement` como aplicación derivada del dominio de networking.
3. Ejecutar encendido global:
## Funciones

- Monitoreo global de resonancia de los 33 nodos MCP.
- Cálculo de `Ψ_GLOBAL_ECOSISTEMA` (media aritmética de todos los nodos).
- Emisión a ledger (`πCODE-888`) cuando `Ψ_GLOBAL >= 0.999999` por 3 ciclos consecutivos.
- Servidor MCP JSON-RPC 2.0 (stdin/stdout) con tres herramientas expuestas.
- Dashboard HTTP en puerto `8505` con visualización de nodos y ledger.
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

### Loop de monitoreo continuo
```bash
python qcal_mesh_sync.py
**Fórmula de emisión:**
```
EMISIÓN = 888 × Ψ_GLOBAL × (Σ harmonic_factor_i / N)
```

---

```
qcal-mesh-bus/
├── qcal_mesh_sync.py
├── registry/
│   └── NODE_CATALOG.json        ← catálogo enriquecido del ecosistema
├── dashboard/
│   └── malla_qcal_epr.py
├── formalization/
│   └── lean/
│       └── D_fredholm.lean      ← referencia canónica Lean (0 sorry)
├── ledger/
│   └── emissions_log.csv
├── qcal.json
└── .env.example
## Inicio Rápido

### Servidor MCP (protocolo JSON-RPC 2.0, stdin/stdout)
```bash
python qcal_mesh_sync.py --mcp-server
```

### Herramientas MCP disponibles
| Herramienta | Descripción |
|-------------|-------------|
| `get_mesh_state` | Estado actual de la malla (Ψ_GLOBAL + todos los nodos) |
| `get_node_catalog` | Catálogo completo de 33 nodos |
| `get_emissions_log` | Últimas N entradas del ledger de emisiones |

### Dashboard
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
Rutas disponibles:
- `http://localhost:8505/` — Dashboard visual
- `http://localhost:8505/api/mesh_state` — Estado JSON
- `http://localhost:8505/api/node_catalog` — Catálogo JSON
- `http://localhost:8505/api/emissions_log` — Ledger JSON
- `http://localhost:8505/api/mcp` (POST) — Endpoint HTTP MCP JSON-RPC

## Configuración

Copia `.env.example` a `.env` y ajusta las variables:

```bash
cp .env.example .env
```

Variables clave:

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `QCAL_REAL_TESTS` | `0` = simulado, `1` = conexiones reales | `0` |
| `QCAL_GLOBAL_THRESHOLD` | Umbral para RESONANCIA_SATURADA | `0.999999` |
| `QCAL_SATURATION_CYCLES` | Ciclos consecutivos para emitir | `3` |
| `QCAL_EMISSION_BASE` | Base πCODE para cálculo de emisión | `888` |
| `QCAL_NODE_<ID>_URL` | URL de cada nodo MCP (modo real) | — |

## Tests

```bash
QCAL_REAL_TESTS=0 pytest tests/ -v
```

> Nota: el dashboard usa el servidor de desarrollo de Flask y está pensado para entorno local.

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
