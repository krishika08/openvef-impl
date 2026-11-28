# Note on document audit #7 of the v1.3.7 CANDIDATE (D-033 item 4, D-035)

**Not part of the report.** Written by Claude (Claude Opus 5.5, via Claude Code), the implementation author and
the author of every correction and test under audit, at Krishika's instruction.

**Copy and hash**
- [doc-audit7-gpt6-2026-11-28.md](doc-audit7-gpt6-2026-11-28.md): 27,218 bytes,
  SHA-256 `a948ab97207582037851ffa3f302e46a5f12b2c27cdc13e9d1e17465d9376a67`.
- Krishika uploaded it through GitHub web to the repository root on `main` (commit `b8e37e4`, "Add files via upload"),
  under the name given. Its size and SHA-256 equal the values Krishika gave. It was moved here with `git mv`, unchanged,
  and re-hashed. The hash shows the file equals what Krishika gave, not that it equals the auditor's original output.
- **Auditor:** the header names the auditor twice, differently. L4 reads "**Auditor:** Independent review"; L17 reads
  "**Auditor:** OpenAI GPT-6". Operator Krishika.
- **Order:** the report and this note are committed alone, before any D-035 change.

**Bundle hash.** The report gives `7e44902c5e6e20a0415b7f5c0eab5149a06456ed618f87887edf9cb5a711ed63`, which equals
`dist/openvef-docaudit-bundle.zip` (build commit `cc4bf41`, committed `fa15db9`, release `docaudit7-7e44902c`).

**What the report says**
- **CLEARED.** It finds no BLOCKER, MAJOR or MINOR finding in the D-033 scope (section 6). The report says it applied
  the severity scale independently of the stopping rule (section 7).
- **Resolved:** D6-1, D4-1 and D6-2.
- **Integrity PASS:**
  - 666 zip entries; 665 manifest entries;
  - 205 of 205 candidate sums, and 205 of 205 C18 sums;
  - 202 baseline files, with 61 archive objects absent;
  - a byte-identical rebuild of 206 files;
  - six run hashes;
  - reports #1–#6 and both owner records.
- **Regression PASS:** the 17 status lines and both index fields are unchanged (by manifest identity), as are E01–E237,
  the 144 descriptors, OD-1 to OD-4, A1 to A4 (with the implementation limitation), the File 25 copy, zero
  expected-object changes, the counts (143/0/1/0), and continuity against audit #6. The manual review was carried
  forward, not repeated.
- **Named limitations still open:**
  - L1 (PACK);
  - L2, L3, L5, L6;
  - L4 (DEPARTURE), "open until v1.3.7 is adopted or rejected";
  - D5-2 with D6-3.
- **Audit-context limitations:**
  - raw artifacts for 5 candidate runs, 10 control runs and 13 container-test runs are not in the bundle;
  - the Ayush ratification entry was not supplied;
  - the assistance log cited by DEV-004 was not supplied;
  - the Sign-off Pack L96 hash attestation has no historical hashes behind it.
- **DEV-004 (context, v1.3.6):**
  - the quotes and line numbers are accurate, and the four gaps are supported;
  - the §1 mismatch in gap 3 is Claude's addition, and DEV-004 "should not imply otherwise";
  - the L96 hash-attestation caveat should be explicit in DEV-004;
  - Sign-off Pack L5 ("Nothing in this pack is selected or signed.") is in "unresolved tension" with its marked
    contents.

  The report says this "is not a finding against the v1.3.7 candidate".

**Checked by Claude**
- The bundle hash is as stated above.
- `docs/ambiguities.md` L2207–L2209, which the report cites, is the D-034 paragraph that records the §1 addition as
  Claude's.

**Points to read with care** (kept as written; not resolved here)
- The two auditor lines in the header (L4, L17) differ. L17 and the rest of the report name OpenAI GPT-6.
- The title of brief #7 calls the audit a document audit, and the report says the same. It is an AI document audit
  by a model other than the author. It is not a human independent review, and it is not an implementation audit.
- Clearance applies "under the document-audit #7 / D-033 stopping rule only" (section 7). Adoption is the owners' act.

It does not satisfy Protocol L555 (5) or L271, and F18 is not passed.
