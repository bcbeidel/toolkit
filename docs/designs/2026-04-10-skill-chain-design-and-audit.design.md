---
name: Skill Chain Design and Audit
description: Two skills and a lint extension for designing, documenting, and validating Claude Code skill chains — design-chain produces a chain manifest, check-chain cross-references it against actual SKILL.md files, and lint auto-detects chain manifests for structural checks.
type: design
status: draft
related:
  - docs/context/skill-handoff-contracts-and-state-design.context.md
  - docs/context/skill-chain-failure-modes-and-antipatterns.context.md
  - docs/context/skill-chain-sequential-and-recursive-design-rules.context.md
  - docs/context/skill-chain-hitl-patterns-and-cli-translation-gap.context.md
  - docs/context/skill-chain-handoff-signaling-and-evidence-packs.context.md
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
  - docs/research/2026-04-10-skill-effectiveness-audit.research.md
  - docs/plans/2026-04-09-wiki-structural-refactor.plan.md
---

# Skill Chain Design and Audit

Two skills and a lint extension that bring design discipline to Claude Code
skill chains. The chain manifest (`*.chain.md`) is the central artifact — a
human-readable specification that documents skill sequence, handoff contracts,
and gate points. Human execution: the user reads the manifest and invokes each
skill manually. No automated execution.

## Purpose

Most skill chain failures are structural design failures, not prompt failures
(MASFT research). The highest-leverage intervention is declaring output
contracts before writing skills. These tools make that discipline tractable:
`design-chain` forces explicit contract declaration at design time;
`check-chain` verifies those contracts against reality; `lint` catches
structural gaps automatically.

## Behavior

### `design-chain`

1. Takes a user-described workflow goal as free-text input
2. Discovers available SKILL.md files across the project and any installed
   plugins
3. Through structured dialogue: establishes skill sequence, elicits an output
   contract per skill (what it produces), declares input requirements per
   skill (what it needs from the prior step), identifies human gate points,
   declares termination condition and chain-level negative scope
4. Produces `plans/YYYY-MM-DD-<name>.chain.md` documenting all of the above
5. Hard gate: design only — does not create SKILL.md files, does not invoke
   any skill in the chain

### `check-chain`

Four phases; the last is opt-in:

1. **Existence** — each skill declared in the manifest exists and is
   accessible
2. **Internal consistency** — each step's declared input matches the prior
   step's declared output; termination condition present; gate points declared
   before consequential steps; no circular references
3. **Cross-reference** — reads each referenced SKILL.md body; uses LLM
   judgment to assess whether the manifest's declared output contract for each
   skill is plausibly supported by what the SKILL.md body actually describes;
   flags mismatches as findings
4. **Improvement (opt-in)** — after showing findings, proposes specific edits
   to the manifest or SKILL.md files; applies only on per-change confirmation

Output format: structured findings (file, issue, severity) matching
`scripts/lint.py` output format.

### `lint` extension

Auto-detects `*.chain.md` files in the project during a normal lint pass.
When found, runs structural chain checks (phases 1–2 of `check-chain`).
No new flag required. Same auto-activation pattern as wiki checks.
Structural checks only — no LLM judgment in `scripts/lint.py`.

## Components

**New skills:**
- `skills/design-chain/SKILL.md`
- `skills/check-chain/SKILL.md`

**New Python module:**
- `wos/chain.py` — structural validators:
  - `parse_chain(manifest_path)` — reads and parses a `*.chain.md` manifest
  - `check_chain_skills_exist(manifest, skills_dirs)` — each declared skill exists
  - `check_chain_internal_consistency(manifest)` — handoff outputs match inputs
  - `check_chain_gates(manifest)` — gate points present before consequential steps
  - `check_chain_termination(manifest)` — termination condition declared
  - `check_chain_cycles(manifest)` — no circular skill references
- `tests/test_chain.py` — tests for `wos/chain.py`

**Modified:**
- `wos/validators.py` — add `validate_chain(manifest_path, skills_dirs)`
- `scripts/lint.py` — auto-detect `*.chain.md`; call `validate_chain()` when found
- `tests/test_lint.py` — chain auto-detection tests

**New file type:**
`*.chain.md` — lives in `plans/`. Must declare at the chain level: name,
goal, termination condition, chain-level negative scope. Must declare per
skill: which skill, what it produces (output contract), what it requires from
the prior step (input contract), gate type.

## Constraints

**`design-chain`:**
- Produces a manifest only — does not create SKILL.md files, does not invoke
  any skill in the chain
- Hard gate: design only, no implementation actions
- The manifest must be human-readable without running any tool

**`check-chain`:**
- Does not modify anything without explicit per-change user confirmation
- Improvement phase is opt-in — only triggered after user reviews findings
- Structural checks run before LLM cross-referencing (fast fail first)
- Partial or incomplete manifests produce findings, not errors

**`lint` extension:**
- Auto-activation only — no new flag required
- Structural checks only — no LLM judgment in `scripts/lint.py`
- Additive — projects without chain manifests see identical `lint` behavior

**Both skills:**
- Work on SKILL.md files from any source — WOS plugin or user-defined

## Acceptance Criteria

1. A user with a multi-step workflow goal can run `/wos:design-chain` and
   receive a `*.chain.md` manifest in `plans/`
2. `/wos:check-chain` against that manifest surfaces mismatches between
   declared output contracts and what SKILL.md bodies actually describe
3. `scripts/lint.py` on a project with `*.chain.md` files includes structural
   chain findings in the output
4. `scripts/lint.py` on a project without `*.chain.md` files produces
   identical output to before — no regression
5. A chain manifest with undeclared output contracts produces a specific
   finding per missing contract in both `check-chain` and `lint`
6. The improvement phase proposes specific edits; does not apply without
   per-change confirmation
7. `from wos.chain import parse_chain, check_chain_skills_exist,
   check_chain_internal_consistency, check_chain_gates,
   check_chain_termination, check_chain_cycles` imports cleanly
