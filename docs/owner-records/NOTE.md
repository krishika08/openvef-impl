# Note on the owner records (D-034)

**Not part of the records.** Written by Claude (Claude Opus 5.5, via Claude Code) at Krishika's instruction. The two
files in this directory are kept byte-for-byte as uploaded. Nothing in them was edited, reformatted or regenerated.

## Files and hashes

| File | Bytes | SHA-256 | Record and revision |
| --- | ---: | --- | --- |
| [owner-decision-record-rev25.md](owner-decision-record-rev25.md) | 10,604 | `64b836147ea35dbd2c98489513e8575fa3f0d1a130a5cf6973ec76d39c32594b` | OpenVEF Owner Decision Record (v1.3.6 baseline), revision 25 |
| [owner-signoff-pack-rev95.md](owner-signoff-pack-rev95.md) | 13,956 | `13b805cb3ec9cf91eda4a3cee8aa35e380f5a17512124b834fd4274c8159a83d` | OpenVEF Owner Sign-off Pack (v1.3.6), revision 95 |

## How they were exported and received

- Both are claude.ai Docs Markdown exports. Claude (claude.ai) made them on 28 Nov 2026 at Krishika's request.
  Krishika gave this description and the revision numbers. The files themselves contain no export metadata, so
  Claude Code cannot check the revision numbers or the export date.
- Krishika uploaded them through GitHub web to the repository root on `main`, in commit `ad3c109` ("Add files via
  upload"). They were moved here with `git mv` and re-hashed. Size and SHA-256 equal the values Krishika gave.
- The hashes show that these files equal what Krishika gave. They do not show that the files equal the live
  claude.ai documents, or what those documents read at any earlier time.

## Points to read with care (Claude's observations; not resolved here)

- **The Sign-off Pack export is a later revision.** At revision 95 it contains Amendment D-005, dated 24 Nov 2026. The
  export therefore shows the pack as it stood on 28 Nov 2026. It does not by itself show what Part 4 read at
  23 Nov 2026 13:54 IST. The Decision Record export is stated to be revision 25, the revision Part 4 adopts.
- **The records' own status lines say the documents are blank or unsigned:**
  - The Decision Record's title ends "— BLANK", and its L5 says "**Form status:** PARTLY COMPLETED, UNSIGNED."
  - Its §6.3 signature table (L149–L155) is empty. Its L157–L163 still lists "A1–A11: NOT ACCEPTED." … "Authorization:
    NONE." as the state "Until this section is signed and dated".
  - The Sign-off Pack's title ends "— BLANK", and its L5 says "Nothing in this pack is selected or signed."
  - Sign-off Pack Part 4 (L129) says its signature "substitutes for its §6.3 signature block".
- **Part 3 ticks items the Decision Record leaves blank.** This is gap (3) of DEV-004 in
  [../DEVIATIONS.md](../DEVIATIONS.md).
- The Part 3 item "Each signed file saved unchanged; SHA-256 of each exact signed file recorded" (L96) is ticked. No
  such hashes were in this repository before this commit.

These records bear on DEV-004 (the v1.3.6 L555 (3) gate). They are v1.3.6 owner records. They are not v1.3.7 adoption,
not F18 acceptance and not F18 evidence, and they satisfy neither Protocol L555 (5) nor L271.
