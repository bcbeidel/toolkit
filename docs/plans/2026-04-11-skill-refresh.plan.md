---
name: Refresh All Skills Against v0.35.0 Research
description: Review and update all 14 SKILL.md files against the v0.35.0 context base — adding anti-pattern guards, strengthening gate checks, and removing contraindicated approaches
type: plan
status: completed
branch: feat/skill-refresh
pr: TBD
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
  - docs/plans/2026-04-11-handoff-contracts.plan.md
---

# Refresh All Skills Against v0.35.0 Research

**Goal:** Review every SKILL.md against the ~170 context files produced in v0.35.0, applying at least one substantive improvement per skill — stronger anti-pattern guards, tightened gate checks, removed contraindicated patterns — grounded in specific research findings.

**Scope:**

Must have:
- All 14 existing SKILL.md files reviewed and changed
- `## Anti-Pattern Guards` section present in every skill (7 are currently missing: distill, ingest, lint, refine-prompt, research, retrospective, setup)
- At least one change per skill traceable to a named context file finding
- `python scripts/lint.py --root . --no-urls` — no new warnings or failures

Won't have:
- New skills (those are Tasks 9–15 in the roadmap)
- Changes to Python code, tests, or scripts
- Changes to reference files under `skills/*/references/`
- Cosmetic-only changes (whitespace, rewording that doesn't change meaning)
- Skill body exceeding 500 instruction lines (enforce during execution)

**Approach:** Skills are grouped by shared research cluster so the executor reads context files once and applies findings across a batch. For each skill: (1) read the assigned context files, (2) read the current SKILL.md, (3) identify the highest-leverage gap in anti-pattern guards, gate checks, or constraints, (4) add a targeted improvement. Every change must cite which finding drove it. The 7 skills missing `## Anti-Pattern Guards` must gain that section as part of their refresh.

The five refresh dimensions (from issue #223):
1. **Anti-pattern guards** — add guards for known failure modes documented in research
2. **Gate checks** — strengthen or add phase gates based on structural patterns research
3. **Constraints** — add constraints for anti-patterns from instruction-file-authoring research
4. **Examples** — update to reflect current capabilities and patterns
5. **Remove** — approaches explicitly contraindicated by research

**File Changes:**
- Modify: `skills/research/SKILL.md`
- Modify: `skills/ingest/SKILL.md`
- Modify: `skills/distill/SKILL.md`
- Modify: `skills/write-plan/SKILL.md`
- Modify: `skills/execute-plan/SKILL.md`
- Modify: `skills/validate-work/SKILL.md`
- Modify: `skills/lint/SKILL.md`
- Modify: `skills/setup/SKILL.md`
- Modify: `skills/finish-work/SKILL.md`
- Modify: `skills/brainstorm/SKILL.md`
- Modify: `skills/refine-prompt/SKILL.md`
- Modify: `skills/check-rules/SKILL.md`
- Modify: `skills/extract-rules/SKILL.md`
- Modify: `skills/retrospective/SKILL.md`

**Branch:** `feat/skill-refresh` (recreate from main — Task 6 was squash-merged)
**PR:** TBD

---

## Chunk 1: Research Methodology Cluster

### Task 1: Refresh research, ingest, distill

**Primary context files to read:**
- `docs/context/sift-lateral-reading-and-tool-based-verification.context.md`
- `docs/context/knowledge-confidence-lifecycle-and-state-tracking.context.md`
- `docs/context/bidirectional-linking-and-knowledge-graph-primitives.context.md`
- `docs/context/instruction-file-authoring-anti-patterns.context.md`

**Skills:**
- Modify: `skills/research/SKILL.md` (missing Anti-Pattern Guards)
- Modify: `skills/ingest/SKILL.md` (missing Anti-Pattern Guards)
- Modify: `skills/distill/SKILL.md` (missing Anti-Pattern Guards)

**Assessment guidance per skill:**
- **research:** SIFT framework already present — check if lateral reading protocol is described, not just "evaluate sources." Add guards for: skipping counter-evidence, treating primary sources as the only input, failing to log searches in the protocol.
- **ingest:** Append-only constraint is present — check if contradiction handling is explicit (not just "add"). Add guards for: overwriting existing claims, ingesting without reading SCHEMA.md first, ignoring `confidence` lifecycle when updating pages.
- **distill:** Key Constraints present but no Anti-Pattern Guards — add guards for: creating context files without sources traced back to research, splitting one concept across multiple files, exceeding 800-word target without noting it.

- [x] **Step 1:** Read the four context files listed above.
- [x] **Step 2:** Read `skills/research/SKILL.md`, `skills/ingest/SKILL.md`, `skills/distill/SKILL.md`.
- [x] **Step 3:** For each skill, identify the highest-leverage gap using the assessment guidance. Apply at least one substantive change per skill, adding `## Anti-Pattern Guards` to each (research, ingest, distill all currently lack it).
- [x] **Step 4:** Verify: `grep -L "## Anti-Pattern Guards" skills/research/SKILL.md skills/ingest/SKILL.md skills/distill/SKILL.md` → empty output
- [x] **Step 5:** `python scripts/lint.py --root . --no-urls 2>&1 | grep -E "research|ingest|distill"` → no new skill warnings for these three
- [x] **Step 6:** Commit: `git commit -m "feat: refresh knowledge-pipeline skills against v0.35.0 research"` <!-- sha:0da6f69 -->

---

## Chunk 2: Planning & Execution Cluster

### Task 2: Refresh write-plan, execute-plan

**Primary context files to read:**
- `docs/context/agentic-planning-hybrid-global-plan-local-react.context.md`
- `docs/context/multi-agent-orchestration-patterns-and-selection-criteria.context.md`
- `docs/context/agent-memory-tier-taxonomy-and-implementation-gaps.context.md`
- `docs/context/multi-agent-shared-state-failure-mechanisms.context.md`

**Skills:**
- Modify: `skills/write-plan/SKILL.md` (has Anti-Pattern Guards — strengthen)
- Modify: `skills/execute-plan/SKILL.md` (has Anti-Pattern Guards — strengthen)

**Assessment guidance per skill:**
- **write-plan:** Check if the plan-globally/act-locally principle is reflected — does the skill distinguish between planning artifacts (disk) and execution context (transient)? Add a guard for treating plan tasks as single-session state rather than persistent files.
- **execute-plan:** Check for shared-state failure modes — does the skill explicitly address what happens when a task fails mid-execution (state checkpointing, rollback boundary via per-task commits)? Strengthen the "commit per task" rationale with the shared-state failure research.

- [x] **Step 1:** Read the four context files listed above.
- [x] **Step 2:** Read `skills/write-plan/SKILL.md`, `skills/execute-plan/SKILL.md`.
- [x] **Step 3:** Apply at least one substantive change per skill grounded in a specific finding from the context files.
- [x] **Step 4:** Verify: `git diff --name-only HEAD | grep -E "write-plan|execute-plan"` → both files changed
- [x] **Step 5:** `python scripts/lint.py --root . --no-urls 2>&1 | grep -E "write-plan|execute-plan"` → no new warnings
- [x] **Step 6:** Commit: `git commit -m "feat: refresh planning-pipeline skills against v0.35.0 research"` <!-- sha:d517256 -->

---

## Chunk 3: Validation Cluster

### Task 3: Refresh validate-work, lint, setup

**Primary context files to read:**
- `docs/context/structural-gates-llm-quality-checks.context.md`
- `docs/context/composable-validators-stateless-accumulator-pattern.context.md`
- `docs/context/validation-severity-tiers-and-confidence-decoupling.context.md`
- `docs/context/approval-gate-trust-calibration-and-overconfidence.context.md`

**Skills:**
- Modify: `skills/validate-work/SKILL.md` (has Anti-Pattern Guards — strengthen)
- Modify: `skills/lint/SKILL.md` (missing Anti-Pattern Guards)
- Modify: `skills/setup/SKILL.md` (missing Anti-Pattern Guards)

**Assessment guidance per skill:**
- **validate-work:** Check whether the skill distinguishes structural checks (must pass first) from quality checks (LLM judgment). The gate ordering — deterministic before LLM-based — should be explicit. Add a guard for skipping structural pre-checks and going straight to judgment.
- **lint:** Read-only diagnostic — add Anti-Pattern Guards for: interpreting pre-existing failures as new regressions, running with `--strict` on first audit of legacy projects, over-relying on automated checks without addressing root causes.
- **setup:** Add Anti-Pattern Guards for: running setup on a repo with uncommitted changes, skipping the layout selection and applying a default silently, overwriting an existing AGENTS.md without reading current content first.

- [x] **Step 1:** Read the four context files listed above.
- [x] **Step 2:** Read `skills/validate-work/SKILL.md`, `skills/lint/SKILL.md`, `skills/setup/SKILL.md`.
- [x] **Step 3:** Apply at least one substantive change per skill. Add `## Anti-Pattern Guards` to lint and setup.
- [x] **Step 4:** Verify: `grep -L "## Anti-Pattern Guards" skills/validate-work/SKILL.md skills/lint/SKILL.md skills/setup/SKILL.md` → empty output
- [x] **Step 5:** `python scripts/lint.py --root . --no-urls 2>&1 | grep -E "validate-work|lint|setup"` → no new warnings
- [x] **Step 6:** Commit: `git commit -m "feat: refresh validation-cluster skills against v0.35.0 research"` <!-- sha:d183311 -->

---

## Chunk 4: Delivery & Authoring Cluster

### Task 4: Refresh finish-work, brainstorm, refine-prompt

**Primary context files to read:**
- `docs/context/skill-chain-hitl-patterns-and-cli-translation-gap.context.md`
- `docs/context/hitl-oversight-as-tuned-policy-and-reversibility-gate.context.md`
- `docs/context/prompt-design-principles-framing-and-emphasis.context.md`
- `docs/context/instruction-file-authoring-anti-patterns.context.md`

**Skills:**
- Modify: `skills/finish-work/SKILL.md` (has Anti-Pattern Guards — strengthen)
- Modify: `skills/brainstorm/SKILL.md` (has Anti-Pattern Guards — strengthen)
- Modify: `skills/refine-prompt/SKILL.md` (missing Anti-Pattern Guards)

**Assessment guidance per skill:**
- **finish-work:** HITL patterns research identifies "propose-before-commit" as the primary CLI pattern. Check whether the skill's option-presentation step reflects the reversibility classification — irreversible options (discard) need stronger confirmation than reversible ones (keep). Strengthen accordingly.
- **brainstorm:** Brainstorm is the earliest intervention point against premature convergence. Check if the diverge step is explicit enough — does it guard against the "single approach" failure? The approval gate before hand-off should be stronger based on HITL research.
- **refine-prompt:** Missing Anti-Pattern Guards. Known failure modes: executing the prompt instead of analyzing it, over-refining (adding unnecessary techniques), treating every dimension as needing improvement. Add based on HITL and instruction-authoring findings.

- [x] **Step 1:** Read the four context files listed above.
- [x] **Step 2:** Read `skills/finish-work/SKILL.md`, `skills/brainstorm/SKILL.md`, `skills/refine-prompt/SKILL.md`.
- [x] **Step 3:** Apply at least one substantive change per skill. Add `## Anti-Pattern Guards` to refine-prompt.
- [x] **Step 4:** Verify: `grep -L "## Anti-Pattern Guards" skills/finish-work/SKILL.md skills/brainstorm/SKILL.md skills/refine-prompt/SKILL.md` → empty output
- [x] **Step 5:** `python scripts/lint.py --root . --no-urls 2>&1 | grep -E "finish-work|brainstorm|refine-prompt"` → no new warnings
- [x] **Step 6:** Commit: `git commit -m "feat: refresh delivery-and-authoring skills against v0.35.0 research"` <!-- sha:3138dd8 -->

---

## Chunk 5: Governance & Chain Cluster

### Task 5: Refresh check-rules, extract-rules, retrospective

**Primary context files to read:**
- `docs/context/linter-patterns-transferable-to-llm-rules.context.md`
- `docs/context/llm-rule-structural-characteristics.context.md`
- `docs/context/skill-chain-failure-modes-and-antipatterns.context.md`
- `docs/context/skill-chain-handoff-signaling-and-evidence-packs.context.md`

**Skills:**
- Modify: `skills/check-rules/SKILL.md` (has Anti-Pattern Guards — strengthen)
- Modify: `skills/extract-rules/SKILL.md` (has Anti-Pattern Guards — strengthen)
- Modify: `skills/retrospective/SKILL.md` (missing Anti-Pattern Guards)

**Assessment guidance per skill:**
- **check-rules:** Five structural patterns from linter research (start-narrow, default-closed, fix-safety classification, etc.) — does the skill reflect that scope isolation prevents false positives? Check whether the "one rule, one file" evaluation pattern is strong enough. Add a guard for batching multiple rules in one evaluation.
- **extract-rules:** LLM rule structural characteristics (specificity, scale matching, scope isolation, behavioral anchoring) — check if the rule drafting step explicitly covers all four. Add a guard for rules that lack a non-compliant example (already present but should be strengthened with failure-mode data).
- **retrospective:** Missing Anti-Pattern Guards. Add guards for: submitting feedback without reading prior retrospective issues first (duplicate prevention), inventing observations not grounded in the session, using vague language that doesn't produce actionable issues.

- [x] **Step 1:** Read the four context files listed above.
- [x] **Step 2:** Read `skills/check-rules/SKILL.md`, `skills/extract-rules/SKILL.md`, `skills/retrospective/SKILL.md`.
- [x] **Step 3:** Apply at least one substantive change per skill. Add `## Anti-Pattern Guards` to retrospective.
- [x] **Step 4:** Verify: `grep -L "## Anti-Pattern Guards" skills/check-rules/SKILL.md skills/extract-rules/SKILL.md skills/retrospective/SKILL.md` → empty output
- [x] **Step 5:** `python scripts/lint.py --root . --no-urls 2>&1 | grep -E "check-rules|extract-rules|retrospective"` → no new warnings
- [x] **Step 6:** Commit: `git commit -m "feat: refresh governance-and-chain skills against v0.35.0 research"` <!-- sha:c177f3b -->

---

### Task 6: Final validation and roadmap update

- [x] **Step 1:** `grep -L "## Anti-Pattern Guards" skills/*/SKILL.md` → empty output (all 14 have the section)
- [x] **Step 2:** `git diff main...HEAD --name-only | grep "SKILL.md" | wc -l` → 14 (all skills changed)
- [x] **Step 3:** `python scripts/lint.py --root . --no-urls` → no new warnings or failures vs. pre-change baseline
- [x] **Step 4:** Confirm no SKILL.md body exceeds 500 lines: review lint output's instruction density table — no skill should exceed 500 total lines
- [ ] **Step 5:** Update roadmap Task 7 checkbox in `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` with merge commit SHA once PR merges
- [x] **Step 6:** Commit: `git commit -m "chore: validate skill-refresh complete"` <!-- sha:f486a71 -->

---

## Validation

- [ ] `grep -L "## Anti-Pattern Guards" skills/*/SKILL.md` — empty output (all 14 skills have the section)
- [ ] `git diff main...HEAD --name-only | grep "SKILL.md" | wc -l` — outputs `14` (every skill has at least one commit changing it)
- [ ] `python scripts/lint.py --root . --no-urls` — no new warnings or failures vs. pre-change baseline
- [ ] Lint instruction density table — no skill exceeds 500 total lines
- [ ] Each changed skill has a comment or commit message that names the context file that drove the change (evidence of non-cosmetic work)

## Notes

- Branch `feat/skill-refresh` was squash-merged in Task 6 — recreate from main: `git checkout -b feat/skill-refresh`
- check-rules, extract-rules, and retrospective are slated for deprecation in v0.38.0 but still need a refresh pass now (deprecation notice comes later in Task 12/15)
- `build-rule` and `audit-rule` appear in the issue's scope table but don't exist yet — those are created in Task 10/12; exclude from this plan
- distill is not in the issue's cluster table but is on disk and must be covered per acceptance criteria "each SKILL.md reviewed"
- Instruction-file-authoring anti-patterns (`instruction-file-authoring-anti-patterns.context.md`) apply across multiple skills — read it in Task 1 and apply findings throughout
