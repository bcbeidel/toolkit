---
name: greet
description: >
  Greets a person by name with a time-appropriate salutation. Supports
  human mode (prompts for missing info, asks for approval) and
  `--as-tool` mode (structured return, no ceremony, for skill callers).
  Scratch skill validating the --as-tool invocation pattern (issue #327).
argument-hint: "[name] [time-of-day]"
user-invocable: true
---

# Greet

Emit a time-appropriate greeting for a given name. Two invocation modes:

- **Human** (default) — prompts for missing info, prints the greeting, asks for approval.
- **`--as-tool`** — skill-caller mode. No prompts, no approval, no rendering. Returns structured JSON.

## Required fields

- `name` — the person to greet.
- `time-of-day` — one of `morning`, `afternoon`, `evening`. Anything else falls back to a generic `Hello`.

## `$ARGUMENTS` parsing

| Shape | Mode | Behavior |
|---|---|---|
| empty | human | full Elicit |
| freeform text (no `=`, no `--`) | human | LLM-parse `name` and `time-of-day` from text; prompt for missing |
| `key=value` tokens | human | parse named fields; prompt for missing; non-kv tokens ignored |
| `--as-tool` present | skill | require all fields; hard-fail via `NeedsMoreInfo` if any missing; skip Elicit + approval |

## Workflow

### 1. Parse `$ARGUMENTS` per the table above.

### 2. Scope gate

If `name` starts with `root` (case-sensitive): refuse.
- **Human mode:** print `REFUSED: refusing to greet a privileged account` and stop.
- **`--as-tool` mode:** return `Refusal` (see Return below).

### 3. Compose

Map `time-of-day` to a salutation:
- `morning` → `Good morning`
- `afternoon` → `Good afternoon`
- `evening` → `Good evening`
- anything else → `Hello`

Compose: `<salutation>, <name>!`

### 4a. Human mode — present + approve

Print the greeting. Ask `approve? [y/N]`. Print the final greeting regardless of response (this is a scratch skill; no save step).

### 4b. `--as-tool` mode — return structured

**Evidence marker (temporary — invocation-mechanism probe for #327).**

Before emitting the return JSON, use the Bash tool to append one line to the evidence file:

```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) inner name=<NAME-OR-null> tod=<TOD-OR-null>" >> /tmp/greet-evidence.txt
```

Substitute the actual parsed values in place of `<NAME-OR-null>` and `<TOD-OR-null>` (use the literal string `null` when a field is missing). This line runs on every `--as-tool` invocation regardless of the return kind (Success, NeedsMoreInfo, or Refusal) — it is the invocation trace, not an output artifact. The marker will be removed after the probe completes.

After the evidence append, output **only** a JSON block. No prose, no preamble. One of three shapes:

**Success:**
```json
{"type": "Success", "value": {"text": "Good morning, bob!", "name": "bob", "time_of_day": "morning"}}
```

**NeedsMoreInfo** (any required field missing):
```json
{"type": "NeedsMoreInfo", "missing": ["time_of_day"], "hint": "pass `name` and `time_of_day` as structured args under --as-tool"}
```

**Refusal** (scope gate fired):
```json
{"type": "Refusal", "reason": "refusing to greet a privileged account", "category": "scope-gate"}
```

## Key Instructions

- Under `--as-tool`: emit the JSON block and nothing else. No `input()`. No approval.
- Under `--as-tool`: hard-fail on missing required fields by returning `NeedsMoreInfo`. Do not prompt.
- Under human mode: prompt for whatever `$ARGUMENTS` didn't supply.

## Handoff

**Receives:** `name`, `time-of-day` (from `$ARGUMENTS` or elicited).
**Produces:** a greeting string (human) or structured JSON (`--as-tool`).
