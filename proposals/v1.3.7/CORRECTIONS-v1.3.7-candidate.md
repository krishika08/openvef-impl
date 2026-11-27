# OpenVEF Planning v1.3.7 CANDIDATE — corrections C1–C10 (D-024 Phase A)

**v1.3.7 CANDIDATE, not audited.** Owner decision D-024 (Krishika, on a Claude (claude.ai) plan). Written by
Claude (Claude Opus 5.5, via Claude Code), the implementation author. Not approved, not frozen, not released;
it needs an independent document audit. v1.3.6 (`baseline/`) is unchanged and remains the default.

- **What it is:** the rationale for `proposals/v1.3.7/pack/`, a full copy of v1.3.6 with only C1–C10 applied.
  The edits themselves, line by line, are in `pack/CHANGELOG-v1.3.7-candidate.md`; the build is
  `build_candidate.py`, checked by `tests/test_v137_candidate_pack.py`.
- **Order (the point of Phase A):** this file, the pack and its tests are committed **before any implementation
  change for v1.3.7**. A correction found wrong while implementing is amended in a later, numbered commit, not
  edited here silently.
- **Scope chosen by Krishika:** C1–C10 only. Fixtures no correction covers are flagged, not corrected.
- **Every edit stays inside one line**, so no line moves and every line citation means the same line in both packs.
- Quoted v1.3.6 text is checked verbatim by `tests/test_doc_quotes.py`.
- **Correction cycle 2 (owner decision D-027, after document audit #1, NOT CLEARED):** section 11. Its items are
  numbered OD-n (OWNER-DECIDED), A3, A4 and C17. Each is in its own commit, and no earlier section is changed
  except by a note that names the item superseding it.
- **Correction cycle 3 (owner decision D-029, after document audit #2, NOT CLEARED on one MINOR finding):** section 12,
  item C18 (D2-1), in its own commit; earlier sections unchanged.

**Conflict to weigh.** The corrections were drafted on 24 Nov 2026 by the implementation author, after the
v1.3.6 implementation existed, and several make executable fixtures the code does not execute now. Each
correction below states its fit with the current code. **No correction was chosen because it suits the current
code**; where it agrees with the code, that agreement is stated, and the argument rests on the pack text cited.
Where a token's exact spelling exists only in a fixture descriptor, that is said too.

## 1. The 17 NOT_IMPLEMENTED fixtures → pack defects → corrections

v1.3.6 evidence: `run-20261126T144718Z` (17 NOT_IMPLEMENTED). PD numbers are from `docs/pack-defects.md`.

| Fixture | What blocks it in v1.3.6 | PD | Correction | Covered? |
|---|---|---|---|---|
| M27 | prose predicate; no port widths; `full` (an output) in the driven vector | PD-06, PD-25 | C5, C6 | **Yes** |
| M36 | `parser_unit_vector` undefined; no input contract | PD-04, PD-07 | C9 | **Yes** |
| M48 | error class unstated; `rerun_scope_rule` token only in the descriptor; `change_class` input undefined | PD-02, PD-03, PD-07 | C1, C2, C4 | **Yes** |
| M50 | error class unstated; `affected_slots` token only in the descriptor | PD-02, PD-03, PD-07 | C1, C2, C4 | **Yes** |
| M53 | `change_class` input undefined (its values were stated) | PD-02, PD-03, PD-07 | C1, C2, C4 | **Yes** |
| M54 | `stable_*_rule` tokens only in the descriptor | PD-02, PD-03, PD-07 | C1, C2, C3, C4 | **Yes** |
| M58 | error class unstated; `affected_scope`, `unaffected_design_scope` only in the descriptor | PD-02, PD-03, PD-07 | C1, C2, C4 | **Yes** |
| M42 | signature components outside the L185 domains; no error class for `DESIGN_HALT_REPEATED` | PD-01, PD-26 | C10 (PD-01 only) | **No — PD-26 open** |
| M47 | as M42 | PD-01, PD-26 | C10 (PD-01 only) | **No — PD-26 open** |
| M41 | lower-case component; no input contract or output schema for its lifecycle input | PD-01, PD-03, PD-07 | C10 (PD-01 only), C4 (comparison only) | **No — PD-03/PD-07 open** |
| M15 | no error class for `FEEDBACK_SERIALIZER_REJECT`; `allowed_diagnostics` not in the text | PD-20, PD-26, PD-07 | none | **No** |
| M14 | no output schema for its control-vector properties; no input contract | PD-03, PD-07 | C4 (comparison only) | **No** |
| M17 | as M14 | PD-03, PD-07 | C4 (comparison only) | **No** |
| M13 | no input contract for a lifecycle `event` input | PD-07 | none | **No** |
| M37 | no input contract for `runtime_pair` | PD-07 | none | **No** |
| P17 | no input contract for `port_manifest` + `response_object` | PD-07 | none | **No** |
| R07 | no input contract for `design_preflight` | PD-07 | none | **No** |

**Flagged: 10 of the 17 are not covered by C1–C10** (M13, M14, M15, M17, M37, M41, M42, M47, P17, R07). They stay
NOT_IMPLEMENTED on the candidate pack. Covering them needs new corrections (PD-03 output schemas, PD-07 input
contracts, PD-20, PD-26), most of which would have to be derived from the descriptors themselves; Krishika chose
not to draft them in this phase.

## 2. Differences from the 24 Nov 2026 draft (`PROPOSED-CORRECTIONS-DRAFT.md`)

The draft is kept unchanged as history. Applying it exposed four points; each is decided here from the pack text:
1. **C9 also amends Protocol L177.** The draft aligned only File 36 L15, so the two `CONTROL_EXPECTATION`
   definitions PD-04 names would still differ (L177 lacks "parser"). Both now read "serializer, parser, protocol
   or lifecycle".
2. **C5 names the input properties** of a check-(e) fixture. The draft required a fixture to "supply the
   input-port widths, the sampled outputs and the predicate" without naming them, so an input contract would
   still have come from the descriptor (D-013). The names are the ones the draft's own M27 already used.
3. **C8 no longer appends to File 22 L16.** The draft added "A retrieval attempt on 24 November 2026 returned HTTP
   403". PD-24 is the File 10 vs File 22 inconsistency; File 22 is already right. The sentence would add an
   observation made in a Claude Code session to the pack's provenance log, which nothing else records.
4. **C10's sentence and C3's tokens share L185**, and **every changed file carries the candidate label** (an
   appended Markdown trailer; `fixture_version` = `1.3.7-candidate, not audited` instead of `1.3.7-DRAFT`).

## 3. The corrections

### C1 — Error classes of the change-class vectors (PD-02 (2))

**Conflicting v1.3.6 text.** Error classes are stated for two revision vectors, by fixture ID; the other three
expect one the Protocol never states, and "error class = diagnostic CODE" is not a rule the Protocol keeps:

> [02 L175] "The `M53` study-reset vector uses error class `AUTHORING_REVISION_REQUIRED`"

> [02 L175] "`M54` uses error class `HALT_SIGNATURE_SCHEMA`"

> [02 L175] "`RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` (error class `MID_RUN_REEVALUATION`)"

> [02 L154] "`SIMULATOR_ERROR|target=<RTL_OR_NULL>|class=<EXCEPTION_CLASS>`"

> [41/M48.json L16] "\"error_class\": \"EVALUATOR_REVISION_REQUIRED\","

**Chosen fix (CHANGELOG C1).** A rule limited to three CODEs: `EVALUATOR_REVISION_REQUIRED`,
`AUTHORING_REVISION_REQUIRED` and `HALT_SIGNATURE_SCHEMA` each have the error class of the same name. It
says explicitly that M41 and the stage map are unchanged, and the fixture labels are removed.

**Why.** Every error class L175 does state for these codes has the CODE's own name (the M53 and M54 sentences).
The two counter-examples are other codes: M41's diagnostic is not a CODE of this family, and L154 is a stage-map
row. A rule restricted to these three codes therefore states what L175 already does in its two examples, extends
it to the same codes in M48, M50 and M58, and contradicts nothing.

**Alternatives rejected.**
- "Error class = CODE" for every control expectation: contradicted by L175 (M41) and L154.
- More per-fixture sentences ("`M48` uses error class …"): repeats the PD-02 (1) defect (rules tied to fixture IDs).
- Changing the descriptors' expected error classes: changes the test to fit, and no text argues for other values.
- Leaving it unstated: M48, M50 and M58 stay unresolvable, and File 36 L176 makes an unresolved expectation fail F18.

**Fit with the current code.** `src/openvef/ledger.py` `LIFECYCLE_CASES` marks these three error classes
UNSUPPORTED today, so C1 changes what the code can support. The values equal the descriptors' expected values;
that is the purpose of a correction that settles an under-specification, and the argument above does not rely on it.

### C2 — Change classes and scope tokens as rules (PD-02 (1), (3); PD-07 for the `change_class` input)

**Amended by OD-3 (D-027; section 11).** Document audit #1 (D1-1, MAJOR) found the token vocabulary descriptor-derived,
the `change_class` input contract incomplete, and `HALT_SIGNATURE_COMPONENT_ENUMERATION` misfiled as a change class.
Under OD-3 the scope tokens are owner vocabulary, there are four change classes, and the halt-signature domain
validation is a separate vector (`domain_validation`). The text below is kept as written for the record.

**Conflicting v1.3.6 text.** The literals are keyed by fixture ID, the `change_class` input labels exist only in
descriptors, and four scope tokens exist only as expected values:

> [02 L176] "- **Closed `required_action` literals used by lifecycle fixtures:** `M48` = `"

> [02 L176] "`M48` re-evaluates the affected scope with the same frozen artifact bytes and zero new confirmatory generation calls."

> [41/M48.json L23] "\"rerun_scope_rule\": \"shared_evaluator_component_all_designs_and_all_arm_x_design_slots; design_specific_component_affected_design_in_both_arms\""

> [41/M50.json L21] "\"affected_slots\": \"all_designs_x_all_arms\","

> [41/M58.json L18] "\"affected_scope\": \"affected_design_in_both_arms\","

> [41/M58.json L19] "\"unaffected_design_scope\": \"not_invalidated_when_membership_estimand_and_weights_are_unchanged\","

The meanings are in §7b:

> [02 L183] "If the revised evaluator component is shared across FIFO and UART, the affected scope is both designs and every arm × design slot; if it is design-specific, the affected scope is that design in both arms."

> [02 L181] "halt the entire study and invalidate every scheduled slot across both designs and both arms"

> [02 L181] "If a design-specific author-visible item changes, halt and invalidate every slot for that design in both arms."

**Chosen fix (CHANGELOG C2).** Each literal is keyed by a closed change class instead of a fixture ID (the literal
text is unchanged); the five change classes are defined as cases of §7b; the four scope tokens are stated as
closed tokens with the §7b sentence each one encodes; the closing sentences describe cases, not fixtures.

**Why.** L176 already says each literal is "a closed local control expectation", and its closing sentences
already describe each literal by the case it belongs to (re-evaluation, study invalidation, study reset,
design-specific invalidation). Keying by case is what those sentences describe. The tokens are spelled exactly
as the pack's own expected objects spell them, because the token is the expected output; each is placed next to
the §7b sentence whose meaning it carries.

**Alternatives rejected.**
- Removing the tokens from the descriptors' expected objects: changes the tests to fit.
- Defining scope as a structured value (lists of designs and arms) instead of tokens: no pack text uses such a
  structure, and it would also require changing the expected objects.
- Keeping fixture IDs and adding the change-class name beside each: leaves PD-02 (1) in place.

**Fit with the current code.** The token *strings* are copied from the descriptors, as the draft disclosed; the
Protocol contains none. `LIFECYCLE_CASES` already keys by these change-class labels and cites L176 literals
"labelled M48" and so on; under C2 those citations become "keyed by change class". The **M58
`unaffected_design_scope` token has no single sentence behind it**: it combines L176's "only when membership,
estimand and weights remain unchanged" with L181's contrast between shared and design-specific items.

### C3 — Halt-signature rule tokens (PD-02 (3))

**Conflicting v1.3.6 text.**

> [02 L185] "`stable_error_class` is a simple exception class name matching `[A-Za-z_][A-Za-z0-9_]*` for `SIMULATOR_ERROR` and the literal `NONE` for the other two halt codes; `stable_diagnostic_code` is exactly the corresponding `halt_code` token."

> [41/M54.json L36] "\"stable_error_class_rule\": \"simple_exception_class_for_SIMULATOR_ERROR_else_NONE\","

> [41/M54.json L37] "\"stable_diagnostic_code_rule\": \"exact_halt_code_token\""

**Chosen fix (CHANGELOG C3).** Each of the two rules carries its token in parentheses; the rules are unchanged.

**Why.** The tokens name exactly the two rules already stated in the same sentence; nothing else in the pack
describes them.

**Alternatives rejected.** Removing the two properties from M54 (changes the test); a structured rule language
(no pack text supports one).

**Fit with the current code.** `LIFECYCLE_CASES` marks both UNSUPPORTED today. Token strings copied from M54.

### C4 — Which comparison applies to control vectors (PD-03)

**Completed by OD-3 (D-027; section 11).** D1-2 (PACK) found that the Protocol did not define the properties C4
requires to be defined. OD-3's §20 tables now list them. C4's comparison rule is unchanged.

**Conflicting v1.3.6 text.**

> [36 L176] "compares actual disposition, stage, error class and exact diagnostic bytes with the expected object."

> [36 L23] "a single exact expected disposition/stage/error/diagnostic (or exact control-vector expectation)"

**Chosen fix (CHANGELOG C4).** A four-key expected object is compared on those four values; any other expected
object is a control-vector expectation, compared whole (key set included), and every property it names must be
defined by a rule in the Protocol.

**Why.** L23 already admits "exact control-vector expectation"; L176 only describes the four-field case. The
correction states both cases, and "exact" in L23 is read as the whole object, key set included.

**Alternatives rejected.**
- Comparing only the four fields of a control vector: the extra properties would go unchecked, so L23's "exact"
  would mean nothing, and M14 and M17 have no `diagnostic` key at all.
- Comparing only the keys an implementation computes: lets an implementation pass by omitting properties.

**Fit with the current code.** It states as a rule what A-032 (Claude-decided, approved under D-009) already does.
It does **not** give the output schema PD-03 asks for: the property names of M14, M17 and M41 stay undefined,
and so do the boolean property names of the change-class vectors (`f16_required` and the like), whose values
follow from §7b sentences but whose names come from the descriptors.

### C5 — Legal-input predicate form, check order, check-(e) fixture inputs (PD-06, PD-25)

**Re-based on OD-2 (D-027; section 11).** Document audit #1 (D1-3, MAJOR) ruled that the Python representation is a
new contract, not a reading of v1.3.6. The representation, the purity condition, the hash gate and the
evaluator-failure rule are now the owner rule OD-2. The check order (a)–(e) and the missing-before-extra order stay C5.

**Conflicting v1.3.6 text.**

> [30 L83] "(e) the full vector satisfies the design-specific legal-input predicate from the author-visible reset/legal-input specification."

> [30 L83] "Missing keys, extra keys, wrong width, non-string values, illegal symbols and illegal protocol combinations are distinct reason codes."

> [41/M27.json L14] "\"legal_input_predicate\": \"wr_en must be 0 when full is 1\""

**Chosen fix (CHANGELOG C5).** The predicate is one Python 3.11 function of `(vector, sampled)` returning exactly
`True` or `False`; anything else is an evaluator failure, never an artifact verdict. Within (a), missing keys
before extra keys; (a)–(e) in order, first failure reported. A check-(e) fixture supplies `driver_return`,
`input_port_widths`, `sampled_outputs` and `legal_input_predicate` (`language`, `function`, `source`).

**Why.**
- **Python:** artifacts, harness and pinned interpreter are Python 3.11 (File 30); a predicate in that language
  needs no second language or interpreter.
- **Two arguments:** "illegal protocol combinations" (L83) depend on state, and the only state a driver vector
  meets is the outputs sampled in the same row.
- **Evaluator failure:** a predicate that raises is a defect in frozen evaluator material, not in the artifact.
- **Order:** (a)–(e) are lettered and "verifies before driving" lists them in order, and the Protocol's reason
  enumeration lists `MISSING_KEYS` before `EXTRA_KEYS`:

> [02 L125] "`DRIVER_VECTOR_INVALID.reason` is one of `RETURN_TYPE`, `MISSING_KEYS`, `EXTRA_KEYS`, `NON_STRING_VALUE`, `WRONG_WIDTH`, `ILLEGAL_SYMBOL`, or `ILLEGAL_PROTOCOL_STATE`."

**Alternatives rejected.**
- A declarative predicate language (truth tables, boolean expressions): no pack text defines one, and it
  would need its own interpreter.
- Reporting all failures: L83 gives one reason per invalid vector.
- Extra keys before missing keys: no text supports it; the enumeration order is the only textual order.
- One-argument predicate (vector only): cannot express any state-dependent rule such as "no write while full".

**Fit with the current code.** The two-argument form and the order equal A-041/FIFO-042 (approved by Krishika in
the freeze) and A-027 (Claude-decided, approved under D-009), which `src/openvef/stage_map.py` `validate_vector`
implements. The property names were first used in the draft's own M27, written by the implementation author.

### C6 — M27 descriptor (PD-06, PD-25)

**Superseded (D-027; section 11).** This original C6, the FIFO-042 predicate of the 24 Nov draft, is superseded by A1
(section 5). Document audit #1 (D1-4) asked for that to be kept. A1 stands on OD-2. The text below is kept as written for
the record.

**Amended by A1 (section 5, D-025):** the FIFO-042 predicate below is replaced by the v1.3.6 descriptor's own rule.

**Conflicting v1.3.6 text.**

> [41/M27.json L11] "\"wr_en\": \"1\","

> [41/M27.json L12] "\"full\": \"1\""

> [30 L83] "(a) its key set equals the frozen top-level input-port set exactly"

> [36 L133] "| M27 | missing-case | Driver vector violates a design-specific legal-input predicate |"

**Chosen fix (CHANGELOG C6).** M27 is replaced: a FIFO vector that passes (a)–(d) under supplied widths, the
outputs sampled in that row (`full` = 1), and FIFO-042 in the C5 form. The expected object is unchanged. The
File 36 row says what the vector exercises.

**Why.** As written M27 cannot reach (e): no port set or widths, and `full` is an output, so (a) fails first
(PD-25). The expected object is the fixture's intent, so the input is corrected to reach it. The predicate is
FIFO-042 from the frozen FIFO specification, which also keeps `wr_en` = 1 with `rd_en` = 1 at full legal
(FIFO-030); the v1.3.6 prose forbids it, which the frozen spec does not.

**Alternatives rejected.**
- Keeping the v1.3.6 prose rule in executable form: contradicts FIFO-030.
- A design-neutral toy predicate: possible, and arguably cleaner, but it would be a new rule with no pack or
  spec text behind it; the auditor may prefer it.
- Changing the expected object to `EXTRA_KEYS`: changes the test to fit the defect.

**Fit with the current code.** The FIFO predicate is DRAFT material Claude wrote under D-005 and the owners froze.
The fixture ties M27 to spec v0.2.

### C7 — Stale version label (PD-22)

> [30 L7] "schema version `1.0` is independent of planning-pack version `1.3.1`"

**Fix.** "is independent of the planning-pack version". **Why:** the pack is v1.3.6; any number here goes stale
again. **Rejected:** writing `1.3.6` or `1.3.7` (stale at the next release). **Code:** no effect. No fixture.

### C8 — TechRxiv preprint status (PD-24)

> [10 L174] "**Reported proof of concept.** It evaluates a round-robin arbiter and synchronous FIFO (150–350 LOC), with 12 total test cases."

> [10 L383] "Extracted TechRxiv PDF text, including Definitions and experimental limitations"

> [11 L37] "- TechRxiv checker-gap paper: full extracted text was read; PDF page images were not inspected; the paper's automated/manual injection descriptions conflict."

> [22 L16] "- TechRxiv: the independent Step 3 audit reports abstract-only access. Do not rely on detailed full-text claims from the earlier draft until the exact source PDF is retrieved, versioned and inspected."

**Fix (CHANGELOG C8).** Files 10 (L174, L308, L353, L383) and 11 (L37) stop asserting the preprint's contents
and say they are unverified (File 22). File 22 is unchanged.

**Why.** File 10's own header defers to the provenance log where access claims differ, and File 22 records
abstract-only access; the pack settles which wins.

**Rejected:** asserting the contents (not verified); deleting the passages (loses the record that a claim was
made); appending the 403 observation to File 22 (see section 2). **Code:** no effect. No fixture.
**Stale reference:** File 22 L8–L12 cite the v1.3.6 SHA-256 of File 10; left as written (CHANGELOG).

### C9 — `parser_unit_vector` contract (PD-04)

> [41/M36.json L6] "\"fixture_class\": \"parser_unit_vector\","

> [36 L27] "Serializer unit vectors and lifecycle unit vectors are marked by `fixture_class` and are deliberately grammar-exempt"

> [36 L15] "- `CONTROL_EXPECTATION`: a serializer, lifecycle or policy test vector;"

> [02 L177] "A `CONTROL_EXPECTATION` fixture exercises a serializer, protocol or lifecycle rule"

**Chosen fix (CHANGELOG C9).** File 36 L27 defines the class, its input keys (`source_file`; `syntax_error` with
`lineno` and optional `offset`), the rule it applies (the Protocol §3.4 column rule) and its result. File 36 L15
and Protocol L177 both read "serializer, parser, protocol or lifecycle".

**Why.** The column rule already exists:

> [02 L127] "If `offset` is absent, null or less than 1, emit `column=1`; otherwise emit the positive one-based source-character column reported by CPython."

The contract names exactly the inputs that rule reads (file, line, offset). The disposition `CONTROL_EXPECTATION`
follows from L177: the vector tests a rule, not an artifact. L177 is the Protocol and controls the definition;
File 36 is aligned to it, adding "parser" to both.

**Alternatives rejected.** Treating M36 as a source file to parse (the input has no source); keeping "policy" in
File 36 (it then still differs from the Protocol); a disposition by `fixture_class` alone (M42/M47 are lifecycle
vectors with a non-control disposition, PD-04).

**Fit with the current code.** `src/openvef/source_ast.py` `syntax_reject` implements the L127 column rule
already; the contract matches the only existing vector, M36. A second vector of this class would test it properly.

### C10 — Halt signatures outside the L185 domains (PD-01)

**Amended by A3 (D-027; section 11).** Document audit #1 (D1-7, MAJOR) found the handling of an invalid
supplied signature incomplete. A3 places it outside the executable fixture contract. The text below is kept as
written.

> [02 L185] "`evaluator_component` is `SIMULATOR`, `REPLAY_VERIFIER`, `RECORDER`, `TRACE_ALIGNMENT_CHECKER`, `TRACE_SERIALIZER` or `RTL_NULL_COMPARATOR`"

> [41/M42.json L16] "\"evaluator_component\": \"simulator\","

> [41/M47.json L23] "\"evaluator_component\": \"recorder\","

> [41/M47.json L24] "\"stable_error_class\": \"RecorderFault\","

**Chosen fix (CHANGELOG C10).** The descriptors use the L185 values (`SIMULATOR`, `RECORDER`, and `NONE` for the
trace-integrity signature's error class), and L185 adds: a supplied signature with any out-of-domain component is
an evaluator input error, never compared for recurrence. Expected objects are unchanged.

**Why.** L185 gives "exact domains"; the descriptors are the outliers, and their expected outcomes do not depend
on the spelling (M42's signatures stay identical, M47's stay different).

**Alternatives rejected.** Case-insensitive domains (L185 says "exact"); accepting any string (domains would be
void); keeping the descriptors and defining only the error outcome (M42 and M47 would then expect the wrong result).

**Fit with the current code.** `HaltSignature.given()` already rejects out-of-domain values (D-012, after audit
#1 A8-1). **M42 and M47 still need an error class for `DESIGN_HALT_REPEATED` (PD-26), which no correction
supplies, so they stay NOT_IMPLEMENTED.** M41 also needs an input contract (PD-07).

## 4. What a document auditor is likely to attack

1. **Author conflict:** the implementation author drafted every correction, after writing the code.
2. **Descriptor-derived tokens (C2, C3):** six token strings exist only because the descriptors contain them.
3. **C4 does not supply a schema;** boolean property names of the change-class vectors come from descriptors.
4. **C6 rewrites a fixture's input**, using a predicate the author also drafted (FIFO-042).
5. **C5 chooses Python** as the predicate language; another reading could want a declarative form.
6. **Stale references** left in place: File 22's File 10 hash, file names and headers still saying v1.3.6,
   `03_Change_Log` and `32_Status_and_Gates`; the `archive_*` entries of `27_SHA256SUMS.txt` are not in the copy.
7. **Ten fixtures are not covered,** so a v1.3.7 F18 cannot pass on these corrections alone.

## 5. Amendments (numbered; each in its own commit)

### A1 — C6: a design-neutral predicate (D-025 item 2)

**Stands on OD-2 (D-027; section 11).** A1's executable predicate uses the representation that OD-2 adopts. Under OD-2,
M27's predicate also carries its frozen hash `source_sha256`, and its expected object is unchanged.

**What changes.** M27's input becomes `driver_return` = `{"wr_en": "1"}`, `input_port_widths` = `{"wr_en": 1}`,
`sampled_outputs` = `{"full": "1"}`, and the predicate `not (sampled["full"] == "1" and vector["wr_en"] == "1")`. The
expected object, the File 36 row and C5 are unchanged.

**From the pack text.** The pack already states the rule M27 is meant to exercise:

> [41/M27.json L14] "\"legal_input_predicate\": \"wr_en must be 0 when full is 1\""

Its defects (PD-25) were that `full` sits in the driven vector and that no port set or widths are given:

> [41/M27.json L12] "\"full\": \"1\""

> [30 L83] "(a) its key set equals the frozen top-level input-port set exactly"

The rule names `full` only as a condition ("when full is 1"), so it is a sampled value, and `wr_en` is the only driven
port it mentions. Executing exactly that rule over a port set of `wr_en` alone, with `full` sampled, keeps the pack's
own predicate and fixes only what PD-25 names. A fixture executes "under pinned Python 3.11 and parser/schema
versions" (36 L176): nothing in that list is a design specification, so a fixture should not need one.

**Rejected.**
- **FIFO-042** (the D-024 choice): it comes from the owner-frozen FIFO specification, outside the pack, written by
  the implementation author, and ties F18 to one design's materials.
- **Abstract port names** (`a`, `b`): further from the pack's own wording than needed.
- **Adding `rd_en`**: brings back the question PD-25 raised (is a write with a read at full legal?), which the pack
  answers nowhere; FIFO-030 answers it only for the FIFO.

**Withdrawn.** C6's rejection "Keeping the v1.3.6 prose rule in executable form: contradicts FIFO-030" held only for a
port set that includes `rd_en`; with `wr_en` alone there is no such case.

**Fit with the current code.** None needed: the C5 adapter is general. The amended M27 passes (a)–(d) and fails (e);
`{"wr_en": "0"}` is legal (tests/test_v137_candidate_pack.py).


### A2 — The File 25 normative copy of Protocol §3.4 (D-025 item 3; a defect in how D-024 applied C1–C3, C9, C10)

**What was wrong.** File 25 carries a line-for-line copy of Protocol L90–L187 and says so:

> [25 L32] "NORMATIVE CONTROL COPY (NOT MODEL-VISIBLE; normative text below is identical to Protocol §3.4):"

D-024 changed Protocol L175, L176, L177 and L185 but not their copies (File 25 L118, L119, L120, L128), so the
candidate contradicted its own statement. Found while checking stale references for D-025.

**What changes.** Every edit inside Protocol L90–L187 is applied to File 25 at the line 57 lower; the build asserts the
two ranges are identical before and after, and the test checks that File 25 L1–L32 (both model-visible bodies) are
byte-identical to v1.3.6, so no prompt text and no sidecar hash changes. File 25 gets the candidate trailer after its
last line, outside the model-visible bodies.

**Rejected.** Leaving the copy stale (contradicts L32); deleting the copy (removes text the pack declares normative).

## 6. Stale references (D-025 item 3; CHANGELOG entries `S`)

**Rule.** A reference is stale when its correct target in the candidate differs from what it names. That covers:
- the pack's own version, title or audit status in a current document (Files 01, 02, 21, 30, 31, 32, 33, 36, 38 and
  the README): titles and version lines now name v1.3.7-candidate, and each version line keeps the v1.3.6 text after
  "Based on:";
- the names of those nine files, which carry the pack version: renamed (`…v1.3.6…` → `…v1.3.7-candidate…`), and every
  reference to them in a current document updated, including Protocol L187's copy in File 25 (A2 applies);
- File 22 L8–L12, which cite File 10 by SHA-256 as the literature-review record: now the candidate File 10's hash;
- `27_SHA256SUMS.txt` (derived) and the sidecar's `sidecar_version` and `payload_manifest_file`.

**Kept on purpose (not stale). DECIDED: these three exceptions are approved by Krishika under D-026 item 1.**
- **History:** the v1.3.6 change log, build, correction and audit records (Files 03, 48, 50, 56, 57, 58, 63 and the
  audit transcripts), and statements of what v1.3.6 did or what stayed unchanged "from v1.3.3 through v1.3.6". These are
  true of v1.3.6, and rewriting them would falsify the record.
- **Owner records (Files 16, 23):** they record owner decisions and approvals on v1.3.6. Renaming or retitling them
  would present the candidate as owner-reviewed, which it is not.
- **Pack status of the implementation** (File 32 "NOT IMPLEMENTED / NOT RUN"): the pack's own statement; this
  repository's implementation is outside the pack, and importing it would be a new claim, not a fix.
  **Qualified by C17 (D-027; section 11):** document audit #1 (D1-9) asked for this status to be split. C17 rewords
  File 32 L21 and L33 into development-run evidence, formal F18 status and approval. It names no run of this
  repository and claims nothing for it.

**Check.** `tests/test_v137_candidate_pack.py` `test_no_stale_name_or_hash`: no current document names a renamed
file by its old name or cites File 10's old hash.

## 7. C11–C16 (D-025 Phase A: PD-26, PD-20, PD-03, PD-07)

Same rules as sections 1–3: each correction quotes the conflict, takes the reading most consistent with the pack, lists
what was rejected, and states its fit with the current code; none was chosen because it suits the code. Where a fixture
could be corrected only by inventing behaviour the pack never states, it is **not** corrected: section 8 records the
exact owner decision it needs. All Protocol edits lie in L90–L187, so A2 applies them to File 25 too; input contracts are
a new section after File 36's last line, so no line moves.

### C11 — Error classes of `DESIGN_HALT_REPEATED` and `FEEDBACK_SERIALIZER_REJECT` (PD-26)

**Retired in part by OD-1 (D-027; section 11).** Document audit #1 (D1-5, BLOCKER) found that the majority pattern
below is not a normative rule. The two error classes now rest on the owner convention OD-1, labelled in the pack text.
The argument under "Why" is kept as written for the record. It is no longer the basis of these values.

> [02 L185] "terminate with `DESIGN_HALT_REPEATED|reason=EVALUATOR_FAILURE_REPRODUCED`"

> [02 L173] "`FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC`"

> [41/M42.json L32] "\"error_class\": \"DESIGN_HALT_REPEATED\","

> [41/M15.json L18] "\"error_class\": \"FEEDBACK_SERIALIZER_REJECT\","

**Fix.** L185: both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED` (the
disposition `DESIGN_ABORTED_NO_SLOTS_SCORED` is already stated). L174: `FEEDBACK_SERIALIZER_REJECT` is recorded at stage
`FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`.

**Why.** In the stage map (L141–L162), of the 14 rows whose diagnostic is one CODE of its own (the two checker-null rows
and the two grouping rows aside), 13 have that CODE as their error class, for example:

> [02 L155] "| `DESIGN_HALT` | `TRACE_INTEGRITY_FAILURE` | `TRACE_INTEGRITY_FAILURE|reason=<REASON>`"

A different class appears where one class groups several codes (`IMPORT_POLICY_REJECT`, `ENTRY_POINT_REJECT`,
`ASSEMBLY_OR_MANIFEST_FAILURE`), and once for a single code:

> [02 L154] "| `DESIGN_HALT` | `EVALUATOR_INFRASTRUCTURE_FAILURE` |"

Both codes here stand alone, with two reasons each at most, so the majority rule applies. The stages are the ones the
L172 stage list provides for a design halt and for the serializer; `CONTROL_EXPECTATION` follows L177 (a serializer
rule under test, not an artifact event).

**Rejected.**
- `EVALUATOR_INFRASTRUCTURE_FAILURE` for `DESIGN_HALT_REPEATED`: that class labels a simulator error; M47's second
  halt is a trace-integrity fault, so a class taken from the triggering halt would differ between the two terminations
  L185 treats alike.
- `ASSEMBLY_OR_MANIFEST_FAILURE` for `FEEDBACK_SERIALIZER_REJECT`: L174 states it for `F18_REJECT` fixtures (assembly
  and manifest gates); a serializer rejection is neither.
- A general "error class = CODE" rule: contradicted by L154 and the grouping classes.

**Fit with the current code.** The values equal the descriptors'; the existing recurrence adapter stops at PD-26 and
`serializer.NON_NORMATIVE` already uses this class (A-029). The textual argument is the majority rule above.

### C12 — The emitted-set rule (PD-20)

> [02 L168] "The serializer accepts only a complete diagnostic emitted by the authoritative stage map."

> [41/M15.json L11] "\"allowed_diagnostics\": ["

**Fix.** L168: when the set of diagnostics the stage map emitted is given, a diagnostic that passes the grammar but is
not in it is also rejected at step (1), with the same diagnostic. File 36: the serializer-grammar vector (`diagnostic`,
optional `allowed_diagnostics`).

**Why.** "Accepts only a complete diagnostic emitted by the authoritative stage map" is a membership condition; the
grammar check is step (1) and comes first. The only reason code the pack has for a rejected diagnostic is
`NON_NORMATIVE_DIAGNOSTIC`.

**Rejected.** A new reason such as `NOT_EMITTED` (invented token); ignoring `allowed_diagnostics` (drops L168's
membership condition); membership before grammar (step (1) names the grammar).

**Fit with the current code.** A-029 (Claude-decided, approved under D-009) and `serializer.check_diagnostic` already
read L168 this way.

### C13 — The truncation-primitive vector, and the primitive error classes by rule (PD-03, PD-02 (1), PD-07)

> [02 L174] "The M14 truncation primitive uses error class `TRUNCATION`."

> [02 L187] "M14 tests the UTF-8 truncation function in isolation, and M17 tests JSON escaping in isolation."

> [41/M14.json L22] "\"contains_marker\": true,"

**Fix.** L174 states both primitive error classes for a kind of vector, not a fixture ID, and adds their stage and
disposition. L168 defines the four step-(2) output properties. File 36 gives the input contract; the properties L168
fixes (cap 2,048, marker `...[TRUNCATED]`, code-point boundary, before escaping) must equal L168 and do not change the
result.

**Why.** L187 says the primitive is tested in isolation, and L168 step (2) determines every reported value; C4 requires
each control-vector property to be defined by a Protocol rule, which this supplies. The property names are the pack's
own (the descriptor's).

**Rejected.** Reporting the truncated string itself (the expected object does not contain it, and the descriptor is the
pack's statement of what is compared); running the full pipeline (L187: isolation, and the grammar would reject it).

**Fit with the current code.** `serializer.truncate` implements step (2) already.

### C14 — The JSON-escaping-primitive vector (PD-03, PD-07)

> [02 L168] "Serialize UTF-8 with `ensure_ascii=false`, two-space indentation, LF line endings, exactly one final LF and the same key order."

> [41/M17.json L28] "\"diagnostic_sha256\": \"226a87deb777b94556d262a0e45e669ced8c80f5cf8ec1bc3d691e9d4570423f\","

**Fix.** L168 defines `diagnostic_utf8`, `diagnostic_sha256` and `diagnostic_bytes` for step (3) alone; File 36 gives
the input contract, whose formatting properties must equal L168's.

**Why.** Step (3) fixes every byte of the output; the three properties are that output, its hash and its length.

**Rejected.** Using the input's own formatting values to drive serialization (L168 fixes them; the input only restates
them); naming the output `diagnostic` (the descriptors use `diagnostic_utf8`, and C4 keeps the four-key form for
four-key objects only).

**Fit with the current code.** `serializer._serialize_object` is step (3).

### C15 — The lifecycle halt-event vector (PD-07)

**Defined by OD-4 (D-027; section 11).** Document audit #1 (D1-6, MAJOR) found that the meaning of
`evaluator_repair_attempt` rested partly on the descriptor's field name. OD-4 now defines it in §7b (L185). The
input contract below is unchanged.

> [41/M13.json L10] "\"lifecycle\": \"MID_RUN\","

> [41/M13.json L22] "\"evaluator_repair_attempt\": 1"

> [41/M42.json L12] "\"recovery_cycles_used\": 1,"

> [02 L183] "One recovery cycle per affected design is allowed."

**Fix.** File 36: `lifecycle` = `MID_RUN`; one design-halt `event` (`simulator_error` or `trace_integrity`); `slots`
counts that add up; `evaluator_repair_attempt` = 1, the ordinal of the recovery cycle this halt opens. The result is
the event's stage-map row with disposition `DESIGN_HALT_NO_SLOT_SCORED`.

**Why.** §7b names a design-local simulator error or trace-integrity fault "after slots have begun" as the mid-run halt,
and the stage map gives its record. The pack itself distinguishes "attempt" from cycles used: the recurrence vectors
count `recovery_cycles_used`, and M13 counts `evaluator_repair_attempt`. Read as the ordinal of the cycle this halt
opens, attempt 1 is the one cycle L183 allows, and a halt after it is a recurrence (L185), which has its own shape.
`DESIGN_HALT_NO_SLOT_SCORED` follows from L185 "Discard all pre-halt partial scores".

**Rejected.** Reading `evaluator_repair_attempt` as cycles already used: then L185 would make every such halt a
recurrence, and the field would duplicate `recovery_cycles_used`. Letting the slot counts change the record: the stage
map gives the record from the event alone.

**Fit with the current code.** `stage_map.EVENT_ROWS` already gives these rows and disposition (A-025). **Attack
point:** the reading of `evaluator_repair_attempt` rests on the contrast between two descriptor field names.

### C16 — The design-preflight vector (§7a; PD-07)

> [02 L179] "Any baseline mismatch halts the design before slots exist; no slot is scored."

> [02 L157] "| Same paired inputs produce a masked output divergence under the artifact's own stimulus | `DESIGN_HALT` | `RTL_NULL_CONTROL_FAILURE` |"

> [41/R07.json L11] "\"rtl_null_masked_divergence\": true"

**Fix.** L179: a baseline mismatch is recorded at stage `DESIGN_HALT`, error class `RTL_NULL_CONTROL_FAILURE`, diagnostic
`RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE`, disposition `DESIGN_HALT_NO_SLOT_SCORED`. File 36: the
`design_preflight` input contract.

**Why.** §7a requires "original-RTL/null equivalence under the frozen mask", so its mismatch is a same-input masked
divergence; L157 is the only row for that, `RTL_NULL_CONTROL_FAILURE` is also its L185 halt code, and "no slot is
scored" names the disposition.

**Rejected.** A new baseline diagnostic (no pack text); disposition `DESIGN_ABORTED_NO_SLOTS_SCORED` (L185 uses it for a
second halt after recovery, not for a gate before slots).

**Fit with the current code.** `stage_map.paired_run_failure` already produces this record for a masked divergence; R07
passed with an earlier adapter until D-013 removed it for lack of a cited contract.

## 8. Needs owner specification (not corrected)

These three cannot be corrected without behaviour the pack never states. They stay NOT_IMPLEMENTED on the candidate.
**Answered by owner decision D-026** (Krishika): the questions below are kept as asked; the answers are the
OWNER-SPECIFIED items OS-1 to OS-3 in section 10, which are not corrections and are counted separately.

**M41 — operational-recovery vector.**

> [41/M41.json L21] "\"required_action\": \"pause_repair_preflight_rerun_all_10_slots\","

> [41/M41.json L14] "\"previously_evaluated\": 4,"

> [41/M41.json L28] "\"pre_halt_scored_slots\": 3,"

*Question for the owners:* what is the input contract of an operational-recovery vector? Specifically: (1) which of its
fifteen input properties decide the outcome, and what is the outcome when one of the L183 conditions fails
(`frozen_evaluator_hashes_unchanged` false, `f16_required` true, `same_artifact_bytes` false, or
`author_visible_materials_changed` true)? (2) What does the input `required_action` mean? Its literal appears in no pack
text. (3) Which count is the number of pre-halt scores: `slots.previously_evaluated` (4) or `pre_halt_scored_slots` (3)?

**M37 — aliased global random access.**

> [41/M37.json L30] "\"driver_source_excerpt\": \"r = random; r.random()\","

> [41/M37.json L32] "\"next_input_schedules_equal\": false"

*Question for the owners:* the excerpt is not in the response's driver source, which uses a seeded `random.Random(seed)`
and is deterministic. Should M37 (a) be a supplied-outcome vector, where the response's static stages run and
`runtime_pair` stands in for the paired run, and if so what role, if any, has `driver_source_excerpt`; or (b) carry a
driver source that actually contains the aliased access and be run in the sandbox on a design? If (b), on which design
and ports?

**P17 — driver returns an incomplete vector at runtime.**

> [41/P17.json L29] "\"port_manifest\": {"

*Question for the owners:* P17 gives a response and an input-port list but no design, RTL or widths, and the Protocol runs
a driver only in stage (7) on the original RTL. How is the driver's vector obtained? Is `create_driver` called with which
seed, `step` called with which `cycle_index` and `outputs_after_edge`, how many times, outside any simulation? Or should
P17 instead name a design whose RTL the harness runs?

## 9. Coverage of the 17 after C1–C16

| Fixture | Correction | Status on the candidate |
|---|---|---|
| M27 | C5, C6 + A1 | covered |
| M36 | C9 | covered |
| M48, M50, M53, M54, M58 | C1–C4 | covered |
| M42, M47 | C10, C11 | covered |
| M15 | C11, C12 | covered |
| M14 | C13 | covered |
| M17 | C13, C14 | covered |
| M13 | C15 | covered (attack point: `evaluator_repair_attempt`) |
| R07 | C16 | covered |
| M41 | OS-1 (OWNER-SPECIFIED) | covered by an owner specification, not a correction (section 10) |
| M37 | OS-2 (OWNER-SPECIFIED) | covered by an owner specification, not a correction (section 10) |
| P17 | OS-3 (OWNER-SPECIFIED) | **NOT_IMPLEMENTED**: expected stage is at runtime (section 10) |

**Counted separately (D-026):** pack-derived corrections C1–C16 (with A1, A2) cover 14 of the 17; OWNER-SPECIFIED
items cover 2 more (M41, M37); 1 (P17) stays NOT_IMPLEMENTED under OS-3. No fixture is both.

## 10. OWNER-SPECIFIED items OS-1 to OS-3 (owner decision D-026)

**Category.** These are **OWNER-SPECIFIED**, not pack-derived corrections. Owner decision D-026 (Krishika) answered the
section 8 questions with rules; the text below applies those rules, and candidate File 36 L201–L207 states the result,
labelled OWNER-SPECIFIED. Every evidence record of a fixture they cover carries the label, and run summaries count them
apart from C1–C16. Drafted by Claude (the implementation author) from D-026; not audited.

**D-026's governing rule.** The expected outcome is fixed by the pack; an OS item specifies only how the vector reaches
the stage that outcome names, and never adds an outcome code. If a rule does not determine an answer, the fixture stays
NOT_IMPLEMENTED with the reason. Each expected stage was read from pack text when the items were drafted; the code never
reads an expected object (rule 4). Each item is a general input contract for a shape, not a rule for one fixture.

### OS-1 — Operational-recovery vector (M41)

D-026: (1) the outcome-deciding properties are exactly those named by the L183 conditions; for a failed condition use
the outcome the pack states, otherwise leave it unspecified; (2) `required_action` is an informational label; (3)
pre-halt scores are counted by `pre_halt_scored_slots`, since "scored" is the pack's word.

**The L183 conditions and the properties they name.**

> [02 L183] "For a design-local simulator error, evaluator trace-integrity fault or same-input masked RTL/null divergence after slots have begun"

The trigger names the halt (`halt_signature`, with `design_id` as the affected design) and that slots had begun
(`slots`, with the same domain as the C15 halt-event vector).

> [02 L183] "One recovery cycle per affected design is allowed."

This names `evaluator_repair_attempt` = `1` (the C15 reading: the ordinal of the cycle this halt opens).

> [02 L183] "it creates no new hashes, requires no new F16 and changes no artifact"

These three conditions of operational recovery name `frozen_evaluator_hashes_unchanged`, `f16_required` and
`same_artifact_bytes`; the form itself names `recovery_mode` = `OPERATIONAL_RECOVERY` (the token is the descriptor's).

> [02 L183] "A change to any author-visible or estimand-defining item follows the study/design revision rules in the preceding paragraph, not the evaluator-revision path."

This names `author_visible_materials_changed`.

> [02 L183] "A masked RTL/null divergence may use operational recovery only when a documented root-cause review attributes it to a transient evaluator fault"

The vector carries no root-cause review, so `halt_code` `RTL_NULL_CONTROL_FAILURE` is out of scope (the outcome is not
determined).

**Failed conditions (D-026 (1)).**

| Condition that fails | Outcome the pack states | OS-1 result |
|---|---|---|
| frozen evaluator hashes changed (`frozen_evaluator_hashes_unchanged` false; `f16_required` true; artifact bytes the same; no author-visible change) | L183 path (b) and L175, below | the change-class control expectation of `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` (C1–C4) |
| `author_visible_materials_changed` true | L183 sends it to the L181 study or design revision rules, but a shared-item revision, a design-specific revision and a study reset are three outcomes with different records, and the vector does not say which applies | out of scope |
| `f16_required` true with hashes unchanged; `same_artifact_bytes` false; any other mix | none | out of scope |
| masked RTL/null divergence | operational recovery needs a review the vector lacks | out of scope |

> [02 L175] "`EVALUATOR_REVISION_REQUIRED|reason=FROZEN_EVALUATOR_CHANGED` means a frozen evaluator source/binary/tool-version/command/option/configuration changed"

> [02 L183] "An evaluator revision is not an operational restart"

A changed frozen-evaluator hash is that change. Path (b) also requires F16 and keeps the artifact bytes, so the evaluator-revision record
applies only when the vector agrees with path (b) (`f16_required` true, `same_artifact_bytes` true). The author-visible
row comes first because L183 says such a change does not follow the evaluator-revision path.

**Success.** All four conditions hold.

> [02 L175] "`RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` (error class `MID_RUN_REEVALUATION`) is the M41 control-expectation diagnostic for a successful operational recovery"

> [02 L185] "Discard all pre-halt partial scores and use only the complete post-recovery rerun ledger."

> [02 L185] "with the same frozen artifact bytes and slot seeds; no confirmatory generation call is made"

The record is L175's diagnostic and error class, at stage `DESIGN_HALT` (the L172 stage of a §7b design halt, as in
C11) with disposition `CONTROL_EXPECTATION` (a lifecycle rule under test, L177). Its four further properties are L175's
own sentence ("It discards pre-halt scores, reruns preflight, and re-evaluates every scheduled slot ... with identical
artifact bytes and seeds and zero new confirmatory generation calls"): `discard_pre_halt_scores` = `true`,
`rerun_slots` = `scheduled_slots`, `reuse_same_artifact_bytes` = `true`, `new_confirmatory_generation_calls` = `0`. The
property names are the descriptor's (as in C13).

**Properties that do not decide the outcome.**
- `required_action` (D-026 (2)): a string; never compared. Its literal appears in no pack text.
- `pre_halt_scored_slots` (D-026 (3)): 1 to `slots.previously_evaluated` (the triggering slot halted, L154, so it has no
  pre-halt score). Zero is out of scope: L185 does not say whether discarding no scores is reported as a discard.
- `scheduled_slots` must equal `slots.scheduled`; `same_artifacts_for_all_slots` = `true`, `same_slot_seeds` = `true` and
  `new_generation_calls` = `0` restate L185. As with C13's fixed properties, they must equal those values and do not
  change the result.

**Rejected.** `slots.previously_evaluated` as the pre-halt score count (D-026 (3)). An outcome for an author-visible
change: the pack states three revision outcomes and the vector does not choose between them, so picking one would add
behaviour. Reading `required_action` as an outcome input (D-026 (2)).

**Fit with the current code.** The evaluator-revision record is `ledger.lifecycle_expectation_candidate` (C1–C4);
the success record is new code, built from the values above.

### OS-2 — Paired-run outcome vector (M37)

**Amended by A4 (D-027; section 11).** M37 is relabelled a paired-outcome control vector, not a test of
source-level alias detection (D1-8). The text below is kept as written.

D-026: a static-stage outcome makes it a static vector; a runtime or paired outcome uses option (a): `runtime_pair`
stands in for the paired run, and the excerpt documents the access being tested.

**Which case applies.** M37's expected stage is `TERMINAL`, the L156 row:

> [02 L156] "| Before first raw output divergence, paired next-input schedules differ | `TERMINAL` | `DRIVER_NONDETERMINISM` |"

> [02 L166] "any next-input mismatch before first raw-output divergence is terminal driver nondeterminism"

That is evaluation step (8), a paired outcome, so option (a) applies; the static-vector branch of the rule is not used.

**Specification.** Steps (1)–(6) (schema, source, import policy, AST signature, both compilations) run on
`response_object`; their first failure is the result. If they all pass, `runtime_pair` stands in for steps (7)–(8). Step (7)
includes the factory and runtime-signature checks, so those do not run either: the paired run is not executed. This differs
from the null-runs vector (A-028), which also runs the sandboxed factory checks. D-026 option (a) says the response's
*static* stages run, and nothing in this vector needs the sandbox. Only `before_first_raw_output_divergence` = `true` with
`next_input_schedules_equal` = `false` gives the L156 record. A pair with equal schedules, or one after the first raw
divergence, leaves the rest of the paired run (masked divergence, checker null runs) undetermined, so it is out of
scope. `driver_source_excerpt` is a string and is never executed, matched or read for the outcome.

**Rejected.** Checking that the excerpt occurs in the driver source (D-026: it documents the access; the response's
driver uses `random.Random(seed)` and does not contain it). Running the factory checks (see above).

### OS-3 — Runtime driver-vector input (P17): stays NOT_IMPLEMENTED

D-026: if P17's expected stage precedes runtime, run up to that stage only; otherwise leave it NOT_IMPLEMENTED.

> [02 L152] "| Driver return value/vector is invalid | `DRIVER_VECTOR` | `DRIVER_VECTOR_INVALID` |"

> [02 L166] "(7) Execute `create_driver(seed)` and `Driver.step` on original RTL, then on null netlist"

> [02 L166] "within each cycle, exception wins over vector validation"

`DRIVER_VECTOR` is checked inside step (7), while the driver runs on the original RTL, so it does not precede runtime.
The rule therefore leaves P17 NOT_IMPLEMENTED. Its record gives the reason and the OS-3 label. Candidate File 36 L207
says so, so the input shape is labelled without code that names the fixture.

## 11. Correction cycle 2 (owner decision D-027, after document audit #1)

Document audit #1 (GPT-6, an AI model, operated by Krishika, bundle `c4caff40…cbd7`;
`docs/reviews/doc-audit1-gpt6-2026-11-27.md`) found cycle 1 NOT CLEARED: 1 BLOCKER, 5 MAJOR, 2 MINOR and 1 PACK
finding (D1-1 to D1-9). Krishika decided D-027 on a Claude (claude.ai) triage of the report. These items answer it.

- **New category OWNER-DECIDED (OD-n):** a normative rule the pack owners add that v1.3.6 does not state. Every OD rule is
  labelled `OWNER-DECIDED OD-n` in the pack text that states it, in the CHANGELOG and in every record that depends on it.
  A fixture that depends on any OD rule counts as OWNER-DECIDED, not as PACK-DERIVED. OD rules are not argued from the
  v1.3.6 text. Each item below states what the pack leaves open, the rule the owners chose, and the pack text it rests on.
- **Unchanged:** every expected object (D-027). Cycle-2 edits stay inside one line or are appended after a file's last
  line, as in cycle 1. They are logged after E158 and edit the text as cycle 1 left it.
- **Order:** OD-1, OD-2, OD-3, OD-4, A3 (D1-7), A4 (D1-8) and C17 (D1-9), each in its own pack-only commit, before any
  code change (Phase A).

### OD-1 — Error class of a single-code row with no stated error class (D1-5; amends C11)

**Finding D1-5 (BLOCKER).** v1.3.6 names `DESIGN_HALT_REPEATED` and `FEEDBACK_SERIALIZER_REJECT` but gives neither an
error class:

> [02 L185] "If the identical halt signature recurs after recovery, terminate with `DESIGN_HALT_REPEATED|reason=EVALUATOR_FAILURE_REPRODUCED`."

> [02 L173] "- F18/packet diagnostics: `PACKET_FREEZE_REJECT|reason=RESERVED_HEADING_LINE`, `ASSEMBLY_REJECT|reason=UNRESOLVED_PLACEHOLDER`, `F18_REJECT|reason=VISIBLE_CLAUSE_ID_SET_MISMATCH`, `F18_REJECT|reason=MALFORMED_CLAUSE_ID_TOKEN`, `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC`."

C11 chose the classes by the pattern of the stage map. The audit ruled that a majority of rows is not a rule.

**Owner rule (D-027).** "A stage-map row with a single diagnostic code and no stated error class has error class =
diagnostic code; SIMULATOR_ERROR is the stated exception." Applied to `DESIGN_HALT_REPEATED` and
`FEEDBACK_SERIALIZER_REJECT`. The exception is the row whose single code differs from its stated class:

> [02 L154] "| Simulator error on RTL or null run | `DESIGN_HALT` | `EVALUATOR_INFRASTRUCTURE_FAILURE` | `SIMULATOR_ERROR|target=<RTL_OR_NULL>|class=<EXCEPTION_CLASS>`; halt design, repair evaluator and apply §7b; no model feedback |"

**Pack text (candidate).** L174 states OD-1, labelled, and applies it to `FEEDBACK_SERIALIZER_REJECT`. L185 labels the
`DESIGN_HALT_REPEATED` sentence `OWNER-DECIDED OD-1`. Both lines lie in L90–L187, so A2 copies them into File 25.

**Two choices made in wording it (decided by Claude under standing delegation; A-059, approved by Krishika under D-029 item 2):**
- *"Stage-map row" includes the local-ledger vocabulary rows.* The two codes D-027 names are not rows of the L141–L162
  table. They are listed in the §3.4 local-ledger vocabulary (L173, L175) and in §7b (L185). D-027 applies OD-1 to
  exactly these two, so the rule must reach those rows.
- *A cell `—` states "no error class".* The stage map gives `—` as the error class of two rows, for example:

> [02 L162] "| Malformed diagnostic item with otherwise valid top-level return and verdict | — | — | Log `DIAGNOSTIC_FORMAT_WARNING`, discard item; `ACCEPT_WITH_WARNING`; verdict retained |"

  The table states a value there (none), so that row has a stated error class and OD-1 does not reach it. Read the
  other way, OD-1 would give `DIAGNOSTIC_FORMAT_WARNING` an error class that the L162 table cell denies.
- **Scope check.** Every other single-code row and local-ledger diagnostic states its class: L143–L161 in the table,
  L174 for `F18_REJECT`, `PACKET_FREEZE_REJECT` and `ASSEMBLY_REJECT` fixtures, and L175 for the lifecycle codes (C1).
  OD-1 therefore decides exactly two error classes, and the pack text says so.

**Fixtures that depend on OD-1:** M15 (`FEEDBACK_SERIALIZER_REJECT`), M42 and M47 (`DESIGN_HALT_REPEATED`). Their
expected objects are unchanged. C1's three revision codes keep their own rule (C1), so OD-1 does not re-base them.

**Fit with the current code.** The values are the ones the C11 code already produces. Only the citation and the record
label change (Phase B).

### OD-2 — The legal-input predicate is a Python 3.11 function (D1-3, D1-4; re-bases C5, A1 stands on it)

**Findings D1-3 (MAJOR) and D1-4 (MAJOR).** v1.3.6 requires a predicate but no representation:

> [30 L83] "(e) the full vector satisfies the design-specific legal-input predicate from the author-visible reset/legal-input specification."

C5 made the predicate a Python function and presented that as the reading of this line. The audit ruled that it is an
added contract: v1.3.6 does not prescribe the language, the source in the fixture, the two-argument interface or the
exception rule. D1-4 asked that A1 be kept rather than the original C6.

**Owner rule (D-027).** "Owners adopt Python 3.11 as the legal-input predicate representation: one pure function
(vector, sampled) -> bool, frozen and hash-gated, executed by the evaluator; exceptions are evaluator failures."

**Pack text (candidate File 30 L83).** The C5 sentence is labelled `OWNER-DECIDED OD-2` and gains the purity condition
(the result depends only on the two arguments; no other effect). A new sentence states that the predicate is evaluator
material, executed by the evaluator outside every artifact process, and that it is hash-gated: its SHA-256 is recorded
when frozen, and it runs only after its source is checked against that hash, with a mismatch an evaluator failure. The
check-(e) fixture input gains `source_sha256`. C5's other content (the Boolean result, exceptions as evaluator
failures, check order) is unchanged.

**Descriptor (M27, whole file, logged as OD-2).** A1's descriptor plus `source_sha256` =
`sha256(source)` (UTF-8, lowercase hex). The source, the other inputs and the expected object are A1's, unchanged.

**Not decided here.** Purity is a condition on the frozen predicate. The evaluator cannot prove it of arbitrary source:
it checks the hash, the Boolean result and the absence of an exception. The owners freeze a pure predicate, and the
evaluator does not certify purity. This is a stated limit, not a guess.

**Fixtures that depend on OD-2:** M27.

**Fit with the current code.** The runner already executes the predicate in the evaluator, and only after the candidate
pack's SHA256SUMS verify (D-025). Phase B adds the per-predicate hash check and the OD-2 label.

### OD-3 — Control-vector input contracts and result schemas (D1-1, D1-2; amends C2, completes C4)

**Findings D1-1 (MAJOR) and D1-2 (PACK).** v1.3.6 keys the `required_action` literals by fixture and defines no schema
for the other properties of those expected objects:

> [02 L176] "- **Closed `required_action` literals used by lifecycle fixtures:** `M48` = `"

> [02 L176] "Each literal is a closed local control expectation, not a model-feedback diagnostic."

> [41/M48.json L19] "\"new_evaluator_version_hashes_required\": true,"

The audit found three problems with C2: the scope-token spellings come from the descriptors, `change_class` has no
complete input contract, and the halt-signature domain check is filed as a change class. D1-2 adds that C4 requires
every property to be defined by a Protocol rule, but the Protocol does not define them.

**Owner rule (D-027).** "A normative control-vector schema table in the Protocol for every property in M48, M50, M53,
M54, M58 (and any other control vector): name, type, allowed values, rule. Define the change_class input contract; move
HALT_SIGNATURE_COMPONENT_ENUMERATION out of change classes into domain validation; adopt the scope tokens explicitly as
owner vocabulary. Any property no rule can fix: list it, don't guess."

**Pack text (candidate).**
- **Protocol §20**, appended after the last line (no line moves), labelled `OWNER-DECIDED OD-3`:
  - §20.1 gives the two input contracts. `change_class` is exactly one of four classes; the input is the class alone,
    so the result states the rule for that class. `domain_validation` is exactly `HALT_SIGNATURE_COMPONENT_ENUMERATION`.
  - §20.2 gives the five properties every such result has.
  - §20.3 gives each further property with its type, value, quoted rule and basis.
  - §20.4 lists the other control vectors, whose schemas were already stated by C9, C12–C14 and OS-1, so the table
    covers every control vector.
- **Protocol L176:**
  - four change classes;
  - `HALT_SIGNATURE_COMPONENT_ENUMERATION` "is not a change class: it names the halt-signature domain validation";
  - the scope tokens are labelled owner vocabulary;
  - a pointer to §20.
  A2 copies the L176 edits into File 25.
- **File 36 L176:** the rule that every property needs a Protocol rule points to §20.
- **M54 descriptor:** its input key is `domain_validation` instead of `change_class`. The value and the expected object
  are unchanged.

**Basis column.** A row is `pack` when a quoted v1.3.6 sentence fixes the value. It is `OD-3` for the four scope tokens
and the two new input contracts. `C1`/`C3` mark the error-class rule and the rule labels. `A-033` marks the stage
`DESIGN_HALT`, a reading approved under D-009 (no sentence names the stage of these records; §7b is the design-halt
policy). "order OD-3" marks the domain arrays, which follow L185's listing order. The arrays are compared whole, so their
order matters, and only the listing gives one.

**Properties no rule can fix: none found.** Every property of the five expected objects has a sentence that fixes its
value (checked by `tests/test_v137_candidate_pack.py`, which parses §20 against the descriptors). The two
reading-based rows are named in §20 itself. The audit's example (`unaffected_design_scope` "combines multiple
statements") is now an OD-3 token: its meaning combines the two L181 sentences that §20.3 quotes, and its spelling is
owner vocabulary.

**Fixtures that depend on OD-3:** M48, M50, M53, M54, M58. §20.4 rows rest on C9, C12–C14 and OS-1 and are not OD-3, so
M14, M15, M17, M36 and M41 do not depend on OD-3 through them.

**Fit with the current code.** The ledger already produces these values. Phase B splits the M54 input into its own
domain-validation adapter, cites §20, and labels the records OWNER-DECIDED.

### OD-4 — `evaluator_repair_attempt` defined in §7b (D1-6; underlies C15 and OS-1)

**Finding D1-6 (MAJOR).** v1.3.6 allows one recovery cycle and defines the repeated-halt terminations, but never
defines an attempt field:

> [02 L183] "One recovery cycle per affected design is allowed."

> [02 L185] "No second recovery cycle is permitted."

> [41/M13.json L22] "\"evaluator_repair_attempt\": 1"

C15 called the value "the ordinal of the recovery cycle this halt opens". The audit found that the descriptor's field
name did part of the normative work.

**Owner rule (D-027).** "Define evaluator_repair_attempt in §7b (ordinal of the recovery cycle the halt opens; relation
to the one-cycle limit and repeated-halt condition)."

**Pack text (candidate Protocol L185, labelled `OWNER-DECIDED OD-4`; A2 copies it into File 25).** §7b is normative in
§3.4 "Mid-run design halt" (L251 says so), so the definition goes into L185, after "No second recovery cycle is
permitted." It covers the three relations D-027 asks for:
- **The ordinal:** the attempt of a halt is the ordinal of the recovery cycle that halt opens.
- **The one-cycle limit:** a first halt (no cycle used) opens the only permitted cycle and has ordinal `1`, and no
  ordinal above `1` is valid.
- **The repeated-halt condition:** a halt after that cycle is not a second attempt but the `DESIGN_HALT_REPEATED`
  termination.

The sentence also states that the ordinal is not a signature component, consistent with L185's "attempt numbers ... are
not signature components". File 36 L198 (C15) and L205 (OS-1) cite OD-4.

**Relation to `recovery_cycles_used` (M42, M47).** That input counts the cycles used before the second halt. Under
OD-4 it is `1`, the case L185 terminates. OD-4 does not change the M42 and M47 contracts, so they do not depend on it.

**Fixtures that depend on OD-4:** M13 (C15) and M41 (OS-1; M41 also stays labelled OWNER-SPECIFIED, see A-059).

**Fit with the current code.** Both adapters already accept exactly `1`. Phase B changes only the citation and the
label.

### A3 — Invalid supplied halt signatures are outside the executable fixture contract (D1-7; amends C10)

**Finding D1-7 (MAJOR).** C10 made an out-of-domain supplied signature "an evaluator input error" but gave it no
diagnostic, stage, disposition or handling. The audit asked to "specify the invalid-signature outcome, or explicitly
leave such cases outside the executable fixture contract". v1.3.6 states the domains, but nothing about inputs outside
them:

> [02 L185] "Its components have these exact domains: `design_id` is `FIFO` or `UART`;"

**Owner decision (D-027).** "State that invalid supplied signatures are outside the executable fixture contract
(evaluator input error, no ledger record); no new outcome." This is the second option the audit offered. It is not an
OD rule, because it adds no normative behaviour: it states where the contract ends.

**Pack text (candidate Protocol L185; A2 copies it into File 25).** After C10's sentence: "Such an input is outside the
executable fixture contract: it is not an outcome, has no diagnostic, stage, error class or disposition, and produces no
ledger record."

**Fixtures affected:** none executed. No candidate descriptor carries an out-of-domain signature since C10 corrected
M42 and M47. The rule bounds the M41, M42 and M47 input contracts and their boundary vectors.

**Fit with the current code.** The adapters already refuse such an input without a record; the runner reports
NOT_IMPLEMENTED with the reason. Phase B cites A3.

### A4 — M37 relabelled a paired-outcome control vector (D1-8; amends OS-2)

**Finding D1-8 (MINOR).** OS-2 says that `driver_source_excerpt` "is not executed, matched or read for the outcome".
The audit found that the fixture's name and description still suggest that the aliased access is detected in the
response source. The v1.3.6 row:

> [36 L143] "| M37 | missing-case | Aliased global random access leads to paired next-input divergence at runtime | `TERMINAL_INVALID_NO_REPAIR` — `DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE` | `41_F18_Fixture_Inputs/M37.json` |"

**Owner decision (D-027).** "Relabel M37 a paired-outcome control vector, not a test of source-level alias detection."
Not an OD rule: no behaviour changes.

**Pack text (candidate File 36 L143, L206; M37 descriptor).**
- The catalog row and the descriptor's `description` read: "Paired-outcome control vector (OS-2): a supplied paired-run
  outcome with next-input divergence before the first raw-output divergence; the documented aliased global random
  access is not detected from the source".
- The OS-2 item is headed "a paired-outcome control vector, not a test of source-level alias detection". It ends: the
  vector "tests the supplied paired-run outcome and the precedence of the static stages; it does not show that the
  response contains the access its excerpt documents".
- The input, the expected object and the OS-2 rule are unchanged.

**Fixtures affected:** M37 (label only). It stays OWNER-SPECIFIED and depends on no OD rule.

### C17 — Status wording in three parts (D1-9)

**Finding D1-9 (MINOR).** The pack says that every fixture is NOT RUN / NOT PASSED. The bundle also contains a candidate
development run with 143 PASS records. The two can coexist only if the distinction is explicit:

> [36 L3] "All fixtures remain **NOT RUN / NOT PASSED**."

> [32 L21] "- Execution status: **NOT RUN / NOT PASSED** for every fixture."

**Owner decision (D-027).** "Status wording split into development-run evidence / formal F18 status / approval." Not an
OD rule: no behaviour changes.

**Pack text (candidate).** Each current status statement now has three parts:
- **development-run evidence:** fixture runs of a project implementation, recorded outside this pack, are development
  runs and not F18 acceptance;
- **formal F18 status:** NOT RUN / NOT PASSED, since no authorized F18 acceptance run exists;
- **approval:** no implementation is qualified or approved.

The lines changed are File 36 L3 and L176, File 32 L21 and L33, README L16, L35 and L46, and Protocol L559 (§19), which
repeats the fixture status. History is unchanged: the Charter L9 statement about the v1.3.5 audit records what that
audit found. The wording names no run, so the pack does not cite this repository's evidence. It qualifies the D-025
item-3 exception for File 32 (section 6 note).

**Fixtures affected:** none (wording only).

## 12. Correction cycle 3 (owner decision D-029, after document audit #2)

Document audit #2 (GPT-6, an AI model, operated by Krishika, bundle `4ee28f46…5cee`;
`docs/reviews/doc-audit2-gpt6-2026-11-27.md`) found cycle 2 NOT CLEARED on one MINOR finding (D2-1). D1-1 to D1-8 are
resolved, and D1-9 is partly resolved. Krishika decided D-029 on a Claude (claude.ai) triage. Its entries follow E205,
so no earlier CHANGELOG number moves. Every edit stays inside one line. Expected objects are unchanged.

### C18 — Three-part status in every current status statement (D2-1; completes C17 / D1-9)

**Finding D2-1 (MINOR).** File 21 is a current document, and two of its status statements still give only the formal
status:

> [21 L52] "F18 is **NOT RUN / NOT PASSED**."

> [21 L70] "- Current release status: F18 **NOT RUN / NOT PASSED**; A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE REQUIRED**."

**Owner decision (D-029 item 1).** Fix L52 and L70 with the three-part status and keep the A1–A11 and X14 status. Then
sweep the whole candidate, fix every current status statement that lacks the split, and leave historical records alone.
Not an OD rule: no behaviour changes.

**Pack text (candidate).** The three parts use C17's wording: development-run evidence (fixture runs of a project
implementation, recorded outside this pack, are development runs, not F18 acceptance); formal F18 status (NOT RUN / NOT
PASSED, since no authorized F18 acceptance run exists); and approval (no implementation is qualified or approved). The
wording names no run.
- **File 21 L52, L70** (the finding): the full three-part status. L70 keeps "A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE
  REQUIRED**" unchanged.
- **File 21 L7, L40:** the "Status" column headers now say that `NOT RUN` in the column is the formal F18 status and point
  to "F18 result" (L52) for the other two parts. This covers the 24 per-row `NOT RUN` cells without rewriting each.
- **File 21 L26:** "RECORDED; F18 NOT RUN" now carries the three parts in short form.
- **File 21 L69:** "until F18 is actually executed" is a rule, not a status. It now names a formal F18 acceptance run, so
  that development runs cannot be read as setting the sidecar check values.
- **Charter L177** (milestone 5, "F1–F18: not run"): the three parts.
- **Charter L194** (§18): "No parser, assembler, harness or fixture suite has been executed." is an unqualified present
  claim. It now says that the v1.0 response executed none, then gives the current three-part status.
- **File 30 L3:** "Not implemented, frozen or executable until …" now reads "Not frozen, and not executable for F18
  acceptance, until …" and adds the three parts, as C17 did for File 32 L33.
- **File 31 L3:** the three parts are added after the specification's own status.
- **README L19** (File 50): the pinned-runtime Unicode test's formal status, with development runs not counting as that
  check. It is not an F18 line, but it is a current run status.
- **Fixture index L4 and L1931** (`execution_status`, `status`): the same three-part string. The build rebuilds the index
  from v1.3.6, so these two edits are applied in that step. They are logged with C18 and change no descriptor.

**Kept (not current, or not a status).** Charter L9 records what the v1.3.5 audit found (kept under C17). File 32 L11
records the v1.3.4 and v1.3.5 audits, and README L29 records what v1.3.6 changed. Document, audit, freeze and reviewer
statuses (TO FREEZE, NOT AUDITED, DESIGN DRAFT, PENDING) make no run, pass or implementation claim. Charter L178 (F16
pilot "not run") needs LLM calls, and none was made in any run. History files are unchanged, per section 6.

**Full sweep list:** `STATUS-SWEEP-D029.md`. It has 342 lines in 59 files, each with its file, line and class: FIXED 13,
ALREADY THREE-PART (C17) 8, COVERED BY HEADER 24, CURRENT NOT AN F18 STATUS 36, NOT A STATUS STATEMENT 23, HISTORICAL 238.

**Check.** `tests/test_v137_candidate_pack.py` `test_current_status_lines_have_three_parts` fails if a line in a current
document has `NOT RUN`, `NOT PASSED`, `PASSED` or `status` (any case), mentions F18, and lacks any of the three parts. It
also checks the fixture index's two status fields. The three lines it exempts (Charter L9, File 32 L11, File 36 L48, the
P11b "provider truncation status") are listed in the test with their reasons.

**Fixtures affected:** none. Wording only, and the fixture-index status fields change no descriptor hash or expected
object.
