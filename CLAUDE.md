@AGENTS.md

# CLAUDE.md

This repo is **toolkit** — a Claude Code plugin marketplace. You are building
the tools, not using them.

## Build & Test

Install plugin packages and dev dependencies:

```bash
pip install -e plugins/wiki -e ".[dev]"
```

Run tests:
```bash
python -m pytest plugins/wiki/tests/ -v
```

Lint:
```bash
ruff check plugins/
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

## Conventions

- **Script path convention:** Scripts use `Path(__file__).parent.parent` (2 levels)
  to reach plugin root. Per-skill scripts go deeper. No marker-based walk-up —
  it finds the user's project root, not the plugin root.
- **`work`/`build` scripts:** No Python package — rely on editable install of
  `wiki`. Do not add sys.path manipulation to these scripts.
- **Per-plugin versioning:** A version bump updates the plugin's `pyproject.toml`
  and `.claude-plugin/plugin.json`. See CONTRIBUTING.md.
- Python 3.9 — use `from __future__ import annotations` for type hints
- `ValueError` + stdlib exceptions only (no custom exception hierarchy)
- Tests use inline markdown strings and `tmp_path` fixtures