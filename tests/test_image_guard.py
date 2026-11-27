"""D-028: evidence entry points check the pinned image ID and never build an image."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def conf():
    text = (REPO / "tools" / "pinned-image.conf").read_text(encoding="utf-8")
    return dict(re.findall(r"^([A-Z0-9_]+)=(.*)$", text, re.M))


class ImageGuard(unittest.TestCase):
    def test_pin_values_are_well_formed(self):
        c = conf()
        self.assertEqual(set(c), {"PINNED_IMAGE_TAG", "PINNED_IMAGE_ID", "PINNED_TARBALL",
                                  "PINNED_TARBALL_SHA256", "PINNED_TARBALL_BYTES"})
        self.assertRegex(c["PINNED_IMAGE_ID"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(c["PINNED_TARBALL_SHA256"], r"^[0-9a-f]{64}$")
        self.assertRegex(c["PINNED_TARBALL_BYTES"], r"^[1-9][0-9]*$")
        self.assertFalse(Path(c["PINNED_TARBALL"]).is_relative_to(REPO))  # kept outside the repository

    def test_pinned_tag_is_the_content_tag(self):
        from openvef import sandbox
        self.assertEqual(conf()["PINNED_IMAGE_TAG"], sandbox.image_tag())

    def test_entry_points_call_the_guard_and_never_build(self):
        shell = (REPO / "runner" / "run_f18_container.sh").read_text(encoding="utf-8")
        self.assertIn('IMAGE_GUARD=$("$REPO/tools/ensure_pinned_image.sh" "$TAG")', shell)
        self.assertIn('"$OUT/image-guard.txt"', shell)
        self.assertNotIn("docker build", shell)
        tests = (REPO / "tools" / "run_container_tests.py").read_text(encoding="utf-8")
        self.assertIn('"ensure_pinned_image.sh"', tests)
        self.assertIn('"image-guard.txt"', tests)
        guard = (REPO / "tools" / "ensure_pinned_image.sh").read_text(encoding="utf-8")
        self.assertNotIn("docker build", guard)
        self.assertIn("docker load", guard)


if __name__ == "__main__":
    unittest.main()
