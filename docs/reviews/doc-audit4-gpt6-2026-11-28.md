# OpenVEF — Independent Document Audit #4 — NOT CLEARED

**Pack:** OpenVEF Planning v1.3.7 CANDIDATE  
**Audit:** #4 — D-030, C19 / E219–E237, run continuity and regression  
**Auditor:** GPT-6 (OpenAI), independent of the correction author  
**Correction author:** Claude (Anthropic) via Claude Code  
**Operator:** Krishika  
**Audit date:** 28 November 2026  
**Overall status:** **NOT CLEARED**

This is a document audit of a candidate pack. It is not an implementation audit, does not run or pass F18, satisfies neither Protocol L555(5) nor L271, and approves nothing. v1.3.6 remains the default pack. The audit followed `docs/DOC-AUDIT4-BRIEF.md`; the brief was treated as an audit plan, not as evidence.

## 1. Bundle identity

**Uploaded ZIP:** `openvef-docaudit-bundle (2).zip`  
**ZIP size:** 1,325,651 bytes  
**SHA-256:**

```text
f01d344d150d89aae0f545890a0e5c97ad2f49a4f6a0e88a9add6731fbfe73cb
```

**Method: RUN.** Computed directly from the uploaded ZIP bytes. Every bundle reference in this report is to that exact archive.

## 2. Integrity checks and rebuild

| Check | Method | Result |
|---|---|---|
| Uploaded ZIP SHA-256 | **RUN** — SHA-256 computed from uploaded ZIP bytes | PASS |
| `MANIFEST.sha256` | **RUN** — parsed and checked every listed path and digest | PASS — 436/436 entries; zero missing, mismatched or unlisted files |
| Candidate `SHA256SUMS-v1.3.7-candidate.txt` | **RUN** — checked every listed path and digest | PASS — 205/205 entries; zero missing, mismatched or unlisted candidate files |
| Baseline `27_SHA256SUMS.txt` | **RUN** — checked all extracted baseline files | PASS for 202/202 present files; zero mismatches |
| Missing baseline entries | **RUN** — compared all checksum paths with extracted baseline paths | 61 absent entries, all `archive_*`; explicitly disclosed by the brief. They cannot be individually verified from this extraction |
| Candidate rebuild | **RUN** — executed `python3 proposals/v1.3.7/build_candidate.py /mnt/data/openvef_audit4_rebuilt` | PASS — builder reported 237 edits and 206 files |
| Rebuilt candidate | **RUN** — compared relative path sets and every file's bytes | PASS — 206/206 byte-identical; no missing, extra or different files |
| Audit #1 report hash | **RUN** — recomputed | MATCH: `ba81408bde5339291d4b2ef25cab70b5eaa3e518412ecd45cdbeb11f54604b95` |
| Audit #2 report hash | **RUN** — recomputed | MATCH: `b3534eee86e9af1f937e795223354498d994501be90dcc6e910d3a02297b6f13` |
| Audit #3 report hash | **RUN** — recomputed | MATCH: `757ae6e53002b93bc8738cbe07fac36f865b6253dafd1d4d042fa2f3cd94a34f` |
| Run `summary.json` results hashes | **RUN** — recomputed each `results.jsonl` hash and compared with its summary | PASS — all three match |
| Latest pack manifest and fixture-index hashes | **RUN** — compared latest `summary.json` with candidate pack manifest and index | PASS — both recorded hashes match the current candidate bytes |

**Integrity conclusion:** all available bundle and candidate integrity checks pass. The only extraction defect is the 61 absent historical baseline archive entries disclosed in the brief. This is a named limitation, not a checksum mismatch in an available file.

## 3. D3-1 — three-run continuity

**Verdict: RESOLVED.** The row-level comparison, report contents and corrected statement are independently supported.

### 3.1 First-to-second run: audit #2 versus audit #3

**Method: RUN.** Executed the bundled tool directly:

```text
python3 -I tools/diff_runs.py evidence/run-v137c-20261127T134318Z/results.jsonl evidence/run-v137c-20261127T153351Z/results.jsonl
```

The fresh tool output was byte-compared with the `Tool report (verbatim)` section embedded in `evidence/RUN-CONTINUITY-D030.md`; they match exactly. The evidence report's own recorded report hash also matches the reproduced output.

| Comparison result | Independently reproduced |
|---|---:|
| Rows in each file | 144 / 144 |
| Fixtures present in both | 144 |
| Fixture order | Same |
| Byte-identical rows | 135 |
| Rows with at least one changed field | 9 |
| Differing field paths | 5 |
| Differing (fixture, path) pairs | 45 |
| Critical differences (`status`, `category`, `actual`, `expected`, including descendants) | **0** |

The nine changed rows are M07, M31, M32, M33, M57, P01, P14, P21 and P42. They are all PASS rows. The five changed paths are exactly:

- `simulator.l334.wall_times_s[0]`
- `simulator.l334.wall_times_s[1]`
- `simulator.l334.wall_times_s[2]`
- `simulator.l334.median_s`
- `simulator.l334.t_timeout_s`

Each of those paths changes in each of the nine fixtures. No other result path differs. Independent comparison also confirms no difference in `note`, `pack_label` or `descriptor_sha256`.

### 3.2 Second-to-third run: audit #3 versus current C19 run

**Method: RUN.** Executed the bundled tool directly:

```text
python3 -I tools/diff_runs.py evidence/run-v137c-20261127T153351Z/results.jsonl evidence/run-v137c-20261127T163649Z/results.jsonl
```

The fresh output matches the verbatim report embedded in `evidence/RUN-CONTINUITY-D030-regression.md`.

| Comparison result | Independently reproduced |
|---|---:|
| Rows in each file | 144 / 144 |
| Fixtures present in both | 144 |
| Fixture order | Same |
| Byte-identical rows | 135 |
| Rows with at least one changed field | 9 |
| Differing field paths | 5 |
| Differing (fixture, path) pairs | 42 of 45 possible |
| Critical differences | **0** |

The same nine fixtures differ only in the same five timing paths. Three timing pairs happen to be equal between the later two runs. Independently comparing the first and third runs also found the same nine timing-only rows and zero critical differences.

Across all three files, **no `status`, `category`, `actual` or `expected` value differs**. There are also no changes in notes, pack labels or descriptor hashes. The run summaries retain 144 results and the same outcome and category counts.

### 3.3 Summary-file continuity and timing formula

**Method: RUN.** Compared `summary.json` leaf values and verified the recorded results hash against each actual file. The results hashes are:

- Audit #2 run: `81c73e32cc7643c8900dd3f83c5824b5f7ae6ae82d90f140f4465b2f4c8acd09`
- Audit #3 run: `4b9714a43e7dfb4d9833de986302bf5f9d476da200e4e6871e967b608329284b`
- Latest C19 run: `9b07f3c8d390d84bc6096f898188fd9b18cf63192153b5f0a8b77db7f38ce21b`

The `summary.json` differences include the pinned pack-manifest and fixture-index hashes, results hash, runner source hash, Git commit and run/container provenance. They do not indicate a change to any fixture's status, category, actual or expected value. Between audit #3 and the latest run, the new pack manifest and fixture-index hashes correspond to the C19 documentation and the two fixture-index status fields.

**Method: RUN.** For each available simulator timing record in all three runs, verified that `median_s` equals the median of the three `wall_times_s` samples and `t_timeout_s` equals `round(max(5 * median_s, 2.0), 3)`. No violation was found.

**Method: REASONED / LIMITATION.** The actual `l334_timeout` implementation source is not in this document-audit bundle. The observed values support the formula and report's description, but I cannot independently verify the implementation's measurement mechanism or the source-level cause of the timing changes.

### 3.4 Tool behavior and unit tests

**Method: RUN.** Inspected `tools/diff_runs.py` and executed:

```text
python3 -m unittest discover -s tests -p 'test_diff_runs.py' -v
```

All 7 tests passed. They cover identical files, non-critical path differences, critical-field differences and exit code 3, missing fixtures/order differences, byte-different but JSON-equal rows, type and absent-field differences, and malformed/duplicate input with exit code 2.

The tool's implementation agrees with its docstring for the bundled schema: it recursively reports differing leaves, groups by field path, includes absent fields, compares JSON values with type distinction, checks fixture identity/order, and treats `status`, `category`, `actual` and `expected` (including descendants) as critical.

**D3-1 conclusion:** the audit #4 brief corrects audit #3's inaccurate statement that only pinned pack hashes changed. The actual `results.jsonl` files also differ in measured simulator timing values in nine rows. The evidence reports are accurate and complete for the fields compared. **D3-1: RESOLVED.**

## 4. C19 and D3-2 — status labels and test strength

**C19 verdict: SOUND WITH NOTE. D3-2: PARTLY RESOLVED.**

### 4.1 Current status wording

**Method: RUN.** Inspected all 17 C19-labelled current status lines specified in the brief:

- File 21: L7, L26, L40, L52 and L70
- Charter: L177 and L194
- Protocol: L559
- File 30: L3
- File 31: L3
- File 32: L21 and L33
- File 36: L3 and L176
- README: L16, L35 and L46

Each line states, in order, `Development-run evidence: …; Formal F18 status: …; Approval: …`. The values retain the C17/C18 distinction between development-run evidence, formal F18 acceptance status, and approval. I found no added behavior, outcome, implementation qualification or approval claim. File 21 L70 still ends exactly:

```text
A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE REQUIRED**.
```

**Method: RUN.** Inspected the two fixture-index status fields (`execution_status` and `status`) at the specified locations. Both contain the same three-part structure. The current status scan covers 17 current-document lines, uses precisely the three named historical/input exemptions, and does not exempt a current F18 status line:

- Charter L9: historical audit status.
- File 32 L11: historical v1.3.4/v1.3.5 audit status.
- File 36 L48: P11b provider-truncation description, not an F18 run-status claim.

README L19 is not an F18 status statement and retains its C18 wording. The candidate-pack test checks that all three exemptions are used and no additional exemption silently appears.

### 4.2 Candidate-pack tests and independent negative case

**Method: RUN.** Executed from the bundle root:

```text
python3 -m unittest discover -s tests -p 'test_v137_candidate_pack.py' -v
```

Result: 16 tests run, 15 passed, 1 skipped. The skipped test is `test_corrected_m27_reaches_check_e`, because the `openvef` implementation package is not included in this document-audit bundle. The other tests passed, including the status scan, C19 negative examples, rebuild, expected-object equality, File 25 copy, cycle ordering, and OD-3 schema check.

**Method: RUN.** Independently imported `labelled_status` from `tests/test_v137_candidate_pack.py` and submitted additional adversarial lines. This line returns an empty problem list, which the test interprets as a valid status line, even though all three clauses are inside a single-quoted block:

```text
F18 NOT RUN; ' Development-run evidence: x; Formal F18 status: y; Approval: z'
```

An unquoted placeholder-only line also passes:

```text
F18 NOT RUN; Development-run evidence: x; Formal F18 status: y; Approval: z.
```

Both are false positives: the first quotes the complete set of labels rather than asserting the three status parts; the second supplies placeholders rather than meaningful values. The validator also searches for `label + ":"` rather than requiring the specified `": "`, and its value check accepts any `\w` character.

**D4-1 — LIMITATION: C19 validator remains bypassable.**  
**Location:** `tests/test_v137_candidate_pack.py`, L34 and L37–74, particularly L47, L51–53 and L72.  
**Quoted implementation:**

```python
for m in re.finditer(re.escape(label) + ":", line):
    ...
if sum(before.count(q) for q in "\"`") % 2 or before.count("“") > before.count("”") or \\
        before.count("‘") > before.count("’"):
    continue  # inside quotation marks
...
if not re.search(r"\w", value):
```

`QUOTES` includes the single-quote character, but the quote-parity check does not count it. As a result, the single-quoted false-positive line above is accepted. The non-empty check proves only that a word character exists; it does not validate the clause's meaning or status value. In addition, the matching expression accepts a label immediately followed by `:` without the required following space.

**Fix:** make the parser consistently recognize paired straight-single, straight-double, backtick and typographic quotes; require the exact `": "` separator; and validate the three clauses against meaningful status content rather than a single word character. Add regression tests for single-quoted labels, arbitrary placeholders (`x`, `y`, `z`), and other non-semantic values. The existing C19 status prose is correct on inspection; this finding concerns the automated guard, not a discovered defective current status line.

**D3-2 conclusion:** C19 resolves the wording and the old unlabelled-line weakness. The test rejects the audit #3 constructed example and many reordered/quoted/empty cases, but the single-quote and placeholder counterexamples show that its semantic enforcement is incomplete. **D3-2: PARTLY RESOLVED.**

## 5. Regression checks

Each entry below states the method used. “RUN” means the relevant pack text, fixture data, hashes or tests were actually inspected/executed. “REASONED” identifies conclusions that are not runtime proof.

| Check | Method | Result |
|---|---|---|
| OD-1 | **RUN** — inspected Protocol L174/L185 and the relevant fixture expectations | PASS. The two named local-ledger codes are distinguished from the explicit `SIMULATOR_ERROR` exception; the no-class “—” cell is preserved. Related M15, M42 and M47 expectations remain consistent. |
| OD-2 | **RUN + REASONED** — inspected File 30 L83 and M27 predicate source/hash | PASS as a documented owner condition. The predicate uses sampled `full` and driven `wr_en`; its embedded source hash matches the recomputed UTF-8 source hash. **REASONED:** a source hash does not establish arbitrary-source purity. The implementation-dependent test was skipped. |
| OD-3 | **RUN** — executed `test_od3_schema_covers_every_change_class_property`; compared Protocol §20.3 with M48, M50, M53, M54 and M58 expected property maps | PASS. All five maps match; M54 correctly uses `domain_validation`, not `change_class`. |
| OD-4 | **RUN** — inspected Protocol L185 and M13/M41 fixture records | PASS. Recovery attempt is the ordinal of the opened recovery cycle; only attempt 1 is valid, no second cycle is permitted, and attempt is not a halt-signature component. |
| A1 | **RUN + REASONED** — inspected M27 input, predicate hash and expected object against baseline | PASS for document/fixture content; the expected object is unchanged. **LIMITATION:** the implementation-dependent `check_e` path was not executed because `openvef` is absent from the bundle. |
| A2 / File 25 copy | **RUN** — line and byte comparison; candidate-pack test passed | PASS. File 25 L33–L130 equals Protocol L90–L187 exactly (98/98 lines); File 25 L1–L32 remains byte-identical to v1.3.6. |
| A3 | **REASONED** — read Protocol L185 and the correction rationale | PASS. Invalid supplied halt-signature components are outside the executable fixture contract and do not create an invented outcome or ledger record. |
| A4 | **RUN** — inspected File 36 and M37 description/labels | PASS. M37 is a supplied paired-outcome control vector, not source-level alias detection; OS-2 remains. |
| Category counts | **RUN** — counted each run's results and compared with all three summaries | PASS in all three runs: 131 PACK-DERIVED PASS; 11 OWNER-DECIDED PASS; OWNER-SPECIFIED 1 PASS + 1 NOT_IMPLEMENTED. Overall: 143 PASS, 0 FAIL, 1 NOT_IMPLEMENTED, 0 ERROR. |
| Expected objects | **RUN** — compared all 144 candidate fixture `expected` objects with v1.3.6; candidate-pack test passed | PASS — zero expected-object changes. All 143 PASS result rows in the latest run have `actual` equal to `expected`. |
| Fixture descriptors / C19 scope | **RUN + LIMITATION** — inspected C19 E219–E237 entries and builder CYCLE4 / INDEX_CYCLE4 targets | PASS for C19 scope: 17 document lines and the two fixture-index status fields; no C19 entry targets a fixture descriptor. **LIMITATION:** the previous C18 candidate snapshot is not bundled, so a direct byte comparison of all descriptors between C18 and C19 is unavailable. Six descriptor files differ from v1.3.6 due to earlier correction cycles; this must not be described as a C19 change. |
| File and changelog coverage | **RUN + LIMITATION** — rebuilt candidate, passed `test_only_the_expected_files_differ`, `test_no_line_moves_and_only_edited_lines_change`, and `test_cycle4_follows_cycle3`; inspected E01–E237 | PASS for reproducible build, edit scope, and continuous E01–E237 numbering; C19 occupies E219–E237. **LIMITATION:** without the prior C18 pack snapshot, exact byte identity of E01–E218 text relative to that earlier candidate cannot be independently compared. |
| Latest run versus audit #3 run | **RUN** — executed `diff_runs.py` and compared summary fields | PASS — no status/category/actual/expected/note/pack-label/descriptor-hash changes; timing-only differences in the same nine fixtures. Counts and toolchain identity remain consistent. |

### Category totals (all three runs)

| Category | PASS | FAIL | NOT_IMPLEMENTED | ERROR |
|---|---:|---:|---:|---:|
| PACK-DERIVED | 131 | 0 | 0 | 0 |
| OWNER-DECIDED | 11 | 0 | 0 | 0 |
| OWNER-SPECIFIED | 1 | 0 | 1 | 0 |
| **Total** | **143** | **0** | **1** | **0** |

M41 retains its OWNER-SPECIFIED label OS-1 while correctly appearing in OWNER-DECIDED for its OD-4 dependency. M37 is OS-2 and P17 is OS-3; P17 is the single NOT_IMPLEMENTED fixture.

## 6. Findings and named limitations

### D4-1 — LIMITATION: C19 status test has false positives

**Location:** `tests/test_v137_candidate_pack.py` L34, L37–74 (especially L47, L51–53, L72).  
**Evidence:** the single-quoted and placeholder-only lines in §4.2 both return `[]` from `labelled_status`.  
**Effect:** the test does not fully enforce the brief's requirement that each labelled clause is an unquoted, meaningful statement.  
**Resolution required:** harden quote parsing, require `": "`, validate meaningful part values and add the identified negative tests. The current 17 status lines and both index status fields are correctly worded on inspection.

### Additional named limitations

1. **PACK — baseline archive extraction.** 61 `archive_*` paths in baseline `27_SHA256SUMS.txt` are absent from the extraction. All 202 present baseline files match; the 61 absent objects cannot be verified.
2. **LIMITATION — prior C18 snapshot absent.** The bundle includes prior reports but not the complete prior C18 candidate pack. It is not possible to byte-compare E01–E218 text or every fixture descriptor directly against that exact prior snapshot. C19's own builder targets and E219–E237 changelog scope were checked instead.
3. **LIMITATION — implementation package absent.** `src/openvef` is not included. `test_corrected_m27_reaches_check_e` was skipped; actual M27 runtime behavior and predicate purity are not independently established by this document audit.
4. **LIMITATION — simulator implementation source absent.** The `l334_timeout` implementation is not bundled. The three-run values, derived median and timeout formula are verified, but source-level timing measurement/cause is not.
5. **LIMITATION — F18 not run.** This audit deliberately does not run F18, approve the implementation, certify acceptance, or assess the external implementation. Development-run records are treated as supplied evidence, not as an independent acceptance run.

## 7. Final ruling

- **Integrity and rebuild:** PASS, subject to the 61 absent baseline archive entries.
- **D3-1:** RESOLVED. Both run-continuity reports reproduce; across all three runs no status, category, actual or expected values differ. The only `results.jsonl` differences are simulator timing fields in nine fixtures.
- **C19 wording:** SOUND WITH NOTE. All 17 current status lines and both fixture-index fields are correctly structured and preserve the prior dispositions.
- **D3-2:** PARTLY RESOLVED. The strengthened test rejects the audit #3 example, but D4-1 demonstrates remaining quote and placeholder false positives.
- **OD-1–OD-4, A1–A4, File 25 copy, category counts and zero expected-object changes:** confirmed to the extent stated in §5; implementation-dependent checks remain limited as named above.

**Overall: NOT CLEARED.** D3-1 is resolved and the current C19 status wording is sound, but D3-2 remains only partly resolved because the validator accepts lines that do not genuinely state the three status parts. The audit also records the baseline extraction, prior-snapshot, implementation-source and F18-scope limitations above. No finding is marked closed on the owner's behalf.

**NOT CLEARED**
