# OpenVEF — Independent Document Audit #6

**Overall status: NOT CLEARED**  
**Audit date:** 28 November 2026  
**Auditor:** OpenAI GPT-6  
**Operator:** Krishika  
**Correction/test author:** Claude (Anthropic), via Claude Code  
**Target:** OpenVEF Planning v1.3.7 CANDIDATE, C19  
**Uploaded bundle SHA-256:** `e9719fb37ff9c548b22c6b8262ef93b911bca9bb06bc79844acf684d91f86982`

This is a document audit. It is not an implementation audit, does not run or pass formal F18 acceptance, does not satisfy Protocol L555(5) or L271, and approves nothing. The v1.3.6 baseline remains the default unless and until the owners adopt a candidate.

## 1. Integrity and reproducibility

| Check | Result | Method |
|---|---|---|
| Uploaded ZIP CRC/readability | PASS | RUN — `ZipFile.testzip()` returned `None`; archive extracted successfully |
| Uploaded `MANIFEST.sha256` | PASS — 656 entries | RUN — every listed file hash matched; no missing, mismatched, malformed or unlisted files |
| Candidate `SHA256SUMS-v1.3.7-candidate.txt` | PASS — 205 entries | RUN — all 205 entries matched; no missing or unlisted candidate files |
| Prior C18 candidate sums | PASS — 205 entries | RUN — all 205 entries matched; no missing or unlisted C18 files |
| v1.3.6 baseline `27_SHA256SUMS.txt` | PASS for extracted files; PACK limitation for absent archive entries | RUN — all 202 present files matched; 61 checksum-listed historical archive objects are absent |
| Prior audit reports #1–#5 | PASS | RUN — each report hash matched the value prescribed in the audit #6 brief and BUNDLE-INFO |
| Five bundled run `results.jsonl` hashes | PASS | RUN — every `results_sha256` matched its `summary.json` |
| Latest run pack/index pins | PASS | RUN — latest summary pins the candidate manifest and fixture-index hashes |
| Candidate rebuild from v1.3.6 | PASS | RUN — separate output directory; 206 rebuilt files were byte-identical to the supplied candidate |

The candidate sum-file SHA-256 is `d64a91a8a13483866eb2788c19ce17ae268eac54d829d916bdd2926e161b3fff`, matching the manifest identity recorded by audit #5. The C18 sum-file SHA-256 is `3294d2a3920e6c06874535fc54dc037e2bc0461473cab33b6558b61f27a84eb1`.

**PACK limitation (L1):** the baseline checksum file has 263 entries. Of those, 202 extracted files match and 61 historical `archive_*` objects are not in the extraction. The absent objects remain unverified; no supplied baseline file mismatched.

### Test execution

Commands run from the extracted bundle root:

```bash
python -m unittest discover -s tests -p 'test_v137_candidate_pack.py' -v
python -m unittest discover -s tests -p 'test_diff_runs.py' -v
```

Candidate-pack result: 19 tests discovered, 18 passed, 0 failed, 1 skipped. The skipped test is `test_corrected_m27_reaches_check_e`; `src/openvef` is absent from this document-audit bundle. It is not counted as passed. The separate `test_diff_runs.py` suite passed all 7 tests.

The optional rebuild command completed with 237 edits and 206 files; a byte comparison of every path and file confirmed the rebuilt directory equals the supplied candidate.

## 2. D5-1 / D4-1 — label validator

**D5-1: RESOLVED as originally reported.** The underscore defect is fixed. `WORD_CHAR = r"\w"` is used by `_is_word_char` for the label boundary and by `_inside_quotes` for apostrophe detection. No `.isalnum()` remains in the test file. I found no second, divergent definition of a word character in `labelled_status` or its helpers. All six new negatives (`_` and `x_` before each of the three labels) fail for the specified reason, `0 unquoted occurrences`; the earlier negative and positive cases also pass.

**D4-1: PARTLY RESOLVED.** I found a different Unicode continuation boundary false positive. This line is accepted by `labelled_status()`:

```text
F18 status: x́Development-run evidence: none; Formal F18 status: NOT RUN; Approval: nothing is approved.
```

The character immediately before `Development` is U+0301 COMBINING ACUTE ACCENT (Unicode category `Mn`). Python's `\w` does not match that code point, so the current one-code-point boundary test accepts it. The preceding `x` plus U+0301 is an identifier continuation (`"x\u0301Development".isidentifier()` is true), so the label's first word is joined to the preceding token rather than separated. The six underscore negatives do not exercise this case.

**D6-1 — MINOR: Unicode label-boundary false positive.**  
**Location:** `tests/test_v137_candidate_pack.py`, `WORD_CHAR`, `_is_word_char()` and the preceding-character check in `labelled_status()`.  
**Quoted code:**

```python
if before and (_is_word_char(before[-1]) or before[-1] in QUOTES + "-"):
    continue
```

**Effect:** checking only the final code point misses a combining mark that belongs to the preceding identifier/grapheme. The validator can accept a label that is not visibly a separate label.  
**Fix:** define the intended Unicode token-boundary semantics explicitly (including combining/identifier-continuation characters), check the full trailing continuation sequence rather than only one code point, and add negative tests for U+0301 and related relevant cases.

### Additional semantic probe beyond the two examples in D5-2

The validator also accepts this line:

```text
This is not a status statement; it is only an example: F18 status: Development-run evidence: none; Formal F18 status: NOT RUN; Approval: nothing is approved.
```

An explicitly contradictory prefix ("The following values are false and must not be treated as the current status:") also passes. This shows that the validator does not inspect surrounding context or negation. It is within the general D5-2 limitation that lexical acceptance does not establish semantic truth, but it is an additional concrete bypass beyond the two examples (unbound timestamp-shaped run IDs and arbitrary approval text after a period) expressly listed there. It does not falsify the manual review of the current pack lines; it reinforces why that review must remain mandatory.

**D6-3 — LIMITATION: context/negation blindness.** Add this concrete case to the D5-2 disclosure. It is inherent to the stated lexical-only approach and does not, by itself, establish a false claim in any of the current 17 lines.

## 3. Manual review and pack identity

**RUN + REASONED (carry-forward).** The current candidate manifest hash is identical to the C19 candidate identity recorded in audit #5. Consequently the candidate pack, including all status-bearing files, is byte-identical to the candidate manually reviewed in audit #5. I carried forward the prior per-line manual verdicts rather than claiming a second independent contextual review of unchanged text.

The current test scan found exactly 17 non-exempt status lines; all 17 pass `labelled_status()`. Both fixture-index fields (`execution_status` and `status`) were rechecked and pass. By manifest identity, the 17 lines and two fields are unchanged since audit #5. Audit #5's contextual manual review marked all 17 lines and both fields PASS.

The current `CHANGELOG-v1.3.7-candidate.md` contains 237 unique, contiguous entries E01–E237. Its inclusion in the same candidate checksum manifest as audit #5 establishes byte identity to that C19 candidate. All 144 fixture descriptor files are byte-identical to the bundled C18 snapshot; combined with the unchanged audit #5 candidate manifest, the descriptors are unchanged from audit #5's candidate as well. C18→C19 changes exactly the 13 expected candidate files listed in BUNDLE-INFO; no fixture descriptor file is among them.

## 4. DEVIATIONS.md and Protocol L555(3)

### Quote and owner-record accuracy

**PASS — RUN / REASONED.** `DEVIATIONS.md` reproduces the operative Protocol L555(3) sentence exactly:

> "Until both the document audit and owner record are complete, no implementation or fixture execution is authorized."

The section is explicitly headed **Owner interpretation (D-032)**, identifies the statement as Krishika's owner interpretation, and says the pack names no development-only exception and that the reading is the owners', not the text's. It does not misquote the pack or falsely claim that the exception appears in Protocol text.

### D6-2 — MAJOR: owner interpretation is not the best-supported reading of L555(3)

**Location:** `docs/DEVIATIONS.md`, "Owner interpretation (D-032)" and the L4 row of the disclosed-limitations table; Protocol v1.3.7-candidate L555(3).  
**Quoted owner interpretation:**

> "the owners authorized development-only regression runs (run_class: development) during the v1.3.7 document audits; they are not implementation or fixture execution under Protocol L555(3)'s gate and are not F18 acceptance"

**Quoted Protocol text:**

> "Until both the document audit and owner record are complete, no implementation or fixture execution is authorized."

**Finding:** the quotation and disclosure are accurate, but the conclusion that these runs are not implementation or fixture execution under the gate is not the best-supported reading of the unqualified Protocol wording. The bundled latest run is labelled `run_class: development`, yet its `run.log`, `results.jsonl` and `summary.json` show a 144-fixture run with actual/expected results. It is fixture execution against a project implementation, even though it is not formal F18 acceptance. `run_class: development` distinguishes it from formal acceptance; the Protocol clause does not itself create that distinction or state a development-only exception. The run occurred during document audit #6, before this re-audit had passed and before an owner record accepted/rejected A1–A11 and selected X14. The pack itself also says that development runs are fixture runs of a project implementation.

The owners may explicitly authorize a departure, but that would be an owner-authorized exception/waiver, not a reading supported by the literal clause. The present section openly labels the position as an owner interpretation, which is good disclosure; however, `Ends when: Answered by the owner interpretation` prematurely treats L4 as resolved while the underlying pack text remains unchanged.

**Fix:** either (a) record the development-only runs as an explicit owner-authorized deviation/waiver from L555(3), identifying their scope and that they are not F18 acceptance, and keep L4 disclosed as a departure; or (b) amend the Protocol to state the intended development-only exception and re-audit the changed normative text. Do not describe the exception as already contained in, or compelled by, the current Protocol wording.

### Limitations table completeness

**PASS with the L4 qualification above — REASONED.** `DEVIATIONS.md` carries D5-2 and all six report #5 limitations:

- **D5-2:** lexical acceptance does not establish semantic truth; fake timestamp-shaped IDs and unrestricted approval tails; contextual manual review required after changes.
- **L1 (PACK):** 61 absent baseline archive objects; 202 extracted baseline files verified.
- **L2:** implementation source absent; M27 `check_e` skipped; implementation behavior, predicate purity and runner internals not audited.
- **L3:** no formal F18 acceptance; this document audit does not satisfy L555(5) or L271.
- **L4:** no express development-only exception in L555(3); the owner interpretation is recorded, but the text remains unchanged and the interpretation issue is not closed as a textual matter (see D6-2).
- **L5:** implementation source for `simulator.l334` timing methodology/cause is absent.
- **L6:** no implementation approval or owner adoption; the document audit cannot record A1–A11 or X14 decisions.

The table preserves the substance of report #5's limitations. The additional D6-3 context/negation case should be added under D5-2. L4 should not be marked ended solely by the current interpretation.

## 5. Regression

### OD-1 through OD-4 and A1 through A4

| Check | Result | Method and qualification |
|---|---|---|
| OD-1 | PASS | RUN — latest rows M15, M42 and M47; each actual object equals expected |
| OD-2 | PASS for descriptor/hash contract; implementation check remains unavailable | RUN + REASONED — M27 row actual equals expected; predicate source SHA-256 recomputes; implementation `check_e` test was skipped because `src/openvef` is absent |
| OD-3 | PASS | RUN — `test_od3_schema_covers_every_change_class_property`; M48, M50, M53, M54 and M58 actual objects equal expected |
| OD-4 | PASS | RUN + REASONED — Protocol L185 and M13/M41 descriptors/results; actual objects equal expected |
| A1 | PASS for document/descriptor content; implementation path unavailable | RUN + REASONED — M27 predicate source/hash and expected object checked; the `check_e` implementation path remains skipped |
| A2 / File 25 copy | PASS | RUN — candidate-pack test confirms Protocol L90–L187 equals File 25 L33–L130 (98 lines) |
| A3 | PASS as a boundary statement | REASONED — Protocol L185 and all candidate descriptors inspected; no dedicated invalid-signature fixture is executed |
| A4 | PASS | RUN + REASONED — File 36/M37 and latest M37 result; actual equals expected |

### Descriptors, expected objects and categories

- **144 descriptors:** RUN — candidate descriptors compared byte-for-byte with the C18 snapshot; all identical.
- **Expected objects:** RUN — all 144 candidate `expected` objects compared with v1.3.6 baseline values; zero differences.
- **Current category counts:** RUN — summary and result rows agree.

| Category | PASS | FAIL | NOT_IMPLEMENTED | ERROR |
|---|---:|---:|---:|---:|
| PACK-DERIVED | 131 | 0 | 0 | 0 |
| OWNER-DECIDED | 11 | 0 | 0 | 0 |
| OWNER-SPECIFIED | 1 | 0 | 1 | 0 |
| **Total** | **143** | **0** | **1** | **0** |

The OWNER-SPECIFIED category therefore remains 1 PASS + 1 NOT_IMPLEMENTED. The latest run is a development run, not F18 acceptance.

### Run continuity against audit #5

**RUN.** I executed:

```bash
python3 -I tools/diff_runs.py \
  evidence/run-v137c-20261128T033242Z/results.jsonl \
  evidence/run-v137c-20261128T042052Z/results.jsonl
```

The tool exited successfully. Both result files contain the same 144 fixture IDs in the same order. 135 rows are byte-identical; 9 rows differ. The only differing paths are the five `simulator.l334` timing fields (`median_s`, `t_timeout_s`, and `wall_times_s[0..2]`), 45 fixture/path pairs in total. Changes to `status`, `category`, `actual`, `expected`, or any nested values under those fields: **zero**.

**RUN.** Independent leaf-by-leaf comparison of the two `summary.json` files found exactly six changed leaves: `git_commit`, `results_sha256`, `run_started_utc`, `run_finished_utc`, and the runner container's `--volume` and `--name` flags. The pack manifest, fixture-index hash, source hashes, counts, category counts, image, interpreter and toolchain identity are unchanged. All five bundled run summaries have result hashes matching their `results.jsonl` files.

## 6. Findings and named limitations

| ID | Severity | Finding |
|---|---|---|
| D6-1 | **MINOR** | Unicode combining-mark continuation can join the first label to the preceding identifier while passing the one-code-point `\w` boundary check. D5-1's exact underscore issue is fixed, but D4-1 remains partly resolved. |
| D6-2 | **MAJOR** | The D-032 owner interpretation that development fixture runs fall outside L555(3) is not the best-supported reading of the Protocol's unqualified ban. Record a waiver/deviation or amend the Protocol. |
| D6-3 | **LIMITATION** | The lexical validator accepts example/negation/contradiction prefixes; add this concrete context-blindness probe to the D5-2 disclosure. |
| L1 | **PACK** | 61 baseline archive objects are absent; only the 202 extracted baseline files are verified. |
| D5-2 | **LIMITATION** | Lexical run-ID and approval-tail acceptance does not establish semantic truth; manual review remains necessary. |
| L2 | **LIMITATION** | Implementation source missing; M27 `check_e`, predicate purity and runner internals not audited. |
| L3 | **LIMITATION** | No formal F18 acceptance; this document audit does not satisfy L555(5) or L271. |
| L4 | **LIMITATION** | The pack has no express development-only exception to L555(3); D6-2 explains why the owner interpretation does not close the textual issue. |
| L5 | **LIMITATION** | `simulator.l334` timing source/method not independently established because implementation source is absent. |
| L6 | **LIMITATION** | No implementation approval or owner adoption of A1–A11/X14 is recorded by this audit. |

## 7. Stopping rule and final ruling

**REASONED.** The D-031 stopping rule, reaffirmed by D-032 for audit #6, says the owners adopt only if this audit finds no BLOCKER, MAJOR or MINOR finding; remaining LIMITATION findings must be disclosed. I applied the severity scale independently and did not adjust severities to satisfy the rule.

D5-1 is resolved narrowly, but D6-1 is a new **MINOR** label-boundary defect and D6-2 is a **MAJOR** unsupported reading of L555(3). The stopping-rule condition is therefore not met. The owner's act of adoption is not asserted here.

**NOT CLEARED — because D6-1 (MINOR) and D6-2 (MAJOR) remain.** The candidate must not be treated as cleared by this report. The 61 absent baseline archive objects, D5-2/D6-3 lexical-semantic limitations, unavailable implementation source, absence of formal F18 acceptance, unresolved L555(3) interpretation/waiver, unverified simulator timing source and absence of implementation/owner approval remain disclosed limitations. No owner finding is marked closed by the auditor.
