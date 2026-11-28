# OpenVEF v1.3.4 Audit

Nov 23, 2026

## Verdict

**Document audit: FAIL (one narrow blocker, N14).**

The N13 fix itself is correct and complete. In Protocol §3.4, its file 25 copy, file 30 and the Catalog, rank 7 now covers `is_async == 1` **or** any `ast.Await` in the comprehension subtree. That catches every placement I tried on \[P311\]: element, filter, later `for` clause, first iterator, nested lambda, the list, set and dict forms, and header defaults.

The other fixes also hold:

- Ancestry-based symbol naming.
- The compile-stage policy for standalone async constructs.
- M70, which is byte-identical to the JSON in my v1.3.3 audit.
- M63, restored to 8 spaces.
- All 144 descriptors, the hashes, the archives and the manifest.

**N14: the F18 checklist (file 21) was not updated.** It is the document that tells F18 what to run and verify, and it still describes v1.3.3:

- **Fixture count.** It says “All 143 fixtures” and “71 M” (L38, L45).
- **Mandatory range.** It lists M01–M69 (L44), so it excludes M70.
- **Rank-7 rule.** Its verification bullet still states the rule as `is_async == 1` only (L57).
- **Async precedence row.** L34 omits M70.

An F18 run that followed file 21 would skip the one fixture that tests N13, and would check the superseded rule. This differs from the stale counts I treated as non-blocking in v1.3.1 (N11). Those sat in prose; here the stale text is the operative checklist for the very rule being fixed.

There are seven non-blocking cleanup items (C1–C7), mostly stale version labels.

C7 is the missing v1.3.2 audit export. **I can supply that file. It is attached to this reply.**

**LLM-call gate: NOT MET.** Nothing is authorized, and a document PASS would not change that:

- A1–A11: NOT ACCEPTED.
- X14: OWNER CHOICE REQUIRED.
- Identities: TO CONFIRM.
- Signature and date: NOT RECORDED.
- Authorization: NONE.
- No implementation exists, all 144 fixtures are NOT RUN, and the pinned CPython 3.11 patch is TO FREEZE.

**Evidence classes:**

- **\[S\]** document reading.
- **\[H\]** static audit scripts: SHA-256, assembly reproduction, vocabulary cross-checks, and audit-only models of the L164 AST pass (ranks 1–7, including the `Await` subtree test) and the L133 identifier rule.
- **\[P311\]** `/usr/bin/python3.11 -I`, which is CPython 3.11.18. It is not the pinned patch.
- **\[I\]** project implementation execution. None exists, and none was performed.

No parser, assembler, F18, harness or simulator was run. No LLM or provider call was made, and no source PDF was opened.

## Scope items 1–14

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Active root, controlling files, archives | **PASS.** The active root is `OpenVEF_Planning_v1_3_4/`. `archive_v1.3.3/OpenVEF_Planning_v1.3.3.zip` is byte-identical to the released v1.3.3 ZIP. The v1.3.2, v1.3.1, v1.3 and v1.2 archive ZIPs are also byte-identical to their releases. | \[H\] |
| 2 | Reproduce N13 | **REPRODUCED.** In a synchronous function, `(await item for item in stream)` passes `ast.parse` and `compile()`. Its comprehension has `is_async == 0`. | \[P311\] |
| 3 | Rank-7 definition | **PASS.** Protocol L135 and L164, the file 25 copy, file 30 L29 and L33, and Catalog L172 define rank 7 the same way: `is_async == 1` **or** any `ast.Await` anywhere in the subtree. It still comes after the required-symbol pass and ranks 1–6, which M60, M61 and M67–M69 confirm. **The checklist does not match (file 21 L57, N14).** | \[S\]\[H\] |
| 4 | Rationale sentence and examples | **PASS.** The “generator expression containing `await` is asynchronous even when every `is_async` flag is 0” sentence is present in all four places. The audit model with the subtree test rejects `await` in the element, the filter, a later `for` clause, the first iterator, a nested lambda, list, set and dict comprehensions, and a default argument. Each gives `symbol=helper` and `ASYNC_COMPREHENSION`. | \[S\]\[H\]\[P311\] |
| 5 | Symbol semantics | **PASS.** The symbol uses AST ancestry: every ancestor `FunctionDef`, `AsyncFunctionDef` and `ClassDef`, outermost first, including header expressions; lambda names are excluded. `<module>` is declared unreachable. That holds: every module-body expression is rejected by `IMPORT_POLICY` (literal-only assignments, a docstring, imports), so any comprehension reaching `AST_SIGNATURE` has a definition ancestor. | \[S\]\[H\] |
| 6 | Compile-stage policy | **PASS, with a wording note (C6).** Standalone `await`, `async for` and `async with` in a synchronous function pass `ast.parse` and `AST_SIGNATURE`, and `compile()` rejects them, so they become `COMPILE_ERROR`; this was confirmed on \[P311\]. Rank 7 does not claim them. A bare `await` in a function header or a class body also reaches `COMPILE_ERROR`, but the sentence only says “function body”. | \[S\]\[P311\] |
| 7 | M70 and unchanged fixtures | **PASS.** The M70 driver and checker sources are byte-identical to the `M70_await_genexp` JSON in my v1.3.3 audit, and M70 expects `REPAIR / AST_SIGNATURE / ENTRY_POINT_REJECT / ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper\|reason=ASYNC_COMPREHENSION`. The audit model reproduces it. The M59–M61 and M65–M69 files are byte-identical to v1.3.3. | \[H\]\[P311\] |
| 8 | M63 | **PASS.** Line 7 has exactly 8 spaces and now matches the M59 base (L5–L8 against M59 L3–L6). The expected object and checker are unchanged, and only line 7 differs from v1.3.3. The index lists 1,653 B with SHA-256 `9f61a5824c23d462…`, and the manifest matches. Column 5 recomputes. | \[H\]\[P311\] |
| 9 | 144 fixtures (59 P, 13 R, 72 M) | **PASS.** Index, files and catalog each list 144 unique ids, and hashes, lengths, ids and expected objects match. Every vocabulary value traces to Protocol, file 25 or file 30. The index says `NOT RUN / NOT PASSED`; this is a descriptor check only, and nothing was executed. **File 21 still says 143 (N14).** | \[H\] |
| 10 | §3.4 against file 25; system and repair bytes | **PASS.** The two are byte-identical: 98 lines and 39,417 bytes. File 25 L1–L32 (the system and repair messages) are byte-identical to v1.3.3. | \[H\] |
| 11 | Prompt hashes | **PASS.** Schema, system and repair recompute to the same values. ORG-A and ORG-B are each 13,377 bytes and match the sidecar. Files 19, 20 and 34 are byte-identical to v1.3.3, so no model-visible bytes changed. | \[H\] |
| 12 | Register 16, labels, counts, references | **PARTIAL.** Register 16 has the v1.3.3 N13 audit section (L116) and the v1.3.4 correction section (L120), and owner state is unchanged. It still has no section for v1.3.3's own corrections (N12, M65–M69), so the C4 request from my v1.3.3 audit was only half met. All file references resolve. **Stale labels remain (C1–C5).** | \[S\]\[H\] |
| 13 | Files 59 and 60 | **PASS.** File 59 is byte-identical to the v1.3.3 audit export I delivered. File 60 says plainly that the v1.3.2 export is not included and that file 55 is only a summary, and it substitutes nothing. **C7 stays open** until the export is added. | \[H\]\[S\] |
| 14 | Manifest and ZIP CRC | **PASS.** `27_SHA256SUMS.txt` lists 256 entries, all OK, and only the manifest itself is excluded. `unzip -t` is clean, and the ZIP holds 257 files. | \[H\] |

## Fixture table: all 144 descriptors

**Summary:** all 144 are deterministic, with none ambiguous or contradictory. Status describes the **expected outcome only**; no fixture was executed by a project runner.

**\[H\] checks:**

- Index, file and catalog equality, plus SHA-256, byte length and expected object for every fixture.
- Vocabulary traceability: zero undeclared values.
- The static AST model (ranks 1–7, including the `Await` subtree test) reproduces M01, M02, M03, M38, M39, M49, M51, M52, M59–M61, M65–M70, P16 and P27. It does not model parameters, so it is silent on P15 and P26.
- The identifier model reproduces M35, M43–M46, M55–M57 and M62–M64 on \[P311\].

Only M63 changed and only M70 is new. Rows without a note are byte-identical to v1.3.3 and re-check as deterministic.

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
| M39 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper.Nested\|reason=NESTED_CLASS_FORBIDDEN` | Static AST model: rank 1. |
| M40 | DET | F18\_REJECT / F18 / ASSEMBLY\_OR\_MANIFEST\_FAILURE / `F18_REJECT\|reason=MALFORMED_CLAUSE_ID_TOKEN` |  |
| M41 | DET | CONTROL\_EXPECTATION / DESIGN\_HALT / MID\_RUN\_REEVALUATION / `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` | Declared at L175. |
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
| M60 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=create_driver\|reason=WRONG_ENTRY_POINT_KIND` | Static AST model: the required pass runs first. |
| M61 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.step\|reason=WRONG_ENTRY_POINT_KIND` | Static AST model: matches. |
| M62 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=1` | 3.11.18: byte column 1. |
| M63 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=driver.py\|line=1\|column=5` | **Changed:** line 7 restored to 8 spaces. Expected outcome is byte-identical; column 5 recomputes. |
| M64 | DET | REPAIR / IMPORT\_POLICY / IMPORT\_POLICY\_REJECT / `NON_ASCII_IDENTIFIER\|file=checker.py\|line=2\|column=15` | Character column 14, byte column 15. |
| M65 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper\|reason=ASYNC_COMPREHENSION` | Rank 7 (`is_async`). |
| M66 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=check_trace\|reason=ASYNC_COMPREHENSION` | Rank 7 (`is_async`). |
| M67 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=checker.py\|symbol=check_trace\|reason=WRONG_ENTRY_POINT_KIND` | Required pass. |
| M68 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=Driver.extra\|reason=FORBIDDEN_METHOD` | Rank 3 beats rank 6. |
| M69 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `DECORATOR_REJECT\|file=driver.py\|symbol=helper` | Rank 5 beats rank 6. |
| M70 | DET | REPAIR / AST\_SIGNATURE / ENTRY\_POINT\_REJECT / `ENTRY_POINT_REJECT\|file=driver.py\|symbol=helper\|reason=ASYNC_COMPREHENSION` | **New.** Source is byte-identical to the v1.3.3 audit JSON. 3.11.18: parses and compiles with `is_async` \[0\]; rank 7 via the `Await` subtree. |

## Hashes, assembly and package integrity

All values below were recomputed \[H\] by audit scripts, not by the project assembler.

| Object | Bytes | SHA-256 (recomputed) | Record | Result |
| --- | --- | --- | --- | --- |
| Response schema (34) | 2,529 | `6fb5d282b09540949f21ee134b522841c3345031cb3e118a83bdffc18b4e7c34` | Sidecar; byte-identical to v1.3.3 | PASS |
| System message (25) | 602 | `98020d4f9cf818968f15e4a7c0a5adc3633694aa98c5cbfe170b0904aee3c7a4` | Sidecar | PASS |
| Repair message (25) | 621 | `f11d574f4e5afb223a096b74f039ecb6a222d6ed6dc5bcf7f115dc5922c2620d` | Sidecar | PASS |
| ORG-A template stage | 13,377 | `960b6cc9877f731e46f4c53aa755e4974bcae567ae0451bda833344876c7db7d` | Sidecar; carried forward | PASS |
| ORG-B template stage | 13,377 | `ec5d391f3c2fe8c9ed91e857dc0e5d3b18e1e8db9050aae4d66561d53edc432f` | Sidecar; carried forward | PASS |
| Superseded v1.1, v1.2, v1.3 and v1.3.1 | 12,004 / 12,187 / 12,957 / 13,481 | 64-hex values | Identical to the v1.3.3 sidecar | PASS; note text inconsistent (C4) |

**Assembly \[H\]:**

- **Token-only insertion.** It reproduces both 13,377-byte values.
- **Arms.** They differ only by block order, and their rendered-block multisets are identical.
- **Fixed texts.** The fixed texts in file 30 §3.1 (B5 3,246 B, B7 2,658 B, B8 3,310 B) are exact byte prefixes of the corresponding block bodies in both arms. Each is followed by exactly `\n\n`.
- **Schema substitution.** The substituted schema equals `json.dumps(indent=2)` plus LF.
- **No model-visible change.** Files 19, 20 and 34 and file 25 L1–L32 are byte-identical to v1.3.3. The final prompts are still `TEMPLATE_STAGE_ONLY_DESIGN_PAYLOADS_UNRESOLVED`.

**Package \[H\]:**

- **ZIP.** `unzip -t` passes the CRC check with no errors, and the ZIP holds 257 files.
- **Manifest.** `27_SHA256SUMS.txt` lists 256 entries and every one verifies. Only the manifest itself is excluded.
- **Archives.** `archive_v1.3.3`, `archive_v1.3.2`, `archive_v1.3.1`, `archive_v1.3` and `archive_v1.2` each hold a ZIP that is byte-identical to its released ZIP.
- **File 59.** It is byte-identical to the v1.3.3 audit export I delivered. Its one dangling reference, to `16_OpenVEF_v1.3.3_Owner_Decision_Register.md`, is historical: that is the filename that existed in v1.3.3.

**Python runtime \[P311\], CPython 3.11.18, not the pinned patch:**

- **Parse and compile.** M70 parses and compiles, and its comprehension has `is_async` \[0\].
- **Rank-7 coverage.** Every rank-7 placement listed under scope item 4 is caught.
- **Compile-stage cases.** These pass `ast.parse` and fail `compile()`:
  - standalone `await` and `async with` in a function body;
  - `lambda: await y`;
  - `def helper(a=await x)` and `a: await x` in a header;
  - `y = await x` in a class body.
- **Pinned interpreter.** File 50 stays NOT RUN until the pinned patch is frozen.

## Findings, exact edits and owner status

### Blocker

| ID | Finding | Locations | Evidence |
| --- | --- | --- | --- |
| N14 | **The F18 checklist still describes v1.3.3.** File 21 is the controlling checklist for F18 execution, but its text matches the previous release rather than the Protocol, index and Catalog. In detail: it declares 143 mandatory fixtures and 71 M (L38, L45); its mandatory M range is M01–M69 (L44), so it excludes M70; its async-precedence row omits M70 (L34); and its rank-7 verification bullet still says `comprehension.is_async == 1` with no `ast.Await` clause (L57). The Protocol (L555), the index (`fixture_count: 144`) and the Catalog (L172) say 144 and include the `Await` clause. An F18 run that follows file 21 would skip M70 and verify the superseded rule. | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.4.md` L34, L38, L44, L45, L57; byte-identical to v1.3.3 L36–L46 | \[S\]\[H\] |

### Cleanup items (non-blocking)

| ID | Finding | Locations |
| --- | --- | --- |
| C1 | Three controlling files still carry v1.3.3 in their title or `Version:` line. | Protocol L1 (“… Protocol v1.3.3”) and L4 (“Version: 1.3.3”); file 30 L1 (“… Contract v1.3.3”); Catalog 36 L1 (“… Catalog v1.3.3”) |
| C2 | Charter §16 is stale: it says “The v1.3.3 release … records … v1.2, v1.3 and v1.3.1 audit outcomes”. That contradicts the Charter's own L9 status note, which correctly lists the v1.3.2 and v1.3.3 FAILs. | Charter L184 |
| C3 | The approval record has two sections both headed “v1.3.4 corrective release status”. The first (L66–L68) actually describes v1.3.3's N12 work (rank 7, M65–M69, M61/M63/M64 normalization), so it attributes v1.3.3 changes to v1.3.4. | `23_Owner_Approval_Record_v1.3.4.md` L66, L68, L77 |
| C4 | Two stale hash or version notes. The sidecar `hash_status_note` lists v1.3.2 among the “superseded historical values”, yet the current hashes are the v1.3.2 values and the superseded block correctly stops at v1.3.1. The manifest template's notes still say “Planning-pack v1.3.3 … unchanged from v1.3.2”. | Sidecar 33 L262; manifest 38 L71 |
| C5 | Register 16 records the v1.3.3 audit (N13) and the v1.3.4 corrections, but not v1.3.3's own corrections (N12 rank 7, M65–M69, normalization). The sequence jumps from the v1.3.2 corrections to the v1.3.3 audit. | Register 16 L111–L120 |
| C6 | The compile-stage sentence says “inside a synchronous function body”. On \[P311\], `await` in a function header (default or annotation), in a lambda, or in a class body also passes `AST_SIGNATURE` and becomes `COMPILE_ERROR`. The outcome is deterministic either way; only the wording is narrower than the behavior. | Protocol L135; file 30 L29; file 25 copy |
| C7 | The original v1.3.2 audit export was missing. **I've attached it as `OpenVEF_v1.3.2_Audit.md`:** 36,940 bytes, SHA-256 `3f23cabb8f38cfbed41b33276bdca8b28d8a59de9a74961a74a9080a92fc6f52`. It is exported from the doc at the revision I delivered (rev 6, unchanged since). File 60 handled the gap transparently. | Files 55 and 60; README |

### Exact edits (proposed only; the pack was not modified)

1. **P0 – N14 (file 21).**
   - **L34.** “M60–M61, M65–M69” → “M60–M61, M65–M70”.
   - **L38.** “All 143 fixtures” → “All 144 fixtures”, and “71 edge/missing-case descriptors” → “72 edge/missing-case descriptors”.
   - **L44.** “M01–M69 (71 descriptors” → “M01–M70 (72 descriptors”.
   - **L45.** “143 (59 P + 13 R + 71 M” → “144 (59 P + 13 R + 72 M”.
   - **L57.** After “with `comprehension.is_async == 1`” insert “**or with any `ast.Await` node anywhere in the comprehension subtree**”, and append “Confirm M70 covers a generator expression containing `await` with every `is_async` flag 0.”
   - **Then** recompute the file 21 hash in `27_SHA256SUMS.txt`.
2. **P1 – C1.** Change the Protocol L1 title to v1.3.4 and L4 to “Version: 1.3.4 …”. Change the file 30 L1 and Catalog L1 titles to v1.3.4.
3. **P1 – C2.** Charter L184: “The v1.3.4 release retains … and records the historical v0.8, v0.9, v1.0, v1.1, v1.2, v1.3, v1.3.1, v1.3.2 and v1.3.3 audit outcomes.”
4. **P1 – C3.** Rename the approval record's L66 heading to “v1.3.3 corrective release status” and, at L68, change “The v1.3.4 corrections address N12” to “The v1.3.3 corrections address N12”.
5. **P2 – C4.** In the sidecar note, change “v1.1, v1.2, v1.3, v1.3.1 and v1.3.2 … are superseded” to “v1.1, v1.2, v1.3 and v1.3.1 … are superseded; the current values were first computed in v1.3.2 and are carried forward unchanged through v1.3.4”. Change the manifest template 38 L71 note to v1.3.4.
6. **P2 – C5.** Insert a “v1.3.3 corrective document changes (not owner approvals)” section before L116 of Register 16, covering N12 rank 7, M65–M69 and the M61/M63/M64 normalization.
7. **P2 – C6.** Change “inside a synchronous function body” to “anywhere outside an `ast.AsyncFunctionDef` (including synchronous function bodies and headers, lambdas and class bodies)” in Protocol L135, file 25 and file 30 L29.
8. **P2 – C7.** Add the attached export, for example as `61_OpenVEF_v1.3.2_Independent_Audit.md` and in `archive_v1.3.2/release_documents/`. Update file 60, README and Register 16, then recompute the manifest.
9. **Housekeeping.** Update the change log and files 56–58, then archive v1.3.4 byte-for-byte.

None of these edits changes model-visible bytes, so the prompt hashes carry forward.

### Owner and authorization status

The owner state below is reproduced exactly from README L45, file 32 L6 and L40–L44, Register 16 and approval record 23:

- A1–A11: **NOT ACCEPTED** (proposed; owner acceptance `PENDING`).
- X14: **OWNER CHOICE REQUIRED**.
- Owner, TEEP applicant, contributors and approver: **TO CONFIRM**.
- Signature and date: **NOT RECORDED**.
- Authorization: **NONE**.

No identity or approval is inferred.

The required order is unchanged:

1. Independent document audit. This audit is a FAIL on N14.
2. The owner records A1–A11 and the X14 choice.
3. Implementation, with all mandatory fixtures run on the pinned CPython 3.11.
4. Independent implementation audit.
5. Only then, consideration of the LLM-call gate.

A document PASS would satisfy step 1 only.

**Evidence boundaries:**

- **\[S\] and \[H\]:** all document, vocabulary, fixture-descriptor, hash, assembly, archive and manifest results.
- **\[P311\], CPython 3.11.18, not the pinned patch:** parse and compile results, `is_async` flags, rank-7 coverage cases and identifier columns. Python 3.11 compatibility is **not marked PASS**.
- **Audit-only models:** the AST model (ranks 1–7 with the `Await` subtree test) and the identifier model are audit scripts, not the project parser.
- **\[I\], none:** no parser, assembler, harness, simulator or F1–F18 was implemented or run.
- **Not done:** no LLM or provider call, no F16, no format probe, and no source PDF or literature verification.
