---
name: Restructure wos into toolkit marketplace
description: Split the wos monorepo into a Claude Code plugin marketplace with 5 self-contained plugins — build, check, wiki, work, consider
type: plan
status: draft
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
- All 22 skills migrated to new plugins with new names
- 16 `consider` commands converted to `consider` plugin skills
- `_shared/references/` distributed to owning plugins
- Tests migrated and passing against new package structure
- CI updated for new structure
- Root `pyproject.toml` retained for dev tooling only

## Won't Have
- GitHub repo rename (manual step, post-merge)
- New skills or features
- Skill content changes beyond the pre-requisite fix already applied: removing 5 cross-plugin `_shared/references/` entries from `start-work` frontmatter and replacing the opaque reference-file pointer with explicit `wiki:research` and `wiki:distill` invocations (done prior to plan execution)
- Plugin marketplace publishing or registration
- Version bumps beyond `0.1.0` for new plugins

# Approach

Work proceeds in 4 sequential chunks. Each chunk ends with a commit creating a
rollback boundary. The old structure (`wos/`, `skills/`, `commands/`, `scripts/`)
is removed only in Chunk 4, after all content is confirmed migrated.

**Python ownership:**
- `tools/wiki/wiki/` — document model, validators, index, discovery, research/, plan/, url_checker
- `tools/check/check/` — skill_audit, url_checker (duplicated from wiki; accepted)
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
| `distill` | `wiki` | `wiki:distill` |
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
| `distill/*` | `tools/wiki/skills/distill/references/` |
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
- `tools/wiki/wiki/` (Python package, ~14 modules from `wos/`)
- `tools/check/check/` (Python package — `skill_audit.py` + `url_checker.py`)
- `tools/wiki/scripts/` (6 scripts, updated imports)
- `tools/build/skills/` (5 skill directories)
- `tools/check/skills/` (5 skill directories)
- `tools/wiki/skills/` (5 skill directories)
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

- [ ] Create `tools/` with 5 plugin subdirectories (`build`, `check`, `wiki`, `work`,
  `consider`), each containing a `.claude-plugin/` folder. No content yet.
  Verify: `ls tools/` outputs `build check consider wiki work`
  Commit: `chore: create tools/ marketplace directory skeleton`

- [ ] Write `.claude-plugin/plugin.json` for each of the 5 plugins. Fields: `name`
  (matching directory), `version` (`0.1.0`), `description` (one sentence), `author`
  (`{"name": "Brandon Beidel"}`). Use the agreed names: `build`, `check`, `wiki`,
  `work`, `consider`.
  Verify: `python -c "import json; [json.load(open(f'tools/{p}/.claude-plugin/plugin.json')) for p in ['build','check','wiki','work','consider']]; print('ok')"` exits 0
  Commit: `chore: add plugin.json manifests for all 5 plugins`

- [ ] Write `marketplace.json` at repo root. List all 5 plugins with `name`,
  `description`, `path` (e.g. `./tools/build`), and a top-level `recommended`
  object documenting common install groupings (knowledge, build-tooling, full-suite).
  Verify: `python -c "import json; json.load(open('marketplace.json')); print('ok')"` exits 0
  Commit: `chore: add marketplace.json`

- [ ] Create `tools/wiki/pyproject.toml` (package name `wiki`) and
  `tools/check/pyproject.toml` (package name `check`). Both: Python `>=3.9`,
  no runtime dependencies, setuptools build backend.
  Verify: `pip install -e tools/wiki -e tools/check` exits 0
  Commit: `chore: add per-plugin pyproject.toml for wiki and check`

- [ ] Update root `pyproject.toml`: remove the `wos` package declaration and
  `[tool.setuptools.packages.find]` section. Keep `[project.optional-dependencies].dev`
  with pytest and ruff. Update `[tool.pytest.ini_options].testpaths` to
  `["tools/wiki/tests", "tools/check/tests"]`. Update `[tool.ruff]` paths in CI
  (not in pyproject, but note for CI task).
  Verify: `pip install -e ".[dev]"` exits 0
  Commit: `chore: update root pyproject.toml to dev-deps only`

## Chunk 2: Split Python Packages

- [ ] Create `tools/wiki/wiki/` package. Copy from `wos/` all modules except
  `skill_audit.py`: `document.py`, `frontmatter.py`, `discovery.py`, `index.py`,
  `validators.py`, `agents_md.py`, `markers.py`, `preferences.py`,
  `research_protocol.py`, `wiki.py`, `chain.py`, `suffix.py`, `url_checker.py`,
  `__init__.py`. Copy subdirs `wos/research/` → `tools/wiki/wiki/research/` and
  `wos/plan/` → `tools/wiki/wiki/plan/`. Update all internal imports: `from wos.`
  → `from wiki.`, `import wos.` → `import wiki.`.
  Verify: `cd tools/wiki && python -c "from wiki.document import Document; print('ok')"` exits 0
  Commit: `feat: create wiki Python package from wos modules`

- [ ] Create `tools/check/check/` package with `__init__.py`, `skill_audit.py`
  (copied from `wos/`), and `url_checker.py` (copied from `wos/`). Update imports.
  Verify: `cd tools/check && python -c "from check.skill_audit import check_skill_sizes; print('ok')"` exits 0
  Commit: `feat: create check Python package`

- [ ] Migrate `scripts/` to `tools/wiki/scripts/`. For each script, update:
  (1) `sys.path` insertion to use `Path(__file__).parent.parent` (plugin root = `tools/wiki/`),
  (2) all `from wos.` imports → `from wiki.`, (3) remove any `CLAUDE_PLUGIN_ROOT`
  walk-up logic. Migrate: `lint.py`, `reindex.py`, `update_preferences.py`,
  `get_version.py`, `deploy.py`, `check_url.py`. Update `get_version.py` to read
  from `tools/wiki/.claude-plugin/plugin.json` (or root `marketplace.json`).
  Verify: `python tools/wiki/scripts/get_version.py` prints a version string without error
  Commit: `feat: migrate scripts to tools/wiki/scripts with updated imports`

## Chunk 3: Migrate Skills and Commands

- [ ] Migrate `build` skills. Move directories:
  `skills/build-skill/ → tools/build/skills/skill/`,
  `skills/build-rule/ → tools/build/skills/rule/`,
  `skills/build-hook/ → tools/build/skills/hook/`,
  `skills/build-subagent/ → tools/build/skills/subagent/`,
  `skills/refine-prompt/ → tools/build/skills/refine-prompt/`.
  Move `skills/build-skill/scripts/` → `tools/build/skills/skill/scripts/`.
  Move `_shared/references/primitive-routing.md` → `tools/build/_shared/references/`.
  In each SKILL.md, update `${CLAUDE_PLUGIN_ROOT}` paths to reflect new plugin root.
  If any SKILL.md references `_shared/references/feedback-loop.md`, copy that file
  to `tools/build/_shared/references/` as well.
  Verify: `ls tools/build/skills/` shows `hook  refine-prompt  rule  skill  subagent`
  Commit: `feat: migrate build skills to tools/build`

- [ ] Migrate `check` skills. Move directories:
  `skills/check-skill/ → tools/check/skills/skill/`,
  `skills/check-rule/ → tools/check/skills/rule/`,
  `skills/check-hook/ → tools/check/skills/hook/`,
  `skills/check-subagent/ → tools/check/skills/subagent/`,
  `skills/check-skill-chain/ → tools/check/skills/skill-chain/`.
  Update `${CLAUDE_PLUGIN_ROOT}` paths in each SKILL.md.
  Verify: `ls tools/check/skills/` shows `hook  rule  skill  skill-chain  subagent`
  Commit: `feat: migrate check skills to tools/check`

- [ ] Migrate `wiki` skills. Move directories:
  `skills/setup/ → tools/wiki/skills/setup/`,
  `skills/research/ → tools/wiki/skills/research/`,
  `skills/ingest/ → tools/wiki/skills/ingest/`,
  `skills/distill/ → tools/wiki/skills/distill/`,
  `skills/lint/ → tools/wiki/skills/lint/`.
  Move `skills/research/scripts/` → `tools/wiki/skills/research/scripts/`.
  Move `_shared/references/research/*` → `tools/wiki/skills/research/references/`.
  Move `_shared/references/distill/*` → `tools/wiki/skills/distill/references/`.
  Update all `${CLAUDE_PLUGIN_ROOT}` script paths in SKILL.md files.
  Verify: `ls tools/wiki/skills/` shows `distill  ingest  lint  research  setup`
  Commit: `feat: migrate wiki skills to tools/wiki`

- [ ] Migrate `work` skills. Move directories:
  `skills/scope-work/ → tools/work/skills/scope/`,
  `skills/plan-work/ → tools/work/skills/plan/`,
  `skills/start-work/ → tools/work/skills/start/`,
  `skills/check-work/ → tools/work/skills/verify/`,
  `skills/finish-work/ → tools/work/skills/finish/`,
  `skills/audit/ → tools/work/skills/audit/`,
  `skills/retrospective/ → tools/work/skills/retro/`.
  Move `skills/start-work/scripts/plan_assess.py` → `tools/work/skills/start/scripts/`.
  Move `_shared/references/plan-format.md` and `feedback-loop.md` →
  `tools/work/_shared/references/`.
  Update all `${CLAUDE_PLUGIN_ROOT}` paths in SKILL.md files.
  Verify: `ls tools/work/skills/` shows `audit  finish  plan  retro  scope  start  verify`
  Commit: `feat: migrate work skills to tools/work`

- [ ] Convert `commands/consider/` to `consider` plugin. For each of the 16 files in
  `commands/consider/<name>.md`, create `tools/consider/skills/<name>/SKILL.md`
  with the file content as the skill body. Convert `commands/consider.md` to
  `tools/consider/skills/consider/SKILL.md` as the meta entry point. No Python needed.
  Verify: `ls tools/consider/skills/ | wc -l` outputs `17`
  Commit: `feat: convert consider commands to tools/consider plugin`

## Chunk 4: Tests, CI, Docs, Cleanup

- [ ] Migrate tests. Copy wiki-related tests to `tools/wiki/tests/`:
  `test_document.py`, `test_frontmatter.py`, `test_discovery.py`, `test_index.py`,
  `test_validators.py`, `test_agents_md.py`, `test_markers.py`, `test_preferences.py`,
  `test_research_protocol.py`, `test_wiki.py`, `test_chain.py`, `test_suffix.py`,
  `test_lint.py`, `test_update_preferences.py`, `test_deploy.py`, `test_check_url.py`,
  `test_url_checker.py`, `test_research_assess.py`, `test_research_gates.py`,
  `test_get_version.py`, `test_version.py`, `test_script_syspath.py`.
  Copy check-related tests to `tools/check/tests/`: `test_skill_audit.py`,
  `test_plan_assess.py`. Update all imports `from wos.` → `from wiki.`/`from check.`.
  Write root `conftest.py` that inserts `tools/wiki` and `tools/check` into `sys.path`.
  Verify: `python -m pytest tools/wiki/tests/ tools/check/tests/ -v` passes
  Commit: `test: migrate test suite to per-plugin directories`

- [ ] Update `.github/workflows/ci.yml`. Change install step:
  `pip install -e tools/wiki -e tools/check -e ".[dev]"`. Change ruff step:
  `ruff check tools/`. Change pytest step:
  `python -m pytest tools/wiki/tests/ tools/check/tests/ -v`.
  Verify: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` parses without error (install pyyaml if needed, or review manually)
  Commit: `ci: update workflow for toolkit marketplace structure`

- [ ] Update `CLAUDE.md`. Replace the Architecture section with the new marketplace
  structure (5 plugins, per-plugin packages). Update Package Structure listing to
  describe `tools/<plugin>/<package>/` pattern. Update Script invocation convention
  to `Path(__file__).parent.parent` (2-level). Update Build & Test commands to
  `pip install -e tools/wiki -e tools/check -e ".[dev]"`. Remove all `wos/` references.
  Verify: `grep -c "wos/" CLAUDE.md` outputs `0`
  Commit: `docs: update CLAUDE.md for toolkit marketplace structure`

- [ ] Update `AGENTS.md` navigation: revise areas table and any `wos/`-specific
  references to reflect `tools/` structure. Update `README.md`: add marketplace
  overview, per-plugin install commands, recommended groupings (knowledge, tooling,
  full suite). Include manual repo rename note.
  Verify: `grep -c "wos/" AGENTS.md README.md` outputs `0`
  Commit: `docs: update AGENTS.md and README for toolkit structure`

- [ ] Remove legacy directories: `wos/`, `skills/`, `commands/`, `scripts/`, `tests/`.
  Before deletion, verify no dangling references:
  `grep -r "from wos\." tools/ .github/ CLAUDE.md` returns no matches.
  `grep -r "skills/" CLAUDE.md AGENTS.md` returns no unexpected matches.
  Then: `rm -rf wos/ skills/ commands/ scripts/ tests/`
  Verify: `ls` at repo root does not show `wos skills commands scripts tests`
  Commit: `chore: remove legacy wos/ skills/ commands/ scripts/ directories`

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
