# Freeze record FREEZE-2026-11-24 — FIFO feasibility materials

**For:** the owners and the independent implementation auditor. **Transcribed by:** Claude
(Claude Opus 5.5, via Claude Code) at Krishika's instruction. Claude approved and signed
nothing. The machine-readable copy, `design/fifo/freeze/freeze-record-2026-11-24.json`,
is what the runner reads.

## Basis

- **Signature:** Krishika (owner), commit `a955245`. Her typed statement is quoted in
  [OWNER-FREEZE-PACKAGE.md](OWNER-FREEZE-PACKAGE.md).
- **Governance:** rule [D-008](ambiguities.md): approvals signed by Krishika alone take
  effect. This supersedes the package's own step 3, which required both owners.
- **Ayush ratification pending:** recorded once, in [AUDIT-READINESS.md](AUDIT-READINESS.md) §4.
- **Files not edited in place:** the frozen files keep their names and their "DRAFT"
  wording, as the package requires ("The listed files are not edited in place after
  signing"). Their frozen status is this record, at these hashes.

## Frozen items

Every hash is re-checked by `tests/test_freeze_package.py`, and by each F18 run
(`simulator_stages.prepare`). If a frozen file's bytes change, that item counts as not
frozen.

| # | Item | Reference | SHA-256 |
|---|---|---|---|
| A1 | FIFO specification v0.2: FIFO-001…FIFO-043, port manifest, reset and legal-input rules, FIFO-042 executable predicate | `docs/fifo-spec-v0.2.md` | `5e57ce18c8297aaed27e80b1a7a49476f41c70359e331fe8f5c54f96594c24b5` |
| B1 | Cycle cap (item 7) | `docs/fifo-frozen-values-proposal-DRAFT.md` | `b8d5ec793bd9aef0be41f684f009afbabe819912c618da4e2da39a7244305952` |
|  |  | `design/fifo/design-materials-DRAFT.json` | `30758c86ad88a5dc34bbe7802c5272935e8cdca810f6eec5f8cd1ff8895ba393` |
| B2 | Safe-idle vector (item 8) | `docs/fifo-frozen-values-proposal-DRAFT.md` | `b8d5ec793bd9aef0be41f684f009afbabe819912c618da4e2da39a7244305952` |
|  |  | `design/fifo/design-materials-DRAFT.json` | `30758c86ad88a5dc34bbe7802c5272935e8cdca810f6eec5f8cd1ff8895ba393` |
| B3 | Watchdog (item 9) | `docs/fifo-frozen-values-proposal-DRAFT.md` | `b8d5ec793bd9aef0be41f684f009afbabe819912c618da4e2da39a7244305952` |
|  |  | `design/fifo/design-materials-DRAFT.json` | `30758c86ad88a5dc34bbe7802c5272935e8cdca810f6eec5f8cd1ff8895ba393` |
| B4 | Scheduler (item 10) | `docs/fifo-frozen-values-proposal-DRAFT.md` | `b8d5ec793bd9aef0be41f684f009afbabe819912c618da4e2da39a7244305952` |
|  |  | `design/fifo/design-materials-DRAFT.json` | `30758c86ad88a5dc34bbe7802c5272935e8cdca810f6eec5f8cd1ff8895ba393` |
| B5 | Trace schema (item 11) | `docs/fifo-frozen-values-proposal-DRAFT.md` | `b8d5ec793bd9aef0be41f684f009afbabe819912c618da4e2da39a7244305952` |
|  |  | `design/fifo/design-materials-DRAFT.json` | `30758c86ad88a5dc34bbe7802c5272935e8cdca810f6eec5f8cd1ff8895ba393` |
| B6 | Checker metadata (item 12) | `docs/fifo-frozen-values-proposal-DRAFT.md` | `b8d5ec793bd9aef0be41f684f009afbabe819912c618da4e2da39a7244305952` |
|  |  | `design/fifo/design-materials-DRAFT.json` | `30758c86ad88a5dc34bbe7802c5272935e8cdca810f6eec5f8cd1ff8895ba393` |
| C1 | FIFO RTL `ovf_fifo` (Verilog, Icarus 12 `-g2012`) | `design/fifo/rtl/ovf_fifo.v` | `ca06abf55e6a82e6617dab9cd5d7e4ef0118d082b7789fce169016307fe2042b` |
| C2 | Null-netlist export script (Yosys v0.71). The frozen L544 export script, mutation modes and mutant population are separate owner items, **not** frozen by this line | `design/fifo/export_null.ys` | `85dfdddda430adc22ea3df9c961397d596264b195e56cba8c49da84b4bc474b1` |
| D1 | D-004: Yosys v0.71 and MCY v0.71 pins | `docs/ambiguities.md#D-004` | `cd34f9a4b75010db7a95b918dc8251881eae85870465b4414ace1f10d67af80a` |
| D2 | D-004a: `click==8.5.1` for MCY's command-line tool | `docs/ambiguities.md#D-004a` | `4f51302297ae8dc264669bc3766fdbc31b32ab1030f6a1bfe8308bfa3956b060` |
| D3 | D-005: FIFO design materials AI-assisted, with disclosure | `docs/ambiguities.md#D-005` | `d3dd7667dfc1661242f013ca32b7ee7e8110e5bb791933584a86c66dbdc2d9b8` |
| D4 | D-006: approvals (A-042, threshold 3, `ovf_fifo`, cap 64, watchdog per run) | `docs/ambiguities.md#D-006` | `41d68cc0a6f39cc6ddae0522400f6049a23a5c2a2d256b331a9106f0c4fccfce` |
| E1 | A-040: trace-row fields and row numbering | `docs/ambiguities.md#A-040` | `2329ab5b9ee388e29ef14ff266749ce6db8b205a613b02d285f41e4027a2de9a` |
| E2 | A-041: predicate scope (vector plus same-row sampled outputs) | `docs/ambiguities.md#A-041` | `6c215691edd86c33481bfc05e36e655e5a3a095941aea2deaa161c09edb67cae` |
| E3 | A-042: harness-owned reset, not a driver key (accepted by Krishika, D-006) | `docs/ambiguities.md#A-042` | `423211c6484c3cb04cbce32fa9fb344050b29302608a87f9db12c5236b3d3064` |
| E4 | A-043: L334 wall time = the whole null-run container | `docs/ambiguities.md#A-043` | `3e16a6d1fe840456dc7342c92ff0d32a2e4ce30b96d09c6ebe975f7c1095c0be` |
| E5 | A-044: a fixture's names-only port manifest (P17) | `docs/ambiguities.md#A-044` | `395848f1bb6b6630610ab026e1025a17ca003a2bae5fce47857ea5ace19f0d3b` |
| E6 | *(additional, not in the requested list)* A-038 revisited: M27 stays NOT_IMPLEMENTED | `docs/ambiguities.md#A-038` | `483c8539baa37494807333cffa1ba33db4cef578fe29286503604326d0800dad` |
| F1 | Disclosure note with the GateTruth/DVBench comparison. **Decision: disclose; do not rename ports.** Re-check the relayed source extracts before signing | `docs/fifo-benchmark-overlap-disclosure-DRAFT.md` | `ae37c774e98a6a0db0b9af0642dd5de399c281becc58115c74ae609f433bf417` |

**Frozen value (B6, computed at freeze):**
`spec_version_sha256` = `5e57ce18c8297aaed27e80b1a7a49476f41c70359e331fe8f5c54f96594c24b5`, the SHA-256 of
`docs/fifo-spec-v0.2.md` as frozen in A1.

## Amendment D-010: observation mask (Krishika, recorded 24 Nov 2026 UTC)

Frozen at Krishika's instruction (D-010, under DEV-001). It is **not** covered by the
signature `a955245`, and the review behind it is **not independent**; L271 stays unmet.
The runner reads it from `design/fifo/freeze/deviation-DEV-001.json`.

| File | SHA-256 (frozen) | SHA-256 (as reviewed, before the placeholder fixes) |
|---|---|---|
| `design/fifo/mask/ovf_fifo-mask-DRAFT.json` | `ea877da0046541550a23cc2beb69c2b9960ede422727ee080e1e00827602acbe` | `78477cd41df36074c06aca31bfca3aae4de7a085980559480a35e2a08c180b0f` |
| `design/fifo/mask/ovf_fifo-mask-traceability-DRAFT.csv` | `af2a846174bead3924d10212b36bf3c46cc41380811bf1d84f636e17caf6c97e` | `3e443a68368b693e33608db0daa94ae52e8e61a9a6b7a55b55de834862360f92` |

## Amendment D-011: observation mask, current hashes (Krishika, recorded 24 Nov 2026 UTC)

Supersedes the D-010 frozen hashes above; the same limits apply. The table's
`independent_reviewer` column now reads "none (DEV-001)", and the JSON status again states
the L270 rule.

| File | SHA-256 (frozen) |
|---|---|
| `design/fifo/mask/ovf_fifo-mask-DRAFT.json` | `64c7a9e6f25845521b9ad8164c3dff4d371f97fbd7c78c7c43c02e92540bbb59` |
| `design/fifo/mask/ovf_fifo-mask-traceability-DRAFT.csv` | `25e15c1e38ab8ff8a4a4a1172c144feabfdad24aa00992ed5d0876a87418dfd8` |

File names and `author_packet_location` cells keep "DRAFT": see D-011 in
[ambiguities.md](ambiguities.md).

## Amendment D-037: miter N, solver and timeouts (Krishika, recorded 28 Nov 2026 UTC)

Owner decision D-037 (Krishika, on a Claude (claude.ai) review; takes effect under D-008, Ayush's ratification pending
as recorded in AUDIT-READINESS.md): freeze the DRAFT values in `docs/fifo-miter-proposal-DRAFT.md` exactly as proposed,
provided each is consistent with Protocol L299 and the cycle cap. It is **not** covered by signature `a955245`.
Transcribed by Claude, who approved nothing. The runner reads `design/fifo/freeze/miter-freeze-D-037.json`
(`runner/run_controls.py` `miter_settings`). It re-checks these hashes before every F4 or F5 run, and stops with ERROR if
any hash differs or N is not the cycle cap.

**Recorded before any owner mutant exists.** No file under `design/fifo/controls/mutants/` exists in the tree or in any
commit of the repository at this amendment (`tests/test_miter_freeze.py` checks the commit order on the host), so the
values were not chosen with any mutant's result in view.

Pack lines (the same text in v1.3.6 and in the adopted v1.3.7, File 02):

> [02 L293] "Use bound `N` no greater than the design cycle cap. Record the shortest counterexample length where one is found."

> [02 L296] "`UNDECIDED`: solver/resource limit prevents a classification."

> [02 L299] "N, solver and timeout are **TO FREEZE**."

| Value | Frozen as proposed | Consistency with L299 and the cycle cap |
|---|---|---|
| N | the design cycle cap: 64 driver cycles after reset release | L293 allows N up to the cap. Item B1 froze the cap at 64 driver cycles after reset release (`cycle_cap` in `design-materials-DRAFT.json`, frozen hash below), and `openvef.miter.bounded_check` counts N in the same unit. So N equals the cap, and L293's limit holds. The shortest counterexample is searched below N and recorded |
| Solver | Yosys built-in `sat` (minisat), Yosys v0.71 in the pinned image | L299 names the solver as a value to freeze. The Yosys pin is frozen item D1 (D-004), and the solver choice is D-007 (3). No new dependency |
| Solver timeout | 300 s per `sat` script | L299 names the timeout as a value to freeze. When the limit is reached, the result is `UNDECIDED` (L296), recorded as the control's ERROR and never as a pass |
| Wall-clock limit | 900 s per Yosys run | A second resource limit under L299's "timeout". Exceeding it during the full-bound check or the shortest-counterexample search also gives `UNDECIDED` (L296). Separate from the driver watchdog (B3, L334), which it does not change |

No conflict was found, so nothing was stopped.

| File | SHA-256 (frozen) |
|---|---|
| `docs/fifo-miter-proposal-DRAFT.md` | `ff865bf9d0f824e98e1e161b9a5176f7fc9812e81265ac157a37c294bdb18de1` |
| `design/fifo/design-materials-DRAFT.json` | `30758c86ad88a5dc34bbe7802c5272935e8cdca810f6eec5f8cd1ff8895ba393` |
| `design/fifo/freeze/miter-freeze-D-037.json` | `52bb84607250051f913b3cfed48f56fb7d9bdf9b3615bad1cb3a2a0b18f0aba0` |

The proposal file keeps its name and its "DRAFT" wording, and it is not edited in place. Its frozen status is this
amendment, at this hash. Still **not** frozen: the L544 mutant export script, mutation modes and mutant population;
`OUT_OF_BUDGET_COUNTEREXAMPLE` (L297) has no search beyond the cap and no frozen bound beyond it.

## Not frozen by this record

The first row below was written before D-010: the mask is now frozen by the amendments
above, but the signature it names still does not exist.

| Item | Why |
|---|---|
| Observation mask, stricter variant and File 24 traceability table | needs the independent human mask reviewer's signature (Protocol L271; package section G); no owner signature replaces it |
| The overlap disclosure note's own owner-signature table | not signed; F1 in the package is approved |
| Frozen L544 mutant export script, mutation modes, mutant population, bounded-equivalence assumptions | separate owner items; C2 freezes only the null-netlist export script. The miter N, solver and timeouts (L299) are frozen by Amendment D-037 above; the rest of this row is unchanged |
