"""Design-lifecycle ledger: halt signatures and the single recovery cycle (Protocol §7b).

Implements:
  Protocol L183-L185 — design-local halt after slots have begun; one recovery cycle per
                   affected design (operational recovery or evaluator revision); halt
                   signature `(design_id, halt_code, evaluator_component,
                   stable_error_class, stable_diagnostic_code)` with exact component
                   domains and the reason-to-component mapping; termination with
                   `DESIGN_HALT_REPEATED|reason=EVALUATOR_FAILURE_REPRODUCED` or
                   `|reason=SECOND_HALT_AFTER_RECOVERY`; every scheduled slot in scope is
                   `DESIGN_ABORTED_NO_SLOTS_SCORED`.
  Protocol L175 (closed lifecycle vocabulary) — `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_
                   FROZEN_ARTIFACTS` (error class `MID_RUN_REEVALUATION`) for a successful
                   operational recovery.

A-031 was reversed by owner decision D-012: every signature, constructed or supplied, must
lie in the L185 domains; a supplied signature outside them is rejected (PD-01).
"""
from __future__ import annotations

import re
from typing import Any, Mapping, NamedTuple, Optional

from openvef.envelope import Failure

DESIGN_IDS = ("FIFO", "UART")
HALT_CODES = ("SIMULATOR_ERROR", "TRACE_INTEGRITY_FAILURE", "RTL_NULL_CONTROL_FAILURE")
EVALUATOR_COMPONENTS = ("SIMULATOR", "REPLAY_VERIFIER", "RECORDER", "TRACE_ALIGNMENT_CHECKER", "TRACE_SERIALIZER",
                        "RTL_NULL_COMPARATOR")
TRACE_REASON_COMPONENT = {
    "REPLAY_HASH_MISMATCH": "REPLAY_VERIFIER",
    "MALFORMED_RECORDER_OUTPUT": "RECORDER",
    "ROW_ALIGNMENT": "TRACE_ALIGNMENT_CHECKER",
    "UNTRUSTED_TRACE_SERIALIZATION": "TRACE_SERIALIZER",
}
_EXC = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
SIGNATURE_FIELDS = ("design_id", "halt_code", "evaluator_component", "stable_error_class", "stable_diagnostic_code")

ABORTED = "DESIGN_ABORTED_NO_SLOTS_SCORED"


class SignatureDomainError(ValueError):
    """A supplied halt signature has a component outside its Protocol L185 domain."""


class HaltSignature(NamedTuple):
    design_id: str
    halt_code: str
    evaluator_component: str
    stable_error_class: str
    stable_diagnostic_code: str

    @classmethod
    def build(cls, design_id: str, halt_code: str, *, exception_class: Optional[str] = None,
              trace_reason: Optional[str] = None) -> "HaltSignature":
        """Construct a signature from a halt event, enforcing the L185 domains."""
        if design_id not in DESIGN_IDS or halt_code not in HALT_CODES:
            raise ValueError("design_id or halt_code outside its domain")
        if halt_code == "SIMULATOR_ERROR":
            if not (isinstance(exception_class, str) and _EXC.fullmatch(exception_class)):
                raise ValueError("SIMULATOR_ERROR needs a simple exception class name")
            return cls(design_id, halt_code, "SIMULATOR", exception_class, halt_code)
        if halt_code == "TRACE_INTEGRITY_FAILURE":
            return cls(design_id, halt_code, TRACE_REASON_COMPONENT[trace_reason], "NONE", halt_code)
        return cls(design_id, halt_code, "RTL_NULL_COMPARATOR", "NONE", halt_code)

    @classmethod
    def given(cls, record: Mapping[str, Any]) -> "HaltSignature":
        """A ready-made signature: exactly the five components, each in its L185 domain (D-012)."""
        if set(record) != set(SIGNATURE_FIELDS):
            raise SignatureDomainError(f"halt signature must have exactly {SIGNATURE_FIELDS}")
        code = record["halt_code"]
        component = {"SIMULATOR_ERROR": ("SIMULATOR",), "RTL_NULL_CONTROL_FAILURE": ("RTL_NULL_COMPARATOR",),
                     "TRACE_INTEGRITY_FAILURE": tuple(TRACE_REASON_COMPONENT.values())}
        cls_ = record["stable_error_class"]
        ok = {
            "design_id": record["design_id"] in DESIGN_IDS,
            "halt_code": code in HALT_CODES,
            "evaluator_component": record["evaluator_component"] in component.get(code, EVALUATOR_COMPONENTS),
            "stable_error_class": (isinstance(cls_, str) and _EXC.fullmatch(cls_) is not None
                                   if code == "SIMULATOR_ERROR" else cls_ == "NONE"),
            "stable_diagnostic_code": record["stable_diagnostic_code"] == code,
        }
        bad = [f"{f}={record[f]!r}" for f in SIGNATURE_FIELDS if not ok[f]]
        if bad:
            raise SignatureDomainError(", ".join(bad))
        return cls(*(record[f] for f in SIGNATURE_FIELDS))


def halt_after_recovery(first: HaltSignature, second: HaltSignature, recovery_cycles_used: int) -> Failure:
    """A design halt after the single recovery cycle terminates the design (L185)."""
    if recovery_cycles_used != 1:
        raise ValueError("this rule applies to a halt after the one recovery cycle")
    reason = "EVALUATOR_FAILURE_REPRODUCED" if first == second else "SECOND_HALT_AFTER_RECOVERY"
    return Failure("DESIGN_HALT", "DESIGN_HALT_REPEATED", f"DESIGN_HALT_REPEATED|reason={reason}", ABORTED)


class OperationalRecovery(NamedTuple):
    """The control expectation of a successful operational recovery (L175, L183-L185)."""
    failure: Failure
    discard_pre_halt_scores: bool      # "Discard all pre-halt partial scores"
    rerun_slots: int                   # "re-evaluate every scheduled slot in the affected scope"
    reuse_same_artifact_bytes: bool    # "with the same frozen artifact bytes and slot seeds"
    new_confirmatory_generation_calls: int  # "no confirmatory generation call is made"


def operational_recovery(*, scheduled_slots: int, frozen_evaluator_hashes_unchanged: bool, same_artifact_bytes: bool,
                         same_slot_seeds: bool, author_visible_materials_changed: bool,
                         new_generation_calls: int, f16_required: bool) -> Optional[OperationalRecovery]:
    """None unless every operational-recovery condition of L183 holds.

    Operational recovery uses "the exact same frozen source, binaries, ... configuration";
    "it creates no new hashes, requires no new F16 and changes no artifact".
    """
    if not (frozen_evaluator_hashes_unchanged and same_artifact_bytes and same_slot_seeds
            and not author_visible_materials_changed and new_generation_calls == 0 and not f16_required):
        return None
    failure = Failure("DESIGN_HALT", "MID_RUN_REEVALUATION", "RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS",
                      "CONTROL_EXPECTATION")
    return OperationalRecovery(failure, True, scheduled_slots, True, 0)


# --- Change-class lifecycle control expectations (Protocol L175-L176, L181-L185) -------
#
# A-033 (revised per owner correction, 23 Nov 2026; field derivations decided by Claude
# under standing delegation, approved under D-009). Each `change_class` input label is
# matched to the Protocol case its words name; each output field is either a value with
# the Protocol sentence that supports it, or UNSUPPORTED with the reason. Field NAMES
# follow the control-vector expectations (A-032 disclosure); no VALUE is read from an
# expected object. `required_action` literals are copied verbatim from L176, where the
# Protocol labels each literal with its lifecycle case (`M48 = ...` etc.).

class Unsupported(NamedTuple):
    reason: str


_ERROR_CLASS_UNSTATED = Unsupported(
    "error class not stated: L175 states error classes only for the M41 (MID_RUN_REEVALUATION), M53 and M54 "
    "vectors, and the stage map shows the error class need not equal the diagnostic CODE (L154: SIMULATOR_ERROR "
    "under EVALUATOR_INFRASTRUCTURE_FAILURE)")


def _token_unstated(meaning: str) -> Unsupported:
    return Unsupported(f"meaning supported ({meaning}) but the exact token appears nowhere in the Protocol; "
                       "writing it would copy the expected output (hard rule 4)")


_CONTROL = ("CONTROL_EXPECTATION", "L176 'Each literal is a closed local control expectation'; L177")
_STAGE = ("DESIGN_HALT", "L172 stage list; §7b 'Mid-run design halt' L181-L185")
_AUTHORING_DIAG = ("AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED",
                   "L175 'means an author-visible or estimand-defining item changed and prior confirmatory artifacts "
                   "are not reusable'")

LIFECYCLE_CASES: dict[str, dict[str, Any]] = {
    # L175 "`EVALUATOR_REVISION_REQUIRED|reason=FROZEN_EVALUATOR_CHANGED` means a frozen evaluator
    # source/binary/tool-version/command/option/configuration changed"; L183 path (b).
    "FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED": {
        "disposition": _CONTROL,
        "stage_id": _STAGE,
        "error_class": _ERROR_CLASS_UNSTATED,
        "diagnostic": ("EVALUATOR_REVISION_REQUIRED|reason=FROZEN_EVALUATOR_CHANGED", "L175"),
        "required_action": ("new_evaluator_hashes_then_F16_then_rerun_every_slot_in_affected_scope_with_same_frozen_"
                            "artifact_bytes_no_new_confirmatory_generation", "L176 literal labelled M48"),
        "new_evaluator_version_hashes_required": (True, "L183 'assign a new evaluator version and hashes'"),
        "f16_required": (True, "L183 'run the frozen F16 eligibility procedure with fresh mutant-blind pilot seeds'"),
        "reuse_same_artifact_bytes": (True, "L183 'using the same already-generated artifact bytes'"),
        "new_confirmatory_generation_calls": (0, "L183 'and no new confirmatory generation calls'; L176 'zero new "
                                                 "confirmatory generation calls'"),
        "rerun_scope_rule": _token_unstated("L183 'If the revised evaluator component is shared across FIFO and UART, "
                                            "the affected scope is both designs and every arm x design slot; if it is "
                                            "design-specific, the affected scope is that design in both arms'"),
    },
    # L181 "If any shared study item changes after confirmatory generation begins, halt the
    # entire study and invalidate every scheduled slot across both designs and both arms".
    "SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED": {
        "disposition": _CONTROL,
        "stage_id": _STAGE,
        "error_class": _ERROR_CLASS_UNSTATED,
        "diagnostic": _AUTHORING_DIAG,
        "required_action": ("halt_study_invalidate_all_designs_and_all_arm_x_design_slots_archive_and_disclose_partial_"
                            "confirmatory_ledgers_new_preregistration_refreeze_f16_and_fresh_confirmatory_generation",
                            "L176 literal labelled M50"),
        "reuse_old_confirmatory_artifacts": (False, "L181 'No invalidated confirmatory artifact may be reused'"),
        "new_confirmatory_generation_required": (True, "L181 'fresh confirmatory generation for every affected slot'"),
        "affected_slots": _token_unstated("L181 'invalidate every scheduled slot across both designs and both arms'"),
        "archive_and_disclose_partial_ledgers": (True, "L181 'Preserve and archive every partial confirmatory ledger "
                                                       "... disclose the archived partial ledgers'"),
        "new_preregistration_required": (True, "L181 'A shared-item revision requires a new study preregistration'"),
    },
    # L181 "A change in design membership, estimand or any confirmatory weight after
    # confirmatory generation starts always requires a new preregistered study".
    "DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START": {
        "disposition": _CONTROL,
        "stage_id": _STAGE,
        "error_class": ("AUTHORING_REVISION_REQUIRED", "L175 'The M53 study-reset vector uses error class "
                                                       "AUTHORING_REVISION_REQUIRED'"),
        "diagnostic": (_AUTHORING_DIAG[0], "L175 '... and diagnostic AUTHORING_REVISION_REQUIRED|reason="
                                           "AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED'"),
        "required_action": ("archive_and_disclose_all_partial_confirmatory_ledgers_new_preregistration_refreeze_new_"
                            "design_set_and_weights_F16_then_generate_fresh_slots", "L176 literal labelled M53"),
        "old_confirmatory_artifacts_reusable": (False, "L181 'A study reset ... cannot retain old confirmatory "
                                                       "artifacts'"),
        "new_preregistration_required": (True, "L181 'always requires a new preregistered study'"),
        "all_partial_ledgers_archived_and_disclosed": (True, "L181 'archive and disclose all partial confirmatory "
                                                             "ledgers'"),
        "fresh_confirmatory_generation_required": (True, "L181 'generate fresh confirmatory slots under the newly "
                                                         "preregistered design set and weights'"),
    },
    # L175 "`HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED` is the `M54`
    # control-expectation diagnostic for validating the closed halt-signature component
    # domains and mapping"; domains from L185.
    "HALT_SIGNATURE_COMPONENT_ENUMERATION": {
        "disposition": _CONTROL,
        "stage_id": _STAGE,
        "error_class": ("HALT_SIGNATURE_SCHEMA", "L175 'M54 uses error class HALT_SIGNATURE_SCHEMA'"),
        "diagnostic": ("HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED", "L175"),
        "required_action": ("enforce_design_id_halt_code_evaluator_component_stable_error_class_stable_diagnostic_code_"
                            "domains_and_reason_to_component_mapping; exclude timestamps_process_ids_attempts_hosts_and_"
                            "trace_row_indices", "L176 literal labelled M54"),
        "design_id_values": (list(DESIGN_IDS), "L185 '`design_id` is `FIFO` or `UART`'"),
        "halt_code_values": (list(HALT_CODES), "L185 '`halt_code` is `SIMULATOR_ERROR`, `TRACE_INTEGRITY_FAILURE` "
                                               "or `RTL_NULL_CONTROL_FAILURE`'"),
        "evaluator_component_values": (list(EVALUATOR_COMPONENTS), "L185 '`evaluator_component` is `SIMULATOR`, ... "
                                                                   "or `RTL_NULL_COMPARATOR`'"),
        "stable_error_class_rule": _token_unstated("L185 'a simple exception class name ... for SIMULATOR_ERROR and the "
                                                   "literal NONE for the other two halt codes'"),
        "stable_diagnostic_code_rule": _token_unstated("L185 'stable_diagnostic_code is exactly the corresponding "
                                                       "halt_code token'"),
    },
    # L181 "If a design-specific author-visible item changes, halt and invalidate every slot
    # for that design in both arms."
    "DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED": {
        "disposition": _CONTROL,
        "stage_id": _STAGE,
        "error_class": _ERROR_CLASS_UNSTATED,
        "diagnostic": _AUTHORING_DIAG,
        "affected_scope": _token_unstated("L181 'halt and invalidate every slot for that design in both arms'"),
        "unaffected_design_scope": _token_unstated("L176 'M58 invalidates both arms for the affected design only when "
                                                   "membership, estimand and weights remain unchanged'"),
        "required_action": ("halt_affected_design_invalidate_both_arm_slots_refreeze_design_specific_materials_archive_"
                            "partial_ledgers_generate_fresh_confirmatory_slots_for_affected_design",
                            "L176 literal labelled M58"),
        "reuse_old_artifacts_for_affected_design": (False, "L181 'No invalidated confirmatory artifact may be reused'"),
        "new_study_preregistration_required_if_design_membership_estimand_or_weights_change": (
            True, "L181 'A change in design membership, estimand or any confirmatory weight after confirmatory "
                  "generation starts always requires a new preregistered study, even if the changed item is otherwise "
                  "described as design-specific'"),
    },
}


def lifecycle_expectation(change_class: str) -> tuple[dict, dict[str, str]]:
    """(record of supported fields in order, {field: reason} for unsupported fields)."""
    case = LIFECYCLE_CASES.get(change_class)
    if case is None:
        raise ValueError(f"change_class {change_class!r} names no Protocol lifecycle case")
    record, missing = {}, {}
    for name, entry in case.items():
        if isinstance(entry, Unsupported):
            missing[name] = entry.reason
        else:
            record[name] = entry[0]
    return record, missing


# --- D-024: the same cases under the v1.3.7 CANDIDATE pack (not audited) ----------------
#
# Used only when the runner is given `--pack v1.3.7-candidate` (proposals/v1.3.7/pack). Corrections
# C1-C3 state as rules what v1.3.6 leaves UNSUPPORTED above; every other field keeps its v1.3.6
# derivation and citation. Citations are to the candidate Protocol, whose lines are numbered as
# in v1.3.6 (every correction stays inside its line).

# Candidate L175 (C1): "a control expectation whose diagnostic CODE is `EVALUATOR_REVISION_REQUIRED` has error
# class `EVALUATOR_REVISION_REQUIRED`; one whose CODE is `AUTHORING_REVISION_REQUIRED` has error class
# `AUTHORING_REVISION_REQUIRED`; and one whose CODE is `HALT_SIGNATURE_SCHEMA` has error class
# `HALT_SIGNATURE_SCHEMA`. This rule applies only to these three codes".
REVISION_CODES = ("EVALUATOR_REVISION_REQUIRED", "AUTHORING_REVISION_REQUIRED", "HALT_SIGNATURE_SCHEMA")


def revision_error_class(diagnostic: str) -> str:
    """Candidate L175 (C1): the error class of a change-class control expectation, from its diagnostic CODE."""
    code = diagnostic.split("|", 1)[0]
    if code not in REVISION_CODES:
        raise ValueError(f"candidate L175 states no error class for CODE {code!r}")
    return code


# Candidate L176 (C2) "Closed scope tokens (OWNER-DECIDED OD-3: owner vocabulary adopted by owner decision D-027 ...)"
# and §20.3 (OD-3), and L185 (C3) "(rule token ...)": (value, citation). D-027: the scope tokens are owner
# vocabulary (OD-3), not pack-derived; the rule tokens label rules L185 states (C3).
CANDIDATE_TOKENS: dict[str, dict[str, tuple[str, str]]] = {
    "FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED": {
        "rerun_scope_rule": ("shared_evaluator_component_all_designs_and_all_arm_x_design_slots; "
                             "design_specific_component_affected_design_in_both_arms",
                             "candidate L176 'for an evaluator revision, `rerun_scope_rule` = ...' (OD-3); §20.3")},
    "SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED": {
        "affected_slots": ("all_designs_x_all_arms", "candidate L176 'For a shared-item revision, `affected_slots` = ...' (OD-3); §20.3")},
    "DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED": {
        "affected_scope": ("affected_design_in_both_arms",
                           "candidate L176 'For a design-specific revision, `affected_scope` = ...' (OD-3); §20.3"),
        "unaffected_design_scope": ("not_invalidated_when_membership_estimand_and_weights_are_unchanged",
                                    "candidate L176 '... and `unaffected_design_scope` = ...' (OD-3); §20.3")},
    "HALT_SIGNATURE_COMPONENT_ENUMERATION": {
        "stable_error_class_rule": ("simple_exception_class_for_SIMULATOR_ERROR_else_NONE",
                                    "candidate L185 '(rule token `stable_error_class_rule` = ...)'"),
        "stable_diagnostic_code_rule": ("exact_halt_code_token",
                                        "candidate L185 '(rule token `stable_diagnostic_code_rule` = ...)'")},
}


def lifecycle_expectation_candidate(change_class: str) -> tuple[dict, dict[str, str]]:
    """As lifecycle_expectation, under the v1.3.7 CANDIDATE Protocol, for one of the four change classes or the
    halt-signature domain validation (`HALT_SIGNATURE_COMPONENT_ENUMERATION`, not a change class under OD-3, D-027);
    the schema of every result is candidate Protocol §20 (OD-3). The error class is by the C1 rule
    (for every case, so v1.3.6's per-fixture L175 sentences are not used), the C2/C3 tokens from
    CANDIDATE_TOKENS, and every other field as in v1.3.6. `required_action` is the candidate L176 literal
    keyed by this change class (C2). A field still unsupported is reported, never filled."""
    case = LIFECYCLE_CASES.get(change_class)
    if case is None:
        raise ValueError(f"{change_class!r} names no candidate L176 change class or domain validation")
    tokens = CANDIDATE_TOKENS.get(change_class, {})
    record, missing = {}, {}
    for name, entry in case.items():
        if name == "error_class":
            record[name] = revision_error_class(case["diagnostic"][0])
        elif isinstance(entry, Unsupported):
            if name in tokens:
                record[name] = tokens[name][0]
            else:
                missing[name] = entry.reason
        else:
            record[name] = entry[0]
    return record, missing
