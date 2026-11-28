# FIFO feasibility controls: owner-artifact slots

**For:** the owners (Krishika, Ayush Kumar Singh). **Written by:** Claude (Claude Opus
5.5, via Claude Code), 24 Nov 2026, as harness documentation.

**Every file listed below is owner-written.** Sources:
- CLAUDE.md "Still human-written";
- owner decision D-007 (Krishika, 24 Nov 2026; Ayush's confirmation pending).

Claude never places content in these slots. The only Claude-written files in this
directory are this README and `slots.json`, the machine-readable copy of the slot table.
`tests/test_controls_slots.py` keeps the two in step.

**How the runner uses this directory.** `runner/run_controls.py` runs the feasibility
controls in the pinned image. For each control it reports:
- `BLOCKED_OWNER_ARTIFACTS`, with the missing files, until every file the control needs
  exists;
- `NOT_WIRED`, once the files exist but the control's procedure has not been composed from
  the harness components yet (plan step 8, [F1-F17-plan.md](../../../docs/F1-F17-plan.md)).
  F1 and F3 are composed (D-036), so they run as soon as `drivers/reference_driver.py` and
  `checkers/f6_correct_checker.py` both exist. F4 and F5 are composed (D-036 follow-up), so they
  run as soon as `mutants/manifest.json` names an M-exposed mutant (F4), or an M-dontcare mutant
  and the reference driver exists (F5);
- `ARTIFACT_REJECTED`, with the production stage diagnostic, when the production static or
  runtime stages reject the owner files. That is never a pass.

**Checking one file yourself (D-036).** `.venv/bin/python -I tools/check_control_file.py <path>`
runs only File 30's static stages (SOURCE_AST, IMPORT_POLICY, AST_SIGNATURE) on one file, judged
as `driver.py` or `checker.py` by its directory. It prints which stage accepted or rejected it,
with the diagnostic. It only reads the file. COMPILE and the runtime stages run in the control run.
For a mutant (`mutants/<id>.v`), the same command checks, in the pinned image, that it defines
module `ovf_fifo`, differs from `design/fifo/rtl/ovf_fifo.v` (the size of the difference is
reported), compiles with the pinned Icarus (`iverilog -g2012`), and keeps the original's port list.

F14 and F15 need no owner artifact.

## 1. Files to write

Paths are relative to this directory.

### Mutants (checklist item 15)

| File | What it is | Feeds |
|---|---|---|
| `mutants/manifest.json` | the mutant list (format in §3) | F4, F5, F6, F7, F8, F9, F10, F12, F17 |
| `mutants/<id>.v` | one file per mutant: an **edit of `design/fifo/rtl/ovf_fifo.v`** (D-007 (2)), keeping module `ovf_fifo` and its ports | as its roles |

### Drivers

| File | Behaviour the control needs | Feeds |
|---|---|---|
| `drivers/reference_driver.py` | the frozen reference driver (checklist item 14). Must reach `rd_valid = 0` rows after a write, so F5/F7 can see the don't-care window | F1, F3, F5, F7, F8, F13 |
| `drivers/directed/suite.json` + `drivers/directed/<scenario>.py` | the directed legal-input suite (item 14), one driver file per scenario (format in §3) | F17 (`DIRECTED`) |
| `drivers/f2_echo_driver.py` | echoes a registered output into its next-cycle input | F2 |
| `drivers/f2_echo.json` | which output it echoes into which input (format in §3) | F2 |
| `drivers/f6_exposing_driver.py` | exposes M-exposed | F6 |
| `drivers/f6_nonexposing_driver.py` | does not expose M-exposed | F6 |
| `drivers/f9_unseeded_driver.py` | changes a next-input decision before the first raw divergence, using unseeded module-global `random` reached through an alias. A direct `random.random()` is rejected statically (`GLOBAL_RANDOM_USE`, File 30 L20) and never runs | F9 |
| `drivers/f9_seeded_driver.py` | the same decisions from a local `random.Random(seed)` only | F9 |
| `drivers/f10_full_reactive_driver.py` | changes its next input according to the sampled `full` | F10 |
| `drivers/f11_runs_to_cap_driver.py` | never returns `COMPLETE` | F11 |
| `drivers/f11_infinite_loop_driver.py` | a `step` call that never returns | F11 |
| `drivers/f12_x_convert_driver.py` | converts the output that M-x drives to X with `int(…, 2)` | F12 |
| `drivers/f17_reactive_random_driver.py` | a legal reactive random driver, run over the `REACTIVE_RANDOM` seeds | F17 (`REACTIVE_RANDOM`) |

### Checkers

| File | Behaviour the control needs | Feeds |
|---|---|---|
| `checkers/f6_correct_checker.py` | a correct checker: PASS on every legal null trace; FAIL on M-exposed's exposed trace. Per D-007 (4) it is also F1's checker | F1, F3, F6, F9, F10, F11, F12 |
| `checkers/f6_always_pass_checker.py` | always PASS | F6 |
| `checkers/f7_stricter_checker.py` | compares `rd_data` during the don't-care window. Must PASS both null runs, so it stays a valid artifact | F7 |
| `checkers/f8_nondeterministic_checker.py` | can return FAIL on a trace identical to one it passed. See plan §4 F8: this happens only by chance | F8 |
| `checkers/f13_adversarial_checker.py` | mutates its `trace` argument and tries to reach the simulator or the trace file. It must pass the static checks to reach the runtime path | F13 |
| `checkers/f17_reference_checker.py` | correct reference checker | F17 |
| `checkers/f17_always_pass_checker.py` | always PASS | F17 |
| `checkers/f17_always_fail_checker.py` | always FAIL | F17 |
| `checkers/f17_stimulus_literal_checker.py` | keyed to one literal stimulus sequence | F17 |
| `checkers/f17_crashing_checker.py` | raises | F17 |
| `checkers/f17_stricter_than_mask_checker.py` | stricter than the mask | F17 |
| `checkers/f17_nondeterministic_checker.py` | nondeterministic | F17 |

A file may have the same content as another file (for example, the F17 reference checker
and the F6 correct checker), but it must still be present under its own name.

### Mutant roles

Each role must be named in at least one manifest entry's `roles`. One mutant may carry
several roles, but M-exposed and M-dontcare must be different mutants (Charter L74:
"distinct control mutants").

| Role | Behaviour required | Feeds |
|---|---|---|
| M-exposed | a masked-observable divergence under legal inputs within the bound N | F4, F6, F17 |
| M-dontcare | changes `rd_data` only in rows where the null trace has `rd_valid = 0`; must not change `rd_valid` or any other always-observed output | F5, F7, F17 |
| M-full | changes `full` | F10 |
| M-x | drives X on a public output | F12 |
| M-silent | distinct from the original, but no raw divergence under the reference driver | F8 |
| M-any | any distinct control mutant | F9 |

## 2. Required interfaces

**Drivers** satisfy the `driver.py` contract of File 30, the same API as LLM artifacts
(Protocol L208–L212):
- exactly one class `Driver` with one method `step(self, cycle_index, outputs_after_edge)`;
- one function `create_driver(seed)` that returns a `Driver`;
- imports only from the File 30 allow-list (`random` only as `random.Random(seed)`);
- ASCII identifiers.

The runner applies the production static checks first. A control artifact that fails
them is recorded as rejected and does not exercise its control.

**Driver inputs and returns** (DRAFT FIFO materials, `design/fifo/design-materials-DRAFT.json`):
- `step` receives `outputs_after_edge` with keys `almost_full`, `empty`, `full`, `rd_data`,
  `rd_valid`. Values are MSB-first strings that can contain `0`, `1`, `X` and `Z`.
- The first call is after reset release, with `cycle_index = 0`.
- `step` returns either `"COMPLETE"` or a dictionary with exactly the keys `wr_en` (1 bit),
  `wr_data` (8 bits) and `rd_en` (1 bit), each a string of `0` and `1`.
- `rst` is harness-owned and is not a key (A-042, accepted under D-006).
- A vector that breaks FIFO-042 (`wr_en = 1`, `rd_en = 0` while the sampled `full = 1`)
  ends the run as `ILLEGAL_PROTOCOL_STATE`.
- After `COMPLETE`, the harness drives the safe-idle vector to the cycle cap (64, DRAFT).

**Checkers** satisfy the `checker.py` contract of File 30 and Protocol L284–L286:
- signature `check_trace(trace, metadata)`, with no classes;
- returns `{"verdict": "PASS" | "FAIL", "diagnostics": [...]}`;
- `trace` is a list of rows in the DRAFT trace schema `openvef-trace-0.1-draft`. Each row
  has exactly these keys: `cycle_index`, `reset`, `inputs_consumed_at_edge_n`,
  `outputs_after_edge_n`, `next_inputs_scheduled_for_edge_n_plus_1`, `driver_completed`;
- `metadata` has exactly `design_id`, `spec_version_sha256`, `trace_schema_version`,
  `cycle_cap`, `reset_release_cycle` and `trace_integrity_status`.

## 3. Formats

**`mutants/manifest.json`:**

```json
{"mutants": [
  {"id": "<letters, digits, _ or ->", "file": "<id>.v", "roles": ["M-exposed"],
   "description": "<what was changed, in the owners' words>"}
]}
```

The harness checks each mutant:
- it defines module `ovf_fifo` and is not identical to the original;
- it exports twice through the same script as the null netlist, with equal hashes;
- its netlist differs from the null netlist and from every other mutant;
- it keeps the null netlist's public ports (Protocol L233).

The diff against the original RTL and its SHA-256 are recorded in the evidence.

**`drivers/directed/suite.json`:**

```json
{"scenarios": [{"scenario_id": "<name>", "file": "<name>.py", "seed": 0}]}
```

**`drivers/f2_echo.json`:**

```json
{"output": "<output port>", "input": "<driver input port of the same width>"}
```
