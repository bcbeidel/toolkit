---
name: Wiki Schema Infrastructure
description: Add wos/wiki.py validators, validate_wiki() in validators.py, wiki auto-detection in scripts/lint.py, and a default SCHEMA.md template — Python foundation for the wiki feature.
type: plan
status: executing
branch: feat/wiki-schema-infrastructure
pr: ~
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
  - docs/research/2026-04-09-llm-wiki-knowledge-base-pattern.research.md
---

# Wiki Schema Infrastructure

Add the Python foundation for the wiki feature. Closes bcbeidel/wos#218. Implements
Task 2 of the v0.36.0 roadmap.

## Goal

Ship `wos/wiki.py` with four validator functions, `validate_wiki()` in
`wos/validators.py`, wiki auto-detection in `scripts/lint.py`, a default
SCHEMA.md template, and 7 passing tests — with no regressions.

## Scope

**Must have:**
- `wos/document.py` — `meta: dict` field on Document to expose unknown frontmatter
- `wos/wiki.py` — `parse_schema`, `check_wiki_orphans`, `check_wiki_schema_violations`, `check_wiki_frontmatter`
- `wos/validators.py` — `validate_wiki(wiki_dir, schema_path)`
- `scripts/lint.py` — wiki auto-detection (`wiki/SCHEMA.md` presence → run validation)
- `skills/setup/references/wiki-schema-template.md` — default SCHEMA.md with all required sections
- `tests/test_wiki.py` — 7 tests using inline fixtures and `tmp_path`

**Won't have:**
- `/wos:ingest` skill (Issue #219 — separate task)
- Migration of existing context files to wiki schema (Issue #220 — separate task)
- Staleness date arithmetic against `updated` (no datetime math in this PR)
- New CLI flags — wiki detection is automatic, zero-config

## Approach

**Task 1 already merged:** bcbeidel/wos#221 (rename `audit-wos`→`lint`, `init-wos`→`setup`,
`scripts/audit.py`→`scripts/lint.py`) landed before this plan was executed. This plan targets
the current filenames: `scripts/lint.py` and `skills/setup/references/`.

**`Document.meta`:** `check_wiki_schema_violations` needs `confidence` and
`check_wiki_frontmatter` needs `confidence`, `created`, `updated` — all wiki-specific
frontmatter that `parse_document()` currently discards. Add `meta: dict = field(default_factory=dict)`
to Document and capture unknown frontmatter keys there. This is backwards-compatible (empty dict
for all existing documents), preserves the single-Document-dataclass principle, and aligns
with the `meta:` convention used in SKILL.md and other formats.

**Module split:** `parse_schema`, `check_wiki_orphans`, `check_wiki_schema_violations`,
`check_wiki_frontmatter` live in `wos/wiki.py` (domain-specific, parallel to `index.py` and
`skill_audit.py`). `validate_wiki()` lives in `wos/validators.py`, consistent with the
`validate_project()` / `validate_file()` orchestration pattern.

**`parse_schema` parser:** stdlib line-by-line scan of SCHEMA.md. On `## Page Types`,
collect `- value` items until the next `##` section. Repeat for `## Confidence Tiers`
and `## Relationship Types`. Missing any of the three sections → `ValueError`.

**`check_wiki_orphans`:** read `wiki_dir/_index.md` content; for each `.md` file in
`wiki_dir` (excluding `_index.md` and `SCHEMA.md`), warn if the filename does not appear
as a substring in the index text.

**Auto-detection insertion point:** after the `if args.file / else` block populates
`issues`, add wiki check before the `--fix` section:
```python
wiki_schema = root / "wiki" / "SCHEMA.md"
if wiki_schema.is_file():
    from wos.validators import validate_wiki
    issues.extend(validate_wiki(root / "wiki", wiki_schema))
```

## File Changes

| Action | File | Description |
|--------|------|-------------|
| Modify | `wos/document.py` | Add `meta: dict` to Document; capture unknown frontmatter keys in `parse_document()` |
| Create | `wos/wiki.py` | Four wiki validator functions |
| Modify | `wos/validators.py` | Add `validate_wiki(wiki_dir, schema_path)` |
| Modify | `scripts/lint.py` | Wiki auto-detection block after issue list is populated |
| Create | `skills/setup/references/wiki-schema-template.md` | Default SCHEMA.md template |
| Create | `tests/test_wiki.py` | 7 tests using inline fixtures and `tmp_path` |

## Tasks

### Task 1 — Add `meta: dict` to Document

- [x] Task 1: Add `meta: dict` field to Document dataclass and capture unknown frontmatter keys in `parse_document()` <!-- sha:d6a9e83 -->

Modify `wos/document.py`:

1. Add `meta: dict = field(default_factory=dict)` to the `Document` dataclass, after `updated_at`.
2. In `parse_document()`, after extracting all known keys, collect remaining `fm` entries into `meta`:
   ```python
   _KNOWN_KEYS = {"name", "description", "type", "sources", "related",
                  "status", "created_at", "updated_at"}
   meta = {k: v for k, v in fm.items() if k not in _KNOWN_KEYS}
   ```
3. Pass `meta=meta` in the `Document(...)` constructor call.

**Verify:**
```bash
python -c "
from wos.document import parse_document
doc = parse_document('test.md', '---\nname: T\ndescription: D\nconfidence: high\n---\nbody')
assert doc.meta.get('confidence') == 'high', doc.meta
print('ok')
"
# Expected: ok
```

**Commit:** `feat: add meta dict field to Document for unknown frontmatter keys`

---

### Task 2 — Create `wos/wiki.py`

- [x] Task 2: Create `wos/wiki.py` with `parse_schema`, `check_wiki_orphans`, `check_wiki_schema_violations`, `check_wiki_frontmatter` <!-- sha:2c3721d -->

Create `wos/wiki.py` with four functions. Use `from __future__ import annotations` and
`from typing import List`. No third-party deps.

```python
def parse_schema(schema_path: Path) -> dict:
    """Read SCHEMA.md, extract page_types, confidence_tiers, relationship_types.
    Returns dict with those keys as lists. Raises ValueError if any section is missing."""

def check_wiki_orphans(wiki_dir: Path) -> List[dict]:
    """Warn issues for .md files in wiki_dir not referenced in wiki_dir/_index.md.
    Skips _index.md and SCHEMA.md."""

def check_wiki_schema_violations(doc: Document, schema: dict) -> List[dict]:
    """Fail issues if doc.type not in schema['page_types'],
    or doc.meta.get('confidence') (when present) not in schema['confidence_tiers']."""

def check_wiki_frontmatter(doc: Document) -> List[dict]:
    """Warn issues for missing confidence, created, or updated fields in doc.meta."""
```

Implementation notes:
- `parse_schema`: open and read `schema_path`; track current section; collect `- value` lines.
  Required sections: `Page Types`, `Confidence Tiers`, `Relationship Types`.
  Return keys: `page_types`, `confidence_tiers`, `relationship_types`.
- `check_wiki_schema_violations`: for `confidence`, only emit a fail if the field is
  *present but invalid*. A missing `confidence` is handled by `check_wiki_frontmatter`.
- Each issue dict: `{"file": str(doc.path), "issue": "...", "severity": "fail"|"warn"}`.
  Orphan issues use `str(file_path)` as the `file` key.

**Verify:**
```bash
python -c "from wos.wiki import parse_schema, check_wiki_orphans, check_wiki_schema_violations, check_wiki_frontmatter; print('ok')"
# Expected: ok
```

**Commit:** `feat: add wos/wiki.py with parse_schema and wiki validator functions`

---

### Task 3 — Add `validate_wiki()` to `wos/validators.py`

- [x] Task 3: Add `validate_wiki(wiki_dir, schema_path)` to `wos/validators.py` <!-- sha:5117f9c -->

Add `validate_wiki(wiki_dir: Path, schema_path: Path) -> List[dict]` to the bottom of
`wos/validators.py`, in the composite-functions section:

```python
def validate_wiki(wiki_dir: Path, schema_path: Path) -> List[dict]:
    """Validate all documents in a wiki directory against its SCHEMA.md.

    Runs schema violation and frontmatter checks per file, orphan check
    across the directory, and index sync for wiki_dir.

    Args:
        wiki_dir: Path to the wiki directory.
        schema_path: Path to wiki/SCHEMA.md.

    Returns:
        List of issue dicts. Empty on a clean wiki.
    """
    from wos.wiki import (
        check_wiki_frontmatter,
        check_wiki_orphans,
        check_wiki_schema_violations,
        parse_schema,
    )

    issues: List[dict] = []

    # Parse schema — on failure, emit a single warn and abort
    try:
        schema = parse_schema(schema_path)
    except ValueError as exc:
        return [{"file": str(schema_path), "issue": f"Invalid SCHEMA.md: {exc}", "severity": "warn"}]

    # Per-file checks
    for md_file in sorted(wiki_dir.iterdir()):
        if not md_file.is_file() or md_file.suffix != ".md":
            continue
        if md_file.name in ("_index.md", "SCHEMA.md"):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            doc = parse_document(str(md_file), text)
        except (OSError, ValueError) as exc:
            issues.append({"file": str(md_file), "issue": f"Parse error: {exc}", "severity": "fail"})
            continue
        issues.extend(check_wiki_schema_violations(doc, schema))
        issues.extend(check_wiki_frontmatter(doc))

    # Directory-level checks
    issues.extend(check_wiki_orphans(wiki_dir))
    issues.extend(check_index_sync(wiki_dir))

    return issues
```

**Verify:**
```bash
python -c "from wos.validators import validate_wiki; print('ok')"
# Expected: ok
```

**Commit:** `feat: add validate_wiki() to wos/validators.py`

---

### Task 4 — Wire wiki auto-detection into `scripts/lint.py`

- [x] Task 4: Add wiki auto-detection block to `scripts/lint.py` (triggered by `wiki/SCHEMA.md` presence) <!-- sha:1260879 -->

In `scripts/lint.py`, locate the block after the `if args.file: ... else: ...` branch
that sets `issues` (around line 131) and after the `--fix` block (around line 156).
Insert the wiki auto-detection immediately after `issues = remaining` (end of `--fix` block),
before the skill-density section:

```python
# Wiki validation — auto-activated when wiki/SCHEMA.md is present
wiki_schema = root / "wiki" / "SCHEMA.md"
if wiki_schema.is_file():
    from wos.validators import validate_wiki
    issues.extend(validate_wiki(root / "wiki", wiki_schema))
```

**Verify (current project has no `wiki/SCHEMA.md` — output unchanged):**
```bash
python scripts/lint.py --root . --no-urls 2>&1 | tail -5
# Expected: same output as running on main branch
```

**Commit:** `feat: auto-detect wiki/SCHEMA.md and run validate_wiki in scripts/lint.py`

---

### Task 5 — Create `skills/setup/references/wiki-schema-template.md`

- [x] Task 5: Create `skills/setup/references/wiki-schema-template.md` with default SCHEMA.md content <!-- sha:cba0e20 -->

Create the default SCHEMA.md template:

```markdown
# SCHEMA.md

Define the structure of this project's wiki.
Validated automatically by `/wos:lint` when `wiki/SCHEMA.md` is present.

## Page Types
- concept
- entity
- source-summary
- comparison

## Confidence Tiers
- high
- medium
- low

## Relationship Types
- related_to
- uses
- depends_on
- contradicts
- supersedes

## Lint Rules
- staleness: high-confidence pages flagged after 90 days without update
- min-sources: high-confidence pages require at least 2 sources
```

Note: `parse_schema()` reads only `## Page Types`, `## Confidence Tiers`,
and `## Relationship Types`. `## Lint Rules` is informational for humans; future
validators may interpret it.

**Verify:**
```bash
python -c "
from pathlib import Path
from wos.wiki import parse_schema
schema = parse_schema(Path('skills/setup/references/wiki-schema-template.md'))
assert schema['page_types'] == ['concept', 'entity', 'source-summary', 'comparison']
assert schema['confidence_tiers'] == ['high', 'medium', 'low']
assert 'related_to' in schema['relationship_types']
print('ok')
"
# Expected: ok
```

**Commit:** `feat: add wiki-schema-template.md to setup references`

---

### Task 6 — Write `tests/test_wiki.py`

- [x] Task 6: Create `tests/test_wiki.py` with 7 tests covering all wiki validator functions <!-- sha:7410173 -->

Create `tests/test_wiki.py` with 7 tests. All use inline markdown strings and `tmp_path`.

```
test_parse_schema_valid              — valid SCHEMA.md → correct lists for all three keys
test_parse_schema_missing_section    — SCHEMA.md without ## Confidence Tiers → ValueError
test_check_wiki_orphans              — unindexed file → warn; indexed file → no issue
test_check_wiki_schema_violations    — unrecognized type → fail; unrecognized confidence → fail
test_check_wiki_frontmatter          — missing confidence/created/updated in meta → 3 warns; all present → empty
test_validate_wiki_clean             — valid SCHEMA.md + valid doc + proper _index.md → no issues
test_validate_wiki_with_violations   — valid SCHEMA.md + doc with type "unknown-type" → fail issues
```

Reference `tests/test_validators.py` for fixture conventions (inline strings, `tmp_path`-based
file writes). Import `validate_wiki` from `wos.validators` for the integration tests.

**Verify:**
```bash
python -m pytest tests/test_wiki.py -v
# Expected: 7 passed, 0 failed
```

**Commit:** `test: add tests/test_wiki.py — 7 tests for wiki schema infrastructure`

---

### Task 7 — Full regression pass

- [x] Task 7: Verify full test suite and lint pass with no regressions <!-- sha:7410173 -->

No code changes. Verify no regressions across the full test suite and audit run.

**Verify:**
```bash
python -m pytest tests/ -v
# Expected: zero failures (all pre-existing tests still pass)

python scripts/lint.py --root . --no-urls
# Expected: no new failures compared to main branch
```

If any existing test breaks, fix the root cause before opening the PR.

## Validation

```bash
# Import check
python -c "from wos.wiki import parse_schema, check_wiki_orphans, check_wiki_schema_violations, check_wiki_frontmatter; print('ok')"
# Expected: ok

# validate_wiki importable
python -c "from wos.validators import validate_wiki; print('ok')"
# Expected: ok

# All 7 wiki tests pass
python -m pytest tests/test_wiki.py -v
# Expected: 7 passed

# Template parses cleanly
python -c "
from pathlib import Path; from wos.wiki import parse_schema
s = parse_schema(Path('skills/setup/references/wiki-schema-template.md'))
assert len(s['page_types']) >= 4 and len(s['confidence_tiers']) >= 3
print('ok')
"
# Expected: ok

# No behavior change on a project without wiki/SCHEMA.md
python scripts/lint.py --root . --no-urls
# Expected: same output as main branch

# Full suite clean
python -m pytest tests/ -v
# Expected: zero failures
```
