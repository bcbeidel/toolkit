---
name: Quality Ratchet Pattern for Gradual Enforcement
description: "Version-control a per-file, per-rule violation baseline in TSV format. CI blocks merges that increase any count; fixes reduce it. Gradual quality improvement without blocking velocity."
type: concept
confidence: medium
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.notion.com/blog/how-we-evolved-our-code-notions-ratcheting-system-using-custom-eslint-rules
related:
  - docs/context/precommit-hooks-vs-ci-enforcement-boundary.context.md
  - docs/context/ci-validation-for-llm-generated-code.context.md
  - docs/context/rule-library-operational-practices.context.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
---
# Quality Ratchet Pattern for Gradual Enforcement

## Key Insight

The ratchet pattern enables gradual quality improvement without blocking velocity. Version-control a per-file, per-rule violation baseline. CI blocks merges that increase any violation count; fixes reduce it. The baseline ratchets down over time — quality improves without requiring a clean-slate enforcement that would block all development.

## How the Pattern Works

1. **Capture baseline**: Run the linter or quality tool across the entire codebase. Record the violation count per file per rule in a version-controlled TSV file. TSV is preferred over JSON specifically to avoid merge conflicts when multiple developers modify the baseline simultaneously.

2. **CI enforcement**: On every PR, run the same tool and compare results to the baseline. If any file has more violations than its baseline count, the merge is blocked. If it has fewer (or the file is new with zero violations), the merge proceeds.

3. **Ratchet direction**: The baseline is immutable in the increase direction — no PR can make quality worse. Fixes reduce the count in the baseline, permanently tightening the constraint for subsequent PRs. Over time the baseline approaches zero without requiring a "big bang" enforcement.

## Why TSV Format

Notion Engineering chose TSV specifically because JSON baselines produced frequent merge conflicts when multiple developers modified the same file's violation counts in different branches. TSV's line-per-entry structure minimizes conflict surface: edits to different files produce non-overlapping lines.

## Applicability to LLM-Generated Code

The ratchet pattern is particularly valuable for codebases where LLM-generated code introduces measurable quality regressions. Rather than adding a hard gate that fails all LLM PRs until they meet a clean standard (which blocks velocity), the ratchet prevents PRs from making quality *worse* while allowing gradual improvement.

Ruff's `--statistics` output and `noqa` suppression tracking implement the same pattern for Python: track suppression counts per rule, block merges that increase any suppression count.

## Relationship to Warn-Before-Enforce

The ratchet pattern is complementary to the warn-before-enforce practice. The initial baseline capture is equivalent to the warning period: existing violations are acknowledged and recorded rather than immediately blocking. New violations are blocked. This is the "start where you are, move in one direction" implementation of gradual enforcement.

## Takeaway

When the codebase has accumulated violations that would block all development if enforced immediately, the ratchet pattern is the correct path. It turns quality improvement into a monotonic process: each fix reduces the baseline permanently, each new PR cannot increase it. The TSV format prevents the baseline file itself from becoming a conflict source.
