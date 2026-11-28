# OpenVEF implementation — rules for Claude Code

Baseline: OpenVEF Planning v1.3.6, ZIP SHA-256
`2e7008210a807868ad3d8a878820afa7cf1066f1c2b5b1cb437b911aa9b30c21`.
Owners: Krishika and Ayush Kumar Singh. Governing records: Owner Sign-off Pack
(Part 1 interpretation note, Part 2 build-method decision) and the Owner Decision Record.

## Scope
Only the limited hand-built FIFO scope of Protocol §18(4) is open. Build the parser,
assembler, harness, ledger and runner.

Owner decision D-005 (Krishika, 24 Nov 2026; Ayush's confirmation pending; Owner
Sign-off Pack Amendment D-005, Part 2 row 4 changed) makes these items AI-assisted.
Claude drafts them; the owners review and approve them:
- the FIFO design specification, port manifest and reset/legal-input rules;
- the other payload blocks (docs/fifo-owner-checklist.md item 17);
- the FIFO RTL;
- proposed frozen values and the trace schema (checklist items 7–12).
Everything Claude drafts under D-005 is marked DRAFT. Claude never marks it approved or
frozen; only the owners do that.

The observation mask may be drafted by Claude, but it must be signed by an independent
human mask reviewer (Protocol L271). Claude is never that reviewer.
Deviation DEV-001 (Krishika, 24 Nov 2026; docs/DEVIATIONS.md): no such reviewer is
available, so the owner accepted the FIFO mask and File 24 table at their frozen hashes
(D-011) with a saved, non-independent Claude review
(docs/reviews/claude-mask-review-2026-11-25.md). L271 stays unmet. Every affected result
carries "cleared under DEV-001 (non-independent review saved)";
never call the mask independently reviewed.
Deviation DEV-002 (Krishika; docs/DEVIATIONS.md): the L555 (5) implementation audit will be
performed by a different AI model (ChatGPT, OpenAI), not a human. Never call it a human
independent audit, and never report it done before its report is saved verbatim under
docs/reviews/.
Owner decisions D-012 and D-013 (Krishika; docs/ambiguities.md): a runner adapter is allowed only
with an input contract cited to the pack and at least 3 synthetic non-fixture vectors, one whose
outcome no fixture expects (tests/test_dispatch_shapes.py). Adapters encoding knowledge of a
specific fixture are forbidden. The rule changed after audit A1-1 and requires re-audit. A-031 is
reversed, and D-009's approval of it is withdrawn.
Owner decision D-015: artifact code runs only in sandbox/artifact_worker.py (confined process); no
evaluator module may share an interpreter with it. Not yet re-audited.
Owner decision D-016: A-054 approved as decided; the worker denies wall-clock reads (File 30 L101),
residuals in docs/sandbox.md and docs/DEVIATIONS.md. Not yet re-audited.
Owner decision D-017: the D-013 rule is kept (disclosed) and strengthened: every adapter also needs, per
input property, a boundary pair for its cited domain (in-domain edge, just outside), enforced by
tests/test_dispatch_shapes.py. Container test logs (tools/run_container_tests.py) are not F18 evidence.
Owner decision D-019: no trust-critical measurement may be produced by a process in which artifact code has
executed; the rest is labelled SELF_REPORTED and recorded as a residual, never called closed. The original
single-fixture-shape criterion is superseded by D-013 and will not be met by design; disclose it for every
audit. Not yet re-audited.
Owner decision D-022 (Krishika; docs/ambiguities.md): every adapter selecting value is also listed in VALUE_SUPPORT with
the words of its own quote that support it (tests/test_dispatch_shapes.py); the runtime signature checks also call the
literal inspect.signature after import, which must agree with the trusted measurement (names/kinds/counts, A-058). Still
self-reported; the SELF_REPORTED residual is not closed. Not yet re-audited.
Owner decision D-023 (Krishika; docs/ambiguities.md): the AI audit sequence #1–#5 is complete with no open BLOCKER or
MAJOR (fifth audit: D-022 CLEARED, 11 limitations); this supersedes the "not yet re-audited" notes above. A1-1 and A9-2
are closed as findings; A1-1-L1 (support-table validator is not a semantic proof) and the SELF_REPORTED residual stay
disclosed limitations. Never mark L555 (5) done on these AI audits (DEV-002), and never claim F18 passed.
Owner decision D-024 (Krishika; docs/ambiguities.md): proposals/v1.3.7/pack is a v1.3.7 CANDIDATE (v1.3.6 + C1–C10),
not audited; v1.3.6 stays the default and baseline/ is never edited. Candidate-pack corrections are changed only by a
numbered amendment in its own commit; candidate-only adapters cite candidate text only; candidate results never count as
v1.3.6 F18 evidence.

Owner decision D-035 (Krishika, 28 Nov 2026; Ayush's ratification pending; docs/V137-ADOPTION.md): v1.3.7 is ADOPTED
under the D-031 stopping rule after document audit #7 CLEARED. For v1.3.7, A1–A11 are accepted as written and X14
Option A is chosen, so v1.3.7's L555 (3) gate is met. The adopted pack is in baseline-v1.3.7/ (read-only, like baseline/;
label file outside the pack directory; release pack-v1.3.7). `--pack v1.3.7` is the F18 default; v1.3.6 and
v1.3.7-candidate stay selectable, and v1.3.6 records are unchanged. This supersedes D-024's "v1.3.6 stays the default".
v1.3.7 runs are authorized development runs; never call them F18 acceptance, an implementation audit, L555 (5) or L271.

Deviation DEV-003 (Krishika, D-033; docs/DEVIATIONS.md): the owners waived Protocol L555 (3) for development-only
regression runs from the candidate's creation (b9f3d54) until v1.3.7 is adopted or rejected. ENDED at adoption (D-035); L4 closed.
Its 34 runs stay waived fixture execution; never call them outside the gate, F18 acceptance or F18 evidence. Add no new runs to it. DEV-004 (D-034, Krishika): "v1.3.6 gate recorded as
met, with evidentiary gaps": the owner records in docs/owner-records/ (claude.ai exports, 28 Nov 2026) show the Part 4
signature 3 minutes before the first v1.3.6 run, but four gaps stay open (document-audit report absent; Ayush's
signature unverified; Part 3 ticks vs blank Decision Record items; boxes marked by Claude). Label those runs "v1.3.6
gate recorded as met; gaps DEV-004"; never call the gate fully evidenced or a gap closed until its "Ends when" is met.

Still human-written. Do NOT write: F6/F17 control checkers or drivers, the directed
suite, control mutants. Owners write those by hand; Claude may comment on them in prose
only. Owner decision D-007 (Krishika, 24 Nov 2026; Ayush's confirmation pending) adds the
control drivers and checkers for F1–F5 and F7–F13 to this list (independence from the
harness author). Control mutants are RTL edits of `design/fifo/rtl/ovf_fifo.v` (D-007).
Owner artifacts go in `design/fifo/controls/` (see its README); Claude builds only the
harness that runs them and must not place content in their slots.
Owner rule (Krishika, 28 Nov 2026; applies to every later session): never edit, rewrite or generate any
owner-written control file (every slot in design/fifo/controls/slots.json, every mutant .v file, every directed
scenario file). When Krishika says a file is ready, run only the controls that file feeds (slots.json `feeds`), and
report the results in prose only, quoting pack lines. Never propose code, pseudocode or skeletons for these files
(Sign-off Pack Part 2 row 5). If a control is still NOT_WIRED, say so; composing its procedure is harness work and
never touches the owner's files.
Owner decision D-036 (Krishika, 28 Nov 2026; docs/ambiguities.md): every commit Claude creates uses
`--author="Claude Code (Anthropic) <noreply@anthropic.com>"`, so git's author field separates Claude's commits from
Krishika's hand-written ones. Commits before D-036 used Krishika's identity with a Co-Authored-By line, and git cannot
separate those. tests/test_controls_provenance.py fails if any file under design/fifo/controls/ other than README.md
and slots.json was last changed by a Claude Code-authored commit. tools/check_control_file.py runs only File 30's
static stages on one owner file and only reads it.

Disclosure (D-005), carried in docs/assistance-log.md: "The FIFO specification, RTL and
authoring-packet payloads were drafted by Claude (Anthropic) via Claude Code and reviewed
and approved by the owners. If any Claude model is among the models evaluated, this is
reported as a potential familiarity confound."

## Hard rules
1. The v1.3.6 pack under `baseline/` is read-only. Never edit, reformat or regenerate it. The same holds for the
   adopted v1.3.7 pack under `baseline-v1.3.7/OpenVEF_Planning_v1_3_7/` (D-035).
2. Runtime (owner decision D-002a): the pinned interpreter is CPython 3.11.18 inside
   `python:3.11.18-slim` pinned by digest
   (`python@sha256:07d4824036af339fa1b6ef769cc99d9c10a141769538b52b3b597c84f7a7b535`),
   built as `sandbox/Dockerfile`. Evidence runs only via `runner/run_f18_container.sh`,
   which runs the whole runner and every artifact in that image. Record `sys.version`,
   the interpreter SHA-256 and the image identity in every evidence run. Host Python is
   for development only; results from any other interpreter are not evidence.
3. Dependencies: only those pinned in `requirements.lock` with hashes. Adding or changing
   one needs owner approval.
4. No fixture-specific code: never branch on fixture IDs, file names under
   `41_F18_Fixture_Inputs/`, or expected outputs. Behaviour must follow the spec text.
5. No LLM or provider calls from any code, test or script.
6. When a rule in the pack is ambiguous, write it up in `docs/ambiguities.md` (exact
   quote, competing readings, what changes). Then, under the standing delegation below,
   choose the reading best supported by the pack text, mark it "decided by Claude under
   standing delegation, owner review pending", give the textual reason, implement it and
   keep building without asking. Never pick a reading silently, and never pick one
   because it makes a fixture pass: argue from the pack text only (rule 4).

## Standing delegation for unsettled specification cases
Given by Krishika (owner) in Claude Code on 23 Nov 2026: "resolve every unsettled
specification case yourself by choosing the reading best supported by the pack text,
record it in docs/ambiguities.md as 'decided by Claude under standing delegation, owner
review pending', add the rule to CLAUDE.md, and keep building without asking me. This
covers A-007 to A-019, the tie case, and all future cases."
- Covers spec interpretation only. It does not relax the Scope section or hard rules
  1–5, 7 and 8, and it does not cover dependency pins (D-001 stays with the owners).
- Given by Krishika alone; Ayush Kumar Singh's agreement is not recorded. Every such
  decision stays "owner review pending" until an owner reviews it.
- Governance rule D-008 (Krishika, 24 Nov 2026): decisions and approvals signed by Krishika
  alone take effect. Ayush's agreement is recorded once, as the single "Ayush ratification
  pending" entry in docs/AUDIT-READINESS.md, not on individual items. Claude never signs or
  approves for either owner. The independent mask reviewer's signature (L271) is still
  required and no owner signature replaces it (except as DEV-001 records, for the
  FIFO mask at its frozen hashes only).
- Owner decision D-009 (Krishika, 24 Nov 2026): every reading decided under this
  delegation and not yet owner-approved (A-007..A-012, A-013 tie, A-015..A-037, A-039,
  A-045..A-052, F15 case table) is approved by Krishika as decided, without itemised owner
  review. Later readings start as "owner review pending" again.
- Evidence runs that depend on a Claude-decided reading say so in `docs/traceability.md`,
  and do not count toward F18 until the owners have reviewed that reading.
7. Every commit message names the clause it implements, e.g. `File 30 §1: reject BOM`.
   Keep `docs/traceability.md` current: requirement → module → fixtures → evidence.
8. Never report a fixture as passed unless the runner executed it on the pinned
   interpreter and the evidence file records the result.

## Assistance log
Append one entry per Claude session to `docs/assistance-log.md`: date, tool and model,
scope, files touched. Human-written items: list each suggestion and whether it was
adopted, modified or rejected.

## Layout
- `baseline/` — extracted v1.3.6 pack (read-only, verified against `27_SHA256SUMS.txt`)
- `baseline-v1.3.7/` — adopted v1.3.7 pack (D-035; read-only, verified against `SHA256SUMS-v1.3.7-candidate.txt`) and its label file
- `src/openvef/` — implementation
- `tests/` — unit tests that are not F18 fixtures
- `runner/` — F18 fixture runner
- `design/fifo/` — DRAFT FIFO design materials under D-005 (RTL, export script, proposed values)
- `evidence/` — run outputs, logs, hashes (append-only)
- `docs/` — traceability, ambiguities, assistance log
