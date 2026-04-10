---
name: "Skill, MCP, Tool, and Subagent Taxonomy"
description: "Skills, MCP servers, tools, and subagents are orthogonal composable layers — one skill per coherent workflow, not per API endpoint"
type: context
sources:
  - https://agentskills.io/specification
  - https://code.claude.com/docs/en/skills
  - https://www.llamaindex.ai/blog/skills-vs-mcp-tools-for-agents-when-to-use-what
  - https://dev.to/phil-whittaker/mcp-vs-agent-skills-why-theyre-different-not-competing-2bc1
  - https://arxiv.org/html/2602.12430v3
related:
  - docs/context/skill-progressive-loading-and-routing.context.md
  - docs/context/mcp-vs-function-calling-tradeoffs.context.md
  - docs/context/tool-description-quality-and-consolidation.context.md
  - docs/context/production-reliability-gap-and-multi-agent-failures.context.md
---

Four layers compose the agentic tool stack. They are orthogonal and composable, not competing alternatives:

| Layer | What it is | Context cost | Determinism | Primary use |
|---|---|---|---|---|
| Tools | Atomic functions (single input/output) | Low per-call | High | Read file, search, run command |
| MCP servers | Protocol-based service adapters | Medium (per-use) | High | Third-party integrations, auth, data access |
| Skills | Instruction bundles with progressive disclosure | Low at rest, medium when active | Low (LLM-driven) | Procedural workflows, behavioral guidance |
| Subagents | Isolated agents with separate context windows | High (full fork) | Medium | Complex isolated tasks, parallel workstreams |

The right mental model: **skills are the brain** (procedural knowledge, standing instructions), **MCP is the muscle** (deterministic execution, service connectivity), **subagents are map/reduce** for complex isolated tasks. A skill may instruct the use of a specific MCP server, specify how to interpret its outputs, and define fallback strategies — they compose cleanly.

**Granularity calibration.** Too fine (one skill per API endpoint or per file type) causes routing degradation as library size grows — the arxiv 2026 survey identifies a phase transition in selection accuracy beyond certain ecosystem sizes. Too coarse (one skill per major domain) makes selective disabling or updating impossible. The sweet spot is one skill per coherent workflow that a practitioner would naturally hand off as a unit of work.

Calibration heuristics:
- Keep `SKILL.md` under 500 lines; move detailed references to separate files
- Use `user-invocable: false` for sub-workflow reference knowledge — keeps routing pool clean
- Domain-level granularity (e.g., "deployment workflows") outperforms function-level granularity ("call deploy endpoint")

**Composition has no standard primitive.** The Agent Skills spec deliberately omits declarative composition — there is no "skill A calls skill B" mechanism in the standard. Composition happens through: `context: fork` (subagent-based, Claude Code), AGENTS.md if/then rules mandating skill sequences (Codex), code-level workflow patterns, and implicit LLM routing by mentioning skill names in instructions. This is an active gap in the ecosystem.

**The proliferation anti-pattern.** Excessive tool and skill counts are a consistently documented failure mode. Each additional description in the routing pool adds noise. The LlamaIndex finding: "Skills were rarely invoked and often did not yield substantially better results" when MCP documentation was already available — adding skills at the micro-task level adds overhead without proportional benefit.

A skill may invoke MCP, subagents, and tools in sequence. The correct design question is not "which layer" but "what is the boundary of meaningful work that justifies a discrete unit."
