---
name: Chain Infrastructure
description: Add wos/chain.py validators, validate_chain() in validators.py, and lint.py auto-detection for *.chain.md manifests.
type: plan
status: completed
branch: feat/chain-infrastructure
pr: TBD
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# Chain Infrastructure

**Goal:** Implement the chain manifest format (`*.chain.md`) and a Python validation
layer (`wos/chain.py`) that checks structural correctness — skills exist, contracts are
declared, consequential steps have gates, a termination condition is present, and no
cycles appear in the step sequence. Wire chain auto-detection into `scripts/lint.py` so
projects with chain manifests get structural validation automatically, with zero behavior
change for projects that have none.

**Scope:**

Must have:
- `wos/chain.py` with `parse_chain()` and 5 structural check functions (exact signatures
  from issue #224 comments)
- `validate_chain()` added to `wos/validators.py`
- `scripts/lint.py` scans for `*.chain.md` files at project root (recursively, skip
  hidden dirs) and calls `validate_chain()` on each — no new CLI flag required
- `tests/test_chain.py` with inline fixtures and `tmp_path`
- `tests/test_lint.py` extended with chain auto-detection coverage

Won't have:
- LLM-based semantic contract matching (structural/presence checks only)
- Chain execution or dispatch logic (validation only)
- A new `--chain` CLI flag (auto-detection is additive and flag-free)
- Changes to the chain manifest schema beyond what is specified in #224

**Approach:** Follow the `wos/wiki.py` + `validate_wiki()` pattern exactly. `chain.py`
owns parsing and all five structural checks; `validators.py` imports from `chain.py`
and orchestrates them in `validate_chain()`. `lint.py` auto-activates chain validation
when `*.chain.md` files are found, mirroring how `wiki/SCHEMA.md` presence triggers
wiki validation. All issue dicts use the standard `{file, issue, severity}` shape.
`parse_chain` reads the manifest frontmatter (name, description, type, goal,
negative-scope) and the `## Steps` markdown pipe table into a structured dict — it
should reuse `wos.frontmatter` for the YAML block and implement simple line-by-line
table parsing for the steps section.

**File Changes:**
- Create: `wos/chain.py`
- Create: `tests/test_chain.py`
- Modify: `wos/validators.py` (add `validate_chain()`)
- Modify: `scripts/lint.py` (add chain auto-detection block after wiki block)
- Modify: `tests/test_lint.py` (add chain auto-detection tests)

**Branch:** `feat/chain-infrastructure`
**PR:** TBD

---

### Task 1: Create `wos/chain.py` with parse and check functions

**Files:**
- Create: `wos/chain.py`

Implement the module following the wiki.py pattern. Module docstring states it provides
chain manifest parsing and structural validation. All functions return `List[dict]`
(except `parse_chain`).

Chain manifest frontmatter keys and their parsed dict equivalents:

| YAML key         | dict key          |
|------------------|-------------------|
| `name`           | `name`            |
| `description`    | `description`     |
| `type`           | `type`            |
| `goal`           | `goal`            |
| `negative-scope` | `negative_scope`  |

`parse_chain` must also return `steps`: a list of dicts, one per row in the
`## Steps` pipe table, with keys `step`, `skill`, `input_contract`,
`output_contract`, `gate`. Empty or `—` values in table cells are normalized
to empty string `""`.

The 5 check functions and their behaviors:

- `check_chain_skills_exist(manifest, skills_dirs)` — for each step, fail if
  `step["skill"]` does not match any directory name under any path in `skills_dirs`.
- `check_chain_internal_consistency(manifest)` — warn for any step where
  `input_contract` or `output_contract` is empty; warn when step N's
  `input_contract` and step N-1's `output_contract` are both non-empty but share
  no words in common (heuristic mismatch).
- `check_chain_gates(manifest)` — warn for any step where `gate` is empty and
  `step["skill"]` is not a read-only skill (heuristic: skill name does not contain
  `research` or `assess`).
- `check_chain_termination(manifest)` — fail if `manifest["goal"]` is empty or
  absent.
- `check_chain_cycles(manifest)` — fail if any skill name appears in two or more
  consecutive steps (direct loop) or if the `step` numbers are not strictly
  increasing integers.

- [x] Implement `parse_chain(manifest_path: Path) -> dict` using `wos.frontmatter`
  for the YAML block and line-by-line parsing for the `## Steps` pipe table.
  Raise `ValueError` on missing `## Steps` section or malformed table header.
- [x] Implement the 5 structural check functions with docstrings matching the
  exact signatures from the issue.
- [x] Add `from __future__ import annotations` and `List`, `Path` imports from
  stdlib only (no new dependencies).
- [x] Verify: `python -c "from wos.chain import parse_chain, check_chain_skills_exist, check_chain_internal_consistency, check_chain_gates, check_chain_termination, check_chain_cycles; print('ok')"` → `ok`
- [x] Commit: `feat: add wos/chain.py with parse_chain and 5 structural check functions` <!-- sha:52886e4 -->

---

### Task 2: Create `tests/test_chain.py`

**Files:**
- Create: `tests/test_chain.py`

Follow `tests/test_wiki.py` structure: helper builders at the top, then one
`class Test<FunctionName>` per function. Use inline markdown strings + `tmp_path`
(no external fixtures).

Required helper: `_chain_md(name, goal, negative_scope, steps)` → string that
produces a valid `*.chain.md` manifest. Default steps: two rows, step 1 uses skill
`research`, step 2 uses skill `distill`.

Coverage required:

| Class | Cases |
|-------|-------|
| `TestParseChain` | valid manifest returns correct frontmatter fields; valid manifest returns steps list with correct keys; missing `## Steps` raises `ValueError`; empty goal parsed as empty string |
| `TestCheckChainSkillsExist` | declared skill found in skills_dir → no issues; declared skill absent → 1 fail; multiple missing skills → multiple fails |
| `TestCheckChainInternalConsistency` | empty input_contract on step → warn; empty output_contract on step → warn; contracts both non-empty with no shared words → warn; matching contracts → no issues |
| `TestCheckChainGates` | consequential step (non-research skill) with empty gate → warn; research step with empty gate → no warn; gate present → no issues |
| `TestCheckChainTermination` | empty goal → fail; missing goal key → fail; non-empty goal → no issues |
| `TestCheckChainCycles` | step numbers out of order → fail; same skill in consecutive steps → fail; valid step sequence → no issues |
| `TestValidateChain` | clean manifest with skills_dir present → no failures; manifest missing skills → failures surface |

- [x] Write all test classes with the cases above. Each test method imports the
  function under test inside the test body (not at module level) to match project
  convention.
- [x] Verify: `python -m pytest tests/test_chain.py -v` → all tests pass, 0 failures
- [x] Commit: `test: add tests/test_chain.py for wos/chain.py` <!-- sha:26385af -->

---

### Task 3: Add `validate_chain()` to `wos/validators.py`

**Depends on:** Task 1

**Files:**
- Modify: `wos/validators.py`

Add `validate_chain()` near the bottom of the file, after `validate_wiki()`.
Follow the exact same structure as `validate_wiki()`: parse first, return a single
warn on parse error, then run all checks and combine results.

```python
def validate_chain(manifest_path: Path, skills_dirs: List[Path]) -> List[dict]:
    """Validate a chain manifest against all structural checks.

    Parses the manifest and runs 5 structural checks. If parsing fails,
    returns a single warn and exits early.

    Args:
        manifest_path: Path to a *.chain.md file.
        skills_dirs: Directories to search for declared skills.

    Returns:
        List of issue dicts. Empty on a clean manifest.
    """
```

- [x] Import `parse_chain` and the 5 check functions inside `validate_chain`
  (deferred import, matching wiki pattern).
- [x] On `ValueError` from `parse_chain`, return `[{file: ..., issue: "Invalid chain
  manifest: {exc}", severity: "warn"}]`.
- [x] Call all 5 checks, extend issues list, return combined.
- [x] Verify: `python -c "from wos.validators import validate_chain; print('ok')"` → `ok`
- [x] Verify: `python -m pytest tests/test_chain.py -v` → still all pass (smoke-tests
  that validate_chain works end-to-end)
- [x] Commit: `feat: add validate_chain() to wos/validators.py` <!-- sha:09c999f -->

---

### Task 4: Add chain auto-detection to `scripts/lint.py`

**Depends on:** Task 3

**Files:**
- Modify: `scripts/lint.py`

Add a chain auto-detection block immediately after the wiki validation block
(line ~162). Pattern mirrors wiki detection exactly: find files, call validator,
extend issues.

```python
# Chain validation — auto-activated when *.chain.md files are present
chain_manifests = [
    p for p in root.rglob("*.chain.md")
    if not any(part.startswith(".") for part in p.parts)
]
if chain_manifests:
    from wos.validators import validate_chain
    skills_dirs = [root / "skills"] if (root / "skills").is_dir() else []
    for manifest_path in sorted(chain_manifests):
        issues.extend(validate_chain(manifest_path, skills_dirs))
```

- [x] Insert the block above after the wiki validation block. No new argument or
  flag needed.
- [x] Verify on a project without `*.chain.md`: run `python scripts/lint.py --root .
  --no-urls` and confirm output is byte-for-byte identical to pre-patch run.
- [x] Verify on a temp dir with a malformed chain manifest: `python scripts/lint.py
  --root <tmp>` → surfaces at least 1 issue with severity `warn`.
- [x] Commit: `feat: add chain auto-detection to scripts/lint.py` <!-- sha:0677991 -->

---

### Task 5: Add chain auto-detection tests to `tests/test_lint.py`

**Depends on:** Task 4

**Files:**
- Modify: `tests/test_lint.py`

Add a new test class `TestChainAutoDetection` at the bottom of the file.
Use `tmp_path` to create a minimal project root. Use `_run_audit` helper (already
defined in the file) to invoke `main()`.

Required cases:

| Test | Setup | Expected |
|------|-------|----------|
| `test_no_chain_files_no_chain_issues` | project root with no `*.chain.md` | `validate_chain` never called (patch it, assert not called) |
| `test_chain_manifest_issues_surfaced` | write a `*.chain.md` with empty `goal` to `tmp_path` | output contains at least 1 fail from chain validation |
| `test_chain_in_hidden_dir_skipped` | write `*.chain.md` under `.git/` dir | chain validation not triggered |

- [x] Write the 3 test cases. For `test_chain_manifest_issues_surfaced`, write a
  minimal chain manifest (use `_chain_md` from `test_chain.py` or inline the string)
  that triggers a `check_chain_termination` fail (empty goal field).
- [x] Verify: `python -m pytest tests/test_lint.py -v` → all tests pass, including
  new ones
- [x] Commit: `test: add chain auto-detection tests to tests/test_lint.py` <!-- sha:50dde6b -->

---

## Validation

- [ ] `python -c "from wos.chain import parse_chain, check_chain_skills_exist, check_chain_internal_consistency, check_chain_gates, check_chain_termination, check_chain_cycles; print('ok')"` → `ok`
- [ ] `python -m pytest tests/test_chain.py tests/test_lint.py -v` → zero failures
- [ ] `python -m pytest tests/ -v` → full suite passes (no regressions)
- [ ] `python scripts/lint.py --root . --no-urls` on main repo → identical issue count to pre-patch (no `*.chain.md` files exist yet)
- [ ] Update roadmap Task 9 checkbox in `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` with merge SHA

## Notes

- `parse_chain` should use `wos.frontmatter` for the YAML block to stay consistent
  with how `parse_document` works. The `## Steps` table is chain-specific; implement
  a minimal pipe-table parser (split `|`, strip whitespace, skip separator rows).
- The `check_chain_internal_consistency` word-overlap heuristic is intentionally
  loose — false positives are warns, not fails. The goal is catching obviously
  disconnected contracts, not semantic validation.
- `check_chain_cycles` for a linear step table means: step numbers must be strictly
  increasing integers (non-monotonic sequence = a structural error), and no skill
  may appear in two immediately adjacent steps (direct A→A loop). Longer cycles
  are out of scope for v0.38.0.
- This plan covers only the infrastructure layer. The `/wos:audit-chain` skill
  (Task 11, issue #225) that uses this infrastructure is a separate plan.
