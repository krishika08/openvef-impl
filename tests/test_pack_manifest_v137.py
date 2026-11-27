"""D-025 item 1: the runner-executed C5 predicate runs only when the candidate pack's SHA256SUMS verify. Checks the
manifest verification itself, that the predicate refuses to run before it, and that a run on a tampered candidate
pack stops before any fixture. Not an F18 run and not evidence."""
from __future__ import annotations

import hashlib

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
for p in (REPO / "src", REPO / "runner"):
    sys.path.insert(0, str(p))

import adapters_v137  # noqa: E402
import run_f18  # noqa: E402

PACK = REPO / "proposals/v1.3.7/pack"
INFO = run_f18.PACKS["v1.3.7-candidate"]
_SRC = "def ok(vector, sampled):\n    return sampled['busy'] == '0'\n"
TOY = {"driver_return": {"a": "1"}, "input_port_widths": {"a": 1}, "sampled_outputs": {"busy": "1"},
       "legal_input_predicate": {"language": "python3.11", "function": "ok", "source": _SRC,  # OD-2: with its frozen hash
                                 "source_sha256": hashlib.sha256(_SRC.encode("utf-8")).hexdigest()}}


def copy_pack(tmp: str) -> Path:
    dst = Path(tmp) / "pack"
    shutil.copytree(PACK, dst, copy_function=shutil.copyfile)
    return dst


@unittest.skipUnless(PACK.exists(), "candidate pack not present (audit bundle)")
class PackManifestTests(unittest.TestCase):
    def verify(self, root, pin=INFO["manifest_sha256"]):
        return run_f18.verify_pack_manifest(root, INFO["manifest"], pin)

    def test_committed_pack_verifies(self):
        self.assertEqual(self.verify(PACK), len((PACK / INFO["manifest"]).read_text().splitlines()))

    def test_tampered_file_extra_file_and_wrong_pin_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_pack(tmp)
            m27 = root / "41_F18_Fixture_Inputs/M27.json"
            m27.write_bytes(m27.read_bytes().replace(b'== \\"1\\")', b'== \\"0\\")'))
            with self.assertRaises(run_f18.IntegrityError):
                self.verify(root)
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_pack(tmp)
            (root / "extra.py").write_text("x = 1\n")
            with self.assertRaises(run_f18.IntegrityError):
                self.verify(root)
        with self.assertRaises(run_f18.IntegrityError):
            self.verify(PACK, pin="0" * 64)

    def test_predicate_does_not_run_before_verification(self):
        with mock.patch.object(adapters_v137, "PACK_VERIFIED", False):
            with self.assertRaises(adapters_v137.NotDetermined) as ctx:
                adapters_v137.adapt_legal_input({"input": TOY}, None)
            self.assertIn("not verified", str(ctx.exception))
        with mock.patch.object(adapters_v137, "PACK_VERIFIED", True):
            failure = adapters_v137.adapt_legal_input({"input": TOY}, None)
            self.assertEqual(failure.diagnostic, "DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE")

    def test_run_on_a_tampered_candidate_stops_before_any_fixture(self):
        def no_image():
            raise run_f18.SandboxUnavailable("synthetic run")
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_pack(tmp)
            (root / "README.md").write_text("tampered\n")
            out = Path(tmp) / "out"
            out.mkdir()
            with mock.patch.multiple(run_f18, ensure_image=no_image, broker_mode=lambda: False,
                                     git_commit=lambda: "synthetic", SANDBOX=None, SIM=None), \
                    mock.patch.object(adapters_v137, "PACK_VERIFIED", False), \
                    mock.patch.object(sys, "argv", ["run_f18.py", str(root), str(out), "unit-test", "--pack",
                                                    "v1.3.7-candidate"]), \
                    contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(run_f18.IntegrityError):
                    run_f18.main()
                self.assertFalse(adapters_v137.PACK_VERIFIED)
            run_dir, = out.glob("run-*")
            self.assertFalse((run_dir / "results.jsonl").exists())
        run_f18.ADAPTER_TABLE, run_f18.ACTIVE_INDEX_SHA256 = run_f18.ADAPTERS, run_f18.INDEX_SHA256


if __name__ == "__main__":
    unittest.main()
