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

## DEV-003 — Development regression runs before the v1.3.7 gate is met (Protocol L555 (3))

> [02 L555] "(3) Only after that document re-audit passes, the owner must explicitly record acceptance or rejection of A1–A11 and choose the X14 strict-AST branch. Until both the document audit and owner record are complete, no implementation or fixture execution is authorized."

**Owner-authorized deviation (Krishika, D-033, 28 Nov 2026; scope reworded by Krishika the same day), verbatim:** "Protocol L555(3) bars implementation or fixture execution until the document audit and owner record are complete. The owners waived this bar for development-only regression runs (run_class: development) from the candidate's creation (b9f3d54) until v1.3.7 is adopted or rejected, to check that corrections did not change outcomes. These runs are fixture execution; they are not F18 acceptance and are not counted as F18 evidence. The waiver ends when v1.3.7 is adopted or rejected."

It replaces the D-032 owner interpretation below, which document audit #6 found unsupported by the text (D6-2, MAJOR;
`docs/reviews/doc-audit6-gpt6-2026-11-28.md`). The D-032 wording was Claude's error. The Protocol text is unchanged: the
bar stands, and the runs below are a departure from it, not an exception the text contains.

**Waived runs.** Every implementation or fixture execution made against the v1.3.7 candidate from its creation
(commit `b9f3d54`, 26 Nov 2026 15:45 UTC) until v1.3.7 is adopted or rejected. Each is a development run (`run_class: development` in its `summary.json`;
the container test runs are development test logs, D-017), none is F18 acceptance or F18 evidence. Runs added later
while the waiver lasts are listed here in the commit that adds their evidence.
- Candidate fixture runs (11): `run-v137c-20261126T155948Z`, `run-v137c-20261126T164050Z`, `run-v137c-20261127T052443Z`, `run-v137c-20261127T114201Z`, `run-v137c-20261127T134318Z`, `run-v137c-20261127T153351Z`, `run-v137c-20261127T163649Z`, `run-v137c-20261128T032116Z`, `run-v137c-20261128T033242Z`, `run-v137c-20261128T042052Z`, `run-v137c-20261128T102409Z`. `run-v137c-20261127T114201Z` was cut off by a host restart and has no
  summary; it executed fixtures, so it is listed.
- Control runs (10): `controls-20261126T160156Z`, `controls-20261126T164304Z`, `controls-20261127T052649Z`, `controls-20261127T134510Z`, `controls-20261127T153602Z`, `controls-20261127T163904Z`, `controls-20261128T032418Z`, `controls-20261128T033441Z`, `controls-20261128T042259Z`, `controls-20261128T102625Z`.
- Container test runs (13): `container-tests-20261126T160212Z`, `container-tests-20261126T164316Z`, `container-tests-20261127T052653Z`, `container-tests-20261127T053222Z`, `container-tests-20261127T134545Z`, `container-tests-20261127T135044Z`, `container-tests-20261127T153608Z`, `container-tests-20261127T154913Z`, `container-tests-20261127T163956Z`, `container-tests-20261128T032456Z`, `container-tests-20261128T033514Z`, `container-tests-20261128T042332Z`, `container-tests-20261128T102719Z`.
- Of these, `run-v137c-20261126T155948Z`, `run-v137c-20261126T164050Z`, `run-v137c-20261127T052443Z`,
  `controls-20261126T160156Z`, `controls-20261126T164304Z`, `controls-20261127T052649Z` and the container test runs up to
  `container-tests-20261127T053222Z` came before document audit #1's bundle (`docaudit1-c4caff40`, 27 Nov 2026 05:38
  UTC). Krishika confirmed (D-033) that the waiver covers them: its scope runs from the candidate's creation.
- Runs of the v1.3.6 pack are not waived here. Whether v1.3.6's own L555 (3) gate was met before them is recorded in
  DEV-004.

**Label on every waived run:** "development run under DEV-003 (L555 (3) waived; not F18 acceptance, not F18 evidence)".

**Ends when** v1.3.7 is adopted or rejected (the owners' act). L4 below stays open until then.

## DEV-004 — v1.3.6 gate recorded as met, with evidentiary gaps (Protocol L555 (3))

> [02 L555] "(2) Obtain an independent document-only v1.3.6 re-audit of the actual pack, including the operative F18 checklist, every fixture expectation and all cross-document rules; a pass authorizes nothing by itself. (3) Only after that document re-audit passes, the owner must explicitly record acceptance or rejection of A1–A11 and choose the X14 strict-AST branch. Until both the document audit and owner record are complete, no implementation or fixture execution is authorized."

**Owner decision D-034 (Krishika, 28 Nov 2026, on a Claude (claude.ai) review of the owner records; takes effect under
D-008):** the v1.3.6 gate is recorded as met, with evidentiary gaps. Each gap below stays open until its "Ends when" is
met. This is **not a waiver**, and the gaps are not closed by this entry. The owner records are in
`docs/owner-records/`: `owner-signoff-pack-rev95.md` (SHA-256 `13b805cb…a83d`) and `owner-decision-record-rev25.md`
(SHA-256 `64b83614…594b`). Both are claude.ai Docs Markdown exports made on 28 Nov 2026; see
[owner-records/NOTE.md](owner-records/NOTE.md).

**What the owner records show** (file and line, quoted exactly):
- **Owner record (A1–A11, X14).**
  - Sign-off Pack Part 4, L129: "By signing here, both owners adopt the Owner Decision Record ([link](https://claude.ai/artifact/88YV4kTXQxcDYP7jx351Sm)) exactly as marked at its revision 25 on 23 Nov 2026: A1–A11 accepted as written (11/11), X14 Option A, CPython 3.11.18, F18 scope confirmed, freeze valid. This substitutes for its §6.3 signature block. Identities in its §4 other than the owners remain TO CONFIRM."
  - Sign-off Pack Part 4, L133, Owner 1: "Krishika", "Signed by written statement in chat, transcribed by Claude: “I, Krishika, co-owner of OpenVEF, sign the Owner Decision Record as marked at revision 25 on 23 Nov 2026.”", "23 Nov 2026, 13:54 IST".
  - 13:54 IST is 08:24 UTC. `run-20261123T082747Z` started at 08:27:47 UTC, about 3 minutes later (the signature is
    recorded to the minute).
  - Decision Record (rev 25): L38–L48 have every A1–A11 row "☒" under "Accept as written". L50 reads "Number accepted
    as written: 11 / 11. Number rejected or modified: 0." L58 has Option A "☒". L140 has "Freeze valid" "☒".
- **F18 scope.** Decision Record §5.2, L104, quotes the scope Register 16 L47 opens: "hand-built FIFO
  specification/mask, harness, F1–F15, parser/assembler hand-tests, and F17 using hand-built FIFO control mutants only."
  L108 reads: "Running them is treated as part of the “parser/assembler hand-tests”: ☒ Confirmed".
- **Document audit.** Decision Record L14: "| Document audit | PASS, 23 Nov 2026 (independent, documents only) |".
- **Order in the repository's own records.** `docs/assistance-log.md` L28 dates the first implementation session
  (Session 1) "23 Nov 2026, from 13:55 IST", one minute after the signature. The earlier claude.ai session (L22,
  "23 Nov 2026, 11:00–13:45 IST") drafted the Sign-off Pack and marked the Decision Record boxes. The log does not
  record it as writing implementation code.

**Gaps** (D-034; each stays open until its "Ends when" is met):

| # | Gap | Ends when |
|---|---|---|
| 1 | **The 23 Nov document-audit report is not in the repository.** The Decision Record states the result (L14), but the report itself is not here. `docs/assistance-log.md` L21 names a "v1.3.6 audit doc" from separate Claude sessions before 23 Nov 2026, and its outcome is not recorded there. If that is the audit relied on, "independent" in L14 means independent of the pack author. It was not independent of the AI that later built the implementation. | The report is found and committed, or the owners record a waiver for it |
| 2 | **Ayush's signature is unverified.** Sign-off Pack L134: "Written statement posted in the chat from Krishika's session, transcribed by Claude: “I, Ayush Kumar Singh, co-owner of OpenVEF, sign the Owner Decision Record as marked at revision 25 on 23 Nov 2026.” Claude cannot verify who typed it; Ayush should confirm it from his own account or by a message the owners keep with this record." L121 likewise records Ayush's acceptance as "Relayed by Krishika". The exports do not record who typed the "Ayush" entries in the Part 1 and Part 2 signature tables (L42, L74). | Ayush confirms from his own account, or by a message the owners keep with this record (the single "Ayush ratification pending" entry in `docs/AUDIT-READINESS.md`, D-008) |
| 3 | **The Part 3 checklist and the Decision Record disagree.** Part 3 ticks these items (L82, L85, L86, L88), but in the Decision Record they are blank or unmarked:<br>• L82 "[x] §1 “Owner has reviewed the baseline pack” marked": Decision Record L16 is "☐ Yes ☐ No".<br>• L85 "[x] §4 Owners' full legal names … implementation auditor": Decision Record L76–L81 are empty in every column.<br>• L86 "[x] §5.1 Exact CPython version, interpreter/container hash, OS and architecture": the version is given (L91), but the hash (L92) and the OS and architecture (L93) are empty.<br>• L88 "[x] §5.4 Auditor independence confirmed": Decision Record L130 (auditor) is empty, and L131–L132 are "☐ Confirmed" and "☐ Agreed".<br>The checklist was ticked for items the record does not contain. The Sign-off Pack's own L125 says these were "Not marked, because the recommended set did not cover them". | The owners complete those items in the Decision Record, or record that the Part 3 ticks were wrong |
| 4 | **The Decision Record boxes were marked by Claude.** Decision Record L5: "Boxes marked ☒ were marked by Claude on the co-owners' written instruction of 23 Nov 2026 (see the OpenVEF Owner Sign-off Pack, Owner instruction log)." Sign-off Pack L125 lists them: "§2 A1–A11 accepted as written (11/11), §3 X14 Option A, §5.1 version 3.11.18, §5.2 F18 scope confirmed, §6.1 freeze valid". The owners' instruction is L120–L121. The owners' own act is the Part 4 signature that adopts the marked record. | The owners record that the marks are theirs (re-marking the Decision Record themselves, or a signed statement kept with it) |

**Read with care** (Claude's observations, not D-034 gaps; see [owner-records/NOTE.md](owner-records/NOTE.md)):
- **The exports are 28 Nov 2026 copies.** The Sign-off Pack export is revision 95 and contains a 24 Nov amendment.
  Neither file shows what the documents read at 23 Nov 2026 08:24 UTC.
- **Both records say "BLANK" in their titles.** The Decision Record's L5 reads "PARTLY COMPLETED, UNSIGNED", and its §6.3
  (L149–L155) is empty. Its L157–L163 still lists the state "Until this section is signed and dated" ("A1–A11: NOT
  ACCEPTED." … "Authorization: NONE."). The Sign-off Pack's L5 reads "Nothing in this pack is selected or signed." The
  owner record therefore rests on Part 4's statement that it "substitutes for its §6.3 signature block" (L129).

**Before D-034** this entry was titled "v1.3.6 implementation and fixture execution without a recorded v1.3.6 L555 (3)
gate (OPEN: owner decision required)". Its finding was that the gate "**cannot be shown**" met from the repository,
because the owner records were not in it. Its covered runs carried the label "v1.3.6 gate not shown met (DEV-004)". That
label is replaced below.

**What the pack says** (`baseline/OpenVEF_Planning_v1_3_6/`, read-only): File 23 L4 and L97, File 32 L40–L41 and L49,
and File 16 L93 and L108 show the gate **not met at release** (A1–A11 "NOT ACCEPTED", X14 "OWNER CHOICE REQUIRED").
They cannot show anything later. The owner records above are the later record.

**First implementation and run:**
- First implementation: Session 1 workspace commit `8bca94d…` (`8bca94d6235cacc4400430fc174a39505804d140`). It is not in
  this repository's history; `af4340d` imported it on 23 Nov 2026.
- First v1.3.6 fixture run: `run-20261123T082747Z`, started 23 Nov 2026 08:27:47 UTC at that commit (8 PASS /
  136 NOT_IMPLEMENTED).

**Executions covered** (the implementation work from `8bca94d` on, and):
- v1.3.6 fixture runs (39): `run-20261123T082747Z`, `run-20261123T152509Z`, `run-20261123T153734Z`, `run-20261123T155910Z`, `run-20261123T160656Z`, `run-20261123T162630Z`, `run-20261123T173644Z`, `run-20261123T173956Z`, `run-20261123T174358Z`, `run-20261123T182731Z`, `run-20261123T183649Z`, `run-20261123T195911Z`, `run-20261123T195936Z`, `run-20261124T111335Z`, `run-20261124T112030Z`, `run-20261124T144337Z`, `run-20261124T151744Z`, `run-20261124T163535Z`, `run-20261124T193435Z`, `run-20261124T194216Z`, `run-20261124T195043Z`, `run-20261124T195537Z`, `run-20261124T202333Z`, `run-20261124T203551Z`, `run-20261124T211459Z`, `run-20261125T040905Z`, `run-20261125T075113Z`, `run-20261125T081829Z`, `run-20261125T173501Z`, `run-20261125T183002Z`, `run-20261126T144718Z`, `run-20261126T155713Z`, `run-20261126T155730Z`, `run-20261126T163836Z`, `run-20261127T052200Z`, `run-20261127T052242Z`, `run-20261127T113929Z`, `run-20261127T134052Z`, `run-20261127T134112Z`.
- Control runs before the candidate existed (12): `controls-20261124T151740Z`, `controls-20261124T163709Z`, `controls-20261124T193604Z`, `controls-20261124T194343Z`, `controls-20261124T195210Z`, `controls-20261124T211644Z`, `controls-20261125T041047Z`, `controls-20261125T075247Z`, `controls-20261125T082020Z`, `controls-20261125T173726Z`, `controls-20261125T183210Z`, `controls-20261126T144918Z`. Later control and container test runs are listed in
  DEV-003; they also executed the v1.3.6 implementation, so this entry covers them too.
- Container test runs before the candidate existed (6): `container-tests-20261125T075330Z`, `container-tests-20261125T082050Z`, `container-tests-20261125T173914Z`, `container-tests-20261125T183231Z`, `container-tests-20261126T144933Z`, `container-tests-20261126T145729Z`.
- Not covered: `probe-file50-20261124T112645Z`, the U+2118 tokenizer probe, which v1.3.6 L555 (4) allows "earlier on
  the exact pinned Python 3.11 interpreter".

**Label on every covered run (D-034):** "v1.3.6 gate recorded as met; gaps DEV-004". None of these runs is F18
evidence (CLAUDE.md rule 8; every one is `run_class` development).

**Ends when:** the entry as a whole ends when every gap above has ended. Until then the label stays.

## Owner interpretation (D-032) — development-only regression runs (Protocol L555 (3)) — SUPERSEDED by DEV-003

**Superseded (D-033, 28 Nov 2026).** Kept as it was recorded, not deleted. Document audit #6 found its conclusion (that
these runs "are not implementation or fixture execution under Protocol L555(3)'s gate") not the best-supported
reading of the unqualified text (D6-2, MAJOR). The owners accepted the finding; the wording was Claude's error. The
runs are fixture execution, and the owners waived the bar for them: see DEV-003 above. Before D-033, L4's "Ends when"
read: "Answered by the owner interpretation above (D-032); the pack text itself is unchanged".

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

## Disclosed limitations of the v1.3.7 candidate (D-032, D-033)

Recorded now, at Krishika's instruction (D-032 item 3), so that an adoption under the D-031 stopping rule only has to
reference this section. Not accepted deviations and not closed: each stays a limitation until the condition named
"Ends when" is met. Source: document audit #5 (`docs/reviews/doc-audit5-gpt6-2026-11-28.md`, section 8), an AI document
audit (GPT-6), not a human independent review; D6-3 and the L4 change from document audit #6 (D-033).

| ID | Kind | Limitation (report #5's wording, shortened) | Ends when |
|---|---|---|---|
| D5-2 | LIMITATION | Lexical acceptance does not establish semantic truth: the run-ID form in `labelled_status` accepts any timestamp-shaped ID without binding it to a run record, and `APPROVAL_TAIL` accepts any sentence after a period. Truth of the status values rests on the audited manual review (report #5 section 4: PASS for all 17 lines and both index fields), which must be repeated whenever a status value changes. D6-3 (audit #6): the validator is also blind to context and negation: a line that says it is only an example ("This is not a status statement; it is only an example: F18 status: …"), or a prefix that calls the values false ("The following values are false and must not be treated as the current status:"), passes. It does not show a false claim in any of the 17 current lines; it is why the manual review stays mandatory. | Not ended by a test change; owner decision D-032 item 1 keeps it |
| L1 | PACK | 61 `archive_*` objects named in baseline `27_SHA256SUMS.txt` are absent from the extraction; all 202 extracted baseline files match, the absent ones are unverified. | The archive objects are supplied and checked |
| L2 | LIMITATION | The implementation source is not in the document-audit bundle: M27 `check_e` was skipped there, and implementation behaviour, predicate purity and runner internals were not audited by the document audit. | The implementation re-audit (Protocol L555 (5); DEV-002) covers them |
| L3 | LIMITATION | No formal F18 acceptance: every run is a development run; the document audit does not execute F18, certify fixture acceptance, or satisfy Protocol L555 (5) or L271. | An authorized F18 acceptance run passes (CLAUDE.md rule 8) |
| L4 | DEPARTURE | Protocol L555 (3) gives no express development-only exception, while D-031, D-032 and D-033 directed development re-runs. Those runs are fixture execution under the bar, waived by the owners (DEV-003); the text is unchanged (audit #6, D6-2). | The waiver ends (DEV-003: v1.3.7 adopted or rejected) |
| L5 | LIMITATION | The implementation that measures `simulator.l334` is not bundled, so the source-level cause and method of the timing differences are not established by the document audit. | The implementation re-audit covers `l334_timeout` |
| L6 | LIMITATION | No implementation approval or owner adoption: a document audit cannot qualify the implementation or record owner acceptance of A1–A11 or X14. | The owners record those decisions; Claude records none |
