"""tools/check_control_file.py (D-036 item 3): the one-file static-stage check agrees with the production pair pipeline.

Uses only pack-authored sources: the driver.py and checker.py of every F18 fixture in the adopted v1.3.7 pack whose input
carries a response object. For each pair, the production static sequence (SOURCE_AST on both files, then IMPORT_POLICY,
then AST_SIGNATURE) gives a first failure or none. When that failure names a file, the tool on that file alone must give
the same failure; when there is none, the tool must accept both files. The CLI is also run as its own process: it reports
the stage and diagnostic, never changes the file it reads, and refuses an unknown role. No owner control file is read,
written or imitated. Not an F18 run and not evidence."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from openvef.ast_signature import check_ast_signature  # noqa: E402
from openvef.envelope import Failure  # noqa: E402
from openvef.import_policy import check_import_policy  # noqa: E402
from openvef.source_ast import UnsettledSpec, check_sources  # noqa: E402

TOOL = REPO / "tools" / "check_control_file.py"
FIXTURES = REPO / "baseline-v1.3.7" / "OpenVEF_Planning_v1_3_7" / "41_F18_Fixture_Inputs"
spec = importlib.util.spec_from_file_location("check_control_file", TOOL)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def pairs() -> list[tuple[str, str, str]]:
    out = []
    for p in sorted(FIXTURES.glob("*.json")):
        if p.name == "fixture-index.json":
            continue
        ro = json.loads(p.read_text(encoding="utf-8")).get("input", {}).get("response_object")
        if isinstance(ro, dict) and isinstance(ro.get("driver"), dict) and isinstance(ro.get("checker"), dict):
            d, c = ro["driver"].get("source"), ro["checker"].get("source")
            if isinstance(d, str) and isinstance(c, str):
                out.append((p.stem, d, c))
    return out


def production(driver: str, checker: str) -> Failure | None:
    sources = {"driver.py": driver, "checker.py": checker}
    trees = check_sources(list(sources.items()))
    if isinstance(trees, Failure):
        return trees
    return check_import_policy(sources, trees) or check_ast_signature(trees)


def first_failure(name: str, source: str) -> Failure | None:
    return next((f for _, f in tool.static_stages(name, source.encode("utf-8")) if f is not None), None)


@unittest.skipUnless(FIXTURES.exists(), "adopted pack not present (audit bundle)")
class AgreesWithProductionTests(unittest.TestCase):
    def test_every_pack_pair(self):
        checked = {"driver.py": 0, "checker.py": 0, "accepted": 0}
        for fid, driver, checker in pairs():
            with self.subTest(fixture=fid):
                try:
                    prod = production(driver, checker)
                except UnsettledSpec:
                    continue
                if prod is None:
                    self.assertIsNone(first_failure("driver.py", driver))
                    self.assertIsNone(first_failure("checker.py", checker))
                    checked["accepted"] += 1
                    continue
                named = False
                for name, source in (("driver.py", driver), ("checker.py", checker)):
                    if f"file={name}" in prod.diagnostic:
                        self.assertEqual(first_failure(name, source), prod)
                        checked[name] += 1
                        named = True
                if not named:
                    # Some IMPORT_POLICY diagnostics name no file. SOURCE_AST and IMPORT_POLICY take the driver's
                    # result first, then the checker's (Protocol §3.4 (2), (3)), so the pair's failure is the driver's
                    # stage failure if it has one, otherwise the checker's.
                    self.assertIn(prod.stage_id, ("SOURCE_AST", "IMPORT_POLICY"), prod)
                    per_file = {n: dict(tool.static_stages(n, s.encode("utf-8")))
                                for n, s in (("driver.py", driver), ("checker.py", checker))}
                    first = per_file["driver.py"].get(prod.stage_id) or per_file["checker.py"].get(prod.stage_id)
                    self.assertEqual(first, prod)
                    checked["unnamed"] = checked.get("unnamed", 0) + 1
        # The pack's pairs exercise rejections in both files and fully accepted pairs.
        self.assertGreater(checked["driver.py"], 10, checked)
        self.assertGreater(checked["checker.py"], 3, checked)
        self.assertGreater(checked["accepted"], 3, checked)


@unittest.skipUnless(FIXTURES.exists(), "adopted pack not present (audit bundle)")
class CommandLineTests(unittest.TestCase):
    def run_tool(self, path: Path, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-I", str(TOOL), str(path), *extra], capture_output=True, text=True)

    def pack_pair(self, rejected_file: str) -> tuple[str, Failure]:
        for _, driver, checker in pairs():
            try:
                prod = production(driver, checker)
            except UnsettledSpec:
                continue
            if prod is not None and f"file={rejected_file}" in prod.diagnostic:
                return (driver if rejected_file == "driver.py" else checker), prod
        self.fail(f"no pack pair rejects {rejected_file}")

    def test_rejection_reports_stage_and_diagnostic_and_leaves_file_unchanged(self):
        source, prod = self.pack_pair("driver.py")
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "drivers" / "x.py"
            path.parent.mkdir()
            path.write_bytes(source.encode("utf-8"))
            os.chmod(path, 0o444)
            before = (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            r = self.run_tool(path)
            after = (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            self.assertEqual(sorted(p.name for p in Path(t).rglob("*")), ["drivers", "x.py"])  # nothing written
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(f"{prod.stage_id}: REJECTED -- {prod.error_class}: {prod.diagnostic}", r.stdout)
        self.assertIn("judged as driver.py", r.stdout)
        self.assertEqual(before, after)

    def test_accepted_pair_files_pass_every_static_stage(self):
        for _, driver, checker in pairs():
            try:
                if production(driver, checker) is None:
                    break
            except UnsettledSpec:
                continue
        else:
            self.fail("no fully accepted pack pair")
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "checkers" / "y.py"
            path.parent.mkdir()
            path.write_bytes(checker.encode("utf-8"))
            r = self.run_tool(path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for stage in tool.STAGES:
            self.assertIn(f"{stage}: accepted", r.stdout)
        self.assertIn("static stages: ACCEPTED", r.stdout)

    def test_bom_and_invalid_utf8_are_source_ast_rejections(self):
        with tempfile.TemporaryDirectory() as t:
            for name, data in (("bom.py", b"\xef\xbb\xbf"), ("bad.py", b"\xff")):
                path = Path(t) / name
                path.write_bytes(data)
                r = self.run_tool(path, "--as", "checker")
                with self.subTest(file=name):
                    self.assertEqual(r.returncode, 1, r.stdout)
                    self.assertIn("SOURCE_AST: REJECTED", r.stdout)
                    self.assertIn("SOURCE_SYNTAX_REJECT|file=checker.py|line=1|column=1", r.stdout)

    def test_role_must_be_known(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "z.py"
            path.write_bytes(b"")
            self.assertEqual(self.run_tool(path).returncode, 2)  # no drivers/ or checkers/ directory, no --as
            self.assertEqual(self.run_tool(path, "--as", "mutant").returncode, 2)
            r = self.run_tool(path, "--as", "driver")
        self.assertEqual(r.returncode, 1)
        self.assertIn("SOURCE_EMPTY|file=driver.py", r.stdout)


if __name__ == "__main__":
    unittest.main()


ORIGINAL = (REPO / "design" / "fifo" / "rtl" / "ovf_fifo.v").read_text(encoding="utf-8")
PORTS = [["clk", "input", 1], ["q", "output", 2]]


class MutantCheckLogicTests(unittest.TestCase):
    """D-036 follow-up: the mutant checks' decisions, with the harness tasks replaced by recorded results. No text here is an
    edit of the original RTL: the 'changed' text is the original with a marker appended, never parsed as Verilog."""

    def run_checks(self, text, compiled=0, ports_mine=PORTS, ports_orig=PORTS):
        iface = {text: ports_mine, ORIGINAL: ports_orig}
        return tool.mutant_checks(text, ORIGINAL, "ovf_fifo",
                                  compile_verilog=lambda v, t: {"returncode": compiled, "messages": "msg",
                                                                "iverilog_version_line": "Icarus Verilog version 12.0"},
                                  interface=lambda v, t: {"ports": iface[v]})

    def test_accepts_and_reports_diff_size(self):
        r = self.run_checks(ORIGINAL + "MARKER\n")
        self.assertEqual([c for c, reason, _ in r if reason is None], list(tool.MUTANT_CHECKS))
        self.assertIn("0 line(s) removed, 1 added, in 1 hunk(s)", dict((c, d) for c, _, d in r)["DIFFERS"])

    def test_rejections_stop_at_the_first_failed_check(self):
        cases = {"MODULE": (ORIGINAL.replace("module ovf_fifo", "module other"), {}),
                 "DIFFERS": (ORIGINAL, {}),
                 "ICARUS_COMPILE": (ORIGINAL + "MARKER\n", {"compiled": 1}),
                 "PORTS": (ORIGINAL + "MARKER\n", {"ports_mine": PORTS[:1]})}
        for check, (text, kw) in cases.items():
            with self.subTest(check=check):
                r = self.run_checks(text, **kw)
                self.assertEqual(r[-1][0], check)
                self.assertIsNotNone(r[-1][1])
                self.assertTrue(all(reason is None for _, reason, _ in r[:-1]))

    def test_diff_size_counts_lines(self):
        self.assertEqual(tool.diff_size("a\nb\nc\n", "a\nB\nc\nd\n"), {"removed": 1, "added": 2, "hunks": 2})


DOCKER = __import__("shutil").which("docker") is not None  # in the container tests: the broker shim


@unittest.skipUnless(DOCKER, "docker not available")
class IcarusTaskDockerTests(unittest.TestCase):
    """The `icarus` harness task in the pinned image, on the unedited original RTL and on broken text only."""

    def test_original_rtl_compiles(self):
        from openvef import eda
        r = eda.icarus_compile(ORIGINAL, "ovf_fifo")
        self.assertEqual(r["returncode"], 0, r)
        self.assertIn("Icarus Verilog", r["iverilog_version_line"] or "")

    def test_broken_text_does_not_compile(self):
        from openvef import eda
        r = eda.icarus_compile("module ovf_fifo(\n", "ovf_fifo")
        self.assertNotEqual(r["returncode"], 0)
        self.assertTrue(r["messages"])

    def test_identical_copy_is_rejected_before_compiling(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "same.v"
            path.write_bytes(ORIGINAL.encode("utf-8"))
            r = subprocess.run([sys.executable, "-I", str(TOOL), str(path)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("DIFFERS: REJECTED -- identical to the original RTL", r.stdout)
