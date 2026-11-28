# Audit readiness — OpenVEF v1.3.6 implementation

**For:** the owners (Krishika, Ayush Kumar Singh) and the independent implementation
auditor. **Prepared by:** Claude (Claude Opus 5.5, via Claude Code), 24 Nov 2026.
It is a status document: it claims no gate as passed.

## 1. Where the project stands in the release gates

> [02 L555] "(5) Independently re-audit the implementation, parser/assembler, Python 3.11 behavior and all mandatory fixture results."

- **Step (4) scope only:** implementation is open only within the limited hand-built FIFO
  feasibility scope of L555 step (4), as the owners' Sign-off Pack opened it (CLAUDE.md).
  The v1.3.6 baseline files still record their own pre-implementation status (Files 16,
  21, 23 and 32); they are read-only and are not updated by this work.
- **Step (3), v1.3.6 (D-034):** "v1.3.6 gate recorded as met, with evidentiary gaps" ([DEV-004](DEVIATIONS.md)).
  The owner records are in [owner-records/](owner-records/NOTE.md): the Sign-off Pack Part 4 signature by Krishika,
  23 Nov 2026 13:54 IST, adopting the Decision Record at revision 25. The record states "PASS, 23 Nov 2026
  (independent, documents only)" for the document audit. Four gaps stay open, each with its "Ends when": the audit
  report is absent; Ayush's signature is unverified; the Part 3 ticks disagree with blank Decision Record items; the
  boxes were marked by Claude. This document does not claim the step passed.
- **Not done:** step (5), the independent implementation re-audit. It is **not
  done**. Under DEV-002 a different AI model audits it, which is not a human independent
  audit. A first report (OpenAI GPT-6) is saved ([report](reviews/implementation-audit-gpt6-2026-11-25.md)): one BLOCKER, one MAJOR and four limitations. The
  re-audit after D-012 to D-014 ([report](reviews/implementation-reaudit-gpt6-2026-11-25.md)) ended NOT CLEARED: two BLOCKERs, one
  MAJOR and a cross-reference, three limitations. A third audit
  ([report](reviews/implementation-reaudit3-gpt6-2026-11-25.md), after D-015 to D-018) also ended NOT CLEARED: BLOCKERs A1-1 and
  A9-2. A fourth audit ([report](reviews/implementation-reaudit4-gpt6-2026-11-26.md), after D-019 to D-021) also ended
  NOT CLEARED: no BLOCKER, MAJORs A1-1 and A9-2. A fifth audit ([report](reviews/implementation-reaudit5-gpt6-2026-11-26.md),
  after D-022) ended **CLEARED for D-022**: 0 BLOCKER, 0 MAJOR, 0 MINOR, 11 LIMITATIONs. **D-023:** the AI audit
  sequence #1–#5 is complete with no open BLOCKER or MAJOR; A1-1 and A9-2 are closed as findings; A1-1-L1 (the
  support-table validator is not a semantic proof) and the SELF_REPORTED residual stay disclosed limitations.
  Step (5) is still **not marked done**: an AI audit under DEV-002 is not a human independent audit.
- **Prohibited:** no LLM or provider call has been made by any code, test or script
  (CLAUDE.md hard rule 5). The LLM-call gate, step (6), is closed.

## 2. Current counts

Latest evidence run: **`evidence/run-20261127T134112Z`** (pack v1.3.6), on the restored original image `565e5547…`
(D-028; [ENV-CHANGE-2026-11-27.md](ENV-CHANGE-2026-11-27.md); `image-guard.txt` `IMAGE_GUARD OK`).
- Run class `development`; commit `9feeac1`, clean tree; after DEV-001
  ([DEVIATIONS.md](DEVIATIONS.md)) and D-009 ([READINGS-REVIEW.md](READINGS-REVIEW.md)).
  The run re-verified all 20 frozen items, the DEV-001 mask files and the 39 D-009 items
  against their recorded hashes; none changed.
- Pinned image per D-002a: CPython 3.11.18, interpreter SHA-256 `92d7e40e…`. The image ID
  and toolchain identity are recorded in its `summary.json`.
- Every record is identical to `run-20261126T163836Z` except measured wall-clock times (the `simulator.l334` fields);
  D-024 to D-027 changed no v1.3.6 status, note or label. `run-20261127T113929Z` (retired image `fa254bba…`) is
  equivalence evidence only (D-028).
- **Candidate pack (D-024; v1.3.7 CANDIDATE, not audited; not v1.3.6 F18 evidence, does not count toward F18):**
  `run-v137c-20261128T102409Z`, commit `e993517` (C19 pack, manifest `d64a91a8`, unchanged by D-031 to D-033; development run under DEV-003), same image: 143 PASS, 0 FAIL, 1 NOT_IMPLEMENTED, 0 ERROR. Counted
  separately (D-026, D-027 Phase B): **PACK-DERIVED** 131 / 0 / 0 / 0; **OWNER-DECIDED** (OD-1–OD-4) 11 / 0 / 0 / 0 (M13,
  M41 OD-4; M15, M42, M47 OD-1; M27 OD-2; M48, M50, M53, M54, M58 OD-3); **OWNER-SPECIFIED** 1 PASS (M37, OS-2) / 0 FAIL /
  1 NOT_IMPLEMENTED (P17, OS-3: its stage is at runtime) / 0 ERROR. M41 counts OWNER-DECIDED and keeps OS-1 (A-059, approved by Krishika under D-029). Every status and category equals `run-v137c-20261127T134318Z`, `153351Z`, `163649Z`, `run-v137c-20261128T033242Z` and `042052Z` (C18 and C19 changed no expected object; D-031 to D-033 changed only a test); row-level diffs in `evidence/RUN-CONTINUITY-D030.md`, `-D030-regression.md`, `-D031.md`, `-D032.md` and `-D033.md` (only `simulator.l334` timings differ). The candidate needs an
  independent document audit and owner approval before it could replace v1.3.6.
- D-022 (re-audit #4: `stop` cites File 36 L48; literal `inspect.signature` after
  import) changed no status, note or label. D-019 to D-022 are audited (fourth and fifth audits); A9-2 is closed as a
  finding, and its SELF_REPORTED residual stays a disclosed limitation (D-023).
- **Runtime checks (D-019; SELF_REPORTED policy D-020):** 16 fixtures reach them. M06's driver is SELF_REPORTED (it returns a non-Driver and is rejected); the
  rest are PROVEN, so no accepted result rests on a report the artifact could forge. Per D-020 a SELF_REPORTED
  fixture keeps its verdict with a visible label; **SELF_REPORTED fixtures: `M06:driver.py` (PASS, labelled)**.
- **P11b rests on A-057, approved as decided (D-020); its pass now counts toward F18.**

| Status | Count | Fixtures |
|---|---|---|
| PASS | 127 | 0 provisional; 117 unlabelled, 1 "SELF_REPORTED (D-020)" (M06), 9 "cleared under DEV-001 (non-independent review saved)" (below) |
| FAIL | 0 | — |
| NOT_IMPLEMENTED | 17 | M13, M14, M15, M17, M27, M36, M37, M41, M48, M50, M53, M54, M58, P17, R07 (no cited input contract or outcome, D-013); M42, M47 (PD-01) |
| ERROR | 0 | — |
| **Total** | **144** | the full mandatory set (File 21: 59 P + 13 R + 72 M) |

**Passes cleared under DEV-001 (9):** P01, P14, P21, P42, M07, M31, M32, M33, M57.
They reach L166 (7)–(11) on the FIFO materials.
- **Settled by the owner freeze (`a955245`, D-008):** the specification, frozen values,
  RTL, null-export script, `spec_version_sha256`, and readings A-040–A-044.
- **Mask and File 24 table:** accepted by the owner without an independent review. A
  non-independent Claude (claude.ai) review, done after DEV-001 was recorded, is saved
  ([review](reviews/claude-mask-review-2026-11-25.md)); the mask is re-frozen under D-011. They
  carry the label "cleared under DEV-001 (non-independent review saved)". **L271 and File 21
  L32 remain unmet**; the auditor decides whether these 9 can count toward F18.

**Readings:** every other Claude-decided reading is approved by Krishika as decided, without
itemised owner review (D-009). Claude decided them, and Claude recommended the approval. The
auditor should weigh them with that in mind.

**F18 is therefore not passed.**
- File 21: "F18 must fail if any fixture is missing, not materialized, hash-mismatched,
  ambiguous, assigned an outcome not in the normative contract, or produces a different
  stage, error class, diagnostic byte string or terminal disposition".
- 17 fixtures are not run to an outcome, L271 is unmet (DEV-001), and the independent
  implementation re-audit (L555 (5)) is not done: the DEV-002 AI audit sequence #1–#5 is complete with no open
  BLOCKER or MAJOR (D-023), but it is an AI audit, not a human independent audit, and the fifth report's clearance
  is scoped to D-022 with 11 named limitations.

## 2a. Feasibility controls F1–F15, F17 (Protocol §17)

Plan: [F1-F17-plan.md](F1-F17-plan.md). Owner-written control artifacts are listed in
[design/fifo/controls/README.md](../design/fifo/controls/README.md) (D-007).

Latest control run: **`evidence/controls-20261127T052649Z`**, pinned image, commit
`000f6a9`. It carries the same identity records as an F18 run.

| Status | Controls |
|---|---|
| PASS, not provisional | F14 (A-052) and F15 (case table): each rests on a D-009 approval "as decided, without itemised owner review" |
| BLOCKED_OWNER_ARTIFACTS | F1–F13, F17: each record lists the owner files it is waiting for |

**What is built:** the harness components H1–H10.
- They are unit-tested on synthetic inputs and TEST-ONLY toy designs.
- The per-control procedures for F1–F13 and F17 are composed and run as the owner files
  arrive (plan step 8).
- **No control besides F14 and F15 has run.**

## 3. Evidence bundle for the independent implementation auditor

**Source:** the evidence-bundle list in the Owner Decision Record §5.3, an external
document not in this repository. The list was supplied by Krishika on 24 Nov 2026.

Status is checked against the latest evidence run, `evidence/run-20261127T134112Z`. **9 of 9 met.**
- **Met:** the run records it as stated.
- **Partly met:** some of it is recorded; the gap is named. (None at present; items 4
  and 6 were partly met up to `run-20261124T112030Z`.)

| # | §5.3 item | Where it is in each run | Status |
|---|---|---|---|
| 1 | Fixture-index SHA-256 verified at run time | `runner/run_f18.py` `load_index` aborts the run on a mismatch with the pinned `INDEX_SHA256`; `summary.json` `fixture_index_sha256` (`f37808c7…de54`) | **Met** |
| 2 | Interpreter version and binary/image hash | `summary.json` `python_version` (3.11.18), `python_executable_sha256` (`92d7e40e…6b79`), `interpreter_status` PINNED, `sandbox.image_id`, `base_image_digest`, `dockerfile_sha256`, `requirements_lock_sha256`, `toolchain` | **Met** |
| 3 | Parser/assembler/runner source commit and per-file SHA-256 | `summary.json` `git_commit` (with `+UNCOMMITTED_CHANGES` if the tree was dirty) and `source_sha256` for every file under `src/`, `runner/`, `sandbox/` and `design/`; `sandbox.harness_sha256`; `design_materials.file_sha256` (includes the spec) | **Met** |
| 4 | Exact run commands and environment variables | `summary.json` `command` (the in-container command); `sandbox.runner_container_flags` / `artifact_container_flags` (every `--env` passed to the containers); `sandbox.host_invocation`: host `argv` (`runner/run_f18_container.sh development`), `cwd`, `docker_client`, and the host `environment` under the recorded allow-list `environment_policy` (every `OPENVEF_*` variable plus named docker CLI and locale variables, if set) | **Met.** The full host environment is deliberately not recorded: it can hold credentials. The allow-list names every variable that can change the broker script or the docker CLI |
| 5 | Per-fixture record: ID, descriptor SHA-256, actual disposition/stage/error class/diagnostic, expected, match | `results.jsonl`: `fixture_id`, `descriptor_sha256`, `actual` (four fields), `expected`, `status` (PASS = match, FAIL = mismatch), `note`; provisional block where applicable | **Met** |
| 6 | Raw run logs with timestamps | `run.log`: run metadata (with `run_started_utc`), then one line per fixture, each prefixed with an ISO 8601 UTC timestamp in milliseconds (written and flushed as the fixture finishes); `summary.json` `run_finished_utc` | **Met** |
| 7 | Results files and SHA-256 | `results.jsonl`, with its SHA-256 in `summary.json` `results_sha256`; `summary.json` itself is not hashed inside the run | **Met** for results; the summary's own hash is computable but not recorded |
| 8 | Every failed/errored/skipped fixture, with reason | `results.jsonl` `note` for every non-PASS; this run has 0 FAIL, 0 ERROR and 17 NOT_IMPLEMENTED (listed above), each with its blocking reason | **Met** |
| 9 | Isolation arrangement for LLM-generated code | artifact containers: no network, read-only root, all capabilities dropped, non-root, noexec tmpfs, limits, wall-clock kill; flags in each run's `artifact_container_flags`; [sandbox.md](sandbox.md); `tests/test_sandbox.py`, `tests/test_broker.py` (D-002, D-002a) | **Met** as built. Whether it is adequate as the security boundary for F16 is for the owners to decide (sandbox.md) |

**Also available to the auditor:**
- [traceability.md](traceability.md), [ambiguities.md](ambiguities.md),
  [pack-defects.md](pack-defects.md), [assistance-log.md](assistance-log.md);
- the unit tests in `tests/`, 28 files, run with `.venv/bin/python -I tests/<file>`;
- `evidence/container-tests-*`: logs of the whole suite inside the pinned image (D-017). Inspection evidence, not an F18 run.

**File 50 Python 3.11 Unicode tokenizer check (L555 (4)): recorded.** Run
`evidence/probe-file50-20261124T112645Z/` on the pinned image (CPython 3.11.18,
interpreter SHA-256 `92d7e40e…6b79`, image `sha256:565e5547…`). Results:
- the File 50 code block ran byte-for-byte;
- `℘ = 1` gives `ERRORTOKEN '℘' (1, 0)`;
- `a℘ = 1` gives `NAME 'a' (1, 0)`, then `ERRORTOKEN '℘' (1, 1)`;
- `ast.parse` accepts both;
- the scanner rejects both as `NON_ASCII_IDENTIFIER|…|column=1`, at the start of the
  complete identifier lexeme;
- Unicode in a STRING and in a COMMENT is not rejected.

This **matches the audit-time CPython 3.11.18 results** in File 54 (M55: "ERRORTOKEN `℘`
at (1,0)"; M56: "NAME `a` + ERRORTOKEN `℘`"), and it differs from the 3.13.5 exploratory
result in File 50, which emitted NAME. No difference from the audit-time results was
found. The audit used a different 3.11.18 binary (`/usr/bin/python3.11`, File 54 L35);
this run is on the pinned one.

## 4. Open items and owners

**Owner signatures and reviews (Krishika and Ayush together, unless noted)**

| Item | Owner | Reference |
|---|---|---|
| **Ayush ratification pending** (the single entry under D-008): Ayush Kumar Singh's agreement to every decision and approval Krishika signed alone, including the freeze package (`a955245`) and every decision recorded as awaiting his confirmation (D-001–D-023, DEV-001, DEV-002, A-001–A-006, A-013, A-014, A-015 case 2, A-042). Under D-008 these take effect now | Ayush | [ambiguities.md](ambiguities.md) D-008; [FREEZE-RECORD-2026-11-24.md](FREEZE-RECORD-2026-11-24.md) |
| Sign the overlap disclosure note's own owner-signature table (F1 in the package is approved) | owners | [fifo-benchmark-overlap-disclosure-DRAFT.md](fifo-benchmark-overlap-disclosure-DRAFT.md) |
| Itemised review of the readings approved under D-009 (A-007–A-012, A-013 tie, A-015–A-037, A-039, A-045–A-052, F15 case table): approved as decided, **not** reviewed item by item; A-031 withdrawn (D-012). Optional for the owners | an owner | [READINGS-REVIEW.md](READINGS-REVIEW.md); D-009 |
| Pack defects PD-01…PD-24 (settle, or accept the interim readings) | owners | [pack-defects.md](pack-defects.md) |
| M27: a corrected fixture in a future pack release (port manifest with widths, an executable predicate consistent with the frozen FIFO rules) | owners | PD-25; A-038 (revisited) |
| Disclosed for every audit: the original single-fixture-shape criterion is unmet by design (D-019 owner statement; five shapes M18, M19, M25, M26, M28 kept under D-013, as the fifth audit lists them) | owners (disclosure) | DEV-002; D-013; D-017; D-023 |
| How a SELF_REPORTED artifact is treated (A9-2 residual): **owner decision taken (D-020)** — F18 keeps the verdict with a visible label; confirmatory use reports the validity endpoint as measured (primary) and with every SELF_REPORTED artifact counted invalid (pre-registered sensitivity), plus the per-arm SELF_REPORTED count. Judged an honest disclosure policy by the fourth audit; the residual stays a disclosed limitation (D-023) | — (done) | D-020, D-023 |
| Review of A-057 (P11b depends on it): **approved as decided (D-020)** | — (done) | D-020 |
| AI audit sequence #1–#5: **complete, no open BLOCKER or MAJOR** (fifth audit CLEARED for D-022). Kept as disclosed limitations: A1-1-L1, the SELF_REPORTED residual, the wall-clock residuals in [DEVIATIONS.md](DEVIATIONS.md), and the fifth report's coverage limitations L-02–L-11 | — (done; limitations stay disclosed) | D-023 |
| Input contracts and outcomes for the 15 fixtures without one (PD-03, PD-04, PD-07, PD-26) | owners | D-013 |
| A-053 (approved, D-014) and the other historical readings were not re-examined by the fifth audit (its L-08); the passes resting on A-053 are listed in [traceability.md](traceability.md) | owners (disclosure) | D-014, A-053 |
| Draft pack corrections for M27, M36, M42, M47, M48, M50, M54, M58, PD-22 and PD-24: `proposals/v1.3.7/PROPOSED-CORRECTIONS-DRAFT.md` (DRAFT; needs a new independent document audit) | owners | PD-02, PD-03, PD-06, PD-22, PD-24, PD-25 |
| M48, M50, M54, M58: the change-class fields with no supporting Protocol sentence | owners | A-033, PD-02 |
| TechRxiv preprint: retrieve it, or record its access status; make the Charter and File 10 agree | owners | PD-24 |

**People still to be found**

| Item | Owner | Reference |
|---|---|---|
| Independent human mask reviewer: none available (DEV-001). Signing would end the deviation | owners to appoint if one becomes available; must not have authored the templates or the mask | L271; File 21 "Independent reviewer"; package §G |
| Independent human implementation auditor: none available (DEV-002). Five AI audits (OpenAI GPT-6) are saved in [reviews/](reviews/); the sequence is complete with no open BLOCKER or MAJOR (D-023). Not a human independent audit, so step (5) is not marked done | owners | L555 (5); [DEVIATIONS.md](DEVIATIONS.md) DEV-002; [AUDIT-BRIEF.md](AUDIT-BRIEF.md) |

**Human-written work (reserved by CLAUDE.md; Claude does not write it)**

| Item | Owner | Reference |
|---|---|---|
| Directed legal-input suite and reference driver (checklist item 14) | owners | L245, L415 |
| Hand-built FIFO control mutants (item 15), sufficient for F1–F15, including F5 and F10 | owners | Charter L74; L506, L514, L519 |
| F6/F17 control checkers and drivers (item 16); under D-007 also the F1–F5 and F7–F13 control drivers and checkers | owners | L489, L515; D-007; design/fifo/controls/README.md |
| Frozen L544 export script, mutation modes, mutant population, bounded-equivalence assumptions | owners | L544 |

**Work Claude can do on request (under D-005 or the build scope)**

| Item | Owner | Reference |
|---|---|---|
| Draft the remaining payload blocks (`[Execution envelope]`, `[Driver API]`, `[Trace schema]`, `[Checker contract]`) and the File 38 manifest (checklist items 2, 17), then run the assembler and clause-ID checks on them | Claude drafts; owners approve | D-005; File 31 L29–L30 |
| Compose and run the F1–F13 and F17 procedures from H1–H10 as the owner files arrive (harness built; F14, F15 run) | Claude; owners supply the artifacts | L555 (4); plan step 8 |
| If a mask reviewer signs: end DEV-001 and make a new pinned evidence run without its label | Claude | DEVIATIONS.md |
