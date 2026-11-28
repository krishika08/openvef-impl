"""Static stages for one artifact file alone (D-036 item 3; used by tools/check_control_file.py and the control runner).

File 30 §3 L27 order, with the production stage functions:
  SOURCE_AST     strict UTF-8 with BOM rejection, empty/whitespace-only rejection, `ast.parse` (source_ast);
  IMPORT_POLICY  ASCII identifier scan, module-body, import, prohibited-name and module-global `random` rules
                 (import_policy; File 30 L20, L29, L31, L74);
  AST_SIGNATURE  the file's required-symbol pass and category pass (ast_signature; File 30 L33, L35, L37);
  COMPILE        `compile()` of the file (COMPILE_DRIVER / COMPILE_CHECKER), only when asked.

Where a pair's first failure lies in this file, these stages give that same failure (tests/test_check_control_file.py).
Nothing here imports or runs the file.
"""
from __future__ import annotations

from openvef.ast_signature import COMPILE_STAGES, check_ast_signature_file, check_compile_file
from openvef.envelope import Failure
from openvef.import_policy import check_file
from openvef.source_ast import check_source, syntax_reject

STAGES = ("SOURCE_AST", "IMPORT_POLICY", "AST_SIGNATURE")


def decode(data: bytes, name: str) -> str | Failure:
    """Strict UTF-8, keeping a BOM so SOURCE_AST rejects it (A-008); undecodable bytes are invalid UTF-8 (A-009)."""
    try:
        return data.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return syntax_reject(name, 1, None)


def static_stages(name: str, data: bytes, *, compile_stage: bool = False) -> list[tuple[str, Failure | None]]:
    """[(stage, None = accepted | Failure)], stopping at the first rejection. `name` is driver.py or checker.py."""
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
    failure = check_ast_signature_file(name, tree)
    out.append(("AST_SIGNATURE", failure))
    if failure is None and compile_stage:
        out.append((COMPILE_STAGES[name], check_compile_file(name, source)))
    return out


def first_failure(name: str, data: bytes, *, compile_stage: bool = False) -> Failure | None:
    return next((f for _, f in static_stages(name, data, compile_stage=compile_stage) if f is not None), None)
