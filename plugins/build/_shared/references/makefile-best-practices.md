---
name: Makefile Best Practices
description: Authoring guide for top-level Makefiles that orchestrate developer workflows — what a load-bearing Makefile does, the canonical anatomy, the patterns that work, and the safety and maintenance posture. Referenced by build-makefile and check-makefile.
---

# Makefile Best Practices

## What a Good Makefile Does

A Makefile at the top of a repository is the single source of truth for developer workflows — build, test, lint, format, run, deploy, clean. A new contributor runs `make help` and sees the public surface; CI invokes the same targets the developer runs locally. If the Makefile is not the source of truth, it is a lie — commands drift between README, CI config, and oral tradition, and "works on my machine" replaces deterministic setup.

The scope here is **GNU Make ≥ 4.0 with bash pinned as `SHELL`**, for repository-local workflow orchestration. POSIX `make` portability and C/C++ compilation trees are different concerns with different rubrics. Multi-module recursive builds (`$(MAKE) -C subdir`) break parallelism and dependency tracking and fall outside this scope; a flat target graph wins for workflow orchestration.

## Anatomy

```makefile
# repo-name — developer workflow orchestration.
# Requires: GNU Make ≥ 4.0, bash.

SHELL            := bash
.SHELLFLAGS      := -eu -o pipefail -c
MAKEFLAGS        += --warn-undefined-variables --no-builtin-rules
.SUFFIXES:
.DELETE_ON_ERROR:
.DEFAULT_GOAL    := help

# --- Configuration ----------------------------------------------------------
PYTHON           ?= python3
BUILD_DIR        ?= build
-include .env.mk

# --- Public targets ---------------------------------------------------------

.PHONY: help build test lint fmt run clean ci

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"} /^[a-z][a-zA-Z0-9_-]+:.*##/ \
	  { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build: | $(BUILD_DIR) ## Build the project.
	$(PYTHON) -m build --outdir "$(BUILD_DIR)"

test: ## Run the test suite.
	$(PYTHON) -m pytest

lint: ## Run linters.
	$(PYTHON) -m ruff check .

clean: ## Remove build artifacts.
	rm -rf -- "$(BUILD_DIR)"

ci: lint test ## Run the exact checks CI runs.

# --- Internal helpers -------------------------------------------------------

$(BUILD_DIR):
	mkdir -p "$@"
```

Load-bearing pieces: strict-shell header (`SHELL`, `.SHELLFLAGS`), safety `MAKEFLAGS` (`--warn-undefined-variables`, `--no-builtin-rules`), `.SUFFIXES:` to kill legacy inference, `.DELETE_ON_ERROR:` so failed recipes don't leave partial outputs, `.DEFAULT_GOAL := help`, overridable config via `?=`, `-include .env.mk` for local overrides, every public target in `.PHONY`, every public target annotated with `## description`, quoted variable expansions in recipes, scoped `clean`, flat target graph with order-only prerequisite for the build directory.

## Authoring Principles

**Make `help` the default goal.** `.DEFAULT_GOAL := help` plus a `help` target that parses `## description` comments means bare `make` is always informative, never destructive. A Makefile where `make` silently runs `build` is a footgun — contributors hit Enter expecting docs and get a ten-minute build.

**Declare every non-file target as `.PHONY`.** Without `.PHONY`, a file named `test` in the repo silently breaks `make test`. The single most important correctness rule; every public verb (`build`, `test`, `lint`, `fmt`, `run`, `deploy`, `clean`, `ci`) belongs in `.PHONY`.

**Pin the shell explicitly.** `SHELL := bash` and `.SHELLFLAGS := -eu -o pipefail -c`. Default `/bin/sh` varies across systems; without `pipefail`, a failure inside a pipeline is silently swallowed. Broadly distributed tooling that needs POSIX `sh` is a different skill's scope — this rubric pins bash for clarity and fail-fast semantics.

**Enable the safety `MAKEFLAGS`.** `--warn-undefined-variables` catches typos like `$(BULID_DIR)` before they expand to empty and turn `rm -rf $(BUILD_DIR)/` into `rm -rf /`. `--no-builtin-rules` plus a bare `.SUFFIXES:` disables decades of legacy C/Fortran inference rules. `.DELETE_ON_ERROR:` prevents Make from leaving a corrupted partial output on failure.

**Indent recipes with real tabs.** Non-negotiable Make syntax; spaces produce `missing separator`. Configure `.editorconfig` with `[Makefile] indent_style = tab` so editors don't silently subvert this.

**Name public targets as lowercase-hyphenated verbs.** `build`, `test`, `lint`, `fmt`, `run`, `deploy`, `clean`, `ci`. Muscle memory for `make test` should work in every project a contributor touches.

**Document every public target with a `## description`.** The `help` target parses these; hand-maintained help rots, generated help stays honest. Targets without a description are invisible to `make help` and should not be part of the public API.

**Prefix internal helpers with `_` and omit the `##`.** `_check-deps:`, `_build-stamp:`. Separates user-facing API from implementation; keeps `make help` output clean.

**Put variables at the top; use `:=` and `?=` deliberately.** Configuration before behavior. Default to `:=` (immediate) for simple assignment; use `?=` for overridable defaults that respect environment and CI variables; use bare `=` (deferred) only when lazy expansion is deliberate, documented with an inline comment. Recursive `=` re-evaluates on every reference and causes surprising performance and ordering bugs.

**Quote variable expansions in recipes.** `"$(VAR)"`, not `$(VAR)`. Unquoted paths with spaces or empty variables silently corrupt commands — same bug class as unquoted `$var` in any shell script.

**Keep recipes short.** ≤5 lines. When logic grows, extract to `scripts/` and invoke from the target. Make is a poor scripting language; complex shell belongs in testable `.sh` files that `shellcheck` and `shfmt` can audit.

**Scope `clean` and guard destructive targets.** `clean` removes only `$(BUILD_DIR)` and an explicit allowlist, never `rm -rf` with an unvalidated variable. Targets that mutate external state (`deploy`, `publish`, `release`) require an explicit confirmation variable (`CONFIRM=1`). Accidental deploys are expensive; typing `CONFIRM=1` is cheap.

**Never mutate the user's machine.** No `sudo`, `npm install -g`, unscoped `pip install`, `curl | sh`. Install into project-local locations — `.venv/`, `node_modules/`, vendored binaries. Supply-chain risk from piped-remote-install is not worth a one-line convenience.

**Pin tool invocations to project-local versions.** `./node_modules/.bin/eslint`, `.venv/bin/pytest`, `poetry run`, `uv run`. Relying on `$PATH` lets global tool versions drift and makes CI diverge from local.

**Don't hide commands.** `@` prefix only for `echo`, `printf`, or `:`. Hiding output obscures failures during debugging. Users who want quiet output run `make -s`.

**Don't swallow failures.** `|| true` silently suppresses errors — the mechanism through which broken builds ship. If failure is genuinely acceptable, annotate with a comment explaining why.

**Provide a `ci` target.** `ci: lint test` — the exact checks CI runs, callable locally. The largest payoff from writing a Makefile at all: the "works on my machine" ritual dissolves when every contributor and pipeline invokes the same target graph.

**Support local overrides without touching the tracked file.** `-include .env.mk` (leading `-` makes the include non-fatal when absent). `.env.mk` in `.gitignore`. Contributors tune without drifting committed config.

**Don't embed secrets.** No tokens, credentials, or environment-specific URLs in the Makefile. `include .env` with `.env` gitignored is the minimum bar; a secrets manager is better where available.

**Use sentinel files for expensive idempotent setup.** `.venv/.installed`, `.stamp-deps`. Avoids re-running slow installs on every invocation while keeping the target graph honest.

**Use order-only prerequisites for directories.** `target: | $(BUILD_DIR)` creates the directory once without retriggering dependent work every time its mtime changes.

**Prefer a flat target graph over recursive Make.** `$(MAKE) -C subdir` for workflow orchestration breaks parallelism and dependency tracking. When recursion is genuinely needed, invoke as `$(MAKE)` — never literal `make` — so flags and `-j` counts propagate.

## Patterns That Work

**`help`-as-default over bare-`make`-builds.** `.DEFAULT_GOAL := help` keeps the no-argument invocation informative.

**`.PHONY`-coverage over file-name collisions.** Every non-file verb declared; `make test` never silently skipped.

**Strict shell over default `sh`.** `SHELL := bash` + `.SHELLFLAGS := -eu -o pipefail -c` + `--warn-undefined-variables` + `--no-builtin-rules` + `.DELETE_ON_ERROR:`.

**Quoted expansions over silent corruption.** `"$(VAR)"` in recipes.

**Short recipes over inline scripting.** ≤5 lines; extract to `scripts/` otherwise.

**`:=` / `?=` over bare `=`.** Deferred expansion only when deliberate and commented.

**`make help` from `##` descriptions over hand-maintained help text.** Parses `MAKEFILE_LIST` so nothing rots.

**Project-local tools over `$PATH` drift.** `./node_modules/.bin/…`, `.venv/bin/…`.

**Sentinel files over unconditional reruns.** `.venv/.installed` for expensive idempotent setup.

**Order-only dir prerequisites over retrigger.** `target: | $(BUILD_DIR)`.

**`ci` target over duplicated CI config.** One graph, two callers.

**Flat graph over recursive `$(MAKE) -C subdir`.** Preserves parallelism and deps.

## Safety

Makefiles run at the invoker's privilege and reach the filesystem, the network, and arbitrary subprocesses. The safety rules are non-negotiable.

- **No unguarded `rm -rf $(VAR)`.** Validate non-empty; scope to the repo. `--warn-undefined-variables` catches the typo class before expansion.
- **No `sudo` in recipes.** Dev workflows don't mutate the user's machine.
- **No global installs.** No `npm install -g`, unscoped `pip install`, or `gem install` without `--user-install`. Use project-local virtualenvs, `node_modules`, or pinned binaries.
- **No `curl | sh` / `curl | bash`.** Supply-chain risk; require explicit, versioned installation steps.
- **No secrets in the Makefile.** `include .env` with `.env` gitignored; escalate to a secrets manager where available.
- **Guard destructive targets.** `deploy`, `publish`, `release`, `prod-*` begin their recipe with an explicit `CONFIRM=1` check.
- **Don't pipe errors away.** `|| true` without an adjacent comment is how broken builds ship.

Tier-1 scripts audit these deterministically. Remaining rules — recipe length, naming, commenting intent, cross-target consistency — rely on judgment.

## Review and Decay

Makefiles rot. Safety `MAKEFLAGS` get edited and defaults fall off; targets accumulate as authors add one more helper each release; CI starts running commands the Makefile no longer covers; `.PHONY` lists drift out of sync with actual targets. Retire targets when their workflow is dead. Split into included `*.mk` files past ~300 lines — beyond that, navigation suffers and the single-file advantage is lost. Convert recipes to `scripts/` files when they exceed ~5 lines — bash in a Makefile is less testable than bash in a `.sh` file, and only marginally more portable.

---

**Diagnostic when a Makefile misbehaves.** First check the strict-shell header (`SHELL`, `.SHELLFLAGS`, `MAKEFLAGS`). Then check `.PHONY` against the actual target set — mismatches are how `make test` silently no-ops when a `test` directory appears. Then check quoting in recipes (`"$(VAR)"`). Then check `clean`'s scope. Most pathologies live in one of those four places.

### Contested rules (adopt or reject per team, be consistent)

- **`.ONESHELL:`** — off by default here; some teams prefer it over `&& \` continuations.
- **Bash vs POSIX `sh`** — this rubric pins bash; broadly distributed tooling may need strict POSIX instead.
- **Line-length limits** — not enforced here; defer to repo-wide style.
- **Default to `:=` over `=`** — strongly recommended; not universal.
