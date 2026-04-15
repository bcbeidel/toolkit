---
name: Document Inheritance Refactor
description: Replace the flat Document dataclass with a base class + typed subclasses (ResearchDocument, PlanDocument, ChainDocument, WikiDocument), each owning its own validation via issues() and is_valid().
type: plan
status: completed
branch: refactor/document-inheritance
related: []
---

# Document Inheritance Refactor

## Goal

Replace the flat `Document` dataclass with a proper class hierarchy. Each document
type becomes a subclass that carries its own structured data fields and runs its own
validation — no more scattered check functions that re-examine `doc.type` at call
sites. The result is a cleaner API: `doc.issues(root)` and `doc.is_valid(root)` work
on any document regardless of type, and type-specific behavior lives where it belongs.

## Scope

**Must have:**
- `Document` base class with `issues(root) -> list[dict]` and `is_valid(root) -> bool`
- `ResearchDocument(Document)` — source URL checks, draft marker, sources required
- `PlanDocument(Document)` — `tasks` field parsed from content, completion methods
- `ChainDocument(Document)` in `chain.py` — `steps` field, cycle/termination checks
- `WikiDocument(Document)` in `wiki.py` — schema conformance, wiki frontmatter checks
- `parse_document()` factory routes to the right subclass via lazy imports
- `validators.py` simplified: removes check functions that moved to classes, keeps project-level orchestration
- Dead code in `suffix.py` removed: `is_markdown` and `stem_name` have no callers outside tests

**Won't have:**
- `ContextDocument` subclass — content-length check stays in `validators.py`
- Changes to script entry points (`scripts/lint.py`, etc.) — orchestrator interfaces are stable
- Changes to skill SKILL.md files
- New features or validation rules beyond what currently exists

## Approach

Work in four chunks: **extend the base class and add simple subclasses** (Research,
Plan) in `document.py` first, then **add the complex subclasses** (Chain, Wiki) in
their own modules, then **strip the now-redundant check functions from validators.py**,
and finally **clean up dead code and thin the assess modules**.

Each chunk must leave the test suite fully green before moving on. The factory
`parse_document()` uses lazy imports (`from wos.chain import ChainDocument` inside
the function body) to avoid circular imports — `chain.py` and `wiki.py` import from
`document.py`, not the reverse at module level.

Type-specific checks belong on the subclass. Base class `issues()` covers only what
applies to every document: non-empty name/description and valid related paths.

## File Changes

**Modify:**
- `wos/document.py` — add `issues(root)` and `is_valid(root)` to `Document`; add `ResearchDocument` and `PlanDocument` subclasses; update `parse_document()` factory
- `wos/chain.py` — add `ChainDocument(Document)`; move `check_chain_*` functions to class methods; thin `validate_chain()`
- `wos/wiki.py` — add `WikiDocument(Document)`; move `check_wiki_schema_violations` and `check_wiki_frontmatter` to class methods; thin `validate_wiki()`
- `wos/validators.py` — remove `check_frontmatter`, `check_draft_markers`, `check_source_urls`, `check_related_paths`; update `validate_file` and `validate_project` to call `doc.issues(root)`
- `wos/research/assess_research.py` — use `ResearchDocument` properties directly; remove re-parsing of fields already on the doc
- `wos/plan/assess_plan.py` — remove `_parse_tasks` (moves to `PlanDocument`); read `doc.tasks` directly
- `wos/suffix.py` — remove `is_markdown` and `stem_name` (no production callers)
- `tests/test_document.py` — add tests for subclass construction, `issues()`, `is_valid()`, and factory routing
- `tests/test_validators.py` — update: remove tests for deleted check functions; update `validate_file` / `validate_project` tests to work with class-based validation
- `tests/test_chain.py` — update `TestParseChain` to test `ChainDocument`; add `ChainDocument.issues()` tests; existing structural check tests still pass via orchestrator
- `tests/test_wiki.py` — update to test `WikiDocument.issues()` directly; orchestrator tests stay
- `tests/test_suffix.py` — remove `TestIsMarkdown` and `TestStemName` test classes
- `tests/test_plan_assess.py` — update: `_parse_tasks` is gone; use `PlanDocument.tasks` instead

**No files deleted** — all existing modules shrink but remain.

---

## Chunk 1: Base class + ResearchDocument + PlanDocument

### Task 1: Add `issues()` and `is_valid()` to Document base class

Add two methods to the `Document` dataclass in `wos/document.py`. These implement the
base-level validation that applies to every document regardless of type:

- `issues(root: Path) -> list[dict]` — returns issues for empty `name`/`description`
  fields and for any path in `doc.related` that does not exist on disk relative to
  `root`. Each issue dict has keys `file`, `issue`, `severity`.
- `is_valid(root: Path) -> bool` — returns `True` if `issues(root)` contains no entry
  with `severity == "fail"`.

Do not add any type-specific logic here. The `related`-path check currently lives in
`check_related_paths()` in `validators.py` — copy that logic into `issues()` (it moves
here; the standalone function is removed in Task 6).

Update `tests/test_document.py` to cover: `issues()` returns empty list for a valid
document; returns fail issue for empty name; returns fail issue for a missing related
path; `is_valid()` returns False when there are fail issues.

**Files:** `wos/document.py`, `tests/test_document.py`

- [x] Add `issues(root: Path) -> list[dict]` to `Document` with base checks <!-- sha:d27bdbf -->
- [x] Add `is_valid(root: Path) -> bool` to `Document` <!-- sha:d27bdbf -->
- [x] Add tests to `tests/test_document.py` covering both methods <!-- sha:d27bdbf -->
- [x] Verify: `.venv/bin/python -m pytest tests/test_document.py -v` → all pass <!-- sha:d27bdbf -->
- [x] Commit <!-- sha:d27bdbf -->

---

### Task 2: Add ResearchDocument subclass

Add `ResearchDocument(Document)` to `wos/document.py`. It overrides `issues()` to
call `super().issues(root)` and extend with research-specific checks:

- Fail if `doc.sources` is empty
- Warn for each source that is a `dict` instead of a URL string
- Warn if `<!-- DRAFT -->` appears in `doc.content`
- Fail/warn for unreachable source URLs (reuse `check_urls` from `wos.url_checker`;
  403/429 → warn, others → fail). Add `verify_urls: bool = True` parameter to
  `issues()` to allow skipping in tests.

Convert `parse_document()` to a classmethod `Document.parse(path, text) -> Document`
that contains all routing logic. Keep `parse_document = Document.parse` as a
module-level alias so existing callers in validators.py, chain.py, wiki.py, etc.
need no changes. The classmethod routes `type: research` → `ResearchDocument`.

Add tests to `tests/test_document.py`: `ResearchDocument.issues()` returns fail for
missing sources; returns warn for draft marker; `parse_document()` returns a
`ResearchDocument` instance for `type: research` frontmatter.

**Files:** `wos/document.py`, `tests/test_document.py`

- [x] Add `ResearchDocument(Document)` class with `issues(root, verify_urls=True)` <!-- sha:33a716a -->
- [x] Update `parse_document()` to return `ResearchDocument` when type is `research` <!-- sha:33a716a -->
- [x] Add tests covering research-specific issues and factory routing <!-- sha:33a716a -->
- [x] Verify: `.venv/bin/python -m pytest tests/test_document.py -v` → all pass <!-- sha:33a716a -->
- [x] Commit <!-- sha:33a716a -->

---

### Task 3: Add PlanDocument subclass

Add `PlanDocument(Document)` to `wos/document.py`. Move `_parse_tasks()` from
`wos/plan/assess_plan.py` into `document.py` as a private module-level function.

`PlanDocument` adds:
- `tasks: list[dict]` field — `init=False`, populated in `__post_init__` by calling
  `_parse_tasks(self.content)`. Each task dict has keys: `index`, `title`,
  `completed`, `sha`.
- `tasks_complete() -> bool` — returns True if all tasks are completed
- `completion_stats() -> dict` — returns `{"total": N, "done": N, "remaining": N}`

`issues()` calls `super().issues(root)` and adds plan-specific checks (at minimum:
inherit from base — add more checks if obvious ones exist based on the current
`assess_plan.py` logic).

Update `parse_document()` factory: when `doc_type == "plan"`, return `PlanDocument`.

Update `wos/plan/assess_plan.py`: replace `_parse_tasks()` call with `doc.tasks`
(the field is now on the document). Remove the `_parse_tasks` function from that
module.

Add tests to `tests/test_document.py`: `PlanDocument.tasks` is populated from
content; `tasks_complete()` returns correct bool; factory returns `PlanDocument` for
`type: plan`. Update `tests/test_plan_assess.py` to remove tests for the deleted
`_parse_tasks` function and update `assess_file()` tests to work with `PlanDocument`.

**Files:** `wos/document.py`, `wos/plan/assess_plan.py`, `tests/test_document.py`, `tests/test_plan_assess.py`

- [x] Move `_parse_tasks()` from `assess_plan.py` to `document.py` <!-- sha:33a716a -->
- [x] Add `PlanDocument(Document)` with `tasks` field and completion methods <!-- sha:33a716a -->
- [x] Update `parse_document()` to return `PlanDocument` when type is `plan` <!-- sha:33a716a -->
- [x] Update `assess_plan.py` to use `doc.tasks` instead of calling `_parse_tasks` <!-- sha:bfcdec0 -->
- [x] Add/update tests <!-- sha:33a716a -->
- [x] Verify: `.venv/bin/python -m pytest tests/test_document.py tests/test_plan_assess.py -v` → all pass <!-- sha:bfcdec0 -->
- [x] Commit <!-- sha:33a716a -->

---

## Chunk 2: ChainDocument + WikiDocument

### Task 4: Add ChainDocument to chain.py

Add `ChainDocument(Document)` to `wos/chain.py`. It imports `Document` from
`wos.document`.

`ChainDocument` adds:
- `steps: list[dict]` field — `init=False`, populated in `__post_init__` by calling
  `_parse_steps_table(self.content, Path(self.path))`. If parsing raises `ValueError`
  (no Steps section), store an empty list and record the error for `issues()`.
- `issues(root: Path, skills_dirs: list[Path] = None) -> list[dict]` — calls
  `super().issues(root)` and adds: skill existence check (default `skills_dirs` to
  `[root / "skills"]` if None), termination condition check, cycle check. These are
  the logic currently in `check_chain_skills_exist()`, `check_chain_termination()`,
  and `check_chain_cycles()` — move that logic into the method body or private helpers
  on the class.

Update `parse_document()` in `document.py`: add a lazy import branch —
`if doc_type == "chain": from wos.chain import ChainDocument; return ChainDocument(...)`.

Simplify `validate_chain()` in `chain.py`: it should call `parse_document()` (which
returns a `ChainDocument`), then call `doc.issues(manifest_path.parent, skills_dirs)`.
The three standalone `check_chain_*` functions can be removed once their logic is on
the class.

Update `tests/test_chain.py`: `parse_chain()` now returns a `ChainDocument`;
`ChainDocument.issues()` tests replace the standalone check function tests;
`validate_chain()` orchestrator tests are unchanged.

**Files:** `wos/chain.py`, `wos/document.py`, `tests/test_chain.py`

- [x] Add `ChainDocument(Document)` with `steps` field and `issues()` method <!-- sha:91eb1b2 -->
- [x] Move `check_chain_*` logic into `ChainDocument.issues()` <!-- sha:91eb1b2 -->
- [x] Update `validate_chain()` to call `doc.issues()` <!-- sha:91eb1b2 -->
- [x] Add lazy import branch to `parse_document()` in `document.py` <!-- sha:91eb1b2 -->
- [x] Update `tests/test_chain.py` <!-- sha:91eb1b2 -->
- [x] Verify: `.venv/bin/python -m pytest tests/test_chain.py -v` → all pass <!-- sha:91eb1b2 -->
- [x] Commit <!-- sha:91eb1b2 -->

---

### Task 5: Add WikiDocument to wiki.py

Add `WikiDocument(Document)` to `wos/wiki.py`. It imports `Document` from
`wos.document`.

`WikiDocument` adds:
- `issues(root: Path, schema: dict = None) -> list[dict]` — calls `super().issues(root)`
  and adds: schema violation check (page_type, confidence_tier) and missing wiki
  frontmatter fields check (confidence, created, updated). If `schema` is None, the
  method attempts to load it from `(Path(self.path).parent / "SCHEMA.md")` relative
  to `root`; if SCHEMA.md is missing, skip schema checks.

Update `parse_document()` in `document.py`: add a lazy import branch —
`if doc_type == "wiki": from wos.wiki import WikiDocument; return WikiDocument(...)`.

Simplify `validate_wiki()` in `wiki.py`: parse schema once, then call `doc.issues(root,
schema=schema)` for each document in the wiki directory. Remove the standalone
`check_wiki_schema_violations()` and `check_wiki_frontmatter()` functions once their
logic is on the class.

Update `tests/test_wiki.py`: add `WikiDocument.issues()` tests; update orchestrator
tests.

**Files:** `wos/wiki.py`, `wos/document.py`, `tests/test_wiki.py`

- [x] Add `WikiDocument(Document)` with `issues(root, schema=None)` method <!-- sha:1dd77b2 -->
- [x] Move `check_wiki_schema_violations` and `check_wiki_frontmatter` logic into `WikiDocument.issues()` <!-- sha:1dd77b2 -->
- [x] Update `validate_wiki()` to call `doc.issues()` <!-- sha:1dd77b2 -->
- [x] Add lazy import branch to `parse_document()` in `document.py` <!-- sha:1dd77b2 -->
- [x] Update `tests/test_wiki.py` <!-- sha:1dd77b2 -->
- [x] Verify: `.venv/bin/python -m pytest tests/test_wiki.py -v` → all pass <!-- sha:1dd77b2 -->
- [x] Commit <!-- sha:1dd77b2 -->

---

## Chunk 3: Simplify validators.py

### Task 6: Strip individual check functions from validators.py

Remove from `wos/validators.py` the four functions whose logic has moved into classes:
`check_frontmatter`, `check_draft_markers`, `check_source_urls`, `check_related_paths`.

The context-related-field warning (previously in `check_frontmatter`:
`if doc.type == "context" and not doc.related`) has no subclass home — keep it as a
private helper or inline it in `validate_project`.

Update `validate_file()`: replace the four removed check function calls with a single
`doc.issues(root, verify_urls=verify_urls)` call. The content-length check
(`check_content`) stays and continues to be called separately.

Update `validate_project()`: same pattern — call `doc.issues(root)` per document
instead of the four removed functions.

Update `tests/test_validators.py`: remove tests for the four deleted functions; update
`validate_file` and `validate_project` tests to confirm they still surface the same
categories of issues via the class-based path.

**Files:** `wos/validators.py`, `tests/test_validators.py`

- [x] Remove `check_frontmatter`, `check_draft_markers`, `check_source_urls`, `check_related_paths` from `validators.py` <!-- sha:3f04c7c -->
- [x] Update `validate_file()` and `validate_project()` to call `doc.issues()` <!-- sha:3f04c7c -->
- [x] Update `tests/test_validators.py` <!-- sha:3f04c7c -->
- [x] Verify: `.venv/bin/python -m pytest tests/test_validators.py -v` → all pass <!-- sha:3f04c7c -->
- [x] Verify: `.venv/bin/python -m pytest tests/ -v` → all pass (full suite) <!-- sha:3f04c7c -->
- [x] Commit <!-- sha:3f04c7c -->

---

## Chunk 4: Dead code removal + assess module thinning

### Task 7: Remove dead suffix.py functions + thin assess modules

**suffix.py:** Remove `is_markdown` and `stem_name` — neither has any production
callers (confirmed: only `tests/test_suffix.py` references them). Remove the
corresponding test classes `TestIsMarkdown` and `TestStemName` from
`tests/test_suffix.py`.

**assess_research.py:** `parse_document()` now returns a `ResearchDocument` —
remove any re-extraction of fields that are already properties of the returned doc.
Specifically, anywhere the module re-reads `doc.type`, `doc.sources`, or calls
`parse_document()` a second time can be simplified to read from the doc directly.

**assess_plan.py:** Remove the `_parse_tasks` function (it moved to `document.py` in
Task 3). Update any remaining references to `_parse_tasks()` to read `doc.tasks`.

**Files:** `wos/suffix.py`, `tests/test_suffix.py`, `wos/research/assess_research.py`, `wos/plan/assess_plan.py`

- [x] Remove `is_markdown` and `stem_name` from `suffix.py` <!-- sha:bfcdec0 -->
- [x] Remove `TestIsMarkdown` and `TestStemName` from `tests/test_suffix.py` <!-- sha:bfcdec0 -->
- [x] Thin `assess_research.py` to read from `ResearchDocument` fields <!-- sha:bfcdec0 -->
- [x] Confirm `_parse_tasks` is removed from `assess_plan.py` (done in Task 3; verify here) <!-- sha:bfcdec0 -->
- [x] Verify: `.venv/bin/python -m pytest tests/ -v` → all pass <!-- sha:bfcdec0 -->
- [x] Commit <!-- sha:bfcdec0 -->

---

### Task 8: Final validation

Run the full test suite and lint to confirm zero regressions.

**Files:** none

- [x] Verify: `.venv/bin/python -m pytest tests/ -v` → all pass, 0 failures <!-- sha:bfcdec0 -->
- [x] Verify: `.venv/bin/python scripts/lint.py --root . --no-urls` → 0 fail findings (pre-existing fixture fail excluded) <!-- sha:bfcdec0 -->
- [x] Commit (bump or tag if appropriate) <!-- sha:bfcdec0 -->

---

## Validation

- [x] `.venv/bin/python -m pytest tests/ -v` — all tests pass, 0 failures <!-- sha:bfcdec0 -->
- [x] `.venv/bin/python scripts/lint.py --root . --no-urls` — 0 fail findings (pre-existing fixture fail excluded) <!-- sha:bfcdec0 -->
- [x] `parse_document('x.research.md', ...)` → `ResearchDocument` <!-- sha:bfcdec0 -->
- [x] `parse_document('x.plan.md', ...)` → `doc.tasks` list with one incomplete task <!-- sha:bfcdec0 -->
- [x] `grep -c "def check_frontmatter\|..." wos/validators.py` → `0` <!-- sha:bfcdec0 -->
- [x] `grep -c "def is_markdown\|def stem_name" wos/suffix.py` → `0` <!-- sha:bfcdec0 -->
