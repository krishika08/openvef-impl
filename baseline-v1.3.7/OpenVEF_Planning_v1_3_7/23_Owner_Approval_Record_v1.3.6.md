# OpenVEF Owner Approval Record — v1.3.6

**Date:** 22 November 2026  
**Status:** OWNER ACCEPTANCE NOT RECORDED; v1.3.5 document audit PASS reported; v1.3.6 corrective document re-audit pending

## Previously approved v0.7 design directions

The following seven methodological directions remain approved in the earlier decision record:
1. Complete-trace conditional `E_i` and crash-inclusive `S_i` definitions.
2. H1 estimation-only; exactly three H2 outcomes.
3. ORG-A/ORG-B whole-block presentation-order comparison.
4. Evaluator-only mask/reference-model boundary with mask-to-specification traceability.
5. Common-trace checker panel as a secondary analysis.
6. Per-arm/design minimum validity floor for F16; mutant-blind pilot.
7. Prior-art, provenance, overlap, contamination and consistency corrections.

These v0.7 approvals do not approve later implementation details or remove the separate gates below.

## v0.8 owner decisions A1–A11

All eleven decisions remain **PROPOSED — NOT ACCEPTED**. The owner must review and explicitly accept or reject them in the approval record before any work is authorized.

Owner acceptance: `PENDING`  
Owner legal name: `TO CONFIRM`  
TEEP applicant identity: `TO CONFIRM`  
Contributors and roles: `TO CONFIRM`  
Approver identity: `TO CONFIRM`  
Approval date/signature: `NOT RECORDED`

## v1.1 audit-response corrections X1–X15

X1–X13 and X15 are proposed technical/document corrections responding to the v1.0 independent audit. Their presence in this pack is not owner acceptance, implementation or test success.

**X14 — strict-AST branch choice: OWNER CHOICE REQUIRED.** Option A retains the strict AST policy currently represented in B5/B7/B8 and the fixture expectations. Option B would require a separately revised, relaxed policy, model-visible prompt text, parser contract and fixtures, followed by a new independent audit. No option is accepted by this record.

## Identity and authorship

Owner legal name, TEEP applicant, contributor roles and approver identity remain **TO CONFIRM against the actual TEEP application**. No identity is inferred from prior draft metadata or project history. The same confirmed ownership/authorship line must appear in the Charter, Protocol, this record and any faculty/TEEP submission.

## Work authorization

**Current authorization: NONE.** No FIFO feasibility work, parser/assembler implementation, F1–F18 execution, provider probe, F16 or confirmatory generation is authorized by the existence of this draft or by an audit request.

Only after the owner records acceptance of A1–A11 and an explicit X14 branch choice may the following limited hand-built scope open: (1) FIFO specification and clause/mask traceability rows; (2) hand-built FIFO harness and ledger; (3) F1–F15; (4) parser/assembler tests against the mandatory hand-written fixtures; and (5) F17 using hand-built FIFO control mutants only.

No LLM call of any kind, including F16, smoke tests and provider-format probes, is permitted until the complete mandatory fixture set and all blocking document findings receive an independent re-audit confirming that every expected outcome is deterministic and consistent. Confirmatory generation remains prohibited until every Protocol §18 freeze item is completed, checked and sealed.

Owner acceptance: `PENDING`  
Owner signature: `NOT RECORDED`  
Date: `NOT RECORDED`


## v1.1 audit-response corrections X16–X21

X16–X21 are proposed responses to the v1.1 independent audit. Their presence is not owner acceptance, implementation or F18 execution. All six remain **PROPOSED — NOT ACCEPTED**.

Owner acceptance: `PENDING`  
Owner legal name: `TO CONFIRM`  
TEEP applicant identity: `TO CONFIRM`  
Contributors and roles: `TO CONFIRM`  
Approver identity: `TO CONFIRM`  
Approval date/signature: `NOT RECORDED`

**No work is authorized.** A1–A11 remain not accepted and X14 remains an explicit owner choice. The current required sequence is the independent document re-audit specified in file 32, then this owner record must explicitly record A1–A11 acceptance/rejection and the X14 choice, then the limited implementation-validation scope may open. The LLM-call gate remains separate: F16, smoke tests and provider-format probes are prohibited until the implementation, the complete mandatory fixture suite on pinned CPython 3.11, and their independent re-audit have passed and the owner has explicitly opened that gate.

## v1.3.3 corrective release status

The v1.3.3 corrections address N12 by defining AST_SIGNATURE rank-7 rejection of asynchronous comprehension expressions and adding M65/M66 coverage, alongside M67–M69 async-precedence cases and whitespace normalization in M61/M63/M64. Their inclusion is not owner acceptance, implementation, fixture execution or LLM authorization. The subsequent v1.3.3 independent document audit returned FAIL on N13. The v1.3.3 mandatory fixture inventory was 143 descriptors (59 P / 13 R / 71 M), all NOT RUN / NOT PASSED in that release record.

Owner acceptance: `PENDING`  
Owner signature: `NOT RECORDED`  
Date: `NOT RECORDED`

**Historical authorization: NONE.** A1–A11 were not accepted; X14 remained an explicit owner choice. No LLM/provider call was authorized by the v1.3.3 release.


## v1.3.4 corrective release status

The v1.3.4 pack addresses N13 and audit cleanup C1–C4. At the time of the v1.3.4 build, the exact v1.3.2 audit export requested by C5 was unavailable; this historical gap was subsequently closed in v1.3.6 by including and verifying the exact source as file 62. The v1.3.3 audit is preserved as file 59 and the v1.3.4 audit as file 61. All 144 fixture descriptors remain NOT RUN / NOT PASSED; no project parser, assembler, harness, simulator or fixture runner has been executed. The pinned CPython 3.11 patch remains TO FREEZE.

A1–A11: **NOT ACCEPTED**. X14: **OWNER CHOICE REQUIRED**. Identities: **TO CONFIRM**. Signature/date: **NOT RECORDED**. Authorization: **NONE**.


## v1.3.5 corrective release status

The v1.3.5 pack corrects N14 by updating the operative F18 checklist to 144 mandatory fixture descriptors, including M70, and to the `is_async == 1` or `ast.Await` subtree rule. It also updates stale current-version labels, Charter §16, sidecar/manifest notes, Register 16 history and compile-stage wording. The v1.3.4 audit is preserved verbatim as file 61. The original v1.3.2 audit export is reported as 36,940 bytes with SHA-256 `3f23cabb8f38cfbed41b33276bdca8b28d8a59de9a74961a74a9080a92fc6f52`, but that exact file was not available among the mounted build inputs; file 60 keeps the evidence item pending.

All 144 fixture descriptors remain NOT RUN / NOT PASSED. No project parser, assembler, harness, simulator or F1–F18 was executed. The pinned CPython 3.11 patch remains TO FREEZE.

A1–A11: **NOT ACCEPTED**. X14: **OWNER CHOICE REQUIRED**. Owner/applicant/contributor/approver identities: **TO CONFIRM**. Signature/date: **NOT RECORDED**. Authorization: **NONE**.


## v1.3.6 corrective evidence and metadata release status

The v1.3.6 release incorporates the owner-reported v1.3.5 DOCUMENT AUDIT PASS (documents only), corrects the remaining v1.3.5 non-blocking metadata/cross-reference items, and includes the exact v1.3.2 audit export as file 62. The export is verified at 36,940 bytes with SHA-256 `3f23cabb8f38cfbed41b33276bdca8b28d8a59de9a74961a74a9080a92fc6f52`; a byte-identical copy is stored under `archive_v1.3.2/release_documents/`. The v1.3.5 complete audit export was not supplied; file 63 is only the owner-supplied outcome summary. The v1.3.6 independent document re-audit remains pending.

No fixture execution, implementation, provider probe or LLM call is authorized by this release. A1–A11 remain **NOT ACCEPTED**; X14 remains **OWNER CHOICE REQUIRED**; identities remain **TO CONFIRM**; signature/date remain **NOT RECORDED**; authorization remains **NONE**.
