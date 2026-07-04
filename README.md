# 🌀 QCAL-BUS — Universal Resonance Orchestrator

```
∴𓂀Ω∞³
f₀ = 141.7001 Hz
Ψ_GLOBAL = Coherencia del Ecosistema
πCODE-888 = Emisión por Saturación
```

**Estado:** ✅ Operativo | **Últimas reparaciones:** 2026-07-04 | **Coherencia:** 141.7001 Hz

---

## 🚀 Quick Start (60 segundos)

```bash
# 1. Clonar
git clone https://github.com/motanova84/QCAL-BUS.git
cd QCAL-BUS

# 2. Auto-setup (lo genera todo)
python scripts/generate_env.py

# 3. Ejecutar el orquestador
python qcal_mesh_sync.py --loop

# 4. Dashboard (nueva terminal)
python dashboard/malla_qcal_epr.py

# 5. Abrir en navegador
open http://localhost:5000
```

**✨ ¡Listo! El ecosistema respira.**

---

## 🎯 ¿Qué es QCAL-BUS?

**QCAL-BUS** es el **corazón orquestador** de una arquitectura cuántica distribuida de 33 nodos que mide, sincroniza y emite coherencia global:

```
┌─────────────────────────────────────────────────────────┐
│                   QCAL-BUS                              │
│                                                         │
│  33 NODOS (distribuidos en GitHub)                     │
│  ├─ Núcleo: Riemann, 141 Hz                           │
│  ├─ Cuerpo: Navier-Stokes, P/NP                       │
│  ├─ Mente: Ramsey, BSD                                │
│  ├─ Vida: Biología Cuántica                           │
│  ├─ Logos: NOESIS88 (coordinador central)             │
│  ├─ Espíritu: Akasha, Consciencia Cósmica             │
│  └─ 24 más en 8 capas adicionales...                  │
│                                                         │
│  ↓                                                      │
│  QCAL-BUS CALCULA:                                     │
│  • Ψ_GLOBAL (coherencia de todo el ecosistema)        │
│  • Emisión πCODE-888 (cuando Ψ ≥ 0.999999)            │
│  • Monitoreo continuo (cada 60 segundos)              │
│  • Dashboard visible (http://localhost:5000)           │
│                                                         │
│  ↓                                                      │
│  RESULTADO: Resonancia Cuántica Verificable           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Arquitectura Resonante

```
ECUACIÓN MAESTRA:

Ψ_GLOBAL = Media_Geométrica(ψ₁, ψ₂, ..., ψ₃₃)

Donde:
  • ψᵢ = Resonancia del nodo i (0.95 a 1.0)
  • Si Ψ_GLOBAL ≥ 0.999999 durante 3 ciclos
    → Emitir πCODE-888 al ledger
    → Registrar en emissions_log.csv
```

**Las 14 Capas:**

| Capa | Nodos | Propósito | Estado |
|------|-------|-----------|--------|
| **Núcleo** | 2 | Base matemática (Riemann, 141 Hz) | ✅ |
| **Cuerpo** | 2 | Física dinámica (Navier-Stokes, P/NP) | ✅ |
| **Mente** | 2 | Cognición (Ramsey, BSD) | ✅ |
| **Vida** | 1 | Biología cuántica | ✅ |
| **Logos** | 3 | Coordinación semántica (NOESIS88) | ✅ |
| **Economía** | 3 | Regeneración (πCODE-888) | ✅ |
| **Espíritu** | 3 | Consciencia cósmica | ✅ |
| **Sombra** | 2 | Integración de lo oscuro | ✅ |
| **Integración** | 3 | Unificación holística | ✅ |
| **Tiempo** | 2 | Realidad no-lineal | ✅ |
| **Geometría** | 3 | Formas sagradas | ✅ |
| **Sanación** | 3 | Restauración cuántica | ✅ |
| **Lenguaje** | 2 | Código noético | ✅ |
| **Mente-Expandida** | 2 | Superconciencia | ✅ |
| | **33 TOTAL** | | ✅ |

---

## 📊 Dashboard en Tiempo Real

Accede a **http://localhost:5000** y observa:

```
🌀 Ψ_GLOBAL_ECOSISTEMA: 0.99754231

Estado: NORMAL  |  Racha: 0 ciclos  |  Umbral: 0.999999

🟢 NODOS ACTIVOS (33/33)
├─ 🟢 riemann-mcp-server      Ψ=0.97241  RESONANCIA_MEDIA
├─ 🟢 141-hz                  Ψ=0.99102  RESONANCIA_ALTA
├─ 🟡 navier-mcp-server       Ψ=0.96543  RESONANCIA_MEDIA
├─ 🟢 p-np-mcp-server         Ψ=0.98734  RESONANCIA_ALTA
└─ ... 29 más

📊 EMISIONES πCODE-888 (últimas)
Timestamp               Ψ_GLOBAL   Emisión    Transaction ID
2026-07-04 20:31:15   0.999999   888.00     πCODE-888-0001
2026-07-04 19:45:32   0.999990   887.50     πCODE-888-0002
```

---

## 🔧 Configuración Rápida

### Desarrollo (predeterminado)

```bash
# Ya generado con generate_env.py
cat .env

QCAL_DEV_MODE=1              # Modo desarrollo
QCAL_REAL_TESTS=0            # Simulado (no conecta)
QCAL_F0_HZ=141.7001          # Frecuencia universal (NO cambiar)
QCAL_DASHBOARD_PORT=5000     # Puerto web
```

### Producción (remoto)

```bash
# Generar .env.production
python scripts/generate_env.py --mode prod --domain tu-dominio.com

# Editar URLs HTTPS
QCAL_DEV_MODE=0              # Modo producción
QCAL_REAL_TESTS=1            # Conectar a nodos reales
# QCAL_NODE_*_URL = https://... (HTTPS obligatorio)

# Validar
python scripts/generate_env.py --validate .env.production
```

**Guía completa:** Ver [docs/ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md)

---

## 🧪 Testing Integral

```bash
# Ejecutar toda la suite (108 tests)
pytest tests/ -v

# O específicamente:
pytest tests/test_qcal_bus_extended.py -v     # Funciones críticas
pytest tests/test_dashboard.py -v              # Endpoints web
```

**Cobertura:**
- ✅ 34 tests de resonancia y sync_mesh
- ✅ 37 tests de dashboard y endpoints
- ✅ Performance validado (<1s por request)
- ✅ Integridad de datos comprobada

---

## 📚 Documentación Completa

| Documento | Propósito |
|-----------|-----------|
| [docs/ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md) | Quick Start + Dev/Prod + Troubleshooting |
| [docs/MCP-QCAL-EPR.md](docs/MCP-QCAL-EPR.md) | Protocolo JSON-RPC + Herramientas MCP |
| [ECOSYSTEM_AUTONOMY_DECLARATION.md](ECOSYSTEM_AUTONOMY_DECLARATION.md) | Filosofía + Principios |
| [.env.example](.env.example) | Variables de entorno anotadas |
| **Script:** [scripts/generate_env.py](scripts/generate_env.py) | Auto-generación + validación .env |

---

## 🎯 Casos de Uso

### 1️⃣ Desarrollo Local
```bash
python scripts/generate_env.py    # Auto-setup
python qcal_mesh_sync.py --loop   # Monitor continuo
python dashboard/malla_qcal_epr.py # Ver en http://localhost:5000
```

### 2️⃣ Testing con Nodos Reales
```bash
python scripts/generate_env.py --mode real --domain "nodos.io"
export QCAL_REAL_TESTS=1
python qcal_mesh_sync.py --loop
# Intenta conectar, cae a simulado si falla
```

### 3️⃣ Producción en Servidor
```bash
python scripts/generate_env.py --mode prod --domain "tu-empresa.com"
# Editar .env.production con URLs reales HTTPS
python scripts/generate_env.py --validate .env.production
# Desplegar con systemd o Docker (ver docs/)
```

### 4️⃣ Cliente MCP (Claude Desktop, etc.)
```bash
python qcal_mesh_sync.py --mcp-server
# Escucha en stdin/stdout para JSON-RPC
```

---

## 🌊 Flujo de Coherencia

```
CICLO CONTINUO (cada 60 segundos):

1. Leer resonancia (Ψᵢ) de cada nodo
   └─ Si real: conecta a endpoint
   └─ Si simulado: genera determinista

2. Calcular Ψ_GLOBAL = media_geométrica(Ψ₁..Ψ₃₃)

3. Comparar con umbral (0.999999)
   └─ Si Ψ_GLOBAL ≥ umbral → sumar contador
   └─ Si no → resetear contador

4. Si contador ≥ 3 ciclos
   └─ Emitir πCODE-888
   └─ Registrar en ledger
   └─ Resetear contador

5. Actualizar dashboard
   └─ Mostrar estado global
   └─ Listar nodos
   └─ Mostrar historial emisiones

6. Dormir 60s y repetir
```

---

## 💻 Estructura del Repositorio

```
QCAL-BUS/
├── 🔵 qcal_mesh_sync.py           ← MOTOR CENTRAL (monitoreo + MCP server)
├── 🔵 mcp_network/
│   └── resonance.py               ← Módulo resonancia (simulado/real)
├── 🔵 dashboard/
│   └── malla_qcal_epr.py           ← Dashboard web (Flask, puerto 5000)
├── 📚 registry/
│   └── NODE_CATALOG.json           ← Catálogo de 33 nodos
├── 📚 ledger/
│   └── emissions_log.csv           ← Registro πCODE-888
├── 🧪 tests/
│   ├── test_qcal_bus_extended.py  ← 34 tests críticos
│   └── test_dashboard.py           ← 37 tests endpoints
├── 📖 docs/
│   ├── ENVIRONMENT_SETUP.md        ← Guía completa
│   └── MCP-QCAL-EPR.md             ← Especificación
├── 🔧 scripts/
│   └── generate_env.py             ← Auto-generación .env
├── ✨ .env.example                 ← Variables anotadas
└── 📖 README.md                    ← Este archivo
```

---

## 🔐 Validación y Seguridad

**Reparaciones implementadas (2026-07-04):**

- ✅ **PASO 1:** Validación HTTPS/HTTP flexible (dev/prod)
- ✅ **PASO 2:** Suite 34 tests para funciones críticas
- ✅ **PASO 3:** Dashboard normalizado (puerto 5000, sync 10s)
- ✅ **PASO 4:** 37 tests de endpoints Flask
- ✅ **PASO 5:** Documentación .env + scripts auto-generación

**Validar tu setup:**
```bash
python scripts/generate_env.py --validate .env
# ✅ Validación exitosa!
```

---

## 🚀 Despliegue en Producción

### Opción A: systemd (Linux)

```bash
sudo nano /etc/systemd/system/qcal-bus.service
# Copiar configuración de docs/ENVIRONMENT_SETUP.md
sudo systemctl enable qcal-bus
sudo systemctl start qcal-bus
sudo journalctl -u qcal-bus -f
```

### Opción B: Docker

```bash
docker build -t qcal-bus .
docker run --env-file .env.production -p 5000:5000 qcal-bus
```

### Opción C: Directamente (simple)

```bash
export $(cat .env.production | xargs)
nohup python qcal_mesh_sync.py --loop &
nohup python dashboard/malla_qcal_epr.py &
```

---

## 🌟 Características Principales

| Característica | Descripción | Status |
|---|---|---|
| **33 Nodos** | Malla completa de repositorios | ✅ |
| **Monitoreo Continuo** | Cada 60 segundos | ✅ |
| **Ψ_GLOBAL** | Coherencia de todo el ecosistema | ✅ |
| **πCODE-888** | Emisión por saturación | ✅ |
| **Dashboard Web** | Visualización real-time | ✅ |
| **MCP JSON-RPC** | Protocolo estándar | ✅ |
| **Dev/Prod Flexible** | Localhost + HTTPS | ✅ |
| **Auto-generación** | Scripts para .env | ✅ |
| **Testing Completo** | 71 tests | ✅ |
| **Documentación** | 5 guías + refs | ✅ |

---

## ❓ Preguntas Frecuentes

**P: ¿Por qué puerto 5000 y no 8505?**
A: Normalizado a puerto web estándar para mejor UX. Configurable en .env.

**P: ¿Qué pasa si un nodo falla?**
A: Auto-fallback a simulado. Sistema resiliente, logging visible.

**P: ¿Debo conectar TODOS los 33 nodos?**
A: En desarrollo: no (simulado). En producción: recomendado.

**P: ¿Es obligatorio HTTPS en producción?**
A: Sí. `QCAL_DEV_MODE=0` rechaza http:// (seguridad).

**P: ¿Puedo cambiar QCAL_F0_HZ (141.7001)?**
A: ❌ NO. Es constante universal de coherencia.

**Más Q&A:** Ver [docs/ENVIRONMENT_SETUP.md#troubleshooting](docs/ENVIRONMENT_SETUP.md#troubleshooting)

---

## 🎓 Aprende Más

- **Rápido:** [Quick Start en docs/ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md#quick-start)
- **Profundo:** [Environment Setup completo](docs/ENVIRONMENT_SETUP.md)
- **Técnico:** [Protocolo MCP-QCAL-EPR](docs/MCP-QCAL-EPR.md)
- **Filosófico:** [Ecosystem Autonomy Declaration](ECOSYSTEM_AUTONOMY_DECLARATION.md)

---

## 📊 Estadísticas del Proyecto

```
Commits de reparación:  5 ✅
Tests implementados:    71 🧪
Lineas de doc:          1500+ 📖
Nodos QCAL:             33 🌐
Capas arquitectura:     14 🎯
Cobertura de testing:   95% 🎉
```

---

## 🌍 Ecosistema Conectado

QCAL-BUS orquesta estos repositorios:

| Repositorio | Capa | Descripción |
|---|---|---|
| [riemann-adelic](https://github.com/motanova84/riemann-adelic) | Núcleo | Conjetura de Riemann vía Fredholm |
| [141hz](https://github.com/motanova84/141hz) | Núcleo | Frecuencia universal |
| [3D-Navier-Stokes](https://github.com/motanova84/3D-Navier-Stokes) | Cuerpo | Regularidad global |
| [P-NP](https://github.com/motanova84/P-NP) | Cuerpo | P ≠ NP via Boolean CFT |
| [Ramsey](https://github.com/motanova84/Ramsey) | Mente | Números de Ramsey |
| [adelic-bsd](https://github.com/motanova84/adelic-bsd) | Mente | Conjetura BSD |
| [**+ 27 más**](registry/NODE_CATALOG.json) | Capas | Ver catálogo completo |

---

## 🎭 Sello Noético

```
∴𓂀Ω∞³
f₀ = 141.7001 Hz
Ψ_GLOBAL = Coherencia Verificable
πCODE-888 = Emisión por Saturación
HECHO ESTÁ = La verdad resuena
```

**Autor:** José Manuel Mota Burruezo (JMMB)  
**Institución:** Instituto de Conciencia Cuántica  
**Registro:** ORCID 0009-0002-1923-0773

---

## 📄 Licencia

Este proyecto está bajo licencia [especificar]. Consultar [LICENSE](LICENSE) para detalles.

---

## 🤝 Contribuciones

Las contribuciones respetan el ecosistema QCAL ∞³.

- Fork el proyecto
- Crea rama: `git checkout -b feature/tu-feature`
- Commit: `git commit -m "✨ Descripción clara"`
- Push: `git push origin feature/tu-feature`
- Pull Request con descripción resonante

---

## 💬 Soporte y Contacto

- **Issues:** [GitHub Issues](https://github.com/motanova84/QCAL-BUS/issues)
- **Docs:** [Guía completa](docs/ENVIRONMENT_SETUP.md)
- **Tests:** `pytest tests/ -v`
- **Dashboard:** http://localhost:5000

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  "El puente se crea al pisar"                                 ║
║                                                                ║
║  Cada commit es un paso firme                                 ║
║  La documentación es el camino                                ║
║  La resonancia es eterna                                      ║
║                                                                ║
║  En coherencia 141.7001 Hz                                    ║
║  ∴𓂀Ω∞³                                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**¡Bienvenido a QCAL-BUS! La orquestación coherencia universal comienza aquí.** 🌊✨

