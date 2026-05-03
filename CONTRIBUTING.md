# Contributing to toolkit

## Development Setup

```bash
pip install -e plugins/wiki -e plugins/check -e ".[dev]"
python -m pytest plugins/wiki/tests/ plugins/check/tests/ -v
ruff check plugins/
```

### Pre-commit hooks

Bootstrap once per clone:

```bash
pip install pre-commit
pre-commit install
```

Hooks defined in `.pre-commit-config.yaml`:

- **`skill-security-scan`** — runs `cisco-ai-skill-scanner` (static analyzers
  only, no LLM) against any `plugins/<plugin>/skills/<skill>/` directory with
  staged changes. Fails the commit on HIGH or CRITICAL findings. Requires
  `pip install cisco-ai-skill-scanner==2.0.9`.

Run on demand without committing:

```bash
pre-commit run --all-files                      # every hook, every file
pre-commit run skill-security-scan --all-files  # one hook, every file
```

## Versioning (SemVer)

Pre-1.0 — the public API is not yet stable.

Each plugin versions independently. A version bump requires updating both the
plugin's `pyproject.toml` and its `.claude-plugin/plugin.json`. Also update
`.claude-plugin/marketplace.json` if the manifest references a plugin version.

| Bump | When | Examples |
|------|------|----------|
| **Patch** (0.x.**Z**) | Bug fixes, internal refactors, doc-only changes | Fix `--fix` stripping preambles, rename private to public API |
| **Minor** (0.**Y**.0) | New features, new/removed skills or commands, behavioral changes to existing skills/scripts | Add `/consider:consider`, new validation check, change CLI flags |
| **Major** (**X**.0.0) | Explicit human decision only. Signals API stability commitment. Never automated, never triggered by a single change. | Declaring 1.0 |

**No version bump needed for:** plans, research docs, changelog updates,
CI config changes — anything that doesn't ship in the plugin.
