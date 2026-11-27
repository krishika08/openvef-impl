# Note: 1 ERROR, superseded

At commit `be86ae5`, 424 tests passed and 1 errored: `tests/test_image_guard.py::test_pinned_tag_is_the_content_tag`
imported `openvef` without putting `src/` on `sys.path`, as the other test files do. The test passed on the host only
because it was run there with `PYTHONPATH=src`. This was a defect in the new D-028 test, not in the code under test.
It was fixed in the next commit and the suite was run again. Kept because evidence/ is append-only. Recorded by Claude
(Claude Opus 5.5, via Claude Code).
