"""In-container harness: factory and signature checks, checker calls, EDA tasks.

Runs inside the D-002 sandbox only (`python -I /opt/openvef/harness.py`), standard
library only. Reads one JSON request on stdin and writes one result line
`OPENVEF_SANDBOX_RESULT <json>`. **No artifact code runs in this interpreter** (D-015, audit
A9-1): driver.py and checker.py run in artifact_worker.py, a confined process reached only
through artifact_proc.py.

Implements:
  File 30 §3 L27 — "compilation; restricted-runtime import; runtime `inspect.signature`
                   and factory-return checks".
  File 30 §3 L35/L37 — `create_driver(seed)` must return an instance of the module's
                   `Driver` class; runtime `inspect.signature` must confirm the same
                   parameter names/kinds/counts for create_driver, Driver.step and
                   check_trace.
  Protocol §3.4 L166 (7) — "Factory return type and runtime signatures are checked
                   immediately after factory construction."
  Protocol stage map — RUNTIME_EXCEPTION|file=driver.py|phase=factory|class=<C>;
                   ENTRY_POINT_REJECT|...|reason=RETURN_TYPE / RUNTIME_SIGNATURE;
                   CHECKER_RUNTIME_ERROR|class=<C>; File 30 L97 return classification.

Readings decided by Claude under the standing delegation (docs/ambiguities.md; approved
under D-009): A-034 an exception while importing a module; A-035 order of the
post-construction checks and when check_trace's signature is checked.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # `-I` leaves it off
from artifact_proc import ArtifactFailed, ArtifactHostError, ArtifactProcess, inspect_source, runtime_signature_ok  # noqa: E402

RESULT_MARKER = "OPENVEF_SANDBOX_RESULT "


def emit(result: dict) -> None:
    sys.stdout.write(RESULT_MARKER + json.dumps(result, sort_keys=True) + "\n")
    sys.stdout.flush()


def failure(stage: str, error_class: str, diagnostic: str, disposition: str = "REPAIR") -> dict:
    return {"failure": {"stage_id": stage, "error_class": error_class, "diagnostic": diagnostic,
                        "disposition": disposition}}


def entry_reject(file: str, symbol: str, reason: str) -> dict:
    return failure("AST_SIGNATURE", "ENTRY_POINT_REJECT", f"ENTRY_POINT_REJECT|file={file}|symbol={symbol}|reason={reason}")


def construct(artifact: ArtifactProcess, driver_source: str, seed: int):
    """Import driver.py and call create_driver(seed) once in the artifact process, then the
    return-type and signature checks here. Returns a failure record or None.

    D-019: the signatures that must be right are those of `trusted`, measured where no artifact
    code has run. The artifact process's own report (code objects, and the literal
    inspect.signature of File 30 L35/L37, D-022) must agree, so it can reject but never accept. The return type is known only from that report (docs/sandbox.md
    "Runtime checks"); openvef.runtime_basis says which artifacts cannot have forged it."""
    trusted = inspect_source("driver", driver_source)
    try:
        type_ok, create, step = artifact.construct(driver_source, seed)
    except ArtifactFailed as exc:  # A-034: import is the first execution of driver code
        return failure("DRIVER_RUNTIME", "RUNTIME_EXCEPTION",
                       f"RUNTIME_EXCEPTION|file=driver.py|phase=factory|class={exc.exception_class}")
    # A-035: return type, then create_driver's signature, then Driver.step's.
    if not type_ok:
        return entry_reject("driver.py", "create_driver", "RETURN_TYPE")
    if not runtime_signature_ok(trusted.get("create_driver"), *create, "create_driver"):
        return entry_reject("driver.py", "create_driver", "RUNTIME_SIGNATURE")
    if not runtime_signature_ok(trusted.get("Driver.step"), *step, "Driver.step"):
        return entry_reject("driver.py", "Driver.step", "RUNTIME_SIGNATURE")
    return None


def task_factory(request: dict) -> dict:
    """Import driver.py, construct the driver, then return-type and signature checks."""
    with ArtifactProcess() as artifact:
        return construct(artifact, request["driver_source"], request["seed"]) or {"failure": None}


def classify_return(value) -> dict:
    """File 30 L97 exact order; malformed items counted, not errors."""
    def invalid(reason):
        return {"error": ["CHECKER_RETURN_INVALID", f"CHECKER_RETURN_INVALID|reason={reason}"]}
    if not isinstance(value, dict):
        return invalid("NON_DICTIONARY")
    if "diagnostics" not in value:
        return invalid("MISSING_DIAGNOSTICS")
    if set(value) != {"verdict", "diagnostics"}:
        return invalid("TOP_LEVEL_KEYS")
    if not (isinstance(value["verdict"], str) and value["verdict"] in ("PASS", "FAIL")):
        return invalid("INVALID_VERDICT")
    if not isinstance(value["diagnostics"], list):
        return invalid("DIAGNOSTICS_NOT_LIST")

    def item_ok(item):
        return (isinstance(item, dict) and set(item) == {"code", "message", "cycle", "clause_id"}
                and isinstance(item["code"], str) and isinstance(item["message"], str)
                and (item["cycle"] is None or type(item["cycle"]) is int)
                and (item["clause_id"] is None or isinstance(item["clause_id"], str)))
    return {"verdict": value["verdict"], "malformed_items": sum(not item_ok(i) for i in value["diagnostics"])}


def task_checker(request: dict) -> dict:
    """One checker null invocation on an immutable trace (its own container and process)."""
    trusted = inspect_source("checker", request["checker_source"])
    with ArtifactProcess() as artifact:
        try:
            report = artifact.load_checker(request["checker_source"])
            # A-035: check_trace's runtime signature is checked before the first call.
            if not runtime_signature_ok(trusted.get("check_trace"), *report, "check_trace"):
                return entry_reject("checker.py", "check_trace", "RUNTIME_SIGNATURE")
            value = artifact.check(request["trace"], request["metadata"])
        except ArtifactFailed as exc:  # A-034
            return {"error": ["CHECKER_RUNTIME_ERROR", f"CHECKER_RUNTIME_ERROR|class={exc.exception_class}"]}
    return classify_return(value)


def task_simulate(request: dict) -> dict:
    """One driver run on one target (rtl or null) through Icarus + cocotb (sim.py)."""
    import sim
    return sim.run(request)


def task_export(request: dict) -> dict:
    """Null-netlist export (Protocol L233) with the design pack's Yosys script.

    The script reads /tmp/in.v and writes /tmp/net.v (design/fifo/export_null.ys). Evaluator
    material only: no artifact code is involved. Returns the netlist text and its SHA-256."""
    import hashlib
    import subprocess
    with open("/tmp/in.v", "w", encoding="utf-8") as f:
        f.write(request["verilog"])
    with open("/tmp/export.ys", "w", encoding="utf-8") as f:
        f.write(request["script"])
    p = subprocess.run(["yosys", "-q", "-s", "/tmp/export.ys"], capture_output=True, text=True)
    if p.returncode != 0:
        return {"error": f"yosys exit {p.returncode}: {(p.stderr or p.stdout)[-800:]}"}
    data = open("/tmp/net.v", "rb").read()
    version = subprocess.run(["yosys", "-V"], capture_output=True, text=True).stdout.strip()
    return {"netlist": data.decode("utf-8"), "sha256": hashlib.sha256(data).hexdigest(), "yosys_version": version}


def task_interface(request: dict) -> dict:
    """Top module and public ports of a Verilog text, from Yosys `write_json` (F14; H1).

    Evaluator material only. Returns {"modules", "top", "ports": [[name, direction, width],
    ...] in declaration order}."""
    import subprocess
    with open("/tmp/iface.v", "w", encoding="utf-8") as f:
        f.write(request["verilog"])
    top = request["top"]
    script = f"read_verilog -sv /tmp/iface.v\nhierarchy -check -top {top}\nproc\nwrite_json /tmp/iface.json\n"
    p = subprocess.run(["yosys", "-q", "-p", script], capture_output=True, text=True)
    if p.returncode != 0:
        return {"error": f"yosys exit {p.returncode}: {(p.stderr or p.stdout)[-800:]}"}
    data = json.load(open("/tmp/iface.json", encoding="utf-8"))
    mod = data["modules"][top]
    ports = [[name, spec["direction"], len(spec["bits"])] for name, spec in mod["ports"].items()]
    return {"modules": sorted(data["modules"]), "top": top, "ports": ports}


def task_yosys(request: dict) -> dict:
    """Run evaluator-built Yosys scripts on evaluator-supplied files (H5 bounded check).

    `files` maps plain names to text, written under /tmp/y; each of `scripts` runs as one
    `yosys -s` invocation with its own wall-clock limit. Returns each log and exit code.
    No artifact code is involved."""
    import subprocess
    os.makedirs("/tmp/y", exist_ok=True)
    for name, text in request["files"].items():
        if "/" in name or name.startswith("."):
            return {"error": "file names must be plain"}
        with open(f"/tmp/y/{name}", "w", encoding="utf-8") as f:
            f.write(text)
    runs = []
    for i, script in enumerate(request["scripts"]):
        path = f"/tmp/y/script{i}.ys"
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)
        try:
            p = subprocess.run(["yosys", "-q", "-l", f"/tmp/y/log{i}.txt", "-s", path], capture_output=True,
                               text=True, timeout=float(request["timeout_s"]), cwd="/tmp/y")
            log = open(f"/tmp/y/log{i}.txt", encoding="utf-8", errors="replace").read()
            runs.append({"returncode": p.returncode, "log": log[-int(request.get("log_tail", 200000)):],
                         "stderr": (p.stderr or "")[-800:]})
        except subprocess.TimeoutExpired:
            runs.append({"returncode": None, "timed_out": True, "log": ""})
            break
    version = subprocess.run(["yosys", "-V"], capture_output=True, text=True).stdout.strip()
    return {"runs": runs, "yosys_version": version}


def task_icarus(request: dict) -> dict:
    """Compile one Verilog text with the pinned Icarus (`iverilog -g2012 -s <top>`) and report the result (D-036 follow-up; the
    mutant check of tools/check_control_file.py). Evaluator material only: no artifact code is involved, and the
    compiled program is not run. Returns the exit code, the compiler's messages and the Icarus version line."""
    import subprocess
    os.makedirs("/tmp/ic", exist_ok=True)
    with open("/tmp/ic/in.v", "w", encoding="utf-8") as f:
        f.write(request["verilog"])
    p = subprocess.run(["iverilog", "-g2012", "-s", request["top"], "-o", "/tmp/ic/out.vvp", "/tmp/ic/in.v"],
                       capture_output=True, text=True)
    version = subprocess.run(["iverilog", "-V"], capture_output=True, text=True).stdout.splitlines()
    return {"returncode": p.returncode, "messages": ((p.stderr or "") + (p.stdout or ""))[-4000:],
            "iverilog_version_line": version[0] if version else None}


TASKS = {"factory": task_factory, "checker": task_checker, "simulate": task_simulate, "export": task_export,
         "interface": task_interface, "yosys": task_yosys, "icarus": task_icarus}


def main() -> None:
    request = json.loads(sys.stdin.read())
    try:
        result = TASKS[request["task"]](request)
    except ArtifactHostError as exc:
        sys.exit(f"artifact host error: {exc}")  # no result line: an evaluator-side error
    emit(result)


if __name__ == "__main__":
    main()
