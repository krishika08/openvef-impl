# OpenVEF v1.3.2 Audit

Nov 23, 2026

## Verdict

**Document audit: FAIL (one narrow blocker).** v1.3.2 resolves N8, N9, N10 and N11 from the v1.3.1 audit, and every resolution reproduces against the pack bytes. All 138 fixture descriptors are consistent and deterministic, and every expected value now traces to a normative definition.

One new blocker, **N12**, remains. It is the same kind of defect as v1.3 N3, and the fix is one sentence plus one fixture:

- **Async generator expressions are forbidden but not enforced.** File 30 L29 and the model-visible B5/B7 text in both arms forbid “async comprehensions” and say async generators are “covered by their `AsyncFunctionDef`”. On CPython 3.11.18, an async generator expression such as `(x async for x in y)` inside a synchronous helper passes both `ast.parse` and `compile()`. It contains no `AsyncFunctionDef`, and no stage or diagnostic rejects it.
- **This corrects my v1.3 edit list.** I wrote there that the other async-only constructs “are already `SyntaxError` on 3.11 and need no rule”. That was wrong in two ways. On 3.11.18, `await`, `async for`, `async with` and async list comprehensions inside a synchronous function pass `ast.parse` and fail only at `compile()`, so they would surface as `COMPILE_ERROR`, not at `SOURCE_AST`. Async generator expressions don't fail at all.

There are three non-blocking cleanup items (C1–C3, below).

**LLM-call gate: NOT MET, and nothing is authorized.** A document PASS would not change this:

- A1–A11: NOT ACCEPTED.
- X14: OWNER CHOICE REQUIRED.
- Identities: TO CONFIRM.
- Authorization: NONE.
- No parser, assembler or harness exists, all 138 fixtures are NOT RUN, and the pinned CPython 3.11 patch is TO FREEZE.

**Evidence classes:**

- **\[S\]** document reading of the pack.
- **\[H\]** static audit scripts: SHA-256, assembly reproduction, vocabulary cross-checks, and audit-only reimplementations of the L164 AST pass and the L133 identifier rule.
- **\[P311\]** `/usr/bin/python3.11 -I`, which is CPython 3.11.18. It is not the pinned patch.
- **\[I\]** project implementation execution. None exists, and none was performed.

No parser, assembler, F18, harness or simulator was run. No LLM or provider call was made, and no source PDF was opened.

## Scope items 1–12

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Active root, archives, controlling files | **PASS.** The active root is `OpenVEF_Planning_v1_3_2/`. The README's controlling-file list matches the files present, and every file reference in the current documents resolves. Historical archives are `archive_v0.6` through `archive_v1.3.1`. Kept historical files at the top level: `03_Change_Log_v1.3.1_Historical.md`, `22_…_v1.2.md`, `47_…_v1.2.md`, `48_…_v1.3.1_…_Historical.txt` and `54_OpenVEF_v1.3.1_Independent_Audit.md`. | \[S\]\[H\] |
| 2a | N8 – closed vocabulary | **RESOLVED.** Protocol L174 declares `ASSEMBLY_OR_MANIFEST_FAILURE`, `TRUNCATION` and `JSON_SERIALIZATION` as local-only F18 labels. L175 declares `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` with error class `MID_RUN_REEVALUATION`. A cross-check of every fixture's disposition, stage, error class, diagnostic code, reason and `required_action` against Protocol, file 25 and file 30 finds **zero** undeclared values across 138 fixtures. | \[H\] |
| 2b | N9 – async precedence | **RESOLVED.** See item 5. | \[S\]\[H\] |
| 2c | N10 – stale v1.2 files | **RESOLVED.** See item 8. | \[H\] |
| 2d | N11 – version labels | **RESOLVED.** See item 9. | \[S\] |
| 3 | 138 fixtures (59 P, 13 R, 66 M) | **PASS.** Index, files and catalog each list 138 unique ids. Every SHA-256, byte length, `fixture_id` and expected object matches the index, and each catalog row's disposition and diagnostic match. The index says `NOT RUN / NOT PASSED`. This is descriptor consistency only; nothing was executed. | \[H\] |
| 4 | Protocol §3.4 against file 25 | **PASS.** The two are byte-identical: 98 lines and 35,558 bytes, Protocol L89–L188 against file 25 from L33. | \[H\] |
| 5 | Async precedence | **PASS for `async def`.** Protocol L135, file 30 L29 and L33, and file 25 all state the four-way rule: a required async symbol gives `WRONG_ENTRY_POINT_KIND`, an extra async `Driver` method gives `FORBIDDEN_METHOD` (rank 3), a decorated async definition gives `DECORATOR_REJECT` (rank 5), and any other gives `ASYNC_DEFINITION` (rank 6). File 30 L33 says “exactly one non-`FunctionDef` binding (including `AsyncFunctionDef`)”. B5/B7 in both arms and in file 30 §3.1 no longer promise a specific reason. **FAIL for async generator expressions (N12).** | \[S\]\[H\]\[P311\] |
| 6 | Local-only F18/serializer labels | **PASS.** Each label is declared as “local F18 ledger labels, never model feedback” (L174) and “never serialized to an LLM” (L175). None appears in B0–B8 or in the system or repair message. | \[S\]\[H\] |
| 7 | M60–M64 | **PASS on outcomes.** All five sources pass `ast.parse` and `compile()` on \[P311\]. The static AST model reproduces M60 and M61, and the identifier model reproduces M62 (column 1), M63 (column 5) and M64 (byte column 15, character column 14). **The M64 note in file 52 rests on a misreading (C1).** | \[H\]\[P311\] |
| 8 | Stale v1.2 files and the v1.2 archive | **PASS.** None of the eleven files is at the top level. `archive_v1.2/` still holds the v1.2 ZIP, byte-identical to earlier copies, plus the `.xlsx`. | \[H\] |
| 9 | Titles, versions, history | **PASS.** Protocol and catalog titles say `v1.3.2`. The Charter's version line says 1.3.2, and its status note and §16 record the v1.3 and v1.3.1 FAILs and cite the v1.3.2 Protocol. Protocol L555 says 138 fixtures and v1.3.2; L559 says “following the v1.3.1 … FAIL”. File 32 L22 says v1.1, v1.2, v1.3 and v1.3.1 are superseded. No `v1.3.1.1`, `132-fixture` or stale `133` counts remain in the current files. | \[S\]\[H\] |
| 10 | Prompt hashes | **PASS.** See the hashes section. | \[H\] |
| 11 | v1.3.1 archive | **PASS.** `archive_v1.3.1/OpenVEF_Planning_v1.3.1.zip` is byte-identical to the released v1.3.1 ZIP. `54_…` and `archive_v1.3.1/OpenVEF_v1.3.1_Audit.md` are byte-identical to the audit export I delivered. | \[H\] |
| 12 | SHA-256 manifest | **PASS.** `27_SHA256SUMS.txt` lists 239 entries, all OK. Only the manifest itself is excluded, and that exclusion is stated in file 51 L18. The ZIP holds 240 files. | \[H\] |

## Fixture table: all 138 descriptors

**Summary:** all 138 are deterministic. None is ambiguous or contradictory.

Status describes the **expected outcome only**. No fixture was executed by a project runner.

**\[H\] checks:**

- Index, file and catalog equality; SHA-256, byte length and expected object for every fixture.
- Vocabulary traceability for every field against Protocol, file 25 and file 30: zero undeclared values.
- An audit-only static model of the L164 AST pass reproduces M01, M02, M03, M38, M39, M49, M51, M52, M59, M60, M61, P16 and P27. It does not model parameters, so it is silent on P15 and P26.
- The L133 identifier model on \[P311\] reproduces M35, M43–M46 and M55–M57, plus M62–M64.

Rows without a note are byte-identical to v1.3.1 and re-check as deterministic.

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
| P20 | DET | REPAIR / PARSE\_SCHEMA / SCHEMA\_REJECT / `SCHEMA_REJECT\|pointer=/assumptions/0/clause_id` | The pointer follows the clause rule. |
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
| P39 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `IMPORT_FORM_REJECT\|file=driver.py\|line=1\|reason=MULTIPLE_NAMES` | The multi-name rule precedes the future rule; consistent with P48. |
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
| M01 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.__init__\|reason=FORBIDDEN_METHOD` | Static AST model: matches. |
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
| M14 | DET | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / TRUNCATION / `contains_marker=True; output_diagnostic_bytes=2047` | **Resolved:** `TRUNCATION` is declared at Protocol L174. |
| M15 | DET | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / FEEDBACK\_SERIALIZER\_REJECT / `FEEDBACK_SERIALIZER_REJECT\|reason=NON_NORMATIVE_DIAGNOSTIC` |  |
| M16 | DET | REPAIR / SOURCE\_AST / SOURCE\_EMPTY / `SOURCE_EMPTY\|file=driver.py` |  |
| M17 | DET | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / JSON\_SERIALIZATION / `diagnostic_sha256=226a87deb777b94556d262a0e45e669ced8c80f5cf8ec1bc3d691e9d4570423f` | **Resolved:** `JSON_SERIALIZATION` is declared at L174. |
| M18 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `PACKET_FREEZE_REJECT\|reason=RESERVED_HEADING_LINE` | **Resolved:** `ASSEMBLY_OR_MANIFEST_FAILURE` is declared at L174. |
| M19 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `ASSEMBLY_REJECT\|reason=UNRESOLVED_PLACEHOLDER` | **Resolved** (L174). |
| M20 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `F18_REJECT\|reason=VISIBLE_CLAUSE_ID_SET_MISMATCH` | **Resolved** (L174). |
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
| M35 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=5` | 3.11.18: column 5. |
| M36 | DET | CONTROL\_EXPECTATION / SOURCE\_AST / SOURCE\_SYNTAX\_REJECT / `SOURCE_SYNTAX_REJECT\|file=driver.py\|line=4\|column=1` |  |
| M37 | DET | TERMINAL\_INVALID\_NO\_REPAIR / TERMINAL / DRIVER\_NONDETERMINISM / `DRIVER_NONDETERMINISM\|reason=NEXT_INPUT_DIVERGENCE` |  |
| M38 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `DECORATOR_REJECT\|file=driver.py\|symbol=helper` | Static AST model: matches. |
| M39 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: matches (rank 1). |
| M40 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `F18_REJECT\|reason=MALFORMED_CLAUSE_ID_TOKEN` | **Resolved** (L174). |
| M41 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / MID\_RUN\_REEVALUATION / `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` | **Resolved:** the diagnostic and `MID_RUN_REEVALUATION` are declared at L175. |
| M42 | DET | DESIGN\_ABORTED\_NO\_SLOTS\_SCORED / DESIGN\_HALT / DESIGN\_HALT\_REPEATED / `DESIGN_HALT_REPEATED\|reason=EVALUATOR_FAILURE_REPRODUCED` |  |
| M43 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=19` | Byte column 19 (character column would be 18). |
| M44 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=8` | 3.11.18: column 8. |
| M45 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=17` | 3.11.18: column 17. |
| M46 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=1\|column=5` | 3.11.18: column 5. |
| M47 | DET | DESIGN\_ABORTED\_NO\_SLOTS\_SCORED / DESIGN\_HALT / DESIGN\_HALT\_REPEATED / `DESIGN_HALT_REPEATED\|reason=SECOND_HALT_AFTER_RECOVERY` |  |
| M48 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / EVALUATOR\_REVISION\_REQUIRED / `EVALUATOR_REVISION_REQUIRED\|reason=FROZEN_EVALUATOR_CHANGED` | `required_action` is declared (L176). |
| M49 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=MISSING_ENTRY_POINT` | Static AST model: required symbols are checked before categories. |
| M50 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | `required_action` is declared (L176); scope is all designs × all arms. |
| M51 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=nested_holder.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: rank 1 beats rank 5. |
| M52 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=nested_holder.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: global pass across files. |
| M53 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | Error class and `required_action` are declared (L175–L176). |
| M54 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / HALT\_SIGNATURE\_SCHEMA / `HALT_SIGNATURE_SCHEMA\|reason=COMPONENT_VALUES_ENUMERATED` | Diagnostic, error class and `required_action` are declared (L175–L176). |
| M55 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=1` | 3.11.18: ERRORTOKEN `℘` at (1,0). |
| M56 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=5` | 3.11.18: lexeme `a℘` at byte column 5. |
| M57 | DET | ACCEPT / — / — / `—` | Non-ASCII appears only in STRING and COMMENT tokens. |
| M58 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | `required_action` is declared (L176); scope is the affected design in both arms. |
| M59 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper.nested_async\|reason=ASYNC_DEFINITION` | Static AST model: rank 6. |
| M60 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=WRONG_ENTRY_POINT_KIND` | **New.** The required pass rejects it before the rank-6 nested async in `helper`. |
| M61 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.step\|reason=WRONG_ENTRY_POINT_KIND` | **New.** Static AST model: matches. The source has a 5-space `async def step` with a trailing space, which is export padding; the outcome is unaffected (C1). |
| M62 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=1` | **New.** 3.11.18: the `x·y` lexeme starts at `x`. |
| M63 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=5` | **New.** 3.11.18 emits a spurious ERRORTOKEN for the space, then `℘f` starts at byte column 5. The body is indented 5 spaces, which is export padding; the outcome is unaffected (C1). |
| M64 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=15` | **New.** 3.11.18: byte column 15 (character column 14). The line ends with a trailing space, which is export padding; the outcome is unaffected (C1). |

## Hashes, assembly and package integrity

All values are recomputed \[H\] by audit scripts, not by the project assembler.

| Object | Bytes | SHA-256 (recomputed) | Record | Result |
| --- | --- | --- | --- | --- |
| Response schema (34) | 2,529 | `6fb5d282b09540949f21ee134b522841c3345031cb3e118a83bdffc18b4e7c34` | Sidecar | PASS |
| System message (25) | 602 | `98020d4f9cf818968f15e4a7c0a5adc3633694aa98c5cbfe170b0904aee3c7a4` | Sidecar | PASS |
| Repair message (25) | 621 | `f11d574f4e5afb223a096b74f039ecb6a222d6ed6dc5bcf7f115dc5922c2620d` | Sidecar | PASS |
| ORG-A template stage, v1.3.2 | 13,377 | `960b6cc9877f731e46f4c53aa755e4974bcae567ae0451bda833344876c7db7d` | Sidecar | PASS |
| ORG-B template stage, v1.3.2 | 13,377 | `ec5d391f3c2fe8c9ed91e857dc0e5d3b18e1e8db9050aae4d66561d53edc432f` | Sidecar | PASS |
| Superseded v1.3.1 ORG-A / ORG-B | 13,481 | `b63be015…e7af` / `cdfcc0ac…49d8` | Equal to the archived v1.3.1 sidecar | PASS |
| Superseded v1.1, v1.2, v1.3 | 12,004 / 12,187 / 12,957 | All 64 hex characters | Carried unchanged from the v1.3.1 sidecar | PASS |

**Assembly \[H\]:**

- **Rule.** I used the token-only schema-insertion rule: strip 3 metadata lines plus 1 blank line; render each block as heading, LF, then the trimmed body; join blocks with two LFs; end with one terminal LF.
- **Result.** This reproduces both 13,377-byte values. The 104-byte drop from v1.3.1 matches the shorter B5/B7 async sentences.
- **Block order.** ORG-B is B0, B2, B5, B1, B6, B3, B7, B4, B8, which matches the sidecar's `arm_orders`. The two arms contain an identical multiset of rendered blocks, so they differ only by block order.
- **Fixed texts.** The fixed texts in file 30 §3.1 (B5 3,246 B, B7 2,658 B, B8 3,310 B) are exact byte prefixes of the corresponding block bodies in both arms. Each is followed by exactly `\n\n`, then `Design-specific API and top-level port`, `Design-specific checker obligations` and `BEGIN_OPENVEF_RESPONSE_SCHEMA_JSON` respectively.
- **Schema substitution.** The substituted schema equals `json.dumps(indent=2)` plus LF, followed by the template LF.

**Package \[H\]:**

- `unzip -t` is clean.
- `27_SHA256SUMS.txt` lists 239 entries and every one verifies. Only the manifest itself is excluded, which file 51 L18 documents. The ZIP holds 240 files.
- `archive_v1.3.1/OpenVEF_Planning_v1.3.1.zip` is byte-identical to the released v1.3.1 ZIP.
- `archive_v1.3/OpenVEF_Planning_v1.3.zip` is byte-identical to the released v1.3 ZIP.
- `archive_v1.2/OpenVEF_Planning_v1.2.zip` is unchanged.

**Python runtime \[P311\], CPython 3.11.18, not the pinned patch:**

- **Fixture sources.** All five sources M60–M64 pass `ast.parse` and `compile()`, and the identifier columns match.
- **N12 evidence.** In a synchronous function:
  - `return (x async for x in y)` passes both `ast.parse` and `compile()`.
  - `[x async for x in y]`, `await y`, `async for` and `async with` pass `ast.parse` but fail `compile()` with `SyntaxError` on line 2.
- **Pinned interpreter.** File 50 stays NOT RUN until the pinned patch is frozen.

## Findings, exact edits and owner status

### Blocker

| ID | Finding | Locations | Evidence |
| --- | --- | --- | --- |
| N12 | **An async generator expression inside a synchronous function is forbidden but never rejected.** The text says “async generators are covered by their `AsyncFunctionDef`”, which is false for a generator expression: `(x async for x in y)` contains no `AsyncFunctionDef`. It passes `ast.parse` and `compile()`, no AST\_SIGNATURE category matches it, and no fixture covers it. A conforming parser would accept it, while a parser that follows the prose would reject it with an invented diagnostic. That is the same kind of implementation-divergence risk as v1.3 N3. **Related gap:** `await`, `async for`, `async with` and async list, set or dict comprehensions in a synchronous function reach `COMPILE_DRIVER` or `COMPILE_CHECKER` as `COMPILE_ERROR`. Nothing documents that, so the pack splits async rejection across two stages without saying so. | File 30 L29; model-visible “Do not define async functions, async generators or async comprehensions” in ORG-A L25/L40, ORG-B L16/L37 and file 30 L52/L64; Protocol L135 and L164; file 25 copy | \[S\]\[P311\] |

This also corrects my v1.3 edit list, which said those constructs “are already `SyntaxError` on 3.11 and need no rule”.

### Cleanup items (non-blocking)

| ID | Finding | Locations |
| --- | --- | --- |
| C1 | **Markdown-export padding in M61, M63 and M64, and a misdiagnosis in file 52.** The exporter writes an inline code span that starts or ends with a space with one extra pad space on each side; this is the CommonMark convention, and a renderer strips the padding again. The raw export bytes therefore showed 5 leading spaces and a trailing space. The audit text rendered with 4 spaces and was arithmetically consistent. File 52 calls this an arithmetic contradiction and normalizes M64's indentation only. M61 still has `     async def step(…): ` (5 leading spaces plus a trailing space), M63 has a 5-space `      return None `, and M64 keeps a trailing space. All three outcomes are unaffected, as recomputed. | `41_F18_Fixture_Inputs/M61.json`, `M63.json`, `M64.json`; file 52 L14 and L22; change log 03 L19 (“exact source snippets”) |
| C2 | No fixture for async `check_trace`. Expected outcome under the current rule: `ENTRY_POINT_REJECT\|file=checker.py\|symbol=check_trace\|reason=WRONG_ENTRY_POINT_KIND`. | Catalog 36; index |
| C3 | No fixture for the rank-3 and rank-5 async branches. Expected outcomes: an async `Driver.extra` gives `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.extra\|reason=FORBIDDEN_METHOD`, and a decorated module-level `async def h` gives `DECORATOR_REJECT\|file=driver.py\|symbol=h`. | Catalog 36; index |

### Exact edits (proposed only; the pack was not modified)

1. **P0 – N12.** I recommend rejecting every async construct at one stage.
   - **Rank 6.** In Protocol L164, its file 25 copy and file 30 L33, change rank (6) to: “any `ast.AsyncFunctionDef`, `ast.Await`, `ast.AsyncFor`, `ast.AsyncWith`, or `ast.comprehension` with `is_async=1`, at any lexical depth → `ASYNC_DEFINITION`”.
   - **Symbol.** For a non-definition node, the symbol is the dotted name of the innermost enclosing definition. The global key uses the node's own position.
   - **Async sentence.** In Protocol L135, file 25 and file 30 L29, add “and every `await`, `async for`, `async with` and async comprehension or generator expression” to the async sentence.
   - **Generator wording.** Replace “async generators are covered by their `AsyncFunctionDef`” with “async generator functions are covered by their `AsyncFunctionDef`; async generator expressions are covered by the async-comprehension rule”.
   - **No prompt-hash change.** B5/B7 already forbid these constructs and promise only rejection at `AST_SIGNATURE`, so the model-visible text, and therefore the prompt hashes, need not change.
   - **Fixtures.** Add the two fixtures in the code block below.
   - **Alternative.** Keep the compile-stage outcome for the `SyntaxError` constructs and document it, then add rank-6 coverage for async generator expressions alone.
2. **P1 – C1.** Remove the export padding from M61, M63 and M64:
   - M61: 4-space `async def step(self, cycle_index, outputs_after_edge):`, with no trailing space.
   - M63: body `     return None `, 4 spaces.
   - M64: no trailing space.

   The expected outcomes stay the same. Then recompute the fixture hashes, the index and the manifest, and correct file 52 L14 and L22 and change log L19.
3. **P2 – C2/C3.** Add the three async fixtures, using the expected outcomes in the cleanup table and the M59-style base sources.
4. **Housekeeping.** Update the counts, catalog, file 51/52/53, change log, README and SHA-256 manifest. Archive v1.3.2 byte-for-byte.

Take fixture sources from the fenced block below rather than from inline code, so that no export padding gets in. Each value is a JSON string. The values were recomputed on \[P311\] 3.11.18.

```json
{
  "M65_async_genexp": {
    "driver": "import random\n\ndef helper(items):\n    return (x async for x in items)\n\ndef create_driver(seed):\n    driver = Driver()\n    driver.rng = random.Random(seed)\n    return driver\n\nclass Driver:\n    def step(self, cycle_index, outputs_after_edge):\n        return \"COMPLETE\"\n",
    "checker": "def check_trace(trace, metadata):\n    return {\"verdict\": \"PASS\", \"diagnostics\": []}\n",
    "python_3_11_18": "ast.parse OK; compile OK",
    "expected_if_edit_1": "REPAIR / AST_SIGNATURE / ENTRY_POINT_REJECT / ENTRY_POINT_REJECT|file=driver.py|symbol=helper|reason=ASYNC_DEFINITION"
  },
  "M66_await_in_sync": {
    "driver": "same as M65 with line 4 replaced by '    await items'",
    "python_3_11_18": "ast.parse OK; compile SyntaxError line 4",
    "expected_if_edit_1": "REPAIR / AST_SIGNATURE / ENTRY_POINT_REJECT / ENTRY_POINT_REJECT|file=driver.py|symbol=helper|reason=ASYNC_DEFINITION",
    "expected_if_alternative": "REPAIR / COMPILE_DRIVER / COMPILE_ERROR / COMPILE_ERROR|file=driver.py|line=4"
  }
}
```

### Owner and authorization status

This state is reproduced exactly from README L46, file 32 L30–L33, register 16 L93 and L108, and approval record 23 L4, L21–L28, L34, L38 and L42:

- A1–A11: **NOT ACCEPTED** (proposed; owner acceptance `PENDING`).
- X14: **OWNER CHOICE REQUIRED**.
- Owner, TEEP applicant, contributors and approver: **TO CONFIRM**.
- Signature and date: **NOT RECORDED**.
- Authorization: **NONE**.

No identity or approval is inferred.

The required order is unchanged:

1. Independent document audit. This audit is a FAIL on N12.
2. The owner records A1–A11 and the X14 choice.
3. Implementation, with all mandatory fixtures run on the pinned CPython 3.11.
4. Independent audit of the implementation.
5. Only then, consideration of the LLM-call gate.

A document PASS would satisfy step 1 only.

**Evidence boundaries:**

- **\[S\] and \[H\]:** all document, vocabulary, fixture-descriptor, hash, assembly, archive and manifest results.
- **\[P311\], CPython 3.11.18, not the pinned patch:** parse and compile results, async constructs and identifier columns. Python 3.11 compatibility is **not marked PASS**.
- **Audit-only models:** the AST and identifier models are audit scripts, not the project parser.
- **\[I\], none:** no parser, assembler, harness, simulator or F1–F18 was implemented or run.
- **Not done:** no LLM or provider call, no F16, no format probe, and no source PDF or literature verification. Every source in scope was inspectable.
