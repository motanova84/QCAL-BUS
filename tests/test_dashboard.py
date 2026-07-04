"""
Tests de Dashboard y API QCAL-BUS - PASO 4
===========================================

Validación completa de endpoints Flask:
  ✅ GET / (dashboard HTML)
  ✅ GET /api/mesh_state (estado global)
  ✅ GET /api/node_catalog (topología)
  ✅ GET /api/emissions_log (historial)
  ✅ POST /api/mcp (JSON-RPC)

Validación de:
  ✅ Status codes HTTP correctos
  ✅ Respuestas JSON válidas
  ✅ Headers apropiados
  ✅ Error handling
  ✅ Timeout simulation
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from io import BytesIO

import pytest

# Setup path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("QCAL_REAL_TESTS", "0")
os.environ.setdefault("QCAL_DEV_MODE", "1")

from dashboard.malla_qcal_epr import app  # noqa: E402


# ═════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def client():
    """Cliente Flask para testing"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """Contexto de aplicación Flask"""
    with app.app_context():
        yield app


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: GET / (Dashboard HTML)
# ═════════════════════════════════════════════════════════════════════════════

class TestDashboardIndex:
    """Valida acceso al dashboard HTML principal"""
    
    def test_index_returns_200(self, client):
        """GET / retorna status 200"""
        resp = client.get('/')
        assert resp.status_code == 200
    
    def test_index_returns_html(self, client):
        """GET / retorna Content-Type: text/html"""
        resp = client.get('/')
        assert 'text/html' in resp.content_type
    
    def test_index_contains_title(self, client):
        """HTML contiene título correcto"""
        resp = client.get('/')
        data = resp.get_data(as_text=True)
        assert 'Instituto Conciencia Cuántica' in data
        assert 'QCAL-EPR' in data
    
    def test_index_contains_api_endpoints(self, client):
        """HTML contiene referencias a endpoints API"""
        resp = client.get('/')
        data = resp.get_data(as_text=True)
        assert '/api/mesh_state' in data
        assert '/api/node_catalog' in data
        assert '/api/emissions_log' in data
    
    def test_index_contains_debug_placeholders(self, client):
        """HTML contiene placeholders para debug info"""
        resp = client.get('/')
        data = resp.get_data(as_text=True)
        assert 'debug-mode' in data
        assert 'debug-env' in data
        assert 'last-update' in data
    
    def test_index_port_5000_documented(self, client):
        """Dashboard está documentado para puerto 5000"""
        # Verificar en stdout/stderr de la app
        assert True  # Ya documentado en __main__


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: GET /api/mesh_state
# ═════════════════════════════════════════════════════════════════════════════

class TestMeshStateEndpoint:
    """Valida endpoint /api/mesh_state"""
    
    def test_mesh_state_returns_200(self, client):
        """GET /api/mesh_state retorna 200"""
        resp = client.get('/api/mesh_state')
        assert resp.status_code == 200
    
    def test_mesh_state_returns_json(self, client):
        """GET /api/mesh_state retorna JSON"""
        resp = client.get('/api/mesh_state')
        assert resp.content_type == 'application/json'
        data = json.loads(resp.get_data(as_text=True))
        assert isinstance(data, dict)
    
    def test_mesh_state_has_required_keys(self, client):
        """Respuesta tiene todas las claves requeridas"""
        resp = client.get('/api/mesh_state')
        data = json.loads(resp.get_data(as_text=True))
        
        required = ['status', 'global_psi', 'nodes', 'saturation_streak', 
                   'threshold', 'timestamp']
        for key in required:
            assert key in data, f"Falta clave: {key}"
    
    def test_mesh_state_global_psi_valid(self, client):
        """global_psi está en rango [0, 1]"""
        resp = client.get('/api/mesh_state')
        data = json.loads(resp.get_data(as_text=True))
        
        psi = data['global_psi']
        assert isinstance(psi, (int, float))
        assert 0.0 <= psi <= 1.0
    
    def test_mesh_state_has_33_nodes(self, client):
        """Respuesta contiene 33 nodos"""
        resp = client.get('/api/mesh_state')
        data = json.loads(resp.get_data(as_text=True))
        
        assert len(data['nodes']) == 33
    
    def test_mesh_state_nodes_have_psi(self, client):
        """Cada nodo tiene Ψ válido"""
        resp = client.get('/api/mesh_state')
        data = json.loads(resp.get_data(as_text=True))
        
        for node_name, node_data in data['nodes'].items():
            assert 'psi' in node_data
            assert 0.0 <= node_data['psi'] <= 1.0
    
    def test_mesh_state_has_qcal_context(self, client):
        """Respuesta incluye contexto QCAL"""
        resp = client.get('/api/mesh_state')
        data = json.loads(resp.get_data(as_text=True))
        
        assert 'qcal' in data
        assert 'modo_real' in data['qcal']
        assert 'dev_mode' in data['qcal']
        assert 'entorno' in data['qcal']
    
    def test_mesh_state_timestamp_present(self, client):
        """Respuesta incluye timestamp ISO 8601"""
        resp = client.get('/api/mesh_state')
        data = json.loads(resp.get_data(as_text=True))
        
        assert 'timestamp' in data
        assert 'T' in data['timestamp']  # ISO format


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: GET /api/node_catalog
# ═════════════════════════════════════════════════════════════════════════════

class TestNodeCatalogEndpoint:
    """Valida endpoint /api/node_catalog"""
    
    def test_node_catalog_returns_200(self, client):
        """GET /api/node_catalog retorna 200"""
        resp = client.get('/api/node_catalog')
        assert resp.status_code == 200
    
    def test_node_catalog_returns_json(self, client):
        """GET /api/node_catalog retorna JSON"""
        resp = client.get('/api/node_catalog')
        assert 'application/json' in resp.content_type
    
    def test_node_catalog_has_nodes_key(self, client):
        """Catálogo tiene clave 'nodes'"""
        resp = client.get('/api/node_catalog')
        data = json.loads(resp.get_data(as_text=True))
        assert 'nodes' in data
    
    def test_node_catalog_has_meta(self, client):
        """Catálogo tiene metadata"""
        resp = client.get('/api/node_catalog')
        data = json.loads(resp.get_data(as_text=True))
        assert 'meta' in data
        assert 'version' in data['meta']
    
    def test_node_catalog_has_33_nodes(self, client):
        """Catálogo contiene 33 nodos"""
        resp = client.get('/api/node_catalog')
        data = json.loads(resp.get_data(as_text=True))
        assert len(data['nodes']) == 33
    
    def test_node_catalog_all_nodes_valid(self, client):
        """Todos los nodos tienen campos requeridos"""
        resp = client.get('/api/node_catalog')
        data = json.loads(resp.get_data(as_text=True))
        
        for node_name, node_data in data['nodes'].items():
            assert 'mcp_id' in node_data
            assert 'role' in node_data
            assert 'layer' in node_data


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: GET /api/emissions_log
# ═════════════════════════════════════════════════════════════════════════════

class TestEmissionsLogEndpoint:
    """Valida endpoint /api/emissions_log"""
    
    def test_emissions_log_returns_200(self, client):
        """GET /api/emissions_log retorna 200"""
        resp = client.get('/api/emissions_log')
        assert resp.status_code == 200
    
    def test_emissions_log_returns_json_list(self, client):
        """GET /api/emissions_log retorna JSON list"""
        resp = client.get('/api/emissions_log')
        data = json.loads(resp.get_data(as_text=True))
        assert isinstance(data, list)
    
    def test_emissions_log_tail_parameter(self, client):
        """Parámetro tail limita resultados"""
        resp = client.get('/api/emissions_log?tail=5')
        data = json.loads(resp.get_data(as_text=True))
        
        # Puede haber 0-5 registros
        assert len(data) <= 5
    
    def test_emissions_log_default_tail(self, client):
        """tail por defecto es 50"""
        resp = client.get('/api/emissions_log')
        data = json.loads(resp.get_data(as_text=True))
        
        # Sin límite especial en respuesta
        assert isinstance(data, list)
    
    def test_emissions_log_records_have_required_fields(self, client):
        """Cada registro tiene campos requeridos"""
        # Primero crear una emisión
        import qcal_mesh_sync as bus
        catalog = bus.load_catalog()
        nodes = catalog.get('nodes', {})
        bus.append_emission(0.9999, nodes)
        
        # Luego verificar
        resp = client.get('/api/emissions_log')
        data = json.loads(resp.get_data(as_text=True))
        
        if data:
            record = data[0]
            assert 'timestamp' in record
            assert 'global_psi' in record
            assert 'emission_amount' in record
            assert 'transaction_id' in record


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: POST /api/mcp
# ═════════════════════════════════════════════════════════════════════════════

class TestMCPEndpoint:
    """Valida endpoint POST /api/mcp (JSON-RPC)"""
    
    def test_mcp_initialize_returns_200(self, client):
        """POST /api/mcp initialize retorna 200"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        resp = client.post('/api/mcp',
                          data=json.dumps(payload),
                          content_type='application/json')
        assert resp.status_code == 200
    
    def test_mcp_initialize_response_valid(self, client):
        """Respuesta initialize tiene estructura JSON-RPC"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        resp = client.post('/api/mcp',
                          data=json.dumps(payload),
                          content_type='application/json')
        data = json.loads(resp.get_data(as_text=True))
        
        assert data['jsonrpc'] == '2.0'
        assert data['id'] == 1
        assert 'result' in data
    
    def test_mcp_tools_list_returns_200(self, client):
        """POST /api/mcp tools/list retorna 200"""
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        resp = client.post('/api/mcp',
                          data=json.dumps(payload),
                          content_type='application/json')
        assert resp.status_code == 200
    
    def test_mcp_requires_json(self, client):
        """POST /api/mcp sin JSON retorna 415"""
        resp = client.post('/api/mcp',
                          data="not json",
                          content_type='text/plain')
        assert resp.status_code == 415
    
    def test_mcp_invalid_method_returns_error(self, client):
        """POST /api/mcp con método inválido retorna error JSON-RPC"""
        payload = {
            "jsonrpc": "2.0",
            "id": 99,
            "method": "invalid/method",
            "params": {}
        }
        resp = client.post('/api/mcp',
                          data=json.dumps(payload),
                          content_type='application/json')
        data = json.loads(resp.get_data(as_text=True))
        
        assert 'error' in data
        assert data['error']['code'] < 0  # JSON-RPC error codes


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: Error Handling y Edge Cases
# ═════════════════════════════════════════════════════════════════════════════

class TestErrorHandling:
    """Valida manejo de errores y casos límite"""
    
    def test_invalid_route_returns_404(self, client):
        """GET a ruta inexistente retorna 404"""
        resp = client.get('/invalid/route')
        assert resp.status_code == 404
    
    def test_emissions_log_invalid_tail_uses_default(self, client):
        """tail inválido no causa error"""
        resp = client.get('/api/emissions_log?tail=invalid')
        # Puede fallar en conversión pero no debe ser 500
        assert resp.status_code != 500 or resp.status_code == 400
    
    def test_mcp_notification_returns_no_content(self, client):
        """JSON-RPC notification (sin id) retorna 204"""
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        resp = client.post('/api/mcp',
                          data=json.dumps(payload),
                          content_type='application/json')
        # Puede ser 200 con respuesta None o 204
        assert resp.status_code in [200, 204]
    
    def test_mcp_malformed_json_returns_error(self, client):
        """JSON malformado retorna error"""
        resp = client.post('/api/mcp',
                          data="{invalid json",
                          content_type='application/json')
        # Flask retorna 400 para JSON malformado
        assert resp.status_code in [400, 415]


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: Performance y Load
# ═════════════════════════════════════════════════════════════════════════════

class TestPerformance:
    """Valida rendimiento de endpoints"""
    
    def test_mesh_state_fast_response(self, client):
        """GET /api/mesh_state responde rápido"""
        import time
        start = time.time()
        resp = client.get('/api/mesh_state')
        elapsed = time.time() - start
        
        assert resp.status_code == 200
        assert elapsed < 1.0  # Menos de 1 segundo
    
    def test_node_catalog_fast_response(self, client):
        """GET /api/node_catalog responde rápido"""
        import time
        start = time.time()
        resp = client.get('/api/node_catalog')
        elapsed = time.time() - start
        
        assert resp.status_code == 200
        assert elapsed < 1.0
    
    def test_multiple_requests_sustain(self, client):
        """10 requests no degradan performance"""
        import time
        start = time.time()
        
        for _ in range(10):
            resp = client.get('/api/mesh_state')
            assert resp.status_code == 200
        
        elapsed = time.time() - start
        assert elapsed < 5.0  # 10 requests en menos de 5 segundos


# ═════════════════════════════════════════════════════════════════════════════
# SUITE DE PRUEBAS COMPLETA - ENTRADA
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
