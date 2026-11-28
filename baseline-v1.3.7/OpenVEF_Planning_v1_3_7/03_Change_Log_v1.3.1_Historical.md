# OpenVEF Change Log v1.3.1

**Date:** 22 November 2026
**Status:** Corrective document release draft; independent re-audit pending; no implementation, fixture execution or owner approval implied.

## Changes from v1.0 after Claude's independent audit

1. Corrected the three malformed event fixtures M10–M12: `checker.source` is now a source string and run outcomes are in sibling `input.null_runs`.
2. Added valid factories to M01/M03 to isolate their intended AST defects.
3. Aligned fixture `error_class` values with stage-map error classes while preserving diagnostic codes.
4. Defined module-policy stage ownership: `FunctionDef`/`ClassDef` are deferred from module-body policy to AST_SIGNATURE; decorators/classes/nesting have one owner stage.
5. Defined total `Import` and `ImportFrom` priority, including multi-name imports; added priority-pair fixtures.
6. Added non-ASCII identifier rejection and `SyntaxError.offset` column fallback.
7. Added the mid-run halt lifecycle: preserve artifacts, repair evaluator once, rerun all design slots, abort if the halt recurs.
8. Added a normative F18-only disposition/stage/error vocabulary distinct from model-feedback grammar. Removed arbitrary path redaction; feedback serialization accepts only fixed diagnostics.
9. Defined exact clause-ID extraction and near-match regexes; visible payload IDs must equal manifest IDs.
10. Changed sidecar pre-execution validation flags to `REQUIRED`; no result is marked true before F18.
11. Preserved the strict-AST branch as an owner choice, not an accepted decision.
12. Preserved v1.0 as `archive_v1.0/OpenVEF_Planning_v1.0.zip`; regenerated current checksums.

## Non-claims

No parser/assembler/harness implementation exists in this package. No fixture was executed. No LLM/provider call was made. No source PDF was retrieved or independently verified. A1–A11 remain unaccepted and X14 remains an owner choice.


## v1.2 — v1.1 audit-response draft

- Made the ASCII-only Python identifier requirement model-visible in B8 and defined token scanning, same-line import precedence and UTF-8 byte-column reporting.
- Removed the B5 design-specific lead-in from the normative fixed-text prefix so the model-visible payload is separated by exactly two LF bytes.
- Removed all path-redaction operations/references from current controlling text; feedback now follows closed-grammar validation, UTF-8-safe truncation with marker inside the 2,048-byte cap, then JSON escaping.
- Reworked mid-run halt/recovery into operational recovery, evaluator revision and author-visible revision paths; defined halt signatures and one-recovery terminal outcomes.
- Added a deterministic ENTRY_POINT_REJECT reason/symbol assignment algorithm and multi-defect order.
- Corrected M13, M14 and P42; added P44–P48 and M43–M49; regenerated fixture index and checksums.
- Added M50 for author-visible/estimand revision; made M14/M17 explicit grammar-exempt primitive vectors; defined nested-class-first AST_SIGNATURE precedence and wrong-kind entry points; aligned current references to v1.2; removed stale duplicate FSM row. The current mandatory fixture inventory is 124 descriptors: 59 P, 13 R and 52 M; every descriptor remains NOT RUN / NOT PASSED.
- No parser, assembler, harness, fixture suite, F1–F18 or LLM/provider call was executed. All fixtures remain NOT RUN / NOT PASSED. Owner decisions remain pending.

## v1.3 — response to the v1.2 independent audit FAIL

1. Corrected P39: `from __future__ import annotations, division` expects `MULTIPLE_NAMES`, because multi-name precedence precedes future-feature classification.
2. Replaced per-file/source-order AST structure selection with a global category pass after the fixed required-symbol pass. The exact key is `(category, file_order, lineno, col_offset, end_lineno, end_col_offset)`. Protocol, file 25 and file 30 now state the same rule; M51/M52 cover same-file and cross-file conflicts.
3. Defined arms (ORG-A/ORG-B), designs (FIFO/UART) and slots (arm × design). Shared-item changes invalidate all designs and all arm × design slots; design-specific changes invalidate both arms for the affected design.
4. Required a new preregistered study for design-membership, estimand or confirmatory-weight changes after confirmatory generation starts. All partial confirmatory ledgers must be archived and disclosed; old confirmatory artifacts are not reusable. M48/M50 inputs contain only the change class; M53 covers the study reset.
5. Enumerated halt-signature domains and the trace-integrity reason-to-component mapping; M54 covers the closed vocabulary and volatile-field exclusion.
6. Extended non-ASCII identifier scanning to `tokenize.NAME` and identifier-relevant `tokenize.ERRORTOKEN` code points. M55/M56 exercise U+2118 and an ASCII-prefixed identifier; M57 protects Unicode strings/comments. The pinned Python 3.11 runtime check remains pending and must be completed before implementation validation.
7. Aligned B5 helper-function wording with the parser's actual AST policy: synchronous undecorated helpers are not restricted to module scope except where class/method rules apply.
8. Clarified source-character columns (`SyntaxError.offset`) versus UTF-8 byte columns (`NON_ASCII_IDENTIFIER`).
9. Removed the duplicated phrase in file 25 and corrected the stale v1.1 LLM-gate reference in Protocol §17.
10. Recomputed v1.3 prompt-template-stage hashes after model-visible B5/B8 edits; v1.1 and v1.2 hashes are retained as superseded history.
11. Increased the mandatory fixture inventory from 124 to 132. All 132 fixtures remain NOT RUN / NOT PASSED.
12. Preserved the original v1.2 ZIP byte-for-byte in `archive_v1.2/`; the v1.2 audit tracker is retained unchanged as historical evidence.

## Non-claims

No project parser, assembler, harness, simulator, F1–F18 or fixture runner was implemented or executed. No LLM/provider call was made. No source PDF was opened or verified. The Python 3.11 tokenizer check was not run because no CPython 3.11 interpreter is available in this environment; Python 3.13 lexical probing is not a substitute. A1–A11 remain PROPOSED / NOT ACCEPTED, X14 remains OWNER CHOICE REQUIRED, and nothing is authorized.


## v1.3.1 — response to the v1.3 independent document audit FAIL

1. Corrected M53 to use the declared `AUTHORING_REVISION_REQUIRED` error class; declared M54's `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED` diagnostic and matching error class in the closed local lifecycle/control vocabulary.
2. Replaced obsolete lifecycle action literals with the exact closed `required_action` values used by M48, M50, M53, M54 and M58. The rules preserve study-wide shared-item invalidation, design-specific invalidation across both arms, and new-preregistration reset for membership/estimand/weight changes.
3. Assigned all `ast.AsyncFunctionDef` nodes at any lexical depth to `AST_SIGNATURE`, category rank 6, with `ENTRY_POINT_REJECT` / `ASYNC_DEFINITION`; updated stage ownership, closed reason enumerations, B5/B7 model-visible prompt text and file 30. Added mandatory fixture M59 for a nested `async def` within a synchronous helper.
4. Completed the file 25 Protocol §3.4 control copy by including the three initial human/LLM feedback-policy bullets and synchronized the full body from the canonical Protocol.
5. Corrected the superseded v1.2 ORG-B hash using the original v1.2 sidecar value; retained v1.3 prompt-stage hashes as superseded history and recomputed v1.3.1 prompt-stage hashes after B5/B7 edits.
6. Corrected Charter §16 to reference `02_OpenVEF_Experimental_Protocol_v1.3.1.md`. Preserved the v1.3 release ZIP byte-for-byte in `archive_v1.3/`.
7. Mandatory fixture inventory: 133 descriptors (59 P, 13 R, 61 M). All fixtures remain NOT RUN / NOT PASSED.

## Non-claims for v1.3.1

No project parser, assembler, harness, simulator or F1–F18 suite was implemented or executed. No LLM/provider call was made. No authorization is recorded. A1–A11 remain unaccepted and X14 remains an owner choice. The exact pinned Python 3.11 runtime remains to be frozen. The three optional additional fixtures mentioned in the linked v1.3 audit artifact were not added because the artifact could not be retrieved in this environment and their exact inputs/precomputed columns were not present in the supplied audit summary.
