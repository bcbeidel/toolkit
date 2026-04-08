---
name: LLM Rule Evaluation Reliability
description: How to get reliable compliance verdicts from LLM-based rule evaluation — binary verdicts, chain-of-thought, locked rubrics, independent evaluation
type: context
sources:
  - https://arxiv.org/html/2601.08654
  - https://arxiv.org/abs/2603.01896
  - https://arxiv.org/html/2601.03444v1
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://eugeneyan.com/writing/llm-evaluators/
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method
related:
  - docs/research/2026-04-07-effective-rules-for-llm-enforcement.research.md
  - docs/context/effective-rule-anatomy.context.md
  - docs/context/rule-system-pitfalls.context.md
  - docs/context/llm-as-judge-evaluation.md
---

LLM-based rule evaluation is reliable when four conditions are met.
Violating any one produces inconsistent verdicts that undermine the
enforcement system.

## Binary Pass/Fail Outperforms Graded Scales

Binary evaluation is more reliable than numeric scales for objective
compliance tasks. The 0-5 scale produces the strongest human-LLM
agreement among graded options (ICC: 0.853), but binary outperforms
all scales when compliance is objectively determinable. For code rules —
where a file either complies or it doesn't — pass/fail is the right
evaluation mode.

## Chain-of-Thought Before Verdict

Structured reasoning before judgment improves accuracy by 10-15
percentage points. Requiring explicit premises and formal conclusions
boosted code review accuracy from 78% to 88% on curated examples and
93% on real-world patches. Few-shot prompting increased evaluation
consistency from 65% to 77.5%. The evaluation prompt must require
reasoning before the verdict, not just "does this comply?"

## The Rule File IS the Locked Rubric

Compiling evaluation criteria into immutable specifications prevents
interpretation drift across evaluations. This "locked rubric" approach
achieved QWK of 0.7276 versus 0.5566 baseline — a 30% improvement.
The practical implementation: include the full rule file verbatim in
the evaluation prompt. Never summarize, paraphrase, or abbreviate.
Summaries allow the LLM to reinterpret criteria differently each time.

## One Rule, One File, One Verdict

Evaluating individual dimensions separately with separate judges
produces more reliable results than assessing everything simultaneously.
Transformations between evaluation modes are unreliable — pointwise
scores cannot reliably convert to pairwise judgments. Each rule-file
pair should be an independent evaluation: a single binary judgment on
a single compliance dimension.

Evidence suggests that even with best practices, LLM judges achieve
Cohen's kappa of approximately 0.84, below human-human agreement of
0.97. The gap is largest for ambiguous criteria. When compliance is
ambiguous, default to pass — false positives erode trust faster than
false negatives.

## Positioning: Complement, Not Replace

LLM-based enforcement provides semantic understanding that traditional
linters cannot. But CLAUDE.md instructions are advisory, not guaranteed.
LLM evaluation excels at architectural rules, layer boundaries, and
convention-based judgments that require understanding intent. Traditional
linters excel at syntax, formatting, and pattern matching. Use both.
