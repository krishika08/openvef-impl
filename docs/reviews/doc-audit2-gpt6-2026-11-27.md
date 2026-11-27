# **OpenVEF — Independent Document Audit #2**

OVERALL STATUS: NOT CLEARED

**Audit target:** Planning Pack v1.3.7 CANDIDATE, correction cycle 2\
**Baseline:** v1.3.6\
**Operator:** Krishika\
**Author of corrections:** Claude (Anthropic), via Claude Code\
**Auditor:** ChatGPT, GPT-6 (OpenAI), independent of the author\
**Audit date:** 27 November 2026

## **1. Bundle identification**

**Uploaded ZIP SHA-256:**

```
4ee28f4651c8af4dd09c50299f2909b641ddadf55c0c70255bb2e529cb2c5cee
```

HASH COMPUTED

The uploaded ZIP was opened and its archive entries enumerated. The bundle metadata identifies the candidate as a 206-file v1.3.7 pack built from the 203-file v1.3.6 baseline.

## **2. Integrity verification**

| Check                                       | Method                                                    | Result                                                      |
| ------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------- |
| Uploaded ZIP SHA-256                        | **RUN** — computed from uploaded archive                  | PASS                                                        |
| `MANIFEST.sha256`                           | **RUN** — verified every listed file                      | PASS: 421/421                                               |
| Candidate `SHA256SUMS-v1.3.7-candidate.txt` | **RUN** — verified every listed candidate file            | PASS: 205/205                                               |
| Unlisted candidate files                    | **RUN** — compared checksum entries with actual directory | None; checksum file itself is excluded from its own entries |
| Baseline `27_SHA256SUMS.txt`                | **RUN** — verified extracted baseline files               | PASS: 202/202 present files                                 |
| Missing baseline archive entries            | **RUN** — checked documented archive exception            | 61 `archive_*` entries absent from extraction               |
| Candidate rebuild                           | **RUN** — executed `build_candidate.py` from bundle root  | PASS                                                        |
| Rebuilt candidate comparison                | **RUN** — compared all paths and file contents            | PASS: 206/206 byte-identical                                |
| Change-log sequence                         | **RUN** — checked edit identifiers                        | E01–E205 sequential                                         |
| Candidate run manifest hash                 | **RUN** — compared `summary.json` with bundled manifest   | MATCH                                                       |
| Candidate run results hash                  | **RUN** — recomputed `results.jsonl` SHA-256              | MATCH                                                       |
| Audit #1 report hash                        | **RUN** — recomputed SHA-256                              | MATCH                                                       |

### **Rebuild result**

Executed:

```
python proposals/v1.3.7/build_candidate.py /mnt/data/openvef_audit2_work/rebuilt_candidate
```

The build script reported:

- **205 edits processed**
- **206 files produced**
- **Zero missing paths**
- **Zero extra paths**
- **Zero differing files** against the bundled candidate

The candidate manifest SHA-256 is:

```
e704d194284c51bcac0f6ad20c119645c679bfce10fc71fe493ed0c02c9d7893
```

The candidate run's `summary.json` contains the same manifest hash. Its recorded `results_sha256` is `81c73e32cc7643c8900dd3f83c5824b5f7ae6ae82d90f140f4465b2f4c8acd09`, matching the independently computed hash of `results.jsonl`.

The bundled audit #1 report also matches its required SHA-256:

```
ba81408bde5339291d4b2ef25cab70b5eaa3e518412ecd45cdbeb11f54604b95
```

**Integrity limitation:** 61 `archive_*` entries named in the baseline checksum file are absent from the extracted baseline. They could not be individually verified. This is the exception disclosed in the audit brief, not a mismatch among the files that were present.

## **3. Cycle-2 correction assessment**

| Item | Verdict                | Assessment                                                                                                                                      |
| ---- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| OD-1 | **FAITHFUL WITH NOTE** | D-027's two specified error-class decisions are implemented and labelled. A-059's interpretation is supported, with owner review still pending. |
| OD-2 | **FAITHFUL**           | The Python 3.11 predicate representation, purity condition, evaluator execution and hash gate are explicitly adopted as an owner addition.      |
| OD-3 | **FAITHFUL**           | Protocol §20 provides the change-class/domain-validation inputs and control-vector schemas. No expected object or outcome code was changed.     |
| OD-4 | **FAITHFUL**           | `evaluator_repair_attempt` is defined consistently with the one-cycle limit and repeated-halt rule.                                             |
| A3   | **SOUND**              | Invalid supplied halt signatures are explicitly outside the executable fixture contract; no new outcome is introduced.                          |
| A4   | **SOUND**              | M37 is correctly described as a paired-outcome control vector, not source-level alias detection.                                                |
| C17  | **SOUND WITH NOTE**    | The named status statements were corrected, but the current File 21 checklist retains incomplete status wording. See D2-1.                      |

### **OD-1 — Error-class rule**

**Assessment: FAITHFUL WITH NOTE.**

Protocol L174 explicitly labels the owner addition and states that v1.3.6 did not specify the rule. The resulting assignments apply to exactly:

- `FEEDBACK_SERIALIZER_REJECT`
- `DESIGN_HALT_REPEATED`

I checked the relevant stage-map and local-ledger entries. The stated `SIMULATOR_ERROR` exception remains intact. The `—` in the error-class cell at L162 is correctly treated as an explicit statement that the row has no error class; it does not trigger another assignment to `DIAGNOSTIC_FORMAT_WARNING`.

A-059 extends the interpretation of “stage-map row” to the local-ledger vocabulary rows. Although those two codes are not literally rows in the L141–L162 table, D-027 item 3 names those exact codes. The interpretation therefore reaches the outcomes D-027 intended, without expanding the rule to additional codes.

**Note:** A-059 records that its interpretation is under owner review. That governance note remains visible; I found no third OD-1 assignment.

### **OD-2 — Legal-input predicate**

**Assessment: FAITHFUL.**

File 30 L83 explicitly marks the Python 3.11 representation as `OWNER-DECIDED OD-2`, rather than presenting it as a rule derived from v1.3.6.

The contract specifies:

- One function taking `(vector, sampled)`.
- A pure predicate, returning exactly Boolean `True` or `False`.
- Execution by the evaluator, outside artifact processes.
- SHA-256 verification of the UTF-8 source before execution.
- Exceptions, hash mismatches and invalid return values as evaluator failures, not artifact verdicts.

I independently computed the SHA-256 of M27's UTF-8 predicate source. It matches the fixture's lowercase 64-character `source_sha256`.

The document is also honest about the limit: the evaluator checks the hash and result, but cannot certify that arbitrary Python source is pure. Purity remains a condition imposed on the frozen predicate.

### **OD-3 — Control-vector schemas**

**Assessment: FAITHFUL.**

Protocol §20 is explicitly headed `OWNER-DECIDED OD-3`. Its opening explains that the owners adopt the schemas as normative and that the new vocabulary does not originate in v1.3.6.

I compared the expected properties against the descriptor objects.

- §20.1 defines the `change_class` input and separates `domain_validation`.
- §20.2 defines the common result properties.
- §20.3 defines the additional properties for M48, M50, M53, M54 and M58.
- §20.4 accounts for the other control vectors and identifies where their properties are fixed.

The `Properties no rule fixes: none` statement is supported by the descriptor comparison and the cited Protocol rules. The basis column distinguishes pack-derived rules from OD-3 vocabulary, earlier corrections, the A-033 reading and the stated ordering convention. It does not falsely represent the newly adopted vocabulary as v1.3.6 text.

The M54 input is now `domain_validation`, with `HALT_SIGNATURE_COMPONENT_ENUMERATION` no longer represented as a change class. This is consistent with the four change classes at Protocol L176 and the halt-signature domains at L185.

**No expected object changed. No new disposition, stage, diagnostic or outcome code was introduced.**

### **OD-4 — Recovery attempt**

**Assessment: FAITHFUL.**

Protocol L185 defines the attempt as the ordinal of the recovery cycle opened by the halt:

- A halt before any recovery cycle opens the permitted first cycle and has attempt `1`.
- A halt after that cycle has been used is the repeated-halt termination, not a second attempt.
- No attempt greater than `1` is valid.
- The attempt is not a halt-signature component.

This fits the v1.3.6 one-cycle allowance and prohibition on a second recovery cycle. File 36 L198 and L205 identify their dependency on OD-4. The M13 and M41 expected objects remain unchanged.

### **A3 and A4**

**A3 — SOUND.** Protocol L185 says an out-of-domain supplied halt signature is outside the executable fixture contract. It has no diagnostic, stage, error class, disposition or ledger record. That resolves D1-7 without inventing an outcome.

**A4 — SOUND.** File 36 L143 and L206 and the M37 description now identify it as a supplied paired-outcome control vector. The text expressly disclaims source-level alias detection. M37 remains OWNER-SPECIFIED under OS-2.

### **C17 — Status wording**

**SOUND WITH NOTE.**

The listed locations were updated:

- File 36 L3 and L176
- File 32 L21 and L33
- README L16, L35 and L46
- Protocol L559

The full status statements distinguish development-run evidence, formal F18 status and approval. They correctly avoid treating the supplied development run as an authorized F18 acceptance run.

However, this was not applied to every current status statement. File 21 remains an exception, detailed below.

## **4. Audit #1 finding resolution**

| Audit #1 finding | Original severity | Cycle-2 result      | Reason                                                                                                                       |
| ---------------- | ----------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| D1-1             | MAJOR             | **RESOLVED**        | OD-3 adopts the scope vocabulary, defines four change classes and separates domain validation.                               |
| D1-2             | PACK              | **RESOLVED**        | OD-3 supplies the missing control-vector schemas and rules.                                                                  |
| D1-3             | MAJOR             | **RESOLVED**        | OD-2 explicitly adopts the executable Python predicate contract as an owner addition.                                        |
| D1-4             | MAJOR             | **RESOLVED**        | Original C6 is superseded; A1 stands on OD-2 and retains the descriptor's own legal-input condition.                         |
| D1-5             | BLOCKER           | **RESOLVED**        | OD-1 explicitly decides the two previously unspecified error classes.                                                        |
| D1-6             | MAJOR             | **RESOLVED**        | OD-4 defines the attempt ordinal and repeated-halt relationship in §7b.                                                      |
| D1-7             | MAJOR             | **RESOLVED**        | A3 excludes invalid supplied signatures from the executable fixture contract.                                                |
| D1-8             | MINOR             | **RESOLVED**        | A4 relabels M37 as a paired-outcome control vector.                                                                          |
| D1-9             | MINOR             | **PARTLY RESOLVED** | The listed statuses were corrected, but File 21 still contains current status statements without the three-part distinction. |

## **5. Regression assessment**

| Regression check                       | Method                                                    | Result                                                                                                                  |
| -------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| C7 — version-neutral schema wording    | **REASONED** — inspected File 30 L7                       | PASS. Schema version is independent of planning-pack version.                                                           |
| C8 — TechRxiv provenance qualification | **REASONED** — inspected File 10 L174 and File 22 L8, L16 | PASS. Earlier synchronous-FIFO and numerical claims remain identified as unverified; abstract-only access is disclosed. |
| C9 — parser unit-vector contract       | **REASONED** — inspected File 36 L27 and Protocol L177    | PASS. Parser input and syntax-error column rule remain explicit.                                                        |
| C13 — truncation primitive             | **REASONED** — compared File 36 L196 with Protocol L168   | PASS. Byte cap, marker, UTF-8 boundary and output properties remain specified.                                          |
| C14 — JSON-escaping primitive          | **REASONED** — compared File 36 L197 with Protocol L168   | PASS. Encoding, indentation, key order, line endings and terminal newline remain specified.                             |
| A2 — copied normative text             | **RUN** — byte and line comparison                        | PASS.                                                                                                                   |
| File 25 copy                           | **RUN** — exact line comparison                           | PASS.                                                                                                                   |
| OWNER-SPECIFIED separation             | **RUN** — inspected descriptors, results and summary      | PASS.                                                                                                                   |

### **File 25 copy**

I compared the two required ranges:

- File 25 L33–L130 against candidate Protocol L90–L187: **98/98 lines exactly equal**.
- File 25 L1–L32 against v1.3.6: **byte-identical**.

The cycle-2 edits to Protocol L174, L176 and L185 are present in the copied normative text.

### **OWNER-SPECIFIED / OWNER-DECIDED separation**

The run records and `summary.json` retain the three separate categories.

| Category        | PASS    | FAIL  | NOT_IMPLEMENTED | ERROR |
| --------------- | ------- | ----- | --------------- | ----- |
| PACK-DERIVED    | 131     | 0     | 0               | 0     |
| OWNER-DECIDED   | 11      | 0     | 0               | 0     |
| OWNER-SPECIFIED | 1       | 0     | 1               | 0     |
| **Total**       | **143** | **0** | **1**           | **0** |

The OWNER-DECIDED fixture set is exactly:

- OD-1: M15, M42, M47
- OD-2: M27
- OD-3: M48, M50, M53, M54, M58
- OD-4: M13, M41

Every corresponding run record has `category = OWNER-DECIDED` and the appropriate `owner_decided` label.

M41 correctly retains `owner_specified = OS-1` as well as its OD-4 dependency. Under D-027 item 2, a fixture that depends on any OD rule counts as OWNER-DECIDED. The separate OWNER-SPECIFIED count therefore excludes M41. M37 and P17 remain OWNER-SPECIFIED.

### **Expected objects and fixture changes**

**RUN:** Compared all 144 fixture descriptors between baseline and candidate.

- 144/144 descriptor IDs match.
- **Zero expected objects changed.**
- Every candidate run record's expected object matches its descriptor.

A clarification about the brief's input-change statement: the full v1.3.6-to-candidate comparison shows changed descriptors M27, M37, M41, M42, M47 and M54. M41, M42 and M47 are earlier cycle-1 changes logged at E32–E37. The cycle-2 deltas are M27's OD-2 source hash, M54's `domain_validation` input key and M37's description-only relabelling. I found no unlogged cycle-2 fixture change.

## **6. New finding**

### **D2-1 — File 21 retains incomplete current status wording**

MINOR

**Location:** `21_Prompt_Equivalence_and_Mask_Traceability_Checklist_v1.3.7-candidate.md`, L52 and L70.

L52 states:

> F18 is **NOT RUN / NOT PASSED**. This checklist is a proposed test specification, not evidence that a parser, assembler, sandbox, harness or experiment has been implemented. No owner acceptance of A1–A11 is recorded; no work or LLM call is authorized.

L70 states:

> Current release status: F18 **NOT RUN / NOT PASSED**; A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE REQUIRED**.

**Problem:** File 21 is part of the current v1.3.7 candidate and explicitly labels L70 as the *current release status*. Neither statement distinguishes the supplied project development-run evidence from formal F18 status and approval. The bundle contains 143 development-run PASS records, but those records are not formal F18 acceptance.

The statements are not necessarily false about formal F18 status. They are incomplete under C17's requirement that current status wording distinguish all three parts.

**Required fix:** Update both statements to distinguish development-run evidence, formal F18 status and approval, while preserving the A1–A11 and X14 status. Historical v1.3.6 records should remain historical and should not be rewritten as current v1.3.7 status.

This is the remaining reason D1-9 is only partly resolved.

## **7. Limitations**

| ID   | Severity   | Limitation                                                                                                                                                                          |
| ---- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| L-01 | LIMITATION | The 61 `archive_*` baseline entries are absent from the extraction and could not be individually hash-verified.                                                                     |
| L-02 | LIMITATION | I did not independently execute the OpenVEF implementation or reproduce the supplied development run. Its supplied records and hashes were checked, not its behavioral correctness. |
| L-03 | LIMITATION | I did not run F18, certify its fixtures, or authorize any implementation, LLM or provider call. This is a document audit, not F18 acceptance.                                       |
| L-04 | LIMITATION | I did not retrieve and inspect the original TechRxiv PDF. C8 was checked against the pack's provenance treatment, not against the paper's full text.                                |
| L-05 | LIMITATION | I did not externally authenticate the build commit or owner-decision authorship; those are assessed from the bundle's own records.                                                  |

No BLOCKER, MAJOR or PACK finding remains in the correction-cycle-2 assessment. The remaining candidate finding is MINOR.

## **8. Final audit decision**

**OVERALL STATUS: NOT CLEARED**

The bundle integrity checks pass for all files present in the extraction. The candidate rebuilds byte-for-byte from v1.3.6, the change log is sequential, and all 144 expected objects remain unchanged.

OD-1 through OD-4 are faithful to D-027 and clearly labelled as owner additions. A3 and A4 are sound. The required regression checks, File 25 copy and OWNER-SPECIFIED separation remain sound.

**Reason for NOT CLEARED:** D2-1 remains open. File 21 still contains current status statements that omit the distinction between development-run evidence, formal F18 status and approval. This leaves D1-9 only partly resolved and C17 incompletely applied.

The 61 absent archive entries and the document-only scope are recorded limitations, not candidate-integrity failures.

**Final ruling: NOT CLEARED.**