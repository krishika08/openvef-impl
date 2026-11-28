"""D-039 item 4, DEV-005: every control file is listed in the DEV-005 inventory with its SHA-256 and commit.

Owner decision D-039 (Krishika, 28 Nov 2026) lets Claude Code write all control artifacts, under deviation DEV-005
"AI-written controls" (docs/DEVIATIONS.md). This replaces the D-036 check that no control file was last changed by a
Claude Code-authored commit. A control file is every file under design/fifo/controls/ other than the harness files
README.md and slots.json, tracked or not. docs/DEV-005-inventory.json lists each one with the SHA-256 of its current
bytes and a commit whose copy of the file has those bytes.

The listing and hash tests run everywhere. The commit test needs git and the repository history, so it skips in the
pinned image. Not an F18 run and not evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONTROLS = "design/fifo/controls"
HARNESS_OWNED = {f"{CONTROLS}/README.md", f"{CONTROLS}/slots.json"}
INVENTORY = "docs/DEV-005-inventory.json"
LABEL = "AI-written (DEV-005)"


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def control_files(repo: Path) -> set[str]:
    root = repo / CONTROLS
    found = ({p.relative_to(repo).as_posix() for p in root.rglob("*")
              if p.is_file() and "__pycache__" not in p.parts} if root.is_dir() else set())  # bytecode caches are not controls
    return found - HARNESS_OWNED


def load_inventory(repo: Path) -> dict:
    return json.loads((repo / INVENTORY).read_text(encoding="utf-8"))


def inventory_problems(repo: Path, check_commits: bool) -> list[str]:
    """Every mismatch between the control files and the inventory; [] when they agree."""
    inv = load_inventory(repo)
    entries = {e["path"]: e for e in inv["files"]}
    problems = []
    if len(entries) != len(inv["files"]):
        problems.append("duplicate path in the inventory")
    files = control_files(repo)
    problems += [f"not in the inventory: {p}" for p in sorted(files - set(entries))]
    problems += [f"listed but absent: {p}" for p in sorted(set(entries) - files)]
    for path in sorted(files & set(entries)):
        e = entries[path]
        if e.get("label") != LABEL:
            problems.append(f"{path}: label is not {LABEL!r}")
        if hashlib.sha256((repo / path).read_bytes()).hexdigest() != e.get("sha256"):
            problems.append(f"{path}: SHA-256 differs from the inventory")
        if check_commits:
            try:
                blob = git(repo, "show", f"{e.get('commit')}:{path}")
            except subprocess.CalledProcessError:
                problems.append(f"{path}: commit {e.get('commit')} does not contain the file")
                continue
            if hashlib.sha256(blob).hexdigest() != e.get("sha256"):
                problems.append(f"{path}: the copy in commit {e.get('commit')} has other bytes")
    return problems


def git_available(repo: Path) -> bool:
    if shutil.which("git") is None:
        return False
    try:
        return git(repo, "rev-parse", "--is-inside-work-tree").strip() == b"true"
    except (subprocess.CalledProcessError, OSError):
        return False


class InventoryTests(unittest.TestCase):
    def test_every_control_file_listed_with_its_bytes(self):
        self.assertEqual(inventory_problems(REPO, check_commits=False), [])

    @unittest.skipUnless(git_available(REPO), "git or the repository history is not available (e.g. the pinned image)")
    def test_every_listed_commit_holds_those_bytes(self):
        self.assertEqual(inventory_problems(REPO, check_commits=True), [])


@unittest.skipUnless(shutil.which("git") is not None, "git is not available (e.g. the pinned image)")
class DetectorTests(unittest.TestCase):
    """The checker on a throwaway repository: unlisted, changed, absent and wrongly committed files are reported."""

    def test_reports_each_kind_of_mismatch(self):
        with tempfile.TemporaryDirectory() as t:
            repo = Path(t)
            env_free = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env_free)

            def commit(rel: str, data: bytes) -> str:
                (repo / rel).parent.mkdir(parents=True, exist_ok=True)
                (repo / rel).write_bytes(data)
                git(repo, "add", rel)
                git(repo, "-c", "user.name=C", "-c", "user.email=c@example.invalid", "commit", "-q", "-m", "s")
                return git(repo, "rev-parse", "HEAD").decode().strip()

            def write_inventory(entries: list) -> None:
                (repo / INVENTORY).parent.mkdir(parents=True, exist_ok=True)
                (repo / INVENTORY).write_text(json.dumps({"files": entries}), encoding="utf-8")

            commit(f"{CONTROLS}/README.md", b"r")                       # harness file: never listed
            c1 = commit(f"{CONTROLS}/drivers/a.py", b"a")
            entry = {"path": f"{CONTROLS}/drivers/a.py", "sha256": hashlib.sha256(b"a").hexdigest(), "commit": c1,
                     "label": LABEL}
            write_inventory([entry])
            self.assertEqual(inventory_problems(repo, check_commits=True), [])
            (repo / CONTROLS / "checkers").mkdir()
            (repo / CONTROLS / "checkers" / "b.py").write_bytes(b"b")   # untracked and unlisted
            self.assertEqual(inventory_problems(repo, check_commits=True),
                             [f"not in the inventory: {CONTROLS}/checkers/b.py"])
            (repo / CONTROLS / "checkers" / "b.py").unlink()
            (repo / CONTROLS / "drivers" / "a.py").write_bytes(b"a2")   # changed after listing
            self.assertIn(f"{CONTROLS}/drivers/a.py: SHA-256 differs from the inventory",
                          inventory_problems(repo, check_commits=False))
            (repo / CONTROLS / "drivers" / "a.py").write_bytes(b"a")
            write_inventory([{**entry, "commit": "0" * 40}])            # commit without those bytes
            self.assertEqual(inventory_problems(repo, check_commits=True),
                             [f"{CONTROLS}/drivers/a.py: commit {'0' * 40} does not contain the file"])
            write_inventory([entry, {**entry, "path": f"{CONTROLS}/gone.py"}])
            self.assertIn(f"listed but absent: {CONTROLS}/gone.py", inventory_problems(repo, check_commits=False))


if __name__ == "__main__":
    unittest.main()
