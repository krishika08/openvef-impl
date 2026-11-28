# Note on document audit #5 of the v1.3.7 CANDIDATE (D-031 item 3, D-032)

**Not part of the report.** Written by Claude (Claude Opus 5.5, via Claude Code), the implementation author and
the author of every correction and test under audit, at Krishika's instruction.

**Copy and hash**
- [doc-audit5-gpt6-2026-11-28.md](doc-audit5-gpt6-2026-11-28.md): 26,769 bytes,
  SHA-256 `efb7b795c4a3dc5fe36d3151b3657fcfabcce704bd5240a85f23e0ccf1d725bb`.
- Krishika gave that hash and size and named the upload `docs/doc-audit5-gpt6-2026-11-28.md`, but no such file
  reached the workspace (nor anywhere else on the machine); the report arrived as a document attached to the Claude Code
  conversation. Claude wrote that text to a scratch file and checked it: 26,769 bytes and the given SHA-256 at the first
  write, so it is byte-identical to what Krishika gave. (Three variants, without the final newline or the Markdown
  line-break spaces, were hashed only as a check that the match is not loose; none matched and none was used.) It was
  then copied here unchanged and re-hashed. The hash shows the file equals what Krishika gave, not that it equals the
  auditor's original output.
- **Auditor:** the report header names "OpenAI ChatGPT, GPT-6 (independent of the correction author)", operator
  Krishika.
- **Order:** the report and this note are committed alone, before any D-032 change.

**Bundle hash.** The report gives `5f35d75bd7a5fdac36aa8f49be1ad049fa339f61f62d5a8af20143408136cd47`, which equals
`dist/openvef-docaudit-bundle.zip` (build commit `431beaf`, committed `3a31633`, release `docaudit5-5f35d75b`).

**What the report says**
- **NOT CLEARED** on one **MINOR** finding, D5-1 (`labelled_status` checks the character before a label with
  `str.isalnum()`, which is false for `_`, so `x_Development-run evidence:` is accepted, although the docstring says a
  label is not preceded by a word character). Under the D-031 stopping rule a MINOR finding stops adoption; the report
  applies the rule and says it did not change any severity because of it.
- One further finding, D5-2 (LIMITATION): the run-ID form accepts any timestamp-shaped ID, and `APPROVAL_TAIL` accepts
  any sentence after a period; lexical acceptance does not establish truth. Six named limitations: (1) 61 baseline
  `archive_*` entries absent; (2) implementation source absent, M27 `check_e` skipped; (3) no formal F18 acceptance;
  (4) Protocol L555(3) says "no implementation or fixture execution is authorized" with no express development-only
  exception, while D-031 directed a development run; (5) simulator timing source absent; (6) no implementation
  approval or owner adoption.
- D3-2 RESOLVED; D4-1 PARTLY RESOLVED (through D5-1). Manual review PASS for all 17 lines and both fixture-index fields,
  with scope notes on Protocol L559 and File 36 L3. Integrity, rebuild and the C18 to C19 byte comparison PASS (E01–E218
  rows and 144 descriptors identical; 13 files differ). Regression PASS: OD-1 to OD-4, A1 to A4, File 25 copy, counts
  143/0/1/0, zero expected-object changes, run continuity.

**Checked by Claude.** The three probes of the report's section 3.2 return `[]` from the current `labelled_status`, as
the report says. `MANIFEST.sha256` in the audited zip has 649 lines (the report's 649 entries; `BUNDLE-INFO.json`'s
`"files": 648` leaves out `BUNDLE-INFO.json` and `MANIFEST.sha256`, as noted for audit #4).

**Points to read with care** (kept as written; not resolved here)
- D5-1 is a valid point against the test. The audited docstring promised "not preceded by ... a word character"; the
  code did not keep that promise for `_`. It is a fault in the test written by Claude, not in the pack text.
- Limitation 4 is a fair reading. Every development run since D-024 was made while Protocol L555(3)'s gate is unmet;
  the runs are labelled `run_class: development` and never called F18 acceptance, but the pack text names no exception.
- The title says "Independent Document Audit". It is an AI document audit by a model other than the author, not a
  human independent review, and it is not an implementation audit.

It does not satisfy Protocol L555 (5) or L271, F18 is not passed, and the v1.3.7 candidate remains not audited-cleared.
