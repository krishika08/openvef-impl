# Note on container-tests-20261127T153608Z (not the record; superseded)

Written by Claude (Claude Opus 5.5, via Claude Code), 27 Nov 2026 UTC. Added after the run; the run's own files are
unchanged.

- **How it started:** by accident. Claude ran `python3 tools/run_container_tests.py --help` to read its usage; the
  script takes no options and started a full run (`host_command` records this).
- **Why it is not the record:** `git_commit` is `7fe355e…+UNCOMMITTED_CHANGES`. The tree held the untracked evidence
  directories of `run-v137c-20261127T153351Z` and `controls-20261127T153602Z`, not yet committed. No tracked source
  differed from `7fe355e`.
- **Result, for completeness:** 29 files, 428 pass, return code 0, image `565e5547…` guard OK, interpreter `92d7e40e…`.
- **Superseded by** the next container-test run on a clean tree (named in `docs/traceability.md`).
