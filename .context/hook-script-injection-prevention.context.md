---
name: "Hook Script Injection Prevention"
description: "Shell injection prevention for hook scripts: prohibit eval, quote all variable expansions, and use absolute command paths to neutralize the three primary injection vectors."
type: context
sources:
  - https://developer.apple.com/library/archive/documentation/OpenSource/Conceptual/ShellScripting/ShellScriptSecurity/ShellScriptSecurity.html
  - https://matklad.github.io/2021/07/30/shell-injection.html
  - https://sipb.mit.edu/doc/safe-shell/
  - https://bertvv.github.io/cheat-sheets/Bash.html
  - https://mywiki.wooledge.org/BashGuide/Practices
  - https://www.linuxbash.sh/post/bash-shell-script-security-best-practices
related:
  - docs/research/2026-04-13-shell-script-best-practices.research.md
  - docs/context/hook-script-safety-preamble.context.md
  - docs/context/hook-script-error-reporting.context.md
  - docs/context/hook-script-json-payload-handling.context.md
  - docs/context/hook-script-testing-strategies.context.md
  - docs/context/hook-script-shellcheck-static-analysis.context.md
  - docs/context/hook-script-bash-style-conventions.context.md
---

# Hook Script Injection Prevention

Hook scripts that process JSON payloads from Claude Code receive user-influenced data. The `tool_input.command` field in Bash hook payloads reflects what the user asked Claude to run. Three rules — no `eval`, quote everything, use absolute paths — eliminate the primary injection vectors.

## Rule 1: Never Use `eval`

`eval` passes a string to the shell interpreter for execution. If any part of that string derives from user input, the user controls what gets executed. Apple Developer documentation and matklad's shell injection analysis converge on this independently: do not pass user-influenced data to `eval`. There is no safe way to sanitize input sufficiently for `eval` use; the correct fix is to avoid `eval` entirely.

## Rule 2: Always Quote Variable Expansions

Unquoted variables undergo two transformations that create injection opportunities:

- **Word splitting** — the shell splits the value on `IFS` characters (space, tab, newline); a value containing spaces becomes multiple arguments
- **Globbing** — values containing `*`, `?`, or `[` are expanded against the filesystem

Both mechanisms allow content in `tool_input` fields to alter script control flow. The fix is consistent quoting:

```bash
# Wrong — word-splitting and globbing apply
tool_name=$tool_name

# Correct — quoted, brace-delimited form
tool_name="${tool_name}"
```

This rule applies to every variable derived from the JSON payload, including fields that appear harmless (file paths, tool names, command arguments). MIT SIPB, Apple Developer docs, Bert Van Vreckem's cheat sheet, and Greg's Wiki all confirm this independently.

## Rule 3: Use Absolute Paths for External Commands

Evidence suggests that PATH manipulation can redirect commonly used tools to malicious replacements. If a hook calls `jq`, `grep`, or `python3` by bare name, and an attacker has modified PATH, the call resolves to a replacement binary.

Use absolute paths for all external command invocations in hook scripts:

```bash
# Prefer
/usr/bin/jq -r '.tool_name' <<< "${payload}"

# Or resolve at the top of the script
JQ=/usr/bin/jq
"${JQ}" -r '.tool_name' <<< "${payload}"
```

Note: this is a MODERATE-confidence finding from a single T5 source. On controlled environments where PATH is not attacker-controlled, bare command names are lower risk. Apply judgment based on the deployment context.

## Threat Model for Claude Code Hooks

The `tool_input` field in hook payloads contains user-influenced data — specifically, `tool_input.command` in PreToolUse Bash hooks reflects what the user asked Claude to execute. This field flows through the hook script and must be treated as untrusted input for all injection prevention purposes.

## Takeaway

Apply three rules unconditionally: no `eval`, quote `"${all_variables}"`, use absolute paths for external tools. These eliminate the three primary injection vectors for hook scripts processing Claude Code JSON payloads.
