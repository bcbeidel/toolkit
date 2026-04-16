---
name: "Hook Script JSON Payload Handling"
description: "Safe JSON payload extraction patterns for bash hook scripts: use jq --arg to pass shell variables into filter expressions, and treat tool_input fields as user-influenced data."
type: context
sources:
  - https://medium.com/data-science/jq-a-saviour-for-sanitising-inputs-not-just-outputs-1fd6728c0dc4
related:
  - docs/research/2026-04-13-shell-script-best-practices.research.md
  - docs/context/hook-script-safety-preamble.context.md
  - docs/context/hook-script-error-reporting.context.md
  - docs/context/hook-script-injection-prevention.context.md
  - docs/context/hook-script-testing-strategies.context.md
  - docs/context/hook-script-shellcheck-static-analysis.context.md
  - docs/context/hook-script-bash-style-conventions.context.md
---

# Hook Script JSON Payload Handling

Hook scripts read JSON from stdin. Two patterns govern safe extraction: use `jq --arg` when shell variables must be passed into jq filter expressions, and always quote extracted values before further shell use.

## Extracting Fields from the Payload

Basic extraction reads the payload once and assigns fields:

```bash
payload="$(cat)"
tool_name="$(jq -r '.tool_name' <<< "${payload}")"
command="$(jq -r '.tool_input.command' <<< "${payload}")"
```

The `-r` flag outputs raw strings without JSON quoting. Store the full payload in a variable rather than re-reading stdin; stdin is a one-shot stream.

## Passing Shell Variables into jq: Use `--arg`

Evidence suggests that interpolating shell variables directly into jq filter expressions is an injection vector. If a variable contains jq syntax characters (`.`, `[`, `"`, `|`), the filter breaks or executes unintended queries.

The `--arg` flag handles escaping correctly:

```bash
# Wrong — direct interpolation is an injection vector
result="$(jq ".[\"${USER_VAR}\"]" <<< "${payload}")"

# Correct — --arg escapes the value
result="$(jq --arg key "${USER_VAR}" '.[$key]' <<< "${payload}")"
```

`--arg name value` binds the shell variable as a typed jq string, bypassing any jq syntax interpretation of its contents.

Note: this is a MODERATE-confidence finding. The primary source had 403 access issues during research. The jq project's own documentation would be the authoritative reference; `--arg` behavior is well-established in community practice but lacks a T1 source in this research.

## The `tool_input.command` Field Is User-Influenced

The `command` field in Bash PreToolUse hook payloads reflects what the user asked Claude to execute. Extract it with:

```bash
command="$(jq -r '.tool_input.command' <<< "${payload}")"
```

Then quote `"${command}"` before any further shell use. Never interpolate it unquoted into another command string. This field is the primary injection surface in Bash hook scripts.

## jq Availability

`jq` may not be installed on minimal systems. If `jq` absence would silently break the hook (no error, wrong behavior), add an availability check:

```bash
if ! command -v jq &>/dev/null; then
  echo "jq is required but not installed" >&2
  exit 1
fi
```

For environments where `jq` cannot be guaranteed, `python3 -c "import json,sys; ..."` with the stdlib `json` module is universally available.

## Takeaway

Read stdin once into a variable. Extract fields with `jq -r`. Use `--arg` when shell variables must enter jq filter expressions. Always quote extracted values. Treat `tool_input.command` as user-controlled input and handle accordingly.
