# OpenVEF v1.3.6 — Owner Decision Register

**Date:** 22 November 2026  
**Status:** Seven v0.7 design decisions remain owner-approved. v0.8 owner decisions A1–A11 remain unaccepted; X14 remains OWNER CHOICE REQUIRED; the v1.3.5 document audit is reported PASS (documents only), and the v1.3.6 independent document re-audit is pending; numerical parameters are not frozen.

## Retained approved design direction (v0.7 decision IDs D1–D7)

| ID | Decision | Status |
|---|---|---|
| D1 | Complete-trace exposure: `T_i` includes all valid complete-trace pairs; `X_i = DET + PND + CHECKER_ERROR_AFTER`; `E_i=X_i/|T_i|`; `S_i=DET/X_i` | APPROVED in v0.7 |
| D2 | H1 estimation-only; H2 has exactly validity, joint exposure and joint detection | APPROVED in v0.7 |
| D3 | ORG-A/ORG-B vary whole-block presentation order only | APPROVED in v0.7; v0.8 templates correct new confounds |
| D4 | Withhold evaluator mask and reference model/API; mask entries map to author-visible specification clauses | APPROVED in v0.7 |
| D5 | Common-trace checker panel is a secondary analysis | APPROVED in v0.7; v0.8 adds stream and integrity rules |
| D6 | F16 uses a minimum validity floor per arm and is mutant-blind | APPROVED in v0.7; v0.8 adds bounded re-pilot policy |
| D7 | Apply v0.6 provenance, overlap, contamination and consistency corrections | APPROVED in v0.7 |

## v0.8 decisions A1–A11 — acceptance still required

| ID | Proposed decision | Status |
|---|---|---|
| A1 | Remove model-visible block IDs; keep IDs only in assembler metadata | PROPOSED |
| A2 | Use order-free task/repair instructions; limit interpretation to the two exact orders | PROPOSED |
| A3 | Adopt machine-readable JSON Schema v1.0 and Python 3.11 entry-point contract | PROPOSED; runtime patch/image TO FREEZE |
| A4 | Same-conversation repair; full prior messages resent byte-identically; feedback whitelist and 2,048-byte parser/compiler cap | PROPOSED |
| A5 | Integrity adjudication and panel stream/pair/nondeterminism rules | PROPOSED |
| A6 | Freeze ordering replaces impossible owner-blinding rule | PROPOSED |
| A7 | Adopt prompt assembly/canonicalization specification | PROPOSED |
| A8 | Exclude FSM from confirmatory set; FIFO + UART only | PROPOSED; decide before F16 |
| A9 | Set `R_max=2` re-pilot cap | PROPOSED; numerical value TO FREEZE |
| A10 | Human baseline author must be evaluator-independent or baseline is labelled evaluator-informed | PROPOSED |
| A11 | Apply `V_min` separately to each arm × design stratum; if any stratum remains below the floor after `R_max`, do not proceed with the pre-declared confirmatory design set | PROPOSED; owner decision required |

## Parameters still TO FREEZE

- Exact FIFO and UART specifications, clause IDs, port manifests, legal-input/reset rules and payload block allocation.
- Mask rows, don't-care windows, strict-mask variant and independent signatures.
- Confirmatory set/weights (current proposal FIFO + UART, equal weights; FSM out).
- MCY/Yosys versions, mutation modes, eligible mutant set and bounded-equivalence settings.
- Python patch/container digest/parser version, selected model/provider/tokenizer and decoding settings.
- `k=2` repair attempts, `k_null=20`, `R_max=2`, `V_min`, `n_pilot`, final sample size and power grid.
- Cycle cap, safe idle, watchdog, solver limits, bootstrap settings, balanced randomization seed and analysis release tag.
- Human baseline author and time box.
- Owner legal-name form, contributor roles and approver identity; use the same line as the actual TEEP application before external use.
- Original source-PDF binaries, SHA-256 values and page references for full-text claims.

**Implementation gate:** nothing is authorized until the owner explicitly records acceptance of v0.8 decisions A1–A11 and chooses the X14 strict-AST branch. After both decisions, only hand-built FIFO specification/mask, harness, F1–F15, parser/assembler hand-tests, and F17 using hand-built FIFO control mutants only may begin. No LLM call (including F16) until B1–B9 and the complete mandatory fixture set pass independent re-audit. Confirmatory generation remains prohibited until Protocol §18 is sealed.


## v1.0 audit corrections carried forward (renamed X1–X15)

To avoid collisions with approved v0.7 design-decision IDs D1–D7, v1.0 audit-response corrections use X1–X15. None of these correction IDs records owner approval.

| ID | Proposed correction | Status |
|---|---|---|
| X1 | Correct M10–M12 fixture shape: checker source is a string; simulated null-run outcomes move to sibling `input.null_runs` | PROPOSED |
| X2 | Add valid `create_driver` factories to M01 and M03 so only the target defect fires | PROPOSED |
| X3 | Align P27/M03/M34 fixture error classes with the normative stage map; retain diagnostic codes as defined | PROPOSED |
| X4 | Make stage 3 explicitly defer `FunctionDef` and `ClassDef` nodes to AST_SIGNATURE; define module statement reason ownership | PROPOSED |
| X5 | Define total `Import`/`ImportFrom` precedence and `MULTIPLE_NAMES`; add all conflicting-pair fixtures | PROPOSED |
| X6 | Define non-ASCII identifier rejection and SyntaxError column fallback; pin CPython 3.11 expectations | PROPOSED |
| X7 | Define mid-run design halt pause/repair/full-design rerun and repeated-failure abort behavior | PROPOSED |
| X8 | Define F18-only dispositions, stages and packet/assembly error codes separately from model feedback grammar; remove arbitrary path redaction | PROPOSED |
| X9 | Define clause-ID exact search and near-match regex; require extracted visible IDs to equal manifest IDs | PROPOSED |
| X10 | Make sidecar validation states `REQUIRED` until F18 actually records results | PROPOSED |
| X11 | Correct historical audit status wording and rename v1.0 correction IDs X1–X15 to avoid D1–D7 collision | PROPOSED |
| X12 | Record exact template-stage prompt hashes and all fixture descriptor hashes/lengths after document edits | PROPOSED; static package check only |
| X13 | Rebuild all mandatory P/R/M descriptors with one literal expected result; no fixture execution claimed | PROPOSED |
| X14 | Clarify strict-AST owner choice: keep strict AST as the current recommendation or request a separately revised relaxed branch | OWNER CHOICE REQUIRED |
| X15 | Preserve v1.0 pack and audit record as a versioned archive; regenerate checksum manifest | PROPOSED |

The strict AST policy is a recommended draft choice, not owner-approved. X14 requires an explicit owner choice. A1–A11 remain PROPOSED / NOT ACCEPTED. No work is authorized by preparing this v1.3.3 corrective draft. The v1.2, v1.3, v1.3.1 and v1.3.2 independent document audits returned FAIL for the LLM-call gate; the v1.3.2 audit identified N12. The v1.3.3 independent document audit is now the next required review. The required sequence is an independent v1.3.3 document re-audit first, then explicit A1–A11 owner decisions and an X14 branch choice, then the limited implementation-validation stage and its independent re-audit. No LLM call is authorized before the separate LLM-call gate is explicitly opened.


## Explicit owner choice required before the next gate

**X14 — AST policy branch.** Option A (recommended): retain the current strict AST policy already specified in the model-visible B5/B7/B8 blocks: no `Driver.__init__`, only `Driver.step`, no helper classes or nested classes, no decorators, no checker classes, and literal-only module constants. This minimizes policy churn and is the branch used by the proposed v1.3 fixture expectations. Option B: relax AST restrictions (for example permit `__init__`, additional methods/helper classes and selected decorators); choosing B requires new model-visible contract text, parser policy, fixtures and a fresh independent audit before any implementation/LLM call. **Status: OWNER CHOICE REQUIRED; no default acceptance inferred.**


## v1.1 audit-response corrections X16–X21

These are proposed text/fixture corrections only. Their inclusion is not owner approval, implementation or test success.

| ID | Proposed correction | Status |
|---|---|---|
| X16 | Make ASCII-only identifier policy model-visible; define tokenizer.NAME scan order, same-line import precedence and UTF-8 byte-column calculation | PROPOSED |
| X17 | Remove the B5 design-specific lead-in from the fixed-text byte string so the model-visible block has exactly two LF bytes after the fixed contract | PROPOSED |
| X18 | Remove all path-redaction references and freeze grammar-validation → UTF-8-safe truncation with marker inside cap → JSON-escape | PROPOSED |
| X19 | Separate operational recovery, evaluator revision and author-visible revision; define halt signature, one recovery cycle and second-halt terminal outcomes | PROPOSED |
| X20 | Define deterministic ENTRY_POINT_REJECT reason/symbol precedence and canonical dotted symbol names | PROPOSED |
| X21 | Correct M13/M14/P42, resolve M01/M02/M39, add M50 authoring-revision coverage and N1/N4/N5/import-precedence fixtures; mark M14/M17 as grammar-exempt primitive tests and update hashes/index/catalog | PROPOSED; fixture suite NOT RUN |

**Current authorization remains NONE.** A1–A11 remain PROPOSED / NOT ACCEPTED and X14 remains OWNER CHOICE REQUIRED. X16–X21 are not accepted by this register. No implementation, fixture execution, provider probe or LLM call is authorized by this v1.3.3 corrective draft.

## v1.2/v1.3/v1.3.1 audit response — v1.3.2 technical corrections (not owner approvals)

| ID | Proposed correction | Status |
|---|---|---|
| X22 | Correct P39 expected result to `MULTIPLE_NAMES` under multi-name-before-future precedence | PROPOSED; re-audit pending |
| X23 | Apply global AST category ordering with key `(category, file_order, lineno, col_offset, end_lineno, end_col_offset)` after the fixed required-symbol pass; align Protocol, file 25 and file 30 | PROPOSED; re-audit pending |
| X24 | Define arm/design/slot terminology and shared-item invalidation across every design × arm slot; distinguish design-local changes | PROPOSED; re-audit pending |
| X25 | Require a new preregistered study after design-membership, estimand or confirmatory-weight changes; archive and disclose all partial confirmatory ledgers | PROPOSED; re-audit pending |
| X26 | Enumerate all halt-signature component domains and trace-integrity reason mapping | PROPOSED; re-audit pending |
| X27 | Extend non-ASCII scanner to identifier-relevant `ERRORTOKEN` characters; add U+2118 and Unicode exemption fixtures; pinned Python 3.11 test remains pending | PROPOSED; runtime confirmation pending |
| X28 | Align model-visible B5 helper-function wording to actual parser enforcement; clarify character-column vs UTF-8 byte-column semantics | PROPOSED; re-audit pending |
| X29 | Remove file 25 duplicated phrase, correct stale Protocol §17 gate reference, and recompute prompt hashes after all v1.3 edits | PROPOSED; static hashes regenerated |

**No decision above records owner acceptance.** A1–A11 remain PROPOSED / NOT ACCEPTED. X14 remains OWNER CHOICE REQUIRED. No implementation, fixture execution, provider probe or LLM call is authorized by this register.


## v1.3.2 corrective document changes (not owner approvals)

The v1.3.1 independent audit's N8/N9 blockers and N10/N11 packaging/version corrections are addressed in the v1.3.2 document pack. The three optional identifier edge cases in the audit's exact-edit list are included as M62–M64 and promoted to mandatory fixture coverage. The corrections do not resolve or alter any owner decision: A1–A11 remain PROPOSED / NOT ACCEPTED, X14 remains OWNER CHOICE REQUIRED, identities remain TO CONFIRM, and authorization remains NONE.


## v1.3.3 corrective document changes (not owner approvals)

The v1.3.3 corrective pack addressed v1.3.2 audit finding N12 by adding AST_SIGNATURE category rank 7 for asynchronous `GeneratorExp`, `ListComp`, `SetComp` and `DictComp` nodes with an associated `comprehension.is_async == 1`. It added M65/M66 for `async for` generator expressions, M67 for async `check_trace`, M68 for an extra async `Driver` method, and M69 for a decorated async helper. It also normalized whitespace in M61/M63/M64. These were document/fixture changes only; they did not record owner acceptance or authorize execution. The subsequent v1.3.3 audit found N13 because the rank-7 rule did not yet cover an `ast.Await` descendant when all `is_async` flags were zero.

## v1.3.3 independent document audit — N13 (audit finding; not owner approval)

The owner-supplied `59_OpenVEF_v1.3.3_Independent_Audit.md` returned **DOCUMENT AUDIT FAIL** on N13. The audit confirmed the existing `async for` spelling was caught by rank 7, but a generator expression containing `await` could pass because all `ast.comprehension.is_async` flags remained zero. The audit also recorded five non-blocking cleanup items C1–C5. The N13 finding and C1–C4 were addressable from the available source pack and audit; the actual v1.3.2 audit export requested by C5 was not present in the current conversation or searchable Library results. File 60 records this unresolved evidence availability; no substitute or reconstructed audit is represented as the original.

## v1.3.4 corrective document changes (proposed; not owner approvals)

| Finding | v1.3.4 correction | Status |
|---|---|---|
| N13 | Extend rank 7 to any GeneratorExp/ListComp/SetComp/DictComp with `comprehension.is_async == 1` **or any `ast.Await` node anywhere in its AST subtree**; add M70 from the supplied audit JSON. | DOCUMENT EDITED; INDEPENDENT RE-AUDIT PENDING |
| C1 | Restore M63 `nested_async` body indentation to exactly eight spaces; regenerate descriptor hash/index/manifest. | STATIC BYTE CHECK PENDING INDEPENDENT RE-AUDIT |
| C2 | Define async-comprehension symbol by AST definition ancestors, including header expressions; document `<module>` as unreachable after IMPORT_POLICY. | DOCUMENT EDITED; INDEPENDENT RE-AUDIT PENDING |
| C3 | Document compile-stage `COMPILE_ERROR` handling for standalone `await`, `async for` and `async with` in synchronous function bodies when not covered by rank 7. | DOCUMENT EDITED; INDEPENDENT RE-AUDIT PENDING |
| C4 | Add this v1.3.3 audit finding and the v1.3.4 corrective status to the register. | DOCUMENT EDITED |
| C5 | Preserve the actual v1.3.2 audit export. Only the owner-supplied summary and the v1.3.2 independent-audit prompt were discoverable; the actual export was not supplied or retrievable. | **PENDING SOURCE FILE** |

The v1.3.4 pack has 144 mandatory fixture descriptors (59 P, 13 R, 72 M), all NOT RUN / NOT PASSED. No implementation or provider call is authorized by these corrections.

Owner acceptance: `PENDING`  
Owner signature: `NOT RECORDED`  
Date: `NOT RECORDED`

**Current authorization remains NONE.** A1–A11 remain PROPOSED / NOT ACCEPTED, X14 remains OWNER CHOICE REQUIRED, identities remain TO CONFIRM, and no work is authorized.


## v1.3.4 independent document audit — N14 (audit finding; not owner approval)

The uploaded `61_OpenVEF_v1.3.4_Independent_Audit.md` returned **DOCUMENT AUDIT FAIL** on N14. The audit confirmed the N13 rule and all 144 fixture descriptors, but found that the operative F18 checklist (file 21) still said 143 fixtures, stopped its M range at M69, omitted M70 from the async precedence row, and stated only the old `comprehension.is_async == 1` trigger. The audit also listed non-blocking cleanup items C1–C7. No implementation or fixture run was performed.

## v1.3.5 corrective document changes (not owner approvals)

| Finding | v1.3.5 correction | Status |
|---|---|---|
| N14 | Updated file 21 async precedence row, total counts, M01–M70 mandatory range, and rank-7 `is_async == 1` or `ast.Await` subtree condition; M70 explicitly verifies an await-containing generator expression with all `is_async` flags zero. | DOCUMENT EDITED; INDEPENDENT RE-AUDIT PENDING |
| C1 | Updated Protocol, file 30 and Catalog current-version titles/labels to v1.3.5. | DOCUMENT EDITED |
| C2 | Updated Charter §16 to describe v1.3.5 and the v0.8–v1.3.3 audit history. | DOCUMENT EDITED |
| C3 | Corrected the first duplicate approval-record heading/body to v1.3.3 history; retained a separate v1.3.4 section and added v1.3.5 status. | DOCUMENT EDITED |
| C4 | Corrected sidecar superseded-hash note and manifest-template release note. | DOCUMENT EDITED |
| C5 | Added the v1.3.3 N12/M65–M69 corrective history to this register. | DOCUMENT EDITED |
| C6 | Broadened compile-stage wording to cover locations outside `ast.AsyncFunctionDef`, including headers, lambdas and class bodies. | DOCUMENT EDITED |
| C7 | Preserve the actual v1.3.2 audit export. Its expected size/hash were supplied, but the exact file was not accessible among mounted inputs during this build; file 60 records the unresolved evidence item. | **PENDING EXACT SOURCE FILE** |

The v1.3.5 pack retains 144 mandatory descriptors (59 P / 13 R / 72 M), all NOT RUN / NOT PASSED. These corrections do not change owner decisions. A1–A11 remain PROPOSED / NOT ACCEPTED; X14 remains OWNER CHOICE REQUIRED; identities remain TO CONFIRM; signature/date remain NOT RECORDED; authorization remains NONE.


## v1.3.5 independent document audit — PASS (documents only; owner-reported)

The owner-supplied v1.3.5 audit outcome summary (file 63) reports that the v1.3.5 document audit passed. This result covers documents only: the F18 checklist, Protocol/file 25 equality, prompt-byte stability, fixture descriptor consistency, archives and checksum manifest. It does not record owner acceptance, fixture execution, implementation or authorization. The full v1.3.5 audit export was not supplied and is not represented by file 63.

## v1.3.6 corrective evidence and metadata changes (not owner approvals)

| Item | v1.3.6 correction | Status |
|---|---|---|
| C1 | Updated the F18 checklist cross-reference to include M70 in M65–M70 precedence coverage; the mandatory count/range was already correct in v1.3.5. | DOCUMENT EDITED |
| C2 | Corrected approval-record title, Charter status wording, sidecar prompt-history note and Python 3.11 check heading. | DOCUMENT EDITED |
| C3 | Included the original v1.3.2 audit export as file 62 and a byte-identical copy in `archive_v1.3.2/release_documents/`; verified 36,940 bytes and the recorded SHA-256. | SOURCE VERIFIED; C7 CLOSED |
| C4 | Recorded the owner-reported v1.3.5 document-only PASS summary as file 63 without presenting it as the full audit export. | SUMMARY RECORDED |

The v1.3.6 independent document re-audit remains pending. A1–A11 remain PROPOSED / NOT ACCEPTED; X14 remains OWNER CHOICE REQUIRED; identities remain TO CONFIRM; signature/date remain NOT RECORDED; authorization remains NONE. No implementation, fixture execution or LLM/provider call is authorized by these corrections.
