# Automated Validation Patterns

Patterns for running and interpreting automated validation commands from
a plan's Validation section.

## Command Execution Protocol

Run each code block from the Validation section in numbered-list order
(priority order). For each command:

1. Execute the command in the project root
2. Capture exit code, stdout, and stderr
3. Record the result: exit code 0 = pass, non-zero = fail

Report results immediately per criterion — do not batch all commands
before reporting.

## Structural vs. Semantic Checks

**Structural checks** confirm observable state exists:
- File exists at expected path
- Function or class is exported from module
- Endpoint returns expected HTTP status
- Configuration key is present

**Semantic checks** confirm behavior is correct:
- Test suite passes
- Migration runs without error
- Linter reports zero violations
- Build completes successfully

Both types can be fully automated. Structural checks are faster and
less environment-dependent; prefer them for quick confidence before
running heavier semantic checks.

## Output Interpretation

Not all non-zero exits are failures. Read command output:

| Tool Type | Exit Behavior | What to Check |
|-----------|--------------|---------------|
| Test runners | Non-zero = failures exist | Count of failures, which tests |
| Linters | Non-zero = violations found | Severity — errors vs. warnings |
| Build tools | Non-zero = build failed | Missing deps vs. code errors |
| Type checkers | Non-zero = type errors | Count and location of errors |

A linter reporting only warnings with a non-zero exit may be acceptable
depending on the plan's criteria. Read the criterion text — if it says
"no errors" then warnings are fine. If it says "clean lint" then warnings
also fail.

## Environment Sensitivity

Commands may depend on project setup. When a command fails with an
environment error, classify it as **blocked**, not **failed**:

| Signal | Classification | Action |
|--------|---------------|--------|
| `command not found` | Blocked | Report missing tool, suggest install |
| `connection refused` | Blocked | Report missing service (database, server) |
| `No module named...` | Blocked | Report missing dependency |
| Test assertion failure | Failed | Report as validation failure |
| Syntax/type error | Failed | Report as validation failure |

Report blocked items separately: "Criterion N could not be evaluated —
[tool/service] is not available. Set up [what's needed] and re-run."

## Idempotency

Validation commands should be safe to re-run without side effects. If a
command creates data, modifies state, or sends external requests, flag
it to the user before running:

> "Criterion N runs `[command]` which may [describe side effect].
> Proceed?"

## Examples

**Code implementation:**
```bash
uv run python -m pytest tests/ -v
```
Check: exit code 0, output contains "N passed, 0 failed"

**Refactoring (regression check):**
```bash
ruff check src/ && uv run python -m pytest tests/ -v
```
Check: both commands exit 0, no new lint errors, no test regressions

**Migration:**
```bash
python manage.py migrate --check
```
Check: exit code 0, output contains "No migrations to apply"

**Build:**
```bash
npm run build
```
Check: exit code 0, no error output. Warnings are acceptable unless
the criterion specifies "clean build."
