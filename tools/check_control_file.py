"""Check one owner-written control file before handing it over (D-036 item 3 and its follow-up). Harness code only.

    .venv/bin/python -I tools/check_control_file.py <path> [--as driver|checker]

**Python files** (drivers and checkers): runs only File 30's static stages on the one file, in File 30 §3 L27 order, with
the production functions the F18 runner uses (src/openvef/static_file.py):
  SOURCE_AST     strict UTF-8 with BOM rejection, empty/whitespace-only rejection, `ast.parse`;
  IMPORT_POLICY  ASCII identifier scan, module-body, import, prohibited-name and module-global `random` rules
                 (File 30 L20, L29, L31, L74);
  AST_SIGNATURE  the required-symbol pass and the category pass for this file (File 30 L33, L35, L37).
The file is judged under its production name (`driver.py` or `checker.py`), chosen from its directory (`drivers/` or
`checkers/`) or by `--as`. COMPILE and the runtime stages run only in the control run. The pack requires `ast.parse` on
the pinned CPython 3.11.18; another interpreter is reported, and its verdict is advisory only.

**Verilog mutants** (`*.v`, D-036 follow-up; D-007 (2): an edit of design/fifo/rtl/ovf_fifo.v), in the pinned image:
  MODULE         it defines the top module of the design materials (`ovf_fifo`);
  DIFFERS        it is not identical to the original RTL; the size of the difference is reported;
  ICARUS_COMPILE it compiles with the pinned Icarus, `iverilog -g2012 -s ovf_fifo` (harness task `icarus`);
  PORTS          its public port list (names, directions, widths, in order) equals the original RTL's, from the same
                 Yosys interface task the mutant export uses (Protocol L233).
The control run then exports it twice with the null-netlist script and checks the netlist (src/openvef/mutants.py).

The file is only read (one `read_bytes`); this tool never writes, moves or edits it, and writes nothing else.
Exit status: 0 every check accepted; 1 a check rejected; 2 usage error, unreadable file, sandbox unavailable, or blocked
on an unsettled reading.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from openvef.source_ast import UnsettledSpec  # noqa: E402
from openvef.static_file import STAGES, static_stages  # noqa: E402

PINNED = "3.11.18"
ROLES = {"driver": "driver.py", "checker": "checker.py"}
MATERIALS = REPO / "design" / "fifo" / "design-materials-DRAFT.json"
MUTANT_CHECKS = ("MODULE", "DIFFERS", "ICARUS_COMPILE", "PORTS")


def role_of(path: Path, override: str | None) -> str:
    if override is not None:
        if override not in ROLES:
            raise ValueError(f"--as must be one of {sorted(ROLES)}")
        return ROLES[override]
    parts = set(path.resolve().parts)
    if "checkers" in parts and "drivers" not in parts:
        return "checker.py"
    if "drivers" in parts and "checkers" not in parts:
        return "driver.py"
    raise ValueError("cannot tell driver from checker by directory; pass --as driver or --as checker")


def diff_size(original: str, text: str) -> dict:
    """Lines removed from and added to the original RTL (a unified diff, without its headers)."""
    lines = list(difflib.unified_diff(original.splitlines(), text.splitlines(), lineterm="", n=0))
    body = [ln for ln in lines if not ln.startswith(("---", "+++", "@@"))]
    return {"removed": sum(ln.startswith("-") for ln in body), "added": sum(ln.startswith("+") for ln in body),
            "hunks": sum(ln.startswith("@@") for ln in lines)}


def mutant_checks(text: str, original: str, top: str, *, compile_verilog, interface) -> list[tuple[str, str | None, str]]:
    """[(check, None = accepted | reason, detail)], stopping at the first rejection. `compile_verilog(verilog, top)`
    and `interface(verilog, top)` are the harness tasks (openvef.eda.icarus_compile, openvef.eda.interface)."""
    out: list[tuple[str, str | None, str]] = []
    if not re.search(rf"\bmodule\s+{re.escape(top)}\b", text):
        return [("MODULE", f"does not define module {top} (D-007 (2): an edit of the original RTL)", "")]
    out.append(("MODULE", None, f"defines module {top}"))
    if text == original:
        return out + [("DIFFERS", "identical to the original RTL", "")]
    d = diff_size(original, text)
    out.append(("DIFFERS", None, f"{d['removed']} line(s) removed, {d['added']} added, in {d['hunks']} hunk(s)"))
    c = compile_verilog(text, top)
    if c["returncode"] != 0:
        return out + [("ICARUS_COMPILE", f"iverilog exit {c['returncode']}: {c['messages'].strip()[-1500:]}", "")]
    out.append(("ICARUS_COMPILE", None, f"{c.get('iverilog_version_line')}, -g2012"))
    mine, theirs = interface(text, top)["ports"], interface(original, top)["ports"]
    if mine != theirs:
        return out + [("PORTS", f"ports {mine} differ from the original RTL's {theirs} (Protocol L233)", "")]
    out.append(("PORTS", None, f"{len(mine)} ports, identical to the original RTL"))
    return out


def check_mutant(path: Path, data: bytes) -> int:
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        print("MODULE: REJECTED -- the file is not valid UTF-8")
        return 1
    materials = json.loads(MATERIALS.read_text(encoding="utf-8"))
    original = (REPO / materials["rtl"]).read_text(encoding="utf-8")
    top = materials["toplevel"]
    print(f"file: {path} (judged as a control mutant of {materials['rtl']})")
    from openvef import eda
    from openvef.simulation import SimulationError
    try:
        results = mutant_checks(text, original, top, compile_verilog=eda.icarus_compile, interface=eda.interface)
    except (SimulationError, OSError) as exc:
        print(f"error: the pinned image is needed for ICARUS_COMPILE and PORTS: {exc}", file=sys.stderr)
        return 2
    for check, reason, detail in results:
        if reason is None:
            print(f"{check}: accepted -- {detail}")
        else:
            print(f"{check}: REJECTED -- {reason}")
            not_run = MUTANT_CHECKS[MUTANT_CHECKS.index(check) + 1:]
            if not_run:
                print(f"not run after the rejection: {', '.join(not_run)}")
            return 1
    print("mutant checks: ACCEPTED (the control run also exports it twice and checks the netlist)")
    return 0


def check_python(path: Path, data: bytes, override: str | None) -> int:
    try:
        name = role_of(path, override)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    version = sys.version.split()[0]
    print(f"file: {path} (judged as {name}); interpreter: CPython {version}"
          + ("" if version == PINNED else f" -- not the pinned {PINNED}; verdict advisory only"))
    try:
        results = static_stages(name, data)
    except UnsettledSpec as exc:
        print(f"BLOCKED: the stage depends on an unsettled reading (docs/ambiguities.md {exc})")
        return 2
    for stage, failure in results:
        if failure is None:
            print(f"{stage}: accepted")
        else:
            print(f"{stage}: REJECTED -- {failure.error_class}: {failure.diagnostic}")
            not_run = STAGES[STAGES.index(stage) + 1:]
            if not_run:
                print(f"not run after the rejection: {', '.join(not_run)}")
            return 1
    print("static stages: ACCEPTED (COMPILE and the runtime stages run only in the control run)")
    return 0


def main(argv: list[str]) -> int:
    args = list(argv[1:])
    override = None
    if "--as" in args:
        i = args.index("--as")
        if i + 1 >= len(args):
            print("usage: check_control_file.py <path> [--as driver|checker]", file=sys.stderr)
            return 2
        override = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        print("usage: check_control_file.py <path> [--as driver|checker]", file=sys.stderr)
        return 2
    path = Path(args[0])
    try:
        data = path.read_bytes()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if path.suffix == ".v":
        if override is not None:
            print("error: --as applies to Python files only", file=sys.stderr)
            return 2
        return check_mutant(path, data)
    return check_python(path, data, override)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
