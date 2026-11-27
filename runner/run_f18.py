"""F18 fixture runner (v1.3.6).

Implements the runner duties in Catalog (file 36) "Fixture requirements" 1-6 and L176:
verify the index, every descriptor's SHA-256 and byte length, the exact count (144),
then execute each fixture and compare exact expected values.

Rules (CLAUDE.md): the code path is chosen from the fixture INPUT shape only, never
from its ID or expected output. A fixture whose path reaches a stage that is not yet
implemented is reported NOT_IMPLEMENTED -- never PASS.

Usage (evidence, D-002a):  runner/run_f18_container.sh <run_class> [f18 [<pack>]]
Usage (development only):  python3.11 -I runner/run_f18.py <pack_root> <evidence_dir> <run_class> [--pack <pack>]

D-024: <pack> is `v1.3.6` (default, the baseline) or `v1.3.7-candidate` (proposals/v1.3.7/pack, v1.3.7 CANDIDATE,
not audited). The pack selects the pinned index hash and the adapter table; v1.3.6 behaviour is unchanged.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "runner"))  # `-I` leaves the script directory off (adapters_v137)

from openvef.envelope import Envelope, Failure, parse_envelope  # noqa: E402
from openvef.schema import SCHEMA_REL, ValidatedResponse, load_validator, validate_clause_ids, validate_schema  # noqa: E402
from openvef.import_policy import check_import_policy  # noqa: E402
from openvef.ast_signature import check_ast_signature, check_compile  # noqa: E402
from openvef.assembler import (CLAUSE_ID_REGEX_DEFAULT, NEAR_MATCH_REGEX_DEFAULT, RESERVED_HEADINGS,  # noqa: E402
                               SEARCH_REGEX_DEFAULT, check_reserved_heading_lines,  # noqa: E402
                               check_unresolved_placeholders, check_visible_clause_ids)
from openvef.runtime import RuntimeStageError, factory_checks  # noqa: E402
from openvef import runtime_basis  # noqa: E402
from openvef.sandbox import SandboxUnavailable, broker_mode, ensure_image  # noqa: E402
from openvef import simulator_stages  # noqa: E402
from openvef.simulation import SimulationError  # noqa: E402
from openvef.ledger import HaltSignature, SignatureDomainError  # noqa: E402
from openvef.stage_map import (EventError, NotDetermined, adjudicate_checker, first_event,  # noqa: E402
                               outcome_from_record, paired_run_failure, runtime_signature_failure, validate_vector)
from openvef.source_ast import UnsettledSpec, check_sources  # noqa: E402
import adapters_v137  # noqa: E402  (same directory; D-024 candidate-only rows)

INDEX_REL = "41_F18_Fixture_Inputs/fixture-index.json"
INDEX_SHA256 = "f37808c7a662b8fdf164e27feaef023aadd6dfefaada35d11c3719185d1bde54"
EXPECTED_COUNT = 144
COMPARE_KEYS = ("disposition", "stage_id", "error_class", "diagnostic")
# 27_SHA256SUMS.txt entry for the canonical response schema (File 30 §1).
SCHEMA_SHA256 = "6fb5d282b09540949f21ee134b522841c3345031cb3e118a83bdffc18b4e7c34"
PINNED_DISTRIBUTIONS = ("jsonschema", "attrs", "jsonschema-specifications", "referencing", "rpds-py",
                        "typing_extensions", "cocotb", "find-libpython", "iniconfig", "packaging", "pluggy",
                        "pygments", "pytest")
# D-002a: the pinned interpreter for all F18 evidence is CPython 3.11.18 in the
# python:3.11.18-slim image pinned by digest (docs/sandbox.md).
PINNED_PYTHON_VERSION = "3.11.18 (main, Nov  5 2026, 07:57:53) [GCC 14.2.0]"
PINNED_PYTHON_SHA256 = "92d7e40ec50be176cb1b790c7568b7e08cd862137b5aa69f1413ba1967886b79"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


class IntegrityError(Exception):
    pass


ACTIVE_INDEX_SHA256 = INDEX_SHA256  # D-024: set by main() from --pack


def load_index(root: Path) -> list[dict]:
    index_path = root / INDEX_REL
    raw = index_path.read_bytes()
    if sha256_bytes(raw) != ACTIVE_INDEX_SHA256:
        raise IntegrityError(f"fixture index SHA-256 mismatch: {sha256_bytes(raw)}")
    fixtures = json.loads(raw)["fixtures"]
    ids = [f["fixture_id"] for f in fixtures]
    if len(fixtures) != EXPECTED_COUNT:
        raise IntegrityError(f"fixture count {len(fixtures)} != {EXPECTED_COUNT}")
    if len(set(ids)) != len(ids):
        raise IntegrityError("duplicate fixture IDs in index")
    on_disk = {p.name for p in (root / "41_F18_Fixture_Inputs").glob("*.json")} - {"fixture-index.json"}
    listed = {Path(f["path"]).name for f in fixtures}
    if on_disk != listed:
        raise IntegrityError(f"unlisted or missing descriptors: {sorted(on_disk ^ listed)}")
    return fixtures


def load_descriptor(root: Path, entry: dict) -> dict:
    raw = (root / entry["path"]).read_bytes()
    if len(raw) != entry["bytes"] or sha256_bytes(raw) != entry["sha256"]:
        raise IntegrityError(f"{entry['fixture_id']}: descriptor hash/length mismatch")
    desc = json.loads(raw)
    if desc["fixture_id"] != entry["fixture_id"]:
        raise IntegrityError(f"{entry['fixture_id']}: descriptor ID mismatch")
    if desc["expected"] != entry["expected"]:
        raise IntegrityError(f"{entry['fixture_id']}: index/descriptor expected mismatch")
    return desc


def load_schema_validator(root: Path):
    path = root / SCHEMA_REL
    if sha256_file(path) != SCHEMA_SHA256:
        raise IntegrityError(f"response schema SHA-256 mismatch: {sha256_file(path)}")
    return load_validator(path)


def failure_record(result: Failure) -> dict:
    return {
        "disposition": result.disposition,
        "stage_id": result.stage_id,
        "error_class": result.error_class,
        "diagnostic": result.diagnostic,
    }


class Blocked(Exception):
    """The fixture reaches a stage or rule that is not implemented (NOT_IMPLEMENTED)."""


ACCEPT = {"disposition": "ACCEPT", "stage_id": None, "error_class": None, "diagnostic": None}


SANDBOX: dict | None = None  # set by main() once the pinned image is verified
# D-005 DRAFT design materials for L166 (7)-(11); set by main(). Every result that uses
# them says what is still provisional or was cleared under a deviation (simulator_stages.prepare).
DESIGN_MATERIALS_FILE = "design/fifo/design-materials-DRAFT.json"
SIM: dict | None = None
SIM_UNAVAILABLE = "not prepared"
RUNTIME_BASIS: dict | None = None  # D-019: whether the runtime checks of the current fixture could be forged
# D-020: a SELF_REPORTED pass stays PASS with this visible label (like DEV-001), listed per record
# and in the summary. See docs/sandbox.md "Runtime checks" and docs/DEVIATIONS.md "Open residual (D-019)".
SELF_REPORTED_LABEL = "SELF_REPORTED (D-020): runtime check not statically PROVEN"
PROVISIONAL: dict = {}  # fixture descriptor id -> simulator details, filled by sim_stages


def source_stages(driver_source: str, checker_source: str) -> Failure | None:
    """SOURCE_AST, IMPORT_POLICY, static AST_SIGNATURE, COMPILE_DRIVER, COMPILE_CHECKER
    (Protocol §3.4 evaluation order (2)-(6)), then the sandboxed runtime import, factory
    return-type and signature checks (File 30 §3 L27, L39; L166 (7)). None means every
    implemented stage passed."""
    sources = {"driver.py": driver_source, "checker.py": checker_source}
    try:
        trees = check_sources(list(sources.items()))
        if isinstance(trees, Failure):
            return trees
        static = check_import_policy(sources, trees) or check_ast_signature(trees) or check_compile(sources)
    except UnsettledSpec as exc:
        raise Blocked(f"blocked on docs/ambiguities.md {exc}") from exc
    if static is not None:
        return static
    global RUNTIME_BASIS
    RUNTIME_BASIS = {name: runtime_basis.basis(name, text) for name, text in sources.items()}
    if SANDBOX is None:
        raise Blocked("static stages and compilation passed; sandbox unavailable, runtime stage not run")
    return factory_checks(driver_source)


def response_object(inp: dict) -> dict:
    """The response object a response input carries (envelope already accepted)."""
    if "response_object" in inp:
        return inp["response_object"]
    raw = (inp["raw_response_utf8"].encode("utf-8") if "raw_response_utf8" in inp
           else base64.b64decode(inp["raw_response_base64"], validate=True))
    return parse_envelope(raw, inp.get("provider_finish_reason")).obj


def sim_stages(desc: dict, obj: dict) -> Failure | None:
    """L166 (7)-(11) on the design materials (D-005); see SIM provisional/cleared."""
    if SIM is None:
        raise Blocked(RUNTIME_NEXT + f" [D-005 materials: {SIM_UNAVAILABLE}]")
    failure, details = simulator_stages.run_response(SIM, obj["driver"]["source"], obj["checker"]["source"])
    PROVISIONAL[id(desc)] = details
    return failure


def response_stages(desc: dict, inp: dict, validator) -> Failure | None:
    """Evaluation order (1)-(6) for a response input; None if all of them pass."""
    raw: bytes | None = None
    if "raw_response_utf8" in inp:
        raw = inp["raw_response_utf8"].encode("utf-8")
    elif "raw_response_base64" in inp:
        raw = base64.b64decode(inp["raw_response_base64"], validate=True)
    if raw is not None:
        envelope = parse_envelope(raw, inp.get("provider_finish_reason"))
        if isinstance(envelope, Failure):
            return envelope
        obj = envelope.obj
    else:
        # A-002 (owner decision): skip envelope decoding only.
        obj = inp["response_object"]
    # PARSE_SCHEMA part 1b; manifest clause_ids from the descriptor (A-005).
    checked = validate_schema(validator, obj)
    if isinstance(checked, ValidatedResponse):
        checked = validate_clause_ids(checked, desc["manifest_clause_ids"])
    if isinstance(checked, Failure):
        return checked
    return source_stages(obj["driver"]["source"], obj["checker"]["source"])


# L166 (7)-(11) are implemented (src/openvef/simulation.py, sandbox/sim.py; D-003 toolchain)
# but need inputs that are owner-written or TO FREEZE and absent from the pack.
MISSING_DESIGN_MATERIALS = ("FIFO RTL and null netlist; port manifest with widths; reset sequence; legal-input "
                            "predicate (owner-written FIFO specification, Scope); cycle cap, safe-idle vector and "
                            "watchdog formula (TO FREEZE, Protocol L229); observation mask (owner-written); "
                            "checker trace schema and metadata (TO FREEZE, L543)")
RUNTIME_NEXT = ("runtime import, factory and signature checks passed in the sandbox; L166 (7)-(11) simulator "
                "stages are built but blocked on design materials absent from the pack: " + MISSING_DESIGN_MATERIALS)


def two_runs(runs) -> tuple:
    if not isinstance(runs, list) or len(runs) != 2 or not all(isinstance(r, dict) for r in runs):
        raise Blocked("checker adjudication needs exactly two run records (L166 steps (9)-(10))")
    return outcome_from_record(runs[0]), outcome_from_record(runs[1])


def in_domain(ok: bool, name: str) -> None:
    """Every input property is checked against its cited domain (D-015, A8-2)."""
    if not ok:
        raise Blocked(f"{name} outside its cited domain")


def utf8_text(value, bom_ok: bool = True) -> bool:
    """A string that has UTF-8 bytes (D-017). File 31 L26, L74 also reject a BOM."""
    try:
        return isinstance(value, str) and bool(value.encode("utf-8") or True) and (bom_ok or not value.startswith("\ufeff"))
    except UnicodeEncodeError:
        return False


def base64_text(value) -> bool:
    try:
        return isinstance(value, str) and base64.b64decode(value, validate=True) is not None
    except ValueError:
        return False


def strings(value) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def adapt_response(desc: dict, validator) -> Failure | dict | None:
    in_domain(utf8_text(desc["input"].get("raw_response_utf8", "")) and base64_text(desc["input"].get("raw_response_base64", "")),
              "raw response")
    if desc["input"].get("provider_finish_reason", "stop") not in ("length", "stop"):
        raise Blocked("provider finish reason outside the cited values")
    result = response_stages(desc, desc["input"], validator)
    return sim_stages(desc, response_object(desc["input"])) if result is None else result


def adapt_source_pair(desc: dict, validator) -> Failure | dict | None:
    """A-012 source pair."""
    in_domain(strings(list(desc["input"].values())), "source pair")
    result = source_stages(desc["input"]["driver_source"], desc["input"]["checker_source"])
    if result is None:
        raise Blocked(RUNTIME_NEXT)
    return result


def adapt_null_runs(desc: dict, validator) -> Failure | dict | None:
    """A-028: run every implemented response stage first; the supplied outcomes stand in."""
    inp = desc["input"]
    result = response_stages(desc, {"response_object": inp["response_object"]}, validator)
    return adjudicate_checker(*two_runs(inp["null_runs"])) if result is None else result


def adapt_events(desc: dict, validator) -> Failure | dict | None:
    events = desc["input"]["events"]
    in_domain(isinstance(events, list) and all(isinstance(e, dict) for e in events), "events")
    return first_event(events)  # A-025


def adapt_checker_runs(desc: dict, validator) -> Failure | dict | None:
    return adjudicate_checker(*two_runs(desc["input"]["checker_runs"]))  # A-026


def adapt_halt_recurrence(desc: dict, validator) -> Failure | dict | None:
    """Ledger, Protocol L185. An out-of-domain supplied signature is a fixture defect (D-012)."""
    inp = desc["input"]
    in_domain(inp["design_id"] in ("FIFO", "UART"), "design_id")
    in_domain(type(inp["recovery_cycles_used"]) is int and inp["recovery_cycles_used"] == 1, "recovery_cycles_used")
    in_domain(type(inp["scheduled_slots"]) is int and inp["scheduled_slots"] >= 1, "scheduled_slots")  # A-055: no stated maximum
    in_domain(all(isinstance(inp[k], dict) for k in ("first_halt_signature", "second_halt_signature")), "halt signature")
    try:
        first, second = (HaltSignature.given(inp[k]) for k in ("first_halt_signature", "second_halt_signature"))
    except SignatureDomainError as exc:
        raise Blocked(f"PD-01 fixture defect: supplied halt signature outside the Protocol L185 domains: {exc}") from exc
    raise Blocked(f"PD-26: signatures valid (identical: {first == second}), but the pack states no error class for "
                  "DESIGN_HALT_REPEATED")


def adapt_clause_ids(desc: dict, validator) -> Failure | dict | None:
    """The patterns are File 31 §8's; a supplied pattern must equal it and is never used (D-015)."""
    inp = desc["input"]
    ids = inp["manifest_clause_ids"]
    in_domain(utf8_text(inp["visible_payload"], bom_ok=False), "visible_payload")
    in_domain(strings(ids) and ids == sorted(set(ids)) and all(re.fullmatch(CLAUSE_ID_REGEX_DEFAULT, i) for i in ids),
              "manifest_clause_ids")
    for name, fixed in (("clause_id_regex", CLAUSE_ID_REGEX_DEFAULT), ("clause_id_search_regex", SEARCH_REGEX_DEFAULT),
                        ("clause_id_near_match_regex", NEAR_MATCH_REGEX_DEFAULT)):
        in_domain(inp.get(name, fixed) == fixed, name)
    result = check_visible_clause_ids(inp["visible_payload"], ids)
    return rejected(result)


def rejected(result: Failure | None) -> Failure:
    """A packet or local check's rejection; the pack defines no record for "not rejected"."""
    if result is None:
        raise Blocked("check passed; nothing further to compare")
    return result


def adapt_reserved_headings(desc: dict, validator) -> Failure | dict | None:
    """The headings are the sidecar's; supplied ones must be a subset and are never used (D-015)."""
    supplied = desc["input"]["reserved_headings"]
    in_domain(strings(supplied) and set(supplied) <= set(RESERVED_HEADINGS), "reserved_headings")
    in_domain(utf8_text(desc["input"]["payload"], bom_ok=False), "payload")
    return rejected(check_reserved_heading_lines(desc["input"]["payload"]))


def adapt_rendered(desc: dict, validator) -> Failure | dict | None:
    in_domain(utf8_text(desc["input"]["rendered"], bom_ok=False), "rendered")
    return rejected(check_unresolved_placeholders(desc["input"]["rendered"]))


# File 30 L35, L37: the parameter names the runtime signature must confirm.
REQUIRED_PARAMETERS = {("driver.py", "create_driver"): ["seed"],
                       ("driver.py", "Driver.step"): ["self", "cycle_index", "outputs_after_edge"],
                       ("checker.py", "check_trace"): ["trace", "metadata"]}


def adapt_runtime_signature(desc: dict, validator) -> Failure | dict | None:
    sig = desc["input"]["runtime_signature"]
    if not isinstance(sig, dict) or set(sig) != {"file", "symbol", "actual", "expected"} or not strings(sig["actual"]):
        raise Blocked("runtime signature outside the contract's fields")
    in_domain(isinstance(sig["file"], str) and isinstance(sig["symbol"], str), "runtime_signature")
    required = REQUIRED_PARAMETERS.get((sig["file"], sig["symbol"]))
    if required is None or sig["expected"] != required:
        raise Blocked("runtime signature: not a File 30 L35/L37 entry point, or its required parameters differ")
    return rejected(runtime_signature_failure(sig["file"], sig["symbol"], sig["actual"], required))


def adapt_vector_keys(desc: dict, validator) -> Failure | dict | None:
    """File 30 L83 (a)-(b); a vector passing them is not determined without widths (A-027)."""
    ports = desc["input"]["expected_keys"]
    in_domain(strings(ports) and len(ports) == len(set(ports)) > 0, "expected_keys")
    return rejected(validate_vector(desc["input"]["driver_return"], ports))


def adapt_paired_runs(desc: dict, validator) -> Failure | dict | None:
    runs = desc["input"]["paired_runs"]
    fields = ("first_raw_output_divergence_cycle", "first_next_input_divergence_cycle")
    if not isinstance(runs, dict) or set(runs) != set(fields) or not all(runs[f] is None or (type(runs[f]) is int and runs[f] >= 0) for f in fields):
        raise Blocked("paired runs outside the contract's fields")
    return rejected(paired_run_failure(*(runs[f] for f in fields)))


# (required keys, optional keys, adapter). This table is the ONLY place an input shape
# selects code. D-013: each adapter needs an input contract cited to the pack
# (runner/adapter_contracts.py) and at least three synthetic non-fixture vectors, and
# D-017 boundary pairs per property (tests/adapter_vectors.py); tests/test_dispatch_shapes.py enforces both.
ADAPTERS = (
    ({"raw_response_utf8"}, {"provider_finish_reason"}, adapt_response),
    ({"raw_response_base64"}, set(), adapt_response),
    ({"response_object"}, set(), adapt_response),
    ({"driver_source", "checker_source"}, set(), adapt_source_pair),
    ({"null_runs", "response_object"}, set(), adapt_null_runs),
    ({"events"}, set(), adapt_events),
    ({"checker_runs"}, set(), adapt_checker_runs),
    ({"design_id", "recovery_cycles_used", "first_halt_signature", "second_halt_signature", "scheduled_slots"}, set(),
     adapt_halt_recurrence),
    ({"visible_payload", "manifest_clause_ids", "clause_id_regex"},
     {"clause_id_search_regex", "clause_id_near_match_regex"}, adapt_clause_ids),
    ({"payload", "reserved_headings"}, set(), adapt_reserved_headings),
    ({"rendered"}, set(), adapt_rendered),
    ({"runtime_signature"}, set(), adapt_runtime_signature),
    ({"driver_return", "expected_keys"}, set(), adapt_vector_keys),
    ({"paired_runs"}, set(), adapt_paired_runs),
)


# D-024: the pack selects the table. v1.3.7-candidate adds rows whose contracts cite candidate text only
# (runner/adapters_v137.py); v1.3.6 uses ADAPTERS unchanged.
PACKS = {
    "v1.3.6": {"index_sha256": INDEX_SHA256, "adapters": ADAPTERS, "label": None},
    "v1.3.7-candidate": {"index_sha256": "18c346368a81f8411f54ffab5c09affaa83fe8f185108656bb0c2a8b19d73523",
                         "adapters": tuple((req, opt, adapters_v137.REPLACEMENTS.get(fn.__name__, fn))
                                           for req, opt, fn in ADAPTERS) + adapters_v137.ROWS,
                         "label": "v1.3.7 CANDIDATE, not audited", "manifest": "SHA256SUMS-v1.3.7-candidate.txt",
                         "manifest_sha256": "e704d194284c51bcac0f6ad20c119645c679bfce10fc71fe493ed0c02c9d7893",
                         # D-026: OWNER-SPECIFIED rows and the input shapes the owners left unspecified
                         "owner_specified": adapters_v137.OWNER_SPECIFIED, "open_shapes": adapters_v137.OPEN_SHAPES,
                         # D-027: the OWNER-DECIDED rules (OD-n) each candidate adapter rests on
                         "owner_decided": adapters_v137.OWNER_DECIDED},
}
ADAPTER_TABLE = ADAPTERS  # set by main() from --pack
OWNER_SPECIFIED_ROWS: dict = {}  # D-026: adapter name -> OS item; set by main() from --pack (empty for v1.3.6)
OPEN_SHAPES: tuple = ()  # D-026: (required, optional, OS item, reason) the owners left unspecified
OWNER_SPEC: str | None = None  # the OS item of the current fixture, set by dispatch(); None = pack-derived
OWNER_DECIDED_ROWS: dict = {}  # D-027: adapter name -> OD rules; set by main() from --pack (empty for v1.3.6)
OWNER_DEC: tuple = ()  # the OD rules of the current fixture's adapter, set by dispatch()
OWNER_SPECIFIED = "OWNER-SPECIFIED"
OWNER_DECIDED = "OWNER-DECIDED"
PACK_DERIVED = "PACK-DERIVED"


def category(owner_decided: tuple, owner_spec: str | None) -> str:
    """D-027: a fixture that depends on any OD rule counts OWNER-DECIDED, also when it is OWNER-SPECIFIED (A-059);
    otherwise an OS item counts OWNER-SPECIFIED (D-026); otherwise PACK-DERIVED."""
    return OWNER_DECIDED if owner_decided else OWNER_SPECIFIED if owner_spec else PACK_DERIVED


def find_adapters(inp: dict, table=None) -> list:
    """Every row of the active table whose key sets fit the input (at most one)."""
    keys = set(inp)
    return [row for row in (ADAPTER_TABLE if table is None else table) if row[0] <= keys <= row[0] | row[1]]


def dispatch(desc: dict, validator) -> Failure | dict | None:
    """The outcome for one descriptor: a Failure, a full record, or None (ACCEPT).

    The code path is chosen from the input's key set only (CLAUDE.md rule 4).
    """
    global OWNER_SPEC, OWNER_DEC
    rows = find_adapters(desc["input"])
    if not rows:
        raise Blocked(no_adapter_reason(desc["input"]))
    OWNER_SPEC = OWNER_SPECIFIED_ROWS.get(rows[0][2].__name__)
    OWNER_DEC = tuple(OWNER_DECIDED_ROWS.get(rows[0][2].__name__, ()))
    return rows[0][2](desc, validator)


def no_adapter_reason(inp: dict) -> str:
    """Why an input has no adapter. D-026: an OWNER-SPECIFIED shape left unspecified (OS-3) says so, and is labelled."""
    global OWNER_SPEC
    open_rows = find_adapters(inp, OPEN_SHAPES)
    if open_rows:
        OWNER_SPEC = open_rows[0][2]
        return f"{OWNER_SPEC} ({OWNER_SPECIFIED}, D-026): {open_rows[0][3]}"
    return f"no adapter for this input shape: {sorted(inp)}"


def execute(desc: dict, validator) -> tuple[str, dict | None, str]:
    """Return (status, actual, note)."""
    try:
        outcome = dispatch(desc, validator)
    except (Blocked, NotDetermined) as exc:
        return "NOT_IMPLEMENTED", None, str(exc)
    except EventError as exc:
        return "NOT_IMPLEMENTED", None, f"input outside the adapter vocabulary: {exc}"
    if outcome is None:
        return "EXECUTED", dict(ACCEPT), ""
    if isinstance(outcome, Failure):
        return "EXECUTED", failure_record(outcome), ""
    return "EXECUTED", outcome, ""


def installed_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def git_commit() -> str:
    if broker_mode():  # D-002a: the host broker reads git; the runner container has no git
        return os.environ["OPENVEF_GIT_COMMIT"]
    try:
        out = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        dirty = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--", "src", "runner", "sandbox",
                                "design", "docs/fifo-spec-v0.2.md"],
                               capture_output=True, text=True, check=True).stdout.strip()
        return out.stdout.strip() + ("+UNCOMMITTED_CHANGES" if dirty else "")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "NO_GIT_COMMIT"


def utc_stamp() -> str:
    """ISO 8601 UTC time with milliseconds, for each run.log fixture line (§3 item 6)."""
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def self_reported_parts(note: str, basis: dict | None) -> tuple[str, dict, list]:
    """D-020/D-021: the note, the extra record fields and the SELF_REPORTED file names for one
    fixture. The verdict is not touched."""
    if basis is None:
        return note, {}, []
    extra: dict = {"runtime_checks": basis}
    sr = sorted(name for name, b in basis.items() if b["basis"] != runtime_basis.PROVEN)
    if sr:
        note = f"{note} [{SELF_REPORTED_LABEL}: {', '.join(sr)}]".strip()
        extra.update(self_reported_runtime_checks=sr, self_reported_label=SELF_REPORTED_LABEL)
    return note, extra, sr


def verify_pack_manifest(root: Path, manifest: str, pinned: str) -> int:
    """D-025 item 1: the pinned manifest's hash, every file it lists, and no unlisted file. Returns the file count."""
    raw = (root / manifest).read_bytes()
    if sha256_bytes(raw) != pinned:
        raise IntegrityError(f"pack manifest SHA-256 mismatch: {sha256_bytes(raw)}")
    listed = set()
    for entry in raw.decode("utf-8").splitlines():
        digest, rel = entry.split("  ", 1)
        path = root / rel
        if ".." in Path(rel).parts or not path.is_file() or sha256_file(path) != digest:
            raise IntegrityError(f"pack file does not match its manifest: {rel}")
        listed.add(rel)
    on_disk = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()} - {manifest}
    if on_disk != listed:
        raise IntegrityError(f"pack files not in the manifest, or missing: {sorted(on_disk ^ listed)}")
    return len(listed)


def parse_args(argv: list[str]) -> tuple[Path, Path, str, str]:
    args = list(argv[1:])
    pack = "v1.3.6"
    if "--pack" in args:
        i = args.index("--pack")
        pack = args[i + 1]
        del args[i:i + 2]
    if len(args) != 3 or pack not in PACKS:
        raise SystemExit(f"usage: run_f18.py <pack_root> <evidence_dir> <run_class> [--pack {{{','.join(PACKS)}}}]")
    return Path(args[0]), Path(args[1]), args[2], pack


def main() -> int:
    global ADAPTER_TABLE, ACTIVE_INDEX_SHA256, OWNER_SPECIFIED_ROWS, OPEN_SHAPES, OWNER_SPEC, OWNER_DECIDED_ROWS, OWNER_DEC
    root, evidence_root, run_class, pack = parse_args(sys.argv)
    pack_info = PACKS[pack]
    ADAPTER_TABLE, ACTIVE_INDEX_SHA256 = pack_info["adapters"], pack_info["index_sha256"]
    OWNER_SPECIFIED_ROWS, OPEN_SHAPES = pack_info.get("owner_specified", {}), pack_info.get("open_shapes", ())
    OWNER_DECIDED_ROWS = pack_info.get("owner_decided", {})
    if broker_mode():  # D-002a: the broker created and mounted the (empty) run directory
        started = os.environ["OPENVEF_RUN_STARTED"]
        out_dir = evidence_root
        if any(out_dir.iterdir()):
            raise IntegrityError("evidence directory is not empty")
    else:
        started = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = evidence_root / f"run-{started}"
        out_dir.mkdir(parents=True, exist_ok=False)

    source_files = sorted([*(REPO / "src").rglob("*.py"), *(REPO / "runner").rglob("*.py"),
                           *(REPO / "sandbox").glob("*"), *(p for p in (REPO / "design").rglob("*") if p.is_file())])
    global SANDBOX
    try:
        SANDBOX = ensure_image()
    except (SandboxUnavailable, FileNotFoundError) as exc:
        SANDBOX = None
        print(f"sandbox unavailable: {exc}", file=sys.stderr)
    if broker_mode() and SANDBOX is None:
        raise SystemExit("D-002a: the runner container must have the sandbox identity")
    py_sha = sha256_file(Path(os.path.realpath(sys.executable)))
    pinned = broker_mode() and sys.version == PINNED_PYTHON_VERSION and py_sha == PINNED_PYTHON_SHA256
    meta = {
        "run_started_utc": started,
        "run_class": run_class,
        "interpreter_status": ("PINNED (D-002a: runner and artifacts in the pinned image)" if pinned else
                               "NOT_PINNED: development run, not F18 evidence (D-002a)"),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "python_executable_sha256": py_sha,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "fixture_index_sha256": pack_info["index_sha256"],
        "response_schema_sha256": SCHEMA_SHA256,
        "distributions": {name: installed_version(name) for name in PINNED_DISTRIBUTIONS},
        "git_commit": git_commit(),
        "source_sha256": {str(p.relative_to(REPO)): sha256_file(p) for p in source_files},
        "command": [sys.executable, *sys.argv],
        "sandbox": SANDBOX,
    }
    if pack_info["label"]:  # D-024: v1.3.6 records are unchanged; a candidate run says what it ran
        meta["pack"] = pack
        meta["pack_label"] = pack_info["label"]
        meta["pack_manifest_sha256"] = sha256_file(root / pack_info["manifest"])
        # D-025 item 1: verify before any fixture runs; only then may the C5 predicate run (IntegrityError aborts).
        meta["pack_manifest_files_verified"] = verify_pack_manifest(root, pack_info["manifest"], pack_info["manifest_sha256"])
        adapters_v137.PACK_VERIFIED = True

    global SIM, SIM_UNAVAILABLE, RUNTIME_BASIS
    if SANDBOX is not None:
        try:
            SIM = simulator_stages.prepare(REPO, DESIGN_MATERIALS_FILE)
            meta["design_materials"] = SIM["record"]
        except (OSError, KeyError, ValueError, SimulationError) as exc:
            SIM, SIM_UNAVAILABLE = None, f"{type(exc).__name__}: {exc}"
            meta["design_materials"] = {"unavailable": SIM_UNAVAILABLE}
    provisional_ids: list = []
    deviation_ids: list = []
    self_reported: list = []
    counts = {"PASS": 0, "FAIL": 0, "NOT_IMPLEMENTED": 0, "ERROR": 0}
    by_category = {c: dict.fromkeys(counts, 0) for c in (PACK_DERIVED, OWNER_DECIDED, OWNER_SPECIFIED)}  # D-026, D-027
    owner_specified_ids: dict = {}
    owner_decided_ids: dict = {}
    with open(out_dir / "results.jsonl", "w", encoding="utf-8") as res, open(out_dir / "run.log", "w", encoding="utf-8") as log:
        log.write(json.dumps(meta, indent=2) + "\n")
        fixtures = load_index(root)  # IntegrityError aborts the whole run
        validator = load_schema_validator(root)
        for entry in fixtures:
            desc = load_descriptor(root, entry)
            expected = desc["expected"]
            RUNTIME_BASIS = None
            OWNER_SPEC, OWNER_DEC = None, ()
            adapters_v137.take_od_used()  # D-027: path-only OD rules are counted per fixture
            try:
                status, actual, note = execute(desc, validator)
            except Exception as exc:  # recorded, never hidden
                status, actual, note = "ERROR", None, f"{type(exc).__name__}: {exc}"
            owner_dec = tuple(sorted(set(OWNER_DEC) | set(adapters_v137.take_od_used()))) if pack_info["label"] else ()
            if status == "EXECUTED":
                # Standard expectations compare the four fields; a control-vector
                # expectation compares the whole object exactly (A-032).
                status = "PASS" if actual == expected else "FAIL"
            counts[status] += 1
            # D-021: the label goes into the note before the record is built, so that every output agrees.
            note, extra, sr = self_reported_parts(note, RUNTIME_BASIS)
            rec = {"fixture_id": entry["fixture_id"], "descriptor_sha256": entry["sha256"], "status": status,
                   "expected": expected, "actual": actual, "note": note, **extra}
            if pack_info["label"]:
                rec["pack_label"] = pack_info["label"]
                # D-026, D-027: every record says whether its path is PACK-DERIVED, OWNER-DECIDED (rests on an OD
                # rule) or OWNER-SPECIFIED (OS-n); an OD record that is also OS keeps both labels (A-059)
                rec["category"] = category(owner_dec, OWNER_SPEC)
                by_category[rec["category"]][status] += 1
                if OWNER_SPEC:
                    rec["owner_specified"] = OWNER_SPEC
                    owner_specified_ids[entry["fixture_id"]] = OWNER_SPEC
                    note = f"[{OWNER_SPECIFIED} {OWNER_SPEC} (D-026)] {note}".strip()
                if owner_dec:
                    rec["owner_decided"] = list(owner_dec)
                    owner_decided_ids[entry["fixture_id"]] = list(owner_dec)
                    note = f"[{OWNER_DECIDED} {', '.join(owner_dec)} (D-027)] {note}".strip()
                rec["note"] = note
            self_reported.extend(f"{entry['fixture_id']}:{name}" for name in sr)
            sim_details = PROVISIONAL.pop(id(desc), None)
            if sim_details is not None and SIM["provisional"]:  # reached L166 (7)-(11); items still open
                rec["provisional"] = {"reason": "depends on design items not yet frozen or signed: "
                                                + "; ".join(SIM["provisional"]),
                                      "simulator": sim_details}
                provisional_ids.append(entry["fixture_id"])
            if sim_details is not None and SIM["cleared"]:
                rec["cleared_under_deviation"] = SIM["cleared"]
                rec["label"] = "; ".join(c["label"] for c in SIM["cleared"])
                rec.setdefault("simulator", sim_details)
                note = f"{note} [{rec['label']}]".strip()
                deviation_ids.append(entry["fixture_id"])
            res.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
            log.write(f"{utc_stamp()} {entry['fixture_id']}: {status} {note}\n")
            log.flush()

    meta["run_finished_utc"] = utc_stamp()
    summary = {**meta, "counts": counts, "total": sum(counts.values()),
               "provisional_fixtures": provisional_ids,
               "deviation_cleared_fixtures": deviation_ids,
               "runtime_checks_self_reported": self_reported,
               "self_reported_label": SELF_REPORTED_LABEL if self_reported else None,
               "deviation_labels": sorted({c["label"] for c in SIM["cleared"]}) if SIM else [],
               "results_sha256": sha256_file(out_dir / "results.jsonl")}
    if pack_info["label"]:  # D-026, D-027: OWNER-DECIDED and OWNER-SPECIFIED results are counted apart
        summary["counts_by_category"] = by_category
        summary["owner_specified_fixtures"] = owner_specified_ids
        summary["owner_decided_fixtures"] = owner_decided_ids
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "run": f"run-{started}", "pack": pack,
                      "counts": counts}), file=sys.stderr)
    return 0 if counts["FAIL"] == 0 and counts["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
