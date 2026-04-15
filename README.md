# toolkit

> **Experimental** — This project is under active development. APIs, skill interfaces, and document conventions may change without notice.

A Claude Code plugin marketplace for building and maintaining structured project context,
with AI-assisted research, source verification, and quality validation.

> **Note:** GitHub repo rename from `wos` → `toolkit` is a pending manual step.

## Plugins

Five self-contained plugins, each independently installable:

| Plugin | Install | Skills |
|--------|---------|--------|
| `wiki` | `claude plugin install bcbeidel/toolkit --plugin wiki` | `setup`, `research`, `ingest`, `lint` |
| `build` | `claude plugin install bcbeidel/toolkit --plugin build` | `skill`, `rule`, `hook`, `subagent`, `refine-prompt` |
| `check` | `claude plugin install bcbeidel/toolkit --plugin check` | `skill`, `rule`, `hook`, `subagent`, `skill-chain` |
| `work` | `claude plugin install bcbeidel/toolkit --plugin work` | `scope`, `plan`, `start`, `verify`, `finish`, `audit`, `retro` |
| `consider` | `claude plugin install bcbeidel/toolkit --plugin consider` | 16 mental models + meta |

## Recommended Groupings

**Knowledge** — build and maintain project context documents:
```bash
claude plugin install bcbeidel/toolkit --plugin wiki
```

**Build tooling** — create and audit Claude Code skills and rules:
```bash
claude plugin install bcbeidel/toolkit --plugin build
claude plugin install bcbeidel/toolkit --plugin check
```

**Full suite** — complete toolkit for AI-assisted project work:
```bash
claude plugin install bcbeidel/toolkit --plugin wiki
claude plugin install bcbeidel/toolkit --plugin build
claude plugin install bcbeidel/toolkit --plugin check
claude plugin install bcbeidel/toolkit --plugin work
claude plugin install bcbeidel/toolkit --plugin consider
```

## Local Development

```bash
# Install Python packages and dev dependencies
pip install -e tools/wiki -e tools/check -e ".[dev]"

# Run tests
python -m pytest tools/wiki/tests/ tools/check/tests/ -v

# Lint
ruff check tools/
```

## Project Structure

```
tools/
  build/               # Plugin: create skills, rules, hooks, subagents
  check/               # Plugin: audit skills, rules, hooks, subagents
  wiki/                # Plugin: setup, research, ingest, lint
    wiki/              # Python package
    scripts/           # Shared CLI scripts
    skills/            # Skill definitions
    tests/             # Tests
  work/                # Plugin: scope, plan, start, verify, finish, audit, retro
  consider/            # Plugin: structured mental models
docs/                  # Documentation, plans, and research
  context/             # Topic areas
  plans/               # Design docs and implementation plans
  research/            # Research artifacts
.claude-plugin/
  marketplace.json     # Plugin marketplace manifest
```

## Dependencies

- Python 3.9+
- No runtime Python dependencies (stdlib only)
- `gh` CLI (for retrospective skill)
