---
name: Repair Playbook — Makefiles
description: One repair recipe per Tier-1 finding type plus one per Tier-2 dimension plus one per Tier-3 collision. Each recipe is Signal → CHANGE → FROM → TO → REASON. Applied during the check-makefile opt-in repair loop with per-finding confirmation.
---

# Repair Playbook

Per-finding repair recipes for check-makefile. Every Tier-1 finding
type and every Tier-2 dimension has a recipe here. Apply one at a
time, with explicit user confirmation, re-running the producing
check after each fix.

## Table of Contents

- [Format](#format)
- Tier-1 recipes
  - [`check_secrets.py`](#tier-1--check_secretspy)
  - [`check_structure.py`](#tier-1--check_structurepy)
  - [`check_phony.py`](#tier-1--check_phonypy)
  - [`check_help.py`](#tier-1--check_helppy)
  - [`check_indent.py`](#tier-1--check_indentpy)
  - [`check_naming.py`](#tier-1--check_namingpy)
  - [`check_variables.py`](#tier-1--check_variablespy)
  - [`check_safety.py`](#tier-1--check_safetypy)
  - [`check_recipes.py`](#tier-1--check_recipespy)
  - [`check_checkmake.sh`](#tier-1--check_checkmakesh)
  - [`check_size.sh`](#tier-1--check_sizesh)
- [Tier-2 — Judgment Dimension Recipes](#tier-2--judgment-dimension-recipes)
- [Tier-3 — Cross-Entity Collision](#tier-3--cross-entity-collision)

## Format

Each recipe carries five fields:

- **Signal** — the finding string that triggers the recipe
- **CHANGE** — what to modify, in one sentence
- **FROM** — a concrete example of the non-compliant pattern
- **TO** — the compliant replacement
- **REASON** — why the change matters, tied to the source principle

---

## Tier-1 — `check_secrets.py`

### Signal: `secret — API key / token / private URL detected`

**CHANGE** Remove the secret; replace with an `include .env` at the
top (and ensure `.env` is gitignored).

**FROM** `API_TOKEN := sk-proj-abc123def456...`
**TO**
```makefile
-include .env                    # .env is .gitignored; commit .env.example instead
API_TOKEN ?=                     # set in .env
```

**REASON** Secrets in committed source leak through git history,
CI logs, and backups. Externalizing to `.env` is the minimum bar.

---

## Tier-1 — `check_structure.py`

### Signal: `shell-pin — \`SHELL := bash\` missing`

**CHANGE** Add `SHELL := bash` near the top of the file.

**FROM** *(no `SHELL` assignment — Makefile uses default `/bin/sh`)*
**TO**
```makefile
SHELL := bash
```

**REASON** Default `/bin/sh` varies (dash on Debian, bash on older
Red Hat, ash on Alpine). Pinning bash locks the dialect so `pipefail`,
`[[ ]]`, and other bashisms work predictably.

### Signal: `shellflags — \`.SHELLFLAGS\` missing \`-e\` / \`-o pipefail\` / \`-c\``

**CHANGE** Set `.SHELLFLAGS := -eu -o pipefail -c`.

**FROM** *(no `.SHELLFLAGS` — Make invokes shell as `/bin/sh -c`)*
**TO**
```makefile
.SHELLFLAGS := -eu -o pipefail -c
```

**REASON** Without `pipefail`, a failing `curl | jq` silently
succeeds if `jq` exits 0. Without `-e`, a failing intermediate
command lets the recipe continue. `-u` catches undefined-variable
typos in recipes.

### Signal: `warn-undefined — \`MAKEFLAGS += --warn-undefined-variables\` missing`

**CHANGE** Add `MAKEFLAGS += --warn-undefined-variables`.

**FROM** *(no `--warn-undefined-variables`)*
**TO** `MAKEFLAGS += --warn-undefined-variables`

**REASON** A typo like `$(BULID_DIR)` expands to empty; `rm -rf
$(BUILD_DIR)/` turns into `rm -rf /`. Make catches the typo only
with this flag set.

### Signal: `no-builtin-rules — \`--no-builtin-rules\` and \`.SUFFIXES:\` both missing`

**CHANGE** Add `MAKEFLAGS += --no-builtin-rules` and/or a bare
`.SUFFIXES:` line.

**FROM** *(neither present)*
**TO**
```makefile
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:
```

**REASON** Built-in implicit rules (C compilation, Fortran,
RCS/SCCS checkout) predate modern workflows and produce surprising
behavior — `make foo` may "just work" because a `foo.c` nearby
triggers `%.o: %.c`. Disabling the rules removes the surprise.

### Signal: `delete-on-error — \`.DELETE_ON_ERROR:\` missing`

**CHANGE** Add a bare `.DELETE_ON_ERROR:` line.

**FROM** *(missing)*
**TO** `.DELETE_ON_ERROR:`

**REASON** Without this, a recipe that writes to `$@` and then
fails leaves a truncated file on disk. Make thinks the target is
built on the next run and skips it. Enabling it makes Make delete
the target on recipe failure.

### Signal: `default-goal — \`.DEFAULT_GOAL := help\` missing and \`help\` is not the first target`

**CHANGE** Add `.DEFAULT_GOAL := help` (or reorder to put `help`
first).

**FROM**
```makefile
build:
	...

help:
	...
```
**TO**
```makefile
.DEFAULT_GOAL := help

help:
	...

build:
	...
```

**REASON** Bare `make` currently builds. That's a footgun —
contributors hit Enter expecting docs and get a ten-minute build.
Making `help` the default preserves the no-surprise invariant.

### Signal: `header-comment — no project/requirements comment in first 5 lines`

**CHANGE** Add a header comment naming the project and requirements.

**FROM** *(no header)*
**TO**
```makefile
# repo-name — developer workflow orchestration.
# Requires: GNU Make ≥ 4.0, bash.

SHELL := bash
```

**REASON** The header is the first thing a reader sees. A file
without one is opaque to anyone who isn't the author.

---

## Tier-1 — `check_phony.py`

### Signal: `phony-coverage — non-file target(s) missing from \`.PHONY\``

**CHANGE** Add the missing targets to the `.PHONY` prerequisite
list (or split into multiple `.PHONY` lines if grouping aids
readability).

**FROM**
```makefile
.PHONY: build test

lint:
	ruff check .
```
**TO**
```makefile
.PHONY: build test lint

lint:
	ruff check .
```

**REASON** A file named `lint` in the repo silently breaks `make
lint` — Make sees the file, decides the target is up to date, and
does nothing. Declaring `.PHONY` tells Make the target is a verb,
not a file.

---

## Tier-1 — `check_help.py`

### Signal: `help-target — no \`help\` target defined`

**CHANGE** Add a `help` target that parses `##` descriptions from
`$(MAKEFILE_LIST)`.

**FROM** *(no help target)*
**TO**
```makefile
help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"} /^[a-z][a-zA-Z0-9_-]+:.*##/ \
	  { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
```

**REASON** `make help` is the user's entry point to the repo's
public surface. Missing it means contributors have to read the
Makefile to find available commands.

### Signal: `help-auto — \`help\` recipe is hand-maintained`

**CHANGE** Replace the hand-maintained `echo` list with an `awk`
parse of `$(MAKEFILE_LIST)`.

**FROM**
```makefile
help:
	@echo "  build    Build the project"
	@echo "  test     Run tests"
	@echo "  lint     Run linters"
```
**TO**
```makefile
help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"} /^[a-z][a-zA-Z0-9_-]+:.*##/ \
	  { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
```

**REASON** Hand-maintained help rots — a new target gets added,
the help list doesn't, and `make help` lies. Parsing `##` comments
makes documentation a side effect of defining a target.

### Signal: `help-desc — public target missing \`## description\``

**CHANGE** Add a `## description` suffix to the target's definition
line.

**FROM** `build:`
**TO** `build: ## Build the project.`

**REASON** Targets without `##` are invisible to the parsed `help`
output. If the target is part of the public API, document it; if
it's not, rename it to `_build` and hide it.

---

## Tier-1 — `check_indent.py`

### Signal: `tab-indent — recipe line uses spaces, not tab` *(FAIL)*

**CHANGE** Replace leading spaces with a single real tab on every
recipe line.

**FROM**
```
build:
    $(PYTHON) -m build
```
*(four spaces — Make rejects with `missing separator`)*

**TO**
```
build:
	$(PYTHON) -m build
```
*(one tab)*

**REASON** Make syntactically requires a tab as the recipe prefix
(unless `.RECIPEPREFIX` is redefined, which is discouraged). Spaces
break parsing outright.

---

## Tier-1 — `check_naming.py`

### Signal: `target-name — public target does not match \`^[a-z][a-z0-9-]*$\``

**CHANGE** Rename to lowercase-hyphenated.

**FROM** `runTheTests:`, `build_prod:`, `Deploy:`
**TO** `run-tests:`, `build-prod:`, `deploy:`

**REASON** Muscle memory for `make test` / `make build` works
across repos only when names follow the shell-command convention.
PascalCase, snake_case, and camelCase break that.

### Signal: `helper-prefix — internal helper target not prefixed with \`_\``

**CHANGE** Rename the helper target to `_<name>` and omit the `##`.

**FROM** `check-deps:` *(no `##`, used only as a prerequisite)*
**TO** `_check-deps:`

**REASON** The underscore prefix signals "not part of the public
API" to both readers and the `help` parser. Keeps `make help`
clean.

---

## Tier-1 — `check_variables.py`

### Signal: `assignment-op — top-level bare \`=\` without justification`

**CHANGE** Change to `:=` (immediate) or `?=` (conditional). If the
deferred evaluation is intentional, annotate with a `# deferred:`
comment.

**FROM** `PYTHON = python3`
**TO** `PYTHON ?= python3` *(if environment should override)* or
`PYTHON := python3` *(fixed)*

**REASON** Recursive `=` re-evaluates the right-hand side every
time the variable is referenced, causing surprising performance
regressions when the RHS has a `$(shell …)`. Default to `:=`.

### Signal: `top-level-shell — expensive \`$(shell …)\` at parse time`

**CHANGE** Move the `$(shell …)` into a recipe, or use a sentinel
file, or switch to a cheap allowlisted command (`git rev-parse`,
`uname`).

**FROM** `VERSION := $(shell curl -s https://...)`
**TO**
```makefile
version:
	@curl -s https://... > .version
```
*(lazy — only invoked when `version` is a prerequisite)*

**REASON** Top-level `$(shell …)` runs on every `make` invocation,
including `make help`. A slow command there makes every `make`
feel broken.

---

## Tier-1 — `check_safety.py`

### Signal: `unguarded-rm — \`rm -rf $(VAR)\` without guard or scope` *(FAIL)*

**CHANGE** Guard with a non-empty check, scope to `$(BUILD_DIR)`,
or add `--` before args.

**FROM** `clean: \n\trm -rf $(OUTPUT)`
**TO**
```makefile
clean: ## Remove build artifacts.
	@[[ -n "$(BUILD_DIR)" && "$(BUILD_DIR)" != "/" ]] || { echo "BUILD_DIR misconfigured" >&2; exit 1; }
	rm -rf -- "$(BUILD_DIR)"
```

**REASON** `rm -rf $(VAR)` with an unset `VAR` is `rm -rf`, which
with an expanded empty does *nothing* but is one typo away from
`rm -rf /`. Validation is cheap insurance.

### Signal: `sudo — \`sudo\` in recipe` *(FAIL)*

**CHANGE** Remove `sudo`; use a user-local install path instead.

**FROM** `install: \n\tsudo pip install -e .`
**TO** `install: \n\tpip install --user -e .` *or* use a
`.venv/bin/pip`.

**REASON** Dev workflows must not mutate the user's machine. `sudo`
in a Makefile implies system-level writes, which can affect other
users and other projects.

### Signal: `global-install — global package install` *(FAIL)*

**CHANGE** Install into a project-local location.

**FROM** `setup: \n\tnpm install -g prettier`
**TO** `setup: \n\tnpm install --save-dev prettier` *(local
`node_modules`)*

**REASON** Global installs drift between developer machines and CI,
producing "works on my laptop" bugs. Project-local installs are
pinned and reproducible.

### Signal: `curl-pipe — \`curl | sh\` or \`curl | bash\` in recipe` *(FAIL)*

**CHANGE** Replace with a versioned, checksummed installation.

**FROM** `setup: \n\tcurl -fsSL https://install.example.com | bash`
**TO** Download a specific release, verify a checksum, then install:
```makefile
setup:
	@curl -fsSL -o /tmp/install.sh https://example.com/install-v1.2.3.sh
	@echo "abc123... /tmp/install.sh" | sha256sum -c -
	@bash /tmp/install.sh
```

**REASON** Piped-remote-install is the classic supply-chain
footgun: whoever controls `install.example.com` today controls your
dev machine tomorrow.

### Signal: `destructive-guard — destructive target without confirmation`

**CHANGE** Add a `CONFIRM=1` guard as the first recipe command.

**FROM**
```makefile
deploy:
	./scripts/deploy.sh production
```
**TO**
```makefile
deploy: ## Deploy to production (set CONFIRM=1).
	@[[ "$${CONFIRM:-0}" = "1" ]] || { echo "set CONFIRM=1 to deploy" >&2; exit 1; }
	./scripts/deploy.sh production
```

**REASON** Accidental `make deploy` is how production incidents
happen. Typing `CONFIRM=1` makes the intent explicit and turns a
muscle-memory slip into a no-op.

---

## Tier-1 — `check_recipes.py`

### Signal: `literal-make — bare \`make\` in recipe`

**CHANGE** Replace bare `make` with `$(MAKE)` — or remove the
recursion entirely if a flat target graph works.

**FROM** `ci: \n\tmake lint \n\tmake test`
**TO** `ci: lint test` *(flat target graph, preferred)* or `ci:
\n\t$(MAKE) lint \n\t$(MAKE) test` *(if recursion is needed)*

**REASON** `$(MAKE)` propagates `-j`, `-s`, `MAKEFLAGS`, and
Make's internal state; bare `make` spawns a fresh Make that knows
none of that. A flat graph (dependencies between targets) is even
better — it enables parallelism and proper dependency tracking.

### Signal: `at-discipline — \`@\` on non-echo/printf command`

**CHANGE** Remove `@` unless the command is `echo`, `printf`, or
`:`.

**FROM** `test: \n\t@$(PYTHON) -m pytest`
**TO** `test: \n\t$(PYTHON) -m pytest`

**REASON** Hiding the command obscures what's running when
something fails. Users who want quiet output run `make -s`. `@`
stays legitimate on `echo` / `printf` where the output *is* the
command ("Running tests…" doesn't need the command echoed first).

### Signal: `or-true-guard — \`|| true\` without explanation`

**CHANGE** Either remove `|| true` (let the failure propagate), or
annotate with a comment explaining why failure is acceptable.

**FROM** `cleanup: \n\trm -rf $(BUILD_DIR) || true`
**TO**
```makefile
cleanup:
	# || true is intentional — $(BUILD_DIR) may not exist on a clean checkout.
	rm -rf -- "$(BUILD_DIR)" || true
```

**REASON** Silent error suppression is how broken builds ship. A
comment makes the suppression a deliberate choice reviewable in
code review; removing the `|| true` surfaces the error where it
belongs.

### Signal: `recipe-length — recipe exceeds 10 lines`

**CHANGE** Extract the recipe body into `scripts/<name>.sh`;
invoke from the target.

**FROM**
```makefile
deploy:
	@[[ "$${CONFIRM:-0}" = "1" ]] || exit 1
	git fetch origin
	git checkout "$$(git rev-parse origin/main)"
	./tools/preflight-check
	./tools/build-release
	./tools/upload-artifact
	./tools/notify-slack
	./tools/post-deploy-healthcheck
	./tools/rollback-on-failure
	./tools/record-deploy
```
**TO**
```makefile
deploy: ## Deploy to production (set CONFIRM=1).
	./scripts/deploy.sh
```

**REASON** Long recipes are untestable and unreadable. A
`scripts/deploy.sh` can be `shellcheck`'d, unit-tested, and
invoked independently.

---

## Tier-1 — `check_checkmake.sh`

### Signal: `checkmake — <rule>: <detail>`

**CHANGE** Varies by rule. `MIXDEPS`: split file and phony
prerequisites. `TIMESTAMP_EXPANDED`: quote timestamps.
`MIN_PHONY`: add `.PHONY`.

**FROM** `checkmake` finding
**TO** Rule-specific fix — see the `checkmake` rule reference for
each.

**REASON** `checkmake` catches Make-idiom mistakes that regex
checks miss. Treat its output as authoritative for the rules it
covers.

---

## Tier-1 — `check_size.sh`

### Signal: `size — file exceeds 300 non-blank lines`

**CHANGE** Split cohesive sections into included `*.mk` files.

**FROM** *(a 500-line Makefile with Build/Test/Deploy/CI blocks
inlined)*
**TO** A ~120-line top-level Makefile that `include`s
`mk/build.mk`, `mk/test.mk`, `mk/deploy.mk`, `mk/ci.mk`.

**REASON** Past ~300 lines, navigation suffers. Included `*.mk`
files keep each slice focused and let a diff touch one domain at a
time.

### Signal: `line-length — line exceeds 120 characters`

**CHANGE** Break with `\` continuations or move to `scripts/`.

**FROM** A 200-char recipe line stitching four commands with `&&`.
**TO** A recipe that invokes `./scripts/<name>.sh`, where the
logic is expressed in shell with proper formatting.

**REASON** Long lines break side-by-side diff views and are
unreadable in code review.

---

## Tier-2 — Judgment Dimension Recipes

Tier-2 findings are WARN-level coaching. Each recipe is a pattern
to apply after the judge names a specific violation.

### D1 Target Contract Integrity

**CHANGE** Align the target surface with the repo's actual
workflows. Add missing canonical verbs (`ci` almost always, `test`
when tests exist). Remove or stub aspirational verbs that don't do
their job.

**FROM** `ci:` that re-runs `pytest` and `ruff` directly.
**TO** `ci: lint test` — reuse the same targets the developer runs.

**REASON** CI drifting from local is the failure mode the
Makefile is supposed to prevent. Reusing targets enforces the "one
graph, two callers" contract.

### D2 Destructive-Op Safety

**CHANGE** Wire the `CONFIRM=1` guard as the first command in
every destructive recipe. Scope `clean` to `$(BUILD_DIR)` and an
explicit allowlist.

**FROM**
```makefile
deploy: ## Deploy (set CONFIRM=1).
	# $(CONFIRM) is documented but never checked
	./scripts/deploy.sh
```
**TO**
```makefile
deploy: ## Deploy (set CONFIRM=1).
	@[[ "$${CONFIRM:-0}" = "1" ]] || { echo "set CONFIRM=1" >&2; exit 1; }
	./scripts/deploy.sh
```

**REASON** A `CONFIRM` variable nobody checks is worse than no
`CONFIRM` at all — it implies a safety that isn't there.

### D3 Recipe Hygiene

**CHANGE** Join multi-step shell operations with `\` continuations,
or extract to a `scripts/` file. Use `$$` for shell-variable escapes.

**FROM**
```makefile
release:
	cd dist
	for f in *.whl; do
	  echo "$f"
	done
```
*(each line runs in a fresh shell — the `cd` is lost, `$f` is Make-expanded)*

**TO**
```makefile
release:
	cd dist && \
	for f in *.whl; do \
	  echo "$$f"; \
	done
```
*(or move the body to `scripts/release.sh`, preferred for anything
non-trivial)*

**REASON** Each recipe line is a fresh shell. Without `\`
continuations, `cd` on line 1 has no effect on line 2.

### D4 Variable & Override Discipline

**CHANGE** Factor configurable values into `?=` overrides at the
top. Use `.venv/bin/` / `./node_modules/.bin/` for tool invocations.

**FROM** `test: \n\tpytest`
**TO**
```makefile
PYTHON ?= .venv/bin/python

test:
	$(PYTHON) -m pytest
```

**REASON** Bare `pytest` uses whatever `pytest` is first on
`$PATH` — often the global one, sometimes a version mismatch.
Pinning to `.venv/bin/python` keeps CI and local identical.

### D5 Incremental Correctness

**CHANGE** Declare file-producing targets against their output
files. Use a sentinel for expensive idempotent setup. Use
order-only prerequisites for directories.

**FROM**
```makefile
.PHONY: build setup

setup:
	pip install -r requirements.txt

build:
	mkdir -p build
	python -m build --outdir build
```
**TO**
```makefile
.PHONY: build

.venv/.installed: requirements.txt
	pip install -r requirements.txt
	touch "$@"

build: | build-dir
	python -m build --outdir build

build-dir:
	mkdir -p build

.PHONY: build-dir
```
*(or declare `build` against its actual `build/<file>.whl` output
where possible)*

**REASON** `.PHONY: setup` makes `pip install` run every time;
the sentinel short-circuits to a single `stat`. Order-only `|
build-dir` creates the directory once without retriggering `build`
on every mtime change.

### D6 Naming & Structure

**CHANGE** Rename targets to the shell-command convention; group
by lifecycle with section comments; prefix internal helpers with
`_`.

**FROM**
```makefile
runTheTests:
check-deps:
Deploy:
```
**TO**
```makefile
# --- Test ---
test: _check-deps
_check-deps:
# --- Deploy ---
deploy: _check-deps
```

**REASON** Consistent naming and grouping is the load-bearing
documentation of a Makefile. PascalCase and camelCase break muscle
memory; scattered helpers mixed with public targets obscure the
public API.

### D7 Documentation Intent

**CHANGE** Add header comment; add `##` to every public target;
remove what-comments; annotate non-obvious choices.

**FROM**
```makefile
# Run tests
test:
	pytest
```
**TO**
```makefile
# repo-name — developer workflow orchestration.
# Requires: GNU Make ≥ 4.0, bash.

...

test: ## Run the test suite.
	$(PYTHON) -m pytest
```

**REASON** `## description` feeds `make help`; the what-comment
restates the recipe. Header names the environment requirements so
a contributor with an ancient `make` fails fast instead of running
into mysterious parse errors.

---

## Tier-3 — Cross-Entity Collision

### Signal: `collision — SHELL/SHELLFLAGS divergence, duplicated .PHONY, or duplicated \`help\``

**CHANGE** Move the canonical definition (`SHELL`, `.SHELLFLAGS`,
`help`) to the top-level Makefile. Keep included `*.mk` files
scoped to their lifecycle section — `.PHONY` additions are
fine, re-defining `SHELL` is not.

**FROM** `mk/test.mk` with `SHELL := /bin/sh` (overrides the
top-level `SHELL := bash`).
**TO** Remove the `SHELL` line from `mk/test.mk`; inherit from
`Makefile`.

**REASON** Included files inherit the top-level configuration. A
`mk/test.mk` that resets `SHELL` silently breaks pipelines that
depend on bash features.

---

## Notes

- **HINT-severity findings** are pre-filter context, not repair
  targets. They inform the Tier-2 prompt and do not enter the
  repair queue.
- **Per-finding confirmation** is non-negotiable. Bulk application
  removes the user's ability to review individual changes.
- **Re-run after each fix.** A repair can introduce a new finding
  elsewhere (e.g., adding `SHELL := bash` may surface bashisms the
  previous `/bin/sh` silently tolerated).
- **Missing `checkmake` INFO is not a repair target.** Install with
  `brew install checkmake` (macOS) or `go install
  github.com/mrtazz/checkmake@latest` and re-run the audit.
