import json
import subprocess
import tempfile
import unittest
from pathlib import Path

PARSER = Path(__file__).parent / "vault" / "parse_audit_log.py"


class AuditLogParserTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "audit.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def run_parser(self):
        return subprocess.run(
            ["python3", str(PARSER), str(self.path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_missing_log_fails(self):
        result = self.run_parser()
        self.assertNotEqual(result.returncode, 0)

    def test_empty_log_fails(self):
        self.path.write_text("", encoding="utf-8")
        result = self.run_parser()
        self.assertNotEqual(result.returncode, 0)

    def test_event_only_counts(self):
        rows = [
            {"event": "ok", "status": "SUCCESS"},
            {"event": "down", "status": "UNAVAILABLE"},
            {"event": "fail", "status": "FAIL"},
            {"note": "not an event", "status": "FAIL"},
        ]
        self.path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
        result = self.run_parser()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "3\t1\t1")

    def test_malformed_jsonl_fails(self):
        self.path.write_text('{"event":"ok"}\nnot-json\n', encoding="utf-8")
        result = self.run_parser()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid JSON", result.stderr)


if __name__ == "__main__":
    unittest.main()
