# Note on document audit #2 of the v1.3.7 CANDIDATE (D-027 item 10, D-029)

**Not part of the report.** Written by Claude (Claude Opus 5.5, via Claude Code), the implementation author and
the author of every correction under audit, at Krishika's instruction.

**Copy and hash**
- [doc-audit2-gpt6-2026-11-27.md](doc-audit2-gpt6-2026-11-27.md): 20,970 bytes,
  SHA-256 `b3534eee86e9af1f937e795223354498d994501be90dcc6e910d3a02297b6f13`.
- Uploaded by Krishika as `docs/doc-audit2-gpt6-2026-11-27.txt` with that hash and size. Claude checked both before
  and after moving the file here byte for byte (renamed only; not edited). The hash shows the file equals what
  Krishika uploaded, not that it equals the auditor's original output.
- **Auditor:** the report header names "ChatGPT, GPT-6 (OpenAI), independent of the author", operator Krishika.
- **Order:** the report and this note are committed alone, before any D-029 change.

**Bundle hash.** The report gives `4ee28f4651c8af4dd09c50299f2909b641ddadf55c0c70255bb2e529cb2c5cee`, which equals
`dist/openvef-docaudit-bundle.zip` (build commit `b9723b5`, release `docaudit2-4ee28f46`).

**What the report says**
- **NOT CLEARED.** 0 BLOCKER, 0 MAJOR, 1 MINOR (D2-1: File 21 L52 and L70 lack the three-part status split),
  0 PACK; limitations L-01 to L-05.
- Audit #1: D1-1 to D1-8 RESOLVED; D1-9 PARTLY RESOLVED (remaining part is D2-1).
- Verdicts: OD-1 FAITHFUL WITH NOTE (A-059 then still owner review pending); OD-2, OD-3, OD-4 FAITHFUL; A3, A4 SOUND;
  C17 SOUND WITH NOTE. Regression checks C7, C8, C9, C13, C14, A2, File 25 copy, OWNER-SPECIFIED separation PASS.
- Positive checks it reports running: manifest 421/421, candidate SHA256SUMS 205/205, baseline 202/202 (61 archive
  entries absent as disclosed), rebuild 206/206 byte for byte from 205 edits, zero expected-object changes over 144
  descriptors, category counts PACK-DERIVED 131/0/0/0, OWNER-DECIDED 11/0/0/0, OWNER-SPECIFIED 1/0/1/0.

**Checked by Claude against the audited zip** (extracted in a scratch directory): the zip holds 422 files;
`MANIFEST.sha256` has 421 lines and verifies; candidate `SHA256SUMS` has 205 lines; the CHANGELOG's last edit is E205;
`summary.json` gives `pack_manifest_sha256` `e704d194…7893` and `results_sha256` `81c73e32…cd09`, which equals the
computed hash of `results.jsonl`; `counts_by_category` is as the report states. The quoted File 21 L52 and L70 say
what the report quotes.

**Points to read with care** (kept as written; not resolved here)
- The title says "Independent Document Audit". It is an AI document audit by a model other than the author, not a
  human independent review, and it is not an implementation audit (L-02, L-03).
- The OD-1 note on A-059 reflects its state at audit time; D-029 item 2 records Krishika's approval afterwards.
- D2-1 names only L52 and L70; D-029 item 1 extends the fix to a sweep of every current status statement.

It does not satisfy Protocol L555 (5) or L271, F18 is not passed, and the v1.3.7 candidate remains not audited-cleared.
