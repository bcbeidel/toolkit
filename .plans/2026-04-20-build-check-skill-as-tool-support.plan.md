---
name: build-skill and check-skill support for --as-tool pattern
description: Ship shared as-tool-contract reference, teach build-skill to scaffold the pattern via two-level intake (opt-in + DATA/ARTIFACT shape), extend check-skill with 9 new checks, and bump build plugin to 0.5.0.
type: plan
status: executing
branch: feat/build-skill-as-tool-support
related:
  - .designs/2026-04-20-build-check-skill-as-tool-support.design.md
---

# build-skill and check-skill Support for `--as-tool` Pattern

## Goal

Teach `/build:build-skill` and `/build:check-skill` to treat the `--as-tool` dual-invocation pattern as a first-class skill shape. After this plan lands:

- `plugins/build/_shared/references/as-tool-contract.md` exists as the single authoritative mechanism spec; both `build-skill` and `check-skill` reference it.
- `/build:build-skill` intake asks two questions (opt-in y/N → if y, DATA or ARTIFACT + artifact types); scaffolds the contract section, workflow split, and frontmatter entries accordingly.
- `/build:check-skill` runs 9 new checks (23–31) covering `skill-invocable` frontmatter shape, contract-section presence, Return-shape declaration, all-three-cases coverage, ARTIFACT artifact-types, and non-invocable pathology.
- New Python static checks live in `plugins/build/src/check/skill.py` alongside the existing 22; tests cover each new check.
- Build plugin bumps to 0.5.0.
- All 41 existing SKILL.md files still pass with zero new fail-level findings (no migration).

## Scope

### Must have

- `plugins/build/_shared/references/as-tool-contract.md` created as a skill-agnostic spec documenting: `$ARGUMENTS` four-mode parsing rule; skip/run-per-step semantics under `--as-tool`; three-case envelope (Success / NeedsMoreInfo / Refusal); two return shapes (DATA JSON-only, ARTIFACT JSON envelope + N fenced blocks); emission examples for each; language-tag-per-MIME rule; parallel-safety default; freeform-text mode; when to pick DATA vs ARTIFACT.
- `plugins/build/skills/build-skill/SKILL.md` updated with: intake question added under Interview and Research; new conditional section in Draft describing what to scaffold when `skill-invocable: true`; both DATA and ARTIFACT scaffold variants documented; reference to the shared contract added to `references:` frontmatter.
- `plugins/build/skills/build-skill/references/skill-writing-guide.md` gains a new H2 section on the dual-invocation pattern, pointing at the dummy plugin's `/dummy:greet` (DATA) as the canonical example.
- `plugins/build/skills/check-skill/SKILL.md` updated to document the 9 new checks (23–31) with severities per the design; reference to the shared contract added.
- `plugins/build/src/check/skill.py` gains 9 new `_check_*` functions wired into the check dispatcher; each returns findings in the existing format.
- `plugins/build/tests/test_skill_audit.py` gains tests for each new check covering pass and fail cases.
- `plugins/build/pyproject.toml` and `plugins/build/.claude-plugin/plugin.json` bump to 0.5.0.
- `/build:check-skill` against all 41 existing SKILL.md files produces zero **new** fail-level findings attributable to the new checks.
- PR opened against `main`; CI green (ruff).

### Won't have

- **Migration of existing 41 skills.** No bulk-add of `skill-invocable: false`. Absent = default off.
- **Refactor of hook/shell pair.** Issue #327's original scope; downstream consumer of this work.
- **Dummy plugin changes.** `/dummy:greet` and `/dummy:greet-team` remain as-is.
- **LLM-judgment check** verifying declared contract matches actual workflow semantics. Deterministic presence-checks only.
- **New skill-generation CLI** or helper script for retrofitting existing skills to the pattern.
- **`/build:as-tool-migrate` skill** or any bulk-migration tooling.
- **Blocking hook** to enforce the pattern at commit time.
- **Cross-plugin invocation test harness.** Dummy plugin already proves the mechanism works.
- **Graduation to required declaration** (Q1 Option C from scoping). Deferred until 3+ real adopters exist.
- **`.claude-plugin/marketplace.json` changes.** Manifest references the plugin, not per-skill.
- **Changes outside the `build` plugin.** No edits to wiki, work, consider, or dummy.

## Approach

**Bottom-up order, chunked.** Write the shared contract first — it's the authoritative spec that both `build-skill` (scaffolder) and `check-skill` (auditor) reference. Once the contract is fixed, update `build-skill` to scaffold against it. Then update `check-skill` + Python lint code + tests to audit against it. Release gates (self-audit + version bump + PR) come last.

**Each chunk produces something self-verifiable.**
- Chunk 1 (shared contract): a file on disk with ≥7 top-level sections covering both shapes.
- Chunk 2 (build-skill): SKILL.md prose describes the two-level intake and both scaffold variants; skill-writing-guide has the new H2.
- Chunk 3 (check-skill): SKILL.md documents 9 new checks; Python adds 9 `_check_*` functions; tests cover each.
- Chunk 4 (release): all four modified SKILL.md files pass self-audit; version bumped; PR opened.

**Test-first for the Python checks.** For each new `_check_*` function, write the test first (pass fixture + fail fixture), then the implementation. Keeps the severity contract honest (fail-case fixtures trigger fail; pass-case fixtures don't).

**Fixture-based audit regression test.** Before closing Chunk 3, run `/build:check-skill` (or invoke the lint script directly) against all existing skills to confirm zero new fail findings. This is the guardrail against accidentally requiring the new frontmatter on skills that opted not to adopt.

**No dummy plugin edits.** The dummy plugin is the working reference implementation. Touching it to "align" with the new contract is scope creep — the contract is derived from it, not the other way around. If the contract ends up demanding something the dummy doesn't have, flag as infeasibility and loop back to scope-work.

## File Changes

| File | Change |
|------|--------|
| `plugins/build/_shared/references/as-tool-contract.md` | **Create** — authoritative generic spec: parsing rule, step-skip semantics, three-case envelope, DATA vs ARTIFACT shapes with emission examples, parallel-safety, when-to-use guidance. |
| `plugins/build/skills/build-skill/SKILL.md` | **Modify** — add intake question (§3 Interview), new conditional scaffolding subsection (§4 Draft), reference to shared contract in frontmatter `references:`. |
| `plugins/build/skills/build-skill/references/skill-writing-guide.md` | **Modify** — add H2 section on the dual-invocation pattern, cite shared contract + dummy plugin's greet. |
| `plugins/build/skills/check-skill/SKILL.md` | **Modify** — add 9 new checks (23–31) to the Run Checks table with severities; reference shared contract. |
| `plugins/build/src/check/skill.py` | **Modify** — add 9 new `_check_*` functions; wire into the main dispatcher. |
| `plugins/build/tests/test_skill_audit.py` | **Modify** — add pass/fail test cases for each new `_check_*`. |
| `plugins/build/pyproject.toml` | **Modify** — version `0.4.0` → `0.5.0`. |
| `plugins/build/.claude-plugin/plugin.json` | **Modify** — version `0.4.0` → `0.5.0`. |

No deletions. No new skills. No Python package-structure changes.

## Tasks

### Chunk 1: Shared contract

#### Task 1: Create `as-tool-contract.md`

- [x] Task 1: Create `as-tool-contract.md` <!-- sha:7089c0e -->

Create `plugins/build/_shared/references/as-tool-contract.md` per the design. Skill-agnostic. Required sections (as H2s, in this order):

- **Purpose** — one-paragraph summary of the pattern and when to reach for it.
- **Parsing rule** — the four-mode `$ARGUMENTS` table (empty / freeform / `key=value` / `--as-tool`).
- **Step skip/run under `--as-tool`** — Route (runs), Scope Gate (runs), Elicit (skipped), Draft/Computation (runs), Safety Check (runs, findings into payload), Review Gate (skipped), Save (skipped), Test handoff (skipped).
- **Envelope — three cases** — Success / NeedsMoreInfo / Refusal; rule that `NeedsMoreInfo` and `Refusal` are always JSON-only regardless of shape.
- **Return shape DATA** — JSON only; schema example with `{type, value}`; rule that `value` is a structured object declared by the skill.
- **Return shape ARTIFACT** — JSON envelope + N fenced code blocks; `artifact_types` array rule; language-tag-per-MIME rule (`application/json` → `json`, `text/x-shellscript` → `bash`, `text/markdown` → `markdown`); single-artifact and multi-artifact emission examples.
- **When to pick DATA vs ARTIFACT** — rule of thumb: structured records → DATA, code/markdown/config → ARTIFACT.
- **Parallel-safety** — default yes; document `no` with reason when the skill serializes.
- **Freeform-text human mode** — one paragraph noting voice-dictated intent is a first-class human shape; does not apply under `--as-tool`.
- **When NOT to use the pattern** — exploratory skills, mental-model skills, skills where human judgment is the deliverable.

**Verify:**
```
test -f plugins/build/_shared/references/as-tool-contract.md
grep -c "^## " plugins/build/_shared/references/as-tool-contract.md    # returns ≥ 9
```

**Commit:** `docs(build): add as-tool-contract shared reference`

### Chunk 2: build-skill

#### Task 2: Update `build-skill` SKILL.md

- [x] Task 2: Update `build-skill` SKILL.md <!-- sha:919ea28 -->

Modify `plugins/build/skills/build-skill/SKILL.md`:

- Add `../../_shared/references/as-tool-contract.md` to frontmatter `references:`.
- In §3 Interview and Research, append a new structural-decision bullet:
  > **Should this skill be invocable by other skills via `--as-tool`?** If yes, the skill supports a dual-invocation pattern (human mode + skill-caller mode). Default: no — most skills are human-only. See `../../_shared/references/as-tool-contract.md`.
- Add a second follow-up to the above: if yes, ask whether the skill returns **DATA** (structured object) or **ARTIFACT** (text file like a script, markdown, or config). If ARTIFACT, ask for the `artifact_types` list.
- In §4 Draft (the scaffolding step), add a new subsection **"If `skill-invocable: true`"** specifying:
  - Frontmatter additions: `skill-invocable: true`; `references:` entry pointing at the shared contract.
  - Skill intro: two-mode description ("Human mode: prompts / approval / save. `--as-tool` mode: structured emission per the contract.").
  - Workflow split into `§Xa. Human mode` and `§Xb. --as-tool mode`, with the `--as-tool mode` step instructing the emission format (JSON only for DATA; JSON envelope + fenced blocks for ARTIFACT).
  - `## --as-tool contract` section with the four subsections (Required fields / Return shape / Side effects / Parallel-safe) populated from intake.
  - Key Instructions entries enforcing mode-specific rules.
- Cross-reference the canonical example: `/dummy:greet` (DATA).

**Verify:**
```
grep -c "as-tool-contract" plugins/build/skills/build-skill/SKILL.md     # ≥ 1 (frontmatter reference)
grep -c "skill-invocable" plugins/build/skills/build-skill/SKILL.md      # ≥ 2 (intake question + Draft section)
grep -c "DATA\|ARTIFACT" plugins/build/skills/build-skill/SKILL.md       # ≥ 4 (shape-related prose)
```

**Commit:** `feat(build-skill): add --as-tool two-level intake and conditional scaffolding`

#### Task 3: Update `skill-writing-guide.md`

- [x] Task 3: Update `skill-writing-guide.md` <!-- sha:0226efe -->

Modify `plugins/build/skills/build-skill/references/skill-writing-guide.md`:

- Add a new H2: **"The Dual-Invocation Pattern (`--as-tool`)"**.
- One-paragraph overview of the pattern: what it is, why it exists.
- Pointer at the shared contract for the authoritative mechanism spec.
- Pointer at `plugins/dummy/skills/greet/SKILL.md` as the canonical DATA example.
- Note (for now): no canonical ARTIFACT example exists yet; the design references `build-shell` as the future canonical ARTIFACT example once #327 lands.
- Criteria for when to opt in (produces something consumable by another skill; computation is reusable; inputs can be pre-filled by a caller).
- Criteria for when NOT to opt in (exploratory skill, interactive-by-design, human judgment is the deliverable).

**Verify:**
```
grep -c "^## .*Dual-Invocation\|^## .*as-tool" plugins/build/skills/build-skill/references/skill-writing-guide.md   # ≥ 1
grep "plugins/dummy/skills/greet" plugins/build/skills/build-skill/references/skill-writing-guide.md
```

**Commit:** `docs(build-skill): add dual-invocation pattern to skill-writing-guide`

### Chunk 3: check-skill

#### Task 4: Add 9 new `_check_*` functions in Python

- [x] Task 4: Add 9 new `_check_*` functions in Python <!-- sha:025236f -->

Modify `plugins/build/src/check/skill.py`. Add these functions following the existing `_check_*` style (return `List[dict]` with `check_id`, `severity`, `message`, `line` fields matching existing checks):

- `_check_skill_invocable_boolean(frontmatter, file_str) -> List[dict]` — check 23 (warn). Fires when `skill-invocable` is present but non-boolean.
- `_check_contract_section_present(frontmatter, body, file_str) -> List[dict]` — check 24 (fail). Fires when `skill-invocable: true` but no `## --as-tool contract` (or `##  \`--as-tool\` contract`) H2 in body (or section empty).
- `_check_contract_return_shape_declared(frontmatter, body, file_str) -> List[dict]` — check 25 (fail). Inside contract section: must contain a `**Return shape:**` line declaring `DATA` or `ARTIFACT`.
- `_check_contract_all_three_cases(frontmatter, body, file_str) -> List[dict]` — check 26 (fail). Inside contract section: must mention `Success`, `NeedsMoreInfo`, and `Refusal` at least once each.
- `_check_contract_artifact_types(frontmatter, body, file_str) -> List[dict]` — check 27 (fail). When Return shape is ARTIFACT: must contain a `**Artifact types:**` line with at least one MIME-type-shaped value.
- `_check_contract_required_fields(frontmatter, body, file_str) -> List[dict]` — check 28 (warn). Inside contract section: must contain a `**Required fields:**` subsection with at least one list item (or `"none"`).
- `_check_contract_side_effects(frontmatter, body, file_str) -> List[dict]` — check 29 (warn). Inside contract section: must contain a `**Side effects:**` line.
- `_check_contract_parallel_safe(frontmatter, body, file_str) -> List[dict]` — check 30 (warn). Inside contract section: must contain a `**Parallel-safe:**` line.
- `_check_non_invocable_pathology(frontmatter, file_str) -> List[dict]` — check 31 (warn). Fires when `user-invocable: false` AND (`skill-invocable: false` or absent).

Wire each function into the main `check_skill_meta` dispatcher (or equivalent aggregator — read the existing file to match its dispatcher pattern). Skills with `skill-invocable: false` or absent must not trigger checks 24–30.

Preserve existing check behavior. Order findings by check_id for deterministic output.

**Verify:**
```
grep -c "^def _check_skill_invocable_boolean\|^def _check_contract_\|^def _check_non_invocable_pathology" \
  plugins/build/src/check/skill.py   # returns 9
ruff check plugins/build/src/check/skill.py
```

**Commit:** `feat(check-skill): add 9 --as-tool contract checks to Python lint`

#### Task 5: Add tests for each new check

- [x] Task 5: Add tests for each new check <!-- sha:830517f -->

Modify `plugins/build/tests/test_skill_audit.py`. For each of the 9 new `_check_*` functions, add at least one **pass-case** (clean input, no findings) and one **fail-case** (triggering input, produces finding with correct severity). Use inline markdown fixtures per the existing test style (no file I/O for fixtures beyond `tmp_path`).

Required fail-case coverage:
- Check 23: `skill-invocable: maybe` (non-boolean) → warn.
- Check 24: `skill-invocable: true`, no `## --as-tool contract` section → fail.
- Check 25: contract section present but no `**Return shape:**` line → fail.
- Check 26: contract section present but missing `NeedsMoreInfo` (or any of the three cases) → fail.
- Check 27: `**Return shape:** ARTIFACT` but no `**Artifact types:**` line → fail.
- Check 28: contract section present but no `**Required fields:**` → warn.
- Check 29: no `**Side effects:**` → warn.
- Check 30: no `**Parallel-safe:**` → warn.
- Check 31: `user-invocable: false` and no `skill-invocable` → warn.

Required pass-case coverage:
- Opt-out skill (`skill-invocable: false` or absent) with no contract section: checks 24–30 must NOT fire.
- DATA-shape opted-in skill with all required subsections: no findings from 23–31.
- ARTIFACT-shape opted-in skill with Artifact types and all required subsections: no findings from 23–31.

**Verify:**
```
python3 -m pytest plugins/build/tests/test_skill_audit.py -v
```
All tests pass, including the new ones.

**Commit:** `test(check-skill): add fixtures for --as-tool contract checks`

#### Task 6: Update `check-skill` SKILL.md

- [x] Task 6: Update `check-skill` SKILL.md <!-- sha:e6ca1e2 -->

Modify `plugins/build/skills/check-skill/SKILL.md`:

- Add `../../_shared/references/as-tool-contract.md` to frontmatter `references:`.
- Extend the Run Checks section's structural-checks table with rows 23–31 per the design's severity calibration.
- Update the opening paragraph that counts the checks ("twenty-two research-backed quality criteria" → "thirty-one").
- Add a brief explanatory paragraph pointing at the shared contract doc for the mechanism.

**Verify:**
```
grep -c "as-tool-contract" plugins/build/skills/check-skill/SKILL.md   # ≥ 1
grep -c "skill-invocable\|--as-tool contract" plugins/build/skills/check-skill/SKILL.md   # ≥ 3
grep -E "thirty|31|twenty-two|22" plugins/build/skills/check-skill/SKILL.md | head   # confirm count updated
```

**Commit:** `feat(check-skill): document 9 --as-tool contract checks in SKILL.md`

#### Task 7: Regression-check existing skills

- [x] Task 7: Regression-check existing skills <!-- sha:e6ca1e2 verified --> (lint.py clean; 0 new fail findings across 41 existing skills)

Run `/build:check-skill` (or invoke the lint script directly: `python3 plugins/wiki/scripts/lint.py --root . --no-urls`) against the repo to confirm zero new fail-level findings on the 41 existing skills.

If any new fail fires on a pre-existing skill, investigate: either (a) the skill was secretly dual-invocation and declared inconsistently (fix the skill), or (b) the check is over-eager (adjust the check).

**Verify:**
```
python3 plugins/wiki/scripts/lint.py --root . --no-urls 2>&1 | \
  grep -E "check_id.*(23|24|25|26|27|28|29|30|31)" | grep -c "severity.*fail"
# expect 0 on existing skills
```

**Commit:** None, unless a fix to an existing skill or check is needed.

### Chunk 4: Release

#### Task 8: Self-audit modified SKILL.md files

- [x] Task 8: Self-audit modified SKILL.md files <!-- sha:e6ca1e2 verified --> (lint.py clean on build-skill/SKILL.md, check-skill/SKILL.md; 0 fails)

Run `/build:check-skill` against each of the four modified SKILL.md files:
- `plugins/build/skills/build-skill/SKILL.md`
- `plugins/build/skills/check-skill/SKILL.md`
- `plugins/build/skills/build-skill/references/skill-writing-guide.md` is a reference file, not a SKILL.md — skip the skill-audit but manually inspect it for coherence.

For any fail-level finding, fix in place and re-audit. Warns acceptable if pre-existing or explicitly accepted.

**Verify:** Zero fail-level findings on the two SKILL.md files from their own audit.

**Commit:** None if no fixes needed. If fixes made: `fix(build): resolve check-skill findings from --as-tool support refactor`.

#### Task 9: Bump build plugin version to 0.5.0

- [ ] Task 9: Bump build plugin version to 0.5.0

Edit `plugins/build/pyproject.toml`: `version = "0.4.0"` → `version = "0.5.0"`.
Edit `plugins/build/.claude-plugin/plugin.json`: `"version": "0.4.0"` → `"version": "0.5.0"`.

**Verify:**
```
grep version plugins/build/pyproject.toml plugins/build/.claude-plugin/plugin.json
# both show 0.5.0
```

**Commit:** `chore(build): bump to 0.5.0 for --as-tool pattern support`

#### Task 10: Open PR

- [ ] Task 10: Open PR

Push branch `feat/build-skill-as-tool-support` and open PR against `main`:

- Title: `feat(build): --as-tool pattern support in build-skill and check-skill (build-0.5.0)`
- Body: Summary bullets (shared contract doc, two-level intake in build-skill, 9 new checks in check-skill, no migration of existing skills, version bump). Test plan: sample `/build:build-skill` runs for DATA and ARTIFACT scaffolds; regression pass on existing skills. Link to issue #327 as downstream consumer and the design doc.

**Verify:** `gh pr view` returns the PR URL; CI (ruff + pytest) green.

**Commit:** None (PR creation is not a commit).

## Validation

After all tasks complete, the following must all hold:

1. **Shared contract exists with all sections.**
   ```
   test -f plugins/build/_shared/references/as-tool-contract.md
   grep -c "^## " plugins/build/_shared/references/as-tool-contract.md   # ≥ 9
   ```

2. **build-skill references the shared contract.**
   ```
   grep "as-tool-contract" plugins/build/skills/build-skill/SKILL.md
   ```
   Returns at least one line in frontmatter `references:`.

3. **check-skill references the shared contract.**
   ```
   grep "as-tool-contract" plugins/build/skills/check-skill/SKILL.md
   ```
   Returns at least one line in frontmatter `references:`.

4. **build-skill asks the intake question.**
   ```
   grep -c "skill-invocable\|invocable by other skills" plugins/build/skills/build-skill/SKILL.md
   ```
   Returns ≥ 2.

5. **Both DATA and ARTIFACT scaffolds documented in build-skill.**
   ```
   grep -c "DATA\|ARTIFACT" plugins/build/skills/build-skill/SKILL.md
   ```
   Returns ≥ 4.

6. **skill-writing-guide has dual-invocation section.**
   ```
   grep -E "^## .*[Dd]ual.[Ii]nvocation|^## .*--as-tool" \
     plugins/build/skills/build-skill/references/skill-writing-guide.md
   ```
   Returns ≥ 1 match.

7. **Nine new Python check functions exist.**
   ```
   grep -c "^def _check_skill_invocable_boolean\|^def _check_contract_\|^def _check_non_invocable_pathology" \
     plugins/build/src/check/skill.py
   ```
   Returns 9.

8. **Tests pass including new ones.**
   ```
   python3 -m pytest plugins/build/tests/test_skill_audit.py -v
   ```
   All tests pass; at least one new test per new check function.

9. **check-skill SKILL.md documents 9 new checks (23–31).**
   ```
   grep -E "\| 2[3-9] \||\| 3[01] \|" plugins/build/skills/check-skill/SKILL.md
   ```
   Returns ≥ 9 lines.

10. **No regression on existing skills.**
    ```
    python3 plugins/wiki/scripts/lint.py --root . --no-urls 2>&1 | \
      grep -E "(skill_invocable|contract_)" | grep -c "fail"
    ```
    Returns 0 on all 41 existing SKILL.md files.

11. **Build plugin version bumped coherently.**
    ```
    grep version plugins/build/pyproject.toml plugins/build/.claude-plugin/plugin.json
    ```
    Both show `0.5.0`.

12. **Ruff clean.**
    ```
    ruff check plugins/build
    ```
    Returns 0 warnings.

13. **Manual smoke — DATA scaffold.** A mock run of `/build:build-skill` answered "yes → DATA" produces a SKILL.md with `skill-invocable: true`, `## --as-tool contract` section, `**Return shape:** DATA`, all three cases documented, workflow split into human/as-tool modes.

14. **Manual smoke — ARTIFACT scaffold.** A mock run answered "yes → ARTIFACT, types: text/x-shellscript" produces a SKILL.md with `skill-invocable: true`, `**Return shape:** ARTIFACT`, `**Artifact types:** text/x-shellscript`, workflow emitting JSON envelope + single fenced ```bash block.

15. **Manual smoke — multi-artifact ARTIFACT scaffold.** Same with `text/x-shellscript, application/json` — produces SKILL.md emitting JSON envelope + two fenced blocks in declared order.

16. **Dummy plugin still works.** `/dummy:greet --as-tool name=bob time-of-day=morning` in a fresh session still returns `Success` JSON (no regression from the changes).

17. **PR is open.** `gh pr view` returns a PR URL; CI green.
