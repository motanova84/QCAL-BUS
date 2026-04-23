from pathlib import Path
import sys
import json

from flask import Flask, jsonify, render_template_string

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from qcal_mesh_sync import monitor_global_resonance, load_catalog, read_emissions_log  # noqa: E402
from qcal_mesh_sync import sync_mesh_with_real_sources  # noqa: E402

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>Malla QCAL-EPR</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; background: #0d1117; color: #e6edf3; }
    h1 { margin-top: 0; }
    h2 { color: #58a6ff; margin-top: 1.5rem; }
    .card { border: 1px solid #30363d; border-radius: 8px; padding: 1rem; background: #161b22; margin-bottom: 1rem; }
    .psi-bar { height: 8px; border-radius: 4px; background: #21262d; margin-top: 4px; }
    .psi-fill { height: 100%; border-radius: 4px; background: #3fb950; }
    .psi-drift { background: #d29922; }
    .psi-offline { background: #f85149; }
    .node-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.75rem; }
    .node-card { border: 1px solid #30363d; border-radius: 6px; padding: 0.75rem; background: #0d1117; font-size: 0.85rem; }
    .badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; background: #21262d; }
    .badge-nucleo { background: #1f6feb; }
    .badge-logos { background: #8957e5; }
    .badge-espiritu { background: #3d4f8a; }
    .badge-sanacion { background: #1a7f37; }
    code { white-space: pre-wrap; display: block; margin-top: 0.5rem; font-size: 0.8rem; }
    .global-psi { font-size: 2rem; font-weight: bold; }
    .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
    .dot-ok { background: #3fb950; }
    .dot-warn { background: #d29922; }
    .dot-err { background: #f85149; }
    table { border-collapse: collapse; width: 100%; font-size: 0.8rem; }
    th, td { border: 1px solid #30363d; padding: 4px 8px; text-align: left; }
    th { background: #161b22; }
  </style>
</head>
<body>
  <h1>🌀 Instituto Conciencia Cuántica — Malla QCAL-EPR</h1>

  <div class="card" id="global-card">
    <strong>Ψ_GLOBAL_ECOSISTEMA</strong>
    <div class="global-psi" id="global-psi">—</div>
    <div class="psi-bar"><div class="psi-fill" id="global-bar" style="width:0%"></div></div>
    <div style="margin-top:0.5rem">Estado: <strong id="global-status">—</strong> &nbsp;|&nbsp;
      Racha: <strong id="global-streak">—</strong> ciclos &nbsp;|&nbsp;
      Umbral: <span id="global-threshold">—</span> &nbsp;|&nbsp;
      UTC: <span id="global-ts">—</span>
    </div>
  </div>

  <h2>🔵 Nodos de la Malla (<span id="node-count">0</span>)</h2>
  <div class="node-grid" id="node-grid">Cargando...</div>

  <h2>📊 Emisiones πCODE-888 (últimas 10)</h2>
  <div class="card">
    <table id="ledger-table">
      <thead><tr><th>Timestamp</th><th>Ψ_GLOBAL</th><th>Emisión</th><th>Transaction ID</th></tr></thead>
      <tbody id="ledger-body"><tr><td colspan="4">Cargando...</td></tr></tbody>
    </table>
  </div>

  <script>
    const LAYER_BADGE = {
      'núcleo': 'badge-nucleo', 'cuerpo': '', 'mente': '', 'vida': '',
      'logos': 'badge-logos', 'espíritu': 'badge-espiritu', 'sanación': 'badge-sanacion'
    };

    function psiColor(psi) {
      if (psi >= 0.99) return '';
      if (psi >= 0.95) return 'psi-drift';
      return 'psi-offline';
    }

    function emoji(psi) {
      if (psi >= 0.99) return '🟢';
      if (psi >= 0.95) return '🟡';
      return '🔴';
    }

    async function loadState() {
      try {
        const r = await fetch('/api/mesh_state');
        const d = await r.json();

        document.getElementById('global-psi').textContent = d.global_psi.toFixed(8);
        document.getElementById('global-status').textContent = d.status;
        document.getElementById('global-streak').textContent = d.saturation_streak;
        document.getElementById('global-threshold').textContent = d.threshold;
        document.getElementById('global-ts').textContent = d.timestamp;

        const pct = Math.min(100, d.global_psi * 100);
        const bar = document.getElementById('global-bar');
        bar.style.width = pct + '%';
        bar.className = 'psi-fill ' + psiColor(d.global_psi);

        const nodes = d.nodes || {};
        const keys = Object.keys(nodes);
        document.getElementById('node-count').textContent = keys.length;
        const grid = document.getElementById('node-grid');
        grid.innerHTML = keys.map(k => {
          const n = nodes[k];
          const pct = Math.min(100, n.psi * 100);
          const badge = LAYER_BADGE[n.layer] || '';
          return `<div class="node-card">
            <div>${emoji(n.psi)} <strong>${k}</strong></div>
            <div><span class="badge ${badge}">${n.layer || ''}</span> ${n.role || ''}</div>
            <div>Ψ = ${n.psi.toFixed(6)} &nbsp; <small>${n.resonance}</small></div>
            <div class="psi-bar"><div class="psi-fill ${psiColor(n.psi)}" style="width:${pct}%"></div></div>
          </div>`;
        }).join('');
      } catch (e) {
        console.error('Error cargando estado:', e);
      }
    }

    async function loadLedger() {
      try {
        const r = await fetch('/api/emissions_log?tail=10');
        const rows = await r.json();
        const tbody = document.getElementById('ledger-body');
        if (!rows.length) {
          tbody.innerHTML = '<tr><td colspan="4">Sin emisiones registradas.</td></tr>';
          return;
        }
        tbody.innerHTML = [...rows].reverse().map(row =>
          `<tr><td>${row.timestamp}</td><td>${row.global_psi}</td><td>${row.emission_amount}</td><td>${row.transaction_id}</td></tr>`
        ).join('');
      } catch (e) { console.error('Error cargando ledger:', e); }
    }

    loadState(); loadLedger();
    setInterval(loadState, 10000);
    setInterval(loadLedger, 30000);
  </script>
</body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/mesh_state")
def mesh_state():
    return jsonify(sync_mesh_with_real_sources())


@app.route("/api/node_catalog")
def node_catalog():
    return jsonify(load_catalog())


@app.route("/api/emissions_log")
def emissions_log():
    from flask import request as flask_request
    tail = int(flask_request.args.get("tail", 50))
    return jsonify(read_emissions_log(tail=tail))


@app.route("/api/mcp", methods=["POST"])
def mcp_endpoint():
    """Endpoint HTTP para clientes MCP que no usen stdin/stdout."""
    from flask import request as flask_request
    from qcal_mesh_sync import _mcp_handle
    if not flask_request.is_json:
        return jsonify({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Content-Type debe ser application/json"}}), 415
    try:
        payload = flask_request.get_json()
        response = _mcp_handle(payload)
        if response is None:
            return ("", 204)
        return jsonify(response)
    except Exception:
        return jsonify({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": "Error interno del servidor"}}), 500


if __name__ == "__main__":
    print("Dashboard local activo en http://127.0.0.1:8505 (servidor Flask de desarrollo)")
    app.run(host="127.0.0.1", port=8505, debug=False)
