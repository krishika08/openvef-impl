# Adoption of OpenVEF Planning v1.3.7 (owner decision D-035)

**Owner decision by Krishika, 28 Nov 2026**, on a Claude (claude.ai) triage of document audit #7. It takes effect under
D-008. **Ayush Kumar Singh's ratification is pending**; it stays the single "Ayush ratification pending" entry in
[AUDIT-READINESS.md](AUDIT-READINESS.md). Recorded by Claude (Claude Opus 5.5, via Claude Code) at Krishika's
instruction. Claude adopts nothing; the adoption is the owners' act.

**Effective:** now, as of D-035. It was recorded on 28 Nov 2026 at about 11:00 UTC, in the commit that adds this file.

## 1. The rule applied

The owner recorded this rule before document audit #5 (`docs/ambiguities.md`, D-031). D-032 and D-033 applied it
unchanged to audits #6 and #7, with "#5" read as the audit in question:

> "If document audit #5 finds no BLOCKER, MAJOR or MINOR finding, the owners adopt v1.3.7 as the corrected pack;
> every remaining LIMITATION is disclosed in DEVIATIONS.md. A lexical test cannot prove semantic correctness; that is
> established by the audited manual review."

Document audit #7 found no BLOCKER, MAJOR or MINOR finding (report section 6: "No BLOCKER, MAJOR or MINOR finding
remains in the D-033 candidate-audit scope"; section 7: "**CLEARED**"). The rule's condition is met, and the owners
adopt v1.3.7 as the corrected planning pack.

## 2. The owner record of A1–A11 and X14 for v1.3.7 (Protocol L555 (3))

v1.3.7 Protocol L555 (3) requires that "the owner must explicitly record acceptance or rejection of A1–A11 and choose
the X14 strict-AST branch".

D-035 records it as follows: **"Krishika states in D-035: for v1.3.7, A1–A11 are accepted as written (11/11) and X14
Option A is chosen."**

Provenance:
- Claude asked whether D-035 records A1–A11 and X14 for v1.3.7. The owner's instruction named only the pack adoption
  and the gate.
- The answer was given in the Claude Code session of 28 Nov 2026 (git user KRISHIKA) by selecting the option worded
  by Claude: "Add to D-035 now (Recommended)", whose text is the statement quoted above.
- The A1–A11 and X14 text is Register 16 (`16_OpenVEF_v1.3.6_Owner_Decision_Register.md`). It is byte-identical in
  v1.3.6 and v1.3.7, so "as written" names the same text in both packs.

The pack's own status lines are not edited. File 32 L40–L41 still read "A1–A11: PROPOSED / NOT ACCEPTED; owner
acceptance PENDING." and "X14: OWNER CHOICE REQUIRED.". The owner record is this decision, kept outside the pack, as
the v1.3.6 records are.

## 3. Document audits #1–#7

All seven are AI document audits by OpenAI GPT-6 (operator Krishika), a model other than the author. None is a human
independent review, and none is an implementation audit.

| # | Report (`docs/reviews/`) | Report SHA-256 | Bundle SHA-256 (release) | Verdict |
|---|---|---|---|---|
| 1 | `doc-audit1-gpt6-2026-11-27.md` | `ba81408bde5339291d4b2ef25cab70b5eaa3e518412ecd45cdbeb11f54604b95` | `c4caff409692797b4292a1c6851c79a722d1c60cbf4371e5611f5ef4f0a4cbd7` (`docaudit1-c4caff40`) | NOT CLEARED |
| 2 | `doc-audit2-gpt6-2026-11-27.md` | `b3534eee86e9af1f937e795223354498d994501be90dcc6e910d3a02297b6f13` | `4ee28f4651c8af4dd09c50299f2909b641ddadf55c0c70255bb2e529cb2c5cee` (`docaudit2-4ee28f46`) | NOT CLEARED |
| 3 | `doc-audit3-gpt6-2026-11-27.md` | `757ae6e53002b93bc8738cbe07fac36f865b6253dafd1d4d042fa2f3cd94a34f` | `f82e13342664679e5caa8f56f42c5e6dde0ee1b04bab653fb7cc3c313290b26b` (`docaudit3-f82e1334`) | NOT CLEARED |
| 4 | `doc-audit4-gpt6-2026-11-28.md` | `0cc724cd8c0661c216f956bd98628e2d359fe5702c87f5f3887a6046c8174850` | `f01d344d150d89aae0f545890a0e5c97ad2f49a4f6a0e88a9add6731fbfe73cb` (`docaudit4-f01d344d`) | NOT CLEARED |
| 5 | `doc-audit5-gpt6-2026-11-28.md` | `efb7b795c4a3dc5fe36d3151b3657fcfabcce704bd5240a85f23e0ccf1d725bb` | `5f35d75bd7a5fdac36aa8f49be1ad049fa339f61f62d5a8af20143408136cd47` (`docaudit5-5f35d75b`) | NOT CLEARED |
| 6 | `doc-audit6-gpt6-2026-11-28.md` | `809b2d863542ed50353dab64b8ca29509812afffc5691781598ac2046f2078c7` | `e9719fb37ff9c548b22c6b8262ef93b911bca9bb06bc79844acf684d91f86982` (`docaudit6-e9719fb3`) | NOT CLEARED |
| 7 | `doc-audit7-gpt6-2026-11-28.md` | `a948ab97207582037851ffa3f302e46a5f12b2c27cdc13e9d1e17465d9376a67` | `7e44902c5e6e20a0415b7f5c0eab5149a06456ed618f87887edf9cb5a711ed63` (`docaudit7-7e44902c`) | **CLEARED** |

**The adopted pack** is the candidate audited by audits #4 to #7:
- `SHA256SUMS-v1.3.7-candidate.txt` has SHA-256 `d64a91a8a13483866eb2788c19ce17ae268eac54d829d916bdd2926e161b3fff`;
- the fixture index is `b43da9263e690951754526d8bd334680df96db5bb20a9c19fd4f01f681d4c65d`;
- it has 206 files.

It is copied unchanged to `baseline-v1.3.7/OpenVEF_Planning_v1_3_7/` and released as `pack-v1.3.7`; see section 6.

## 4. What adoption means, and what it does not

**Adoption means:**
- v1.3.7 is the owners' corrected planning pack.
- It is the default pack for F18 runs (`--pack v1.3.7`, D-035 item 4). v1.3.6 stays selectable, and its records are
  unchanged. `baseline/` is never edited.
- **Protocol L555 (3) for v1.3.7 is recorded as met:** the document audit is cleared (audit #7), and the owner record
  is D-035 with section 2. v1.3.7 fixture runs from now on are therefore *authorized* development runs.
- The DEV-003 waiver ends, because it was a waiver only "until v1.3.7 is adopted or rejected". L4 closes.

**Adoption does not mean:**
- **It is not an implementation audit.** No document audit examined the implementation source (L2).
- **It is not F18 acceptance.** No formal F18 acceptance run exists. Every run, including the first authorized v1.3.7
  run, is a development run, and F18 is not passed (CLAUDE.md rule 8).
- **It does not satisfy Protocol L555 (5).** The independent implementation re-audit is not done, and under DEV-002 an
  AI audit would not be a human independent audit.
- **It does not satisfy Protocol L271.** The mask is cleared only under DEV-001 ("cleared under DEV-001
  (non-independent review saved)").
- It does not open the LLM-call gate (L555 (6)), F16, smoke tests, provider-format probes or confirmatory generation.
- It is not Ayush's ratification, which is pending.

## 5. Disclosed limitations carried forward

Every item below stays disclosed and open until its own "Ends when" in [DEVIATIONS.md](DEVIATIONS.md). None is closed
by adoption except L4.

| ID | Kind | Limitation | Status after D-035 |
|---|---|---|---|
| L1 | PACK | 61 `archive_*` objects named in baseline `27_SHA256SUMS.txt` are absent; only the 202 extracted baseline files are verified. | Open |
| L2 | LIMITATION | The implementation source was not in any document-audit bundle: M27 `check_e`, predicate purity and runner internals are not document-audited. | Open (until the L555 (5) re-audit, DEV-002) |
| L3 | LIMITATION | No formal F18 acceptance. The document audits do not satisfy L555 (5) or L271. | Open |
| L4 | DEPARTURE | Development fixture execution under the L555 (3) bar, waived by DEV-003. | **Closed at adoption** (D-035 item 3) |
| L5 | LIMITATION | The `simulator.l334` timing source and method are not established by a document audit. | Open |
| L6 | LIMITATION | No implementation approval. Owner acceptance of A1–A11 and X14 for v1.3.7 is now recorded (section 2). | Open for implementation approval only |
| D5-2 / D6-3 | LIMITATION | Lexical acceptance does not establish semantic truth, and the validator is blind to context and negation. The manual review stays mandatory whenever a status value changes. | Open |
| A7-ctx | LIMITATION | Audit #7's audit-context limitations: raw artifacts of 5 candidate runs, 10 control runs and 13 container-test runs were not in the bundle; the Ayush ratification entry and the assistance log were not supplied. | Open (disclosed) |
| DEV-001 | DEVIATION | No independent mask review (L271). | Open |
| DEV-002 | DEVIATION | The L555 (5) audit is by an AI model, not a human. | Open |
| D-016, D-019 | RESIDUALS | Wall-clock reads; runtime checks an artifact can forge (SELF_REPORTED). | Open |
| DEV-004 | v1.3.6 | "v1.3.6 gate recorded as met, with evidentiary gaps": 4 gaps, plus the L96 hash-attestation caveat (audit #7). | Open |

The D-031 stopping rule and the adoption apply to the planning pack only.
