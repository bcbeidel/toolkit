---
name: "Skill Success Criteria — Four Axes"
description: "Before writing or editing a skill, define success across four axes: outcome, process, style, and efficiency goals — this pre-commitment prevents vague rubrics and makes behavioral assertions constructable."
type: context
sources:
  - https://developers.openai.com/blog/eval-skills
  - https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
related:
  - docs/research/2026-04-11-llm-skill-behavioral-testing.research.md
  - docs/context/skill-behavioral-testing-layer-gap.context.md
  - docs/context/skill-golden-dataset-perishability.context.md
---
# Skill Success Criteria — Four Axes

Define success criteria for a skill before writing it. Without pre-committed success criteria, evaluation becomes post-hoc rationalization — "does this feel right?" rather than "did it achieve the stated goal?"

## The Four Axes (OpenAI Evals Framework)

OpenAI's skill evaluation framework defines four goal categories that must be specified before evaluation begins:

**Outcome goals** — Did the skill complete the intended task? Example for `/wos:research`: Did the agent produce a document with verified sources, frontmatter, and a sub-question structure? These are coarse pass/fail checks and the easiest to make deterministic.

**Process goals** — Did the skill follow the intended steps? Example: Did the agent run the SIFT search protocol? Did it verify URLs before including them as sources? Process goals can be evaluated by inspecting execution traces, not just final output.

**Style goals** — Does the output match required conventions? Example: Does the output use bottom-line-up-front structure? Are headings at the correct level? Is the tone direct rather than hedged? Style goals often require semantic evaluation but some can be converted to deterministic checks (heading level regex, word count bounds).

**Efficiency goals** — Is the skill avoiding unnecessary work? Example: Does the skill avoid duplicate searches? Is instruction density within acceptable token bounds? Efficiency goals protect against token waste and slow execution without catching quality regressions in other dimensions.

## Why Four Axes

A single rubric question ("is this good?") collapses all four axes into a single score, making it impossible to diagnose which dimension failed. A skill that produces correct outcomes via incorrect process (skipping verification) will score well on one axis and poorly on another — a distinction invisible to aggregate scoring.

Pre-commitment forces the author to make each goal explicit. A skill with no explicit process goals has no behavioral contract — only a vague quality expectation.

## Application to WOS

For WOS skills, the four axes map naturally:
- Outcome: frontmatter present, required sections exist, file saved to correct path
- Process: expected tools invoked in expected sequence (search before claim, verify before output)
- Style: direct tone, bottom-line-up-front, no hedge words, correct heading structure
- Efficiency: no redundant tool calls, instruction count within threshold

Specifying all four before authoring a skill creates the surface for behavioral assertions at Layer 2–3 without requiring LLM-as-judge.
