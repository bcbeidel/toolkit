---
name: "Agent Skills Open Standard Has No Independent Governance"
description: "The Agent Skills file format standard has no independent stewardship body — Anthropic controls spec evolution, creating fragmentation risk as vendors add proprietary extensions"
type: context
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://www.mindstudio.ai/blog/agent-skills-open-standard-claude-openai-google
  - https://elguerre.com/2026/03/30/ai-agents-vs-skills-commands-in-claude-code-codex-copilot-cli-gemini-cli-stop-mixing-them-up/
  - https://modelcontextprotocol.io/docs/concepts/tools
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/mcp-vs-skill-format-abstraction-layers.context.md
  - docs/context/skill-frontmatter-extensions-claude-code-specific.context.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
---

# Agent Skills Open Standard Has No Independent Governance

Evidence suggests the Agent Skills file format standard (SKILL.md) has no independent standards body governing its evolution. Anthropic published the spec in December 2025 and remains the primary maintainer. This creates a fragmentation risk: each vendor implementing the standard will add proprietary extensions (Claude Code already has), compressing the window of genuine cross-runtime portability.

## The Governance Contrast With MCP

MCP (Model Context Protocol) has a clear governance trajectory: Anthropic donated it to the Linux Foundation/Agentic AI Foundation (AAIF), with OpenAI, Google, and Microsoft joining. An independent body now stewards the spec, which provides some protection against unilateral Anthropic changes.

The Agent Skills format has no equivalent transition. The spec appears hosted at `agentskills.io` (primary spec URL experienced SSL/redirect issues during research and was not directly fetched), with the Anthropic-controlled `github.com/anthropics/skills` repository hosting example skills. The Agentic AI Foundation hosts MCP but not Agent Skills. No transfer of governance has been announced.

Simon Willison used scare quotes around "open standard" when characterizing Agent Skills, citing under-specification concerns. This skepticism is consistent with the governance gap.

## The Fragmentation Pattern in Progress

Claude Code has already diverged from the spec minimum by adding proprietary extensions (`context: fork`, `allowed-tools`, `model`, `hooks`, etc.). Other runtimes are likely to do the same as their needs diverge from the spec's minimum surface.

Cross-runtime portability under an Anthropic-controlled spec means portability is adoption-dependent — it holds as long as Anthropic maintains the spec in a runtime-neutral way, which is not structurally enforced. As each vendor adds extensions optimized for their runtime, the practical meaning of "Agent Skills compatible" will narrow.

The risk pattern mirrors what happened with early web standards before W3C matured: a nominal standard with rapidly diverging vendor implementations.

## Implications for WOS

WOS currently validates Claude Code-specific fields as correct practice (see: skill-frontmatter-extensions-claude-code-specific). If the standard fragments, WOS's guidance will track one dialect — Claude Code's — while producing skills that are increasingly incompatible with other runtimes' evolving interpretations.

The practical mitigation is to author to the spec minimum (`name` + `description` + markdown body) when portability matters, and treat everything else as Claude-locked by design. WOS does not currently make this distinction explicit.

## Confidence Note

The primary spec at `agentskills.io/specification` was not directly fetched during research due to SSL/redirect issues. Key claims about the spec minimum and governance status derive from T1 vendor sources and T4 practitioner reports. The governance gap conclusion is consistent across all sources that addressed it, but direct inspection of the specification document would upgrade confidence.

---

**Takeaway:** Evidence suggests the Agent Skills format has no independent governance — Anthropic controls spec evolution with no foundation oversight. MCP has cleaner governance (Linux Foundation/AAIF). This creates fragmentation risk: each vendor will add proprietary extensions, narrowing cross-runtime portability over time.
