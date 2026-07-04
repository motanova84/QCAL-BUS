# Guía de Configuración del Ambiente QCAL-BUS
## Environment Setup & Configuration Guide

**Última actualización:** 2026-07-04  
**Versión:** 1.0  
**Estado:** ✅ Operacional en Coherencia

---

## 📋 Tabla de Contenidos

1. [Quick Start](#quick-start)
2. [Desarrollo Local](#desarrollo-local)
3. [Producción Remota](#producción-remota)
4. [Testing con Nodos Reales](#testing-con-nodos-reales)
5. [Validación](#validación)
6. [Troubleshooting](#troubleshooting)
7. [Referencia de Variables](#referencia-de-variables)

---

## 🚀 Quick Start

### Para Desarrollo Inmediato (2 minutos)

```bash
# 1. Clonar y entrar al repo
git clone https://github.com/motanova84/QCAL-BUS.git
cd QCAL-BUS

# 2. Generar .env de desarrollo (automático)
python scripts/generate_env.py

# 3. Activar ambiente y ejecutar
python -m venv venv
source venv/bin/activate  # o en Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Ejecutar el monitor
python qcal_mesh_sync.py --loop

# 5. Abrir dashboard en otra terminal
python dashboard/malla_qcal_epr.py
# Acceder: http://localhost:5000
```

**¡Listo!** El ecosistema está funcionando en modo simulado.

---

## 🖥️ Desarrollo Local

### Configuración Completa

#### Paso 1: Crear archivo .env

```bash
cp .env.example .env
```

**O generar automáticamente:**

```bash
python scripts/generate_env.py
```

El script crea automáticamente:
- ✅ `QCAL_DEV_MODE=1` (Desarrollo)
- ✅ `QCAL_REAL_TESTS=0` (Modo simulado)
- ✅ URLs localhost (8506-8538)
- ✅ Todos los 33 nodos configurados

#### Paso 2: Verificar variables clave

```bash
# Verificar que el archivo fue creado
cat .env | grep "QCAL_DEV_MODE"  # Debe ser 1
cat .env | grep "QCAL_REAL_TESTS"  # Debe ser 0
cat .env | grep "QCAL_F0_HZ"  # Debe ser 141.7001
```

#### Paso 3: Instalar dependencias

```bash
# Crear ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar paquetes
pip install flask pytest
```

#### Paso 4: Ejecutar en modo desarrollo

```bash
# Terminal 1: Monitor central
python qcal_mesh_sync.py --loop

# Terminal 2 (nueva): Dashboard web
python dashboard/malla_qcal_epr.py

# Terminal 3 (nueva): Tests (opcional)
pytest tests/test_qcal_bus_extended.py -v
```

#### Paso 5: Acceder al dashboard

```
🌐 http://localhost:5000
```

**Esperado:**
- ✅ Ψ_GLOBAL entre 0.95 y 1.0
- ✅ 33 nodos visibles
- ✅ Modo: SIMULADO
- ✅ Entorno: DESARROLLO

---

## 🌍 Producción Remota

### Configuración para Servidor Remoto

#### Paso 1: Generar .env de producción

```bash
python scripts/generate_env.py --mode prod --domain tu-dominio.com
```

Esto crea `.env.production` con:
- ✅ `QCAL_DEV_MODE=0` (Producción)
- ✅ `QCAL_REAL_TESTS=1` (Modo real)
- ✅ URLs HTTPS (obligatorio)

#### Paso 2: Personalizar URLs

Editar `.env.production` y reemplazar URLs:

```bash
# Antes:
QCAL_NODE_RIEMANN_MCP_SERVER_URL=https://riemann-mcp-mcp.domain.com

# Después (tu dominio real):
QCAL_NODE_RIEMANN_MCP_SERVER_URL=https://riemann.tu-empresa.com

# Repetir para todos los 33 nodos
```

**Puntos clave:**
- ⚠️ **TODAS las URLs deben ser HTTPS**
- ⚠️ Certificados SSL válidos requeridos
- ⚠️ `QCAL_DEV_MODE=0` NO permite HTTP

#### Paso 3: Validar configuración

```bash
python scripts/generate_env.py --validate .env.production
```

**Salida esperada:**
```
✅ Validando .env.production...
  Modo desarrollo: ✗
  Modo tests real: ✓
  Nodos configurados: 33/33
✅ Validación exitosa!
```

#### Paso 4: Desplegar con gestor de procesos

**Opción A: systemd (Linux recomendado)**

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/qcal-bus.service
```

```ini
[Unit]
Description=QCAL-BUS Quantum Resonance System
After=network.target

[Service]
Type=simple
User=qcal
WorkingDirectory=/home/qcal/QCAL-BUS
EnvironmentFile=/home/qcal/QCAL-BUS/.env.production
ExecStart=/home/qcal/QCAL-BUS/venv/bin/python qcal_mesh_sync.py --loop
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Activar servicio
sudo systemctl daemon-reload
sudo systemctl enable qcal-bus
sudo systemctl start qcal-bus

# Verificar estado
sudo systemctl status qcal-bus
```

**Opción B: Docker**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV QCAL_DEV_MODE=0
ENV QCAL_REAL_TESTS=1

CMD ["python", "qcal_mesh_sync.py", "--loop"]
```

```bash
docker build -t qcal-bus .
docker run --env-file .env.production qcal-bus
```

#### Paso 5: Monitoreo

```bash
# Ver logs en tiempo real
sudo journalctl -u qcal-bus -f

# O con Docker:
docker logs -f <container_id>
```

---

## 🧪 Testing con Nodos Reales

### Configuración Híbrida (Desarrollo + Nodos Reales)

#### Paso 1: Generar .env.real

```bash
python scripts/generate_env.py --mode real --domain "nodos-reales.io"
```

#### Paso 2: Actualizar URLs de nodos reales

```bash
# Solo actualizar nodos que ya tienen endpoints reales
# Ejemplo: si NOESIS88 tiene servidor real

QCAL_NODE_NOESIS88_URL=https://noesis88-api.nodos-reales.io

# Dejar los demás en localhost para fallback a simulado
```

#### Paso 3: Ejecutar con testing real

```bash
export $(cat .env.real | xargs)
export QCAL_REAL_TESTS=1  # Activar modo real

python qcal_mesh_sync.py --loop
```

**Comportamiento esperado:**
- ✅ Intenta conectar a nodos reales
- ✅ Si falla → Fallback automático a simulado
- ✅ Logging visible de intentos y fallos

---

## ✅ Validación

### Script de Validación Automática

```bash
python scripts/generate_env.py --validate .env
```

### Checklist Manual

- [ ] `QCAL_DEV_MODE` es 0 (prod) o 1 (dev)
- [ ] `QCAL_REAL_TESTS` es 0 o 1
- [ ] `QCAL_F0_HZ` es 141.7001 (NUNCA cambiar)
- [ ] En PRODUCCIÓN: todas las URLs son HTTPS
- [ ] En DESARROLLO: URLs son http://localhost:*
- [ ] Exactamente 33 nodos QCAL_NODE_*_URL
- [ ] Puertos no conflictivos (8506-8538 para dev)
- [ ] Dashboard puerto: 5000

### Validación de Conectividad

```bash
# Probar conexión a un nodo (si QCAL_REAL_TESTS=1)
curl -s http://localhost:8506/api/resonance | python -m json.tool

# Esperado:
# {
#   "psi": 0.9756...,
#   "resonance": "RESONANCIA_MEDIA",
#   ...
# }
```

---

## 🔧 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```bash
pip install flask pytest
```

### Problema: "Address already in use" (Puerto 5000)

**Solución:**
```bash
# Opción A: Usar puerto diferente
export QCAL_DASHBOARD_PORT=5001
python dashboard/malla_qcal_epr.py

# Opción B: Encontrar proceso usando puerto
lsof -i :5000
kill -9 <PID>
```

### Problema: "URL no configurada" para nodo

**Causa:** Falta variable de entorno  
**Solución:**
```bash
# Verificar que el .env está cargado
cat .env | grep QCAL_NODE_

# O generar nuevamente
python scripts/generate_env.py
```

### Problema: "La URL del nodo debe usar HTTPS"

**Causa:** En PRODUCCIÓN, URL es http://  
**Solución:**
```bash
# En .env.production, cambiar:
# De: http://nodo.com
# A:  https://nodo.com

# Verificar modo:
grep QCAL_DEV_MODE .env.production  # Debe ser 0
```

### Problema: Dashboard muestra "Error: Timeout"

**Causa:** Nodo no responde en 5 segundos  
**Solución:**
```bash
# Verificar nodo está activo (si QCAL_REAL_TESTS=1)
curl -I http://localhost:8506/api/resonance

# En desarrollo (SIMULADO): ignorar error, es esperado
# En producción: revisar que nodos estén funcionando
```

### Problema: Solo 32 nodos en vez de 33

**Causa:** Un nodo no está configurado  
**Solución:**
```bash
# Regenerar .env
python scripts/generate_env.py

# O verificar .env.example tiene todos:
grep "QCAL_NODE_" .env.example | wc -l  # Debe ser 33
```

---

## 📖 Referencia de Variables

### Variables Obligatorias

| Variable | Rango | Prod | Dev | Notas |
|----------|-------|------|-----|-------|
| `QCAL_DEV_MODE` | 0/1 | 0 | 1 | Modo operación |
| `QCAL_REAL_TESTS` | 0/1 | 1 | 0 | Conectar nodos |
| `QCAL_F0_HZ` | float | 141.7001 | 141.7001 | ⚠️ NO CAMBIAR |
| `QCAL_SYNC_INTERVAL_SECONDS` | int | 60 | 60 | Intervalo monitoreo |
| `QCAL_GLOBAL_THRESHOLD` | 0-1 | 0.999999 | 0.999999 | ⚠️ NO CAMBIAR |

### Variables Opcionales

| Variable | Default | Notas |
|----------|---------|-------|
| `QCAL_SATURATION_CYCLES` | 3 | Ciclos para emisión |
| `QCAL_EMISSION_BASE` | 888 | Cantidad πCODE-888 |
| `QCAL_LEDGER_TAIL` | 50 | Registros en API |
| `QCAL_DASHBOARD_PORT` | 5000 | Puerto web |

### Variables de Nodos (33 totales)

```
QCAL_NODE_<MCP_ID_EN_MAYUSCULAS>_URL
```

**Ejemplo de conversión:**
- `mcp_id`: `riemann-mcp-server`
- `env_var`: `QCAL_NODE_RIEMANN_MCP_SERVER_URL`

**Todos los nodos:**

```
QCAL_NODE_RIEMANN_MCP_SERVER_URL
QCAL_NODE_141_HZ_URL
QCAL_NODE_NAVIER_MCP_SERVER_URL
QCAL_NODE_P_NP_MCP_SERVER_URL
QCAL_NODE_RAMSEY_QCAL_URL
QCAL_NODE_BSD_MCP_SERVER_URL
QCAL_NODE_BIOLOGIA_CUANTICA_NOESICA_URL
QCAL_NODE_NOESIS88_URL
QCAL_NODE_LOGOSNOESIS_URL
QCAL_NODE_QUANTUM_INTERNET_QCAL_URL
QCAL_NODE_NODO_SEMILLA_V1_URL
QCAL_NODE_ECONOMIA_REGENERATIVA_URL
QCAL_NODE_PI_CODE_888_URL
QCAL_NODE_ESPIRITU_QCAL_URL
QCAL_NODE_AKASHA_QCAL_URL
QCAL_NODE_CONCIENCIA_COSMICA_URL
QCAL_NODE_SOMBRA_COLECTIVA_URL
QCAL_NODE_TRAUMA_QUANTICO_URL
QCAL_NODE_INTEGRACION_SOMBRA_URL
QCAL_NODE_CAMPO_MORFOGENICO_URL
QCAL_NODE_ENTRELAZAMIENTO_EPR_URL
QCAL_NODE_TIEMPO_NO_LINEAL_URL
QCAL_NODE_MEMORIA_CUANTICA_URL
QCAL_NODE_GEOMETRIA_SAGRADA_URL
QCAL_NODE_FLOR_DE_VIDA_URL
QCAL_NODE_TORUS_QCAL_URL
QCAL_NODE_SANACION_CUANTICA_URL
QCAL_NODE_ADN_REPARACION_URL
QCAL_NODE_COHERENCIA_CARDIACA_URL
QCAL_NODE_LENGUAJE_QCAL_URL
QCAL_NODE_SIMBOLOS_NOESICOS_URL
QCAL_NODE_RED_NEURONAL_CUANTICA_URL
QCAL_NODE_INTUICION_COLECTIVA_URL
```

---

## 🎯 Resumen Rápido

### Desarrollo
```bash
# Auto-setup (recomendado)
python scripts/generate_env.py
python qcal_mesh_sync.py --loop
python dashboard/malla_qcal_epr.py
# Abierto en: http://localhost:5000
```

### Validación
```bash
python scripts/generate_env.py --validate .env
```

### Producción
```bash
python scripts/generate_env.py --mode prod --domain tu-dominio.com
# Editar .env.production con URLs reales
python scripts/generate_env.py --validate .env.production
# Desplegar con systemd o Docker
```

---

## 📞 Soporte

- **Issues:** GitHub Issues
- **Documentación:** Ver `/docs`
- **Tests:** `pytest tests/ -v`
- **Logs:** Dashboard en tiempo real

---

**Creado con ❤️ en coherencia 141.7001 Hz**

∞³ El puente se crea al pisar
