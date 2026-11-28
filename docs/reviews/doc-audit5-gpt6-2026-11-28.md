# OpenVEF — Independent Document Audit #5

**Overall status: NOT CLEARED**  
**Audit date:** 28 November 2026  
**Auditor:** OpenAI ChatGPT, GPT-6 (independent of the correction author)  
**Operator:** Krishika  
**Correction author:** Claude (Anthropic), via Claude Code  
**Target:** OpenVEF Planning v1.3.7 CANDIDATE, C19  
**Bundle SHA-256:** `5f35d75bd7a5fdac36aa8f49be1ad049fa339f61f62d5a8af20143408136cd47`

This is a document audit of the candidate pack. It is not an implementation audit, does not run or pass formal F18 acceptance, does not satisfy Protocol L555(5) or L271, and approves nothing. The v1.3.6 baseline remains the default unless and until the owners adopt the candidate.

## 1. Executive conclusion

The archive, candidate manifests, rebuild, C18 byte comparison, current status statements, fixture index, and requested regression checks are substantially sound. The 14 supplied D4-1 negative tests all reject for their expected reasons. All 17 current status lines and both fixture-index fields accurately separate development-run evidence, formal F18 status, and approval when read in their local F18/fixture scope.

**D3-2: RESOLVED.** The current pack text contains the three status parts in the required order at all 17 locations and in both fixture-index fields. The two File 21 table headers correctly cross-reference the detailed `F18 result` section below them.

**D4-1: PARTLY RESOLVED.** The strengthened quote, separator, and closed-vocabulary checks repair the previously reported single-quote, placeholder, and missing-space cases. However, an additional label-boundary false positive remains: a label preceded by `_` is accepted, despite the function docstring promising not to accept a label preceded by a word character. This is a **MINOR** finding (D5-1), so the owner stopping rule is not met.

The stopping rule in section 0 of the brief is clear and was applied without changing the severity assessment: BLOCKER, MAJOR, or MINOR findings stop adoption; LIMITATION findings are disclosed but do not stop adoption. Because D5-1 is MINOR, the candidate is **NOT CLEARED** under that rule. The owners—not the auditor or correction author—decide whether and when to adopt it.

## 2. Integrity and reproducibility

| Check | Result | Method |
|---|---|---|
| Uploaded ZIP readable and CRC-valid | PASS | RUN — archive read and `ZipFile.testzip()` |
| `MANIFEST.sha256` | PASS — 649 entries | RUN — every listed file hash checked; no missing, mismatched, malformed, or unlisted files |
| Candidate `SHA256SUMS-v1.3.7-candidate.txt` | PASS — 205 entries | RUN — every entry checked; no missing, mismatched, or unlisted candidate files |
| C18 snapshot `SHA256SUMS-v1.3.7-candidate.txt` | PASS — 205 entries | RUN — every entry checked; no missing, mismatched, or unlisted C18 files |
| Candidate internal `27_SHA256SUMS.txt` / fixture-index consistency | PASS | RUN — candidate-pack checksum/index tests passed; fixture descriptor byte lengths and SHA-256 values agree with the index |
| v1.3.6 baseline `27_SHA256SUMS.txt` | PASS for extracted files; PACK limitation for absent archive entries | RUN — all 202 present baseline files match; 61 `archive_*` paths named in the sum file are absent from the extraction |
| Prior audit reports #1–#4 | PASS | RUN — all four bundled report hashes match the values in the brief |
| Four run `results.jsonl` hashes | PASS | RUN — each run's results hash matches its `summary.json` |
| Latest `pack_manifest_sha256` and fixture-index hash | PASS | RUN — latest summary matches the candidate pack manifest and fixture-index hashes |
| Candidate rebuild from v1.3.6 | PASS | RUN — separate empty output directory; 206 files generated from 237 edits; every path and byte hash matches the supplied candidate |

The candidate sum-file SHA-256 is `d64a91a8a13483866eb2788c19ce17ae268eac54d829d916bdd2926e161b3fff`. The C18 sum-file SHA-256 is `3294d2a3920e6c06874535fc54dc037e2bc0461473cab33b6558b61f27a84eb1`.

**PACK limitation:** the baseline checksum file contains 263 entries, but 61 historical `archive_*` paths are not in the extracted baseline. All 202 extracted baseline files were verified; the 61 absent archived objects could not be checked. This is an extraction limitation, not a mismatch in the files that are present.

### Candidate-pack test run

Command executed from the bundle root:

```bash
python3 -m unittest discover -s tests -p 'test_v137_candidate_pack.py' -v
```

Result: 19 tests discovered; 18 passed, 0 failed, and 1 skipped. The skipped test is `test_corrected_m27_reaches_check_e`, because `src/openvef` is not included in the document-audit bundle. All 14 D4-1 negative cases reject for their expected reason; the supplied positive cases and quote-kind guard also pass.

The run is a test of the document bundle and its tests. It is not a fresh execution of the OpenVEF implementation by this auditor and is not F18 acceptance.

## 3. D4-1 validator and D3-2 status wording

### 3.1 Quotes and separators

**RUN + REASONED.** I inspected and exercised `labelled_status`, `QUOTES`, `QUOTE_PAIRS`, `_inside_quotes`, and the separator checks.

- All quote characters in `QUOTES` are represented in `QUOTE_PAIRS`: straight double quote, straight single quote, backtick, and both typographic opening/closing pairs. The import-time set assertion prevents a quote kind from being silently omitted from the pair list.
- Straight quotes and backticks use odd/even parity; typographic pairs use opening/closing counts. The apostrophe exception removes `'` or `’` only when it occurs between two `\w` characters. The required current status strings do not exploit that exception to hide a label. The specific single-quoted false-positive from audit #4, including the version with valid values and a quote not adjacent to a label, is now rejected.
- The label separator requires `": "` followed by a non-space value character. The first two clauses must end in `"; "` immediately before the next label. Two spaces after a colon, no space after a colon, and a missing space after the semicolon are rejected by the negative tests.
- The function's preceding-character boundary check is not fully consistent with its docstring: it uses `str.isalnum()` but omits underscore, which Python treats as a word character in `\w`. See D5-1.

### 3.2 Closed vocabularies and adversarial probes

**RUN.** The 14 bundled negative tests all pass, including both audit #4 examples and the quote/separator regressions. I also ran additional inputs through the actual `labelled_status` function.

**D5-1 reproducer — accepted malformed label boundary:**

```text
F18 status: x_Development-run evidence: none; Formal F18 status: NOT RUN; Approval: nothing is approved.
```

`labelled_status(...)` returns `[]`. The `Development-run evidence` label is preceded by `_`, which is a word character under `\w`; the function nevertheless accepts it because `before[-1].isalnum()` returns false for underscore. The label is therefore attached to an identifier-like token rather than standing as a separate label.

**Semantic limitation probe — syntactically valid but unverified run ID:**

```text
F18 status: Development-run evidence: run-fake-20991231T235959Z; Formal F18 status: NOT RUN; Approval: nothing is approved.
```

`labelled_status(...)` returns `[]`. The run-ID expression checks only syntax; it does not prove that the ID exists or that its evidence supports the statement. This is consistent with the brief's warning that lexical validation cannot prove truth. The manual review below verifies the actual current statements against the bundled run evidence instead of relying on the regex.

**Semantic limitation probe — arbitrary Approval tail:**

```text
F18 status: Development-run evidence: none; Formal F18 status: NOT RUN; Approval: nothing is approved. The implementation is fully qualified and approved.
```

`labelled_status(...)` returns `[]`. `APPROVAL_TAIL` accepts any text after a period. This permits a contradictory follow-on sentence to accompany an otherwise accepted approval value. The current status lines do not contain that contradiction, but the validator does not police the semantics of the trailing prose; manual review remains necessary.

### 3.3 Resolution

- **D4-1 — PARTLY RESOLVED.** The specified 14 negative cases, quote-kind handling, exact separators, and closed vocabularies improve the guard and correct the earlier concrete bypasses. The underscore boundary false positive remains and is a fixable defect in the validator. See D5-1.
- **D3-2 — RESOLVED.** Every current status statement has the three required labelled parts in order. The two File 21 header cross-references resolve to the detailed `F18 result` section in the same file. This conclusion is based on the manual review below as well as the line-count test; it does not rely solely on lexical acceptance.

## 4. Manual review — all 17 current status lines and both index fields

**RUN + REASONED.** I read each listed line in its surrounding document context and compared the claims with the four bundled run summaries/results, the owner-gate text, and the current fixture index. All four run summaries identify `run_class: development`; none is an authorized F18 acceptance run. The latest results are 143 PASS and 1 NOT_IMPLEMENTED, but those development results do not constitute formal F18 acceptance. The owner record and pack gate text show A1–A11 remain unaccepted and X14 remains pending.

| # | Location | Verdict | Manual assessment |
|---:|---|---|---|
| 1 | File 21 L7 | PASS — cross-reference | Development-run evidence and Approval point to the detailed `F18 result` section below; Formal F18 status says NOT RUN as given in each row. The target section exists in the same file and states the parts. |
| 2 | File 21 L26 | PASS | Schema hash and byte length are recorded; the sidecar hash and length match. The line distinguishes development runs from F18 acceptance, says formal F18 is NOT RUN, and says nothing is approved in the F18/implementation scope. |
| 3 | File 21 L40 | PASS — cross-reference | Same valid header cross-reference as L7; the detailed status section follows below. |
| 4 | File 21 L52 | PASS | Explicitly identifies the external fixture runs as development only, formal F18 as NOT RUN / NOT PASSED because no authorized acceptance run exists, and no implementation as qualified or approved. It also says this checklist is a proposed specification, not proof that implementation components exist. The A1–A11 and authorization statements match the owner record. |
| 5 | File 21 L70 | PASS | Repeats the same accurate three-part status and retains A1–A11 NOT ACCEPTED and X14 OWNER CHOICE REQUIRED. The additional sentence does not reverse the approval state. |
| 6 | Charter L177 | PASS | F1–F18 development runs are explicitly not acceptance; no authorized F1–F18 acceptance run exists; nothing is qualified or approved. This is consistent with the current formal gate. |
| 7 | Charter L194 | PASS | Historical audit failure and open owner choices are described as such. The line correctly says the response executed no parser/assembler/harness/fixture suite as formal acceptance, separately records development-run evidence, and says formal F18 is NOT RUN / NOT PASSED. |
| 8 | Protocol L559 | PASS — scope note | The status is explicitly about the 144 fixture descriptors and F18 implementation approval. “Nothing is approved” is scoped to that F18/fixture qualification context; the next sentence separately records that seven v0.7 design directions remain owner-approved. Read globally, those phrases could sound inconsistent, but their local scopes are distinguishable. |
| 9 | File 30 L3 | PASS | The proposed execution contract is not frozen or executable for F18 acceptance until the stated gates; external fixture runs are development only; no authorized F18 acceptance run exists; no implementation is qualified or approved. |
| 10 | File 31 L3 | PASS | The proposed specification is not frozen pending independent review and owner approval; the three F18 status parts are accurate. |
| 11 | File 32 L21 | PASS | The statement applies the accurate development/formal/approval status to every fixture; descriptor metadata is not represented as a run result. |
| 12 | File 32 L33 | PASS | The implementation exists outside the pack; development runs are not F18 acceptance; formal F18 is NOT RUN / NOT PASSED; the implementation is not qualified or approved. The bundled run summaries corroborate that a project implementation was used, but its source is outside this audit bundle. |
| 13 | File 36 L3 | PASS — scope note | The fixture catalog is correctly called a test specification, not an execution report. Development runs are disclosed, formal F18 acceptance remains NOT RUN / NOT PASSED, and no implementation is qualified or approved. The final “no execution is authorized” sentence is read as the owner-gated F18/implementation execution path, not as a denial that the separately labelled development runs exist; D-031 item 3 specifically directs the development rerun. The pack would be clearer if it said “no formal F18 acceptance execution” rather than the unqualified “no execution”. |
| 14 | File 36 L176 | PASS | The execution-gate description is a proposed runner contract, not evidence of an authorized F18 run. It accurately distinguishes development runs from formal F18 acceptance and points to the status line at the top of the file. |
| 15 | README L16 | PASS | The inventory count of 144 and the three status parts match the fixture index and bundled run evidence. |
| 16 | README L35 | PASS | All 144 descriptors are identified as static package metadata; their hashes and lengths are not misrepresented as runner execution results. The development/formal/approval status is accurate. |
| 17 | README L46 | PASS | The external implementation and development-only run evidence are disclosed; formal F18 has not run; no implementation is qualified or approved. The pinned CPython patch remains TO FREEZE, which matches the release-gate section. |
| 18 | Fixture index `execution_status` | PASS | The field gives the three parts in order and matches the owner-gate and bundled run evidence. |
| 19 | Fixture index `status` | PASS | Same accurate statement as `execution_status`; both values are intentionally identical. |

The File 36 L3 execution wording and Protocol L559 approval wording have been recorded as scope notes, not as false statements. D-031 item 3 specifically directed a development rerun; the latest run is labelled `development`, not F18 acceptance. Protocol L555(3)'s unqualified “no implementation or fixture execution” language would benefit from a precise exception or an explicit definition distinguishing development-only regression runs from formal/authorized execution. This is disclosed as a limitation below, not silently reconciled.

## 5. C18 → C19 byte comparison and expected objects

**RUN.** I compared the complete extracted directories `prior/c18-candidate-pack/` and `proposals/v1.3.7/pack/` directly.

| Check | Result |
|---|---|
| C18 and C19 file counts | 206 each |
| Relative path sets | Identical |
| E01–E218 changelog rows | All 218 rows byte-identical |
| Changelog rows E219–E237 | All 19 present in C19 |
| All fixture descriptor files, excluding `fixture-index.json` | 144/144 byte-identical |
| Fixture-index root fields changed from C18 | Exactly `execution_status` and `status` |
| Fixture-index `fixtures` array | Identical; count remains 144 |
| Files differing between C18 and C19 | Exactly the 13 expected C19 files |
| Candidate expected objects vs v1.3.6 | 0 differences across all 144 descriptors |

The 13 C18→C19 changed files are: Charter, Protocol, File 21, `27_SHA256SUMS.txt`, Files 30, 31, 32 and 36, `41_F18_Fixture_Inputs/fixture-index.json`, `CANDIDATE-LABEL.md`, `CHANGELOG-v1.3.7-candidate.md`, `README.md`, and `SHA256SUMS-v1.3.7-candidate.txt`. This matches the C19 scope in the brief and `BUNDLE-INFO.json`.

All 144 expected objects compare equal to their v1.3.6 baseline values. Six descriptors have documented non-expected-field changes from earlier correction cycles (including M27, M37, M41, M42, M47 and M54); none of those changes occurred between the bundled C18 and C19 snapshots.

## 6. Regression checks

### 6.1 OD-1 through OD-4 and A1 through A4

| Check | Method | Result |
|---|---|---|
| OD-1 | RUN — inspected Protocol L174/L185 and latest M15, M42, M47 result rows | PASS. M15's `FEEDBACK_SERIALIZER_REJECT` and M42/M47's `DESIGN_HALT_REPEATED` actual objects equal their expected objects. The `SIMULATOR_ERROR` exception remains explicit. |
| OD-2 | RUN + REASONED — inspected File 30 L83, M27 predicate source/hash, latest result; implementation check unavailable | PASS for descriptor and hash contract. M27's embedded UTF-8 source hash recomputes exactly; its development-run actual object equals expected. LIMITATION: the implementation-dependent `check_e` test was skipped because the implementation package is not in this bundle; hash equality does not prove arbitrary source purity. |
| OD-3 | RUN — executed `test_od3_schema_covers_every_change_class_property`; compared §20 tables with M48, M50, M53, M54, M58 | PASS. The five control-vector schemas match their complete expected objects; M54 uses `domain_validation`. All five latest development-run rows PASS with actual equal to expected. |
| OD-4 | RUN + REASONED — inspected Protocol L185 and M13/M41 descriptors/results | PASS. The attempt is the ordinal of the recovery cycle opened; the only permitted ordinal is 1; a second halt terminates rather than opening a second cycle; attempt is not a signature component. M13 and M41 latest result objects match expected. |
| A1 | RUN + REASONED — inspected M27 input, predicate source/hash and expected object; compared expected object with v1.3.6 | PASS for document and descriptor content. Input reflects the updated `wr_en`/sampled `full` state and source hash is correct; expected object is unchanged. The implementation `check_e` path remains unexecuted (same limitation as OD-2). |
| A2 / File 25 copy | RUN — byte-compared Protocol L90–L187 with File 25 L33–L130 | PASS. All 98 lines match byte for byte. The candidate-pack test also passes. |
| A3 | REASONED — inspected Protocol L185 and all candidate descriptors | PASS as a boundary statement. An out-of-domain supplied halt signature is expressly outside the executable fixture contract and has no outcome/diagnostic/stage/error/disposition/ledger record. No candidate descriptor supplies an out-of-domain signature; no dedicated invalid-signature fixture is executed. |
| A4 | RUN + REASONED — inspected File 36 and M37 description/expected object; checked latest M37 result | PASS. M37 is described as a paired-outcome control vector, not source-level alias detection. Input and expected outcome are unchanged; M37 is still OWNER-SPECIFIED and latest actual equals expected. |

### 6.2 Categories, expected objects, and run continuity

**Latest run:** `run-v137c-20261128T033242Z`.

| Category | PASS | FAIL | NOT_IMPLEMENTED | ERROR |
|---|---:|---:|---:|---:|
| PACK-DERIVED | 131 | 0 | 0 | 0 |
| OWNER-DECIDED | 11 | 0 | 0 | 0 |
| OWNER-SPECIFIED | 1 | 0 | 1 | 0 |
| **Total** | **143** | **0** | **1** | **0** |

**RUN.** There are 144 results, no duplicate fixture IDs, and all 143 PASS rows have `actual == expected`. The sole NOT_IMPLEMENTED result is the remaining OWNER-SPECIFIED case. The category and status counts agree with the latest summary.

**RUN.** I executed:

```bash
python3 -I tools/diff_runs.py \
  evidence/run-v137c-20261127T163649Z/results.jsonl \
  evidence/run-v137c-20261128T033242Z/results.jsonl \
  --out /mnt/data/openvef_audit5_diff_recheck.md
```

`diff_runs.py` exits 0. Both result files contain the same 144 fixture IDs in the same order. 135 rows are byte-identical; the other 9 rows differ only in five `simulator.l334` timing fields (`median_s`, `t_timeout_s`, and the three `wall_times_s` entries). That is 45 differing (fixture, field) pairs across M07, M31, M32, M33, M57, P01, P14, P21 and P42. Differences in `status`, `category`, `actual`, or `expected` are zero. The `diff_runs.py` report hash is `8e4738f0dad6a02e0b1917c7cc91884c914b47e34fb603dcab18027c160e96e4`.

**RUN.** I independently compared the two `summary.json` structures leaf by leaf. Exactly six leaves differ: `git_commit`, `results_sha256`, `run_started_utc`, `run_finished_utc`, and the runner container's `--volume` and `--name` flags. The pack manifest, fixture-index hash, source hashes, counts, category counts, image, interpreter and toolchain identity are unchanged.

**RUN.** `python3 -m unittest discover -s tests -p 'test_diff_runs.py' -v` — all 7 tests passed.

## 7. Stopping rule

**REASONED.** The rule in section 0 is unambiguous about the categories that count: BLOCKER, MAJOR and MINOR stop automatic adoption; LIMITATION findings are disclosed in `DEVIATIONS.md` and do not stop it. It also correctly leaves the act of adoption to the owners. I did not change any severity because of the rule.

Because D5-1 is MINOR, the rule's condition for adoption is not met. No owner adoption is asserted here.

## 8. Findings and named limitations

### D5-1 — MINOR: underscore label-boundary false positive

**Location:** `tests/test_v137_candidate_pack.py`, `labelled_status`, label-hit boundary condition.

**Quoted code:**

```python
if before and (before[-1].isalnum() or before[-1] in QUOTES + "-"):
    continue
```

The function docstring says a label is not preceded by a word character. `str.isalnum()` does not include underscore, whereas `_` is a word character under `\w`. Consequently, the malformed line in section 3.2 with `x_Development-run evidence:` is accepted as having exactly one valid `Development-run evidence` label.

**Effect:** the automated D4-1 guard can accept a future line in which a required label is embedded in an identifier-like token instead of appearing as a separate label. This is a labelling defect in the test, not a defect found in the current 17 status lines or the two index values.

**Fix:** treat underscore as a word character in the preceding-boundary check (for example, check `before[-1] == "_"` as well as alphanumeric characters, or use a consistent `\w` boundary rule), and add negative tests for `_Development-run evidence:` and `x_Development-run evidence:`. Re-run the 14 existing negatives and the complete candidate-pack test suite.

### D5-2 — LIMITATION: lexical acceptance does not establish semantic truth

**Location:** `tests/test_v137_candidate_pack.py`, `DEV_NAMED_RUNS` and `APPROVAL_TAIL`.

The run-ID vocabulary validates a timestamp-shaped token but does not bind it to a run record. The fake run-ID probe in section 3.2 therefore passes lexically. `APPROVAL_TAIL` also permits arbitrary prose after a period, so a contradictory follow-on sentence can pass. These are limits of the lexical guard, not defects in the current manually reviewed status statements. The brief's section 0 expressly assigns truth to the manual review; the current run IDs/status claims were checked against the bundle's four run records and the owner gate. Keep the limitation disclosed and retain manual review whenever these values change. A future hardening could bind run IDs to known evidence and restrict approval continuations to approved suffixes.

### Additional named limitations

1. **PACK — incomplete baseline archive extraction.** 61 `archive_*` objects named in baseline `27_SHA256SUMS.txt` are not present. All 202 extracted files match; absent archive objects remain unverified.
2. **LIMITATION — implementation source unavailable.** The bundle contains run hashes and results but not the implementation source tree. The M27 `check_e` test was skipped; the source-level implementation behavior, predicate purity, and runner internals were not independently audited.
3. **LIMITATION — no formal F18 acceptance.** The latest and previous runs are explicitly development runs, not F18 acceptance. This audit does not execute F18, certify fixture acceptance, or satisfy Protocol L555(5) or L271.
4. **LIMITATION — development-run authorization wording.** D-031 item 3 directs a development rerun, and the bundled latest run is labelled `development`. Protocol L555(3), however, says without an express development-only exception that no implementation or fixture execution is authorized until the document re-audit and owner record are complete. The best reconciliation is that D-031 authorized a development-only regression run, not formal F18 acceptance; the pack should make this distinction explicit to avoid a reader treating the run as a breach of the execution gate.
5. **LIMITATION — simulator timing source.** `diff_runs.py` establishes that only the five timing fields vary in nine fixtures. The implementation that measures `simulator.l334` is not included in this bundle, so this audit does not independently establish the source-level cause or methodology of those timing changes.
6. **LIMITATION — no implementation approval or owner adoption.** The candidate remains a document-only candidate. A document-audit result cannot by itself qualify the implementation or record owner acceptance of A1–A11 or X14.

## 9. Final ruling

- Archive integrity, candidate/C18 sums, extracted baseline files, prior report hashes, run hashes, and separate candidate rebuild: **PASS**, subject to the 61 absent baseline archive entries.
- D3-2: **RESOLVED**.
- D4-1: **PARTLY RESOLVED**; the 14 supplied negatives pass, but the underscore label-boundary bypass remains.
- Manual status review: **PASS** for all 17 lines and both fixture-index fields, with the scope notes and execution-gate wording limitation recorded above.
- E01–E218 and all 144 C18 fixture descriptors: **byte-identical**; only the expected 13 files differ between C18 and C19.
- OD-1–OD-4, A1–A4, File 25 copy, category counts, zero expected-object changes, and run continuity: **PASS to the extent stated in section 6**, with the implementation-dependent check skipped and A3 reasoned rather than executed.
- Stopping rule: **not satisfied**, because D5-1 is MINOR.

**NOT CLEARED.** The candidate is not adopted by this report. The reason is D5-1 (MINOR), a remaining false-positive label-boundary defect in the D4-1 validator. The semantic-validation, baseline-extraction, implementation-source, F18, simulator-source, and development-run-authorization limitations are separately disclosed above. No finding is marked closed on the owners' behalf.
