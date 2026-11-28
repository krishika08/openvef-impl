# OpenVEF v1.3.6 Change Log

**Release type:** corrective evidence/metadata release.
**Base:** v1.3.5, preserved byte-for-byte in `archive_v1.3.5/OpenVEF_Planning_v1.3.5.zip`.
**Prior audit result:** owner-supplied v1.3.5 audit summary reports DOCUMENT AUDIT PASS (documents only); see file 63. The complete v1.3.5 audit export was not attached.

## v1.3.5 audit cleanup items

- Updated the File 21 entry-point diagnostic assignment cross-reference from M65–M69 to M65–M70. The 144-fixture count, M01–M70 mandatory range and M70 await rule were already correct in v1.3.5.
- Updated the approval-record header to v1.3.6 and added a separate v1.3.6 corrective-release status without changing owner decisions.
- Corrected Charter §1 status history so v1.3.4 corrections are described as a historical release, not “this pack”; recorded the v1.3.5 document-only PASS and the v1.3.6 re-audit-pending state.
- Corrected the sidecar note: current prompt-stage hashes were first computed in v1.3.2; model-visible text changed in v1.3.2 and has remained unchanged from v1.3.3 through v1.3.6.
- Corrected the stale v1.3.4 heading in file 50.

## C7 — original v1.3.2 audit export verified and included

The owner re-uploaded `OpenVEF_v1.3.2_Audit (1).md`. The uploaded source was verified at exactly 36,940 bytes and SHA-256 `3f23cabb8f38cfbed41b33276bdca8b28d8a59de9a74961a74a9080a92fc6f52`. The exact bytes are included as file 62 and copied byte-for-byte to `archive_v1.3.2/release_documents/62_OpenVEF_v1.3.2_Independent_Audit.md`. File 60 records the verification. C7 is closed.

## Integrity and non-claims

- The v1.3.5 release ZIP is preserved byte-for-byte under `archive_v1.3.5/`.
- The v1.3.2 audit source and both included copies have the expected exact size/hash.
- The model-visible prompt templates, schema, system and repair messages were not changed in v1.3.6; template-stage hashes carry forward at 13,377 bytes per arm.
- All 144 fixtures remain NOT RUN / NOT PASSED. Static descriptor and package checks do not constitute project parser or F18 execution.
- No project parser, assembler, harness, simulator, F1–F18, LLM or provider call was executed.
- A1–A11 remain NOT ACCEPTED; X14 remains OWNER CHOICE REQUIRED; identities remain TO CONFIRM; signature/date remain NOT RECORDED; authorization remains NONE.
