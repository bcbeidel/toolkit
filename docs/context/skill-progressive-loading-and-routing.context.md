---
name: "Skill Progressive Loading and Routing"
description: "Skill descriptions (~100 tokens) stay in context permanently; full bodies load only on invocation — description quality is the routing signal and determines selection accuracy"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://code.claude.com/docs/en/skills
  - https://agentskills.io/specification
  - https://arxiv.org/html/2602.12430v3
related:
  - docs/context/skill-mcp-tool-subagent-taxonomy.context.md
  - docs/context/tool-description-quality-and-consolidation.context.md
  - docs/context/agent-context-file-quality-over-completeness.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
---
The core token-efficiency mechanism in skill ecosystems is progressive loading. Skill descriptions (~100 tokens each) are loaded into context at session start for every installed skill. The full `SKILL.md` body (~5,000 tokens) loads only when a skill is explicitly invoked. This design makes large skill ecosystems feasible without saturating the context window.

**The description is the routing signal.** Claude Code's auto-invocation works by semantic matching: all descriptions are in context, Claude matches the user's message against them, and loads the relevant skill. The description is not supplementary metadata — it is the input to the classifier. Description quality directly determines whether the right skill gets selected.

The Agent Skills specification caps descriptions at 1,024 characters. Claude Code's skill listing truncates entries at 250 characters. This means the first sentence of a description carries disproportionate weight. Front-loading the key use case — not the implementation details — is the single highest-leverage act in skill authorship.

**Routing degradation at scale.** An academic survey (arxiv 2602.12430, 2026) identified a phase transition in skill selection accuracy as library size grows. Beyond certain ecosystem sizes, routing reliability degrades sharply. This creates a practical ceiling on how many skills can coexist before the description pool becomes noisy enough to cause misrouting.

Mitigation strategies:
- Keep descriptions specific and use case-focused, not capability-focused
- Use `user-invocable: false` for reference skills not intended for the routing pool — their descriptions are hidden from auto-matching
- Use `disable-model-invocation: true` to remove a skill from context entirely (explicit invocation only)
- Scope skills to paths (Claude Code `paths:` field) to narrow routing to relevant contexts
- Treat routing failures as description quality problems, not library size problems — usually fixable with better phrasing before reducing ecosystem size

**Explicit invocation bypasses routing.** When a user types `/skill-name`, Claude loads and executes that skill without evaluating descriptions. This is the escape hatch for skills that are difficult to route by description alone or that require deliberate human initiation.

**Implication for context files.** The same progressive loading rationale applies to context documents. A document's frontmatter `description` field is what agents read when scanning an index — the full document loads only when the agent decides to read it. Context file descriptions have the same front-loading requirement as skill descriptions.
