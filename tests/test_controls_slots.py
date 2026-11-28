"""Owner-artifact slots (design/fifo/controls/) and the control runner's bookkeeping (H8).

The README is the owners' list; slots.json is the runner's copy. They must name the same
files and mutant roles, and every control must be reported BLOCKED until its owner files
exist. Synthetic directories only.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "runner"))

import run_controls as RC  # noqa: E402

CONTROLS = REPO / "design" / "fifo" / "controls"
SLOTS = json.loads((CONTROLS / "slots.json").read_text(encoding="utf-8"))
README = (CONTROLS / "README.md").read_text(encoding="utf-8")


class SlotListTests(unittest.TestCase):
    def test_readme_lists_every_slot_and_role(self):
        for s in SLOTS["slots"]:
            with self.subTest(slot=s["path"]):
                self.assertIn(f"`{s['path']}`", README)
        for role in SLOTS["mutant_roles"]:
            self.assertIn(f"| {role} |", README)

    def test_readme_has_no_unlisted_file(self):
        listed = {s["path"] for s in SLOTS["slots"]}
        named = set(re.findall(r"`((?:drivers|checkers|mutants)/[^`<>]+\.(?:py|json))`", README))
        self.assertEqual(named - listed, set())

    def test_feeds_match_readme_rows(self):
        for s in SLOTS["slots"]:
            row = next((ln for ln in README.splitlines() if ln.startswith(f"| `{s['path']}`")), None)
            if row is None:  # the directed suite shares a row with its scenario files
                continue
            feeds = set(re.findall(r"\bF\d+\b", row.split("|")[-2]))
            with self.subTest(slot=s["path"]):
                self.assertEqual(feeds, set(s["feeds"]))

    def test_every_control_declared(self):
        self.assertEqual(set(SLOTS["controls"]), set(RC.ORDER))
        for s in SLOTS["slots"]:
            self.assertTrue(set(s["feeds"]) <= set(RC.ORDER), s)

    def test_critical_gates_are_l531(self):
        self.assertEqual(RC.CRITICAL, {"F2", "F4", "F5", "F9", "F15", "F17"})


class MissingArtifactTests(unittest.TestCase):
    def test_empty_directory_blocks_every_control_but_f14_f15(self):
        with tempfile.TemporaryDirectory() as t:
            for c in RC.ORDER:
                missing = RC.missing_artifacts(SLOTS, c, Path(t))
                with self.subTest(control=c):
                    if c in ("F14", "F15"):
                        self.assertEqual(missing, [])
                    else:
                        self.assertTrue(missing)

    def test_roles_checked_against_manifest(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "mutants").mkdir()
            (root / "mutants" / "manifest.json").write_text(json.dumps(
                {"mutants": [{"id": "a", "file": "a.v", "roles": ["M-exposed"], "description": ""}]}))
            self.assertEqual(RC.missing_artifacts(SLOTS, "F4", root), [])
            self.assertEqual(RC.missing_artifacts(SLOTS, "F10", root)[-1], "mutant role M-full (mutants/manifest.json)")

    def test_all_files_present_is_not_wired_not_pass(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for s in SLOTS["slots"]:
                (root / s["path"]).parent.mkdir(parents=True, exist_ok=True)
                (root / s["path"]).write_text("{}")
            (root / "mutants" / "manifest.json").write_text(json.dumps({"mutants": [
                {"id": "a", "file": "a.v", "roles": list(SLOTS["mutant_roles"]), "description": ""}]}))
            orig = RC.CONTROLS_DIR
            RC.CONTROLS_DIR = root
            try:
                rec = RC.run_control("F2", SLOTS, REPO / "baseline")
            finally:
                RC.CONTROLS_DIR = orig
        self.assertEqual(rec["status"], "NOT_WIRED")  # files present, procedure not composed: never a pass

    def test_broker_runner_allow_list(self):
        script = (REPO / "runner" / "run_f18_container.sh").read_text(encoding="utf-8")
        # D-035 item 4: each runner also sets its default pack (F18: v1.3.7; controls: v1.3.6).
        self.assertIn("f18) RUNNER_SCRIPT=run_f18.py; OUT_PREFIX=run; PACK=${3:-v1.3.7} ;;", script)
        self.assertIn("controls) RUNNER_SCRIPT=run_controls.py; OUT_PREFIX=controls; PACK=${3:-v1.3.6} ;;", script)
        self.assertIn('*) echo "unknown runner', script)


if __name__ == "__main__":
    unittest.main()
