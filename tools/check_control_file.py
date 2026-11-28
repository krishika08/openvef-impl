"""Static-stage check of one owner-written control file (owner decision D-036 item 3). Harness code only.

    .venv/bin/python -I tools/check_control_file.py <path> [--as driver|checker]

Runs only File 30's static stages on the one file, in File 30 §3 L27 order, with the production functions the F18 runner
uses:
  SOURCE_AST     strict UTF-8 with BOM rejection, empty/whitespace-only rejection, `ast.parse` (src/openvef/source_ast.py);
  IMPORT_POLICY  ASCII identifier scan, module-body, import, prohibited-name and module-global `random` rules
                 (src/openvef/import_policy.py, File 30 L20, L29, L31, L74);
  AST_SIGNATURE  the required-symbol pass and the category pass for this file (src/openvef/ast_signature.py, File 30 L33,
                 L35, L37).
It prints each stage's verdict and, for the first rejection, the production diagnostic, then stops. COMPILE and the
runtime stages (restricted import, factory return type, runtime signatures) are not run here; the control run applies
every stage. The file is judged under its production name (`driver.py` or `checker.py`), chosen from its directory
(`drivers/` or `checkers/`) or by `--as`.

The file is only read (one `read_bytes`); this tool never writes, moves or edits it, and writes nothing else. The pack
requires `ast.parse` on the pinned CPython 3.11.18; another interpreter is reported, and its verdict is advisory only.
Exit status: 0 every static stage accepted; 1 a stage rejected; 2 usage error, unreadable file, or blocked on an
unsettled reading.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from openvef.ast_signature import check_ast_signature_file  # noqa: E402
from openvef.envelope import Failure  # noqa: E402
from openvef.import_policy import check_file  # noqa: E402
from openvef.source_ast import UnsettledSpec, check_source, syntax_reject  # noqa: E402

PINNED = "3.11.18"
ROLES = {"driver": "driver.py", "checker": "checker.py"}
STAGES = ("SOURCE_AST", "IMPORT_POLICY", "AST_SIGNATURE")


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


def decode(data: bytes, name: str) -> str | Failure:
    """Strict UTF-8, keeping a BOM so SOURCE_AST rejects it (A-008); undecodable bytes are invalid UTF-8 (A-009)."""
    try:
        return data.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return syntax_reject(name, 1, None)


def static_stages(name: str, data: bytes) -> list[tuple[str, Failure | None]]:
    """[(stage, None = accepted | Failure)], stopping at the first rejection."""
    source = decode(data, name)
    if isinstance(source, Failure):
        return [("SOURCE_AST", source)]
    tree = check_source(name, source)
    if isinstance(tree, Failure):
        return [("SOURCE_AST", tree)]
    out: list[tuple[str, Failure | None]] = [("SOURCE_AST", None)]
    failure = check_file(name, source, tree)
    out.append(("IMPORT_POLICY", failure))
    if failure is not None:
        return out
    out.append(("AST_SIGNATURE", check_ast_signature_file(name, tree)))
    return out


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
        name = role_of(path, override)
        data = path.read_bytes()
    except (ValueError, OSError) as exc:
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
