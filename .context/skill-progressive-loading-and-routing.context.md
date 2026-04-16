---
name: "Skill Progressive Loading and Routing"
description: "Skill descriptions (~100 tokens) stay in context permanently; full bodies load only on invocation — description quality is the routing signal and determines selection accuracy"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-11
sources:
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://developers.openai.com/api/docs/guides/function-calling
  - https://agentskills.io/specification
  - https://arxiv.org/html/2602.12430v3
  - https://arxiv.org/abs/2602.20426
related:
  - docs/context/skill-mcp-tool-subagent-taxonomy.context.md
  - docs/context/tool-description-quality-and-consolidation.context.md
  - docs/context/agent-context-file-quality-over-completeness.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/skill-routing-failure-modes-and-pushy-heuristic.context.md
  - docs/context/skill-description-authoring-cross-platform.context.md
  - docs/research/2026-04-11-skill-description-routing.research.md
---
The core token-efficiency mechanism in skill ecosystems is progressive loading. Skill descriptions (~100 tokens each) are loaded into context at session start for every installed skill. The full `SKILL.md` body (~5,000 tokens) loads only when a skill is explicitly invoked. This design makes large skill ecosystems feasible without saturating the context window.

**The description is the routing signal.** Claude Code's auto-invocation works by semantic matching: all descriptions are in context, Claude matches the user's message against them, and loads the relevant skill. The description is not supplementary metadata — it is the input to the classifier. Description quality directly determines whether the right skill gets selected.

**Descriptions must convey both what and when.** Anthropic's documented pattern requires descriptions to answer two questions: what the skill does, and when to use it. Descriptions that answer only one underperform. The recommended format: an action phrase ("Processes Excel files and generates reports") followed by a trigger clause ("Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files"). This pattern is prescriptive consensus across Anthropic and OpenAI; it is not experimentally ablated (MODERATE confidence). The trigger clause is the most direct route to matching user vocabulary, which is the documented mechanism behind routing recall (S1, S3).

**The 250-character truncation constraint.** The Agent Skills specification allows up to 1,024 characters in the description field. Claude Code's skill listing truncates each entry to 250 characters to reduce context usage — this is the operative routing context. Only the first 250 characters participate in routing. Everything after the truncation point is not present when Claude decides whether to invoke the skill. This is not a soft recommendation; it is a stated architectural constraint (S1). Front-loading the key use case — the most discriminating trigger signal — is the single highest-leverage act in skill authorship. If the "Use when..." clause runs past ~200 characters, it will be cut.

**The mechanism transfer gap.** The academic research base on description-driven routing (BFCL, KAMI, ToolTweak, Gorilla, arXiv:2602.20426) entirely studies API-style function calling: tool definitions delivered in the API payload, where models may have been fine-tuned on structured JSON schemas. Claude Code skill routing works differently — descriptions are injected into the system prompt at session startup. Whether findings from function-calling research transfer to system-prompt-injected descriptions is an untested assumption (S1, S2). The architectural surfaces differ; the routing behavior may or may not be analogous. Treat API-based routing findings as directionally informative for Claude Code skills, not as validated evidence for the specific mechanism.

**Routing degradation at scale.** An academic survey (arxiv 2602.12430, 2026) identified a phase transition in skill selection accuracy as library size grows. Beyond certain ecosystem sizes, routing reliability degrades sharply. This creates a practical ceiling on how many skills can coexist before the description pool becomes noisy enough to cause misrouting.

Mitigation strategies:
- Keep descriptions specific and use case-focused, not capability-focused
- Use `user-invocable: false` for reference skills not intended for the routing pool — their descriptions are hidden from auto-matching
- Use `disable-model-invocation: true` to remove a skill from context entirely (explicit invocation only)
- Scope skills to paths (Claude Code `paths:` field) to narrow routing to relevant contexts
- Treat routing failures as description quality problems, not library size problems — usually fixable with better phrasing before reducing ecosystem size

**Explicit invocation bypasses routing.** When a user types `/skill-name`, Claude loads and executes that skill without evaluating descriptions. This is the escape hatch for skills that are difficult to route by description alone or that require deliberate human initiation.

**Implication for context files.** The same progressive loading rationale applies to context documents. A document's frontmatter `description` field is what agents read when scanning an index — the full document loads only when the agent decides to read it. Context file descriptions have the same front-loading requirement as skill descriptions.
