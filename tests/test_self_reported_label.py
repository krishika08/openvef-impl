"""The SELF_REPORTED label is the same in every F18 output (D-020, D-021).

The real main() writes real output files for synthetic, non-pack descriptors. The pack
loaders and the stages are replaced; the classification is the real runtime_basis.basis.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "runner"))
sys.path.insert(0, str(REPO / "src"))
import run_f18  # noqa: E402
from openvef import runtime_basis  # noqa: E402

DRIVERS = {"SYN-REPORTED": "def create_driver(seed):\n    return 7\n",  # return value not provable
           "SYN-NOTED": "def create_driver(seed):\n    return 7\n",     # the same, with an earlier note
           "SYN-NONE": None}                                             # never reaches the runtime checks
NOTES = {"SYN-NOTED": "earlier note"}
OUTCOME = {"disposition": "REPAIR"}


class SelfReportedLabelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def execute(desc, validator):
            source = DRIVERS[desc["fixture_id"]]
            if source is not None:
                run_f18.RUNTIME_BASIS = {"driver.py": runtime_basis.basis("driver.py", source)}
            return "EXECUTED", OUTCOME, NOTES.get(desc["fixture_id"], "")

        def no_image():
            raise run_f18.SandboxUnavailable("synthetic run")

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.multiple(run_f18, execute=execute, ensure_image=no_image, broker_mode=lambda: False,
                                    git_commit=lambda: "synthetic", load_schema_validator=lambda root: None,
                                    load_index=lambda root: [{"fixture_id": i, "sha256": "0"} for i in DRIVERS],
                                    load_descriptor=lambda root, e: {**e, "expected": OUTCOME},
                                    SANDBOX=None, SIM=None, RUNTIME_BASIS=None), \
                mock.patch.object(sys, "argv", ["run_f18.py", tmp, tmp, "unit-test", "--pack", "v1.3.6"]), \
                contextlib.redirect_stderr(io.StringIO()):
            cls.rc = run_f18.main()
            (out,) = Path(tmp).glob("run-*")
            cls.records = {r["fixture_id"]: r for r in map(json.loads, (out / "results.jsonl").read_text().splitlines())}
            cls.log = (out / "run.log").read_text().splitlines()
            cls.summary = json.loads((out / "summary.json").read_text())

    def line(self, fixture_id):
        (line,) = [x for x in self.log if f" {fixture_id}: " in x]
        return line.split(f" {fixture_id}: ", 1)[1]

    def test_note_label_log_and_summary_agree(self):
        self.assertEqual(self.rc, 0)
        label = run_f18.SELF_REPORTED_LABEL
        for fixture_id, note in (("SYN-REPORTED", f"[{label}: driver.py]"),
                                 ("SYN-NOTED", f"earlier note [{label}: driver.py]")):
            with self.subTest(fixture_id):
                rec = self.records[fixture_id]
                self.assertEqual(rec["runtime_checks"]["driver.py"]["basis"], "SELF_REPORTED")
                self.assertEqual(rec["status"], "PASS")  # the verdict is kept
                self.assertEqual(rec["note"], note)
                self.assertEqual(rec["self_reported_label"], label)
                self.assertEqual(rec["self_reported_runtime_checks"], ["driver.py"])
                self.assertEqual(self.line(fixture_id), f"PASS {note}")
        self.assertEqual(self.summary["self_reported_label"], label)
        self.assertEqual(self.summary["runtime_checks_self_reported"], ["SYN-REPORTED:driver.py", "SYN-NOTED:driver.py"])

    def test_no_label_when_runtime_checks_are_not_reached(self):
        rec = self.records["SYN-NONE"]
        self.assertEqual((rec["status"], rec["note"]), ("PASS", ""))
        self.assertNotIn("self_reported_label", rec)
        self.assertEqual(self.line("SYN-NONE").strip(), "PASS")

    def test_no_label_when_every_check_is_proven(self):
        basis = {"driver.py": {"basis": runtime_basis.PROVEN, "reason": "closed fragment"}}
        self.assertEqual(run_f18.self_reported_parts("n", basis), ("n", {"runtime_checks": basis}, []))


if __name__ == "__main__":
    unittest.main()
