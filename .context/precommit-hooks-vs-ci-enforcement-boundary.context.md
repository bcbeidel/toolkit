---
name: Pre-Commit Hooks vs CI Enforcement Boundary
description: Fast checks belong in pre-commit (developer convenience); slow checks belong in CI (enforcement gate) — pre-commit.ci bridges the gap by running hooks on every PR without custom YAML.
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://pre-commit.ci/
  - https://motlin.medium.com/pre-commit-or-ci-cd-5779d3a0e566
  - https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835
  - https://github.com/astral-sh/ruff-pre-commit
related:
  - docs/context/quality-ratchet-pattern-for-gradual-enforcement.context.md
  - docs/context/ci-validation-for-llm-generated-code.context.md
  - docs/context/agent-driven-ci-guardrails-and-confidence-routing.context.md
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
---
# Pre-Commit Hooks vs CI Enforcement Boundary

## Key Insight

Pre-commit hooks are a development-loop accelerator, not an enforcement gate. `--no-verify` is always available. The enforcement gate belongs in CI (via branch protection) or pre-commit.ci (hosted service). Fast checks stay client-side; slow checks move to CI. pre-commit.ci bridges this without requiring custom CI YAML (HIGH — T1 sources, design principle corroborated across multiple sources).

## The Design Principle

Hooks that exceed approximately 1 second routinely get bypassed with `--no-verify`. Once a developer bypasses hooks a few times, they typically disable them entirely. This creates a failure mode where one developer's bypass affects the entire team through failed CI checks later.

The practical implication is a design boundary: **hooks should be restricted to fast, local checks** (formatting, simple linting, secret scanning). **Slow checks belong in CI** — mypy full type checking, pytest execution, CodeQL scanning. The question is not "make hooks faster" but "which checks belong client-side at all?"

Note: The 1-second threshold is a rule of thumb, not an empirical law. Team culture is a confounding variable — `--no-verify` is also a legitimate escape hatch for WIP commits and emergencies, not only a sign of enforcement failure.

## What Belongs Where

**Pre-commit hooks (fast, local):**
- `ruff check --fix` (linting with autofix) — must run before `ruff format`
- `ruff format` (formatting)
- GitLeaks or detect-secrets (secret scanning on staged files)
- ShellCheck (shell script static analysis)

**CI enforcement (slow, mandatory):**
- mypy full type checking (with `.mypy_cache` for incremental caching)
- pytest with coverage thresholds
- CodeQL SAST (PR-targeted incremental + scheduled full-repo scans)
- bandit (Python security scanning)

The hook ordering for ruff is critical: `ruff check --fix` (linter with autofix) must precede `ruff format` (formatter). Running in reverse order produces incorrectly formatted lint fixes.

## pre-commit.ci as the Bridge

pre-commit.ci is a hosted service that runs hooks on every PR automatically. It:
- Requires zero configuration beyond `.pre-commit-config.yaml`
- Auto-commits fixes when hooks make changes (formatting corrections appear as a PR commit)
- Auto-updates hook versions weekly
- Runs even when developers skip hooks locally

This bridges the gap between optional local hooks and mandatory enforcement without requiring custom CI YAML or job configuration. Teams get enforcement without the friction of maintaining CI integration for pre-commit.

## Selective Strictness (STRICT Tier Pattern)

A hook configuration pattern: tier hooks as standard (always enabled) vs. STRICT (commented out by default). STRICT hooks — mypy in strict mode, comprehensive markdownlint rules — are commented out and enabled as the codebase matures. This avoids requiring global day-one adoption while preserving a documented path to tighter enforcement.

This mirrors the ratchet pattern at the hook configuration level: progressively tighten rather than mandate all checks at once.

## Enforcement Gate

Branch protection rules requiring CI status checks on all jobs — not just the final build — are the mandatory enforcement layer. A green build that masks a failing lint job is not useful. Require status checks from lint, type-check, and test jobs independently so partial failures surface immediately.

## Takeaway

Design hooks to be fast enough that bypass is rarely tempting, then accept that bypass will occur for legitimate reasons. Ensure CI is the actual gate. Use pre-commit.ci to run hooks on every PR without custom CI YAML. Apply the STRICT tier pattern to progressively tighten enforcement without mandating everything at once.
