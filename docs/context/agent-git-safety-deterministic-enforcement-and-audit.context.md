---
name: Agent Git Safety — Deterministic Enforcement and Audit
description: "Git safety for agents requires deterministic enforcement at the OS and platform level — branch protection rules, permission-gated operations, and path validation code — not configuration assumptions."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations
  - https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/coding-agent/risks-and-mitigations
  - https://code.claude.com/docs/en/permissions
  - https://www.anthropic.com/engineering/claude-code-sandboxing
  - https://dev.to/ticktockbent/stop-letting-agents-code-push-to-main-2kfk
  - https://arxiv.org/html/2603.15566v1
related:
  - docs/context/agent-git-workflow-branch-isolation-and-attribution.context.md
  - docs/context/hitl-oversight-as-tuned-policy-and-reversibility-gate.context.md
  - docs/context/agentic-resilience-infrastructure-primitives.context.md
---
# Agent Git Safety — Deterministic Enforcement and Audit

**The primary failure mode is unreviewed code landing on main.** If branch protection is absent, an agent with push access will push to main, and CI/CD will deploy. "Your AI coding agent is one bad prompt away from force-pushing to production." The fix is enforcement — not configuration assumptions.

## Required Branch Protection Rules

Essential protections that must be enforced at the platform level:
- Require pull requests before merging to main
- Require status checks to pass before merging
- Block force pushes
- Disable admin bypass exceptions

"Branch protection is foundational but insufficient alone. Additional safeguards needed include secret scanning, CI checks, and AI-specific code review practices."

## Claude Code Permission-Gating

Explicit allow/deny rules for git operations in Claude Code's settings:

```json
{
  "permissions": {
    "allow": ["Bash(git commit *)"],
    "deny": ["Bash(git push *)"]
  }
}
```

The `bypassPermissions` mode skips permission prompts but retains a hard constraint on `.git` directory writes — these always prompt for confirmation to prevent accidental corruption of repository state. This protection cannot be disabled.

Force push and data exfiltration are `soft_deny` defaults in auto mode. These are non-negotiable safety floors.

Claude Code's network sandbox validates git command contents through a proxy: it ensures pushes occur only to configured branches, then attaches proper authentication tokens before contacting GitHub. This OS-level enforcement reduced permission prompts by 84% while maintaining security.

## CVE-2025-68145: Path Validation Must Be Code, Not Config

When `mcp-server-git` was started with `--repository` to restrict operations to a specific path, subsequent tool calls did not validate whether their `repo_path` arguments were within that configured path. An attacker could request paths outside the allowed repository. The fix added explicit path validation that resolved symlinks and verified containment.

**Lesson**: git access restriction requires validation code, not just configuration flags. Assume any path-restriction configuration has a validation gap until explicitly tested.

## Prompt Injection in Git Context

Hidden messages in GitHub Issues or PR comments can inject instructions to AI agents reading them. GitHub filters hidden characters before passing input to Copilot cloud agent — but this is an active mitigation, not a safe assumption about input cleanliness. Treat all external content in the git context (issue titles, PR descriptions, commit messages) as potentially adversarial input.

## CI/CD Default Behavior

GitHub Actions workflows do not execute until a repository maintainer explicitly approves them for first-time contributors. However, established-identity agent accounts or repos with permissive CI settings bypass this gate. Do not rely on the default as a security boundary if the agent runs under a trusted contributor identity.

## Structured Commit Metadata

The Lore protocol (arXiv, March 2026) proposes structured git trailers — `Constraint`, `Rejected`, `Reversibility`, `Scope-risk`, `Confidence`, `Directive` — to encode agent reasoning durably in commit history. The rationale is sound (atomic binding to the diff, universal git availability, agent-parseable), but Lore is a research proposal with no deployment in Copilot, Claude Code, or any major platform. Do not plan for it.

Currently: Copilot's `Agent-Logs-Url` trailer is the only production-deployed structured commit metadata, and it requires GitHub's session log infrastructure to be useful.

## Takeaway

Enforce safety at the platform level: branch protection rules, explicit deny rules for push operations, OS-level sandbox enforcement. Do not rely on prompt instructions to prevent force-push. Treat CVE-2025-68145 as a design principle: path restriction requires validation code. Test your restrictions, not just your configuration.
