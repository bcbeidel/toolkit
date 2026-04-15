@AGENTS.md

# CLAUDE.md

This repo is **toolkit** — a Claude Code plugin marketplace for building and
maintaining structured project context. You are helping build this tooling.

## What This Repo Is

Toolkit is a plugin marketplace (not a project context itself). It provides 5
self-contained, independently installable plugins under `tools/`. Each plugin
owns its Python code, scripts, skills, and tests. When working in this repo,
you are building the tools, not using them.

## Build & Test

Install plugin packages and dev dependencies:

```bash
pip install -e tools/wiki -e tools/check -e ".[dev]"
```

Run tests:
```bash
python -m pytest tools/wiki/tests/ tools/check/tests/ -v
```

Lint:
```bash
ruff check tools/
```

No runtime dependencies (stdlib only). Dev dependencies in root `pyproject.toml`.

Note: `ruff` may not be installed locally; CI runs it via GitHub Actions.

## Design Principles

1. **Convention over configuration** — document patterns, don't enforce them
2. **Structure in code, quality in skills** — deterministic checks in Python or shell scripts, judgment in LLMs
3. **Single source of truth** — navigation is derived from disk, never hand-curated
4. **Keep it simple** — no frameworks, no unnecessary indirection. Inheritance is acceptable when a document type has distinct data or validation behavior that would otherwise scatter across unrelated modules.
5. **When in doubt, leave it out** — every field, abstraction, and feature must justify itself
6. **Omit needless words** — agent-facing output earns every token
7. **Depend on nothing** — stdlib-only core; scripts isolate their own deps
8. **One obvious way to run** — every script, every skill, same entry point
9. **Separate reads from writes** — audit observes; fixes require explicit action
10. **Bottom line up front** — key insights at top and bottom, detail in the middle

Full descriptions: [Design Principles](PRINCIPLES.md)

## Architecture

### Marketplace Structure

Five plugins under `tools/`, each independently installable:

| Plugin | Path | Python package | Skills |
|--------|------|----------------|--------|
| `build` | `tools/build/` | none | `skill`, `rule`, `hook`, `subagent`, `refine-prompt` |
| `check` | `tools/check/` | `check` | `skill`, `rule`, `hook`, `subagent`, `skill-chain` |
| `wiki` | `tools/wiki/` | `wiki` | `setup`, `research`, `ingest`, `lint` |
| `work` | `tools/work/` | none | `scope`, `plan`, `start`, `verify`, `finish`, `audit`, `retro` |
| `consider` | `tools/consider/` | none | 16 mental models + meta |

Each plugin directory contains:
- `.claude-plugin/plugin.json` — plugin manifest
- `skills/` — skill definitions (SKILL.md + references/)
- `<package>/` — Python package (wiki and check only)
- `scripts/` — shared CLI entry points (wiki only)
- `tests/` — pytest tests (wiki and check only)
- `_shared/references/` — references shared across skills in the same plugin

### Package Structure

**`tools/wiki/wiki/`** — importable Python package:
- `frontmatter.py` — custom YAML subset parser (stdlib-only)
- `document.py` — `Document` base class + subclasses + `parse_document()` factory
- `discovery.py` — document discovery via project tree walking (.gitignore-aware)
- `suffix.py` — compound suffix extraction (`type_from_path`)
- `index.py` — `_index.md` generation + sync checking (preamble-preserving)
- `validators.py` — project-wide orchestration (`validate_project()`); index and project-file checks
- `url_checker.py` — HTTP HEAD/GET URL reachability (urllib)
- `agents_md.py` — marker-based AGENTS.md section management + `replace_marker_section()`
- `preferences.py` — communication preferences dimensions and rendering
- `wiki.py` — `WikiDocument` subclass + schema parsing + directory-level orphan checks
- `skill_chain.py` — `ChainDocument` subclass + step table parsing + structural validation
- `research.py` — `ResearchDocument` subclass + source URL checks + gate checking
- `plan.py` — `PlanDocument` subclass + task parsing + completion tracking
- `project.py` — thin orchestration wrapper over validators

**`tools/check/check/`** — importable Python package (standalone for build tooling):
- `document.py` — duplicated from wiki (check must be standalone)
- `url_checker.py` — duplicated from wiki
- `skill.py` — `SkillDocument` + `check_skill_sizes()` + `check_skill_meta()`

**`tools/wiki/scripts/`** — thin CLI entry points with PEP 723 inline metadata:
- `lint.py` — run validation checks
- `check_url.py` — URL reachability checking
- `update_preferences.py` — write communication preferences to AGENTS.md
- `_bootstrap.py` — sys.path insertion helper (imported as side effect)

### Document Model

`Document` is the base class. Type-specific subclasses add structured data fields and
override `issues()` for type-specific validation. `parse_document()` is the single
factory — it routes to the right subclass based on frontmatter `type` and file suffix.

```
Document          — common fields + base validation (required frontmatter, related paths)
├── ResearchDocument  — source URL checks, draft marker check, sources required
├── PlanDocument      — tasks field (parsed from content), completion tracking
├── ChainDocument     — steps field (parsed from content), cycle/termination checks
└── WikiDocument      — schema conformance, wiki-specific frontmatter checks
```

Required frontmatter: `name`, `description`
Optional frontmatter: `type` (routes subclass selection), `sources`, `related`, `status`, plus extra fields in `meta`.

**Validation interface** — two methods on every class:
- `doc.issues(root) -> list[dict]` — full issue list, each with `file`, `issue`, `severity`
- `doc.is_valid(root) -> bool` — True if no `fail`-severity issues

Subclasses call `super().issues(root)` and extend. Type-specific checks live on the
subclass — never on the base class.

### Skills

Skill prefix follows plugin name (e.g., `/wiki:setup`, `/work:plan`, `/build:skill`).
Skills live at `tools/<plugin>/skills/<name>/SKILL.md`.

### Key Entry Points

- `tools/wiki/wiki/document.py` — Document dataclass and `parse_document()`
- `tools/wiki/wiki/validators.py` — `validate_project()` runs all checks
- `tools/check/check/skill.py` — `check_skill_sizes()` and `check_skill_meta()` for skill quality
- `tools/wiki/scripts/lint.py` — CLI for validation

## Reference

- Design principles: [WOS Design Principles](PRINCIPLES.md)

## Plans

- Plans MUST be detailed lists of individual tasks
- Plans MUST be stored as markdown in `/docs/plans`
- Plans MUST include checkboxes to indicate progress, marking things off as completed
- Plans MUST indicate the branch, and pull-request associated with the work
- Plans MUST be implemented on a branch, and merged only after human review of a pull-request

## Conventions

- Python 3.9 — use `from __future__ import annotations` for type hints,
  `Optional[X]` for runtime expressions
- **Script invocation: `python` is the universal pattern.** Scripts in
  `tools/wiki/scripts/` have PEP 723 inline metadata and stdlib-only dependencies.
  Skills invoke them via `python <plugin-scripts-dir>/script.py`. Dev
  dependencies (pytest, ruff) install via `pip install -e ".[dev]"`.
- CLI scripts default to CWD as root; accept `--root` for override
- **Script path convention:** Scripts use `Path(__file__).parent.parent` (2 levels)
  to find the plugin root. Per-skill scripts use the appropriate depth to reach
  their plugin root. Each `sys.path` insertion includes a comment with the full
  path chain (e.g., `# tools/wiki/scripts/ → tools/wiki/ (plugin root)`).
  Do NOT use marker-based walk-up (`pyproject.toml` search) — it finds the
  user's project root instead of the plugin root.
- **`work` and `build` scripts:** These plugins have no Python package. Their
  per-skill scripts rely on editable installs of `wiki` and `check`. Do not add
  sys.path manipulation to `work`/`build` scripts — the editable install is the contract.
- `doc.issues(root)` returns `list[dict]` with keys: `file`, `issue`, `severity`; `doc.is_valid(root)` returns `bool`
- Skills use free-text intake — users describe intent, Claude routes
- `ValueError` + stdlib exceptions only (no custom exception hierarchy)
- Tests use inline markdown strings and `tmp_path` fixtures
