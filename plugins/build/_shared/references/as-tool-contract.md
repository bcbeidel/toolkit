---
name: "--as-tool Invocation Contract"
description: Generic mechanism spec for the dual-invocation pattern. A skill that declares `skill-invocable: true` in its frontmatter becomes callable by another skill via `--as-tool` — structured args in, structured payload out, no human ceremony. This file is the authoritative contract; opt-in skills reference it from their frontmatter.
---

# `--as-tool` Invocation Contract

## Purpose

A skill's computation is often more reusable than its user interface. `greet` computes a greeting *and* prompts the user; but a downstream skill that just wants the greeting shouldn't inherit the prompts. The `--as-tool` pattern lets one skill invoke another at runtime with a structured payload, receive a structured return, and skip all the human ceremony the callee would otherwise perform.

Opt in per-skill via `skill-invocable: true` in frontmatter — the field parallels `user-invocable`. Reach for this pattern when the skill's output is consumable by *another skill* (the caller pre-fills inputs, inspects the return, handles retries). Skip it for exploratory, interactive-by-design, or judgment-heavy skills where the ceremony is the product.

## Parsing rule

Every `--as-tool` skill parses `$ARGUMENTS` with one deterministic rule, regardless of the skill's domain:

| Shape | Mode | Behavior |
|---|---|---|
| empty | human | full Elicit (ask all required fields interactively) |
| freeform text (no `=` tokens, no `--` flags) | human | LLM-parse what it can from the text; prompt for anything still missing |
| `key=value` tokens | human | parse named fields; prompt for anything still missing; non-kv tokens are noise |
| `--as-tool` present (with or without `key=value` tokens) | skill-caller | require all declared fields; hard-fail via `NeedsMoreInfo` if any are missing; skip Elicit, Review Gate, and Save |

Only the fourth row triggers `--as-tool` mode. The first three are human-mode variants.

## Step skip/run under `--as-tool`

`--as-tool` suppresses **human ceremony**, not side effects. Code execution, file reads, invocations of other `--as-tool` skills, and similar non-interactive work all run unchanged. The rule targets humans, not the machine.

| Workflow step | Human mode | `--as-tool` |
|---|---|---|
| Route | runs | runs |
| Scope Gate (FX.1-style) | runs; halts interactively on refusal | runs; refusal returned as structured `Refusal`, does **not** halt |
| Elicit | runs; prompts for missing fields | **skipped**; hard-fail via `NeedsMoreInfo` if any required field missing |
| Draft / core computation | runs | runs |
| Safety Check | runs; revises in place | runs; findings packed into the return payload |
| Review Gate | runs; waits for user approval | **skipped**; the caller owns approval |
| Save (`chmod +x`, file writes) | runs | **skipped**; the caller owns writes |
| Test handoff (offer follow-up skill) | runs | **skipped** |

Rule of thumb: if the step prompts a human or writes to disk on the user's behalf, it's skipped under `--as-tool`.

## Envelope — three cases

Every `--as-tool` skill returns one of three control-flow cases in a JSON envelope. The envelope is always JSON; the success *payload* shape varies by skill (see DATA vs ARTIFACT below).

- `Success` — the skill completed; the payload is ready.
- `NeedsMoreInfo` — recoverable. The required fields are incomplete; the caller can fill the gap and retry. Envelope carries `missing` (array of field names) and `hint` (one-sentence guidance).
- `Refusal` — categorical. The skill declined to compute; retry will not help (e.g., scope-gate fire, invalid input combination, permission boundary). Envelope carries `reason` (one-line explanation) and `category` (short machine-friendly tag like `scope-gate`, `permission`, `invalid-combo`).

`NeedsMoreInfo` and `Refusal` are **always JSON-only**, regardless of the skill's return shape. No fenced code block follows on either failure path. This keeps the failure contract uniform across every `--as-tool` skill.

## Return shape DATA

For skills whose output is a structured object (greet composes a greeting struct; check-skill emits findings; scope-work emits a design summary), use Shape **DATA**.

Success emission is JSON only — no fenced block follows:

```
{"type": "Success", "value": {"text": "Good morning, bob!", "name": "bob", "time_of_day": "morning"}}
```

The `value` schema is skill-declared (documented in the skill's own `## --as-tool contract` section). The caller parses the JSON and reads fields by name.

`NeedsMoreInfo` / `Refusal` follow the envelope rules above (JSON only).

## Return shape ARTIFACT

For skills whose output is a text artifact in its native syntax (build-shell produces a shell script; build-rule produces a markdown file; build-skill produces a SKILL.md; build-hook produces both a hook script and a JSON settings entry), use Shape **ARTIFACT**.

Success emission is a JSON envelope **followed by one or more fenced code blocks** carrying the artifact bodies in their native formats:

```
{"type": "Success", "artifact_types": ["text/x-shellscript"], "metadata": {"target": "bash-3.2-portable"}}
```
```bash
#!/usr/bin/env bash
set -Eeuo pipefail
# ... the full scaffold ...
```

**Multi-artifact variant** — a single call producing multiple artifacts (e.g., a hook script + its settings.json entry):

```
{"type": "Success", "artifact_types": ["text/x-shellscript", "application/json"], "metadata": {"hook_event": "PreToolUse"}}
```
```bash
#!/usr/bin/env bash
# hook script
```
```json
{"hooks": {"PreToolUse": [...]}}
```

**Rules:**

- The number and order of fenced code blocks must match the `artifact_types` array exactly. A skill declaring `["text/x-shellscript", "application/json"]` emits two fenced blocks — bash first, then json.
- Each fenced block's language tag matches the declared MIME type per the table below. Language-tag-per-MIME is what lets the caller route each block to the right consumer (mutate the shell, parse the JSON) without string-matching headers.
- `metadata` is an optional JSON object carrying skill-specific facts that aren't the artifact itself (target shell, hook event, render variant, etc.).
- `NeedsMoreInfo` and `Refusal` remain JSON-only. No fenced blocks follow on the failure paths — the failure envelope is identical across DATA and ARTIFACT skills.

**Language tag per MIME type:**

| MIME type | Fenced-block language tag |
|---|---|
| `application/json` | `json` |
| `text/x-shellscript` | `bash` |
| `text/x-python` | `python` |
| `text/markdown` | `markdown` |
| `text/x-yaml` / `application/yaml` | `yaml` |
| `text/x-toml` | `toml` |
| `text/plain` | `text` |

Add entries only when a new artifact type is genuinely needed. Keep the set small; prefer existing types over inventing new ones.

## When to pick DATA vs ARTIFACT

Use the following rule of thumb:

- **DATA** — the output is a structured record the caller will read field-by-field. Examples: `greet` (a greeting with name/time/text), `check-skill` (findings list), `scope-work` (a design summary object).
- **ARTIFACT** — the output is code, configuration, markdown, or any text file whose value comes from its native syntax. Examples: `build-shell` (bash script), `build-rule` (markdown rule file), `build-skill` (a new SKILL.md), `build-hook` (shell script + settings.json entry).

Pick ARTIFACT whenever JSON-escaping the payload would harm readability or debuggability. Multi-line code embedded in a JSON string is legal but brittle; a fenced code block is the natural medium.

Hybrid case — a skill whose output includes *both* a structured record *and* a text artifact — use ARTIFACT and carry the structured part in the envelope's `metadata` object.

## Parallel-safety

By default, invoking an `--as-tool` skill N times from within a single outer-skill run is **safe to parallelize**. This is a free win when the caller iterates over a collection (greet-team greeting N teammates) — Claude Code will invoke them concurrently.

Skills must document an exception when they are *not* parallel-safe. Common causes: shared resource acquisition (file locks, rate-limited APIs), ordering dependencies (later calls consume earlier-call state), singleton side effects (writes to a specific known path). If any of these apply, declare `**Parallel-safe:** no — <reason>` in the skill's contract section. The caller is responsible for serializing the invocations.

Absence of a parallel-safety note is interpreted as "yes, safe." Declaring `**Parallel-safe:** yes` explicitly is the recommended habit.

## Freeform-text human mode

The parsing rule's second row (freeform text with no `=` or `--`) exists because humans speak the way they speak, not the way a CLI accepts args. A human typing `/dummy:greet blake morning welcome to the thunderdome` expects the skill to extract `name=blake` and `time_of_day=morning` from the text and get on with it. Similarly, voice-dictated inputs are a first-class shape — they arrive as freeform strings.

Under freeform mode, the skill's LLM parses what it can from the text (best-effort) and prompts interactively for anything still missing. There is no hard-fail path in human mode — a user talking to the skill will always be asked to clarify.

Freeform-text mode does **not** apply under `--as-tool`. Callers must pre-fill all required fields using `key=value` tokens (or supply them in `metadata` on re-invocation after `NeedsMoreInfo`). The inner skill will not LLM-parse prose under `--as-tool`.

## When NOT to use the pattern

Not every skill benefits from opt-in. Skip `--as-tool` when:

- **The skill is exploratory or interactive by design.** `/work:scope-work` drives a divergent-then-convergent dialogue; pre-filling its intake defeats the purpose. `/consider:*` skills apply mental models through conversation. Mechanizing these produces empty motions.
- **The deliverable is human judgment.** If the skill's value is a considered recommendation that requires human review at each step, there's nothing to return as a pure function.
- **The output is advisory context** loaded for a human's benefit (CLAUDE.md-style conventions injected into a session). No caller wants to "invoke" advisory context.
- **The skill is a chain orchestrator.** `/work:start-work` sequences other skills under human approval gates; it's a controller, not a computation.

When in doubt, default to opt-out. The ecosystem benefits more from a small set of well-designed `--as-tool` skills than from blanket adoption. A future skill can always opt in later; unwinding premature opt-in is harder.
