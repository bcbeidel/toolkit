---
name: "Agent Context File Quality Over Completeness"
description: "Human-optimized READMEs can actively decrease LLM performance; minimal curated context files beat verbose auto-generated ones"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2504.09798v2
  - https://arxiv.org/abs/2602.11988
  - https://arxiv.org/abs/2601.20404
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://daplab.cs.columbia.edu/general/2026/03/31/your-ai-agent-doesnt-care-about-your-readme.html
  - https://code.claude.com/docs/en/best-practices
related:
  - docs/context/agent-facing-document-structure.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/context-rot-and-window-degradation.context.md
---
Human-optimized README files can actively decrease LLM performance. Providing traditional README.md alone decreased performance for DeepSeek R1 — LLMs process human-optimized formats poorly (Giordano et al., ReadMe.LLM, 2025). Minimal, curated context files outperform verbose or auto-generated ones on both task success and cost.

## The Core Evidence

Two 2026 peer-reviewed studies reach opposing conclusions on AGENTS.md effectiveness, but their reconciliation is the most useful finding:

**Gallotta et al. (Jan 2026)**: AGENTS.md presence reduced median agent runtime by 28.64% and output token consumption by 16.58% across 10 repositories and 124 pull requests.

**Gloaguen et al. / ETH Zurich (Feb 2026)**: Across 138 repository instances and 5,694 pull requests with four coding agents, LLM-generated context files reduced task success rates in 5 of 8 evaluation settings, with 0.5-2 percentage point drops and 20%+ cost increases. Developer-written files showed only marginal positive effects.

The reconciliation: **minimal, human-curated files addressing project-specific quirks help; verbose or auto-generated files hurt**. Signal-to-noise ratio matters more than comprehensiveness. A 5-line context file addressing non-obvious project specifics outperforms a 2,000-word generated overview.

## ReadMe.LLM: ~5x Improvement with Structured Format

Giordano et al. tested an XML-tagged structure (Rules + Library Description + Code Snippets) versus providing traditional README.md alone. Results: approximately 5x correctness improvement over baseline for niche library API tasks. Zero-shot baseline averaged 30% success; with ReadMe.LLM, near-perfect accuracy across most models.

Critical finding: include function signatures and usage examples, but **exclude full implementation code** — excessive length causes hallucinations. The file format is:
- Rules: guidelines instructing the LLM on processing
- Library description: concise overview of purpose and core functionalities
- Code snippets: function signatures with usage examples (not implementations)

The scope is narrow: improvement was measured on niche libraries with 0-40% baselines. The pattern may not generalize to well-known frameworks where the model already has strong priors.

## What Agents Actually Need

Agents need file paths, commands, and constraints — not narratives. Analysis of 2,303 context files (multi-institution, 2025) found developers correctly prioritize:
- Build/run commands with specific flags (62.3%)
- Implementation details (69.9%)
- Architecture (67.7%)

What is almost always absent: security constraints (14.5%) and performance considerations (14.5%).

Effective patterns from analysis of 2,500+ repositories:
- Specificity over generality: "React 18 with TypeScript, Vite, and Tailwind CSS" beats "React project"
- Executable commands early (agents reference them frequently)
- One real code snippet beats three paragraphs describing conventions
- Three-tier boundaries: Always do / Ask first / Never do
- "Never commit secrets" was the most frequently helpful constraint

## The Auto-Generation Trap

LLM-generated context files mostly repeat discoverable information — what any competent agent could find by reading the codebase. They add inference cost without adding value for well-documented repositories. The ETH Zurich recommendation: omit LLM-generated context files entirely; limit human-written instructions to non-inferable details (specific tooling, custom build commands, project-specific constraints).

Adoption volume is not evidence of effectiveness. 20,000+ repositories adopted AGENTS.md; that adoption preceded the controlled studies showing context file quality is the critical variable, not context file presence.

## Anthropic's Minimal Sufficiency Principle

"Find the smallest set of high-signal tokens that maximize the likelihood of some desired outcome." Start with a minimal prompt. Iteratively add based on observed failure modes, not anticipated edge cases. Every line costs context tokens. Expand deliberately based on actual friction, not theoretical concerns.
