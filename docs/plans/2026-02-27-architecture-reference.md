---
name: WOS Architecture Reference
description: Current architecture overview of WOS as of v0.7.0
type: reference
related:
  - docs/plans/2026-02-22-simplification-design.md
  - docs/research/2026-02-22-design-principles.md
---

# WOS Architecture Reference (v0.7.0)

> Concise reference for maintainers returning to the project. For design
> rationale and history, see the related documents above.

## 1. What WOS Is

WOS is a **Claude Code plugin** for building and maintaining structured project
context. It provides skills, scripts, and a Python package that help users
create, validate, and navigate markdown knowledge bases in their own repos.

WOS is the tool, not the context itself. When working in the WOS repo, you are
building the tool.

**Key constraints:**
- Python 3.9+ (use `from __future__ import annotations`)
- stdlib-only core (`wos/` package has zero runtime dependencies)
- Scripts declare their own dependencies via PEP 723 inline metadata
- All script invocation goes through `uv run`

## 2. Design Principles

### What WOS cares about

1. **Convention over configuration.** Good patterns are documented for humans
   and LLMs to follow voluntarily, not enforced in code.

2. **Structure in code, quality in skills.** The code layer checks what's
   deterministic — links resolve, frontmatter exists, indexes sync. The skill
   layer guides content quality through research rigor, source verification,
   and structured workflows. Neither does the other's job.

3. **Single source of truth.** Navigation and indexes are derived from disk
   state, never curated by hand. Anything maintained manually will drift.

### How WOS is built

4. **Keep it simple.** No class hierarchies, no frameworks, no indirection.
   Choose the straightforward implementation over the flexible abstraction.

5. **When in doubt, leave it out.** Every required field, every abstraction,
   every feature must justify its presence.

6. **Omit needless words.** Every word in agent-facing output must earn its
   place. Brevity is a feature.

7. **Depend on nothing.** The core package depends only on the standard
   library. External dependencies are isolated to scripts that declare their
   own.

8. **One obvious way to run.** Every script, every skill, same entry point.
   Consistency eliminates a class of failures.

### How WOS operates

9. **Separate reads from writes.** Audit observes and reports. Fixes require
   explicit user action.

10. **Bottom line up front.** Key insights at the top and bottom. Detail in
    the middle. Convention, not enforcement.

## 3. Project Structure

```
wos/                          # Python package (9 modules, ~1,200 LOC)
scripts/                      # CLI entry points (6 scripts, PEP 723 metadata)
skills/                       # Skill definitions (8 skills + shared references)
tests/                        # pytest tests (17 files, ~2,400 LOC)
docs/plans/              # Design docs and implementation plans
docs/research/           # Research artifacts
.claude-plugin/               # Plugin metadata (plugin.json, marketplace.json)
```

### Package: `wos/`

| Module | Purpose |
|--------|---------|
| `document.py` | `Document` dataclass + `parse_document()` |
| `frontmatter.py` | Custom YAML subset parser (stdlib-only) |
| `index.py` | `_index.md` generation + sync checking |
| `validators.py` | 5 validation checks (warn/fail severity) |
| `url_checker.py` | HTTP HEAD/GET URL reachability |
| `agents_md.py` | Marker-based AGENTS.md section management |
| `markers.py` | Shared marker-based section replacement |
| `preferences.py` | Communication preferences capture |
| `research_protocol.py` | Search protocol logging (`SearchEntry`, `SearchProtocol`) |

### Scripts: `scripts/`

| Script | Dependencies | Purpose |
|--------|-------------|---------|
| `audit.py` | none | Run validation checks (`--fix`, `--json`, `--strict`) |
| `reindex.py` | none | Regenerate all `_index.md` files |
| `check_runtime.py` | httpx | Canary: validate uv + PEP 723 pipeline |
| `check_url.py` | none | URL reachability checking |
| `update_preferences.py` | none | Preference key=value updates |
| `get_version.py` | none | Print plugin version |

All scripts use `sys.path` self-insertion for plugin cache compatibility.
Skills invoke them as `uv run <plugin-scripts-dir>/script.py`.

### Skills

| Skill | Prefix | Purpose |
|-------|--------|---------|
| init | `/wos:init` | Initialize or update WOS project context |
| audit | `/wos:audit` | Validate project health (5 checks + auto-fix) |
| research | `/wos:research` | SIFT-based research with source verification |
| distill | `/wos:distill` | Convert research into focused context files |
| consider | `/wos:consider` | Mental models for analysis (16 models) |
| refine-prompt | `/wos:refine-prompt` | Assess and refine prompts with evidence-backed techniques |
| report-issue | `/wos:report-issue` | File issues against WOS repo |
| retrospective | `/wos:retrospective` | Session review and feedback submission |

Shared references live in `skills/_shared/references/` (e.g., `preflight.md`
for the uv run preflight pattern).

## 4. Document Model

One dataclass. No subclasses, no inheritance.

**Required frontmatter:** `name`, `description`
**Optional frontmatter:** `type`, `sources` (URLs), `related` (file paths),
plus any extra fields (pass through transparently).

`type` is a semantic tag (research, plan, reference, etc.). Only
`type: research` triggers special behavior: sources must be non-empty and URLs
are verified.

## 5. Validation (5 Checks)

Validators return `list[dict]` with keys: `file`, `issue`, `severity`.

| # | Check | What it catches | Severity |
|---|-------|----------------|----------|
| 1 | Frontmatter | Missing name/description, research without sources | fail + warn |
| 2 | Content length | Context files exceeding 800 words | warn |
| 3 | Source URLs | Unreachable URLs in `sources` field | fail |
| 4 | Related paths | File paths in `related` that don't exist on disk | fail |
| 5 | Index sync | `_index.md` out of sync with directory contents | fail + warn |

## 6. Navigation & Discovery

### `_index.md` (auto-generated)

Each directory under `docs/` gets an `_index.md` listing
files with descriptions from frontmatter, plus a subdirectory table. Preamble
text above the generated tables is preserved across regeneration.

Never hand-edit `_index.md` — use `reindex.py` or `/wos:audit --fix`.

### AGENTS.md (marker-managed)

WOS manages a section between `<!-- wos:begin -->` and `<!-- wos:end -->`
markers. Contains: navigation instructions, areas table, metadata format, and
communication preferences. Content outside markers is never touched.

## 7. Script Invocation: `uv run`

All Python invocation uses `uv run`. No bare `python3` calls in skill docs.

**Preflight pattern** (documented in `skills/_shared/references/preflight.md`):

1. Check `uv --version` — if missing, show install instructions, STOP
2. Run canary: `uv run <plugin-scripts-dir>/check_runtime.py` — if fails, STOP
3. Run actual script: `uv run <plugin-scripts-dir>/script.py [args]`

## 8. Development Conventions

- **Tests:** `uv run python -m pytest tests/ -v`
- **Lint:** `ruff check wos/ tests/ scripts/` (CI only; may not be local)
- **Branching:** Branch per feature/fix, merge via PR after review
- **Commits:** Granular within branches
- **Version bump:** Update all three: `pyproject.toml`, `plugin.json`,
  `marketplace.json`
- **Plans:** Stored in `docs/plans/`, include checkboxes, branch, and
  PR links
- **Exceptions:** `ValueError` + stdlib only (no custom exception hierarchy)
- **Tests:** Inline markdown strings + `tmp_path` fixtures

## 9. Related Documents

| Document | What it covers |
|----------|---------------|
| [Design Principles](../research/2026-02-22-design-principles.md) | 10 governing principles (full text with descriptions) |
| [Simplification Design](2026-02-22-simplification-design.md) | Why WOS was rewritten from 23 classes to 1 dataclass |
| [stdlib & Checks Design](2026-02-25-stdlib-and-checks-design.md) | Why runtime deps were removed, validator merge rationale |
| [uv run Preflight Design](2026-02-26-uv-run-preflight-design.md) | Why canary + reference doc instead of shell wrapper |
