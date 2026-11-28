"""Runner adapters that exist only under `--pack v1.3.7` (the adopted pack, default since D-035) and
`--pack v1.3.7-candidate` (D-024; the same bytes, audited by document audit #7).

Each input contract is cited to the candidate pack (proposals/v1.3.7/pack, corrections C2, C5, C9-C16, and the
OWNER-DECIDED rules OD-1..OD-4 of correction cycle 2, D-027), so these rows are never in the v1.3.6 table: v1.3.6 has no text for these shapes (PD-02, PD-04, PD-06, PD-07, D-013).
Contracts: runner/adapter_contracts_v137.py. Vectors and boundary pairs: tests/adapter_vectors_v137.py, checked by
tests/test_dispatch_shapes_v137.py under the same rules as the v1.3.6 adapters (D-013, D-017).

A refusal raises NotDetermined, which the runner reports as NOT_IMPLEMENTED with the reason, exactly as its own
Blocked. This module does not import the runner.
"""
from __future__ import annotations

import hashlib
from typing import Any, Callable, Mapping

from openvef import serializer
from openvef.ast_signature import check_ast_signature, check_compile
from openvef.envelope import Failure
from openvef.import_policy import check_import_policy
from openvef.ledger import (DESIGN_IDS, HaltSignature, SignatureDomainError, halt_after_recovery,
                            lifecycle_expectation_candidate)
from openvef.schema import ValidatedResponse, validate_clause_ids, validate_schema
from openvef.source_ast import UnsettledSpec, check_sources, syntax_reject
from openvef.stage_map import HALT, TERMINAL, EventError, NotDetermined, first_event, validate_vector

# D-025 item 1: the C5 predicate runs only after the runner has verified every file of the candidate pack against its
# pinned SHA256SUMS. Set by runner/run_f18.py main(); nothing else sets it.
PACK_VERIFIED = False

# Candidate 02 L176 (C2, OD-3): "The change classes are closed and have exactly four cases (OWNER-DECIDED OD-3)";
# 02 L571 (§20.1, OD-3): `change_class` is "exactly one of" these four.
CHANGE_CLASSES = ("FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED",
                  "SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED",
                  "DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START",
                  "DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED")
# Candidate 02 L176 (OD-3): "`HALT_SIGNATURE_COMPONENT_ENUMERATION` is not a change class: it names the halt-signature
# domain validation"; 02 L572 (§20.1): `domain_validation` is "exactly `HALT_SIGNATURE_COMPONENT_ENUMERATION`".
DOMAIN_VALIDATIONS = ("HALT_SIGNATURE_COMPONENT_ENUMERATION",)
# Candidate 36 L27 (C9): "`source_file` is `driver.py` or `checker.py`".
SOURCE_FILES = ("driver.py", "checker.py")
# Candidate 30 L83 (C5, OD-2): "`legal_input_predicate` (an object with `language` = `python3.11`, `function`, ...,
# `source`, its Python source, and `source_sha256`, the lowercase hexadecimal SHA-256 of `source` in UTF-8".
PREDICATE_LANGUAGE = "python3.11"
PREDICATE_KEYS = {"language", "function", "source", "source_sha256"}

# D-027: the OWNER-DECIDED rules each adapter's input contract or outcome rests on. A fixture whose adapter is listed
# here counts OWNER-DECIDED (the runner labels its record). An adapter may add a rule used on one path only (_uses).
OWNER_DECIDED = {"adapt_serializer_grammar": ("OD-1",), "adapt_halt_recurrence_v137": ("OD-1",),
                 "adapt_legal_input": ("OD-2",), "adapt_change_class": ("OD-3",), "adapt_domain_validation": ("OD-3",),
                 "adapt_lifecycle_halt_event": ("OD-4",), "adapt_operational_recovery": ("OD-4",)}
_OD_USED: list[str] = []


def _uses(item: str) -> None:
    """Record an OWNER-DECIDED rule that only this path of an adapter depends on (D-027)."""
    _OD_USED.append(item)


def take_od_used() -> tuple[str, ...]:
    """The path-only OD rules recorded since the last call; clears them. Called by the runner around each fixture."""
    used = tuple(sorted(set(_OD_USED)))
    _OD_USED.clear()
    return used


def _in_domain(ok: bool, name: str) -> None:
    if not ok:
        raise NotDetermined(f"{name} outside its cited domain")


def _bits(value: Any) -> bool:
    return isinstance(value, str) and value != "" and set(value) <= {"0", "1"}


def _expectation(key: str) -> dict:
    record, missing = lifecycle_expectation_candidate(key)
    if missing:
        raise NotDetermined(f"candidate Protocol does not support: {sorted(missing)}")
    return record


def adapt_change_class(desc: dict, validator) -> dict:
    """Candidate 02 L175-L176, L181-L185 (C1-C3) and §20 (OD-3): the change-class control expectation, whole (C4)."""
    change_class = desc["input"]["change_class"]
    _in_domain(isinstance(change_class, str) and change_class in CHANGE_CLASSES, "change_class")
    return _expectation(change_class)


def adapt_domain_validation(desc: dict, validator) -> dict:
    """Candidate 02 L176, L185 (C3) and §20 (OD-3): the halt-signature domain-validation control expectation, whole."""
    check = desc["input"]["domain_validation"]
    _in_domain(isinstance(check, str) and check in DOMAIN_VALIDATIONS, "domain_validation")
    return _expectation(check)


def adapt_parser_unit_vector(desc: dict, validator) -> dict:
    """Candidate 36 L27 (C9): the Protocol §3.4 SOURCE_SYNTAX_REJECT column rule (02 L127) at a given position."""
    inp = desc["input"]
    source_file, error = inp["source_file"], inp["syntax_error"]
    _in_domain(isinstance(source_file, str) and source_file in SOURCE_FILES, "source_file")
    _in_domain(isinstance(error, dict) and {"lineno"} <= set(error) <= {"lineno", "offset"}
               and type(error["lineno"]) is int and error["lineno"] >= 1
               and (error.get("offset") is None or type(error.get("offset")) is int), "syntax_error")
    failure = syntax_reject(source_file, error["lineno"], error.get("offset"))
    return {"disposition": "CONTROL_EXPECTATION", "stage_id": failure.stage_id, "error_class": failure.error_class,
            "diagnostic": failure.diagnostic}


def _predicate(spec: Mapping[str, str], sampled: Mapping[str, str]) -> Callable[[Mapping[str, str]], bool]:
    """Candidate 30 L83 (C5, OD-2): one pure Python 3.11 function of (vector, sampled) returning exactly True or
    False; any other outcome is an evaluator failure, never an artifact verdict. It is evaluator material, not artifact
    code (D-015), and hash-gated: it runs only after the candidate pack's SHA256SUMS verify (D-025) and its source
    matches its frozen `source_sha256` (OD-2). Purity is the freezer's condition; it is not certified here."""
    if not PACK_VERIFIED:
        raise NotDetermined("candidate pack SHA256SUMS not verified (D-025); predicate not run")
    if hashlib.sha256(spec["source"].encode("utf-8")).hexdigest() != spec["source_sha256"]:
        raise NotDetermined("evaluator failure (candidate 30 L83, OD-2): predicate source does not match its frozen "
                            "SHA-256; not run")
    namespace: dict = {}
    try:
        exec(compile(spec["source"], "<legal_input_predicate>", "exec", dont_inherit=True), namespace)
        function = namespace[spec["function"]]
    except Exception as exc:
        raise NotDetermined(f"evaluator failure (candidate 30 L83): predicate does not load: {type(exc).__name__}")

    def legal(vector: Mapping[str, str]) -> bool:
        try:
            result = function(dict(vector), dict(sampled))
        except Exception as exc:
            raise NotDetermined(f"evaluator failure (candidate 30 L83): predicate raised {type(exc).__name__}")
        if type(result) is not bool:
            raise NotDetermined("evaluator failure (candidate 30 L83): predicate did not return a Boolean")
        return result
    return legal


def adapt_legal_input(desc: dict, validator) -> Failure:
    """Candidate 30 L83 (C5): checks (a)-(e) in order on a driver vector, with the supplied widths, sampled
    outputs and predicate."""
    inp = desc["input"]
    widths, sampled, spec = inp["input_port_widths"], inp["sampled_outputs"], inp["legal_input_predicate"]
    _in_domain(isinstance(widths, dict) and len(widths) > 0
               and all(isinstance(k, str) and type(w) is int and w >= 1 for k, w in widths.items()),
               "input_port_widths")
    _in_domain(isinstance(sampled, dict) and all(isinstance(k, str) and _bits(v) for k, v in sampled.items()),
               "sampled_outputs")
    _in_domain(isinstance(spec, dict) and set(spec) == PREDICATE_KEYS and spec["language"] == PREDICATE_LANGUAGE
               and isinstance(spec["function"], str) and spec["function"].isidentifier()
               and isinstance(spec["source"], str) and _utf8(spec["source"])
               and isinstance(spec["source_sha256"], str) and len(spec["source_sha256"]) == 64
               and set(spec["source_sha256"]) <= set("0123456789abcdef"), "legal_input_predicate")
    failure = validate_vector(inp["driver_return"], widths, widths, _predicate(spec, sampled))
    if failure is None:
        raise NotDetermined("check passed; nothing further to compare")
    return failure


def _utf8(value: Any) -> bool:
    try:
        return isinstance(value, str) and bool(value.encode("utf-8") or True)
    except UnicodeEncodeError:
        return False


def adapt_halt_recurrence_v137(desc: dict, validator) -> Failure:
    """Candidate 02 L185 (C10, C11): the v1.3.6 recurrence domains, then the termination record that v1.3.6 could not
    give (PD-26). Replaces the v1.3.6 row in the candidate table only."""
    inp = desc["input"]
    _in_domain(inp["design_id"] in DESIGN_IDS, "design_id")
    _in_domain(type(inp["recovery_cycles_used"]) is int and inp["recovery_cycles_used"] == 1, "recovery_cycles_used")
    _in_domain(type(inp["scheduled_slots"]) is int and inp["scheduled_slots"] >= 1, "scheduled_slots")
    _in_domain(all(isinstance(inp[k], dict) for k in ("first_halt_signature", "second_halt_signature")), "halt signature")
    try:
        first, second = (HaltSignature.given(inp[k]) for k in ("first_halt_signature", "second_halt_signature"))
    except SignatureDomainError as exc:  # candidate L185 (C10, A3): input error, outside the fixture contract, no record
        raise NotDetermined(f"supplied halt signature outside the Protocol L185 domains (A3: outside the executable "
                            f"fixture contract, no ledger record): {exc}") from exc
    return halt_after_recovery(first, second, inp["recovery_cycles_used"])


_ABSENT = object()


def adapt_serializer_grammar(desc: dict, validator) -> Failure:
    """Candidate 02 L168 step (1) with the emitted set (C12), 02 L174 record (C11); input 36 L195."""
    inp = desc["input"]
    diagnostic, emitted = inp["diagnostic"], inp.get("allowed_diagnostics", _ABSENT)
    _in_domain(_utf8(diagnostic), "diagnostic")
    _in_domain(emitted is _ABSENT or (isinstance(emitted, list) and all(_utf8(d) for d in emitted)
                                      and len(set(emitted)) == len(emitted)), "allowed_diagnostics")
    failure = serializer.check_diagnostic(diagnostic, None if emitted is _ABSENT else emitted)
    if failure is None:
        raise NotDetermined("check passed; nothing further to compare")
    return failure


# Candidate 36 L196, L197 (C13, C14): the test-scope tokens.
TRUNCATION_SCOPE = "TRUNCATION_PRIMITIVE_ONLY_GRAMMAR_BYPASSED"
JSON_SCOPE = "JSON_ESCAPING_PRIMITIVE_ONLY_GRAMMAR_BYPASSED"
FEEDBACK_KEYS = ("stage_id", "error_class", "diagnostic")


def adapt_truncation_primitive(desc: dict, validator) -> dict:
    """Candidate 02 L168 step (2) alone, L174 (C13); input 36 L196. Properties fixed by L168 must equal it."""
    inp = desc["input"]
    raw = inp["raw_diagnostic"]
    _in_domain(_utf8(raw), "raw_diagnostic")
    _in_domain(type(inp["raw_diagnostic_utf8_bytes"]) is int and inp["raw_diagnostic_utf8_bytes"] == len(raw.encode()),
               "raw_diagnostic_utf8_bytes")
    _in_domain(type(inp["byte_cap"]) is int and inp["byte_cap"] == serializer.BYTE_CAP, "byte_cap")
    _in_domain(inp["marker"] == serializer.MARKER, "marker")
    _in_domain(inp["truncate_on_utf8_boundary"] is True, "truncate_on_utf8_boundary")
    _in_domain(inp["truncate_before_json_escape"] is True, "truncate_before_json_escape")
    _in_domain(inp["test_scope"] == TRUNCATION_SCOPE, "test_scope")
    out = serializer.truncate(raw).encode("utf-8")
    try:
        valid = bool(out.decode("utf-8") or True)
    except UnicodeDecodeError:
        valid = False
    marker = serializer.MARKER.encode("utf-8")
    return {"disposition": "CONTROL_EXPECTATION", "stage_id": "FEEDBACK_SERIALIZER", "error_class": "TRUNCATION",
            "contains_marker": out.endswith(marker), "valid_utf8": valid, "output_diagnostic_bytes": len(out),
            "marker_utf8_bytes": len(marker)}


def adapt_json_primitive(desc: dict, validator) -> dict:
    """Candidate 02 L168 step (3) alone, L174 (C13, C14); input 36 L197. Properties fixed by L168 must equal it."""
    inp = desc["input"]
    obj = inp["feedback_object"]
    _in_domain(isinstance(obj, dict) and set(obj) == set(FEEDBACK_KEYS) and all(_utf8(obj[k]) for k in FEEDBACK_KEYS),
               "feedback_object")
    _in_domain(inp["encoding"] == "UTF-8", "encoding")
    _in_domain(inp["ensure_ascii"] is False, "ensure_ascii")
    _in_domain(type(inp["indent"]) is int and inp["indent"] == 2, "indent")
    _in_domain(inp["line_endings"] == "LF", "line_endings")
    _in_domain(inp["terminal_newline"] is True, "terminal_newline")
    _in_domain(inp["grammar_exempt_for_primitive_test"] is True, "grammar_exempt_for_primitive_test")
    _in_domain(inp["test_scope"] == JSON_SCOPE, "test_scope")
    data = serializer._serialize_object(*(obj[k] for k in FEEDBACK_KEYS))
    return {"disposition": "CONTROL_EXPECTATION", "stage_id": "FEEDBACK_SERIALIZER", "error_class": "JSON_SERIALIZATION",
            "diagnostic_utf8": data.decode("utf-8"), "diagnostic_sha256": hashlib.sha256(data).hexdigest(),
            "diagnostic_bytes": len(data)}


# Candidate 36 L198 (C15): "one stage-map event of kind `simulator_error` ... or `trace_integrity`".
HALT_EVENTS = ("simulator_error", "trace_integrity")
SLOT_KEYS = {"scheduled", "previously_evaluated", "triggering_slot", "remaining"}


def adapt_lifecycle_halt_event(desc: dict, validator) -> Failure:
    """Candidate 36 L198 (C15): a first mid-run design halt; the record is the event's stage-map row."""
    inp = desc["input"]
    event, slots = inp["event"], inp["slots"]
    _in_domain(inp["lifecycle"] == "MID_RUN", "lifecycle")
    _in_domain(isinstance(event, dict) and event.get("kind") in HALT_EVENTS, "event")
    _in_domain(_slots(slots), "slots")
    _in_domain(type(inp["evaluator_repair_attempt"]) is int and inp["evaluator_repair_attempt"] == 1,
               "evaluator_repair_attempt")
    try:
        failure = first_event([event])
    except EventError as exc:
        raise NotDetermined(f"event outside its cited domain: {exc}") from exc
    assert failure.disposition == HALT
    return failure


def adapt_design_preflight(desc: dict, validator) -> Failure:
    """Candidate 02 L179 (C16): the §7a baseline record; input 36 L199."""
    gate = desc["input"]["design_preflight"]
    _in_domain(isinstance(gate, dict) and set(gate) == {"rtl_null_masked_divergence"}
               and type(gate["rtl_null_masked_divergence"]) is bool, "design_preflight")
    if not gate["rtl_null_masked_divergence"]:
        raise NotDetermined("check passed; nothing further to compare")
    return Failure("DESIGN_HALT", "RTL_NULL_CONTROL_FAILURE", "RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE", HALT)


def _slots(slots: Any) -> bool:
    """Candidate 36 L198 (C15) slot counts; OS-1 (36 L205) uses the same domain."""
    return (isinstance(slots, dict) and set(slots) == SLOT_KEYS and all(type(v) is int and v >= 0 for v in slots.values())
            and slots["scheduled"] >= 1 and 1 <= slots["triggering_slot"] <= slots["scheduled"]
            and slots["previously_evaluated"] + 1 + slots["remaining"] == slots["scheduled"])


# --- D-026 Phase B: OWNER-SPECIFIED items (candidate 36 L203-L207; not pack-derived, labelled in every record) -------

# Candidate 36 L205 (OS-1): "`recovery_mode` = `OPERATIONAL_RECOVERY`"; "with `halt_code` `SIMULATOR_ERROR` or
# `TRACE_INTEGRITY_FAILURE`".
RECOVERY_MODE = "OPERATIONAL_RECOVERY"
RECOVERABLE_HALT_CODES = ("SIMULATOR_ERROR", "TRACE_INTEGRITY_FAILURE")
L183_CONDITIONS = ("frozen_evaluator_hashes_unchanged", "f16_required", "same_artifact_bytes",
                   "author_visible_materials_changed")


def _unstated(why: str) -> NotDetermined:
    return NotDetermined(f"OS-1 (candidate 36 L205): the Protocol states no outcome when {why}; outside this vector's scope")


def adapt_operational_recovery(desc: dict, validator) -> dict:
    """Candidate 36 L205 (OS-1, OWNER-SPECIFIED, D-026): the §7b operational-recovery vector. Only the properties the
    L183 recovery conditions name decide the outcome; `required_action` is an informational label."""
    inp = desc["input"]
    slots, scored = inp["slots"], inp["pre_halt_scored_slots"]
    _in_domain(inp["design_id"] in DESIGN_IDS, "design_id")
    _in_domain(_slots(slots), "slots")
    _in_domain(isinstance(inp["halt_signature"], dict), "halt_signature")
    try:
        signature = HaltSignature.given(inp["halt_signature"])
    except SignatureDomainError as exc:  # candidate L185 (C10, A3): input error, outside the fixture contract, no record
        raise NotDetermined(f"supplied halt signature outside the Protocol L185 domains (A3: outside the executable "
                            f"fixture contract, no ledger record): {exc}") from exc
    _in_domain(signature.halt_code in RECOVERABLE_HALT_CODES, "halt_signature")
    _in_domain(signature.design_id == inp["design_id"], "design_id")
    _in_domain(type(inp["evaluator_repair_attempt"]) is int and inp["evaluator_repair_attempt"] == 1,
               "evaluator_repair_attempt")
    _in_domain(inp["recovery_mode"] == RECOVERY_MODE, "recovery_mode")
    for name in L183_CONDITIONS:
        _in_domain(type(inp[name]) is bool, name)
    _in_domain(type(scored) is int and 1 <= scored <= slots["previously_evaluated"], "pre_halt_scored_slots")
    _in_domain(type(inp["scheduled_slots"]) is int and inp["scheduled_slots"] == slots["scheduled"], "scheduled_slots")
    _in_domain(inp["same_artifacts_for_all_slots"] is True, "same_artifacts_for_all_slots")
    _in_domain(inp["same_slot_seeds"] is True, "same_slot_seeds")
    _in_domain(type(inp["new_generation_calls"]) is int and inp["new_generation_calls"] == 0, "new_generation_calls")
    _in_domain(_utf8(inp["required_action"]), "required_action")  # informational; never read further (D-026 (2))
    hashes_unchanged, f16, same_bytes, author_changed = (inp[name] for name in L183_CONDITIONS)
    if author_changed:  # L183: not the evaluator-revision path; which revision of L181 applies is not given
        raise _unstated("an author-visible item changed and the vector does not identify the study or design revision")
    if not same_bytes:
        raise _unstated("the artifact bytes changed")
    if hashes_unchanged and not f16:
        return {"disposition": "CONTROL_EXPECTATION", "stage_id": "DESIGN_HALT", "error_class": "MID_RUN_REEVALUATION",
                "diagnostic": "RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS", "discard_pre_halt_scores": True,
                "rerun_slots": inp["scheduled_slots"], "reuse_same_artifact_bytes": True,
                "new_confirmatory_generation_calls": 0}
    if not hashes_unchanged and f16:  # L183 path (b): an evaluator revision (C1-C4 record, §20 schema)
        _uses("OD-3")
        return _expectation(CHANGE_CLASSES[0])
    raise _unstated("F16 is required with unchanged frozen evaluator hashes" if f16 else
                    "the frozen evaluator hashes changed without F16")


# Candidate 36 L206 (OS-2): "`runtime_pair`, an object with exactly `driver_source_excerpt` (a string ...) and the
# Booleans `before_first_raw_output_divergence` and `next_input_schedules_equal`".
PAIR_FIELDS = {"driver_source_excerpt", "before_first_raw_output_divergence", "next_input_schedules_equal"}


def _static_stages(desc: dict, obj: Any, validator) -> Failure | None:
    """Protocol §3.4 evaluation steps (1)-(6) on a response object (A-002: no envelope), as the runner's response
    stages, without the step (7) factory checks: nothing here runs artifact code (D-015)."""
    checked = validate_schema(validator, obj)
    if isinstance(checked, ValidatedResponse):
        checked = validate_clause_ids(checked, desc["manifest_clause_ids"])
    if isinstance(checked, Failure):
        return checked
    sources = {"driver.py": obj["driver"]["source"], "checker.py": obj["checker"]["source"]}
    try:
        trees = check_sources(list(sources.items()))
        if isinstance(trees, Failure):
            return trees
        return check_import_policy(sources, trees) or check_ast_signature(trees) or check_compile(sources)
    except UnsettledSpec as exc:
        raise NotDetermined(f"blocked on docs/ambiguities.md {exc}") from exc


def adapt_paired_run_outcome(desc: dict, validator) -> Failure:
    """Candidate 36 L206 (OS-2, OWNER-SPECIFIED, D-026; A4: a paired-outcome control vector, not a test of
    source-level alias detection): steps (1)-(6) run; `runtime_pair` stands in for the paired run (steps (7)-(8)),
    which is not executed. The excerpt documents the access under test and is never read."""
    inp = desc["input"]
    pair = inp["runtime_pair"]
    _in_domain(isinstance(pair, dict) and set(pair) == PAIR_FIELDS and _utf8(pair["driver_source_excerpt"])
               and type(pair["before_first_raw_output_divergence"]) is bool
               and type(pair["next_input_schedules_equal"]) is bool, "runtime_pair")
    failure = _static_stages(desc, inp["response_object"], validator)
    if failure is not None:
        return failure
    if pair["before_first_raw_output_divergence"] and not pair["next_input_schedules_equal"]:  # 02 L156
        return Failure("TERMINAL", "DRIVER_NONDETERMINISM", "DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE", TERMINAL)
    raise NotDetermined("OS-2 (candidate 36 L206): this pair does not determine the paired run's outcome; outside this "
                        "vector's scope")


# OWNER-SPECIFIED rows (D-026): adapter -> OS item, for the record label. Counted apart from pack-derived results.
OWNER_SPECIFIED = {"adapt_operational_recovery": "OS-1", "adapt_paired_run_outcome": "OS-2"}
# Candidate 36 L207 (OS-3): an input shape the owners left unspecified. (required, optional, OS item, reason); the
# runner reports it NOT_IMPLEMENTED with this reason and label. No adapter exists for it.
OPEN_SHAPES = (
    ({"response_object", "port_manifest"}, set(), "OS-3",
     "candidate 36 L207: the expected stage DRIVER_VECTOR is checked within evaluation step (7), while Driver.step "
     "runs on the original RTL; no design, RTL or port widths are given and no rule states how the vector is obtained "
     "outside that run (D-026: left NOT_IMPLEMENTED)"),
)

# v1.3.6 rows whose adapter the candidate replaces (same input shape, outcome the candidate text now gives).
REPLACEMENTS = {"adapt_halt_recurrence": adapt_halt_recurrence_v137}

# (required keys, optional keys, adapter): added to the runner's table for the candidate pack only.
ROWS = (
    ({"change_class"}, set(), adapt_change_class),
    ({"domain_validation"}, set(), adapt_domain_validation),  # D-027 OD-3
    ({"source_file", "syntax_error"}, set(), adapt_parser_unit_vector),
    ({"driver_return", "input_port_widths", "sampled_outputs", "legal_input_predicate"}, set(), adapt_legal_input),
    ({"diagnostic"}, {"allowed_diagnostics"}, adapt_serializer_grammar),
    ({"raw_diagnostic", "raw_diagnostic_utf8_bytes", "byte_cap", "marker", "truncate_on_utf8_boundary",
      "truncate_before_json_escape", "test_scope"}, set(), adapt_truncation_primitive),
    ({"feedback_object", "encoding", "ensure_ascii", "indent", "line_endings", "terminal_newline",
      "grammar_exempt_for_primitive_test", "test_scope"}, set(), adapt_json_primitive),
    ({"lifecycle", "event", "slots", "evaluator_repair_attempt"}, set(), adapt_lifecycle_halt_event),
    ({"design_preflight"}, set(), adapt_design_preflight),
    # D-026 OWNER-SPECIFIED (OS-1, OS-2)
    ({"design_id", "slots", "evaluator_repair_attempt", "same_artifacts_for_all_slots", "new_generation_calls",
      "required_action", "recovery_mode", "frozen_evaluator_hashes_unchanged", "same_artifact_bytes", "same_slot_seeds",
      "f16_required", "author_visible_materials_changed", "pre_halt_scored_slots", "scheduled_slots", "halt_signature"},
     set(), adapt_operational_recovery),
    ({"response_object", "runtime_pair"}, set(), adapt_paired_run_outcome),
)
