# Note: three D-031 runs made on a contended host (kept, superseded)

Written by Claude (Claude Opus 5.5, via Claude Code), at Krishika's instruction (D-031 item 3). Not F18 evidence.

**What happened.** At 03:21:09 UTC on 28 Nov 2026 Claude stopped a host-Python `unittest discover -s tests` run it had
started for development (not evidence). Stopping the parent left one sandbox container, `openvef-6d0311e53229`
(`python -I /opt/openvef/harness.py`, a busy loop at 100 % of one of the host's 2 CPUs), running with no parent to
remove it. Claude did not notice it until the container-test run failed, and removed it at 03:32 UTC (`docker rm -f`).
The mistake was Claude's: stopping a test parent that had started containers without checking for them afterwards.

**Runs affected** (all three started while the orphan was running; each is kept unchanged):
- `run-v137c-20261128T032116Z` (commit `ee57aa2`): 143/0/1/0, every status, category, actual and expected equal to
  audit #4's run `run-v137c-20261127T163649Z`; only the `simulator.l334` timings differ, and they are slower (median
  2.46–2.612 s, `t_timeout_s` 12.3–13.06 s). `RUN-CONTINUITY-D031-regression.md` gives "host load" as the most likely
  cause; this note names it: the orphan container.
- `controls-20261128T032418Z`: F14, F15 PASS; 14 BLOCKED_OWNER_ARTIFACTS; every status unchanged.
- `container-tests-20261128T032456Z` (commit `d4a26ea`): 438 pass, **1 FAIL**:
  `test_sandbox.SandboxIsolationTests.test_timeout_kills_and_removes_container` found the leftover container
  (`AssertionError: 'openvef-6d0311e53229' != ''`). That test checks that no `openvef-` container exists after its own
  timeout; the container it found was the orphan created 15 minutes before the test run started, not one the test made.

**Superseded by** the re-runs on the quiet host, made after the orphan was removed and listed in `docs/traceability.md`.
The bundle for audit #5 uses the re-runs, not these.
