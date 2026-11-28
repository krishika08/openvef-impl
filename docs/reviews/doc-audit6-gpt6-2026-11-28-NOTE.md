# Note on document audit #6 of the v1.3.7 CANDIDATE (D-032 item 4, D-033)

**Not part of the report.** Written by Claude (Claude Opus 5.5, via Claude Code), the implementation author and
the author of every correction and test under audit, at Krishika's instruction.

**Copy and hash**
- [doc-audit6-gpt6-2026-11-28.md](doc-audit6-gpt6-2026-11-28.md): 17,645 bytes,
  SHA-256 `809b2d863542ed50353dab64b8ca29509812afffc5691781598ac2046f2078c7`.
- Krishika uploaded it through GitHub web to the repository root on `main` (commit `ad3c109`, "Add files via upload").
  The upload arrived named `doc-audit6-gpt6-2026-11-28 (3).md`, not the name Krishika gave
  (`doc-audit6-gpt6-2026-11-28.md`). Its size and SHA-256 equal the values Krishika gave. It was moved here with
  `git mv`, unchanged, under the name Krishika gave, and re-hashed. The hash shows the file equals what Krishika gave,
  not that it equals the auditor's original output.
- **Auditor:** the report header names "OpenAI GPT-6", operator Krishika.
- **Order:** the report and this note are committed alone, before any D-033 or D-034 change.

**Bundle hash.** The report gives `e9719fb37ff9c548b22c6b8262ef93b911bca9bb06bc79844acf684d91f86982`, which equals
`dist/openvef-docaudit-bundle.zip` (build commit `2451a00`, committed `2ae9ede`, release `docaudit6-e9719fb3`).

**What the report says**
- **NOT CLEARED** on two findings. Under the D-031 stopping rule (reaffirmed by D-032) a MINOR or MAJOR finding stops
  adoption. The report says it applied the severity scale independently and did not adjust severities to satisfy the rule.
  - **D6-1 (MINOR):** a combining mark before a label, such as U+0301 in `x́Development-run evidence:`, passes the
    one-code-point `\w` boundary check. D5-1 (the underscore case) is RESOLVED. D4-1 is still PARTLY RESOLVED.
  - **D6-2 (MAJOR):** the D-032 owner interpretation, that development runs are not fixture execution under Protocol
    L555(3), is not the best-supported reading of the clause. The report suggests two fixes: record the runs as an
    explicit owner-authorized deviation or waiver and keep L4 disclosed as a departure, or amend the Protocol and
    re-audit. It says L4 should not be marked ended by the interpretation.
- **D6-3 (LIMITATION):** the validator does not read context or negation. A prefix such as "it is only an example:"
  still passes, and the report asks for this case to be added under D5-2. The other limitations, L1–L6 and D5-2, are
  carried forward.
- PASS results:
  - integrity: 656 manifest entries, 205 candidate sums, 205 C18 sums, and 202 baseline files with 61 archive
    objects absent;
  - prior reports #1–#5 and run hashes, and a byte-identical rebuild;
  - tests: 19 discovered, 18 passed, 1 skipped (`test_corrected_m27_reaches_check_e`), plus 7 of 7 in `test_diff_runs.py`;
  - the L555(3) quote is accurate;
  - regression: OD-1 to OD-4, A1 to A4, the File 25 copy, counts 143/0/1/0, zero expected-object changes, and
    continuity against audit #5 (9 rows differ, only in `simulator.l334` timings).
- Manual review was carried forward from audit #5 by manifest identity, not repeated.

**Checked by Claude**
- Both probe lines of the report's section 2 return `[]` from `labelled_status` as audited (`HEAD` at `3f14c17`), as
  the report says.
- `MANIFEST.sha256` in the audited zip has 656 lines: `BUNDLE-INFO.json`'s `"files": 655` plus `BUNDLE-INFO.json`
  itself. The zip holds 657 entries, including `MANIFEST.sha256`.

**Points to read with care** (kept as written; not resolved here)
- D6-1 is a valid point against the test written by Claude, not against the pack text.
- D6-2 is a fair reading. `docs/DEVIATIONS.md` as audited gave L4's "Ends when" as "Answered by the owner
  interpretation". That treated a textual departure as closed.
- The title says "Independent Document Audit". It is an AI document audit by a model other than the author. It is not a
  human independent review, and it is not an implementation audit.

It does not satisfy Protocol L555 (5) or L271, F18 is not passed, and the v1.3.7 candidate remains not audited-cleared.
