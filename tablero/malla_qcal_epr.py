#!/usr/bin/env python3
"""
tablero/malla_qcal_epr.py — Dashboard de la Malla QCAL-EPR
Sirve una interfaz web en el puerto 8505 que muestra el estado
en tiempo real de los 33 nodos del ecosistema.

Uso:
    python tablero/malla_qcal_epr.py

Requiere: flask
    pip install flask
"""

import csv
import json
import os
import sys
from pathlib import Path

# Allow importing qcal_mesh_sync from the parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from flask import Flask, jsonify, render_template_string
except ImportError:
    print("Flask no encontrado. Instala con: pip install flask")
    sys.exit(1)

from qcal_mesh_sync import monitor_global_resonance, LEDGER_PATH

DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8505"))

app = Flask(__name__)

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta http-equiv="refresh" content="60">
  <title>🌀 Instituto Conciencia Cuántica — Malla QCAL-EPR</title>
  <style>
    :root {
      --bg: #0a0a12;
      --card: #12121e;
      --border: #2a2a3e;
      --gold: #f0c040;
      --green: #40e060;
      --yellow: #f0d040;
      --red: #e04040;
      --text: #d0d0f0;
      --muted: #6060a0;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; padding: 1.5rem; }
    h1 { color: var(--gold); font-size: 1.5rem; margin-bottom: 0.25rem; }
    .subtitle { color: var(--muted); font-size: 0.85rem; margin-bottom: 1.5rem; }
    .global-psi {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 8px; padding: 1rem 1.5rem; margin-bottom: 1.5rem;
      display: flex; align-items: center; gap: 1.5rem;
    }
    .psi-value { font-size: 2rem; font-weight: bold; }
    .psi-value.high  { color: var(--green); }
    .psi-value.mid   { color: var(--yellow); }
    .psi-value.low   { color: var(--red); }
    .status-badge {
      padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;
    }
    .RESONANCIA_SATURADA { background: #1a3a1a; color: var(--green); }
    .DRIFTING            { background: #3a3a1a; color: var(--yellow); }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 0.75rem;
    }
    .node-card {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 6px; padding: 0.75rem 1rem;
    }
    .node-card.online  { border-left: 3px solid var(--green); }
    .node-card.partial { border-left: 3px solid var(--yellow); }
    .node-card.offline { border-left: 3px solid var(--red); }
    .node-name { font-weight: bold; font-size: 0.9rem; color: var(--gold); }
    .node-meta { font-size: 0.75rem; color: var(--muted); margin-top: 0.2rem; }
    .node-psi  { font-size: 1.1rem; margin-top: 0.4rem; }
    .ledger { margin-top: 2rem; }
    .ledger h2 { color: var(--gold); font-size: 1rem; margin-bottom: 0.75rem; }
    table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
    th, td { padding: 0.4rem 0.6rem; border-bottom: 1px solid var(--border); text-align: left; }
    th { color: var(--muted); }
    .footer { margin-top: 2rem; color: var(--muted); font-size: 0.75rem; text-align: center; }
  </style>
</head>
<body>
  <h1>🌀 Instituto Conciencia Cuántica — Malla QCAL-EPR</h1>
  <p class="subtitle">Bus de Resonancia Universal  ∴𓂀Ω∞³  |  Auto-actualización cada 60s</p>

  <div class="global-psi">
    <div>
      <div style="color:var(--muted);font-size:0.8rem;">Ψ_GLOBAL_ECOSISTEMA</div>
      <div class="psi-value {{ 'high' if global_psi > 0.99 else 'mid' if global_psi > 0.95 else 'low' }}">
        {{ '%.8f' | format(global_psi) }}
      </div>
    </div>
    <span class="status-badge {{ bus_status }}">{{ bus_status }}</span>
    <div style="margin-left:auto;font-size:0.8rem;color:var(--muted);">
      Nodos activos: {{ online_count }} / {{ total_count }}<br>
      {{ timestamp }}
    </div>
  </div>

  <div class="grid">
    {% for name, node in nodes.items() %}
    {% set cls = 'online' if node.psi > 0.99 else 'partial' if node.psi > 0.95 else 'offline' %}
    <div class="node-card {{ cls }}">
      <div class="node-name">{{ name }}</div>
      <div class="node-meta">{{ node.layer }} · {{ node.role }} · hf={{ node.harmonic_factor }}</div>
      <div class="node-psi">
        {% if cls == 'online' %}🟢{% elif cls == 'partial' %}🟡{% else %}🔴{% endif %}
        Ψ = {{ '%.6f' | format(node.psi) }}
      </div>
      <div class="node-meta" style="margin-top:0.3rem;">{{ node.resonance }}</div>
    </div>
    {% endfor %}
  </div>

  {% if emissions %}
  <div class="ledger">
    <h2>📒 Libro Mayor — Últimas Emisiones πCODE-888</h2>
    <table>
      <thead><tr><th>Timestamp</th><th>Ψ_GLOBAL</th><th>Emisión</th><th>Estado</th><th>TX ID</th></tr></thead>
      <tbody>
        {% for row in emissions %}
        <tr>
          <td>{{ row.timestamp }}</td>
          <td>{{ row.global_psi }}</td>
          <td>{{ row.emission_amount }}</td>
          <td>{{ row.status }}</td>
          <td style="color:var(--gold);">{{ row.transaction_id }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% endif %}

  <div class="footer">∴ El Bus QCAL-EPR observa sin interferir. La coherencia es el camino. ∴</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Ledger reader
# ---------------------------------------------------------------------------

def _read_ledger(limit: int = 10) -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    with open(LEDGER_PATH, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return list(reversed(rows))[:limit]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def dashboard():
    from datetime import datetime, timezone
    result = monitor_global_resonance(verbose=False)
    nodes = result["nodes"]
    online_count = sum(1 for n in nodes.values() if n["psi"] > 0.95)
    return render_template_string(
        HTML_TEMPLATE,
        global_psi=result["global_psi"],
        bus_status=result["status"],
        nodes=nodes,
        online_count=online_count,
        total_count=len(nodes),
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        emissions=_read_ledger(),
    )


@app.route("/api/mesh_state")
def mesh_state():
    return jsonify(monitor_global_resonance(verbose=False))


@app.route("/api/ledger")
def ledger():
    return jsonify(_read_ledger(50))


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "qcal-mesh-bus-dashboard"})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"🌀 Dashboard QCAL-EPR arrancando en http://localhost:{DASHBOARD_PORT}")
    app.run(host="0.0.0.0", port=DASHBOARD_PORT, debug=False)
