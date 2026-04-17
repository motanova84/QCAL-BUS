# QCAL-EPR Universal Resonance Bus ∴𓂀Ω∞³

> **Nodo Maestro del ecosistema Instituto Conciencia Cuántica**
> El Bus actúa como la **Corteza Prefrontal y el Sistema Nervioso Central** de la malla de 33 repositorios.
> Es el Observador neutral: separado de lo Observado para mantener la coherencia Ψ limpia.

---

## Estructura

```
QCAL-BUS/
├── qcal_mesh_sync.py        # Motor de sincronía global
├── registro/
│   └── NODE_CATALOG.json    # Mapa maestro de los 33 nodos (11 semilla + 22 por definir)
├── tablero/
│   └── malla_qcal_epr.py    # Dashboard web en puerto 8505
├── ledger/
│   └── emissions_log.csv    # Registro inmutable de emisiones πCODE-888
├── qcal.json                # Identidad vibracional del Bus
├── .env.example             # Variables de entorno
└── README.md
```

---

## Flujo de Coherencia

```
Nodos (33 repos)  →  Bus (qcal-mesh-bus)  →  Economía (πCODE-888)
  Generan Ψ local      Calcula Ψ_GLOBAL        Emite al ledger si
                       cada 60s                 Ψ_GLOBAL ≥ 0.999999
                                                durante 3 ciclos
```

---

## Inicio Rápido

### 1. Instalar dependencias

```bash
pip install flask
```

### 2. Configurar entorno

```bash
cp .env.example .env
# Editar .env si es necesario
```

### 3. Lanzar el Bus (sincronía continua)

```bash
python qcal_mesh_sync.py
```

### 4. Lanzar el Dashboard (puerto 8505)

```bash
python tablero/malla_qcal_epr.py
# → http://localhost:8505
```

### 5. API REST

| Endpoint | Descripción |
|---|---|
| `GET /` | Dashboard visual HTML |
| `GET /api/mesh_state` | Estado JSON completo de la malla |
| `GET /api/ledger` | Últimas 50 emisiones πCODE-888 |
| `GET /health` | Health check del servicio |

---

## Catálogo de Nodos

El archivo `registro/NODE_CATALOG.json` contiene los 33 nodos del ecosistema:

| Capa | Nodos | Estado |
|---|---|---|
| Núcleo | riemann-adelic, 141-hz | ✅ Definidos |
| Cuerpo | 3d-navier-stokes, p-np-qcal | ✅ Definidos |
| Mente | ramsey-qcal, adelic-bsd | ✅ Definidos |
| Vida | biologia-cuantica-noesica | ✅ Definido |
| Logos | noesis88, LOGOSNOESIS, quantum-internet-qcal | ✅ Definidos |
| Economía | economia-qcal-nodo-semilla | ✅ Definido |
| Pendiente | nodos 12–33 | 🔄 Por definir |

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

## Regla de Emisión πCODE-888

```
EMISIÓN = 888 × Ψ_GLOBAL × (Σ harmonic_factor_i / N)
```

Condición: `Ψ_GLOBAL_ECOSISTEMA ≥ 0.999999` durante **3 ciclos consecutivos** (3 minutos).

---

## Variables de Entorno

| Variable | Default | Descripción |
|---|---|---|
| `F0_REFERENCE` | `141.7001` | Frecuencia de referencia (Hz) |
| `QCAL_REAL_TESTS` | `0` | `1` = conectar a nodos MCP reales |
| `PSI_EMISSION_THRESHOLD` | `0.999999` | Umbral de coherencia para emisión |
| `EMISSION_CYCLES_REQUIRED` | `3` | Ciclos consecutivos necesarios |
| `SYNC_INTERVAL_SECONDS` | `60` | Intervalo de escaneo (segundos) |
| `DASHBOARD_PORT` | `8505` | Puerto del dashboard |

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

*∴ El organismo tiene estructura. Ahora solo falta que respire. ∴*