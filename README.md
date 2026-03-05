# wos

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

| Skill | Purpose |
|-------|---------|
| `/wos:init` | Initialize or update WOS project context |
| `/wos:audit` | Validate project health (7 checks + auto-fix) |
| `/wos:research` | SIFT-based research with source verification |
| `/wos:distill` | Convert research artifacts into focused context files |
| `/wos:consider` | Mental models for problem analysis |
| `/wos:refine-prompt` | Assess and refine prompts using evidence-backed techniques |
| `/wos:report-issue` | File GitHub issues against WOS repo |
| `/wos:retrospective` | Session review and feedback submission |

## Project Structure

```
wos/
  document.py          # Document dataclass + parse_document()
  frontmatter.py       # Custom YAML subset parser (stdlib-only)
  index.py             # _index.md generation + sync checking
  validators.py        # 5 validation checks
  url_checker.py       # HTTP HEAD/GET URL reachability
  agents_md.py         # Marker-based AGENTS.md section management
  markers.py           # Shared marker-based section replacement
  preferences.py       # Communication preferences capture
  research_protocol.py # Search protocol logging
scripts/
  audit.py             # CLI: run validation, offer fixes
  reindex.py           # CLI: regenerate all _index.md files
  check_runtime.py     # Canary: validate uv + PEP 723 pipeline
  check_url.py         # CLI: URL reachability checking
  update_preferences.py # CLI: update communication preferences
  get_version.py       # CLI: print plugin version
skills/                # Skill definitions (SKILL.md + references/)
  _shared/references/  # Shared references (e.g., preflight.md)
tests/                 # pytest tests
docs/                  # Documentation, plans, and research
  context/             # Topic areas (created by /wos:init)
  plans/               # Design docs and implementation plans
  research/            # Research artifacts
```

## Usage

```bash
claude --plugin-dir /path/to/wos
```

Or add to Claude Code settings for automatic loading.

## Script Invocation

All scripts use [PEP 723](https://peps.python.org/pep-0723/) inline metadata
and are invoked via `uv run`. This is the universal pattern across all WOS
skills — no bare `python3` for script invocations.

Skills follow a 3-step preflight before any `uv run` call:
1. Check `uv` availability
2. Run the canary (`check_runtime.py`) to validate PEP 723 dependency resolution
3. Run the actual script

See `skills/_shared/references/preflight.md` for the full pattern.

## Dependencies

- Python 3.9+
- [`uv`](https://docs.astral.sh/uv/) — for running scripts with PEP 723 inline dependencies
- No runtime Python dependencies (stdlib only for `wos/` package)
- `gh` CLI (for report-issue skill)
