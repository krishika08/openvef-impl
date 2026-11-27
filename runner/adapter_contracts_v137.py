"""Pack citations for the candidate-only adapters (D-024; v1.3.7 CANDIDATE, not audited).

Data only, in the format of runner/adapter_contracts.py (D-013, D-015, D-017, D-022). Every citation is to the
candidate pack, proposals/v1.3.7/pack; its lines are numbered as in v1.3.6. tests/test_dispatch_shapes_v137.py
checks these against the candidate text with the same functions that check the v1.3.6 contracts.
"""
from __future__ import annotations

from adapter_contracts import LITERAL
from adapters_v137 import CHANGE_CLASSES, DOMAIN_VALIDATIONS

_CC_SENTENCE = {
    CHANGE_CLASSES[0]: "is the evaluator revision of §7b path (b)",
    CHANGE_CLASSES[1]: "is a shared-item revision",
    CHANGE_CLASSES[2]: "is a study reset",
    CHANGE_CLASSES[3]: "is a design-specific revision while membership, estimand and weights remain unchanged",
}
# D-027 OD-3: the §20 table of the candidate Protocol (appended after v1.3.6's last line, L559).
_L20_CC, _L20_DV = ("02", 571), ("02", 572)
_DV = DOMAIN_VALIDATIONS[0]
_SCHEMA = [("02", 176, "The input contract and the complete result schema of every control vector are the normative "
                       "tables of §20 (OWNER-DECIDED OD-3)."),
           ("02", 563, "The owners adopt the tables below as normative."),
           ("02", 175, "Error classes of change-class control expectations are stated by rule, not by fixture"),
           ("36", 176, "Any other expected object is a control-vector expectation")]

CONTRACTS = {
    "adapt_change_class": {
        "inputs": {"change_class": (*_L20_CC, "| Change-class vector | `change_class` | string | exactly one of")},
        "values": {cc: ("02", 176, f"`{cc}` {words}") for cc, words in _CC_SENTENCE.items()},
        "outcome": [*_SCHEMA, ("02", 176, "Closed scope tokens (OWNER-DECIDED OD-3")]},
    "adapt_domain_validation": {
        "inputs": {"domain_validation": (*_L20_DV, f"| Domain-validation vector | `domain_validation` | string | "
                                                   f"exactly `{_DV}` |")},
        "values": {_DV: (*_L20_DV, f"exactly `{_DV}`")},
        "outcome": [*_SCHEMA,
                    ("02", 176, f"`{_DV}` is not a change class: it names the halt-signature domain validation"),
                    ("02", 185, "(rule token `stable_error_class_rule` = `simple_exception_class_for_SIMULATOR_ERROR_else_NONE`)")]},
    "adapt_parser_unit_vector": {
        "inputs": {"source_file": ("36", 27, "`source_file` is `driver.py` or `checker.py`."),
                   "syntax_error": ("36", 27, "`syntax_error` has the key `lineno`, a positive integer, and may have the "
                                              "key `offset`, an integer or null.")},
        "values": {"driver.py": ("36", 27, "`source_file` is `driver.py` or `checker.py`."),
                   "checker.py": ("36", 27, "`source_file` is `driver.py` or `checker.py`.")},
        "outcome": [("36", 27, "Its result has stage `SOURCE_AST`, error class `SOURCE_SYNTAX_REJECT`, the diagnostic "
                               "given by the rule, and disposition `CONTROL_EXPECTATION`."),
                    ("02", 127, "If `offset` is absent, null or less than 1, emit `column=1`")]},
    "adapt_legal_input": {
        "inputs": {"driver_return": ("30", 83, "A return value is either the exact string `COMPLETE` or a dictionary"),
                   "input_port_widths": ("30", 83, "`input_port_widths` (each input port name mapped to its width)"),
                   "sampled_outputs": ("30", 83, "`sampled_outputs` (the outputs sampled in the same row)"),
                   "legal_input_predicate": ("30", 83, "`legal_input_predicate` (an object with `language` = `python3.11`, "
                                                       "`function`, the function's name, `source`, its Python source, and "
                                                       "`source_sha256`, the lowercase hexadecimal SHA-256 of `source` in "
                                                       "UTF-8, which is the frozen hash of OD-2)")},
        "values": {"python3.11": ("30", 83, "an object with `language` = `python3.11`")},
        "outcome": [("30", 83, "Checks (a) to (e) run in that order and the first failure is reported."),
                    ("30", 83, "Any other outcome, including an exception, is an evaluator failure and is never an "
                               "artifact verdict."),
                    ("30", 83, "the evaluator executes it only after checking that the source has that hash; a mismatch "
                               "is an evaluator failure."),
                    ("02", 152, "Driver return value/vector is invalid")]},
}

VALUE_SUPPORT = {
    "adapt_change_class": {cc: (LITERAL, f"`{cc}`") for cc in CHANGE_CLASSES},
    "adapt_domain_validation": {_DV: (LITERAL, f"`{_DV}`")},
    "adapt_parser_unit_vector": {"driver.py": (LITERAL, "`driver.py`"), "checker.py": (LITERAL, "`checker.py`")},
    "adapt_legal_input": {"python3.11": (LITERAL, "`python3.11`")},
}

DOMAINS = {
    "adapt_change_class": {"change_class": {
        "lines": [("02", 176), _L20_CC],
        "terms": ["The change classes are closed and have exactly four cases", "exactly one of",
                  *(f"`{cc}`" for cc in CHANGE_CLASSES)]}},
    "adapt_domain_validation": {"domain_validation": {
        "lines": [_L20_DV], "terms": [f"exactly `{_DV}`"]}},
    "adapt_parser_unit_vector": {
        "source_file": {"lines": [("36", 27)], "terms": ["`source_file` is `driver.py` or `checker.py`"]},
        "syntax_error": {"lines": [("36", 27)], "terms": ["`syntax_error` has the key `lineno`, a positive integer",
                                                          "may have the key `offset`, an integer or null"]}},
    "adapt_legal_input": {
        "driver_return": {"lines": [("30", 83)], "terms": ["exact string `COMPLETE` or a dictionary",
                                                           "each value is a string"]},
        "input_port_widths": {"lines": [("30", 83)], "terms": ["each input port name mapped to its width",
                                                               "the value length equals the port width"]},
        "sampled_outputs": {"lines": [("30", 83)], "terms": ["each mapping a port name to its bit string"]},
        "legal_input_predicate": {"lines": [("30", 83)], "terms": [
            "one Python 3.11 function of two dictionaries", "`language` = `python3.11`",
            "returns the exact Boolean `True` for a legal vector and `False` otherwise",
            "`source_sha256`, the lowercase hexadecimal SHA-256 of `source` in UTF-8"]}},
}

# --- D-025 Phase B: C11-C16 -----------------------------------------------------------------------------------------
from adapter_contracts import CONTRACTS as _V136, DOMAINS as _V136_DOMAINS, VALUE_SUPPORT as _V136_SUPPORT  # noqa: E402
from adapters_v137 import JSON_SCOPE, TRUNCATION_SCOPE  # noqa: E402

_L195 = ("36", 195)
_L196, _L197, _L198, _L199 = ("36", 196), ("36", 197), ("36", 198), ("36", 199)


def _q(at, text):
    return (*at, text)


CONTRACTS.update({
    "adapt_halt_recurrence_v137": {
        "inputs": dict(_V136["adapt_halt_recurrence"]["inputs"]),
        "values": dict(_V136["adapt_halt_recurrence"]["values"]),
        "outcome": [("02", 185, "Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED` "
                                "(OWNER-DECIDED OD-1, §3.4 local-ledger error classes)."),
                    ("02", 185, "mark every scheduled slot in the affected scope `DESIGN_ABORTED_NO_SLOTS_SCORED`"),
                    ("02", 185, "A supplied halt signature with any component outside these domains is an evaluator input "
                                "error; it is never compared for recurrence."),
                    ("02", 185, "Such an input is outside the executable fixture contract")]},
    "adapt_serializer_grammar": {
        "inputs": {"diagnostic": _q(_L195, "`diagnostic` (a string)"),
                   "allowed_diagnostics": _q(_L195, "`allowed_diagnostics` (the duplicate-free list of diagnostics the "
                                                    "stage map emitted)")},
        "values": {},
        "outcome": [("02", 168, "When the set of diagnostics the stage map emitted is given, a diagnostic that passes the "
                                "grammar but is not in that set is also rejected at step (1)"),
                    ("02", 174, "is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` "
                                "and disposition `CONTROL_EXPECTATION`."),
                    ("02", 174, "**OWNER-DECIDED OD-1** (owner decision D-027; v1.3.6 does not state it)")]},
    "adapt_truncation_primitive": {
        "inputs": {"raw_diagnostic": _q(_L196, "`raw_diagnostic` (a string)"),
                   "raw_diagnostic_utf8_bytes": _q(_L196, "`raw_diagnostic_utf8_bytes` (its UTF-8 byte length)"),
                   "byte_cap": _q(_L196, "`byte_cap` = `2048`"),
                   "marker": _q(_L196, "`marker` = `...[TRUNCATED]`"),
                   "truncate_on_utf8_boundary": _q(_L196, "`truncate_on_utf8_boundary` = `true`"),
                   "truncate_before_json_escape": _q(_L196, "`truncate_before_json_escape` = `true`"),
                   "test_scope": _q(_L196, f"`test_scope` = `{TRUNCATION_SCOPE}`")},
        "values": {TRUNCATION_SCOPE: _q(_L196, f"`test_scope` = `{TRUNCATION_SCOPE}`")},
        "outcome": [("02", 168, "A truncation-primitive vector applies step (2) alone to its input string and reports"),
                    ("02", 174, "A truncation-primitive vector uses error class `TRUNCATION`")]},
    "adapt_json_primitive": {
        "inputs": {"feedback_object": _q(_L197, "`feedback_object` (exactly the string keys `stage_id`, `error_class`, "
                                                "`diagnostic`)"),
                   "encoding": _q(_L197, "`encoding` = `UTF-8`"), "ensure_ascii": _q(_L197, "`ensure_ascii` = `false`"),
                   "indent": _q(_L197, "`indent` = `2`"), "line_endings": _q(_L197, "`line_endings` = `LF`"),
                   "terminal_newline": _q(_L197, "`terminal_newline` = `true`"),
                   "grammar_exempt_for_primitive_test": _q(_L197, "`grammar_exempt_for_primitive_test` = `true`"),
                   "test_scope": _q(_L197, f"`test_scope` = `{JSON_SCOPE}`")},
        "values": {"UTF-8": _q(_L197, "`encoding` = `UTF-8`"), "LF": _q(_L197, "`line_endings` = `LF`"),
                   JSON_SCOPE: _q(_L197, f"`test_scope` = `{JSON_SCOPE}`")},
        "outcome": [("02", 168, "A JSON-escaping-primitive vector applies step (3) alone to its three-key object and reports"),
                    ("02", 174, "a JSON-escaping-primitive vector uses error class `JSON_SERIALIZATION`")]},
    "adapt_lifecycle_halt_event": {
        "inputs": {"lifecycle": _q(_L198, "`lifecycle` = `MID_RUN` (the halt occurs after slots have begun, §7b)"),
                   "event": _q(_L198, "one stage-map event of kind `simulator_error`"),
                   "slots": _q(_L198, "`previously_evaluated` + 1 + `remaining` = `scheduled`"),
                   "evaluator_repair_attempt": _q(_L198, "`evaluator_repair_attempt` = `1`, the ordinal of the recovery "
                                                         "cycle this halt opens (OWNER-DECIDED OD-4, Protocol §7b L185")},
        "values": {"MID_RUN": _q(_L198, "`lifecycle` = `MID_RUN`"),
                   "simulator_error": _q(_L198, "one stage-map event of kind `simulator_error`"),
                   "trace_integrity": _q(_L198, "or `trace_integrity` (`reason`)")},
        "outcome": [_q(_L198, "The result is the event's stage-map row with disposition `DESIGN_HALT_NO_SLOT_SCORED`"),
                    ("02", 154, "| Simulator error on RTL or null run | `DESIGN_HALT` | `EVALUATOR_INFRASTRUCTURE_FAILURE` |"),
                    ("02", 155, "| Harness trace-integrity fault | `DESIGN_HALT` | `TRACE_INTEGRITY_FAILURE` |"),
                    ("02", 185, "the *evaluator repair attempt* of a design halt, `evaluator_repair_attempt`, is the "
                                "ordinal of the recovery cycle that halt opens"),
                    ("02", 185, "No ordinal greater than `1` is valid.")]},
    "adapt_design_preflight": {
        "inputs": {"design_preflight": _q(_L199, "`design_preflight`, an object with exactly the Boolean "
                                                 "`rtl_null_masked_divergence`")},
        "values": {},
        "outcome": [("02", 179, "It is recorded at stage `DESIGN_HALT` with error class `RTL_NULL_CONTROL_FAILURE`"),
                    _q(_L199, "`true` is the §7a baseline mismatch record")]},
})

VALUE_SUPPORT.update({
    "adapt_halt_recurrence_v137": dict(_V136_SUPPORT["adapt_halt_recurrence"]),
    "adapt_serializer_grammar": {},
    "adapt_truncation_primitive": {TRUNCATION_SCOPE: (LITERAL, f"`{TRUNCATION_SCOPE}`")},
    "adapt_json_primitive": {"UTF-8": (LITERAL, "`UTF-8`"), "LF": (LITERAL, "`LF`"), JSON_SCOPE: (LITERAL, f"`{JSON_SCOPE}`")},
    "adapt_lifecycle_halt_event": {"MID_RUN": (LITERAL, "`MID_RUN`"), "simulator_error": (LITERAL, "`simulator_error`"),
                                   "trace_integrity": (LITERAL, "`trace_integrity`")},
    "adapt_design_preflight": {},
})


def _d(at, *terms):
    return {"lines": [at], "terms": list(terms)}


DOMAINS.update({
    "adapt_halt_recurrence_v137": {k: dict(v) for k, v in _V136_DOMAINS["adapt_halt_recurrence"].items()},
    "adapt_serializer_grammar": {"diagnostic": _d(_L195, "`diagnostic` (a string)"),
                                 "allowed_diagnostics": _d(_L195, "duplicate-free list of diagnostics the stage map emitted")},
    "adapt_truncation_primitive": {
        "raw_diagnostic": _d(_L196, "`raw_diagnostic` (a string)"),
        "raw_diagnostic_utf8_bytes": _d(_L196, "(its UTF-8 byte length)"),
        "byte_cap": _d(_L196, "`byte_cap` = `2048`"), "marker": _d(_L196, "`marker` = `...[TRUNCATED]`"),
        "truncate_on_utf8_boundary": _d(_L196, "`truncate_on_utf8_boundary` = `true`"),
        "truncate_before_json_escape": _d(_L196, "`truncate_before_json_escape` = `true`"),
        "test_scope": _d(_L196, f"`test_scope` = `{TRUNCATION_SCOPE}`")},
    "adapt_json_primitive": {
        "feedback_object": _d(_L197, "exactly the string keys `stage_id`, `error_class`, `diagnostic`"),
        "encoding": _d(_L197, "`encoding` = `UTF-8`"), "ensure_ascii": _d(_L197, "`ensure_ascii` = `false`"),
        "indent": _d(_L197, "`indent` = `2`"), "line_endings": _d(_L197, "`line_endings` = `LF`"),
        "terminal_newline": _d(_L197, "`terminal_newline` = `true`"),
        "grammar_exempt_for_primitive_test": _d(_L197, "`grammar_exempt_for_primitive_test` = `true`"),
        "test_scope": _d(_L197, f"`test_scope` = `{JSON_SCOPE}`")},
    "adapt_lifecycle_halt_event": {
        "lifecycle": _d(_L198, "`lifecycle` = `MID_RUN`"),
        "event": _d(_L198, "one stage-map event of kind `simulator_error`", "or `trace_integrity` (`reason`)"),
        "slots": _d(_L198, "`scheduled` (at least 1)", "`triggering_slot` (1 to `scheduled`)",
                    "`previously_evaluated` + 1 + `remaining` = `scheduled`"),
        "evaluator_repair_attempt": {"lines": [_L198, ("02", 185)],
                                     "terms": ["`evaluator_repair_attempt` = `1`", "No ordinal greater than `1` is valid."]}},
    "adapt_design_preflight": {"design_preflight": _d(_L199, "an object with exactly the Boolean `rtl_null_masked_divergence`")},
})

# --- D-026 Phase B: OWNER-SPECIFIED OS-1, OS-2 (candidate 36 L205, L206; not pack-derived) ---------------------------
from adapters_v137 import RECOVERY_MODE  # noqa: E402

_L205, _L206 = ("36", 205), ("36", 206)
_OS1_HALTS = "with `halt_code` `SIMULATOR_ERROR` or `TRACE_INTEGRITY_FAILURE`"

CONTRACTS.update({
    "adapt_operational_recovery": {
        "inputs": {
            "design_id": _q(_L205, "`design_id` (`FIFO` or `UART`, equal to the `design_id` of `halt_signature`)"),
            "halt_signature": _q(_L205, "`halt_signature`, the halt's signature in the Protocol §7b domains"),
            "slots": _q(_L205, "`slots` as in the lifecycle halt-event vector"),
            "evaluator_repair_attempt": _q(_L205, "`evaluator_repair_attempt` = `1` (OWNER-DECIDED OD-4, Protocol L185)"),
            "recovery_mode": _q(_L205, f"`recovery_mode` = `{RECOVERY_MODE}`"),
            "frozen_evaluator_hashes_unchanged": _q(_L205, "the Booleans `frozen_evaluator_hashes_unchanged`"),
            "f16_required": _q(_L205, "the Booleans `frozen_evaluator_hashes_unchanged`, `f16_required`"),
            "same_artifact_bytes": _q(_L205, "`f16_required`, `same_artifact_bytes` and `author_visible_materials_changed`"),
            "author_visible_materials_changed": _q(_L205, "and `author_visible_materials_changed`;"),
            "pre_halt_scored_slots": _q(_L205, "`pre_halt_scored_slots` (1 to `previously_evaluated`), the number of "
                                               "pre-halt scores"),
            "scheduled_slots": _q(_L205, "`scheduled_slots` = `scheduled`, the scheduled slots of the affected scope"),
            "same_artifacts_for_all_slots": _q(_L205, "`same_artifacts_for_all_slots` = `true`"),
            "same_slot_seeds": _q(_L205, "`same_slot_seeds` = `true`"),
            "new_generation_calls": _q(_L205, "`new_generation_calls` = `0`, which restate §7b"),
            "required_action": _q(_L205, "`required_action`, a string that is an informational label, not an outcome input")},
        "values": {"FIFO": _q(_L205, "`design_id` (`FIFO` or `UART`"), "UART": _q(_L205, "`design_id` (`FIFO` or `UART`"),
                   "SIMULATOR_ERROR": _q(_L205, _OS1_HALTS), "TRACE_INTEGRITY_FAILURE": _q(_L205, _OS1_HALTS),
                   RECOVERY_MODE: _q(_L205, f"`recovery_mode` = `{RECOVERY_MODE}`")},
        "outcome": [_q(_L205, "Only the properties named by the §7b recovery conditions decide the outcome."),
                    _q(_L205, "the result is the successful-operational-recovery control expectation of Protocol §3.4 at "
                              "stage `DESIGN_HALT` with disposition `CONTROL_EXPECTATION`"),
                    _q(_L205, "the recovery is an evaluator revision and the result is the change-class control "
                              "expectation of `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED`"),
                    _q(_L205, "such an input is outside this vector's scope"),
                    ("02", 175, "`RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` (error class `MID_RUN_REEVALUATION`)"),
                    ("02", 183, "it creates no new hashes, requires no new F16 and changes no artifact"),
                    ("02", 185, "No ordinal greater than `1` is valid."),
                    ("02", 183, "not the evaluator-revision path"),
                    ("02", 185, "Discard all pre-halt partial scores")]},
    "adapt_paired_run_outcome": {
        "inputs": {"response_object": _q(_L206, "`response_object` (a response object, as for any response input)"),
                   "runtime_pair": _q(_L206, "`runtime_pair`, an object with exactly `driver_source_excerpt`")},
        "values": {},
        "outcome": [_q(_L206, "Protocol §3.4 evaluation steps (1)–(6) run on the response object, and their first "
                              "failure is the result."),
                    _q(_L206, "`runtime_pair` stands in for steps (7)–(8), the paired run, which is not executed"),
                    _q(_L206, "a paired-outcome control vector, not a test of source-level alias detection"),
                    _q(_L206, "Any other pair does not determine the paired run's outcome"),
                    ("02", 156, "| Before first raw output divergence, paired next-input schedules differ | `TERMINAL` | "
                                "`DRIVER_NONDETERMINISM` |")]},
})

VALUE_SUPPORT.update({
    "adapt_operational_recovery": {"FIFO": (LITERAL, "`FIFO`"), "UART": (LITERAL, "`UART`"),
                                   "SIMULATOR_ERROR": (LITERAL, "`SIMULATOR_ERROR`"),
                                   "TRACE_INTEGRITY_FAILURE": (LITERAL, "`TRACE_INTEGRITY_FAILURE`"),
                                   RECOVERY_MODE: (LITERAL, f"`{RECOVERY_MODE}`")},
    "adapt_paired_run_outcome": {},
})

DOMAINS.update({
    "adapt_operational_recovery": {
        "design_id": _d(_L205, "`design_id` (`FIFO` or `UART`", "equal to the `design_id` of `halt_signature`"),
        "halt_signature": _d(_L205, "the halt's signature in the Protocol §7b domains", _OS1_HALTS),
        "slots": _d(_L205, "`slots` as in the lifecycle halt-event vector"),
        "evaluator_repair_attempt": {"lines": [_L205, ("02", 185)],
                                     "terms": ["`evaluator_repair_attempt` = `1`", "No ordinal greater than `1` is valid."]},
        "recovery_mode": _d(_L205, f"`recovery_mode` = `{RECOVERY_MODE}`"),
        # Free Booleans: the boundary is the decision term L205 states (success on one side, no stated outcome on the other).
        "frozen_evaluator_hashes_unchanged": _d(_L205, "the Booleans `frozen_evaluator_hashes_unchanged`",
                                                "When `frozen_evaluator_hashes_unchanged` is `true`"),
        "f16_required": _d(_L205, "the Booleans `frozen_evaluator_hashes_unchanged`, `f16_required`",
                           "`f16_required` is `false`"),
        "same_artifact_bytes": _d(_L205, "`same_artifact_bytes` and `author_visible_materials_changed`",
                                  "`same_artifact_bytes` is `true`"),
        "author_visible_materials_changed": _d(_L205, "`author_visible_materials_changed`",
                                               "`author_visible_materials_changed` is `false`"),
        "pre_halt_scored_slots": _d(_L205, "`pre_halt_scored_slots` (1 to `previously_evaluated`)"),
        "scheduled_slots": _d(_L205, "`scheduled_slots` = `scheduled`"),
        "same_artifacts_for_all_slots": _d(_L205, "`same_artifacts_for_all_slots` = `true`"),
        "same_slot_seeds": _d(_L205, "`same_slot_seeds` = `true`"),
        "new_generation_calls": _d(_L205, "`new_generation_calls` = `0`"),
        "required_action": _d(_L205, "`required_action`, a string")},
    "adapt_paired_run_outcome": {
        "response_object": {"lines": [_L206, ("30", 7)],
                            "terms": ["a response object, as for any response input", "34_OpenVEF_Response_Schema_v1.0.json"]},
        "runtime_pair": _d(_L206, "an object with exactly `driver_source_excerpt`",
                           "the Booleans `before_first_raw_output_divergence` and `next_input_schedules_equal`")},
})
