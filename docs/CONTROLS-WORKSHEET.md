# Worksheet: owner-written files for controls F1–F13 and F17

**For:** Krishika (owner), who writes these files by hand. **Prepared by:** Claude (Claude Opus 5.5, via Claude Code),
28 Nov 2026, at Krishika's request.

**Superseded for authorship by D-039 (Krishika, 28 Nov 2026).** Claude Code now writes these files under deviation
DEV-005 "AI-written controls" (`docs/DEVIATIONS.md`). The requirements below still apply; the prose-only paragraph that
follows describes the earlier rule.

**Prose only.** Sign-off Pack Part 2 row 5 says "Claude may suggest changes in prose only". This worksheet therefore
gives no code, no pseudocode and no file skeletons. Pack text is quoted as text. Where this worksheet says what a file
must *do*, the requirement comes from the pack or from the harness slot list. How the file does it is the owner's
design.

**Sources:**
- the adopted v1.3.7 pack (`baseline-v1.3.7/OpenVEF_Planning_v1_3_7/`; Protocol = File 02, Parser and Execution
  Contract = File 30; line numbers as in the pack);
- [F1-F17-plan.md](F1-F17-plan.md);
- [design/fifo/controls/slots.json](../design/fifo/controls/slots.json), the list the runner checks, and its
  [README](../design/fifo/controls/README.md).

Every slot path below is relative to `design/fifo/controls/`.

**Current status:** in `controls-20261128T111046Z`, F1–F13 and F17 are `BLOCKED_OWNER_ARTIFACTS`, and no slot file
exists yet. Once all of a control's files exist, the runner reports `NOT_WIRED` until its procedure is composed
(plan §9, step 8). A file's existence never makes a control pass.

**Results stay provisional.** Every control result depends on DRAFT FIFO materials (spec, RTL, export script, mask,
trace schema, proposed values; D-005). Those results are provisional until the owners freeze the materials. The mask
is cleared only under DEV-001 ("cleared under DEV-001 (non-independent review saved)").

---

## 1. The interfaces every file must follow

### 1.1 Drivers (`*.py` under `drivers/`)

The same contract as an LLM-authored `driver.py`. Protocol L212: "The same API and instructions are given to human and
LLM authors."

- **Calling model.** Protocol L208: "The harness owns the clock and scheduler. The module exposes `create_driver(seed)`;
  the harness calls it exactly once to obtain a `Driver`. The `Driver.step(cycle_index, outputs_after_edge)` method is
  invoked once per active cycle. Its first call is after reset release, with `cycle_index=0` and the public-output
  snapshot sampled after the reset-release active edge. Each later call receives the most recent post-edge snapshot and
  the next integer cycle index. It returns either:". L209–L210 complete it: "a complete next-cycle input dictionary; or"
  / "`COMPLETE`, after which the harness drives safe-idle inputs until the fixed cycle cap."
- **What the file may contain.** File 30 L35: "exactly one module-level class named `Driver` is allowed; no helper or
  nested classes are allowed. `Driver` has no decorators, no metaclass keywords, and either no explicit base or the
  single base `object`. Its body may contain one docstring, literal-only class constants and exactly one synchronous
  undecorated instance method named `step`; it must not define `__init__`, any other method or any nested class.
  Exactly one module-level synchronous undecorated function named `create_driver` must exist. It has exactly one
  required positional-or-keyword parameter named `seed`, not positional-only, with no default, variadic, keyword-only
  or extra parameters. `Driver.step` has exactly three required positional-or-keyword parameters named `self`,
  `cycle_index`, `outputs_after_edge`, with no default, variadic or keyword-only parameters. … The factory constructs
  `Driver()` and may assign instance attributes after construction. … `create_driver(seed)` must return an instance of
  the module's `Driver` class."
- **Module body.** File 30 L52: "Module-level executable statements, control flow, calls, comprehensions, non-literal
  assignments and side effects are prohibited. Every `async def` is prohibited at every lexical depth".
- **Return value.** File 30 L50: "`step` returns either the exact string `COMPLETE` or a complete dictionary whose keys
  are exactly the top-level input-port names in the port manifest. Each value is a string of exactly that port's
  declared width, containing only `0` and `1`; X/Z, missing keys, extra keys, wrong widths and inputs that violate the
  legal-input rules are invalid."
- **Behaviour rules.** Protocol L212: "Drivers must not create free-running Cocotb coroutines, wait on `Timer`/edges,
  own the clock, inspect internal signals, access simulator handles directly, use more than one drive per cycle, or
  obtain unseeded entropy. … The harness calls `create_driver(seed)` exactly once and does not seed global `random`;
  generated driver code must use a local `random.Random(seed)` instance."
- **Imports.** File 30 L74: "The only allowed imported Python standard-library module roots are `__future__`,
  `collections`, `copy`, `functools`, `itertools`, `json`, `math`, `operator`, `random`, `re`, `statistics` and
  `typing`." The same line also says: "`import random` is permitted only to construct a local `random.Random(seed)`
  instance". It prohibits "`open`, filesystem access, network access, environment access, wall-clock access, OS-entropy
  APIs" and says "AST references to the names `__import__`, `eval`, `exec`, `compile` or `open` are prohibited". Every
  identifier must be ASCII.
- **FIFO specifics** (DRAFT materials, README §2):
  - `outputs_after_edge` has the keys `almost_full`, `empty`, `full`, `rd_data` and `rd_valid`. Each value is an
    MSB-first string that may contain `0`, `1`, `X` and `Z`.
  - The input keys are `wr_en` (1 bit), `wr_data` (8 bits) and `rd_en` (1 bit). `rst` is harness-owned and is not a key.
  - The cycle cap is 64 (DRAFT).
  - A write while the sampled `full` is 1, without a read, breaks FIFO-042 and ends the run as `ILLEGAL_PROTOCOL_STATE`.

### 1.2 Checkers (`*.py` under `checkers/`)

- **Calling model.** Protocol L284: "The checker is an isolated synchronous function `check_trace(trace, metadata)` run
  in a separate process after simulation on an immutable serialized trace. It receives no simulator objects, live DUT
  handles, RTL source, mutant identity, driver seed, stimulus list, observation mask, reference model/API or
  expected-output table. `metadata` contains exactly: `design_id` (string), `spec_version_sha256` (64-character
  lowercase hexadecimal string), `trace_schema_version` (string), `cycle_cap` (positive integer),
  `reset_release_cycle` (non-negative integer) and `trace_integrity_status` (literal `VALID`)."
- **Return value.** Protocol L286: "The return value is a dictionary with exactly two top-level keys: `verdict` and
  `diagnostics`. `verdict` is exactly `PASS` or `FAIL`. `diagnostics` is required and must be a list; an empty list is
  valid. A well-formed diagnostic item has exactly `code` (string), `message` (string), `cycle` (integer or null) and
  `clause_id` (string or null). … A missing/non-list diagnostics field, missing/extra top-level key, invalid verdict,
  non-dictionary return or process crash is a checker error. … The same immutable null trace is evaluated twice in
  separate processes; both verdicts must be `PASS` and agree."
- **What the file may contain.** File 30 L37: "no class definition of any kind is allowed. Exactly one module-level
  synchronous undecorated function named `check_trace` must exist, with exactly two required positional-or-keyword
  parameters named `trace` and `metadata`, not positional-only and with no defaults, variadic, keyword-only or extra
  parameters. Synchronous undecorated helper functions are allowed".
- **Behaviour rules.** File 30 L60: "It must not read or write files, access the network, read environment variables
  or wall-clock time, create processes or threads, or invoke subprocesses." The import rules of File 30 L74 apply as for
  drivers.
- **Trace rows** (DRAFT schema `openvef-trace-0.1-draft`, README §2): each row has exactly `cycle_index`, `reset`,
  `inputs_consumed_at_edge_n`, `outputs_after_edge_n`, `next_inputs_scheduled_for_edge_n_plus_1` and
  `driver_completed`.

**The validity gate applies to every control artifact.** Protocol L247: "Every artifact is also run on the null netlist.
It must parse, satisfy the API, compile, execute under the cycle cap/watchdog and pass the offline checker on the
archived null trace. The same checker is then invoked in a second independent process on that exact immutable trace;
both invocations must return `PASS`." The runner applies the production static checks first. A control file that
fails them is recorded as rejected and does not exercise its control (README §2). Some controls need a checker that
misbehaves on purpose (F7, F8, F13 and several F17 checkers). Each still has to pass the static checks, and, where
noted, both null runs.

### 1.3 Control mutants (`mutants/*.v`)

- Owner decision D-007 (2): each mutant is an edit of `design/fifo/rtl/ovf_fifo.v` (66 lines), keeping module `ovf_fifo`
  and its ports.
- Protocol L233: "The null-mutant netlist is generated from the original RTL by exactly the same synthesis/export
  script, tool versions and top-level interface as the mutant netlists, with no mutation applied. Export must preserve
  top module name and public ports."
- The harness exports each mutant twice and checks that it differs from the original and from every other mutant
  (README §3).
- Charter L74 asks for "a **hand-built set of distinct control mutants** sufficient to exercise the F1–F15 cases; this
  is not a one-mutant-only plan."

### 1.4 Data files (`*.json`)

The formats are harness-defined: README §3 gives `mutants/manifest.json`, `drivers/directed/suite.json` and
`drivers/f2_echo.json`. They are lists and declarations, not executable artifacts.

---

## 2. Per-control worksheet

For each control: what it tests, with the §17 row quoted; the files it needs (from `slots.json`, with their type); the
interface it follows (section 1); what "pass" means; and which files it shares. "Pass" is the pack's expected column.
The plan's harness notes say how the runner checks it.

### F1 — Determinism and checker null repeat

- **Tests:** whether one artifact gives the same trace three times on the null netlist, and whether its checker gives
  the same `PASS` twice. Protocol L510: "Run one artifact on null netlist three times; run its checker twice in separate
  processes on the same immutable null trace".
- **Files:**
  - `drivers/reference_driver.py` (driver);
  - `checkers/f6_correct_checker.py` (checker). D-007 (4) reuses these two for F1.
- **Interface:** §1.1 and §1.2.
- **Pass:** "Traces match excluding explicitly non-deterministic metadata; both checker runs return identical `PASS`"
  (L510). The DRAFT trace rows have no non-deterministic field, so the three traces must be byte-identical (A-051).
- **Shares:** both files with F3. The driver is also used by F5, F7, F8 and F13; the checker by F3, F6 and F9–F12.

### F2 — Alignment (critical gate, L531)

- **Tests:** whether each trace row puts the outputs and the driver's next decision on the right edge. Protocol L511:
  "Driver echoes a registered output into next-cycle input".
- **Files:**
  - `drivers/f2_echo_driver.py` (driver) copies a registered output into its next-cycle input;
  - `drivers/f2_echo.json` (data) names which output feeds which input of the same width.
- **Interface:** §1.1; §1.4 for the JSON. The echoed value must still be a legal input vector (only `0` and `1`, right
  width, FIFO-042 respected).
- **Pass:** "Row n records outputs after edge n and the driver's decision for edge n+1; consumed inputs agree with prior
  scheduled vector" (L511). The harness also shows that the echoed output from row n appears as the consumed input at
  edge n+1.
- **Shares:** nothing. Both files are used only by F2.

### F3 — RTL versus null

- **Tests:** whether the original RTL and the null netlist agree under the F1 artifact. Protocol L512: "Run F1 artifact
  on RTL and null netlist".
- **Files:** the same two as F1: `drivers/reference_driver.py` (driver) and `checkers/f6_correct_checker.py` (checker).
- **Interface:** §1.1 and §1.2.
- **Pass:** "No masked divergence and no scheduled next-input divergence before first raw divergence" (L512).
- **Shares:** both files with F1.

### F4 — Miter/simulation agreement (critical gate)

- **Tests:** whether a counterexample found by the mask-aware miter shows up in the simulator at the predicted cycle.
  Protocol L513: "Replay mask-aware miter counterexample in simulator".
- **Files:** `mutants/manifest.json` (data), naming a mutant with role **M-exposed**, and that mutant's `.v` file
  (Verilog mutant). No owner driver or checker is needed: the replayed input schedule comes from the miter.
- **Interface:** §1.3. M-exposed needs "a masked-observable divergence under legal inputs within the bound N"
  (`slots.json`).
- **Pass:** "Masked divergence appears at predicted cycle" (L513).
- **Shares:** the manifest with every mutant control. M-exposed is also used by F6 and F17.

### F5 — Masked don't-care (critical gate)

- **Tests:** whether a change confined to the specification's don't-care window is a raw but not a masked difference.
  Protocol L514: "Mutant changes FIFO data only while valid is low, where spec says data is don't-care".
- **Files:**
  - `mutants/manifest.json` (data) with a mutant of role **M-dontcare**, and its `.v` file (Verilog mutant);
  - `drivers/reference_driver.py` (driver). It must reach `rd_valid = 0` rows after a write, so the window is exercised
    (README §1).
- **Interface:** §1.1 and §1.3. M-dontcare "changes `rd_data` only in rows where the null trace has `rd_valid = 0`; must
  not change `rd_valid` or any other always-observed output" (`slots.json`).
- **Pass:** "Raw divergence but no masked divergence; miter agrees through fixed N" (L514). The miter label is
  `BOUNDED_EQUIVALENT_N`.
- **Shares:** M-dontcare with F7 and F17. The reference driver with F1, F3, F7, F8 and F13.

### F6 — Pair classes

- **Tests:** whether the three basic pair classes come out right for known-answer artifacts. Protocol L515: "Hand-built
  correct checker, always-PASS checker, and non-exposing driver".
- **Files:**
  - `mutants/manifest.json` with **M-exposed** (data and Verilog mutant);
  - `drivers/f6_exposing_driver.py` (driver), which exposes M-exposed;
  - `drivers/f6_nonexposing_driver.py` (driver), which does not;
  - `checkers/f6_correct_checker.py` (checker): PASS on every legal null trace, FAIL on M-exposed's exposed trace;
  - `checkers/f6_always_pass_checker.py` (checker): always PASS.
- **Interface:** §1.1–§1.3.
- **Pass:** "`DETECTED`, `PND`, `NP` respectively" (L515):
  - correct checker with the exposing driver gives `DETECTED`;
  - always-PASS checker on the same pair gives `PND`;
  - the non-exposing driver gives `NP`.
- **Shares:** the correct checker with F1, F3 and F9–F12. M-exposed with F4 and F17.

### F7 — Checker stricter than mask

- **Tests:** whether a checker that judges data inside the don't-care window is flagged as stricter than the mask.
  Protocol L516: "Checker compares data during an explicit don't-care window".
- **Files:**
  - `mutants/manifest.json` with **M-dontcare** (data and Verilog mutant);
  - `drivers/reference_driver.py` (driver);
  - `checkers/f7_stricter_checker.py` (checker). It compares `rd_data` during the window, but must PASS both null
    runs, so it stays a valid artifact (L247; README §1).
- **Interface:** §1.1–§1.3.
- **Pass:** "`ANOMALY_CHECKER_STRICTER_THAN_MASK`" (L516).
- **Shares:** M-dontcare with F5 and F17. The reference driver with F1, F3, F5, F8 and F13.

### F8 — Pipeline anomaly

- **Tests:** whether a checker FAIL on a trace identical to null is classed as a checker/pipeline anomaly, not as
  detection. Protocol L517: "Checker returns FAIL on a trace identical to null".
- **Files:**
  - `mutants/manifest.json` with **M-silent** (data and Verilog mutant): "structurally distinct from the original, but
    gives no raw output divergence under the F8 driver" (`slots.json`);
  - `drivers/reference_driver.py` (driver);
  - `checkers/f8_nondeterministic_checker.py` (checker).
- **Interface:** §1.1–§1.3.
- **Pass:** "`ANOMALY_PIPELINE_OR_NONDETERMINISM`" (L517).
- **Read with care** (plan §4 F8, Q2):
  - A valid deterministic checker cannot FAIL a byte-identical trace it has passed, so only a nondeterministic checker
    can produce this, and only by chance.
  - The checker must also PASS both null runs to stay valid (L247).
  - Under File 30 L74 the only nondeterminism left is the alias bypass of module-global `random` described in File 30
    L20.
  - The planned control is a recorded, bounded attempt reported as "observed" or "not observed", next to a
    classifier-level known answer.
- **Shares:** the reference driver with F1, F3, F5, F7 and F13. The manifest with every mutant control.

### F9 — Invalid pair (critical gate)

- **Tests:** whether a driver that uses unseeded entropy makes the pair invalid, and whether the seeded version obeys
  the paired schedule. Protocol L518: "Driver reads unseeded entropy; rerun with harness-owned seed".
- **Files:**
  - `mutants/manifest.json` with any distinct mutant (role **M-any**; data and Verilog mutant; it may be the same file
    as another role);
  - `drivers/f9_unseeded_driver.py` (driver);
  - `drivers/f9_seeded_driver.py` (driver);
  - `checkers/f6_correct_checker.py` (checker).
- **Interface:** §1.1–§1.3.
- **The unseeded driver must reach the runtime.**
  - File 30 L20: "Any direct attribute access on the module name `random` other than `random.Random` is rejected …
    Static detection may be bypassed by aliasing … or `getattr`; … Such bypasses are not statically claimed as detected
    and are caught only if they cause a paired next-input divergence at runtime."
  - A direct module-global call is rejected statically (`GLOBAL_RANDOM_USE`) and never runs.
  - The unseeded draw must change a next-input decision before the first raw divergence.
  - The seeded driver makes the same kind of decisions from a local `random.Random(seed)` only.
- **Pass:** "First `INVALID_PAIR`; seeded version obeys paired input schedule" (L518). The unseeded result is
  probabilistic, so the trial is recorded.
- **Shares:** the correct checker with F1, F3, F6, F10, F11 and F12. The mutant may be any mutant already written for
  another role.

### F10 — Same-row tie

- **Tests:** whether a driver reacting to an output the mutant changed in the same row keeps the pair valid under
  output-first sampling. Protocol L519: "Mutant changes `full`; driver changes next input based on sampled output".
- **Files:**
  - `mutants/manifest.json` with **M-full** (data and Verilog mutant), which "changes the `full` output";
  - `drivers/f10_full_reactive_driver.py` (driver), whose next input depends on the sampled `full`;
  - `checkers/f6_correct_checker.py` (checker).
- **Interface:** §1.1–§1.3.
- **Pass:** "Pair is valid under output-first sampling rule" (L519). The pair is classified by the normal classes,
  not `INVALID_PAIR`.
- **Shares:** the correct checker. M-full may be the same mutant as another role, if that mutant changes `full`.

### F11 — Cycle cap/timeout

- **Tests:** whether reaching the cycle cap is told apart from a watchdog timeout. Protocol L520: "Driver completes at
  cap vs watchdog fires".
- **Files:**
  - `drivers/f11_runs_to_cap_driver.py` (driver), which never returns `COMPLETE`;
  - `drivers/f11_infinite_loop_driver.py` (driver), with a `step` call that never returns;
  - `checkers/f6_correct_checker.py` (checker).
  No mutant is needed.
- **Interface:** §1.1 and §1.2. Protocol L227: "If the driver has not completed at the cap, record
  `driver_completed=false`; reaching the cap is a normal end, not a timeout." The loop must still pass the static
  checks (no prohibited name or import).
- **Pass:** "Cap is normal incomplete-driver termination; watchdog is timeout" (L520). In the first case the checker
  runs on the complete trace. In the second, the trace is truncated and no checker runs.
- **Shares:** the correct checker only.

### F12 — Driver/simulator error

- **Tests:** whether a driver crash caused by an X on a mutant output is a driver/simulator error, not detection.
  Protocol L521: "Driver converts X output to integer on mutant".
- **Files:**
  - `mutants/manifest.json` with **M-x** (data and Verilog mutant), which "drives X on a public output (e.g. from an
    undriven net)";
  - `drivers/f12_x_convert_driver.py` (driver), which converts that output to an integer in base 2 and so raises on
    `X`;
  - `checkers/f6_correct_checker.py` (checker).
- **Interface:** §1.1–§1.3. On the null netlist the output carries no X. The driver must therefore run cleanly there, or
  it fails the L247 validity gate.
- **Pass:** "Driver/simulator error, not detection; truncated trace excluded from `T_i`" (L521).
- **Open question:** plan Q7 (whether the X reaches the driver as the character `X`) is confirmed only once M-x exists.
- **Shares:** the correct checker.

### F13 — Checker non-interference

- **Tests:** whether a checker in its own process cannot reach the simulator or change the stored trace. Protocol L522:
  "Run checker in separate process on trace file".
- **Files:**
  - `drivers/reference_driver.py` (driver);
  - `checkers/f13_adversarial_checker.py` (checker), which tries to change its `trace` argument and to reach the
    simulator or the trace file.
- **Interface:** §1.1 and §1.2.
- **Read with care:**
  - File 30 L74 rejects the names `open`, `__import__`, `eval`, `exec` and `compile`, and every import outside the
    allow-list, at the static stage.
  - An attempt written with those names never reaches the runtime path, and so does not exercise F13 (README §1: "It
    must pass the static checks to reach the runtime path").
  - Which attempts remain possible within the allow-list is the owner's design.
- **Pass:** "Checker cannot access simulator handles or alter trace" (L522). After each run the harness re-hashes the
  stored trace bytes and checks the container's isolation.
- **Shares:** the reference driver with F1, F3, F5, F7 and F8.

### F17 — Common-trace panel controls (critical gate; pre-freeze feasibility only)

- **Tests:** whether the panel classes and events come out right for seven known-answer checkers. Protocol L526:
  "Pre-freeze feasibility F17 uses only hand-built FIFO control mutants, not the confirmatory MCY manifest. Build
  separate legal `REACTIVE_RANDOM` and `DIRECTED` streams through the production harness; run RTL and null benign
  traces; repeat each checker twice on identical benign and mutant trace bytes".
- **Mutant and stream files:**
  - `mutants/manifest.json` with **M-exposed** and **M-dontcare** (data and two Verilog mutants);
  - `drivers/directed/suite.json` (data), plus one driver file per scenario under `drivers/directed/` (drivers; the
    number is the owner's choice);
  - `drivers/f17_reactive_random_driver.py` (driver): a legal reactive random driver, run over the `REACTIVE_RANDOM`
    seeds.

  Protocol L415 sets two conditions: the directed suite is "written against the specification only, before any LLM
  generation and independently of generated artifacts", and the random driver "respects the specification's
  legal-input rules".
- **Checker files and their expected results** (all quoted from L526):

  | Checker file | Expected result |
  |---|---|
  | `checkers/f17_reference_checker.py` | "Correct reference checker: compatible and detects every exposed case" |
  | `checkers/f17_always_pass_checker.py` | "always-PASS: compatible with zero sensitivity" |
  | `checkers/f17_always_fail_checker.py` | "always-FAIL: `PANEL_FALSE_ALARM`" |
  | `checkers/f17_stimulus_literal_checker.py` | "stimulus-literal: false alarm on at least one distinct legal benign trace" |
  | `checkers/f17_crashing_checker.py` | "crashing checker: `PANEL_ERROR`" |
  | `checkers/f17_stricter_than_mask_checker.py` | "stricter-than-mask checker: `PANEL_STRICTER_THAN_MASK_EVENT`, not detection" |
  | `checkers/f17_nondeterministic_checker.py` | "nondeterministic checker: `PANEL_ERROR`" |

- **Interface:** §1.1–§1.4.
- **Pass:** each checker gets its expected result, and L526 adds: "`PANEL_ERROR`, `PANEL_FALSE_ALARM` and
  `PANEL_COMPATIBLE` partition proportions sum to `V_cd` within each stream/design/arm."
- **Read with care** (plan §4 F17):
  - The stimulus-literal checker needs at least two distinct legal benign traces per stream, so the directed suite
    needs at least two scenarios.
  - The nondeterministic checker can only use the File 30 L20 alias bypass. It escapes detection with a probability
    that halves with each benign trace, so it is reliable but not certain.
  - The stricter-than-mask checker needs M-dontcare.
- **Shares:**
  - M-exposed with F4 and F6; M-dontcare with F5 and F7.
  - The reference checker may have the same content as `checkers/f6_correct_checker.py`, but it must exist under its
    own name (README §1).
  - The seven F17 checkers and the two stream files are used only by F17.

---

## 3. Which controls share which files

| File | Type | Controls |
|---|---|---|
| `mutants/manifest.json` (+ the `.v` files it names) | data + Verilog mutants | F4, F5, F6, F7, F8, F9, F10, F12, F17 |
| `checkers/f6_correct_checker.py` | checker | F1, F3, F6, F9, F10, F11, F12 |
| `drivers/reference_driver.py` | driver | F1, F3, F5, F7, F8, F13 |
| M-exposed (mutant role) | Verilog mutant | F4, F6, F17 |
| M-dontcare (mutant role) | Verilog mutant | F5, F7, F17 |

Every other file feeds one control only.

**The shortest path to the most controls:**
- `reference_driver.py` plus `f6_correct_checker.py` unblocks F1 and F3.
- Adding M-exposed and M-dontcare unblocks F4 and F5, two critical gates.
- The F2 pair unblocks F2, a third critical gate.

This ordering is a suggestion only; the order is the owner's choice.

---

## 4. Distinct files to write, by type, smallest first

**Line counts are rough guesses** for planning only, not targets. They assume the FIFO's small interface (5 outputs, 3
inputs, depth 4, width 8, cycle cap 64).

### 4.1 Data files (3 files, plus a scenario list inside one of them)

| File | Rough size | Note |
|---|---|---|
| `drivers/f2_echo.json` | 1–3 lines | names one output and one input of the same width |
| `drivers/directed/suite.json` | 3–15 lines | one entry per directed scenario, at least two |
| `mutants/manifest.json` | 10–30 lines | one entry per mutant, with its roles and a description in the owner's words |

### 4.2 Checkers (12 files)

| File | Rough size | Note |
|---|---|---|
| `checkers/f6_always_pass_checker.py` | 3–8 | |
| `checkers/f17_always_pass_checker.py` | 3–8 | may equal the F6 one in content |
| `checkers/f17_always_fail_checker.py` | 3–8 | |
| `checkers/f17_crashing_checker.py` | 3–8 | |
| `checkers/f8_nondeterministic_checker.py` | 10–25 | must PASS both null runs; see F8 |
| `checkers/f17_nondeterministic_checker.py` | 10–25 | see F17 |
| `checkers/f17_stimulus_literal_checker.py` | 15–40 | keyed to one literal stimulus sequence |
| `checkers/f13_adversarial_checker.py` | 15–40 | must pass the static checks; see F13 |
| `checkers/f7_stricter_checker.py` | 60–150 | a correct checker that also judges `rd_data` in the don't-care window |
| `checkers/f17_stricter_than_mask_checker.py` | 60–150 | as F7's; may share content |
| `checkers/f6_correct_checker.py` | 60–150 | checks the trace against the specification; the largest single piece of owner logic |
| `checkers/f17_reference_checker.py` | 60–150 | may equal the F6 correct checker in content |

### 4.3 Drivers (11 named files, plus the directed scenario files)

| File | Rough size | Note |
|---|---|---|
| `drivers/f11_infinite_loop_driver.py` | 8–15 | |
| `drivers/f11_runs_to_cap_driver.py` | 10–20 | never returns `COMPLETE` |
| `drivers/f2_echo_driver.py` | 10–25 | |
| `drivers/f12_x_convert_driver.py` | 10–25 | must run cleanly on the null netlist |
| `drivers/f10_full_reactive_driver.py` | 15–30 | |
| `drivers/f6_nonexposing_driver.py` | 15–30 | |
| `drivers/f9_seeded_driver.py` | 15–35 | |
| `drivers/f9_unseeded_driver.py` | 15–35 | same decisions, through the File 30 L20 alias bypass |
| `drivers/f6_exposing_driver.py` | 20–40 | |
| `drivers/reference_driver.py` | 25–60 | the frozen reference driver (checklist item 14); must reach the don't-care window |
| `drivers/f17_reactive_random_driver.py` | 25–60 | legal reactive random driver |
| `drivers/directed/<scenario>.py` × at least 2 | 15–40 each | the directed suite (item 14); written against the spec only (L415) |

### 4.4 Verilog mutants (at least 3 distinct files)

Each mutant is a full copy of `design/fifo/rtl/ovf_fifo.v` (66 lines) with a small edit, typically 1–5 lines changed.

| Role | Can it share a file with another role? |
|---|---|
| M-dontcare | No. It must be distinct from M-exposed (README §1, Charter L74), and it raw-diverges, so it cannot be M-silent |
| M-exposed | Not with M-dontcare or M-silent. It could also serve as M-full if its change is to `full`, and as M-any |
| M-silent | No. It must give no raw divergence under the reference driver, while every other role requires one |
| M-x | Owner's choice. It must drive X on a public output |
| M-full | Owner's choice. It must change `full` |
| M-any | Any of the above |

So the minimum is 3 distinct mutant files (M-exposed, M-dontcare, M-silent), and at most 5 if no roles are combined.
This follows from the role definitions in `slots.json`. Which roles to combine is the owner's design.

**Totals:**
- 26 slot files: 3 data files, 12 checkers and 11 named drivers.
- At least 2 directed scenario drivers.
- At least 3 Verilog mutants.
- Rough total: about 700–1,600 lines, of which about 200–330 are copied RTL in the mutant files.
- If identical content is reused where the README allows it (F17 reference = F6 correct; F17 always-PASS = F6
  always-PASS; F17 stricter = F7 stricter), the new logic is closer to the lower end.

---

## 5. Not covered here

- **F14 and F15** need no owner artifact. Both PASS (provisional) in `controls-20261128T111046Z`.
- **F16** is closed by the LLM-call gate. **F18** is a separate parser and assembly suite.
- **The mask, its traceability table and its independent sign-off (L271)** are not control files. They are covered by
  DEV-001.
- **Composing each control's procedure** from the harness (plan §9, step 8) is Claude's work under label (a). It starts
  for a control when its files exist.
