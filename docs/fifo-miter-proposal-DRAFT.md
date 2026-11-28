# Miter bound, solver and timeouts — DRAFT proposal (D-005)

**Status: DRAFT. Not approved, not frozen.** Proposed by Claude (Claude Opus 5.5, via Claude Code) under D-005, which
lets Claude draft proposed frozen values. Only the owners approve or freeze them. This proposal is kept apart from
[fifo-frozen-values-proposal-DRAFT.md](fifo-frozen-values-proposal-DRAFT.md), because that file is hashed by freeze
items B1–B6 and is not edited.

> [02 L293] "Use bound `N` no greater than the design cycle cap. Record the shortest counterexample length where one is found."

> [02 L299] "N, solver and timeout are **TO FREEZE**."

| Value | Proposal | Reason |
|---|---|---|
| N | the design cycle cap (64, DRAFT item 7) | the largest bound L293 allows. The shortest counterexample is searched and recorded below N (`openvef.miter.bounded_check`) |
| Solver | Yosys built-in `sat` (minisat), Yosys v0.71 in the pinned image | owner decision D-007 (3); no new dependency |
| Solver timeout | 300 s per `sat` script | build default; a timeout is `UNDECIDED` (L296), recorded as the control's ERROR, never a pass |
| Wall-clock limit | 900 s per Yosys run | build default for the harness `yosys` task |

Used by F4 and F5 in `runner/run_controls.py` (`MITER_DRAFT`). Each control record carries these values with
"DRAFT proposed values (D-005); Protocol L299 TO FREEZE".
