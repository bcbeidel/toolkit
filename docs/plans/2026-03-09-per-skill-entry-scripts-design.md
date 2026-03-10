# Per-Skill Entry Scripts Design

**Issue:** #146 — Establish per-skill entry scripts to reduce model guesswork
**Branch:** `feat/per-skill-entry-scripts`

## Summary

Add per-skill `scripts/` directories containing thin CLI wrappers that delegate
to new `wos/<skill>/` subpackages. Prototype with the `research` skill — an
assessment script that reports structural facts about research documents as
JSON, shifting the model from discovery mode to execution mode.

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Script location | Per-skill `skills/<name>/scripts/` | Co-located with the skill it serves; discoverable |
| Logic location | `wos/<skill>/` subpackages | Testable, importable, follows existing wrapper pattern |
| Existing modules | Leave in place | New code uses namespace pattern; migrate later if proven |
| `__init__.py` | Empty | No re-exports; imports are always explicit |
| Script naming | Skill-specific (e.g. `research_assess.py`) | Tied to the underlying action, not a generic name |
| Prototype skill | `research` only | Highest complexity, most to gain from state assessment |
| Assessment scope | Resumption only | Reports facts about existing documents; no scaffolding |
| Phase detection | None — structural facts only | Script reports observables; model infers phase (P2) |
| Output format | JSON to stdout | Consistent with `check_runtime.py`; machine-parseable |
| Two modes | `--file` and `--scan` | Explicit targeting plus directory discovery |
| Dependencies | stdlib only | Reuses `wos.document.parse_document()` (P7) |

## File Structure

```
wos/
  research/
    __init__.py                        — empty, marks package
    assess_research.py                 — assessment logic (two public functions)
skills/
  research/
    scripts/
      research_assess.py               — thin argparse CLI wrapper
tests/
  test_research_assess.py              — unit tests
```

## Assessment Output

### `--file` mode (single document)

```json
{
  "file": "docs/research/2026-03-09-topic.md",
  "exists": true,
  "frontmatter": {
    "name": "Topic Research",
    "description": "Investigation into topic X",
    "type": "research",
    "sources_count": 7,
    "related_count": 2
  },
  "content": {
    "word_count": 1450,
    "draft_marker_present": true,
    "has_sections": {
      "claims": true,
      "synthesis": false,
      "sources": true,
      "findings": true
    }
  },
  "sources": {
    "total": 7,
    "urls": ["https://example.com/a", "https://example.com/b"],
    "non_url_count": 0
  }
}
```

### `--scan` mode (directory discovery)

```json
{
  "directory": "docs/research",
  "documents": [
    {
      "file": "docs/research/2026-03-09-topic-a.md",
      "name": "Topic A Research",
      "draft_marker_present": true,
      "word_count": 1450,
      "sources_count": 7
    },
    {
      "file": "docs/research/2026-03-08-topic-b.md",
      "name": "Topic B Research",
      "draft_marker_present": false,
      "word_count": 2800,
      "sources_count": 12
    }
  ]
}
```

## Core Logic — `wos/research/assess_research.py`

Two public functions:

- **`assess_file(path: str) -> dict`** — Parse one document via
  `wos.document.parse_document()`, return structural facts: frontmatter fields,
  word count, draft marker presence, section detection, source listing.

- **`scan_directory(root: str, subdir: str = "docs/research") -> dict`** — Walk
  directory, filter to `type: research` documents, return summary per file.

### Section Detection

Simple string matching on heading text — look for headings containing keywords
like "claims", "synthesis", "sources", "findings". No markdown parsing library.
Structural assessment, not semantic understanding.

### What This Does NOT Do

- No phase detection — the model infers phase from facts
- No gate validation — the model decides if gates are passed
- No scaffolding — initialization is a separate concern
- No URL verification — that's `audit`'s job
- No file modification — read-only assessment (P9)

## CLI Wrapper — `skills/research/scripts/research_assess.py`

- PEP 723 inline metadata, no runtime dependencies
- `sys.path` self-insertion for plugin cache compatibility
- argparse: `--file <path>` or `--scan` with optional `--root`
- Imports `wos.research.assess_research`, calls appropriate function, prints JSON

## Namespace Convention

New skill-specific logic goes in `wos/<skill>/` subpackages:

```
wos/research/assess_research.py    — this prototype
wos/distill/assess_distill.py      — future, if needed
wos/audit/...                      — future, if needed
```

Existing top-level modules (`research_protocol.py`, `skill_audit.py`,
`validators.py`, etc.) stay in place. Migrate only when there's a concrete
reason.

## Principle Alignment

| Principle | How |
|-----------|-----|
| P2 Structure in code, quality in skills | Script reports facts; model applies judgment |
| P4 Keep it simple | Two functions, one wrapper, no hierarchies |
| P5 When in doubt, leave it out | Only observable facts; no phase/gate logic |
| P6 Omit needless words | JSON output is compact |
| P7 Depend on nothing | stdlib only, reuses existing parsers |
| P8 One obvious way to run | `uv run` with PEP 723 metadata |
| P9 Separate reads from writes | Read-only assessment |
| P10 Bottom line up front | Model gets all facts immediately |

## Skill Integration

Update `skills/research/SKILL.md` to reference the entry script. The model runs
it at the start of resumption workflows to understand document state before
proceeding.
