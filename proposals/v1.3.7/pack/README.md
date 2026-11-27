# OpenVEF Planning Pack v1.3.7-candidate

**Status:** v1.3.7 CANDIDATE, not audited: OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md` (`CANDIDATE-LABEL.md` lists every file); v1.3.6 remains the default. v1.3.6 status: Corrective evidence/metadata release following the owner-reported v1.3.5 document-audit PASS. Independent v1.3.6 document-only re-audit is pending. This pack is not owner-approved, implemented or authorized.

## Current controlling files

- `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` — project framing, scope, risk and gates.
- `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` — canonical metrics, hypotheses, lifecycle, diagnostics, AST precedence and F1–F18.
- `03_Change_Log_v1.3.6.md` — v1.3.6 release changes and audit lineage; the candidate's changes are in `CHANGELOG-v1.3.7-candidate.md`.
- `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` and `23_Owner_Approval_Record_v1.3.6.md` — owner decision/approval state.
- `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` — operative proposed F18 checklist; 144 mandatory descriptors.
- `19_ORG_A_Prompt_Template.txt`, `20_ORG_B_Prompt_Template.txt`, `25_Common_System_and_Repair_Prompt_Templates.txt` — prompt templates and assembler-only normative control copy. The §3.4 copy in file 25 is not model-visible.
- `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` — response, import, AST, async-comprehension, compile, vector, checker and runtime contract.
- `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` and `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` — deterministic assembly and current template-stage hashes.
- `34_OpenVEF_Response_Schema_v1.0.json` — schema version 1.0, independent of planning-pack version.
- `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` and `41_F18_Fixture_Inputs/` — 144 mandatory fixture descriptors and index; formal F18 status NOT RUN / NOT PASSED (development runs are not F18 acceptance; nothing is approved).
- `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` — clause-ID manifest template; payloads and hashes remain TO FREEZE.
- `48_Claude_v1.3.6_Independent_Audit_Prompt.txt` — instructions for independent document-only re-audit.
- `50_Python311_Unicode_Tokenizer_Check.md` — pinned-runtime Unicode test: formal status NOT RUN (development runs of a project implementation, recorded outside this pack, are not this check; nothing is approved).
- `56_v1.3.6_Static_Build_Checks.json`, `57_v1.3.6_Build_Integrity_Record.md`, `58_v1.3.6_Correction_Resolution.md` — package checks and correction provenance.
- `60_v1.3.2_Audit_Export_Status.md` — exact v1.3.2 audit export size/hash and inclusion status.
- `61_OpenVEF_v1.3.4_Independent_Audit.md` — v1.3.4 audit, preserved verbatim.
- `62_OpenVEF_v1.3.2_Independent_Audit.md` — original v1.3.2 audit export, exact bytes verified.
- `63_OpenVEF_v1.3.5_Audit_Summary_Owner_Supplied.md` — owner-supplied summary of the v1.3.5 document-only PASS; not the complete audit export.

## v1.3.6 corrections

1. Added M70 to the File 21 diagnostic-assignment cross-reference (M60–M61, M65–M70); all mandatory counts/ranges and the await-subtree rank-7 rule were already correct in v1.3.5.
2. Corrected the approval-record title, Charter status note, sidecar prompt-history wording and file 50 heading.
3. Verified and included the original v1.3.2 audit export; C7 is closed. Exact size: 36,940 bytes. SHA-256: `3f23cabb8f38cfbed41b33276bdca8b28d8a59de9a74961a74a9080a92fc6f52`.
4. Preserved the v1.3.5 release ZIP byte-for-byte under `archive_v1.3.5/`.

## Fixture inventory and execution status

The current mandatory inventory is **144 descriptors (59 P, 13 R, 72 M)**. Status, in three separate parts, for every fixture: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved. Descriptor hashes and lengths are static package metadata, not project-runner execution results.

## Historical evidence and audit availability

- `archive_v1.2/`, `archive_v1.3/`, `archive_v1.3.1/`, `archive_v1.3.2/`, `archive_v1.3.3/`, `archive_v1.3.4/` and `archive_v1.3.5/` preserve earlier releases.
- The exact v1.3.2 audit export is included as file 62 and copied to `archive_v1.3.2/release_documents/`; file 60 records exact size/hash verification.
- File 59 (v1.3.3) and file 61 (v1.3.4) are preserved audit exports. File 63 is only an owner-supplied v1.3.5 audit outcome summary; the complete v1.3.5 audit export was not attached.
- File 55 is only an earlier summary of the v1.3.2 audit and is not used as a substitute for file 62.

## Status and authorization

The owner-supplied v1.3.5 audit summary reports a document-only PASS. The v1.3.6 independent document audit is pending; the v1.3.7-candidate pack is not audited. All 144 fixture descriptors remain formally NOT RUN / NOT PASSED: a project implementation (parser, assembler, harness, simulator, F1–F18) exists outside this pack with development-run evidence only, there is no authorized F18 acceptance run, and nothing is qualified or approved. The exact pinned CPython 3.11 patch remains TO FREEZE. CPython 3.11.18 audit evidence does not substitute for a pinned-runtime implementation run.

A1–A11 remain **PROPOSED / NOT ACCEPTED**; X14 remains **OWNER CHOICE REQUIRED**. Owner, TEEP applicant, contributors and approver identities remain **TO CONFIRM**. Signature/date are **NOT RECORDED**. Authorization is **NONE**. The required order remains independent document re-audit, owner decisions, implementation and fixture execution on pinned CPython 3.11, independent implementation-results audit, and only then consideration of the separate LLM-call gate. No LLM/provider calls, F16, smoke tests, provider-format probes or confirmatory generation are authorized.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
