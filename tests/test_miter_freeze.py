"""D-037: the miter N, solver and timeouts (Protocol L299) are frozen exactly as proposed, and the control runner
uses only the frozen record. Also the run_controls.py usage message. Not an F18 run and not evidence."""
from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "runner"))

import run_controls as RC  # noqa: E402
from openvef import freeze  # noqa: E402

RECORD = freeze.load(REPO, RC.MITER_FREEZE_RECORD)
PROPOSAL = (REPO / "docs" / "fifo-miter-proposal-DRAFT.md").read_text(encoding="utf-8")
ADDENDUM = (REPO / "docs" / "FREEZE-RECORD-2026-11-24.md").read_text(encoding="utf-8")
MATERIALS = json.loads((REPO / RC.MATERIALS).read_text(encoding="utf-8"))


def pack_line(pack: Path, n: int) -> str:
    return pack.read_text(encoding="utf-8").splitlines()[n - 1]


class FrozenValuesTests(unittest.TestCase):
    def test_hashes_verify(self):
        self.assertEqual(freeze.verify(REPO, RECORD)["changed"], [])

    def test_values_are_the_proposal(self):
        fv = RECORD["frozen_values"]
        self.assertIn("| N | the design cycle cap (64, DRAFT item 7) |", PROPOSAL)
        self.assertEqual((fv["N"]["value"], fv["N"]["cycles"]), ("cycle_cap", MATERIALS["cycle_cap"]))
        self.assertEqual(MATERIALS["cycle_cap"], 64)
        self.assertIn("| Solver | Yosys built-in `sat` (minisat), Yosys v0.71 in the pinned image |", PROPOSAL)
        self.assertEqual(fv["solver"], "yosys sat (minisat), D-007 (3)")
        self.assertEqual(int(re.search(r"\| Solver timeout \| (\d+) s per `sat` script \|", PROPOSAL).group(1)),
                         fv["solver_timeout_s"])
        self.assertEqual(int(re.search(r"\| Wall-clock limit \| (\d+) s per Yosys run \|", PROPOSAL).group(1)),
                         fv["wall_timeout_s"])

    def test_pack_lines_quoted_verbatim_in_both_packs(self):
        packs = [next((REPO / "baseline").glob("*/02_OpenVEF_Experimental_Protocol_v1.3.6.md")),
                 next((REPO / "baseline-v1.3.7").glob("*/02_OpenVEF_Experimental_Protocol_v1.3.7*.md"))]
        for pack in packs:
            for key, text in RECORD["pack_lines"].items():
                with self.subTest(pack=pack.name, line=key):
                    self.assertIn(text, pack_line(pack, int(key[1:])))

    def test_addendum_lists_record_hashes(self):
        self.assertIn("## Amendment D-037", ADDENDUM)
        for ref in RECORD["items"][0]["refs"]:
            self.assertIn(f"| `{ref['ref']}` | `{ref['sha256']}` |", ADDENDUM)
        self.assertIn(f"| `{RC.MITER_FREEZE_RECORD}` | `{freeze.ref_sha256(RC.MITER_FREEZE_RECORD)}` |", ADDENDUM)

    def test_runner_uses_the_record(self):
        s = RC.miter_settings(64)
        self.assertEqual((s["N"], s["solver_timeout_s"], s["wall_timeout_s"]), (64, 300, 900))
        self.assertIn("FROZEN under D-037", s["status"])

    def test_changed_hash_or_other_cap_stops(self):
        with self.assertRaisesRegex(RC.MiterFreezeError, "L293"):
            RC.miter_settings(63)
        real = freeze.ref_sha256
        with mock.patch.object(freeze, "ref_sha256",
                               lambda ref, repo=REPO: "0" * 64 if "miter-proposal" in ref else real(ref, repo)):
            with self.assertRaisesRegex(RC.MiterFreezeError, "not frozen"):
                RC.miter_settings(64)

    @unittest.skipUnless(shutil.which("git") and (REPO / ".git").exists(), "no git (pinned image)")
    def test_frozen_before_any_owner_mutant(self):
        """D-037: recorded before any owner mutant exists, so the values cannot be tuned to results."""
        def first_commit_time(*paths):
            out = subprocess.run(["git", "log", "--all", "--format=%ct", "--", *paths], cwd=REPO,
                                 capture_output=True, text=True, check=True).stdout.split()
            return min(map(int, out)) if out else None
        frozen = first_commit_time(RC.MITER_FREEZE_RECORD)
        mutant = first_commit_time("design/fifo/controls/mutants")
        if frozen is not None and mutant is not None:
            self.assertLess(frozen, mutant)
        if frozen is None:
            self.assertIsNone(mutant, "an owner mutant exists but the D-037 record is uncommitted")


class UsageTests(unittest.TestCase):
    def parse(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                self.assertRaises(SystemExit) as cm:
            RC.parse_args(["run_controls.py", *argv])
        return cm.exception.code, out.getvalue(), err.getvalue()

    def test_help(self):
        for flag in ("-h", "--help"):
            code, out, _ = self.parse(flag)
            self.assertEqual(code, 0)
            self.assertTrue(out.startswith("usage: run_controls.py <baseline_root> <evidence_dir> <run_class>"))

    def test_wrong_arguments(self):
        for argv in ((), ("a",), ("a", "b"), ("a", "b", "c", "d"), ("a", "b", "--pack"), ("a", "b", "")):
            with self.subTest(argv=argv):
                code, out, err = self.parse(*argv)
                self.assertEqual((code, out), (2, ""))
                self.assertIn("usage: run_controls.py", err)

    def test_three_arguments(self):
        self.assertEqual(RC.parse_args(["x", "b", "e", "dev"]), (Path("b"), Path("e"), "dev"))


if __name__ == "__main__":
    unittest.main()
