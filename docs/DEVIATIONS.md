# Deviations from the planning pack

Owner-accepted departures from a pack requirement. A deviation does not make the
requirement met. Each affected result carries the deviation's label.

## DEV-001 — No independent mask review (Protocol L271)

> [02 L271] "The table is signed by an independent mask reviewer and is checked in F18."

> [21 L32] "| Independent reviewer | Reviewer did not author templates or mask; signs exact hashes and checklist | PENDING |"

**Owner decision (Krishika, sole builder, 24 Nov 2026), adopting a Claude (claude.ai)
recommendation; pasted into Claude Code:** "no independent human mask reviewer is
available. The observation mask and File 24 table are accepted by the owner (Krishika) on
the basis of Claude's review; this is NOT an independent review."

**Correction (Krishika, given after the first record of DEV-001, 24 Nov 2026 UTC):** the
Claude (claude.ai) mask review had **not** happened when DEV-001 was recorded, so the
words "on the basis of Claude's review" above were not true at that time. The review is
to be done afterwards and saved as `docs/reviews/claude-mask-review-2026-11-25.md`. Until
it is saved, the 10 affected results carried a "review pending" label.

**Review saved:** [claude-mask-review-2026-11-25.md](reviews/claude-mask-review-2026-11-25.md)
(supplied by Krishika, saved verbatim). Outcome: PASS with placeholder fixes.

**D-010 and D-011 (Krishika):** the placeholder fixes are applied (D-010), the
`independent_reviewer` column reads "none (DEV-001)" and the L270 reminder is restored
(D-011). The mask is re-frozen
(machine-readable: `design/fifo/freeze/deviation-DEV-001.json`):

| File | SHA-256 (frozen under D-011) | SHA-256 (as reviewed) |
|---|---|---|
| `design/fifo/mask/ovf_fifo-mask-DRAFT.json` | `64c7a9e6f25845521b9ad8164c3dff4d371f97fbd7c78c7c43c02e92540bbb59` | `78477cd41df36074c06aca31bfca3aae4de7a085980559480a35e2a08c180b0f` |
| `design/fifo/mask/ovf_fifo-mask-traceability-DRAFT.csv` | `25e15c1e38ab8ff8a4a4a1172c144feabfdad24aa00992ed5d0876a87418dfd8` | `3e443a68368b693e33608db0daa94ae52e8e61a9a6b7a55b55de834862360f92` |

Only `spec_version_sha256`, the status fields and the table's reviewer fields changed.
`tests/test_freeze_package.py` checks that undoing those changes gives the reviewed bytes.

**Label on every affected result:** "cleared under DEV-001 (non-independent review saved)".
Earlier runs keep their labels (evidence is append-only) and are superseded:
`run-20261124T193435Z` ("cleared under DEV-001 (non-independent mask review)", recorded
before any review existed) and `run-20261124T194216Z` ("cleared under DEV-001 — review
pending").

**What this does not do:**
- L271 and File 21 L32 remain **unmet**. Nobody signed section G.
- The review is not independent: Claude drafted the mask and the table (D-005), and the
  reviewer is Claude (claude.ai). Claude Code performed no sign-off review.
- The table's `independent_reviewer` column reads "none (DEV-001)". The `mask_reviewer`
  entry is the non-independent Claude review.
- It does not cover any other mask, or any changed bytes of this one. The runner re-checks
  the hashes and restores the provisional reason on a mismatch.

**Effect on claims:** report DEV-001 wherever results that use the mask are reported. Whether
F18 can pass with it is for the independent implementation auditor (L555 (5)).

**Ends when** an independent human reviewer signs the mask.

## DEV-002 — Implementation audit by an AI model (Protocol L555 (5))

> [02 L555] "(5) Independently re-audit the implementation, parser/assembler, Python 3.11 behavior and all mandatory fixture results."

**Owner decision (Krishika, recorded 24 Nov 2026 UTC; pasted into Claude Code):** "no
independent human implementation auditor is available. The implementation audit (L555 (5))
will be performed by a different AI model (ChatGPT, OpenAI), not the implementation author,
using dist/openvef-audit-bundle.zip (e0ee23ff…fa01) and docs/AUDIT-BRIEF.md. This is NOT a
human independent audit".

**Status: first report received and saved verbatim** (OpenAI GPT-6, 25 Nov 2026):
[report](reviews/implementation-audit-gpt6-2026-11-25.md), SHA-256
`3dfa0865bf1d3c187930ecd63ffb2aac8f0716d2e66e69bd8f865e40e4820296`; [note](reviews/implementation-audit-gpt6-2026-11-25-NOTE.md).
It found one BLOCKER (A1-1) and one MAJOR (A8-1); A2, A3, A5 and A9 are limitations (no Docker,
no CPython 3.11.18). It states a 63-digit bundle hash; the note explains. Step (5) is not
marked done.

**Re-audit: report received and saved** (OpenAI GPT-6, operator Krishika, 25 Nov 2026, bundle
`34bc810934c4865eede3142e876efb54bd83de8ed10ec177f4f2c607744ec0c0`):
[report](reviews/implementation-reaudit-gpt6-2026-11-25.md), SHA-256
`8ef52f96f75f5be983ae7032b59ab5ccc56afc2ec3d02e37e937890a2f001ec7`, equal to the hash Krishika gave; [note](reviews/implementation-reaudit-gpt6-2026-11-25-NOTE.md).
Disposition **NOT CLEARED**: BLOCKERs A1-1 (not fully resolved) and A9-1, MAJOR A4-1 (A8-2 is a
cross-reference), limitations A2, A3, A7. A8-1 is resolved. D-015 accepted its findings and fixed
A9-1, A4-1 and the M18 contract before Claude Code had seen the report; the note lists two points
D-015 leaves open. Step (5) is not marked done.

**Third audit: report received and saved** (OpenAI GPT-6, operator Krishika, 25 Nov 2026, bundle
`b1235ba376442eead14c338b59d73060cb927532c67cdd59324d0f2a0a08327d`):
[report](reviews/implementation-reaudit3-gpt6-2026-11-25.md), SHA-256
`5acba72c970fa5ecb7e3994ebc706222538e64056bca314aee4882d59357cf0a`; [note](reviews/implementation-reaudit3-gpt6-2026-11-25-NOTE.md).
Disposition **NOT CLEARED**: BLOCKERs A1-1 and A9-2 (new), limitations A3-1 and A7-1; A4-1, A8-2 and the
original A9-1 attack resolved. D-019 accepts A9-2, which is **not fully closed** ("Open residual (D-019)" below).
Owner statement on A1-1: "The original single-fixture-shape criterion is superseded by D-013 because the
v1.3.6 pack itself contains one-of-a-kind fixtures; it will not be met by design; disclosed for every
audit." D-019 was covered by the fourth audit. Step (5) is not marked done.

**Fourth audit: report received and saved** (OpenAI GPT-6, operator Krishika, 26 Nov 2026, bundle
`93b249a61eac478304162e52d856f6a5185ed32338582716103a7891585a1907`):
[report](reviews/implementation-reaudit4-gpt6-2026-11-26.md), SHA-256
`07508e1fc6e1f2a879176c7492251048aa77b20c7fe1dd82b71aaae8a09272a9`; [note](reviews/implementation-reaudit4-gpt6-2026-11-26-NOTE.md).
Scope D-019 to D-021. Disposition **NOT CLEARED**: 0 BLOCKER, MAJORs A1-1 (`stop` citation) and A9-2 (code-object
measurement instead of the literal `inspect.signature`), 8 LIMITATIONs. A4-1, A8-1, A8-2, A9-1 resolved; D-020 judged an
honest disclosure policy; D-021 supported. D-022 responds. Step (5) is not marked done.

**Fifth audit: report received and saved** (OpenAI GPT-6, operator Krishika, 26 Nov 2026, bundle
`5bdc25ea3bf0be66f16a0aa5a47737c2b29f8c798f31495ffa670859689b2cc2`, release `audit5-5bdc25ea`):
[report](reviews/implementation-reaudit5-gpt6-2026-11-26.md), SHA-256
`0e56d990e388fbf140f32d6fa7dbb2bf38772e60955e5b680cd00777cb74cc00`; [note](reviews/implementation-reaudit5-gpt6-2026-11-26-NOTE.md).
Scope D-022 plus regression. Disposition **CLEARED for D-022**: 0 BLOCKER, 0 MAJOR, 0 MINOR, 11 LIMITATIONs. A1-1 and
the A9-2 literal-signature correction resolved; A4-1, A8-1, A8-2, A9-1 remain fixed. The clearance is scoped to D-022; the
report says it is not a clearance of the whole implementation.

**Status (D-023, Krishika, on Claude (claude.ai) triage):** the AI audit sequence #1–#5 is complete, with no open
BLOCKER or MAJOR. A1-1 and A9-2 are closed as findings. Kept as disclosed limitations: **A1-1-L1** (the support-table
validator is not a semantic proof) and the **SELF_REPORTED residual** (L-10; "Open residual (D-019)" below), with the
fifth report's coverage limitations L-02 to L-11. **Step (5) is not marked done**: these are AI audits under this
deviation, not a human independent audit. F18 is not passed.

**Response (D-012):** A1-1 and A8-1 accepted and applied; limitations A2, A3, A5 and A9
accepted and recorded, not treated as defects. The D-012 to D-014 code was then
re-audited (above).

**The rule applied to A1-1 was changed afterwards (D-013).** D-012 first removed every
single-fixture adapter (123 PASS). D-013, on Claude (claude.ai) recommendation, replaced that
rule with "cited input contract plus synthetic vectors" and restored five of the 15 (M18, M19,
M25, M26, M28), while removing one more (`change_class`, M53): 127 PASS. The relaxation raises
the pass count after an adverse finding, so **it requires re-audit** and must be disclosed
wherever the count is quoted. Whether A1-1 is resolved is for the auditor. D-017 keeps the rule and adds
boundary tests for every input property.
A later bundle (now with evidence run-20261126T144718Z) replaces the zip in `dist/`; the audited
zip is in git at `9c89b1c`.

| Audit input | Identity |
|---|---|
| `dist/openvef-audit-bundle.zip` | SHA-256 `e0ee23ff6e29ec78c5310405edd6dd50d7625a8893c75bffdb0d6d026464fa01`, built from commit `5341c28` |
| `docs/AUDIT-BRIEF.md` | the copy inside that bundle |
| Evidence run | `run-20261124T195537Z` |

The bundle is not rebuilt for this record, so its documents predate DEV-002.

**What this does not do:**
- It does not mark step (5) done. Recording DEV-002 is not an audit result, and a report's
  findings must be settled before anyone relies on it.
- It opens no later gate. The LLM-call gate, step (6), stays closed, and F18 is not passed.
- It does not cover DEV-001: L271 stays unmet, and an AI auditor is not the independent
  human mask reviewer.
- It does not cover the document audit that `proposals/v1.3.7/` requires.

**Limits to disclose with the report:**
- The auditor is an AI model, and Claude, the implementation author, wrote the brief and
  the bundle script.
- ChatGPT had an earlier role in this project (assistance-log.md, retrospective entry):
  handoff text, reviews of Claude's reports and interpretation-note drafts, with its role in
  drafting the pack "not recorded". The auditor is a different model from the author, but
  not a stranger to the project.
- The report must state the exact model and version, and which checks were run rather than
  read. Checks that need Docker may not be possible for it.
- If a ChatGPT/OpenAI model is later evaluated in the study, the owners should disclose its
  role as auditor, as D-005 does for Claude.

**Ends when** an independent human auditor performs the implementation audit.

## Open residuals (D-016) — wall-clock reads

Not an accepted deviation: recorded for the auditor, at Krishika's instruction (D-016).

> [30 L101] "The runtime sandbox denies network, filesystem access beyond the designated temporary output directory, environment variables, wall-clock reads, subprocess and simulator access."

> [30 L22] "No third-party package, dynamic import, filesystem access, network access, environment access, wall-clock access, process/thread creation, subprocess call or package installation is permitted."

> [30 L54] "Do not obtain unseeded entropy."

Every clock route found was closed and tested in the pinned container on the development host
([sandbox.md](sandbox.md) "Wall-clock reads"). Not closed, or not shown:
1. **Hardware and kernel.** Tested on one host only (AMD EPYC 7763, Linux 6.8.0-1070-azure).
   TPAUSE and UMWAIT are absent there and untested. RDPRU is blocked there by observation, not
   by a documented guarantee of the setting used.
2. **Native code** stays possible inside the confined process, so the list of denied instructions is
   only as complete as the tests.
3. **Startup remnants:** a clock value read by the interpreter before confinement may remain in its
   own memory. It is a past instant, not the current time.
4. **Static rules** accept paths such as `collections._sys.modules["time"]`. Denial is at run time only,
   so such an artifact fails as a runtime error, not at IMPORT_POLICY.
5. **Related, not a clock:** process ID, addresses and unseeded `random.Random()` vary between runs.

**Not re-audited.** Evidence with this change: run-20261126T144718Z (also in the bundle in `dist/`).

## Open residual (D-019) — runtime checks an artifact can forge

Not an accepted deviation: recorded for the auditor, at Krishika's instruction (D-019).

> [30 L35] "Runtime `inspect.signature` must confirm the same parameter names/kinds/counts. `create_driver(seed)` must return an instance of the module's `Driver` class."

> [30 L39] "Runtime signature checks and the `create_driver` return-type check run after import in the restricted execution container. The container sandbox is the security boundary and must be pinned and tested before F16."

1. **Return type (L35).** Known only from the process that ran `create_driver`, so a hostile driver can
   report it falsely. Closed only for sources the evaluator can prove from their text (PROVEN).
2. **Signatures after execution (L35, L37).** The definitions are measured where no artifact code has run. A replacement
   made at run time is seen only by self-report, with the same limit.
3. **"after import" (L39) and `inspect.signature` (L35, L37): both measurements are taken (D-022).** The trusted one is made
   on compiled code objects, before and without import, because import can run artifact expressions. The literal
   `inspect.signature` is called after import in the artifact process; if it raises, or its names, kinds or counts
   differ from the trusted measurement, the artifact is rejected (`RUNTIME_SIGNATURE`). Trusted and self-reported must
   agree. The literal result is self-reported, so the residual remains: outside the PROVEN fragment an artifact
   can still forge it.
4. **Consequence:** an invalid artifact may be counted valid. No trace, verdict or other artifact is affected
   ([sandbox.md](sandbox.md) "Runtime checks"). The proof rests on CPython behaving as documented, and its
   list of allowed names was written by the implementation author.

**Owner decision taken (D-020)** — no pack rule changed, so a decision, not a deviation:
- **F18** keeps the fixture verdict and attaches a visible label, "SELF_REPORTED (D-020): runtime
  check not statically PROVEN" (`self_reported_runtime_checks`/`self_reported_label` per result,
  and in the run summary). A SELF_REPORTED pass stays PASS.
- **Confirmatory use:** the validity endpoint is reported as measured (primary) **and** with every
  SELF_REPORTED artifact counted invalid (pre-registered sensitivity), plus the per-arm SELF_REPORTED
  count. Analysis rule in [F1-F17-plan.md](F1-F17-plan.md); see also [sandbox.md](sandbox.md) "Runtime checks".

**Audited; residual not closed.** D-019 to D-021 were covered by the fourth audit and D-022 (item 3) by the fifth
(CLEARED for D-022). A9-2 is closed as a finding (D-023); the forgery residual above stands as a disclosed
limitation (fifth audit L-10), and nothing here closes it.

## Owner interpretation (D-032) — development-only regression runs (Protocol L555 (3))

An owner reading of a pack rule, with no pack text change. It is recorded here because document audit #5 named it
(limitation 4) and the owners asked for it to be disclosed with the deviations. It is not numbered as a DEV because
the owners do not treat it as a departure; a reader who takes the rule literally may, and the quote is given for that.

> [02 L555] "(3) Only after that document re-audit passes, the owner must explicitly record acceptance or rejection of A1–A11 and choose the X14 strict-AST branch. Until both the document audit and owner record are complete, no implementation or fixture execution is authorized."

**Owner interpretation (Krishika, D-032, 28 Nov 2026), verbatim:** "the owners authorized development-only regression
runs (run_class: development) during the v1.3.7 document audits; they are not implementation or fixture execution
under Protocol L555(3)'s gate and are not F18 acceptance".

- The pack names no development-only exception; the reading is the owners', not the text's.
- It covers runs whose `summary.json` has `run_class: development` (`evidence/run-v137c-*`, `controls-*`) and the
  container test runs. Every such run is labelled development, never F18 acceptance, and is not F18 evidence (CLAUDE.md
  rule 8, D-024).

## Disclosed limitations of the v1.3.7 candidate (D-032)

Recorded now, at Krishika's instruction (D-032 item 3), so that an adoption under the D-031 stopping rule only has to
reference this section. Not accepted deviations and not closed: each stays a limitation until the condition named
"Ends when" is met. Source: document audit #5 (`docs/reviews/doc-audit5-gpt6-2026-11-28.md`, section 8), an AI document
audit (GPT-6), not a human independent review.

| ID | Kind | Limitation (report #5's wording, shortened) | Ends when |
|---|---|---|---|
| D5-2 | LIMITATION | Lexical acceptance does not establish semantic truth: the run-ID form in `labelled_status` accepts any timestamp-shaped ID without binding it to a run record, and `APPROVAL_TAIL` accepts any sentence after a period. Truth of the status values rests on the audited manual review (report #5 section 4: PASS for all 17 lines and both index fields), which must be repeated whenever a status value changes. | Not ended by a test change; owner decision D-032 item 1 keeps it |
| L1 | PACK | 61 `archive_*` objects named in baseline `27_SHA256SUMS.txt` are absent from the extraction; all 202 extracted baseline files match, the absent ones are unverified. | The archive objects are supplied and checked |
| L2 | LIMITATION | The implementation source is not in the document-audit bundle: M27 `check_e` was skipped there, and implementation behaviour, predicate purity and runner internals were not audited by the document audit. | The implementation re-audit (Protocol L555 (5); DEV-002) covers them |
| L3 | LIMITATION | No formal F18 acceptance: every run is a development run; the document audit does not execute F18, certify fixture acceptance, or satisfy Protocol L555 (5) or L271. | An authorized F18 acceptance run passes (CLAUDE.md rule 8) |
| L4 | LIMITATION | Protocol L555 (3) gives no express development-only exception, while D-031 directed a development re-run. | Answered by the owner interpretation above (D-032); the pack text itself is unchanged |
| L5 | LIMITATION | The implementation that measures `simulator.l334` is not bundled, so the source-level cause and method of the timing differences are not established by the document audit. | The implementation re-audit covers `l334_timeout` |
| L6 | LIMITATION | No implementation approval or owner adoption: a document audit cannot qualify the implementation or record owner acceptance of A1–A11 or X14. | The owners record those decisions; Claude records none |
