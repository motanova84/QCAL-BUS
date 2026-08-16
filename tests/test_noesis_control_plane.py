import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "noesis_control_plane.py"


def test_control_plane_checkpoint_is_ready():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["reference"]["f0_hz"] == 141.7001
    assert payload["reference"]["psi_threshold"] == 0.999999
    assert payload["overall_status"] == "READY"
    assert payload["consciousness_engine"]["equation"] == "C = Ψ ∩ I ∩ R ∩ T"
    assert payload["consciousness_engine"]["classification"] == "NOT_EVALUATED"
    assert all(item["exists"] for item in payload["contracts"])
