---
name: "Hook Script Bash Style Conventions"
description: "Google Shell Style Guide conventions for hook scripts: naming, error output, function structure, long-form flags, and use of [[ over [ for conditionals."
type: context
sources:
  - https://google.github.io/styleguide/shellguide.html
  - https://bertvv.github.io/cheat-sheets/Bash.html
  - https://mywiki.wooledge.org/BashGuide/Practices
related:
  - docs/research/2026-04-13-shell-script-best-practices.research.md
  - docs/context/hook-script-safety-preamble.context.md
  - docs/context/hook-script-error-reporting.context.md
  - docs/context/hook-script-injection-prevention.context.md
  - docs/context/hook-script-json-payload-handling.context.md
  - docs/context/hook-script-testing-strategies.context.md
  - docs/context/hook-script-shellcheck-static-analysis.context.md
---

# Hook Script Bash Style Conventions

The Google Shell Style Guide is the T1 reference for bash conventions. Four additional practices — long-form flags, function header comments, `[[` over `[`, and whitespace discipline — round out the readability standard for hook scripts.

## Naming Conventions (Google Style Guide)

Variable and function naming follows a case convention:

- **Local variables and functions** — `lower_case_with_underscores`
- **Exported variables and constants** — `UPPER_CASE_WITH_UNDERSCORES`, declared at the top of the file

```bash
readonly MAX_PAYLOAD_SIZE=65536
local tool_name
tool_name="$(extract_tool "${payload}")"
```

Prefer `"${var}"` over `"$var"` — the brace form makes the variable boundary explicit and is consistent with both Google style and Bert Van Vreckem's cheat sheet.

## Error Output to STDERR

All error messages go to STDERR. This applies to hook blocking messages as well as diagnostic output:

```bash
echo "Blocked: command contains dangerous pattern" >&2
```

Hook scripts communicate block decisions and error details through STDERR. Stdout is reserved for output that the calling process consumes.

## `main` Function and Function Structure

A `main` function is required when the script contains at least one other named function. This keeps the top-level execution path explicit and testable:

```bash
main() {
  local payload
  payload="$(cat)"
  # logic here
}

main "$@"
```

Evidence suggests function header comments should document the function's contract: description, globals used, arguments, outputs (stdout/stderr), and return values. This makes the function inspectable during security review without executing it. In practice this is commonly omitted — apply to public-facing functions and those with non-obvious behavior.

## Long-Form Flags

Use long-form flags where available — `--silent` over `-s`, `--recursive` over `-r`, `--quiet` over `-q`. Long flags are self-documenting and reduce review friction in hook scripts that may be audited for security:

```bash
# Preferred in hook scripts
curl --silent --output /dev/null --write-out "%{http_code}" "${url}"

# Acceptable for well-known tools in context
grep -q "pattern" file.txt
```

This is a MODERATE-confidence practice from a single T4 source. Apply where it improves readability without excessive line length (80-character maximum per Google style).

## `[[` Over `[` for Conditionals

Use `[[` instead of `[` for conditionals in bash scripts. `[[` does not perform word-splitting on unquoted variables, supports `=~` for regex matching, and has more intuitive string comparison semantics:

```bash
# Correct — [[ does not word-split
if [[ "${tool_name}" == "Bash" ]]; then

# Correct — regex matching
if [[ "${command}" =~ ^rm ]]; then

# Avoid — [ performs word-splitting; less safe
if [ "${tool_name}" = "Bash" ]; then
```

This is a MODERATE-confidence recommendation from Greg's Wiki (wooledge), broadly accepted in the bash community.

## Takeaway

Apply Google Shell Style Guide as the baseline: `lower_case` functions, `UPPER_CASE` exports, all errors to STDERR, `main()` required when other functions exist. Supplement with long-form flags for auditable scripts, function header comments for non-obvious contracts, and `[[` over `[` for all bash conditionals.
