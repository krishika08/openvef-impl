"""F4 (L513) and F5 (L514) procedures in the control runner (D-036 follow-up).

Synthetic temporary directories only. No owner control file is read, written or imitated: the manifest names files that
are never parsed as Verilog, the driver file is empty or arbitrary bytes, and the mutant set, bounded check, pair runs
and stage functions are replaced by recorded results. These tests check the procedures' bookkeeping and verdict rules,
not any mutant. Not an F18 run and not evidence."""
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
from openvef import miter, mutants  # noqa: E402

SLOTS = json.loads((REPO / "design" / "fifo" / "controls" / "slots.json").read_text(encoding="utf-8"))
CTX = {"null": {"n": 1, "cycle_cap": 64}, "rtl": {"r": 1}, "mask": [], "metadata": {}, "provisional": ["DRAFT materials"],
       "cleared": [{"label": "cleared under DEV-001 (non-independent review saved)"}], "record": {"file_sha256": {}}}
L334 = {"t_timeout_s": 2.0}


def manifest(roles: dict[str, list[str]]) -> bytes:
    return json.dumps({"mutants": [{"id": i, "file": f"{i}.v", "roles": r, "description": ""}
                                   for i, r in roles.items()]}).encode()


def exported(roles: dict[str, list[str]]) -> dict:
    return {"exported": {i: {"roles": r, "description": "", "file": f"{i}.v", "source_sha256": "s", "diff_sha256": "d",
                             "netlist_sha256": ["n", "n"], "netlist": "net", "design": {"m": i}}
                         for i, r in roles.items()},
            "null_netlist": "null", "design": {"cycle_cap": 64}}


def comparison(raw=True, masked=False, first_masked=None) -> dict:
    return {"termination": "COMPLETE", "integrity_failure": False, "next_input_before_raw": False,
            "raw_divergence": raw, "masked_divergence": masked, "first_masked_row": first_masked}


class Workspace:
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


ROLES = {"a": ["M-exposed"], "b": ["M-dontcare"]}


class BlockedTests(unittest.TestCase):
    def test_blocked_until_manifest_and_roles_exist(self):
        cases = [({}, "F4"), ({}, "F5"),
                 ({RC.MANIFEST_REL: manifest({"b": ["M-dontcare"]})}, "F4"),
                 ({RC.MANIFEST_REL: manifest({"a": ["M-exposed"]}), RC.F5_DRIVER: b""}, "F5"),
                 ({RC.MANIFEST_REL: manifest(ROLES)}, "F5")]  # F5 also needs the reference driver
        for files, control in cases:
            with Workspace(files), mock.patch.object(RC, "sim_context", side_effect=AssertionError("no simulation")):
                with self.subTest(control=control, files=sorted(files)):
                    self.assertEqual(RC.run_control(control, SLOTS, REPO / "baseline")["status"],
                                     "BLOCKED_OWNER_ARTIFACTS")

    def test_needs_follow_slots(self):
        self.assertEqual(RC.needs(SLOTS, "F4"), ([RC.MANIFEST_REL], ["M-exposed"]))
        self.assertEqual(sorted(RC.needs(SLOTS, "F5")[0]), sorted([RC.MANIFEST_REL, RC.F5_DRIVER]))
        self.assertEqual(RC.needs(SLOTS, "F5")[1], ["M-dontcare"])


class RejectionTests(unittest.TestCase):
    def test_mutant_set_form_error_is_artifact_rejected(self):
        with Workspace({RC.MANIFEST_REL: manifest(ROLES)}), \
                mock.patch.object(RC, "sim_context", return_value=CTX), \
                mock.patch.object(RC, "mutant_set", side_effect=mutants.MutantError("a: identical to the original RTL")):
            rec = RC.run_control("F4", SLOTS, REPO / "baseline")
        self.assertEqual(rec["status"], "ARTIFACT_REJECTED")
        self.assertIn("identical to the original RTL", rec["rejection"]["reason"])

    def test_f5_empty_driver_rejected_by_the_real_static_stages(self):
        with Workspace({RC.MANIFEST_REL: manifest(ROLES), RC.F5_DRIVER: b""}), \
                mock.patch.object(RC, "sim_context", side_effect=AssertionError("no simulation")):
            rec = RC.run_control("F5", SLOTS, REPO / "baseline")
        self.assertEqual(rec["status"], "ARTIFACT_REJECTED")
        self.assertEqual(rec["rejection"]["diagnostic"], "SOURCE_EMPTY|file=driver.py")


class ProcedureTests(unittest.TestCase):
    def run_with(self, control, labels, comparisons, roles=ROLES):
        labels_it, comps = iter(labels), iter(comparisons)
        cex = {"predicted_masked_divergence_row": 5, "inputs_by_step": [], "trigger_step": 7}

        def fake_bounded(mid):
            label = next(labels_it)
            return {"label": label, **({"counterexample": cex} if label == miter.NON_EQUIVALENT else {})}
        with Workspace({RC.MANIFEST_REL: manifest(roles), RC.F5_DRIVER: b"x"}), \
                mock.patch.object(RC, "sim_context", return_value=CTX), \
                mock.patch.object(RC, "mutant_set", return_value=exported(roles)), \
                mock.patch.object(RC, "bounded", side_effect=fake_bounded), \
                mock.patch.object(RC.static_file, "first_failure", return_value=None), \
                mock.patch.object(RC, "factory_checks", return_value=None), \
                mock.patch.object(RC, "l334_timeout", return_value=L334), \
                mock.patch.object(RC.miter, "replay_driver", return_value="replay"), \
                mock.patch.object(RC, "run_pair", side_effect=lambda *a, **k: {"comparison": next(comps)}):
            return RC.run_control(control, SLOTS, REPO / "baseline")

    def test_f4_pass_when_counterexample_replays_at_predicted_row(self):
        rec = self.run_with("F4", [miter.NON_EQUIVALENT], [comparison(masked=True, first_masked=5)])
        self.assertEqual(rec["status"], "PASS", rec)
        self.assertEqual(rec["details"][0]["replay"]["observed_row"], 5)
        self.assertEqual(rec["cleared"], CTX["cleared"])
        self.assertIn("FROZEN under D-037", rec["miter"]["status"])
        self.assertEqual((rec["miter"]["N"], rec["miter"]["solver_timeout_s"], rec["miter"]["wall_timeout_s"]),
                         (64, 300, 900))

    def test_f4_fail_when_replay_row_differs_or_no_counterexample(self):
        self.assertEqual(self.run_with("F4", [miter.NON_EQUIVALENT], [comparison(masked=True, first_masked=6)])["status"],
                         "FAIL")
        rec = self.run_with("F4", [miter.BOUNDED_EQUIVALENT], [])
        self.assertEqual(rec["status"], "FAIL")
        self.assertIn("M-exposed", rec["details"][0]["reason"])

    def test_f4_undecided_is_error(self):
        self.assertEqual(self.run_with("F4", [miter.UNDECIDED], [])["status"], "ERROR")

    def test_f5_pass_needs_raw_not_masked_and_bounded_equivalence(self):
        self.assertEqual(self.run_with("F5", [miter.BOUNDED_EQUIVALENT], [comparison()])["status"], "PASS")
        for label, comp in ((miter.NON_EQUIVALENT, comparison()),              # miter disagrees
                            (miter.BOUNDED_EQUIVALENT, comparison(raw=False)),  # window not exercised
                            (miter.BOUNDED_EQUIVALENT, comparison(masked=True))):
            with self.subTest(label=label, comp=comp):
                self.assertEqual(self.run_with("F5", [label], [comp])["status"], "FAIL")

    def test_every_mutant_with_the_role_is_checked(self):
        roles = {"a": ["M-exposed"], "c": ["M-exposed"], "b": ["M-dontcare"]}
        rec = self.run_with("F4", [miter.NON_EQUIVALENT, miter.NON_EQUIVALENT],
                            [comparison(masked=True, first_masked=5), comparison(masked=True, first_masked=4)],
                            roles=roles)
        self.assertEqual([r["mutant"] for r in rec["details"]], ["a", "c"])
        self.assertEqual(rec["status"], "FAIL")  # one of the two does not agree


class LegalAssumptionTests(unittest.TestCase):
    def test_generated_from_the_spec_predicate(self):
        """FIFO-041/-043: illegal exactly when wr_en = 1, rd_en = 0 and the sampled full = 1."""
        from openvef import design_materials
        base = design_materials.load(REPO, RC.MATERIALS)["base"]
        design = dict(base, output_widths={"almost_full": 1, "empty": 1, "full": 1, "rd_data": 8, "rd_valid": 1})
        RC._CACHE.pop("legal", None)
        try:
            r = RC.legal_expression(design)
        finally:
            RC._CACHE.pop("legal", None)
        self.assertEqual(sorted(r["support"]), ["gold_full[0]", "rd_en[0]", "wr_en[0]"])
        self.assertEqual(r["expression"], "~((~rd_en[0] & wr_en[0] & gold_full[0]))")


if __name__ == "__main__":
    unittest.main()
