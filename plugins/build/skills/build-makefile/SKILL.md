---
name: build-makefile
description: >
  Scaffolds a top-level Makefile for repository workflow
  orchestration — strict-shell header, safety `MAKEFLAGS`, `.PHONY`
  coverage, self-documenting `help` from `## description` comments,
  overridable `?=` config, and a flat target graph with scoped
  `clean`. Use when the user wants to "create a makefile", "scaffold
  a makefile", or "new makefile for [X]". Not for POSIX-`make`,
  compilation-driving Makefiles, or multi-module recursive builds.
argument-hint: "[purpose]"
user-invocable: true
references:
  - ../../_shared/references/makefile-best-practices.md
  - ../../_shared/references/primitive-routing.md
license: MIT
---

# Build Makefile

Scaffold a top-level `Makefile` that orchestrates developer workflows
(build, test, lint, fmt, run, deploy, clean, ci) as a single source
of truth shared by local developers and CI. The authoring rubric —
anatomy, patterns that work, safety posture — lives in
[makefile-best-practices.md](../../_shared/references/makefile-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

This skill is scoped to **GNU Make ≥ 4.0 with bash pinned as `SHELL`**.
POSIX `make` portability, C/C++ compilation trees, and multi-module
recursive builds are out of scope and refused at the Scope Gate.

**Workflow sequence:** 1. Route → 2. Scope Gate → 3. Elicit →
4. Draft → 5. Safety Check → 6. Review Gate → 7. Save → 8. Test

## 1. Route

Confirm a top-level `Makefile` is the right primitive before asking
scaffold-specific questions.

**Wrong primitive:**

- **A standalone shell script invoked from a one-off command** →
  `/build:build-bash-script`. Scripts stand alone; Makefiles
  orchestrate named verbs across scripts.
- **A Claude Code hook** → `/build:build-hook`.
- **A Claude Code skill** → `/build:build-skill`.
- **A semantic-judgment rule** → `/build:build-rule`.

**Wrong language/platform:**

- **POSIX `make` portability needed** — strict `/bin/sh` with no GNU
  extensions → out of scope; this skill pins bash.
- **Compilation-driving build** — C/C++/Fortran source tree with
  pattern rules, `.o`/`.so` outputs → out of scope; the rubric this
  skill operationalizes is workflow orchestration, not compilation.
- **Multi-module recursive build** — `$(MAKE) -C subdir` pattern
  across more than trivial dispatch → out of scope; a flat target
  graph is the target shape here.

**Right primitive** (top-level developer-workflow orchestration;
GNU Make ≥ 4.0; bash `SHELL`; flat target graph) → proceed to Scope
Gate.

## 2. Scope Gate

Refuse to scaffold — and recommend an alternative — when the request
signals Makefile is the wrong tool. Probe for any of:

1. **Target repo already has a `Makefile`.** Scaffolding over it
   discards the existing target graph. Offer to run
   `/build:check-makefile` against the existing file and iterate
   from findings instead.
2. **POSIX `make` portability needed.** This skill pins bash; strict
   POSIX `sh` Makefiles are a different scope. Recommend the user
   rewrite without bashisms and remove the `SHELL` pin, or pick a
   different tool.
3. **C/C++/Fortran compilation tree.** Pattern rules, implicit
   suffixes, and multi-stage object-file builds are not this skill's
   target. Recommend a dedicated build system (`cmake`, `bazel`,
   `meson`) or a hand-rolled Makefile that intentionally keeps the
   inference rules this skill disables.
4. **Multi-module recursive build.** More than a trivial
   `$(MAKE) -C subdir` dispatch wants a flat target graph or a real
   build system. Scaffolding one here would misrepresent the scope.
5. **Fewer than three recurring verbs.** A repository with one or two
   commands does not earn a Makefile; a README snippet or a single
   `/build:build-bash-script` is a lower-overhead fit.

If any signal fires, state the signal, name the recommended
alternative, and stop. Do not proceed to Elicit.

## 3. Elicit

If `$ARGUMENTS` is non-empty, parse it as `[purpose]` and pre-fill the
purpose. Otherwise ask, one question at a time:

**1. Purpose** — one sentence: what repo and what workflows?
("orchestrate build/test/lint/run for a Python web service", "wrap
the dbt + pytest workflow for this analytics repo").

**2. Target surface** — which public verbs from the canonical set
apply? `build`, `test`, `lint`, `fmt`, `run`, `deploy`, `clean`,
`ci`, `help`. Check what the repo actually has; omit verbs the
project will never use. `help` and `ci` are almost always present;
`deploy` is often absent for libraries.

**3. Primary tools** — which CLI tools drive each target?
(`pytest`, `ruff`, `black`, `docker`, `npm`, `poetry`, `uv`,
`cargo`, `go`, `terraform`). Drives the `?=` variable list at the
top of the file.

**4. Build artifacts** — is there a `$(BUILD_DIR)` (dist, build,
out, target)? If yes, the scaffold wires `clean` to that directory
with `rm -rf -- "$(BUILD_DIR)"`, adds the order-only prerequisite
pattern for any target that produces files there, and includes the
`$(BUILD_DIR): mkdir -p "$@"` helper. If no (test-only project),
`clean` is omitted or scoped to other artifacts.

**5. Destructive targets?** — does the repo need `deploy`,
`publish`, `release`? If yes, the scaffold adds a `CONFIRM=1` guard
pattern to each and documents it in the `## description`.

**6. Local-override support** — wire `-include .env.mk` and add
`.env.mk` to `.gitignore`? Default yes; decline only if the project
has a different override mechanism already.

**7. Save path** — always `Makefile` (case-sensitive) at the repo
root. Confirm the repo root unless the context already makes it
obvious.

## 4. Draft

Produce two artifacts.

**Artifact 1: The `Makefile`.**

One conditionalized template. Sections marked *(if destructive)*,
*(if has-build-dir)*, or *(if has-override)* are omitted when intake
rules them out.

```makefile
# <repo-name> — <one-line purpose>.
# Requires: GNU Make ≥ 4.0, bash.

SHELL            := bash
.SHELLFLAGS      := -eu -o pipefail -c
MAKEFLAGS        += --warn-undefined-variables --no-builtin-rules
.SUFFIXES:
.DELETE_ON_ERROR:
.DEFAULT_GOAL    := help

# --- Configuration ----------------------------------------------------------
PYTHON           ?= python3                                   # (example — from intake step 3)
BUILD_DIR        ?= build                                     # (if has-build-dir)
-include .env.mk                                              # (if has-override)

# --- Public targets ---------------------------------------------------------

.PHONY: help build test lint fmt run deploy clean ci          # (populate from intake step 2)

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"} /^[a-z][a-zA-Z0-9_-]+:.*##/ \
	  { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build: | $(BUILD_DIR) ## Build the project.                   # | $(BUILD_DIR) (if has-build-dir)
	$(PYTHON) -m build --outdir "$(BUILD_DIR)"

test: ## Run the test suite.
	$(PYTHON) -m pytest

lint: ## Run linters.
	$(PYTHON) -m ruff check .

fmt: ## Format the source tree.
	$(PYTHON) -m ruff format .

deploy: ## Deploy to production (set CONFIRM=1).              # (if destructive)
	@[[ "$${CONFIRM:-0}" = "1" ]] || { echo "set CONFIRM=1 to deploy" >&2; exit 1; }
	./scripts/deploy.sh

clean: ## Remove build artifacts.                             # (if has-build-dir)
	rm -rf -- "$(BUILD_DIR)"

ci: lint test ## Run the exact checks CI runs.

# --- Internal helpers -------------------------------------------------------

$(BUILD_DIR):                                                 # (if has-build-dir)
	mkdir -p "$@"
```

*(if not destructive)* Omit `deploy` from `.PHONY` and the target
block.

*(if no build dir)* Omit `BUILD_DIR`, the order-only `| $(BUILD_DIR)`
prerequisite on `build`, the `clean` target, and the `$(BUILD_DIR):`
helper.

*(if no override)* Omit the `-include .env.mk` line.

**Artifact 2: A `.gitignore` diff**, for the `.env.mk` line *(if
has-override)* — present as a paste-ready addition, do not edit
`.gitignore` yourself. If the repo has no `.gitignore`, propose
creating one with the single line.

Present both artifacts to the user before any safety checks.

## 5. Safety Check

Review the draft against the rubric in
[makefile-best-practices.md](../../_shared/references/makefile-best-practices.md)
before presenting. Group the checks:

**Header.** `SHELL := bash`. `.SHELLFLAGS := -eu -o pipefail -c`.
`MAKEFLAGS += --warn-undefined-variables --no-builtin-rules`.
`.SUFFIXES:` line present. `.DELETE_ON_ERROR:` present.
`.DEFAULT_GOAL := help`.

**`.PHONY` coverage.** Every public verb from intake step 2 is in
`.PHONY`. No accidental file-producing targets listed as `.PHONY`.

**Help discipline.** `help` is the first real target. Every public
target has a `## description` suffix. Recipe parses `$(MAKEFILE_LIST)`
so additions auto-surface.

**Variables.** Tool variables use `?=`; no bare `=` unless an inline
comment explains deliberate deferral. No top-level `$(shell …)` for
expensive commands.

**Safety.** `clean` scoped to `$(BUILD_DIR)` or an explicit allowlist
— never unscoped `rm -rf`. Destructive targets (`deploy`, `publish`,
`release`) begin with a `CONFIRM=1` guard. No `sudo`, `npm install
-g`, unscoped `pip install`, pipe-to-shell installers.

**Recipe hygiene.** Recipes ≤ 5 lines. `@` prefix only on `echo`,
`printf`, `:`. Variable expansions in recipes are quoted as
`"$(VAR)"`. No literal `make` in recipes (use `$(MAKE)` if recursion
is truly needed).

If any check fails, revise the draft before presenting. The Review
Gate is for user approval, not correctness recovery.

## 6. Review Gate

Present both artifacts (Makefile + `.gitignore` diff if applicable)
and wait for explicit user approval before writing any file. Write
only after this gate passes.

If the user requests changes, revise and re-present. Continue until
the user explicitly approves or cancels. Proceed to Save only on
explicit approval.

## 7. Save

Write the approved `Makefile` to the repo root. No `chmod` — a
Makefile is data, not an executable script. If the user accepted the
`.gitignore` diff, append the line (do not rewrite the file).

Show the suggested invocation: `make help` to verify the target list
surfaces correctly and to catch any `## description` issues the
Safety Check missed.

## 8. Test

Offer the audit:

> "Run `/build:check-makefile Makefile` to audit the scaffolded file
> against the deterministic + judgment dimensions?"

Running the audit once after scaffold catches anything the Safety
Check missed and gives the user a baseline-clean starting point.

## Anti-Pattern Guards

1. **Scaffolding over an existing Makefile** — Scope Gate signal #1
   applies without exception. Offer `/build:check-makefile` instead.
2. **Scaffolding for compilation trees** — this skill is scoped to
   workflow orchestration. Pattern rules, implicit inference, and
   object-file build graphs belong in a real build system.
3. **Declaring file-producing targets as `.PHONY`** — breaks Make's
   incremental semantics. If `build` produces `$(BUILD_DIR)/<file>`,
   the target should be `$(BUILD_DIR)/<file>:`, not `build:`.
4. **Hand-maintained `help` text** — the scaffolded `help` parses
   `##` descriptions from `$(MAKEFILE_LIST)`. Do not emit a help
   target that hardcodes a list of commands; it rots the moment a
   target is added.
5. **Skipping the Review Gate** — write to disk only after explicit
   user approval. Present both artifacts first.

## Key Instructions

- Refuse cleanly on Scope Gate signals. POSIX-`make`, compilation
  trees, recursive multi-module builds, and existing-Makefile cases
  are hard refuses.
- Write files to disk only after the Review Gate passes.
- The scaffold pins `SHELL := bash`; do not offer a "portable"
  fallback. This skill's scope is explicitly bash-pinned Make.
- The `CONFIRM=1` guard is only scaffolded when Intake step 3.5
  flagged destructive operations. Do not add it as a general pattern.
- `-include .env.mk` is only scaffolded when Intake step 3.6 opted
  in. Do not add it as dead structure.
- Won't scaffold when any Scope Gate signal fires — recommend the
  appropriate alternative.
- Recovery if a Makefile is written in error: `rm Makefile` removes
  it cleanly. No settings.json entries, no shared-module
  registration — the scaffold is self-contained.

## Handoff

**Receives:** user intent for a top-level Makefile (purpose, target
surface, primary tools, build artifacts, destructive-op flag,
local-override opt-in, save path).

**Produces:** a `Makefile` at the repo root plus, optionally, a
`.gitignore` diff for `.env.mk`.

**Chainable to:** `/build:check-makefile` (audit the scaffolded
Makefile against the deterministic + judgment dimensions).
