import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "examples" / "rustchain_health_snapshot.py"

namespace = {}
exec(SCRIPT.read_text(encoding="utf-8"), namespace)


class SnapshotTests(unittest.TestCase):
    def test_normalize_health_rejects_non_object(self):
        with self.assertRaises(namespace["SnapshotError"]):
            namespace["normalize_health"]([])

    def test_build_snapshot_bounds_miners(self):
        payload = {
            "miners": [
                {"miner_id": "a", "arch": "x86_64", "weight": 1.0},
                {"miner_id": "b", "architecture": "ppc64", "weight": 2.5},
            ]
        }
        snapshot = namespace["build_snapshot"](
            {"ok": True, "epoch": 9, "miners": 2},
            payload,
            miner_limit=1,
        )
        self.assertEqual(snapshot["health"]["epoch"], 9)
        self.assertEqual(len(snapshot["miners"]), 1)
        self.assertEqual(snapshot["miners"][0]["miner_id"], "a")

    def test_fetch_json_rejects_oversized_response(self):
        class FakeHeaders(dict):
            def get(self, key, default=None):
                return super().get(key, default)

        class FakeResponse:
            headers = FakeHeaders({"Content-Type": "application/json"})

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self, _n):
                return b"x" * (namespace["MAX_RESPONSE_BYTES"] + 1)

        with mock.patch.object(
            namespace["urllib"].request, "urlopen", return_value=FakeResponse()
        ):
            with self.assertRaises(namespace["SnapshotError"]):
                namespace["fetch_json"]("https://example.invalid/health")

    def test_sample_cli_is_offline_and_valid_json(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--sample", "--miner-limit", "2"],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["health"]["ok"])
        self.assertEqual(len(payload["miners"]), 2)


if __name__ == "__main__":
    unittest.main()
