# Claude v0.8 Audit Resolution — OpenVEF v0.9 Draft

**Audit date:** 22 November 2026  
**Audit verdict:** FAIL for the LLM-call gate  
**Disposition:** C1–C18 drafted as owner proposals; none is claimed to have passed re-audit.  
**Scope:** This resolution is grounded in the v0.8 audit report supplied by the owner. It does not re-fetch or visually inspect source PDFs.

## 1. Audit conclusion

The v0.8 audit accepted N1 and N2. N3 (model-visible/executable output contract), N4 (complete deterministic repair path) and N9 (reproducible assembly of system/repair messages and sidecar hashes) remain partially resolved. Four blocking edit groups C1–C8 and C18 have therefore been drafted; C9–C17 are also included to resolve minor consistency, freeze-order and hygiene issues. No LLM call of any kind is permitted until C1–C8 and C18 are independently re-audited and owner acceptance of A1–A11 is recorded.

## 2. N3 — output contract

- The proposed author-visible Driver API and Checker contract blocks contain the factory/step/checker interface, first-call semantics, driver restrictions, vector encoding, checker metadata and checker return object.
- The Response schema block states the exact import-root allow-list, no-third-party rule and empty dependency list. B5/B7/B8 are intended to match the normative parser contract in file 30; F18 must compare the fixed contract text byte-for-byte.
- Checker return requires exactly `verdict` and `diagnostics`; diagnostics is a required list and may be empty. Only invalid top-level return, missing/non-list diagnostics, invalid verdict or crash is a checker error. A malformed individual diagnostic is logged and discarded without changing PASS/FAIL.
- File 30 defines AST and inspect checks, ignores annotations, and specifies required names/parameter kinds/counts for `create_driver`, `Driver.step` and `check_trace`.
- Assumption clause IDs are validated against the frozen author-packet manifest; `UNSPECIFIED` is reserved for genuinely unspecified behavior.
- The fixed fixture catalog in file 36 provides hand-written parser/AST/vector/checker/assumption tests and expected outcomes, including separate cases for provider token truncation and malformed JSON.

## 3. N4 — failure and repair contract

Protocol §3.4 provides an exhaustive map for schema/token truncation, import violation, driver/checker compilation, runtime exceptions, vector invalidity, watchdog, checker errors, null rejection, nondeterminism and RTL/null control failures. Every event is either a specific repair stage/error/diagnostic or terminal-invalid with no repair.

The first-failure pipeline order is frozen. Null checker invocation 1 and 2 run in separate processes on the same immutable trace. Two FAIL verdicts trigger null rejection repair; two PASS verdicts pass; disagreements or a valid/error disagreement are terminal nondeterminism; two matching runtime/return errors permit checker-runtime repair. Raw validator/compiler text is not sent. Feedback uses a fixed code/JSON Pointer or filename/line code, redaction → truncation → JSON escaping, UTF-8 code-point boundary, 2,048 pre-escape byte cap and fixed truncation marker.

## 4. N9 — prompt assembly

File 31 now specifies extraction of system and repair messages from the exact marker-delimited regions of file 25, including blank-line trimming, LF, one terminal LF, repair marker retention, exact placeholder replacement, two-space indentation and deterministic feedback serialization. The static system and repair-template message hashes and byte lengths are recorded in the sidecar. Reserved-heading-identical payload lines are hard errors at packet freeze; there is no escaping path. The schema is renumbered to file 34, and its SHA-256 and byte length are recorded in the sidecar; each payload hash/byte field is present but remains TO FREEZE until design packets exist.

## 5. Other audit corrections

- F17 feasibility is hand-built FIFO controls only; confirmatory-manifest F17 runs only after the complete authoring packet/mask/directed suite freeze.
- F16 and any re-pilots finish before confirmatory mutant-manifest generation. `R_max=2` means at most three pilots total (initial plus two re-pilots).
- Panel mutant traces are evaluated twice; inconsistent verdicts/errors are events, not detection, and do not alter the benign-trace compatibility partition.
- `J_exposure` is explicitly checker-dependent through the validity gate; only conditional `E_i` is checker-independent.
- Global `random` is not seeded; generated code uses local `random.Random(seed)`. NumPy removed. Input-vector validation, first-call semantics and checker metadata exclusions are specified.
- README lists all controlling documents; provenance log title/version updated; CSV has defined clause-to-block format; initial vs post-repair validity is named in the funnel; duplicate file number 29 is removed.
- Owner, TEEP applicant, contributors and approver remain TO CONFIRM. No identity is inferred.

## 6. Authorization status

No work is authorized until the owner records acceptance of v0.8 A1–A11. After acceptance, only hand-built FIFO specification/mask, harness, F1–F15, hand-written parser/assembler tests, and F17 using hand-built FIFO control mutants may begin. No LLM call—including F16, smoke tests or provider probes—until C1–C8 and C18 pass independent re-audit. Confirmatory generation remains prohibited until every Protocol §18 freeze item is complete and sealed.

## 7. Explicit limitations

This v0.9 package is a document-level correction draft. It does not include a running parser/assembler implementation, a frozen FIFO/UART payload, a populated mask, pinned runtime/provider, owner signature or F1–F18 results. The v0.8 auditor did not retrieve or visually inspect source PDFs; source claims remain governed by the provenance log.
