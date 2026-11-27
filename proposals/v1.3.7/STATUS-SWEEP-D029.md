# Status-statement sweep of the v1.3.7 CANDIDATE (D-029 item 1; C18)

**v1.3.7 CANDIDATE, not audited.** Written by Claude (Claude Opus 5.5, via Claude Code), the author of the corrections,
under owner decision D-029 (Krishika). Rationale: `CORRECTIONS-v1.3.7-candidate.md` section 12.

**Method.** Every line of `proposals/v1.3.7/pack/` (after C18) that matches, case-insensitively, `NOT RUN`, `NOT PASSED`,
`PASSED` or the word `status` (also `…_status` JSON keys), or that mentions F18 together with `executed`, `implemented`
or `acceptance run`. F18 alone matches 1,100+ lines that name the gate, not its status; those were read through the
second pattern. Not swept: the candidate's own derived files (`CHANGELOG-v1.3.7-candidate.md`, `CANDIDATE-LABEL.md`,
`SHA256SUMS-v1.3.7-candidate.txt`, `27_SHA256SUMS.txt`) and the one-line candidate trailer.

**Current and historical** follow section 6 (D-025 item 3, approved under D-026 item 1): the current documents are Files
01, 02, 21, 30, 31, 32, 33, 36, 38, the README and the fixture index; history is the change logs, build, correction and
audit records, audit transcripts and prompts, research and provenance records, and the owner records (Files 16, 23),
which are not rewritten. A historical line inside a current document (what an earlier audit or release did) is kept.

**Classes.**
- **FIXED (C18):** a current status statement that lacked the three-part split; now has development-run evidence, formal
  F18 status and approval (CHANGELOG entry given).
- **ALREADY THREE-PART (C17):** fixed in cycle 2.
- **COVERED BY HEADER (C18):** a File 21 table cell `NOT RUN`; the column header (L7, L40, fixed) names it the formal F18
  status and points to L52 for the other two parts.
- **CURRENT, NOT AN F18 STATUS:** a document, audit, freeze or reviewer status, or a heading; it makes no run, pass or
  implementation claim, so the split does not apply. Unchanged.
- **NOT A STATUS STATEMENT:** the word is used in another sense (a checker's error status, a provider truncation status,
  model-visible template text). Unchanged.
- **HISTORICAL:** records an earlier release, audit or decision. Unchanged.

**Check.** `tests/test_v137_candidate_pack.py` `test_current_status_lines_have_three_parts` fails if a current document
has a line with a status term that mentions F18 and lacks any of the three parts, except the lines listed there with
their reason.

**Counts:** 342 lines in 59 files. FIXED 13; ALREADY THREE-PART 8; COVERED BY HEADER 24; CURRENT, NOT AN F18 STATUS 36; NOT A STATUS STATEMENT 23; HISTORICAL 238.

| # | File | Line | Class | Note |
|---|---|---|---|---|
| 1 | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | 6 | CURRENT, NOT AN F18 STATUS | document status (DESIGN DRAFT, owner acceptance pending); no run, pass or implementation claim |
| 2 | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | 9 | HISTORICAL | Status note on the v1.3–v1.3.5 audits; 'all 144 fixtures still NOT RUN / NOT PASSED' is what the v1.3.5 audit result reports (kept under C17) |
| 3 | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | 177 | FIXED (C18, E212) |  |
| 4 | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | 178 | CURRENT, NOT AN F18 STATUS | F16 pilot: needs LLM calls; none was made in any run, so 'not run' is true in every sense |
| 5 | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | 187 | HISTORICAL | heading of §17, labelled historical |
| 6 | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | 192 | CURRENT, NOT AN F18 STATUS | heading of §18; the status it heads is L194 |
| 7 | `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | 194 | FIXED (C18, E213) |  |
| 8 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 6 | CURRENT, NOT AN F18 STATUS | document status (DESIGN DRAFT; no work authorized until A1–A11 and X14) |
| 9 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 9 | CURRENT, NOT AN F18 STATUS | points to §19 for the status; L559 carries the three parts |
| 10 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 81 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 11 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 161 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 12 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 164 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 13 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 223 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 14 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 284 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 15 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 437 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 16 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 462 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 17 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 464 | CURRENT, NOT AN F18 STATUS | column of TO FREEZE planning values |
| 18 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 525 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 19 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 557 | CURRENT, NOT AN F18 STATUS | heading of §19; the status it heads is L559 |
| 20 | `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | 559 | ALREADY THREE-PART (C17, E195) |  |
| 21 | `03_Change_Log_v1.3.1_Historical.md` | 4 | HISTORICAL | change log of v1.3.6 and earlier |
| 22 | `03_Change_Log_v1.3.1_Historical.md` | 34 | HISTORICAL | change log of v1.3.6 and earlier |
| 23 | `03_Change_Log_v1.3.1_Historical.md` | 35 | HISTORICAL | change log of v1.3.6 and earlier |
| 24 | `03_Change_Log_v1.3.1_Historical.md` | 49 | HISTORICAL | change log of v1.3.6 and earlier |
| 25 | `03_Change_Log_v1.3.1_Historical.md` | 54 | HISTORICAL | change log of v1.3.6 and earlier |
| 26 | `03_Change_Log_v1.3.1_Historical.md` | 65 | HISTORICAL | change log of v1.3.6 and earlier |
| 27 | `03_Change_Log_v1.3.1_Historical.md` | 69 | HISTORICAL | change log of v1.3.6 and earlier |
| 28 | `03_Change_Log_v1.3.6.md` | 10 | HISTORICAL | change log of v1.3.6 and earlier |
| 29 | `03_Change_Log_v1.3.6.md` | 11 | HISTORICAL | change log of v1.3.6 and earlier |
| 30 | `03_Change_Log_v1.3.6.md` | 24 | HISTORICAL | change log of v1.3.6 and earlier |
| 31 | `03_Change_Log_v1.3.6.md` | 25 | HISTORICAL | change log of v1.3.6 and earlier |
| 32 | `04_Verify_the_Verifier_Paper_Analysis.md` | 121 | HISTORICAL | research note (Step 1) |
| 33 | `04_Verify_the_Verifier_Paper_Analysis.md` | 139 | HISTORICAL | research note (Step 1) |
| 34 | `04_Verify_the_Verifier_Paper_Analysis.md` | 253 | HISTORICAL | research note (Step 1) |
| 35 | `04_Verify_the_Verifier_Paper_Analysis.md` | 261 | HISTORICAL | research note (Step 1) |
| 36 | `05_Claude_Audit_Resolution.md` | 28 | HISTORICAL | audit resolution |
| 37 | `06_Functional_Qualification_and_Mutation_Analysis.md` | 8 | HISTORICAL | research note (Step 2) |
| 38 | `06_Functional_Qualification_and_Mutation_Analysis.md` | 248 | HISTORICAL | research note (Step 2) |
| 39 | `06_Functional_Qualification_and_Mutation_Analysis.md` | 250 | HISTORICAL | research note (Step 2) |
| 40 | `06_Functional_Qualification_and_Mutation_Analysis.md` | 267 | HISTORICAL | research note (Step 2) |
| 41 | `07_Claude_Step1_Audit_Raw.txt` | 5 | HISTORICAL | audit transcript |
| 42 | `07_Claude_Step1_Audit_Raw.txt` | 73 | HISTORICAL | audit transcript |
| 43 | `07_Claude_Step1_Audit_Raw.txt` | 91 | HISTORICAL | audit transcript |
| 44 | `07_Claude_Step1_Audit_Raw.txt` | 98 | HISTORICAL | audit transcript |
| 45 | `07_Claude_Step1_Audit_Raw.txt` | 104 | HISTORICAL | audit transcript |
| 46 | `07_Claude_Step1_Audit_Raw.txt` | 322 | HISTORICAL | audit transcript |
| 47 | `07_Claude_Step1_Audit_Raw.txt` | 326 | HISTORICAL | audit transcript |
| 48 | `08_Claude_Step2_Audit_Raw.txt` | 13 | HISTORICAL | audit transcript |
| 49 | `08_Claude_Step2_Audit_Raw.txt` | 17 | HISTORICAL | audit transcript |
| 50 | `08_Claude_Step2_Audit_Raw.txt` | 73 | HISTORICAL | audit transcript |
| 51 | `08_Claude_Step2_Audit_Raw.txt` | 174 | HISTORICAL | audit transcript |
| 52 | `08_Claude_Step2_Audit_Raw.txt` | 300 | HISTORICAL | audit transcript |
| 53 | `09_Claude_Step2_Audit_Resolution.md` | 7 | HISTORICAL | audit resolution |
| 54 | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 5 | HISTORICAL | literature review; its status line is the review's own |
| 55 | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 8 | HISTORICAL | literature review; its status line is the review's own |
| 56 | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 155 | HISTORICAL | literature review; its status line is the review's own |
| 57 | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 168 | HISTORICAL | literature review; its status line is the review's own |
| 58 | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 180 | HISTORICAL | literature review; its status line is the review's own |
| 59 | `10_LLM_Era_Hardware_Verification_Literature_Review.md` | 287 | HISTORICAL | literature review; its status line is the review's own |
| 60 | `11_Comparative_Research_Matrix.md` | 5 | HISTORICAL | source-comparison record |
| 61 | `12_OpenVEF_Candidate_Gap_Assessment.md` | 3 | HISTORICAL | v1.2 gap assessment, dated 22 Nov 2026 |
| 62 | `12_OpenVEF_Candidate_Gap_Assessment.md` | 114 | HISTORICAL | v1.2 gap assessment, dated 22 Nov 2026 |
| 63 | `14_Claude_Step3_Audit_Raw.txt` | 31 | HISTORICAL | audit transcript |
| 64 | `14_Claude_Step3_Audit_Raw.txt` | 38 | HISTORICAL | audit transcript |
| 65 | `14_Claude_Step3_Audit_Raw.txt` | 64 | HISTORICAL | audit transcript |
| 66 | `14_Claude_Step3_Audit_Raw.txt` | 67 | HISTORICAL | audit transcript |
| 67 | `14_Claude_Step3_Audit_Raw.txt` | 102 | HISTORICAL | audit transcript |
| 68 | `14_Claude_Step3_Audit_Raw.txt` | 104 | HISTORICAL | audit transcript |
| 69 | `14_Claude_Step3_Audit_Raw.txt` | 367 | HISTORICAL | audit transcript |
| 70 | `15_Claude_Step3_Audit_Resolution.md` | 7 | HISTORICAL | audit resolution |
| 71 | `15_Claude_Step3_Audit_Resolution.md` | 8 | HISTORICAL | audit resolution |
| 72 | `15_Claude_Step3_Audit_Resolution.md` | 19 | HISTORICAL | audit resolution |
| 73 | `15_Claude_Step3_Audit_Resolution.md` | 44 | HISTORICAL | audit resolution |
| 74 | `15_Claude_Step3_Audit_Resolution.md` | 84 | HISTORICAL | audit resolution |
| 75 | `15_Claude_Step3_Audit_Resolution.md` | 86 | HISTORICAL | audit resolution |
| 76 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 4 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 77 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 8 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 78 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 20 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 79 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 54 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 80 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 66 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 81 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 77 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 82 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 84 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 83 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 91 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 84 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 97 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 85 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 126 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 86 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 132 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 87 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 135 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 88 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 150 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 89 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 155 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 90 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 161 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 91 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 166 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 92 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 170 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 93 | `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | 173 | HISTORICAL | owner record of decisions on v1.3.6 (section 6: not rewritten) |
| 94 | `17_Step3_Literature_Audit_Addendum_v0.7.md` | 25 | HISTORICAL | literature-audit addendum v0.7 |
| 95 | `17_Step3_Literature_Audit_Addendum_v0.7.md` | 33 | HISTORICAL | literature-audit addendum v0.7 |
| 96 | `19_ORG_A_Prompt_Template.txt` | 38 | NOT A STATUS STATEMENT | ORG-A prompt template (model-visible; byte-frozen) |
| 97 | `20_ORG_B_Prompt_Template.txt` | 35 | NOT A STATUS STATEMENT | ORG-B prompt template (model-visible; byte-frozen) |
| 98 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 7 | FIXED (C18, E206) |  |
| 99 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 9 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 100 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 10 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 101 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 11 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 102 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 12 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 103 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 13 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 104 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 14 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 105 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 15 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 106 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 16 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 107 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 17 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 108 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 18 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 109 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 19 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 110 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 20 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 111 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 21 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 112 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 22 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 113 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 24 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 114 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 25 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 115 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 26 | FIXED (C18, E207) |  |
| 116 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 27 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 117 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 30 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 118 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 34 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 119 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 40 | FIXED (C18, E208) |  |
| 120 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 42 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 121 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 43 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 122 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 44 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 123 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 45 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 124 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 46 | COVERED BY HEADER (C18) | cell NOT RUN under the column header fixed at L7 / L40, which names it the formal F18 status and points to 'F18 result' (L52) for the other two parts |
| 125 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 52 | FIXED (C18, E209) |  |
| 126 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 69 | FIXED (C18, E210) |  |
| 127 | `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | 70 | FIXED (C18, E211) |  |
| 128 | `22_Source_Access_Provenance_Log_v1.2.md` | 4 | HISTORICAL | source provenance log |
| 129 | `23_Owner_Approval_Record_v1.3.6.md` | 4 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 130 | `23_Owner_Approval_Record_v1.3.6.md` | 64 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 131 | `23_Owner_Approval_Record_v1.3.6.md` | 66 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 132 | `23_Owner_Approval_Record_v1.3.6.md` | 68 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 133 | `23_Owner_Approval_Record_v1.3.6.md` | 77 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 134 | `23_Owner_Approval_Record_v1.3.6.md` | 79 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 135 | `23_Owner_Approval_Record_v1.3.6.md` | 84 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 136 | `23_Owner_Approval_Record_v1.3.6.md` | 88 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 137 | `23_Owner_Approval_Record_v1.3.6.md` | 93 | HISTORICAL | owner approval record of v1.3.6 (section 6: not rewritten) |
| 138 | `24_Mask_to_Specification_Traceability_Template.csv` | 1 | NOT A STATUS STATEMENT | mask template CSV header |
| 139 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 104 | NOT A STATUS STATEMENT | common prompt templates / File 25 copy of Protocol text |
| 140 | `25_Common_System_and_Repair_Prompt_Templates.txt` | 107 | NOT A STATUS STATEMENT | common prompt templates / File 25 copy of Protocol text |
| 141 | `26_Claude_v0.6_Audit_Raw.txt` | 18 | HISTORICAL | audit transcript |
| 142 | `26_Claude_v0.6_Audit_Raw.txt` | 32 | HISTORICAL | audit transcript |
| 143 | `26_Claude_v0.6_Audit_Raw.txt` | 73 | HISTORICAL | audit transcript |
| 144 | `28_Claude_v0.7_Audit_Raw.txt` | 13 | HISTORICAL | audit transcript |
| 145 | `28_Claude_v0.7_Audit_Raw.txt` | 15 | HISTORICAL | audit transcript |
| 146 | `28_Claude_v0.7_Audit_Raw.txt` | 277 | HISTORICAL | audit transcript |
| 147 | `28_Claude_v0.7_Audit_Raw.txt` | 368 | HISTORICAL | audit transcript |
| 148 | `28_Claude_v0.7_Audit_Raw.txt` | 399 | HISTORICAL | audit transcript |
| 149 | `28_Claude_v0.7_Audit_Raw.txt` | 414 | HISTORICAL | audit transcript |
| 150 | `28_Claude_v0.7_Audit_Raw.txt` | 468 | HISTORICAL | audit transcript |
| 151 | `29_Claude_v0.8_Audit_Raw.txt` | 16 | HISTORICAL | audit transcript |
| 152 | `29_Claude_v0.8_Audit_Raw.txt` | 21 | HISTORICAL | audit transcript |
| 153 | `29_Claude_v0.8_Audit_Raw.txt` | 286 | HISTORICAL | audit transcript |
| 154 | `29_Claude_v0.8_Audit_Raw.txt` | 310 | HISTORICAL | audit transcript |
| 155 | `29_Claude_v0.8_Audit_Raw.txt` | 332 | HISTORICAL | audit transcript |
| 156 | `29_Claude_v0.8_Audit_Raw.txt` | 348 | HISTORICAL | audit transcript |
| 157 | `29_Claude_v0.8_Audit_Raw.txt` | 351 | HISTORICAL | audit transcript |
| 158 | `29_Claude_v0.8_Audit_Raw.txt` | 368 | HISTORICAL | audit transcript |
| 159 | `29_Claude_v0.8_Audit_Raw.txt` | 374 | HISTORICAL | audit transcript |
| 160 | `29_Claude_v0.8_Audit_Raw.txt` | 377 | HISTORICAL | audit transcript |
| 161 | `29_Claude_v0.8_Audit_Raw.txt` | 378 | HISTORICAL | audit transcript |
| 162 | `29_Claude_v0.8_Audit_Raw.txt` | 380 | HISTORICAL | audit transcript |
| 163 | `29_Claude_v0.8_Audit_Raw.txt` | 391 | HISTORICAL | audit transcript |
| 164 | `29_Claude_v0.8_Audit_Raw.txt` | 465 | HISTORICAL | audit transcript |
| 165 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` | 3 | FIXED (C18, E214) |  |
| 166 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` | 20 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 167 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` | 33 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 168 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` | 62 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 169 | `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` | 93 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 170 | `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` | 3 | FIXED (C18, E215) |  |
| 171 | `32_v1.3.7-candidate_Status_and_Gates.md` | 1 | CURRENT, NOT AN F18 STATUS | title or section heading; the statuses are on the lines below |
| 172 | `32_v1.3.7-candidate_Status_and_Gates.md` | 5 | CURRENT, NOT AN F18 STATUS | document-audit status (candidate NOT AUDITED) |
| 173 | `32_v1.3.7-candidate_Status_and_Gates.md` | 11 | HISTORICAL | what the v1.3.4 and v1.3.5 audits found |
| 174 | `32_v1.3.7-candidate_Status_and_Gates.md` | 16 | CURRENT, NOT AN F18 STATUS | title or section heading; the statuses are on the lines below |
| 175 | `32_v1.3.7-candidate_Status_and_Gates.md` | 21 | ALREADY THREE-PART (C17, E190) |  |
| 176 | `32_v1.3.7-candidate_Status_and_Gates.md` | 23 | CURRENT, NOT AN F18 STATUS | title or section heading; the statuses are on the lines below |
| 177 | `32_v1.3.7-candidate_Status_and_Gates.md` | 29 | CURRENT, NOT AN F18 STATUS | prompt template-stage status (design payloads unresolved) |
| 178 | `32_v1.3.7-candidate_Status_and_Gates.md` | 33 | ALREADY THREE-PART (C17, E191) |  |
| 179 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 136 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 180 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 141 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 181 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 146 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 182 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 151 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 183 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 156 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 184 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 161 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 185 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 166 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 186 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 177 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 187 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 186 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 188 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 206 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 189 | `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | 211 | CURRENT, NOT AN F18 STATUS | sidecar freeze status (TO_FREEZE / template-stage only); no run claim |
| 190 | `35_Claude_v0.8_Audit_Resolution_v0.9.md` | 5 | HISTORICAL | audit resolution |
| 191 | `35_Claude_v0.8_Audit_Resolution_v0.9.md` | 41 | HISTORICAL | audit resolution |
| 192 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` | 3 | ALREADY THREE-PART (C17, E188) |  |
| 193 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` | 48 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 194 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` | 176 | ALREADY THREE-PART (C17, E189) |  |
| 195 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` | 196 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 196 | `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` | 197 | NOT A STATUS STATEMENT | not a status statement: the word is used in another sense |
| 197 | `37_Claude_v0.9_Independent_Audit_Prompt.txt` | 12 | HISTORICAL | audit prompt |
| 198 | `37_Claude_v0.9_Independent_Audit_Prompt.txt` | 40 | HISTORICAL | audit prompt |
| 199 | `37_Claude_v0.9_Independent_Audit_Prompt.txt` | 56 | HISTORICAL | audit prompt |
| 200 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 3 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 201 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 13 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 202 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 19 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 203 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 25 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 204 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 31 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 205 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 37 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 206 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 43 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 207 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 49 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 208 | `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | 65 | CURRENT, NOT AN F18 STATUS | manifest freeze status (TO_FREEZE); no run claim |
| 209 | `39_Claude_v0.9_Audit_Raw.txt` | 8 | HISTORICAL | audit transcript |
| 210 | `39_Claude_v0.9_Audit_Raw.txt` | 251 | HISTORICAL | audit transcript |
| 211 | `39_Claude_v0.9_Audit_Raw.txt` | 258 | HISTORICAL | audit transcript |
| 212 | `39_Claude_v0.9_Audit_Raw.txt` | 269 | HISTORICAL | audit transcript |
| 213 | `39_Claude_v0.9_Audit_Raw.txt` | 478 | HISTORICAL | audit transcript |
| 214 | `39_Claude_v0.9_Audit_Raw.txt` | 595 | HISTORICAL | audit transcript |
| 215 | `41_F18_Fixture_Inputs/M14.json` | 14 | NOT A STATUS STATEMENT | fixture descriptor field (test_scope / description) |
| 216 | `41_F18_Fixture_Inputs/M17.json` | 20 | NOT A STATUS STATEMENT | fixture descriptor field (test_scope / description) |
| 217 | `41_F18_Fixture_Inputs/P11b.json` | 5 | NOT A STATUS STATEMENT | fixture descriptor field (test_scope / description) |
| 218 | `41_F18_Fixture_Inputs/fixture-index.json` | 4 | FIXED (C18, E217) |  |
| 219 | `41_F18_Fixture_Inputs/fixture-index.json` | 1931 | FIXED (C18, E218) |  |
| 220 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 8 | HISTORICAL | audit prompt (historical) |
| 221 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 10 | HISTORICAL | audit prompt (historical) |
| 222 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 51 | HISTORICAL | audit prompt (historical) |
| 223 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 57 | HISTORICAL | audit prompt (historical) |
| 224 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 59 | HISTORICAL | audit prompt (historical) |
| 225 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 62 | HISTORICAL | audit prompt (historical) |
| 226 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 67 | HISTORICAL | audit prompt (historical) |
| 227 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 70 | HISTORICAL | audit prompt (historical) |
| 228 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 75 | HISTORICAL | audit prompt (historical) |
| 229 | `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | 76 | HISTORICAL | audit prompt (historical) |
| 230 | `43_Claude_v1.0_Audit_Raw.txt` | 5 | HISTORICAL | audit transcript |
| 231 | `43_Claude_v1.0_Audit_Raw.txt` | 11 | HISTORICAL | audit transcript |
| 232 | `43_Claude_v1.0_Audit_Raw.txt` | 85 | HISTORICAL | audit transcript |
| 233 | `43_Claude_v1.0_Audit_Raw.txt` | 87 | HISTORICAL | audit transcript |
| 234 | `43_Claude_v1.0_Audit_Raw.txt` | 94 | HISTORICAL | audit transcript |
| 235 | `43_Claude_v1.0_Audit_Raw.txt` | 106 | HISTORICAL | audit transcript |
| 236 | `43_Claude_v1.0_Audit_Raw.txt` | 116 | HISTORICAL | audit transcript |
| 237 | `43_Claude_v1.0_Audit_Raw.txt` | 353 | HISTORICAL | audit transcript |
| 238 | `43_Claude_v1.0_Audit_Raw.txt` | 362 | HISTORICAL | audit transcript |
| 239 | `43_Claude_v1.0_Audit_Raw.txt` | 380 | HISTORICAL | audit transcript |
| 240 | `43_Claude_v1.0_Audit_Raw.txt` | 401 | HISTORICAL | audit transcript |
| 241 | `43_Claude_v1.0_Audit_Raw.txt` | 433 | HISTORICAL | audit transcript |
| 242 | `43_Claude_v1.0_Audit_Raw.txt` | 436 | HISTORICAL | audit transcript |
| 243 | `43_Claude_v1.0_Audit_Raw.txt` | 443 | HISTORICAL | audit transcript |
| 244 | `43_Claude_v1.0_Audit_Raw.txt` | 449 | HISTORICAL | audit transcript |
| 245 | `43_Claude_v1.0_Audit_Raw.txt` | 475 | HISTORICAL | audit transcript |
| 246 | `43_Claude_v1.0_Audit_Raw.txt` | 485 | HISTORICAL | audit transcript |
| 247 | `43_Claude_v1.0_Audit_Raw.txt` | 486 | HISTORICAL | audit transcript |
| 248 | `43_Claude_v1.0_Audit_Raw.txt` | 514 | HISTORICAL | audit transcript |
| 249 | `43_Claude_v1.0_Audit_Raw.txt` | 521 | HISTORICAL | audit transcript |
| 250 | `43_Claude_v1.0_Audit_Raw.txt` | 526 | HISTORICAL | audit transcript |
| 251 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 3 | HISTORICAL | audit resolution (v1.1) |
| 252 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 7 | HISTORICAL | audit resolution (v1.1) |
| 253 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 9 | HISTORICAL | audit resolution (v1.1) |
| 254 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 10 | HISTORICAL | audit resolution (v1.1) |
| 255 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 11 | HISTORICAL | audit resolution (v1.1) |
| 256 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 12 | HISTORICAL | audit resolution (v1.1) |
| 257 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 13 | HISTORICAL | audit resolution (v1.1) |
| 258 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 14 | HISTORICAL | audit resolution (v1.1) |
| 259 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 15 | HISTORICAL | audit resolution (v1.1) |
| 260 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 16 | HISTORICAL | audit resolution (v1.1) |
| 261 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 17 | HISTORICAL | audit resolution (v1.1) |
| 262 | `44_Claude_v1.0_Audit_Resolution_v1.1.md` | 34 | HISTORICAL | audit resolution (v1.1) |
| 263 | `45_Claude_v1.1_Independent_Audit_Prompt.txt` | 19 | HISTORICAL | audit prompt |
| 264 | `45_Claude_v1.1_Independent_Audit_Prompt.txt` | 26 | HISTORICAL | audit prompt |
| 265 | `45_Claude_v1.1_Independent_Audit_Prompt.txt` | 28 | HISTORICAL | audit prompt |
| 266 | `46_Claude_v1.1_Audit_Tracker_Snapshot.md` | 5 | HISTORICAL | v1.1 audit tracker snapshot |
| 267 | `46_Claude_v1.1_Audit_Tracker_Snapshot.md` | 10 | HISTORICAL | v1.1 audit tracker snapshot |
| 268 | `46_Claude_v1.1_Audit_Tracker_Snapshot.md` | 13 | HISTORICAL | v1.1 audit tracker snapshot |
| 269 | `46_Claude_v1.1_Audit_Tracker_Snapshot.md` | 16 | HISTORICAL | v1.1 audit tracker snapshot |
| 270 | `46_Claude_v1.1_Audit_Tracker_Snapshot.md` | 18 | HISTORICAL | v1.1 audit tracker snapshot |
| 271 | `47_Claude_v1.1_Audit_Resolution_v1.2.md` | 4 | HISTORICAL | audit resolution (v1.2) |
| 272 | `47_Claude_v1.1_Audit_Resolution_v1.2.md` | 27 | HISTORICAL | audit resolution (v1.2) |
| 273 | `48_Claude_v1.3.1_Independent_Audit_Prompt_Historical.txt` | 14 | HISTORICAL | v1.3.1 / v1.3.6 audit prompt |
| 274 | `48_Claude_v1.3.1_Independent_Audit_Prompt_Historical.txt` | 18 | HISTORICAL | v1.3.1 / v1.3.6 audit prompt |
| 275 | `48_Claude_v1.3.1_Independent_Audit_Prompt_Historical.txt` | 26 | HISTORICAL | v1.3.1 / v1.3.6 audit prompt |
| 276 | `48_Claude_v1.3.6_Independent_Audit_Prompt.txt` | 8 | HISTORICAL | v1.3.1 / v1.3.6 audit prompt |
| 277 | `48_Claude_v1.3.6_Independent_Audit_Prompt.txt` | 10 | HISTORICAL | v1.3.1 / v1.3.6 audit prompt |
| 278 | `48_Claude_v1.3.6_Independent_Audit_Prompt.txt` | 18 | HISTORICAL | v1.3.1 / v1.3.6 audit prompt |
| 279 | `50_Python311_Unicode_Tokenizer_Check.md` | 3 | HISTORICAL | v1.3.6 runtime-check record (section 6 history) |
| 280 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 26 | HISTORICAL | v1.3.1 audit |
| 281 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 46 | HISTORICAL | v1.3.1 audit |
| 282 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 57 | HISTORICAL | v1.3.1 audit |
| 283 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 69 | HISTORICAL | v1.3.1 audit |
| 284 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 249 | HISTORICAL | v1.3.1 audit |
| 285 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 262 | HISTORICAL | v1.3.1 audit |
| 286 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 306 | HISTORICAL | v1.3.1 audit |
| 287 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 315 | HISTORICAL | v1.3.1 audit |
| 288 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 317 | HISTORICAL | v1.3.1 audit |
| 289 | `54_OpenVEF_v1.3.1_Independent_Audit.md` | 341 | HISTORICAL | v1.3.1 audit |
| 290 | `56_v1.3.6_Static_Build_Checks.json` | 3 | HISTORICAL | v1.3.6 build record |
| 291 | `56_v1.3.6_Static_Build_Checks.json` | 4 | HISTORICAL | v1.3.6 build record |
| 292 | `56_v1.3.6_Static_Build_Checks.json` | 16 | HISTORICAL | v1.3.6 build record |
| 293 | `56_v1.3.6_Static_Build_Checks.json` | 44 | HISTORICAL | v1.3.6 build record |
| 294 | `56_v1.3.6_Static_Build_Checks.json` | 49 | HISTORICAL | v1.3.6 build record |
| 295 | `56_v1.3.6_Static_Build_Checks.json` | 55 | HISTORICAL | v1.3.6 build record |
| 296 | `57_v1.3.6_Build_Integrity_Record.md` | 3 | HISTORICAL | v1.3.6 build record |
| 297 | `57_v1.3.6_Build_Integrity_Record.md` | 21 | HISTORICAL | v1.3.6 build record |
| 298 | `57_v1.3.6_Build_Integrity_Record.md` | 32 | HISTORICAL | v1.3.6 build record |
| 299 | `58_v1.3.6_Correction_Resolution.md` | 10 | HISTORICAL | v1.3.6 correction record |
| 300 | `58_v1.3.6_Correction_Resolution.md` | 11 | HISTORICAL | v1.3.6 correction record |
| 301 | `58_v1.3.6_Correction_Resolution.md` | 25 | HISTORICAL | v1.3.6 correction record |
| 302 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 27 | HISTORICAL | v1.3.3 audit |
| 303 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 49 | HISTORICAL | v1.3.3 audit |
| 304 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 51 | HISTORICAL | v1.3.3 audit |
| 305 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 59 | HISTORICAL | v1.3.3 audit |
| 306 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 70 | HISTORICAL | v1.3.3 audit |
| 307 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 271 | HISTORICAL | v1.3.3 audit |
| 308 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 273 | HISTORICAL | v1.3.3 audit |
| 309 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 321 | HISTORICAL | v1.3.3 audit |
| 310 | `59_OpenVEF_v1.3.3_Independent_Audit.md` | 348 | HISTORICAL | v1.3.3 audit |
| 311 | `60_v1.3.2_Audit_Export_Status.md` | 1 | HISTORICAL | v1.3.2 audit-export record |
| 312 | `60_v1.3.2_Audit_Export_Status.md` | 3 | HISTORICAL | v1.3.2 audit-export record |
| 313 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 39 | HISTORICAL | v1.3.4 audit |
| 314 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 62 | HISTORICAL | v1.3.4 audit |
| 315 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 71 | HISTORICAL | v1.3.4 audit |
| 316 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 82 | HISTORICAL | v1.3.4 audit |
| 317 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 266 | HISTORICAL | v1.3.4 audit |
| 318 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 268 | HISTORICAL | v1.3.4 audit |
| 319 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 281 | HISTORICAL | v1.3.4 audit |
| 320 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 282 | HISTORICAL | v1.3.4 audit |
| 321 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 299 | HISTORICAL | v1.3.4 audit |
| 322 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 308 | HISTORICAL | v1.3.4 audit |
| 323 | `61_OpenVEF_v1.3.4_Independent_Audit.md` | 335 | HISTORICAL | v1.3.4 audit |
| 324 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 22 | HISTORICAL | v1.3.2 audit |
| 325 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 42 | HISTORICAL | v1.3.2 audit |
| 326 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 48 | HISTORICAL | v1.3.2 audit |
| 327 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 57 | HISTORICAL | v1.3.2 audit |
| 328 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 68 | HISTORICAL | v1.3.2 audit |
| 329 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 245 | HISTORICAL | v1.3.2 audit |
| 330 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 247 | HISTORICAL | v1.3.2 audit |
| 331 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 303 | HISTORICAL | v1.3.2 audit |
| 332 | `62_OpenVEF_v1.3.2_Independent_Audit.md` | 330 | HISTORICAL | v1.3.2 audit |
| 333 | `63_OpenVEF_v1.3.5_Audit_Summary_Owner_Supplied.md` | 20 | HISTORICAL | owner-supplied v1.3.5 audit summary |
| 334 | `README.md` | 3 | CURRENT, NOT AN F18 STATUS | pack status (candidate, not audited; v1.3.6 default) |
| 335 | `README.md` | 16 | ALREADY THREE-PART (C17, E192) |  |
| 336 | `README.md` | 19 | FIXED (C18, E216) |  |
| 337 | `README.md` | 21 | CURRENT, NOT AN F18 STATUS | describes File 60 (audit-export inclusion status) |
| 338 | `README.md` | 29 | HISTORICAL | list of what v1.3.6 changed |
| 339 | `README.md` | 33 | CURRENT, NOT AN F18 STATUS | section heading; the statuses are on the lines below |
| 340 | `README.md` | 35 | ALREADY THREE-PART (C17, E193) |  |
| 341 | `README.md` | 44 | CURRENT, NOT AN F18 STATUS | section heading; the statuses are on the lines below |
| 342 | `README.md` | 46 | ALREADY THREE-PART (C17, E194) |  |
