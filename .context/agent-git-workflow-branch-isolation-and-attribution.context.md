---
name: Agent Git Workflow — Branch Isolation and Attribution
description: Branch-per-task with draft PR and dual attribution is the settled production pattern across GitHub Copilot and Claude Code; agents cannot self-approve or merge.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations
  - https://code.claude.com/docs/en/common-workflows
  - https://code.claude.com/docs/en/permissions
  - https://github.blog/changelog/2026-03-20-trace-any-copilot-coding-agent-commit-to-its-session-logs/
  - https://dev.to/jpoehnelt/agent-identity-for-git-commits-53n1
  - https://openai.com/index/practices-for-governing-agentic-ai-systems/
related:
  - docs/context/agent-git-safety-deterministic-enforcement-and-audit.context.md
  - docs/context/hitl-oversight-as-tuned-policy-and-reversibility-gate.context.md
---
# Agent Git Workflow — Branch Isolation and Attribution

**Branch-per-task + draft PR + human review gate is the settled production pattern.** GitHub Copilot and Claude Code converged on this independently. Agents operate on isolated branches, commit with dual attribution, and cannot self-approve or merge.

## The Standard Pattern

**GitHub Copilot**: creates a dedicated `copilot/*` branch per task, opens a draft PR tagged [WIP], and uses that PR to track work. Once complete, it updates the PR title and description and tags the developer for review. The agent cannot mark its PR as "Ready for review," cannot self-approve, and cannot merge. The user who assigned the task cannot self-approve either.

**Claude Code**: uses `--worktree` to create isolated working directories — each subagent gets its own branch with its own filesystem state, sharing only repository history and remote connections. Subagent worktrees are automatically cleaned up when the subagent finishes without changes. PR creation uses `gh pr create`, and the session is automatically linked to the PR for resumption via `--from-pr <number>`.

## Dual Attribution

Commits from AI agents carry the human who assigned the task as co-author. GitHub Copilot includes an `Agent-Logs-Url` trailer in each commit message — a permanent link from agent-authored commits back to full session logs. All Copilot commits are cryptographically signed and appear "Verified."

This creates an audit trail from any commit back to the full reasoning session that produced it — enabling review of not just what changed but why.

## Bot Identity Isolation

Use environment variables to set agent identity — not global git config. Required variables: `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, `GIT_COMMITTER_EMAIL`, `GIT_SSH_COMMAND`. Normal terminal sessions use personal identity; commands with env vars adopt the bot identity; subsequent commands revert automatically.

Dedicated bot accounts enable:
- Per-repository write access scoping
- CODEOWNERS enforcement and differentiated branch protection rules
- Clean audit trails via `git log --author=<bot-name>`

## Reversibility Principle

OpenAI's governance guidance (T1): "approaches that are easily reversible by the assistant are preferred." Applied to git: branch-level changes over direct main modifications; staged commits over force-push. Agents should default to the approach that leaves a human the most options, not the least.

## What the Pattern Does Not Cover

The protection boundary is main only. Feature branches (`copilot/*`) accumulate commits without gating — bad, insecure, or incorrect commits pile up on the feature branch until a human reviews the PR. Branch protection prevents deployment accidents; it does not prevent a reviewer from approving a 50-commit PR superficially.

For task scoping: open-ended tasks ("refactor this module") produce giant cross-cutting PRs that defeat the review model. The branch-per-task pattern requires well-scoped tasks to work as intended.

## Takeaway

Enforce branch-per-task and require PR review before merge. Use dual attribution and session-log trailers for auditability. Establish a dedicated bot identity with scoped permissions. Recognize that branch protection ensures code cannot reach main without review — it does not ensure that review is meaningful.
