# F1–F15 and F17 feasibility controls: plan (no code)

**For:** the owners (Krishika, Ayush Kumar Singh). **Prepared by:** Claude (Claude Opus
5.5, via Claude Code), 24 Nov 2026. **Status:** planning document. Nothing here is built,
run or passed. It decides no spec reading: interpretive questions are listed in §6 and
will go into [ambiguities.md](ambiguities.md) when the step that needs them is built.

## 1. Scope

**Pack text.** Protocol §17 runs from L504 to L531:
- L506 is the preamble;
- the table rows are F1–F15 at L510–L524, F16 at L525 and F17 at L526;
- L529 lists the F15 ledger assertions;
- L531 lists the critical gates.

The task named L506–L521; this plan uses the full range, because F12–F15 (L521–L524) and
F17 (L526) are part of the request.

> [02 L506] "The feasibility experiment uses the synchronous FIFO. Controls are hand-built engineering tests and do not count as confirmatory study evidence. F17 feasibility uses only hand-built FIFO control mutants. F16 is a mutant-blind LLM pilot and is not authorized until the current LLM-call gate passes independent document and implementation review; it runs before the final confirmatory packet/mutant freeze. F17 on the confirmatory MCY manifest occurs only after that freeze. F18 is a hand-built parser/prompt/assembly test and does not require an LLM call."

> [02 L531] "F2, F4, F5, F9, F15, F16, F17 and F18 are critical gates. A failure requires an arm-symmetric instrument correction and rerun of affected controls. Feasibility/pilot artifacts are never included in confirmatory analysis."

**Not in this plan:**
- **F16:** an LLM pilot. It is closed by the LLM-call gate (L506, L555 (6)).
- **F18:** built and run separately (see [AUDIT-READINESS.md](AUDIT-READINESS.md)).

**Open now:** only pre-freeze F17 with hand-built control mutants. Confirmatory F17 on
the MCY manifest is not open:

> [02 L555] "(4) After those prerequisites, only the limited hand-built FIFO feasibility scope may open: FIFO specification and mask-traceability rows first, then the hand-built harness/ledger, F1–F15, parser/assembler implementation and fixture-suite execution against hand-written fixtures on the pinned CPython 3.11 runtime, and F17 using only hand-built FIFO control mutants."

**Mutant set required by the Charter:**

> [01 L74] "- One null reference and a **hand-built set of distinct control mutants** sufficient to exercise the F1–F15 cases; this is not a one-mutant-only plan."

## 2. Who builds what

Each artifact below gets one of three labels.

| Label | Meaning | Basis |
|---|---|---|
| **(a) Claude** | Claude may build it: harness, ledger, classifier, runner, comparators, miter tooling, evidence records. Proposed values (N, timeouts, `k_null` for feasibility) are drafted as DRAFT under D-005 | CLAUDE.md Scope ("parser, assembler, harness, ledger and runner"); D-005 for proposed frozen values and trace schema |
| **(b) Owner** | Reserved to the owners by CLAUDE.md: hand-built control mutants, F6/F17 control checkers and drivers, the directed suite (with the reference driver, checklist item 14) | CLAUDE.md "Still human-written"; checklist items 14–16 |
| **(c) Owner decision** | A control driver or checker for F1–F5 or F7–F13. CLAUDE.md reserves only the **F6/F17** ones by name, so these are not covered either way | L506: "Controls are hand-built engineering tests" |

**Recommendation on (c): owners write them, as for F6/F17.** A known-answer control is
only worth something if it is independent of the instrument it tests. Claude builds the
harness, classifier and ledger, so Claude-written controls would test Claude's harness
with Claude's own expectations. If the owners want Claude to draft them instead, that is
an extension of D-005 and needs a recorded decision. Until then, Claude treats (c) as
owner-written and does not draft them.

F15 is the exception. Its "hand-built cases" are ledger input rows, not executable
artifacts, and their expected classes are fixed by the inclusion table at L370–L384.
Claude can transcribe them, with each expected value quoting its table row, so the owners
review a transcription, not a judgment. These are labelled (a), with owner review.

## 3. What exists today, and what is missing

**Exists (built for F18, L166 (7)–(11), on the DRAFT FIFO materials):**
- `sandbox/sim.py` and `sim_cocotb.py`:
  - harness-owned clock and scheduler;
  - output-first sampling;
  - per-step vector validation, including the legal-input predicate;
  - cycle cap and safe-idle;
  - heartbeat watchdog;
  - FST waveform.
- `src/openvef/simulation.py`:
  - RTL-versus-null comparison (`compare_runs`: raw, masked and next-input divergence);
  - the L334 timeout from three null runs;
  - a null-trace X/Z check.
- `src/openvef/trace.py`: frozen canonical trace bytes and SHA-256.
- `runtime.py` and `harness.py`: checker invocations in separate containers, return
  classification, null-repeat adjudication.
- `simulator_stages.export_null`: null export through `design/fifo/export_null.ys`, run
  twice per evidence run, hashes recorded.
- The pinned image: Yosys 0.71, MCY (pinned commit), Icarus 12.0, cocotb 2.1.0.

**Missing:**

| ID | Component (all label a) | Needed by |
|---|---|---|
| H1 | **Mutant target.** A manifest of hand-built mutants (format only; the content is owner-written). Each mutant is exported through the same frozen script, hashes are recorded, and the netlist runs as a third simulation target besides `rtl` and `null` | F4–F10, F12, F17 |
| H2 | **Pair runner and comparator (§8).** Null versus mutant with the same seed, reset, cap, safe-idle and watchdog. Records the first raw, first masked and first next-input divergence rows (mask predicate evaluated on the null rows, L273); output-first within a row; for truncated runs, whether a masked divergence was recorded before termination | F3–F12, F17 |
| H3 | **Pair classifier (§12).** Precedence 1–5, the 13 classes, `NP` subtypes (L392), integrity adjudication (L311), `INVALID_ARTIFACT_SLOT` | F5–F12, F15 |
| H4 | **Metrics and ledger (§13.1–§13.3).** `V_cd`, `T_i`, `X_i`, `E_i`, `S_i`, `S_i^optimistic`, `M_i`, NA rules, `U_i`, `U_i^X`, `E_i^trunc`, `J_exposure`, `J_detection` and optimistic and truncated variants, ratio-of-sums aggregation, and the executable identities of L405–L411 and L529 | F15 |
| H5 | **Mask-aware miter and bounded check (§11).** Null and mutant netlists in one wrapper, the mask applied with predicates taken from the null side, legal-input assumptions, the reset sequence, a bound N, and labels `NON_EQUIVALENT_WITHIN_N` / `BOUNDED_EQUIVALENT_N` / `UNDECIDED`, with counterexample length. Proposed tool: Yosys's built-in `miter` and `sat -seq N` (already in the image, so no new dependency). An external SMT solver via SymbiYosys would change the Dockerfile and needs owner approval (hard rule 3, D-004) | F4, F5 |
| H6 | **Counterexample replay.** Turns a miter counterexample into a fixed input schedule, replays it through the production harness on null and mutant, and checks the cycle of the first masked divergence | F4 |
| H7 | **Common-trace panel (§13.4).** Builds the `REACTIVE_RANDOM` and `DIRECTED` streams through the production harness: benign RTL and null traces, mutant traces, the `Q_ds` exposure set with invalid pairs excluded and counted, double evaluation on identical bytes, panel partition precedence, event flags and counts, ITT proportions and their sum to `V_cd` | F17 |
| H8 | **Control runner.** `runner/run_controls.py`, run through `runner/run_f18_container.sh`-style brokerage in the pinned image. One evidence directory per run with the same identity records as F18 (§5.3 items 1–9), and one record per control: setup, artifacts and hashes, observed, expected, PASS/FAIL, provisional flags | all |
| H9 | **Ordering probe.** Harness instrumentation recording, per row, the simulator time of the `ReadOnly` sample, the driver call and the drive phase, so F2/F10 can show the actual order (L223), not only the recorded fields | F2, F10 |
| H10 | **Determinism comparison.** Compares trace bytes exactly and the run records with the non-deterministic fields excluded by an explicit list (wall time, container names, temp paths, the FST header date). The list is a DRAFT addition to checklist item 11 | F1 |

## 4. Per-control plan

Each control gives:
- **Pack text:** verbatim, from Protocol §17;
- **Harness:** what the harness must do;
- **Artifacts:** what the control needs, with its label.

"Mutant" always means an owner-written hand-built control mutant (b). The "Required
behaviour" notes say what the pack needs a control to do. They are requirements, not
designs.

### F1 Determinism and checker null repeat

> [02 L510] "| F1 | Determinism and checker null repeat | Run one artifact on null netlist three times; run its checker twice in separate processes on the same immutable null trace | Traces match excluding explicitly non-deterministic metadata; both checker runs return identical `PASS` |"

**Harness:**
- run one artifact three times on the null netlist through the production harness;
- compare the three traces' canonical bytes (H10);
- run the checker twice in separate containers on the same frozen bytes;
- require identical `PASS`.

The DRAFT trace rows contain no non-deterministic field, so the trace comparison is
exact. The exclusion list applies only to run records and the waveform.

**Artifacts:**

| Artifact | Label |
|---|---|
| H8, H10 | a |
| One artifact (driver and checker). Natural choice: the reference driver (item 14) with the F6 correct checker | b (if those are used) or c |

### F2 Alignment

> [02 L511] "| F2 | Alignment | Driver echoes a registered output into next-cycle input | Row n records outputs after edge n and the driver's decision for edge n+1; consumed inputs agree with prior scheduled vector |"

> [02 L221] "The harness—not test code—owns the clock, scheduler and recorder. Ordering is mandatory: sample outputs first, invoke the driver second, record its next-input vector third, drive it before the next active edge. This prevents combinational outputs from being sampled after next inputs have already changed. For pair validity, compare each row's next-input vector after comparing that row's raw outputs. A next-input difference in the same row as the first raw output divergence is output-first; a difference in an earlier row makes the pair invalid. The consumed-input field is retained for audit and must agree with the prior row's scheduled input; the initial reset inputs are defined in the design pack."

**Harness:**
- record H9 timings;
- assert for every row:
  - (i) `inputs_consumed_at_edge_n` equals the prior row's `next_inputs_scheduled_for_edge_n_plus_1` (the first row against the reset inputs of the design pack);
  - (ii) the output snapshot in row n is sampled after edge n and before the driver call;
  - (iii) the vector the driver returns in row n is the one driven before edge n+1;
- with an echo driver, show that the echoed registered output from row n appears as the consumed input at edge n+1.

**Artifacts:**

| Artifact | Label |
|---|---|
| H8, H9, alignment assertions | a |
| Echo driver (copies a registered output, e.g. `full` or `rd_valid`, into a next-cycle input) | c |

Critical gate (L531).

### F3 RTL versus null

> [02 L512] "| F3 | RTL versus null | Run F1 artifact on RTL and null netlist | No masked divergence and no scheduled next-input divergence before first raw divergence |"

**Harness:** existing `compare_runs` on the F1 artifact; report the first raw, masked and
next-input divergence rows.

**Artifacts:**

| Artifact | Label |
|---|---|
| `compare_runs` (exists), H8 | a |
| F1 artifact | as F1 |

### F4 Miter/simulation agreement

> [02 L513] "| F4 | Miter/simulation agreement | Replay mask-aware miter counterexample in simulator | Masked divergence appears at predicted cycle |"

> [02 L291] "Build the miter with the same observation mask as the trace comparator and with the same reset sequence and legal-input assumptions from the design specification. Freeze those assumptions with the design pack."

**Harness:**
- H5 on a mutant that is non-equivalent within N under the mask;
- H6 replay;
- assert that the simulator's first masked divergence is at the counterexample's cycle;
- show that the miter's legal-input assumptions equal FIFO-042's executable predicate (§6 Q5).

**Artifacts:**

| Artifact | Label |
|---|---|
| H5, H6, H8; proposed N, solver and timeout (DRAFT, L299 TO FREEZE) | a |
| Mutant **M-exposed**: masked-observable divergence under legal inputs within N | b |

Critical gate.

### F5 Masked don't-care

> [02 L514] "| F5 | Masked don't-care | Mutant changes FIFO data only while valid is low, where spec says data is don't-care | Raw divergence but no masked divergence; miter agrees through fixed N |"

**Harness:**
- pair run (H2) shows raw divergence with no masked divergence;
- H5 returns `BOUNDED_EQUIVALENT_N` under the mask through the fixed N.

**Artifacts:**

| Artifact | Label |
|---|---|
| H2, H5, H8 | a |
| Mutant **M-dontcare**: changes `rd_data` only in rows where the null trace has `rd_valid = 0` (the DRAFT primary mask's don't-care window). It must not change `rd_valid` | b |
| A driver that reaches the window | b (reference driver) or c |

Critical gate. The don't-care window must be in the signed mask (L271), so F5's result
stays provisional until the mask is signed.

### F6 Pair classes

> [02 L515] "| F6 | Pair classes | Hand-built correct checker, always-PASS checker, and non-exposing driver | `DETECTED`, `PND`, `NP` respectively |"

**Harness:** H2 and H3. Expected classes:
- correct checker with exposing driver on M-exposed: `DETECTED`;
- always-PASS checker on the same pair: `PND`;
- non-exposing driver on M-exposed: `NP`.

**Artifacts:**

| Artifact | Label |
|---|---|
| H2, H3, H8 | a |
| Correct checker, always-PASS checker, exposing driver, non-exposing driver | b (item 16) |
| M-exposed | b |

### F7 Checker stricter than mask

> [02 L516] "| F7 | Checker stricter than mask | Checker compares data during an explicit don't-care window | `ANOMALY_CHECKER_STRICTER_THAN_MASK` |"

**Harness:** H2 and H3 on M-dontcare (raw-only divergence); expected
`ANOMALY_CHECKER_STRICTER_THAN_MASK`.

**Artifacts:**

| Artifact | Label |
|---|---|
| H2, H3, H8 | a |
| M-dontcare | b |
| Stricter checker. It must pass both null runs (to be a valid artifact, L247) and fail on the M-dontcare trace | c |

### F8 Pipeline anomaly

> [02 L517] "| F8 | Pipeline anomaly | Checker returns FAIL on a trace identical to null | `ANOMALY_PIPELINE_OR_NONDETERMINISM` |"

> [02 L311] "**Integrity adjudication for `ANOMALY_PIPELINE_OR_NONDETERMINISM`.** A predeclared harness/trace-integrity failure (for example, replay hash mismatch, malformed recorder output, row alignment failure or untrusted trace serialization) reclassifies the pair as `INVALID_PAIR` under precedence rule 1. A checker-attributable failure (for example, different checker verdicts on byte-identical complete traces) remains in `T_i` and is counted as a checker/pipeline anomaly, not exposure or detection. If the cause cannot be determined from predeclared integrity evidence, classify conservatively as `INVALID_PAIR`. Report harness/trace-integrity and checker-attributable counts separately; do not adjudicate based on prompt arm or desired metric direction."

**Harness:** H2 and H3. The checker's `FAIL` on a mutant trace byte-identical to the null
trace it passed is checker-attributable, so the pair stays in `T_i` as
`ANOMALY_PIPELINE_OR_NONDETERMINISM`. A harness-integrity failure goes to `INVALID_PAIR`
instead, and the two counts are reported separately.

**Feasibility problem (§6 Q2):**
- A valid artifact's checker passes the null trace twice.
- A mutant with no raw divergence and a deterministic driver gives byte-identical trace
  bytes and identical metadata.
- So a deterministic checker cannot return `FAIL` on it. Only a nondeterministic checker
  can, and only by chance.

**Proposal:**
- (1) A classifier-level known-answer test with recorded verdicts (label a). It proves the
  classification rule.
- (2) An end-to-end attempt with a nondeterministic checker over a fixed, predeclared
  number of trials. Every trial is recorded, and the control is reported as observed or
  not observed.

**Artifacts:**

| Artifact | Label |
|---|---|
| H3 known-answer test, H8 | a |
| Mutant **M-silent**: differs structurally but gives no raw output divergence under the driver used (the null netlist itself does not qualify: a mutant must be distinct) | b |
| Nondeterministic checker | c |

### F9 Invalid pair

> [02 L518] "| F9 | Invalid pair | Driver reads unseeded entropy; rerun with harness-owned seed | First `INVALID_PAIR`; seeded version obeys paired input schedule |"

> [30 L20] "- `import random` is permitted only for constructing a local `random.Random(seed)`. Any direct attribute access on the module name `random` other than `random.Random` is rejected, including module-global PRNG calls and `random.SystemRandom`. Static detection may be bypassed by aliasing (`r = random; r.random()`) or `getattr`; disclose this limitation. Such bypasses are not statically claimed as detected and are caught only if they cause a paired next-input divergence at runtime. `from random import ...` is not permitted by the general from-import rule. The artifact must not call OS-entropy APIs."

**Harness:**
- run the pair with a driver that draws from the module-global PRNG through an alias,
  which static checks do not detect (File 30 L20);
- null and mutant run in separate containers, so their global PRNG states differ;
- expect `INVALID_PAIR` (precedence 1);
- rerun the same driver with only a local `random.Random(seed)`, and expect identical
  next-input schedules up to the first raw divergence.

A direct `random.random()` is rejected statically (`GLOBAL_RANDOM_USE`) and would never
reach the run. OS entropy is blocked by the sandbox.

**Artifacts:**

| Artifact | Label |
|---|---|
| H2, H3, H8 | a |
| Unseeded and seeded drivers | c |
| A mutant (any) | b |

Critical gate. The draw must change a next-input decision before the first raw
divergence, or the result is not `INVALID_PAIR`. With a pseudo-random choice per cycle
from cycle 0, this is near-certain, but it is probabilistic: record the trial.

### F10 Same-row tie

> [02 L519] "| F10 | Same-row tie | Mutant changes `full`; driver changes next input based on sampled output | Pair is valid under output-first sampling rule |"

**Harness:**
- H2 with H9;
- the mutant changes `full` at row n;
- the driver reacts in row n's next-input decision;
- the pair is valid (same-row divergence is output-first, L221, L265) and is classified by the normal classes, not `INVALID_PAIR`.

**Artifacts:**

| Artifact | Label |
|---|---|
| H2, H3, H8, H9 | a |
| Mutant **M-full**: changes `full` | b |
| Driver that conditions its next input on sampled `full` | c |

### F11 Cycle cap/timeout

> [02 L520] "| F11 | Cycle cap/timeout | Driver completes at cap vs watchdog fires | Cap is normal incomplete-driver termination; watchdog is timeout |"

> [02 L227] "All artifacts use the same design-specific fixed cycle cap. If a driver returns `COMPLETE`, the harness records `driver_completed=true` and supplies the fixed safe-idle vector for the remaining cycles. The checker evaluates the entire trace through the cycle cap. There is no per-artifact alternative completion policy. If the driver has not completed at the cap, record `driver_completed=false`; reaching the cap is a normal end, not a timeout."

> [02 L334] "- Proposed timeout: `T_timeout = max(5 × median(null-netlist wall time over 3 runs for the same artifact/design), 2 seconds)`. Validate during FIFO feasibility; freeze or amend before confirmatory generation."

**Harness (most of this exists):**
- a driver that never returns `COMPLETE` runs to the cap, records `driver_completed=false` and a complete trace, and the checker runs;
- a driver whose `step` loops forever triggers the watchdog: `TIMEOUT_*`, truncated trace, no checker run;
- record the L334 timeout derivation.

**Artifacts:**

| Artifact | Label |
|---|---|
| Classifier mapping, H8; L334 timeout (exists) | a |
| Drivers "runs to cap" and "infinite loop" | c |

### F12 Driver/simulator error

> [02 L521] "| F12 | Driver/simulator error | Driver converts X output to integer on mutant | Driver/simulator error, not detection; truncated trace excluded from `T_i` |"

> [02 L328] "A driver/simulator error or timeout produces a truncated trace and is excluded from the primary complete-trace conditional diagnostics. A checker error occurs only after a complete trace and is included in the complete-trace denominator. Checkers are never run on truncated traces. `CHECKER_ERROR_AFTER_MASKED_DIVERGENCE` counts as exposed for `E_i`, but as not detected for `S_i` and `J_detection`. Truncated execution after a recorded masked divergence is excluded from the primary exposure numerator and reported in a separate one-sided sensitivity analysis. Invalid artifacts are represented by an `INVALID_ARTIFACT_SLOT` ledger state for every scheduled mutant combination."

**Harness:**
- the driver raises on the mutant (`int()` of an `X` character);
- class `DRIVER_SIM_ERROR_NO_MASKED_DIVERGENCE` or `…_AFTER_MASKED_DIVERGENCE`, depending on whether a masked divergence was recorded first;
- the truncated pair is excluded from `T_i` and counted in `U_i` (and `U_i^X`).

**Artifacts:**

| Artifact | Label |
|---|---|
| H2, H3, H4, H8 | a |
| Mutant **M-x**: drives `X` on a public output (e.g. from an undriven net in the netlist), outside the null-trace X/Z rule, which applies to null runs only (L241) | b |
| Driver that converts that output with `int(…, 2)` | c |

### F13 Checker non-interference

> [02 L522] "| F13 | Checker non-interference | Run checker in separate process on trace file | Checker cannot access simulator handles or alter trace |"

> [02 L284] "The checker is an isolated synchronous function `check_trace(trace, metadata)` run in a separate process after simulation on an immutable serialized trace. It receives no simulator objects, live DUT handles, RTL source, mutant identity, driver seed, stimulus list, observation mask, reference model/API or expected-output table. `metadata` contains exactly: `design_id` (string), `spec_version_sha256` (64-character lowercase hexadecimal string), `trace_schema_version` (string), `cycle_cap` (positive integer), `reset_release_cycle` (non-negative integer) and `trace_integrity_status` (literal `VALID`). It excludes the driver seed and stimulus list."

**Harness:**
- checker in its own container (exists), receiving only the decoded value of the frozen bytes;
- re-hash the stored trace bytes after each invocation and assert they are unchanged;
- assert the container has no simulator process, no simulator library handle, no writable mount of the trace, and no network;
- record the container flags.

**Artifacts:**

| Artifact | Label |
|---|---|
| Re-hash and assertions, H8 | a |
| Adversarial checker: mutates its `trace` argument; attempts to import `cocotb`, open the trace file, write files | c |

### F14 Export repeatability

> [02 L523] "| F14 | Export repeatability | Export null netlist twice with same pinned scripts | Stable null hash, top module and ports |"

> [02 L233] "The null-mutant netlist is generated from the original RTL by exactly the same synthesis/export script, tool versions and top-level interface as the mutant netlists, with no mutation applied. Export must preserve top module name and public ports. Run the export twice and compare null-netlist hashes."

**Harness:** exists (`export_null` twice per evidence run). To add:
- an explicit F14 record comparing top module name and public port list (names, directions, widths) between the RTL and both exports;
- the hash comparison.

**Artifacts:**

| Artifact | Label |
|---|---|
| F14 record, H8 | a |
| The export script | a, DRAFT under D-005; the owners freeze it (L544) |

The result is provisional until the script is frozen.

### F15 Classifier, ledger and metric identities

> [02 L524] "| F15 | Classifier, ledger and metric identities | Feed hand-built cases for every outcome; include invalid artifact slots and a zero-valid-slot arm/design; verify complete-trace categories, `T_i`, `X_i`, H2 denominators and aggregation identities | Exactly one ledger class for every scheduled slot × mutant; total = `|G_cd|×|M_d|`; for each valid artifact, `|T_i|+|U_i|+|INVALID_PAIR_i|=|M_d|`; for each arm/design, valid-slot pair rows plus invalid-slot ledger rows equal `|G_cd|×|M_d|`; `X_i≤|T_i|`, `DET_i≤X_i`, and `|U_i^X|≤|U_i|`; `X_i` includes only DET+PND+checker-error-after-exposure; `E_i`/`S_i` and optimistic crash sensitivities match definitions; `J_exposure` and `J_detection` identities hold, including zero-valid-slot behavior; truncated-exposure sensitivity is one-sided; miss-composition identity tested only on `C_i=NP+PND+DET`; panel partition sums equal `V_cd` separately for each stream. |"

> [02 L529] "F15 ledger assertions must include: (1) per valid artifact, `|T_i| + |U_i| + |INVALID_PAIR_i| = |M_d|`; (2) per arm/design, valid pair rows plus `INVALID_ARTIFACT_SLOT` rows equal `|G_cd|×|M_d|`; (3) `X_i≤|T_i|`, `DET_i≤X_i` and `|U_i^X|≤|U_i|`; (4) on the normal subset `C_i`, `NP_i+PND_i+DET_i=C_i≤|T_i|` and the miss-composition identity holds only using `C_i`-restricted quantities; and (5) for each stream/design/arm, the three panel partition proportions sum to `V_cd`."

> [02 L411] "These identities and the full pair-class ledger must be executable F15 assertions. F15 must also include a zero-valid-slot case: `J_exposure` and `J_detection` remain zero because their scheduled-slot numerators are zero; do not evaluate the right-hand conditional-mean expressions above, which are undefined with no valid slots. Report that no valid artifacts were observed."

**Harness:**
- H3 and H4;
- a case table with at least one case per outcome class (13 pair classes plus `INVALID_ARTIFACT_SLOT`, and both `NP` subtypes);
- arms or designs with invalid slots, including one with zero valid slots;
- assert every identity listed at L524 and L529, plus L405–L409, and that `J_*` is zero with the right-hand side not evaluated when there are no valid slots (L411);
- property-style checks over generated ledgers in addition to the hand-built cases.

**Artifacts:**

| Artifact | Label |
|---|---|
| H3, H4, identity assertions, case table transcribed from L370–L384 with each expected value quoting its row | a (owner review of the case table) |

Critical gate. **F15 can be built and run now:** it needs no simulator and no owner
artifact.

#### Analysis rule — SELF_REPORTED artifacts in the validity endpoint (D-020)

Owner decision D-020 (confirmatory use; no pack rule changed). An artifact is classified
`PROVEN` or `SELF_REPORTED` by `src/openvef/runtime_basis.py` (D-019): `SELF_REPORTED` means the
runtime return-type and post-execution signature checks rest on the artifact process's own report,
which it could forge (docs/sandbox.md "Runtime checks"). For the confirmatory validity endpoint:
- **Primary:** validity is taken as measured — a `SELF_REPORTED` artifact that the runtime checks
  accept is counted valid, like any other.
- **Pre-registered sensitivity:** recompute the validity endpoint with **every `SELF_REPORTED`
  artifact counted invalid** (an `INVALID_ARTIFACT_SLOT` for every scheduled mutant combination,
  as L529 (2) requires for invalid artifacts). Report it beside the primary.
- Report the **count of `SELF_REPORTED` artifacts per arm** (and design) with both.

This is confirmatory-analysis guidance only; F18 (above) keeps each fixture verdict and attaches the
visible `SELF_REPORTED (D-020)` label. F16/F17 confirmatory analysis is not authorized yet, so this
rule is recorded for when it is, and belongs in the frozen analysis plan when that is written.

### F17 Common-trace panel controls (pre-freeze feasibility only)

> [02 L526] "| F17 | Common-trace panel controls and freeze ordering | Pre-freeze feasibility F17 uses only hand-built FIFO control mutants, not the confirmatory MCY manifest. Build separate legal `REACTIVE_RANDOM` and `DIRECTED` streams through the production harness; run RTL and null benign traces; repeat each checker twice on identical benign and mutant trace bytes; exclude paired-input/integrity-invalid corpus pairs from `Q_ds`. Confirmatory F17 is run only after F16/re-pilots and the complete authoring packet, directed suite, mask and analysis plan are frozen and hashed, before any confirmatory panel mutant trace is scored by an LLM checker. | Correct reference checker: compatible and detects every exposed case; always-PASS: compatible with zero sensitivity; always-FAIL: `PANEL_FALSE_ALARM`; stimulus-literal: false alarm on at least one distinct legal benign trace; crashing checker: `PANEL_ERROR`; stricter-than-mask checker: `PANEL_STRICTER_THAN_MASK_EVENT`, not detection; nondeterministic checker: `PANEL_ERROR`. Mutant-trace errors/disagreements count as `PANEL_ERROR_EVENT`, not detection, but do not change the benign-trace compatibility partition. Report event counts separately; `PANEL_ERROR`, `PANEL_FALSE_ALARM` and `PANEL_COMPATIBLE` partition proportions sum to `V_cd` within each stream/design/arm. |"

> [02 L489] "| Panel known-answer controls | reference, always-PASS, always-FAIL, stimulus-literal, crashing, stricter-than-mask and nondeterministic checkers | Validate F17 |"

> [02 L437] "**Streams and corpus validity.** `REACTIVE_RANDOM` and `DIRECTED` are separate streams and are analyzed separately; `k_null` applies only to distinct legal reactive-random seeds. Exclude any corpus null/mutant pair that violates the paired-input or trace-integrity rule from `Q_ds` at corpus freeze and report the excluded count by stream/design. A checker that returns `FAIL` on a mutant trace byte-identical to a benign null trace it passed, or produces inconsistent verdicts on repeated evaluation of identical trace bytes, generates a `PANEL_ERROR_EVENT`, not a detection. Add known-answer controls for a stricter-than-mask checker and a nondeterministic checker."

**Harness (H7):**
- `REACTIVE_RANDOM` stream over feasibility seeds (proposed DRAFT count; `k_null=20` is the planning value, L486);
- `DIRECTED` stream from the owners' directed suite;
- benign RTL and null traces per scenario, kept only when the RTL-versus-null masked-equivalence and legal-input controls pass;
- mutant traces for every hand-built control mutant;
- `Q_ds` with invalid pairs excluded and the exclusion counted;
- each checker run twice on identical bytes for every benign and exposed mutant trace;
- panel partition precedence (L419–L421), separate event counts, the `PANEL_ERROR_EVENT` rules (L435, L437), `PANEL_STRICTER_THAN_MASK_EVENT`, ITT proportions summing to `V_cd`, and `|Q_ds|=0` giving NA.

Expected results (L526):

| Checker | Expected |
|---|---|
| Correct reference | compatible; detects every exposed case |
| Always-PASS | compatible; zero sensitivity |
| Always-FAIL | `PANEL_FALSE_ALARM` |
| Stimulus-literal | false alarm on at least one distinct legal benign trace |
| Crashing | `PANEL_ERROR` |
| Stricter-than-mask | `PANEL_STRICTER_THAN_MASK_EVENT`, not detection |
| Nondeterministic | `PANEL_ERROR` |

**Feasibility notes:**
- **Nondeterministic checker:** can be built only through the alias bypass of global
  `random`. The sandbox fixes `PYTHONHASHSEED=0`, and the import allow-list excludes
  `time` and `os`, so clocks and OS entropy are unavailable. With
  B benign traces evaluated twice, a fair-coin checker escapes detection with probability
  2^-B, so it is reliable but not certain. Record it as such.
- **Stimulus-literal checker:** needs at least two distinct legal benign traces per stream.
- **Stricter-than-mask:** needs M-dontcare in the mutant set.

**Artifacts:**

| Artifact | Label |
|---|---|
| H7, H8; proposed feasibility seed count (DRAFT) | a |
| The seven known-answer checkers; the reactive-random driver; the directed suite and reference driver (item 14) | b (items 14, 16) |
| The control mutants (M-exposed, M-dontcare, M-full, and any others) | b (item 15) |

Critical gate. Confirmatory F17 stays closed.

## 5. Owner-written artifacts, consolidated

The behaviours below are what the controls above require. The owners decide the actual
designs.

| Item | Behaviour required | Used by |
|---|---|---|
| M-exposed | masked divergence under legal inputs, within N | F4, F6, F17 |
| M-dontcare | changes data only where the mask's predicate (null `rd_valid`) is 0 | F5, F7, F17 |
| M-full | changes `full` | F10 |
| M-x | produces X on a public output | F12 |
| M-silent | distinct from null, but no raw divergence under the F8 driver | F8 |
| F6 set | correct checker, always-PASS checker, exposing and non-exposing drivers | F6 (and F1/F3 if reused) |
| F17 set | 7 known-answer checkers; reactive-random driver | F17 |
| Item 14 | reference driver; directed legal-input suite | §7a preflight, F17 `DIRECTED`, possibly F1/F3/F5 |
| (c) set, if owner-written | echo driver (F2); stricter checker (F7); nondeterministic checker (F8); unseeded and seeded drivers (F9); `full`-reactive driver (F10); cap and infinite-loop drivers (F11); X-converting driver (F12); adversarial checker (F13) | F2, F7–F13 |

**Charter L74 requires a set of distinct mutants. The one-mutant-only plan is excluded.**
One mutant may serve several controls, but at least M-exposed and M-dontcare must be
distinct.

## 6. Interpretive questions

Each of these will be entered in [ambiguities.md](ambiguities.md) and decided under the
standing delegation when its step is built. The readings shown are proposals, not
decisions.

| # | Question | Pack text | Proposed reading |
|---|---|---|---|
| Q1 | Are hand-built control mutants RTL edits passed through the frozen export script, or hand-edited netlists? | L233 (mutant netlists use the same export script as the null); Charter L74 ("hand-built") | Hand-written RTL or netlist edits, each exported by the same frozen script, so the top module and ports are guaranteed and hashes recorded (L233). Owners choose the authoring form |
| Q2 | How can F8 occur deterministically? | L517 with L247 and L311 | It cannot with a valid deterministic checker. Use the classifier-level known answer plus a recorded, bounded end-to-end attempt (see F8) |
| Q3 | Which "explicitly non-deterministic metadata" does F1 exclude? | L510, L551 | None in the trace rows; an explicit list for run records and the waveform (H10), added to the DRAFT trace schema (item 11) |
| Q4 | What does "miter agrees through fixed N" mean (F5)? | L514, L293–L295 | `BOUNDED_EQUIVALENT_N` under the same mask and legal-input assumptions, with N the proposed bound |
| Q5 | How is "the same legal-input assumptions" (L278, L291) shown, when the comparator uses FIFO-042's Python predicate and the miter needs Verilog or SAT assumptions? | L278, L291 | Generate both from one source if possible; otherwise check them exhaustively against each other over all input and occupancy combinations (feasible at the FIFO's widths), and record the result |
| Q6 | Is the FIFO's "valid" in L514 `rd_valid`? | L514 | Yes, as named in the DRAFT spec and mask; the owners confirm when they freeze the mask |
| Q7 | For F12, does an X on a mutant output under the production harness reach the driver as the character `X`? | L223, L512, L521 | Yes: the DRAFT trace keeps four-state strings and `step` receives the same snapshot. Confirm in the build |

Note: [fifo-owner-checklist.md](fifo-owner-checklist.md) item 17 still says "CLAUDE.md
reserves authoring-packet text to the owners". D-005 changed that. The line is stale and
should be corrected separately.

## 7. Proposed build order

Order rule: build first what needs no owner artifact and closes a critical gate. Then
build the shared pair machinery, so each owner artifact can be run as soon as it arrives.

| Step | Work | Label | Unblocks | Needs from owners |
|---|---|---|---|---|
| 1 | H3 classifier, H4 metrics and ledger, F15 case table and identity assertions; unit tests | a | **F15 (critical): runnable end to end** | review of the case table |
| 2 | H8 control runner and evidence format (pinned image, same identity records as F18) | a | every control's evidence | — |
| 3 | F14 record (top module, ports, two hashes) | a | F14 (provisional until the export script is frozen) | freeze of the export script |
| 4 | H9 ordering probe and alignment assertions; H10 determinism comparison; F13 re-hash and isolation assertions | a | F1, F2, F3, F13 machinery | the (c) decision; F1/F2/F13 artifacts |
| 5 | H1 mutant manifest format and export path; H2 pair runner and comparator | a | F5–F12 machinery | mutants (item 15) |
| 6 | H5 miter and bounded check; Q5 assumption equivalence; H6 replay; proposed N, solver and timeout (DRAFT) | a | F4, F5 (critical) | M-exposed, M-dontcare; approval if a solver dependency is wanted |
| 7 | H7 panel corpus and partition; proposed feasibility seed count (DRAFT) | a | F17 (critical) | items 14, 15, 16 |
| 8 | Evidence runs for each control as its owner artifacts arrive; traceability rows; AUDIT-READINESS update | a | F1–F15, F17 results | all of the above |

Steps 1–3 can start now. Steps 4–7 can be built and unit-tested on synthetic inputs now,
but their control results wait for owner artifacts.

**Status of results.** Every control result depends on DRAFT materials (spec, RTL, export
script, mask, trace schema, proposed values). Such results are provisional, like the 10
provisional F18 passes, until:
- the owners freeze those materials;
- an independent human signs the mask;
- the readings they depend on are reviewed.

A result that depends on a Claude-decided reading is marked as such in
[traceability.md](traceability.md) (CLAUDE.md, standing delegation).

## 8. Decisions needed from the owners

1. **(c) controls:** owner-written (recommended), or an explicit D-005 extension letting
   Claude draft them?
2. **Mutant authoring form** (Q1) and the minimum mutant set in §5 (item 15).
3. **Miter tool:** Yosys built-in `sat` (no new dependency, proposed), or SymbiYosys with
   an external solver (Dockerfile change; owner approval).
4. **Who writes F1's artifact:** the reference driver (item 14) with the F6 correct
   checker, or a separate (c) artifact?

## 9. Build status (24 Nov 2026, after D-007)

**Owner decisions:** D-007 (Krishika, 24 Nov 2026; Ayush's confirmation pending) answers
§8:
1. The (c) controls are owner-written.
2. Control mutants are RTL edits of `ovf_fifo.v`.
3. The miter uses Yosys's built-in `sat`.
4. F1 reuses the reference driver with the F6 correct checker.

The owner-written files are listed in
[design/fifo/controls/README.md](../design/fifo/controls/README.md). None exists yet.

| Item | Status |
|---|---|
| Step 1 — H3, H4, F15 | Built; F15 **PASS, provisional** in `evidence/controls-20261124T151740Z`. Contents: 16 pair cases, 84 known answers, 88 scenario identities, 34,159 identities over 300 random ledgers, and the inclusion table matched against L372–L384. The case table awaits owner review |
| Step 2 — H8 control runner | Built (`runner/run_controls.py`; `runner/run_f18_container.sh <class> controls`) |
| Step 3 — F14 record | Built; **PASS, provisional** (DRAFT export script and RTL; A-052) |
| H1 mutants | Loader and export path built; waiting for the owners' mutants |
| H2 pair runner | Built; the sandbox now keeps rows recorded before a watchdog kill (A-046–A-048) |
| H5/H6 miter and replay | Built; on TEST-ONLY toy designs it finds the shortest counterexample, the replay agrees in the simulator, and a don't-care variant is `BOUNDED_EQUIVALENT_N` (A-045) |
| H7 panel | Built; synthetic tests (A-049, A-050) |
| H9/H10 ordering probe, alignment, determinism | Built; checked on real toy-design runs in the sandbox (A-051) |
| Step 8 — compose and run F1–F13, F17 | F1 and F3 composed (D-036, 28 Nov 2026); they run when the reference driver and the F6 correct checker exist. The rest: not started, needs the owner files. The runner reports these controls `BLOCKED_OWNER_ARTIFACTS`; once a control's files exist and its procedure is not yet composed, it reports `NOT_WIRED`, never a pass |

**§6 questions:**
- Q1: settled by D-007.
- Q2: unchanged (F8 plan).
- Q3: A-051.
- Q4: the miter's `BOUNDED_EQUIVALENT_N` label.
- Q5: A-045. The assumption is generated from the spec's own predicate, so there is no
  hand translation.
- Q6: A-050.
- Q7: still open, to be confirmed when M-x exists.
