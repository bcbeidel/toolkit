---
name: Hook Testing Guide
description: Three-layer verification procedure for Claude Code hook scripts — stdin simulation, configuration check, execution trace, payload capture, and graduated deployment.
---

# Hook Testing Guide

Before activating the hook, run a syntax check first — it's free and catches
errors before any execution:

```bash
bash -n .claude/hooks/<name>.sh
```

Then verify it behaves correctly with a simulated payload. Use `printf` (not
`echo`) for explicit newline control:

```bash
# Test that a blocking payload is rejected (expect exit 2)
printf '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"},"hook_event_name":"PreToolUse"}' \
  | .claude/hooks/<name>.sh
echo "exit: $?"

# Test that a benign payload passes (expect exit 0)
printf '{"tool_name":"Bash","tool_input":{"command":"echo hello"},"hook_event_name":"PreToolUse"}' \
  | .claude/hooks/<name>.sh
echo "exit: $?"
```

Use accurate Claude Code payload shapes — field name errors (`cmd` instead of
`command`) fail silently with `jq` returning `null`. For comprehensive test
suites, decompose hook logic into named functions and test each with bats-core.

## Three-Layer Verification

1. **Configuration** — Run `/hooks` in Claude Code to confirm the hook appears
   under the correct event and matcher. A hook missing from this list will never
   fire regardless of the script's correctness.

2. **Logic isolation** — The `printf` tests above. Also measure performance:
   ```bash
   time printf '{"tool_name":"Bash","tool_input":{"command":"ls"}}' \
     | .claude/hooks/<name>.sh
   ```
   Target under 1 second for synchronous hooks.

3. **Execution trace** — Start Claude Code with `claude --debug-file /tmp/claude.log`
   and tail the log in a separate terminal. The debug log shows exit codes, full
   stdout, and full stderr for every hook that fires.

## Payload Capture

To validate jq paths against a real payload, add temporarily during development
(remove before production):

```bash
echo "$INPUT" > /tmp/last-hook-input.json
```

Inspect the file to confirm exact field names before writing extraction logic.
jq returns `null` silently on wrong paths — this is the most common cause of
hooks that pass everything through.

## Graduated Deployment

Before enforcing with `exit 2`, deploy the hook using `exit 1` (warning only)
and monitor for false positives for at least a week. One false positive per
session is sufficient to create bypass culture where users habitually override
the hook.
