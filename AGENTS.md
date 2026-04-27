# AGENTS.md

<!-- wiki:begin -->
## Context Navigation

Directory-level routing lives in [RESOLVER.md](RESOLVER.md). Consult it before filing or loading context.
Find files in registered directories via Glob on the directory's naming pattern; read frontmatter `description` to identify the right file.

Each `.md` file starts with YAML metadata (between `---` lines).
Read the `description` field before reading the full file.
Documents put key insights first and last; supplemental detail in the middle.

### File Metadata Format
```yaml
---
name: Title
description: What this covers
type: research       # optional
sources: []          # required if type is research
related: []          # optional, file paths from project root
---
```

### Document Standards

**Structure:** Key insights first, detailed explanation in the middle, takeaways at the bottom.
LLMs lose attention mid-document — first and last sections are what agents retain.

**Conventions:**
- Context files target 200-800 words. Over 800, consider splitting.
- One concept per file. Multiple distinct topics should be separate files.
- Link bidirectionally — if A references B in `related`, B should reference A.
<!-- wiki:end -->

## Content Routing

Before filing new content or loading context beyond a skill's eager
`references:`, consult [RESOLVER.md](RESOLVER.md).

## Plugin Structure

| Plugin | Path | Skills |
|--------|------|--------|
| `build` | `plugins/build/` | `build-skill`, `build-skill-pair`, `build-rule`, `build-hook`, `build-subagent`, `build-bash-script`, `build-python-script`, `build-makefile`, `build-pre-commit-config`, `build-github-workflow`, `build-readme`, `build-resolver`, `refine-prompt`, `check-skill`, `check-skill-pair`, `check-rule`, `check-hook`, `check-subagent`, `check-bash-script`, `check-python-script`, `check-makefile`, `check-pre-commit-config`, `check-github-workflow`, `check-readme`, `check-resolver`, `check-skill-chain` |
| `wiki` | `plugins/wiki/` | `setup`, `research`, `ingest`, `lint` |
| `work` | `plugins/work/` | `scope-work`, `plan-work`, `start-work`, `verify-work`, `finish-work` |
| `consider` | `plugins/consider/` | 16 mental models + meta |

Each plugin's skills live at `plugins/<plugin>/skills/<name>/SKILL.md`.
Python package: `plugins/wiki/src/wiki/` (editable install).
Shared scripts: `plugins/wiki/scripts/`.

## Preferences

- **Directness:** Be direct. State problems and disagreements plainly without hedging or softening.
- **Verbosity:** Keep responses concise. Skip preamble and unnecessary elaboration.
- **Depth:** Explain the reasoning and principles behind recommendations. Help me learn, not just execute.

## Working Agreements

- **Codify repetition.** If something will happen again, do it manually
  once on 3–10 items and show the output. If I approve, codify into a
  skill, hook, or cron. The test: if I have to ask twice, you failed.
- **Watch for patterns.** When you notice recurring work across
  sessions, propose codifying it proactively — don't wait to be asked.

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

- **Convention over configuration.** Document patterns, don't enforce them.
- **Structure in code, quality in skills.** Deterministic checks in Python or shell scripts, judgment in LLMs.
- **Single source of truth.** Navigation is derived from disk, never hand-curated.
- **Keep it simple.** No frameworks, no unnecessary indirection. Inheritance is acceptable when a document type has distinct data or validation behavior that would otherwise scatter across unrelated modules.
- **When in doubt, leave it out.** Every field, abstraction, and feature must justify itself.
- **Omit needless words.** Agent-facing output earns every token.
- **Depend on nothing.** Stdlib-only core; scripts isolate their own deps.
- **One obvious way to run.** Every script, every skill, same entry point.
- **Separate reads from writes.** Audit observes; fixes require explicit action.
- **Bottom line up front.** Key insights at top and bottom, detail in the middle.

## Conventions

- **Script path convention.** Scripts use `Path(__file__).parent.parent` (2 levels) to reach plugin root. Per-skill scripts go deeper. No marker-based walk-up — it finds the user's project root, not the plugin root.
- **`work`/`build` scripts.** No Python package — rely on editable install of `wiki`. Do not add sys.path manipulation to these scripts.
- **Per-plugin versioning.** A version bump updates the plugin's `pyproject.toml` and `.claude-plugin/plugin.json`. See CONTRIBUTING.md.
- **Python 3.9.** Use `from __future__ import annotations` for type hints.
- **Stdlib exceptions only.** `ValueError` and similar; no custom hierarchy.
- **Tests.** Use inline markdown strings and `tmp_path` fixtures.
