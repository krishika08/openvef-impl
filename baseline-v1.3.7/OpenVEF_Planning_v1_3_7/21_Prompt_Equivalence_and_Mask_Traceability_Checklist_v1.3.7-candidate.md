# Prompt Equivalence, Parser, Repair, Assembly and Mask Traceability Checklist (F18) v1.3.7-candidate

**Controlling specifications:** `34_OpenVEF_Response_Schema_v1.0.json`, `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md`, `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md`, `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json`, `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json`, and `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md`.

## Prompt-pair and model-visible contract

| Check | Required pass condition | Status (Development-run evidence: see "F18 result" below; Formal F18 status: NOT RUN, as given in each row; Approval: see "F18 result" below) |
|---|---|---|
| Headings and arms | Exact reserved headings only; no standalone B0–B8 token, ORG label or assembler marker in model-visible bytes | NOT RUN |
| Block inventory/order | Exactly nine blocks and exact sidecar ORG-A/ORG-B orders; only whole-block permutation differs | NOT RUN |
| B5 driver contract | Factory/step positional-or-keyword signatures; local Random(seed); strict Driver-only class, only step method, no __init__, helper class or decorator; async def and async generator/comprehension expressions prohibited; required-symbol and category precedence select WRONG_ENTRY_POINT_KIND, FORBIDDEN_METHOD, DECORATOR_REJECT, ASYNC_DEFINITION or ASYNC_COMPREHENSION as applicable; module-level AST restrictions match file 30 | NOT RUN |
| B7 checker contract | Checker positional-or-keyword signature; no class or decorator; async def and async generator/comprehension expressions prohibited; required-symbol and category precedence select WRONG_ENTRY_POINT_KIND, FORBIDDEN_METHOD, DECORATOR_REJECT, ASYNC_DEFINITION or ASYNC_COMPREHENSION as applicable; module-level AST restrictions and return object match file 30 | NOT RUN |
| B8 imports/schema | Exact root allow-list; no aliases/from-imports except future annotations; submodules rejected; re.compile allowed; prohibited names/global random rules; schema byte-identical | NOT RUN |
| Fixed-text agreement | B5/B7/B8 fixed byte prefixes in each model-visible block match file 30 and are followed by exactly two LF bytes; B5 fixed text excludes its design-specific lead-in | NOT RUN |
| ASCII-only identifier visibility | B8 states every Python identifier token must be ASCII; NAME/ERRORTOKEN identifier scan, source-character vs UTF-8 byte-column semantics and import precedence are consistent across Protocol/file 30/templates | NOT RUN |
| Entry-point diagnostic assignment | Required-symbol pass and global `(category, file_order, lineno, col_offset, end_lineno, end_col_offset)` category ordering match Protocol/file 30 and M51/M52/M60/M61/M65–M70; global ranks 1–7 | NOT RUN |
| Mid-run recovery/refreeze | Operational recovery vs evaluator revision vs design/study-wide author-visible revision is distinguished; all shared-item/arm × design invalidations, preregistration reset, partial-ledger archive/disclosure, halt-signature values and one-recovery terminal behavior have fixtures | NOT RUN |
| Source AST semantics | Every strict AST rule is represented in model-visible text and has one deterministic parser rule | NOT RUN |
| Diagnostic grammar | Protocol §3.4 and file 25 contain identical exact diagnostic templates and reason enums | NOT RUN |
| JSON Pointer | Pinned validator; deterministic all-errors collection/sort; literal pointer expected for every schema fixture | NOT RUN |
| Failure-stage map | Every event maps to one repair stage or fixed terminal/design-halt outcome; precedence and driver.py-before-checker.py order are deterministic | NOT RUN |
| Feedback strings | Every repair fixture contains a literal exact diagnostic; closed-grammar validation→UTF-8-safe truncate→JSON-escape order and 2,048-byte cap are tested; path-bearing diagnostics are rejected | NOT RUN |
| Clause IDs | Manifest regex is frozen; set of regex-matched IDs in seven model-visible design payloads equals manifest clause_ids exactly; B5/B7/B8 fixed text is non-citable | TO FREEZE |
| Double-brace placeholder syntax | Every placeholder matches `{{UPPER_SNAKE_CASE}}`; unresolved matches of `\{\{[A-Z0-9_]+\}\}` hard-fail | NOT RUN |
| System and repair extraction | File-25 markers, leading/trailing blank-line handling, serialization and role mapping reproduce static message bytes | NOT RUN |
| Schema hashes | Schema SHA-256 and byte length match sidecar | RECORDED. Development-run evidence: development runs are not F18 acceptance; Formal F18 status: NOT RUN; Approval: nothing is approved |
| Prompt template-stage hashes | ORG-A and ORG-B template-stage hashes match sidecar; final hashes remain TO FREEZE until design payloads exist | NOT RUN |
| Payload/manifest binding | Seven payload hashes, spec_version_sha256 linkage and visible clause IDs are internally consistent | TO FREEZE |
| Mask traceability | Every mask row maps to author-visible spec clause; independent reviewer signs exact version | TO FREEZE |
| Runtime sandbox | Pinned Python patch/container; `import random` and local `random.Random(seed)` work; prohibited APIs remain unavailable | NOT RUN |
| Provider/model | Provider, model, role handling, tokenizer/version, token counts and generation settings pinned | TO FREEZE |
| Independent reviewer | Reviewer did not author templates or mask; signs exact hashes and checklist | PENDING |

| Async AST precedence | M60–M61, M65–M70: required symbols, extra async methods, decorators and async comprehensions follow the documented global precedence | NOT RUN |

## Mandatory fixture execution

All 144 fixtures below are mandatory: 59 parser/schema/AST/import/vector descriptors (P), 13 repair/failure-precedence descriptors (R), and 72 edge/missing-case descriptors (M). Every descriptor contains literal input data and one expected result, and its hash and byte length are listed in `41_F18_Fixture_Inputs/fixture-index.json`.

| Fixture family | Mandatory IDs | Status (Development-run evidence: see "F18 result" below; Formal F18 status: NOT RUN, as given in each row; Approval: see "F18 result" below) |
|---|---|---|
| Parser/schema/AST/import/vector fixtures | P01–P48 (59 descriptors, including lettered subcases and P44–P48 import/ASCII boundary cases) | NOT RUN |
| Repair/failure-precedence fixtures | R01–R13 (13 descriptors) | NOT RUN |
| Previously uncovered edge/missing-case fixtures | M01–M70 (72 descriptors, including M04a/b and M08a/b) | NOT RUN |
| Total materialized fixture descriptors | 144 (59 P + 13 R + 72 M; all mandatory, including local unit vectors) | NOT RUN |
| Fixture byte hashes | Every listed descriptor hash in `fixture-index.json` | NOT RUN |

F18 must fail if any fixture is missing, not materialized, hash-mismatched, ambiguous, assigned an outcome not in the normative contract, or produces a different stage, error class, diagnostic byte string or terminal disposition.

## F18 result

F18 status, in three separate parts: Development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; Formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; Approval: no implementation is qualified or approved. This checklist is a proposed test specification, not evidence that a parser, assembler, sandbox, harness or experiment has been implemented. No owner acceptance of A1–A11 is recorded; no work or LLM call is authorized.


## v1.3.5 audit gate additions

- Verify async generator/comprehension nodes (`ast.GeneratorExp`, `ast.ListComp`, `ast.SetComp`, `ast.DictComp`) with `comprehension.is_async == 1` **or with any `ast.Await` node anywhere in the comprehension subtree** are rejected at `AST_SIGNATURE` category rank 7, after ranks 1–6 and the required-symbol pass. Confirm M65/M66 cover driver and checker files. Confirm M70 covers a generator expression containing `await` with every `is_async` flag 0.
- Confirm M67–M69 exercise async `check_trace`, an extra async `Driver` method and a decorated async helper.
- M61/M63/M64 whitespace cleanup must not change their expected AST or identifier-column results.

## v1.1 audit gate additions

- Confirm the exact disposition/stage/error/diagnostic vocabulary in Protocol §3.4 and Catalog v1.3.7-candidate; F18-only codes are not sent to the model. M14/M17 are isolated grammar-exempt serializer primitive tests, not production acceptance tests.
- Verify the total import node precedence fixtures P29a/P29b/P30 and P31–P43.
- Verify `ClassDef` and `FunctionDef` stage ownership: module policy defers these nodes; AST_SIGNATURE owns decorators/classes/nesting.
- Verify non-ASCII identifier token detection, same-statement import precedence and UTF-8 byte-column fixtures under the pinned CPython 3.11 patch.
- Verify mid-run design halt and repeated halt lifecycle fixtures; no slot is final-scored before the design-wide rerun.
- Verify `clause_id_regex`, `clause_id_search_regex`, `clause_id_near_match_regex`, and exact visible-ID/manifest equality.
- Sidecar check values remain `REQUIRED` until a formal F18 acceptance run is executed (development runs are not F18 acceptance and do not set them; nothing is approved); no static package audit sets a pass flag.
- Current release status: Development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; Formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; Approval: no implementation is qualified or approved; A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE REQUIRED**.

- [ ] M14/M17 are treated only as grammar-exempt serializer primitive tests; neither bypasses production feedback grammar validation.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
