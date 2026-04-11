---
name: audit-chain
description: >
  Design a skill chain from a goal, or audit an existing chain manifest for
  structural and contract issues. Use when the user wants to "design a chain",
  "create a workflow", "check a chain manifest", "audit a chain", or "repair
  a chain".
argument-hint: "[workflow goal or path/to/manifest.chain.md]"
user-invocable: true
---

# Audit Chain

Design a `*.chain.md` manifest from a workflow goal, or audit an existing
manifest for structural and contract correctness with an opt-in repair loop.

## Workflow

### Detect Mode

- **Argument is a path to a `*.chain.md` file** → **Manifest mode**
- **No argument, or free-text goal** → **Goal mode**

### Goal Mode

1. **Discover skills** — list available SKILL.md files from `skills/` (and any
   installed plugin `skills/` directories). Present as a numbered list with descriptions.
2. **Structured dialogue** — collect in order:
   - Skill sequence (ordered; user can reorder or add)
   - Output contract per step (what artifact or state does this step produce?)
   - Input requirement per step (what does this step need from the prior step?)
   - Gate condition per consequential step (when does a human review before continuing?)
   - Termination condition (what constitutes chain-complete success?)
   - Negative scope (what does this chain explicitly not do?)
3. **Produce manifest** — write `plans/YYYY-MM-DD-<name>.chain.md`:
   - Frontmatter: `name`, `description`, `type: chain`, `goal`, `negative-scope`
   - Body: `## Steps` pipe table — `| Step | Skill | Input Contract | Output Contract | Gate |`
4. **Hard gate** — present for user review. State: "This is a design artifact — invoke
   `/wos:execute-plan` or run each skill manually to execute." Do not invoke any step.

### Manifest Mode

1. **Structural checks** — run `scripts/lint.py --root <project-root> --no-urls` and
   extract chain findings for the target manifest. Surface structural failures before
   cross-reference (fast fail first). If `parse_chain()` raises on a malformed manifest,
   report it as a `fail` finding and continue — do not crash.
2. **Cross-reference check** — for each step: read the referenced SKILL.md body; assess
   whether the declared `output_contract` is plausible given what the skill actually
   produces. Flag mismatches as `warn` (not `fail`).
3. **Findings table** — present all findings:
   ```
   | File | Issue | Severity |
   |------|-------|----------|
   ```
   Summary line: `N fail, N warn`. Sort: fail before warn; structural before cross-reference.
4. **Repair loop** — ask: "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."
   For each selected finding:
   - Manifest fix: propose targeted edit, show diff, apply on confirmation
   - SKILL.md fix: propose targeted edit, show diff, apply on confirmation
   - Missing skill (step references a skill that doesn't exist): invoke `/wos:build-skill`
     inline to create it, then re-check existence
5. **Re-verify** — after each applied fix, re-run `scripts/lint.py` and re-run
   cross-reference on affected steps. Return to findings presentation.
6. **Exit** — when all findings are resolved or user declines remaining fixes:
   "Chain manifest is well-formed — 0 issues found."

## Anti-Pattern Guards

1. **Cross-reference before structural checks** — `scripts/lint.py` runs first, always;
   surface structural failures before LLM judgment
2. **Bulk repair without per-change confirmation** — each fix requires separate confirmation;
   never apply more than one change without a confirmation step between them
3. **Executing the chain in goal mode** — goal mode produces a design artifact only; the
   hard gate must be stated explicitly before exiting
4. **Treating cross-reference mismatches as fail** — cross-reference findings are `warn`;
   the user decides whether the contract or the SKILL.md needs updating
5. **Crashing on malformed manifest** — if parsing fails, report as a `fail` finding and
   continue; partial or incomplete manifests produce findings, not errors

## Handoff

**Receives:** Free-text workflow goal (goal mode) or path to `*.chain.md` (manifest mode)
**Produces:** Goal mode — `plans/YYYY-MM-DD-<name>.chain.md`. Manifest mode — structured
findings table; optionally, targeted edits applied to the manifest or referenced SKILL.md files.
**Chainable to:** execute-plan (to run the chain steps), build-skill (gap case in repair loop)

## Key Instructions

- Goal mode is design-only — never invoke a step in the chain; the manifest is the deliverable
- Cross-reference is LLM judgment — flag mismatches as `warn` only; the user decides what to fix
- Per-change confirmation is non-negotiable — never apply more than one fix without separate confirmation
- `scripts/lint.py` structural checks cover 5 dimensions (skills exist, contracts declared, gates
  on consequential steps, termination condition, no cycles) — do not re-implement them
- Won't: execute chain steps, bulk-apply fixes, or treat cross-reference mismatches as hard failures
