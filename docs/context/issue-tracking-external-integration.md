---
name: "Issue Tracking and External Integration Patterns"
description: "Three integration layers, authentication tiers, deduplication strategies, and feedback loop patterns for agent-to-issue-tracker systems"
metadata:
  type: reference
  sources:
    - https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/
    - https://github.com/anthropics/claude-code/blob/main/.github/workflows/claude-dedupe-issues.yml
    - https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3
    - https://docs.github.com/en/rest/issues/issues
    - https://linear.app/developers/graphql
    - https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
    - https://github.com/atlassian/atlassian-mcp-server
  related:
    - docs/research/issue-tracking-external-integration.md
    - docs/context/feedback-loop-design.md
    - docs/context/tool-design-for-llms.md
    - docs/context/multi-agent-coordination.md
---

Agent systems interact with issue trackers through three integration layers, three authentication tiers, and four feedback loop patterns. The right combination depends on scope: single-platform scripts need different patterns than multi-tenant agent fleets.

## Three Integration Layers

**Direct API calls** remain the foundation. GitHub Issues uses REST, Linear uses GraphQL, Jira uses REST -- all accept structured payloads that agents populate from templates or LLM-generated content. This is the right choice for single-platform, single-tenant automation.

**MCP-mediated tool calls** provide cross-platform abstraction. Atlassian maintains an official MCP server for Jira, Confluence, and Compass. Third-party MCP servers cover Linear and combined Jira+Linear access. MCP separates agent protocol-level access from API-level credentials. Still early-stage (introduced late 2024), but adoption is accelerating.

**Orchestration platforms** (Composio, Sarge) add a middleware layer for multi-tenant scenarios. The agent calls generic actions; the platform translates to platform-specific APIs while managing OAuth flows, token refresh, and credential storage.

## Authentication Tiers

Authentication complexity should match deployment scope:

- **Direct tokens** (PATs, API keys) for development and personal scripts
- **OAuth 2.0** for production integrations serving multiple users -- all three major platforms support it
- **Brokered credentials** for multi-tenant agent systems where the LLM never sees user tokens

GitHub Actions' built-in `GITHUB_TOKEN` with read-only-by-default permissions is the most developer-friendly pattern. GitHub Agentic Workflows enforce this: write actions must pass through reviewable "safe outputs."

## Deduplication: The Missing Piece

Most agent systems that create issues have no deduplication strategy. The notable exception is Claude Code's multi-agent semantic search: when a new issue is opened, 5 parallel sub-agents search for duplicates using diverse keywords, returning up to 3 likely matches. Confirmed duplicates get a 3-day grace period before auto-close, avoiding false-positive closures. This search-before-create pattern is the current best practice but remains rare in production systems.

## Feedback Loop Patterns

Four patterns have emerged, ordered by sophistication:

1. **Issue-to-PR pipeline.** Agent reads an issue, generates code, creates a PR, links it back. The most common pattern (SWE-agent, Sarge, CodeRabbit).

2. **CI-driven iteration.** Agents monitor CI results and iterate until checks pass. Spotify's Honk system uses independent verifiers plus an LLM judge that vetoes ~25% of proposed changes; the agent course-corrects about half the time. Datadog's Bits AI opens PRs as drafts, marks them ready when checks pass.

3. **Bidirectional ticket updates.** PR review feedback flows back to issue trackers automatically. CodeRabbit updates linked Jira and Linear tickets with component validation status.

4. **Self-generated follow-up issues.** Agents create new issues for problems found during self-review, creating a recursive loop where agent activity generates trackable work items.

## Inner vs. Outer Loops

Spotify's distinction between inner loops (agent-local verification before PR creation) and outer loops (reacting to CI failures and review comments on submitted PRs) is architecturally significant. Most production systems implement only the inner loop today. The outer loop -- where agents respond to post-submission feedback -- is the emerging frontier. This mirrors the broader pattern in feedback loop design: verification layers closest to the action are easiest to implement, while layers that cross system boundaries require more coordination infrastructure.

## Key Design Decisions

When building agent-to-tracker integration, three choices dominate:

- **Layer selection:** Direct API for single-platform, MCP for cross-platform, orchestration for multi-tenant
- **Deduplication investment:** Search-before-create with semantic matching prevents issue proliferation but adds latency and complexity
- **Feedback scope:** Inner-loop verification is table stakes; outer-loop CI response differentiates sophisticated systems
