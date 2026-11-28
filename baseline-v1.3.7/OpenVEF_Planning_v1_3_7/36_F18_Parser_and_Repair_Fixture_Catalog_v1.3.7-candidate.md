# OpenVEF F18 Parser, Repair and Missing-Case Fixture Catalog v1.3.7-candidate

**Status:** Mandatory proposed fixture set. All inputs are materialized under `41_F18_Fixture_Inputs/` and indexed by literal byte length and SHA-256. This catalog is a test specification, not an execution report. Status, in three separate parts: Development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; Formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; Approval: no implementation is qualified or approved. No LLM call is required to run the hand-written suite, but no execution is authorized until the owner-acceptance gate is met.

## Normative local disposition vocabulary

The following values exist only in the F18/local ledger and are not model-feedback diagnostic codes:

- `ACCEPT`: response passes all checks and validity can proceed.
- `ACCEPT_WITH_WARNING`: top-level checker verdict remains valid, but a malformed individual diagnostic item is discarded and logged as `DIAGNOSTIC_FORMAT_WARNING`.
- `REPAIR`: one deterministic repair stage and fixed diagnostic are emitted.
- `TERMINAL_INVALID_NO_REPAIR`: the scheduled slot is terminal-invalid; no repair is sent.
- `DESIGN_HALT_NO_SLOT_SCORED`: the design pauses; affected slots remain unscored until the §7b re-evaluation completes.
- `DESIGN_ABORTED_NO_SLOTS_SCORED`: a repeated design-halt condition aborts the design; no slots for that design are final-scored.
- `CONTROL_EXPECTATION`: a serializer, parser, protocol or lifecycle test vector; it does not represent an artifact feedback event.
- `F18_REJECT`: a packet-freeze, assembly, manifest or fixture-integrity gate rejects the packet/test input.

`stage_id` is one of the normative stages listed in Protocol §3.4, or null where a response is accepted without repair. F18-only errors use their own separate diagnostics: `PACKET_FREEZE_REJECT|reason=RESERVED_HEADING_LINE`, `ASSEMBLY_REJECT|reason=UNRESOLVED_PLACEHOLDER`, `F18_REJECT|reason=VISIBLE_CLAUSE_ID_SET_MISMATCH`, `F18_REJECT|reason=MALFORMED_CLAUSE_ID_TOKEN`, and `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC`. These F18-only codes are not part of the model-feedback grammar. Local ledger error classes are also closed: `F18_REJECT` uses `ASSEMBLY_OR_MANIFEST_FAILURE`; M14 uses `TRUNCATION`; M17 uses `JSON_SERIALIZATION`; and the M41 operational-recovery control expectation uses error class `MID_RUN_REEVALUATION` with diagnostic `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS`. These labels are local test-ledger values and are never model feedback.

## Fixture requirements

1. Every descriptor listed below is mandatory; no P, R or M fixture is optional.
2. Each descriptor contains a literal JSON input, a single exact expected disposition/stage/error/diagnostic (or exact control-vector expectation), and the descriptor's byte hash/length is in `fixture-index.json`.
3. Each fixture is independent. No descriptor may bundle multiple alternative expected outcomes.
4. P fixtures test schema/source/parser behavior; R fixtures test repair-stage precedence and lifecycle behavior; M fixtures test previously missing edge cases, AST precedence, async-comprehension detection and the F18/serializer boundaries.
5. The fixture index, each descriptor hash, expected object, and exact fixture count must agree. A missing, duplicate, hash-mismatched, ambiguous or unlisted fixture fails F18.
6. The F18 fixture runner must compare exact diagnostic bytes, not only display labels. Serializer, lifecycle and parser unit vectors are marked by `fixture_class` (`serializer_primitive_unit_vector_grammar_exempt`, `lifecycle_unit_vector`, `parser_unit_vector`) and are deliberately grammar-exempt; they test local utilities/policies, not model feedback. A `parser_unit_vector` input has exactly the keys `source_file` and `syntax_error`. `source_file` is `driver.py` or `checker.py`. `syntax_error` has the key `lineno`, a positive integer, and may have the key `offset`, an integer or null. The vector applies the Protocol §3.4 `SOURCE_SYNTAX_REJECT` column rule to that position. Its result has stage `SOURCE_AST`, error class `SOURCE_SYNTAX_REJECT`, the diagnostic given by the rule, and disposition `CONTROL_EXPECTATION`.

## Mandatory inventory

| ID | Scope | Description | Expected outcome | Descriptor |
|---|---|---|---|---|
| P01 | parser | Minimal response accepted under strict AST and known manifest. | `ACCEPT` — `None` | `41_F18_Fixture_Inputs/P01.json` |
| P02 | parser | Markdown-fenced response JSON. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P02.json` |
| P03 | parser | Prose prefix before otherwise-valid response JSON. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P03.json` |
| P04 | parser | Trailing non-whitespace after valid JSON. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P04.json` |
| P05 | parser | Duplicate top-level JSON key. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P05.json` |
| P06a | parser | Unexpected top-level property. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P06a.json` |
| P06b | parser | Unexpected nested property in driver object. | `REPAIR` — `SCHEMA_REJECT|pointer=/driver` | `41_F18_Fixture_Inputs/P06b.json` |
| P07 | parser | Missing required checker property. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P07.json` |
| P08a | parser | Wrong schema constant or prohibited dependency: schema_version. | `REPAIR` — `SCHEMA_REJECT|pointer=/schema_version` | `41_F18_Fixture_Inputs/P08a.json` |
| P08b | parser | Wrong schema constant or prohibited dependency: language. | `REPAIR` — `SCHEMA_REJECT|pointer=/language` | `41_F18_Fixture_Inputs/P08b.json` |
| P08c | parser | Wrong schema constant or prohibited dependency: language_version. | `REPAIR` — `SCHEMA_REJECT|pointer=/language_version` | `41_F18_Fixture_Inputs/P08c.json` |
| P08d | parser | Wrong schema constant or prohibited dependency: dependencies. | `REPAIR` — `SCHEMA_REJECT|pointer=/dependencies` | `41_F18_Fixture_Inputs/P08d.json` |
| P09 | parser | UTF-8 BOM before otherwise-valid response. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P09.json` |
| P10 | parser | Invalid UTF-8 byte sequence. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P10.json` |
| P11a | parser | Provider finish reason explicitly reports max-token truncation. | `REPAIR` — `OUTPUT_TRUNCATED` | `41_F18_Fixture_Inputs/P11a.json` |
| P11b | parser | Syntactically truncated JSON without provider truncation status. | `REPAIR` — `SCHEMA_REJECT|pointer=/` | `41_F18_Fixture_Inputs/P11b.json` |
| P12a | parser | Whitespace-only source after valid response schema: driver. | `REPAIR` — `SOURCE_EMPTY|file=driver.py` | `41_F18_Fixture_Inputs/P12a.json` |
| P12b | parser | Whitespace-only source after valid response schema: checker. | `REPAIR` — `SOURCE_EMPTY|file=checker.py` | `41_F18_Fixture_Inputs/P12b.json` |
| P13 | parser | Disallowed import root os. | `REPAIR` — `IMPORT_NOT_ALLOWED|module=os` | `41_F18_Fixture_Inputs/P13.json` |
| P14 | parser | The one permitted from-import. | `ACCEPT` — `None` | `41_F18_Fixture_Inputs/P14.json` |
| P15 | parser | Correct schema echo but wrong source step parameter names. | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=Driver.step|reason=PARAMETER_NAMES` | `41_F18_Fixture_Inputs/P15.json` |
| P16 | parser | Missing module-level create_driver factory. | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=create_driver|reason=MISSING_ENTRY_POINT` | `41_F18_Fixture_Inputs/P16.json` |
| P17 | parser | Driver returns an incomplete input vector at runtime. | `REPAIR` — `DRIVER_VECTOR_INVALID|reason=MISSING_KEYS` | `41_F18_Fixture_Inputs/P17.json` |
| P18 | parser | Checker return object omits required diagnostics key. | `REPAIR` — `CHECKER_RETURN_INVALID|reason=MISSING_DIAGNOSTICS` | `41_F18_Fixture_Inputs/P18.json` |
| P19 | parser | Checker returns bare string PASS. | `REPAIR` — `CHECKER_RETURN_INVALID|reason=NON_DICTIONARY` | `41_F18_Fixture_Inputs/P19.json` |
| P20 | parser | Assumption cites an unknown clause ID. | `REPAIR` — `SCHEMA_REJECT|pointer=/assumptions/0/clause_id` | `41_F18_Fixture_Inputs/P20.json` |
| P21 | parser | UNSPECIFIED used with a non-empty description of missing behavior. | `ACCEPT` — `None` | `41_F18_Fixture_Inputs/P21.json` |
| P22 | parser | Malformed individual diagnostic item with valid PASS verdict. | `ACCEPT_WITH_WARNING` — `DIAGNOSTIC_FORMAT_WARNING` | `41_F18_Fixture_Inputs/P22.json` |
| P23 | parser | Dotted submodule import collections.abc. | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=SUBMODULE_IMPORT` | `41_F18_Fixture_Inputs/P23.json` |
| P24a | parser | Prohibited built-in name reference exec. | `REPAIR` — `PROHIBITED_BUILTIN|name=exec` | `41_F18_Fixture_Inputs/P24a.json` |
| P24b | parser | Prohibited built-in name reference eval. | `REPAIR` — `PROHIBITED_BUILTIN|name=eval` | `41_F18_Fixture_Inputs/P24b.json` |
| P24c | parser | Prohibited built-in name reference compile. | `REPAIR` — `PROHIBITED_BUILTIN|name=compile` | `41_F18_Fixture_Inputs/P24c.json` |
| P24d | parser | Prohibited built-in name reference open. | `REPAIR` — `PROHIBITED_BUILTIN|name=open` | `41_F18_Fixture_Inputs/P24d.json` |
| P25a | parser | Python syntax error in driver.py. | `REPAIR` — `SOURCE_SYNTAX_REJECT|file=driver.py|line=1|column=5` | `41_F18_Fixture_Inputs/P25a.json` |
| P25b | parser | Python syntax error in checker.py. | `REPAIR` — `SOURCE_SYNTAX_REJECT|file=checker.py|line=1|column=5` | `41_F18_Fixture_Inputs/P25b.json` |
| P26 | parser | Checker source uses wrong parameter names. | `REPAIR` — `ENTRY_POINT_REJECT|file=checker.py|symbol=check_trace|reason=PARAMETER_NAMES` | `41_F18_Fixture_Inputs/P26.json` |
| P27 | parser | Driver class has a decorator. | `REPAIR` — `DECORATOR_REJECT|file=driver.py|symbol=Driver` | `41_F18_Fixture_Inputs/P27.json` |
| P28 | parser | Module-level call before definitions. | `REPAIR` — `MODULE_STATEMENT_REJECT|file=driver.py|line=1|reason=MODULE_EXECUTABLE` | `41_F18_Fixture_Inputs/P28.json` |
| P29a | parser | Relative import. | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=RELATIVE_IMPORT` | `41_F18_Fixture_Inputs/P29a.json` |
| P29b | parser | Star import. | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=STAR_IMPORT` | `41_F18_Fixture_Inputs/P29b.json` |
| P30 | parser | Disallowed future feature. | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=FUTURE_FEATURE` | `41_F18_Fixture_Inputs/P30.json` |
| P31 | parser | One ast.Import node containing multiple names | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=MULTIPLE_NAMES` | `41_F18_Fixture_Inputs/P31.json` |
| P32 | parser | Disallowed root wins over dotted-submodule classification | `REPAIR` — `IMPORT_NOT_ALLOWED|module=os` | `41_F18_Fixture_Inputs/P32.json` |
| P33 | parser | Allowed root with alias is rejected | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=IMPORT_ALIAS` | `41_F18_Fixture_Inputs/P33.json` |
| P34 | parser | The sole permitted future import with an alias is rejected | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=IMPORT_ALIAS` | `41_F18_Fixture_Inputs/P34.json` |
| P35 | parser | Disallowed from-import root wins over generic from-import rejection | `REPAIR` — `IMPORT_NOT_ALLOWED|module=os` | `41_F18_Fixture_Inputs/P35.json` |
| P36 | parser | Non-future from-import from allowed root is forbidden | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=FROM_IMPORT_FORBIDDEN` | `41_F18_Fixture_Inputs/P36.json` |
| P37 | parser | Relative import wins over star-import reason | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=RELATIVE_IMPORT` | `41_F18_Fixture_Inputs/P37.json` |
| P38 | parser | Star import wins over future-feature reason | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=STAR_IMPORT` | `41_F18_Fixture_Inputs/P38.json` |
| P39 | parser | Multi-name future import uses MULTIPLE_NAMES before future-feature classification | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=MULTIPLE_NAMES` | `41_F18_Fixture_Inputs/P39.json` |
| P40 | parser | Multiple names wins before per-root inspection | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=MULTIPLE_NAMES` | `41_F18_Fixture_Inputs/P40.json` |
| P41 | parser | from-import from permitted root with alias is still rejected as FROM_IMPORT_FORBIDDEN | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=FROM_IMPORT_FORBIDDEN` | `41_F18_Fixture_Inputs/P41.json` |
| P42 | parser | Exact future annotations import is permitted | `ACCEPT` — `null` | `41_F18_Fixture_Inputs/P42.json` |
| P43 | parser | Disallowed root with alias reports root violation first | `REPAIR` — `IMPORT_NOT_ALLOWED|module=os` | `41_F18_Fixture_Inputs/P43.json` |
| P44 | parser | Dotted allowed-root import with alias; submodule precedes alias | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=SUBMODULE_IMPORT` | `41_F18_Fixture_Inputs/P44.json` |
| P45 | parser | Unsupported future feature with alias; future-feature precedes alias | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=FUTURE_FEATURE` | `41_F18_Fixture_Inputs/P45.json` |
| P46 | parser | Disallowed root with from-import alias; root precedes alias | `REPAIR` — `IMPORT_NOT_ALLOWED|module=os` | `41_F18_Fixture_Inputs/P46.json` |
| P47 | parser | Relative from-import with a module path | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=RELATIVE_IMPORT` | `41_F18_Fixture_Inputs/P47.json` |
| P48 | parser | Duplicate future annotations names use MULTIPLE_NAMES | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=MULTIPLE_NAMES` | `41_F18_Fixture_Inputs/P48.json` |
| R01 | repair | driver compile error only | `REPAIR` — `COMPILE_ERROR|file=driver.py|line=1` | `41_F18_Fixture_Inputs/R01.json` |
| R02 | repair | checker compile error only | `REPAIR` — `COMPILE_ERROR|file=checker.py|line=1` | `41_F18_Fixture_Inputs/R02.json` |
| R03 | repair | Import violation and compile error; import precedes compilation | `REPAIR` — `IMPORT_NOT_ALLOWED|module=os` | `41_F18_Fixture_Inputs/R03.json` |
| R04 | repair | Driver step raises KeyError | `REPAIR` — `RUNTIME_EXCEPTION|file=driver.py|phase=step|class=KeyError` | `41_F18_Fixture_Inputs/R04.json` |
| R05 | repair | Driver vector has wrong width | `REPAIR` — `DRIVER_VECTOR_INVALID|reason=WRONG_WIDTH` | `41_F18_Fixture_Inputs/R05.json` |
| R06 | repair | Driver watchdog expires | `REPAIR` — `WATCHDOG_TIMEOUT|phase=driver_step` | `41_F18_Fixture_Inputs/R06.json` |
| R07 | repair | Design-level baseline has masked output divergence under identical inputs | `DESIGN_HALT_NO_SLOT_SCORED` — `RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE` | `41_F18_Fixture_Inputs/R07.json` |
| R08 | repair | Both checker null runs raise the same KeyError | `REPAIR` — `CHECKER_RUNTIME_ERROR|class=KeyError` | `41_F18_Fixture_Inputs/R08.json` |
| R09 | repair | Both checker null runs return FAIL | `REPAIR` — `The checker returned FAIL on a legal null-netlist trace.` | `41_F18_Fixture_Inputs/R09.json` |
| R10 | repair | Checker null-run verdicts disagree PASS then FAIL | `TERMINAL_INVALID_NO_REPAIR` — `CHECKER_NONDETERMINISM|reason=RUN_DISAGREEMENT` | `41_F18_Fixture_Inputs/R10.json` |
| R11 | repair | Checker runtime error on one run and PASS on the other | `TERMINAL_INVALID_NO_REPAIR` — `CHECKER_NONDETERMINISM|reason=RUN_DISAGREEMENT` | `41_F18_Fixture_Inputs/R11.json` |
| R12 | repair | Harness row-alignment integrity failure | `DESIGN_HALT_NO_SLOT_SCORED` — `TRACE_INTEGRITY_FAILURE|reason=ROW_ALIGNMENT` | `41_F18_Fixture_Inputs/R12.json` |
| R13 | repair | Multiple failures: schema rejection and static import violation | `REPAIR` — `SCHEMA_REJECT|pointer=/driver` | `41_F18_Fixture_Inputs/R13.json` |
| M01 | missing-case | Driver defines __init__; required entry points pass, then the forbidden method rule wins | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=Driver.__init__|reason=FORBIDDEN_METHOD` | `41_F18_Fixture_Inputs/M01.json` |
| M02 | missing-case | Top-level helper class in checker.py is CLASS_FORBIDDEN after required symbols pass | `REPAIR` — `ENTRY_POINT_REJECT|file=checker.py|symbol=Helper|reason=CLASS_FORBIDDEN` | `41_F18_Fixture_Inputs/M02.json` |
| M03 | missing-case | Decorator such as dataclass or staticmethod | `REPAIR` — `DECORATOR_REJECT|file=driver.py|symbol=Driver` | `41_F18_Fixture_Inputs/M03.json` |
| M04a | missing-case | Non-literal module constant | `REPAIR` — `MODULE_STATEMENT_REJECT|file=driver.py|line=1|reason=NON_LITERAL_CONSTANT` | `41_F18_Fixture_Inputs/M04a.json` |
| M04b | missing-case | Module-level if __name__ guard | `REPAIR` — `MODULE_STATEMENT_REJECT|file=driver.py|line=1|reason=MODULE_CONTROL_FLOW` | `41_F18_Fixture_Inputs/M04b.json` |
| M05 | missing-case | Positional-only factory parameter | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=create_driver|reason=PARAMETER_KIND` | `41_F18_Fixture_Inputs/M05.json` |
| M06 | missing-case | Factory returns non-Driver object | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=create_driver|reason=RETURN_TYPE` | `41_F18_Fixture_Inputs/M06.json` |
| M07 | missing-case | re.compile is explicitly permitted | `ACCEPT` — `None` | `41_F18_Fixture_Inputs/M07.json` |
| M08a | missing-case | from collections import abc is prohibited | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=FROM_IMPORT_FORBIDDEN` | `41_F18_Fixture_Inputs/M08a.json` |
| M08b | missing-case | import collections.abc is prohibited | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=SUBMODULE_IMPORT` | `41_F18_Fixture_Inputs/M08b.json` |
| M09 | missing-case | Global random.random use is prohibited | `REPAIR` — `GLOBAL_RANDOM_USE|name=random.random` | `41_F18_Fixture_Inputs/M09.json` |
| M10 | missing-case | Checker timeout on null trace | `REPAIR` — `CHECKER_TIMEOUT|phase=null_check` | `41_F18_Fixture_Inputs/M10.json` |
| M11 | missing-case | Different checker crash exception classes across null runs | `TERMINAL_INVALID_NO_REPAIR` — `CHECKER_NONDETERMINISM|reason=RUN_DISAGREEMENT` | `41_F18_Fixture_Inputs/M11.json` |
| M12 | missing-case | Malformed diagnostic on one run but both verdicts PASS | `ACCEPT_WITH_WARNING` — `DIAGNOSTIC_FORMAT_WARNING` | `41_F18_Fixture_Inputs/M12.json` |
| M13 | missing-case | Simulator error on null run | `DESIGN_HALT_NO_SLOT_SCORED` — local error class `EVALUATOR_INFRASTRUCTURE_FAILURE`; diagnostic `SIMULATOR_ERROR|target=null|class=RuntimeError` | `41_F18_Fixture_Inputs/M13.json` |
| M14 | missing-case | Grammar-exempt UTF-8 truncation primitive unit vector; input is deliberately non-grammar and tests the truncation primitive only | `CONTROL_EXPECTATION` — output diagnostic 2,047 bytes including 14-byte marker; valid UTF-8; truncation primitive only | `41_F18_Fixture_Inputs/M14.json` |
| M15 | missing-case | Non-normative path-bearing diagnostic is rejected by the closed feedback serializer (no redaction stage). | `CONTROL_EXPECTATION` — `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` | `41_F18_Fixture_Inputs/M15.json` |
| M16 | missing-case | Both source files empty; driver.py has precedence | `REPAIR` — `SOURCE_EMPTY|file=driver.py` | `41_F18_Fixture_Inputs/M16.json` |
| M17 | missing-case | Grammar-exempt JSON-escaping primitive unit vector; not an end-to-end feedback acceptance test | `CONTROL_EXPECTATION` — exact JSON UTF-8 output bytes and SHA-256 recorded in fixture; JSON-escaping primitive only | `41_F18_Fixture_Inputs/M17.json` |
| M18 | missing-case | Payload line equal to reserved block heading | `F18_REJECT` — `PACKET_FREEZE_REJECT|reason=RESERVED_HEADING_LINE` | `41_F18_Fixture_Inputs/M18.json` |
| M19 | missing-case | Unresolved double-brace placeholder | `F18_REJECT` — `ASSEMBLY_REJECT|reason=UNRESOLVED_PLACEHOLDER` | `41_F18_Fixture_Inputs/M19.json` |
| M20 | missing-case | Visible clause ID absent from manifest clause_ids | `F18_REJECT` — `F18_REJECT|reason=VISIBLE_CLAUSE_ID_SET_MISMATCH` | `41_F18_Fixture_Inputs/M20.json` |
| M21 | missing-case | Import alias is prohibited | `REPAIR` — `IMPORT_FORM_REJECT|file=driver.py|line=1|reason=IMPORT_ALIAS` | `41_F18_Fixture_Inputs/M21.json` |
| M22 | missing-case | random.SystemRandom is prohibited | `REPAIR` — `GLOBAL_RANDOM_USE|name=random.SystemRandom` | `41_F18_Fixture_Inputs/M22.json` |
| M23 | missing-case | random.randint module-global call is prohibited | `REPAIR` — `GLOBAL_RANDOM_USE|name=random.randint` | `41_F18_Fixture_Inputs/M23.json` |
| M24 | missing-case | builtins.open attribute is prohibited | `REPAIR` — `PROHIBITED_BUILTIN|name=open` | `41_F18_Fixture_Inputs/M24.json` |
| M25 | missing-case | Runtime inspect.signature mismatch after successful static AST check | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=Driver.step|reason=RUNTIME_SIGNATURE` | `41_F18_Fixture_Inputs/M25.json` |
| M26 | missing-case | Driver vector contains an extra key | `REPAIR` — `DRIVER_VECTOR_INVALID|reason=EXTRA_KEYS` | `41_F18_Fixture_Inputs/M26.json` |
| M27 | missing-case | Driver vector passes the key, type, width and symbol checks and violates the supplied legal-input predicate | `REPAIR` — `DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE` | `41_F18_Fixture_Inputs/M27.json` |
| M28 | missing-case | Artifact paired runs diverge in next-input schedule before any raw output divergence | `TERMINAL_INVALID_NO_REPAIR` — `DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE` | `41_F18_Fixture_Inputs/M28.json` |
| M29 | missing-case | AST node order tie uses file order driver.py before checker.py | `REPAIR` — `IMPORT_NOT_ALLOWED|module=os` | `41_F18_Fixture_Inputs/M29.json` |
| M30 | missing-case | Non-empty third-party dependency array is rejected by the response schema. | `REPAIR` — `SCHEMA_REJECT|pointer=/dependencies` | `41_F18_Fixture_Inputs/M30.json` |
| M31 | missing-case | Checker return object has an extra top-level key | `REPAIR` — `CHECKER_RETURN_INVALID|reason=TOP_LEVEL_KEYS` | `41_F18_Fixture_Inputs/M31.json` |
| M32 | missing-case | Checker return object has an invalid verdict | `REPAIR` — `CHECKER_RETURN_INVALID|reason=INVALID_VERDICT` | `41_F18_Fixture_Inputs/M32.json` |
| M33 | missing-case | Checker return object has a non-list diagnostics field | `REPAIR` — `CHECKER_RETURN_INVALID|reason=DIAGNOSTICS_NOT_LIST` | `41_F18_Fixture_Inputs/M33.json` |
| M34 | missing-case | Prohibited __import__ name use inside checker function | `REPAIR` — `PROHIBITED_BUILTIN|name=__import__` | `41_F18_Fixture_Inputs/M34.json` |
| M35 | missing-case | Non-ASCII identifier is rejected before later static stages | `REPAIR` — `NON_ASCII_IDENTIFIER|file=checker.py|line=2|column=5` | `41_F18_Fixture_Inputs/M35.json` |
| M36 | missing-case | SyntaxError with absent/null offset uses column=1 | `CONTROL_EXPECTATION` — `SOURCE_SYNTAX_REJECT|file=driver.py|line=4|column=1` | `41_F18_Fixture_Inputs/M36.json` |
| M37 | missing-case | Paired-outcome control vector (OS-2): a supplied paired-run outcome with next-input divergence before the first raw-output divergence; the documented aliased global random access is not detected from the source | `TERMINAL_INVALID_NO_REPAIR` — `DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE` | `41_F18_Fixture_Inputs/M37.json` |
| M38 | missing-case | Decorated module-level helper function is rejected at AST_SIGNATURE | `REPAIR` — `DECORATOR_REJECT|file=driver.py|symbol=helper` | `41_F18_Fixture_Inputs/M38.json` |
| M39 | missing-case | Nested class inside a function uses canonical lexical symbol helper.Nested | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=helper.Nested|reason=NESTED_CLASS_FORBIDDEN` | `41_F18_Fixture_Inputs/M39.json` |
| M40 | missing-case | Malformed clause-like token FIFO-01 is rejected as a near-match | `F18_REJECT` — `F18_REJECT|reason=MALFORMED_CLAUSE_ID_TOKEN` | `41_F18_Fixture_Inputs/M40.json` |
| M41 | missing-case | One recoverable mid-run evaluator halt triggers a full design-wide rerun using frozen artifacts | `CONTROL_EXPECTATION` — `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` | `41_F18_Fixture_Inputs/M41.json` |
| M42 | missing-case | The same design-halt signature recurring after one recovery aborts the design | `DESIGN_ABORTED_NO_SLOTS_SCORED` — `DESIGN_HALT_REPEATED|reason=EVALUATOR_FAILURE_REPRODUCED` | `41_F18_Fixture_Inputs/M42.json` |
| M43 | missing-case | Non-ASCII identifier after multibyte string literal; UTF-8 byte column at token start | `REPAIR` — `NON_ASCII_IDENTIFIER|file=checker.py|line=2|column=19` | `41_F18_Fixture_Inputs/M43.json` |
| M44 | missing-case | Non-ASCII imported identifier wins over import-root classification on same statement | `REPAIR` — `NON_ASCII_IDENTIFIER|file=driver.py|line=1|column=8` | `41_F18_Fixture_Inputs/M44.json` |
| M45 | missing-case | Non-ASCII attribute identifier is rejected as a NAME token | `REPAIR` — `NON_ASCII_IDENTIFIER|file=checker.py|line=2|column=17` | `41_F18_Fixture_Inputs/M45.json` |
| M46 | missing-case | Non-ASCII helper function name is rejected before entry-point checks | `REPAIR` — `NON_ASCII_IDENTIFIER|file=checker.py|line=1|column=5` | `41_F18_Fixture_Inputs/M46.json` |
| M47 | missing-case | A second different design halt after the single recovery cycle aborts the design | `DESIGN_ABORTED_NO_SLOTS_SCORED` — `DESIGN_HALT_REPEATED|reason=SECOND_HALT_AFTER_RECOVERY` | `41_F18_Fixture_Inputs/M47.json` |
| M48 | missing-case | A frozen evaluator binary/source/configuration change requires a new evaluator version and F16 before full rerun | `CONTROL_EXPECTATION` — `EVALUATOR_REVISION_REQUIRED|reason=FROZEN_EVALUATOR_CHANGED` | `41_F18_Fixture_Inputs/M48.json` |
| M49 | missing-case | Required create_driver check precedes forbidden Driver.__init__ on multi-defect input | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=create_driver|reason=MISSING_ENTRY_POINT` | `41_F18_Fixture_Inputs/M49.json` |
| M50 | missing-case | Shared author-visible/estimand revision invalidates every arm × design slot and requires a new preregistration; old artifacts are not reusable | `CONTROL_EXPECTATION` — `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | `41_F18_Fixture_Inputs/M50.json` |

| M51 | missing-case | Nested class category outranks an earlier decorated helper in the same file | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=nested_holder.Nested|reason=NESTED_CLASS_FORBIDDEN` | `41_F18_Fixture_Inputs/M51.json` |
| M52 | missing-case | Global category rank makes checker.py nested class outrank driver.py decorator | `REPAIR` — `ENTRY_POINT_REJECT|file=checker.py|symbol=nested_holder.Nested|reason=NESTED_CLASS_FORBIDDEN` | `41_F18_Fixture_Inputs/M52.json` |
| M53 | missing-case | Design-membership, estimand or weight change after confirmatory start requires a new preregistered study and archived/disclosed partial ledgers | `CONTROL_EXPECTATION` — `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | `41_F18_Fixture_Inputs/M53.json` |
| M54 | missing-case | Halt-signature fields, enumerated values and reason-to-component mapping are closed and exclude volatile metadata | `CONTROL_EXPECTATION` — `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED` | `41_F18_Fixture_Inputs/M54.json` |
| M55 | missing-case | U+2118 identifier is rejected even when Python 3.11 tokenize may emit it as ERRORTOKEN | `REPAIR` — `NON_ASCII_IDENTIFIER|file=driver.py|line=1|column=1` | `41_F18_Fixture_Inputs/M55.json` |
| M56 | missing-case | Non-ASCII XID_Continue character in ASCII-prefixed identifier is rejected at complete lexeme start | `REPAIR` — `NON_ASCII_IDENTIFIER|file=checker.py|line=2|column=5` | `41_F18_Fixture_Inputs/M56.json` |
| M57 | missing-case | Unicode inside strings, docstrings and comments remains permitted | `ACCEPT` — `null` | `41_F18_Fixture_Inputs/M57.json` |
| M58 | missing-case | Design-specific author-visible change invalidates both arms for the affected design only | `CONTROL_EXPECTATION` — `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | `41_F18_Fixture_Inputs/M58.json` |

M14 and M17 are explicitly grammar-exempt primitive unit vectors. M14 tests the UTF-8 truncation primitive in isolation; M17 tests JSON escaping in isolation. Their deliberately non-grammar inputs are not accepted by the production serializer, which performs closed-grammar validation before invoking either primitive.


## Async-comprehension rule and fixtures

An asynchronous comprehension is an `ast.GeneratorExp`, `ast.ListComp`, `ast.SetComp` or `ast.DictComp` with at least one associated `ast.comprehension.is_async == 1` **or any `ast.Await` node anywhere in its AST subtree**. Python treats a generator expression containing `await` as asynchronous even if all `is_async` flags are zero. The global AST_SIGNATURE pass assigns this category rank 7 with reason `ASYNC_COMPREHENSION`, after required-symbol checks and category ranks 1–6. The expression symbol is the dot-joined names of all ancestor `FunctionDef`, `AsyncFunctionDef` and `ClassDef` nodes in AST ancestry, outermost first; header expressions in defaults, annotations, bases, decorators and keywords therefore have a deterministic definition symbol. A `<module>` symbol is unreachable after IMPORT_POLICY rejects module-body expressions. Standalone `await`, `async for` and `async with` statements in synchronous function bodies, when not within a comprehension expression caught by rank 7, are rejected at `COMPILE_DRIVER`/`COMPILE_CHECKER` as `COMPILE_ERROR`. M65/M66 cover `async for` generator expressions, M67–M69 cover the async-precedence cases, and M70 covers a generator expression containing `await` with all `is_async` flags set to zero.

## Execution gate

Fixture descriptors in index: **144**. Mandatory count must equal the number of descriptor files and catalog rows. The fixture runner verifies each descriptor's SHA-256 and byte length before loading its input, executes every mandatory case under pinned Python 3.11 and parser/schema versions, and compares the actual result with the expected object. When the expected object has exactly the keys `disposition`, `stage_id`, `error_class` and `diagnostic`, those four values are compared exactly. Any other expected object is a control-vector expectation: its whole object is compared exactly, key set included, and every property it names must be defined by a rule in the Protocol (Protocol §20, OWNER-DECIDED OD-3, lists every control-vector property and its rule). Any unresolved expectation fails F18. Development-run evidence: development runs are not F18 acceptance; Formal F18 status: **NOT RUN / NOT PASSED**; Approval: nothing is approved (see the status line at the top of this file).

| M59 | missing-case | A valid nested `async def` inside a synchronous helper is prohibited at `AST_SIGNATURE` | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=helper.nested_async|reason=ASYNC_DEFINITION` | `41_F18_Fixture_Inputs/M59.json` |
| M60 | missing-case | Async module-level `create_driver` binding is rejected by required-symbol precedence | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=create_driver|reason=WRONG_ENTRY_POINT_KIND` | `41_F18_Fixture_Inputs/M60.json` |
| M61 | missing-case | Async direct `Driver.step` binding is rejected by required-symbol precedence | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=Driver.step|reason=WRONG_ENTRY_POINT_KIND` | `41_F18_Fixture_Inputs/M61.json` |
| M62 | missing-case | Non-ASCII continuation character in driver identifier is rejected at lexeme start (UTF-8 byte column 1) | `REPAIR` — `NON_ASCII_IDENTIFIER|file=driver.py|line=1|column=1` | `41_F18_Fixture_Inputs/M62.json` |
| M63 | missing-case | Non-ASCII identifier-start character emitted as ERRORTOKEN is rejected (UTF-8 byte column 5) | `REPAIR` — `NON_ASCII_IDENTIFIER|file=driver.py|line=1|column=5` | `41_F18_Fixture_Inputs/M63.json` |
| M64 | missing-case | Non-ASCII checker identifier after a multibyte string is rejected using UTF-8 byte column 15 | `REPAIR` — `NON_ASCII_IDENTIFIER|file=checker.py|line=2|column=15` | `41_F18_Fixture_Inputs/M64.json` |
| M65 | missing-case | Async generator expression in a synchronous driver helper is explicitly rejected by AST_SIGNATURE category rank 7 | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=helper|reason=ASYNC_COMPREHENSION` | `41_F18_Fixture_Inputs/M65.json` |
| M66 | missing-case | Async generator expression in synchronous check_trace is explicitly rejected by AST_SIGNATURE category rank 7 | `REPAIR` — `ENTRY_POINT_REJECT|file=checker.py|symbol=check_trace|reason=ASYNC_COMPREHENSION` | `41_F18_Fixture_Inputs/M66.json` |
| M67 | missing-case | Async required checker entry point is rejected by the required-symbol pass | `REPAIR` — `ENTRY_POINT_REJECT|file=checker.py|symbol=check_trace|reason=WRONG_ENTRY_POINT_KIND` | `41_F18_Fixture_Inputs/M67.json` |
| M68 | missing-case | Extra direct async Driver method is rejected by category rank 3 before async-definition rank 6 | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=Driver.extra|reason=FORBIDDEN_METHOD` | `41_F18_Fixture_Inputs/M68.json` |
| M69 | missing-case | Decorated async helper is rejected by decorator category rank 5 before async-definition rank 6 | `REPAIR` — `DECORATOR_REJECT|file=driver.py|symbol=helper` | `41_F18_Fixture_Inputs/M69.json` |
| M70 | missing-case | Generator expression containing `await` is rejected by rank 7 even when every `comprehension.is_async` flag is zero | `REPAIR` — `ENTRY_POINT_REJECT|file=driver.py|symbol=helper|reason=ASYNC_COMPREHENSION` | `41_F18_Fixture_Inputs/M70.json` |

## Input shapes of control and lifecycle vectors (v1.3.7 candidate, C12–C16)

Each shape below is the complete input of a fixture; a property outside its stated domain is an input error, not an outcome. A property whose value the Protocol fixes must equal that value and does not change the result.

- **Serializer-grammar vector** (C12): `diagnostic` (a string) and, optionally, `allowed_diagnostics` (the duplicate-free list of diagnostics the stage map emitted). It applies Protocol §3.4 feedback-serialization step (1): the closed grammar, then membership when the list is given. A failure is the `FEEDBACK_SERIALIZER_REJECT` record; a pass has no record to compare.
- **Truncation-primitive vector** (C13): `raw_diagnostic` (a string); `raw_diagnostic_utf8_bytes` (its UTF-8 byte length); `byte_cap` = `2048`; `marker` = `...[TRUNCATED]`; `truncate_on_utf8_boundary` = `true`; `truncate_before_json_escape` = `true`; `test_scope` = `TRUNCATION_PRIMITIVE_ONLY_GRAMMAR_BYPASSED`. The result is the step (2) control vector of Protocol §3.4.
- **JSON-escaping-primitive vector** (C14): `feedback_object` (exactly the string keys `stage_id`, `error_class`, `diagnostic`); `encoding` = `UTF-8`; `ensure_ascii` = `false`; `indent` = `2`; `line_endings` = `LF`; `terminal_newline` = `true`; `grammar_exempt_for_primitive_test` = `true`; `test_scope` = `JSON_ESCAPING_PRIMITIVE_ONLY_GRAMMAR_BYPASSED`. The result is the step (3) control vector of Protocol §3.4, keys serialized in the order `stage_id`, `error_class`, `diagnostic`.
- **Lifecycle halt-event vector** (C15): `lifecycle` = `MID_RUN` (the halt occurs after slots have begun, §7b); `event`, one stage-map event of kind `simulator_error` (`target` `rtl` or `null`, `exception_class`) or `trace_integrity` (`reason`); `slots` with non-negative integers `scheduled` (at least 1), `previously_evaluated`, `triggering_slot` (1 to `scheduled`) and `remaining`, where `previously_evaluated` + 1 + `remaining` = `scheduled`; `evaluator_repair_attempt` = `1`, the ordinal of the recovery cycle this halt opens (OWNER-DECIDED OD-4, Protocol §7b L185; §7b allows one; a halt after that cycle is a recurrence, given as two halt signatures). The result is the event's stage-map row with disposition `DESIGN_HALT_NO_SLOT_SCORED`; the slot counts do not change it.
- **Design-preflight vector** (C16): `design_preflight`, an object with exactly the Boolean `rtl_null_masked_divergence`. `true` is the §7a baseline mismatch record; `false` passes the gate, with no record to compare.

## Owner-specified vector inputs (v1.3.7 candidate, OWNER-SPECIFIED OS-1–OS-3, owner decision D-026)

These items are OWNER-SPECIFIED, not derived from pack text: the Protocol fixes each expected outcome, and owner decision D-026 specifies only how the vector reaches the stage that outcome names. They add no outcome code. A property outside its stated domain, or an input for which neither these items nor the Protocol states an outcome, is an input error, not an outcome.

- **Operational-recovery vector** (OS-1, §7b): `design_id` (`FIFO` or `UART`, equal to the `design_id` of `halt_signature`); `halt_signature`, the halt's signature in the Protocol §7b domains, with `halt_code` `SIMULATOR_ERROR` or `TRACE_INTEGRITY_FAILURE` (a masked RTL/null divergence may use operational recovery only after a root-cause review, which this vector does not carry); `slots` as in the lifecycle halt-event vector, so the halt occurred after slots had begun; `evaluator_repair_attempt` = `1` (OWNER-DECIDED OD-4, Protocol L185); `recovery_mode` = `OPERATIONAL_RECOVERY`; the Booleans `frozen_evaluator_hashes_unchanged`, `f16_required`, `same_artifact_bytes` and `author_visible_materials_changed`; `pre_halt_scored_slots` (1 to `previously_evaluated`), the number of pre-halt scores; `scheduled_slots` = `scheduled`, the scheduled slots of the affected scope; `same_artifacts_for_all_slots` = `true`, `same_slot_seeds` = `true` and `new_generation_calls` = `0`, which restate §7b; and `required_action`, a string that is an informational label, not an outcome input. Only the properties named by the §7b recovery conditions decide the outcome. When `frozen_evaluator_hashes_unchanged` is `true`, `f16_required` is `false`, `same_artifact_bytes` is `true` and `author_visible_materials_changed` is `false`, the result is the successful-operational-recovery control expectation of Protocol §3.4 at stage `DESIGN_HALT` with disposition `CONTROL_EXPECTATION` and the properties `discard_pre_halt_scores` = `true`, `rerun_slots` = `scheduled_slots`, `reuse_same_artifact_bytes` = `true` and `new_confirmatory_generation_calls` = `0`. When the frozen evaluator hashes changed (`frozen_evaluator_hashes_unchanged` is `false`, `f16_required` is `true`, `same_artifact_bytes` is `true` and `author_visible_materials_changed` is `false`), the recovery is an evaluator revision and the result is the change-class control expectation of `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED`. The Protocol states no outcome for any other combination, including an author-visible change, which §7b sends to a study or design revision that the vector does not identify; such an input is outside this vector's scope.
- **Paired-run outcome vector** (OS-2; a paired-outcome control vector, not a test of source-level alias detection): `response_object` (a response object, as for any response input) and `runtime_pair`, an object with exactly `driver_source_excerpt` (a string that documents the access under test; it is not executed, matched or read for the outcome) and the Booleans `before_first_raw_output_divergence` and `next_input_schedules_equal`. Protocol §3.4 evaluation steps (1)–(6) run on the response object, and their first failure is the result. If all pass, `runtime_pair` stands in for steps (7)–(8), the paired run, which is not executed: `before_first_raw_output_divergence` = `true` with `next_input_schedules_equal` = `false` is the `DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE` row of the stage map. Any other pair does not determine the paired run's outcome and is outside this vector's scope. The vector therefore tests the supplied paired-run outcome and the precedence of the static stages; it does not show that the response contains the access its excerpt documents.
- **Runtime driver-vector input** (OS-3): `response_object` with `port_manifest` (`input_ports`). Its expected stage, `DRIVER_VECTOR`, is checked within evaluation step (7), while `Driver.step` runs on the original RTL; the input gives no design, RTL or port widths, and no rule states how the driver's vector is obtained outside that run. This input is not specified, and a fixture with it stays NOT_IMPLEMENTED.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
