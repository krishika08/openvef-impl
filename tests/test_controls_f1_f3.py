"""F1 (L510) and F3 (L512) procedures in the control runner (D-036 item 4).

Synthetic temporary directories only; no owner control file is read, written or imitated. A file's contents here are
empty or arbitrary bytes. Where a run must get past the static stages, the stage function itself is replaced, and the
simulation and checker calls are replaced by recorded results, so these tests check the procedure's bookkeeping and
verdict rules, not any artifact. Not an F18 run and not evidence."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "runner"))

import run_controls as RC  # noqa: E402
from openvef.stage_map import CheckerOutcome  # noqa: E402
from openvef.trace import ROW_KEYS  # noqa: E402

SLOTS = json.loads((REPO / "design" / "fifo" / "controls" / "slots.json").read_text(encoding="utf-8"))
CTX = {"null": {"n": 1}, "rtl": {"r": 1}, "mask": None, "metadata": {"design_id": "x"},
       "provisional": ["DRAFT materials"], "cleared": [{"label": "cleared under DEV-001 (non-independent review saved)"}],
       "record": {"file_sha256": {}}}
L334 = {"t_timeout_s": 2.0, "median_s": 0.1, "wall_times_s": [0.1, 0.1, 0.1]}


def row(i: int, out: str = "0", nxt: str = "0") -> dict:
    r = {k: None for k in ROW_KEYS}
    r.update(cycle_index=i, reset=False, outputs_after_edge_n={"o": out}, next_inputs_scheduled_for_edge_n_plus_1={"i": nxt},
             inputs_consumed_at_edge_n={"i": "0"}, driver_completed=False)
    return r


def result(rows: list) -> dict:
    return {"rows": rows, "events": []}


class Workspace:
    """A temporary CONTROLS_DIR holding only the named files, with arbitrary contents."""

    def __init__(self, files: dict[str, bytes]):
        self.files = files

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        for rel, data in self.files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(data)
        self.orig, RC.CONTROLS_DIR = RC.CONTROLS_DIR, root
        RC._CACHE.clear()
        return root

    def __exit__(self, *exc):
        RC.CONTROLS_DIR = self.orig
        RC._CACHE.clear()
        self.tmp.cleanup()


BOTH = {RC.F1_F3_DRIVER: b"", RC.F1_F3_CHECKER: b""}


class BlockedTests(unittest.TestCase):
    def test_blocked_until_both_files_exist(self):
        for files in ({}, {RC.F1_F3_DRIVER: b""}, {RC.F1_F3_CHECKER: b""}):
            with Workspace(files), mock.patch.object(RC, "sim_context", side_effect=AssertionError("no simulation")):
                for control in ("F1", "F3"):
                    with self.subTest(control=control, files=sorted(files)):
                        rec = RC.run_control(control, SLOTS, REPO / "baseline")
                        self.assertEqual(rec["status"], "BLOCKED_OWNER_ARTIFACTS")

    def test_f1_f3_need_exactly_the_reference_driver_and_correct_checker(self):
        for control in ("F1", "F3"):
            self.assertEqual(sorted(RC.needs(SLOTS, control)[0]), sorted([RC.F1_F3_DRIVER, RC.F1_F3_CHECKER]))


class RejectionTests(unittest.TestCase):
    def test_empty_files_are_rejected_by_the_real_static_stages(self):
        with Workspace(BOTH), mock.patch.object(RC, "sim_context", side_effect=AssertionError("no simulation")):
            for control in ("F1", "F3"):
                rec = RC.run_control(control, SLOTS, REPO / "baseline")
                with self.subTest(control=control):
                    self.assertEqual(rec["status"], "ARTIFACT_REJECTED")
                    self.assertEqual(rec["rejection"]["diagnostic"], "SOURCE_EMPTY|file=driver.py")
                    self.assertIn(RC.F1_F3_DRIVER, rec["artifact_sha256"])

    def test_invalid_utf8_is_a_source_ast_rejection(self):
        with Workspace({RC.F1_F3_DRIVER: b"\xff", RC.F1_F3_CHECKER: b""}):
            rec = RC.run_control("F1", SLOTS, REPO / "baseline")
        self.assertEqual(rec["status"], "ARTIFACT_REJECTED")
        self.assertEqual(rec["rejection"]["diagnostic"], "SOURCE_SYNTAX_REJECT|file=driver.py|line=1|column=1")

    def test_owner_files_are_not_changed(self):
        with Workspace({RC.F1_F3_DRIVER: b"x", RC.F1_F3_CHECKER: b"y"}) as root:
            RC.run_control("F1", SLOTS, REPO / "baseline")
            self.assertEqual((root / RC.F1_F3_DRIVER).read_bytes(), b"x")
            self.assertEqual((root / RC.F1_F3_CHECKER).read_bytes(), b"y")
            self.assertEqual(sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()),
                             sorted([RC.F1_F3_DRIVER, RC.F1_F3_CHECKER]))


class ProcedureTests(unittest.TestCase):
    """Static stages replaced; simulation and checker calls replaced by recorded results."""

    def run_with(self, control: str, runs: list, verdicts: list) -> dict:
        outcomes = iter(CheckerOutcome(v, None) if v else CheckerOutcome(None, ("CHECKER_RUNTIME_ERROR", "x"))
                        for v in verdicts)
        runs_iter = iter(runs)
        with Workspace(BOTH), \
                mock.patch.object(RC, "artifact_stages", return_value=None), \
                mock.patch.object(RC, "sim_context", return_value=CTX), \
                mock.patch.object(RC, "l334_timeout", return_value=L334), \
                mock.patch.object(RC, "null_trace_xz", return_value=None), \
                mock.patch.object(RC, "driver_run", side_effect=lambda *a, **k: next(runs_iter)), \
                mock.patch.object(RC, "checker_invocation", side_effect=lambda *a, **k: next(outcomes)):
            return RC.run_control(control, SLOTS, REPO / "baseline")

    def test_f1_pass_needs_identical_traces_and_two_pass_verdicts(self):
        same = [result([row(0), row(1)]) for _ in range(3)]
        rec = self.run_with("F1", same, ["PASS", "PASS"])
        self.assertEqual(rec["status"], "PASS", rec)
        self.assertEqual(len(set(rec["details"]["trace_sha256"])), 1)
        self.assertEqual(rec["cleared"], CTX["cleared"])
        self.assertEqual(rec["provisional"], CTX["provisional"])

    def test_f1_fails_on_different_traces(self):
        runs = [result([row(0)]), result([row(0)]), result([row(0, out="1")])]
        self.assertEqual(self.run_with("F1", runs, ["PASS", "PASS"])["status"], "FAIL")

    def test_f1_fails_unless_both_verdicts_pass(self):
        same = [result([row(0)]) for _ in range(3)]
        for verdicts in (["PASS", "FAIL"], ["FAIL", "FAIL"], ["PASS", None]):
            with self.subTest(verdicts=verdicts):
                self.assertEqual(self.run_with("F1", same, verdicts)["status"], "FAIL")

    def test_f1_fails_when_a_null_run_ends_early(self):
        bad = {"rows": [row(0)], "events": [{"stage_id": "DRIVER_RUNTIME", "error_class": "DRIVER_RUNTIME_ERROR",
                                             "diagnostic": "DRIVER_RUNTIME_ERROR|x", "disposition": "REPAIR"}]}
        with mock.patch.object(RC, "run_outcome", side_effect=[None, RC.Failure("S", "E", "E|x")]):
            rec = self.run_with("F1", [result([row(0)]), bad, result([row(0)])], [])
        self.assertEqual(rec["status"], "FAIL")
        self.assertIn("null run 2 of 3", rec["reason"])

    def test_f3_pass_when_rtl_and_null_agree(self):
        rec = self.run_with("F3", [result([row(0), row(1)]), result([row(0), row(1)])], [])
        self.assertEqual(rec["status"], "PASS", rec)
        self.assertIsNone(rec["details"]["first_raw_divergence_row"])
        self.assertIsNone(rec["details"]["comparison_failure"])

    def test_f3_fails_on_next_input_divergence_before_raw_divergence(self):
        rec = self.run_with("F3", [result([row(0, nxt="1"), row(1, out="1")]), result([row(0), row(1)])], [])
        self.assertEqual(rec["status"], "FAIL")
        self.assertEqual(rec["details"]["first_next_input_divergence_row"], 0)
        self.assertEqual(rec["details"]["first_raw_divergence_row"], 1)
        self.assertIn("DRIVER_NONDETERMINISM", rec["details"]["comparison_failure"]["diagnostic"])


if __name__ == "__main__":
    unittest.main()
