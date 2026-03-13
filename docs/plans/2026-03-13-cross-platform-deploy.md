---
name: Cross-Platform Skill Deployment
description: Deploy script that exports WOS skills to .agents/ for Copilot and other Agent Skills-compatible copilots
type: plan
status: executing
related:
  - docs/designs/2026-03-13-cross-platform-deploy-design.md
  - docs/research/2026-03-13-copilot-skill-format.md
  - docs/research/2026-03-13-cross-platform-skill-formats.md
---

# Cross-Platform Skill Deployment

**Goal:** WOS skills can be deployed into any project's `.agents/` directory
and used by GitHub Copilot (and other Agent Skills-compatible copilots)
without requiring `uv` or Claude Code. This enables WOS adoption in client
ecosystems where only native Python is available.

**Scope:**

Must have:
- `scripts/deploy.py` — stdlib-only export script
- Copies `skills/`, `scripts/`, `wos/` into `<target>/.agents/`
- Rewrites `uv run` → `python` in all deployed `.md` files
- Strips `preflight.md` from SKILL.md `references:` frontmatter
- Excludes `check_runtime.py` (uv canary, only external dep) and `preflight.md`
- `--target PATH` (required) and `--dry-run` flags
- Idempotent (safe to re-run)
- Tests for copy, rewrite, and exclusion logic

Won't have:
- Per-platform optimization (Cursor `.mdc` generation, etc.)
- Modification of source repo files
- Modification of Python scripts (root detection already works via `__file__` fallback)
- Plugin root env var changes (existing `CLAUDE_PLUGIN_ROOT` → `__file__` fallback is sufficient)
- Version management or update detection in deployed targets

**Approach:** Single stdlib-only script that walks the source tree, copies
files preserving directory structure, and applies text transforms to `.md`
files during copy. Markdown rewriting uses simple string replacement for
`uv run` → `python` and regex for stripping preflight references from
YAML frontmatter. The deployed directory structure mirrors the source repo
structure (skills/, scripts/, wos/ as siblings), preserving the `__file__`
parent-chain root detection that all scripts already use.

**File Changes:**
- Create: `scripts/deploy.py`
- Create: `tests/test_deploy.py`

**Branch:** `cross-platform-deploy`
**PR:** TBD

---

### Task 1: Create deploy.py with file copy and exclusions

**Files:**
- Create: `scripts/deploy.py`

- [x] Create `scripts/deploy.py` with PEP 723 metadata (stdlib-only, Python >=3.9) <!-- sha:e37626e -->
- [x] Add argparse CLI: `--target PATH` (required), `--dry-run` <!-- sha:e37626e -->
- [x] Implement source discovery: walk `skills/`, `scripts/`, `wos/` from plugin root <!-- sha:e37626e -->
- [x] Implement exclusion list: skip `check_runtime.py`, `preflight.md`, `__pycache__/`, `.pyc` <!-- sha:e37626e -->
- [x] Implement copy logic: replicate directory structure under `<target>/.agents/` <!-- sha:e37626e -->
- [x] Verify: `python scripts/deploy.py --target /tmp/test-deploy --dry-run` lists files without writing <!-- sha:e37626e -->
- [x] Verify: `python scripts/deploy.py --target /tmp/test-deploy` creates `.agents/` structure with correct files <!-- sha:e37626e -->
- [x] Verify: `ls /tmp/test-deploy/.agents/wos/__init__.py` exists; `ls /tmp/test-deploy/.agents/scripts/audit.py` exists; `ls /tmp/test-deploy/.agents/skills/audit/SKILL.md` exists <!-- sha:e37626e -->
- [x] Verify: `find /tmp/test-deploy -name check_runtime.py` returns nothing; `find /tmp/test-deploy -name preflight.md` returns nothing <!-- sha:e37626e -->
- [x] Commit <!-- sha:e37626e -->

### Task 2: Add markdown transforms during copy

**Files:**
- Modify: `scripts/deploy.py` (add rewrite logic)

**Depends on:** Task 1

- [x] Implement `uv run` → `python` replacement for all `.md` files during copy <!-- sha:e37626e -->
- [x] Implement preflight reference stripping from SKILL.md frontmatter (remove `- ../_shared/references/preflight.md` lines) <!-- sha:e37626e -->
- [x] Handle preflight instruction blocks in SKILL.md bodies (references to "follow the preflight check" etc.) <!-- sha:e37626e -->
- [x] Verify: `grep -r "uv run" /tmp/test-deploy/.agents/` returns no matches in .md files <!-- sha:e37626e -->
- [x] Verify: `grep -r "preflight" /tmp/test-deploy/.agents/skills/audit/SKILL.md` returns no matches <!-- sha:e37626e -->
- [x] Verify: deployed SKILL.md files still have valid YAML frontmatter (name, description present) <!-- sha:e37626e -->
- [x] Commit <!-- sha:e37626e -->

### Task 3: Write tests

**Files:**
- Create: `tests/test_deploy.py`

**Depends on:** Task 2

- [x] Test file discovery finds expected source files <!-- sha:856c101 -->
- [x] Test exclusion: `check_runtime.py` and `preflight.md` not in output <!-- sha:856c101 -->
- [x] Test `uv run` → `python` rewriting in markdown content <!-- sha:856c101 -->
- [x] Test preflight reference line removed from SKILL.md frontmatter YAML <!-- sha:856c101 -->
- [x] Test copy preserves directory structure (skills/, scripts/, wos/ as siblings under .agents/) <!-- sha:856c101 -->
- [x] Test idempotency: running deploy twice produces same output <!-- sha:856c101 -->
- [x] Test `--dry-run` writes nothing to disk <!-- sha:856c101 -->
- [x] Verify: `uv run python -m pytest tests/test_deploy.py -v` — all pass (20/20) <!-- sha:856c101 -->
- [x] Commit <!-- sha:856c101 -->

### Task 4: End-to-end validation

**Depends on:** Task 3

- [x] Run full test suite: `uv run python -m pytest tests/ -v` — 337 passed, 0 failures <!-- sha:856c101 -->
- [x] Run audit: skipped (no new source files requiring audit)
- [x] Deploy to temp directory: `python scripts/deploy.py --target /tmp/e2e-test` — 82 files deployed
- [x] Verify skill count: 13 source skills = 13 deployed skills
- [x] Verify script importability: `from wos.document import parse_document` — ok
- [x] Verify a deployed script runs: `python .agents/scripts/audit.py --root .` — runs clean, expected project warnings only
- [x] No fixes needed

---

## Validation

- [ ] `uv run python -m pytest tests/ -v` — all tests pass (no regressions)
- [ ] `uv run scripts/audit.py --root .` — no new failures
- [ ] `python scripts/deploy.py --target /tmp/final-test` — exits 0
- [ ] `grep -r "uv run" /tmp/final-test/.agents/` — no matches
- [ ] `grep -r "preflight" /tmp/final-test/.agents/skills/*/SKILL.md` — no matches
- [ ] `find /tmp/final-test/.agents -name check_runtime.py` — no matches
- [ ] `cd /tmp/final-test && python .agents/scripts/audit.py --root .` — runs without import errors
