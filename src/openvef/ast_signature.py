"""Stage AST_SIGNATURE (static part) and stages COMPILE_DRIVER / COMPILE_CHECKER.

Implements:
  Protocol §3.4 "Deterministic `ENTRY_POINT_REJECT` assignment and symbol naming"
                   (file 02 L164); File 30 §3 L33 — the required-symbol pass in the fixed
                   sequence driver.py:create_driver, driver.py:Driver,
                   driver.py:Driver.step, checker.py:check_trace; then one global pass
                   over both files with category ranks 1-7, selected by
                   (category, file_order, lineno, col_offset, end_lineno, end_col_offset).
  File 30 §3 L35 (driver file), L37 (checker file) — required parameter lists.
  Protocol §3.4 L135 — async definitions, async comprehensions, ENCLOSING_SYMBOL.
  Protocol §3.4 stage map rows "Driver compile error" / "Checker compile error" and
                   evaluation order (5), (6) — `compile()` of driver.py, then checker.py.

The runtime part of AST_SIGNATURE (`inspect.signature` and the factory return type)
runs after import in the restricted execution container and is not implemented here.

Readings decided by Claude under the standing delegation (docs/ambiguities.md; approved
under D-009): A-020 parameter checks; A-021 what counts as a binding; A-022 Driver
class-body statements; A-023 positions of definition violations; A-024 compile errors
without a line number.
"""
from __future__ import annotations

import ast
from typing import Iterator, NamedTuple, Optional

from openvef.envelope import Failure
from openvef.import_policy import is_literal_only

STAGE = "AST_SIGNATURE"
ERROR_CLASS = "ENTRY_POINT_REJECT"
FILE_ORDER = ("driver.py", "checker.py")

# File 30 §3 L35/L37: exact required positional-or-keyword parameters.
CREATE_DRIVER_PARAMS = ("seed",)
STEP_PARAMS = ("self", "cycle_index", "outputs_after_edge")
CHECK_TRACE_PARAMS = ("trace", "metadata")

# Global category ranks (Protocol §3.4 file 02 L164).
NESTED_CLASS_FORBIDDEN, CLASS_FORBIDDEN, FORBIDDEN_METHOD, DRIVER_CLASS_FORM = 1, 2, 3, 4
DECORATOR, ASYNC_DEFINITION, ASYNC_COMPREHENSION = 5, 6, 7

_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
_COMPREHENSIONS = (ast.GeneratorExp, ast.ListComp, ast.SetComp, ast.DictComp)


def _entry_reject(file: str, symbol: str, reason: str) -> Failure:
    return Failure(STAGE, ERROR_CLASS, f"ENTRY_POINT_REJECT|file={file}|symbol={symbol}|reason={reason}")


def _decorator_reject(file: str, symbol: str) -> Failure:
    # "`DECORATOR_REJECT` has error class `ENTRY_POINT_REJECT`; its diagnostic code
    # remains `DECORATOR_REJECT`." (Protocol §3.4 file 02 L139.)
    return Failure(STAGE, ERROR_CLASS, f"DECORATOR_REJECT|file={file}|symbol={symbol}")


# --- Required-symbol pass ---------------------------------------------------------------

def _bound_names(target: ast.expr) -> Iterator[str]:
    if isinstance(target, ast.Name):
        yield target.id
    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            yield from _bound_names(element)
    elif isinstance(target, ast.Starred):
        yield from _bound_names(target.value)


def bindings(body: list[ast.stmt], name: str) -> list[ast.stmt]:
    """Statements in one scope's own body that bind `name` (A-021).

    A-021 (decided by Claude, approved under D-009): a binding is a def, async def or
    class of that name, an assignment or annotated assignment with a value whose
    target binds that name, or an import whose bound name is that name. An annotated
    name without a value (`x: int`) binds nothing in Python and is not counted. Only
    the scope's own statements count ("at the required scope").
    """
    found = []
    for stmt in body:
        if isinstance(stmt, _DEFS):
            names = [stmt.name]
        elif isinstance(stmt, ast.Assign):
            names = [n for t in stmt.targets for n in _bound_names(t)]
        elif isinstance(stmt, ast.AnnAssign):
            names = list(_bound_names(stmt.target)) if stmt.value is not None else []
        elif isinstance(stmt, (ast.Import, ast.ImportFrom)):
            names = [a.asname or a.name.split(".", 1)[0] for a in stmt.names]
        else:
            names = []
        if name in names:
            found.append(stmt)
    return found


def check_parameters(file: str, symbol: str, node: ast.FunctionDef, expected: tuple[str, ...]) -> Optional[Failure]:
    """PARAMETER_NAMES, then PARAMETER_KIND, then DEFAULT_OR_VARIADIC (A-020).

    File 30 §3 L33: "parameter checks in the order names, kinds, then
    defaults/variadic/keyword-only shape". A-020 (decided by Claude, approved under
    D-009): the names check compares the positional parameter names (positional-only
    then positional-or-keyword, in order) with the required list; the kind check
    rejects any positional-only parameter; the last check rejects any default, `*args`,
    keyword-only parameter or `**kwargs`. Annotations are ignored (File 30 §3 L35).
    """
    a = node.args
    positional = [p.arg for p in a.posonlyargs + a.args]
    if tuple(positional) != expected:
        return _entry_reject(file, symbol, "PARAMETER_NAMES")
    if a.posonlyargs:
        return _entry_reject(file, symbol, "PARAMETER_KIND")
    if a.defaults or a.vararg or a.kwonlyargs or a.kw_defaults or a.kwarg:
        return _entry_reject(file, symbol, "DEFAULT_OR_VARIADIC")
    return None


def _required_function(file: str, symbol: str, body: list[ast.stmt], name: str,
                       expected: tuple[str, ...]) -> Optional[Failure]:
    found = bindings(body, name)
    if not found:
        return _entry_reject(file, symbol, "MISSING_ENTRY_POINT")
    if len(found) > 1:
        return _entry_reject(file, symbol, "EXTRA_ENTRY_POINT")
    if not isinstance(found[0], ast.FunctionDef):  # includes AsyncFunctionDef
        return _entry_reject(file, symbol, "WRONG_ENTRY_POINT_KIND")
    return check_parameters(file, symbol, found[0], expected)


def required_symbols_in(file: str, tree: ast.Module) -> Optional[Failure]:
    """The required-symbol pass for one file, in the fixed sequence (Protocol §3.4 file 02 L164):
    driver.py: create_driver, Driver, Driver.step; checker.py: check_trace."""
    body = tree.body
    if file == "checker.py":
        return _required_function("checker.py", "check_trace", body, "check_trace", CHECK_TRACE_PARAMS)
    if file != "driver.py":
        raise ValueError(f"unknown artifact file {file!r}")
    failure = _required_function("driver.py", "create_driver", body, "create_driver", CREATE_DRIVER_PARAMS)
    if failure:
        return failure
    found = bindings(body, "Driver")
    if not found:
        return _entry_reject("driver.py", "Driver", "MISSING_ENTRY_POINT")
    if len(found) > 1:
        return _entry_reject("driver.py", "Driver", "EXTRA_ENTRY_POINT")
    if not isinstance(found[0], ast.ClassDef):
        return _entry_reject("driver.py", "Driver", "DRIVER_CLASS_FORM")
    return _required_function("driver.py", "Driver.step", found[0].body, "step", STEP_PARAMS)


def required_symbols(trees: dict[str, ast.Module]) -> Optional[Failure]:
    """The fixed-sequence required-symbol pass (Protocol §3.4 file 02 L164): driver.py, then checker.py."""
    for file in FILE_ORDER:
        failure = required_symbols_in(file, trees[file])
        if failure:
            return failure
    return None


# --- Global remaining-structure pass ----------------------------------------------------

class Violation(NamedTuple):
    sort_key: tuple[int, int, int, int, int, int]
    failure: Failure


def _key(category: int, file: str, node: ast.AST) -> tuple[int, int, int, int, int, int]:
    return (category, FILE_ORDER.index(file), node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)


def _is_async_comprehension(node: ast.AST) -> bool:
    return isinstance(node, _COMPREHENSIONS) and (
        any(g.is_async for g in node.generators) or any(isinstance(n, ast.Await) for n in ast.walk(node)))


def _driver_body_violations(file: str, cls: ast.ClassDef, add) -> None:
    """Driver class-body statements other than methods and nested classes (A-022).

    File 30 §3 L35: "Its body may contain one docstring, literal-only class constants
    and exactly one synchronous undecorated instance method named `step`". A-022
    (decided by Claude, approved under D-009): any other class-body statement is
    `DRIVER_CLASS_FORM` at rank 4, positioned at the statement. Class constants follow
    the module-constant rules: plain-name targets and literal-only values.
    """
    for index, stmt in enumerate(cls.body):
        if isinstance(stmt, _DEFS):
            continue  # methods: rank 3 / required pass; nested classes: rank 1
        if isinstance(stmt, ast.Expr) and index == 0 and isinstance(stmt.value, ast.Constant) \
                and type(stmt.value.value) is str:
            continue  # the class docstring
        if isinstance(stmt, ast.Assign):
            ok = all(isinstance(t, ast.Name) for t in stmt.targets) and is_literal_only(stmt.value)
        elif isinstance(stmt, ast.AnnAssign):
            ok = isinstance(stmt.target, ast.Name) and (stmt.value is None or is_literal_only(stmt.value))
        else:
            ok = False
        if not ok:
            add(DRIVER_CLASS_FORM, stmt, _entry_reject(file, "Driver", "DRIVER_CLASS_FORM"))


def structure_violations(file: str, tree: ast.Module) -> list[Violation]:
    """Every rank 1-7 violation in one file, with its global sort key."""
    found: list[Violation] = []

    def add(category: int, node: ast.AST, failure: Failure) -> None:
        found.append(Violation(_key(category, file, node), failure))

    def visit(node: ast.AST, enclosing: tuple[str, ...], parent_class_is_driver: bool) -> None:
        for child in ast.iter_child_nodes(node):
            if _is_async_comprehension(child):
                # Rank 7: symbol is the enclosing definitions only; at least one exists,
                # because module-body expressions were rejected at IMPORT_POLICY.
                add(ASYNC_COMPREHENSION, child, _entry_reject(file, ".".join(enclosing), "ASYNC_COMPREHENSION"))
            if isinstance(child, _DEFS):
                symbol = ".".join(enclosing + (child.name,))
                top_level = not enclosing
                if isinstance(child, ast.ClassDef):
                    is_driver = file == "driver.py" and top_level and child.name == "Driver"
                    if not top_level:
                        add(NESTED_CLASS_FORBIDDEN, child, _entry_reject(file, symbol, "NESTED_CLASS_FORBIDDEN"))
                    elif not is_driver:
                        add(CLASS_FORBIDDEN, child, _entry_reject(file, symbol, "CLASS_FORBIDDEN"))
                    else:
                        explicit_object = [b for b in child.bases if not (isinstance(b, ast.Name) and b.id == "object")]
                        if child.keywords or explicit_object or len(child.bases) > 1:
                            add(DRIVER_CLASS_FORM, child, _entry_reject(file, symbol, "DRIVER_CLASS_FORM"))
                        _driver_body_violations(file, child, add)
                else:
                    if parent_class_is_driver and child.name != "step":
                        add(FORBIDDEN_METHOD, child, _entry_reject(file, symbol, "FORBIDDEN_METHOD"))
                    if isinstance(child, ast.AsyncFunctionDef):
                        add(ASYNC_DEFINITION, child, _entry_reject(file, symbol, "ASYNC_DEFINITION"))
                if child.decorator_list:
                    add(DECORATOR, child, _decorator_reject(file, symbol))
                is_driver_class = (isinstance(child, ast.ClassDef) and file == "driver.py"
                                   and top_level and child.name == "Driver")
                visit(child, enclosing + (child.name,), is_driver_class)
            else:
                visit(child, enclosing, False)

    visit(tree, (), False)
    return found


def check_ast_signature(trees: dict[str, ast.Module]) -> Optional[Failure]:
    """Static AST_SIGNATURE: required-symbol pass, then the global category pass."""
    failure = required_symbols(trees)
    if failure:
        return failure
    violations = [v for file in FILE_ORDER for v in structure_violations(file, trees[file])]
    if not violations:
        return None
    return min(violations, key=lambda v: v.sort_key).failure


def check_ast_signature_file(file: str, tree: ast.Module) -> Optional[Failure]:
    """Static AST_SIGNATURE for one file alone (D-036 item 3, tools/check_control_file.py): its
    required-symbol pass, then its own category pass. When the pair's first AST_SIGNATURE
    failure lies in this file, this returns that same failure: the global minimum over both
    files, when it is in this file, is also the minimum over this file."""
    failure = required_symbols_in(file, tree)
    if failure:
        return failure
    violations = structure_violations(file, tree)
    return min(violations, key=lambda v: v.sort_key).failure if violations else None


# --- COMPILE_DRIVER / COMPILE_CHECKER (Protocol §3.4 evaluation order (5), (6)) ---------

COMPILE_STAGES = {"driver.py": "COMPILE_DRIVER", "checker.py": "COMPILE_CHECKER"}


def check_compile(sources: dict[str, str]) -> Optional[Failure]:
    """`compile()` driver.py, then checker.py; the first SyntaxError wins.

    A-024 (decided by Claude, approved under D-009): a compile error without a positive
    line number uses line=1 (the A-011 fallback); any other exception from `compile()`
    is also a compile error at line 1.
    """
    for file in FILE_ORDER:
        try:
            compile(sources[file], file, "exec", dont_inherit=True)
        except SyntaxError as exc:
            line = exc.lineno if isinstance(exc.lineno, int) and exc.lineno >= 1 else 1
        except Exception:
            line = 1
        else:
            continue
        return Failure(COMPILE_STAGES[file], "COMPILE_ERROR", f"COMPILE_ERROR|file={file}|line={line}")
    return None
