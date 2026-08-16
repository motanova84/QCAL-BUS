import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "noesis_control_plane.py"


class NoesisControlPlaneTest(unittest.TestCase):
    def test_control_plane_checkpoint_is_ready(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["reference"]["f0_hz"], 141.7001)
        self.assertEqual(payload["reference"]["psi_threshold"], 0.999999)
        self.assertEqual(payload["overall_status"], "READY")
        self.assertEqual(
            payload["consciousness_engine"]["equation"],
            "C = Ψ ∩ I ∩ R ∩ T",
        )
        self.assertEqual(
            payload["consciousness_engine"]["classification"],
            "NOT_EVALUATED",
        )
        self.assertTrue(all(item["exists"] for item in payload["contracts"]))


if __name__ == "__main__":
    unittest.main()
