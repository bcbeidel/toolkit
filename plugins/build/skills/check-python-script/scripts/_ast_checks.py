#!/usr/bin/env python3
"""AST-backed deterministic checks for Python scripts.

Invoked by check_structure.sh / check_argparse.sh / check_deps.sh
to perform per-check AST analysis that POSIX awk cannot express.
Each subcommand emits findings in the fixed Tier-1 lint format and
exits per the shared contract (0 clean / 1 FAIL / 64 arg error).

Usage:
    _ast_checks.py <check> <file>

Subcommands:
    structure   shebang / main guard shape / main return type /
                KeyboardInterrupt handler / exec bit
    argparse    argparse-when-sys.argv / add_argument help= /
                subprocess check=True
    deps        non-stdlib imports without a declared-deps mechanism
"""

from __future__ import annotations

import argparse
import ast
import stat
import sys
from pathlib import Path
from typing import Iterator

EXIT_CLEAN = 0
EXIT_FAIL = 1
EXIT_USAGE = 64

# Stdlib module names available from Python 3.10 onward via sys.stdlib_module_names.
# Fall back to a baked-in set for 3.9 compatibility.
try:
    STDLIB_MODULES = set(sys.stdlib_module_names)  # type: ignore[attr-defined]
except AttributeError:
    # Minimal stdlib set sufficient for most scripting use — extend as needed.
    STDLIB_MODULES = {
        "abc",
        "argparse",
        "ast",
        "asyncio",
        "base64",
        "collections",
        "concurrent",
        "contextlib",
        "copy",
        "csv",
        "dataclasses",
        "datetime",
        "enum",
        "functools",
        "glob",
        "hashlib",
        "http",
        "importlib",
        "io",
        "itertools",
        "json",
        "logging",
        "math",
        "multiprocessing",
        "os",
        "pathlib",
        "pickle",
        "platform",
        "queue",
        "random",
        "re",
        "shutil",
        "socket",
        "sqlite3",
        "stat",
        "string",
        "subprocess",
        "sys",
        "tempfile",
        "textwrap",
        "threading",
        "time",
        "traceback",
        "typing",
        "unittest",
        "urllib",
        "uuid",
        "warnings",
        "weakref",
        "xml",
        "zipfile",
    }


def emit(severity: str, path: Path, check: str, detail: str, rec: str) -> None:
    """Write one finding in the canonical Tier-1 lint format."""
    print(f"{severity}  {path} — {check}: {detail}")
    print(f"  Recommendation: {rec}")


def parse_or_fail(path: Path) -> ast.Module | None:
    """Parse the file; emit a FAIL finding and return None on SyntaxError."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return ast.parse(fh.read(), filename=str(path))
    except SyntaxError as err:
        emit(
            "FAIL",
            path,
            "syntax",
            f"SyntaxError at line {err.lineno}: {err.msg}",
            "Fix the syntax error — the file cannot be evaluated until it parses.",
        )
        return None
    except OSError as err:
        print(f"_ast_checks.py: cannot read {path}: {err}", file=sys.stderr)
        return None


# ---- structure ------------------------------------------------------------


def check_shebang(path: Path, source: str) -> bool:
    """First line must be exactly `#!/usr/bin/env python3`."""
    first = source.splitlines()[0] if source else ""
    if first != "#!/usr/bin/env python3":
        emit(
            "FAIL",
            path,
            "shebang",
            f"first line is {first!r}, expected '#!/usr/bin/env python3'",
            "Replace the first line with '#!/usr/bin/env python3'.",
        )
        return False
    return True


def check_exec_bit(path: Path, has_shebang: bool) -> None:
    """Executable bit should be set when a shebang is present."""
    if not has_shebang:
        return
    mode = path.stat().st_mode
    if not mode & stat.S_IXUSR:
        emit(
            "INFO",
            path,
            "exec-bit",
            "shebang present but executable bit not set",
            f"Run: chmod +x {path}",
        )


def find_main_def(tree: ast.Module) -> ast.FunctionDef | None:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            return node
    return None


def find_main_guard(tree: ast.Module) -> ast.If | None:
    for node in tree.body:
        if not isinstance(node, ast.If):
            continue
        test = node.test
        # Match `__name__ == "__main__"` in either order.
        if (
            isinstance(test, ast.Compare)
            and len(test.ops) == 1
            and isinstance(test.ops[0], ast.Eq)
        ):
            left_name = isinstance(test.left, ast.Name) and test.left.id == "__name__"
            right_const = (
                isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            )
            if left_name and right_const:
                return node
    return None


def guard_invokes_sys_exit_main(guard: ast.If) -> bool:
    """Return True iff the guard body contains `sys.exit(main(...))`."""
    for stmt in guard.body:
        if not isinstance(stmt, ast.Expr):
            continue
        call = stmt.value
        if not isinstance(call, ast.Call):
            continue
        # sys.exit(...)
        if not (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "exit"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "sys"
        ):
            continue
        # argument is a call to main(...)
        if call.args and isinstance(call.args[0], ast.Call):
            inner = call.args[0].func
            if isinstance(inner, ast.Name) and inner.id == "main":
                return True
    return False


def main_returns_int(main_fn: ast.FunctionDef) -> bool:
    """Best-effort: annotated return type is `int` (as Name or Subscript)."""
    ret = main_fn.returns
    if isinstance(ret, ast.Name) and ret.id == "int":
        return True
    return False


def has_keyboard_interrupt_handler(main_fn: ast.FunctionDef) -> bool:
    """Does main() contain a top-level `except KeyboardInterrupt`?"""
    for node in ast.walk(main_fn):
        if isinstance(node, ast.ExceptHandler):
            exc = node.type
            if isinstance(exc, ast.Name) and exc.id == "KeyboardInterrupt":
                return True
            if isinstance(exc, ast.Tuple):
                for elt in exc.elts:
                    if isinstance(elt, ast.Name) and elt.id == "KeyboardInterrupt":
                        return True
    return False


def check_structure(path: Path) -> int:
    """Run all structure checks. Returns 1 if any FAIL was emitted."""
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as err:
        print(f"_ast_checks.py: cannot read {path}: {err}", file=sys.stderr)
        return EXIT_FAIL

    fail = False
    has_shebang = check_shebang(path, source)
    if not has_shebang:
        fail = True

    check_exec_bit(path, has_shebang)

    tree = parse_or_fail(path)
    if tree is None:
        return EXIT_FAIL

    main_fn = find_main_def(tree)
    guard = find_main_guard(tree)

    if guard is None:
        emit(
            "FAIL",
            path,
            "guard-missing",
            "no 'if __name__ == \"__main__\":' guard at top level",
            "Add 'if __name__ == \"__main__\": sys.exit(main())' at the module bottom.",
        )
        fail = True
    elif not guard_invokes_sys_exit_main(guard):
        emit(
            "FAIL",
            path,
            "guard-shape",
            "__main__ guard does not invoke sys.exit(main())",
            "Change the guard body to 'sys.exit(main())'.",
        )
        fail = True

    if main_fn is not None:
        if not main_returns_int(main_fn):
            emit(
                "WARN",
                path,
                "main-returns",
                "main() signature does not declare '-> int' return type",
                "Annotate main() as '-> int' and ensure every path returns an int.",
            )
        if not has_keyboard_interrupt_handler(main_fn):
            emit(
                "WARN",
                path,
                "keyboard-interrupt",
                "main() has no 'except KeyboardInterrupt' handler",
                "Wrap main()'s body in try/except KeyboardInterrupt: return 130.",
            )

    return EXIT_FAIL if fail else EXIT_CLEAN


# ---- argparse -------------------------------------------------------------


def walks_sys_argv_past_zero(tree: ast.Module) -> bool:
    """Detect any sys.argv[N] where N != 0, or any slice of sys.argv."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Subscript):
            continue
        value = node.value
        if not (
            isinstance(value, ast.Attribute)
            and value.attr == "argv"
            and isinstance(value.value, ast.Name)
            and value.value.id == "sys"
        ):
            continue
        slice_node = node.slice
        # sys.argv[N] with N != 0
        if isinstance(slice_node, ast.Constant):
            if slice_node.value != 0:
                return True
        else:
            # sys.argv[1:], sys.argv[i], len(sys.argv), etc.
            return True
    return False


def imports_argparse(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "argparse":
                    return True
        elif isinstance(node, ast.ImportFrom) and node.module == "argparse":
            return True
    return False


def walk_add_argument_calls(tree: ast.Module) -> Iterator[ast.Call]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "add_argument":
            yield node


def walk_subprocess_run_calls(tree: ast.Module) -> Iterator[ast.Call]:
    """Yield calls that match subprocess.run / .call / .check_output / Popen."""
    targets = {"run", "call", "check_output", "Popen", "check_call"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (
            isinstance(func, ast.Attribute)
            and func.attr in targets
            and isinstance(func.value, ast.Name)
            and func.value.id == "subprocess"
        ):
            yield node


def kwarg_value(call: ast.Call, name: str) -> ast.expr | None:
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def result_is_assigned(call: ast.Call, tree: ast.Module) -> bool:
    """Is this subprocess.run(...) call's return value bound to a name?

    We approximate: walk the tree and find the Assign/AnnAssign whose value
    is this Call node. ast doesn't give us parent links; do a targeted walk.
    """
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr))
            and node.value is call
        ):
            return True
    return False


def check_argparse(path: Path) -> int:
    tree = parse_or_fail(path)
    if tree is None:
        return EXIT_FAIL

    # argparse-when-sys.argv
    if walks_sys_argv_past_zero(tree) and not imports_argparse(tree):
        emit(
            "WARN",
            path,
            "argparse-when-argv",
            "sys.argv indexed past [0] but argparse is not imported",
            "Replace manual sys.argv parsing with argparse.",
        )

    # add-argument help=
    for call in walk_add_argument_calls(tree):
        help_val = kwarg_value(call, "help")
        empty = help_val is None or (
            isinstance(help_val, ast.Constant) and help_val.value in ("", None)
        )
        if empty:
            emit(
                "WARN",
                path,
                "add-argument-help",
                f"add_argument() at line {call.lineno} missing non-empty help=",
                "Add a help='...' string; it is what the user sees on --help.",
            )

    # subprocess check=True or result inspected
    for call in walk_subprocess_run_calls(tree):
        if isinstance(call.func, ast.Attribute) and call.func.attr in {
            "Popen",
            "check_output",
            "check_call",
        }:
            # Popen constructs; check_output/check_call already raise.
            continue
        check_kw = kwarg_value(call, "check")
        is_check_true = isinstance(check_kw, ast.Constant) and check_kw.value is True
        if not is_check_true and not result_is_assigned(call, tree):
            emit(
                "WARN",
                path,
                "subprocess-check",
                (
                    f"subprocess.{call.func.attr}() at line {call.lineno} "
                    "neither sets check=True nor inspects the return"
                ),
                "Add check=True, or assign the result and inspect returncode.",
            )

    return EXIT_CLEAN


# ---- deps -----------------------------------------------------------------


def top_level_imports(tree: ast.Module) -> set[str]:
    """Return the set of top-level module names imported (first dotted part)."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            # node.module is None for `from . import foo` (relative)
            if node.level == 0 and node.module:
                names.add(node.module.split(".")[0])
    return names


def has_pep723_block(source: str) -> bool:
    """Look for the `# /// script` PEP 723 block anywhere in the first 50 lines."""
    for line in source.splitlines()[:50]:
        if line.strip() == "# /// script":
            return True
    return False


def has_top_of_file_deps_comment(source: str) -> bool:
    """Heuristic — a top-of-file comment block mentioning 'dependencies'/'requires'."""
    header_lines = []
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if (
            stripped.startswith("#")
            or stripped.startswith('"""')
            or stripped.startswith("'''")
        ):
            header_lines.append(stripped.lower())
            if len(header_lines) >= 30:
                break
        else:
            break
    joined = " ".join(header_lines)
    return (
        "requires" in joined or "dependencies" in joined or "requirements" in joined
    ) and (
        "pip" in joined
        or "install" in joined
        or "requires-python" in joined
        or "==" in joined
    )


def colocated_requirements_txt(path: Path) -> bool:
    return (path.parent / "requirements.txt").is_file()


def check_deps(path: Path) -> int:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as err:
        print(f"_ast_checks.py: cannot read {path}: {err}", file=sys.stderr)
        return EXIT_FAIL

    tree = parse_or_fail(path)
    if tree is None:
        return EXIT_FAIL

    imports = top_level_imports(tree)
    non_stdlib = {
        n for n in imports if n not in STDLIB_MODULES and not n.startswith("_")
    }
    if not non_stdlib:
        return EXIT_CLEAN

    if has_pep723_block(source):
        return EXIT_CLEAN
    if colocated_requirements_txt(path):
        return EXIT_CLEAN
    if has_top_of_file_deps_comment(source):
        return EXIT_CLEAN

    emit(
        "WARN",
        path,
        "declared-deps",
        (
            "non-stdlib imports with no declared-deps mechanism: "
            f"{', '.join(sorted(non_stdlib))}"
        ),
        (
            "Add a PEP 723 '# /// script' block, a colocated "
            "requirements.txt, or a top-of-file deps comment."
        ),
    )
    return EXIT_CLEAN


# ---- dispatch -------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AST-backed deterministic checks for Python scripts.",
    )
    parser.add_argument(
        "check",
        choices=("structure", "argparse", "deps"),
        help="Which check family to run.",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to a single .py file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.file.is_file():
        print(f"_ast_checks.py: not a file: {args.file}", file=sys.stderr)
        return EXIT_USAGE

    try:
        if args.check == "structure":
            return check_structure(args.file)
        if args.check == "argparse":
            return check_argparse(args.file)
        if args.check == "deps":
            return check_deps(args.file)
    except KeyboardInterrupt:
        return 130

    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
