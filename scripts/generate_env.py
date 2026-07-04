#!/usr/bin/env python3
"""
QCAL-BUS Environment Generator
==============================

Script para generar y validar archivos .env automáticamente.

Uso:
  python scripts/generate_env.py                    # Generar .env de desarrollo
  python scripts/generate_env.py --mode prod       # Generar .env de producción
  python scripts/generate_env.py --validate .env   # Validar .env existente
  python scripts/generate_env.py --help            # Ver todas las opciones

Características:
  ✅ Auto-generación de .env
  ✅ Conversión automática de mcp_id → env_key
  ✅ Validación de variables
  ✅ Detección automática de contexto (dev/prod)
  ✅ Seguridad: verifica HTTPS en producción
"""

import argparse
import json
import os
import sys
from pathlib import Path


# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE NODOS
# ═════════════════════════════════════════════════════════════════════════════

QCAL_NODES = {
    # Capa: núcleo
    "riemann-mcp-server": {"layer": "núcleo", "port": 8506},
    "141-hz": {"layer": "núcleo", "port": 8507},
    
    # Capa: cuerpo
    "navier-mcp-server": {"layer": "cuerpo", "port": 8508},
    "p-np-mcp-server": {"layer": "cuerpo", "port": 8509},
    
    # Capa: mente
    "ramsey-qcal": {"layer": "mente", "port": 8510},
    "bsd-mcp-server": {"layer": "mente", "port": 8511},
    
    # Capa: vida
    "biologia-cuantica-noesica": {"layer": "vida", "port": 8512},
    
    # Capa: logos
    "noesis88": {"layer": "logos", "port": 8513},
    "logosnoesis": {"layer": "logos", "port": 8514},
    "quantum-internet-qcal": {"layer": "logos", "port": 8515},
    
    # Capa: economía
    "nodo-semilla-v1": {"layer": "economía", "port": 8516},
    "economia-regenerativa": {"layer": "economía", "port": 8517},
    "pi-code-888": {"layer": "economía", "port": 8518},
    
    # Capa: espíritu
    "espiritu-qcal": {"layer": "espíritu", "port": 8519},
    "akasha-qcal": {"layer": "espíritu", "port": 8520},
    "conciencia-cosmica": {"layer": "espíritu", "port": 8521},
    
    # Capa: sombra
    "sombra-colectiva": {"layer": "sombra", "port": 8522},
    "trauma-quantico": {"layer": "sombra", "port": 8523},
    
    # Capa: integración
    "integracion-sombra": {"layer": "integración", "port": 8524},
    "campo-morfogenico": {"layer": "integración", "port": 8525},
    "entrelazamiento-epr": {"layer": "integración", "port": 8526},
    
    # Capa: tiempo
    "tiempo-no-lineal": {"layer": "tiempo", "port": 8527},
    "memoria-cuantica": {"layer": "tiempo", "port": 8528},
    
    # Capa: geometría
    "geometria-sagrada": {"layer": "geometría", "port": 8529},
    "flor-de-vida": {"layer": "geometría", "port": 8530},
    "torus-qcal": {"layer": "geometría", "port": 8531},
    
    # Capa: sanación
    "sanacion-cuantica": {"layer": "sanación", "port": 8532},
    "adn-reparacion": {"layer": "sanación", "port": 8533},
    "coherencia-cardiaca": {"layer": "sanación", "port": 8534},
    
    # Capa: lenguaje
    "lenguaje-qcal": {"layer": "lenguaje", "port": 8535},
    "simbolos-noesicos": {"layer": "lenguaje", "port": 8536},
    
    # Capa: mente-expandida
    "red-neuronal-cuantica": {"layer": "mente-expandida", "port": 8537},
    "intuicion-colectiva": {"layer": "mente-expandida", "port": 8538},
}


# ═════════════════════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═════════════════════════════════════════════════════════════════════════════

def mcp_id_to_env_key(mcp_id: str) -> str:
    """Convierte mcp_id a clave de variable de entorno segura."""
    return "QCAL_NODE_" + mcp_id.upper().replace("-", "_") + "_URL"


def env_key_to_mcp_id(env_key: str) -> str:
    """Convierte clave de variable de entorno a mcp_id."""
    # Remove QCAL_NODE_ prefix and _URL suffix
    s = env_key.replace("QCAL_NODE_", "").replace("_URL", "")
    # Reemplazar _ con - (excepto en límites)
    return s.lower().replace("_", "-")


def get_env_path(mode: str = "dev") -> Path:
    """Retorna la ruta del archivo .env según el modo."""
    if mode == "prod":
        return Path(".env.production")
    elif mode == "real":
        return Path(".env.real")
    else:
        return Path(".env")


def generate_env_content(mode: str = "dev", domain: str = "domain.com") -> str:
    """Genera el contenido completo del archivo .env."""
    
    is_prod = mode == "prod"
    protocol = "https" if is_prod else "http"
    
    lines = [
        "# QCAL-BUS Environment Configuration - Auto-generated",
        f"# Modo: {'PRODUCCIÓN' if is_prod else 'DESARROLLO'}",
        "# " + "=" * 76,
        "",
        "# ─ CONFIGURACIÓN CENTRAL ─────────────────────────────────────",
        "QCAL_SYNC_INTERVAL_SECONDS=60",
        "QCAL_GLOBAL_THRESHOLD=0.999999",
        "QCAL_SATURATION_CYCLES=3",
        "QCAL_EMISSION_BASE=888",
        "QCAL_LEDGER_TAIL=50",
        "",
        "# ─ MODOS DE OPERACIÓN ────────────────────────────────────────",
        f"QCAL_REAL_TESTS={1 if is_prod else 0}",
        f"QCAL_DEV_MODE={0 if is_prod else 1}",
        "",
        "# ─ FRECUENCIA DE REFERENCIA ──────────────────────────────────",
        "QCAL_F0_HZ=141.7001",
        "",
        "# ─ PUERTO DEL DASHBOARD ──────────────────────────────────────",
        "QCAL_DASHBOARD_PORT=5000",
        "",
        "# ─ URLS DE NODOS MCP (33 nodos) ──────────────────────────────",
        "",
    ]
    
    current_layer = None
    
    for mcp_id in sorted(QCAL_NODES.keys()):
        node_info = QCAL_NODES[mcp_id]
        layer = node_info["layer"]
        port = node_info["port"]
        
        # Agregar encabezado de capa si cambió
        if layer != current_layer:
            lines.append(f"# ▬▬▬ CAPA: {layer.upper()} ▬▬▬")
            current_layer = layer
        
        env_key = mcp_id_to_env_key(mcp_id)
        
        if is_prod:
            # Producción: HTTPS
            url = f"https://{mcp_id.replace('_', '-')}-mcp.{domain}"
        else:
            # Desarrollo: localhost
            url = f"http://localhost:{port}"
        
        lines.append(f"{env_key}={url}")
    
    lines.extend([
        "",
        "# " + "=" * 76,
        "# Auto-generado con scripts/generate_env.py",
        "",
    ])
    
    return "\n".join(lines)


def validate_env(env_path: Path, mode: str = "auto") -> bool:
    """Valida un archivo .env."""
    
    if not env_path.exists():
        print(f"❌ Archivo no encontrado: {env_path}")
        return False
    
    print(f"✅ Validando {env_path}...")
    
    with env_path.open() as f:
        content = f.read()
    
    env_vars = {}
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            if "=" in line:
                key, value = line.split("=", 1)
                env_vars[key] = value
    
    errors = []
    
    # Validar variables requeridas
    required = [
        "QCAL_SYNC_INTERVAL_SECONDS",
        "QCAL_GLOBAL_THRESHOLD",
        "QCAL_DEV_MODE",
        "QCAL_F0_HZ",
    ]
    
    for var in required:
        if var not in env_vars:
            errors.append(f"Falta variable requerida: {var}")
    
    # Validar modo
    dev_mode = env_vars.get("QCAL_DEV_MODE", "").strip() == "1"
    real_tests = env_vars.get("QCAL_REAL_TESTS", "").strip() == "1"
    
    print(f"  Modo desarrollo: {'✓' if dev_mode else '✗'}")
    print(f"  Modo tests real: {'✓' if real_tests else '✗'}")
    
    # Validar URLs de nodos
    node_count = 0
    for key, value in env_vars.items():
        if key.startswith("QCAL_NODE_") and key.endswith("_URL"):
            node_count += 1
            
            if not dev_mode and not value.startswith("https://"):
                errors.append(f"En modo PRODUCCIÓN, {key} debe ser HTTPS: {value}")
            
            if dev_mode and not (value.startswith("http://") or value.startswith("https://")):
                errors.append(f"URL inválida en {key}: {value}")
    
    print(f"  Nodos configurados: {node_count}/33")
    
    if errors:
        print("\n❌ Errores encontrados:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✅ Validación exitosa!")
        return True


# ═════════════════════════════════════════════════════════════════════════════
# INTERFAZ CLI
# ═════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="QCAL-BUS Environment Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s                           # Generar .env desarrollo
  %(prog)s --mode prod               # Generar .env.production
  %(prog)s --mode real --domain prod.io  # Generar .env.real
  %(prog)s --validate .env           # Validar .env
  %(prog)s --validate .env.production # Validar producción
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # Comando: generate
    gen_parser = subparsers.add_parser("generate", help="Generar archivo .env")
    gen_parser.add_argument("--mode", choices=["dev", "prod", "real"], default="dev",
                           help="Modo de generación (default: dev)")
    gen_parser.add_argument("--domain", default="domain.com",
                           help="Dominio para producción (default: domain.com)")
    gen_parser.add_argument("--output", help="Archivo de salida (default: .env o .env.production)")
    
    # Comando: validate
    val_parser = subparsers.add_parser("validate", help="Validar archivo .env")
    val_parser.add_argument("env_file", help="Archivo .env a validar")
    
    # Sin subcommand, usar args globales
    parser.add_argument("--mode", choices=["dev", "prod", "real"], default="dev",
                       help="Modo (para generar)")
    parser.add_argument("--validate", help="Validar archivo .env")
    parser.add_argument("--domain", default="domain.com", help="Dominio")
    
    args = parser.parse_args()
    
    # Si es validate directo
    if args.validate:
        mode = "prod" if "production" in args.validate else "dev"
        success = validate_env(Path(args.validate), mode=mode)
        sys.exit(0 if success else 1)
    
    # Si no hay comando específico, generar
    print("🌟 QCAL-BUS Environment Generator")
    print("=" * 70)
    print()
    
    mode = args.mode
    output_path = get_env_path(mode)
    
    print(f"Generando {output_path.name}...")
    print(f"  Modo: {'PRODUCCIÓN' if mode == 'prod' else 'DESARROLLO'}")
    print(f"  Nodos: 33")
    print()
    
    content = generate_env_content(mode, args.domain)
    
    output_path.write_text(content)
    
    print(f"✅ Archivo creado: {output_path}")
    print()
    print("Próximos pasos:")
    
    if mode == "dev":
        print("  1. cp .env.example .env  (ya existe)")
        print("  2. python qcal_mesh_sync.py --loop")
        print("  3. Abrir http://localhost:5000")
    elif mode == "prod":
        print("  1. Editar .env.production")
        print("  2. Reemplazar domain.com con tu dominio real")
        print("  3. Verificar que todas las URLs usen HTTPS")
        print("  4. python scripts/generate_env.py --validate .env.production")
        print("  5. export $(cat .env.production | xargs)")
        print("  6. python qcal_mesh_sync.py --loop")
    
    print()


if __name__ == "__main__":
    main()
