---
name: "Hook Script Testing Strategies"
description: "Testing strategies for bash hook scripts: bats-core as the framework, function decomposition as the prerequisite, stdin simulation for integration tests, and function-override mocking."
type: context
sources:
  - https://www.hackerone.com/blog/testing-bash-scripts-bats-practical-guide
  - https://bats-core.readthedocs.io/en/stable/writing-tests.html
  - https://advancedweb.hu/how-to-mock-in-bash-tests/
  - https://honeytreelabs.com/posts/writing-unit-tests-and-mocks-for-unix-shells/
related:
  - docs/research/2026-04-13-shell-script-best-practices.research.md
  - docs/context/hook-script-safety-preamble.context.md
  - docs/context/hook-script-error-reporting.context.md
  - docs/context/hook-script-injection-prevention.context.md
  - docs/context/hook-script-json-payload-handling.context.md
  - docs/context/hook-script-shellcheck-static-analysis.context.md
  - docs/context/hook-script-bash-style-conventions.context.md
---

# Hook Script Testing Strategies

Function decomposition is the prerequisite for testable hook scripts. bats-core is the primary framework at scale; stdin simulation with `printf` works for lightweight integration tests. Function overriding is the simplest mocking approach.

## Prerequisite: Function Decomposition

Hook scripts that run all logic at the top level are not amenable to unit testing with sufficient coverage. The bats-core documentation states this explicitly: "library functions and shell scripts that run many commands when they are called or executed... The only way to test this pile of code with sufficient coverage is to break it into many small, reusable, and, most importantly, independently testable functions."

Structure hooks as a collection of named functions with a `main` call at the bottom:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

extract_tool_name() { jq -r '.tool_name' <<< "${1}"; }
is_bash_tool() { [[ "${1}" == "Bash" ]]; }
check_command() { ... }

main() {
  local payload
  payload="$(cat)"
  local tool_name
  tool_name="$(extract_tool_name "${payload}")"
  ...
}

main "$@"
```

This structure allows each function to be tested in isolation.

## bats-core Framework

bats-core is the most widely documented bash testing framework (alternatives exist: shunit2, shellspec). It is TAP-compliant, written in bash, and provides three key helpers:

- **`run`** — executes a command and captures its exit status and output without triggering `set -e`
- **`$status`** — the exit code of the last `run` invocation
- **`$output`** — the combined stdout of the last `run` invocation

A minimal test:

```bash
@test "rejects rm -rf /" {
  run bash hook.sh <<< '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}'
  [ "$status" -eq 2 ]
  [[ "$output" =~ "blocked" ]]
}
```

Tests pass when all commands in the test body exit 0.

## Stdin Simulation for Integration Tests

Evidence suggests that for hooks expecting JSON on stdin, `printf` with a pipe is the correct simulation pattern:

```bash
printf '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | ./hook.sh
```

Use `printf` rather than `echo` for explicit newline control when the script expects multi-line JSON. This pattern requires no framework and is appropriate for simple hooks or CI environments where installing bats is not feasible.

Test with real payload shapes, not just mocked stubs. Hook integration failures commonly arise from field name changes or missing fields in actual Claude Code payloads — tests that use accurate payload templates catch these.

## Mocking Priority

Evidence suggests a priority order for mocking external commands:

1. **Function override (preferred)** — define a shell function with the same name as the command; it takes precedence over the PATH entry. Use `export -f` to make it visible to subshells.

```bash
jq() { echo "mocked-output"; }
export -f jq
```

2. **PATH override** — place a custom executable earlier in PATH. Requires maintaining a separate file per mock; separates mock definitions from test cases.

3. **`eval`-based dynamic mocks** — avoid for hook tests; `eval` is a security anti-pattern and adds unnecessary complexity.

The function override approach has one limitation: it affects the entire test process, not a single test case. Scope mock definitions carefully, or unset them after each test.

## Takeaway

Decompose hook logic into small functions before writing tests. Use bats-core for comprehensive test suites; use `printf | ./hook.sh` for lightweight integration checks. Mock external commands (including `jq`) with function overrides and `export -f`. Test with accurate Claude Code payload shapes, not synthetic minimal inputs.
