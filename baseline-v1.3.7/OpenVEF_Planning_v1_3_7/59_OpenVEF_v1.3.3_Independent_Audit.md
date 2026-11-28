# OpenVEF v1.3.3 Audit

Nov 23, 2026

## Verdict

**Document audit: FAIL (one narrow blocker, N13).**

v1.3.3 fixes the exact N12 spelling. `(item async for item in stream)` is now rejected at rank 7, and the rule reproduces in Protocol §3.4, file 25 and file 30. All 143 descriptors are consistent and deterministic. Hashes, archives and the manifest verify, and no model-visible bytes changed.

**N13: the rank-7 rule only partly closes N12.** The rule defines an asynchronous comprehension as one with `comprehension.is_async == 1`. Python also makes a generator expression asynchronous when it contains `await`:

- `(await item for item in stream)` inside a synchronous function is an async generator expression.
- On CPython 3.11.18 it passes both `ast.parse` and `compile()`, and every `is_async` flag on it is 0.
- So the current rank-7 rule never matches it, and nothing else does either.

File 30 L29 says async generator expressions “are covered by the `ASYNC_COMPREHENSION` rank-7 rule”. For the `await` form, that claim is false. The fix is one clause in Protocol L135/L164, file 25 and file 30, plus one fixture.

There are five non-blocking cleanup items (C1–C5, in the last section).

**LLM-call gate: NOT MET.** Nothing is authorized, and a document PASS would not change that:

- A1–A11: NOT ACCEPTED.
- X14: OWNER CHOICE REQUIRED.
- Identities: TO CONFIRM.
- Authorization: NONE.
- No implementation exists. All 143 fixtures are NOT RUN. The pinned CPython 3.11 patch is TO FREEZE.

**Evidence classes:**

- **\[S\]** document reading.
- **\[H\]** static audit scripts: SHA-256, assembly reproduction, vocabulary cross-checks, and audit-only reimplementations of the L164 required-symbol pass with ranks 1–7 and of the L133 identifier rule.
- **\[P311\]** `/usr/bin/python3.11 -I`, which is CPython 3.11.18. It is not the pinned patch.
- **\[I\]** project implementation execution. None exists, and none was performed.

No parser, assembler, F18, harness or simulator was run. No LLM or provider call was made, and no source PDF was opened.

## Scope items 1–12

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Active root and archives; v1.3.2 archive | **PASS.** The active root is `OpenVEF_Planning_v1_3_3/`. `archive_v1.3.2/OpenVEF_Planning_v1.3.2.zip` is byte-identical to the released v1.3.2 ZIP. The v1.3.2 release documents (03, 48, 51, 52, 53) are kept in `archive_v1.3.2/release_documents/`. | \[H\] |
| 2 | Reproduce N12 | **REPRODUCED.** In a synchronous function, `(item async for item in stream)` is an `ast.GeneratorExp` with `is_async == 1`, not an `AsyncFunctionDef`. It passes `ast.parse` and `compile()` on \[P311\]. **A second spelling, `(await item for item in stream)`, does the same with `is_async == 0` (N13).** | \[P311\] |
| 3 | Rank-7 rule across Protocol, file 25 and file 30 | **PASS as written.** Protocol L135 and L164, the file 25 copy and file 30 L29/L33 agree: any `GeneratorExp`, `ListComp`, `SetComp` or `DictComp` with any `is_async == 1` gives `ENTRY_POINT_REJECT … ASYNC_COMPREHENSION` at rank 7. `ASYNC_COMPREHENSION` is added to the reason domain (L125). The rule's scope is incomplete (N13). | \[S\]\[H\] |
| 4 | Sort key, precedence, symbol | **PASS.** The key is still `(category, file_order, lineno, col_offset, end_lineno, end_col_offset)`. Required symbols run first, and rank 7 sorts after ranks 1–6 because category is the first key element. The expression's own position is used, and its symbol is the dot-joined enclosing definition names. M60, M61, M67, M68 and M69 confirm rank 7 never outranks those. The symbol for a header expression is ambiguous (C2). | \[S\]\[H\] |
| 5 | M65/M66 | **PASS.** The async genexp is in driver.py `helper` (M65) and in checker.py `check_trace` (M66). Bytes, SHA-256, length, expected object and catalog row match. The rank-7 static model reproduces both symbols. | \[H\]\[P311\] |
| 6 | M67/M68/M69 | **PASS.** M67 → `WRONG_ENTRY_POINT_KIND` for `check_trace`. M68 → `FORBIDDEN_METHOD`, `Driver.extra` (rank 3). M69 → `DECORATOR_REJECT`, `helper` (rank 5). All reproduced. | \[H\]\[P311\] |
| 7 | M61/M63/M64 normalization | **PASS on outcomes.** The expected objects are byte-for-byte unchanged from v1.3.2. M61 L14 now has 4 spaces and no trailing space. M64 line 2 is `     s = "é"; a℘ = 1 `: character column 14 and UTF-8 byte column 15, recomputed from the bytes. **M63 has a collateral mutation:** line 7 (`return None` inside `nested_async`) went from 8 to 7 spaces (C1). It still parses, and line 1 rejects first. | \[H\]\[P311\] |
| 8 | 143 fixtures (59 P, 13 R, 71 M) | **PASS.** Index, files and catalog each list 143 unique ids, and hashes, lengths, ids and expected objects match. Every disposition, stage, error class, diagnostic code, reason and `required_action` traces to Protocol, file 25 or file 30. The index says `NOT RUN / NOT PASSED`. This is a descriptor check only; nothing was executed. | \[H\] |
| 9 | Protocol §3.4 against file 25 | **PASS.** They are byte-identical: 98 lines and 37,403 bytes, Protocol L89–L188 against file 25 from L33. | \[H\] |
| 10 | Prompt hashes | **PASS.** Files 19, 20 and 34 and the system and repair portion of file 25 are byte-identical to v1.3.2. ORG-A and ORG-B recompute to the carried-forward 13,377-byte values. The status is `TEMPLATE_STAGE_ONLY_DESIGN_PAYLOADS_UNRESOLVED`. | \[H\] |
| 11 | Archives and manifest | **PASS.** The v1.3.2, v1.3.1, v1.3 and v1.2 archive ZIPs are byte-identical to their releases. `27_SHA256SUMS.txt` lists 251 entries, all OK. Only the manifest itself is excluded, as file 57 documents. The ZIP holds 252 files. | \[H\] |
| 12 | Version labels and cross-references | **PASS.** Every current title and `Version:` line reads v1.3.3, and every file reference resolves. Protocol L555 says 143 fixtures; L559 records the v1.3.2 N12 FAIL and says no model-visible bytes changed. No stale `138`, `six category` or doubled labels remain. **Correction to my v1.3.2 audit:** Protocol L4 still read “Version: 1.3” in v1.3.2 and I marked labels PASS. That line is now correct. Register 16 lacks a v1.3.3 section (C4). | \[S\]\[H\] |

## Fixture table: all 143 descriptors

**Summary:** all 143 descriptors are deterministic, and none is ambiguous or contradictory. That covers only the expected outcomes the fixtures already state. The N13 case has no fixture.

Status describes the **expected outcome only**. No fixture was executed by a project runner.

**\[H\] checks:**

- Index, file and catalog equality; SHA-256, byte length and expected object for every fixture.
- Vocabulary traceability: zero undeclared values.
- The static AST model now includes rank 7. It reproduces M01, M02, M03, M38, M39, M49, M51, M52, M59, M60, M61, M65, M66, M67, M68, M69, P16 and P27. It does not model parameters, so it is silent on P15 and P26.
- The identifier model reproduces M35, M43–M46, M55–M57 and M62–M64 on \[P311\].

Rows without a note are byte-identical to v1.3.2 and re-check as deterministic.

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
| M14 | DET | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / TRUNCATION / `contains_marker=True; output_diagnostic_bytes=2047` |  |
| M15 | DET | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / FEEDBACK\_SERIALIZER\_REJECT / `FEEDBACK_SERIALIZER_REJECT\|reason=NON_NORMATIVE_DIAGNOSTIC` |  |
| M16 | DET | REPAIR / SOURCE\_AST / SOURCE\_EMPTY / `SOURCE_EMPTY\|file=driver.py` |  |
| M17 | DET | CONTROL\_EXPECTATION / FEEDBACK\_SERIALIZER / JSON\_SERIALIZATION / `diagnostic_sha256=226a87deb777b94556d262a0e45e669ced8c80f5cf8ec1bc3d691e9d4570423f` |  |
| M18 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `PACKET_FREEZE_REJECT\|reason=RESERVED_HEADING_LINE` |  |
| M19 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `ASSEMBLY_REJECT\|reason=UNRESOLVED_PLACEHOLDER` |  |
| M20 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `F18_REJECT\|reason=VISIBLE_CLAUSE_ID_SET_MISMATCH` |  |
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
| M40 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `F18_REJECT\|reason=MALFORMED_CLAUSE_ID_TOKEN` |  |
| M41 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / MID\_RUN\_REEVALUATION / `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` | Diagnostic and error class are declared at L175. |
| M42 | DET | DESIGN\_ABORTED\_NO\_SLOTS\_SCORED / DESIGN\_HALT / DESIGN\_HALT\_REPEATED / `DESIGN_HALT_REPEATED\|reason=EVALUATOR_FAILURE_REPRODUCED` |  |
| M43 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=19` | Byte column 19 (character column would be 18). |
| M44 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=8` | 3.11.18: column 8. |
| M45 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=17` | 3.11.18: column 17. |
| M46 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=1\|column=5` | 3.11.18: column 5. |
| M47 | DET | DESIGN\_ABORTED\_NO\_SLOTS\_SCORED / DESIGN\_HALT / DESIGN\_HALT\_REPEATED / `DESIGN_HALT_REPEATED\|reason=SECOND_HALT_AFTER_RECOVERY` |  |
| M48 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / EVALUATOR\_REVISION\_REQUIRED / `EVALUATOR_REVISION_REQUIRED\|reason=FROZEN_EVALUATOR_CHANGED` |  |
| M49 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=MISSING_ENTRY_POINT` | Static AST model: required symbols are checked before categories. |
| M50 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` |  |
| M51 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=nested_holder.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: rank 1 beats rank 5. |
| M52 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=nested_holder.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: global pass across files. |
| M53 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` |  |
| M54 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / HALT\_SIGNATURE\_SCHEMA / `HALT_SIGNATURE_SCHEMA\|reason=COMPONENT_VALUES_ENUMERATED` |  |
| M55 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=1` | 3.11.18: ERRORTOKEN `℘` at (1,0). |
| M56 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=5` | 3.11.18: lexeme `a℘` at byte column 5. |
| M57 | DET | ACCEPT / — / — / `—` | Non-ASCII appears only in STRING and COMMENT tokens. |
| M58 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / AUTHORING\_REVISION\_REQUIRED / `AUTHORING_REVISION_REQUIRED\|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` |  |
| M59 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper.nested_async\|reason=ASYNC_DEFINITION` | Static AST model: rank 6. |
| M60 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=WRONG_ENTRY_POINT_KIND` | Static AST model: the required pass runs before rank 6. |
| M61 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.step\|reason=WRONG_ENTRY_POINT_KIND` | **Normalized:** 4-space `async def step`, no trailing space. Expected outcome unchanged; model matches. |
| M62 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=1` | 3.11.18: byte column 1. |
| M63 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=5` | **Normalized:** line 2 now has 4 spaces. **Collateral change:** line 7 (the `nested_async` body) went from 8 to 7 spaces (C1). It still parses, and column 5 on 3.11.18 is unchanged. |
| M64 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=15` | **Normalized:** trailing space removed. Recomputed from the bytes: character column 14, byte column 15. |
| M65 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper\|reason=ASYNC_COMPREHENSION` | **New.** Rank-7 model: the async genexp in `helper` gives symbol `helper`. |
| M66 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=check_trace\|reason=ASYNC_COMPREHENSION` | **New.** Rank-7 model: the async genexp in `check_trace` gives symbol `check_trace`. |
| M67 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=check_trace\|reason=WRONG_ENTRY_POINT_KIND` | **New.** The required pass applies. |
| M68 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.extra\|reason=FORBIDDEN_METHOD` | **New.** Rank 3 beats rank 6. |
| M69 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `DECORATOR_REJECT\|file=driver.py\|symbol=helper` | **New.** Rank 5 beats rank 6. |

## Hashes, assembly and package integrity

All values below are recomputed \[H\] by audit scripts, not by the project assembler.

| Object | Bytes | SHA-256 (recomputed) | Record | Result |
| --- | --- | --- | --- | --- |
| Response schema (34) | 2,529 | `6fb5d282b09540949f21ee134b522841c3345031cb3e118a83bdffc18b4e7c34` | Sidecar; byte-identical to v1.3.2 | PASS |
| System message (25) | 602 | `98020d4f9cf818968f15e4a7c0a5adc3633694aa98c5cbfe170b0904aee3c7a4` | Sidecar | PASS |
| Repair message (25) | 621 | `f11d574f4e5afb223a096b74f039ecb6a222d6ed6dc5bcf7f115dc5922c2620d` | Sidecar | PASS |
| ORG-A template stage | 13,377 | `960b6cc9877f731e46f4c53aa755e4974bcae567ae0451bda833344876c7db7d` | Sidecar; same as v1.3.2 | PASS |
| ORG-B template stage | 13,377 | `ec5d391f3c2fe8c9ed91e857dc0e5d3b18e1e8db9050aae4d66561d53edc432f` | Sidecar; same as v1.3.2 | PASS |
| Superseded v1.1, v1.2, v1.3 and v1.3.1 | 12,004 / 12,187 / 12,957 / 13,481 | 64-hex values | Identical to the v1.3.2 sidecar's superseded block | PASS |

**No model-visible bytes changed \[H\]:**

- Files 19, 20 and 34 are byte-identical to v1.3.2.
- File 25 lines 1–32 (the system and repair messages) are byte-identical.
- File 25 changed only inside the assembler-only §3.4 control copy, which is not model-visible.
- The sidecar's `hash_status_note` says the hashes were carried forward. The final prompts remain `TEMPLATE_STAGE_ONLY_DESIGN_PAYLOADS_UNRESOLVED` until all seven design payloads are frozen.

**Assembly \[H\]:**

- The token-only schema-insertion rule reproduces both 13,377-byte values.
- The two arms differ only by block order (B0, B2, B5, B1, B6, B3, B7, B4, B8 for ORG-B).
- The fixed texts in file 30 §3.1 are exact byte prefixes of the corresponding block bodies in both arms: B5 3,246 B, B7 2,658 B, B8 3,310 B. Each is followed by exactly `\n\n`.
- The substituted schema equals `json.dumps(indent=2)` plus LF.

**Package \[H\]:**

- `unzip -t` is clean.
- `27_SHA256SUMS.txt` lists 251 entries and every one verifies. Only the manifest itself is excluded, and file 57 states the exclusion.
- The ZIP holds 252 files.

**Archives \[H\]:** each archived ZIP is byte-identical to its released ZIP.

- `archive_v1.3.2/OpenVEF_Planning_v1.3.2.zip`
- `archive_v1.3.1/OpenVEF_Planning_v1.3.1.zip`
- `archive_v1.3/OpenVEF_Planning_v1.3.zip`
- `archive_v1.2/OpenVEF_Planning_v1.2.zip`

**Earlier audit artifacts:** File 55 is an *owner-supplied summary* of my v1.3.2 audit. It says it is not a byte-for-byte export. I could inspect my own v1.3.2 audit doc, but the pack does not contain it. My v1.3.2 edit list had proposed covering `ast.Await` in the async rule. The summary does not carry that detail, and that is the gap N13 now reports (see C5).

**Python runtime \[P311\], CPython 3.11.18, not the pinned patch:**

| Snippet, inside a synchronous function | `is_async` flags | `compile()` |
| --- | --- | --- |
| `(item async for item in stream)` | \[1\] | OK, rejected by rank 7 |
| `(await x for x in y)` | \[0\] | **OK, not rejected (N13)** |
| `(x for x in y if await x)` | \[0\] | **OK, not rejected (N13)** |
| `(x for z in y for x in await z)` | \[0, 0\] | **OK, not rejected (N13)** |
| `lambda: (await x for x in y)` | \[0\] | **OK, not rejected (N13)** |
| `[await x for x in y]` and set/dict forms | \[0\] | SyntaxError, so `COMPILE_ERROR` (C3) |
| `(x for x in await y)` | \[0\] | SyntaxError (`await` outside async), so `COMPILE_ERROR` (C3) |
| `def helper(a=(x async for x in [])):` | \[1\] | OK; rank 7 matches, but the symbol is ambiguous (C2) |

File 50 stays NOT RUN until the pinned patch is frozen.

## Findings, exact edits and owner status

### Blocker

| ID | Finding | Locations | Evidence |
| --- | --- | --- | --- |
| N13 | **A generator expression that contains `await` is an async generator expression, but rank 7 does not catch it.** Python's language reference defines an asynchronous generator expression as one containing either `async for` or `await`. The rank-7 test checks only `comprehension.is_async == 1`. As a result, `(await item for item in stream)` inside a synchronous function is accepted: it passes `ast.parse` and `compile()` on \[P311\], all of its `is_async` flags are 0, and no other rule matches. The same applies when `await` sits in a filter, in a later `for` clause, or inside a lambda. File 30 L29 says async generator expressions “are covered by the `ASYNC_COMPREHENSION` rank-7 rule”, which is false for this form. B5/B7 forbid async generators to the model, so a conforming parser would accept what the prompt forbids. This is the residue of N12. | Protocol L135 and L164; file 25 copy; file 30 L29 and L33 | \[S\]\[P311\]\[H\] |

### Cleanup items (non-blocking)

| ID | Finding | Locations |
| --- | --- | --- |
| C1 | **Collateral normalization in M63.** Line 7 (`return None` inside `nested_async`) went from 8 spaces to 7, apparently because the 5-space→4-space replacement also matched inside an 8-space run. It still parses and the outcome is unaffected, but the fixture now differs from its M59-style base for no reason. | `41_F18_Fixture_Inputs/M63.json` driver line 7 |
| C2 | **Ambiguous symbol for async comprehensions in definition headers.** `def helper(a=(x async for x in [])):` compiles on \[P311\]. Rank 7 matches it, but the rule's `<module>` clause invites a Python-scope reading, under which defaults, annotations and class bases are evaluated in the enclosing scope and the symbol is `<module>`. An AST-ancestry reading gives `helper`. Both readings reject at the same stage with the same reason; only the `symbol` field can differ. | Protocol L135 and L164; file 30 L33 |
| C3 | **Compile-stage async outcomes are still undocumented.** In a synchronous function, `await`, `async for` and `async with` outside a comprehension, plus `await` inside a list, set or dict comprehension or in the first iterator, pass `ast.parse` and fail only at `compile()`, giving `COMPILE_ERROR`. The outcome is deterministic, but no text says so. This is the “related gap” from my v1.3.2 audit. | Protocol L135; file 30 L29 |
| C4 | **Register 16 has no v1.3.3 entry.** Its latest section is “v1.3.2 corrective document changes”, while approval record 23 L68 records the v1.3.3 corrections. | `16_OpenVEF_v1.3.3_Owner_Decision_Register.md` L111–L113 |
| C5 | **The v1.3.2 audit itself is not in the pack.** File 55 is a summary, and the summary omitted my recommendation to include `ast.Await`, which is how N13 got through. Include the actual audit export. The doc's own Export → Markdown keeps fenced code blocks unpadded. | File 55; README controlling-file list |

### Exact edits (proposed only; the pack was not modified)

1. **P0 – N13.**
   - **Rank-7 definition.** In Protocol L135 and L164, the file 25 copy and file 30 L29/L33, change it to: “any `ast.GeneratorExp`, `ast.ListComp`, `ast.SetComp` or `ast.DictComp` that has at least one associated `ast.comprehension` with `is_async == 1` **or that contains an `ast.Await` node anywhere in its subtree**”.
   - **Rationale sentence.** Add: “Python treats a generator expression containing `await` as an asynchronous generator expression even when every `is_async` flag is 0.”
   - **Side effects.** Under this rule, `await` inside a list, set or dict comprehension, or in a first iterator, also moves from `COMPILE_ERROR` to rank 7. That makes one stage own all async comprehensions.
   - **Fixture.** Add M70 from the code block below.
   - **Prompt hashes.** No model-visible bytes change, so the prompt hashes carry forward.
2. **P1 – C2.** In the same places, define the symbol by AST ancestry: “the dot-joined names of the definition nodes of which the expression is a descendant, including expressions in its arguments, defaults, annotations, bases and keywords”. State that `<module>` is unreachable after `IMPORT_POLICY`, or delete the `<module>` clause.
3. **P1 – C3.** Add to Protocol L135 and file 30 L29: “`await`, `async for` and `async with` statements inside a synchronous function body pass `AST_SIGNATURE` and are rejected by Python `compile()` as `COMPILE_ERROR|file=<FILE>|line=<LINE>` at `COMPILE_DRIVER`/`COMPILE_CHECKER`.” Optionally add one fixture, such as `await stream` inside `helper` → `COMPILE_ERROR|file=driver.py|line=4`.
4. **P2 – C1.** Restore M63 driver line 7 to 8 spaces (`         return None `). The expected outcome is unchanged. Recompute the M63 hash, index and manifest.
5. **P2 – C4 and C5.** Add a v1.3.3 section to register 16. Include the actual v1.3.2 audit export next to file 55.
6. **Housekeeping.** Update the count (144 with M70), catalog, change log, files 56–58, README and SHA-256 manifest. Archive v1.3.3 byte-for-byte.

Take the source from this fenced block so that no export padding gets in. Each value is a JSON string, verified on \[P311\] 3.11.18. The expected outcome was computed with the audit model extended per edit 1.

```json
{
  "M70_await_genexp": {
    "driver": "import random\n\ndef helper(stream):\n    return (await item for item in stream)\n\ndef create_driver(seed):\n    driver = Driver()\n    driver.rng = random.Random(seed)\n    return driver\n\nclass Driver:\n    def step(self, cycle_index, outputs_after_edge):\n        return \"COMPLETE\"\n",
    "checker": "def check_trace(trace, metadata):\n    return {\"verdict\": \"PASS\", \"diagnostics\": []}\n",
    "python_3_11_18": "ast.parse OK; compile OK; all comprehension.is_async == 0",
    "expected_after_edit_1": "REPAIR / AST_SIGNATURE / ENTRY_POINT_REJECT / ENTRY_POINT_REJECT|file=driver.py|symbol=helper|reason=ASYNC_COMPREHENSION",
    "current_v1_3_3_behaviour": "no AST_SIGNATURE match; compiles; accepted"
  }
}
```

With the extended rule, the audit model still reproduces M59–M61 and M65–M69 unchanged.

### Owner and authorization status

This state is reproduced exactly from README L45, file 32 L30–L34, register 16 L93 and L108, and approval record 23 L4 and L21:

- A1–A11: **NOT ACCEPTED** (proposed; owner acceptance `PENDING`).
- X14: **OWNER CHOICE REQUIRED**.
- Owner, TEEP applicant, contributors and approver: **TO CONFIRM**.
- Signature and date: **NOT RECORDED**.
- Authorization: **NONE**.

No identity or approval is inferred.

The required order is unchanged:

1. Independent document audit. This audit is a FAIL on N13.
2. The owner records A1–A11 and the X14 choice.
3. Implementation, with all mandatory fixtures run on the pinned CPython 3.11.
4. Independent implementation audit.
5. Only then, consideration of the LLM-call gate.

A document PASS would satisfy step 1 only.

**Evidence boundaries:**

- **\[S\] and \[H\]:** all document, vocabulary, fixture-descriptor, hash, assembly, archive and manifest results.
- **\[P311\], CPython 3.11.18, not the pinned patch:** parse and compile results, `is_async` flags and identifier columns. The build environment's lack of the pinned interpreter is noted; Python 3.11 compatibility is **not marked PASS**.
- **Audit-only models:** the AST (ranks 1–7) and identifier models are audit scripts, not the project parser.
- **\[I\], none:** no parser, assembler, harness, simulator or F1–F18 was implemented or run.
- **Not done:** no LLM or provider call, no F16, no format probe, and no source PDF or literature verification.
