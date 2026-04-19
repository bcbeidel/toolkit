---
name: FX.1 Scope Gate
description: >
  Catalog of five signals that indicate shell is the wrong tool, with
  detection heuristics and per-signal refusal copy for build-shell.
---

# FX.1 Scope Gate

`/build:build-shell` must refuse to scaffold when intake signals that
shell is the wrong tool. This reference lists the five signals, how to
detect each, the recommended alternative, and the phrasing to use when
refusing.

Derived from [FX.1 cross-cutting finding] — research summarized in
issue bcbeidel/toolkit#322. Without this gate, the skill would actively
increase bash prevalence in codebases where Python or Go serves better
(MIT SIPB: "when possible, instead of writing a 'safe' shell script,
use a higher-level language like Python").

## How to use this reference

Probe each signal during Elicit. If any fires, halt before Draft and
respond with the refusal copy. Do not continue into the scaffold flow.

If the signals are ambiguous, name the ambiguity for the user and ask
them to confirm — do not guess. A false-positive refusal is cheaper
than a scaffolded script for the wrong primitive.

## Signals

### 1. Structured records

**Detection.** The user describes data as typed rows, multiple fields
per record, joins across tables or files, or anything that implies a
schema — "parse this CSV with five columns and compute a rolling
average per category", "merge two JSON arrays on `id`", "validate each
row against a spec".

**Alternative.** Python with `pandas` / `pydantic` / `dataclasses`, or
Go with `encoding/json` + structs.

**Refusal copy.**
> "Shell scripts can pipe lines but not structured records. Once you
> need columns, joins, or schema validation, bash loses its leverage —
> you spend more lines on `awk`/`cut` gymnastics than on the actual
> logic. Recommend Python with `pandas` (for CSV) or `pydantic` (for
> JSON). Want to redirect?"

### 2. JSON/YAML beyond a jq one-liner

**Detection.** The user describes multi-step JSON or YAML manipulation
— reads, transforms, and writes that cannot be expressed as a single
`jq` filter. Sign-markers: "parse this YAML config", "merge three JSON
files and produce a fourth", "validate JSON against a schema".

**Alternative.** Python with stdlib `json` / `yaml` (PyYAML), or a
typed language.

**Refusal copy.**
> "`jq` is great for single-pass reads and simple transforms. Anything
> that composes transforms, maintains state, or validates structure is
> a Python or Go task. Recommend stdlib Python. Want to redirect?"

### 3. Projected >100 LOC of business logic

**Detection.** Estimate the non-boilerplate length from the user's
description. Header, help text, and preflight do not count. If the
logic the user is describing will require more than ~100 lines of
actual behavior — nested loops, multiple state variables, error
handling across multiple failure modes — shell is the wrong tool.

**Alternative.** Python is the default. Go for performance-sensitive
or strictly-typed needs.

**Refusal copy.**
> "A shell script this size will read like a Rube Goldberg machine
> within a month. Past ~100 lines of business logic, bash pays a
> complexity tax on everything — error handling, control flow,
> testability. Recommend Python. Want to redirect?"

### 4. Windows compatibility need

**Detection.** The user mentions Windows, WSL-optional, PowerShell, or
"cross-platform including Windows". Git Bash and WSL are shell
environments but the scripts will hit platform-specific gaps
(different `find`, different `sed`, no `readlink -f`, different path
separators in a shell that doesn't translate them).

**Alternative.** Pick one:
- **Unix-only** — commit to `#!/usr/bin/env bash` and document that
  Windows is not supported.
- **True cross-platform** — use Python (`pathlib` handles separators,
  stdlib covers the rest) or Go (single binary, native Windows build).
- **PowerShell** — a different primitive; this skill does not
  scaffold PowerShell.

**Refusal copy.**
> "Cross-platform including Windows is not a bash target. Shell
> pipelines differ between Git Bash, WSL, and MSYS2; a single script
> rarely works on all three. Pick one: commit to Unix-only bash, or
> switch to Python / Go for true portability. Which?"

### 5. Concurrency / threading

**Detection.** The user describes parallel tasks, fan-out/fan-in, a
worker pool, or anything that implies multiple units running at once.
Sign-markers: "run N jobs in parallel", "process while downloading",
"rate-limited worker pool".

Simple `cmd1 & cmd2 & wait` is fine for 2–3 one-off background jobs.
Anything beyond that hits bash's concurrency sharp edges (`wait -n` is
bash 4+ only, race conditions between subshells, no mutex primitives,
no structured cancellation).

**Alternative.** Python `concurrent.futures` or `asyncio`; Go goroutines.

**Refusal copy.**
> "Bash has no concurrency primitives beyond backgrounded processes.
> Anything more than 'run these two things at once and wait' will
> acquire race conditions faster than you can test them. Recommend
> Python `concurrent.futures` or Go. Want to redirect?"

## When a signal is borderline

If the user's description genuinely straddles the line — e.g., "this
script is 80 lines now but might grow" — state the risk plainly and
ask them to pick:

> "This is on the edge: shell works for the current scope but grows
> painful past ~100 lines of logic. Scaffold in bash and plan to
> rewrite in Python if it grows, or start in Python now? I'll go with
> your call."

Do not scaffold silently over a yellow signal.
