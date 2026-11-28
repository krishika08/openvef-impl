# v1.3.7 CANDIDATE, not audited

**Every file in this directory is part of OpenVEF Planning v1.3.7 CANDIDATE, not audited.** It is a copy of v1.3.6 with
corrections C1–C16 and amendments A1–A2 applied (owner decisions D-024, D-025) and the OWNER-SPECIFIED
items OS-1–OS-3 (owner decision D-026; `CHANGELOG-v1.3.7-candidate.md`), and with correction cycle 2 (owner
decision D-027: OWNER-DECIDED rules OD-n and numbered amendments) after document audit #1 of cycle 1
(NOT CLEARED), and with correction cycle 3 (owner decision D-029: C18, the three-part status wording) after
document audit #2 (NOT CLEARED), and with correction cycle 4 (owner decision D-030: C19, the three parts as
explicit labels) after document audit #3 (NOT CLEARED). It is not released, not audit-cleared and not approved, and v1.3.6 (`baseline/`) remains
the default pack.

- **In-file label:** every file a correction changed carries the label itself (Markdown and File 25: an
  appended trailer, in File 25 after its last line and outside the model-visible bodies; fixture JSON:
  `fixture_version` / `fixture_index_version`). `27_SHA256SUMS.txt` is changed
  (derived hashes) but cannot carry text without breaking its format; it is labelled here.
- **Labelled by this file:** every other file is byte-identical to v1.3.6 (JSON, CSV, prompt templates
  and verbatim audit records cannot be edited without changing bytes that tools or provenance depend on).
- `SHA256SUMS-v1.3.7-candidate.txt` lists the SHA-256 of every file here except itself.

| File | Status |
|---|---|
| `01_OpenVEF_Project_Charter_v1.3.7-candidate.md` | changed; labelled in-file |
| `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md` | changed; labelled in-file |
| `03_Change_Log_v1.3.1_Historical.md` | identical to v1.3.6; labelled here |
| `03_Change_Log_v1.3.6.md` | identical to v1.3.6; labelled here |
| `04_Verify_the_Verifier_Paper_Analysis.md` | identical to v1.3.6; labelled here |
| `05_Claude_Audit_Resolution.md` | identical to v1.3.6; labelled here |
| `06_Functional_Qualification_and_Mutation_Analysis.md` | identical to v1.3.6; labelled here |
| `07_Claude_Step1_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `08_Claude_Step2_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `09_Claude_Step2_Audit_Resolution.md` | identical to v1.3.6; labelled here |
| `10_LLM_Era_Hardware_Verification_Literature_Review.md` | changed; labelled in-file |
| `11_Comparative_Research_Matrix.md` | changed; labelled in-file |
| `12_OpenVEF_Candidate_Gap_Assessment.md` | identical to v1.3.6; labelled here |
| `14_Claude_Step3_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `15_Claude_Step3_Audit_Resolution.md` | identical to v1.3.6; labelled here |
| `16_OpenVEF_v1.3.6_Owner_Decision_Register.md` | identical to v1.3.6; labelled here |
| `17_Step3_Literature_Audit_Addendum_v0.7.md` | identical to v1.3.6; labelled here |
| `19_ORG_A_Prompt_Template.txt` | identical to v1.3.6; labelled here |
| `20_ORG_B_Prompt_Template.txt` | identical to v1.3.6; labelled here |
| `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md` | changed; labelled in-file |
| `22_Source_Access_Provenance_Log_v1.2.md` | changed; labelled in-file |
| `23_Owner_Approval_Record_v1.3.6.md` | identical to v1.3.6; labelled here |
| `24_Mask_to_Specification_Traceability_Template.csv` | identical to v1.3.6; labelled here |
| `25_Common_System_and_Repair_Prompt_Templates.txt` | changed; labelled in-file |
| `26_Claude_v0.6_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `27_SHA256SUMS.txt` | changed (derived); labelled here |
| `28_Claude_v0.7_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `29_Claude_v0.8_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` | changed; labelled in-file |
| `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md` | changed; labelled in-file |
| `32_v1.3.7-candidate_Status_and_Gates.md` | changed; labelled in-file |
| `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json` | changed; labelled in-file |
| `34_OpenVEF_Response_Schema_v1.0.json` | identical to v1.3.6; labelled here |
| `35_Claude_v0.8_Audit_Resolution_v0.9.md` | identical to v1.3.6; labelled here |
| `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` | changed; labelled in-file |
| `37_Claude_v0.9_Independent_Audit_Prompt.txt` | identical to v1.3.6; labelled here |
| `38_Authoring_Packet_Manifest_Template_v1.3.7-candidate.json` | changed; labelled in-file |
| `39_Claude_v0.9_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M01.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M02.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M03.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M04a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M04b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M05.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M06.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M07.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M08a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M08b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M09.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M10.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M11.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M12.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M13.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M14.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M15.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M16.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M17.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M18.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M19.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M20.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M21.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M22.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M23.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M24.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M25.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M26.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M27.json` | changed; labelled in-file |
| `41_F18_Fixture_Inputs/M28.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M29.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M30.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M31.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M32.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M33.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M34.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M35.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M36.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M37.json` | changed; labelled in-file |
| `41_F18_Fixture_Inputs/M38.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M39.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M40.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M41.json` | changed; labelled in-file |
| `41_F18_Fixture_Inputs/M42.json` | changed; labelled in-file |
| `41_F18_Fixture_Inputs/M43.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M44.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M45.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M46.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M47.json` | changed; labelled in-file |
| `41_F18_Fixture_Inputs/M48.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M49.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M50.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M51.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M52.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M53.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M54.json` | changed; labelled in-file |
| `41_F18_Fixture_Inputs/M55.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M56.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M57.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M58.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M59.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M60.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M61.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M62.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M63.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M64.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M65.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M66.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M67.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M68.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M69.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/M70.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P01.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P02.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P03.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P04.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P05.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P06a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P06b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P07.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P08a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P08b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P08c.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P08d.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P09.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P10.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P11a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P11b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P12a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P12b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P13.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P14.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P15.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P16.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P17.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P18.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P19.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P20.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P21.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P22.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P23.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P24a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P24b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P24c.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P24d.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P25a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P25b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P26.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P27.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P28.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P29a.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P29b.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P30.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P31.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P32.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P33.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P34.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P35.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P36.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P37.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P38.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P39.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P40.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P41.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P42.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P43.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P44.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P45.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P46.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P47.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/P48.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R01.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R02.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R03.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R04.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R05.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R06.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R07.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R08.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R09.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R10.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R11.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R12.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/R13.json` | identical to v1.3.6; labelled here |
| `41_F18_Fixture_Inputs/fixture-index.json` | changed; labelled in-file |
| `42_Claude_v1.0_Independent_Audit_Prompt_Historical.txt` | identical to v1.3.6; labelled here |
| `43_Claude_v1.0_Audit_Raw.txt` | identical to v1.3.6; labelled here |
| `44_Claude_v1.0_Audit_Resolution_v1.1.md` | identical to v1.3.6; labelled here |
| `45_Claude_v1.1_Independent_Audit_Prompt.txt` | identical to v1.3.6; labelled here |
| `46_Claude_v1.1_Audit_Tracker_Snapshot.md` | identical to v1.3.6; labelled here |
| `47_Claude_v1.1_Audit_Resolution_v1.2.md` | identical to v1.3.6; labelled here |
| `48_Claude_v1.3.1_Independent_Audit_Prompt_Historical.txt` | identical to v1.3.6; labelled here |
| `48_Claude_v1.3.6_Independent_Audit_Prompt.txt` | identical to v1.3.6; labelled here |
| `50_Python311_Unicode_Tokenizer_Check.md` | identical to v1.3.6; labelled here |
| `54_OpenVEF_v1.3.1_Independent_Audit.md` | identical to v1.3.6; labelled here |
| `55_OpenVEF_v1.3.2_Audit_Summary_Owner_Supplied.md` | identical to v1.3.6; labelled here |
| `56_v1.3.6_Static_Build_Checks.json` | identical to v1.3.6; labelled here |
| `57_v1.3.6_Build_Integrity_Record.md` | identical to v1.3.6; labelled here |
| `58_v1.3.6_Correction_Resolution.md` | identical to v1.3.6; labelled here |
| `59_OpenVEF_v1.3.3_Independent_Audit.md` | identical to v1.3.6; labelled here |
| `60_v1.3.2_Audit_Export_Status.md` | identical to v1.3.6; labelled here |
| `61_OpenVEF_v1.3.4_Independent_Audit.md` | identical to v1.3.6; labelled here |
| `62_OpenVEF_v1.3.2_Independent_Audit.md` | identical to v1.3.6; labelled here |
| `63_OpenVEF_v1.3.5_Audit_Summary_Owner_Supplied.md` | identical to v1.3.6; labelled here |
| `CHANGELOG-v1.3.7-candidate.md` | candidate record; labelled in-file |
| `README.md` | changed; labelled in-file |
| `CANDIDATE-LABEL.md` | candidate record; labelled in-file |
| `SHA256SUMS-v1.3.7-candidate.txt` | candidate record; labelled in-file |
