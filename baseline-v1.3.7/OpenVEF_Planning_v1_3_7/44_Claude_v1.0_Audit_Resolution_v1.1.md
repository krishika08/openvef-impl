# Claude v1.0 Audit Resolution — OpenVEF v1.1

**Audit verdict:** FAIL for the LLM-call gate. This document records the proposed response; it does not assert that B1–B9 passed re-audit.

## Blocker-to-correction map

| v1.0 blocker | v1.1 proposal | Files / fixtures | Status |
|---|---|---|---|
| B1 malformed M10–M12 fixture response shape | Checker `source` is a valid string; simulated outcomes are sibling `input.null_runs` | `41_F18_Fixture_Inputs/M10.json`–`M12.json` | PROPOSED / NOT RUN |
| B2 M01/M03 fail before target defect | Add valid `create_driver` to both fixture driver sources | M01, M03 | PROPOSED / NOT RUN |
| B3 error-class mismatch | Align fixture error_class with map category; diagnostic code remains specific | P27, M03, M34; Protocol §3.4 | PROPOSED / NOT RUN |
| B4 class/function stage overlap | Module-policy stage explicitly defers FunctionDef/ClassDef; AST_SIGNATURE owns class/decorator/nesting | Protocol §3.4; file 30; M02, M03, M38, M39 | PROPOSED / NOT RUN |
| B5 incomplete import precedence | Total precedence for Import and ImportFrom, including multiple names and conflict pairs | Protocol §3.4; file 30 §2; P29a/P29b/P30/P31–P43 | PROPOSED / NOT RUN |
| B6 non-ASCII/column behavior | Fixed non-ASCII identifier diagnostic; offset fallback column=1; pin CPython 3.11 and reconfirm P25 | Protocol §3.4; M35/M36 | PROPOSED / NOT RUN |
| B7 mid-run halt accounting | Pause, one evaluator repair, re-run every design slot with identical frozen artifacts; second occurrence aborts all slots | Protocol §3.4/§7b; M13/M41/M42 | PROPOSED / NOT RUN |
| B8 local F18 vocabulary and path handling | Define F18 dispositions/stages/codes separately; accept only fixed feedback diagnostics and remove free-form path redaction | Protocol §3.4; catalog; M15/M18–M20 | PROPOSED / NOT RUN |
| B9 clause-ID token boundaries | Add exact search/near-match regex and exact set-equality check | Protocol §3.4; file 31 §8; manifest and sidecar; M40 | PROPOSED / NOT RUN |

## Additional consistency actions

- Sidecar validation flags are `REQUIRED`, not `true`, until F18 records execution results.
- M14 is a serializer unit vector with the multibyte character placed at the truncation boundary; M17 is also marked grammar-exempt.
- P22 and M12 use the same `ACCEPT_WITH_WARNING` disposition and `DIAGNOSTIC_FORMAT_WARNING`.
- M15 now tests rejection of a path-bearing non-normative diagnostic; no arbitrary path redaction is specified.
- Owner decision IDs for v1.0 corrections are renamed X1–X15 to avoid collision with approved v0.7 D1–D7.
- v1.0 pack is retained under `archive_v1.0/`.

## Owner decisions not made

A1–A11 remain `PROPOSED / NOT ACCEPTED`. The strict-AST branch (X14) remains `OWNER CHOICE REQUIRED`; the v1.1 fixtures assume the existing strict branch only as a proposed technical baseline. The owner, TEEP applicant, contributors and approver remain `TO CONFIRM` against the actual TEEP application. The presence of this package does not constitute approval.

## Verification boundary

This package revision includes document/fixture edits and static package generation only. It does not contain a working project parser, assembler, sandbox, simulator or harness. No F18 fixture was executed. No provider/LLM call was made. No source PDF was accessed or verified. The next required step is an independent document-and-fixture re-audit; implementation remains unauthorized until A1–A11 and X14 are explicitly recorded.
