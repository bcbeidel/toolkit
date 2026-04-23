---
name: Audit Dimensions — Python Scripts
description: The complete check inventory for check-python-script — Tier-1 deterministic check table (22 checks grouped across 6 scripts) and Tier-2 judgment dimension specifications (9 dimensions, each citing its source principle). Referenced by the check-python-script workflow.
---

# Audit Dimensions

The check-python-script audit runs in three tiers. This document is
the inventory: every deterministic check Tier-1 emits, every
judgment dimension Tier-2 evaluates. Every dimension cites the source
principle it audits from
[python-script-best-practices.md](../../../_shared/references/python-script-best-practices.md).

## Tier-1 — Deterministic Checks

Six scripts, 22 checks. Each script emits findings in the fixed lint
format (`SEVERITY  <path> — <check>: <detail>` + `Recommendation:`).
Exit codes: `0` clean / WARN / INFO / HINT-only; `1` on FAIL; `64`
arg error; `69` missing dependency.

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_secrets.sh` | `secret` | API keys, tokens, private URLs via regex pattern list | FAIL | Safety — "No secrets" (toolkit convention) |
| `check_structure.sh` | `shebang` | First line is exactly `#!/usr/bin/env python3` | FAIL | Make the entry point explicit |
| `check_structure.sh` | `guard-missing` | `if __name__ == "__main__":` guard exists at module top level | FAIL | Make the entry point explicit |
| `check_structure.sh` | `guard-shape` | guard body invokes `sys.exit(main())` (not just `main()`) | FAIL | Make the entry point explicit |
| `check_structure.sh` | `syntax` | file parses as Python (emitted by the AST helper when `ast.parse` raises) | FAIL | Fail loud, fail early, return meaningful codes |
| `check_structure.sh` | `main-returns` | `main()` signature returns an `int` | WARN | Make the entry point explicit |
| `check_structure.sh` | `keyboard-interrupt` | `except KeyboardInterrupt` handler at top level of `main()` | WARN | Fail loud, fail early, return meaningful codes |
| `check_structure.sh` | `exec-bit` | Executable bit set when shebang is present | INFO | Make the entry point explicit |
| `check_argparse.sh` | `argparse-when-argv` | `argparse` imported when `sys.argv` accessed past `[0]` | WARN | Parse arguments with argparse |
| `check_argparse.sh` | `add-argument-help` | Every `add_argument()` call carries a non-empty `help=` | WARN | Parse arguments with argparse |
| `check_argparse.sh` | `subprocess-check` | `subprocess.run()` includes `check=True` or inspects the return | WARN | Hold the safety posture |
| `check_deps.sh` | `declared-deps` | 3rd-party imports are declared (PEP 723 block, colocated `requirements.txt`, or top-of-file comment) | WARN | Prefer the standard library |
| `check_ruff.sh` | `ruff-D100` | Module docstring present | WARN | Document intent at the top |
| `check_ruff.sh` | `ruff-E722` | No bare `except:` | FAIL | Fail loud, fail early, return meaningful codes |
| `check_ruff.sh` | `ruff-SIM115` | Context manager wraps `open()` calls | WARN | Treat I/O as a contract |
| `check_ruff.sh` | `ruff-PLW1514` | `encoding="utf-8"` on text-mode `open()` | WARN | Treat I/O as a contract |
| `check_ruff.sh` | `ruff-PTH` | `pathlib.Path` over `os.path` string manipulation | WARN | Treat I/O as a contract |
| `check_ruff.sh` | `ruff-S602` / `ruff-S604` | No `shell=True` in subprocess calls (both rule codes cover the same pattern) | FAIL | Hold the safety posture |
| `check_ruff.sh` | `ruff-S307` | No `eval` / `exec` | FAIL | Hold the safety posture |
| `check_ruff.sh` | `ruff-F401` | No unused imports | WARN | Prefer the standard library |
| `check_ruff.sh` | `ruff-ANN` | Type hints on function signatures | WARN | Dress the style |
| `check_ruff.sh` | `ruff-format` | `ruff format --check` passes | WARN | Dress the style |
| `check_ruff.sh` | `ruff-UP031 / ruff-UP032` | f-strings over `%` / `.format()` | WARN | Dress the style |
| `check_ruff.sh` | `ruff-F403` | No wildcard imports | FAIL | Dress the style |
| `check_ruff.sh` | `ruff-S108` | No hardcoded `/tmp/` or `/var/tmp/` path literals | FAIL | Hold the safety posture |
| `check_size.sh` | `size` | Script length ≤ 500 non-blank lines | WARN | Keep functions small and single-purpose (script-level) |

**FAIL exclusions from Tier-2.** Any `secret`, `syntax` (Python
`SyntaxError`), `ruff-S307`, `ruff-S602` / `ruff-S604`, `ruff-S108`,
`ruff-E722`, or `ruff-F403` finding excludes the file from Tier-2.
Other FAILs (`shebang`, `guard-missing`, `guard-shape`) leave a
parseable script that judgment can still evaluate productively.

## Tier-2 — Judgment Dimensions

One LLM call per file. All nine dimensions run every time; a dimension
that doesn't apply returns PASS silently. Findings carry WARN severity
unless a dimension explicitly marks otherwise — judgment-level drift
is coaching, not blocking.

### D1 Output Discipline

**Source principles:** *Treat I/O as a contract*; *Fail loud, fail
early, return meaningful codes.*

**Judges:** Does data output go to stdout and chatter (logs, errors,
prompts) go to stderr? Does every error path actually produce a
non-zero exit code, or is there an error path that logs-and-returns-0?
When operational messages are emitted, is `logging` used (configured to
stderr) rather than `print` for them?

**PASS conditions:** No `print()` of error/log content to stdout. Every
documented or implied failure mode results in `return N` where `N > 0`
or `raise`. Operational messages route through `logging` when the
script carries verbosity flags or runs in automation.

**Common fail signal:** `print(f"error: {err}")` without `file=sys.stderr`;
error branches that log and then `return 0`; `print()` used as a mix of
data output and status narration.

### D2 Input Validation

**Source principles:** *Fail loud, fail early, return meaningful codes*;
*Hold the safety posture.*

**Scope:** Input validation and destructive-operation safety — these are
two sides of the same discipline: don't damage state on input you haven't
inspected.

**Judges:** Are inputs validated before any destructive or expensive
work begins? For deletes, overwrites, or irreversible network calls, is
there a `--dry-run` flag (or equivalent confirmation gate), and does
the destructive branch actually read it? Are credentials, hostnames,
and paths sourced from arguments or the environment rather than
hardcoded?

**PASS conditions:** Validation of required inputs is the first work
`main()` does after argparse. Destructive branches check a dry-run or
confirmation flag. No credentials or absolute paths appear as string
literals.

**Common fail signal:** A `shutil.rmtree()` call that runs before the
input path is checked to exist; a `--dry-run` flag that's declared but
never consulted in the destructive branch; a hostname embedded in a
string literal.

### D3 Dependency Posture

**Source principles:** *Prefer the standard library.*

**Judges:** When a third-party dependency is imported, is the
complexity it brings justified — or would `argparse`, `pathlib`, `json`,
`csv`, `subprocess`, `logging`, `tempfile`, or `http.client` suffice?

**PASS conditions:** Every non-stdlib import has a clear reason the
stdlib equivalent cannot meet (e.g., `requests` for streaming + retry,
`pydantic` for schema validation). Stdlib-solvable problems use the
stdlib.

**Common fail signal:** `requests.get(url).json()` where
`urllib.request.urlopen(url).read()` + `json.loads()` would do;
`pandas.read_csv()` for a 200-row CSV that `csv.DictReader` handles.

### D4 Performance Intent

**Source principles:** *Treat I/O as a contract* (streaming subset);
the performance subsection of the principles doc.

**Judges:** Does the script read whole files into memory when it only
iterates over them? Does it materialize lists or sets from generators
without needing random access or repeated traversal?

**PASS conditions:** Line-by-line iteration for text files consumed
once; generator chains for transformations; explicit `list()` only
where materialization is needed.

**Common fail signal:** `content = open(path).read()` followed by
`for line in content.splitlines()`; `list(map(f, xs))` where the result
is iterated once; loading a large CSV into memory before filtering.

### D5 Naming

**Source principles:** *Name intent into the code* (plus external
sources: Clean Code ch. 2 Meaningful Names).

**Judges:** Do function and variable names state their intent
specifically enough that a reader can predict behavior without diving
into the body? Are single-letter names confined to loop counters, math
conventions, and comprehensions? Are builtins shadowed (`list`, `id`,
`file`, `type`)?

**PASS conditions:** Names at module scope are descriptive.
Single-letter names appear only in `for i in range(...)` or similar
local-scope conventions. No builtin is shadowed.

**Common fail signal:** `def process(data):`, `tmp = ...`, `d = ...`,
`list = []`, module-level `x = config()` with no meaningful name.

### D6 Function Design

**Source principles:** *Keep functions small and single-purpose*;
*Eliminate duplication* (plus external sources: Clean Code ch. 3
Functions; *The Pragmatic Programmer* §15 DRY).

**Judges:** Does each function do one coherent thing at one level of
abstraction? Are three or more near-identical blocks extracted into a
shared helper? Do function names stay clean, or do they sprout
conjunctions (`parse_and_validate_and_write`)?

**PASS conditions:** `main()` reads as a sequence of named operations.
Helper functions each have a single verb-phrased name. Repeated blocks
become helpers.

**Common fail signal:** A 200-line `main()` that inlines fetch,
transform, validate, and write; the same 6-line try/except block
copy-pasted three times with different filenames.

### D7 Module-Scope Discipline

**Source principles:** *Keep the module scope disciplined* (plus
external sources: Clean Code ch. 17 G13; *Effective Python* Item 16).

**Judges:** Does the module top level hold only imports, constants,
class/function definitions, and the `__main__` guard? Are there
module-level function calls, global mutable state, or side-effecting
initialization that would fire at import time?

**PASS conditions:** No module-level assignments beyond constants
(CONSTANT_CASE) and typed aliases. No function calls outside the
`__main__` guard. No mutable globals referenced from within functions
(use arguments instead).

**Common fail signal:** `client = HTTPClient()` at module scope;
`CONFIG = json.load(open("cfg.json"))` at module scope; a `setup()` call
outside the guard.

### D8 Literal Intent

**Source principles:** *Name intent into the code* (literal-constant
subset; plus Clean Code ch. 17 G25 magic numbers).

**Judges:** Do numeric and string literals that carry meaning have
named-constant homes? `0`, `1`, `-1`, and empty strings are exempt; a
`30` that represents a timeout, or a `10` that represents page size, is
not.

**PASS conditions:** Meaningful literals live at the top of the module
as `UPPER_SNAKE_CASE` constants. Exemptions apply for trivial values
(`0`, `1`, `-1`, `""`, `None` equivalents) and for values that would
not improve with a name (array indexing, single-use values tied to the
literal in-place).

**Common fail signal:** `requests.get(url, timeout=30)` with no
`REQUEST_TIMEOUT_SECONDS = 30` constant; a page-size `100` repeated
across three call sites.

### D9 Commenting Intent

**Source principles:** *Document intent at the top* (inline-comment
subset; plus Clean Code ch. 4).

**Judges:** Do comments explain *why* a non-obvious choice was made —
constraint, trade-off, workaround — or do they restate what the code
already says? Do TODOs carry an owner or a ticket?

**PASS conditions:** Comments name hidden constraints or subtle
invariants. TODOs are tagged (`TODO(bbeidel)` or `TODO(WIKI-123)`).
Code that needs extensive what-comments is refactored to read on its
own.

**Common fail signal:** `# increment counter` above `counter += 1`;
bare `# TODO: fix this` with no owner; a paragraph comment explaining
logic that a helper function would name.

## Tier-3 — Cross-Entity Collision

### collision

**What it checks:** When the audit scope holds multiple Python scripts
in the same directory, look for near-identical `get_parser()` /
error-handler / docstring patterns the maintainer could lift into a
shared module.
**Severity:** WARN.
**Source principle:** *Keep functions small and single-purpose* +
*Review and Decay* — duplicated scaffolding is the early signal that
the script collection wants a real package.

## Cross-Dimension Notes

**All dimensions run always.** A dimension that doesn't apply (D4
Performance intent on a script with no file I/O; D2 Input validation on
a read-only query tool) returns PASS silently. Conditional evaluation
produces inconsistent rubrics across runs and makes findings
non-comparable.

**One finding per dimension maximum.** If D6 Function design identifies
four problematic functions, surface the highest-signal one with
concrete detail (line numbers, what to extract). Bulk findings train
the user to disregard the audit.

**Severity defaults to WARN.** Tier-2 findings are judgment-level
coaching, not blocking. A dimension that surfaces a safety concern the
Tier-1 scripts missed can be escalated to FAIL by the judge, but the
default is WARN — Tier-1 is where blocking lives.
