from pathlib import Path
import sys

from flask import Flask, jsonify, render_template_string

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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
    .card { border: 1px solid #30363d; border-radius: 8px; padding: 1rem; background: #161b22; }
    code { white-space: pre-wrap; display: block; margin-top: 1rem; }
  </style>
</head>
<body>
  <h1>🌀 Instituto Conciencia Cuántica — Malla QCAL-EPR</h1>
  <div class="card">
    <strong>Estado de la malla:</strong>
    <code id="mesh-state">Cargando...</code>
  </div>
  <script>
    async function loadState() {
      const response = await fetch('/api/mesh_state');
      const data = await response.json();
      document.getElementById('mesh-state').textContent = JSON.stringify(data, null, 2);
    }
    loadState();
    setInterval(loadState, 10000);
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


if __name__ == "__main__":
    print("Dashboard local activo en http://127.0.0.1:8505 (servidor Flask de desarrollo)")
    app.run(host="127.0.0.1", port=8505, debug=False)
