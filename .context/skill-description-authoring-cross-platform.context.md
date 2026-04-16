---
name: "Skill Description Authoring: Cross-Platform Comparison"
description: "Anthropic, OpenAI, and LangChain treat tool description authoring differently; Anthropic has the most structured guidance, OpenAI diverges on examples, and LangChain has near-absent guidance"
type: concept
confidence: high
created: 2026-04-11
updated: 2026-04-11
sources:
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://developers.openai.com/api/docs/guides/function-calling
  - https://aclanthology.org/2025.naacl-long.44
related:
  - docs/context/skill-progressive-loading-and-routing.context.md
  - docs/context/skill-routing-failure-modes-and-pushy-heuristic.context.md
  - docs/research/2026-04-11-skill-description-routing.research.md
---

The three major agentic frameworks have substantially different approaches to description authoring. The differences are not cosmetic — they reflect different routing architectures and different assumptions about what the model needs to select correctly.

**Anthropic (Claude Code / Agent Skills).** The most structured guidance of the three. Key requirements: (1) descriptions must be written in third person — the description is injected into the system prompt, and inconsistent point-of-view causes discovery problems; (2) descriptions must answer both what the skill does and when to use it, using the "Use when..." clause pattern; (3) the effective routing window is 250 characters (truncation in the skill listing), so trigger signal must front-load; (4) descriptions cannot contain XML tags. Negative trigger: `disable-model-invocation: true` (full removal) or `user-invocable: false` (Claude-only, hidden from auto-matching). Skill names use gerund form (`analyzing-spreadsheets`). Vague descriptions are explicitly called out as anti-patterns: "Helps with documents," "Processes data."

**OpenAI (Function Calling).** Guidance is framed around an "intern test": could someone use this function knowing only the description? If not, add clarifications. Required content: purpose, parameters, formats, outputs, and when and when *not* to use the tool. No stated character limit in the retrieved documentation. Two-level description hierarchy: namespace descriptions (concise, for selection) + function descriptions (detailed, for usage). Role prompting in the system prompt frames tool scope before descriptions are evaluated. Key divergence from Anthropic: **OpenAI explicitly warns that adding examples may hurt performance for reasoning models** — no analogous caveat exists in Anthropic's guidance, which recommends examples as a pattern for output quality improvement. This difference has practical consequences for teams targeting reasoning models (o3, o4-mini) vs. standard chat models.

**LangChain.** No structured description authoring documentation comparable to Anthropic's or OpenAI's. The tool description is the Python function docstring. LangChain's official documentation states the docstring "should be informative and concise." There is no "Use when..." clause pattern, no third-person requirement, no character limit, no negative trigger mechanism. When tools misroute, the community response is to improve Pydantic schemas for cleaner schema generation — treating description quality as an engineering problem (schema structure) rather than a prompt-authoring problem (description text). This near-absence of guidance is itself a signal: LangChain's routing model is less description-driven than Anthropic's.

**The key divergence to remember for WOS.** The examples-in-descriptions question splits by model family: use examples freely in skill bodies and descriptions for standard models; be cautious adding examples to descriptions when targeting reasoning models. If WOS skill authors are writing cross-platform skills, this is the most practically consequential difference between Anthropic and OpenAI guidance (S1, S3, S5).

Empirical research on description quality (arXiv:2602.20426, NAACL 2025 EASYTOOL) confirms that description characteristics causally affect routing, but the underlying studies target API-style function calling, not system-prompt-injected descriptions. The extent to which cross-platform findings transfer within each platform's specific mechanism remains an open question.
