# OpenVEF v1.3.1 Audit

Nov 22, 2026

## (a) Verdict

**Document audit: FAIL (narrow).** v1.3.1 correctly resolves all three v1.3 blockers (N1–N3) and all three smaller v1.3 findings (N4–N6), and each resolution re-checks against the pack bytes. Two blocking contradictions remain:

- **N8 – incomplete closed vocabulary.**
  - *Regression:* v1.3.1 deleted the only declaration of M41's diagnostic `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS`.
  - *Pre-existing:* four fixture error classes are declared in no normative file: `MID_RUN_REEVALUATION`, `TRUNCATION`, `JSON_SERIALIZATION` and `ASSEMBLY_OR_MANIFEST_FAILURE` (the last used by four F18 fixtures).
  - *My miss:* these classes were present in v1.3 and **I missed them in my v1.3 audit**. I marked M14, M17, M18–M20, M40 and M41 as deterministic. That was wrong by the same standard I applied to M53/M54.
- **N9 – async-reason contradiction.** Protocol L135, file 30 and the model-visible B5/B7 text say every `async def` is rejected with `ASYNC_DEFINITION`. The normative precedence in L164 gives a different reason in four cases:
  - `async def create_driver` and `async def step` → `WRONG_ENTRY_POINT_KIND`, from the required-symbol pass.
  - An async `Driver` method other than `step` → `FORBIDDEN_METHOD`, rank 3.
  - A decorated `async def` → `DECORATOR_REJECT`, rank 5.

  No fixture covers any of these four cases, and no fixture uses `WRONG_ENTRY_POINT_KIND` at all.

There are also packaging and version-label regressions (N10, N11). Eleven stale v1.2 files are back in the active top level, and several current files carry wrong version labels.

**LLM-call gate: NOT MET.** This holds regardless of the document verdict:

- A1–A11 are unaccepted and X14 is open.
- No implementation exists.
- All 133 fixtures are NOT RUN.
- The pinned CPython 3.11 patch is TO FREEZE and has not been run.

Nothing is authorized.

**Evidence classes:**

- **\[S\]** document reading.
- **\[H\]** static audit scripts: hashes, assembly reproduction, an audit-only reimplementation of the L164 AST pass and of the L133 identifier rule, and vocabulary cross-checks.
- **\[P311\]** `/usr/bin/python3.11 -I`, which is CPython 3.11.18 and not the pinned patch.
- **\[I\]** project implementation execution. None exists, and none was done.

## (b) v1.3 findings and v1.3.1 corrections

| # | v1.3 finding | v1.3.1 correction (file 52) | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| N1 | M53/M54 lifecycle vocabulary undeclared | M53 error class → `AUTHORING_REVISION_REQUIRED`; the M54 diagnostic and error class are declared at L174 | **RESOLVED.** M53 now maps to the declared author-visible/estimand event, which is the correct §7b study reset. The M54 code and class are in the closed list. Only these two fields changed (M54 changed only `fixture_version`). | \[S\]\[H\] |
| N2 | Stale design-only action literals; fixture actions undeclared | Closed `required_action` list at L175 | **RESOLVED for M48/M50/M53/M54/M58.** All five literals match the fixture bytes exactly. `FULL_DESIGN_RERUN` and `ABORT_REFREEZE` appear nowhere in the active files. §7b scope (L180) is byte-identical to v1.3. **Side effect:** the deleted sentence also held M41's declaration (N8). | \[S\]\[H\] |
| N3 | Nested `async def` not enforced | All `AsyncFunctionDef` nodes deferred to AST\_SIGNATURE at rank 6 with `ASYNC_DEFINITION`; `MODULE_STATEMENT_REJECT.reason` no longer lists it; M59 added | **RESOLVED for nested helpers.** The literal key and "six category ranks" match in Protocol L164/L166, file 25 and file 30 L33. Required-symbol checks still run first. M59 recomputes exactly on \[P311\], and 3.11.18 parses it. The reason-level claims conflict with L164 for required and higher-ranked async definitions (N9). | \[S\]\[H\]\[P311\] |
| N4 | Superseded v1.2 ORG-B hash corrupt | Corrected | **RESOLVED.** The value has 64 hex characters and equals the archived v1.2 sidecar. All six superseded values (v1.1, v1.2, v1.3) match their archives. | \[H\] |
| N5 | Charter §16 stale | Rewritten | **RESOLVED in §16.** It cites `02_…_v1.3.1.md` and records the v1.3 FAIL. The Charter header (L4 "Version: 1.3") and status note (L9 "v1.2 … FAIL", v1.3 change list) are still stale (N11). | \[S\] |
| N6 | File 25 copy omitted three §3.4 bullets | Synchronized | **RESOLVED.** The file 25 copy is 97 lines and 34,545 bytes, byte-identical to Protocol §3.4 L89–L186, including the human-baseline, `k=2` and repair-template bullets. | \[H\] |
| N7 | Optional identifier fixtures | Not added; file 52 says the definitions were unavailable | **OPEN (optional).** Exact definitions are in (g). | \[S\] |
| — | Hash recompute after B5/B7 edits | v1.3.1 prompt hashes | **CONFIRMED.** Both prompts are 13,481 B and match the sidecar; see (d). | \[H\] |
| — | Fixture inventory: 133 (59 P / 13 R / 61 M) | Index regenerated | **CONFIRMED.** Index, files and catalog all list 133, and hashes, lengths and expected objects agree. Only M53, M54 and M59 differ from v1.3. | \[H\] |
| — | v1.3 archive preserved | `archive_v1.3/OpenVEF_Planning_v1.3.zip` | **CONFIRMED.** It is byte-identical to the released v1.3 ZIP. The v1.2 archive is unchanged. | \[H\] |

## (c) Fixture table: all 133 descriptors

**Summary:** 126 deterministic, 6 ambiguous (M14, M17, M18, M19, M20, M40) and 1 contradictory (M41). All seven non-deterministic fixtures fall under N8.

Status describes the **expected outcome only**. No fixture was executed by a project runner.

**\[H\] checks:**

- 133 index entries, files and catalog rows (59 P, 13 R, 61 M), with no duplicates.
- Every SHA-256, byte length and expected object matches the index, and every catalog row's disposition and diagnostic matches its fixture.
- Every fixture's error class, stage, disposition, diagnostic code, reason and `required_action` was cross-checked against the normative text of Protocol v1.3.1, file 25 and file 30. That cross-check is where N8 surfaced.
- An audit-only static model of the L164 required-symbol and 6-rank global pass reproduces M01, M02, M03, M38, M39, M49, M51, M52, M59, P16 and P27. It does not model parameters, so it is silent on P15 and P26.
- The L133 identifier model reproduces M35, M43–M46 and M55–M57 on \[P311\].

Rows without a note are byte-identical to v1.3 and re-check as deterministic.

| ID | Status | Expected: disposition / stage / error class / diagnostic | Note |
| --- | --- | --- | --- |
| P01 | DET | ACCEPT / — / — / `—` |  |
| P02 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P03 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P04 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P05 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P06a | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P06b | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/driver` |  |
| P07 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P08a | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/schema_version` |  |
| P08b | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/language` |  |
| P08c | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/language_version` |  |
| P08d | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/dependencies` |  |
| P09 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P10 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P11a | DET | REPAIR / PARSE\_SCHEMA / OUTPUT\_TRUNCATED / `OUTPUT_TRUNCATED` |  |
| P11b | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/` |  |
| P12a | DET | REPAIR / SOURCE\_AST / SOURCE\_EMPTY / `SOURCE_EMPTY\|file=driver.py` |  |
| P12b | DET | REPAIR / SOURCE\_AST / SOURCE\_EMPTY / `SOURCE_EMPTY\|file=checker.py` |  |
| P13 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_NOT_ALLOWED\|module=os` |  |
| P14 | DET | ACCEPT / — / — / `—` |  |
| P15 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.step\|reason=PARAMETER_NAMES` |  |
| P16 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=MISSING_ENTRY_POINT` | Static AST model: matches. |
| P17 | DET | REPAIR / DRIVER\_VECTOR / DRIVER\_VECTOR\_INVALID / `DRIVER_VECTOR_INVALID\|reason=MISSING_KEYS` |  |
| P18 | DET | REPAIR / CHECKER\_NULL / CHECKER\_RETURN\_INVALID / `CHECKER_RETURN_INVALID\|reason=MISSING_DIAGNOSTICS` |  |
| P19 | DET | REPAIR / CHECKER\_NULL / CHECKER\_RETURN\_INVALID / `CHECKER_RETURN_INVALID\|reason=NON_DICTIONARY` |  |
| P20 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/assumptions/0/clause_id` | Pointer follows the clause rule (unchanged from v1.2). |
| P21 | DET | ACCEPT / — / — / `—` |  |
| P22 | DET | ACCEPT\_WITH\_WARNING / — / — / `DIAGNOSTIC_FORMAT_WARNING` |  |
| P23 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=SUBMODULE_IMPORT` |  |
| P24a | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `PROHIBITED_BUILTIN\|name=exec` |  |
| P24b | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `PROHIBITED_BUILTIN\|name=eval` |  |
| P24c | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `PROHIBITED_BUILTIN\|name=compile` |  |
| P24d | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `PROHIBITED_BUILTIN\|name=open` |  |
| P25a | DET | REPAIR / SOURCE\_AST / SOURCE\_SYNTAX\_REJECT / `SOURCE_SYNTAX_REJECT\|file=driver.py\|line=1\|column=5` | Re-confirm on the pinned 3.11 patch (L127). |
| P25b | DET | REPAIR / SOURCE\_AST / SOURCE\_SYNTAX\_REJECT / `SOURCE_SYNTAX_REJECT\|file=checker.py\|line=1\|column=5` | Re-confirm on the pinned 3.11 patch (L127). |
| P26 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=check_trace\|reason=PARAMETER_NAMES` |  |
| P27 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `DECORATOR_REJECT\|file=driver.py\|symbol=Driver` | Static AST model: matches. |
| P28 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `MODULE_STATEMENT_REJECT\|file=driver.py\|line=1\|reason=MODULE_EXECUTABLE` |  |
| P29a | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=RELATIVE_IMPORT` |  |
| P29b | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=STAR_IMPORT` |  |
| P30 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=FUTURE_FEATURE` |  |
| P31 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=MULTIPLE_NAMES` |  |
| P32 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_NOT_ALLOWED\|module=os` |  |
| P33 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=IMPORT_ALIAS` |  |
| P34 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=IMPORT_ALIAS` |  |
| P35 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_NOT_ALLOWED\|module=os` |  |
| P36 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=FROM_IMPORT_FORBIDDEN` |  |
| P37 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=RELATIVE_IMPORT` |  |
| P38 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=STAR_IMPORT` |  |
| P39 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=MULTIPLE_NAMES` | Multi-name rule precedes the future rule; consistent with P48. |
| P40 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=MULTIPLE_NAMES` |  |
| P41 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=FROM_IMPORT_FORBIDDEN` |  |
| P42 | DET | ACCEPT / — / — / `—` |  |
| P43 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_NOT_ALLOWED\|module=os` |  |
| P44 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=SUBMODULE_IMPORT` |  |
| P45 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=FUTURE_FEATURE` |  |
| P46 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_NOT_ALLOWED\|module=os` |  |
| P47 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=RELATIVE_IMPORT` |  |
| P48 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=MULTIPLE_NAMES` | Consistent with P39. |
| R01 | DET | REPAIR / COMPILE\_DRIVER / COMPILE\_ERROR / `COMPILE_ERROR\|file=driver.py\|line=1` |  |
| R02 | DET | REPAIR / COMPILE\_CHECKER / COMPILE\_ERROR / `COMPILE_ERROR\|file=checker.py\|line=1` |  |
| R03 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_NOT_ALLOWED\|module=os` |  |
| R04 | DET | REPAIR / DRIVER\_RUNTIME / RUNTIME\_EXCEPTION / `RUNTIME_EXCEPTION\|file=driver.py\|phase=step\|class=KeyError` |  |
| R05 | DET | REPAIR / DRIVER\_VECTOR / DRIVER\_VECTOR\_INVALID / `DRIVER_VECTOR_INVALID\|reason=WRONG_WIDTH` |  |
| R06 | DET | REPAIR / DRIVER\_WATCHDOG / WATCHDOG\_TIMEOUT / `WATCHDOG_TIMEOUT\|phase=driver_step` |  |
| R07 | DET | DESIGN\_HALT\_NO\_SLOT\_SCORED / DESIGN\_HALT / RTL\_NULL\_CONTROL\_FAILURE / `RTL_NULL_CONTROL_FAILURE\|reason=MASKED_OUTPUT_DIVERGENCE` |  |
| R08 | DET | REPAIR / CHECKER\_NULL / CHECKER\_RUNTIME\_ERROR / `CHECKER_RUNTIME_ERROR\|class=KeyError` |  |
| R09 | DET | REPAIR / CHECKER\_NULL\_REJECT / CHECKER\_NULL\_REJECT / `The checker returned FAIL on a legal null-netlist trace.` |  |
| R10 | DET | TERMINAL\_INVALID\_NO\_REPAIR / TERMINAL / CHECKER\_NONDETERMINISM / `CHECKER_NONDETERMINISM\|reason=RUN_DISAGREEMENT` |  |
| R11 | DET | TERMINAL\_INVALID\_NO\_REPAIR / TERMINAL / CHECKER\_NONDETERMINISM / `CHECKER_NONDETERMINISM\|reason=RUN_DISAGREEMENT` |  |
| R12 | DET | DESIGN\_HALT\_NO\_SLOT\_SCORED / DESIGN\_HALT / TRACE\_INTEGRITY\_FAILURE / `TRACE_INTEGRITY_FAILURE\|reason=ROW_ALIGNMENT` |  |
| R13 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/driver` |  |
| M01 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.__init__\|reason=FORBIDDEN_METHOD` | Static AST model on 3.11.18: matches. |
| M02 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=Helper\|reason=CLASS_FORBIDDEN` | Static AST model: matches. |
| M03 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `DECORATOR_REJECT\|file=driver.py\|symbol=Driver` | Static AST model: matches. |
| M04a | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `MODULE_STATEMENT_REJECT\|file=driver.py\|line=1\|reason=NON_LITERAL_CONSTANT` |  |
| M04b | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `MODULE_STATEMENT_REJECT\|file=driver.py\|line=1\|reason=MODULE_CONTROL_FLOW` |  |
| M05 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=PARAMETER_KIND` |  |
| M06 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=RETURN_TYPE` |  |
| M07 | DET | ACCEPT / — / — / `—` |  |
| M08a | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=FROM_IMPORT_FORBIDDEN` |  |
| M08b | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=SUBMODULE_IMPORT` |  |
| M09 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `GLOBAL_RANDOM_USE\|name=random.random` |  |
| M10 | DET | REPAIR / CHECKER\_NULL / CHECKER\_TIMEOUT / `CHECKER_TIMEOUT\|phase=null_check` |  |
| M11 | DET | TERMINAL\_INVALID\_NO\_REPAIR / TERMINAL / CHECKER\_NONDETERMINISM / `CHECKER_NONDETERMINISM\|reason=RUN_DISAGREEMENT` |  |
| M12 | DET | ACCEPT\_WITH\_WARNING / — / — / `DIAGNOSTIC_FORMAT_WARNING` |  |
| M13 | DET | DESIGN\_HALT\_NO\_SLOT\_SCORED / DESIGN\_HALT / EVALUATOR\_INFRASTRUCTURE\_FAILURE / `SIMULATOR_ERROR\|target=null\|class=RuntimeError` |  |
| M14 | AMBIGUOUS | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / TRUNCATION / `contains_marker=True; output_diagnostic_bytes=2047` | Error class `TRUNCATION` is not declared in Protocol, file 25 or file 30 (N8; pre-existing, missed in my v1.3 audit). |
| M15 | DET | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / FEEDBACK\_SERIALIZER\_REJECT / `FEEDBACK_SERIALIZER_REJECT\|reason=NON_NORMATIVE_DIAGNOSTIC` |  |
| M16 | DET | REPAIR / SOURCE\_AST / SOURCE\_EMPTY / `SOURCE_EMPTY\|file=driver.py` |  |
| M17 | AMBIGUOUS | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / JSON\_SERIALIZATION / `diagnostic_sha256=226a87deb777b94556d262a0e45e669ced8c80f5cf8ec1bc3d691e9d4570423f` | Error class `JSON_SERIALIZATION` is not declared (N8; pre-existing). |
| M18 | AMBIGUOUS | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `PACKET_FREEZE_REJECT\|reason=RESERVED_HEADING_LINE` | Error class `ASSEMBLY_OR_MANIFEST_FAILURE` is not declared; the diagnostic is declared (N8; pre-existing). |
| M19 | AMBIGUOUS | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `ASSEMBLY_REJECT\|reason=UNRESOLVED_PLACEHOLDER` | Error class not declared (N8; pre-existing). |
| M20 | AMBIGUOUS | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `F18_REJECT\|reason=VISIBLE_CLAUSE_ID_SET_MISMATCH` | Error class not declared (N8; pre-existing). |
| M21 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=IMPORT_ALIAS` |  |
| M22 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `GLOBAL_RANDOM_USE\|name=random.SystemRandom` |  |
| M23 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `GLOBAL_RANDOM_USE\|name=random.randint` |  |
| M24 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `PROHIBITED_BUILTIN\|name=open` |  |
| M25 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.step\|reason=RUNTIME_SIGNATURE` |  |
| M26 | DET | REPAIR / DRIVER\_VECTOR / DRIVER\_VECTOR\_INVALID / `DRIVER_VECTOR_INVALID\|reason=EXTRA_KEYS` |  |
| M27 | DET | REPAIR / DRIVER\_VECTOR / DRIVER\_VECTOR\_INVALID / `DRIVER_VECTOR_INVALID\|reason=ILLEGAL_PROTOCOL_STATE` |  |
| M28 | DET | TERMINAL\_INVALID\_NO\_REPAIR / TERMINAL / DRIVER\_NONDETERMINISM / `DRIVER_NONDETERMINISM\|reason=NEXT_INPUT_DIVERGENCE` |  |
| M29 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_NOT_ALLOWED\|module=os` |  |
| M30 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/dependencies` |  |
| M31 | DET | REPAIR / CHECKER\_NULL / CHECKER\_RETURN\_INVALID / `CHECKER_RETURN_INVALID\|reason=TOP_LEVEL_KEYS` |  |
| M32 | DET | REPAIR / CHECKER\_NULL / CHECKER\_RETURN\_INVALID / `CHECKER_RETURN_INVALID\|reason=INVALID_VERDICT` |  |
| M33 | DET | REPAIR / CHECKER\_NULL / CHECKER\_RETURN\_INVALID / `CHECKER_RETURN_INVALID\|reason=DIAGNOSTICS_NOT_LIST` |  |
| M34 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `PROHIBITED_BUILTIN\|name=__import__` |  |
| M35 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=5` | Recomputed on 3.11.18: column 5. |
| M36 | DET | CONTROL\_EXPECTATION / SOURCE\_AST / SOURCE\_SYNTAX\_REJECT / `SOURCE_SYNTAX_REJECT\|file=driver.py\|line=4\|column=1` |  |
| M37 | DET | TERMINAL\_INVALID\_NO\_REPAIR / TERMINAL / DRIVER\_NONDETERMINISM / `DRIVER_NONDETERMINISM\|reason=NEXT_INPUT_DIVERGENCE` |  |
| M38 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `DECORATOR_REJECT\|file=driver.py\|symbol=helper` | Static AST model: matches. |
| M39 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: matches (rank 1). |
| M40 | AMBIGUOUS | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `F18_REJECT\|reason=MALFORMED_CLAUSE_ID_TOKEN` | Error class not declared (N8; pre-existing). |
| M41 | **CONTRADICTORY** | CONTROL\_EXPECTATION / DESIGN\_HALT / MID\_RUN\_REEVALUATION / `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` | **Regression.** This diagnostic was declared in v1.3 L174 but deleted in v1.3.1, and error class `MID_RUN_REEVALUATION` is declared nowhere (N8). |
| M42 | DET | DESIGN\_ABORTED\_NO\_SLOTS\_SCORED / DESIGN\_HALT / DESIGN\_HALT\_REPEATED / `DESIGN_HALT_REPEATED\|reason=EVALUATOR_FAILURE_REPRODUCED` |  |
| M43 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=19` | Byte column 19 (character column would be 18). |
| M44 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=8` | Recomputed: column 8. |
| M45 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=17` | Recomputed: column 17. |
| M46 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=1\|column=5` | Recomputed: column 5. |
| M47 | DET | DESIGN\_ABORTED\_NO\_SLOTS\_SCORED / DESIGN\_HALT / DESIGN\_HALT\_REPEATED / `DESIGN_HALT_REPEATED\|reason=SECOND_HALT_AFTER_RECOVERY` |  |
| M48 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / EVALUATOR\_REVISION\_REQUIRED / `EVALUATOR_REVISION_REQUIRED\|reason=FROZEN_EVALUATOR_CHANGED` | `required_action` is the declared literal at L175. |
| M49 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=MISSING_ENTRY_POINT` | Static AST model: required symbols before categories. |
| M50 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | `required_action` declared (L175); scope all designs × all arms. |
| M51 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=nested_holder.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: rank 1 beats rank 5 in the same file. |
| M52 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=nested_holder.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: global pass across files. |
| M53 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | **Resolved.** Error class declared (L174); `required_action` declared (L175). |
| M54 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / HALT\_SIGNATURE\_SCHEMA / `HALT_SIGNATURE_SCHEMA\|reason=COMPONENT_VALUES_ENUMERATED` | **Resolved.** Diagnostic and error class declared (L174); `required_action` declared (L175). |
| M55 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=1` | 3.11.18: ERRORTOKEN `℘` at (1,0); byte column 1. |
| M56 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=5` | 3.11.18: NAME `a` + ERRORTOKEN `℘`; byte column 5. |
| M57 | DET | ACCEPT / — / — / `—` | Non-ASCII appears only in STRING and COMMENT tokens. |
| M58 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | `required_action` declared (L175); scope is the affected design in both arms. |
| M59 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper.nested_async\|reason=ASYNC_DEFINITION` | **New.** Python 3.11.18 parses it; required symbols pass; rank 6 gives `helper.nested_async`. |

## (d) Hash and assembly results

All values are recomputed \[H\] from the pack bytes by audit scripts, not by the project assembler.

| Object | Bytes | SHA-256 (recomputed) | Record | Result |
| --- | --- | --- | --- | --- |
| Response schema (34) | 2,529 | `6fb5d282b09540949f21ee134b522841c3345031cb3e118a83bdffc18b4e7c34` | Sidecar | PASS |
| System message (25) | 602 | `98020d4f9cf818968f15e4a7c0a5adc3633694aa98c5cbfe170b0904aee3c7a4` | Sidecar | PASS |
| Repair message (25) | 621 | `f11d574f4e5afb223a096b74f039ecb6a222d6ed6dc5bcf7f115dc5922c2620d` | Sidecar | PASS |
| ORG-A template stage, v1.3.1 | 13,481 | `b63be015dbf5c8c4dd6ab518d092fd523dc113dd430a4e4826c551f8de8fe7af` | Sidecar and file 53 | PASS |
| ORG-B template stage, v1.3.1 | 13,481 | `cdfcc0acb306337247acd0b0c68df42c375a480e328fc41ecc7b334391c349d8` | Sidecar and file 53 | PASS |
| Superseded v1.1 ORG-A / ORG-B | 12,004 | `de1b8d40…b3be` / `4c55f297…fd56` | v1.1 history | PASS |
| Superseded v1.2 ORG-A / ORG-B | 12,187 | `0546e8d2…a252` / `363fcf2d34de08afaeef6a683ec9affb2c2158d4aa23b79032baab3adcdb603d` (64 hex) | Archived v1.2 sidecar | PASS (N4 resolved) |
| Superseded v1.3 ORG-A / ORG-B | 12,957 | `a028311e…c012` / `fc88102d…6c72e` | Archived v1.3 sidecar | PASS |

**Assembly \[H\]:**

- **Rule.** I used the token-only schema-insertion rule: strip 3 metadata lines plus 1 blank line; render each block as heading, LF, then the trimmed body; join blocks with two LFs; end with one terminal LF. This reproduces both 13,481-byte values exactly.
- **Block order.** ORG-A is B0–B8 in order. ORG-B is B0, B2, B5, B1, B6, B3, B7, B4, B8, which matches the sidecar's `arm_orders`. The two arms contain an identical multiset of rendered blocks, so they differ only by block order.
- **B5/B7 against file 30.** The fixed texts in file 30 §3.1 (B5 3,298 B, B7 2,710 B, B8 3,310 B) are exact byte prefixes of the corresponding block bodies in both arms.
- **Two-LF boundaries.** Each fixed text is followed by exactly `\n\n`, then `Design-specific API and top-level port…` (B5), `Design-specific checker obligations…` (B7) and `BEGIN_OPENVEF_RESPONSE_SCHEMA_JSON` (B8).
- **Async sentence.** The new sentence ("Every `async def` is prohibited at every lexical depth …") is present in B5 and B7 of ORG-A (L25, L40), ORG-B (L16, L37) and file 30 (L52, L64). Apart from that sentence, the ORG-A diff from v1.3 is empty.
- **Schema substitution.** The substituted schema equals `json.dumps(indent=2)` plus LF, followed by the template LF.

**Copy of Protocol §3.4 in file 25 \[H\]:** It is byte-identical: 97 lines, 34,545 bytes, Protocol L89–L186 against file 25 L33 onward. It includes the human-baseline, `k=2` and repair-template bullets, the L174 and L175 vocabulary, and the L164 6-rank key.

**Package \[H\]:**

- `unzip -t` is clean.
- `27_SHA256SUMS.txt` lists 242 entries, all OK. Only the manifest itself is uncovered.
- `archive_v1.3/OpenVEF_Planning_v1.3.zip` is byte-identical to the released v1.3 ZIP, and the v1.2 archive is byte-identical to v1.2.
- Every file reference in the current files resolves to an existing file.
- The checksummed set includes the 11 stale files described in N10.

**Python runtime \[P311\], CPython 3.11.18:**

- `ast.parse` accepts M59's nested `async def`.
- The identifier columns (M35, M43–M46, M55–M57) are unchanged and match.
- Async cases outside the fixtures (computed with the audit model of L164):
  - `async def create_driver` → `WRONG_ENTRY_POINT_KIND`
  - `async def step` → `WRONG_ENTRY_POINT_KIND`
  - an async `Driver.extra` → `FORBIDDEN_METHOD`
  - a decorated module-level `async def` → `DECORATOR_REJECT`
  - a plain module-level `async def h` → `ASYNC_DEFINITION`
- This is not the pinned interpreter, so file 50 stays NOT RUN and Python 3.11 compatibility is not marked PASS.

## (e) Cross-document contradictions

| # | Location A | Location B | Contradiction | Severity |
| --- | --- | --- | --- | --- |
| E1 | Protocol L174–L175 and file 25: the closed lifecycle/control vocabulary and `required_action` list | M41.json, index L567–L568, catalog L147 | M41's diagnostic `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` was declared in v1.3 L174 and deleted in v1.3.1. Its error class `MID_RUN_REEVALUATION` is declared nowhere. The only other occurrence of the diagnostic is in the non-controlling stale `02_…_v1.2.md`. | Blocking (N8) |
| E2 | Protocol, file 25 and file 30 (none declares these classes); file 36 requirement 2 ("a single exact expected … error") | M14 `TRUNCATION`, M17 `JSON_SERIALIZATION`, M18/M19/M20/M40 `ASSEMBLY_OR_MANIFEST_FAILURE` | The expected error classes have no normative source. They are pre-existing since v1.2 or earlier, and my v1.3 audit missed them. | Blocking (N8) |
| E3 | Protocol L135 ("every `ast.AsyncFunctionDef` … emits … `ASYNC_DEFINITION`"); file 30 L29 and L33; B5/B7 in both arms and file 30 L52/L64 ("the parser rejects each such definition … with … `ASYNC_DEFINITION`") | Protocol L164 and file 30 L33: the required-symbol pass runs first and ranks 3 and 5 outrank rank 6 | For `async def create_driver`, `async def step`, an async non-`step` `Driver` method or a decorated `async def`, the normative precedence emits a different reason than the absolute async sentence promises. The model-visible contract is therefore false for those inputs. File 30 L33 also says "non-synchronous `FunctionDef`", while the Protocol says "non-`FunctionDef`". | Blocking (N9) |
| E4 | README "Current controlling files"; v1.3 had no such files at top level | Top-level `01/02/03/21/23/30/31/36_…_v1.2.md`, `16_OpenVEF_v1.2_…`, `32_v1.2_…` and `49_….xlsx` | Eleven stale v1.2 files were reintroduced next to the v1.3.1 files. Each is byte-identical to the v1.2 archive, all are checksummed as part of the release, and the README does not mention them. | Correction (N10) |
| E5 | README, file 32, Charter §16 | Protocol L1 and catalog L1 ("v1.3.1.1"); Charter L4 ("Version: 1.3") and L9 ("v1.2 … FAIL" plus the v1.3 change list); Protocol L554 ("expanded 132-fixture set", "document-only v1.3 re-audit") and L558 ("following the v1.2 … FAIL", the v1.3 change list, "until B1–B9") | There are version-label and history contradictions, and the fixture count is stale (132 against 133). | Correction (N11) |
| E6 | Sidecar `hash_status_note` (B5/B7 edits; v1.1, v1.2 and v1.3 superseded) | File 32 L21 ("after B5/B8 changes; v1.1 and v1.2 values are marked superseded") | File 32 is stale and does not list any v1.3.1 correction (async, M59). | Correction (N11) |

No contradiction was found in owner or authorization state across README, file 32, register 16, approval record 23, fixture index status and file 52.

## (f) New blockers

| ID | Blocker | Why it blocks | Evidence |
| --- | --- | --- | --- |
| N8 | The closed lifecycle/control/F18 vocabulary does not cover every fixture expectation. M41's diagnostic declaration was **removed in v1.3.1**. `MID_RUN_REEVALUATION`, `TRUNCATION`, `JSON_SERIALIZATION` and `ASSEMBLY_OR_MANIFEST_FAILURE` are declared nowhere. | Seven fixtures (M14, M17, M18, M19, M20, M40, M41) expect values that no normative rule produces. This is the same defect class as v1.3 N1. I missed the six pre-existing cases in my v1.3 audit, so this is a correction to my earlier report as well as a pack defect. | \[S\]\[H\] |
| N9 | The absolute async-reason claim conflicts with the L164 precedence | The Protocol (L135), file 30 and the model-visible B5/B7 text promise `ASYNC_DEFINITION` for every `async def`. L164 yields `WRONG_ENTRY_POINT_KIND`, `FORBIDDEN_METHOD` or `DECORATOR_REJECT` for async required symbols, async extra `Driver` methods and decorated async definitions. No fixture exercises these cases or `WRONG_ENTRY_POINT_KIND`. | \[S\]\[H\]; cases computed on \[P311\] with the audit model |

These items are corrections but not blockers:

- **N10:** eleven stale v1.2 files in the active top level.
- **N11:** version labels and stale history text in Protocol L1/L554/L558, catalog L1, Charter L4/L9 and file 32 L21.
- **N7 (optional):** coverage for identifier edge cases.

**Gate condition, not a document defect.** The pinned Python 3.11 patch must be frozen, and file 50 plus the column fixtures must be run on it.

## (g) Prioritized exact-edit list

These are proposed edits only. The pack was not modified.

1. **P0 – N8.** Add to Protocol L174 and its file 25 copy:
   - “`RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` (error class `MID_RUN_REEVALUATION`) is the M41 control-expectation diagnostic for a successful operational recovery. It discards pre-halt scores, reruns preflight, and re-evaluates every scheduled slot in the affected scope with identical artifact bytes and seeds and zero new confirmatory generation calls.”
   - “`F18_REJECT` fixtures use error class `ASSEMBLY_OR_MANIFEST_FAILURE`. The M14 truncation primitive uses error class `TRUNCATION`. The M17 JSON-escaping primitive uses error class `JSON_SERIALIZATION`. These are local F18 ledger labels, never model feedback.”
   - Keep the resulting list closed.
2. **P0 – N9.**
   - **Protocol L135 and file 25.** Replace “is checked exactly once at `AST_SIGNATURE` and emits `ENTRY_POINT_REJECT|file=<FILE>|symbol=<SYMBOL>|reason=ASYNC_DEFINITION`” with: “is checked exactly once at `AST_SIGNATURE` under the precedence below. An async binding of a required symbol (`create_driver`, `Driver.step`, `check_trace`) emits `WRONG_ENTRY_POINT_KIND` in the required-symbol pass. An async direct `Driver` method other than `step` emits `FORBIDDEN_METHOD` (rank 3). A decorated async definition emits `DECORATOR_REJECT` (rank 5). Every other async definition emits `ENTRY_POINT_REJECT|file=<FILE>|symbol=<SYMBOL>|reason=ASYNC_DEFINITION` (rank 6).”
   - **File 30 L29.** Mirror the same change.
   - **File 30 L33.** Change “exactly one non-synchronous `FunctionDef` binding” to “exactly one non-`FunctionDef` binding (including `AsyncFunctionDef`)”.
   - **B5 and B7 in both arms, and file 30 §3.1.** Change “the parser rejects each such definition at `AST_SIGNATURE` with `ENTRY_POINT_REJECT` reason `ASYNC_DEFINITION`” to “the parser rejects each such definition at `AST_SIGNATURE`”. Alternatively, state the four-way rule above. Then recompute the prompt hashes and mark the v1.3.1 hashes as superseded.
   - **Add fixtures.** Both use the M59 base driver and the standard checker:
     - (i) `async def create_driver(seed):` → `REPAIR` / `AST_SIGNATURE` / `ENTRY_POINT_REJECT` / `ENTRY_POINT_REJECT|file=driver.py|symbol=create_driver|reason=WRONG_ENTRY_POINT_KIND`.
     - (ii) `     async def step(self, cycle_index, outputs_after_edge): ` → `ENTRY_POINT_REJECT|file=driver.py|symbol=Driver.step|reason=WRONG_ENTRY_POINT_KIND`.
     - Both were recomputed with the audit model on \[P311\].
3. **P1 – N10.** Remove these files from the active top level. Each is byte-identical to its copy inside `archive_v1.2/OpenVEF_Planning_v1.2.zip`:
   - `01_…_v1.2.md`, `02_…_v1.2.md`, `03_…_v1.2.md`, `16_OpenVEF_v1.2_…`, `21_…_v1.2.md`, `23_…_v1.2.md`, `30_…_v1.2.md`, `31_…_v1.2.md`, `32_v1.2_…`, `36_…_v1.2.md`
   - `49_OpenVEF_v1.2_Audit_Tracker.xlsx` (a copy already exists in `archive_v1.2/`)
   - Then regenerate `27_SHA256SUMS.txt`.
4. **P1 – N11.**
   - **Protocol L1 and catalog L1:** `v1.3.1.1` → `v1.3.1`.
   - **Charter L4:** “Version: 1.3.1 …”.
   - **Charter L9:** “The v1.3 independent document audit returned FAIL … This v1.3.1 pack addresses the M53/M54 lifecycle vocabulary, closed lifecycle action literals, async-definition enforcement, …”.
   - **Protocol L554:** “index the 133-fixture set” and “(2) Obtain an independent document-only v1.3.1 re-audit”.
   - **Protocol L558:** “following the v1.3 independent `FAIL for the LLM-call gate` audit”, followed by the v1.3.1 change list. Replace “until B1–B9 and all mandatory fixtures receive a further independent re-audit” with “until the gates in this section are met”.
   - **File 32 L21:** “Prompt-stage hashes were recomputed after the v1.3.1 B5/B7 edits; v1.1, v1.2 and v1.3 values are marked superseded.” Also add the async, M59 and M53/M54 status lines.
5. **P2 – N7 (optional; exact definitions, computed on \[P311\] 3.11.18).** Each uses the M59 base driver and the standard checker, varied as follows:
   - Prepend `x·y = 1` to driver.py → `NON_ASCII_IDENTIFIER|file=driver.py|line=1|column=1`.
   - Prepend `def ℘f():` with body `     return None ` to driver.py → `NON_ASCII_IDENTIFIER|file=driver.py|line=1|column=5`.
   - Make the checker's line 2 `     s = "é"; a℘ = 1 ` → `NON_ASCII_IDENTIFIER|file=checker.py|line=2|column=15`. Its character column would be 14.
6. **Housekeeping.**
   - Update the fixture index, catalog and counts; files 51, 52 and 53; change log 03; README; and `27_SHA256SUMS.txt`.
   - Archive v1.3.1 byte-for-byte as `archive_v1.3.1/`.

## (h) Owner and authorization status

The status is consistent across README, file 32 (L26–34), register 16 and approval record 23 (L4, L23–28, L42, L48–50, L57–61):

- A1–A11: **PROPOSED / NOT ACCEPTED**, with owner acceptance `PENDING`.
- X14: **OWNER CHOICE REQUIRED**.
- Owner legal name, TEEP applicant, contributors and approver: **TO CONFIRM**.
- Signature and date: **NOT RECORDED**.
- Authorization: **NONE**.

No identity is inferred.

The required order is unchanged:

1. Independent document audit. v1.3.1 fails it; a v1.3.2 is needed.
2. The owner records A1–A11 and the X14 choice.
3. Implementation, with all mandatory fixtures run on the pinned CPython 3.11.
4. Independent audit of the implementation.
5. Only then, consideration of the LLM-call gate.

A document PASS would satisfy only step 1.

**Evidence boundaries:**

- **\[S\] and \[H\]:** all document, vocabulary, fixture-descriptor, hash, assembly and packaging results.
- **\[P311\], CPython 3.11.18, not the pinned patch:** that `ast.parse` accepts M59 and the async cases, and the identifier columns. Python 3.11 compatibility is **not marked PASS**.
- **Audit-only models:** the AST-pass and identifier reimplementations are audit scripts, not the project parser. No project parser, assembler, harness, simulator or F1–F18 was implemented or run (\[I\]: none).
- **Not done:** no LLM or provider call, no F16, no format probe, and no source PDF or literature verification.
