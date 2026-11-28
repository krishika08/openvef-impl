"""D-035 item 2: the adopted v1.3.7 pack (baseline-v1.3.7/) is byte-identical to the audited candidate, matches its
manifest with no unlisted file, carries the cleared manifest and fixture-index hashes, and is labelled only by the
label file outside the pack directory. Not an F18 run and not evidence."""
from __future__ import annotations

import hashlib
import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACK = REPO / "baseline-v1.3.7" / "OpenVEF_Planning_v1_3_7"
CAND = REPO / "proposals" / "v1.3.7" / "pack"
LABEL = REPO / "baseline-v1.3.7" / "LABEL-v1.3.7-ADOPTED.md"

spec = importlib.util.spec_from_file_location("build_pack_release", REPO / "tools" / "build_pack_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


def files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


@unittest.skipUnless(PACK.exists() and CAND.exists(), "adopted or candidate pack not present (audit bundle)")
class AdoptedPackTests(unittest.TestCase):
    def test_byte_identical_to_the_audited_candidate(self):
        self.assertEqual(files(PACK), files(CAND))

    def test_manifest_and_index_are_the_cleared_ones(self):
        pack = files(PACK)
        self.assertEqual(hashlib.sha256(pack[release.MANIFEST]).hexdigest(), release.MANIFEST_SHA256)
        self.assertEqual(hashlib.sha256(pack[release.INDEX]).hexdigest(), release.INDEX_SHA256)

    def test_every_file_listed_and_matching(self):
        pack = files(PACK)
        listed = {rel: d for d, rel in (l.split("  ", 1) for l in pack[release.MANIFEST].decode().splitlines())}
        self.assertEqual(set(pack) - {release.MANIFEST}, set(listed))
        for rel, digest in listed.items():
            self.assertEqual(hashlib.sha256(pack[rel]).hexdigest(), digest, rel)

    def test_label_only_outside_the_pack(self):
        self.assertTrue(LABEL.is_file())
        self.assertNotIn("v1.3.7 ADOPTED", "".join(d.decode("utf-8", "replace") for d in files(PACK).values()))
        self.assertIn("v1.3.7 ADOPTED", LABEL.read_text(encoding="utf-8"))

    def test_runner_default_pack_is_the_adopted_one(self):
        import sys
        sys.path.insert(0, str(REPO / "runner"))
        import run_f18
        self.assertEqual(run_f18.DEFAULT_PACK, "v1.3.7")
        adopted, cand = run_f18.PACKS["v1.3.7"], run_f18.PACKS["v1.3.7-candidate"]
        for key in ("index_sha256", "manifest", "manifest_sha256", "adapters", "owner_specified", "owner_decided",
                    "open_shapes"):
            self.assertEqual(adopted[key], cand[key], key)
        self.assertEqual(adopted["manifest_sha256"], release.MANIFEST_SHA256)
        self.assertIn("ADOPTED", adopted["label"])
        self.assertEqual(run_f18.PACKS["v1.3.6"]["adapters"], run_f18.ADAPTERS)  # v1.3.6 unchanged
        self.assertEqual(run_f18.parse_args(["run_f18.py", "r", "e", "c"])[3], "v1.3.7")
        self.assertEqual(run_f18.parse_args(["run_f18.py", "r", "e", "c", "--pack", "v1.3.6"])[3], "v1.3.6")


if __name__ == "__main__":
    unittest.main()
