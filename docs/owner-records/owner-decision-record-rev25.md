# OpenVEF Owner Decision Record (v1.3.6 baseline) — BLANK

## 1. Purpose and baseline

**Form status:** PARTLY COMPLETED, UNSIGNED. Boxes marked ☒ were marked by Claude on the co-owners' written instruction of 23 Nov 2026 (see the OpenVEF Owner Sign-off Pack, Owner instruction log). Identities, hashes, signatures and dates are completed by the owners themselves.

This record captures the owner decisions that `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` (L47) requires before the implementation gate can open: acceptance or rejection of A1–A11, and the X14 branch choice. It also records the identity, runtime-pin and evidence arrangements for the next stage.

| Baseline field | Value |
| --- | --- |
| Baseline pack | OpenVEF Planning Pack v1.3.6 |
| Baseline ZIP SHA-256 | `2e7008210a807868ad3d8a878820afa7cf1066f1c2b5b1cb437b911aa9b30c21` |
| Baseline ZIP size | 254,691,432 bytes |
| Document audit | PASS, 23 Nov 2026 (independent, documents only) |
| Fixture status at baseline | 144 descriptors, all NOT RUN / NOT PASSED |
| Owner has reviewed the baseline pack | ☐ Yes ☐ No |

### What signing this record does NOT authorize

Signing this record does **not** authorize any of the following:

- Any LLM or provider call, including F16, smoke tests or provider-format probes. The LLM-call gate is a **separate, later decision**, taken only after the implementation audit passes and only by explicit owner authorization.
- Confirmatory generation or the full study.
- Any work outside the limited, hand-built FIFO scope defined in section 5.

> **Note on Register 16 L47.** The gate sentence there still says “No LLM call (including F16) until B1–B9 and the complete mandatory fixture set pass independent re-audit”. “B1–B9” is a stale reference to the v1.0 audit's blockers, which were resolved long ago; the v1.3.6 audit missed it. For this record, the operative rule is the one stated above: no LLM call until the implementation audit passes and the owner separately authorizes it.

## 2. Decisions A1–A11

The proposed decisions are quoted from Register 16 (L22–L32). For each one, mark exactly one decision.

- **Accept as written** accepts the text exactly as it stands in v1.3.6.
- **Reject** and **Modify** each change the operative design. Either one requires a revised document release and a new independent document audit before implementation (see section 6).
- Where a numerical value is still TO FREEZE, accepting the policy does **not** freeze the number. Numbers are recorded separately in section 5.

| ID | Proposed decision (as written in v1.3.6) | Accept as written | Reject | Modify | Rationale or modification text |
| --- | --- | --- | --- | --- | --- |
| A1 | Remove model-visible block IDs; keep IDs only in assembler metadata | ☒ | ☐ | ☐ |  |
| A2 | Use order-free task/repair instructions; limit interpretation to the two exact orders | ☒ | ☐ | ☐ |  |
| A3 | Adopt machine-readable JSON Schema v1.0 and Python 3.11 entry-point contract (runtime patch/image TO FREEZE) | ☒ | ☐ | ☐ |  |
| A4 | Same-conversation repair; full prior messages resent byte-identically; feedback whitelist and 2,048-byte parser/compiler cap | ☒ | ☐ | ☐ |  |
| A5 | Integrity adjudication and panel stream/pair/nondeterminism rules | ☒ | ☐ | ☐ |  |
| A6 | Freeze ordering replaces impossible owner-blinding rule | ☒ | ☐ | ☐ |  |
| A7 | Adopt prompt assembly/canonicalization specification | ☒ | ☐ | ☐ |  |
| A8 | Exclude FSM from confirmatory set; FIFO + UART only (decide before F16) | ☒ | ☐ | ☐ |  |
| A9 | Set `R_max=2` re-pilot cap (numerical value TO FREEZE) | ☒ | ☐ | ☐ |  |
| A10 | Human baseline author must be evaluator-independent, or the baseline is labelled evaluator-informed | ☒ | ☐ | ☐ |  |
| A11 | Apply `V_min` separately to each arm × design stratum; if any stratum remains below the floor after `R_max`, do not proceed with the pre-declared confirmatory design set | ☒ | ☐ | ☐ |  |

**Summary (owner to complete):** Number accepted as written: 11 / 11. Number rejected or modified: 0.

## 3. X14 — AST policy branch

The two options are summarised from Register 16 (L77). Mark exactly one. The register labels Option A “recommended”; that label is the pack author's, not an owner decision, and this form does not preselect it.

| Option | What it means | Parser and document implications | Select |
| --- | --- | --- | --- |
| A — strict AST (as specified) | Keep the strict policy already in model-visible B5/B7/B8: no `Driver.__init__`; only `Driver.step`; no helper or nested classes; no decorators; no checker classes; literal-only module constants. | No change to model-visible text, parser rules or fixtures. The 144 fixtures were written for this branch. The v1.3.6 freeze stays valid. | ☒ |
| B — relaxed AST | Relax restrictions, for example by permitting `__init__`, additional methods, helper classes or selected decorators. | Requires new model-visible contract text, new parser policy and new fixtures. Prompt hashes change. A revised release and a fresh independent document audit are required before any implementation. The v1.3.6 freeze does **not** stay valid. | ☐ |

**If Option B is selected, list the intended relaxations:**

- ***
- ***

**Owner notes on X14:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## 4. Identities and roles

Each field stays blank until the named person supplies and confirms it. Nothing here may be inferred from the pack, from earlier conversations or from the audits.

Register 16 (L45) requires the owner's legal-name form to match the line used on the actual TEEP application before any external use.

| Role | Name (as confirmed by the person) | Affiliation | Confirmed by the person on (date) |
| --- | --- | --- | --- |
| Owner (legal-name form) |  |  |  |
| TEEP applicant |  |  |  |
| Contributor(s) and their roles |  |  |  |
| Approver |  |  |  |
| Human baseline author (A10) |  |  |  |
| Independent implementation auditor (section 5) |  |  |  |

**Is the human baseline author independent of the evaluator (A10)?** ☐ Yes ☐ No. If No, the baseline is labelled evaluator-informed.

## 5. Runtime pin, implementation scope, evidence and independence

### 5.1 Python runtime pin

| Field | Value |
| --- | --- |
| Exact CPython version (for example `3.11.x`) | 3.11.18 (CPython), run inside WSL Ubuntu; runtime not yet installed or verified |
| Interpreter binary SHA-256 or container image digest |  |
| Operating system and architecture |  |
| Is the pinned version 3.11.18? | ☒ Yes ☐ No |
| If No: file 50 probe run on the pinned interpreter (date, result file SHA-256) |  |
| If No: identifier and column fixtures re-confirmed on the pinned interpreter before relying on earlier results (M35, M43–M46, M55–M57, M62–M64, P25a, P25b) | ☐ Done ☐ Not yet |

The audit-time Python results were obtained on CPython 3.11.18. They are not pinned-runtime evidence, and file 50 remains NOT RUN until this section is completed.

### 5.2 Implementation scope opened by acceptance

If all of A1–A11 are accepted as written and X14 Option A is selected, Register 16 L47 opens **only**:

> hand-built FIFO specification/mask, harness, F1–F15, parser/assembler hand-tests, and F17 using hand-built FIFO control mutants only.

It does **not** open UART work, confirmatory generation, F16, or any LLM or provider call.

**Owner confirmation:** L47 does not name the F18 fixture suite explicitly. The 144 F18 descriptors use only hand-written inputs and make no LLM call. Running them is treated as part of the “parser/assembler hand-tests”: ☒ Confirmed ☐ Not confirmed (if not confirmed, record the intended scope: \_\_\_\_\_\_\_\_\_\_\_\_).

### 5.3 Evidence bundle, defined before any fixture run

The bundle is defined before the first run so that the implementation audit can verify it.

| Item | Required | Recorded value or location |
| --- | --- | --- |
| Baseline fixture index SHA-256 (`41_F18_Fixture_Inputs/fixture-index.json`) | Must equal `f37808c7a662b8fdf164e27feaef023aadd6dfefaada35d11c3719185d1bde54` | ☐ Verified at run time |
| Interpreter version string and binary/image hash (from 5.1) | Yes |  |
| Parser, assembler and runner source: repository commit and per-file SHA-256 | Yes |  |
| Exact run command(s) and environment variables | Yes |  |
| Per-fixture record: fixture ID, descriptor SHA-256, actual disposition/stage/error class/diagnostic, expected values, match yes/no | Yes, for all 144 |  |
| Raw run logs with timestamps | Yes |  |
| Results file(s) and their SHA-256 | Yes |  |
| Any fixture that failed, errored or was skipped, with its reason | Yes; none may be silently omitted |  |
| Isolation arrangement for any LLM-generated code (none is expected at this stage) | Yes |  |

### 5.4 Independent implementation auditor

| Field | Value |
| --- | --- |
| Auditor (name or system) |  |
| Confirmation that the auditor did not write the implementation or the runner | ☐ Confirmed |
| Audit scope: implementation conforms to the v1.3.6 specification and the evidence bundle is complete and valid | ☐ Agreed |

## 6. Outcome and sign-off

### 6.1 Freeze validity (owner to mark one)

| Outcome | Condition | Consequence | Select |
| --- | --- | --- | --- |
| Freeze valid | All 11 of A1–A11 accepted as written, **and** X14 Option A selected | The v1.3.6 baseline stands. Only the scope in section 5.2 opens. | ☒ |
| Revised release required | Any of A1–A11 rejected or modified, **or** X14 Option B selected | A revised document release and a new independent document audit are required before any implementation. Nothing opens. | ☐ |

### 6.2 Authorization statement

By signing, the owner records the decisions above and nothing else. **This record does not authorize any LLM or provider call, F16, smoke test, provider-format probe, confirmatory generation or the full study.** LLM-call authorization is a separate, later decision. It may be considered only after the independent implementation audit passes, and only by explicit owner authorization in a separate record.

### 6.3 Signature

| Field | Value |
| --- | --- |
| Owner signature |  |
| Printed name (must match section 4) |  |
| Date |  |
| Approver signature (if different from owner) |  |
| Approver printed name and date |  |

**Until this section is signed and dated, the state remains:**

- A1–A11: NOT ACCEPTED.
- X14: OWNER CHOICE REQUIRED.
- Identities: TO CONFIRM.
- Signature and date: NOT RECORDED.
- Authorization: NONE.
