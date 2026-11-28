# Claude v1.1 Audit Resolution — OpenVEF v1.2

**Date:** 22 November 2026  
**Status:** Technical correction draft; not owner-approved, not implemented, not independently re-audited.

## Audit outcome carried forward

The v1.1 audit returned **FAIL for the LLM-call gate** with five document-level blockers N1–N5. It verified hashes and rendering statically but did not execute the project's parser, assembler, harness or F18, did not make LLM/provider calls and did not access source PDFs. The uploaded tracker records 105 deterministic, 3 ambiguous and 3 contradictory expectations among 111 fixture descriptors. See `46_Claude_v1.1_Audit_Tracker_Snapshot.md`.

## Proposed resolutions

| v1.1 blocker | v1.2 proposal | Required independent check |
|---|---|---|
| N1 — non-ASCII identifier rule hidden / column and same-line import precedence unclear | B8 model-visible ASCII-only rule; `tokenize.NAME` scan after syntax parse and before import classification; first non-ASCII token by file/source order; UTF-8 byte column at token start | Confirm B8 is byte-identical to file 30; verify M35, M43–M46 and Python 3.11 column expectations |
| N2 — B5 fixed text has one-LF boundary | Remove design-specific lead-in from file 30's B5 fixed byte string; retain it as design-specific text in both prompts after exactly `\n\n` | Recompute fixed prefix and verify exact two-LF boundary in both arms and checklist |
| N3 — redaction text contradicts closed serializer | Remove path redaction; validate complete closed grammar, truncate at UTF-8 code-point boundary with marker inside 2,048-byte cap, then JSON-escape | Search all current controlling files; compare Protocol, file 25, file 31 and checklist; verify M14/M15/M17 |
| N4 — §7b recovery/refreeze and “same condition” ambiguous | One recovery cycle; distinguish unchanged-hash operational recovery from evaluator revision (new hashes and F16, reuse same artifact bytes only if author-visible/estimand unchanged) and author-visible revision (new freeze and fresh generation); define exact halt signature and second-halt termination | Validate M41/M42/M47/M48 and a full lifecycle truth table |
| N5 — ENTRY_POINT_REJECT reason/symbol assignment ambiguous | Fixed required-symbol order, class/method/nested/decorator precedence and canonical symbol names | Re-evaluate M01/M02/M39/M49 and add multi-defect fixture outcomes |

## Fixture corrections

- M13: change local error class to `EVALUATOR_INFRASTRUCTURE_FAILURE`; keep diagnostic `SIMULATOR_ERROR|target=null|class=RuntimeError`.
- M14: retain 2,048-byte cap as input; expected serialized result is 2,047 bytes for the specified boundary case.
- P42: accepted response has `diagnostic: null`, not an em-dash string.
- M01/M02/M39 become unambiguous under the deterministic symbol table; add M49 to test multi-defect ordering.
- Add P44–P48 for import precedence and M43–M48 for non-ASCII and lifecycle rules.
- The v1.2 catalog/index declare 124 mandatory fixtures; all remain **NOT RUN / NOT PASSED**. Hashes and expected descriptors are documentary/static checks, not F18 results.

## Owner decisions and authorization

A1–A11 remain **PROPOSED / NOT ACCEPTED**. X14 remains **OWNER CHOICE REQUIRED**. Owner, TEEP applicant, contributors and approver identities remain **TO CONFIRM against the actual TEEP application**. X16–X21 are proposed technical corrections only.

**Current authorization: NONE.** The v1.2 pack authorizes no hand-built work, implementation, fixture execution, provider probe, F16 or LLM call. After the owner records A1–A11 and X14, only the explicitly defined hand-built FIFO feasibility scope may open. LLM calls remain prohibited until N1–N5 and the entire mandatory fixture suite pass a further independent audit. Confirmatory generation remains prohibited until every Protocol §18 freeze item is sealed.
