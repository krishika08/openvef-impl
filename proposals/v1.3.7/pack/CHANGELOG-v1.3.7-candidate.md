# CHANGELOG — OpenVEF Planning v1.3.7 CANDIDATE (from v1.3.6)

**v1.3.7 CANDIDATE, not audited.** Built by `proposals/v1.3.7/build_candidate.py` from `baseline/OpenVEF_Planning_v1_3_6/`
(read-only, unchanged) under owner decision D-024 (Krishika). Rationale for every correction, with the
conflicting v1.3.6 text and the alternatives rejected: `proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md`.

- Every edit replaces text inside one line; no line moves, so line citations are the same in both packs.
- `correction` = C1–C16; `A1`, `A2` = numbered amendments; `OS-1–OS-3` = OWNER-SPECIFIED items (owner
  decision D-026; not pack-derived, counted separately from C1–C16); `S` = a stale reference fixed (D-025 item 3;
  `line` `name` = a file renamed); `label` = the in-file candidate label; `derived` = a hash or byte length
  that follows mechanically from another edit. Old and new text are the replaced part of the line, unless
  `line` is `all` (whole-file replacement).
- **Correction cycle 2 (owner decision D-027), after document audit #1 (NOT CLEARED;
  `docs/reviews/doc-audit1-gpt6-2026-11-27.md` in the implementation repository).** Its entries follow the last
  cycle-1 entry (E158) and edit the text as cycle 1 left it, so no cycle-1 entry number moves. `OD-n` =
  OWNER-DECIDED: a normative rule the owners add that v1.3.6 does not state, labelled as such in the pack text;
  every fixture that depends on one is counted OWNER-DECIDED. For cycle-2 entries the `PD` column holds the
  audit finding (`D1-n`). `derived` entries show the hashes of the final build, cycle 2 included.
- **Correction cycle 3 (owner decision D-029), after document audit #2 (NOT CLEARED, one MINOR finding D2-1;
  `docs/reviews/doc-audit2-gpt6-2026-11-27.md` in the implementation repository).** Its entries follow the last
  cycle-2 entry (E205), so no earlier entry number moves. `C18` = the three-part status wording (development-run
  evidence / formal F18 status / approval) applied to every current status statement that lacked it; the `PD`
  column holds the finding (`D2-1`). `derived` entries show the hashes of the final build, cycle 3 included.
- **Kept on purpose (not stale):** references that record history — the v1.3.6 change log, build, correction
  and audit records (Files 03, 48, 50, 56, 57, 58, 63 and the audit transcripts), and statements of what
  v1.3.6 did — and the owners' records (Files 16, 23), which describe owner decisions on v1.3.6 and are not
  rewritten for a candidate the owners have not approved.
- The 61 `archive_*` entries of `27_SHA256SUMS.txt` are not in the extracted baseline and are not in this copy.

| # | Correction | PD / finding | Fixtures | File | Line |
|---|---|---|---|---|---|
| E01 | C1 | PD-02 (2) | M48, M50, M53, M54, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 175 |
| E02 | A2 (copy of C1) | PD-02 (2) | M48, M50, M53, M54, M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 118 |
| E03 | C2 | PD-02 (1) | M48, M50, M53, M54, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E04 | A2 (copy of C2) | PD-02 (1) | M48, M50, M53, M54, M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E05 | C2 | PD-02 (1) | M50 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E06 | A2 (copy of C2) | PD-02 (1) | M50 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E07 | C2 | PD-02 (1) | M53 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E08 | A2 (copy of C2) | PD-02 (1) | M53 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E09 | C2 | PD-02 (1) | M54 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E10 | A2 (copy of C2) | PD-02 (1) | M54 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E11 | C2 | PD-02 (1) | M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E12 | A2 (copy of C2) | PD-02 (1) | M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E13 | C2 | PD-02 (1), (3) | M48, M50, M53, M54, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E14 | A2 (copy of C2) | PD-02 (1), (3) | M48, M50, M53, M54, M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E15 | C3 | PD-02 (3) | M54 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 185 |
| E16 | A2 (copy of C3) | PD-02 (3) | M54 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 128 |
| E17 | C10 | PD-01 | M41, M42, M47 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 185 |
| E18 | A2 (copy of C10) | PD-01 | M41, M42, M47 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 128 |
| E19 | C4 | PD-03 | M14, M17, M41, M48, M50, M53, M54, M58 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 176 |
| E20 | C5 | PD-06, PD-25 | M27 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 83 |
| E21 | C6 | PD-06, PD-25 | M27 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 133 |
| E22 | C7 | PD-22 | none | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 7 |
| E23 | C8 | PD-24 | none | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 174 |
| E24 | C8 | PD-24 | none | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 308 |
| E25 | C8 | PD-24 | none | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 353 |
| E26 | C8 | PD-24 | none | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 383 |
| E27 | C8 | PD-24 | none | `11_Comparative_Research_Matrix.md` | 37 |
| E28 | C9 | PD-04 | M36 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 27 |
| E29 | C9 | PD-04 | M36 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 15 |
| E30 | C9 | PD-04 | M36 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 177 |
| E31 | A2 (copy of C9) | PD-04 | M36 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 120 |
| E32 | C10 | PD-01 | M41 | `41_F18_Fixture_Inputs/M41.json` | 33 |
| E33 | C10 | PD-01 | M42 | `41_F18_Fixture_Inputs/M42.json` | 16 |
| E34 | C10 | PD-01 | M42 | `41_F18_Fixture_Inputs/M42.json` | 23 |
| E35 | C10 | PD-01 | M47 | `41_F18_Fixture_Inputs/M47.json` | 16 |
| E36 | C10 | PD-01 | M47 | `41_F18_Fixture_Inputs/M47.json` | 23 |
| E37 | C10 | PD-01 | M47 | `41_F18_Fixture_Inputs/M47.json` | 24 |
| E38 | C11 | PD-26 | M42, M47 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 185 |
| E39 | A2 (copy of C11) | PD-26 | M42, M47 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 128 |
| E40 | C11 | PD-26 | M15 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 174 |
| E41 | A2 (copy of C11) | PD-26 | M15 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 117 |
| E42 | C13 | PD-02 (1), PD-03 | M14, M17 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 174 |
| E43 | A2 (copy of C13) | PD-02 (1), PD-03 | M14, M17 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 117 |
| E44 | C12 | PD-20 | M15 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 168 |
| E45 | A2 (copy of C12) | PD-20 | M15 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 111 |
| E46 | C13 | PD-03 | M14, M17 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 168 |
| E47 | A2 (copy of C13) | PD-03 | M14, M17 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 111 |
| E48 | C16 | PD-07 | R07 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 179 |
| E49 | A2 (copy of C16) | PD-07 | R07 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 122 |
| E50 | S | — | — | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | 1 |
| E51 | S | — | — | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | 4 |
| E52 | S | — | — | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | 9 |
| E53 | S | — | — | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | 184 |
| E54 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 1 |
| E55 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 4 |
| E56 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 9 |
| E57 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 81 |
| E58 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 81 |
| E59 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 83 |
| E60 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 187 |
| E61 | A2 (copy of S) | — | — | `25_Common_System_and_Repair_Prompt_Templates.txt` | 130 |
| E62 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 288 |
| E63 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 555 |
| E64 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 555 |
| E65 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 559 |
| E66 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 1 |
| E67 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 3 |
| E68 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 3 |
| E69 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 3 |
| E70 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 3 |
| E71 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 3 |
| E72 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 63 |
| E73 | S | — | — | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 1 |
| E74 | S | — | — | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 109 |
| E75 | S | — | — | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` | 1 |
| E76 | S | — | — | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` | 17 |
| E77 | S | — | — | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` | 84 |
| E78 | S | — | — | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` | 84 |
| E79 | S | — | — | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | 1 |
| E80 | S | — | — | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | 3 |
| E81 | S | — | — | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | 5 |
| E82 | S | — | — | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | 48 |
| E83 | S | — | — | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` (was `33_Prompt_Assembly_Sidecar_v1.3.6.json` | 2 |
| E84 | S | — | — | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` (was `33_Prompt_Assembly_Sidecar_v1.3.6.json` | 189 |
| E85 | S | — | — | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 1 |
| E86 | S | — | — | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` (was `38_Authoring_Packet_Manifest_Template_v1.3.6.json` | 71 |
| E87 | S | — | — | `README.md` | 1 |
| E88 | S | — | — | `README.md` | 3 |
| E89 | S | — | — | `README.md` | 7 |
| E90 | S | — | — | `README.md` | 8 |
| E91 | S | — | — | `README.md` | 11 |
| E92 | S | — | — | `README.md` | 13 |
| E93 | S | — | — | `README.md` | 14 |
| E94 | S | — | — | `README.md` | 14 |
| E95 | S | — | — | `README.md` | 16 |
| E96 | S | — | — | `README.md` | 17 |
| E97 | S | — | — | `README.md` | 9 |
| E98 | S | — | — | `README.md` | 46 |
| E99 | label | — | M41 | `41_F18_Fixture_Inputs/M41.json` | 3 |
| E100 | label | — | M42 | `41_F18_Fixture_Inputs/M42.json` | 3 |
| E101 | label | — | M47 | `41_F18_Fixture_Inputs/M47.json` | 3 |
| E102 | C12–C16 | PD-07 | M13, M14, M15, M17, R07 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 190–199 |
| E103 | label | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 628 |
| E104 | label | — | — | `25_Common_System_and_Repair_Prompt_Templates.txt` | 132 |
| E105 | label | — | — | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 208 |
| E106 | label | — | — | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 110 |
| E107 | label | — | — | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 418 |
| E108 | label | — | — | `11_Comparative_Research_Matrix.md` | 44 |
| E109 | label | — | — | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | 195 |
| E110 | label | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 73 |
| E111 | label | — | — | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` | 98 |
| E112 | label | — | — | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | 55 |
| E113 | label | — | — | `README.md` | 49 |
| E114 | S | — | — | `22_Source_Access_Provenance_Log_v1.2.md` | 8 |
| E115 | S | — | — | `22_Source_Access_Provenance_Log_v1.2.md` | 9 |
| E116 | S | — | — | `22_Source_Access_Provenance_Log_v1.2.md` | 10 |
| E117 | S | — | — | `22_Source_Access_Provenance_Log_v1.2.md` | 11 |
| E118 | S | — | — | `22_Source_Access_Provenance_Log_v1.2.md` | 12 |
| E119 | label | — | — | `22_Source_Access_Provenance_Log_v1.2.md` | 47 |
| E120 | C6 + A1 | PD-06, PD-25 | M27 | `41_F18_Fixture_Inputs/M27.json` | all |
| E121 | derived | — | M27 | `41_F18_Fixture_Inputs/fixture-index.json` | 380 |
| E122 | derived | — | M27 | `41_F18_Fixture_Inputs/fixture-index.json` | 381 |
| E123 | derived | — | M41 | `41_F18_Fixture_Inputs/fixture-index.json` | 562 |
| E124 | derived | — | M41 | `41_F18_Fixture_Inputs/fixture-index.json` | 563 |
| E125 | derived | — | M42 | `41_F18_Fixture_Inputs/fixture-index.json` | 579 |
| E126 | derived | — | M42 | `41_F18_Fixture_Inputs/fixture-index.json` | 580 |
| E127 | derived | — | M47 | `41_F18_Fixture_Inputs/fixture-index.json` | 644 |
| E128 | derived | — | M47 | `41_F18_Fixture_Inputs/fixture-index.json` | 645 |
| E129 | label | — | — | `41_F18_Fixture_Inputs/fixture-index.json` | 2 |
| E130 | S | — | — | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | name |
| E131 | S | — | — | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | name |
| E132 | S | — | — | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | name |
| E133 | S | — | — | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | name |
| E134 | S | — | — | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` | name |
| E135 | S | — | — | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | name |
| E136 | S | — | — | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` (was `33_Prompt_Assembly_Sidecar_v1.3.6.json` | name |
| E137 | S | — | — | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | name |
| E138 | S | — | — | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` (was `38_Authoring_Packet_Manifest_Template_v1.3.6.json` | name |
| E139 | derived | — | — | `27_SHA256SUMS.txt` | 1 |
| E140 | derived | — | — | `27_SHA256SUMS.txt` | 2 |
| E141 | derived | — | — | `27_SHA256SUMS.txt` | 11 |
| E142 | derived | — | — | `27_SHA256SUMS.txt` | 12 |
| E143 | derived | — | — | `27_SHA256SUMS.txt` | 20 |
| E144 | derived | — | — | `27_SHA256SUMS.txt` | 21 |
| E145 | derived | — | — | `27_SHA256SUMS.txt` | 24 |
| E146 | derived | — | — | `27_SHA256SUMS.txt` | 28 |
| E147 | derived | — | — | `27_SHA256SUMS.txt` | 29 |
| E148 | derived | — | — | `27_SHA256SUMS.txt` | 30 |
| E149 | derived | — | — | `27_SHA256SUMS.txt` | 31 |
| E150 | derived | — | — | `27_SHA256SUMS.txt` | 34 |
| E151 | derived | — | — | `27_SHA256SUMS.txt` | 36 |
| E152 | derived | — | — | `27_SHA256SUMS.txt` | 66 |
| E153 | derived | — | — | `27_SHA256SUMS.txt` | 80 |
| E154 | derived | — | — | `27_SHA256SUMS.txt` | 81 |
| E155 | derived | — | — | `27_SHA256SUMS.txt` | 86 |
| E156 | derived | — | — | `27_SHA256SUMS.txt` | 182 |
| E157 | derived | — | — | `27_SHA256SUMS.txt` | 202 |
| E158 | OS-1–OS-3 (OWNER-SPECIFIED, D-026) | PD-07, PD-01, PD-03 | M41, M37, P17 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 200–207 |
| E159 | OD-1 | D1-5 | M15 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 174 |
| E160 | A2 (copy of OD-1) | D1-5 | M15 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 117 |
| E161 | OD-1 | D1-5 | M42, M47 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 185 |
| E162 | A2 (copy of OD-1) | D1-5 | M42, M47 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 128 |
| E163 | OD-2 | D1-3 | M27 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 83 |
| E164 | OD-2 | D1-3 | M27 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 83 |
| E165 | OD-2 | D1-3 | M27 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 83 |
| E166 | OD-3 | D1-1 | M54 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E167 | A2 (copy of OD-3) | D1-1 | M54 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E168 | OD-3 | D1-1 | M48, M50, M53, M54, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E169 | A2 (copy of OD-3) | D1-1 | M48, M50, M53, M54, M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E170 | OD-3 | D1-1 | M54, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E171 | A2 (copy of OD-3) | D1-1 | M54, M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E172 | OD-3 | D1-1 | M48, M50, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E173 | A2 (copy of OD-3) | D1-1 | M48, M50, M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E174 | OD-3 | D1-2 | M48, M50, M53, M54, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 176 |
| E175 | A2 (copy of OD-3) | D1-2 | M48, M50, M53, M54, M58 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 119 |
| E176 | OD-3 | D1-2 | M48, M50, M53, M54, M58 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 176 |
| E177 | OD-3 | D1-1 | M54 | `41_F18_Fixture_Inputs/M54.json` | 11 |
| E178 | OD-4 | D1-6 | M13, M41 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 185 |
| E179 | A2 (copy of OD-4) | D1-6 | M13, M41 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 128 |
| E180 | OD-4 | D1-6 | M13 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 198 |
| E181 | OD-4 | D1-6 | M41 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 205 |
| E182 | A3 | D1-7 | M41, M42, M47 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 185 |
| E183 | A2 (copy of A3) | D1-7 | M41, M42, M47 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 128 |
| E184 | A4 | D1-8 | M37 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 143 |
| E185 | A4 | D1-8 | M37 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 206 |
| E186 | A4 | D1-8 | M37 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 206 |
| E187 | A4 | D1-8 | M37 | `41_F18_Fixture_Inputs/M37.json` | 5 |
| E188 | C17 | D1-9 | all | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 3 |
| E189 | C17 | D1-9 | all | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` | 176 |
| E190 | C17 | D1-9 | all | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | 21 |
| E191 | C17 | D1-9 | all | `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` | 33 |
| E192 | C17 | D1-9 | all | `README.md` | 16 |
| E193 | C17 | D1-9 | all | `README.md` | 35 |
| E194 | C17 | D1-9 | all | `README.md` | 46 |
| E195 | C17 | D1-9 | all | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 559 |
| E196 | label | — | M54 | `41_F18_Fixture_Inputs/M54.json` | 3 |
| E197 | label | — | M37 | `41_F18_Fixture_Inputs/M37.json` | 3 |
| E198 | OD-3 | D1-1, D1-2 | M48, M50, M53, M54, M58 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` | 560–627 |
| E199 | OD-2 | D1-3, D1-4 | M27 | `41_F18_Fixture_Inputs/M27.json` | all |
| E200 | derived | — | M37 | `41_F18_Fixture_Inputs/fixture-index.json` | 510 |
| E201 | derived | — | M37 | `41_F18_Fixture_Inputs/fixture-index.json` | 511 |
| E202 | derived | — | M54 | `41_F18_Fixture_Inputs/fixture-index.json` | 752 |
| E203 | derived | — | M54 | `41_F18_Fixture_Inputs/fixture-index.json` | 753 |
| E204 | derived | — | — | `27_SHA256SUMS.txt` | 76 |
| E205 | derived | — | — | `27_SHA256SUMS.txt` | 93 |
| E206 | C18 | D2-1 | all | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 7 |
| E207 | C18 | D2-1 | all | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 26 |
| E208 | C18 | D2-1 | all | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 40 |
| E209 | C18 | D2-1 | all | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 52 |
| E210 | C18 | D2-1 | all | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 69 |
| E211 | C18 | D2-1 | all | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` | 70 |
| E212 | C18 | D2-1 | all | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | 177 |
| E213 | C18 | D2-1 | all | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` | 194 |
| E214 | C18 | D2-1 | all | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` | 3 |
| E215 | C18 | D2-1 | all | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` | 3 |
| E216 | C18 | D2-1 | — | `README.md` | 19 |
| E217 | C18 | D2-1 | all | `41_F18_Fixture_Inputs/fixture-index.json` | 4 |
| E218 | C18 | D2-1 | all | `41_F18_Fixture_Inputs/fixture-index.json` | 1931 |

## E01 — C1 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L175 · PD-02 (2) · fixtures: M48, M50, M53, M54, M58

Old:

```text
The `M53` study-reset vector uses error class `AUTHORING_REVISION_REQUIRED` and diagnostic `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED`; `M54` uses error class `HALT_SIGNATURE_SCHEMA` and diagnostic `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED`.
```

New:

```text
Error classes of change-class control expectations are stated by rule, not by fixture: a control expectation whose diagnostic CODE is `EVALUATOR_REVISION_REQUIRED` has error class `EVALUATOR_REVISION_REQUIRED`; one whose CODE is `AUTHORING_REVISION_REQUIRED` has error class `AUTHORING_REVISION_REQUIRED`; and one whose CODE is `HALT_SIGNATURE_SCHEMA` has error class `HALT_SIGNATURE_SCHEMA`. This rule applies only to these three codes; it does not change the M41 error class `MID_RUN_REEVALUATION` or any stage-map row. The study-reset vector uses diagnostic `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED`; the halt-signature vector uses diagnostic `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED`.
```

## E02 — A2 (copy of C1) · `25_Common_System_and_Repair_Prompt_Templates.txt` L118 · PD-02 (2) · fixtures: M48, M50, M53, M54, M58

Old:

```text
The `M53` study-reset vector uses error class `AUTHORING_REVISION_REQUIRED` and diagnostic `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED`; `M54` uses error class `HALT_SIGNATURE_SCHEMA` and diagnostic `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED`.
```

New:

```text
Error classes of change-class control expectations are stated by rule, not by fixture: a control expectation whose diagnostic CODE is `EVALUATOR_REVISION_REQUIRED` has error class `EVALUATOR_REVISION_REQUIRED`; one whose CODE is `AUTHORING_REVISION_REQUIRED` has error class `AUTHORING_REVISION_REQUIRED`; and one whose CODE is `HALT_SIGNATURE_SCHEMA` has error class `HALT_SIGNATURE_SCHEMA`. This rule applies only to these three codes; it does not change the M41 error class `MID_RUN_REEVALUATION` or any stage-map row. The study-reset vector uses diagnostic `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED`; the halt-signature vector uses diagnostic `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED`.
```

## E03 — C2 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · PD-02 (1) · fixtures: M48, M50, M53, M54, M58

Old:

```text
**Closed `required_action` literals used by lifecycle fixtures:** `M48` = `
```

New:

```text
**Closed `required_action` literals, by change class:** `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` = `
```

## E04 — A2 (copy of C2) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · PD-02 (1) · fixtures: M48, M50, M53, M54, M58

Old:

```text
**Closed `required_action` literals used by lifecycle fixtures:** `M48` = `
```

New:

```text
**Closed `required_action` literals, by change class:** `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` = `
```

## E05 — C2 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · PD-02 (1) · fixtures: M50

Old:

```text
`; `M50` = `
```

New:

```text
`; `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` = `
```

## E06 — A2 (copy of C2) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · PD-02 (1) · fixtures: M50

Old:

```text
`; `M50` = `
```

New:

```text
`; `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` = `
```

## E07 — C2 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · PD-02 (1) · fixtures: M53

Old:

```text
`; `M53` = `
```

New:

```text
`; `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` = `
```

## E08 — A2 (copy of C2) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · PD-02 (1) · fixtures: M53

Old:

```text
`; `M53` = `
```

New:

```text
`; `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` = `
```

## E09 — C2 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · PD-02 (1) · fixtures: M54

Old:

```text
`; `M54` = `
```

New:

```text
`; `HALT_SIGNATURE_COMPONENT_ENUMERATION` = `
```

## E10 — A2 (copy of C2) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · PD-02 (1) · fixtures: M54

Old:

```text
`; `M54` = `
```

New:

```text
`; `HALT_SIGNATURE_COMPONENT_ENUMERATION` = `
```

## E11 — C2 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · PD-02 (1) · fixtures: M58

Old:

```text
`; and `M58` = `
```

New:

```text
`; and `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` = `
```

## E12 — A2 (copy of C2) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · PD-02 (1) · fixtures: M58

Old:

```text
`; and `M58` = `
```

New:

```text
`; and `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` = `
```

## E13 — C2 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · PD-02 (1), (3) · fixtures: M48, M50, M53, M54, M58

Old:

```text
Each literal is a closed local control expectation, not a model-feedback diagnostic. `M48` re-evaluates the affected scope with the same frozen artifact bytes and zero new confirmatory generation calls. `M50` invalidates all designs and all arm × design slots and starts a new preregistered study. `M53` resets the preregistered design set and weights and requires fresh confirmatory slots. `M58` invalidates both arms for the affected design only when membership, estimand and weights remain unchanged.
```

New:

```text
Each literal is a closed local control expectation, not a model-feedback diagnostic. The change classes are closed and have these cases: `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` is the evaluator revision of §7b path (b); `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` is a shared-item revision; `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` is a study reset; `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` is a design-specific revision while membership, estimand and weights remain unchanged; and `HALT_SIGNATURE_COMPONENT_ENUMERATION` is the halt-signature domain check. Closed scope tokens: for an evaluator revision, `rerun_scope_rule` = `shared_evaluator_component_all_designs_and_all_arm_x_design_slots; design_specific_component_affected_design_in_both_arms` (§7b: shared component, both designs and every slot; design-specific component, that design in both arms). For a shared-item revision, `affected_slots` = `all_designs_x_all_arms` (§7b: every scheduled slot across both designs and both arms). For a design-specific revision, `affected_scope` = `affected_design_in_both_arms` and `unaffected_design_scope` = `not_invalidated_when_membership_estimand_and_weights_are_unchanged`. An evaluator revision re-evaluates the affected scope with the same frozen artifact bytes and zero new confirmatory generation calls. A shared-item revision invalidates all designs and all arm × design slots and starts a new preregistered study. A study reset resets the preregistered design set and weights and requires fresh confirmatory slots. A design-specific revision invalidates both arms for the affected design only when membership, estimand and weights remain unchanged.
```

## E14 — A2 (copy of C2) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · PD-02 (1), (3) · fixtures: M48, M50, M53, M54, M58

Old:

```text
Each literal is a closed local control expectation, not a model-feedback diagnostic. `M48` re-evaluates the affected scope with the same frozen artifact bytes and zero new confirmatory generation calls. `M50` invalidates all designs and all arm × design slots and starts a new preregistered study. `M53` resets the preregistered design set and weights and requires fresh confirmatory slots. `M58` invalidates both arms for the affected design only when membership, estimand and weights remain unchanged.
```

New:

```text
Each literal is a closed local control expectation, not a model-feedback diagnostic. The change classes are closed and have these cases: `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` is the evaluator revision of §7b path (b); `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` is a shared-item revision; `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` is a study reset; `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` is a design-specific revision while membership, estimand and weights remain unchanged; and `HALT_SIGNATURE_COMPONENT_ENUMERATION` is the halt-signature domain check. Closed scope tokens: for an evaluator revision, `rerun_scope_rule` = `shared_evaluator_component_all_designs_and_all_arm_x_design_slots; design_specific_component_affected_design_in_both_arms` (§7b: shared component, both designs and every slot; design-specific component, that design in both arms). For a shared-item revision, `affected_slots` = `all_designs_x_all_arms` (§7b: every scheduled slot across both designs and both arms). For a design-specific revision, `affected_scope` = `affected_design_in_both_arms` and `unaffected_design_scope` = `not_invalidated_when_membership_estimand_and_weights_are_unchanged`. An evaluator revision re-evaluates the affected scope with the same frozen artifact bytes and zero new confirmatory generation calls. A shared-item revision invalidates all designs and all arm × design slots and starts a new preregistered study. A study reset resets the preregistered design set and weights and requires fresh confirmatory slots. A design-specific revision invalidates both arms for the affected design only when membership, estimand and weights remain unchanged.
```

## E15 — C3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L185 · PD-02 (3) · fixtures: M54

Old:

```text
for `SIMULATOR_ERROR` and the literal `NONE` for the other two halt codes; `stable_diagnostic_code` is exactly the corresponding `halt_code` token.
```

New:

```text
for `SIMULATOR_ERROR` and the literal `NONE` for the other two halt codes (rule token `stable_error_class_rule` = `simple_exception_class_for_SIMULATOR_ERROR_else_NONE`); `stable_diagnostic_code` is exactly the corresponding `halt_code` token (rule token `stable_diagnostic_code_rule` = `exact_halt_code_token`).
```

## E16 — A2 (copy of C3) · `25_Common_System_and_Repair_Prompt_Templates.txt` L128 · PD-02 (3) · fixtures: M54

Old:

```text
for `SIMULATOR_ERROR` and the literal `NONE` for the other two halt codes; `stable_diagnostic_code` is exactly the corresponding `halt_code` token.
```

New:

```text
for `SIMULATOR_ERROR` and the literal `NONE` for the other two halt codes (rule token `stable_error_class_rule` = `simple_exception_class_for_SIMULATOR_ERROR_else_NONE`); `stable_diagnostic_code` is exactly the corresponding `halt_code` token (rule token `stable_diagnostic_code_rule` = `exact_halt_code_token`).
```

## E17 — C10 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L185 · PD-01 · fixtures: M41, M42, M47

Old:

```text
(rule token `stable_diagnostic_code_rule` = `exact_halt_code_token`).
```

New:

```text
(rule token `stable_diagnostic_code_rule` = `exact_halt_code_token`). A supplied halt signature with any component outside these domains is an evaluator input error; it is never compared for recurrence.
```

## E18 — A2 (copy of C10) · `25_Common_System_and_Repair_Prompt_Templates.txt` L128 · PD-01 · fixtures: M41, M42, M47

Old:

```text
(rule token `stable_diagnostic_code_rule` = `exact_halt_code_token`).
```

New:

```text
(rule token `stable_diagnostic_code_rule` = `exact_halt_code_token`). A supplied halt signature with any component outside these domains is an evaluator input error; it is never compared for recurrence.
```

## E19 — C4 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L176 · PD-03 · fixtures: M14, M17, M41, M48, M50, M53, M54, M58

Old:

```text
compares actual disposition, stage, error class and exact diagnostic bytes with the expected object.
```

New:

```text
compares the actual result with the expected object. When the expected object has exactly the keys `disposition`, `stage_id`, `error_class` and `diagnostic`, those four values are compared exactly. Any other expected object is a control-vector expectation: its whole object is compared exactly, key set included, and every property it names must be defined by a rule in the Protocol.
```

## E20 — C5 · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L83 · PD-06, PD-25 · fixtures: M27

Old:

```text
(e) the full vector satisfies the design-specific legal-input predicate from the author-visible reset/legal-input specification.
```

New:

```text
(e) the full vector satisfies the design-specific legal-input predicate from the author-visible reset/legal-input specification. The predicate is frozen as one Python 3.11 function of two dictionaries, `(vector, sampled)`: the driver vector, and the outputs sampled in the same row, each mapping a port name to its bit string. It returns the exact Boolean `True` for a legal vector and `False` otherwise. Any other outcome, including an exception, is an evaluator failure and is never an artifact verdict. Within check (a), missing keys are reported before extra keys. Checks (a) to (e) run in that order and the first failure is reported. A fixture that exercises check (e) supplies the input properties `driver_return` (the vector), `input_port_widths` (each input port name mapped to its width), `sampled_outputs` (the outputs sampled in the same row) and `legal_input_predicate` (an object with `language` = `python3.11`, `function`, the function's name, and `source`, its Python source).
```

## E21 — C6 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L133 · PD-06, PD-25 · fixtures: M27

Old:

```text
| M27 | missing-case | Driver vector violates a design-specific legal-input predicate |
```

New:

```text
| M27 | missing-case | Driver vector passes the key, type, width and symbol checks and violates the supplied legal-input predicate |
```

## E22 — C7 · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L7 · PD-22 · fixtures: none

Old:

```text
is independent of planning-pack version `1.3.1`.
```

New:

```text
is independent of the planning-pack version.
```

## E23 — C8 · `10_LLM_Era_Hardware_Verification_Literature_Review.md` L174 · PD-24 · fixtures: none

Old:

```text
**Reported proof of concept.** It evaluates a round-robin arbiter and synchronous FIFO (150–350 LOC), with 12 total test cases. It reports 10/12 tests detecting targeted gaps, zero false positives on the golden design, and an approximately 80-second detection cycle. The paper itself says this sample is too small for strong statistical confidence and treats it as a feasibility demonstration (Section VII-D). It also identifies one LLM model, manual mutation injection, small single-module designs, and UVM-specific scope as limitations (Section VII-E). The preprint is not peer reviewed.
```

New:

```text
**Reported proof of concept (unverified).** An earlier draft attributed a synchronous-FIFO case and numerical results to this preprint. Those details are not verified from its text (abstract-only access, File 22) and are not relied upon. The preprint is not peer reviewed.
```

## E24 — C8 · `10_LLM_Era_Hardware_Verification_Literature_Review.md` L308 · PD-24 · fixtures: none

Old:

```text
- The TechRxiv preprint reports 10/12 targeted gap detections on two small UVM IPs; it is a proof of concept, not a broad benchmark.
```

New:

```text
- The TechRxiv preprint is an unreviewed proof of concept; its numerical results and designs are not verified from its text (File 22) and are not relied upon.
```

## E25 — C8 · `10_LLM_Era_Hardware_Verification_Literature_Review.md` L353 · PD-24 · fixtures: none

Old:

```text
the TechRxiv checker-gap preprint also evaluates a synchronous FIFO;
```

New:

```text
whether the TechRxiv checker-gap preprint also evaluates a synchronous FIFO is not verified (File 22);
```

## E26 — C8 · `10_LLM_Era_Hardware_Verification_Literature_Review.md` L383 · PD-24 · fixtures: none

Old:

```text
| Extracted TechRxiv PDF text, including Definitions and experimental limitations (Sections II-A, III, IV–V, VII-D/VII-E); page-image screenshot fetch failed (502) | Moderate for method and declared limitations; checker-dependent definition of output observability; unreviewed preprint, two designs, 12 cases; treat cautiously but disclose as prior art |
```

New:

```text
| Abstract only, per File 22; the earlier statement that extracted full text was read is superseded | Low for method and limitations until the exact PDF is retrieved and inspected; unreviewed preprint; disclose as prior art |
```

## E27 — C8 · `11_Comparative_Research_Matrix.md` L37 · PD-24 · fixtures: none

Old:

```text
- TechRxiv checker-gap paper: full extracted text was read; PDF page images were not inspected; the paper's automated/manual injection descriptions conflict.
```

New:

```text
- TechRxiv checker-gap paper: abstract-only access is recorded (File 22); full-text and injection-method claims are not verified.
```

## E28 — C9 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L27 · PD-04 · fixtures: M36

Old:

```text
Serializer unit vectors and lifecycle unit vectors are marked by `fixture_class` and are deliberately grammar-exempt; they test local utilities/policies, not model feedback.
```

New:

```text
Serializer, lifecycle and parser unit vectors are marked by `fixture_class` (`serializer_primitive_unit_vector_grammar_exempt`, `lifecycle_unit_vector`, `parser_unit_vector`) and are deliberately grammar-exempt; they test local utilities/policies, not model feedback. A `parser_unit_vector` input has exactly the keys `source_file` and `syntax_error`. `source_file` is `driver.py` or `checker.py`. `syntax_error` has the key `lineno`, a positive integer, and may have the key `offset`, an integer or null. The vector applies the Protocol §3.4 `SOURCE_SYNTAX_REJECT` column rule to that position. Its result has stage `SOURCE_AST`, error class `SOURCE_SYNTAX_REJECT`, the diagnostic given by the rule, and disposition `CONTROL_EXPECTATION`.
```

## E29 — C9 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L15 · PD-04 · fixtures: M36

Old:

```text
- `CONTROL_EXPECTATION`: a serializer, lifecycle or policy test vector;
```

New:

```text
- `CONTROL_EXPECTATION`: a serializer, parser, protocol or lifecycle test vector;
```

## E30 — C9 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L177 · PD-04 · fixtures: M36

Old:

```text
exercises a serializer, protocol or lifecycle rule;
```

New:

```text
exercises a serializer, parser, protocol or lifecycle rule;
```

## E31 — A2 (copy of C9) · `25_Common_System_and_Repair_Prompt_Templates.txt` L120 · PD-04 · fixtures: M36

Old:

```text
exercises a serializer, protocol or lifecycle rule;
```

New:

```text
exercises a serializer, parser, protocol or lifecycle rule;
```

## E32 — C10 · `41_F18_Fixture_Inputs/M41.json` L33 · PD-01 · fixtures: M41

Old:

```text
"evaluator_component": "simulator",
```

New:

```text
"evaluator_component": "SIMULATOR",
```

## E33 — C10 · `41_F18_Fixture_Inputs/M42.json` L16 · PD-01 · fixtures: M42

Old:

```text
"evaluator_component": "simulator",
```

New:

```text
"evaluator_component": "SIMULATOR",
```

## E34 — C10 · `41_F18_Fixture_Inputs/M42.json` L23 · PD-01 · fixtures: M42

Old:

```text
"evaluator_component": "simulator",
```

New:

```text
"evaluator_component": "SIMULATOR",
```

## E35 — C10 · `41_F18_Fixture_Inputs/M47.json` L16 · PD-01 · fixtures: M47

Old:

```text
"evaluator_component": "simulator",
```

New:

```text
"evaluator_component": "SIMULATOR",
```

## E36 — C10 · `41_F18_Fixture_Inputs/M47.json` L23 · PD-01 · fixtures: M47

Old:

```text
"evaluator_component": "recorder",
```

New:

```text
"evaluator_component": "RECORDER",
```

## E37 — C10 · `41_F18_Fixture_Inputs/M47.json` L24 · PD-01 · fixtures: M47

Old:

```text
"stable_error_class": "RecorderFault",
```

New:

```text
"stable_error_class": "NONE",
```

## E38 — C11 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L185 · PD-26 · fixtures: M42, M47

Old:

```text
terminate with `DESIGN_HALT_REPEATED|reason=SECOND_HALT_AFTER_RECOVERY`.
```

New:

```text
terminate with `DESIGN_HALT_REPEATED|reason=SECOND_HALT_AFTER_RECOVERY`. Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED`.
```

## E39 — A2 (copy of C11) · `25_Common_System_and_Repair_Prompt_Templates.txt` L128 · PD-26 · fixtures: M42, M47

Old:

```text
terminate with `DESIGN_HALT_REPEATED|reason=SECOND_HALT_AFTER_RECOVERY`.
```

New:

```text
terminate with `DESIGN_HALT_REPEATED|reason=SECOND_HALT_AFTER_RECOVERY`. Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED`.
```

## E40 — C11 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L174 · PD-26 · fixtures: M15

Old:

```text
The M17 JSON-escaping primitive uses error class `JSON_SERIALIZATION`.
```

New:

```text
The M17 JSON-escaping primitive uses error class `JSON_SERIALIZATION`. `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`.
```

## E41 — A2 (copy of C11) · `25_Common_System_and_Repair_Prompt_Templates.txt` L117 · PD-26 · fixtures: M15

Old:

```text
The M17 JSON-escaping primitive uses error class `JSON_SERIALIZATION`.
```

New:

```text
The M17 JSON-escaping primitive uses error class `JSON_SERIALIZATION`. `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`.
```

## E42 — C13 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L174 · PD-02 (1), PD-03 · fixtures: M14, M17

Old:

```text
The M14 truncation primitive uses error class `TRUNCATION`. The M17 JSON-escaping primitive uses error class `JSON_SERIALIZATION`.
```

New:

```text
A truncation-primitive vector uses error class `TRUNCATION` and a JSON-escaping-primitive vector uses error class `JSON_SERIALIZATION`; both are recorded at stage `FEEDBACK_SERIALIZER` with disposition `CONTROL_EXPECTATION`.
```

## E43 — A2 (copy of C13) · `25_Common_System_and_Repair_Prompt_Templates.txt` L117 · PD-02 (1), PD-03 · fixtures: M14, M17

Old:

```text
The M14 truncation primitive uses error class `TRUNCATION`. The M17 JSON-escaping primitive uses error class `JSON_SERIALIZATION`.
```

New:

```text
A truncation-primitive vector uses error class `TRUNCATION` and a JSON-escaping-primitive vector uses error class `JSON_SERIALIZATION`; both are recorded at stage `FEEDBACK_SERIALIZER` with disposition `CONTROL_EXPECTATION`.
```

## E44 — C12 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L168 · PD-20 · fixtures: M15

Old:

```text
a path-bearing or otherwise non-normative diagnostic fails the closed-grammar check and is not sent.
```

New:

```text
a path-bearing or otherwise non-normative diagnostic fails the closed-grammar check and is not sent. When the set of diagnostics the stage map emitted is given, a diagnostic that passes the grammar but is not in that set is also rejected at step (1), with the same `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC`.
```

## E45 — A2 (copy of C12) · `25_Common_System_and_Repair_Prompt_Templates.txt` L111 · PD-20 · fixtures: M15

Old:

```text
a path-bearing or otherwise non-normative diagnostic fails the closed-grammar check and is not sent.
```

New:

```text
a path-bearing or otherwise non-normative diagnostic fails the closed-grammar check and is not sent. When the set of diagnostics the stage map emitted is given, a diagnostic that passes the grammar but is not in that set is also rejected at step (1), with the same `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC`.
```

## E46 — C13 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L168 · PD-03 · fixtures: M14, M17

Old:

```text
No raw exception text, validator/compiler message, file path, trace/output value or arbitrary free-form content is sent to the model.
```

New:

```text
No raw exception text, validator/compiler message, file path, trace/output value or arbitrary free-form content is sent to the model. A truncation-primitive vector applies step (2) alone to its input string and reports `contains_marker` (whether the output ends with the marker), `valid_utf8` (whether the output bytes are valid UTF-8), `output_diagnostic_bytes` (the output's UTF-8 byte length) and `marker_utf8_bytes` (the marker's UTF-8 byte length). A JSON-escaping-primitive vector applies step (3) alone to its three-key object and reports `diagnostic_utf8` (the serialized text), `diagnostic_sha256` (the lowercase hexadecimal SHA-256 of its UTF-8 bytes) and `diagnostic_bytes` (their number).
```

## E47 — A2 (copy of C13) · `25_Common_System_and_Repair_Prompt_Templates.txt` L111 · PD-03 · fixtures: M14, M17

Old:

```text
No raw exception text, validator/compiler message, file path, trace/output value or arbitrary free-form content is sent to the model.
```

New:

```text
No raw exception text, validator/compiler message, file path, trace/output value or arbitrary free-form content is sent to the model. A truncation-primitive vector applies step (2) alone to its input string and reports `contains_marker` (whether the output ends with the marker), `valid_utf8` (whether the output bytes are valid UTF-8), `output_diagnostic_bytes` (the output's UTF-8 byte length) and `marker_utf8_bytes` (the marker's UTF-8 byte length). A JSON-escaping-primitive vector applies step (3) alone to its three-key object and reports `diagnostic_utf8` (the serialized text), `diagnostic_sha256` (the lowercase hexadecimal SHA-256 of its UTF-8 bytes) and `diagnostic_bytes` (their number).
```

## E48 — C16 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L179 · PD-07 · fixtures: R07

Old:

```text
Any baseline mismatch halts the design before slots exist; no slot is scored.
```

New:

```text
Any baseline mismatch halts the design before slots exist; no slot is scored. It is recorded at stage `DESIGN_HALT` with error class `RTL_NULL_CONTROL_FAILURE`, diagnostic `RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE` and disposition `DESIGN_HALT_NO_SLOT_SCORED`.
```

## E49 — A2 (copy of C16) · `25_Common_System_and_Repair_Prompt_Templates.txt` L122 · PD-07 · fixtures: R07

Old:

```text
Any baseline mismatch halts the design before slots exist; no slot is scored.
```

New:

```text
Any baseline mismatch halts the design before slots exist; no slot is scored. It is recorded at stage `DESIGN_HALT` with error class `RTL_NULL_CONTROL_FAILURE`, diagnostic `RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE` and disposition `DESIGN_HALT_NO_SLOT_SCORED`.
```

## E50 — S · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` L1 · — · fixtures: —

Old:

```text
# OpenVEF Project Charter v1.3.6
```

New:

```text
# OpenVEF Project Charter v1.3.7-candidate
```

## E51 — S · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` L4 · — · fixtures: —

Old:

```text
**Version:** 1.3.6 (
```

New:

```text
**Version:** 1.3.7-candidate (OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md`; not audited; not frozen; not approved). Based on: 1.3.6 (
```

## E52 — S · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` L9 · — · fixtures: —

Old:

```text
independent v1.3.6 document re-audit is pending.
```

New:

```text
independent v1.3.6 document re-audit is pending. The v1.3.7-candidate pack is not audited.
```

## E53 — S · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` L184 · — · fixtures: —

Old:

```text
`02_OpenVEF_Experimental_Protocol_v1.3.6.md`
```

New:

```text
`02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md`
```

## E54 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L1 · — · fixtures: —

Old:

```text
# OpenVEF Experimental Protocol v1.3.6
```

New:

```text
# OpenVEF Experimental Protocol v1.3.7-candidate
```

## E55 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L4 · — · fixtures: —

Old:

```text
**Version:** 1.3.6 (
```

New:

```text
**Version:** 1.3.7-candidate (OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md`; not audited; not frozen; not approved). Based on: 1.3.6 (
```

## E56 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L9 · — · fixtures: —

Old:

```text
current v1.3.6 re-audit-pending status are recorded in §19.
```

New:

```text
v1.3.6 re-audit-pending status, and the not-audited v1.3.7-candidate status, are recorded in §19.
```

## E57 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L81 · — · fixtures: —

Old:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.6.md`
```

New:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md`
```

## E58 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L81 · — · fixtures: —

Old:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md`
```

New:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md`
```

## E59 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L83 · — · fixtures: —

Old:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md`
```

New:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md`
```

## E60 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L187 · — · fixtures: —

Old:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md`
```

New:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md`
```

## E61 — A2 (copy of S) · `25_Common_System_and_Repair_Prompt_Templates.txt` L130 · — · fixtures: —

Old:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md`
```

New:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md`
```

## E62 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L288 · — · fixtures: —

Old:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.6.md`
```

New:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md`
```

## E63 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L555 · — · fixtures: —

Old:

```text
(1) Complete the v1.3.6 corrective document pack
```

New:

```text
(1) Complete the v1.3.7-candidate document pack
```

## E64 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L555 · — · fixtures: —

Old:

```text
(2) Obtain an independent document-only v1.3.6 re-audit
```

New:

```text
(2) Obtain an independent document-only v1.3.7-candidate audit
```

## E65 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L559 · — · fixtures: —

Old:

```text
v1.3.6 is a corrective evidence/metadata release
```

New:

```text
v1.3.7-candidate is OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md`; it is not audited, frozen or approved, and v1.3.6 remains the default pack. v1.3.6 is a corrective evidence/metadata release
```

## E66 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L1 · — · fixtures: —

Old:

```text
Checklist (F18) v1.3.6
```

New:

```text
Checklist (F18) v1.3.7-candidate
```

## E67 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L3 · — · fixtures: —

Old:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.6.md`
```

New:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md`
```

## E68 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L3 · — · fixtures: —

Old:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md`
```

New:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md`
```

## E69 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L3 · — · fixtures: —

Old:

```text
`33_Prompt_Assembly_Sidecar_v1.3.6.json`
```

New:

```text
`33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json`
```

## E70 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L3 · — · fixtures: —

Old:

```text
`38_Authoring_Packet_Manifest_Template_v1.3.6.json`
```

New:

```text
`38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json`
```

## E71 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L3 · — · fixtures: —

Old:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md`
```

New:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md`
```

## E72 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L63 · — · fixtures: —

Old:

```text
Protocol §3.4 and Catalog v1.3.6;
```

New:

```text
Protocol §3.4 and Catalog v1.3.7-candidate;
```

## E73 — S · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L1 · — · fixtures: —

Old:

```text
# OpenVEF Response Parser and Execution Contract v1.3.6
```

New:

```text
# OpenVEF Response Parser and Execution Contract v1.3.7-candidate
```

## E74 — S · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L109 · — · fixtures: —

Old:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md`
```

New:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md`
```

## E75 — S · `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` L1 · — · fixtures: —

Old:

```text
Canonicalization Specification v1.3.6
```

New:

```text
Canonicalization Specification v1.3.7-candidate
```

## E76 — S · `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` L17 · — · fixtures: —

Old:

```text
`33_Prompt_Assembly_Sidecar_v1.3.6.json`
```

New:

```text
`33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json`
```

## E77 — S · `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` L84 · — · fixtures: —

Old:

```text
after all v1.3.6 document and model-visible text edits are complete. This v1.3.6 release
```

New:

```text
after all v1.3.7-candidate document and model-visible text edits are complete. This v1.3.7-candidate release
```

## E78 — S · `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` L84 · — · fixtures: —

Old:

```text
retain their exact values in the v1.3.6 sidecar
```

New:

```text
retain their exact values in the v1.3.7-candidate sidecar
```

## E79 — S · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` L1 · — · fixtures: —

Old:

```text
# OpenVEF v1.3.6 Status and Gates
```

New:

```text
# OpenVEF v1.3.7-candidate Status and Gates
```

## E80 — S · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` L3 · — · fixtures: —

Old:

```text
**Current release:** v1.3.6 corrective evidence/metadata pack.
```

New:

```text
**Current release:** v1.3.7-candidate (the v1.3.6 corrective evidence/metadata pack with the corrections in `CHANGELOG-v1.3.7-candidate.md`; not audited, not frozen, not approved; v1.3.6 remains the default).
```

## E81 — S · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` L5 · — · fixtures: —

Old:

```text
**Current document audit status:** PENDING INDEPENDENT RE-AUDIT.
```

New:

```text
**Current document audit status:** v1.3.7-candidate NOT AUDITED; v1.3.6 PENDING INDEPENDENT RE-AUDIT.
```

## E82 — S · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` L48 · — · fixtures: —

Old:

```text
1. Independent document-only audit of the actual v1.3.6 pack.
```

New:

```text
1. Independent document-only audit of the actual v1.3.7-candidate pack.
```

## E83 — S · `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` (was `33_Prompt_Assembly_Sidecar_v1.3.6.json` L2 · — · fixtures: —

Old:

```text
"sidecar_version": "1.3.6",
```

New:

```text
"sidecar_version": "1.3.7-candidate, not audited",
```

## E84 — S · `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` (was `33_Prompt_Assembly_Sidecar_v1.3.6.json` L189 · — · fixtures: —

Old:

```text
"payload_manifest_file": "38_Authoring_Packet_Manifest_Template_v1.3.6.json",
```

New:

```text
"payload_manifest_file": "38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json",
```

## E85 — S · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L1 · — · fixtures: —

Old:

```text
Missing-Case Fixture Catalog v1.3.6
```

New:

```text
Missing-Case Fixture Catalog v1.3.7-candidate
```

## E86 — S · `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` (was `38_Authoring_Packet_Manifest_Template_v1.3.6.json` L71 · — · fixtures: —

Old:

```text
"Planning-pack v1.3.6 corrective evidence/metadata release.
```

New:

```text
"Planning-pack v1.3.7-candidate (v1.3.6 corrective evidence/metadata release with the corrections in CHANGELOG-v1.3.7-candidate.md; not audited).
```

## E87 — S · `README.md` L1 · — · fixtures: —

Old:

```text
# OpenVEF Planning Pack v1.3.6
```

New:

```text
# OpenVEF Planning Pack v1.3.7-candidate
```

## E88 — S · `README.md` L3 · — · fixtures: —

Old:

```text
**Status:** Corrective evidence/metadata release
```

New:

```text
**Status:** v1.3.7 CANDIDATE, not audited: OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md` (`CANDIDATE-LABEL.md` lists every file); v1.3.6 remains the default. v1.3.6 status: Corrective evidence/metadata release
```

## E89 — S · `README.md` L7 · — · fixtures: —

Old:

```text
`01_OpenVEF_Project_Charter_v1.3.6.md`
```

New:

```text
`01_OpenVEF_Project_Charter_v1.3.7-candidate.md`
```

## E90 — S · `README.md` L8 · — · fixtures: —

Old:

```text
`02_OpenVEF_Experimental_Protocol_v1.3.6.md`
```

New:

```text
`02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md`
```

## E91 — S · `README.md` L11 · — · fixtures: —

Old:

```text
`21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md`
```

New:

```text
`21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md`
```

## E92 — S · `README.md` L13 · — · fixtures: —

Old:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.6.md`
```

New:

```text
`30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md`
```

## E93 — S · `README.md` L14 · — · fixtures: —

Old:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md`
```

New:

```text
`31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md`
```

## E94 — S · `README.md` L14 · — · fixtures: —

Old:

```text
`33_Prompt_Assembly_Sidecar_v1.3.6.json`
```

New:

```text
`33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json`
```

## E95 — S · `README.md` L16 · — · fixtures: —

Old:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md`
```

New:

```text
`36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md`
```

## E96 — S · `README.md` L17 · — · fixtures: —

Old:

```text
`38_Authoring_Packet_Manifest_Template_v1.3.6.json`
```

New:

```text
`38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json`
```

## E97 — S · `README.md` L9 · — · fixtures: —

Old:

```text
— current release changes and audit lineage.
```

New:

```text
— v1.3.6 release changes and audit lineage; the candidate's changes are in `CHANGELOG-v1.3.7-candidate.md`.
```

## E98 — S · `README.md` L46 · — · fixtures: —

Old:

```text
The current v1.3.6 independent document audit is pending.
```

New:

```text
The v1.3.6 independent document audit is pending; the v1.3.7-candidate pack is not audited.
```

## E99 — label · `41_F18_Fixture_Inputs/M41.json` L3 · — · fixtures: M41

Old:

```text
"fixture_version": "1.2",
```

New:

```text
"fixture_version": "1.3.7-candidate, not audited",
```

## E100 — label · `41_F18_Fixture_Inputs/M42.json` L3 · — · fixtures: M42

Old:

```text
"fixture_version": "1.2",
```

New:

```text
"fixture_version": "1.3.7-candidate, not audited",
```

## E101 — label · `41_F18_Fixture_Inputs/M47.json` L3 · — · fixtures: M47

Old:

```text
"fixture_version": "1.2",
```

New:

```text
"fixture_version": "1.3.7-candidate, not audited",
```

## E102 — C12–C16 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L190–199 · PD-07 · fixtures: M13, M14, M15, M17, R07

Old:

```text
(after the last line)
```

New:

```text

## Input shapes of control and lifecycle vectors (v1.3.7 candidate, C12–C16)

Each shape below is the complete input of a fixture; a property outside its stated domain is an input error, not an outcome. A property whose value the Protocol fixes must equal that value and does not change the result.

- **Serializer-grammar vector** (C12): `diagnostic` (a string) and, optionally, `allowed_diagnostics` (the duplicate-free list of diagnostics the stage map emitted). It applies Protocol §3.4 feedback-serialization step (1): the closed grammar, then membership when the list is given. A failure is the `FEEDBACK_SERIALIZER_REJECT` record; a pass has no record to compare.
- **Truncation-primitive vector** (C13): `raw_diagnostic` (a string); `raw_diagnostic_utf8_bytes` (its UTF-8 byte length); `byte_cap` = `2048`; `marker` = `...[TRUNCATED]`; `truncate_on_utf8_boundary` = `true`; `truncate_before_json_escape` = `true`; `test_scope` = `TRUNCATION_PRIMITIVE_ONLY_GRAMMAR_BYPASSED`. The result is the step (2) control vector of Protocol §3.4.
- **JSON-escaping-primitive vector** (C14): `feedback_object` (exactly the string keys `stage_id`, `error_class`, `diagnostic`); `encoding` = `UTF-8`; `ensure_ascii` = `false`; `indent` = `2`; `line_endings` = `LF`; `terminal_newline` = `true`; `grammar_exempt_for_primitive_test` = `true`; `test_scope` = `JSON_ESCAPING_PRIMITIVE_ONLY_GRAMMAR_BYPASSED`. The result is the step (3) control vector of Protocol §3.4, keys serialized in the order `stage_id`, `error_class`, `diagnostic`.
- **Lifecycle halt-event vector** (C15): `lifecycle` = `MID_RUN` (the halt occurs after slots have begun, §7b); `event`, one stage-map event of kind `simulator_error` (`target` `rtl` or `null`, `exception_class`) or `trace_integrity` (`reason`); `slots` with non-negative integers `scheduled` (at least 1), `previously_evaluated`, `triggering_slot` (1 to `scheduled`) and `remaining`, where `previously_evaluated` + 1 + `remaining` = `scheduled`; `evaluator_repair_attempt` = `1`, the ordinal of the recovery cycle this halt opens (§7b allows one; a halt after that cycle is a recurrence, given as two halt signatures). The result is the event's stage-map row with disposition `DESIGN_HALT_NO_SLOT_SCORED`; the slot counts do not change it.
- **Design-preflight vector** (C16): `design_preflight`, an object with exactly the Boolean `rtl_null_masked_divergence`. `true` is the §7a baseline mismatch record; `false` passes the gate, with no record to compare.
```

## E103 — label · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L628 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E104 — label · `25_Common_System_and_Repair_Prompt_Templates.txt` L132 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E105 — label · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L208 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E106 — label · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L110 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E107 — label · `10_LLM_Era_Hardware_Verification_Literature_Review.md` L418 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E108 — label · `11_Comparative_Research_Matrix.md` L44 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E109 — label · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` L195 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E110 — label · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L73 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E111 — label · `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` L98 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E112 — label · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` L55 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E113 — label · `README.md` L49 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E114 — S · `22_Source_Access_Provenance_Log_v1.2.md` L8 · — · fixtures: —

Old:

```text
Literature review record: SHA-256 a79a4d68e445827be7d0c0f176aa3881f40e230814deb93481f109e50aeca11a
```

New:

```text
Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974
```

## E115 — S · `22_Source_Access_Provenance_Log_v1.2.md` L9 · — · fixtures: —

Old:

```text
Literature review record: SHA-256 a79a4d68e445827be7d0c0f176aa3881f40e230814deb93481f109e50aeca11a
```

New:

```text
Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974
```

## E116 — S · `22_Source_Access_Provenance_Log_v1.2.md` L10 · — · fixtures: —

Old:

```text
Literature review record: SHA-256 a79a4d68e445827be7d0c0f176aa3881f40e230814deb93481f109e50aeca11a
```

New:

```text
Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974
```

## E117 — S · `22_Source_Access_Provenance_Log_v1.2.md` L11 · — · fixtures: —

Old:

```text
Literature review record: SHA-256 a79a4d68e445827be7d0c0f176aa3881f40e230814deb93481f109e50aeca11a
```

New:

```text
Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974
```

## E118 — S · `22_Source_Access_Provenance_Log_v1.2.md` L12 · — · fixtures: —

Old:

```text
Literature review record: SHA-256 a79a4d68e445827be7d0c0f176aa3881f40e230814deb93481f109e50aeca11a
```

New:

```text
Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974
```

## E119 — label · `22_Source_Access_Provenance_Log_v1.2.md` L47 · — · fixtures: —

Old:

```text
(end of file)
```

New:

```text
appended trailer: ---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
```

## E120 — C6 + A1 · `41_F18_Fixture_Inputs/M27.json` Lall · PD-06, PD-25 · fixtures: M27

Old:

```text
{
  "fixture_id": "M27",
  "fixture_version": "1.0",
  "scope": "missing-case",
  "description": "Driver vector violates a design-specific legal-input predicate",
  "manifest_clause_ids": [
    "FIFO-001"
  ],
  "input": {
    "driver_return": {
      "wr_en": "1",
      "full": "1"
    },
    "legal_input_predicate": "wr_en must be 0 when full is 1"
  },
  "expected": {
    "disposition": "REPAIR",
    "stage_id": "DRIVER_VECTOR",
    "error_class": "DRIVER_VECTOR_INVALID",
    "diagnostic": "DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE"
  }
}
```

New:

```text
{
  "fixture_id": "M27",
  "fixture_version": "1.3.7-candidate, not audited",
  "scope": "missing-case",
  "description": "Driver vector passes the key, type, width and symbol checks and violates the supplied legal-input predicate",
  "manifest_clause_ids": [
    "FIFO-001"
  ],
  "input": {
    "driver_return": {
      "wr_en": "1"
    },
    "input_port_widths": {
      "wr_en": 1
    },
    "sampled_outputs": {
      "full": "1"
    },
    "legal_input_predicate": {
      "language": "python3.11",
      "function": "legal_input",
      "source": "def legal_input(vector, sampled):\n    return not (sampled[\"full\"] == \"1\" and vector[\"wr_en\"] == \"1\")\n"
    }
  },
  "expected": {
    "disposition": "REPAIR",
    "stage_id": "DRIVER_VECTOR",
    "error_class": "DRIVER_VECTOR_INVALID",
    "diagnostic": "DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE"
  }
}
```

## E121 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L380 · — · fixtures: M27

Old:

```text
"sha256": "fb7cd4179e9f103a1dc6f158839cd242b054f5d1e8fcf7e3c2a046c8c145e529",
```

New:

```text
"sha256": "b037404ddb874bd9a72e85f6ffe09a52d2b37d3f47f3e8e49a519884d0495508",
```

## E122 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L381 · — · fixtures: M27

Old:

```text
"bytes": 558,
```

New:

```text
"bytes": 971,
```

## E123 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L562 · — · fixtures: M41

Old:

```text
"sha256": "56ba49bdedf6eda6f72d0231a1a2861112ff8691ef3a453725341449aab11863",
```

New:

```text
"sha256": "c2e42af7bf912c214f974d5ec371a0fe6845ee8f356d729226edf2db097723b7",
```

## E124 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L563 · — · fixtures: M41

Old:

```text
"bytes": 1626,
```

New:

```text
"bytes": 1651,
```

## E125 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L579 · — · fixtures: M42

Old:

```text
"sha256": "f76023e38e25f9b04059aa7e8d1a8360229c1ea840fb19c68484e5bae7fcfc01",
```

New:

```text
"sha256": "c86181f5e754d50a891def2cae82e194711a098e42419437c0d1985745d15d03",
```

## E126 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L580 · — · fixtures: M42

Old:

```text
"bytes": 1079,
```

New:

```text
"bytes": 1104,
```

## E127 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L644 · — · fixtures: M47

Old:

```text
"sha256": "c9868971e3f2c334ce6d08c925b1319a1c4e8a9ef5b2d7620799c09fe1b27797",
```

New:

```text
"sha256": "4958c30a5d0fd2baa1b032a4104e20268a832e265a7107409a8772b9d9d7515f",
```

## E128 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L645 · — · fixtures: M47

Old:

```text
"bytes": 1119,
```

New:

```text
"bytes": 1135,
```

## E129 — label · `41_F18_Fixture_Inputs/fixture-index.json` L2 · — · fixtures: —

Old:

```text
"fixture_index_version": "1.3.6",
```

New:

```text
"fixture_index_version": "1.3.7-candidate, not audited",
```

## E130 — S · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` Lname · — · fixtures: —

Old:

```text
01_OpenVEF_Project_Charter_v1.3.6.md
```

New:

```text
01_OpenVEF_Project_Charter_v1.3.7-candidate.md
```

## E131 — S · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` Lname · — · fixtures: —

Old:

```text
02_OpenVEF_Experimental_Protocol_v1.3.6.md
```

New:

```text
02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md
```

## E132 — S · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` Lname · — · fixtures: —

Old:

```text
21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md
```

New:

```text
21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md
```

## E133 — S · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` Lname · — · fixtures: —

Old:

```text
30_Response_Parser_and_Execution_Contract_v1.3.6.md
```

New:

```text
30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md
```

## E134 — S · `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` Lname · — · fixtures: —

Old:

```text
31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md
```

New:

```text
31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md
```

## E135 — S · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` Lname · — · fixtures: —

Old:

```text
32_v1.3.6_Status_and_Gates.md
```

New:

```text
32_v1.3.7-candidate_Status_and_Gates.md
```

## E136 — S · `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` (was `33_Prompt_Assembly_Sidecar_v1.3.6.json` Lname · — · fixtures: —

Old:

```text
33_Prompt_Assembly_Sidecar_v1.3.6.json
```

New:

```text
33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json
```

## E137 — S · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` Lname · — · fixtures: —

Old:

```text
36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md
```

New:

```text
36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md
```

## E138 — S · `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` (was `38_Authoring_Packet_Manifest_Template_v1.3.6.json` Lname · — · fixtures: —

Old:

```text
38_Authoring_Packet_Manifest_Template_v1.3.6.json
```

New:

```text
38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json
```

## E139 — derived · `27_SHA256SUMS.txt` L1 · — · fixtures: —

Old:

```text
af3bd1c72683c2e9bb56a38a3cc85d228bec53e8fc786f81c4593cdfd3d9412b  01_OpenVEF_Project_Charter_v1.3.6.md
```

New:

```text
ec6537278d998400a60119e386cecf68a79c6698550d50f37e684421ea85c016  01_OpenVEF_Project_Charter_v1.3.7-candidate.md
```

## E140 — derived · `27_SHA256SUMS.txt` L2 · — · fixtures: —

Old:

```text
1a3015ea38f96ab97e813076476d34f3043a40a83825106937ff633d14b61a87  02_OpenVEF_Experimental_Protocol_v1.3.6.md
```

New:

```text
55f52d1fa4012a9206bf4b66999766fd0b45b8eb47c110533d49122e500e6049  02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md
```

## E141 — derived · `27_SHA256SUMS.txt` L11 · — · fixtures: —

Old:

```text
a79a4d68e445827be7d0c0f176aa3881f40e230814deb93481f109e50aeca11a  10_LLM_Era_Hardware_Verification_Literature_Review.md
```

New:

```text
0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974  10_LLM_Era_Hardware_Verification_Literature_Review.md
```

## E142 — derived · `27_SHA256SUMS.txt` L12 · — · fixtures: —

Old:

```text
014094c32d8c521ab0e865a358207ca09959b018978f67492a35626f9ff89fbe  11_Comparative_Research_Matrix.md
```

New:

```text
3e40cc28eacce8289660ee8a2c5239fb66e91e20abf7409a99dd5bcb0e07d8a3  11_Comparative_Research_Matrix.md
```

## E143 — derived · `27_SHA256SUMS.txt` L20 · — · fixtures: —

Old:

```text
a84a89837e3158c294a351adc1f90c6aa583e462733622027ea1ac9feaeb40b1  21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md
```

New:

```text
36b07acb8f16a1f58f3d3630fc44c683e2386481d0c98e97c16dcb073848d649  21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md
```

## E144 — derived · `27_SHA256SUMS.txt` L21 · — · fixtures: —

Old:

```text
c19d937d1849ec3b8a4529c54822674da433e26094b0ed4c407538f2dace0dac  22_Source_Access_Provenance_Log_v1.2.md
```

New:

```text
3705bfda6bee79e0e4f3f85848eefd32b0f46d09dd9b947e6b788c2441635ef9  22_Source_Access_Provenance_Log_v1.2.md
```

## E145 — derived · `27_SHA256SUMS.txt` L24 · — · fixtures: —

Old:

```text
987378853f21b108704b5d97e10a1832de7fcdeca7ed7aae65b26a5e0e04bc49  25_Common_System_and_Repair_Prompt_Templates.txt
```

New:

```text
03fb29ec36b5cb85baee9c0aa9c0a36294d59290c80a72cddb973db428244889  25_Common_System_and_Repair_Prompt_Templates.txt
```

## E146 — derived · `27_SHA256SUMS.txt` L28 · — · fixtures: —

Old:

```text
b0b43989beb81be986caed48562c6832ca981449f82fd14f6ae8bdceed5b2ba6  30_Response_Parser_and_Execution_Contract_v1.3.6.md
```

New:

```text
bef2e314f5f57fdf7e14ecdd03fdab2d103c6318c5d831526db13fb7a23a8936  30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md
```

## E147 — derived · `27_SHA256SUMS.txt` L29 · — · fixtures: —

Old:

```text
aa963c39eedf087c1b7f4b5d4df0545a69451e6d78e94256f45c70bc54f91e72  31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md
```

New:

```text
9d29dff10264627e581e93f66244ea32dcdb902232356584509dd31153b86f85  31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md
```

## E148 — derived · `27_SHA256SUMS.txt` L30 · — · fixtures: —

Old:

```text
614046f17efb4609ddee10830b781fb0fecb3dbe9fb7bd681e0bdd043b3c6e66  32_v1.3.6_Status_and_Gates.md
```

New:

```text
c6be64aee3962196185e7298d2e02f3740e69a33cc22cb56596dfef3f3120f53  32_v1.3.7-candidate_Status_and_Gates.md
```

## E149 — derived · `27_SHA256SUMS.txt` L31 · — · fixtures: —

Old:

```text
b2585edb095d29a7decd94f509f45c3a481d8d3747db1bcbcf0a908605219902  33_Prompt_Assembly_Sidecar_v1.3.6.json
```

New:

```text
a948bd1ef3f05223af0f741087b6e29795ffcb27f87428f84a13bb245f9e6792  33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json
```

## E150 — derived · `27_SHA256SUMS.txt` L34 · — · fixtures: —

Old:

```text
270ccbd73691e6e32fbec8817e7c235d50ba3a803796270f236006e938f4983e  36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md
```

New:

```text
6a08b3bc2685258b5671d2a5f176f9ec3f6687f006cb13f8ed2624d86ee4e936  36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md
```

## E151 — derived · `27_SHA256SUMS.txt` L36 · — · fixtures: —

Old:

```text
55dc7f4f9e9ca3424a73831cae2f1e90a280173e8e463698f1989bd3d47ee8e6  38_Authoring_Packet_Manifest_Template_v1.3.6.json
```

New:

```text
d841b87ee410ad462521aaa76f27cae1c2f5a7923aff6d51b4fb0a61fc7e8819  38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json
```

## E152 — derived · `27_SHA256SUMS.txt` L66 · — · fixtures: —

Old:

```text
fb7cd4179e9f103a1dc6f158839cd242b054f5d1e8fcf7e3c2a046c8c145e529  41_F18_Fixture_Inputs/M27.json
```

New:

```text
b037404ddb874bd9a72e85f6ffe09a52d2b37d3f47f3e8e49a519884d0495508  41_F18_Fixture_Inputs/M27.json
```

## E153 — derived · `27_SHA256SUMS.txt` L80 · — · fixtures: —

Old:

```text
56ba49bdedf6eda6f72d0231a1a2861112ff8691ef3a453725341449aab11863  41_F18_Fixture_Inputs/M41.json
```

New:

```text
c2e42af7bf912c214f974d5ec371a0fe6845ee8f356d729226edf2db097723b7  41_F18_Fixture_Inputs/M41.json
```

## E154 — derived · `27_SHA256SUMS.txt` L81 · — · fixtures: —

Old:

```text
f76023e38e25f9b04059aa7e8d1a8360229c1ea840fb19c68484e5bae7fcfc01  41_F18_Fixture_Inputs/M42.json
```

New:

```text
c86181f5e754d50a891def2cae82e194711a098e42419437c0d1985745d15d03  41_F18_Fixture_Inputs/M42.json
```

## E155 — derived · `27_SHA256SUMS.txt` L86 · — · fixtures: —

Old:

```text
c9868971e3f2c334ce6d08c925b1319a1c4e8a9ef5b2d7620799c09fe1b27797  41_F18_Fixture_Inputs/M47.json
```

New:

```text
4958c30a5d0fd2baa1b032a4104e20268a832e265a7107409a8772b9d9d7515f  41_F18_Fixture_Inputs/M47.json
```

## E156 — derived · `27_SHA256SUMS.txt` L182 · — · fixtures: —

Old:

```text
f37808c7a662b8fdf164e27feaef023aadd6dfefaada35d11c3719185d1bde54  41_F18_Fixture_Inputs/fixture-index.json
```

New:

```text
5aef6de9993d2f7aec544536068ed046e6f001d5e384075f8dbe94877f17d7e0  41_F18_Fixture_Inputs/fixture-index.json
```

## E157 — derived · `27_SHA256SUMS.txt` L202 · — · fixtures: —

Old:

```text
cd222521cb455c1eb12241a05a8f31bda908bd6b5a00efcd22ca4029c9feeca5  README.md
```

New:

```text
f1dabfafbf5ae5af6a39f38247dc59b3fd26fd64ea8b77863cb290cf3c364ae9  README.md
```

## E158 — OS-1–OS-3 (OWNER-SPECIFIED, D-026) · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L200–207 · PD-07, PD-01, PD-03 · fixtures: M41, M37, P17

Old:

```text
(after the C12–C16 lines)
```

New:

```text

## Owner-specified vector inputs (v1.3.7 candidate, OWNER-SPECIFIED OS-1–OS-3, owner decision D-026)

These items are OWNER-SPECIFIED, not derived from pack text: the Protocol fixes each expected outcome, and owner decision D-026 specifies only how the vector reaches the stage that outcome names. They add no outcome code. A property outside its stated domain, or an input for which neither these items nor the Protocol states an outcome, is an input error, not an outcome.

- **Operational-recovery vector** (OS-1, §7b): `design_id` (`FIFO` or `UART`, equal to the `design_id` of `halt_signature`); `halt_signature`, the halt's signature in the Protocol §7b domains, with `halt_code` `SIMULATOR_ERROR` or `TRACE_INTEGRITY_FAILURE` (a masked RTL/null divergence may use operational recovery only after a root-cause review, which this vector does not carry); `slots` as in the lifecycle halt-event vector, so the halt occurred after slots had begun; `evaluator_repair_attempt` = `1`; `recovery_mode` = `OPERATIONAL_RECOVERY`; the Booleans `frozen_evaluator_hashes_unchanged`, `f16_required`, `same_artifact_bytes` and `author_visible_materials_changed`; `pre_halt_scored_slots` (1 to `previously_evaluated`), the number of pre-halt scores; `scheduled_slots` = `scheduled`, the scheduled slots of the affected scope; `same_artifacts_for_all_slots` = `true`, `same_slot_seeds` = `true` and `new_generation_calls` = `0`, which restate §7b; and `required_action`, a string that is an informational label, not an outcome input. Only the properties named by the §7b recovery conditions decide the outcome. When `frozen_evaluator_hashes_unchanged` is `true`, `f16_required` is `false`, `same_artifact_bytes` is `true` and `author_visible_materials_changed` is `false`, the result is the successful-operational-recovery control expectation of Protocol §3.4 at stage `DESIGN_HALT` with disposition `CONTROL_EXPECTATION` and the properties `discard_pre_halt_scores` = `true`, `rerun_slots` = `scheduled_slots`, `reuse_same_artifact_bytes` = `true` and `new_confirmatory_generation_calls` = `0`. When the frozen evaluator hashes changed (`frozen_evaluator_hashes_unchanged` is `false`, `f16_required` is `true`, `same_artifact_bytes` is `true` and `author_visible_materials_changed` is `false`), the recovery is an evaluator revision and the result is the change-class control expectation of `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED`. The Protocol states no outcome for any other combination, including an author-visible change, which §7b sends to a study or design revision that the vector does not identify; such an input is outside this vector's scope.
- **Paired-run outcome vector** (OS-2): `response_object` (a response object, as for any response input) and `runtime_pair`, an object with exactly `driver_source_excerpt` (a string that documents the access under test; it is not executed, matched or read for the outcome) and the Booleans `before_first_raw_output_divergence` and `next_input_schedules_equal`. Protocol §3.4 evaluation steps (1)–(6) run on the response object, and their first failure is the result. If all pass, `runtime_pair` stands in for steps (7)–(8), the paired run, which is not executed: `before_first_raw_output_divergence` = `true` with `next_input_schedules_equal` = `false` is the `DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE` row of the stage map. Any other pair does not determine the paired run's outcome and is outside this vector's scope.
- **Runtime driver-vector input** (OS-3): `response_object` with `port_manifest` (`input_ports`). Its expected stage, `DRIVER_VECTOR`, is checked within evaluation step (7), while `Driver.step` runs on the original RTL; the input gives no design, RTL or port widths, and no rule states how the driver's vector is obtained outside that run. This input is not specified, and a fixture with it stays NOT_IMPLEMENTED.
```

## E159 — OD-1 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L174 · D1-5 · fixtures: M15

Old:

```text
`FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`.
```

New:

```text
**OWNER-DECIDED OD-1** (owner decision D-027; v1.3.6 does not state it): a stage-map row with a single diagnostic code and no stated error class has the error class equal to that diagnostic code; the `SIMULATOR_ERROR` row, whose stated error class is `EVALUATOR_INFRASTRUCTURE_FAILURE`, is the stated exception. An error-class cell `—` states that a row has no error class, so OD-1 does not apply to it. OD-1 decides exactly two error classes, those of the local-ledger rows `FEEDBACK_SERIALIZER_REJECT` and `DESIGN_HALT_REPEATED`; every other row of the stage map and of this vocabulary states its error class. By OD-1, `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`.
```

## E160 — A2 (copy of OD-1) · `25_Common_System_and_Repair_Prompt_Templates.txt` L117 · D1-5 · fixtures: M15

Old:

```text
`FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`.
```

New:

```text
**OWNER-DECIDED OD-1** (owner decision D-027; v1.3.6 does not state it): a stage-map row with a single diagnostic code and no stated error class has the error class equal to that diagnostic code; the `SIMULATOR_ERROR` row, whose stated error class is `EVALUATOR_INFRASTRUCTURE_FAILURE`, is the stated exception. An error-class cell `—` states that a row has no error class, so OD-1 does not apply to it. OD-1 decides exactly two error classes, those of the local-ledger rows `FEEDBACK_SERIALIZER_REJECT` and `DESIGN_HALT_REPEATED`; every other row of the stage map and of this vocabulary states its error class. By OD-1, `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`.
```

## E161 — OD-1 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L185 · D1-5 · fixtures: M42, M47

Old:

```text
Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED`.
```

New:

```text
Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED` (OWNER-DECIDED OD-1, §3.4 local-ledger error classes).
```

## E162 — A2 (copy of OD-1) · `25_Common_System_and_Repair_Prompt_Templates.txt` L128 · D1-5 · fixtures: M42, M47

Old:

```text
Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED`.
```

New:

```text
Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED` (OWNER-DECIDED OD-1, §3.4 local-ledger error classes).
```

## E163 — OD-2 · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L83 · D1-3 · fixtures: M27

Old:

```text
The predicate is frozen as one Python 3.11 function of two dictionaries, `(vector, sampled)`: the driver vector, and the outputs sampled in the same row, each mapping a port name to its bit string.
```

New:

```text
**OWNER-DECIDED OD-2** (owner decision D-027; v1.3.6 does not state how the predicate is represented): the owners adopt Python 3.11 as its representation. The predicate is frozen as one Python 3.11 function of two dictionaries, `(vector, sampled)`: the driver vector, and the outputs sampled in the same row, each mapping a port name to its bit string. The function is pure: its result depends only on its two arguments, and it has no other effect.
```

## E164 — OD-2 · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L83 · D1-3 · fixtures: M27

Old:

```text
Any other outcome, including an exception, is an evaluator failure and is never an artifact verdict.
```

New:

```text
Any other outcome, including an exception, is an evaluator failure and is never an artifact verdict. The predicate is evaluator material, not artifact code: the evaluator executes it, outside every artifact process. It is hash-gated: the SHA-256 of its UTF-8 source is recorded when it is frozen, and the evaluator executes it only after checking that the source has that hash; a mismatch is an evaluator failure.
```

## E165 — OD-2 · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L83 · D1-3 · fixtures: M27

Old:

```text
`function`, the function's name, and `source`, its Python source)
```

New:

```text
`function`, the function's name, `source`, its Python source, and `source_sha256`, the lowercase hexadecimal SHA-256 of `source` in UTF-8, which is the frozen hash of OD-2)
```

## E166 — OD-3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · D1-1 · fixtures: M54

Old:

```text
**Closed `required_action` literals, by change class:**
```

New:

```text
**Closed `required_action` literals, by change class and, for `HALT_SIGNATURE_COMPONENT_ENUMERATION`, by domain validation (OD-3):**
```

## E167 — A2 (copy of OD-3) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · D1-1 · fixtures: M54

Old:

```text
**Closed `required_action` literals, by change class:**
```

New:

```text
**Closed `required_action` literals, by change class and, for `HALT_SIGNATURE_COMPONENT_ENUMERATION`, by domain validation (OD-3):**
```

## E168 — OD-3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · D1-1 · fixtures: M48, M50, M53, M54, M58

Old:

```text
The change classes are closed and have these cases:
```

New:

```text
The change classes are closed and have exactly four cases (OWNER-DECIDED OD-3):
```

## E169 — A2 (copy of OD-3) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · D1-1 · fixtures: M48, M50, M53, M54, M58

Old:

```text
The change classes are closed and have these cases:
```

New:

```text
The change classes are closed and have exactly four cases (OWNER-DECIDED OD-3):
```

## E170 — OD-3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · D1-1 · fixtures: M54, M58

Old:

```text
is a study reset; `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` is a design-specific revision while membership, estimand and weights remain unchanged; and `HALT_SIGNATURE_COMPONENT_ENUMERATION` is the halt-signature domain check.
```

New:

```text
is a study reset; and `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` is a design-specific revision while membership, estimand and weights remain unchanged. `HALT_SIGNATURE_COMPONENT_ENUMERATION` is not a change class: it names the halt-signature domain validation (§7b, L185).
```

## E171 — A2 (copy of OD-3) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · D1-1 · fixtures: M54, M58

Old:

```text
is a study reset; `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` is a design-specific revision while membership, estimand and weights remain unchanged; and `HALT_SIGNATURE_COMPONENT_ENUMERATION` is the halt-signature domain check.
```

New:

```text
is a study reset; and `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` is a design-specific revision while membership, estimand and weights remain unchanged. `HALT_SIGNATURE_COMPONENT_ENUMERATION` is not a change class: it names the halt-signature domain validation (§7b, L185).
```

## E172 — OD-3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · D1-1 · fixtures: M48, M50, M58

Old:

```text
Closed scope tokens:
```

New:

```text
Closed scope tokens (OWNER-DECIDED OD-3: owner vocabulary adopted by owner decision D-027; the spellings are not v1.3.6 text, and each token means the §7b text cited with it):
```

## E173 — A2 (copy of OD-3) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · D1-1 · fixtures: M48, M50, M58

Old:

```text
Closed scope tokens:
```

New:

```text
Closed scope tokens (OWNER-DECIDED OD-3: owner vocabulary adopted by owner decision D-027; the spellings are not v1.3.6 text, and each token means the §7b text cited with it):
```

## E174 — OD-3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L176 · D1-2 · fixtures: M48, M50, M53, M54, M58

Old:

```text
A design-specific revision invalidates both arms for the affected design only when membership, estimand and weights remain unchanged.
```

New:

```text
A design-specific revision invalidates both arms for the affected design only when membership, estimand and weights remain unchanged. The input contract and the complete result schema of every control vector are the normative tables of §20 (OWNER-DECIDED OD-3).
```

## E175 — A2 (copy of OD-3) · `25_Common_System_and_Repair_Prompt_Templates.txt` L119 · D1-2 · fixtures: M48, M50, M53, M54, M58

Old:

```text
A design-specific revision invalidates both arms for the affected design only when membership, estimand and weights remain unchanged.
```

New:

```text
A design-specific revision invalidates both arms for the affected design only when membership, estimand and weights remain unchanged. The input contract and the complete result schema of every control vector are the normative tables of §20 (OWNER-DECIDED OD-3).
```

## E176 — OD-3 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L176 · D1-2 · fixtures: M48, M50, M53, M54, M58

Old:

```text
every property it names must be defined by a rule in the Protocol.
```

New:

```text
every property it names must be defined by a rule in the Protocol (Protocol §20, OWNER-DECIDED OD-3, lists every control-vector property and its rule).
```

## E177 — OD-3 · `41_F18_Fixture_Inputs/M54.json` L11 · D1-1 · fixtures: M54

Old:

```text
"change_class": "HALT_SIGNATURE_COMPONENT_ENUMERATION"
```

New:

```text
"domain_validation": "HALT_SIGNATURE_COMPONENT_ENUMERATION"
```

## E178 — OD-4 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L185 · D1-6 · fixtures: M13, M41

Old:

```text
No second recovery cycle is permitted.
```

New:

```text
No second recovery cycle is permitted. **OWNER-DECIDED OD-4** (owner decision D-027; v1.3.6 does not define it): the *evaluator repair attempt* of a design halt, `evaluator_repair_attempt`, is the ordinal of the recovery cycle that halt opens. A halt that occurs while the design has used no recovery cycle opens its one permitted cycle and has `evaluator_repair_attempt` = `1`. A halt that occurs after that cycle has been used would open a second cycle, which is not permitted: it is not a new attempt but the `DESIGN_HALT_REPEATED` termination above (by recurrence of the identical signature, or as a different halt). No ordinal greater than `1` is valid. The ordinal is a lifecycle count, not a halt-signature component.
```

## E179 — A2 (copy of OD-4) · `25_Common_System_and_Repair_Prompt_Templates.txt` L128 · D1-6 · fixtures: M13, M41

Old:

```text
No second recovery cycle is permitted.
```

New:

```text
No second recovery cycle is permitted. **OWNER-DECIDED OD-4** (owner decision D-027; v1.3.6 does not define it): the *evaluator repair attempt* of a design halt, `evaluator_repair_attempt`, is the ordinal of the recovery cycle that halt opens. A halt that occurs while the design has used no recovery cycle opens its one permitted cycle and has `evaluator_repair_attempt` = `1`. A halt that occurs after that cycle has been used would open a second cycle, which is not permitted: it is not a new attempt but the `DESIGN_HALT_REPEATED` termination above (by recurrence of the identical signature, or as a different halt). No ordinal greater than `1` is valid. The ordinal is a lifecycle count, not a halt-signature component.
```

## E180 — OD-4 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L198 · D1-6 · fixtures: M13

Old:

```text
`evaluator_repair_attempt` = `1`, the ordinal of the recovery cycle this halt opens (§7b allows one;
```

New:

```text
`evaluator_repair_attempt` = `1`, the ordinal of the recovery cycle this halt opens (OWNER-DECIDED OD-4, Protocol §7b L185; §7b allows one;
```

## E181 — OD-4 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L205 · D1-6 · fixtures: M41

Old:

```text
`evaluator_repair_attempt` = `1`; `recovery_mode`
```

New:

```text
`evaluator_repair_attempt` = `1` (OWNER-DECIDED OD-4, Protocol L185); `recovery_mode`
```

## E182 — A3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L185 · D1-7 · fixtures: M41, M42, M47

Old:

```text
A supplied halt signature with any component outside these domains is an evaluator input error; it is never compared for recurrence.
```

New:

```text
A supplied halt signature with any component outside these domains is an evaluator input error; it is never compared for recurrence. Such an input is outside the executable fixture contract: it is not an outcome, has no diagnostic, stage, error class or disposition, and produces no ledger record.
```

## E183 — A2 (copy of A3) · `25_Common_System_and_Repair_Prompt_Templates.txt` L128 · D1-7 · fixtures: M41, M42, M47

Old:

```text
A supplied halt signature with any component outside these domains is an evaluator input error; it is never compared for recurrence.
```

New:

```text
A supplied halt signature with any component outside these domains is an evaluator input error; it is never compared for recurrence. Such an input is outside the executable fixture contract: it is not an outcome, has no diagnostic, stage, error class or disposition, and produces no ledger record.
```

## E184 — A4 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L143 · D1-8 · fixtures: M37

Old:

```text
| M37 | missing-case | Aliased global random access leads to paired next-input divergence at runtime |
```

New:

```text
| M37 | missing-case | Paired-outcome control vector (OS-2): a supplied paired-run outcome with next-input divergence before the first raw-output divergence; the documented aliased global random access is not detected from the source |
```

## E185 — A4 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L206 · D1-8 · fixtures: M37

Old:

```text
- **Paired-run outcome vector** (OS-2): 
```

New:

```text
- **Paired-run outcome vector** (OS-2; a paired-outcome control vector, not a test of source-level alias detection): 
```

## E186 — A4 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L206 · D1-8 · fixtures: M37

Old:

```text
Any other pair does not determine the paired run's outcome and is outside this vector's scope.
```

New:

```text
Any other pair does not determine the paired run's outcome and is outside this vector's scope. The vector therefore tests the supplied paired-run outcome and the precedence of the static stages; it does not show that the response contains the access its excerpt documents.
```

## E187 — A4 · `41_F18_Fixture_Inputs/M37.json` L5 · D1-8 · fixtures: M37

Old:

```text
"description": "Aliased global random access leads to paired next-input divergence at runtime"
```

New:

```text
"description": "Paired-outcome control vector (OS-2): a supplied paired-run outcome with next-input divergence before the first raw-output divergence; the documented aliased global random access is not detected from the source"
```

## E188 — C17 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L3 · D1-9 · fixtures: all

Old:

```text
All fixtures remain **NOT RUN / NOT PASSED**.
```

New:

```text
Status, in three separate parts: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.
```

## E189 — C17 · `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` (was `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.6.md` L176 · D1-9 · fixtures: all

Old:

```text
Current execution status: **NOT RUN / NOT PASSED**.
```

New:

```text
Formal F18 status: **NOT RUN / NOT PASSED** (development-run evidence is not F18 acceptance, and nothing is approved; see the status line at the top of this file).
```

## E190 — C17 · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` L21 · D1-9 · fixtures: all

Old:

```text
- Execution status: **NOT RUN / NOT PASSED** for every fixture.
```

New:

```text
- Status, in three separate parts, for every fixture: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.
```

## E191 — C17 · `32_v1.3.7-candidate_Status_and_Gates.md` (was `32_v1.3.6_Status_and_Gates.md` L33 · D1-9 · fixtures: all

Old:

```text
- Parser, assembler, harness, simulator and F1–F18: NOT IMPLEMENTED / NOT RUN.
```

New:

```text
- Parser, assembler, harness, simulator and F1–F18: a project implementation exists outside this pack and has development-run evidence only; formal F18 status NOT RUN / NOT PASSED; the implementation is not qualified or approved.
```

## E192 — C17 · `README.md` L16 · D1-9 · fixtures: all

Old:

```text
all NOT RUN / NOT PASSED.
```

New:

```text
formal F18 status NOT RUN / NOT PASSED (development runs are not F18 acceptance; nothing is approved).
```

## E193 — C17 · `README.md` L35 · D1-9 · fixtures: all

Old:

```text
Every fixture remains **NOT RUN / NOT PASSED**.
```

New:

```text
Status, in three separate parts, for every fixture: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.
```

## E194 — C17 · `README.md` L46 · D1-9 · fixtures: all

Old:

```text
All 144 fixture descriptors remain NOT RUN / NOT PASSED. The project parser, assembler, harness, simulator and F1–F18 remain NOT IMPLEMENTED / NOT RUN.
```

New:

```text
All 144 fixture descriptors remain formally NOT RUN / NOT PASSED: a project implementation (parser, assembler, harness, simulator, F1–F18) exists outside this pack with development-run evidence only, there is no authorized F18 acceptance run, and nothing is qualified or approved.
```

## E195 — C17 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L559 · D1-9 · fixtures: all

Old:

```text
All 144 fixture descriptors remain NOT RUN / NOT PASSED.
```

New:

```text
All 144 fixture descriptors remain formally NOT RUN / NOT PASSED (development-run evidence of a project implementation is not F18 acceptance, and nothing is approved).
```

## E196 — label · `41_F18_Fixture_Inputs/M54.json` L3 · — · fixtures: M54

Old:

```text
"fixture_version": "1.3.1",
```

New:

```text
"fixture_version": "1.3.7-candidate, not audited",
```

## E197 — label · `41_F18_Fixture_Inputs/M37.json` L3 · — · fixtures: M37

Old:

```text
"fixture_version": "1.1",
```

New:

```text
"fixture_version": "1.3.7-candidate, not audited",
```

## E198 — OD-3 · `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` (was `02_OpenVEF_Experimental_Protocol_v1.3.6.md` L560–627 · D1-1, D1-2 · fixtures: M48, M50, M53, M54, M58

Old:

```text
(after the last line)
```

New:

```text

## 20. Control-vector input contracts and result schemas (v1.3.7 candidate, OWNER-DECIDED OD-3)

**OWNER-DECIDED OD-3** (owner decision D-027). v1.3.6 names the properties of its control vectors only in fixture descriptors and does not state their schema. The owners adopt the tables below as normative. Each row names one property, its type, its allowed values and the Protocol text that fixes its value. Basis `pack` means that the cited text fixes the value. `C1`, `C3`, `C9`, `C12`, `C13` and `C14` name candidate corrections, `OD-1` is the owner rule of L174, `OS-1` is the owner specification of owner decision D-026, and `A-033` is the reading approved under owner decision D-009. Basis `OD-3` means owner vocabulary or schema adopted by D-027: its spelling is not v1.3.6 text, and its meaning is the text cited with it. A control-vector result has exactly the properties its table lists and is compared whole (File 36 L176). An input with a value outside its allowed values, or with any other property, is an input error, not an outcome.

**Properties no rule fixes:** none. Every property of every control vector below has a rule. Two rows rest on a reading rather than on one sentence: the stage `DESIGN_HALT` of the change-class and domain-validation results (A-033), and the order of the three domain arrays, which is the order L185 lists them in (OD-3).

### 20.1 Inputs of the change-class and domain-validation vectors

| Vector | Property | Type | Allowed values | Rule | Basis |
| --- | --- | --- | --- | --- | --- |
| Change-class vector | `change_class` | string | exactly one of `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED`, `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED`, `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START`, `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | L176: the four change classes. The input is the class alone, so the result states the rule for that class and names no design, component or slot. | OD-3 |
| Domain-validation vector | `domain_validation` | string | exactly `HALT_SIGNATURE_COMPONENT_ENUMERATION` | L185: the halt-signature domains. The result states the closed component domains and the two component rules. | OD-3 |

### 20.2 Properties of every change-class and domain-validation result

| Property | Type | Value | Rule | Basis |
| --- | --- | --- | --- | --- |
| `disposition` | string | `CONTROL_EXPECTATION` | L176 "Each literal is a closed local control expectation"; L177 | pack |
| `stage_id` | string | `DESIGN_HALT` | L172 stage list; §7b, which L251 makes normative in §3.4 "Mid-run design halt" (L181–L185) | A-033 |
| `error_class` | string | the CODE of `diagnostic` | L175 error-class rule for `EVALUATOR_REVISION_REQUIRED`, `AUTHORING_REVISION_REQUIRED` and `HALT_SIGNATURE_SCHEMA` | C1 |
| `diagnostic` | string | the value given for the input in §20.3 | L175 | pack |
| `required_action` | string | the L176 literal of the change class, or of `HALT_SIGNATURE_COMPONENT_ENUMERATION` | L176 | pack |

### 20.3 Further properties of each result

| Input value | Property | Type | Value | Rule | Basis |
| --- | --- | --- | --- | --- | --- |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `diagnostic` | string | `EVALUATOR_REVISION_REQUIRED|reason=FROZEN_EVALUATOR_CHANGED` | L175 "means a frozen evaluator source/binary/tool-version/command/option/configuration changed" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `new_evaluator_version_hashes_required` | Boolean | `true` | L183 "assign a new evaluator version and hashes" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `f16_required` | Boolean | `true` | L183 "run the frozen F16 eligibility procedure with fresh mutant-blind pilot seeds" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `reuse_same_artifact_bytes` | Boolean | `true` | L183 "using the same already-generated artifact bytes" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `new_confirmatory_generation_calls` | integer | `0` | L183 "and no new confirmatory generation calls" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `rerun_scope_rule` | string | `shared_evaluator_component_all_designs_and_all_arm_x_design_slots; design_specific_component_affected_design_in_both_arms` | L183 "If the revised evaluator component is shared across FIFO and UART, the affected scope is both designs and every arm × design slot; if it is design-specific, the affected scope is that design in both arms" | OD-3 |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `diagnostic` | string | `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | L175 "means an author-visible or estimand-defining item changed and prior confirmatory artifacts are not reusable" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `reuse_old_confirmatory_artifacts` | Boolean | `false` | L181 "No invalidated confirmatory artifact may be reused" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `new_confirmatory_generation_required` | Boolean | `true` | L181 "fresh confirmatory generation for every affected slot" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `affected_slots` | string | `all_designs_x_all_arms` | L181 "invalidate every scheduled slot across both designs and both arms" | OD-3 |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `archive_and_disclose_partial_ledgers` | Boolean | `true` | L181 "Preserve and archive every partial confirmatory ledger" and "disclose the archived partial ledgers" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `new_preregistration_required` | Boolean | `true` | L181 "A shared-item revision requires a new study preregistration" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `diagnostic` | string | `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | L175 "means an author-visible or estimand-defining item changed and prior confirmatory artifacts are not reusable"; L175 study-reset sentence | pack, C1 |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `old_confirmatory_artifacts_reusable` | Boolean | `false` | L181 "A study reset is not an operational recovery and cannot retain old confirmatory artifacts" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `new_preregistration_required` | Boolean | `true` | L181 "always requires a new preregistered study" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `all_partial_ledgers_archived_and_disclosed` | Boolean | `true` | L181 "archive and disclose all partial confirmatory ledgers" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `fresh_confirmatory_generation_required` | Boolean | `true` | L181 "generate fresh confirmatory slots under the newly preregistered design set and weights" | pack |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `diagnostic` | string | `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | L175 "means an author-visible or estimand-defining item changed and prior confirmatory artifacts are not reusable" | pack |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `affected_scope` | string | `affected_design_in_both_arms` | L181 "If a design-specific author-visible item changes, halt and invalidate every slot for that design in both arms" | OD-3 |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `unaffected_design_scope` | string | `not_invalidated_when_membership_estimand_and_weights_are_unchanged` | L181 "every slot for that design in both arms" (the other design is outside that scope) and "A change in design membership, estimand or any confirmatory weight after confirmatory generation starts always requires a new preregistered study" | OD-3 |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `reuse_old_artifacts_for_affected_design` | Boolean | `false` | L181 "No invalidated confirmatory artifact may be reused" | pack |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `new_study_preregistration_required_if_design_membership_estimand_or_weights_change` | Boolean | `true` | L181 "always requires a new preregistered study, even if the changed item is otherwise described as design-specific" | pack |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `diagnostic` | string | `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED` | L175 "control-expectation diagnostic for validating the closed halt-signature component domains and mapping" | pack |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `design_id_values` | array of strings | [`FIFO`, `UART`] | L185 "`design_id` is `FIFO` or `UART`", in that order | pack; order OD-3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `halt_code_values` | array of strings | [`SIMULATOR_ERROR`, `TRACE_INTEGRITY_FAILURE`, `RTL_NULL_CONTROL_FAILURE`] | L185 "`halt_code` is `SIMULATOR_ERROR`, `TRACE_INTEGRITY_FAILURE` or `RTL_NULL_CONTROL_FAILURE`", in that order | pack; order OD-3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `evaluator_component_values` | array of strings | [`SIMULATOR`, `REPLAY_VERIFIER`, `RECORDER`, `TRACE_ALIGNMENT_CHECKER`, `TRACE_SERIALIZER`, `RTL_NULL_COMPARATOR`] | L185 "`evaluator_component` is `SIMULATOR`, `REPLAY_VERIFIER`, `RECORDER`, `TRACE_ALIGNMENT_CHECKER`, `TRACE_SERIALIZER` or `RTL_NULL_COMPARATOR`", in that order | pack; order OD-3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `stable_error_class_rule` | string | `simple_exception_class_for_SIMULATOR_ERROR_else_NONE` | L185: the label of the `stable_error_class` rule stated there | C3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `stable_diagnostic_code_rule` | string | `exact_halt_code_token` | L185: the label of the `stable_diagnostic_code` rule stated there | C3 |

### 20.4 The other control vectors (schemas stated elsewhere, listed for completeness)

| Vector | Result properties besides `disposition`, `stage_id` and `error_class` | Where fixed | Basis |
| --- | --- | --- | --- |
| Serializer-grammar vector (File 36 L195) | `diagnostic` = `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` | L168, L174 | C12, OD-1 |
| Truncation-primitive vector (File 36 L196) | `contains_marker` (Boolean), `valid_utf8` (Boolean), `output_diagnostic_bytes` (integer), `marker_utf8_bytes` (integer); no `diagnostic` | L168, L174 | C13 |
| JSON-escaping-primitive vector (File 36 L197) | `diagnostic_utf8` (string), `diagnostic_sha256` (string of 64 lowercase hexadecimal digits), `diagnostic_bytes` (integer); no `diagnostic` | L168, L174 | C14 |
| Parser unit vector (File 36 L27) | `diagnostic` by the L127 column rule | File 36 L27 | C9 |
| Operational-recovery vector (File 36 L205) | `diagnostic` = `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS`, `discard_pre_halt_scores` (Boolean `true`), `rerun_slots` (integer, equal to the input `scheduled_slots`), `reuse_same_artifact_bytes` (Boolean `true`), `new_confirmatory_generation_calls` (integer `0`); or the `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` result of §20.2–§20.3 | L175, L183, L185 | OS-1 |

The lifecycle halt-event vector (File 36 L198) and the design-preflight vector (File 36 L199) give stage-map records with the four comparison keys. They are not control-vector results.
```

## E199 — OD-2 · `41_F18_Fixture_Inputs/M27.json` Lall · D1-3, D1-4 · fixtures: M27

Old:

```text
{
  "fixture_id": "M27",
  "fixture_version": "1.3.7-candidate, not audited",
  "scope": "missing-case",
  "description": "Driver vector passes the key, type, width and symbol checks and violates the supplied legal-input predicate",
  "manifest_clause_ids": [
    "FIFO-001"
  ],
  "input": {
    "driver_return": {
      "wr_en": "1"
    },
    "input_port_widths": {
      "wr_en": 1
    },
    "sampled_outputs": {
      "full": "1"
    },
    "legal_input_predicate": {
      "language": "python3.11",
      "function": "legal_input",
      "source": "def legal_input(vector, sampled):\n    return not (sampled[\"full\"] == \"1\" and vector[\"wr_en\"] == \"1\")\n"
    }
  },
  "expected": {
    "disposition": "REPAIR",
    "stage_id": "DRIVER_VECTOR",
    "error_class": "DRIVER_VECTOR_INVALID",
    "diagnostic": "DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE"
  }
}
```

New:

```text
{
  "fixture_id": "M27",
  "fixture_version": "1.3.7-candidate, not audited",
  "scope": "missing-case",
  "description": "Driver vector passes the key, type, width and symbol checks and violates the supplied legal-input predicate",
  "manifest_clause_ids": [
    "FIFO-001"
  ],
  "input": {
    "driver_return": {
      "wr_en": "1"
    },
    "input_port_widths": {
      "wr_en": 1
    },
    "sampled_outputs": {
      "full": "1"
    },
    "legal_input_predicate": {
      "language": "python3.11",
      "function": "legal_input",
      "source": "def legal_input(vector, sampled):\n    return not (sampled[\"full\"] == \"1\" and vector[\"wr_en\"] == \"1\")\n",
      "source_sha256": "bc3d897f8b118b6a366453a24923f1a75683472f05372907df23286653fe6154"
    }
  },
  "expected": {
    "disposition": "REPAIR",
    "stage_id": "DRIVER_VECTOR",
    "error_class": "DRIVER_VECTOR_INVALID",
    "diagnostic": "DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE"
  }
}
```

## E200 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L510 · — · fixtures: M37

Old:

```text
"sha256": "1498ec86204bbc434f5baeb2f16c862ec655d161a3ff016ae717348961bfdd19",
```

New:

```text
"sha256": "3d3a1855eb0609de81ccc72349b9afdaf23768849ffb7a8546006253eb1b6300",
```

## E201 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L511 · — · fixtures: M37

Old:

```text
"bytes": 1595,
```

New:

```text
"bytes": 1753,
```

## E202 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L752 · — · fixtures: M54

Old:

```text
"sha256": "96828e2572f59c74d879aa72dfef0d15f4eb6b6c7e97f3a4331db9ad46a6cac4",
```

New:

```text
"sha256": "c6dfe1caff678f305fa8a855f49c04c209c7a494df91917415c083b482405890",
```

## E203 — derived · `41_F18_Fixture_Inputs/fixture-index.json` L753 · — · fixtures: M54

Old:

```text
"bytes": 1350,
```

New:

```text
"bytes": 1378,
```

## E204 — derived · `27_SHA256SUMS.txt` L76 · — · fixtures: —

Old:

```text
1498ec86204bbc434f5baeb2f16c862ec655d161a3ff016ae717348961bfdd19  41_F18_Fixture_Inputs/M37.json
```

New:

```text
3d3a1855eb0609de81ccc72349b9afdaf23768849ffb7a8546006253eb1b6300  41_F18_Fixture_Inputs/M37.json
```

## E205 — derived · `27_SHA256SUMS.txt` L93 · — · fixtures: —

Old:

```text
96828e2572f59c74d879aa72dfef0d15f4eb6b6c7e97f3a4331db9ad46a6cac4  41_F18_Fixture_Inputs/M54.json
```

New:

```text
c6dfe1caff678f305fa8a855f49c04c209c7a494df91917415c083b482405890  41_F18_Fixture_Inputs/M54.json
```

## E206 — C18 · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L7 · D2-1 · fixtures: all

Old:

```text
| Check | Required pass condition | Status |
```

New:

```text
| Check | Required pass condition | Status (NOT RUN here is the formal F18 status; for development-run evidence and approval see "F18 result" below) |
```

## E207 — C18 · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L26 · D2-1 · fixtures: all

Old:

```text
RECORDED; F18 NOT RUN
```

New:

```text
RECORDED; formal F18 status NOT RUN (development-run evidence is not F18 acceptance; nothing is approved)
```

## E208 — C18 · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L40 · D2-1 · fixtures: all

Old:

```text
| Fixture family | Mandatory IDs | Status |
```

New:

```text
| Fixture family | Mandatory IDs | Status (NOT RUN here is the formal F18 status; for development-run evidence and approval see "F18 result" below) |
```

## E209 — C18 · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L52 · D2-1 · fixtures: all

Old:

```text
F18 is **NOT RUN / NOT PASSED**.
```

New:

```text
F18 status, in three separate parts: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.
```

## E210 — C18 · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L69 · D2-1 · fixtures: all

Old:

```text
until F18 is actually executed;
```

New:

```text
until a formal F18 acceptance run is executed (development runs are not F18 acceptance and do not set them; nothing is approved);
```

## E211 — C18 · `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` (was `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.6.md` L70 · D2-1 · fixtures: all

Old:

```text
- Current release status: F18 **NOT RUN / NOT PASSED**;
```

New:

```text
- Current release status: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved;
```

## E212 — C18 · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` L177 · D2-1 · fixtures: all

Old:

```text
**F1–F18:** not run; all must pass on FIFO.
```

New:

```text
**F1–F18:** formal status not run, since no authorized F1–F18 acceptance run exists (development-run evidence: runs of a project implementation, recorded outside this pack, are development runs, not F1–F18 acceptance; approval: nothing is qualified or approved); all must pass on FIFO.
```

## E213 — C18 · `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` (was `01_OpenVEF_Project_Charter_v1.3.6.md` L194 · D2-1 · fixtures: all

Old:

```text
No parser, assembler, harness or fixture suite has been executed.
```

New:

```text
That response executed no parser, assembler, harness or fixture suite. Current status, in three separate parts: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.
```

## E214 — C18 · `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` (was `30_Response_Parser_and_Execution_Contract_v1.3.6.md` L3 · D2-1 · fixtures: all

Old:

```text
Not implemented, frozen or executable until owner acceptance, independent re-audit, and runtime pinning.
```

New:

```text
Not frozen, and not executable for F18 acceptance, until owner acceptance, independent re-audit, and runtime pinning. Status, in three separate parts: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.
```

## E215 — C18 · `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` (was `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.6.md` L3 · D2-1 · fixtures: all

Old:

```text
Not frozen until independent review and owner approval.
```

New:

```text
Not frozen until independent review and owner approval. Status, in three separate parts: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.
```

## E216 — C18 · `README.md` L19 · D2-1 · fixtures: —

Old:

```text
pinned-runtime Unicode test remains NOT RUN.
```

New:

```text
pinned-runtime Unicode test: formal status NOT RUN (development runs of a project implementation, recorded outside this pack, are not this check; nothing is approved).
```

## E217 — C18 · `41_F18_Fixture_Inputs/fixture-index.json` L4 · D2-1 · fixtures: all

Old:

```text
"execution_status": "NOT RUN / NOT PASSED",
```

New:

```text
"execution_status": "formal F18 status NOT RUN / NOT PASSED, since no authorized F18 acceptance run exists; development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; approval: no implementation is qualified or approved",
```

## E218 — C18 · `41_F18_Fixture_Inputs/fixture-index.json` L1931 · D2-1 · fixtures: all

Old:

```text
"status": "NOT RUN / NOT PASSED"
```

New:

```text
"status": "formal F18 status NOT RUN / NOT PASSED, since no authorized F18 acceptance run exists; development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; approval: no implementation is qualified or approved"
```
