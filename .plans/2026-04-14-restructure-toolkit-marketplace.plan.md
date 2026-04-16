---
name: Restructure wos into toolkit marketplace
description: Split the wos monorepo into a Claude Code plugin marketplace with 5 self-contained plugins — build, check, wiki, work, consider
type: plan
status: completed
branch: restructure/toolkit-marketplace
related: []
---

# Goal

Restructure the `wos` repo into a Claude Code plugin marketplace named `toolkit`
(`github.com/bcbeidel/toolkit`), containing 5 self-contained, independently installable
plugins under a `tools/` directory. Each plugin owns its Python code, scripts, skills,
and tests.

# Scope

## Must Have
- `tools/` marketplace container with 5 plugin subdirectories
- Each plugin has a valid `.claude-plugin/plugin.json`
- `marketplace.json` at repo root
- `wiki` and `check` plugins have self-contained Python packages
- All 21 skills migrated to new plugins with new names
- 16 `consider` commands converted to `consider` plugin skills
- `_shared/references/` distributed to owning plugins
- Tests migrated and passing against new package structure
- CI updated for new structure
- Root `pyproject.toml` retained for dev tooling only

## Won't Have
- GitHub repo rename (manual step, post-merge)
- `_index.md` files (removed from repo; library no longer generates them)
- New skills or features
- Skill content changes beyond the pre-requisite fix already applied: removing 5 cross-plugin `_shared/references/` entries from `start-work` frontmatter (done prior to plan execution)
- `distill` skill (deleted; replaced by `ingest`)
- Plugin marketplace publishing or registration
- Version bumps beyond `0.1.0` for new plugins

# Approach

Work proceeds in 4 sequential chunks. Each chunk ends with a commit creating a
rollback boundary. The old structure (`wos/`, `skills/`, `commands/`, `scripts/`)
is removed only in Chunk 4, after all content is confirmed migrated.

**Python ownership:**
- `tools/wiki/wiki/` — document.py, agents_md.py, plan.py, project.py, research.py, skill_chain.py, url_checker.py, wiki.py
- `tools/check/check/` — skill.py, document.py, url_checker.py (document.py and url_checker.py duplicated from wiki; accepted — check must be standalone for build tooling)
- `tools/build/`, `tools/work/`, `tools/consider/` — pure skills, no Python

**Script path convention:** scripts in `tools/<plugin>/scripts/` use
`Path(__file__).parent.parent` (2 levels up) to find plugin root. No marker-based
walk-up, no `CLAUDE_PLUGIN_ROOT` required for path discovery.

**Skill rename map:**

| Old skill | New plugin | New skill name |
|-----------|-----------|----------------|
| `build-skill` | `build` | `build:skill` |
| `build-rule` | `build` | `build:rule` |
| `build-hook` | `build` | `build:hook` |
| `build-subagent` | `build` | `build:subagent` |
| `refine-prompt` | `build` | `build:refine-prompt` |
| `check-skill` | `check` | `check:skill` |
| `check-rule` | `check` | `check:rule` |
| `check-hook` | `check` | `check:hook` |
| `check-subagent` | `check` | `check:subagent` |
| `check-skill-chain` | `check` | `check:skill-chain` |
| `setup` | `wiki` | `wiki:setup` |
| `research` | `wiki` | `wiki:research` |
| `ingest` | `wiki` | `wiki:ingest` |
| `lint` | `wiki` | `wiki:lint` |
| `scope-work` | `work` | `work:scope` |
| `plan-work` | `work` | `work:plan` |
| `start-work` | `work` | `work:start` |
| `check-work` | `work` | `work:verify` |
| `finish-work` | `work` | `work:finish` |
| `audit` | `work` | `work:audit` |
| `retrospective` | `work` | `work:retro` |
| `commands/consider/*` | `consider` | `consider:<name>` |

**`_shared/references/` distribution:**

| Source | Destination |
|--------|-------------|
| `research/*` | `tools/wiki/skills/research/references/` |
| `plan-format.md`, `feedback-loop.md` | `tools/work/_shared/references/` |
| `primitive-routing.md` | `tools/build/_shared/references/` |

Note: if `feedback-loop.md` is referenced by `build` or `check` skills, duplicate it
into `tools/build/_shared/references/` as well. Verify during execution by grepping
each SKILL.md for the reference path.

# File Changes

## Created
- `tools/build/.claude-plugin/plugin.json`
- `tools/check/.claude-plugin/plugin.json`
- `tools/wiki/.claude-plugin/plugin.json`
- `tools/work/.claude-plugin/plugin.json`
- `tools/consider/.claude-plugin/plugin.json`
- `marketplace.json`
- `tools/wiki/pyproject.toml`
- `tools/check/pyproject.toml`
- `tools/wiki/wiki/` (Python package — 8 modules from `wos/`: document.py, agents_md.py, plan.py, project.py, research.py, skill_chain.py, url_checker.py, wiki.py)
- `tools/check/check/` (Python package — `skill.py`, `document.py`, `url_checker.py`; latter two duplicated from wiki)
- `tools/wiki/scripts/` (4 scripts: lint.py, update_preferences.py, check_url.py, _bootstrap.py)
- `tools/build/skills/` (5 skill directories)
- `tools/check/skills/` (5 skill directories)
- `tools/wiki/skills/` (4 skill directories — no distill)
- `tools/work/skills/` (7 skill directories)
- `tools/consider/skills/` (17 skill directories — 16 models + meta)
- `tools/wiki/tests/` (wiki module tests)
- `tools/check/tests/` (check module tests)
- `conftest.py` (root sys.path setup for cross-plugin test discovery)

## Modified
- `pyproject.toml` (dev deps only; update testpaths and ruff paths)
- `.github/workflows/ci.yml` (install both plugin packages; lint `tools/`)
- `CLAUDE.md` (new architecture and marketplace structure)
- `AGENTS.md` (updated navigation)
- `README.md` (install instructions)

## Deleted
- `wos/` (entire Python package)
- `skills/` (entire directory)
- `commands/` (entire directory)
- `scripts/` (entire directory)
- `tests/` (root-level, after migration to plugin test dirs)

# Tasks

## Chunk 1: Scaffold Marketplace Structure

- [x] Create `tools/` with 5 plugin subdirectories (`build`, `check`, `wiki`, `work`,
  `consider`), each containing a `.claude-plugin/` folder. No content yet.
  Verify: `ls tools/` outputs `build check consider wiki work`
  Commit: `chore: create tools/ marketplace directory skeleton` <!-- sha:300e013 -->

- [x] Write `.claude-plugin/plugin.json` for each of the 5 plugins. Fields: `name`
  (matching directory), `version` (`0.1.0`), `description` (one sentence), `author`
  (`{"name": "Brandon Beidel"}`). Use the agreed names: `build`, `check`, `wiki`,
  `work`, `consider`.
  Verify: `python -c "import json; [json.load(open(f'tools/{p}/.claude-plugin/plugin.json')) for p in ['build','check','wiki','work','consider']]; print('ok')"` exits 0
  Commit: `chore: add plugin.json manifests for all 5 plugins` <!-- sha:300e013 -->

- [x] Write `marketplace.json` — spec requires `.claude-plugin/marketplace.json` (not repo
  root). Updated existing `.claude-plugin/marketplace.json` to 5-plugin toolkit structure
  with `source` field (spec uses `source`, not `path`). `recommended` groupings included.
  Verify: `python -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('ok')"` exits 0
  Commit: `chore: update marketplace.json to toolkit 5-plugin structure` <!-- sha:fef851d -->

- [x] Create `tools/wiki/pyproject.toml` (package name `wiki`) and
  `tools/check/pyproject.toml` (package name `check`). Both: Python `>=3.9`,
  no runtime dependencies, setuptools build backend.
  Verify: `pip install -e tools/wiki -e tools/check` exits 0
  Commit: `chore: add per-plugin pyproject.toml for wiki and check` <!-- sha:beab4b6 -->

- [x] Update root `pyproject.toml`: remove the `wos` package declaration and
  `[tool.setuptools.packages.find]` section. Rename `[project] name` from `wos` to
  `toolkit` (the root is now a dev-deps meta-package, not the `wos` library). Keep
  `[project.optional-dependencies].dev` with pytest and ruff. Update
  `[tool.pytest.ini_options].testpaths` to `["tools/wiki/tests", "tools/check/tests"]`.
  Update `[tool.ruff]` paths in CI (not in pyproject, but note for CI task).
  Verify: `pip install -e ".[dev]"` exits 0
  Commit: `chore: update root pyproject.toml to dev-deps only toolkit meta-package` <!-- sha:a6a8989 -->

## Chunk 2: Split Python Packages

- [x] Create `tools/wiki/wiki/` package. Copy from `wos/` all modules except
  `skill.py`: `document.py`, `agents_md.py`, `plan.py`, `project.py`, `research.py`,
  `skill_chain.py`, `url_checker.py`, `wiki.py`, `__init__.py`. No subdirectories.
  Update all internal imports: `from wos.` → `from wiki.`, `import wos.` → `import wiki.`.
  Verify: `python -c "from wiki.document import Document; print('ok')"` exits 0
  Commit: `feat: create wiki Python package from wos modules` <!-- sha:b669e1f -->

- [x] Create `tools/check/check/` package with `skill.py`, `document.py`,
  `url_checker.py` (all copied from `wos/`). `document.py` and `url_checker.py` are
  intentional duplicates — check must be standalone for build tooling. Update all
  internal imports: `from wos.` → `from check.`.
  Verify: `python -c "from check.skill import check_skill_sizes; print('ok')"` exits 0
  Commit: `feat: create check Python package` <!-- sha:5ec1e7e -->

- [x] Migrate `scripts/` to `tools/wiki/scripts/`. Updated `from wos.` imports → `from wiki.`
  (and `from check.` for skill imports). `_bootstrap.py` updated with new path chain comment.
  lint.py patched: `from wiki.skill` → `from check.skill` (skill.py lives in check).
  Verify: `python tools/wiki/scripts/lint.py --help` exits 0
  Commit: `feat: migrate scripts to tools/wiki/scripts with updated imports` <!-- sha:9e39cd9 -->

## Chunk 3: Migrate Skills and Commands

- [x] Migrate `build` skills. Updated `../_shared/references/` → `../../_shared/references/`
  in SKILL.md files (moved down one dir level). Primitive-routing.md copied to
  `tools/build/_shared/references/`. No wos. imports found in build scripts.
  Fixed .gitignore — added `!tools/build/` to negate `build/` exclusion.
  Verify: `ls tools/build/skills/` shows `hook  refine-prompt  rule  skill  subagent`
  Commit: `feat: migrate build skills to tools/build` <!-- sha:60ad364 -->

- [x] Migrate `check` skills. No path or import updates needed.
  Verify: `ls tools/check/skills/` shows `hook  rule  skill  skill-chain  subagent`
  Commit: `feat: migrate check skills to tools/check` <!-- sha:f8dcbee -->

- [x] Migrate `wiki` skills. research/references/ populated from _shared/references/research/*.
  SKILL.md paths updated from `../_shared/references/research/` → `references/` (local).
  research_assess.py: removed wos. import, updated path comment, fixed docstring paths.
  Verify: `ls tools/wiki/skills/` shows `ingest  lint  research  setup`
  Commit: `feat: migrate wiki skills to tools/wiki` <!-- sha:bd62889 -->

- [x] Migrate `work` skills. plan-format.md and feedback-loop.md copied to work/_shared/references/.
  SKILL.md paths: `../_shared/references/` → `../../_shared/references/`. plan_assess.py:
  removed sys.path block (work has no Python package; editable install is the contract),
  updated `from wos.plan` → `from wiki.plan`, fixed docstring paths.
  Verify: `ls tools/work/skills/` shows `audit  finish  plan  retro  scope  start  verify`
  Commit: `feat: migrate work skills to tools/work` <!-- sha:d72ea25 -->

- [x] Convert `commands/consider/` to `consider` plugin. All 16 commands + meta converted.
  Verify: `ls tools/consider/skills/ | wc -l` outputs `17`
  Commit: `feat: convert consider commands to tools/consider plugin` <!-- sha:0f4a871 -->

## Chunk 4: Tests, CI, Docs, Cleanup

- [x] Migrate tests. test_deploy.py removed (deploy.py not migrated). test_version.py
  rewritten for single-plugin version check (wiki pyproject.toml vs plugin.json).
  test_url_checker.py: @patch targets updated from wos.url_checker → wiki.url_checker.
  test_lint.py: mock patch targets updated wos. → wiki. conftest.py updated to add
  tools/wiki/ to sys.path for namespace package import (from scripts.lint import main).
  test_plan_assess.py: uses wiki.plan (not check.plan — plan lives in wiki). Research
  fixtures: copied directly after initial cp -r missed them.
  Verify: `python -m pytest tools/wiki/tests/ tools/check/tests/ -v` — 290 passed
  Commit: `test: migrate test suite to per-plugin directories` <!-- sha:769101f -->

- [x] Update `.github/workflows/ci.yml`. Changed install, ruff, and pytest steps.
  Also updated .git/hooks/pre-commit to `ruff check tools/` (was checking old dirs).
  Verify: CI YAML parses without error
  Commit: `ci: update workflow for toolkit marketplace structure` <!-- sha:ddf775c -->

- [x] Update `CLAUDE.md`. Rewritten for toolkit marketplace structure. All wos/ refs removed.
  Verify: `grep -c "wos/" CLAUDE.md` outputs `0`
  Commit: `docs: update CLAUDE.md for toolkit marketplace structure` <!-- sha:abc730b -->

- [x] Update `AGENTS.md` navigation and `README.md`. Plugin table added to AGENTS.md.
  README rewritten with marketplace overview and install groupings.
  Verify: `grep -c "wos/" AGENTS.md README.md` outputs `0`
  Commit: `docs: update AGENTS.md and README for toolkit structure` <!-- sha:3ee3294 -->

- [x] Remove legacy directories: `wos/`, `skills/`, `commands/`, `scripts/`, `tests/`.
  Verified no dangling references before deletion. Also fixed pre-commit hook.
  Added ruff exclude for build eval-viewer/scripts (pre-existing style issues, never linted).
  Verify: `ls` at repo root does not show `wos skills commands scripts tests`
  Commit: `chore: remove legacy wos/ skills/ commands/ scripts/ directories` <!-- sha:601a27c -->

- [x] Orphan review completed. All checks passed:
  - No `wos.` imports in tools/
  - `skills/` reference in CLAUDE.md:68 is correct (describes plugin dir layout)
  - Python files in tools/build/skills/skill/ are expected eval tooling
  - No Python at repo root
  Commit: included in previous commit (no separate changes needed)

# Validation

1. **All 5 plugins load:**
   `claude --plugin-dir tools/build --plugin-dir tools/check --plugin-dir tools/wiki --plugin-dir tools/work --plugin-dir tools/consider`
   Expected: no manifest errors reported

2. **Python packages install:**
   `pip install -e tools/wiki -e tools/check`
   Expected: exit 0

3. **Test suite passes:**
   `python -m pytest tools/wiki/tests/ tools/check/tests/ -v`
   Expected: all green

4. **Lint clean:**
   `ruff check tools/`
   Expected: no errors

5. **No legacy imports:**
   `grep -r "from wos\." tools/`
   Expected: no output

6. **Marketplace JSON valid:**
   `python -c "import json; json.load(open('marketplace.json')); print('ok')"`
   Expected: `ok`

7. **Manual post-merge:** rename GitHub repo `wos` → `toolkit` at
   github.com/bcbeidel/wos → Settings → Repository name
