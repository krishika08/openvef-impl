"""D-030 item 1 (D3-1): tools/diff_runs.py on synthetic results.jsonl files (no fixture file is read). Not an F18 run."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def tool():
    spec = importlib.util.spec_from_file_location("diff_runs", REPO / "tools/diff_runs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ROW_A = {"fixture_id": "X1", "status": "PASS", "category": "PACK-DERIVED", "actual": {"k": 1}, "expected": {"k": 1},
         "timing": {"walls": [1.0, 2.0]}}
ROW_B = {"fixture_id": "X2", "status": "PASS", "category": "PACK-DERIVED", "actual": [], "expected": []}


class DiffRunsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = tool()

    def run_pair(self, old_rows, new_rows, raw_new: bytes | None = None):
        with tempfile.TemporaryDirectory() as d:
            a, b, out = Path(d, "a.jsonl"), Path(d, "b.jsonl"), Path(d, "r.md")
            a.write_bytes(b"".join(json.dumps(r).encode() + b"\n" for r in old_rows))
            b.write_bytes(raw_new if raw_new is not None else
                          b"".join(json.dumps(r).encode() + b"\n" for r in new_rows))
            code = self.mod.main([str(a), str(b), "--out", str(out)])
            return code, out.read_text("utf-8") if out.exists() else ""

    def test_identical(self):
        code, text = self.run_pair([ROW_A, ROW_B], [ROW_A, ROW_B])
        self.assertEqual(code, 0)
        self.assertIn("Files byte-identical: **yes**", text)
        self.assertIn("Rows byte-identical: 2", text)

    def test_non_critical_field_is_reported_by_path(self):
        new = dict(ROW_A, timing={"walls": [1.0, 2.5]})
        code, text = self.run_pair([ROW_A, ROW_B], [new, ROW_B])
        self.assertEqual(code, 0)
        self.assertIn("### `timing.walls[1]`", text)
        self.assertIn("| X1 | `2.0` | `2.5` |", text)
        self.assertIn("that differ: **0**", text)

    def test_critical_fields_exit_3(self):
        for field, value in (("status", "FAIL"), ("category", "OWNER-DECIDED"), ("actual", {"k": 2}),
                             ("expected", {"k": 1, "j": 0})):
            with self.subTest(field=field):
                code, text = self.run_pair([ROW_A], [dict(ROW_A, **{field: value})])
                self.assertEqual(code, 3)
                self.assertIn("CRITICAL", text)

    def test_type_and_absent_differences(self):
        code, text = self.run_pair([dict(ROW_B, n=1)], [dict(ROW_B, n=1.0, extra=True)])
        self.assertEqual(code, 0)
        self.assertIn("| X2 | `1` | `1.0` |", text)
        self.assertIn("| X2 | `<absent>` | `true` |", text)

    def test_same_json_different_bytes(self):
        raw = json.dumps(ROW_B, indent=None, separators=(",", ":")).encode() + b"\n"
        code, text = self.run_pair([ROW_B], [], raw_new=raw)
        self.assertEqual(code, 0)
        self.assertIn("equal as JSON but different bytes: 1", text)

    def test_fixture_in_one_file_only_and_order(self):
        code, text = self.run_pair([ROW_A, ROW_B], [ROW_B])
        self.assertEqual(code, 3)
        self.assertIn("only in old: 1 (X1)", text)
        code, text = self.run_pair([ROW_A, ROW_B], [ROW_B, ROW_A])
        self.assertEqual(code, 0)
        self.assertIn("Same fixture order: **no**", text)

    def test_bad_input_exit_2(self):
        for raw in (b"not json\n", b'{"status": "PASS"}\n', b'{"fixture_id": "X1"}\n{"fixture_id": "X1"}\n'):
            with self.subTest(raw=raw):
                code, _ = self.run_pair([ROW_A], [], raw_new=raw)
                self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
