# wos

> **Experimental** — This project is under active development. APIs, skill interfaces, and document conventions may change without notice.

A Claude Code plugin for building and maintaining structured project context
with AI-assisted research, source verification, and quality validation.

## What It Does

WOS helps teams create and maintain a structured knowledge base alongside their
code. It provides skills for creating context documents, verifying sources,
and auditing quality — so agents can find what they need and trust what they
find.

**Structured context** — Documents have YAML metadata (`name`, `description`,
optional `type`, `sources`, `related`). Auto-generated `_index.md` files
provide lookup tables at every directory level.

**Research quality** — The SIFT framework guides source evaluation. Source URLs
are verified programmatically (HTTP HEAD/GET) at creation time and during
audit. Research documents require non-empty `sources` lists.

**Agent navigation** — AGENTS.md contains a WOS-managed section
(`<!-- wos:begin -->` / `<!-- wos:end -->`) with navigation instructions,
an areas table, metadata format, and communication preferences.

## Skills

WOS provides 13 active skills organized into four layers — knowledge, delivery,
infrastructure, and feedback. See [OVERVIEW.md](OVERVIEW.md) for the full
skill ecosystem diagram, lifecycle descriptions, and reference table.

## Project Structure

```
wos/
  document.py          # Document dataclass + parse_document()
  frontmatter.py       # Custom YAML subset parser (stdlib-only)
  index.py             # _index.md generation + sync checking
  validators.py        # 8 validation checks
  url_checker.py       # HTTP HEAD/GET URL reachability
  agents_md.py         # Marker-based AGENTS.md section management
  markers.py           # Shared marker-based section replacement
  preferences.py       # Communication preferences capture
  research_protocol.py # Search protocol logging
scripts/
  lint.py              # CLI: run validation, offer fixes
  reindex.py           # CLI: regenerate all _index.md files
  deploy.py            # CLI: export skills to .agents/ for cross-platform use
  check_url.py         # CLI: URL reachability checking
  update_preferences.py # CLI: update communication preferences
  get_version.py       # CLI: print plugin version
skills/                # Skill definitions (SKILL.md + references/)
  _shared/references/  # Shared references (research, distill pipelines)
tests/                 # pytest tests
docs/                  # Documentation, plans, and research
  context/             # Topic areas (created by /wos:setup)
  plans/               # Design docs and implementation plans
  research/            # Research artifacts
```

## Usage

```bash
claude --plugin-dir /path/to/wos
```

Or add to Claude Code settings for automatic loading.

## Cross-Platform Deployment

WOS skills can be deployed to GitHub Copilot, Cursor, Windsurf, Codex,
Gemini CLI, and other platforms. See [DEPLOYING.md](DEPLOYING.md) for
the full guide.

```bash
python scripts/deploy.py --platform copilot   # or --target /path/to/project
```

## Script Invocation

All scripts use [PEP 723](https://peps.python.org/pep-0723/) inline metadata
and are invoked via `python`. No external runtime dependencies — stdlib only.
Dev dependencies (pytest, ruff) install via `pip install -e ".[dev]"`.

## Dependencies

- Python 3.9+
- No runtime Python dependencies (stdlib only for `wos/` package)
- `gh` CLI (for report-issue skill)
