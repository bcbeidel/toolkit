---
name: wiki:lint bugfix batch
description: Fix cross-plugin check.skill dependency crash and wrong orphan warning message in wiki:lint
type: plan
status: completed
branch: fix/wiki-lint-bugs
related: []
---

## Goal

Fix two bugs that make `wiki:lint` broken or misleading out of the box:
1. `lint.py` crashes with `ModuleNotFoundError: No module named 'check'` whenever the `build` plugin isn't installed (#271/#273) — caused by an unconditional import of `check.skill`, a build-plugin module.
2. The orphan page warning in `wiki.py` tells users to run `/wos:ingest wiki/<page>.md`, which would re-ingest a local file as an external source — the wrong remediation (#274).

## Scope

**Must have:**
- `lint.py` runs without error when only the `wiki` plugin is installed
- Orphan page warning message points to the correct remediation
- `test_script_syspath.py` passes (currently fails due to ModuleNotFoundError)
- `test_wiki.py` orphan tests pass and assert the new message

**Won't have:**
- Alternative automated skill density reporting (removed, not replaced)
- Migration path for users relying on `--skill-max-lines` flag

## Approach

**Bug 1 (#271/#273):** The `from check.skill import check_skill_meta, check_skill_sizes` import in `lint.py` (line 105) is unconditional — it fires regardless of whether a `skills/` directory exists. Remove the entire density-reporting block (lines 104–135) and the `--skill-max-lines` argparse argument (lines 64–72) that only feeds it. The `lint` SKILL.md already delegates skill quality evaluation to `/wiki:check-skill` for LLM-level analysis; removing the Python layer is consistent with the design principle "quality in skills, structure in code."

**Bug 2 (#274):** The orphan message in `wiki.py:178–179` says `Run /wos:ingest wiki/<page>.md to index it`. Ingest is for external sources, not local wiki files. Update the message to point at `wiki/_index.md` directly or `/wiki:lint --fix`.

## File Changes

| File | Change |
|------|--------|
| `plugins/wiki/scripts/lint.py` | Remove `--skill-max-lines` arg (lines 64–72) and check.skill density block (lines 104–135) |
| `plugins/wiki/skills/lint/SKILL.md` | Update Skill Evaluation section: remove "automated Python checks" sentence; clarify all skill evaluation goes through `/wiki:check-skill` |
| `plugins/wiki/src/wiki/wiki.py` | Fix orphan warning message (lines 178–179) |
| `plugins/wiki/tests/test_wiki.py` | Update `TestCheckWikiOrphans.test_unindexed_file_returns_warn` to assert new message text |

## Tasks

- [x] Task 1: Remove `--skill-max-lines` argument and `check.skill` density block from `lint.py`. <!-- sha:2e495f1 -->
  - Delete the argparse `--skill-max-lines` block (lines 64–72 in current source).
  - Delete the skill density reporting block (lines 104–135: the `from check.skill import` line through the closing `print(file=sys.stderr)` and blank line).
  - Verify: `python3 plugins/wiki/scripts/lint.py --root . --no-urls` exits 0 and does not print `ModuleNotFoundError` or `No module named`.
  - Verify: `python3 plugins/wiki/scripts/lint.py --help` no longer shows `--skill-max-lines`.
  - Commit: `fix(wiki): remove cross-plugin check.skill import from lint.py (#271, #273)`

- [x] Task 2: Update lint SKILL.md to reflect removal of automated Python skill checks. <!-- sha:af0d1d6 -->
  - In `plugins/wiki/skills/lint/SKILL.md`, find the `## Skill Evaluation` section.
  - Remove the sentence "the automated Python checks (name format, description length/voice, body size, instruction density) appear in the standard issue table as usual."
  - Replace it with: "Skill quality evaluation is handled entirely by `/wiki:check-skill` — lint does not run automated Python-level skill checks."
  - Verify: `grep -n "automated Python checks" plugins/wiki/skills/lint/SKILL.md` returns no matches.
  - Commit: `docs(wiki): update lint SKILL.md — remove automated skill check reference (#271, #273)`

- [x] Task 3: Fix orphan warning message in `wiki.py` and update test. <!-- sha:9f4308d -->
  - In `plugins/wiki/src/wiki/wiki.py`, lines 178–179: replace the issue string with:
    `"Wiki page not in index. Add an entry to wiki/_index.md or run /wiki:lint --fix to regenerate the index."`
  - In `plugins/wiki/tests/test_wiki.py`, `TestCheckWikiOrphans.test_unindexed_file_returns_warn`: update the assertion to check for `"wiki/_index.md"` in the issue string instead of `"wos:ingest"`.
  - Verify: `python -m pytest plugins/wiki/tests/test_wiki.py::TestCheckWikiOrphans -v` — all 3 tests pass.
  - Commit: `fix(wiki): correct orphan page warning remediation message (#274)`

## Validation

1. Previously-failing syspath tests now pass:
   ```bash
   python -m pytest plugins/wiki/tests/test_script_syspath.py -v
   ```
   Expected: all tests pass, no `ModuleNotFoundError` in stderr.

2. Full wiki test suite passes:
   ```bash
   python -m pytest plugins/wiki/tests/ -v
   ```
   Expected: all tests pass (excluding pre-existing failures in `test_lint.py` from `check` import — those are resolved by Task 1).

3. `lint.py` runs without cross-plugin error on the toolkit itself:
   ```bash
   python3 plugins/wiki/scripts/lint.py --root . --no-urls
   ```
   Expected: exits 0 or exits 1 with content issues only — no `ModuleNotFoundError`.
