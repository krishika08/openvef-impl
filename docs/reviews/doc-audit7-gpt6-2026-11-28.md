# **OpenVEF document audit #7 — v1.3.7 CANDIDATE**

**Operator:** Krishika\
**Auditor:** Independent review\
**Audit basis:** Uploaded audit #7 bundle

**Bundle SHA-256**

```
7e44902c5e6e20a0415b7f5c0eab5149a06456ed618f87887edf9cb5a711ed63
```

ZIP integrity: PASS

The archive was opened successfully, all 666 entries were readable, and the ZIP CRC test passed. This establishes archive readability, not yet the integrity of its individual manifest entries or the candidate.

**Auditor:** OpenAI GPT-6\
**Audit date:** 28 November 2026\
**Operator:** Krishika\
**Author of corrections under review:** Claude (Anthropic), via Claude Code

HEADER STATUS: CLEARED

**Scope:** v1.3.7 CANDIDATE document audit #7, specifically D6-1, D6-2 and the regression checks. DEV-004 is reviewed as contextual evidence concerning v1.3.6, not as an implementation or F18 audit.

## **1. Integrity checks**

| Check                           | Method | Result                                    |
| ------------------------------- | ------ | ----------------------------------------- |
| ZIP readability and CRC         | RAN    | PASS — 666 archive entries                |
| `MANIFEST.sha256`               | RAN    | PASS — all 665 entries match              |
| Candidate `SHA256SUMS`          | RAN    | PASS — 205/205 files match                |
| C18 `SHA256SUMS`                | RAN    | PASS — 205/205 files match                |
| v1.3.6 baseline checksums       | RAN    | PASS for all 202 supplied baseline files  |
| Rebuild from v1.3.6             | RAN    | PASS — 206/206 files byte-identical       |
| Six candidate-run result hashes | RAN    | PASS — all six match their summaries      |
| Reports #1–#6                   | RAN    | PASS — all six match the specified hashes |
| Owner-record hashes             | RAN    | PASS — both match the specified hashes    |

**Baseline PACK limitation L1:** The baseline checksum file contains 263 entries, but 61 `archive_*` objects are absent from the extraction. All 202 supplied baseline files match their expected hashes. The 61 absent objects remain unverified; they are not checksum mismatches.

The rebuild command produced 237 edits across 206 files. Comparing the resulting rebuild with the supplied candidate produced no differing paths or file bytes.

The candidate checksum-file SHA-256 is:

```
d64a91a8a13483866eb2788c19ce17ae268eac54d829d916bdd2926e161b3fff
```

The latest run pins this candidate manifest. Its fixture-index hash also matches the bundled `fixture-index.json`.

The uploaded bundle SHA-256 remains exactly:

```
7e44902c5e6e20a0415b7f5c0eab5149a06456ed618f87887edf9cb5a711ed63
```

## **2. D6-1 and D4-1 — label boundary**



D6-1: RESOLVED

D4-1: RESOLVED



**Method: RAN — source inspection, unit tests and adversarial probes.**

The implementation now uses one allow-list:

```
LABEL_PRECEDERS = frozenset(" (|*")
```

A label is accepted at the start of the line or immediately after one of those four ASCII characters.

The implementation also:

- Matches the literal label text using `re.escape(label)`, without case folding.
- Checks that the matched label is ASCII.
- Uses `WORD_CHAR` only in `_inside_quotes()` to distinguish apostrophes from quotation marks.
- Does not use a separate block-list or word-character boundary test to decide whether a label is valid.

The same boundary logic applies to every label.

### **Negative and positive tests**

The new negative cases cover:

| Negative category                                              | Cases |
| -------------------------------------------------------------- | ----- |
| U+0301, U+200D and U+200B before each label                    | 9     |
| U+00A0 and tab instead of the required space before each label | 6     |
| Cyrillic look-alike letters inside labels                      | 3     |
| No space after the semicolon                                   | 1     |
| Comma instead of the required semicolon separator              | 1     |

The 39-negative and 11-positive test sets pass. The new cases reject for the specified reasons. The semicolon-without-space case now fails earlier because `;` is not an allowed label predecessor; the comma case fails the `'; '` separator requirement.

The existing positives remain accepted, including line-start labels and the three permitted punctuation boundaries.

### **Adversarial probes**

**Method: RAN.**

I directly called `labelled_status()` with the following variations:

\| Probe | Result |\
\|---|---|\
\| Label immediately after an ASCII letter | REJECT |\
\| Label immediately after `_` | REJECT |\
\| Label preceded by a combining mark | REJECT |\
\| Label immediately after `(` | ACCEPT |\
\| Label immediately after `|` | ACCEPT |\
\| Label immediately after `*` | ACCEPT |

The punctuation cases deserve a precise distinction: they allow a label to be adjacent to punctuation without an intervening space. They do **not** allow a label to be fused into an uninterrupted alphanumeric or identifier-like token. The three characters are explicitly permitted delimiters in D-033, so these positives are consistent with the specified rule.

I also retried two semantic probes:

- A line saying that the following text is only an example, not a status statement.
- A line saying that the following values are false and must not be treated as current status.

Both still pass the lexical validator. These are the previously disclosed D6-3 context/negation cases, already recorded under D5-2. They are not a newly discovered D6-1 boundary bypass.

**Candidate-pack tests:** RAN.

```
Ran 19 tests
18 passed
1 skipped
0 failed
```

The skipped test is `test_corrected_m27_reaches_check_e`. The implementation source directory `src/openvef` is absent from this document-audit bundle, so the implementation-dependent check cannot run.

**Diff-tool tests:** RAN.

```
Ran 7 tests
7 passed
0 failed
```

**Conclusion:** D6-1 is resolved. The earlier D4-1 boundary issue is also resolved. No new lexical bypass was found beyond the already disclosed D5-2/D6-3 semantic limits.

## **3. D6-2 — DEV-003 and Protocol L555(3)**

D6-2: RESOLVED

**Method: RAN and REASONED.**

I compared the Protocol wording, the DEV-003 text, the D-033 owner decision and the run IDs in the evidence directory.

### **Protocol and owner authorization**

Protocol L555(3) states:

> “Until both the document audit and owner record are complete, no implementation or fixture execution is authorized.”

DEV-003 accurately represents this as a prohibition in the Protocol, followed by an explicit owner waiver for development-only runs. It does not claim that the Protocol itself contains a development-run exception.

The waiver states that these runs:

- Are development runs (`run_class: development`).
- Cover the period from candidate creation, commit `b9f3d54`, until v1.3.7 is adopted or rejected.
- Are fixture execution under a waived bar.
- Are not F18 acceptance and are not F18 evidence.

This is the correction required by D6-2. The superseded D-032 interpretation is still present and clearly labelled superseded. The Protocol itself is unchanged.

The owner decision is recorded as Krishika's D-033 decision taking effect under D-008. The separate Ayush ratification entry referenced in the governance records is not supplied in this bundle, so I did not independently verify that entry.

### **Waived-run inventory**

**Method: RAN — compared DEV-003's inventory with the bundled evidence directories.**

DEV-003 names 34 runs:

| Category               | Number | IDs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Candidate fixture runs | 11     | `run-v137c-20261126T155948Z`, `run-v137c-20261126T164050Z`, `run-v137c-20261127T052443Z`, `run-v137c-20261127T114201Z`, `run-v137c-20261127T134318Z`, `run-v137c-20261127T153351Z`, `run-v137c-20261127T163649Z`, `run-v137c-20261128T032116Z`, `run-v137c-20261128T033242Z`, `run-v137c-20261128T042052Z`, `run-v137c-20261128T102409Z`                                                                                                                                           |
| Control runs           | 10     | `controls-20261126T160156Z`, `controls-20261126T164304Z`, `controls-20261127T052649Z`, `controls-20261127T134510Z`, `controls-20261127T153602Z`, `controls-20261127T163904Z`, `controls-20261128T032418Z`, `controls-20261128T033441Z`, `controls-20261128T042259Z`, `controls-20261128T102625Z`                                                                                                                                                                                   |
| Container-test runs    | 13     | `container-tests-20261126T160212Z`, `container-tests-20261126T164316Z`, `container-tests-20261127T052653Z`, `container-tests-20261127T053222Z`, `container-tests-20261127T134545Z`, `container-tests-20261127T135044Z`, `container-tests-20261127T153608Z`, `container-tests-20261127T154913Z`, `container-tests-20261127T163956Z`, `container-tests-20261128T032456Z`, `container-tests-20261128T033514Z`, `container-tests-20261128T042332Z`, `container-tests-20261128T102719Z` |

All six candidate fixture-run directories actually supplied in the bundle are included in DEV-003's list.

**Evidence limitation:** Five of the 11 candidate-run records are not present as raw run directories in this bundle. The 10 control-run and 13 container-test raw logs are also not supplied. The run IDs are listed, but their underlying historical execution records cannot all be independently revalidated here. DEV-003 expressly identifies the interrupted `run-v137c-20261127T114201Z` as having no summary while recording that fixtures were executed.

### **L4 and D6-3**

L4 correctly remains classified as a **DEPARTURE**, not as a resolved Protocol exception. Its ending condition is tied to the waiver:

> “The waiver ends (DEV-003: v1.3.7 adopted or rejected).”

That is correct. L4 remains open until the owners adopt or reject v1.3.7.

D6-3 is added to the existing D5-2 disclosure without removing the earlier limitations. The disclosure still identifies the unbound timestamp-shaped run ID and permissive approval-tail behavior, and now additionally identifies context/negation blindness. Manual review remains mandatory when status values change.

**Conclusion:** D6-2 is resolved. DEV-003 is an accurate owner-authorized departure, with its run inventory explicitly recorded. L4 correctly remains open.

## **4. DEV-004 — v1.3.6 owner-record review**

**Method: RAN — direct line-by-line comparison of the two bundled owner-record exports. REASONED — assessment of what those records establish and what remains uncertain.**

The two owner-record files have the expected SHA-256 values. I checked the quotations and line references in DEV-004 against the actual files.

### **What is accurately represented**

**A1–A11, X14 and freeze validity**

The Owner Decision Record rev25:

- Lines 38–48 mark A1–A11 accepted as written.
- Line 50 states 11/11 accepted and zero rejected or modified.
- Line 58 selects X14 Option A.
- Line 140 marks the freeze valid.

The Sign-off Pack rev95, Part 4 line 129, accurately states that the owners adopt the Decision Record at revision 25 and that Part 4 substitutes for its §6.3 signature block.

**Signature and chronology**

Sign-off Pack line 133 records Krishika's written statement at 13:54 IST on 23 November 2026. That corresponds to 08:24 UTC. The first listed v1.3.6 fixture run began at 08:27:47 UTC — 3 minutes and 47 seconds later.

Line 134 records Ayush's statement as posted from Krishika's session and explicitly says Claude cannot verify who typed it. DEV-004 accurately identifies this as an unverified signature.

**F18 scope**

Owner Decision Record §5.2:

- Line 104 quotes the scope opened by Register 16.
- Line 108 confirms that the hand-built F18 descriptors are treated as part of the parser/assembler hand-tests.

DEV-004's account is accurate.

**Document audit**

Owner Decision Record line 14 states:

> “PASS, 23 Nov 2026 (independent, documents only)”

The quotation is exact.

### **The four stated gaps**

All four gaps are supported by the records.

| DEV-004 gap                                        | Verification                                                                                                             |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 1. The 23 November document-audit report is absent | Supported by the repository contents and the cited decision-record statement. The separate audit report is not included. |
| 2. Ayush's signature is unverified                 | Supported by Sign-off Pack L134 and the relayed-acceptance record at L121.                                               |
| 3. Part 3 checklist and Decision Record disagree   | Supported by Sign-off Pack L82, L85, L86 and L88 versus Decision Record L16, L76–L81, L92–L93 and L130–L132.             |
| 4. Claude marked Decision Record boxes             | Supported by Decision Record L5 and Sign-off Pack L125, with owner instructions recorded at L120–L121.                   |

One attribution detail matters: the §1 baseline-review mismatch included within Gap 3 was added by Claude. `docs/ambiguities.md` explicitly says this at lines 2207–2209. It is factually supported, but it was not one of the original owner-specified Gap 3 points. DEV-004 should not imply otherwise.

### **“Read with care” notes**

The following observations are accurate:

1. The exports were made on 28 November. Sign-off Pack revision 95 includes a 24 November amendment. It cannot establish what the Part 4 statement looked like at 13:54 IST on 23 November.
2. Both records carry BLANK titles and unsigned-status language.
3. The Decision Record's §6.3 signature fields are empty, while its lines 157–163 retain the default “NOT ACCEPTED” and “Authorization: NONE” state until a signature is recorded.
4. Part 4 states that its signature substitutes for the Decision Record's §6.3 signature block.

There is an important unresolved tension: Sign-off Pack L5 says:

> “Nothing in this pack is selected or signed.”

Yet its Parts 1–3 contain marked items, and Part 4 contains written signature statements. The owner-record NOTE flags this, but the documents themselves do not independently resolve the contradiction. The Part 4 substitution is the stated basis for the owner decision; the export alone cannot establish the historical state.

### **Additional evidence caveats**

Contextual limitation — DEV-004

Two further points should remain visible when reading DEV-004:

- Sign-off Pack L96 ticks the statement that SHA-256 values for each exact signed file were recorded. However, `owner-records/NOTE.md` says no such hashes were in the repository before this commit. The hashes supplied now verify the 28 November exports as received; they do not prove those are byte-identical to the exact files signed on 23 November. This is an additional evidentiary caveat beyond the four D-034 gaps.
- DEV-004 relies on `docs/assistance-log.md` lines 21 and 28 for session chronology. That file is not included in this audit bundle, so I could not independently inspect those cited entries. The 23 November first-session timing is therefore not independently verified by this audit.

**Judgment on DEV-004:** Its quoted owner-record statements and cited line numbers are accurate. The four D-034 gaps are represented fairly, and the later-export/blank-record caveats are appropriately disclosed. However, DEV-004 should also make the L96 hash-attestation caveat explicit in its own account. The missing assistance log further limits independent verification of the chronology.

This is a contextual evidentiary limitation concerning v1.3.6. It is not a finding against the v1.3.7 candidate and does not alter the D-033 stopping-rule assessment.

## **5. Regression checks**

**Method: RAN unless marked REASONED below.**

| Required regression                               | Result                                      |
| ------------------------------------------------- | ------------------------------------------- |
| 17 status lines unchanged since audit #5          | PASS — same candidate manifest identity     |
| Two fixture-index fields unchanged since audit #5 | PASS — same candidate manifest identity     |
| All E01–E237 changelog entries                    | PASS — 237 unique, contiguous entries       |
| All 144 descriptors                               | PASS — byte-identical to C18                |
| OD-1 through OD-4                                 | PASS                                        |
| A1 through A4                                     | PASS, with stated implementation limitation |
| File 25 copy                                      | PASS                                        |
| Expected objects                                  | PASS — zero changes                         |
| Category counts                                   | PASS                                        |
| Run continuity against audit #6                   | PASS — no status or expected-object changes |

### **Changelog, descriptors and status statements**

The candidate contains E01–E237 with no missing or duplicate entry.

Compared with C18, E01–E218 are byte-identical and E219–E237 are the 19 subsequent C19 additions. The complete candidate manifest is the same C19 artifact pinned by audits #5 and #6, so the complete E01–E237 sequence remains unchanged since those audits.

The 144 descriptor JSON files were compared byte-for-byte with C18: all 144 match.

The current status-line test ran and confirmed 17 required lines plus both `fixture-index.json` fields (`execution_status` and `status`). The complete candidate manifest matches the audit #5/#6 candidate manifest. Therefore, the two fields and 17 status lines are unchanged since audit #5.

**Manual review:** REASONED carry-forward. Audit #5 marked all 17 lines and both index fields PASS after contextual review; audit #6 confirmed their unchanged identity. I have not repeated the full contextual review of every line because the candidate manifest is identical.

### **OD-1 through OD-4 and A1 through A4**

| Check        | Method                                                         | Result                                                                            |
| ------------ | -------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| OD-1         | RAN — M15, M42, M47 result rows                                | PASS; actual equals expected                                                      |
| OD-2         | RAN + REASONED — M27 descriptor, hash and expected object      | PASS for descriptor/hash contract; implementation `check_e` unavailable           |
| OD-3         | RAN — schema test and M48, M50, M53, M54, M58                  | PASS                                                                              |
| OD-4         | RAN + REASONED — Protocol L185, M13 and M41                    | PASS                                                                              |
| A1           | RAN + REASONED — M27 predicate source/hash and expected object | PASS for document/descriptor content; implementation path unavailable             |
| A2 / File 25 | RAN — line comparison                                          | PASS                                                                              |
| A3           | REASONED — Protocol L185 and descriptors                       | PASS as a boundary statement; no dedicated invalid-signature fixture was executed |
| A4           | RAN + REASONED — File 36, M37 descriptor and latest result     | PASS                                                                              |

File 25's copy was checked directly: Protocol L90–L187 matches File 25 L33–L130, all 98 lines.

All 144 expected objects were compared with the v1.3.6 baseline values. The comparison found **zero expected-object changes**.

### **Counts and run continuity**

The latest development-run results show:

| Category        | PASS    | FAIL  | NOT_IMPLEMENTED | ERROR |
| --------------- | ------- | ----- | --------------- | ----- |
| PACK-DERIVED    | 131     | 0     | 0               | 0     |
| OWNER-DECIDED   | 11      | 0     | 0               | 0     |
| OWNER-SPECIFIED | 1       | 0     | 1               | 0     |
| **Total**       | **143** | **0** | **1**           | **0** |

**Run continuity: RAN.** I reran `tools/diff_runs.py` on audit #6's run `run-v137c-20261128T042052Z` and the latest run `run-v137c-20261128T102409Z`.

Results:

- Both files contain the same 144 fixtures in the same order.
- 135 rows are byte-identical.
- Nine rows differ, and only in five `simulator.l334` timing fields.
- The nine affected rows are M07, M31, M32, M33, M57, P01, P14, P21 and P42.
- Differences in `status`, `category`, `actual` and `expected`: **zero**.

The two summary files differ only in run provenance and container volume/name arguments. Their pack manifest, fixture-index hash, source hashes, counts, category counts, image, interpreter and toolchain identity match.

The control-run comparison in `RUN-CONTINUITY-D033.md` reports the same 16 status records between the two control runs, with only wall-time differences on F14 and F15. **REASONED:** the raw control-run files were not included, so I verified that statement against the bundled continuity report rather than independently rerunning the controls.

The `simulator.l334` source and timing methodology remain unavailable. The recorded timing changes are real result-field differences, but their source-level cause is not established by this document audit.

## **6. Findings and limitations**

### **D-033 candidate findings**

**No BLOCKER, MAJOR or MINOR finding remains in the D-033 candidate-audit scope.**

D6-1, D4-1 and D6-2 are resolved. The regression checks reveal no changed status, category or expected object. The discovered context/negation cases are already disclosed under D5-2/D6-3.

### **Named limitations**

The following remain open and must not be mistaken for audit failures newly introduced by D6-1 or D6-2:

| ID          | Severity / type | Limitation                                                                                                                                                                                      |
| ----------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| L1          | PACK            | 61 baseline `archive_*` objects are absent; only 202 supplied baseline objects were verified.                                                                                                   |
| L2          | LIMITATION      | Implementation source is missing. M27 `check_e`, implementation behaviour, predicate purity and runner internals could not be audited.                                                          |
| L3          | LIMITATION      | No formal F18 acceptance run. The development runs are not F18 evidence and do not satisfy Protocol L555(5) or L271.                                                                            |
| L4          | DEPARTURE       | Development fixture execution occurred under the owner waiver in DEV-003. The departure remains open until v1.3.7 is adopted or rejected.                                                       |
| L5          | LIMITATION      | The implementation measuring `simulator.l334` is absent, so the cause and methodology of timing differences are not independently established.                                                  |
| L6          | LIMITATION      | This document audit does not approve the implementation or record owner adoption of A1–A11 or X14.                                                                                              |
| D5-2 / D6-3 | LIMITATION      | Lexical validation does not prove the truth of timestamp-shaped run IDs or approval statements. It is blind to context and negation. Manual review remains mandatory when status values change. |

Additional audit-context limitations:

- Five candidate fixture runs, 10 control runs and 13 container-test runs are listed in DEV-003 but lack raw run artifacts in this bundle.
- The Ayush ratification entry referenced in the governance record was not supplied.
- DEV-004's cited assistance log is not supplied, and its owner-record exports cannot independently authenticate what the live documents contained on 23 November.
- The Sign-off Pack's L96 hash attestation lacks the corresponding historical hashes in this repository, as disclosed in its NOTE.

None of these has been silently treated as a pass or closed.

## **7. Final decision**

The unchanged stopping rule requires no BLOCKER, MAJOR or MINOR finding for this candidate audit. I applied the severity scale independently of that rule.

D6-1 is resolved by the uniform ASCII allow-list boundary and its new negatives. D4-1 is resolved. D6-2 is resolved by the explicit owner-authorized departure in DEV-003, which correctly leaves L4 open. The required regression checks preserve the candidate's status statements, index fields, descriptors, expected objects and fixture outcomes.

DEV-004's direct quotations are accurate, but its historical evidentiary limitations remain. That contextual review does not establish that v1.3.6's gate was independently proven at the time of the first run, nor does it affect the D-033 candidate stopping rule.

**CLEARED**

This is clearance under the document-audit #7 / D-033 stopping rule only. It is not an implementation audit, F18 acceptance, Protocol L555(5) pass, L271 sign-off or owner adoption. The owners retain the adoption decision; v1.3.6 remains the default until that decision is recorded.