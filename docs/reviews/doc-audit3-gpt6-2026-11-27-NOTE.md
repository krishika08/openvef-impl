# Note on document audit #3 of the v1.3.7 CANDIDATE (D-029 item 3, D-030)

**Not part of the report.** Written by Claude (Claude Opus 5.5, via Claude Code), the implementation author and
the author of every correction under audit, at Krishika's instruction.

**Copy and hash**
- [doc-audit3-gpt6-2026-11-27.md](doc-audit3-gpt6-2026-11-27.md): 17,895 bytes,
  SHA-256 `757ae6e53002b93bc8738cbe07fac36f865b6253dafd1d4d042fa2f3cd94a34f`.
- Krishika gave that hash and size and named the upload `docs/doc-audit3-gpt6-2026-11-27.md`, but no such file
  reached the workspace; the report arrived as a document attached to the Claude Code conversation. Claude wrote that
  text to a scratch file and checked it: 17,895 bytes and the given SHA-256, so it is byte-identical to what Krishika
  uploaded (no other variant was used). It was then copied here unchanged and re-hashed. The hash shows the file equals
  what Krishika gave, not that it equals the auditor's original output.
- **Auditor:** the report header names "GPT-6 (OpenAI), independent of the correction author", operator Krishika.
- **Order:** the report and this note are committed alone, before any D-030 change.

**Bundle hash.** The report gives `f82e13342664679e5caa8f56f42c5e6dde0ee1b04bab653fb7cc3c313290b26b`, which equals
`dist/openvef-docaudit-bundle.zip` (build commit `c24be7f`, committed `f5c6556`, release `docaudit3-f82e1334`).

**What the report says**
- **NOT CLEARED** on two LIMITATIONs: D3-1 (run-artifact continuity: audit #2's `results.jsonl` `81c73e32…cd09` and
  the current `4b9714a4…284b` differ, the old file is not bundled, so the brief's "Only the pinned pack hashes differ"
  is not confirmed) and D3-2 (`test_current_status_lines_have_three_parts` is lexical; a constructed sentence with the
  words in quotes passes). 0 BLOCKER, 0 MAJOR, 0 MINOR; five further named limitations (baseline archive entries,
  prior snapshot absent, test suite not runnable without `openvef`, implementation not audited, F18 not run).
- C18 SOUND WITH NOTE; D2-1 RESOLVED; D1-9 RESOLVED. Sweep totals reproduced (342 rows), 63 rows sampled.
- Regression PASS: OD-1 to OD-4, A1 to A4, File 25 copy, category counts, zero expected-object changes, changelog
  E01–E218 continuous.

**Checked by Claude against the audited zip** (extracted in a scratch directory): the zip holds 426 files;
`MANIFEST.sha256` has 425 lines and verifies; the CHANGELOG's last edit is E218. `docs/DOC-AUDIT3-BRIEF.md` L85 does say
"Only the pinned pack hashes differ."

**Points to read with care** (kept as written; not resolved here)
- D3-1 is a valid point against the brief. A read-only comparison by Claude before this commit found that the two
  runs' `results.jsonl` records differ in measured simulator timings (`simulator.l334` wall times, median and the
  derived timeout, 9 fixtures); the pack manifest hash is in `summary.json`, not in the records. The brief's sentence
  was therefore inaccurate; D-030 item 1 records the full diff and corrects it.
- The title says "Independent Document Audit". It is an AI document audit by a model other than the author, not a
  human independent review, and it is not an implementation audit.

It does not satisfy Protocol L555 (5) or L271, F18 is not passed, and the v1.3.7 candidate remains not audited-cleared.
