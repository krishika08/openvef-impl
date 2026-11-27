# OpenVEF Prompt Assembly and Canonicalization Specification v1.3.7-candidate

**Status:** Normative proposed specification for F18. Not frozen until independent review and owner approval. Status, in three separate parts: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.

## 1. Source-template format

- Template encoding is strict UTF-8 without BOM; line endings are LF only.
- Exactly the first three metadata lines are removed, followed by exactly the one blank line that follows them. No other source-template lines are stripped as metadata.
- Each model-visible block starts at an exact complete line equal to one of the nine reserved headings in the sidecar. The heading line is included in the rendered model-visible message.
- Block body continues to the next known heading or end of file. The block order comes only from the template file and is checked against the sidecar's exact arm order.
- Reject unknown, duplicate, missing or malformed headings. Reject a payload line that is exactly equal to any reserved heading after LF normalization. No backslash escape or heading de-escaping is performed.
- No model-visible text may contain `ORG-A`, `ORG-B`, a standalone ordinal token matching `\bB[0-8]\b`, or assembler metadata markers. Payload authors must not use standalone B0–B8 tokens as identifiers; the F18 check uses the exact word-boundary regex.
- The sidecar is assembler-only (`model_visible=false`); never include its contents, hidden IDs, file names or arm labels in provider messages.

## 2. Block inventory and order

The fixed heading-to-ID mapping and the two exact orders are in `33_Prompt_Assembly_Sidecar_v1.3.7-candidate.json`:
- ORG-A: B0, B1, B2, B3, B4, B5, B6, B7, B8.
- ORG-B: B0, B2, B5, B1, B6, B3, B7, B4, B8.

B0 and B8 remain first and last. Only whole blocks B1–B7 are permuted. The interpretation is limited to these two exact orders, not ordering generally.

## 3. Payload insertion

- Each design-specific payload is sourced from the frozen author-packet manifest. The same exact payload bytes are inserted into the corresponding block in both arms.
- Convert CRLF and CR to LF once at payload ingestion; reject invalid UTF-8 and BOM. Do not otherwise paraphrase, reflow, trim or normalize payload bytes before the block-specific rendering rule.
- If any payload line equals one of the reserved headings after LF normalization, packet freeze fails. Do not escape, prefix or alter the payload to bypass this rule.
- Every required placeholder must occur exactly once per arm. All placeholders use double-brace syntax `{{UPPER_SNAKE_CASE}}`. Missing, duplicate or unresolved matches of `\{\{[A-Z0-9_]+\}\}` are hard errors.
- The authoring-packet manifest must contain `clause_id_regex`, `clause_ids`, and the seven payload sources listed in the sidecar. `clause_id_regex` is a fully anchored regular expression; the v1.0 proposed pattern is `^[A-Z]{2,6}-[0-9]{3}$`. `clause_ids` must be a duplicate-free, lexicographically sorted array of strings, each of which fully matches that pattern. The reserved value `UNSPECIFIED` is not a clause ID and must never appear in `clause_ids`.
- At packet freeze, extract the seven design-specific payload regions named in `visible_clause_id_sources` from the frozen manifest, after removing only their fixed non-citable contract prefixes from the `[Driver API]` and `[Checker contract]` blocks. Search those payload bytes using `clause_id_search_regex = (?<![A-Za-z0-9_-])[A-Z]{2,6}-[0-9]{3}(?![A-Za-z0-9_-])`. Separately scan for malformed near-matches using `clause_id_near_match_regex = (?<![A-Za-z0-9_-])[A-Za-z]{2,6}-[0-9]{1,3}(?![A-Za-z0-9_-])`. A candidate that is not an exact full match of `clause_id_regex` is a packet-freeze error. F18 records the extracted exact-ID set and requires equality with manifest `clause_ids`; no visible valid ID may be absent from the manifest and no manifest ID may be absent from visible payloads. This rule is mechanical and uses Python 3.11 regular-expression semantics.
- The fixed normative contract paragraphs in the B5, B7 and B8 blocks are explicitly non-citable. Model-visible contract obligations in those fixed paragraphs must not be cited in assumptions. An author may use `UNSPECIFIED` only for behavior that is genuinely absent from the design-specific authoring packet, with a non-empty explanation of the missing behavior. The parser accepts `UNSPECIFIED` as the reserved sentinel and validates every other assumption `clause_id` against the frozen manifest set.
- Each design-specific clause appears in exactly one payload block unless an intentional duplication is declared; any declared duplication must have byte-identical clause text in both arms and be listed in `clause_appears_in_blocks` as a semicolon-separated list of visible heading labels in lexical order.

## 4. Frozen schema insertion

- The schema is `34_OpenVEF_Response_Schema_v1.0.json`. Schema version `1.0` is independent of planning-pack version `1.3`.
- The sole schema placeholder is `{{OPENVEF_RESPONSE_SCHEMA_JSON}}`. The literal placeholder syntax is double-brace throughout this specification, both templates and sidecar. Replace only the exact standalone double-brace placeholder token bytes with the complete schema-file byte sequence, byte-for-byte; retain the template LF that terminates the placeholder line. Because the schema file itself ends with LF, the rendered B8 contains that schema-terminal LF followed by the retained template LF before `END_OPENVEF_RESPONSE_SCHEMA_JSON`. This two-LF boundary is intentional and is included in the sidecar prompt-stage hashes. Do not parse/re-serialize, pretty-print or normalize schema contents. Preserve both `BEGIN_OPENVEF_RESPONSE_SCHEMA_JSON` / `END_OPENVEF_RESPONSE_SCHEMA_JSON` lines.
- Schema SHA-256 is `6fb5d282b09540949f21ee134b522841c3345031cb3e118a83bdffc18b4e7c34` and file/inserted byte length is `2529`. Record these values in the sidecar. Both arms must contain exactly these same schema bytes. Any schema change requires rebuilding both arms and re-running F18.

## 5. Common system and repair messages (file 25)

The common messages are extracted only from `25_Common_System_and_Repair_Prompt_Templates.txt` using the exact marker lines below. Assembler notes and control rules are never model-visible.

**System message extraction:**
1. Find the exact line `--- BEGIN MODEL-VISIBLE SYSTEM-MESSAGE BODY ---`.
2. Extract all subsequent lines strictly before the exact line `--- END MODEL-VISIBLE SYSTEM-MESSAGE BODY ---`.
3. Remove all leading and trailing empty lines (lines of length zero; whitespace-only lines are not silently converted).
4. Join with LF and append exactly one terminal LF.
5. Do not include either marker line, the assembler note or control rules.

**Repair message extraction:**
1. Find the exact line `--- BEGIN MODEL-VISIBLE REPAIR-MESSAGE BODY ---`.
2. Extract all subsequent lines strictly before the exact line `--- END MODEL-VISIBLE REPAIR-MESSAGE BODY ---`.
3. Remove all leading and trailing empty lines; join with LF; append exactly one terminal LF.
4. Retain the literal `[VALIDATION_FEEDBACK_JSON]` marker and the JSON block's two-space indentation. At send time replace the three placeholder values only; do not remove the marker or reflow the JSON.
5. Dynamic feedback JSON serialization: first validate the complete diagnostic against the closed grammar; do not rewrite or normalize content. If it exceeds 2,048 UTF-8 bytes, truncate to the longest complete-code-point prefix that leaves room for `...[TRUNCATED]` inside the 2,048-byte cap; output need not fill the cap. Then JSON-escape and serialize UTF-8 with `ensure_ascii=false`, key order `stage_id`, `error_class`, `diagnostic`, two-space indentation, LF line endings and one final LF. Grammar validation is performed before truncation and is not repeated after truncation.
6. In the extracted repair body, replace `{{STAGE_ID}}` and `{{ERROR_CLASS}}` with JSON-string contents (without outer quotes), and replace `{{DIAGNOSTIC_JSON_STRING}}` with a complete JSON string literal including its outer quotes. The literal key order, two-space indentation, `[VALIDATION_FEEDBACK_JSON]` marker and all other repair-message bytes remain unchanged. No placeholder may remain after rendering.
7. At pack revision, compute and record the exact static extracted system-message and repair-template SHA-256 values and byte lengths in the sidecar. At each repair, additionally hash the fully substituted dynamic repair message and record that per-call hash in the F18 run ledger.

The extracted system and repair bytes, their message roles and their SHA-256 hashes are recorded in the sidecar and final F18 report. No content substitution or normalization is permitted in dynamic feedback; non-normative/path-bearing diagnostics are rejected by the closed grammar before serialization. The system body is one provider `system` message. The assembled arm template is one `user` message. Model replies use the `assistant` role. Each repair is a new `user` message appended to the complete, byte-identically resent prior message array.

## 6. Template rendering

- Parse each arm into its nine blocks using exact headings.
- Insert the frozen schema bytes into B8 and insert design payloads into their unique placeholders.
- For each block, render its heading, one LF, then its block body after removing all leading and trailing empty lines only; preserve all internal bytes and whitespace.
- Join rendered blocks with exactly two LF characters.
- The complete user prompt has no leading blank line and exactly one terminal LF.
- Do not include metadata, hidden IDs, sidecar data or arm labels.

## 7. Canonical normalization and hashing

For each corresponding semantic block independently:
1. Decode strict UTF-8; reject BOM and invalid sequences.
2. Convert CRLF and CR to LF.
3. Normalize Unicode to NFC.
4. Trim leading/trailing whitespace from the block for the canonical comparison only.
5. Collapse every contiguous run of Unicode whitespace to one ASCII space.
6. Preserve case, punctuation, Markdown markers and all non-whitespace characters.
7. Compare canonical UTF-8 bytes and also compare raw block body bytes after line-ending normalization. Any difference fails F18.

The fixed B5, B7 and B8 normative text in file 30 §3.1 must be the exact byte prefix of its corresponding model-visible block body, followed by exactly two LF bytes (`\n\n`) before any design-specific lead-in or schema delimiter. For B5, the fixed-text boundary ends after the final sentence about the fixed import allow-list/no-third-party rule; the following `Design-specific API and top-level port details:` line is not part of the fixed-text byte string and must follow the two-LF separator. The fixed-text boundary is not inferred from a semantic re-parse.

Hash source templates, payloads, sidecar, manifest, schema, extracted system/repair messages, assembled system/ORG-A/ORG-B/repair message bytes, per-block raw/canonical bytes and final message-role sequence with SHA-256 over the exact UTF-8 bytes. Recompute every affected hash after all v1.3.7-candidate document and model-visible text edits are complete. This v1.3.7-candidate release does not alter the model-visible ORG-A/ORG-B templates or the schema/system/repair messages; the verified v1.3.4 template-stage prompt hashes therefore carry forward unchanged. The v1.1, v1.2, v1.3 and v1.3.1 prompt-template-stage hashes are historical and superseded; retain their exact values in the v1.3.7-candidate sidecar for audit history, but never use them as current prompt hashes. Record the schema SHA-256/byte length, each payload SHA-256/byte length, and the template-stage ORG-A/ORG-B hashes (with design placeholders still unresolved) in the sidecar. The sidecar field `spec_version_sha256` must equal the manifest field `spec_version_sha256` byte-for-byte after freeze; `manifest_spec_version_sha256_field` identifies that manifest field, and `manifest_spec_version_sha256` is a recorded copy for an explicit equality check. Final assembled prompts are hashed only after all seven payloads are frozen. No implicit trimming, escaping, newline conversion or metadata stripping beyond the rules above is permitted.


## 8. Clause-ID token extraction and near-match policy

The manifest contains these three regex strings (all are interpreted by the pinned Python 3.11 `re` engine):

- `clause_id_regex`: anchored full match `^[A-Z]{2,6}-[0-9]{3}$`, applied independently to every `clause_ids` element.
- `clause_id_search_regex`: token search `(?<![A-Za-z0-9_-])[A-Z]{2,6}-[0-9]{3}(?![A-Za-z0-9_-])`, used to extract exact visible clause-ID tokens from the seven payload regions.
- `clause_id_near_match_regex`: token search `(?<![A-Za-z0-9_-])[A-Za-z]{2,6}-[0-9]{1,3}(?![A-Za-z0-9_-])`, used to detect candidate clause-like tokens. A candidate that is not also a full match of `clause_id_regex` is a packet-freeze error.

The `clause_ids` array is unique, sorted lexicographically, and every element must fully match `clause_id_regex`. Extract exact tokens only from the seven `visible_clause_id_sources`, excluding the fixed non-citable B5/B7 contract prefixes. The extracted set must equal the manifest set exactly. An assumption clause ID is either a member of that set or the exact reserved sentinel `UNSPECIFIED`; clause rejection uses the lowest numeric failing assumptions index and pointer `/assumptions/<index>/clause_id`.

F18 records the raw payload bytes, exact extracted IDs, near-match candidates, manifest IDs and comparison result. No `true` validation result may be written to the sidecar before F18 runs; pending checks must be `REQUIRED` or `null`.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
