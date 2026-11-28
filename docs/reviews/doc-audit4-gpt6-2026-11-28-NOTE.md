# Note on document audit #4 of the v1.3.7 CANDIDATE (D-030 item 3, D-031)

**Not part of the report.** Written by Claude (Claude Opus 5.5, via Claude Code), the implementation author and
the author of every correction under audit, at Krishika's instruction.

**Copy and hash**
- [doc-audit4-gpt6-2026-11-28.md](doc-audit4-gpt6-2026-11-28.md): 21,006 bytes,
  SHA-256 `0cc724cd8c0661c216f956bd98628e2d359fe5702c87f5f3887a6046c8174850`.
- Krishika gave that hash and size and named the upload `docs/doc-audit4-gpt6-2026-11-28.md`. The file actually
  arrived untracked at the repository root (`doc-audit4-gpt6-2026-11-28.md`), with no copy under `docs/`. Claude
  checked it there (21,006 bytes, the given SHA-256), moved it here with `mv` (no rewrite) and re-hashed it: unchanged.
  The hash shows the file equals what Krishika gave, not that it equals the auditor's original output.
- **Auditor:** the report header names "GPT-6 (OpenAI), independent of the correction author", operator Krishika.
- **Order:** the report and this note are committed alone, before any D-031 change.

**Bundle hash.** The report gives `f01d344d150d89aae0f545890a0e5c97ad2f49a4f6a0e88a9add6731fbfe73cb`, which equals
`dist/openvef-docaudit-bundle.zip` (build commit `95fe05d`, committed `5745eee`, release `docaudit4-f01d344d`).

**What the report says**
- **NOT CLEARED** on one LIMITATION: D4-1 (`labelled_status` in `tests/test_v137_candidate_pack.py` accepts a line
  whose three labels sit inside a single-quoted block, because the quote-parity check counts `"` and `` ` `` but not
  `'`; accepts placeholder values `x`, `y`, `z`; matches `label + ":"` rather than `label + ": "`). 0 BLOCKER,
  0 MAJOR, 0 MINOR; five further named limitations (61 baseline `archive_*` entries absent, prior C18 candidate
  snapshot absent, `openvef` absent so the M27 test is skipped, simulator timing source absent, F18 not run).
- D3-1 RESOLVED (both continuity reports reproduced; across three runs no status, category, actual or expected value
  differs). C19 wording SOUND WITH NOTE (all 17 lines and both fixture-index fields). D3-2 PARTLY RESOLVED, through D4-1.
  The report finds no defect in the pack text.
- Regression PASS: OD-1 to OD-4, A1 to A4, File 25 copy, category counts (143/0/1/0), zero expected-object changes,
  E01–E237 continuous.

**Checked by Claude against the audited zip** (extracted in a scratch directory): the zip holds 437 files;
`MANIFEST.sha256` has 436 lines (every file except itself) and verifies. `BUNDLE-INFO.json` says `"files": 435`, the
count recorded in the traceability row and the bundle commit; that count leaves out `BUNDLE-INFO.json` and
`MANIFEST.sha256`, so it does not contradict the auditor's 436/436. Claude ran the audited `labelled_status` on the
auditor's single-quoted line, the `x`/`y`/`z` line and a `label:` line with no space: all three return `[]`, as the
report says.

**Points to read with care** (kept as written; not resolved here)
- D4-1 is a valid point against the test, not against the pack text. The docstring of `labelled_status` promises
  that a label inside quotation marks does not count and that each label is followed by `": "`; the code keeps
  neither promise for `'` or for the separator. The report's own fix says a lexical validator should check
  "meaningful status content"; a closed vocabulary can only reject placeholders, it cannot prove a value is true.
- The title says "Independent Document Audit". It is an AI document audit by a model other than the author, not a
  human independent review, and it is not an implementation audit.

It does not satisfy Protocol L555 (5) or L271, F18 is not passed, and the v1.3.7 candidate remains not audited-cleared.
