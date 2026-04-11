---
name: Wiki + Structural Refactor
description: Add /wos:ingest wiki skill, rename audit-wos→lint and init-wos→setup, migrate docs/ areas to project root
type: plan
status: draft
branch: feat-rebuild-knowledge-base
pr: ~
related:
  - docs/research/2026-04-09-llm-wiki-knowledge-base-pattern.research.md
---

# Wiki + Structural Refactor

Extend WOS with a persistent wiki skill set and migrate all WOS-managed
document areas from `docs/<area>/` to root-level directories. Rename
`audit-wos` → `lint` and `init-wos` → `setup` to drop redundant suffixes
and adopt developer-native terminology. Net result: users get `/wos:setup`,
`/wos:lint`, and `/wos:ingest` as a coherent wiki workflow, with a flatter,
more intuitive project structure.

## Scope

**Must have:**
- `/wos:lint` (rename of `audit-wos`) — all existing checks preserved, wiki-aware
- `/wos:setup` (rename of `init-wos`) — root-level area scaffolding + wiki opt-in
- `/wos:ingest` — new skill: one source → 5–15 wiki page updates, append-only
- `wos/wiki.py` — `parse_schema()` + wiki frontmatter validators
- `scripts/lint.py` — renamed from `audit.py`, all existing CLI flags preserved
- Wiki checks in `scripts/lint.py`: orphan pages, schema violations, missing fields
- `wiki/SCHEMA.md` default template (in `skills/setup/references/`)
- WOS repo self-migration: `docs/research/` → `research/`, `docs/plans/` → `plans/`, `docs/prompts/` → `prompts/`
- All cross-references updated (README, OVERVIEW, CLAUDE.md, skill docs, tests)

**Won't have:**
- `/wos:wiki-query` skill
- Vector/embedding search
- MCP server wrapper
- `docs/context/` migration (WOS repo has no context area)

## Approach

Discovery confirmed: `wos/discovery.py`, `reindex.py`, and `agents_md.py`
contain zero `docs/` hardcoding — they already walk from project root.
Root-level migration is file moves + reference updates + a `reindex.py` run.
Wiki functionality requires a new `wos/wiki.py` module and three validator
functions. The ingest skill is SKILL.md instruction-driven; Python provides
post-ingest frontmatter validation and reindexing.

Execution order: skill renames first (Chunk 1), wiki Python infrastructure
second (Chunk 2), repo self-migration third (Chunk 3), ingest skill last
(Chunk 4). Chunks 1 and 2 are independent and can proceed in parallel.

## File Changes

**Create:**
- `wos/wiki.py` — `parse_schema()`, `check_wiki_orphans()`, `check_wiki_schema_violations()`, `check_wiki_frontmatter()`
- `tests/test_wiki.py` — tests for `wos/wiki.py`
- `skills/ingest/SKILL.md` — new ingest skill
- `skills/setup/references/wiki-schema-template.md` — default SCHEMA.md template

**Rename / Move (git mv):**
- `skills/audit-wos/` → `skills/lint/`
- `skills/init-wos/` → `skills/setup/`
- `scripts/audit.py` → `scripts/lint.py`
- `tests/test_audit.py` → `tests/test_lint.py`
- `docs/research/` → `research/`
- `docs/plans/` → `plans/`
- `docs/prompts/` → `prompts/`

**Modify:**
- `skills/lint/SKILL.md` — name/description/triggers updated
- `skills/setup/SKILL.md` — root-level dirs + wiki setup added
- `wos/validators.py` — `validate_wiki()` added
- `scripts/lint.py` — wiki checks added; `--wiki` auto-activated by `wiki/SCHEMA.md` presence
- `tests/test_lint.py` — imports updated from `scripts.audit` → `scripts.lint`
- `tests/test_script_syspath.py`, `tests/test_deploy.py`, `tests/test_skill_audit.py` — reference updates
- `CLAUDE.md`, `README.md`, `OVERVIEW.md`, `CHANGELOG.md`, `DEPLOYING.md`, `PRINCIPLES.md` — skill/script name refs
- `skills/_shared/references/` — any `audit-wos`/`init-wos`/`audit.py` refs
- `skills/write-plan/references/` — ref updates
- `skills/execute-plan/references/` — ref updates

**Delete:**
- `docs/` directory (after migration, once empty)

## Branch / PR

Branch: `feat-rebuild-knowledge-base`
PR: open after all chunks pass validation

---

## Chunk 1: Skill + Script Renames

### Task 1 — Rename `audit-wos` skill to `lint`

**Files:** `skills/audit-wos/` → `skills/lint/`

- [ ] `git mv skills/audit-wos skills/lint`
- [ ] Edit `skills/lint/SKILL.md`: set `name: lint`, update description to use "lint" / "lint checks" terminology, update trigger phrases (add "lint", "run lint", "check lint")
- [ ] Rename `skills/lint/references/skill-authoring-guide.md` path only if references inside it need updating
- [ ] Verify: `ls skills/lint/SKILL.md && ! ls skills/audit-wos 2>/dev/null`
- [ ] `python -m pytest tests/ -v -k "not test_audit"` — existing tests pass
- [ ] Commit: `git commit -m "rename: audit-wos skill → lint"`

### Task 2 — Rename `scripts/audit.py` to `scripts/lint.py`

**Files:** `scripts/audit.py` → `scripts/lint.py`, `tests/test_audit.py` → `tests/test_lint.py`

- [ ] `git mv scripts/audit.py scripts/lint.py`
- [ ] `git mv tests/test_audit.py tests/test_lint.py`
- [ ] Edit `tests/test_lint.py`: replace all `from scripts.audit import` with `from scripts.lint import`, replace `"audit.py"` argv references with `"lint.py"`
- [ ] Edit `tests/test_script_syspath.py`: update any `audit.py` path references to `lint.py`
- [ ] Verify script CLI preserved: `python scripts/lint.py --help` — shows identical flags to old `audit.py` (file, --root, --no-urls, --json, --fix, --strict, --context-max-words, --context-min-words, --skill-max-lines)
- [ ] `python -m pytest tests/test_lint.py -v` — all tests pass
- [ ] Commit: `git commit -m "rename: scripts/audit.py → scripts/lint.py, test_audit.py → test_lint.py"`

### Task 3 — Rename `init-wos` skill to `setup`

**Files:** `skills/init-wos/` → `skills/setup/`

- [ ] `git mv skills/init-wos skills/setup`
- [ ] Edit `skills/setup/SKILL.md`:
  - Set `name: setup`
  - Update description: "Initialize or update WOS project context" (keep intent, drop `-wos`)
  - Update all directory references from `docs/<area>/` to root-level `<area>/`
  - Add wiki setup step: if user opts in, scaffold `wiki/` with `SCHEMA.md` from template and generate `wiki/_index.md`
  - Update trigger phrases to include "setup", "/wos:setup"
- [ ] Verify: `ls skills/setup/SKILL.md && ! ls skills/init-wos 2>/dev/null`
- [ ] `python -m pytest tests/ -v` — all pass
- [ ] Commit: `git commit -m "rename: init-wos skill → setup, update dir references to root-level"`

### Task 4 — Update all remaining cross-references

**Files:** README.md, OVERVIEW.md, CLAUDE.md, CHANGELOG.md, DEPLOYING.md, PRINCIPLES.md, `skills/_shared/references/`, `skills/write-plan/references/`, `skills/execute-plan/references/`, `tests/test_deploy.py`, `tests/test_skill_audit.py`

- [ ] `grep -r "audit-wos\|init-wos\|audit\.py" --include="*.md" --include="*.py" . -l` — enumerate remaining references
- [ ] Replace `audit-wos` → `lint`, `init-wos` → `setup`, `audit.py` → `lint.py` in all listed files (verify each change is contextually correct, not mechanical)
- [ ] `python -m pytest tests/ -v` — full suite passes
- [ ] `python scripts/lint.py --root .` — clean pass (no new issues introduced)
- [ ] Commit: `git commit -m "chore: update all audit-wos/init-wos/audit.py references to lint/setup/lint.py"`

---

## Chunk 2: Wiki Python Infrastructure

*Chunks 1 and 2 are independent — can proceed in parallel with Chunk 1.*

### Task 5 — Create `wos/wiki.py`

**Files:** `wos/wiki.py` (create), `tests/test_wiki.py` (create)

`wos/wiki.py` must provide:
- `parse_schema(schema_path: Path) -> dict` — reads `SCHEMA.md`, extracts `page_types`, `confidence_tiers`, `relationship_types` as lists. Returns dict with those keys. Raises `ValueError` if required sections are missing.
- `check_wiki_orphans(wiki_dir: Path) -> List[dict]` — returns issues for `.md` files in `wiki_dir` not referenced in `wiki_dir/_index.md`. Severity: `warn`.
- `check_wiki_schema_violations(doc: Document, schema: dict) -> List[dict]` — returns issues if `doc.type` or `doc.extra.get("confidence")` are not in schema's defined values. Severity: `fail`.
- `check_wiki_frontmatter(doc: Document) -> List[dict]` — returns issues for missing wiki-required fields: `confidence`, `created`, `updated`. Severity: `warn`.

Schema section format in SCHEMA.md (used by `parse_schema`):
```markdown
## Page Types
- concept
- entity
...

## Confidence Tiers
- high
- medium
- low

## Relationship Types
- related_to
...
```

Tests in `tests/test_wiki.py`:
- `test_parse_schema_valid` — parses a well-formed SCHEMA.md
- `test_parse_schema_missing_section` — raises ValueError
- `test_check_wiki_orphans` — detects a file not in index
- `test_check_wiki_schema_violations` — catches invalid type/confidence
- `test_check_wiki_frontmatter` — catches missing confidence/created/updated

- [ ] Write `wos/wiki.py` with four functions above
- [ ] Write `tests/test_wiki.py` with five tests above using inline markdown fixtures and `tmp_path`
- [ ] `python -m pytest tests/test_wiki.py -v` — all 5 tests pass
- [ ] `python -c "from wos.wiki import parse_schema, check_wiki_orphans, check_wiki_schema_violations, check_wiki_frontmatter; print('ok')`
- [ ] Commit: `git commit -m "feat: add wos/wiki.py — parse_schema, wiki validators"`

### Task 6 — Add `validate_wiki()` to `wos/validators.py`

**Files:** `wos/validators.py`

- [ ] Add `validate_wiki(wiki_dir: Path, schema_path: Path) -> List[dict]` to `wos/validators.py`:
  - Calls `parse_schema(schema_path)` — if missing or malformed, returns single warn issue and exits early
  - Discovers all `.md` files in `wiki_dir` (excluding `_index.md`, `SCHEMA.md`)
  - Parses each as a Document; runs `check_wiki_schema_violations`, `check_wiki_frontmatter` per file
  - Runs `check_wiki_orphans(wiki_dir)` once
  - Runs `check_index_sync` on `wiki_dir` (reuses existing check)
  - Returns combined issue list
- [ ] Add tests to `tests/test_wiki.py` for `validate_wiki()` (two cases: clean wiki, wiki with violations)
- [ ] `python -m pytest tests/test_wiki.py tests/test_validators.py -v` — all pass
- [ ] Commit: `git commit -m "feat: add validate_wiki() to wos/validators.py"`

### Task 7 — Extend `scripts/lint.py` with wiki checks

**Files:** `scripts/lint.py`

- [ ] Add auto-detection: at start of `main()`, check if `<root>/wiki/SCHEMA.md` exists; if so, set `wiki_mode = True`
- [ ] When `wiki_mode` is True: call `validate_wiki(root / "wiki", root / "wiki/SCHEMA.md")` and include results in output alongside existing checks
- [ ] Wiki issues display in same format as existing issues (file, issue, severity)
- [ ] Verify all existing CLI flags still work: `python scripts/lint.py --help` — same flags as before
- [ ] Test with a synthetic wiki dir: create `tmp/wiki/SCHEMA.md` + a page with bad `confidence` value → `python scripts/lint.py --root tmp` → shows schema violation
- [ ] `python -m pytest tests/test_lint.py -v` — all pass
- [ ] Commit: `git commit -m "feat: extend scripts/lint.py with auto-activated wiki checks"`

### Task 8 — Create `wiki/SCHEMA.md` default template

**Files:** `skills/setup/references/wiki-schema-template.md` (create)

The template must include all four required sections with sensible defaults and inline comments explaining each value. Referenced by `skills/setup/SKILL.md` when scaffolding a new wiki.

Required sections: `## Page Types`, `## Confidence Tiers`, `## Relationship Types`, `## Lint Rules`

Default page types: `concept`, `entity`, `source-summary`, `comparison`
Default confidence tiers: `high` (3+ corroborating sources, recent), `medium` (1-2 sources or older), `low` (single source, unverified, or inferred)
Default relationship types: `related_to`, `uses`, `depends_on`, `contradicts`, `supersedes`
Default lint rules: staleness threshold 90 days for high-confidence, minimum 2 sources for high confidence

- [ ] Write `skills/setup/references/wiki-schema-template.md` with four sections above
- [ ] Verify `parse_schema()` parses it without error: `python -c "from wos.wiki import parse_schema; from pathlib import Path; s = parse_schema(Path('skills/setup/references/wiki-schema-template.md')); print(s)"`
- [ ] Update `skills/setup/SKILL.md` to reference this template file in the wiki setup step
- [ ] Commit: `git commit -m "feat: add wiki/SCHEMA.md default template to skills/setup/references/"`

---

## Chunk 3: WOS Repo Self-Migration

*Depends on Chunk 1 (Task 4) completing — CLAUDE.md and skill references must be updated before migration.*

### Task 9 — Move `docs/` areas to project root

**Files:** `docs/research/` → `research/`, `docs/plans/` → `plans/`, `docs/prompts/` → `prompts/`

- [ ] `git mv docs/research research`
- [ ] `git mv docs/plans plans`
- [ ] `git mv docs/prompts prompts`
- [ ] `rmdir docs` (if now empty; verify first with `ls docs/`)
- [ ] Verify files moved: `ls research/_index.md plans/_index.md prompts/_index.md`
- [ ] `git status` — moved files show as renames, no untracked residue
- [ ] Commit: `git commit -m "refactor: migrate docs/research, docs/plans, docs/prompts to project root"`

### Task 10 — Update `related:` frontmatter paths in moved files

**Files:** all `.md` files in `research/`, `plans/`, `prompts/`

- [ ] `grep -r "docs/research\|docs/plans\|docs/prompts" research/ plans/ prompts/ --include="*.md" -l` — enumerate affected files
- [ ] For each file: update `related:` frontmatter entries from `docs/<area>/file.md` → `<area>/file.md`
- [ ] `python scripts/lint.py --root . --no-urls` — zero "related path does not exist" failures
- [ ] Commit: `git commit -m "fix: update related: frontmatter paths after docs/ migration"`

### Task 11 — Update CLAUDE.md and regenerate indexes

**Files:** `CLAUDE.md`, `AGENTS.md` (via reindex), `research/_index.md`, `plans/_index.md`, `prompts/_index.md`

- [ ] Edit `CLAUDE.md`: replace all `docs/plans`, `docs/research`, `docs/prompts` path references with root-level equivalents
- [ ] `python scripts/reindex.py --root .` — regenerates `_index.md` files and updates AGENTS.md areas table
- [ ] Verify AGENTS.md areas table shows `research`, `plans`, `prompts` (not `docs/research` etc.): `grep "docs/" AGENTS.md` → no matches within areas table
- [ ] `python scripts/lint.py --root . --no-urls` — clean pass, zero failures
- [ ] `python -m pytest tests/ -v` — full suite passes
- [ ] Commit: `git commit -m "chore: update CLAUDE.md paths, regenerate indexes after docs/ migration"`

---

## Chunk 4: Ingest Skill

*Depends on Chunk 2 (Tasks 5–8) completing.*

### Task 12 — Create `skills/ingest/SKILL.md`

**Files:** `skills/ingest/SKILL.md` (create)

The skill must specify:
- **Trigger phrases:** "ingest this", "add to wiki", "process this source", "update wiki with"
- **Input handling:** accept URL, file path, or pasted text; resolve to readable content before proceeding
- **Pre-ingest:** read `wiki/_index.md` to understand existing page inventory; read `wiki/SCHEMA.md` for valid types/confidence values
- **Ingest protocol (LLM):**
  1. Identify 5–15 wiki pages affected by this source (new + existing)
  2. For each page: update content append-only (never delete existing content), assign `type` + `confidence` from schema, update `sources:` list, update `updated:` date, update `related:` cross-references
  3. Flag any contradictions with existing pages as inline comments `<!-- CONTRADICTION: ... -->`
  4. Create new pages if topic has no existing page
- **Post-ingest (Python):** run `python scripts/lint.py --root <project-root> --no-urls` and report any new issues; run `python scripts/reindex.py --root <project-root>` to update `wiki/_index.md`
- **Append-only constraint:** document explicitly — existing prose is never removed or overwritten; only additions and frontmatter updates are permitted

- [ ] Write `skills/ingest/SKILL.md` with all sections above
- [ ] Verify required sections present: `grep -E "append-only|SCHEMA\.md|_index\.md|contradiction" skills/ingest/SKILL.md` — all four match
- [ ] `python scripts/lint.py --root .` — skill passes skill quality checks (name format, description length, instruction density)
- [ ] Commit: `git commit -m "feat: add /wos:ingest skill for wiki page ingestion"`

### Task 13 — End-to-end validation

**Files:** none (verification only)

- [ ] `python -m pytest tests/ -v` — full suite passes, zero failures
- [ ] `python scripts/lint.py --root . --no-urls` — clean pass
- [ ] `python scripts/reindex.py --root .` — "AGENTS.md areas table already up to date" (confirms areas match new structure)
- [ ] `grep -r "docs/plans\|docs/research\|docs/prompts\|audit-wos\|init-wos" --include="*.md" --include="*.py" . --exclude-dir=".git"` — zero matches (all old refs purged)
- [ ] `ls skills/lint/ skills/setup/ skills/ingest/` — all three skill directories exist
- [ ] `ls research/ plans/ prompts/` — all three areas at root
- [ ] Commit: `git commit -m "chore: final validation pass — wiki refactor complete"`

---

## Validation

```bash
# 1. Full test suite — zero failures
python -m pytest tests/ -v

# 2. Lint clean pass
python scripts/lint.py --root . --no-urls

# 3. Indexes regenerate cleanly
python scripts/reindex.py --root .

# 4. No old references remain
grep -r "docs/plans\|docs/research\|docs/prompts\|audit-wos\|init-wos\|audit\.py" \
  --include="*.md" --include="*.py" . --exclude-dir=".git"
# Expected: zero matches

# 5. New skills discoverable
ls skills/lint/SKILL.md skills/setup/SKILL.md skills/ingest/SKILL.md
# Expected: all three files exist

# 6. Wiki validators importable
python -c "from wos.wiki import parse_schema, check_wiki_orphans, \
  check_wiki_schema_violations, check_wiki_frontmatter; print('ok')"
# Expected: ok

# 7. Root-level areas present
ls research/ plans/ prompts/
# Expected: all three directories exist with _index.md files
```

## Notes

- `discovery.py`, `reindex.py`, and `agents_md.py` contain zero `docs/` hardcoding (verified by grep). Root-level migration requires no Python infrastructure changes beyond tests and reference updates.
- `test_audit.py` must be renamed to `test_lint.py` (Task 2) — it imports `from scripts.audit import main` which breaks after the script rename.
- 22 files reference `audit-wos`, `init-wos`, or `audit.py` (grep-verified). Task 4 handles bulk update; Tasks 1–3 handle the primary artifacts.
- This plan file lives at `docs/plans/` and migrates to `plans/` in Task 9. The plan path in `related:` frontmatter will update in Task 10.
