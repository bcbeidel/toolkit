---
name: Hook/Shell --as-tool Delegation
description: Opt build-shell, check-shell, build-hook, and check-hook into skill-invocable mode; route hook-pair shell concerns through the shell pair; add check-shell S11; bump build plugin to 0.6.0.
type: plan
status: executing
branch: feat/327-hook-shell-as-tool-delegation
related:
  - .designs/2026-04-20-hook-shell-as-tool-delegation.design.md
  - plugins/build/_shared/references/as-tool-contract.md
  - plugins/build/skills/build-skill/references/as-tool-scaffolding.md
  - plugins/dummy/skills/greet/SKILL.md
---

# Hook/Shell `--as-tool` Delegation

## Goal

Four skills in the `build` plugin change shape in concert:

- `build-shell` and `check-shell` opt into `--as-tool` as providers.
- `build-hook` and `check-hook` opt in as providers *and* become callers — `build-hook` invokes `/build:build-shell --as-tool` to generate its scaffold; `check-hook` invokes `/build:check-shell --as-tool` per hook script and merges findings.
- `check-shell` gains one new lint (**S11: missing strict-mode preamble, warn**) to close the delegation gap left when `check-hook` drops its preamble audit.
- Build plugin bumps 0.5.0 → 0.6.0.

After this plan lands, shell-hygiene concerns have a single owner, and the hook pair is a consumer of the shell pair via the settled `--as-tool` contract.

**Closes #327.**

## Scope

### Must have

- `plugins/build/skills/build-shell/SKILL.md`: `skill-invocable: true`; `## --as-tool contract` section (Required fields = five; Return shape = ARTIFACT; Artifact types = `text/x-shellscript`); intro paragraph naming both modes; workflow split into `§Xa. Human` and `§Xb. --as-tool`; FX.1 scope-gate fires return structured `Refusal` under `--as-tool` instead of halting; shared contract added to `references:`.
- `plugins/build/skills/check-shell/SKILL.md`: `skill-invocable: true`; `## --as-tool contract` section (Required fields = `path`; Return shape = DATA); Report step split into human (table + preamble) and `--as-tool` (DATA envelope) branches; new **S11** lint entry added to the Safety subsection; `external_tools` payload shape documented; shared contract added to `references:`.
- `plugins/build/skills/build-hook/SKILL.md`: `skill-invocable: true`; `## --as-tool contract` section (Required fields = four; Return shape = ARTIFACT; Artifact types = `text/x-shellscript, application/json`); Draft step becomes a caller of `/build:build-shell --as-tool` with pinned `target-shell=bash-3.2-portable`; hook-specific content (`INPUT=$(cat)`, `jq tool_input` extraction, `updatedInput` contract) layered onto the returned scaffold; emits MULTI-ARTIFACT Success with `metadata = {hook_event, matcher, handler_type}`; shared contract added to `references:`.
- `plugins/build/skills/check-hook/SKILL.md`: `skill-invocable: true`; `## --as-tool contract` section (Required fields = `settings-path`; Return shape = DATA); Checks step becomes a caller of `/build:check-shell --as-tool` per `"type": "command"` hook script; delegated checks removed (14 fully; 11, 15 fully; 12's unquoted-variable portion); findings merged with `source: "check-hook"` / `source: "check-shell"` labels; shared contract added to `references:`.
- `plugins/build/pyproject.toml` and `plugins/build/.claude-plugin/plugin.json` bump to 0.6.0.
- `/build:check-skill` self-audit: zero fail-level findings on all four modified SKILL.md files (checks 23-31 pass).
- No regression on the other 41 existing SKILL.md files (checks 23-31 still pass; no new fails introduced by this change).
- PR opened against `main`; CI green (ruff + pytest).

### Won't have

- Changes to `plugins/build/_shared/references/as-tool-contract.md`. The contract is consumed as-is.
- Changes to `plugins/build/skills/build-skill/references/as-tool-scaffolding.md`. The scaffolding recipe is consumed as-is.
- Dummy plugin edits. `/dummy:greet` remains the canonical DATA example.
- Changes to any other `build` skill (`build-skill`, `build-rule`, `build-subagent`, `refine-prompt`, `check-skill`, `check-rule`, `check-subagent`, `check-skill-chain`).
- Changes to wiki, work, or consider plugins.
- Python source changes. `check-shell` and `check-hook` are LLM-driven markdown skills; S11 is documented in SKILL.md prose, not in Python lint code.
- Migration of `target-shell` for `build-hook`'s inner `build-shell` call to a caller-supplied field. Pinned to `bash-3.2-portable` for now; future revision out of scope.
- New skill creation. No new skills in this plan.
- Auto-patching of `settings.json` by `build-hook`. The write step stays with the user (human mode) or caller (`--as-tool` mode).
- "Amplifier" findings in `check-hook` that duplicate `check-shell`'s shell-hygiene output. Single ownership per lint is the refactor's point.
- Changes to `.claude-plugin/marketplace.json`. Marketplace references the plugin, not per-skill.

## Approach

**Bottom-up order, chunked.** The hook pair depends on the shell pair being `--as-tool`-ready; ship the providers first, then the callers.

- **Chunk 1** — opt-in for `build-shell` + `check-shell`, plus the new S11 lint. Self-contained and verifiable in isolation: each SKILL.md passes `/build:check-skill` checks 23-31, and each skill emits a valid `--as-tool` envelope when given valid inputs.
- **Chunk 2** — `build-hook` Draft step refactor. Now callable: the inner `build-shell --as-tool` call exists and works. Verifiable by invoking `/build:build-hook --as-tool` and inspecting the multi-artifact envelope.
- **Chunk 3** — `check-hook` Checks step refactor. Now callable: the inner `check-shell --as-tool` call exists and works. Verifiable by invoking `/build:check-hook --as-tool` against a fixture settings.json and confirming findings carry `source:` labels.
- **Chunk 4** — release gates. Self-audit all four files, bump version, open PR.

**No migration of existing skills.** The 41 non-hook/non-shell skills stay as-is. Regression test is "no new fails from checks 23-31 on existing skills" — a strict bound.

**Settings.json write-step stays with the caller.** `build-hook` emits the settings.json block in the fenced artifact; it never writes. Preserves existing behavior (the skill has never auto-patched `settings.json`) and matches the contract's rule that Save is skipped under `--as-tool`.

**`metadata` kept minimal.** Three keys for `build-hook` Success (`hook_event`, `matcher`, `handler_type`) — per design Question 5, everything else the caller needs is parseable from the settings.json fenced block. Resist the urge to duplicate.

**Test discipline.** For `check-shell` S11, the lint is documented in SKILL.md prose (markdown lint skill, not Python). Regression test is `/build:check-shell` against a fixture script missing `set -Eeuo pipefail` producing an S11 warn finding. For `build-hook` multi-artifact emission, the test is an actual `--as-tool` invocation with a smoke-check on the two fenced-block shape.

## File Changes

| File | Change |
|---|---|
| `plugins/build/skills/build-shell/SKILL.md` | **Modify** — add `skill-invocable: true` to frontmatter; add shared contract to `references:`; add two-modes intro paragraph; add `## --as-tool contract` section (Required fields / Return shape / Artifact types / three cases / Side effects / Parallel-safe); split §6 Review Gate and §7 Save + §8 Test into `§6a/b`, `§7a/b`, `§8a/b` (human vs `--as-tool`); modify §2 Scope Gate to return structured `Refusal` under `--as-tool`. |
| `plugins/build/skills/check-shell/SKILL.md` | **Modify** — add `skill-invocable: true` to frontmatter; add shared contract to `references:`; add two-modes intro paragraph; add `## --as-tool contract` section (Required fields = `path`; Return shape = DATA; three cases; DATA schema documented; Side effects; Parallel-safe); add **S11** lint under Safety subsection (warn; body wording per design); split §5 Report into `§5a/b`. |
| `plugins/build/skills/build-hook/SKILL.md` | **Modify** — add `skill-invocable: true` to frontmatter; add shared contract to `references:`; add two-modes intro paragraph; add `## --as-tool contract` section (Required fields = four; Return shape = ARTIFACT; Artifact types = `text/x-shellscript, application/json`; multi-artifact emission rule; three cases; Side effects = invokes `build-shell`; Parallel-safe); refactor §3 Draft to invoke `/build:build-shell --as-tool target-shell=bash-3.2-portable purpose=... invocation-style=glue setuid=no deps=jq,...`, receive the scaffold, layer hook-specific content; split §7 Review Gate + §8 Save + §9 Test into human/`--as-tool` branches; under `--as-tool` emit MULTI-ARTIFACT Success with the two fenced blocks in declared order. |
| `plugins/build/skills/check-hook/SKILL.md` | **Modify** — add `skill-invocable: true` to frontmatter; add shared contract to `references:`; add two-modes intro paragraph; add `## --as-tool contract` section (Required fields = `settings-path`; Return shape = DATA; DATA schema with `source:` labels documented; three cases; Side effects = invokes `check-shell` per script; Parallel-safe); refactor §4 Checks to invoke `/build:check-shell --as-tool path=<hook-script-path>` per `"type": "command"` hook, merge findings with retained hook-specific checks; delete delegated check bodies (11, 14, 15 fully; 12's unquoted-variable portion); renumber or preserve check IDs per existing convention; split §5 Report into human (table) and `--as-tool` (DATA envelope) branches. |
| `plugins/build/pyproject.toml` | **Modify** — version `0.5.0` → `0.6.0`. |
| `plugins/build/.claude-plugin/plugin.json` | **Modify** — version `0.5.0` → `0.6.0`. |

No files created. No files deleted. No Python source changes.

## Tasks

### Chunk 1: build-shell + check-shell opt-in

#### Task 1: Opt `build-shell` into `--as-tool`

**Files:**
- Modify: `plugins/build/skills/build-shell/SKILL.md`

- [x] Task 1 complete <!-- sha:4d91093 -->

- [x] **Step 1:** Add `skill-invocable: true` to frontmatter. Add `../../_shared/references/as-tool-contract.md` to `references:`.
- [x] **Step 2:** Insert two-modes intro paragraph immediately after the H1/one-line purpose, per `as-tool-scaffolding.md`: "Two invocation modes: Human — prompts for missing info, shows the result, asks for approval. `--as-tool` — structured emission per the shared contract. No prompts, no approval."
- [x] **Step 3:** Add `## --as-tool contract` H2 near the end of the body (before `## Anti-Pattern Guards`). Populate subsections: **Required fields:** `target-shell`, `purpose`, `invocation-style`, `setuid`, `deps` (one-line description each); **Return shape:** ARTIFACT; **Artifact types:** `text/x-shellscript`; three bullets for Success (metadata shape + one fenced ```bash block carries the scaffold), NeedsMoreInfo (JSON only; `missing`, `hint`), Refusal (JSON only; `reason`, `category`; enumerate categories: `scope-gate`, `invalid-combo`); **Side effects:** reads intake; no file writes under `--as-tool`; **Parallel-safe:** yes.
- [x] **Step 4:** Modify §2 FX.1 Scope Gate: add a sub-note that under `--as-tool`, a tripped signal returns a structured `Refusal` (category `scope-gate`, reason citing the signal) instead of halting interactively.
- [x] **Step 5:** Split §6 Review Gate → §6a Human (current prose) and §6b `--as-tool` ("skipped; caller owns approval"). Same for §7 Save → §7a Human / §7b `--as-tool` (emission: output the JSON envelope with `artifact_types: ["text/x-shellscript"]` and `metadata: {target_shell, invocation_style}`, followed by one fenced ```bash block carrying the scaffold). Same for §8 Test → §8a/8b ("skipped under `--as-tool`").
- [x] **Step 6:** Add three Key Instructions entries per the scaffolding recipe: (a) under `--as-tool` emit per the contract (JSON envelope + one fenced ```bash block); (b) hard-fail with `NeedsMoreInfo` when any required field is missing; (c) `NeedsMoreInfo` and `Refusal` emit JSON only, never fenced blocks.
- [x] **Step 7:** Verify: `grep -c "skill-invocable: true" plugins/build/skills/build-shell/SKILL.md` returns 1; `grep -c "^## --as-tool contract" plugins/build/skills/build-shell/SKILL.md` returns 1; `grep -c "Required fields\|Return shape\|Artifact types\|Side effects\|Parallel-safe" plugins/build/skills/build-shell/SKILL.md` returns ≥ 5.
- [x] **Step 8:** Commit: `feat(build-shell): opt into --as-tool as ARTIFACT provider (text/x-shellscript)`.

#### Task 2: Opt `check-shell` into `--as-tool` and add S11 lint

**Files:**
- Modify: `plugins/build/skills/check-shell/SKILL.md`

- [x] Task 2 complete <!-- sha:cf7cbbe -->

- [x] **Step 1:** Add `skill-invocable: true` to frontmatter. Add `../../_shared/references/as-tool-contract.md` to `references:`.
- [x] **Step 2:** Insert two-modes intro paragraph after the H1/purpose.
- [x] **Step 3:** Add new lint **S11: Missing strict-mode preamble (warn)** under §4 Checks → Safety subsection (after S10). Body per design: "Script does not begin (after the shebang and header) with `set -Eeuo pipefail` (bash) or `set -eu` (posix-sh). Without strict mode, commands that exit non-zero proceed silently and unset-variable dereferences expand to empty strings, producing actions on wrong inputs. Fix: add the appropriate strict-mode line near the top of the script."
- [x] **Step 4:** Split §5 Report into §5a Human (current table + Missing Tools preamble prose) and §5b `--as-tool` (emit a single JSON envelope — no fenced blocks — per the DATA schema in the design: `{type: "Success", value: {path, target_shell, summary, findings: [...], external_tools: {...}}}`, with severity ∈ `{fail, warn}`, line nullable for file-level findings, `external_tools` keyed per tool with `present`/`output`/`install_hint`).
- [x] **Step 5:** Add `## --as-tool contract` H2 before `## Anti-Pattern Guards`: **Required fields:** `path`; **Return shape:** DATA; three bullets (Success with `value` schema; NeedsMoreInfo; Refusal — category examples: `file-not-found`, `not-a-shell-script`); **Side effects:** reads the script at `path`, probes `PATH` for `shellcheck`/`shfmt`/`checkbashisms`, runs whichever are present; **Parallel-safe:** yes.
- [x] **Step 6:** Add three Key Instructions entries per the scaffolding recipe (DATA variant).
- [x] **Step 7:** Verify: `grep -c "skill-invocable: true" plugins/build/skills/check-shell/SKILL.md` returns 1; `grep -c "^## --as-tool contract" plugins/build/skills/check-shell/SKILL.md` returns 1; `grep -c "S11\." plugins/build/skills/check-shell/SKILL.md` returns ≥ 1; `grep "strict-mode preamble" plugins/build/skills/check-shell/SKILL.md` non-empty.
- [x] **Step 8:** Commit: `feat(check-shell): opt into --as-tool as DATA provider; add S11 strict-mode preamble lint`.

#### Task 3: Self-audit Chunk 1 SKILL.md files

**Depends on:** Task 1, Task 2

- [x] Task 3 complete <!-- sha:72f7e55 -->

- [x] **Step 1:** Invoke `/build:check-skill --as-tool path=plugins/build/skills/build-shell/SKILL.md` and confirm zero fail-level findings on checks 23-31.
- [x] **Step 2:** Invoke `/build:check-skill --as-tool path=plugins/build/skills/check-shell/SKILL.md` and confirm zero fail-level findings on checks 23-31.
- [x] **Step 3:** If fails: fix in place. Re-audit. If warnings are acceptable (pre-existing or explicit), document in Notes.
- [x] **Step 4:** Verify: the two `/build:check-skill` invocations each show 0 fail findings on 23-31.
- [x] **Step 5:** Commit (only if fixes needed): `fix(build): resolve check-skill findings on build-shell/check-shell opt-in`.

### Chunk 2: build-hook Draft step refactor

#### Task 4: Opt `build-hook` into `--as-tool` and refactor Draft to call `build-shell`

**Files:**
- Modify: `plugins/build/skills/build-hook/SKILL.md`

**Depends on:** Task 1 (inner `build-shell --as-tool` must exist).

- [x] Task 4 complete <!-- sha:846da0e -->

- [x] **Step 1:** Add `skill-invocable: true` to frontmatter. Add `../../_shared/references/as-tool-contract.md` to `references:`.
- [x] **Step 2:** Insert two-modes intro paragraph after the H1/purpose.
- [x] **Step 3:** Refactor §3 Draft:
  - Artifact 1 (hook script): under human mode, retain current scaffold. Under both modes, the scaffold is now generated by invoking `/build:build-shell --as-tool target-shell=bash-3.2-portable purpose="<derived from enforcement-goal>" invocation-style=glue setuid=no deps=jq`; receive the ARTIFACT envelope + fenced ```bash block; layer hook-specific content onto it: `INPUT=$(cat)` near the top, `jq -r '.tool_input.<field>'` extraction per `tool_name` (table preserved), optional ERR/EXIT traps, `updatedInput` JSON output contract (preserved), tool-name case/matcher handling.
  - Artifact 2 (settings.json entry): unchanged generation; emitted as a fenced ```json block under `--as-tool`.
  - Document that a `NeedsMoreInfo` or `Refusal` from the inner `build-shell` invocation propagates up as the outer skill's own envelope.
- [x] **Step 4:** Split §7 Review Gate → §7a Human / §7b `--as-tool` ("skipped; caller owns approval"). §8 Save → §8a Human (retain current: write script, chmod +x, show settings snippet) / §8b `--as-tool` (skipped; emit MULTI-ARTIFACT Success with `artifact_types: ["text/x-shellscript", "application/json"]` and `metadata: {hook_event, matcher, handler_type}`, then the two fenced blocks in declared order: ```bash hook script first, ```json settings entry second). §9 Test → §9a/9b.
- [x] **Step 5:** Add `## --as-tool contract` H2 before `## Anti-Pattern Guards`: **Required fields:** `hook-event`, `handler-type`, `enforcement-goal`, `matcher` (note: pass `"*"` for non-tool events); **Return shape:** ARTIFACT; **Artifact types:** `text/x-shellscript, application/json`; three bullets (Success with metadata = 3 keys and two fenced blocks; NeedsMoreInfo; Refusal — categories: `wrong-primitive`, `inner-refusal`); **Side effects:** invokes `/build:build-shell --as-tool` with pinned `target-shell=bash-3.2-portable`; **Parallel-safe:** yes.
- [x] **Step 6:** Add three Key Instructions entries per the scaffolding recipe (ARTIFACT variant).
- [x] **Step 7:** Verify: `grep -c "skill-invocable: true" plugins/build/skills/build-hook/SKILL.md` returns 1; `grep -c "^## --as-tool contract" plugins/build/skills/build-hook/SKILL.md` returns 1; `grep -c "/build:build-shell --as-tool" plugins/build/skills/build-hook/SKILL.md` returns ≥ 1; `grep -c "text/x-shellscript.*application/json\|application/json.*text/x-shellscript" plugins/build/skills/build-hook/SKILL.md` returns ≥ 1.
- [x] **Step 8:** Commit: `feat(build-hook): opt into --as-tool as MULTI-ARTIFACT provider; delegate scaffold to build-shell`.

#### Task 5: Self-audit `build-hook` SKILL.md

**Depends on:** Task 4

- [x] Task 5 complete <!-- sha:846da0e verified — 0 fail, 2 pre-existing warn -->

- [x] **Step 1:** Invoke `/build:check-skill --as-tool path=plugins/build/skills/build-hook/SKILL.md`; confirm zero fail findings on checks 23-31.
- [x] **Step 2:** If fails: fix in place. Re-audit.
- [x] **Step 3:** Commit (only if fixes): `fix(build-hook): resolve check-skill findings on --as-tool opt-in`.

### Chunk 3: check-hook Checks step refactor

#### Task 6: Opt `check-hook` into `--as-tool` and refactor Checks to call `check-shell`

**Files:**
- Modify: `plugins/build/skills/check-hook/SKILL.md`

**Depends on:** Task 2 (inner `check-shell --as-tool` must exist).

- [x] Task 6 complete <!-- sha:ec5269d -->

- [x] **Step 1:** Add `skill-invocable: true` to frontmatter. Add `../../_shared/references/as-tool-contract.md` to `references:`.
- [x] **Step 2:** Insert two-modes intro paragraph after the H1/purpose.
- [x] **Step 3:** Refactor §4 Checks:
  - For each `"type": "command"` hook script found in `settings-path`: invoke `/build:check-shell --as-tool path=<hook-script-path>`; collect its findings (labeled `source: "check-shell"` on merge).
  - Remove delegated check bodies: **14** (ShellCheck + shfmt) fully; **11** (script safety preamble) fully — the generic `set -Eeuo pipefail` concern is now owned by `check-shell` S11; the `|| true` guards on `grep`/`diff` etc. also belong to `check-shell`; **15** (script style — stderr, `[[` vs `[`, `set -x`, shebang form) fully; **12's unquoted-variable portion** — map to `check-shell` S1; retain only the `eval`-on-payload branch and PATH-override branch under `check-hook` 12 (since these depend on `tool_input` semantics).
  - Renumber remaining checks OR preserve original IDs with explicit "delegated" notes per existing convention — pick whichever yields a cleaner file; document choice in Notes.
  - Retained checks: 1 (PreToolUse gap), 2 (destructive ops), 3 (async+blocking), 4 (Stop hook loop), 5 (stdin + executable bit), 6 (tool-name case + path expansion), 7 (PostToolUse enforcement intent), 8 (rule overlap vs CLAUDE.md), 9 (idempotency), 10 (latency), 12 (eval-on-payload + PATH-override only), 13 (jq availability + `tool_input` field-path), 16 (settings.json attack surface).
- [x] **Step 4:** Split §5 Report into §5a Human (current table, with a new `source` column prepended; include `check-shell` findings interleaved; external-tool preamble preserved) and §5b `--as-tool` (emit single JSON envelope per design DATA schema: `{type: "Success", value: {settings_path, summary, findings: [{source, check|lint, severity, event|null, hook, line|null, message}, ...]}}`).
- [x] **Step 5:** Add `## --as-tool contract` H2 before `## Anti-Pattern Guards`: **Required fields:** `settings-path`; **Return shape:** DATA; three bullets (Success schema; NeedsMoreInfo; Refusal — categories: `file-not-found`, `no-hooks`, `parse-error`); **Side effects:** reads `settings-path`; invokes `/build:check-shell --as-tool` once per `"type": "command"` hook script; **Parallel-safe:** yes (inner `check-shell` calls are parallel-safe; document that concurrent outer calls on the same `settings-path` are redundant but correct).
- [x] **Step 6:** Add three Key Instructions entries per the scaffolding recipe (DATA variant). Plus one skill-specific instruction: "Under `--as-tool`, every finding carries a `source` field — `check-hook` or `check-shell` — so callers can trace ownership."
- [x] **Step 7:** Verify: `grep -c "skill-invocable: true" plugins/build/skills/check-hook/SKILL.md` returns 1; `grep -c "^## --as-tool contract" plugins/build/skills/check-hook/SKILL.md` returns 1; `grep -c "/build:check-shell --as-tool" plugins/build/skills/check-hook/SKILL.md` returns ≥ 1; `grep -c "source.*check-shell\|source.*check-hook" plugins/build/skills/check-hook/SKILL.md` returns ≥ 2.
- [x] **Step 8:** Commit: `feat(check-hook): opt into --as-tool as DATA provider; delegate shell-hygiene to check-shell`.

#### Task 7: Self-audit `check-hook` SKILL.md

**Depends on:** Task 6

- [x] Task 7 complete <!-- sha:ec5269d verified — 0 fail, 1 pre-existing warn -->

- [x] **Step 1:** Invoke `/build:check-skill --as-tool path=plugins/build/skills/check-hook/SKILL.md`; confirm zero fail findings on checks 23-31.
- [x] **Step 2:** If fails: fix in place. Re-audit.
- [x] **Step 3:** Commit (only if fixes): `fix(check-hook): resolve check-skill findings on --as-tool opt-in`.

### Chunk 4: Release

#### Task 8: Regression check across all existing SKILL.md files

**Depends on:** Task 3, Task 5, Task 7

- [x] Task 8 complete <!-- sha:4728b99 verified — repo-wide 0 fails; 140 tests pass -->

- [x] **Step 1:** Invoke `/build:check-skill` (human mode) or run the lint script (`python3 plugins/wiki/scripts/lint.py --root . --no-urls`) across the full repo.
- [x] **Step 2:** Confirm zero new fail-level findings on the 41 pre-existing non-hook/non-shell SKILL.md files that are attributable to checks 23-31. Existing warn-level findings that predate this plan are acceptable.
- [x] **Step 3:** Verify: `python3 plugins/wiki/scripts/lint.py --root . --no-urls 2>&1 | grep -E "(skill_invocable|contract_|check_2[3-9]|check_3[01])" | grep -c "fail"` returns 0.
- [x] **Step 4:** Commit (only if regressions require a fix): `fix(build): resolve regressions from --as-tool opt-ins`.

#### Task 9: Bump build plugin version to 0.6.0

**Files:**
- Modify: `plugins/build/pyproject.toml`
- Modify: `plugins/build/.claude-plugin/plugin.json`

**Depends on:** Tasks 1–8

- [x] Task 9 complete <!-- sha:4728b99 -->

- [x] **Step 1:** Edit `plugins/build/pyproject.toml`: `version = "0.5.0"` → `version = "0.6.0"`.
- [x] **Step 2:** Edit `plugins/build/.claude-plugin/plugin.json`: `"version": "0.5.0"` → `"version": "0.6.0"`.
- [x] **Step 3:** Verify: `grep version plugins/build/pyproject.toml plugins/build/.claude-plugin/plugin.json` — both show `0.6.0`.
- [x] **Step 4:** Commit: `chore(build): bump to 0.6.0 for hook/shell --as-tool delegation`.

#### Task 10: Open PR

**Depends on:** Task 9

- [ ] **Step 1:** Push branch `feat/327-hook-shell-as-tool-delegation` with `-u origin`.
- [ ] **Step 2:** Open PR against `main`. Title: `feat(build): hook/shell --as-tool delegation (build-0.6.0)`. Body: Summary (4 skills opt in; hook pair delegates to shell pair; check-shell S11; no migration of other skills; version bump). Test plan bullets: Chunk 1 self-audits, Chunk 2/3 invocation smoke, regression check, human-mode regression spot-check. Link #327 (closes) and the design doc.
- [ ] **Step 3:** Verify: `gh pr view` returns a PR URL; CI (ruff + pytest) green.
- [ ] **Step 4:** No commit (PR creation is not a commit).

## Validation

After all tasks complete:

1. **All four SKILL.md files declare `skill-invocable: true`.**
   ```
   grep -l "skill-invocable: true" \
     plugins/build/skills/build-shell/SKILL.md \
     plugins/build/skills/check-shell/SKILL.md \
     plugins/build/skills/build-hook/SKILL.md \
     plugins/build/skills/check-hook/SKILL.md | wc -l
   ```
   Returns `4`.

2. **All four SKILL.md files carry a `## --as-tool contract` H2.**
   ```
   for f in plugins/build/skills/{build-shell,check-shell,build-hook,check-hook}/SKILL.md; do
     grep -c "^## --as-tool contract" "$f"
   done
   ```
   Each line prints `1`.

3. **All four SKILL.md files reference the shared contract.**
   ```
   for f in plugins/build/skills/{build-shell,check-shell,build-hook,check-hook}/SKILL.md; do
     grep -c "as-tool-contract.md" "$f"
   done
   ```
   Each line prints ≥ 1.

4. **`/build:check-skill` passes checks 23-31 on all four files.**
   For each of the four SKILL.md paths, `/build:check-skill --as-tool path=<file>` returns `Success` with zero findings where `check_id` ∈ 23..31 and `severity == "fail"`.

5. **`check-shell` documents S11.**
   ```
   grep -E "^#### S11\.|S11: Missing strict-mode preamble" plugins/build/skills/check-shell/SKILL.md
   ```
   Non-empty.

6. **`check-hook` no longer documents check 14, check 11, check 15, or the unquoted-variable portion of check 12.**
   ```
   grep -cE "^### 11\. Script safety preamble|^### 14\. ShellCheck|^### 15\. Script style conventions" \
     plugins/build/skills/check-hook/SKILL.md
   ```
   Returns `0`.

7. **`check-hook` still documents retained checks 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12 (eval/PATH only), 13, 16.**
   ```
   grep -cE "^### [0-9]+\." plugins/build/skills/check-hook/SKILL.md
   ```
   Returns ≥ 13 (count equals the retained set; exact value depends on renumbering choice in Task 6 Step 3).

8. **Smoke — `build-shell --as-tool`.** A mock invocation `/build:build-shell --as-tool target-shell=bash-3.2-portable purpose="echo hello" invocation-style=glue setuid=no deps=` returns a single JSON envelope `{type: "Success", artifact_types: ["text/x-shellscript"], metadata: {...}}` followed by exactly one fenced ```bash block containing a scaffold that starts with `#!/usr/bin/env bash` and includes `set -Eeuo pipefail`.

9. **Smoke — `check-shell --as-tool`.** `/build:check-shell --as-tool path=<script-without-preamble>` returns a single JSON envelope `{type: "Success", value: {..., findings: [..., {"lint": "S11", "severity": "warn", ...}, ...]}}` — no fenced blocks.

10. **Smoke — `build-hook --as-tool`.** `/build:build-hook --as-tool hook-event=PreToolUse handler-type=command enforcement-goal="block rm -rf" matcher=Bash` returns a JSON envelope `{type: "Success", artifact_types: ["text/x-shellscript", "application/json"], metadata: {hook_event: "PreToolUse", matcher: "Bash", handler_type: "command"}}` followed by exactly two fenced blocks in order: ```bash (hook script; contains `INPUT=$(cat)` and `set -Eeuo pipefail`) then ```json (settings entry; `hooks.PreToolUse[].matcher == "Bash"`).

11. **Smoke — `check-hook --as-tool`.** Against a fixture settings.json referencing at least one command hook whose script has an unquoted variable expansion (triggers `check-shell` S1), `/build:check-hook --as-tool settings-path=<path>` returns a single JSON envelope with `value.findings` containing at least one finding with `source: "check-shell"` and at least one with `source: "check-hook"` — no fenced blocks.

12. **Smoke — `NeedsMoreInfo` envelopes.** Each of the four skills, invoked with `--as-tool` and a required field omitted, returns `{"type": "NeedsMoreInfo", "missing": [...], "hint": "..."}` — no fenced blocks.

13. **Human-mode regression — `build-shell`.** A mock human-mode run completes the current §1–§8 flow unchanged (Elicit asks six fields including `save-path`; Save writes the file; `chmod +x` runs).

14. **Human-mode regression — `check-shell`.** A mock human-mode run produces the current report format (table + Missing Tools preamble) against a sample script. S11 surfaces as a new warn when the script lacks `set -Eeuo pipefail`.

15. **Human-mode regression — `build-hook`.** A mock human-mode run for a PreToolUse blocker produces the current two artifacts (hook script + settings.json snippet) and waits for Review Gate approval before Save. The inner `build-shell --as-tool` call is used internally; no user-visible change to the human flow.

16. **Human-mode regression — `check-hook`.** A mock human-mode run against a sample `settings.json` produces the current report format (table with findings per hook). Shell-hygiene findings appear under `source: check-shell` (new column); hook-specific findings under `source: check-hook`.

17. **Build plugin version is 0.6.0.**
    ```
    grep version plugins/build/pyproject.toml plugins/build/.claude-plugin/plugin.json
    ```
    Both show `0.6.0`.

18. **Shared contract unchanged.**
    ```
    git diff main -- plugins/build/_shared/references/as-tool-contract.md
    ```
    Returns no output.

19. **`as-tool-scaffolding.md` unchanged.**
    ```
    git diff main -- plugins/build/skills/build-skill/references/as-tool-scaffolding.md
    ```
    Returns no output.

20. **No regression on other 41 SKILL.md files.** `python3 plugins/wiki/scripts/lint.py --root . --no-urls` shows zero new fail-level findings on non-hook/non-shell SKILL.md files attributable to checks 23-31.

21. **Ruff clean.**
    ```
    ruff check plugins/build
    ```
    Returns 0 warnings.

22. **Tests pass.**
    ```
    python3 -m pytest plugins/build/tests/ -v
    ```
    All tests pass.

23. **Dummy plugin still works.** `/dummy:greet --as-tool name=bob time-of-day=morning` returns `{type: "Success", value: {text: "Good morning, bob!", ...}}` — no regression from shared-contract or scaffolding changes (neither should have happened).

24. **PR is open.** `gh pr view` returns a PR URL; CI green.

## Notes

- **Superseded plan.** `.plans/2026-04-19-hook-shell-structured-invocation.plan.md` (branch `explore/327-structured-invocation-thinking`) is pre-refinement exploration. Do not use it as implementation basis. This plan is the authoritative one for #327.
- **Renumbering in `check-hook`.** Chose to renumber checks rather than
  preserve original IDs with "delegated" stubs. Old → new mapping:
  1-10 unchanged; old 11 (script safety preamble) removed; old 12
  (injection safety) reshaped to keep eval-on-payload + PATH-override
  only, renumbered to 11; old 13 (jq availability) → 12; old 14
  (ShellCheck/shfmt) removed; old 15 (script style) removed; old 16
  (settings.json attack surface) → 13. A short delegation note under
  §4 Checks lists what moved to `check-shell`.
- **Pre-existing D6 false-positive fix.** Task 3 self-audit surfaced a
  pre-existing fail on `check-shell` line 217 (on main): the D6
  example `printf '...\n' >&2` tripped `_check_body_paths`'s Windows-
  path regex because `..\n` matches the `..\<name>` pattern. Fixed by
  rewording to `printf 'message\n' >&2`; SHA 72f7e55.
- **Inner-skill `Refusal` propagation.** When `/build:build-shell --as-tool` returns a `Refusal` (e.g., FX.1 scope gate fires for an inner call), `build-hook --as-tool` wraps it as its own `Refusal` with `category: "inner-refusal"` and `reason` echoing the inner envelope. Documented in `build-hook`'s contract section.
