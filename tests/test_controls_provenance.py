"""D-036 item 2: no owner-written control file was last changed by a commit whose author is Claude Code.

Since D-036 (28 Nov 2026) every commit Claude creates has the author "Claude Code (Anthropic) <noreply@anthropic.com>".
Commits before D-036 used Krishika's identity with a Co-Authored-By trailer, so this test cannot see them; that limit
is recorded in CLAUDE.md and docs/assistance-log.md. Every tracked file under design/fifo/controls/ other than the
harness-owned README.md and slots.json is an owner slot, a mutant or a directed scenario file (CLAUDE.md, D-007).
The pinned image has no git, so this test skips there and runs where git and the repository history are available.
Not an F18 run and not evidence."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONTROLS = "design/fifo/controls"
HARNESS_OWNED = {f"{CONTROLS}/README.md", f"{CONTROLS}/slots.json"}
CLAUDE_NAME = "Claude Code (Anthropic)"
CLAUDE_EMAIL = "noreply@anthropic.com"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def claude_authored_owner_files(repo: Path) -> list[tuple[str, str]]:
    """[(path, author)] for each tracked owner file under design/fifo/controls/ whose last commit Claude Code authored."""
    found = []
    for path in sorted(p for p in git(repo, "ls-files", "-z", "--", CONTROLS).split("\0") if p):
        if path in HARNESS_OWNED:
            continue
        name, _, email = git(repo, "log", "-1", "--format=%an%x1f%ae", "--", path).strip().partition("\x1f")
        if name == CLAUDE_NAME or email.lower() == CLAUDE_EMAIL:
            found.append((path, f"{name} <{email}>"))
    return found


def git_available(repo: Path) -> bool:
    if shutil.which("git") is None:
        return False
    try:
        return git(repo, "rev-parse", "--is-inside-work-tree").strip() == "true"
    except (subprocess.CalledProcessError, OSError):
        return False


@unittest.skipUnless(git_available(REPO), "git or the repository history is not available (e.g. the pinned image)")
class ControlsProvenanceTests(unittest.TestCase):
    def test_no_owner_control_file_last_changed_by_claude_code(self):
        self.assertEqual(claude_authored_owner_files(REPO), [])


@unittest.skipUnless(shutil.which("git") is not None, "git is not available (e.g. the pinned image)")
class DetectorTests(unittest.TestCase):
    """The detector on a throwaway repository: it flags a Claude-authored owner file, and only that."""

    def commit(self, repo: Path, rel: str, data: bytes, author: str) -> None:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_bytes(data)
        git(repo, "add", rel)
        git(repo, "-c", "user.name=Committer", "-c", "user.email=committer@example.invalid", "commit", "-q",
            f"--author={author}", "-m", "synthetic")

    def test_flags_only_claude_authored_owner_files(self):
        with tempfile.TemporaryDirectory() as t:
            repo = Path(t)
            env_free = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env_free)
            owner = "Owner <owner@example.invalid>"
            claude = f"{CLAUDE_NAME} <{CLAUDE_EMAIL}>"
            self.commit(repo, f"{CONTROLS}/README.md", b"r", claude)          # harness-owned: allowed
            self.commit(repo, f"{CONTROLS}/slots.json", b"{}", claude)        # harness-owned: allowed
            self.commit(repo, f"{CONTROLS}/drivers/a.py", b"a", owner)
            self.commit(repo, f"{CONTROLS}/checkers/b.py", b"b", owner)
            self.assertEqual(claude_authored_owner_files(repo), [])
            self.commit(repo, f"{CONTROLS}/checkers/b.py", b"b2", claude)      # Claude changed an owner file
            self.assertEqual(claude_authored_owner_files(repo), [(f"{CONTROLS}/checkers/b.py", claude)])
            self.commit(repo, f"{CONTROLS}/checkers/b.py", b"b3", owner)       # the owner's later change is the last one
            self.assertEqual(claude_authored_owner_files(repo), [])


if __name__ == "__main__":
    unittest.main()
