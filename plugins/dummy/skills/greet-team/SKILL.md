---
name: greet-team
description: >
  Composes greetings for several teammates by invoking
  `/dummy:greet --as-tool` once per name. Demonstrates the caller side
  of the --as-tool invocation pattern — single elicit, repeated inner
  invocations, merged output, single approval gate. Scratch skill
  validating the pattern (issue #327).
argument-hint: "[names]"
user-invocable: true
---

# Greet Team

Compose greetings for a list of teammates by repeatedly invoking `/dummy:greet` under `--as-tool`. The inner skill never speaks to the user directly — this skill owns all human interaction.

## Workflow

### 1. Elicit

Ask the user once:

- **Names** — a comma-separated list or freeform text naming several people. LLM-parse the list out.
- **Time of day** — one of `morning`, `afternoon`, `evening`. Used for every greeting.

### 2. Invoke `/dummy:greet --as-tool` per name

For each name, invoke:

```
/dummy:greet --as-tool name=<name> time-of-day=<shared-tod>
```

Read the JSON block the inner skill returns. Dispatch on `type`:

- **`Success`** — append `value.text` to the collected greetings list.
- **`NeedsMoreInfo`** — one retry only. Attempt to fill any fields listed in `missing` from this skill's elicited context (usually `time_of_day` is already in scope). If the retry still returns `NeedsMoreInfo`, skip that name and note it.
- **`Refusal`** — skip the name. Append `{name, reason}` to a "skipped" list.

Retry budget: **one retry per name**. No unbounded loops.

### 3. Present

Show the user a single combined view:

```
Greetings:
  - Good morning, bob!
  - Good morning, alice!

Skipped:
  - root — refusing to greet a privileged account
```

### 4. Approve

Ask `approve? [y/N]`. Print the final combined list regardless of response.

## Key Instructions

- Do not prompt the user per name. Elicit once; reuse the shared `time-of-day` for every inner invocation.
- Do not show the inner skill's raw JSON to the user — read it, branch on `type`, render only the merged result.
- A `Refusal` is not an error for this skill. Collect refusals and show them alongside successes.
- Retry budget is **one** per name. Do not loop beyond that.

## Handoff

**Receives:** list of teammate names (from `$ARGUMENTS` or elicited), one shared `time-of-day`.
**Produces:** a combined list of greetings plus a skipped list.
**Chainable to:** any skill consuming a list of composed greetings.
