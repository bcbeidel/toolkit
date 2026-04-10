---
name: "Context File Content Selection and Coverage Threshold"
description: "Context files should document only what is non-inferable from code; LLM-generated files hurt performance; human-written yield only +4% at +19% inference cost"
type: context
sources:
  - https://arxiv.org/html/2510.21413v1
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://code.claude.com/docs/en/best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
related:
  - docs/context/agent-context-file-quality-over-completeness.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/agent-facing-document-structure.context.md
  - docs/context/context-rot-and-window-degradation.context.md
---

Context files have a documented marginal benefit and a real cost. The ETH Zurich study (Gloaguen et al., 2025) provides the strongest empirical evidence available: across 10,000 open-source repositories, human-written context files yielded only +4% task success improvement at up to +19% inference cost. LLM-generated context files reduced task success in 5 of 8 settings and increased inference costs 20-23%.

The practical conclusion is not that context files are useless — it is that most of what developers put in them provides no value, and the selection threshold must be high.

## The Selection Rule

Include only what an agent cannot infer by reading the codebase. Exclude everything else.

Anthropic is explicit: "Include Bash commands Claude can't guess. Exclude anything Claude can figure out by reading code, standard language conventions, and file-by-file codebase descriptions." Modern frontier models already know standard library conventions, common framework patterns, and idiomatic language practices. Documenting these adds token cost without adding signal.

Content that belongs in a context file:
- Custom commands and non-standard build steps not visible from configuration files
- Non-public domain knowledge (internal APIs, proprietary toolchains, business rules)
- Constraints that override default agent behavior (files to never edit, tools to always use)
- Workflow conventions that cannot be inferred from code structure

Content that does not belong:
- Language idioms and standard library usage
- Framework conventions the model already knows
- File-by-file summaries of a codebase the model can read directly
- Motivational or philosophical framing with no behavioral implication

## Start Under 150 Lines

Start minimal. Add based on observed failure modes. Do not front-load everything that seems potentially useful — over-inclusion causes the documented failure mode: bloated context files cause agents to ignore actual instructions as relevant rules get diluted in noise.

HumanLayer's guideline that "every single line deserves careful consideration" is not hyperbole. Each line consumes attention budget. The question for each line is not "is this true?" but "does including this change agent behavior in a measurable way?"

## The Inference Cost Is Real

Every context file token doubles as a per-request cost at inference time. Doubling context tokens roughly quadruples computation. The +4% task success gain from human-written files, at +19% inference cost, may not be positive ROI for most teams — especially if the gains are concentrated in domain-specific knowledge that only applies to a subset of tasks.

The study's scope limits generalizability: 138 Python tasks in small open-source repositories. For proprietary codebases with idiosyncratic toolchains and non-public domain knowledge, the gains from high-quality human-written context files are likely larger. The study found LLM-generated files improved performance by +2.7% when all other documentation was first removed — suggesting context files provide real value when they are the only source of project-specific knowledge.

## LLM-Generated Files Are Actively Harmful

The finding that LLM-generated context files reduce task success is counterintuitive but consistent across the ETH Zurich data. The most plausible explanation: LLM-generated context files tend to include inferred information that the model already knows, redundant summaries of code it can read directly, and hallucinated or imprecise details that contradict the actual codebase. This noise degrades retrieval accuracy for the high-signal content that genuinely matters.

Human-written files that capture genuinely non-inferable knowledge outperform LLM-generated files because human authors have ground truth access to the constraints, exceptions, and business rules that cannot be inferred from code. The quality bar is: would a new team member need to be explicitly told this? If yes, document it. If no, don't.
