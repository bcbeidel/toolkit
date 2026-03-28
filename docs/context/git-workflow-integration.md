---
name: "Git Workflow Integration for Agent-Driven Development"
description: "Branch naming, atomic commits, PR automation, worktree isolation, and CI/CD parity patterns for integrating agent-produced code into team git workflows"
metadata:
  type: reference
  sources:
    - https://nx.dev/blog/git-worktrees-ai-agents
    - https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/
    - https://www.conventionalcommits.org/en/v1.0.0/
    - https://github.com/semantic-release/semantic-release
    - https://git-scm.com/docs/git-revert
  related:
    - docs/research/git-workflow-integration.md
    - docs/context/multi-agent-coordination.md
    - docs/context/human-in-the-loop-design.md
    - docs/context/workflow-orchestration.md
---

Agent-driven development introduces new demands on git workflows. Agents produce commits at machine speed, operate in parallel, and lack the social awareness that makes team conventions self-enforcing. Six practices address this, and they work together as a unified integration pattern applicable to trunk-based, GitHub Flow, and GitFlow workflows alike.

## Branch Naming

Agent branches must be distinguishable from human branches for filtering, CI routing, and cleanup automation. The converging convention is `<type>/<agent>/<task-slug>` (e.g., `feat/claude/add-auth-middleware`). GitHub Copilot enforces a `copilot/` prefix; teams using other agents should adopt analogous conventions through pre-push hooks or CI checks. The type prefix enables conventional commit alignment, the agent name provides attribution and filtering, and the slug provides human-readable context.

## Atomic Commits as Rollback Boundaries

Each agent commit must represent a reversible unit of work: one logical change, codebase in valid state afterward. This enables clean rollback via `git revert`, which creates an inverse commit preserving history. `git reset --hard` is appropriate only for local agent cleanup before push — never on shared branches where others may have pulled. Agent instructions should encode this as an invariant.

Agents can produce either extremely fine-grained commits (every file save) or extremely coarse ones (entire feature). Neither extreme serves rollback. The target is one commit per logical change: a function addition, a test suite, a configuration update.

## Conventional Commits

The Conventional Commits format (`<type>[scope]: <description>`) is mechanical and rule-based — well-suited for agents. Types map to semantic versioning: `fix` triggers PATCH, `feat` triggers MINOR, `feat!` or `BREAKING CHANGE` triggers MAJOR. Combined with commitlint (local hook enforcement) and semantic-release (CI-driven versioning), this enables fully automated release pipelines from agent-produced commits.

Agent-specific metadata fits in commit trailers: `Co-Authored-By` for attribution, `Agent:` and `Task:` for traceability.

## PR Automation

Agents create PRs via `gh pr create` with structured metadata: conventional commit-style titles, structured body (summary, changes, test plan), labels for agent attribution, and auto-assigned reviewers from CODEOWNERS. Draft status signals agent confidence — draft means needs iteration, ready means confident.

Human review remains a mandatory gate. Agents cannot approve or merge their own PRs. GitHub Agentic Workflows (2026 technical preview) formalize this with read-only default permissions, sandboxed execution, and explicit "safe outputs" for write operations.

## Worktree Isolation

Git worktrees are the dominant isolation pattern for parallel agent work. Each agent gets its own working directory on a dedicated branch while sharing a single `.git` directory — low disk cost, no remote sync overhead, shared history. Tools like Worktrunk and ccswarm automate worktree lifecycle.

Limitations: one branch per worktree, merge conflicts are deferred not prevented, and shared resources beyond git (databases, Docker daemon) can create race conditions between agents.

## CI/CD Parity

Agent-produced code passes through identical CI gates as human code — unit tests, linting, type checking, security scanning, branch protection rules. The principle is equal scrutiny, not special treatment. GitHub explicitly states that agentic workflows complement deterministic CI/CD, not replace it.

Agent-specific CI considerations: rate limiting (agents produce PRs faster than CI processes them), avoiding auto-retry on flaky tests (masks real failures), and managing resource costs from high-volume agent PRs.

## The Non-Negotiable

Agents must never push directly to protected branches. All agent work flows through PRs with human approval. This constraint holds across all team git workflows and is the single rule that makes agent integration compatible with existing processes.
