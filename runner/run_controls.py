"""Feasibility-control runner, F1–F15 and pre-freeze F17 (Protocol §17) — H8.

Implements the evidence side of plan step 2 (docs/F1-F17-plan.md):
  - one evidence directory per run, with the same identity records as an F18 run
    (interpreter version and SHA-256, image identity, toolchain, source hashes, commit,
    host invocation; Owner Decision Record §5.3 items 1-9);
  - one record per control: status, critical-gate flag (L531), owner artifacts it needs
    and which are missing, provisional reasons, details;
  - a timestamped line per control in run.log.

Statuses:
  PASS / FAIL — the control ran and met / did not meet its expected result;
  ERROR — the control could not be adjudicated (evaluator-side failure), never hidden;
  BLOCKED_OWNER_ARTIFACTS — an owner-written file the control needs is missing
      (design/fifo/controls/slots.json; CLAUDE.md, D-007);
  NOT_WIRED — the owner files exist, but the control's procedure has not yet been
      composed from the harness components (plan step 8). Never reported as a pass.
  ARTIFACT_REJECTED — the owner files exist, but the production static or runtime stages
      reject them (README §2), so they cannot exercise the control. Never a pass; the
      stage diagnostic is recorded.

Composed procedures (D-036 item 4): F1 (L510) and F3 (L512), on the reference driver and
the F6 correct checker (D-007 (4)); F14 and F15.

Each record lists what is still provisional and which approvals it rests on. No wired
procedure (F14, F15) uses the mask; one that does must carry the DEV-001 label.

Usage (evidence, D-002a):  runner/run_f18_container.sh <run_class> controls
Usage (development only):  python3.11 -I runner/run_controls.py <baseline_root> <evidence_dir> <run_class>
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import platform
import sys
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "runner"))

import run_f18 as F18  # noqa: E402  (identity helpers and pinned-interpreter constants)
from openvef import eda, f14, f15, freeze, simulator_stages  # noqa: E402
from openvef import trace as trace_mod  # noqa: E402
from openvef.alignment import compare_repeats, null_checker_repeat  # noqa: E402
from openvef.ast_signature import check_ast_signature, check_compile  # noqa: E402
from openvef.envelope import Failure  # noqa: E402
from openvef.import_policy import check_import_policy  # noqa: E402
from openvef.runtime import checker_invocation, factory_checks  # noqa: E402
from openvef.simulation import (NEXT, OUTPUTS, SimulationError, compare_runs, driver_run,  # noqa: E402
                                l334_timeout, null_trace_xz, run_outcome)
from openvef.source_ast import check_sources, syntax_reject  # noqa: E402
from openvef.sandbox import SandboxUnavailable, broker_mode, ensure_image  # noqa: E402

MATERIALS = "design/fifo/design-materials-DRAFT.json"
CONTROLS_DIR = REPO / "design" / "fifo" / "controls"
SLOTS_FILE = CONTROLS_DIR / "slots.json"
ORDER = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15", "F17")
# Protocol L531: "F2, F4, F5, F9, F15, F16, F17 and F18 are critical gates."
CRITICAL = {"F2", "F4", "F5", "F9", "F15", "F17"}


def reading_status(item: str, pending: str) -> tuple[list, list]:
    """([provisional], [approval label]) for one Claude-decided item, from the D-009 record."""
    record = freeze.load(REPO, simulator_stages.READINGS_RECORD)
    if item in freeze.verify(REPO, record)["frozen"]:
        return [], [f"{item}: {record['label']}"]
    return [pending], []


def needs(slots: dict, control: str) -> tuple[list, list]:
    files = [s["path"] for s in slots["slots"] if control in s["feeds"]]
    return files, list(slots["controls"][control]["mutant_roles"])


def missing_artifacts(slots: dict, control: str, root: Path | None = None) -> list[str]:
    """Owner files (and mutant roles) the control still lacks."""
    root = CONTROLS_DIR if root is None else root
    files, roles = needs(slots, control)
    missing = [f for f in files if not (root / f).is_file()]
    manifest = root / "mutants" / "manifest.json"
    if roles and manifest.is_file():
        try:
            declared = {r for e in json.loads(manifest.read_text(encoding="utf-8")).get("mutants", [])
                        for r in e.get("roles", [])}
        except (ValueError, AttributeError):
            declared = set()
        missing += [f"mutant role {r} (mutants/manifest.json)" for r in roles if r not in declared]
    elif roles:
        missing += [f"mutant role {r} (mutants/manifest.json)" for r in roles]
    return missing


def run_f14() -> dict:
    rec = f14.run(REPO, MATERIALS, simulator_stages.export_null, eda.interface)
    rec.pop("provisional")
    record = freeze.load(REPO, simulator_stages.FREEZE_RECORD)
    fr = freeze.verify(REPO, record)
    rec["freeze"] = fr
    provisional, approvals = reading_status("A-052", "A-052 (port comparison) decided by Claude, approval absent or bytes changed")
    if not {"C1", "C2"} <= set(fr["frozen"]):
        provisional.insert(0, "RTL or null-netlist export script not frozen, or changed since the freeze (C1, C2)")
    return {"status": rec.pop("status"), "provisional": provisional, "approvals": approvals, "details": rec}


def run_f15(baseline: Path) -> dict:
    rec = f15.run(baseline)
    provisional, approvals = reading_status(
        "F15-case-table", "case table built by Claude (plan §2 label (a)); approval absent or bytes changed")
    return {"status": rec.pop("status"), "provisional": provisional, "approvals": approvals, "details": rec}


# --- F1 and F3 (D-036 item 4): the reference driver with the F6 correct checker (D-007 (4)) ---------------------

F1_F3_DRIVER = "drivers/reference_driver.py"
F1_F3_CHECKER = "checkers/f6_correct_checker.py"
SEED = simulator_stages.SEED  # harness-owned seed; the owners' files never choose it
_CACHE: dict = {}


def _failure_dict(f: Failure) -> dict:
    return {"stage_id": f.stage_id, "error_class": f.error_class, "diagnostic": f.diagnostic}


def load_artifact(driver_rel: str, checker_rel: str) -> tuple[dict, dict, Failure | None]:
    """(sources, file SHA-256s, SOURCE_AST failure for undecodable bytes). Owner files are only read."""
    sources, hashes, bad = {}, {}, None
    for name, rel in (("driver.py", driver_rel), ("checker.py", checker_rel)):
        data = (CONTROLS_DIR / rel).read_bytes()
        hashes[rel] = hashlib.sha256(data).hexdigest()
        try:
            sources[name] = data.decode("utf-8", errors="strict")  # a BOM is kept, so SOURCE_AST rejects it (A-008)
        except UnicodeDecodeError:
            sources[name] = ""
            bad = bad or syntax_reject(name, 1, None)  # A-009: invalid UTF-8, line 1, column 1
    return sources, hashes, bad


def artifact_stages(sources: dict) -> Failure | None:
    """The production order of run_f18.source_stages: SOURCE_AST, IMPORT_POLICY, AST_SIGNATURE, COMPILE, then the
    sandboxed factory/signature checks (File 30 §3 L27, L39). None: every stage accepted the pair."""
    trees = check_sources(list(sources.items()))
    if isinstance(trees, Failure):
        return trees
    return (check_import_policy(sources, trees) or check_ast_signature(trees) or check_compile(sources)
            or factory_checks(sources["driver.py"], seed=SEED))


def sim_context() -> dict:
    """The DRAFT design materials and the null netlist (exported twice, L233), prepared once per control run."""
    if "ctx" not in _CACHE:
        _CACHE["ctx"] = simulator_stages.prepare(REPO, MATERIALS)
    return _CACHE["ctx"]


def _prepared(driver_rel: str, checker_rel: str) -> tuple[dict, dict]:
    """(base record, sources). The base record carries the artifact hashes, any rejection, and the
    provisional/cleared labels of the DRAFT materials."""
    sources, hashes, bad = load_artifact(driver_rel, checker_rel)
    base: dict = {"artifact_sha256": hashes, "seed": SEED}
    rejected = bad or artifact_stages(sources)
    if rejected is not None:
        base["rejection"] = _failure_dict(rejected)
        return base, sources
    ctx = sim_context()
    key = hashlib.sha256(sources["driver.py"].encode("utf-8")).hexdigest()
    if key not in _CACHE:  # Protocol L334, from three null runs of this artifact
        _CACHE[key] = l334_timeout(sources["driver.py"], ctx["null"], SEED)
    base.update(l334=_CACHE[key], provisional=list(ctx["provisional"]), cleared=list(ctx["cleared"]),
                design_materials=ctx["record"]["file_sha256"])
    return base, sources


def _run(sources: dict, target: str) -> dict:
    ctx = sim_context()
    t = _CACHE[hashlib.sha256(sources["driver.py"].encode("utf-8")).hexdigest()]["t_timeout_s"]
    design = ctx["null"] if target == "null" else ctx["rtl"]
    return driver_run(sources["driver.py"], design, target, SEED, step_timeout_s=t, budget_s=t)


def _null_xz(rows: list) -> None:
    xz = null_trace_xz(rows, sim_context()["mask"])
    if xz is not None:  # L241/L277: a design-validation failure, not an artifact or control verdict
        raise SimulationError(f"X/Z on an always-observable output in the null trace at row {xz} (L241)")


def run_f1(baseline: Path) -> dict:
    """Protocol L510: "Run one artifact on null netlist three times; run its checker twice in separate processes on
    the same immutable null trace" -- expected "Traces match excluding explicitly non-deterministic metadata; both
    checker runs return identical `PASS`"."""
    base, sources = _prepared(F1_F3_DRIVER, F1_F3_CHECKER)
    if "rejection" in base:
        return {"status": "ARTIFACT_REJECTED", **base}
    runs = [_run(sources, "null") for _ in range(3)]
    for i, r in enumerate(runs):
        f = run_outcome(r)
        if f is not None:  # the artifact does not complete on the null netlist (L247): F1 cannot be met
            return {"status": "FAIL", **base, "reason": f"null run {i + 1} of 3 ended with {f.diagnostic}"}
    _null_xz(runs[0]["rows"])
    repeats = compare_repeats(runs)
    frozen = trace_mod.freeze(runs[0]["rows"])
    outcomes = []
    for _ in range(2):  # separate containers, the same immutable bytes
        o = checker_invocation(sources["checker.py"], frozen.decoded(), dict(sim_context()["metadata"]))
        if isinstance(o, Failure):  # runtime signature of check_trace (AST_SIGNATURE)
            return {"status": "ARTIFACT_REJECTED", **base, "rejection": _failure_dict(o)}
        outcomes.append(o)
    if not frozen.verify():
        raise SimulationError("serialized null trace changed during checker invocations")
    repeat = null_checker_repeat(outcomes)
    ok = repeats["traces_identical"] and repeats["records_identical"] and repeat["identical_pass"]
    return {"status": "PASS" if ok else "FAIL", **base,
            "details": {"null_runs": 3, "trace_sha256": repeats["trace_sha256"],
                        "records_identical_excluding": repeats["records_identical_excluding"],
                        "differing_fields": repeats["differing_fields"],
                        "checker_verdicts": repeat["verdicts"],
                        "checker_errors": [list(o.error) if o.error else None for o in outcomes],
                        "null_trace_rows": len(runs[0]["rows"])}}


def first_rows(rtl_rows: list, null_rows: list) -> dict:
    """The first raw-output and the first next-input divergence rows (plan §4 F3)."""
    raw = next((i for i, (a, b) in enumerate(zip(rtl_rows, null_rows)) if a[OUTPUTS] != b[OUTPUTS]), None)
    nxt = next((i for i, (a, b) in enumerate(zip(rtl_rows, null_rows)) if a[NEXT] != b[NEXT]), None)
    return {"first_raw_divergence_row": raw, "first_next_input_divergence_row": nxt}


def run_f3(baseline: Path) -> dict:
    """Protocol L512: "Run F1 artifact on RTL and null netlist" -- expected "No masked divergence and no scheduled
    next-input divergence before first raw divergence". The mask is the DRAFT primary mask, evaluated on the null
    rows (L273); its use carries the DEV-001 label (`cleared`)."""
    base, sources = _prepared(F1_F3_DRIVER, F1_F3_CHECKER)
    if "rejection" in base:
        return {"status": "ARTIFACT_REJECTED", **base}
    rows = {}
    for target in ("rtl", "null"):
        r = _run(sources, target)
        f = run_outcome(r)
        if f is not None:
            return {"status": "FAIL", **base, "reason": f"{target} run ended with {f.diagnostic}"}
        rows[target] = r["rows"]
    _null_xz(rows["null"])
    failure = compare_runs(rows["rtl"], rows["null"], mask=sim_context()["mask"])
    return {"status": "PASS" if failure is None else "FAIL", **base,
            "details": {**first_rows(rows["rtl"], rows["null"]), "rows": len(rows["null"]),
                        "comparison_failure": None if failure is None else _failure_dict(failure)}}


PROCEDURES = {"F1": run_f1, "F3": run_f3, "F14": lambda baseline: run_f14(), "F15": run_f15}


def run_control(control: str, slots: dict, baseline: Path) -> dict:
    files, roles = needs(slots, control)
    record = {"control": control, "critical_gate": control in CRITICAL, "owner_artifacts": files,
              "mutant_roles": roles}
    missing = missing_artifacts(slots, control)
    if missing:
        return {**record, "status": "BLOCKED_OWNER_ARTIFACTS", "missing": missing}
    if control not in PROCEDURES:
        return {**record, "status": "NOT_WIRED",
                "note": "owner files present; procedure not yet composed from H1-H10 (plan step 8)"}
    started = time.monotonic()
    try:
        out = PROCEDURES[control](baseline)
    except Exception as exc:  # recorded, never hidden
        return {**record, "status": "ERROR", "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc()[-2000:]}
    return {**record, **out, "wall_s": round(time.monotonic() - started, 3)}


def main() -> int:
    baseline, evidence_root, run_class = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    if broker_mode():
        started = os.environ["OPENVEF_RUN_STARTED"]
        out_dir = evidence_root
        if any(out_dir.iterdir()):
            raise F18.IntegrityError("evidence directory is not empty")
    else:
        started = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = evidence_root / f"controls-{started}"
        out_dir.mkdir(parents=True, exist_ok=False)
    try:
        sandbox = ensure_image()
    except (SandboxUnavailable, FileNotFoundError) as exc:
        sandbox = None
        print(f"sandbox unavailable: {exc}", file=sys.stderr)
    if broker_mode() and sandbox is None:
        raise SystemExit("D-002a: the runner container must have the sandbox identity")
    py_sha = F18.sha256_file(Path(os.path.realpath(sys.executable)))
    pinned = broker_mode() and sys.version == F18.PINNED_PYTHON_VERSION and py_sha == F18.PINNED_PYTHON_SHA256
    source_files = sorted([*(REPO / "src").rglob("*.py"), *(REPO / "runner").rglob("*.py"),
                           *(REPO / "sandbox").glob("*"),
                           *(p for p in (REPO / "design").rglob("*") if p.is_file())])
    meta = {
        "run_kind": "feasibility controls F1-F15, F17 (Protocol §17)",
        "run_started_utc": started, "run_class": run_class,
        "interpreter_status": ("PINNED (D-002a: runner and artifacts in the pinned image)" if pinned else
                               "NOT_PINNED: development run, not evidence (D-002a)"),
        "python_version": sys.version, "python_executable": sys.executable, "python_executable_sha256": py_sha,
        "platform": platform.platform(), "machine": platform.machine(),
        "distributions": {n: F18.installed_version(n) for n in F18.PINNED_DISTRIBUTIONS},
        "git_commit": F18.git_commit(),
        "source_sha256": {str(p.relative_to(REPO)): F18.sha256_file(p) for p in source_files},
        "slots_sha256": F18.sha256_file(SLOTS_FILE),
        "command": [sys.executable, *sys.argv], "sandbox": sandbox,
    }
    slots = json.loads(SLOTS_FILE.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    with open(out_dir / "controls.jsonl", "w", encoding="utf-8") as res, \
            open(out_dir / "run.log", "w", encoding="utf-8") as log:
        log.write(json.dumps(meta, indent=2) + "\n")
        for control in ORDER:
            rec = run_control(control, slots, baseline)
            counts[rec["status"]] = counts.get(rec["status"], 0) + 1
            res.write(json.dumps(rec, ensure_ascii=False, sort_keys=True, default=str) + "\n")
            res.flush()
            extra = rec.get("missing") or rec.get("error") or ""
            log.write(f"{F18.utc_stamp()} {control}: {rec['status']} {extra if isinstance(extra, str) else len(extra)}"
                      f"{' missing' if rec.get('missing') else ''}\n")
            log.flush()
    meta["run_finished_utc"] = F18.utc_stamp()
    summary = {**meta, "counts": counts, "controls": len(ORDER),
               "controls_sha256": F18.sha256_file(out_dir / "controls.jsonl")}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "counts": counts}), file=sys.stderr)
    return 0 if not counts.get("FAIL") and not counts.get("ERROR") and not counts.get("ARTIFACT_REJECTED") else 1


if __name__ == "__main__":
    sys.exit(main())
