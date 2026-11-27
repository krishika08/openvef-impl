# OpenVEF — Independent Document Audit #3 — NOT CLEARED

**Pack:** OpenVEF Planning v1.3.7 CANDIDATE  
**Audit:** #3, correction C18 / D-029 status sweep and regression  
**Auditor:** GPT-6 (OpenAI), independent of the correction author  
**Operator:** Krishika  
**Audit date:** 27 November 2026  
**Overall status:** **NOT CLEARED**

This is a document audit of a candidate pack. It is not an implementation audit, does not run or pass F18, and approves nothing. v1.3.6 remains the default pack.

## 1. Bundle identity

**Uploaded ZIP:** `openvef-docaudit-bundle.zip`  
**ZIP size:** 1,255,057 bytes  
**SHA-256:**

```text
f82e13342664679e5caa8f56f42c5e6dde0ee1b04bab653fb7cc3c313290b26b
```

**Method: RUN.** Computed SHA-256 directly from the uploaded ZIP. All references in this report to the uploaded bundle refer to this exact hash.

## 2. Integrity checks

| Check | Method | Result |
|---|---|---|
| Uploaded ZIP SHA-256 | **RUN** — computed from the uploaded archive | PASS |
| `MANIFEST.sha256` | **RUN** — checked every listed entry | PASS, 425/425; no unlisted bundle files |
| Candidate `SHA256SUMS-v1.3.7-candidate.txt` | **RUN** — checked every candidate entry | PASS, 205/205; no unlisted candidate files |
| Baseline `27_SHA256SUMS.txt` | **RUN** — checked extracted baseline files | All extracted entries match |
| Missing baseline archive entries | **RUN** — compared checksum names with extraction | 61 `archive_*` entries are absent, as disclosed by the brief; they cannot be individually verified |
| Candidate rebuild | **RUN** — executed `build_candidate.py` into an isolated output directory | PASS; builder reports 218 edits and 206 files |
| Rebuilt candidate | **RUN** — compared every path and byte | PASS, 206/206 byte-identical |
| Candidate pack manifest hash | **RUN** — compared `BUNDLE-INFO.json` with run `summary.json` | MATCH: `3294d2a3920e6c06874535fc54dc037e2bc0461473cab33b6558b61f27a84eb1` |
| Current `results.jsonl` hash | **RUN** — computed file hash and compared to `summary.json` | MATCH: `4b9714a43e7dfb4d9833de986302bf5f9d476da200e4e6871e967b608329284b` |
| Audit #1 report hash | **RUN** — recomputed | MATCH: `ba81408bde5339291d4b2ef25cab70b5eaa3e518412ecd45cdbeb11f54604b95` |
| Audit #2 report hash | **RUN** — recomputed | MATCH: `b3534eee86e9af1f937e795223354498d994501be90dcc6e910d3a02297b6f13` |

**Integrity result:** the available bundle and candidate checksums pass. The 61 absent archived baseline objects remain an explicit extraction limitation, not a mismatch among extracted files.

## 3. C18 and prior findings

### 3.1 C18 verdict: SOUND WITH NOTE

C18's wording changes are correct, remain wording-only, and do not add a behaviour, outcome, fixture expectation or approval. The thirteen C18 edits are logged as E206–E218, after E205.

| Location | Assessment | Method |
|---|---|---|
| File 21 L52 | Gives development-run evidence, formal F18 status, and approval as separate parts | **RUN** — inspected candidate line |
| File 21 L70 | Gives the same three parts and retains `A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE REQUIRED**` | **RUN** — inspected candidate line; exact retained clause checked |
| File 21 L7 and L40 | Each status-column header explicitly treats row `NOT RUN` as the formal F18 status and points to L52 for development-run evidence and approval; this adequately covers the 24 cells | **RUN** — inspected headers and sampled cells; **REASONED** — header governs the table cells |
| File 21 L26 | The “RECORDED; F18 NOT RUN” status is now split into the three parts | **RUN** — inspected candidate line |
| File 21 L69 | A rule, not a current status claim; “formal F18 acceptance run” correctly prevents an external development run from setting sidecar check values | **RUN** — inspected candidate line; **REASONED** — interpreted in context |
| Charter L177 | The F1–F18 milestone says no authorized acceptance run exists, distinguishes development runs and states nothing is approved; “all must pass on FIFO” remains | **RUN** — inspected candidate line |
| Charter L194 | “That response executed no parser…” is a fair historical restatement of what the v1.0 response did; the current three-part status follows separately | **RUN** — compared the v1.3.6 source context and candidate line |
| File 30 L3 | Removing “Not implemented” is appropriate because the supplied development-run record supports a project implementation outside the pack; the new wording still says it is not frozen or executable for F18 acceptance | **RUN** — inspected wording and evidence metadata; **REASONED** — this is not an implementation verification |
| File 31 L3 | Three-part status is added after the proposed specification's own freeze/review status; no new rule is introduced | **RUN** — inspected candidate line |
| README L19 | Correctly distinguishes the pinned-runtime Unicode test from development runs and says nothing is approved | **RUN** — inspected candidate line |
| Fixture index L4 and L1931 | Both status fields carry the three parts; no fixture descriptor or expected object was changed by these edits | **RUN** — parsed JSON and compared descriptor expected objects |

**D2-1: RESOLVED.** Both originally deficient File 21 status statements now contain the three parts, and the A1–A11 and X14 dispositions are retained verbatim.

**D1-9: RESOLVED.** C17's partial status sweep is completed by C18. The current status scan and the status-sweep sample found no remaining current F18 status statement missing one of the three parts. Historical audit/release statements remain historical rather than being rewritten as present status.

### 3.2 Independent status-sweep review

`STATUS-SWEEP-D029.md` contains 342 classified rows across 59 files. I independently parsed the rows and reproduced the six totals:

| Class | Listed rows | Sample manually reviewed |
|---|---:|---:|
| FIXED (C18) | 13 | 13 |
| ALREADY THREE-PART (C17) | 8 | 8 |
| COVERED BY HEADER (C18) | 24 | 4 |
| CURRENT, NOT AN F18 STATUS | 36 | 4 |
| NOT A STATUS STATEMENT | 23 | 4 |
| HISTORICAL | 238 | 30 |
| **Total** | **342** | **63** |

The 30 historical samples were distributed through the historical class, from early entries to the final entries, and included earlier change/audit transcripts, v1.3.6 owner-decision and owner-approval records, build records and prior audit reports. The classifications were appropriate: they record what an earlier release, audit or owner decision said, not the current F18 result. All 13 C18-fixed rows and all 8 already-three-part C17 rows were inspected. The other four classes were sampled as shown.

Specific exemptions were checked:

- Charter L9 is a historical v1.3.5 audit-result statement.
- File 32 L11 is a historical v1.3.4/v1.3.5 audit statement.
- File 36 L48 describes provider truncation status for P11b; it is not an F18 execution-status claim.

I also scanned the ten current documents named by the test, not merely the sweep list. The test's status-term pattern matched 20 current-document lines; all non-exempt lines contained the three required lexical parts, and all three exemptions were used. The two fixture-index status fields also pass the same lexical check. No missed current F18 status line was found.

Two lines outside the sweep's matching criteria were examined separately: Protocol L478 (“Approved; F18 required”) and L481 (“Approved; F18 verifies”). In context, “Approved” is the status of the specific prompt-factor or wrapper-token design choice; the lines expressly leave F18 validation required. They do not claim F18 has run, passed or received approval, so excluding them from the three-part F18 run-status wording is correct.

**Test limitation.** `test_current_status_lines_have_three_parts` searches for three word patterns anywhere on the same line: `development-run`, `formal`, and `approv`. It checks token presence, not the semantic relationship or the content of each part. For example, this constructed line would pass its regex despite not giving the required three-part status:

> `F18 NOT RUN; “development-run” is a glossary term, “formal” describes the document style, and “approval” is a separate governance section.`

The old two-part D2-1 line fails the test and the current File 21 L70 line passes it, so the check is not vacuous. The false-positive example nevertheless shows that the regex is not a semantic guarantee. Manual review found no current content defect; the guard should be strengthened with explicit labels/structure and a negative semantic test.

**C18 verdict: SOUND WITH NOTE.** The note concerns the regression test's lexical rather than semantic enforcement, not a remaining deficient current status line.

## 4. Regression checks

| Regression | Method | Result |
|---|---|---|
| OD-1 | **RUN** — inspected Protocol L174/L185, owner decision A-059, related fixtures and run categories | PASS. Applies only to the two named local-ledger codes; the `SIMULATOR_ERROR` exception and the “—” no-class cell are preserved. A-059 is approved under D-029. |
| OD-2 | **RUN** — checked File 30 L83, M27 predicate source and its embedded hash | PASS. The Python 3.11 `(vector, sampled)` predicate is labelled owner-decided and hash-gated; the SHA-256 of its UTF-8 source matches `source_sha256`. **REASONED:** purity remains an owner-imposed condition; a hash cannot prove arbitrary source pure. |
| OD-3 | **RUN** — independently parsed Protocol §20 and compared the schema with M48, M50, M53, M54 and M58 descriptors | PASS. All five property maps match their expected objects; M54 correctly uses `domain_validation`, not `change_class`. |
| OD-4 | **RUN** — inspected Protocol L185 and M13/M41 records | PASS. Attempt is the ordinal of the recovery cycle opened; only attempt 1 is valid, no second cycle is permitted, and attempt is not a halt-signature component. |
| A1 | **RUN** — inspected M27 input and verified predicate-source hash; checked its expected object against baseline | PASS. Predicate uses sampled `full` and driven `wr_en`; expected object is unchanged. |
| A2 / File 25 copy | **RUN** — line comparison | PASS. File 25 L33–L130 equals Protocol L90–L187 exactly, 98/98 lines; File 25 L1–L32 remains byte-identical to v1.3.6. C18 makes no edit in this mirrored range. |
| A3 | **REASONED** — inspected Protocol L185 and correction rationale | PASS. Invalid supplied halt signatures are expressly outside the executable fixture contract and produce no invented outcome or ledger record. |
| A4 | **RUN** — inspected File 36 and M37 description/labels | PASS. M37 is accurately described as a supplied paired-outcome control vector, not source-level alias detection; OS-2 remains. |
| Category counts | **RUN** — counted `results.jsonl` rows by status/category and compared with `summary.json` | PASS: PACK-DERIVED 131 PASS; OWNER-DECIDED 11 PASS; OWNER-SPECIFIED 1 PASS + 1 NOT_IMPLEMENTED. |
| Expected objects | **RUN** — compared all 144 candidate fixture expected objects with v1.3.6 and each run result with its candidate descriptor | PASS: zero expected-object changes; all 144 result descriptor hashes match their candidate descriptor bytes. |
| Candidate development-run outcomes | **RUN** — counted 144 result rows and compared PASS actual/expected objects | PASS: 143 PASS, 1 NOT_IMPLEMENTED (P17), 0 FAIL, 0 ERROR; all 143 PASS rows have actual equal to expected. |
| Candidate manifest/result hashes | **RUN** — compared run summary with current bundle manifest and results file | PASS for the current run: both recorded hashes match their respective current files. |
| Changelog sequence and coverage | **RUN** — rebuilt and inspected the 218-entry builder log; compared mapped baseline/candidate file differences with logged paths | PASS: E01–E218 continuous; every one of the 22 changed baseline files is represented in the builder log; all C18 edits are E206–E218. |
| E01–E205 text unchanged from audit #2 | **REASONED, not byte-compared** — inspected cycle ordering and current build logic | C18 is appended after E205 and does not renumber earlier entries. The prior audit #2 candidate bundle is not present, so exact text comparison against that earlier candidate is not possible. |

### Run counts and category ownership

The current run contains 144 rows: 143 PASS, 1 NOT_IMPLEMENTED, 0 FAIL and 0 ERROR. Category totals match the brief and audit #2's recorded counts: 131 PACK-DERIVED PASS, 11 OWNER-DECIDED PASS, and OWNER-SPECIFIED 1 PASS plus 1 NOT_IMPLEMENTED.

The OWNER-DECIDED fixtures are M13, M15, M27, M41, M42, M47, M48, M50, M53, M54 and M58. The OWNER-SPECIFIED labels remain M37 = OS-2, M41 = OS-1 and P17 = OS-3. M41 correctly appears in OWNER-DECIDED because it depends on OD-4, while retaining its OS-1 label; only M37 and P17 remain in the OWNER-SPECIFIED category.

### Run-artifact continuity discrepancy

Audit #2's signed report records the earlier candidate pack manifest SHA-256 as `e704d194284c51bcac0f6ad20c119645c679bfce10fc71fe493ed0c02c9d7893`; the current candidate manifest hash is `3294d2a3920e6c06874535fc54dc037e2bc0461473cab33b6558b61f27a84eb1`. That pinned-manifest change is expected. The same report records the earlier `results.jsonl` SHA-256 as:

```text
81c73e32cc7643c8900dd3f83c5824b5f7ae6ae82d90f140f4465b2f4c8acd09
```

The current `results.jsonl` hash is:

```text
4b9714a43e7dfb4d9833de986302bf5f9d476da200e4e6871e967b608329284b
```

Both hashes are internally consistent with their respective audit report/current summary, but they differ. The current bundle does not include audit #2's raw `results.jsonl`, so I cannot perform a row-by-row comparison or establish why it changed. Thus the counts and categories match, but the stronger brief assertion that **only the pinned pack hashes differ** is not independently confirmed. A changed result-file hash is not, by itself, proof that a result value changed; it is an unresolved artifact-continuity discrepancy.

## 5. Findings and limitations

### D3-1 — LIMITATION: prior run artifact continuity is not established

**Location:** `docs/reviews/doc-audit2-gpt6-2026-11-27.md` (recorded previous `results_sha256`) and `evidence/run-v137c-20261127T153351Z/results.jsonl` (current file).  
**Quoted prior value:** `81c73e32cc7643c8900dd3f83c5824b5f7ae6ae82d90f140f4465b2f4c8acd09`  
**Current value:** `4b9714a43e7dfb4d9833de986302bf5f9d476da200e4e6871e967b608329284b`  
**Assessment:** status and category totals match; the current file matches its summary; however, the two results hashes differ and the old raw file is absent. This prevents confirmation that only the pinned pack hashes changed.  
**What would resolve it:** include the audit #2 `results.jsonl` (or a trusted content-addressed copy) and provide a row-level semantic/byte diff with an explanation of any intended difference; update the regression claim if the result artifact was intentionally regenerated with content changes.

### D3-2 — LIMITATION: status test is lexical, not semantic

**Location:** `tests/test_v137_candidate_pack.py`, `test_current_status_lines_have_three_parts`.  
**Quoted rule:** the test searches independently for `development-run`, `formal`, and `approv` anywhere on the same line.  
**Assessment:** the constructed false-positive sentence in §3.2 passes despite not expressing the three parts. This does not reveal a missed current status line in the pack, because the manual scan found none, but the automated test alone cannot guarantee the stated semantic rule.  
**What would resolve it:** require explicit labelled clauses and their corresponding values, and include negative tests where the words appear in unrelated quoted or explanatory text.

### Additional named limitations

1. **Baseline archive extraction:** 61 `archive_*` checksum entries are missing from the extracted baseline; they are disclosed in the supplied brief and could not be individually checked.
2. **Prior candidate snapshot absent:** audit #2's complete candidate pack and raw run results are not bundled. E01–E205 numbering and cycle ordering were checked, but prior-pack byte identity and the full old results content cannot be compared.
3. **Candidate test suite unavailable in this bundle:** `python -m pytest -q tests/test_v137_candidate_pack.py` was attempted and stopped during collection with `ModuleNotFoundError: No module named 'openvef'` at `from openvef.stage_map import validate_vector`. The implementation package is not included. I independently replicated the D-029 regex scan and OD-3 property comparison, but did not run the full project test suite.
4. **Implementation not audited:** the external project implementation, the actual evaluator, and the truth of the predicate's purity are outside this document audit. The development-run evidence is treated as evidence supplied in the bundle, not as an independently executed F18 acceptance run.
5. **F18 not run:** deliberately not run; this audit does not authorize or claim F18 acceptance or approval.

## 6. Final ruling

**C18: SOUND WITH NOTE. D2-1: RESOLVED. D1-9: RESOLVED.** The status wording and the sweep sample are sound; no current F18 status line missing the three parts was found. The requested OD-1–OD-4, A1–A4, File 25 copy, category counts and zero expected-object changes are confirmed as described above.

**Overall: NOT CLEARED.** The current result counts pass, but D3-1 leaves the explicit run-artifact regression assertion (“only the pinned pack hashes differ”) unresolved because audit #2's raw results file is absent and its recorded result hash differs from the current one. D3-2 and the additional test/implementation limitations are also recorded for the owners. No finding is marked closed on the owner's behalf.

**NOT CLEARED**
