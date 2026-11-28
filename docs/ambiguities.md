# Specification ambiguities and open owner decisions

Each item quotes the source, lists the readings, and says what changes. Items marked
PROVISIONAL are implemented one way so work can continue; the owners must confirm or
change them before any evidence run counts toward F18.

Items marked **DECIDED BY CLAUDE** were decided by Claude under the standing delegation
Krishika gave on 23 Nov 2026 (see CLAUDE.md, "Standing delegation"). Each says "decided by
Claude under standing delegation, owner review pending" and gives the textual reason.
They are implemented, but like PROVISIONAL items they must be reviewed by the owners
(both: the delegation came from Krishika alone) before any evidence run that depends on
them counts toward F18.

**Update, 24 Nov 2026:** A-038 and A-040–A-044 were approved in the owner freeze, and
D-009 (end of this file) approves every other Claude-decided reading, as decided, without
itemised owner review; those items now read "approved under D-009". A-038 and A-040–A-044
keep the wording "owner review pending": the signed freeze covers their exact bytes, so
they are not edited. They are approved.

**Update, D-012:** D-009's approval of A-031 is withdrawn, and A-031 is reversed. The M36 part
of A-012 and the fixture adapters tied to a single input shape are removed; see D-012 at the
end of this file. Entries that still say such a fixture passes are superseded on that point
(their text is bound to approval hashes).

## A-001 — OUTPUT_TRUNCATED versus envelope rejection (DECIDED — Ayush's confirmation pending)

- Protocol §3.4 stage map lists "Envelope, schema or clause manifest rejection" first and
  "Provider finish reason explicitly reports max-token truncation" second, and says "The
  first applicable row after the exact evaluation order below controls".
- The "Deterministic evaluation order" step (1) names "Response UTF-8/JSON/schema/
  manifest-clause checks" and does not mention the finish reason.
- File 30 §1: truncation "is `OUTPUT_TRUNCATED` at `PARSE_SCHEMA` and is reported separately."
- Fixture P11a: finish reason `length` with truncated JSON expects `OUTPUT_TRUNCATED`.

Readings: (a) truncation is checked before envelope decoding — matches P11a;
(b) table row order applies — P11a would give `SCHEMA_REJECT|pointer=/`, contradicting
its expected value. Unspecified either way: finish reason `length` with complete, valid JSON.

Implemented: (a). Also implemented: `length` always yields `OUTPUT_TRUNCATED`, even if the
JSON is complete.

**Decision:** truncation is checked first (reading (a), as implemented). Source: statement typed by Krishika in claude.ai on 23 Nov 2026 at 21:24 IST, naming Krishika and Ayush Kumar Singh. Ayush's own confirmation is pending.

## A-002 — How fixture input shapes are fed to the parser (DECIDED — Ayush's confirmation pending)

The catalog says each descriptor holds "a literal JSON input" but does not define how the
runner turns each input shape into the call under test. 86 fixtures use `response_object`
(an already-decoded JSON object); others use `events`, `null_runs`, `change_class`, etc.

For `response_object`, readings: (a) serialize to UTF-8 JSON bytes and run the full
parser; (b) skip envelope decoding and start at schema validation. For every current
`response_object` fixture both readings should give the same result, because the object
has no duplicate keys and serializes to valid JSON — this is to be confirmed when part 1b
exists.

**Decision:** `response_object` fixtures start at schema validation with the object
as given (reading (b)). Source: statement typed by Krishika in claude.ai on 23 Nov 2026 at 21:24 IST, naming Krishika and Ayush Kumar Singh. Ayush's own confirmation is pending. The decision covers `response_object` only; other input
shapes are listed in A-012.

## A-003 — NaN / Infinity tokens (DECIDED — Ayush's confirmation pending)

File 30 §1 requires one JSON object and rejection of malformed JSON. Python's `json`
module accepts `NaN`, `Infinity` and `-Infinity`, which are not JSON under RFC 8259.
Implemented: rejected as JSON syntax (`SCHEMA_REJECT|pointer=/`). No current fixture
exercises this.

**Decision:** `NaN`/`Infinity` are rejected (as implemented). Source: statement typed by Krishika in claude.ai on 23 Nov 2026 at 21:24 IST, naming Krishika and Ayush Kumar Singh. Ayush's own confirmation is pending.

## D-001 — Pin the Draft 2020-12 validator (PENDING — one owner confirmation outstanding)

Protocol §3.4: "Use the pinned Draft 2020-12 validator". Register 16 L40 lists the parser
version as TO FREEZE. Schema validation (part 1b) needs an exact `jsonschema` version and
its dependencies, pinned with hashes in `requirements.lock`.

**Not fully decided.** Krishika has confirmed `jsonschema==4.26.0`; Ayush Kumar Singh's
confirmation is pending. Resolved with pip-tools 7.7.0 (`pip-compile --generate-hashes`, separate tools venv) on CPython
3.11.18: attrs 26.1.0, jsonschema-specifications 2025.9.1, referencing 0.37.0,
rpds-py 2026.9.1, typing-extensions 4.16.0. Installed into `.venv` with
`pip --require-hashes`. Register 16 L40 still needs this version recorded as frozen.

## A-004 — `UNSPECIFIED` text must identify the missing behavior (DECIDED — Ayush's confirmation pending)

File 30 §1 L9: "`UNSPECIFIED` is permitted only for behavior not specified in the received
packet, and the text must identify the missing behavior."

Readings: (a) not mechanically checkable; the parser accepts any `UNSPECIFIED` whose text
passes the schema (`minLength` 1) and the requirement is reviewed by humans; (b) the parser
must apply some mechanical test, which the pack does not define (no diagnostic, pointer or
rule is given). Fixture P21 ("UNSPECIFIED used with a non-empty description of missing
behavior") expects acceptance at this stage and is consistent with (a).

Implemented: (a) — `UNSPECIFIED` is accepted with no text check. No pointer exists for a
failure under (b).

**Decision:** `UNSPECIFIED` text is accepted at parse time (reading (a), as implemented).
Source: statement typed by Krishika in claude.ai on 23 Nov 2026 at 21:24 IST, naming Krishika and Ayush Kumar Singh. Ayush's own confirmation is pending.

## A-005 — Source of the manifest `clause_ids` for fixtures (DECIDED — Ayush's confirmation pending)

File 30 §1 L9 validates clause IDs "against the exact `clause_ids` array and
`clause_id_regex` in the frozen manifest". No frozen manifest exists yet. Every F18
descriptor has a top-level `manifest_clause_ids` field outside `input`; the catalog does
not say how the runner uses it.

Readings: (a) `manifest_clause_ids` is the frozen-manifest `clause_ids` for that fixture;
(b) the runner should use a frozen manifest file (none exists; File 38 is a template).

Implemented: (a). On `clause_id_regex`: L9's next sentence defines validity completely
("an exact member of that array or the reserved literal `UNSPECIFIED`"), and File 31
L29/L91 applies the regex to each `clause_ids` element at packet freeze. So the response
check is exact membership; the regex is not re-applied to response values (any member
already matches it). If the owners read L9 as requiring a separate regex test on response
values, the outcome is unchanged for every value, because a non-member is rejected
either way.

**Decision:** fixtures use their own `manifest_clause_ids` list (reading (a), as
implemented). Source: statement typed by Krishika in claude.ai on 23 Nov 2026 at 21:24 IST, naming Krishika and Ayush Kumar Singh. Ayush's own confirmation is pending.

## A-006 — Sorting array-index tokens in the schema pointer key (DECIDED — Ayush's confirmation pending)

Protocol §3.4 (file 02 L137): "Sort by: (1) instance-token sequence, Unicode code-point
order, shorter equal prefix first". RFC 6901 tokens are strings, so array index `10` sorts before `2`. The
clause-ID rule, by contrast, says "the lowest numeric `assumptions` index".

Readings: (a) literal — compare every token as a string, so `/assumptions/10/text` is
reported before `/assumptions/2/text`; (b) compare array-index tokens numerically, as in
the clause-ID rule.

Implemented: (a), the literal text (unit test `test_array_index_tokens_compare_as_strings`).
It matters only when schema errors exist at two array indexes with different digit
counts (needs ≥ 11 assumptions or dependencies items). No current fixture exercises it.

**Decision:** the two rules stay as implemented: schema-error pointers sort tokens by
Unicode code point (reading (a)); clause-ID rejection uses the lowest numeric index. Source: statement typed by Krishika in claude.ai on 23 Nov 2026 at 21:24 IST, naming Krishika and Ayush Kumar Singh. Ayush's own confirmation is pending.

## A-007 — SOURCE_AST order across files: per file, or by stage-map row (DECIDED BY CLAUDE — approved under D-009)

- File 30 §3 L27: "For file-local stages, process each source file in this order: strict
  UTF-8 decode with BOM rejection; empty/whitespace-only rejection; `ast.parse`; …"
- Protocol §3.4 evaluation order: "(2) Source UTF-8/BOM/empty/syntax checks in file order
  `driver.py`, then `checker.py`."
- Protocol §3.4 stage map lists "Invalid UTF-8/BOM or syntax parse error" above
  "Empty/whitespace-only source", and says "The first applicable row after the exact
  evaluation order below controls".

Readings: (a) finish all checks on `driver.py`, then `checker.py`; (b) the row order
decides first, so a syntax error in either file beats an empty file. They differ only
when `driver.py` is empty and `checker.py` has a syntax error: (a) gives
`SOURCE_EMPTY|file=driver.py`, (b) gives `SOURCE_SYNTAX_REJECT|file=checker.py|…`.
Within one file, empty and syntax-error cannot both apply (whitespace-only source
parses). No fixture covers the cross-file case; M16 (both empty) agrees with both.

**Decision (decided by Claude under standing delegation, approved under D-009):** reading (a), as implemented (unit test `test_driver_checked_before_checker`). Reason: File 30 §3 L27 is the only text that orders checks *within* a file, and it says to "process each source file in this order", i.e. complete one file before the next; Protocol step (2) also names the file order. The stage-map sentence chooses among rows *after* the evaluation order, so it does not reorder the per-file sequence.

## A-008 — U+FEFF at the start of a source string (DECIDED BY CLAUDE — approved under D-009)

Stage map: "Invalid UTF-8/BOM or syntax parse error" → `SOURCE_SYNTAX_REJECT`; File 30 §3
L27: "strict UTF-8 decode with BOM rejection". The source arrives as a JSON string, not
bytes, so "BOM" has no byte meaning here.

Readings: (a) a leading U+FEFF is the BOM and is rejected before the empty check — but
the pack gives no line/column for a BOM rejection; (b) U+FEFF is an ordinary character
and `ast.parse` decides (on 3.11.18 it raises SyntaxError "invalid non-printable
character U+FEFF", line 1, offset 1, so `…|line=1|column=1`); (c) strip it as Python
does when reading a UTF-8-SIG file — excluded by "BOM rejection". (a) and (b) both
reject; they can differ only in the line/column, which the pack does not give for (a).
**Decision (decided by Claude under standing delegation, approved under D-009):** a leading U+FEFF is rejected as the BOM, before the empty check: `SOURCE_SYNTAX_REJECT|file=<FILE>|line=1|column=1`. Reason: File 30 §3 L27 requires "BOM rejection" as part of the first step, and File 30 §1 forbids silently normalizing source code, which excludes (c). Readings (a) and (b) both reject; the only open point was the position, and a BOM is at line 1, column 1 by any count, which is also what `ast.parse` reports under (b). U+FEFF later in the source is still left to `ast.parse`. Unit test `test_claude_decided_cases`.

## A-009 — Source string that is not valid UTF-8 (DECIDED BY CLAUDE — approved under D-009)

JSON `\ud800` escapes decode to lone surrogates, which cannot be encoded as UTF-8.
`ast.parse` on 3.11.18 raises `UnicodeEncodeError`, not SyntaxError. The stage map
puts this under "Invalid UTF-8 …" → `SOURCE_SYNTAX_REJECT|file=<FILE>|line=<LINE>|
column=<COLUMN>` but says nothing about the line or column. (Raw input of this kind
also passes PARSE_SCHEMA: Python's `json` accepts lone-surrogate escapes.)
**Decision (decided by Claude under standing delegation, approved under D-009):** `SOURCE_SYNTAX_REJECT|file=<FILE>|line=1|column=1`. Reason: the stage map assigns invalid UTF-8 to `SOURCE_SYNTAX_REJECT` at SOURCE_AST, so it is not moved to PARSE_SCHEMA (the response bytes themselves are valid UTF-8; File 30 §1's "Reject invalid UTF-8" applies to them). CPython reports no position for this failure, and the only position rule the pack gives for a missing position is the column rule's "absent … emit `column=1`"; line 1 is the same fallback (A-011). Competing reading not taken: report the line/column of the first lone surrogate — more informative, but no text defines it, and it is not "reported by CPython".

## A-010 — Which characters count as whitespace for SOURCE_EMPTY (DECIDED BY CLAUDE — approved under D-009)

Stage map: "Empty/whitespace-only source". The pack does not define whitespace.
Readings: (a) JSON whitespace (space, tab, LF, CR); (b) `str.isspace()`, which adds
U+000B, U+000C, U+001C–U+001F, U+0085, U+00A0, U+1680, U+2000–U+200A, U+2028, U+2029,
U+202F, U+205F, U+3000; (c) Python tokenizer whitespace (space, tab, form feed, newlines).
What changes: a source of only U+000C parses on 3.11.18 (empty module, so it passes
SOURCE_AST under (a)), but is SOURCE_EMPTY under (b) and (c); U+000B or U+00A0 alone is
`SOURCE_SYNTAX_REJECT|…|line=1|column=1` under (a)/(c) but SOURCE_EMPTY under (b).

**Decision (decided by Claude under standing delegation, approved under D-009):** reading (c), Python source whitespace: space, tab, form feed, CR and LF (Python Language Reference 2.1.2 line terminators and 2.1.9 whitespace between tokens). A source made only of these is SOURCE_EMPTY; any other character, including U+000B, U+00A0 and U+3000, goes to `ast.parse` (on 3.11.18 those give `SOURCE_SYNTAX_REJECT`). Reason: the check is on Python source, inside a stage whose authority on source is CPython 3.11; JSON whitespace (a) belongs to the response envelope, and `str.isspace()` (b) would call "empty" sources that Python itself rejects as invalid characters. A comment-only source is still not empty. Unit test `test_claude_decided_cases`.

## A-011 — SyntaxError with no usable line, or another exception from ast.parse (DECIDED BY CLAUDE — approved under D-009)

The column rule covers a missing offset ("If `offset` is absent, null or less than 1,
emit `column=1`") but nothing covers a missing or non-positive `lineno`, although
`LINE` must be a positive decimal integer. On 3.11.18, a NUL character in the source
gives SyntaxError "source code string cannot contain null bytes" with `lineno=None`.
`ast.parse` may also raise exceptions that are not SyntaxError (e.g. `RecursionError`,
`MemoryError`, `UnicodeEncodeError` — see A-009); the stage map does not say whether
these are "syntax parse error". **Decision (decided by Claude under standing delegation, approved under D-009):** a SyntaxError whose `lineno` is missing or less than 1 uses `line=1`, and its column follows the column rule as usual; any other exception from `ast.parse` (e.g. `MemoryError`, which 3.11.18 raises for very deep nesting such as 200,000 unary minus signs) is a syntax parse error with `line=1|column=1`. Reason: `LINE` must be a positive integer and the pack's only rule for a missing position is "If `offset` is absent, null or less than 1, emit `column=1`"; line 1 applies the same fallback. "Syntax parse error" in the stage map is read as "`ast.parse` did not produce a tree". Competing reading not taken for NUL bytes: report the line of the first NUL — not given by CPython or the text. Unit tests `test_claude_decided_cases`, `test_non_syntax_error_from_parse_is_line_1_column_1`.

Related observation (no change): the column rule says to emit "the positive one-based
source-character column reported by CPython". On 3.11.18 `ast.parse` of a `str` reports
a character offset (`é = 1; y = )` gives offset 12, the character column, not 13, the
byte column — unit test `test_column_counts_characters_not_utf8_bytes`). Warnings from
`ast.parse` (e.g. invalid escape sequences) are not failures; the runner must not be
started with `-W error`, which would turn them into SyntaxError.

## A-012 — Runner adapters for source-pair inputs and the M36 unit vector (DECIDED BY CLAUDE — approved under D-009)

A-002's decision covers `response_object` only. Two more input shapes reach SOURCE_AST.

**`{driver_source, checker_source}` (M16, M29) — PROVISIONAL.** Implemented: run
**Decision (decided by Claude under standing delegation, approved under D-009):** SOURCE_AST directly on the two strings (no envelope, schema or clause-ID step), then
continue with later stages. Alternative: wrap them in a full response object first —
the pack gives no wrapper, so this would need one.

**Decision on the source pair (decided by Claude under standing delegation, approved under D-009):** as implemented. Reason: the pack defines no wrapper, and inventing one would add text the pack does not contain; the input holds exactly the two strings that Protocol step (2) begins with.

**`{source_file, syntax_error: {lineno, offset}}` with `fixture_class:
"parser_unit_vector"` (M36) — OPEN; M36 is NOT_IMPLEMENTED.**

What the pack says (exact text):
- `fixture_class` value `parser_unit_vector`: **not defined anywhere in the pack.** The
  string occurs only in `41_F18_Fixture_Inputs/M36.json`. The only text about
  `fixture_class` is Catalog (file 36) requirement 6: "Serializer unit vectors and
  lifecycle unit vectors are marked by `fixture_class` and are deliberately
  grammar-exempt; they test local utilities/policies, not model feedback." It names
  serializer and lifecycle unit vectors, not parser unit vectors.
- `CONTROL_EXPECTATION`, Catalog (file 36) dispositions list: "`CONTROL_EXPECTATION`: a
  serializer, lifecycle or policy test vector; it does not represent an artifact feedback
  event."
- `CONTROL_EXPECTATION`, Protocol (file 02 L177): "A `CONTROL_EXPECTATION` fixture
  exercises a serializer, protocol or lifecycle rule; its stage and expected diagnostic
  are test labels, not an artifact feedback event."
- The column rule itself (file 02 L127) is fully defined: "If `offset` is absent, null or
  less than 1, emit `column=1`".

Finding: neither definition names a parser vector, and no rule maps an input to the
`CONTROL_EXPECTATION` disposition. The earlier runner (commit e5eb9c0, run
run-20261123T155910Z) set `record["disposition"] = "CONTROL_EXPECTATION"` as a constant
whenever `fixture_class == "parser_unit_vector"`. That label occurs only in M36, so the
disposition was in effect copied from the descriptor, not computed. That PASS is
withdrawn: the runner now reports M36 NOT_IMPLEMENTED. The column rule is still covered
by unit tests (`ColumnRuleTests`, hand-built inputs, not F18 evidence).

Readings for the owners: (a) unit vectors of any class have disposition
`CONTROL_EXPECTATION` (would need a rule saying so, and a definition of
`parser_unit_vector`); (b) for unit vectors the runner compares stage, error class and
diagnostic only, and records the disposition label without comparing it (would change
Catalog requirement 2's "single exact expected disposition/stage/error/diagnostic");
**Decision (decided by Claude under standing delegation, approved under D-009):** (c) the pack is corrected so M36's class and disposition are defined.

**Decision on M36 (decided by Claude under standing delegation, approved under D-009):** an input of shape `{source_file, syntax_error: {lineno, offset}}` applies the column rule (`syntax_reject`) and has disposition `CONTROL_EXPECTATION`. Reason: such an input is a SyntaxError position, not a model response, so it is not an artifact feedback event; it exercises a protocol rule (Protocol §3.4 column rule) directly, and Protocol L177 defines `CONTROL_EXPECTATION` as a fixture that "exercises a serializer, protocol or lifecycle rule". This is a variant of (a) that rests on L177's "protocol" rather than on a definition of `parser_unit_vector`. The rule is keyed on the input shape, never on `fixture_class`: checked against the pack, `fixture_class` does not determine disposition (two `lifecycle_unit_vector` descriptors are not `CONTROL_EXPECTATION`, and `f18_packet_fixture` descriptors are `F18_REJECT`), so a rule keyed on the class label would contradict the pack. The adapter accepts only `driver.py`/`checker.py`, a positive integer `lineno` and an integer-or-null `offset`; anything else is NOT_IMPLEMENTED. **Effect:** M36 moves from NOT_IMPLEMENTED to PASS. This is the one decision in this batch that changes a fixture result, so it should be the first one the owners review. Reading (c) remains open to the owners as a pack correction.

## A-013 — Order of IMPORT_POLICY categories within one file (DECIDED — Ayush's confirmation pending; tie case DECIDED BY CLAUDE — approved under D-009)

- File 30 §3 L27 (per-file stage list): "`ast.parse`; module-level AST policy;
  import/prohibited-name policy; compilation; …"
- File 30 §3 L27 (node order): "within a file, source nodes use ascending `(lineno,
  col_offset, end_lineno, end_col_offset)`."
- Protocol §3.4 evaluation order (3): "If the identifier scan passes, complete that
  file's import, prohibited-name and module-body checks before advancing to the next
  file. AST import nodes use ascending source-position order and the per-node import
  precedence above."
- Protocol §3.4 (file 02 L129): "Nodes are visited by `(lineno, col_offset, end_lineno,
  end_col_offset)` within `driver.py`, then `checker.py`."

The identifier scan runs first (settled by step (3)) and files run `driver.py` first
(settled). Not settled: which of the remaining categories wins inside one file.

Readings:
- (a) Module-body policy first, then import and prohibited-name checks — the order of
  File 30 L27's stage list.
- (b) Imports, then prohibited names, then module-body — the order of Protocol step (3)'s
  sentence.
- (c) One source-order pass: every IMPORT_POLICY violation in the file is placed by its
  node's `(lineno, col_offset, end_lineno, end_col_offset)` and the first wins, whatever
  its category — File 30 L27's node-order sentence.

What changes (driver.py examples):

| Source | (a) | (b) | (c) |
|---|---|---|---|
| `import os` (L1); `print(1)` (L2) | `MODULE_STATEMENT_REJECT\|…\|line=2\|reason=MODULE_EXECUTABLE` | `IMPORT_NOT_ALLOWED\|module=os` | `IMPORT_NOT_ALLOWED\|module=os` |
| `print(1)` (L1); `import os` (L2) | `MODULE_EXECUTABLE`, line 1 | `IMPORT_NOT_ALLOWED\|module=os` | `MODULE_EXECUTABLE`, line 1 |
| function using `eval` (L3); `X = [n for n in ()]` (L9) | `NON_LITERAL_CONSTANT`, line 9 | `PROHIBITED_BUILTIN\|name=eval` | `PROHIBITED_BUILTIN\|name=eval` |

Detail under (c): a module-level `eval("1")` is an `Expr` node and a `Name` node with
the same start `(1, 0)`; the `Name` ends first, so the key puts it first and gives
`PROHIBITED_BUILTIN`, not `MODULE_EXECUTABLE`. A module-level `x = eval("1")` starts with
the `Assign` at `(1, 0)` and gives `NON_LITERAL_CONSTANT`.

No current fixture distinguishes the readings: every IMPORT_POLICY fixture has one
violation.

**Decision:** reading (c) — one source-order pass; the first violation of any
IMPORT_POLICY category wins. Source: statement typed by Krishika in Claude Code on 23 Nov 2026: "I, Krishika, decide A-013 and A-014 as reading (c): single source-order pass, first violation wins. Ayush's confirmation is pending."
Reading (c) was suggested by Claude (claude.ai session) and relayed by Krishika.

Residual gap under (c), found when building step 7: two different findings can share
the smallest key. A bare module-level `eval` or `random.seed` statement is an `Expr`
node and a `Name`/`Attribute` node with identical spans (CPython 3.11.18:
`(1, 0, 1, 4)` for both), so "first violation wins" does not choose between
`MODULE_EXECUTABLE` and `PROHIBITED_BUILTIN`/`GLOBAL_RANDOM_USE`. Implemented: such a
**Decision (decided by Claude under standing delegation, approved under D-009):** tie raised `UnsettledSpec("A-013")`. No current fixture has a tie.

**Decision on the tie (decided by Claude under standing delegation, approved under D-009):** equal keys are ordered by File 30 §3 L27's stage list — "module-level AST policy; import/prohibited-name policy" — so a module-body finding wins, then an import finding, then a prohibited name, then `random` use (File 30 §2 L20 follows L19). A bare module-level `eval`, `random.seed` or `builtins.open` statement is therefore `MODULE_STATEMENT_REJECT|…|reason=MODULE_EXECUTABLE`. Reason: L27's list is the only text that ranks the categories, and the node-order sentence that reading (c) applies is exhausted by the tie. Pre-order traversal (the statement before its child) gives the same answer. Unit test `test_equal_key_tie_uses_file30_stage_order`.

## A-014 — Order between PROHIBITED_BUILTIN and GLOBAL_RANDOM_USE (DECIDED — Ayush's confirmation pending)

- File 30 §2 L19 (prohibited names) and L20 (`random`) are separate bullets; Protocol
  §3.4 (file 02 L133): "Reject AST `Name` nodes whose `id` is `__import__`, `eval`,
  `exec`, `compile` or `open`, and reject access through `builtins.<name>` for those
  same names. … direct `random.<attribute>` use other than `random.Random` emits
  `GLOBAL_RANDOM_USE`."
- Neither diagnostic carries a file or line (`PROHIBITED_BUILTIN|name=<NAME>`,
  `GLOBAL_RANDOM_USE|name=<NAME>`), so the order decides which name is reported.

Readings: (a) all prohibited-name violations before any random violation (the order in
which the text lists them); (b) one source-order pass over both kinds, separate from
imports and module-body; (c) the single source-order pass of A-013 (c). Example (one
function body): `v = random.random()` (L5); `exec("x")` (L6) — (a) gives
`PROHIBITED_BUILTIN|name=exec`; (b) and (c) give `GLOBAL_RANDOM_USE|name=random.random`.
No current fixture has both.

**Decision:** reading (c), the single source-order pass of A-013. Source: statement typed by Krishika in Claude Code on 23 Nov 2026: "I, Krishika, decide A-013 and A-014 as reading (c): single source-order pass, first violation wins. Ayush's confirmation is pending."

## A-015 — Module-body statements the text does not classify (DECIDED BY CLAUDE — approved under D-009; case 2 REVISED BY OWNER — Ayush's confirmation pending)

Protocol §3.4 (file 02 L135): "At module scope, allow only permitted imports, one
optional docstring expression, … and assignments/annotated assignments whose values are
recursively literal-only. A non-literal assignment is `NON_LITERAL_CONSTANT`;
module-level control-flow statements (…) are `MODULE_CONTROL_FLOW`; other executable
statements/calls/expressions are `MODULE_EXECUTABLE`." File 30 §3 L29: "Literal-only
expressions are `ast.Constant` values of type string, bytes, integer, float, complex,
boolean or `None`, and recursively nested tuple/list/set/dict literals containing only
those values; unary plus/minus applied to a numeric literal is permitted."

Unsettled cases (each needs: accept, `NON_LITERAL_CONSTANT` or `MODULE_EXECUTABLE`):
1. `x += 1` — `ast.AugAssign` is not "assignment/annotated assignment" by name.
2. `a.b = 1`, `a[0] = 1` — literal value, but the target is not a plain name.
3. `x: int` — `ast.AnnAssign` with no value: nothing to test for literal-only.
4. `pass` — not executable in effect, but not in the allowed list.
5. A string expression that is not the first statement, or a second one — is "one
   optional docstring expression" only the first statement?
6. `X = ...` — `Ellipsis` is an `ast.Constant` but not one of the listed types.
7. `X = -True` — `bool` is an `int` subclass: is it a "numeric literal"?
8. `X = -(-1)`, `X = +-1` — unary applied to a unary, not directly to a literal.
9. The annotation of an annotated assignment (`X: foo() = 1`): the text tests "values"
   only. Implemented boundary: an annotation made only of names, attributes,
   subscripts, constants, tuples/lists and `|` (e.g. `int`, `dict[str, int] | None`)
   is not examined; any other annotation node (a call, arithmetic, …) is case 9.
10. `global x` / `nonlocal x` at module scope (both pass `ast.parse` on 3.11.18) — no
    effect, like `pass`.
11. `return`, `break`, `continue` at module scope (all pass `ast.parse` on 3.11.18;
    `compile()` would reject them) — control transfer, but not in the
    `MODULE_CONTROL_FLOW` list (`if`, `for`, `while`, `with`, `try`, `match`, `async`).

Before the decision (step 6, `classify_module_body`), each of these cases was returned as an
`UnsettledSpec("A-015")` finding at its source position, not raised at once, so a
settled violation earlier in the file can still win once A-013 is decided. A value with
a non-literal part is `NON_LITERAL_CONSTANT` even if it also has an unsettled part
(e.g. `(..., f())`), because every reading rejects it with that reason.

Treated as settled by the text (no entry needed unless the owners disagree): `del`,
`assert`, `raise` → `MODULE_EXECUTABLE` ("other executable statements"); any
expression statement that is not the first-statement string docstring, including
`await`, `yield`, a bytes or f-string first statement → `MODULE_EXECUTABLE` (File 30
§3 L29: "expressions other than a docstring … are rejected"); `async for`, `async with`
→ `MODULE_CONTROL_FLOW` ("`async` control flow"); `try`/`except*` (`ast.TryStar`) →
`MODULE_CONTROL_FLOW` (`try`); tuple/list/starred unpacking targets made only of names
count as assignments.

**Decision (decided by Claude under standing delegation, approved under D-009):** No current fixture uses any unsettled case (P28, M04a, M04b and M57 do not).

**Decision (decided by Claude under standing delegation, approved under D-009):** Reasons, from L135/L29: the allowed list ("allow only …") is exhaustive; `MODULE_CONTROL_FLOW` covers only the statements it names; "assignments/annotated assignments" are read as `ast.Assign`/`ast.AnnAssign` (the section names AST node types throughout); the literal test is on "values"; and "calls" are named as `MODULE_EXECUTABLE`.

| Case | Outcome |
|---|---|
| 1 `x += 1` | `MODULE_EXECUTABLE` (an augmented assignment is its own statement kind, not in the list) |
| 2 `a.b = 1`, `a[0] = 1` | **revised by owner, see below:** `MODULE_EXECUTABLE` whatever the value. (First decision, superseded: accepted if the value is literal-only.) |
| 3 `x: int` | accepted (no value to fail) |
| 4 `pass` | `MODULE_EXECUTABLE` |
| 5 later string expression | `MODULE_EXECUTABLE` (a docstring is the first statement) |
| 6 `X = ...` | `NON_LITERAL_CONSTANT` (Ellipsis is not in L29's exhaustive type list) |
| 7 `X = -True` | `NON_LITERAL_CONSTANT` (L29 lists boolean separately from the numeric types) |
| 8 `X = -(-1)`, `+-1` | `NON_LITERAL_CONSTANT` (unary applied to a unary, not to a numeric literal) |
| 9 annotation | not tested for literalness; `MODULE_EXECUTABLE` if it contains a call (e.g. `X: foo() = 1`) |
| 10 `global`/`nonlocal` | `MODULE_EXECUTABLE` |
| 11 `return`/`break`/`continue` | `MODULE_EXECUTABLE` (not in the `MODULE_CONTROL_FLOW` list) |
| any other statement type | `MODULE_EXECUTABLE` (none remain on 3.11) |

Competing reading not taken for case 9: reject every non-type annotation as `MODULE_EXECUTABLE`, since it evaluates code at import time. The text tests values only, so only the explicitly named "calls" are rejected. Unit tests `test_a015_decided_cases`, `test_a015_cases_take_part_in_source_order`.

**Case 2 revised — owner decision by Krishika, 23 Nov 2026 (Ayush's confirmation pending).** Claude's first decision (accept an attribute/subscript target when the value is literal-only, rejecting only a call in the target) is **superseded**. Krishika's instruction: "an assignment whose target is not a plain Name (e.g. a.b = 1, math.pi = 3, d[0] = 1) is not a module constant and is a side effect. Reject as MODULE_STATEMENT_REJECT reason MODULE_EXECUTABLE."

Why the first decision was wrong: it read only L135/L29's literal test, which is on values, and missed the wording on what module-level assignments are *for*. Texts cited (verified in the baseline):
- File 30 L52 (driver) and L64 (checker): the file may contain "literal-only module constants"; "Module-level executable statements, control flow, calls, comprehensions, non-literal assignments and side effects are prohibited." The same wording is in the model-visible prompt template, file 19 L25 and L40.
- File 30 L29: "Names, calls, comprehensions, f-strings, attribute access, binary operations and other expressions are not literal-only. Module-level executable statements, … non-literal assignments and other side effects are rejected."

Assigning to an attribute or subscript changes another object instead of defining a constant, so it is a side effect.

Implemented rule: an `ast.Assign` or `ast.AnnAssign` is `MODULE_STATEMENT_REJECT|file=<FILE>|line=<LINE>|reason=MODULE_EXECUTABLE` if any target is not a plain name. Plain names include names unpacked in tuples/lists and starred names, so `a, *b = 1, 2` is still allowed. The rule therefore covers `a, b.c = 1, 2`, `[a, *b[0]] = …`, `X = a.b = 1` and `d[0]: int` (no value).

Detail decided by Claude under the delegation: the target check comes before the value check, so `a.b = f()` is `MODULE_EXECUTABLE`, not `NON_LITERAL_CONSTANT`. Reason: under the owner's rule such a statement is not a module constant at all, so the constant-specific reason does not apply.

Unit tests `test_a015_decided_cases`, `test_attribute_target_is_executable_in_stage`. No current fixture has an attribute or subscript target, so no fixture result changes.

## A-016 — Prohibited-name rule: definitions, parameters and `builtins` (DECIDED BY CLAUDE — approved under D-009)

File 30 §2 L19: "AST `Name` nodes whose `id` is `__import__`, `eval`, `exec`, `compile`
or `open` are rejected, regardless of call context. A `builtins` attribute whose
attribute is one of those names is also rejected. `builtins` itself is not an allowed
import root."

Unsettled: (1) `def open(): …` or `def f(eval): …` binds the name through `ast.FunctionDef.name`
or `ast.arg`, not an `ast.Name` node — rejected or not? Function definitions are
otherwise deferred to AST_SIGNATURE. (2) `import builtins` followed by `builtins.open`:
`IMPORT_NOT_ALLOWED|module=builtins` or `PROHIBITED_BUILTIN|name=open` (same as A-013).
(3) "A `builtins` attribute" — is it only `Attribute(value=Name("builtins"))`, or also
e.g. `__builtins__.open`? M24 (`builtins.open` with no import) expects
`PROHIBITED_BUILTIN|name=open`, consistent with the first form. **Decision (decided by Claude under standing delegation, approved under D-009):** the planned implementation: `ast.Name` nodes in any context, and `Attribute(value=Name(id="builtins"))` only; (1) and `__builtins__` are not flagged; (2) is settled by A-013 reading (c) (the import comes first in source order, so `IMPORT_NOT_ALLOWED|module=builtins`). Reasons: the text says "AST `Name` nodes" and "`builtins.<name>`"; File 30 §3 says IMPORT_POLICY "never rejects or classifies a function/class definition", which excludes flagging `def open`; parameter names are `ast.arg`, not `ast.Name`.

## A-017 — `random.<attribute>` when `random` is not the imported module (DECIDED BY CLAUDE — approved under D-009)

File 30 §2 L20: "Any direct attribute access on the module name `random` other than
`random.Random` is rejected". Protocol §3.4 (file 02 L133): "direct `random.<attribute>`
use other than `random.Random` emits `GLOBAL_RANDOM_USE`."

Unsettled: whether the check is purely syntactic (`Attribute(value=Name(id="random"))`
anywhere) or applies only when `random` is the imported module — e.g. a parameter named
`random`, or a file without `import random`. **Decision (decided by Claude under standing delegation, approved under D-009):** M09, M22, M23 all `import random` and use
it inside a method, so both readings pass them. Syntactic, as planned. Reason: the text says "the module name `random`" and "direct `random.<attribute>`", and calls the check static, saying outright that aliasing and `getattr` are not detected; binding analysis would go beyond what it describes.

## A-018 — Non-ASCII identifiers inside f-string replacement fields (DECIDED BY CLAUDE — approved under D-009)

File 30 §2 L21: "Every Python identifier lexeme must be ASCII. … Unicode in STRING and
COMMENT tokens is permitted." Protocol §3.4 (file 02 L133): "STRING and COMMENT tokens
are not scanned".

Question: in `f"{café}"` the identifier `café` is a real `ast.Name` node, but before
Python 3.12 (PEP 701) the whole f-string is one STRING token.

Probe result (CPython 3.11.18, pinned interpreter, step 1): `ast.parse('x = f"{café}"')`
contains `Name(id="café")`, and `tokenize` emits `NAME 'x'` then `STRING 'f"{café}"'`;
the same holds for `f"{a℘}"`. So, as the rule is written, a non-ASCII identifier inside
an f-string replacement field is **not rejected**. **This is CPython 3.11-specific:**
from 3.12, f-strings are tokenized into parts (PEP 701) and the identifier would be a
`NAME` token. Unit test `test_fstring_identifier_not_scanned_on_311` records the
behaviour.

Readings: (a) literal text — the scan covers tokens only, so f-string identifiers pass;
(b) "Every Python identifier lexeme must be ASCII" governs, so the scan must also check
`ast.Name`/`ast.Attribute` nodes inside `ast.JoinedStr` (the text gives no column rule
for that). **Decision (decided by Claude under standing delegation, approved under D-009):** No current fixture uses an f-string with a non-ASCII identifier.
Reading (a), as implemented. Reason: the operative rule is a token procedure pinned to CPython 3.11 ("scan `tokenize.NAME` and identifier-relevant `tokenize.ERRORTOKEN` tokens", "STRING and COMMENT tokens are not scanned"), and (b) would need a column rule the text does not give. The 3.11-specific gap should be disclosed alongside the alias limitation in File 30 §2 L20.

## A-019 — Line breaks for the identifier scan: lone CR (DECIDED BY CLAUDE — approved under D-009)

File 30 §2 L21 / Protocol §3.4 (file 02 L133): the column is computed "from the UTF-8
byte length of the source-line prefix"; the pack does not define a source line. Probe
on CPython 3.11.18: for `"x = 1\ry = 2\n"`, `ast.parse` puts `y = 2` on line 2, but
`tokenize.generate_tokens` over the same string treats the lone CR as an `ERRORTOKEN`
and reports `y` on line 1. A non-ASCII identifier after a lone CR would therefore get a
line number that disagrees with the AST. CRLF is consistent in both. **Decision (decided by Claude under standing delegation, approved under D-009):** Formerly a lone CR raised `UnsettledSpec("A-019")`. No current fixture contains a lone CR.

**Decision (decided by Claude under standing delegation, approved under D-009):** a source line is a Python physical line, ended by LF, CRLF or a lone CR (Language Reference 2.1.2), which is how `ast.parse` counts lines on 3.11.18. The scanner tokenizes a copy in which each lone CR is replaced by LF; one character replaces one at a line end, so every line prefix and every UTF-8 byte column is unchanged. The source itself is not changed. Reason: the diagnostic's `line` must agree with the AST the rest of the stage uses, and CPython's own compiler translates a lone CR to a newline (so a raw CR inside a quoted string is already a syntax error at SOURCE_AST). Unit test `test_lone_cr_ends_a_line_as_for_ast_parse`.

## A-020 — What PARAMETER_NAMES, PARAMETER_KIND and DEFAULT_OR_VARIADIC each cover (DECIDED BY CLAUDE — approved under D-009)

Protocol §3.4 (file 02 L164): "exactly one binding of the required kind proceeds to
parameter checks in the order `PARAMETER_NAMES`, `PARAMETER_KIND`, then
`DEFAULT_OR_VARIADIC`." File 30 §3 L33: "parameter checks in the order names, kinds,
then defaults/variadic/keyword-only shape." File 30 §3 L35/L37 give the required lists:
`create_driver(seed)`, `Driver.step(self, cycle_index, outputs_after_edge)`,
`check_trace(trace, metadata)`, each "required positional-or-keyword … not
positional-only … no default, variadic, keyword-only or extra parameters".

The text does not say which parameters the names check compares. Readings: (a) the
positional parameters only (positional-only then positional-or-keyword); (b) every
named parameter, including keyword-only and variadic names. Example: `def
create_driver(seed, *args)` is `DEFAULT_OR_VARIADIC` under (a) but `PARAMETER_NAMES`
under (b); `def create_driver(*, seed)` is `PARAMETER_NAMES` under (a) but
`PARAMETER_KIND` under (b).

**Decision (decided by Claude under standing delegation, approved under D-009):** (a).
- The names check compares the positional parameter names, in order, with the required
  list.
- The kind check rejects any positional-only parameter.
- `DEFAULT_OR_VARIADIC` rejects any default, `*args`, keyword-only parameter or
  `**kwargs`.
- Annotations are ignored.

Reason: File 30 groups "keyword-only" with defaults and variadics in the *third*
check. Under (b), a keyword-only or variadic parameter would already fail the names
check, which would leave the third check almost unreachable. "Extra" positional
parameters are a names mismatch under both readings. Unit tests `ParameterTests`.

## A-021 — What counts as a "binding" in the required-symbol pass (DECIDED BY CLAUDE — approved under D-009)

Protocol §3.4 (file 02 L164): "count all same-name binding definitions at the required
scope … more than one binding of any AST kind emits `EXTRA_ENTRY_POINT`; exactly one
binding with the wrong AST kind emits `WRONG_ENTRY_POINT_KIND`". The text does not list
which AST kinds bind.

**Decision (decided by Claude under standing delegation, approved under D-009):** a
binding is a statement in the scope's own body (module body, or `Driver`'s class body
for `step`) that is:
- a `def`, `async def` or `class` with that name;
- an assignment, or an annotated assignment *with a value*, whose target binds that
  name (unpacking included);
- an import whose bound name is that name.

An annotated name without a value (`create_driver: int`) is not counted, because Python
creates no binding for it. Definitions nested inside functions are not at the required
scope.

Reason: "binding" is Python's own term (Language Reference 4.2.1), and these are the
statements that bind a name in a module or class scope after IMPORT_POLICY. Other
binding forms (`for`, `with`, `global` from a function) cannot appear at module scope
by then. Unit tests `test_any_binding_kind_counts_as_extra`,
`test_annotation_without_value_is_not_a_binding`.

## A-022 — `Driver` class-body statements other than methods and nested classes (DECIDED BY CLAUDE — approved under D-009)

File 30 §3 L35: "Its body may contain one docstring, literal-only class constants and
exactly one synchronous undecorated instance method named `step`". IMPORT_POLICY checks
module-body statements only. The seven AST_SIGNATURE category ranks cover methods
(rank 3), nested classes (rank 1), bases and metaclass (rank 4), decorators, async
definitions and comprehensions. None of them names a class-body statement such as
`X = f()`, `pass` or `if …:` inside `Driver`.

Readings: (a) not checked statically; later stages (restricted import) see its effects;
(b) `DRIVER_CLASS_FORM`, the only reason about the `Driver` class's form, at rank 4;
(c) a new reason — excluded, because "No unlisted value is permitted" (file 02 L125).

**Decision (decided by Claude under standing delegation, approved under D-009):** (b).
Any `Driver` class-body statement other than these is `DRIVER_CLASS_FORM` at rank 4,
`symbol=Driver`, positioned at the statement:
- a method or nested class (handled by the other ranks);
- a first-statement string docstring;
- an assignment or annotated assignment with a plain-name target and a literal-only value
  (or no value).

Class constants use the module-constant rules, including the owner's A-015 case 2 rule
(plain-name targets only). Reason: the stage map assigns "class/method/nesting violation" to
AST_SIGNATURE, and B5 (file 19 L25, file 30 L52) states the class-body allowance to
the model, so (a) would leave a stated rule unenforced. Unit test
`test_driver_body_statements`. No current fixture has such a statement.

## A-023 — Source position of definition violations in the global pass (DECIDED BY CLAUDE — approved under D-009)

The global sort key is `(category, file_order, lineno, col_offset, end_lineno,
end_col_offset)`. The text gives the node only for rank 7 ("the expression node's own
source position").

**Decision (decided by Claude under standing delegation, approved under D-009):**
- Ranks 1–3, 5 and 6 use the offending `ClassDef`/`FunctionDef`/`AsyncFunctionDef`
  node's own position (on CPython 3.11 a decorated definition starts at its `def` or
  `class` line, not at the decorator).
- Rank 4 uses the `Driver` `ClassDef`, or the class-body statement for A-022.

Reason: the violation is a property of the definition node, which is how the text
names it ("any nested class", "any decorator on any function, class or method").
Only ties between two violations of the same category in the same file depend on this.

## A-024 — Compile errors without a line number (DECIDED BY CLAUDE — approved under D-009)

Stage map: `COMPILE_ERROR|file=<FILE>|line=<LINE>`, and `LINE` must be positive. The
pack does not say what to do if `compile()` raises a SyntaxError with no line, or
another exception.

**Decision (decided by Claude under standing delegation, approved under D-009):** use
line 1, as A-011 does for SOURCE_AST; any other exception from `compile()` is a compile
error at line 1. Reason: same as A-011. Sources reaching compilation have already parsed,
so this is a defensive rule; no known 3.11.18 input reaches it.

## A-025 — The `events` input vocabulary and multi-failure precedence (DECIDED BY CLAUDE — approved under D-009)

R01–R06, R12 and R13 give a list of observed `events` (`{"kind": …, …}`). The pack
defines neither the event vocabulary nor how several events are ranked, beyond the
evaluation order (Protocol §3.4 L166) and "The first applicable row after the exact
evaluation order below controls" (L139).

**Decision (decided by Claude under standing delegation, approved under D-009):**
- Each event kind names one stage-map row, and its fields fill that row's diagnostic
  template. The table is `EVENT_ROWS` in `src/openvef/stage_map.py`: `schema_reject`,
  `output_truncated`, `import_not_allowed`, `compile_error`, `driver_runtime`,
  `driver_vector`, `driver_watchdog`, `simulator_error`, `trace_integrity`.
- Fields are checked against the enumerated domains (file 02 L125). An unknown kind or
  out-of-domain field is NOT_IMPLEMENTED, never guessed.
- Ranking uses (evaluation step, stage-map row, file order, line). Compile errors take
  step 5 (driver) or 6 (checker).
- Within one step the first applicable row wins. This reproduces L166 (7) "exception
  wins over vector validation, which wins over watchdog". It also places simulator and
  trace-integrity faults, which have no in-cycle rule, after them.
- Two different events with an identical key are reported as outside the vocabulary.

Reason: the evaluation order is called "exact" and the row rule is the only tiebreak the
text gives.

## A-026 — Checker run-outcome records (DECIDED BY CLAUDE — approved under D-009)

`checker_runs` (R08–R11) and `null_runs` (M10–M12, P18, P19, P22) give two records per
fixture in four forms the pack does not define. **Decision (decided by Claude under
standing delegation, approved under D-009):**

| Record | Outcome |
|---|---|
| `{"timeout": true}` | `CHECKER_TIMEOUT\|phase=null_check` |
| `{"error_code": "CHECKER_RUNTIME_ERROR", "exception_class": C}` | `CHECKER_RUNTIME_ERROR\|class=C` |
| `{"type": "return_invalid", "reason": R}` | `CHECKER_RETURN_INVALID\|reason=R` |
| `{"verdict": V}` or `{"verdict": V, "diagnostics": [...]}` | a valid return with verdict V; each item is checked against B7's item form (File 30 L74) and counted as malformed if it fails |

These are outcome summaries, not literal return values: R09's `{"verdict": "FAIL"}` has
no `diagnostics` key and must not be classified as `MISSING_DIAGNOSTICS`. Real checker
returns use `classify_return` (File 30 L97 order). Adjudication follows L166 step (11)
and the CHECKER rows. A malformed item with both verdicts `PASS` gives
`ACCEPT_WITH_WARNING` with null stage and error class and diagnostic
`DIAGNOSTIC_FORMAT_WARNING` (Catalog L10). With both verdicts `FAIL`, the item is
discarded and `CHECKER_NULL_REJECT` stands ("verdict retained").

## A-027 — Driver-vector checks whose parameters are not supplied (DECIDED BY CLAUDE — approved under D-009)

File 30 L83 orders the vector checks: (a) key set, (b) string values, (c) width,
(d) `0`/`1`, (e) "the design-specific legal-input predicate". M26 supplies only the
expected keys (no widths). M27 supplies the predicate as English prose ("wr_en must be 0
when full is 1"), and `full` is an output port.

**Decision (decided by Claude under standing delegation, approved under D-009):**
- Checks run in order. A check whose parameters are not supplied cannot be run.
- If an earlier check fails, that is the result (M26: `EXTRA_KEYS`). If every runnable
  check passes, the outcome is not determined and the fixture is NOT_IMPLEMENTED,
  never ACCEPT.
- Within (a), missing keys are reported before extra keys, following the order of the
  reason enumeration (file 02 L125).
- A prose predicate is not executed. Turning prose into code would be fixture-specific
  code (rule 4), and the predicate belongs to the owner-written FIFO specification. M27
  stays NOT_IMPLEMENTED until the FIFO specification provides an executable predicate.
- Re-examined after the owner's correction of 23 Nov 2026: see A-038 (still
  NOT_IMPLEMENTED; executing it would require inventing behaviour).

## A-028 — Composite inputs: response plus a later-stage outcome (DECIDED BY CLAUDE — approved under D-009)

`null_runs` + `response_object` (M10–M12, P18, P19, P22) and `runtime_pair` +
`response_object` (M37) supply a response and the outcome of a stage that needs the
simulator. **Decision (decided by Claude under standing delegation, approved under
D-009):**
- The response is first run through every stage that can run in this environment. Today
  that is PARSE_SCHEMA through COMPILE_CHECKER; after step 4, also the sandboxed runtime
  import, `inspect.signature` and factory checks.
- A failure there is the result.
- Otherwise the supplied outcome stands in for the simulator-dependent stages (L166
  steps (7)–(10)) and is adjudicated.

Reason: these fixtures test the adjudication rule; the descriptor deliberately supplies
what a simulator would produce. Limitation: the driver's simulator runs are not
executed.

## A-029 — Serializer: grammar and the emitted-diagnostic set (DECIDED BY CLAUDE — approved under D-009)

Protocol L168: "The serializer accepts only a complete diagnostic emitted by the
authoritative stage map"; step (1) validates against "the normative closed grammar and
its enumerated values". M15 also supplies `allowed_diagnostics`. **Decision (decided by
Claude under standing delegation, approved under D-009):** the diagnostic must match the
closed grammar (L94–L123 templates with L125 domains, `src/openvef/serializer.py`
`GRAMMAR`), and, when the emitted set is supplied, be a member of it. Either failure is
`FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` at stage
`FEEDBACK_SERIALIZER` with disposition `CONTROL_EXPECTATION` (Catalog L18).

## A-030 — Clause-ID packet checks: order and default regexes (DECIDED BY CLAUDE — approved under D-009)

**Decision (decided by Claude under standing delegation, approved under D-009):**
- The near-match check (`MALFORMED_CLAUSE_ID_TOKEN`) runs before set equality
  (`VISIBLE_CLAUSE_ID_SET_MISMATCH`), in the order File 31 L30 states them.
- A descriptor that omits a regex (M20 has no search or near-match regex) uses the value
  File 31 §8 fixes.
- Reserved-heading lines are compared after LF normalization (CRLF and lone CR → LF,
  File 31 L11, L27). Unresolved placeholders match `\{\{[A-Z0-9_]+\}\}` (File 31 L28).

## A-031 — Halt-signature domains versus supplied signatures (REVERSED BY OWNER, D-012; D-009 approval withdrawn)

**Reversed by D-012 (Krishika).** Every supplied signature must lie in the L185 domains; one
that does not is a fixture defect (PD-01). M42 and M47 are NOT_IMPLEMENTED. The text below is
the superseded reading, kept for the record.

Protocol L185 gives exact domains: `evaluator_component` is one of `SIMULATOR`, …,
`RTL_NULL_COMPARATOR`, and `stable_error_class` is the literal `NONE` for
`TRACE_INTEGRITY_FAILURE`. M42 and M47 supply signatures with
`"evaluator_component": "simulator"` and `"recorder"` (lower case), and M47's
trace-integrity signature has `"stable_error_class": "RecorderFault"`. These values are
outside the L185 domains.

**Decision (decided by Claude under standing delegation, approved under D-009):**
- `HaltSignature.build` enforces the L185 domains for signatures the ledger constructs
  from halt events.
- Ready-made signatures in a descriptor are compared for identity as given, because L185's
  recurrence rule needs only tuple equality.
- Under this reading M42 and M47 pass. **For the owners:** the descriptors disagree with
  L185's domains. If they should be invalid input, the pack needs a correction and a
  defined outcome for an invalid signature.

## A-032 — Control-vector expectations with extra keys (DECIDED BY CLAUDE — approved under D-009)

Catalog requirement 2 allows "a single exact expected disposition/stage/error/diagnostic
(or exact control-vector expectation)". L176 says the runner compares "disposition,
stage, error class and exact diagnostic bytes". M14, M17 and M41 add keys such as
`output_diagnostic_bytes` and `rerun_slots`, and M14/M17 have no `diagnostic` key.

**Decision (decided by Claude under standing delegation, approved under D-009):**
- A control-vector expectation is compared as a whole object: the runner's record must
  have exactly the same keys and values.
- Each extra key is a named property computed by a rule from the text:
  - M14: Protocol L168 step (2);
  - M17: L168 step (3);
  - M41: L183–L185 ("Discard all pre-halt partial scores", "every scheduled slot", "same
    frozen artifact bytes", "no confirmatory generation call").
- **Disclosure:** the property *names* come from the descriptors' expected objects,
  because the pack gives no output schema for control vectors. No *value* is read from
  an expected object.
- Comparing the four fields only was rejected, because it would report PASS while
  ignoring part of an "exact" expectation.

## A-033 — Change-class lifecycle vectors M48, M50, M53, M54, M58 (REVISED per owner correction; field derivations DECIDED BY CLAUDE — approved under D-009)

**History.** First recorded as OPEN, outside the delegation: the expected objects hold
values that appear only in the descriptors, and the `required_action` literals are
attached to fixture labels ("`M48` = …"), not to a rule.

**Owner correction (Krishika, 23 Nov 2026; Ayush's confirmation pending):** the
`required_action` values appear verbatim in the Protocol (L176); encode them from the
Protocol text. Derive the remaining fields from Protocol sentences under the delegation,
citing each sentence. Any field with no supporting sentence: say so, and keep that
fixture NOT_IMPLEMENTED.

**Decision (decided by Claude under standing delegation, approved under D-009):**
- Each `change_class` label is matched to the Protocol case its words name:
  - `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` → evaluator revision (L175
    "a frozen evaluator source/binary/…/configuration changed"; L183 (b));
  - `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` → shared-item revision
    (L181 "If any shared study item changes …");
  - `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` → study
    reset (L181 "A change in design membership, estimand or any confirmatory weight …");
  - `HALT_SIGNATURE_COMPONENT_ENUMERATION` → halt-signature schema (L175, L185);
  - `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` → design-specific revision (L181 "If a
    design-specific author-visible item changes …").
- L176 also labels each literal with its case and describes that case ("`M48`
  re-evaluates the affected scope …", "`M50` invalidates all designs …", "`M53` resets
  the preregistered design set and weights …", "`M58` invalidates both arms for the
  affected design only …"). That is how a literal is tied to a change class without
  reading the fixture ID: the code is keyed by change class, never by fixture ID.
- A field is produced only from a supporting sentence. "Supporting" means the sentence
  gives the value: a stated literal or list, or a yes/no/zero that the sentence asserts.
  A field whose *meaning* is stated but whose exact *token* appears nowhere in the
  Protocol is unsupported: writing it would mean copying the expected output (hard
  rule 4).
- The per-field table, with each citation, is `LIFECYCLE_CASES` in
  [src/openvef/ledger.py](../src/openvef/ledger.py).

| Fixture | Supported fields (citation) | Unsupported fields | Result |
|---|---|---|---|
| M53 | disposition (L176 "closed local control expectation"); stage `DESIGN_HALT` (L172, §7b); error class and diagnostic (L175 "The `M53` study-reset vector uses error class `AUTHORING_REVISION_REQUIRED` and diagnostic …"); `required_action` (L176); `old_confirmatory_artifacts_reusable: false` (L181 "cannot retain old confirmatory artifacts"); `new_preregistration_required: true` (L181 "always requires a new preregistered study"); `all_partial_ledgers_archived_and_disclosed: true` (L181 "archive and disclose all partial confirmatory ledgers"); `fresh_confirmatory_generation_required: true` (L181 "generate fresh confirmatory slots") | none | executed |
| M48 | disposition, stage, diagnostic (L175), `required_action` (L176), `new_evaluator_version_hashes_required` (L183 "assign a new evaluator version and hashes"), `f16_required` (L183 "run the frozen F16 eligibility procedure"), `reuse_same_artifact_bytes` (L183 "using the same already-generated artifact bytes"), `new_confirmatory_generation_calls: 0` (L183, L176) | `error_class` (see below); `rerun_scope_rule` (meaning in L183, token not in the text) | NOT_IMPLEMENTED |
| M50 | disposition, stage, diagnostic (L175), `required_action` (L176), `reuse_old_confirmatory_artifacts: false`, `new_confirmatory_generation_required: true`, `archive_and_disclose_partial_ledgers: true`, `new_preregistration_required: true` (all L181) | `error_class`; `affected_slots: "all_designs_x_all_arms"` (meaning in L181, token not in the text) | NOT_IMPLEMENTED |
| M54 | disposition, stage, error class and diagnostic (L175 "`M54` uses error class `HALT_SIGNATURE_SCHEMA` …"), `required_action` (L176), the three domain lists (L185, in its order) | `stable_error_class_rule`, `stable_diagnostic_code_rule` (meanings in L185, tokens not in the text) | NOT_IMPLEMENTED |
| M58 | disposition, stage, diagnostic (L175), `required_action` (L176), `reuse_old_artifacts_for_affected_design: false` (L181), `new_study_preregistration_required_if_…: true` (L181 "… even if the changed item is otherwise described as design-specific") | `error_class`; `affected_scope`, `unaffected_design_scope` (meanings in L181/L176, tokens not in the text) | NOT_IMPLEMENTED |

**Error class for M48, M50, M58.** No sentence states it. L175 gives error classes only
for the M41 vector (`MID_RUN_REEVALUATION`, which is *not* its diagnostic's CODE), M53 and
M54. The stage map shows that the error class need not equal the CODE (L154:
`SIMULATOR_ERROR|…` under `EVALUATOR_INFRASTRUCTURE_FAILURE`), so "error class = CODE" is
not a rule I can cite. The closest text is the v1.3.1 change log ("Corrected M53 to use
the declared `AUTHORING_REVISION_REQUIRED` error class"), which is historical, not
normative. The audit tables (file 62) likewise note "Error class … declared (L175–L176)"
only for M53 and M54.

**For the owners:** M48, M50, M54 and M58 need either a Protocol correction (error classes
for the three revision vectors, and the scope/rule tokens as literals) or an owner
ruling that these tokens may be taken from the descriptors.

## D-002 — Artifact-execution sandbox (DECIDED — Ayush's confirmation pending)

**Owner decision by Krishika, 23 Nov 2026 (Ayush's confirmation pending):** F18 artifact
execution uses Docker image `python:3.11.18-slim` pinned by digest, with
`--network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges`, a non-root
user, tmpfs for scratch, pids/memory/CPU limits and a wall-clock timeout. The pinned
`requirements.lock` is installed with `--require-hashes` inside the image. Cocotb and the
simulator are not pinned: fixtures that need them stay NOT_IMPLEMENTED.

Resolved digest: `python@sha256:07d4824036af339fa1b6ef769cc99d9c10a141769538b52b3b597c84f7a7b535`.
Details and tests: [docs/sandbox.md](sandbox.md).

## D-002a — Pinned interpreter is the container's (DECIDED — Ayush's confirmation pending)

**Owner decision by Krishika, 23 Nov 2026 (Ayush's confirmation pending):** the pinned
interpreter for all F18 evidence is the `python:3.11.18-slim` container by digest. The
whole runner, static stages included, moves into the sandbox image; the host Python is
for development only. Recorded in docs and in every run's evidence.

Implemented: [runner/run_f18_container.sh](../runner/run_f18_container.sh) (host broker,
bash only) and the runner in broker mode; `interpreter_status` in every `summary.json`.
Pinned values: `3.11.18 (main, Nov  5 2026, 07:57:53) [GCC 14.2.0]`, SHA-256
`92d7e40ec50be176cb1b790c7568b7e08cd862137b5aa69f1413ba1967886b79`. CLAUDE.md hard
rule 2 was reworded to match (owner instruction, 23 Nov 2026). See [docs/sandbox.md](sandbox.md).

## D-003 — Simulation toolchain (DECIDED — Ayush's confirmation pending)

**Owner decision by Krishika, 23 Nov 2026 (Ayush's confirmation pending):** toolchain per
the Charter ("Cocotb; Icarus Verilog initially"): pin Icarus Verilog and cocotb at the
latest stable versions installable in that image; cocotb from `requirements.lock` with
hashes; iverilog via the image's package manager with the exact version recorded. This
is the owner approval hard rule 3 requires for the new lock entries.

Pinned: `cocotb==2.1.0` (+ `find-libpython==0.5.1`, `iniconfig==2.3.1`,
`packaging==26.3`, `pluggy==1.7.0`, `pygments==2.21.0`, `pytest==9.2.0`, all hashed);
Debian `iverilog` `12.0-2+b1`, `.deb` SHA-256
`febe027d2d3f5a7e570844d55758339ab5490acc09f404f214a8719d89d07056`, fetched from
snapshot.debian.org (owner instruction, 23 Nov 2026). Details in
[docs/sandbox.md](sandbox.md).

## D-004 — Yosys and MCY for the null-netlist export (DECIDED — Ayush's confirmation pending)

**Owner decision by Krishika, 23 Nov 2026 (Ayush's confirmation pending):** pin Yosys and
MCY for the null-netlist export (Protocol L233, L235, L544) at their latest stable
releases that build in the pinned image, from snapshot.debian.org or a pinned source
commit, with exact versions and hashes recorded in docs and in every run.

Pinned:
- **Yosys v0.71**, latest release, 12 Nov 2026. Debian trixie ships only 0.52, and that
  package would also bring a second, system Python (`python3`, `python3-click`) into
  the image.
  - Built from the release tarball `yosys.tar.gz`, SHA-256
    `2ec7c2ee63bb9b4065d6d5fff2786a1455e834f90ede8eb1d47791153ebef2a5`, the digest
    GitHub publishes.
  - Tag commit `b4c586fd37d0ec61bb38fc1a85fd6a2fde48fcd1`. The tarball's `.gitcommit`
    is CI merge commit `5628c13240f670b97aaaca3d47940c4afb8ff572`, which GitHub's
    compare shows has no file differences from it; the build asserts that value.
- **MCY v0.71**: commit `5a2cad0cbefceb7f23051c08348bd23128fd1046` (tag object
  `b062a44a…`). It is pinned by commit because MCY publishes no release asset.
  - Only the command-line tool and its scripts are installed. `mcy-dash` (Flask) and the
    GUI (Qt) are not needed for export.
- **`click`** was left out at first. Hard rule 3 requires owner approval for it, D-004
  does not mention Python packages, and the standing delegation excludes dependency
  pins. D-004a (below) approved it on 24 Nov 2026, and it is now in `requirements.lock`.
  The null-netlist export uses Yosys only.
- **Build tools** (gcc, cmake, bison, flex, …) come from snapshot.debian.org at
  `20261104T212339Z`, the snapshot recorded in the base image's own apt sources.
  - They are used in a separate build stage and are not in the final image.

Build configuration: CMake `release` preset (`-O3`), with these changes:
- Tcl off, editline off, Python off and unit tests off;
- `BUILD_SHARED_LIBS=OFF`, so no new shared libraries are needed at run time;
- everything else at release defaults, including ABC and the slang frontend.

Details and binary hashes: [docs/sandbox.md](sandbox.md). Not decided here: the frozen
export script, mutation modes and the mutant population (L544), which stay owner items.

## D-004a — `click` for the MCY command-line tool (DECIDED — Ayush's confirmation pending)

**Owner decision by Krishika, 24 Nov 2026 (Ayush's confirmation pending):** "approve
adding click (the version mcy requires) to requirements.lock with --require-hashes."
Recorded with D-004.

- MCY v0.71 (commit `5a2cad0c`) states no version bound for `click`. Its README says only
  `pip install click flask`, and `mcy.py` has `import click`.
- The pin is therefore the version pip-tools 7.7.0 resolves in the pinned base image:
  `click==8.5.1` (wheel and sdist hashes `8bb5376d…7e37`, `9bbfada7…72b4`). The lock is regenerated with the same `pip-compile --generate-hashes`
  command, starting from the existing lock, so the existing pins are unchanged.
- On Linux, `click` has no dependencies (`colorama` applies on Windows only).
- `flask` is not added: it serves only `mcy-dash`, which is not installed.
- After this decision, `mcy --help` runs in the image, and `tests/test_netlist_export.py`
  checks that.

## D-005 — FIFO design materials become AI-assisted (DECIDED — Ayush's confirmation pending)

**Owner decision by Krishika, 24 Nov 2026 (Ayush's confirmation pending)**, recorded in
the Owner Sign-off Pack, Amendment D-005: Part 2 row 4 changed. The Sign-off Pack is not
in this repository; this record follows the instruction as given in Claude Code.

**Now AI-assisted (Claude drafts; owners review and approve):**
- the FIFO design specification, port manifest and reset/legal-input rules;
- the other payload blocks (checklist item 17);
- the FIFO RTL;
- proposed frozen values and the trace schema (items 7–12).

**Unchanged (human-written):** F6/F17 control checkers and drivers, the directed suite and
the control mutants.

**Observation mask:** may be drafted, but it must be signed by an independent human mask
reviewer (Protocol L271).

CLAUDE.md's Scope section is updated to match. The disclosure wording is carried in
docs/assistance-log.md.

**Values:** depth 4 and width 8 were recommended by Claude in the claude.ai session and
adopted by Krishika. This attribution is as stated by Krishika on 24 Nov 2026; that
session is not in this repository. Claude Code did not recommend values in its own
session.

**Research consequence, for the owners to weigh:** Protocol L468 requires "Independently
authored, cycle-exact specs"; the pack does not define "independently authored". An
AI-drafted specification weakens that claim. The D-005 disclosure states it, and reports a
potential familiarity confound if a Claude model is evaluated.

## D-006 — Owner approvals of FIFO draft choices (DECIDED — Ayush's confirmation pending)

**Owner approvals by Krishika, 24 Nov 2026 (Ayush's confirmation pending)**, following a
review by Claude (claude.ai):
- A-042 is accepted: `rst` is harness-owned and not a driver-vector key.
- The almost-full threshold is 3 (FIFO-029).
- The top module name is `ovf_fifo`.
- The cycle cap is 64 (proposal item 7).
- The watchdog applies per run (proposal item 9).

**Not frozen.** Spec v0.2 and the item 7–12 proposals stay DRAFT until both owners freeze
them. Every run that uses them is provisional.

## D-007 — Feasibility-control authorship, mutant form, miter tool (DECIDED — Ayush's confirmation pending)

**Owner decisions by Krishika, 24 Nov 2026 (Ayush's confirmation pending)**, on a
recommendation by Claude (claude.ai), answering §8 of
[F1-F17-plan.md](F1-F17-plan.md):
1. The control drivers and checkers for F1–F5 and F7–F13 are owner-written, for
   independence from the harness author. Claude does not draft them.
2. Control mutants are RTL edits of `design/fifo/rtl/ovf_fifo.v`.
3. The mask-aware miter uses Yosys's built-in `sat` (no new dependency).
4. F1 reuses the reference driver (checklist item 14) with the F6 correct checker.

CLAUDE.md's Scope section is updated to match. The owner-artifact slots, their interfaces
and the controls each feeds are listed in `design/fifo/controls/README.md`.

**Disclosure note (recorded 28 Nov 2026 at Krishika's instruction; independence aim of D-007).** On 28 Nov 2026,
Claude (claude.ai) gave Krishika prose guidance for `drivers/reference_driver.py`, an owner control file:
(a) a restatement of the driver contract in File 30 L35 and Protocol L208–L210, and (b) one design suggestion: "a
fixed list of planned rows, where step returns the row for that cycle_index". It was prose only, with no code,
pseudocode or file content, which Sign-off Pack Part 2 row 5 allows. It is disclosed here because D-007 aims at
independence from the harness author, and the guidance came from a Claude model. Krishika decides the design and
writes all of the file's code. Assistance log, entry of 28 Nov 2026 (session 16, continued).

## A-036 — Hash randomization inside the sandbox (DECIDED BY CLAUDE — approved under D-009)

File 30 §6 is headed "Import sandbox and deterministic execution". Paired runs compare
next-input schedules (Protocol L166 (8)), so a driver that iterates over a `set` of
strings would diverge between runs only because of Python's per-process hash
randomization. **Decision (decided by Claude under standing delegation, approved under
D-009):** the sandbox sets `PYTHONHASHSEED=0`. Reason: the section requires
deterministic execution, and the variable is set by the evaluator, so artifacts cannot
observe or change it (no `os`/`sys` import is allowed). The alternative, leaving
randomization on, would let evaluator configuration turn an honest artifact into
`DRIVER_NONDETERMINISM`.

## A-034 — An exception while importing an artifact module (DECIDED BY CLAUDE — approved under D-009)

After IMPORT_POLICY a module body holds only allowed imports, literal constants, a
docstring and definitions, so raising during import is close to impossible. The stage
map still has no row for it. **Decision (decided by Claude under standing delegation,
approved under D-009):** an exception while importing `driver.py` is
`RUNTIME_EXCEPTION|file=driver.py|phase=factory|class=<C>` at DRIVER_RUNTIME. Import is
the first execution of driver code, and the `factory` phase is the stage map's earliest
driver phase. The same rule applies to an import denied by the runtime allow-list. An
exception while importing `checker.py` in a checker invocation is
`CHECKER_RUNTIME_ERROR|class=<C>`: it is a checker process exception (File 30 L97).
Exceptions that are not `Exception` subclasses (e.g. `SystemExit` from `exit()`) are
treated the same way.

## A-035 — Order of post-construction checks; when `check_trace`'s signature is checked (DECIDED BY CLAUDE — approved under D-009)

Protocol L166 (7): "Factory return type and runtime signatures are checked immediately
after factory construction." The order between them is not given, and `check_trace`
lives in a file that runs "in a separate process after the trace is immutable" (B7).
**Decision (decided by Claude under standing delegation, approved under D-009):**
- After construction, check the return type, then `create_driver`'s signature, then
  `Driver.step`'s. This follows the sentence's order and the required-symbol sequence.
- `check_trace`'s runtime signature is checked in the checker's own process, before its
  first call. Loading checker code into the driver process would break the B7 separation.
- A runtime signature must have exactly the required names, all
  `POSITIONAL_OR_KEYWORD`, no defaults (File 30 L35/L37 "the same parameter
  names/kinds/counts").

## A-037 — Wall-clock limit during driver import or factory; F18 factory seed (DECIDED BY CLAUDE — approved under D-009)

The watchdog row is `WATCHDOG_TIMEOUT|phase=driver_step`, and `PHASE` for
`RUNTIME_EXCEPTION` is `factory` or `step`. No row covers a driver import or factory call
that never returns. **Decision (decided by Claude under standing delegation, approved
under D-009):**
- That case is an evaluator-side error: the runner records ERROR, never a REPAIR verdict
  or a made-up exception class.
- A checker invocation that exceeds the limit is `CHECKER_TIMEOUT|phase=null_check`, as
  defined.
- The factory call for F18 fixtures uses seed 0, since no fixture supplies a slot seed.
- The 20 s default limit is this build's value, not a frozen pack value.

## A-038 — M27: executing a prose legal-input predicate (DECIDED BY CLAUDE — owner review pending)

**Owner correction (Krishika, 23 Nov 2026; Ayush's confirmation pending):** "implementing
a check from prose is interpretation; do it under the delegation with citations, unless
it would require inventing behaviour." This re-examines A-027's M27 part.

M27 supplies `driver_return: {"wr_en": "1", "full": "1"}` and
`legal_input_predicate: "wr_en must be 0 when full is 1"`, and expects
`DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE`.

**Decision (decided by Claude under standing delegation, owner review pending):** M27
stays NOT_IMPLEMENTED, because executing it would require inventing behaviour:
1. The pack defines no predicate language. File 30 L83 (e) says only that "the full
   vector satisfies the design-specific legal-input predicate from the author-visible
   reset/legal-input specification". Turning the sentence into a check means inventing a
   grammar (`<port> must be <bits> when <port> is <bits>`) whose only known instance is
   this fixture's string: fixture-shaped code (hard rule 4).
2. The predicate's source is the author-visible reset/legal-input specification (L83;
   Protocol L61 "reset protocol and legal-input assumptions"). For FIFO that is the
   owner-written FIFO specification, which the Scope section reserves to the owners.
3. Checks (a)–(d) come first (L83 order), and M27 supplies no input-port set or widths.
   So the precondition that (a)–(d) pass cannot be established either. `full` is
   conventionally a FIFO output, and if so (a) would report `EXTRA_KEYS`; the pack does
   not say.

What would unblock it: an executable predicate in the FIFO specification's legal-input
rules (owner-written), plus the port manifest. The vector check then calls it as step (e).

**Revisited, 24 Nov 2026 (decided by Claude under standing delegation, owner review
pending), now that FIFO-042 exists as an executable predicate (D-005) and check (e) runs
it (A-041): M27 still stays NOT_IMPLEMENTED.** Reason 2 above no longer applies, because
the FIFO specification exists as a D-005 draft. Reasons 1 and 3 still hold, in narrower
form:
1. **FIFO-042 is not M27's predicate.**
   - M27 supplies its own predicate, "wr_en must be 0 when full is 1". FIFO-041 states a
     different rule: a write is illegal at full only "with `rd_en` = 0", because
     FIFO-030 makes a write together with a read at full legal.
   - The two disagree on the vector `wr_en` = 1, `rd_en` = 1 at full.
   - Substituting FIFO-042 would evaluate a predicate the fixture does not supply. That
     would also contradict the treatment of descriptor-supplied data in A-005 (owner
     decision) and A-044, where fixture-supplied data controls.
   - Executing M27's own string still needs a prose-to-code translation that has a
     single instance, which is fixture-shaped (hard rule 4). No predicate language exists
     (File 30 L83 (e); PD-06).
2. **No port set.** M27 gives no input-port set or widths, so checks (a)–(d), which
   precede (e) (File 30 L83), cannot be established.
   - The vector's own keys cannot be the port set, because check (a) would then pass by
     construction.
   - Under the FIFO port manifest (FIFO-004), the vector `{"wr_en", "full"}` fails (a)
     first, with `MISSING_KEYS` (`wr_data`, `rd_en`), and `full` is an output.
   - So evaluating M27 against the FIFO materials would not reach (e) at all.

**What would unblock it** (an owner or pack action, not an interpretation):
- either a revised M27 descriptor that supplies a port manifest with widths and an
  executable predicate;
- or an owner decision that M27 is evaluated against the frozen FIFO materials, in which
  case its expected outcome must be revisited, because (a) fires before (e).

## A-039 — Simulator failures: the `class` token and an overrun outside `step` (DECIDED BY CLAUDE — approved under D-009)

The stage-map row is `SIMULATOR_ERROR|target=<RTL_OR_NULL>|class=<EXCEPTION_CLASS>`
(L154), and `EXCEPTION_CLASS` is "the simple Python exception class name" (L125). A
failure of the `iverilog`/`vvp` processes is not a Python exception inside the
simulation. **Decision (decided by Claude under standing delegation, approved under
D-009):**
- The harness reports the exception its own process handling raises or would raise:
  - `CalledProcessError` when `iverilog` exits non-zero, or when `vvp` ends without the
    loop's result;
  - `TimeoutExpired` when the overall budget runs out while no `step` call is in
    progress.
- A budget overrun during driver import or factory stays an evaluator ERROR (A-037).
- An overrun inside `step` is `WATCHDOG_TIMEOUT|phase=driver_step`.

Reason: these are the simple class names of the Python exceptions that represent those
failures in the harness process, so the token is a real exception class, as L125
requires. The alternative, the fallback `Exception`, loses the distinction between a
design that does not build and a hung simulator. No current fixture depends on this.

## A-040 — Trace-row fields the pack names only in prose (DECIDED BY CLAUDE — owner review pending)

Protocol §5.2 gives three exact field names (L217 `inputs_consumed_at_edge_n`, L218
`outputs_after_edge_n`, L219 `next_inputs_scheduled_for_edge_n_plus_1`). L223 adds "Record
cycle index, reset, consumed inputs, post-edge outputs, next-input decision, driver
completion state and run status", without names or value domains. File 30 L92 gives
`reset_release_cycle` as a non-negative integer in the checker metadata. The trace
schema itself is TO FREEZE (L543).

**Decision (decided by Claude under standing delegation, owner review pending):**
1. The three given names are used verbatim as keys in every row. In these names, `n`
   refers to the row's own edge, not to a per-row key suffix: L216 says "For trace row
   `n`, record three separate fields", and a key that changed per row could not be
   "three separate fields".
2. Rows begin at the first reset edge. `cycle_index` is the row's edge number `n`. The
   reset-release edge is row `reset_release_cycle` (recorded with the trace), and the
   driver's `step` argument for row `n` is `n − reset_release_cycle`. Reason: a
   `reset_release_cycle` other than 0 is only meaningful if the trace has rows before
   release, and L221 says "the initial reset inputs are defined in the design pack". The
   competing reading, rows from release only, would make `reset_release_cycle` always
   0 and leave reset windows (L276) out of the trace.
3. `reset` is a boolean: true for rows before the reset-release edge.
4. `driver_completed` uses the name in L227 ("records `driver_completed=true`").
5. `run_status` is recorded once per trace: `COMPLETE_TRACE` when the cap is reached
   with no failure, otherwise `TRUNCATED_TRACE`. Reason: L328 "A driver/simulator error
   or timeout produces a truncated trace" and L332 "Reaching the cycle cap is normal
   termination; the checker is run on the complete trace". The tokens are built from
   those phrases. The pack gives no per-row status.
6. The row at the cap edge, and a row whose `step` failed or whose vector was invalid,
   are recorded with `next_inputs_scheduled_for_edge_n_plus_1: null`. An invalid vector
   is not driven (File 30 §4).
7. Consumed inputs are captured passively from the DUT input ports at the active edge
   (L262 "capture … passively"). If they differ from the prior row's scheduled vector,
   the run ends with `TRACE_INTEGRITY_FAILURE|reason=ROW_ALIGNMENT` (L221 "must agree
   with the prior row's scheduled input"; stage-map L155 reason domain). This branch has
   no runtime test: a correct harness does not produce it.
8. The waveform is FST through a `$dumpfile`/`$dumpvars` wrapper module (L223 "FST/VCD
   … where supported"). It is returned with its byte count and SHA-256.

**Open consequence:**
- `compare_runs` compares every row, including reset rows. Reset windows belong to the
  mask (L276), which is owner material.
- Until the mask exists, a raw divergence during reset is compared like any other row.

## A-041 — Scope of the legal-input predicate in check (e) (DECIDED BY CLAUDE — owner review pending)

File 30 L83 lists check (e) among the checks the harness makes on a returned vector
"before driving": "(e) the full vector satisfies the design-specific legal-input
predicate from the author-visible reset/legal-input specification". The same line says
"illegal protocol combinations are distinct reason codes". The pack gives no predicate
language (PD-06).

**Readings:**
- (a) The predicate sees only the vector's own values. It can then reject only
  combinations within one vector.
- (b) The predicate sees the vector together with the outputs that were sampled in the
  same row and given to the driver (`outputs_after_edge_n`, L218). Legality can then
  depend on protocol state.

**Decision (decided by Claude under standing delegation, owner review pending): (b).**
This scope is also part of the AI-drafted FIFO specification under D-005 (FIFO-040 to
FIFO-042). It therefore needs owner review twice: as a pack interpretation under the
standing delegation, and as drafted specification text under D-005.
Reasons from the pack text:
- Protocol L415 gives "undefined writes while full" as its example of an input sequence
  that violates "protocol legality". Whether a write happens while full depends on state,
  and a single vector cannot express it under reading (a).
- The reason-code wording is "illegal protocol combinations", and the stage-map token is
  `ILLEGAL_PROTOCOL_STATE` (L125). Both name protocol state, not only the vector.
- The sampled outputs are exactly what the driver was given in that `step` (L208, L221),
  so the predicate uses no information hidden from the author.

**What changes:**
- The DRAFT FIFO specification states this scope (FIFO-040) and gives the predicate as a
  Python 3.11 function of `(vector, sampled)` (FIFO-042).
- The harness's check (e) does not consume that predicate yet. It still accepts only the
  test-only literal `ALL_INPUTS_LEGAL` (A-038), and that stays so until the owners
  approve the specification.


## A-042 — Harness-owned reset and the "frozen top-level input-port" key set (DECIDED BY CLAUDE — accepted by Krishika under D-006, Ayush's confirmation pending)

File 30 L83 check (a): "its key set equals the frozen top-level input-port set exactly".
Protocol L212: "Every non-`COMPLETE` return must be a dictionary with exactly the frozen
top-level input-port keys".

**Readings:**
- (a) The key set is every top-level input port except the clock. A reset port is then
  a driver key, and the driver must always drive it inactive (FIFO spec v0.1).
- (b) The key set is the set the design pack freezes for driver vectors. It may leave out
  harness-owned control inputs, the clock and the reset, which the harness drives itself.

**Decision (decided by Claude under standing delegation, owner review pending): (b).**
This follows a spec review by Claude (claude.ai), adopted by Krishika. Reasons from the
pack text:
- Both sentences say "frozen", which points to the set the design pack freezes, not a
  mechanical list of all ports.
- The clock is already left out, even though it is a top-level input: drivers must not
  "own the clock" (L212), and "The harness owns the clock and scheduler" (L208). So the
  set is not literally every top-level input under either reading.
- Reset belongs to the harness and the design pack, not the driver:
  - L208: the first `step` call "is after reset release";
  - L221: "the initial reset inputs are defined in the design pack";
  - L260: paired runs "use identical seed, reset, simulator, cycle cap, safe-idle, driver
    API and watchdog". Reset is listed among the fixed run conditions, not among the
    driver's decisions.
- L217 still records every top-level input: "`inputs_consumed_at_edge_n`: top-level
  inputs stable immediately before active rising edge `n`". The harness therefore
  records held inputs in the consumed-input field.

**Implemented:**
- New optional design field `held_inputs` (`{port: bits}`). Reset-sequence vectors give
  these ports, and from the reset-release drive phase onward the harness holds them at
  the given values.
- They are not driver-vector keys: checks (a)–(d) use `input_ports` only.
- They are recorded in `inputs_consumed_at_edge_n` and in the scheduled vector, and
  they are part of the ROW_ALIGNMENT check.
- Designs without `held_inputs` behave exactly as before.

**Competing consequence:** under reading (a), the FIFO's `rst` returns to the driver key
set (v0.1), and `held_inputs` is unused.

## A-043 — What the L334 "null-netlist wall time" measures (DECIDED BY CLAUDE — owner review pending)

Protocol L334: "Proposed timeout: `T_timeout = max(5 × median(null-netlist wall time over
3 runs for the same artifact/design), 2 seconds)`." Item 9 is approved per run (D-006).
The pack does not say what one "wall time" covers, or what happens to the three runs'
outcomes.

**Readings:**
- (a) The evaluator's elapsed time for one complete null-netlist driver run, including the
  sandbox container start and teardown.
- (b) Only the simulator's own elapsed time inside the container.

**Decision (decided by Claude under standing delegation, owner review pending): (a).**
Reasons:
- "wall time" is the elapsed real time of a "run"; L229 says "A wall-clock timeout is
  separate" from the cycle cap, which points to a limit on the run as a whole.
- (a) can be measured identically for every artifact without instrumenting the
  simulator.

**Details:**
- The resulting T_timeout is applied as the per-run budget and as the per-step watchdog
  inside the container. That makes the limit slightly more lenient than the measurement,
  because container start is outside the in-container budget.
- The three calibration runs are used only for their wall times; their outcomes are
  ignored. Each calibration run has a build-default ceiling of 120 s (not from the pack),
  and a run that hits it counts as 120 s.

**What changes under (b):** T_timeout is smaller, and container start-up time no longer
affects it.

## A-044 — A fixture-supplied names-only port manifest (DECIDED BY CLAUDE — owner review pending)

F18 descriptor P17 carries `input.port_manifest` = `{"input_ports": [...]}` with port
names only. File 30 L83 check (a) uses "the frozen top-level input-port set". The catalog
does not say how a fixture's own manifest relates to the design materials. Here the
design materials are the D-005 DRAFT FIFO, whose ports differ from the fixture's.

**Readings:**
- (a) The fixture's names are the key set for checks (a)–(b) for that fixture, as with
  `manifest_clause_ids` (A-005, owner decision). If (a) and (b) pass under names that
  are not the design's ports, checks (c)–(e) cannot run (no widths) and the vector
  cannot be driven, so the result is not determined.
- (b) Ignore the fixture's manifest and use the design materials' ports.

**Decision (decided by Claude under standing delegation, owner review pending): (a).**
- A-005, an owner decision, already treats descriptor-supplied manifest data as the
  frozen manifest for that fixture.
- Reading (b) would discard part of the fixture's input.
- The rule is generic: it never depends on the fixture's ID or expected output.

**Implemented:** design field `driver_vector_keys`, which `run_f18.py` passes for the
`{port_manifest, response_object}` input shape. The simulation still runs on the design
materials, because the driver's `step` receives the design's outputs.

**What changes under (b):** for P17's vector `{"data": "0"}`, nothing does. It lacks
keys under both readings, so the result is `MISSING_KEYS` either way.

## A-045 — Construction of the mask-aware miter (DECIDED BY CLAUDE — approved under D-009)

> [02 L291] "Build the miter with the same observation mask as the trace comparator and with the same reset sequence and legal-input assumptions from the design specification."

The pack does not say:
- on which side's outputs a legal-input predicate that reads outputs is evaluated;
- how the comparator's executable Python predicate becomes a miter assumption;
- what the initial register state is.

FIFO-043 (DRAFT spec) says the FIFO-042 rules are the miter's assumptions.

**Decision (decided by Claude under standing delegation, approved under D-009):**
- **Legal-input predicate:** evaluated on the null (gold) side's outputs at that step,
  i.e. the outputs the driver would have sampled. This is the same side as the mask
  predicate (L273: "evaluated using the null-netlist trace for both members of a pair").
- **Assumption generated from the spec's own predicate:** by exhaustive enumeration of
  every input and output bit (`miter.compile_predicate`). Support bits are proven by
  invariance over the whole domain, and the expression is the truth table on the
  support. So the assumption equals the predicate by construction; there is no
  hand translation. This answers plan Q5.
- **Reset:** each reset vector forces every input at its step. Afterwards, held inputs
  keep their held value.
- **Initial state:** all registers start at zero (`sat -set-init-zero`), a stated
  bounded-equivalence assumption (L544, TO FREEZE). The simulator starts memories at X
  instead. A mutant that reads an unwritten FIFO slot could therefore disagree between the
  miter and the simulator. F4's replay check would show it.
- **Shortest counterexample (L293):** after a failure at the full bound, ascending bounds
  are checked; the first failing bound is the shortest.
- **Step mapping:** sat step t holds the state after t−1 edges, so trace row n is step n+2.

**What changes under another reading:**
- Evaluating the predicate on the mutant side would let a mutant that corrupts `full`
  change which inputs are legal for the comparison.
- Undefined initial state (`-set-init-undef`) would need X-aware triggers.

## A-046 — Mapping harness events to §12 terminations in a pair run (DECIDED BY CLAUDE — approved under D-009)

> [02 L306] "Driver/simulator error, split by whether a masked divergence was recorded before termination."

**Decision (decided by Claude under standing delegation, approved under D-009):** on the
mutant run:

| Harness event | §12 termination | Source |
|---|---|---|
| `driver_runtime`, `driver_vector` (an invalid or illegal vector, which the harness does not drive), `simulator_error` | DRIVER_SIM_ERROR | — |
| `driver_watchdog` | TIMEOUT | L333 |
| `trace_integrity` (row alignment) | integrity failure → INVALID_PAIR | L311 |

An evaluator-side failure of the harness itself (no adjudicable result) is raised, not
classified.

Reason: §12 has no separate class for an invalid vector after an artifact is valid.
The vector ends the run as the driver's fault, which is the "driver" half of rule 2.

The rows recorded before a watchdog kill are now kept (sandbox/sim.py `_truncated`), so
"masked divergence recorded before termination" is measured on them.

## A-047 — A null run that fails inside a pair (DECIDED BY CLAUDE — approved under D-009)

> [02 L336] "A null run must complete within its watchdog for a mutant-run timeout to be interpreted."

**Decision (decided by Claude under standing delegation, approved under D-009):** if the
null member of a pair does not complete, the pair is `INVALID_PAIR` as an integrity
failure.

Reason: the artifact's null runs passed during validation, so a failing null in the pair
can't be explained from predeclared evidence. L311: "If the cause cannot be determined
from predeclared integrity evidence, classify conservatively as INVALID_PAIR."

## A-048 — Checker invocations per pair (DECIDED BY CLAUDE — approved under D-009)

§12 classifies a pair by what "checker returns" on the complete mutant trace. The repeat
rule (two invocations) is stated for null traces (L247) and for the panel (L435), not for
pair classification.

**Decision (decided by Claude under standing delegation, approved under D-009):** one
invocation, in its own process, on the frozen mutant trace bytes. The bytes are
re-hashed afterwards. The pair record also says whether the mutant trace is
byte-identical to the null trace (needed for F8, L311).

## A-049 — Panel false-alarm event per benign trace (DECIDED BY CLAUDE — approved under D-009)

> [02 L429] "Define the false-alarm event rate as the number of `FAIL` outcomes on the `B_ds` benign original-RTL/null-netlist reference traces divided by `|G_cd| × B_ds`"

Each benign trace is evaluated twice (L417).

**Decision (decided by Claude under standing delegation, approved under D-009):** a
benign trace carries one false-alarm event if either evaluation returned FAIL. This keeps
the rate within [0, 1], and an inconsistent pair still counts the FAIL it contains, as
L423 asks ("so an error does not hide a simultaneous false alarm").

## A-050 — Which mutant traces the panel evaluates (DECIDED BY CLAUDE — approved under D-009)

**Decision (decided by Claude under standing delegation, approved under D-009):** each
checker is evaluated twice on every exposed case in `Q_ds` (L427, L435), and twice on
every raw-only unmasked case (for `PANEL_STRICTER_THAN_MASK_EVENT`, L427).

Mutant traces with no raw divergence are not evaluated: they are byte-identical to the
null trace of the same scenario, which is already in the benign set.

Plan Q6 is settled the same way: the "valid" of F5 (L514) is `rd_valid`, the predicate of
the DRAFT mask (MK05); this stays open until the mask is signed.

## A-051 — Non-deterministic run-record fields for F1 (DECIDED BY CLAUDE — approved under D-009)

> [02 L510] "Traces match excluding explicitly non-deterministic metadata"

**Decision (decided by Claude under standing delegation, approved under D-009):**
- The checker-facing trace rows are compared byte for byte, with no exclusions.
- In a simulation run record, only `waveform` is excluded, by an explicit list
  (`alignment.NONDETERMINISTIC_RESULT_FIELDS`).
- Observed on the pinned image: two otherwise identical runs give FST files that differ
  in the header date string ("… 15:16:49 2026") and in a later block. All other fields,
  including the per-row simulator times, are identical.

## A-052 — F14 "ports" comparison (DECIDED BY CLAUDE — approved under D-009)

> [02 L523] "Stable null hash, top module and ports"

**Decision (decided by Claude under standing delegation, approved under D-009):**
- Ports match when the set of (name, direction, width) is the same in the RTL and in both
  exported netlists.
- Declaration order is recorded and compared separately (`port_order_same_as_rtl`), but
  it is not a pass condition. Connections are by name in the harness and the miter.

## D-008 — Governance: approvals signed by Krishika alone take effect (DECIDED)

**Owner governance rule by Krishika (co-owner), 24 Nov 2026**, given in Claude Code:
"decisions and approvals signed by Krishika alone take effect now. Ayush Kumar Singh's
agreement is recorded ONCE, in a single 'Ayush ratification pending' entry in
docs/AUDIT-READINESS.md, and is not repeated on individual items."

**Applied to:** the owner freeze package. Krishika's signature (commit `a955245`) freezes
A1–F1. The record is
[FREEZE-RECORD-2026-11-24.md](FREEZE-RECORD-2026-11-24.md) /
`design/fifo/freeze/freeze-record-2026-11-24.json`.

**Supersedes:** step 3 of the package ("A line is frozen only when both owners approve
it"), and the CLAUDE.md line that kept Claude-decided readings "owner review pending until
both owners review it".

**Does not change:**
- the independent human mask reviewer's signature (Protocol L271), which no owner signature
  replaces;
- the standing-delegation readings that no owner has reviewed yet;
- earlier records, which keep their wording as written.

## D-009 — Approval of the remaining Claude-decided readings (DECIDED)

**Owner decision by Krishika (sole builder), 24 Nov 2026**, adopting a Claude (claude.ai)
recommendation; pasted into Claude Code: "every reading decided under the standing
delegation and not yet owner-approved (A-007..A-012, A-013 tie, A-015..A-037, A-039,
A-045..A-052, F15 case table) is approved by Krishika as decided, without itemised owner
review."

**Record:** `design/fifo/freeze/readings-approval-D-009.json` holds the SHA-256 of each
approved section, and of `src/openvef/f15.py`, as at commit `23e6193`
(`sha256_as_approved`), and after the wording cleanup of "owner review pending" to
"approved under D-009" (`sha256`). `tests/test_freeze_package.py` checks that undoing
that wording gives the approved bytes back. An item changed in any other way is not
covered. Summary table: [READINGS-REVIEW.md](READINGS-REVIEW.md).

**Limits:** no reading was reviewed item by item, and the recommendation came from Claude,
which also decided the readings. Pack defects stay defects; a reading approved here does
not correct the pack. Readings decided later are not covered. Takes effect under D-008;
Ayush's ratification stays the single entry in AUDIT-READINESS.md.

## DEV-001 — Deviation from Protocol L271 (DECIDED)

The owner accepted the observation mask and File 24 table without an independent review.
Full record: [DEVIATIONS.md](DEVIATIONS.md). This supersedes, for this mask only, D-008's
statement that no owner signature replaces the L271 signature. L271 itself stays unmet.

## D-010 — Mask placeholder fixes and re-freeze (DECIDED)

**Owner decision by Krishika**, given in Claude Code with the saved mask review: "fill
spec_version_sha256 with the frozen spec hash in both mask files; set status to "FROZEN under D-010; reviewed non-independently (DEV-001)"; set reviewer fields to "Claude (claude.ai), non-independent, DEV-001; accepted by owner Krishika". Re-freeze the mask at the new hashes". Labels
become "cleared under DEV-001 (non-independent review saved)".

**Applied to:** every row's `mask_reviewer`, `independent_reviewer` and `review_status`, and
the JSON `status`. Mask content is unchanged. The JSON status no longer repeats
"evaluator-only: never part of an authoring packet"; that Protocol rule (L270) still applies.
L271 stays unmet ([DEVIATIONS.md](DEVIATIONS.md)).

## D-011 — Independent-reviewer column and L270 reminder (DECIDED)

**Owner decision by Krishika**, given in Claude Code: "set the independent_reviewer column to
"none (DEV-001)" in every row; restore "Evaluator-only: never part of an authoring packet
(L270)" to the JSON status text. Leave file names and author_packet_location cells as they
are (record why)." This supersedes D-010 on those two points.

**Why the file names and `author_packet_location` cells stay** (reasons recorded by Claude
at the owner's instruction):
- `design/fifo/design-materials-DRAFT.json`, frozen at its signed hash (B1–B6), names
  the mask JSON by its current path. Renaming it would break a frozen item.
- The mask JSON names the table by its path, and earlier evidence, records and reviews
  cite both paths. Renaming would break that trail.
- The cells name `docs/fifo-spec-v0.2.md (DRAFT)`. The frozen specification keeps its DRAFT
  wording, because the package says signed files are not edited in place. Frozen status is
  set by the freeze record and its hashes, not by the word "DRAFT".
- The saved review covers those cells, and changing them has no effect on what is compared.

## DEV-002 — Implementation audit by an AI model (DECIDED)

The L555 (5) implementation audit will be performed by a different AI model (ChatGPT,
OpenAI); not yet performed, and not a human independent audit. Full record:
[DEVIATIONS.md](DEVIATIONS.md).

## D-012 — Response to audit findings A1-1 and A8-1 (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) triage of the DEV-002 audit report; given
in Claude Code. The report itself was not supplied
([note](reviews/implementation-audit-gpt6-2026-11-25-NOTE.md)).

**A1-1 accepted:** "remove every runner branch reachable only by a single fixture's input
shape. M27 and M36 fall to the generic "no adapter for this input shape" path,
NOT_IMPLEMENTED."
- **Scope confirmed by Krishika.** The decision names M27 and M36. Claude reported that 13
  more fixtures (M13, M14, M15, M17, M18, M19, M25, M26, M28, M37, M41, P17, R07) sit on single-fixture branches and all passed, and asked. Krishika
  chose "Literal: remove all".
- **Applied:** 15 branches removed. The rules behind them stay implemented and unit-tested
  (column rule, serializer, packet checks, runtime signature, vector checks, paired runs,
  operational recovery), but no fixture reaches them through the runner.
- **M20 and M40 stay.** They use one adapter (one required key set with two optional keys).
- **Enforced by** `tests/test_dispatch_shapes.py`: an adapter must be reached by at least two
  mandatory fixtures, and only the `ADAPTERS` table may select code by shape.
- **Limit:** the scan is per input shape. Branches on values inside a shape (one event kind,
  one change class) can still be reached by a single fixture; D-012 does not cover them.
- **Supersedes:** the M36 part of A-012, and the adapters of A-027 (M26), A-028 (M37), A-029
  (M15), A-030 (M18, M19), A-032 (M14, M17, M41) and A-044 (P17). The readings stay approved;
  they no longer produce an F18 result for those fixtures. A-025, A-026 and the rest of
  A-028 and A-030 are unaffected.

**A8-1 accepted:** "reverse A-031. HaltSignature.given validates every component against
Protocol L185 domains; out-of-domain supplied signatures are a fixture defect (PD-01), so M42
and M47 become NOT_IMPLEMENTED with that reason." The L185 mapping from halt code to component
is validated too. "D-009's blanket approval of A-031 is withdrawn" is recorded in
`design/fifo/freeze/readings-approval-D-009.json`, which now holds 39 items.

**Limitations A2, A3, A5 and A9:** "accepted and recorded; not defects".

## D-013 — Adapter rule replaced after audit A1-1 (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) recommendation, given in Claude Code:
"replace the literal single-fixture-shape rule. New rule: an adapter is allowed only if (a) its
input contract is defined by cited pack text (file + line), and (b) it is unit-tested with at
least 3 synthetic non-fixture inputs, including at least one where the expected output differs
from every fixture's. Adapters encoding knowledge of a specific fixture remain forbidden."

Supersedes D-012's single-fixture-shape rule. A8-1, A-031 and the rest of D-012 stand. **The
rule was changed after audit finding A1-1 and requires re-audit.**

| Fixture | Decision | Citation (a), or reason |
|---|---|---|
| M18 | restored | File 31 L11, L27 (payload lines, reserved headings, LF normalization); outcome 02 L173, L174, File 36 L16 |
| M19 | restored | File 31 L28 (placeholder pattern); outcome 02 L173, L174, File 36 L16 |
| M25 | restored | File 30 L35, L37 (required parameters, now taken from that text); outcome 02 L148 |
| M26 | restored | File 30 L83 (a), (b); outcome 02 L152 |
| M28 | restored | 02 L166 (8); outcome 02 L156 |
| M13 | out | `slots` and `evaluator_repair_attempt` have no meaning stated in the pack |
| M14 | out | `test_scope` is not defined; the extra output properties appear only in the descriptor (PD-03) |
| M15 | out | the pack states no error class for `FEEDBACK_SERIALIZER_REJECT` (PD-26) |
| M17 | out | as M14; `grammar_exempt_for_primitive_test` is not defined |
| M27 | out | owner; prose predicate, no port set (PD-25) |
| M36 | out | owner; `parser_unit_vector` is not defined (PD-04) |
| M37 | out | `driver_source_excerpt` is not defined; no text lets a supplied result replace the paired runs |
| M41 | out | several properties not defined (for example `evaluator_repair_attempt`, its `required_action` literal); output properties only in the descriptor; its signature is outside L185 (PD-01) |
| P17 | out | a names-only manifest is not the pack's port manifest (02 L60 names widths), and no text joins it to the FIFO materials (A-044) |
| R07 | out | 02 L245 gives the condition but no error class or diagnostic, and the row at L157 is for the artifact's own stimulus. The only rejecting input is the fixture's own, so the adapter would encode it |

**The rule is general, so the adapters that had stayed were checked too:**
- **`change_class` is removed (M53 becomes NOT_IMPLEMENTED).** The change-class labels and the
  output property names appear only in descriptors (PD-02, PD-03), and each label is used by
  one fixture. M48, M50, M54 and M58 now stop at the same path.
- **Halt recurrence keeps its input contract (L185) and gives no outcome.** The pack states no
  error class for `DESIGN_HALT_REPEATED` (PD-26). M42 and M47 still stop earlier, on PD-01.
- **Kept, weakest first:** `events` and the run-record forms (their labels are not in the pack;
  each is cited to the row it names), `null_runs` with `response_object` (the composite order is
  A-028), and the finish reason `length` (cited to 02 L144, which does not spell it; any value
  other than `length` or `stop` is now refused).

Mechanism: `runner/adapter_contracts.py` (citations), `tests/adapter_vectors.py` (synthetic
vectors), `tests/test_dispatch_shapes.py` (both conditions; flags uncited selecting values).
The scan checks that a citation is verbatim, not that it is the right text.

## A-053 — What counts as a cited input contract (DECIDED BY CLAUDE — approved under D-014)

D-013 (a) asks for an input contract "defined by cited pack text". The pack spells no descriptor
JSON keys apart from the response schema (PD-07). Readings: (i) keys must be spelled in the
pack, which would remove nearly every adapter other than the response object, including all
`events`, run-record and packet fixtures; (ii) the pack must state the meaning and domain of
every property, the rule each selecting value names, and the whole outcome; spelling is a carrier.

**Decision (decided by Claude under standing delegation, approved under D-014): (ii).** File 36
L23 requires "a literal JSON input" and defines no key names, so a rule that needs spellings
would contradict the fixture set the pack makes mandatory. Under (ii) a property without a
stated meaning keeps an adapter out even if unused, and so does an outcome field that only a
descriptor states. Not covered by D-009. The results that rest on it are the five restored
fixtures, the `events`, `checker_runs` and `null_runs` fixtures, M16, M20, M29 and M40.

## D-014 — A-053 approved (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) recommendation, given in Claude Code:
"A-053 approved as decided (strict reading). Record it; the passes resting on it now count,
subject to re-audit."

- **What is approved:** A-053 as decided, which is reading (ii): the pack must state each
  property's meaning and domain, each selecting value's rule and the whole outcome, while key
  spelling is a carrier. The stricter reading on spelling was (i), which A-053 rejects. "Strict
  reading" is recorded as the owner's wording; "as decided" is taken to control.
- **Approved text:** SHA-256 of the A-053 section before this record changed its status wording:
  `162af6d93b0d0957c68a14aa81ec1baf08c929dd8c8ec03cfe78c9fd615147c8`; after: `1efb1d29d091d4000f2f09584c3123ed35c6db0618e546b0a0db58f6bd479625`.
- **Effect:** the results resting on A-053 are no longer held back by owner review: M16, M18–M20,
  M25, M26, M28, M29, M40, R01–R06, R08–R13, M10–M12, P18, P19 and P22. They count **subject to
  re-audit** of D-013, which has not happened. Other conditions still apply.
- **Not changed:** F18 is not passed. Claude decided A-053 and Claude (claude.ai) recommended its
  approval. Takes effect under D-008; Ayush's ratification stays the single entry in
  AUDIT-READINESS.md.

## D-015 — Response to the re-audit findings (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) triage of the GPT-6 re-audit (bundle
`34bc8109…c0c0`): "accept all findings, fix in this order". The re-audit report had not reached
this repository when the fixes were made, so they follow the decision's wording, not the report's.

1. **A9-1, artifact isolation.** Before: `driver.step` ran inside the cocotb recorder's interpreter
   and `check_trace` inside the harness's, so artifact code could patch evaluator modules.
   - Now `driver.py` and `checker.py` run in `sandbox/artifact_worker.py`, a separate interpreter
     with no evaluator module, request, RTL or trace file. `sandbox/artifact_proc.py` sends it
     plain JSON and accepts only schema-checked, tagged plain data; it alone computes verdicts.
   - **A separate process was not enough.** Under the same uid, a child wrote into its parent's
     stdout through `/proc/<pid>/fd` in the pinned container (probe, 24 Nov 2026). So the worker
     installs a seccomp allow-list before loading artifact code: pipe, memory and exit calls only.
     File opens, `/proc`, sockets, fork/exec, signals and ptrace fail with EPERM. It also gets an
     address-space limit (build default 160 MiB) and is the first OOM victim.
   - Tests: `tests/test_artifact_isolation.py`, in the pinned container.
   - **Residual:** the runtime return-type and signature facts are measured inside the artifact's
     interpreter, so a hostile driver could misreport its own. That can only affect its own
     disposition, and the static AST_SIGNATURE checks do not depend on it. The wall clock stayed
     readable (vDSO) at D-015; see D-016.
2. **A1-1/A8-2.** The reserved headings are the sidecar's nine (File 31 L9; File 33 L10–L50).
   Descriptor headings must be a subset and are never used; descriptor clause-ID patterns must
   equal File 31 §8's and are never used. `DOMAINS` cites each property's domain, and a test
   requires every adapter to refuse an out-of-domain value for each property.
3. **A4-1.** `serialize` and `feedback_bytes` require the whole (stage, error class, diagnostic) to
   be what one stage-map row emits (L143–L162). The auditor's own case was not in hand then; it is
   now a test (`test_auditor_case_a4_1`). The other
   tests cover wrong stage, class, file, unknown labels, null and trailing newlines.
4. The 3.11-specific f-string test skips on other versions.

**A-036 correction.** A-036 set `PYTHONHASHSEED=0`, but factory and checker runs used
`python -I`, which ignores that variable (probe: two runs gave different hashes). It took effect
only in simulations. The worker now starts without `-I` and with a fixed environment, so it takes
effect everywhere. No fixture outcome changed.

## A-054 — An artifact process that ends or breaks its message schema (APPROVED as decided — D-016)

The stage map has rows for a driver that raises and for a checker "process crash" (File 30 L97),
but `<EXCEPTION_CLASS>` presumes an exception. With process isolation the artifact can also exit,
crash, or send malformed data. Readings: (i) an evaluator error; (ii) the artifact's own failure.

**Decision (decided by Claude under standing delegation; approved as decided by Krishika, D-016):
(ii)**, with the
L125 fallback class: "otherwise the fixed fallback `Exception`". File 30 L97 says a process crash is
`CHECKER_RUNTIME_ERROR|class=<EXCEPTION_CLASS>`; the driver row covers factory and step. A process
killed by SIGKILL (memory), or never confined, stays an evaluator error, because the artifact cannot
send signals. No current fixture reaches it. Not covered by D-009 or D-014.

## D-016 — A-054 and the wall-clock residual (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) recommendation. Takes effect under D-008.

1. **A-054 approved as decided.** Claude decided it and Claude (claude.ai) recommended its approval.
2. **Wall clock.** File 30 L101: "The runtime sandbox denies network, filesystem access beyond the
   designated temporary output directory, environment variables, wall-clock reads, subprocess and
   simulator access." D-015 recorded only the vDSO. A probe in the pinned container
   (25 Nov 2026) read live time by more routes: the `time` and `clock_gettime` system calls, `fstat`
   on a pipe (its mtime is the current time), RDTSC, RDTSCP, RDPRU and the legacy vsyscall page.
   `futex` with an absolute CLOCK_REALTIME deadline also answered whether a given time had passed.
   All of these are now closed in `sandbox/artifact_worker.py` before artifact code loads. Routes,
   mechanisms and tests are in [sandbox.md](sandbox.md) "Wall-clock reads"; what is not closed is in
   [DEVIATIONS.md](DEVIATIONS.md) "Open residuals".
3. Not re-audited. No pack reading changed: the static rules are as the pack states them.

## D-017 — Adapter rule kept and strengthened; container test evidence (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) recommendation, given in Claude Code: "keep the
D-013 adapter rule (disclosed); strengthen it: every adapter needs, besides the 3 synthetic vectors,
boundary tests for each input property's cited domain (one in-domain edge, one just outside it) —
extend the contract test to enforce this." Takes effect under D-008.

1. **Rule kept.** The second audit report said five single-fixture input shapes violate the original
   A1 criterion, and that three vectors are insufficient. D-017 keeps the shapes (disclosed) and
   answers the second point with boundary tests. It does not clear A1-1; that is for the auditor.
2. **Boundary tests.** `BOUNDARIES` in `tests/adapter_vectors.py`; `boundary_problems` in
   `tests/test_dispatch_shapes.py` fails if a property has no pair, if a pair is not tied to a cited
   domain term, changes another property, is not adjacent, gives equal outcomes, has a refused edge
   or uses a fixture input, or if no outside value of a property is refused or rejected.
   - **Limits.** At least one pair per property, not one per domain term. "Adjacent" is approximated:
     same JSON type, integers one apart, other values at most 24 characters of JSON text apart. Some
     domains have no numeric edge; there the pair is a listed value and a near-miss spelling. For
     some pairs the outside value is judged by a pack rule (REPAIR) instead of refused.
   - **Claude chose the pairs**, as it wrote the adapters.
3. **What the boundaries exposed (fixed):** a base64 string that does not decode, text with no UTF-8
   bytes, a BOM in packet text, events whose diagnostic is outside the closed grammar (L94–L127), a
   malformed JSON Pointer, and an `import_not_allowed` event naming an allowed root. On the
   code before D-017 (dba77c7) 11 of the cases fail: 9 were accepted and 2 raised an uncaught error
   (A-056). All are refused now.
4. **Container test evidence.** `tools/run_container_tests.py` runs the whole unit-test suite in the
   pinned container; output in `evidence/container-tests-<UTC>/`. It is not an F18 run and no fixture
   status comes from it. The auditor may inspect these logs for A2, A3, A7 and A9; inspecting is not
   re-running. Requires re-audit with D-015 and D-016.

## A-055 — Upper bound of `scheduled_slots` (DECIDED BY CLAUDE — approved under D-018)

> [02 L181] "a *slot* is exactly one arm × design combination"

> [02 L396] "The scheduled denominator is `|G_cd| × |M_d|`. Every scheduled slot remains in it."

Readings: (i) L181 as a count: two arms and two designs give at most four slots, so the fixtures' 10
is outside the domain; (ii) L181 states what a slot belongs to; an arm/design cell holds `|G_cd|`
scheduled slots, and the pack states no maximum.

**Decision (decided by Claude under standing delegation, approved under D-018): (ii).** L396 and L429
divide by `|G_cd|` per arm and design, and L34 assigns "Scheduled slots ... to arms by a balanced
within-design schedule", which has no meaning if each cell is one slot. So only the lower edge (1 in,
0 out) is tested. Under (i) M42 and M47 would still be NOT_IMPLEMENTED (PD-01). No outcome changes.

## A-056 — Domains of event fields and packet text (DECIDED BY CLAUDE — approved under D-018)

Values the cited text excludes but for which it states no outcome. Readings: (i) refuse the input
(NOT_IMPLEMENTED); (ii) process it as before.

**Decision (decided by Claude under standing delegation, approved under D-018): (i).**
- Events: "No unlisted value is permitted" (02 L125), so an event whose diagnostic is outside the
  grammar is refused. A pointer is RFC 6901 with `/` as root (L137). `import_not_allowed` is the
  "Disallowed import form/root" row (L147), so an allowed root is refused.
- Packet text: File 31 L26 and L74 reject invalid UTF-8 and a BOM but state no diagnostic for it.

No fixture has such a value; no F18 outcome changes (see the run in traceability.md).

## D-018 — A-055 and A-056 approved (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) recommendation, given in Claude Code:
"A-055 and A-056 approved as decided."

- **What is approved:** A-055 reading (ii), no stated maximum for `scheduled_slots`; A-056 reading (i),
  values the cited text excludes without stating an outcome are refused. Not covered by D-009.
- **Approved text** (SHA-256 of each section before this record changed its status wording; after):
  - A-055: `4fe531e2bbb5c705eb1a84a2a84c3d840e3915f49400188b9822b6b377ce0b0f`; `4fe31b31ece3ee14b7fa99a9875ec59780c6150a928c15b33188086af7c658aa`.
  - A-056: `ea4ae0c6895ce32c43c2f7a73c6999b8c3019736935e8286b2575c556cc276b3`; `7c446adc077d28b87dda5b5e81e24de6dbf21275ab22d0e184b7350ca3b52d68`.
- **Effect:** none on results; no fixture outcome depends on either. Code and evidence are unchanged.
- **Not changed:** F18 is not passed, and D-017 still requires re-audit. Claude decided both readings and
  Claude (claude.ai) recommended their approval. Takes effect under D-008; Ayush's ratification stays
  the single entry in AUDIT-READINESS.md.

## D-019 — Response to the third audit report (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) triage of the report saved as
[implementation-reaudit3-gpt6-2026-11-25.md](reviews/implementation-reaudit3-gpt6-2026-11-25.md) (NOT CLEARED).
The decision reached Claude Code before the report; the report was committed before any change.

1. **A9-2 (BLOCKER) accepted.** Principle: "no trust-critical measurement may be produced by a process
   in which artifact code has executed".
   - **Confirmed in the pinned container:** on the audited `sandbox/`, 38 of the new test cases fail,
     because a forged report was accepted.
   - **(a) Parameters.** `artifact_proc.inspect_source` asks a fresh confined process that compiles the
     source and reads names, kinds and counts from code objects. **It does not import.** The decision asked for an
     import-only process on the ground that import runs no artifact logic. That ground does not hold: helper-function
     defaults, and annotations, are evaluated when the `def` runs, and the static stages
     accept them (`test_forgery_at_import_time`). Compile-only keeps the principle.
     `__signature__` and `__wrapped__` are ignored.
   - The artifact process's own report is still required to be right. It can reject, never accept.
   - **(b) Return type, and state changed after execution: not fully closed.** A process that has run
     artifact code can report anything. `src/openvef/runtime_basis.py` decides from the source alone
     whether the artifact stays in a closed fragment where it cannot reach interpreter internals and every
     return of `create_driver` is `Driver()`: PROVEN, else SELF_REPORTED. Each result that
     reaches the runtime stage records it. SELF_REPORTED is not a rejection, because the pack allows
     code outside the fragment. Residual: [sandbox.md](sandbox.md) "Runtime checks" and
     [DEVIATIONS.md](DEVIATIONS.md).
   - **The auditor's own example** (valid `def`, then a variadic `step` installed at run time with a forged
     report) is part of that residual: still accepted, but marked SELF_REPORTED.
2. **A1-1, citation:** `stop` now cites the text that defines the property (A-057). A new test requires every
   selecting value's citation to lie within a property's cited domain; the old citation fails it.
3. **A1-1, original criterion. Owner statement:** "The original single-fixture-shape criterion is
   superseded by D-013 because the v1.3.6 pack itself contains one-of-a-kind fixtures; it will not be
   met by design; disclosed for every audit."

Not re-audited. F18 is not passed.

## A-057 — The finish reason `stop` (DECIDED BY CLAUDE — approved under D-020)

> [02 L144] "Provider finish reason explicitly reports max-token truncation"

> [30 L7] "Provider max-token truncation is `OUTPUT_TRUNCATED` at `PARSE_SCHEMA` and is reported separately."

The pack names the property only by this condition and spells no value. Readings: (i) only a value
that reports truncation has a stated meaning, so `stop` is refused; (ii) the condition divides the
domain in two, and a value that does not report truncation is stated by its complement: L144 does not
apply and the response is judged on its text; (iii) as (ii), for any other string too.

**Decision (decided by Claude under standing delegation, owner review pending): (ii), for `stop` only.**
A row whose condition is "explicitly reports" presumes reasons that do not, and File 36 L48 describes
that state in words ("without provider truncation status"). Like `length`, `stop` is a spelling that
carries it (A-053). Not (iii): another spelling may be a truncation report, and the pack does not say
which. `stop` selects no outcome of its own; it gives the result an absent reason gives. P11b depends
on this reading: under (i) it would be NOT_IMPLEMENTED.

**Approved by Krishika as decided (D-020), without itemised owner review: reading (ii) for `stop`
only, with File 36 L48 ("without provider truncation status") as the primary support for the
complement of File 02 L144.** P11b's pass now counts toward F18. (Takes effect under D-008;
Ayush's ratification stays the single entry in AUDIT-READINESS.md.)

## D-020 — Response to the D-019 read-only report (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) review of the D-019 read-only report. No
pack rule changes, so this is an owner decision, not a deviation. Takes effect under D-008;
Ayush's ratification stays the single entry in AUDIT-READINESS.md.

1. **A-057 approved** (reading (ii) for `stop`; primary support File 36 L48, the complement of
   File 02 L144). Marked decided in this file and in [READINGS-REVIEW.md](READINGS-REVIEW.md);
   **P11b's pass now counts toward F18.**
2. **SELF_REPORTED policy.**
   - **F18:** a SELF_REPORTED runtime check does not change the fixture verdict. A SELF_REPORTED
     pass stays PASS and carries a visible label, "SELF_REPORTED (D-020): runtime check not
     statically PROVEN", recorded per result (`self_reported_runtime_checks`, `self_reported_label`)
     and listed in the run summary (`runtime_checks_self_reported`, `self_reported_label`). It is
     listed in AUDIT-READINESS.md (currently `M06:driver.py`).
   - **Confirmatory use:** the validity endpoint is reported two ways — **primary**, as measured
     (each runtime report at face value); and a **pre-registered sensitivity**, with every
     SELF_REPORTED artifact counted invalid. The **count of SELF_REPORTED artifacts per arm** (and
     design) is reported alongside. Recorded in [sandbox.md](sandbox.md) "Runtime checks",
     [DEVIATIONS.md](DEVIATIONS.md) "Open residual (D-019)", and [F1-F17-plan.md](F1-F17-plan.md)
     (analysis rules). This takes the owner decision the A9-2 residual left open; it does **not**
     close A9-2, which is still not re-audited.
3. **build_audit_bundle.py:** records `build_commit` = git HEAD at build time and refuses to build
   on a dirty tree (any path), keeping `source_commit` as the last commit touching the bundled
   paths. Guarded by `tests/test_audit_bundle.py`.
4. **AUDIT-BRIEF.md:** re-audit #4 is scoped to D-019 + D-020 (see the brief for the priority
   targets).

Not re-audited. F18 is not passed.

## D-021 — Fixes before re-audit #4, then a freeze (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) review of the session 10 and 11 reports. No
pack rule changes. Takes effect under D-008; Ayush's ratification stays the single entry in
AUDIT-READINESS.md. The D-020 bundle (`0e8ea3f2…`) was **not sent to the auditor** (stated by Krishika).

1. **tests/test_audit_bundle.py:** the string check is replaced by a behavioural test. The real script
   runs as its own process with git stubbed at the subprocess boundary: `build_commit` equals HEAD,
   and a dirty tree exits 1 and writes nothing.
2. **runner/run_f18.py:** the SELF_REPORTED label is added to the fixture note before the record is
   built, so `note` and `self_reported_label` in `results.jsonl`, `run.log` and the summary agree
   (`tests/test_self_reported_label.py`). In the D-020 run, M06's `note` in `results.jsonl` lacked it.
3. **docs/assistance-log.md:** entries for the verification of D-020 and for this session.
4. **Freeze:** after the bundle is published as a GitHub release, no further commits until re-audit #4
   is triaged.

Not re-audited. F18 is not passed.

## D-022 — Response to re-audit #4 (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) triage of re-audit #4 (GPT-6; NOT CLEARED,
0 BLOCKER, 2 MAJOR, 8 LIMITATION). No pack rule changes. Takes effect under D-008; Ayush's
ratification stays the single entry in AUDIT-READINESS.md. The freeze was lifted for D-022 only.

1. **A1-1:** `stop` now cites File 36 L48, which is also in the `provider_finish_reason` domain; `length`
   keeps File 02 L144. `VALUE_SUPPORT` (`runner/adapter_contracts.py`) lists, for each selecting value, the
   words of its own quote that support it; `value_support_problems` (`tests/test_dispatch_shapes.py`) enforces it,
   and the audited state fails it. Six other quotes were lengthened or moved so that they name their value.
   **Limits:** L48 is the catalog row of the one fixture that uses `stop`, and it states the case
   ("without provider truncation status"), not the spelling `stop` (A-053, A-057). The test checks that the
   words are in the quote and belong to one value; that they support it is the author's judgement.
2. **A9-2:** the literal `inspect.signature` of File 30 L35/L37 is called after import in the artifact process, in
   addition to the trusted measurement; both must agree ([sandbox.md](sandbox.md) "Runtime checks"). Still
   self-reported: the SELF_REPORTED residual is **not closed**.
3. **F18:** no fixture status changed (checked before committing).
4. **AUDIT-BRIEF.md:** re-audit #5 is scoped to D-022 and regression of prior findings.

Not re-audited. F18 is not passed.

## A-058 — Defaults seen only by `inspect.signature` (DECIDED BY CLAUDE — approved under D-022)

> [30 L35] "Runtime `inspect.signature` must confirm the same parameter names/kinds/counts."

L35 also requires parameters with no default. Readings: (i) the runtime check compares names, kinds and
counts only; (ii) it also compares defaults. They differ only when a correct definition, with no defaults in its
code object report, carries a `__signature__` or `__wrapped__` that shows a default. (A default in the definition, or one set
at run time, is rejected by the other two measurements.)

**Decision (decided by Claude under standing delegation, owner review pending): (i).** L35 and L37 list what
the call must confirm, and defaults are not in the list. D-022 uses the same words. No F18 fixture depends on it.

**Approved by Krishika as decided**, on Claude (claude.ai) review: L35 says names/kinds/counts, and no fixture
depends on defaults. (Takes effect under D-008; Ayush's ratification stays the single entry in AUDIT-READINESS.md.)

## D-023 — Status after re-audit #5 (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) triage of re-audit #5 (GPT-6, bundle `5bdc25ea…2cc2`; D-022
CLEARED, 0 BLOCKER / 0 MAJOR / 0 MINOR, 11 LIMITATIONs; report and note in `docs/reviews/`). No pack rule changes; no code
changes. Takes effect under D-008; Ayush's ratification stays the single entry in AUDIT-READINESS.md. The freeze after
release `audit5-5bdc25ea` is lifted.

1. **Status:** the implementation audit sequence #1–#5 is complete, with no open BLOCKER or MAJOR. A1-1 and A9-2 are closed
   as findings. Kept as disclosed limitations: **A1-1-L1** (`value_support_problems` checks that the words are in the quote,
   not that they support the value; it accepts `(MEANING, "JSON")` for `stop`) and the **SELF_REPORTED residual**
   ([DEVIATIONS.md](DEVIATIONS.md) "Open residual (D-019)"; fifth audit L-10), with the fifth report's coverage
   limitations L-02 to L-11.
2. **Not claimed:** L555 (5) is **not** marked done (AI audits under DEV-002, not a human independent audit); F18 is
   **not** passed; L271 stays unmet (DEV-001).
3. `docs/DEMO-2DEC.md` is rewritten as a 10-minute faculty demo script, with pre-captured outputs in `docs/demo/`.

F18 is not passed.

## D-024 — Corrected pack v1.3.7 as a candidate (DECIDED; Phase A)

**Owner decision by Krishika**, on a Claude (claude.ai) plan. v1.3.6 stays immutable and the default; nothing under
`baseline/` changes. Takes effect under D-008; Ayush's ratification stays the single entry in AUDIT-READINESS.md.

- **Phase A (corrections only, no implementation code):** `proposals/v1.3.7/pack/` is a full copy of v1.3.6 with only
  corrections C1–C10 applied, labelled "v1.3.7 CANDIDATE, not audited"; rationale, fixture → PD → correction map and
  rejected alternatives in `proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md`; edits in the pack's CHANGELOG; checked
  by `tests/test_v137_candidate_pack.py`. Committed and pushed alone, before any implementation change.
- **Choices made by Krishika when asked (26 Nov 2026):** C1–C10 only, with the 10 fixtures they do not cover flagged
  (M13, M14, M15, M17, M37, M41, M42, M47, P17, R07); changed files labelled in-file, unchanged files by
  `CANDIDATE-LABEL.md`.
- **Changes against the 24 Nov draft**, argued in the rationale (section 2): C9 also aligns Protocol L177; C5 names the
  check-(e) input properties; C8 no longer appends to File 22.
- **Phase B (later commits):** `--pack {v1.3.6,v1.3.7-candidate}` in the runner, v1.3.6 results unchanged; the
  covered fixtures implemented by general rules only (D-013, D-017); a correction found wrong is amended in a new,
  numbered commit.

Not audited. F18 is not passed.

### D-024 Phase B — implementation on the candidate pack (owner review pending where marked)

- **Runner:** `runner/run_f18.py --pack {v1.3.6,v1.3.7-candidate}` (`runner/run_f18_container.sh <class> f18 <pack>`).
  The pack selects the pinned index hash and the adapter table; v1.3.6 uses `ADAPTERS` unchanged and its records are
  unchanged. A candidate run records `pack`, `pack_label` and `pack_manifest_sha256`, labels every record, and writes
  to `evidence/run-v137c-<UTC>`.
- **Candidate-only adapters** (`runner/adapters_v137.py`; contracts `runner/adapter_contracts_v137.py`, cited to the
  candidate pack; vectors `tests/adapter_vectors_v137.py`; checked by `tests/test_dispatch_shapes_v137.py` with the
  same functions as v1.3.6): `change_class` (C1–C4; `ledger.lifecycle_expectation_candidate`), `parser_unit_vector`
  (C9; the existing column rule), check-(e) vector (C5; `stage_map.validate_vector`). No fixture ID or expected value
  in code; general rules only (D-013, D-017).
- **Predicate execution (DECIDED: approved by Krishika under D-025, on condition that it runs only when the candidate pack's SHA256SUMS verify).** The C5 predicate is pack text, verified by the
  index SHA-256, and is executed in the runner as evaluator material, not in the artifact worker (D-015 concerns
  artifact code). Any exception or non-Boolean is "evaluator failure" (candidate File 30 L83), reported as
  NOT_IMPLEMENTED with that reason, never as an artifact verdict.
- **Boundary-check exception (DECIDED: approved by Krishika under D-025; domain fully covered by fixtures, disclosed).** The `change_class` property's closed
  domain is exactly the five candidate L176 labels, and each is a fixture input, so no in-domain edge can avoid being a
  fixture input. For that property only, the candidate boundary test allows it, and verifies that every label is a
  fixture input; every other D-017 condition is unchanged. The v1.3.6 test is not changed.
- **No Phase A correction was found wrong**, so there is no amendment.

Not audited. F18 is not passed.

## D-025 — Review of D-024 (DECIDED)

**Owner decision by Krishika**, on Claude (claude.ai) review of D-024. Takes effect under D-008; Ayush's ratification stays
the single entry in AUDIT-READINESS.md.

1. **Approved:** the runner-executed C5 predicate, on condition that it runs only when the candidate pack's SHA256SUMS
   verify (check and test added in Phase B); the `change_class` boundary exception. Both marked decided under D-024.
2. **Amendment A1 to C6:** a design-neutral predicate argued from pack text (`proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md`
   section 5).
3. **Stale references in the candidate** fixed so internal references are to v1.3.7-candidate, each listed in the CHANGELOG.
4. **A new Phase A commit** (corrections only) drafting C11+ for PD-26, PD-07 and PD-20 for M42, M47, M41, M15, M14, M17,
   M13, M37, P17, R07, under D-024's rules; a fixture that cannot be corrected without inventing behaviour is recorded as
   "needs owner specification" with the exact missing decision.
5. **Phase B** for whatever those corrections cover; amendments only as new numbered commits; v1.3.6 must stay 127/0/17/0.

Not audited. F18 is not passed.


### D-025 Phase B — implementation of C11–C16 and the manifest condition

- **Manifest condition (item 1):** the candidate's `SHA256SUMS-v1.3.7-candidate.txt` is pinned by SHA-256 in
  `runner/run_f18.py` `PACKS`; `verify_pack_manifest` checks the pin, every listed file and that no file is unlisted,
  before any fixture runs, and only then sets `adapters_v137.PACK_VERIFIED`; the C5 predicate refuses to run otherwise
  (`tests/test_pack_manifest_v137.py`).
- **Adapters** (candidate table only; contracts cited to candidate text; D-013/D-017/D-022 checks as before):
  `adapt_halt_recurrence_v137` (replaces the v1.3.6 row in the candidate table only; C10, C11),
  `adapt_serializer_grammar` (C11, C12), `adapt_truncation_primitive` (C13), `adapt_json_primitive` (C13, C14),
  `adapt_lifecycle_halt_event` (C15), `adapt_design_preflight` (C16). The v1.3.6 table is unchanged.
- **One test allowance (DECIDED: approved by Krishika under D-026 item 1):** the shape-branch scan flags comparisons naming
  `test_scope`; the candidate test allows exactly the two checks of that cited property against the value candidate
  File 36 L196/L197 fixes. The v1.3.6 test is unchanged.
- **No C11–C16 correction was found wrong**, so there is no amendment. M37, M41 and P17 still need owner specification.

Not audited. F18 is not passed.


## D-026 — Review of D-025; OWNER-SPECIFIED M41, M37, P17; document-audit bundle (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) review of D-025. Takes effect under D-008; Ayush's ratification
stays the single entry in AUDIT-READINESS.md.

1. **Approved and marked decided:** the D-025 item-3 exceptions (history; owner records Files 16, 23; the pack's
   implementation status), recorded in CORRECTIONS section 6, and the two `test_scope` allowances (D-025 Phase B).
2. **New category OWNER-SPECIFIED (OS-1..OS-3)** for M41, M37, P17. Each item is labelled in every record and counted
   apart from the pack-derived corrections. Rule: the pack fixes the expected outcome; an OS item specifies only how the
   vector reaches the stage that outcome names, and never adds an outcome code. Where a rule does not determine an
   answer, the fixture stays NOT_IMPLEMENTED with the reason. M41 (OS-1): the outcome is decided by exactly the
   properties L183's conditions name; a failed condition gets the outcome the pack states, otherwise it is unspecified;
   `required_action` is informational; pre-halt scores are counted by `pre_halt_scored_slots`. M37 (OS-2): a
   static-stage outcome would make it a static vector; a runtime or paired outcome uses option (a). P17 (OS-3): if its
   stage precedes runtime, run up to that stage; otherwise it stays NOT_IMPLEMENTED. Phase A first, then Phase B.
3. **Document-audit bundle** `dist/openvef-docaudit-bundle.zip`, with `docs/DOC-AUDIT-BRIEF.md`; published as release
   `docaudit1-<first 8 of sha>`.

### D-026 Phase A (`78e10bf`, pushed before any code)

Candidate File 36 L201–L207 (CHANGELOG E158, logged last) and CORRECTIONS section 10. The readings below apply D-026's
rules to pack text. Claude drafted them, and each is stated there with its quotes:
- **OS-1 (M41).** The success record is L175's diagnostic and error class, at stage `DESIGN_HALT`, with the four
  L175/L185 properties. Changed frozen hashes (with F16 required and the same bytes) give the evaluator-revision record
  of C1–C4 (L175, L183 path (b)). An author-visible change is out of scope, because L183 sends it to one of three L181
  revisions and the vector does not say which. A masked RTL/null halt is also out of scope (it needs a root-cause
  review). So is `pre_halt_scored_slots` = 0, since L185 does not say whether discarding no scores counts as a discard.
- **OS-2 (M37).** The expected stage `TERMINAL` is the L156 row of step (8), so option (a) applies. Steps (1)–(6) run.
  The step (7) factory checks do not, which differs from A-028 (stated). Only (`true`, `false`) determines the record.
- **OS-3 (P17).** `DRIVER_VECTOR` is checked inside step (7), so P17 stays NOT_IMPLEMENTED with that reason.

### D-026 Phase B

- `runner/adapters_v137.py`: `adapt_operational_recovery` (OS-1) and `adapt_paired_run_outcome` (OS-2). Contracts cite
  candidate File 36 L205/L206 only (`runner/adapter_contracts_v137.py`); vectors and boundary pairs are in
  `tests/adapter_vectors_v137.py`, under D-013/D-017/D-022 as before. `OPEN_SHAPES` names the OS-3 shape without an
  adapter, and the runner reports it NOT_IMPLEMENTED with the reason.
- **Labels and counts:** every candidate record has `category` = `PACK-DERIVED` or `OWNER-SPECIFIED`. An
  OWNER-SPECIFIED record also has `owner_specified` = `OS-n` and its note starts with the label. The candidate summary
  has `counts_by_category` and `owner_specified_fixtures`. v1.3.6 records are unchanged (the v1.3.6 table has no OS
  rows).
- **Boundary pairs for free Booleans (decided by Claude, owner review pending):** the four L183 Booleans of OS-1 have no
  same-type value outside {`true`, `false`}. Their D-017 pair is therefore taken at the decision term L205 states (for
  example "`f16_required` is `false`" gives success; `true` gives no stated outcome). Non-Booleans (`1`, `"false"`,
  `None`) are refused by the out-of-domain test.

Not audited. F18 is not passed. Candidate results never count as v1.3.6 F18 evidence (D-024).

## D-027 — Response to document audit #1: correction cycle 2 (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) triage of document audit #1 (GPT-6, an AI model, operated by
Krishika; bundle `c4caff40…cbd7`; NOT CLEARED: 1 BLOCKER, 5 MAJOR, 2 MINOR, 1 PACK;
`docs/reviews/doc-audit1-gpt6-2026-11-27.md`). Takes effect under D-008; Ayush's ratification stays the single entry in
AUDIT-READINESS.md.

1. **Correction cycle 2**, numbered; nothing is edited silently.
2. **New category OWNER-DECIDED (OD-n):** a normative rule the pack owners add that v1.3.6 does not state. It is labelled
   in the pack text, in the CHANGELOG and in every record that depends on it. Fixture counts are reported as
   PACK-DERIVED / OWNER-DECIDED / OWNER-SPECIFIED, and a fixture that depends on any OD rule counts as OWNER-DECIDED.
   Expected objects stay unchanged.
3. **D1-5 → OD-1:** a stage-map row with a single diagnostic code and no stated error class has error class = diagnostic
   code; `SIMULATOR_ERROR` is the stated exception. Applied to `DESIGN_HALT_REPEATED` and `FEEDBACK_SERIALIZER_REJECT`.
   C11's majority-pattern argument is retired.
4. **D1-3 → OD-2:** the owners adopt Python 3.11 as the representation of the legal-input predicate: one pure function
   `(vector, sampled) -> bool`, frozen and hash-gated, executed by the evaluator; exceptions are evaluator failures. A1
   stands on OD-2, and the original C6 is marked superseded.
5. **D1-1 + D1-2 → OD-3:** a normative control-vector schema table in the Protocol for every property in M48, M50, M53,
   M54 and M58 (and any other control vector), giving name, type, allowed values and rule. Define the `change_class`
   input contract. Move `HALT_SIGNATURE_COMPONENT_ENUMERATION` out of the change classes into domain validation. Adopt
   the scope tokens explicitly as owner vocabulary. List any property that no rule can fix; do not guess.
6. **D1-6 → OD-4:** define `evaluator_repair_attempt` in §7b: the ordinal of the recovery cycle the halt opens, and its
   relation to the one-cycle limit and the repeated-halt condition.
7. **D1-7:** state that invalid supplied signatures are outside the executable fixture contract (evaluator input error,
   no ledger record); no new outcome.
8. **D1-8:** relabel M37 a paired-outcome control vector, not a test of source-level alias detection.
9. **D1-9:** split the status wording into development-run evidence, formal F18 status and approval.
10. Phase A (pack text only) is committed alone, then Phase B (code). v1.3.6 must stay 127/0/17/0. Re-run both packs,
    the controls and the container tests in the pinned image. Rebuild the document-audit bundle, with a brief scoped to
    cycle 2 plus regression, publish it as release `docaudit2-<first 8 of sha>`, commit and push.

Items, rationale and quotes: `proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md` section 11. Numbering: OD-1 to OD-4,
then A3 (D1-7, an amendment to C10), A4 (D1-8, an amendment to OS-2) and C17 (D1-9), each in its own Phase A commit
(D-024: a candidate correction is changed only by a numbered amendment in its own commit).

## A-059 — How far OD-1 reaches (DECIDED BY CLAUDE — approved under D-029)

Decided by Claude under standing delegation; approved by Krishika as decided under D-029 item 2.

**Quote (D-027 item 3):** "a stage-map row with a single diagnostic code and no stated error class has error class =
diagnostic code; SIMULATOR_ERROR is the stated exception; apply to DESIGN_HALT_REPEATED and FEEDBACK_SERIALIZER_REJECT".

**Competing readings.**
1. "Stage-map row" means only the L141–L162 table. Then OD-1 reaches neither code D-027 applies it to, since both are
   listed in the §3.4 local-ledger vocabulary (L173, L175) and §7b (L185), not in the table.
2. It also covers the local-ledger vocabulary rows. **Chosen:** D-027 names exactly those two codes.
3. A cell `—` ("no error class") counts as "no stated error class". Then L162 (`DIAGNOSTIC_FORMAT_WARNING`) would get
   an error class. **Rejected:** the table states a value in that cell (none), so the class is stated. The reason is the
   cell's text, not M12's or P22's expected object.

**What changes.** Under the chosen readings OD-1 decides exactly two error classes, and every other row states its own
class (checked line by line: L143–L162, L174, L175). The candidate L174 text says so.

**Fixture counting under D-027 item 2 (part of this entry).** M41 is OWNER-SPECIFIED (OS-1) and depends on OD-4. D-027
says that a fixture depending on any OD rule counts as OWNER-DECIDED, and states no exception for OS items. M41 is
therefore counted OWNER-DECIDED, and its record keeps both labels (`owner_decided` and `owner_specified` = `OS-1`).
OWNER-SPECIFIED counts only OS fixtures that depend on no OD rule. If the owners prefer OS to take precedence, only the
category of M41 moves. No outcome changes.

## D-029 — Response to document audit #2 (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) triage of document audit #2 (GPT-6, an AI model, operated by
Krishika; bundle `4ee28f46…5cee`; NOT CLEARED: 0 BLOCKER, 0 MAJOR, 1 MINOR (D2-1), 0 PACK; D1-1 to D1-8 resolved, D1-9
partly; `docs/reviews/doc-audit2-gpt6-2026-11-27.md`). Takes effect under D-008; Ayush's ratification stays the single
entry in AUDIT-READINESS.md.

1. **D2-1:** fix File 21 L52 and L70 with the three-part status (development-run evidence / formal F18 status /
   approval), keeping the A1–A11 and X14 status. Then sweep the whole candidate: list every current status statement
   (grep NOT RUN, NOT PASSED, PASSED, status, F18) and fix any that lacks the three-part split; leave historical v1.3.6
   records alone. Report the full list (file, line, fixed or historical). Add a test that fails if a current status
   line mentions F18 without the three parts.
2. **A-059 approved** by Krishika: any OD dependency makes a fixture OWNER-DECIDED; M41 keeps its OS-1 label. Marked
   decided.
3. Phase A (pack text) is committed alone, then any code. Re-run v1.3.7c, the controls and the container tests in the
   pinned image (guard on) and confirm the statuses are unchanged. Rebuild the document-audit bundle with a brief scoped
   to D2-1, the sweep and regression, publish it as release `docaudit3-<first 8 of sha>`, and push.

**A-059 approved text:** SHA-256 of the A-059 section before this record changed its status wording:
`cdd05cdaa289beecbca8a0e6bdfe8e7c1d5179e00d6083a30a002095fa3cc9fa`. Only the heading and the first line changed.

Items, rationale and the sweep list: `proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md` section 12 (correction cycle 3,
item C18).

## D-030 — Response to document audit #3 (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) triage of document audit #3 (GPT-6, an AI model, operated by
Krishika; bundle `f82e1334…b26b`; NOT CLEARED on two LIMITATIONs D3-1 and D3-2 only; 0 BLOCKER, 0 MAJOR, 0 MINOR; D2-1
and D1-9 resolved; `docs/reviews/doc-audit3-gpt6-2026-11-27.md`). Takes effect under D-008; Ayush's ratification stays
the single entry in AUDIT-READINESS.md.

1. **D3-1:** write `tools/diff_runs.py`, a row-level diff of two `results.jsonl` files that reports, for each fixture,
   every field that differs, grouped by field path. Run it on `run-v137c-20261127T134318Z` (audit #2's run, results
   `81c73e32…`) against `run-v137c-20261127T153351Z` (results `4b9714a4…`) and save the output as
   `evidence/RUN-CONTINUITY-D030.md`, with an explanation of each class of field that differs. If any status, category,
   actual or expected value differs, stop and report to the owner. Include both runs' `results.jsonl` and the diff in
   the next bundle. Correct the brief's wording to say exactly what differs.
2. **D3-2:** restructure the current status lines to explicit labels ("Development-run evidence: …; Formal F18 status:
   …; Approval: …"). Strengthen the test to require those labels in order, each followed by a non-empty value, and add
   negative tests that must fail (the auditor's false-positive sentence, the words in quotes, the words out of order).
   Pack text changes go in as C19, Phase A alone, then the code.
3. Re-run v1.3.7c, the controls and the container tests in the pinned image (guard on) and confirm the statuses are
   unchanged. Rebuild the bundle with a brief scoped to D3-1, D3-2 and regression, publish it as release
   `docaudit4-<first 8 of sha>`, and push.

Rationale and the C19 line list: `proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md` section 13 (correction cycle 4).

## D-031 — Response to document audit #4, and the stopping rule (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) triage of document audit #4 (GPT-6, an AI model, operated by
Krishika; bundle `f01d344d…73cb`; NOT CLEARED on one LIMITATION D4-1 only; 0 BLOCKER, 0 MAJOR, 0 MINOR; D3-1 resolved;
no open finding against the pack text; `docs/reviews/doc-audit4-gpt6-2026-11-28.md`). Takes effect under D-008; Ayush's
ratification stays the single entry in AUDIT-READINESS.md.

1. **Stopping rule**, recorded before audit #5, here and in the audit #5 brief (`docs/DOC-AUDIT5-BRIEF.md`), verbatim:

   > "If document audit #5 finds no BLOCKER, MAJOR or MINOR finding, the owners adopt v1.3.7 as the corrected pack;
   > every remaining LIMITATION is disclosed in DEVIATIONS.md. A lexical test cannot prove semantic correctness; that is
   > established by the audited manual review."

   Adoption under this rule is the owners' act. Claude does not adopt the candidate, does not mark it adopted, and does
   not change the default pack (v1.3.6) or edit `baseline/`.
2. **D4-1** (test only, no pack text change): in `labelled_status`, count every quote kind in `QUOTES` consistently
   (straight single and double, backtick, typographic pairs); require the exact `"label: "` separator; give each clause
   a closed vocabulary drawn from the 17 current lines (Development-run evidence must name a run or say none/not
   counted; Formal F18 status must use the pack's formal-status terms; Approval must state an approval state), so
   placeholders fail. Add negative tests: the auditor's single-quoted line, the `x`/`y`/`z` line, `label:` without a
   space, and two more. Confirm all 17 lines and both fixture-index fields still pass.
3. Re-run v1.3.7c, the controls and the container tests in the pinned image (guard on), statuses unchanged. Rebuild the
   bundle with a brief scoped to D4-1, the stopping rule and regression, and also bundle the C18 candidate snapshot so
   E01–E218 can be byte-compared. Publish it as release `docaudit5-<first 8 of sha>`, and push.

## D-032 — Response to document audit #5 (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) triage of document audit #5 (GPT-6, an AI model, operated by
Krishika; bundle `5f35d75b…cd47`; NOT CLEARED on one MINOR finding D5-1; D5-2 LIMITATION and six named limitations;
manual review PASS for all 17 lines and both fixture-index fields; D3-2 resolved; `docs/reviews/doc-audit5-gpt6-2026-11-28.md`).
Takes effect under D-008; Ayush's ratification stays the single entry in AUDIT-READINESS.md.

The D-031 stopping rule is unchanged. It was not met by audit #5 (D5-1 is MINOR), and it applies again, verbatim, to
document audit #6:

> "If document audit #5 finds no BLOCKER, MAJOR or MINOR finding, the owners adopt v1.3.7 as the corrected pack;
> every remaining LIMITATION is disclosed in DEVIATIONS.md. A lexical test cannot prove semantic correctness; that is
> established by the audited manual review."

with "#5" read as "#6". Adoption stays the owners' act; Claude adopts nothing.

1. **D5-1** (test only, no pack text): the label boundary in `labelled_status` uses one consistent `\w`-based rule
   (underscore counts as a word character) everywhere; negatives for `_Development-run evidence:`,
   `x_Development-run evidence:` and the same for the other two labels; every existing negative and positive re-run.
   Nothing else in the validator changes: **D5-2 stays a disclosed LIMITATION**.
2. **Limitation 4, an owner interpretation with no pack text change.** Recorded here and in `docs/DEVIATIONS.md`,
   verbatim: "the owners authorized development-only regression runs (run_class: development) during the v1.3.7
   document audits; they are not implementation or fixture execution under Protocol L555(3)'s gate and are not F18
   acceptance". The pack text (Protocol L555 (3)) names no such exception; this is the owners' reading of it.
   **Superseded by D-033 item 1 (DEV-003):** kept as recorded. Audit #6 found this reading unsupported (D6-2, MAJOR);
   the runs are fixture execution, and the owners waived the bar for them instead.
3. **D5-2 and limitations 1–6** of report #5 are added to `docs/DEVIATIONS.md` now as disclosed limitations, so that an
   adoption, if audit #6 clears, only has to reference them.
4. Re-run v1.3.7c, the controls and the container tests (guard on; check for leftover containers first), statuses
   unchanged. Rebuild the bundle (brief #6: D5-1, regression and the stopping rule), publish it as release
   `docaudit6-<first 8 of sha>`, and push.

## D-033 — Response to document audit #6 (DECIDED)

**Owner decision by Krishika**, on a Claude (claude.ai) triage of document audit #6 (GPT-6, an AI model, operated by
Krishika; bundle `e9719fb3…6982`; NOT CLEARED on D6-2 (MAJOR) and D6-1 (MINOR); D6-3 LIMITATION; D5-1 resolved;
`docs/reviews/doc-audit6-gpt6-2026-11-28.md`). Takes effect under D-008; Ayush's ratification stays the single entry
in AUDIT-READINESS.md.

The D-031 stopping rule is unchanged. It was not met by audit #6, and it applies again, verbatim, to document audit #7:

> "If document audit #5 finds no BLOCKER, MAJOR or MINOR finding, the owners adopt v1.3.7 as the corrected pack;
> every remaining LIMITATION is disclosed in DEVIATIONS.md. A lexical test cannot prove semantic correctness; that is
> established by the audited manual review."

with "#5" read as "#7". Adoption stays the owners' act; Claude adopts nothing.

1. **D6-2 accepted** (the D-032 wording was Claude's error). The D-032 owner interpretation is replaced by an explicit
   owner-authorized deviation, **DEV-003** in `docs/DEVIATIONS.md`, verbatim: "Protocol L555(3) bars implementation or fixture execution until the document audit and owner record are
   complete. The owners waived this bar for development-only regression runs (run_class: development) from the candidate's creation
   (b9f3d54) until v1.3.7 is adopted or rejected, to check that corrections did not change outcomes. These runs are fixture execution; they are not F18
   acceptance and are not counted as F18 evidence. The waiver ends when v1.3.7 is adopted or rejected."
   (Scope reworded by Krishika the same day, from "during the v1.3.7 document audits"; it includes the runs before
   audit #1.) Every waived run ID is listed there. L4 stays open as a disclosed departure ("Ends when: the waiver ends"). The
   superseded D-032 text stays visible with a note; it is not deleted.
2. **D6-1** (test only, no pack text): the preceding-character block-list in `labelled_status` is replaced by an
   allow-list. A label is valid only at the start of the line or right after an ASCII space, "(", "|" or "*" (only
   those), and each label must match exactly as ASCII. Negatives: U+0301 before a label, U+200D, U+200B, U+00A0, a
   Cyrillic look-alike letter inside a label, and a tab. All 17 lines and both fixture-index fields must still pass.
   **v1.3.6 runs** (Krishika, same day): not excluded on assumption. Whether v1.3.6's own L555 (3) gate was met
   before the first v1.3.6 fixture run is recorded in DEV-004 (OPEN: the repository cannot show it; owner decision
   required). **Updated by D-034** (below): DEV-004 now reads "v1.3.6 gate recorded as met, with evidentiary gaps".
3. **D6-3** (context/negation blindness) is added to the D5-2 disclosure in `docs/DEVIATIONS.md`.
4. Re-run v1.3.7c, the controls and the container tests (guard on, no leftover containers), statuses unchanged. Rebuild
   the bundle (brief #7: D6-1, D6-2, regression and the unchanged stopping rule), publish it as release
   `docaudit7-<first 8 of sha>`, and push.

## D-034 — v1.3.6 L555 (3) gate: owner records and DEV-004 (DECIDED)

**Owner decision by Krishika**, 28 Nov 2026, on a Claude (claude.ai) review of the owner records. Takes effect under
D-008. Ayush's ratification stays the single entry in AUDIT-READINESS.md.

1. The audit #6 report is saved verbatim with its NOTE, committed alone first (`docs/reviews/doc-audit6-gpt6-2026-11-28.md`,
   SHA-256 `809b2d86…78c7`, 17,645 bytes).
2. The Owner Decision Record (revision 25) and the Owner Sign-off Pack (revision 95) are saved unchanged in
   `docs/owner-records/`, with a NOTE giving their SHA-256s. Both are claude.ai Docs Markdown exports made by Claude
   (claude.ai) on 28 Nov 2026 at Krishika's request.
3. DEV-004 is rewritten as "v1.3.6 gate recorded as met, with evidentiary gaps", citing exact lines from the exports:
   - the Part 4 signature by Krishika, 23 Nov 2026 13:54 IST (08:24 UTC), adopting the Decision Record at revision 25
     (A1–A11 11/11, X14 Option A, freeze valid), 3 minutes before `run-20261123T082747Z` (08:27 UTC);
   - §5.2, which confirms F18 as part of the parser/assembler hand-tests;
   - the record's "PASS, 23 Nov 2026 (independent, documents only)" for the document audit.

   The gaps, each with an "Ends when":
   - (1) the 23 Nov document-audit report is not in the repository;
   - (2) Ayush's signature was posted from Krishika's session and is unverified;
   - (3) the Part 3 checklist ticks §4 identities, the §5.1 interpreter hash and the §5.4 auditor, which are blank in
     the Decision Record;
   - (4) the Decision Record boxes were marked by Claude on the owners' written instruction.
4. The label "v1.3.6 gate not shown met (DEV-004)" is replaced on the covered runs by "v1.3.6 gate recorded as met; gaps
   DEV-004".

Claude added to gap (3) a fourth mismatch that is the same kind: the §1 "baseline reviewed" item. It also added two
"read with care" observations to DEV-004 that are not gaps decided by D-034: the exports are 28 Nov copies, and both
records' own status lines read BLANK or UNSIGNED. The owners may move either observation into the gap table or drop it.
None of this closes a gap, makes any run F18 evidence, or bears on v1.3.7 adoption.

## D-035 — Adoption of v1.3.7 after document audit #7 (DECIDED)

**Owner decision by Krishika**, 28 Nov 2026, on a Claude (claude.ai) triage of document audit #7 (GPT-6, operator
Krishika; bundle `7e44902c…ed63`; **CLEARED**, no BLOCKER, MAJOR or MINOR; `docs/reviews/doc-audit7-gpt6-2026-11-28.md`,
SHA-256 `a948ab97…6a67`). Takes effect under D-008. **Ayush's ratification is pending**; it stays the single entry in
AUDIT-READINESS.md. The full record is `docs/V137-ADOPTION.md`.

1. **Adoption.** The D-031 stopping rule (recorded before audit #5, unchanged; D-032 and D-033 applied it to #6 and #7)
   is met. The owners adopt v1.3.7 as the corrected planning pack, effective now (recorded about 11:00 UTC, 28 Nov
   2026). The record is in this file, in `docs/DEVIATIONS.md` ("Adoption of v1.3.7 (D-035)") and in
   `docs/V137-ADOPTION.md`. Each says what adoption is not (an implementation audit, F18 acceptance, L555 (5) or L271)
   and lists every disclosed limitation carried forward.
   **A1–A11 and X14 for v1.3.7** (v1.3.7 Protocol L555 (3) requires an explicit owner record). Claude asked, because the
   instruction named only the pack adoption. In this Claude Code session the answer selected was the option worded by
   Claude, "Add to D-035 now (Recommended)": "Krishika states in D-035: for v1.3.7, A1–A11 are accepted as written
   (11/11) and X14 Option A is chosen." Register 16, which holds that text, is byte-identical in v1.3.6 and v1.3.7.
2. **Release.** The candidate is copied unchanged into `baseline-v1.3.7/OpenVEF_Planning_v1_3_7/` (read-only, beside
   the untouched `baseline/`). It is labelled "v1.3.7 ADOPTED" only in a new label file outside the pack directory; no
   pack text is edited. A ZIP is built with its SHA-256 and published as GitHub release `pack-v1.3.7`.
3. **DEV-003 ends at adoption** (end time recorded in `docs/DEVIATIONS.md`), and L4 is closed. From now on the v1.3.7
   L555 (3) gate is met: the document audit is cleared and the owner record is D-035 with item 1. v1.3.7 fixture runs
   are authorized development runs, still not formal F18 acceptance.
4. **Default pack.** `--pack v1.3.7` is the default for F18 runs. v1.3.6 stays selectable, and its records are
   unchanged. `v1.3.7-candidate` stays selectable so that earlier runs can be reproduced. The controls runner is not
   pack-selectable (F15 reads the v1.3.6 Protocol by file name) and keeps v1.3.6, unchanged.
5. **DEV-004 follow-ups from audit #7.** The Sign-off Pack L96 hash-attestation caveat is added, and the §1 mismatch in
   gap 3 is marked as Claude's addition.
6. **Runs.** F18 on v1.3.7 (the first authorized run), the controls and the container tests, in the pinned image.

## D-036 — Commit provenance, static-stage checker, F1 and F3 composed (DECIDED)

**Owner decision by Krishika**, 28 Nov 2026, on a Claude (claude.ai) review. Takes effect under D-008. Ayush's
ratification is pending; it stays the single entry in AUDIT-READINESS.md.

1. Push `e4e1c28`.
2. **Provenance.** From D-036 on, every commit Claude creates uses `--author="Claude Code (Anthropic)
   <noreply@anthropic.com>"`, recorded in CLAUDE.md and the assistance log. Commits before D-036 used Krishika's
   identity with a Co-Authored-By trailer, and git cannot tell those apart. `tests/test_controls_provenance.py` fails if
   any file under `design/fifo/controls/` other than README.md and slots.json was last changed by a Claude Code-authored
   commit. The pinned image has no git, so that test skips there and runs on the host.
3. **`tools/check_control_file.py <path>`.** Harness code only. It runs File 30's static stages (SOURCE_AST, which
   includes the parse, then IMPORT_POLICY and AST_SIGNATURE) on one owner file, with the production functions, and
   prints which stage accepted or rejected it, with the diagnostic. It only reads the file.
   `ast_signature.required_symbols` was split into per-file helpers (`required_symbols_in`,
   `check_ast_signature_file`), with unchanged pair behaviour. `tests/test_check_control_file.py` checks agreement with
   the production pair pipeline on every pack F18 pair.
4. **F1 (L510) and F3 (L512)** are composed in `runner/run_controls.py`, on `drivers/reference_driver.py` and
   `checkers/f6_correct_checker.py` (D-007 (4)). They report `BLOCKED_OWNER_ARTIFACTS` until both files exist, and
   `ARTIFACT_REJECTED` when the production stages reject the files. No placeholder owner file was created.

## D-037 — Miter N, solver and timeouts frozen as proposed; run_controls.py usage (DECIDED)

**Owner decision by Krishika**, 28 Nov 2026, on a Claude (claude.ai) review. Takes effect under D-008. Ayush's
ratification is pending; it stays the single entry in AUDIT-READINESS.md.

1. **Freeze.** The DRAFT values in `docs/fifo-miter-proposal-DRAFT.md` (N, Yosys `sat` settings, timeouts) are frozen
   exactly as proposed, provided each one is consistent with Protocol L299 and the cycle cap. Claude was to quote the
   pack line for each value and stop if any value conflicted. None did:
   - N = the cycle cap, 64 driver cycles after reset release. L293: "Use bound `N` no greater than the design cycle
     cap." B1 counts the cap in the same unit.
   - Solver = Yosys v0.71 built-in `sat` (minisat), from D-004 and D-007 (3). L299: "N, solver and timeout are **TO
     FREEZE**."
   - 300 s per `sat` script and 900 s per Yosys run. L296: "`UNDECIDED`: solver/resource limit prevents a
     classification."
   Recorded in [FREEZE-RECORD-2026-11-24.md](FREEZE-RECORD-2026-11-24.md), Amendment D-037, with hashes, before any owner
   mutant exists. The machine-readable record is `design/fifo/freeze/miter-freeze-D-037.json`. The proposal file is not
   edited in place.
2. **Runner.** `runner/run_controls.py` `miter_settings` reads the record and re-checks its hashes before every F4 or F5
   bounded check. A changed hash, or an N other than the cycle cap, gives `ERROR`, never a run on unfrozen values. Each
   record carries `FROZEN under D-037 (Protocol L299)` and the record's SHA-256. `MITER_DRAFT` is removed.
3. **Usage.** `run_controls.py -h`/`--help` prints the usage message and exits 0. Wrong arguments print it to stderr and
   exit 2, instead of a traceback.
4. Tests: `tests/test_miter_freeze.py`. It checks the hashes, that the values equal the proposal's table, and that the
   L293, L296 and L299 quotes appear verbatim in both packs. It checks that the runner stops on a changed hash or another
   cap, and that the record was committed before any mutant (host only; the pinned image has no git). It also checks the
   usage message.
