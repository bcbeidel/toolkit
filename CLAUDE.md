@AGENTS.md

# CLAUDE.md

This repo is **wos** — a Claude Code plugin for building and maintaining
structured project context. You are helping build this tooling.

## What This Repo Is

WOS is a plugin (not a project context itself). It provides skills, scripts,
and agents that help users create, validate, and maintain structured context in
their own repos. When working in this repo, you are building the tool, not
using it.

## Build & Test

Always use the project venv Python: `.venv/bin/python`

```bash
python -m pytest tests/ -v
```

Lint:
```bash
ruff check wos/ tests/ scripts/
```

No runtime dependencies (stdlib only). Dev dependencies in `pyproject.toml`.

Note: `ruff` may not be installed locally; CI runs it via GitHub Actions.

Versioning policy and version bump process: see [CONTRIBUTING.md](CONTRIBUTING.md)

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

### Package Structure

- `wos/` — importable Python package
  - `frontmatter.py` — custom YAML subset parser (stdlib-only)
  - `document.py` — `Document` base class + subclasses + `parse_document()` factory
  - `discovery.py` — document discovery via project tree walking (.gitignore-aware)
  - `suffix.py` — compound suffix extraction (`type_from_path`)
  - `index.py` — `_index.md` generation + sync checking (preamble-preserving)
  - `validators.py` — project-wide orchestration (`validate_project()`); index and project-file checks
  - `skill_audit.py` — skill instruction density measurement (line counting, size thresholds)
  - `url_checker.py` — HTTP HEAD/GET URL reachability (urllib)
  - `agents_md.py` — marker-based AGENTS.md section management + `replace_marker_section()`
  - `preferences.py` — communication preferences dimensions and rendering
  - `wiki.py` — `WikiDocument` subclass + schema parsing + directory-level orphan checks
  - `chain.py` — `ChainDocument` subclass + step table parsing + structural validation
  - `research/` — research skill support (`assess_research.py` — thin wrapper over `ResearchDocument`)
  - `plan/` — plan skill support (`assess_plan.py` — thin wrapper over `PlanDocument`)
- `scripts/` — thin CLI entry points with argparse and PEP 723 inline metadata
  - `lint.py` — run validation checks (`--root`, `--no-urls`, `--json`, `--fix`, `--strict`, `--context-min-words`, `--context-max-words`, `--skill-max-lines`)
  - `reindex.py` — regenerate all `_index.md` files (preamble-preserving)
  - `deploy.py` — export skills to `.agents/` for cross-platform deployment
  - `check_url.py` — URL reachability checking via `wos.url_checker`
  - `update_preferences.py` — write communication preferences to AGENTS.md
  - `get_version.py` — print plugin version from `plugin.json`
- `skills/` — skill definitions (SKILL.md + references/) auto-discovered by Claude Code
- `tests/` — pytest tests

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

### Navigation

Each directory under `docs/` has an auto-generated `_index.md`
listing files with descriptions from frontmatter. AGENTS.md contains a WOS-managed
section (between `<!-- wos:begin -->` / `<!-- wos:end -->` markers) with navigation
instructions, areas table, metadata format, and communication preferences.

### Skills

Prefix: `/wos:` (e.g., `/wos:setup`, `/wos:lint`). 13 skills + 1 command.
Full skill ecosystem, lifecycle diagram, and layer descriptions: [OVERVIEW.md](OVERVIEW.md)

### Validation

Validation is class-based. Each document class owns its checks via `issues(root)`.
`validators.py` is the project-wide orchestrator — it discovers documents, calls
`doc.issues(root)` on each, and runs directory-level checks (index sync, project files).

**Per-document checks (on the class):**
- `Document` — required frontmatter fields, related paths exist on disk
- `ResearchDocument` — sources required, source URLs reachable (403/429 → warn), no draft markers
- `PlanDocument` — plan-specific structural checks
- `ChainDocument` — termination condition, no cycles, declared skills exist
- `WikiDocument` — schema conformance (page_type, confidence_tier), required wiki frontmatter fields

**Project-level checks (in `validators.py`):**
- **Content length** (warn) — context files below 100 or exceeding 800 words (configurable)
- **Index sync** (fail + warn) — `_index.md` matches directory contents, preamble presence
- **Project files** (warn) — AGENTS.md/CLAUDE.md existence and configuration

**Skill quality** (in `skill_audit.py`) — name format/reserved words (fail), description length/XML/voice (warn), instruction line count (warn, default 500), ALL-CAPS directive density (warn, threshold 3)

### Key Entry Points

- `wos/document.py` — Document dataclass and `parse_document()`
- `wos/validators.py` — `validate_project()` runs all checks
- `wos/skill_audit.py` — `check_skill_sizes()` and `check_skill_meta()` for skill quality
- `wos/index.py` — `generate_index()` and `check_index_sync()`
- `scripts/lint.py` — CLI for validation
- `scripts/reindex.py` — CLI for index regeneration

## Reference

- Skill ecosystem: [WOS Overview](OVERVIEW.md)
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
- **Script invocation: `python` is the universal pattern.** All scripts in
  `scripts/` have PEP 723 inline metadata and stdlib-only dependencies.
  Skills invoke them via `python <plugin-scripts-dir>/script.py`. Dev
  Dev dependencies (pytest, ruff) install via `pip install -e ".[dev]"`.
- CLI scripts default to CWD as root; accept `--root` for override
- **Plugin root discovery (all scripts):** Scripts use a hybrid pattern to
  find the plugin root for `sys.path` insertion. Prefer `CLAUDE_PLUGIN_ROOT`
  env var (forward-compatible with Claude Code), fall back to `__file__`
  parent chain. Shared scripts in `scripts/` use `.parent.parent` (2 levels);
  per-skill scripts in `skills/<name>/scripts/` use `.parent` × depth to root.
  Each fallback line must include a comment documenting the path chain (e.g.,
  `# skills/research/scripts/ → skills/research/ → skills/ → plugin root`).
  Do NOT use marker-based walk-up (`pyproject.toml` search) — it finds the
  user's project root instead of the plugin root.
- `doc.issues(root)` returns `list[dict]` with keys: `file`, `issue`, `severity`; `doc.is_valid(root)` returns `bool`
- Skills use free-text intake — users describe intent, Claude routes
- `ValueError` + stdlib exceptions only (no custom exception hierarchy)
- Tests use inline markdown strings and `tmp_path` fixtures
