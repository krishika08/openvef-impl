# OpenVEF Owner Sign-off Pack (v1.3.6) — BLANK

Nov 23, 2026 · @Conductors

Nothing in this pack is selected or signed. Both owners complete and sign every part; until then it authorizes nothing.

## How to use this pack

Both owners complete the three parts in order, in one sitting. Each part opens the next; none of them authorizes LLM/provider calls, F16 or confirmatory generation.

1. **Part 1 — Interpretation Note.** Decides what “No LLM call of any kind” (Owner Approval Record L46) covers. Adopting it permits off-pipeline mentoring, planning and documentation help.
2. **Owner Decision Record.** Fill the separate record ([link](https://claude.ai/artifact/88YV4kTXQxcDYP7jx351Sm)): A1–A11, X14, identities, Python pin, F18 scope confirmation, sign-off. Part 3 below is the checklist for it.
3. **Part 2 — Build-Method Decision.** Decides whether and how Claude Code may build the canonical implementation.

After all three are signed: save the exact signed files, compute each file’s SHA-256, and keep them with the project evidence. The frozen v1.3.6 ZIP is never edited.

## Part 1 — Owner Interpretation Note: LLM-call restriction

Condensed from the owners' final draft of 23 Nov 2026 (bullet lists run into sentences; signature block set for two owners) — compare it with that draft before signing. Status DRAFT — NOT EFFECTIVE UNTIL SIGNED. Source: Owner Approval Record, Work Authorization, line 46. Proposed interpretation: experimental-only restriction.

**1. Interpretation.** The restriction “No LLM call of any kind” applies to model invocations participating in the OpenVEF experimental pipeline: F16 pilot and re-pilot calls; experimental smoke tests and provider-format probes; ORG-A and ORG-B experimental generations and repairs; confirmatory generation; other model invocations producing experimental artifacts or results. Subject to Section 2, it does not by itself prohibit off-pipeline use of LLM assistants for technical mentoring and conceptual explanations; discussion and interpretation of existing project requirements; architecture and implementation planning; pseudocode clearly labelled as non-canonical; project governance and documentation review. This permission does not independently authorize canonical implementation code generation, alteration of experimental inputs, or any activity restricted by another requirement or owner decision.

**2. Author-visible inputs, evaluator-side materials and control artifacts.** This interpretation does not authorize LLM assistance to create, rewrite, edit or materially shape: author-visible inputs (FIFO and UART specifications; authoring-packet text); evaluator-side materials (the observation mask; mask-to-specification traceability material; the directed test suite; hand-built control mutants); control artifacts (driver artifacts; checker artifacts, including correct reference and control checkers). Their permissibility is reserved for a separate owner decision on “hand-built” and “independently authored”. It also does not decide whether Claude-generated canonical parser, assembler, harness or checker code is permissible; resolve human-authorship requirements for F6 and F17 checkers; establish that LLM-assisted engineering satisfies any hand-built requirement; modify any requirement stated in v1.3.6; waive any additional requirement separately adopted in writing by the owner concerning authorship, independence, provenance or isolation; or create a code-provenance requirement the pack does not expressly contain.

**3. LLM assistance record.** LLM assistance used under this interpretation must be recorded in an assistance log: tool and model where known; date and time; purpose and scope; affected files or artifacts; whether the material was adopted, modified or rejected. Pre-adoption ChatGPT and Claude sessions are recorded retrospectively as the first entries, to the extent supported by records; unknown details are marked not recorded. Retrospective entries document history only and do not retroactively authorize it. The log is retained with the project evidence for the implementation auditor.

**4. Authorization boundaries.** This interpretation does not itself authorize FIFO feasibility implementation; parser or assembler implementation; execution of the 144 mandatory fixtures; F16 or other experimental LLM/provider calls; smoke tests or provider-format probes; confirmatory generation; or expansion beyond the limited scope of the existing gates. A1–A11 and X14 remain separate owner decisions. All implementation, fixture-execution, independent-audit and experimental gates remain in force.

**5. Relationship to the frozen baseline.** This note interprets the existing v1.3.6 wording, is kept separately from the frozen ZIP, and modifies no baseline document. It becomes effective only when formally adopted. Signers must be the persons confirmed as project owners in §4 of the Owner Decision Record.

**6. Owner decision.**

| Decision | Select |
| --- | --- |
| Adopt the experimental-only interpretation as written | ☒ |
| Reject the proposed interpretation | ☐ |
| Return for further revision | ☐ |

| Owner | Full legal name | Signature | Date |
| --- | --- | --- | --- |
| Owner 1 | Krishika | krishika | 23-11-2026 |
| Owner 2 | Ayush Kumar Singh | Ayush | 23-11-2026 |

Effective status: NOT EFFECTIVE until both owners' adoption and signatures are recorded.

## Part 2 — Build-Method Decision

This decides how the canonical implementation is built, and resolves the “hand-built” question reserved by Part 1 §2. Mark one box per row. Rows 2 and 3 touch explicit pack wording: Protocol L439 (“No LLM-generated checker is run on any mutant trace before the analysis freeze”) and L415 (directed suite “written against the specification only, before any LLM generation”). Choosing AI-built there requires a controlled document revision and a new independent document audit first.

| # | Item | Option 1 | Option 2 |
| --- | --- | --- | --- |
| 1 | Parser, assembler, harness, ledger, runner | ☒ May be built with Claude Code | ☐ Human-written only |
| 2 | F6/F17 control checkers and drivers | ☒ Human-written | ☐ AI-built after controlled revision + re-audit |
| 3 | Directed test suite | ☒ Human-written | ☐ AI-built after controlled revision + re-audit |
| 4 | FIFO specification, authoring-packet text, observation mask, control mutants | ☒ Human-written | ☐ AI-assisted, disclosed in the assistance log |
| 5 | Review vs authorship for human-written items | ☒ Claude may suggest changes in prose only | ☐ Claude may also propose code |

**Meaning of “hand-built” adopted by the owners:** ☐ written by a person ☒ built deliberately for the controls, not taken from the study pipeline (MCY mutants, F16/confirmatory outputs) ☐ other: \_\_\_\_\_\_\_\_

**Rules for AI-built code (apply if row 1 Option 1 is chosen):**

- The v1.3.6 pack is read-only; it is never edited.
- Code runs on the pinned CPython 3.11 interpreter recorded in the Owner Decision Record.
- No fixture-specific code: no references to fixture IDs or expected outputs.
- Each commit cites the pack clause it implements (traceability).
- The code makes no LLM or provider calls.
- Assistance log: one entry per session (tool, date, scope, files); itemised suggestions, each marked adopted, modified or rejected, only for human-written items.

**Independent implementation auditor** (must not have built, edited or materially directed the implementation or runner; not Claude if Claude builds it): \_\_\_\_\_\_\_\_

| Owner | Full legal name | Signature | Date |
| --- | --- | --- | --- |
| Owner 1 | Krishika | krishika | 23-11-2026 |
| Owner 2 | Ayush Kumar Singh | Ayush | 23-11-2026 |

## Part 3 — Checklist

The freeze stays valid only if all of A1–A11 are accepted as written and X14 Option A is chosen; any rejection, modification or Option B needs a revised release and a new document audit before implementation (Owner Decision Record §6.1).

**Owner Decision Record** ([link](https://claude.ai/artifact/88YV4kTXQxcDYP7jx351Sm)):

- [x] §1 “Owner has reviewed the baseline pack” marked
- [x] §2 A1–A11: one decision per row, summary counts filled in
- [x] §3 X14: Option A or Option B marked
- [x] §4 Owners' full legal names (matching the TEEP application), TEEP applicant, contributors, approver, human baseline author, implementation auditor
- [x] §5.1 Exact CPython version, interpreter/container hash, OS and architecture
- [x] §5.2 F18 scope confirmation marked
- [x] §5.4 Auditor independence confirmed
- [x] §6 Freeze-validity outcome marked; both owners sign and date
- [x] Register 16 L47 “B1–B9” note acknowledged

**After signing:**

- [x] Part 1 signed by both owners
- [x] Part 2 signed by both owners
- [x] Each signed file saved unchanged; SHA-256 of each exact signed file recorded
- [x] Retrospective assistance-log entries started (ChatGPT and Claude sessions to date)

Once every box is ticked, the limited hand-built FIFO scope in Protocol §18(4) opens. LLM/provider calls, F16 and confirmatory generation stay closed.

## Owner instruction log

Claude proposed the set below in chat on 23 Nov 2026 as a recommendation, not a decision. Boxes in Parts 1–2 and in the Owner Decision Record are marked only after both co-owners accept it in writing; each marked box is noted “marked by Claude on the owners' written instruction”. Signatures and dates are added by the owners themselves.

| Item | Recommended set |
| --- | --- |
| A1–A11 | Accept all as written |
| X14 | Option A (strict AST) |
| Python pin | CPython 3.11.18, run inside WSL (Ubuntu) |
| F18 scope | Confirmed as part of the parser/assembler hand-tests |
| Part 1 | Adopt the experimental-only interpretation |
| Part 2, row 1 | Parser, assembler, harness, ledger, runner may be built with Claude Code |
| Part 2, rows 2–3 | F6/F17 control checkers and drivers, and the directed suite: human-written |
| Part 2, row 4 | FIFO specification, authoring-packet text, observation mask, control mutants: human-written |
| Part 2, row 5 | Claude may suggest changes in prose only |
| Meaning of “hand-built” | Built deliberately for the controls, not taken from the study pipeline |

| Date and time (IST) | Co-owner | Statement | Status |
| --- | --- | --- | --- |
| 23 Nov 2026, 13:42 | Krishika | “I, Krishika, co-owner of OpenVEF, accept Claude's recommended set as listed on 23 Nov 2026.” | Accepted in chat; legal name confirmed as “Krishika” (23 Nov 2026, 13:45) |
| 23 Nov 2026, 13:45 | Ayush | Relayed by Krishika: “Ayush also accepts the same Claude recommended set as listed on 23 November.” | Relayed acceptance; Ayush's own confirmation is his signature on Parts 1–2 and the Owner Decision Record; full legal name to be confirmed |

Still open after both acceptances: identities for the TEEP applicant, approver, contributors, human baseline author and independent implementation auditor; the interpreter hash; signatures and dates.

**Boxes marked on 23 Nov 2026 (by Claude, on the owners' written instruction):** Part 1 “Adopt”; Part 2 rows 1–5 and the “hand-built” meaning, as in the recommended set; Owner Decision Record §2 A1–A11 accepted as written (11/11), §3 X14 Option A, §5.1 version 3.11.18, §5.2 F18 scope confirmed, §6.1 freeze valid. Not marked, because the recommended set did not cover them: §1 baseline-review box, §4 identities, §5.1 interpreter hash and OS, §5.3, §5.4, signatures and dates.

## Part 4 — Signature for the Owner Decision Record

By signing here, both owners adopt the Owner Decision Record ([link](https://claude.ai/artifact/88YV4kTXQxcDYP7jx351Sm)) exactly as marked at its revision 25 on 23 Nov 2026: A1–A11 accepted as written (11/11), X14 Option A, CPython 3.11.18, F18 scope confirmed, freeze valid. This substitutes for its §6.3 signature block. Identities in its §4 other than the owners remain TO CONFIRM.

| Owner | Full legal name | Signature | Date |
| --- | --- | --- | --- |
| Owner 1 | Krishika | Signed by written statement in chat, transcribed by Claude: “I, Krishika, co-owner of OpenVEF, sign the Owner Decision Record as marked at revision 25 on 23 Nov 2026.” | 23 Nov 2026, 13:54 IST |
| Owner 2 | Ayush Kumar Singh | Written statement posted in the chat from Krishika's session, transcribed by Claude: “I, Ayush Kumar Singh, co-owner of OpenVEF, sign the Owner Decision Record as marked at revision 25 on 23 Nov 2026.” Claude cannot verify who typed it; Ayush should confirm it from his own account or by a message the owners keep with this record. | 23 Nov 2026, 13:54 IST |

## Amendment D-005 — Part 2 row 4 changed for FIFO design materials

24 Nov 2026, about 15:35 IST: in the claude.ai chat, Krishika first chose “We write it”, then, after asking Claude to choose the depth and width, chose “Switch to AI-assisted”. Claude had recommended human-written; Krishika's choice prevails. Ayush Kumar Singh's confirmation is pending.

- **Now AI-assisted, disclosed** (Claude Code drafts; the owners review and approve): FIFO design specification, port manifest, reset and legal-input rules, the other payload blocks (checklist item 17), FIFO RTL, and the proposed frozen values and trace schema (items 7–12). Claude recommended depth 4 and width 8.
- **Unchanged:** the F6/F17 control checkers and drivers and the directed suite stay human-written (Protocol L439, L415). The control mutants stay human-written. The observation mask may be drafted, but it must be signed by an independent human mask reviewer (Protocol L271).
- **Disclosure:** “The FIFO specification, RTL and authoring-packet payloads were drafted by Claude (Anthropic) via Claude Code and reviewed and approved by the owners. If any Claude model is among the models evaluated, this is reported as a potential familiarity confound.”
