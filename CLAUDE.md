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

```bash
uv run python -m pytest tests/ -v
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
2. **Structure in code, quality in skills** — deterministic checks in Python, judgment in LLMs
3. **Single source of truth** — navigation is derived from disk, never hand-curated
4. **Keep it simple** — no hierarchies, no frameworks, no indirection
5. **When in doubt, leave it out** — every field, abstraction, and feature must justify itself
6. **Omit needless words** — agent-facing output earns every token
7. **Depend on nothing** — stdlib-only core; scripts isolate their own deps
8. **One obvious way to run** — every script, every skill, same entry point
9. **Separate reads from writes** — audit observes; fixes require explicit action
10. **Bottom line up front** — key insights at top and bottom, detail in the middle

Full descriptions: [Design Principles](PRINCIPLES.md)

## Architecture

### Package Structure

- `wos/` — importable Python package (10 modules + 2 subpackages)
  - `frontmatter.py` — custom YAML subset parser (stdlib-only)
  - `document.py` — `Document` dataclass + `parse_document()`
  - `index.py` — `_index.md` generation + sync checking (preamble-preserving)
  - `validators.py` — 5 validation checks with warn/fail severity (frontmatter, content length, URLs, related paths, index sync)
  - `skill_audit.py` — skill instruction density measurement (line counting, size thresholds)
  - `url_checker.py` — HTTP HEAD/GET URL reachability (urllib)
  - `agents_md.py` — marker-based AGENTS.md section management
  - `markers.py` — shared marker-based section replacement
  - `preferences.py` — communication preferences dimensions and rendering
  - `research_protocol.py` — search protocol logging (`SearchEntry`, `SearchProtocol`, formatters)
  - `research/` — research skill support (`assess_research.py` — research document assessment)
  - `plan/` — plan skill support (`assess_plan.py` — plan document structural assessment)
- `scripts/` — thin CLI entry points with argparse and PEP 723 inline metadata
  - `audit.py` — run validation checks (`--root`, `--no-urls`, `--json`, `--fix`, `--strict`, `--context-min-words`, `--context-max-words`, `--skill-max-lines`)
  - `reindex.py` — regenerate all `_index.md` files (preamble-preserving)
  - `check_runtime.py` — canary script to validate `uv run` + PEP 723 pipeline
  - `check_url.py` — URL reachability checking via `wos.url_checker`
  - `update_preferences.py` — write communication preferences to AGENTS.md
  - `get_version.py` — print plugin version from `plugin.json`
- `skills/` — skill definitions (SKILL.md + references/) auto-discovered by Claude Code
- `tests/` — pytest tests

### Document Model

One `Document` dataclass. No subclasses, no inheritance.

Required frontmatter: `name`, `description`
Optional frontmatter: `type` (semantic tag), `sources` (URLs), `related` (file paths), plus any extra fields.

`type: research` triggers source requirements (sources must be non-empty, URLs verified).

### Navigation

Each directory under `docs/` has an auto-generated `_index.md`
listing files with descriptions from frontmatter. AGENTS.md contains a WOS-managed
section (between `<!-- wos:begin -->` / `<!-- wos:end -->` markers) with navigation
instructions, areas table, metadata format, and communication preferences.

### Skills

Prefix: `/wos:` (e.g., `/wos:init`, `/wos:audit`). 13 skills + 1 command.
Full skill ecosystem, lifecycle diagram, and layer descriptions: [OVERVIEW.md](OVERVIEW.md)

### Validation (8 checks, warn/fail severity)

1. **Frontmatter** (fail + warn) — `name`/`description` non-empty, research sources, dict source warnings, context `related` field warnings
2. **Content length** (warn) — context files below 100 or exceeding 800 words (configurable)
3. **Draft markers** (warn) — research documents containing `<!-- DRAFT -->` markers
4. **Source URLs** (fail + warn) — URLs in `sources` reachable; 403/429 downgraded to `warn`
5. **Related paths** (fail) — file paths in `related` frontmatter exist on disk
6. **Index sync** (fail + warn) — `_index.md` matches directory contents, preamble presence
7. **Project files** (warn) — AGENTS.md/CLAUDE.md existence and configuration
8. **Skill quality** (fail + warn) — skill name format/reserved words (fail), description length/XML/voice (warn), instruction lines exceeding threshold (warn, default 500, configurable), SKILL.md body exceeding 500 lines (warn), ALL-CAPS directive density (warn, threshold 3)

### Key Entry Points

- `wos/document.py` — Document dataclass and `parse_document()`
- `wos/validators.py` — `validate_project()` runs all checks
- `wos/skill_audit.py` — `check_skill_sizes()` and `check_skill_meta()` for skill quality
- `wos/index.py` — `generate_index()` and `check_index_sync()`
- `scripts/audit.py` — CLI for validation
- `scripts/reindex.py` — CLI for index regeneration

## Reference

- Skill ecosystem: [WOS Overview](OVERVIEW.md)
- Architecture: [WOS Architecture Reference](docs/plans/2026-02-27-architecture-reference.md)
- Design principles: [WOS Design Principles](PRINCIPLES.md)
- Simplification history: [Simplification Design](docs/plans/2026-02-22-simplification-design.md)

## Plans

- Plans MUST be detailed lists of individual tasks
- Plans MUST be stored as markdown in `/docs/plans`
- Plans MUST include checkboxes to indicate progress, marking things off as completed
- Plans MUST indicate the branch, and pull-request associated with the work
- Plans MUST be implemented on a branch, and merged only after human review of a pull-request

## Conventions

- Python 3.9 — use `from __future__ import annotations` for type hints,
  `Optional[X]` for runtime expressions
- **Script invocation: `uv run` is the universal pattern.** All scripts in
  `scripts/` have PEP 723 inline metadata. Skills invoke them via
  `uv run <plugin-scripts-dir>/script.py`. The preflight reference at
  `skills/_shared/references/preflight.md` documents the 3-step check
  (uv availability → canary → actual script). No bare `python3 scripts/...`
  invocations in skill docs.
- CLI scripts default to CWD as root; accept `--root` for override
- **Plugin root discovery (all scripts):** Scripts use a hybrid pattern to
  find the plugin root for `sys.path` insertion. Prefer `CLAUDE_PLUGIN_ROOT`
  env var (forward-compatible with Claude Code), fall back to `__file__`
  parent chain. Shared scripts in `scripts/` use `.parent.parent` (2 levels);
  per-skill scripts in `skills/<name>/scripts/` use `.parent` × depth to root.
  Each fallback line must include a comment documenting the path chain (e.g.,
  `# skills/research/scripts/ → skills/research/ → skills/ → plugin root`).
  Do NOT use marker-based walk-up (`pyproject.toml` search) — it finds the
  user's project root instead of the plugin root. See
  `docs/research/2026-03-10-plugin-root-discovery.md` for full rationale.
- Validators return `list[dict]` with keys: `file`, `issue`, `severity`
- Skills use free-text intake — users describe intent, Claude routes
- `ValueError` + stdlib exceptions only (no custom exception hierarchy)
- Tests use inline markdown strings and `tmp_path` fixtures
