---
name: "Prompt Engineering for Reliable LLM Instruction"
description: "Landscape survey of system-level prompt design: constraint specification, output formatting, few-shot examples, CoT, and the specificity-flexibility paradox"
type: research
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://developers.openai.com/api/docs/guides/prompt-engineering/
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/
  - https://arxiv.org/html/2505.13360v1
  - https://arxiv.org/pdf/2509.14404
  - https://www.promptingguide.ai/techniques/cot
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://codeconductor.ai/blog/structured-prompting-techniques-xml-json/
related:
  - docs/context/prompt-engineering.md
---

## Summary

Landscape survey of techniques for writing reliable system-level LLM instructions
(skill prompts), drawing from 8 verified sources including official documentation
from Anthropic and OpenAI, peer-reviewed research, and expert practitioner guides.

**Key findings:**

- **Structure over phrasing.** Both major model providers converge on the same
  organizational pattern: role/identity, then constraints, then examples, then context.
  XML tags outperform JSON as delimiters across vendors (HIGH).
- **Selective specification resolves the specificity paradox.** Underspecified prompts
  regress 2x more on model updates, but specifying 19+ requirements simultaneously
  degrades accuracy by 15-20%. The solution: specify only critical, unstable requirements
  and leverage model defaults for the rest (HIGH).
- **Few-shot examples are the most reliable steering mechanism.** 3-5 diverse examples
  wrapped in structured tags dramatically improve consistency. Example diversity matters
  more than quantity (HIGH).
- **Positive constraints outperform negative ones.** "Write in flowing prose" works
  better than "Don't use markdown." Tell the model what to do, not what to avoid (HIGH).
- **Explain why, not just what.** Providing motivation behind constraints enables the
  model to generalize beyond the literal rule (MODERATE).
- **Anti-patterns cluster around implicit assumptions.** Models guess unspecified
  requirements correctly only 41.1% of the time. Conditional requirements are the most
  dangerous gap (HIGH).

8 searches across 1 source (Google), 80 results found, 16 used.

---

## Research Brief

Investigation of techniques for writing reliable system-level LLM instructions,
focused on skill authoring rather than conversational prompting. The question spans
constraint specification, output formatting, anti-pattern guards, few-shot examples,
chain-of-thought reasoning, and the tradeoff between specificity and flexibility.
Unrestricted by model vendor or framework. Preferred sources: official model provider
documentation, peer-reviewed research, expert practitioner writing. Time period
prioritizes 2023-2026.

### Sub-Questions

1. What constraint specification techniques reliably bound LLM behavior in system prompts?
2. What prompting strategies improve output quality? (few-shot, CoT, structured reasoning)
3. How should skill authors calibrate specificity vs. flexibility in instructions?
4. What are known anti-patterns and failure modes in system-level prompt design?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting Best Practices | Anthropic | 2025 | T1 | verified |
| 2 | https://developers.openai.com/api/docs/guides/prompt-engineering/ | Prompt Engineering Guide | OpenAI | 2024 | T1 | verified |
| 3 | https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/ | GPT-4.1 Prompting Guide | OpenAI | 2025 | T1 | verified |
| 4 | https://arxiv.org/html/2505.13360v1 | What Prompts Don't Say: Underspecification in LLM Prompts | Chen et al. | 2025 | T3 | verified |
| 5 | https://arxiv.org/pdf/2509.14404 | A Taxonomy of Prompt Defects in LLM Systems | Academic | 2025 | T3 | verified |
| 6 | https://www.promptingguide.ai/techniques/cot | Chain-of-Thought Prompting | DAIR.AI | 2024 | T4 | verified |
| 7 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective Context Engineering for AI Agents | Anthropic | 2025 | T1 | verified |
| 8 | https://codeconductor.ai/blog/structured-prompting-techniques-xml-json/ | Structured Prompting Techniques: XML & JSON | CodeConductor | 2024 | T5 | verified |

## Findings

### 1. Constraint Specification Techniques

The strongest pattern across all sources is **structural clarity over clever phrasing**.
Both Anthropic [1] and OpenAI [2][3] converge on organizing system prompts as layered
specifications: identity/role first, then instructions/constraints, then examples, then
context (HIGH — T1 sources converge).

**Positive constraints outperform negative ones.** Anthropic explicitly recommends telling
the model what to do rather than what not to do [1]. "Your response should be composed of
smoothly flowing prose paragraphs" works better than "Do not use markdown" (HIGH — T1).

**XML tags provide unambiguous boundaries.** Claude was trained with XML tags in its data,
making tags like `<instructions>`, `<example>`, and `<context>` effective delimiters [1].
OpenAI's GPT-4.1 testing found XML and ID-based formats "outperformed JSON significantly"
as delimiters for document collections [3] (HIGH — two T1 sources converge).

**Message role hierarchy creates authority layers.** OpenAI's architecture separates
developer messages (highest priority), user messages, and assistant messages — treating
prompts like "function definitions and arguments in programming" [2]. This layered
approach maps naturally to skill authoring where system instructions must override
user-level variance (MODERATE — T1, single vendor).

**Agentic prompt scaffolding.** OpenAI's GPT-4.1 guide found that three system prompt
components — persistence, tool-calling encouragement, and planning mandates — improved
SWE-bench scores by approximately 20% [3] (MODERATE — T1 but single benchmark).

### 2. Prompting Strategies for Output Quality

**Few-shot examples remain the most reliable steering mechanism.** Anthropic calls examples
"one of the most reliable ways to steer Claude's output format, tone, and structure" [1].
The recommended count is 3-5 examples, wrapped in `<example>` tags, designed to be
relevant, diverse, and structured (HIGH — T1 + T4 sources converge).

**Example diversity matters more than quantity.** Diversity across examples prevents the
model from picking up unintended patterns [1][6]. Auto-CoT research confirms that "diversity
in the questions and reasoning demonstrations used is critical" [6] (MODERATE — T1 + T4).

**Chain-of-thought improves reasoning, even in non-reasoning models.** OpenAI confirms
that "induced CoT improves performance" for GPT-4.1 [3]. Anthropic recommends preferring
"general instructions over prescriptive steps" — a prompt like "think thoroughly" often
produces better reasoning than a hand-written step-by-step plan [1] (HIGH — two T1 sources).

**Self-verification catches errors.** Appending verification instructions like "Before
you finish, verify your answer against [test criteria]" catches errors reliably for
coding and math tasks [1] (MODERATE — T1, single vendor).

**Structured output schemas enforce format compliance.** Both vendors support JSON schema
enforcement at the API level (OpenAI's Structured Outputs [2], Anthropic's structured
outputs). This moves format enforcement from prompt-level instruction to mechanical
constraint (HIGH — T1 sources converge).

### 3. Calibrating Specificity vs. Flexibility

This is the most nuanced dimension. Research reveals a clear paradox: underspecification
causes regression, but overspecification also degrades performance.

**Underspecification doubles regression risk.** Chen et al. found that underspecified
prompts are 2x more likely to regress during model or prompt changes, with accuracy drops
exceeding 20% [4]. Conditional requirements are the most dangerous gap — they appear in
only 14.3% of developer prompts but represent 40% of systematically curated requirements [4]
(HIGH — T3, quantitative).

**Overspecification degrades accuracy.** When developers specify 19 requirements
simultaneously, gpt-4o accuracy drops to 85% and Llama-3.3-70B to 79.7% — significant
declines from individual requirement performance [4]. The model's instruction-following
capacity is finite — competing constraints interfere with each other (HIGH — T3,
quantitative).

**The "right altitude" principle.** Anthropic's context engineering guidance describes
an optimal zone: "specific enough to guide behavior effectively yet flexible enough to
provide strong heuristics" [7]. This is the Goldilocks zone between hardcoded brittle
logic and vague high-level guidance (MODERATE — T1, qualitative).

**Selective specification resolves the paradox.** The most actionable finding: specify
only critical, unstable requirements while leveraging model defaults for redundant ones.
Chen et al.'s Bayesian optimization achieved 3.8% accuracy improvement while reducing
prompt tokens by 41-45% [4] (HIGH — T3, quantitative).

**Model evolution shifts the calibration point.** Newer models (Claude 4.6, GPT-4.1)
follow instructions more literally [1][3]. Prompts tuned for older models may overtrigger
on newer ones. Anthropic explicitly warns: "Where you might have said 'CRITICAL: You MUST
use this tool when...', you can use more normal prompting like 'Use this tool when...'" [1]
(MODERATE — T1, qualitative observation).

**Explain "why" to enable generalization.** Providing context or motivation behind
instructions helps models generalize beyond the literal rule [1]. For example, explaining
that output will be read by a text-to-speech engine produces better compliance than simply
prohibiting ellipses (MODERATE — T1, single vendor).

### 4. Anti-Patterns and Failure Modes

**Task overloading.** Packing multiple distinct tasks into a single prompt causes
hallucination, missed tasks, and quality degradation as attention is divided [5]. The
fix: decompose into smaller, focused prompts that can run in parallel (HIGH — T3 + T1
sources converge).

**Unconditional tool mandates.** Mandating tool calls without conditions creates
hallucinated inputs. The fix: "if you don't have enough information, ask the user" [3]
(MODERATE — T1, single vendor).

**ALL-CAPS escalation.** Over-reliance on ALL-CAPS emphasis for important instructions.
OpenAI recommends starting without emphasis, adding only when empirically necessary [3].
WOS skill audit measures ALL-CAPS directive density as a quality signal (MODERATE — T1 +
project evidence).

**Implicit assumption of understanding.** Assuming the model will infer requirements not
explicitly stated is the most common defect category [5]. LLMs succeed at guessing
unspecified requirements only 41.1% of the time [4] (HIGH — T3, quantitative).

**Overengineering bias.** Modern capable models (Claude Opus 4.5/4.6) tend to
overengineer — creating extra files, adding unnecessary abstractions, building flexibility
that was not requested [1]. System prompts must explicitly constrain scope (MODERATE — T1).

**Stale prompt calibration.** Prompts tuned for one model version may cause unexpected
behavior on updates. Hidden model updates caused a 48% reduction in producing "skimmable
outputs" in one study [4] (HIGH — T3, quantitative).

**Security boundary violations.** Leaking system instructions into user-visible space
blurs roles and increases jailbreak risk [5]. System and user prompt boundaries must be
cleanly separated (MODERATE — T3).

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Techniques from one model vendor generalize to others | Both Anthropic [1] and OpenAI [2][3] converge on similar principles (clarity, examples, structured formatting) | GPT-4.1 follows instructions more literally than predecessors [3]; Claude models respond differently to ALL-CAPS emphasis [1] — model-specific tuning matters | Skill authors would need vendor-specific prompt variants rather than universal patterns |
| More explicit specification improves reliability | Underspecified prompts regress 2x more on model updates [4]; explicit constraints prevent ambiguity [5] | Specifying 19+ requirements simultaneously degrades accuracy [4]; over-constraining distorts reasoning | The "specify everything" heuristic backfires; skill authors need selective specification |
| Few-shot examples are the most reliable steering mechanism | Anthropic: "one of the most reliable ways to steer output" [1]; OpenAI: concrete examples guide behavior [2] | Examples increase token cost and may reduce generality if excessive [5]; automated CoT beats manual CoT [6] | If examples are less reliable than claimed, skill authors over-invest in example curation at the expense of structural clarity |
| XML/structured tags improve prompt parsing | Claude trained with XML tags [1]; OpenAI found XML outperformed JSON for delimiters [3] | No strong counter-evidence found, though JSON schemas have native enforcement via structured outputs [2] | Low impact — structured formatting is well-supported across vendors |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| Techniques age rapidly — best practices from 2024-2025 may not apply to 2026+ models that follow instructions more literally | High | Qualifies all findings with temporal caveat; skill authors must re-evaluate prompts on model upgrades |
| Vendor documentation is prescriptive, not empirical — official guides may reflect intended behavior, not measured behavior | Medium | Weakens T1 source reliance; academic studies [4][5] provide stronger empirical grounding |
| Landscape breadth sacrifices depth — the survey may present techniques without sufficient nuance about when each applies | Medium | Risk of oversimplified recommendations; mitigated by the specificity-flexibility finding from [4] |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "one of the most reliable ways to steer Claude's output format, tone, and structure" (re: examples) | quote | [1] | verified |
| 2 | XML and ID-based formats "outperformed JSON significantly" as delimiters | quote | [3] | verified |
| 3 | Three agentic prompt components improved SWE-bench scores by ~20% | statistic | [3] | verified |
| 4 | Include 3-5 examples for best results | statistic | [1] | verified |
| 5 | Underspecified prompts are 2x more likely to regress on model changes | statistic | [4] | verified |
| 6 | Specifying 19 requirements drops gpt-4o to 85%, Llama to 79.7% | statistic | [4] | corrected (was "19% decline") |
| 7 | Bayesian optimization achieved 3.8% accuracy improvement while reducing tokens by 41-45% | statistic | [4] | corrected (was "4.8% / 43%") |
| 8 | LLMs succeed at guessing unspecified requirements only 41.1% of the time | statistic | [4] | verified |
| 9 | Conditional requirements appear in only 14.3% of developer prompts vs 40% of curated requirements | statistic | [4] | verified |
| 10 | Hidden model updates caused 48% reduction in producing "skimmable outputs" | statistic | [4] | verified |
| 11 | LLMs excel at format-related specifications (70.7% success) but struggle with conditional requirements (22.9% success) | statistic | [4] | verified |
| 12 | GPT-4.1 achieved 55% pass rate on SWE-bench Verified | statistic | [3] | verified |

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| system prompt engineering techniques constraint specification LLM reliable output 2024 2025 | google | 2024-2025 | 10 | 2 |
| few-shot examples chain-of-thought system prompt design best practices 2024 | google | 2024-2025 | 10 | 2 |
| prompt engineering anti-patterns failure modes system instructions LLM | google | 2024-2025 | 10 | 4 |
| Anthropic prompt engineering guide system prompt design Claude 2025 | google | 2025 | 10 | 2 |
| OpenAI prompt engineering best practices system message GPT 2024 2025 | google | 2024-2025 | 10 | 2 |
| specificity vs flexibility system prompts LLM over-constraining under-constraining | google | 2024-2025 | 10 | 2 |
| prompt engineering structured output XML JSON schema constraints LLM guardrails 2024 2025 | google | 2024-2025 | 10 | 1 |
| context engineering vs prompt engineering system instructions agent design 2025 2026 | google | 2025-2026 | 10 | 1 |

8 searches across 1 source (Google), 80 found, 16 used.

Not searched: arxiv direct search (used Google to find papers), GitHub issues/discussions,
HuggingFace community posts.

## Limitations

- **Single search engine.** All searches routed through Google. Alternative indices
  (Semantic Scholar, ACL Anthology) may surface additional peer-reviewed work.
- **Vendor-centric.** Four of eight sources are from Anthropic or OpenAI. Findings may
  not fully generalize to open-weight models (Llama, Mistral) or non-Western language tasks.
- **Temporal fragility.** The field evolves rapidly. Techniques validated for 2024-2025
  model versions may need recalibration as models improve instruction-following capability.
- **No controlled experiments.** This survey synthesizes vendor documentation and one
  academic study. No independent A/B tests were conducted on the techniques described.

## Takeaways

For skill authors designing system-level LLM instructions:

1. **Organize prompts as layered specifications** — role, then constraints, then examples,
   then context. Use XML tags to delimit sections unambiguously.
2. **Specify selectively.** Identify which requirements are critical and unstable (likely
   to regress across model versions) and specify those explicitly. Let model defaults
   handle stable, predictable behaviors. Pay special attention to conditional requirements
   — they are the most commonly omitted and hardest for models to infer.
3. **Use 3-5 diverse examples** that cover edge cases and demonstrate the full expected
   workflow. Wrap in `<example>` tags. Diversity across examples matters more than count.
4. **State constraints positively.** "Write in flowing prose" outperforms "Don't use
   markdown." Tell the model what to produce, not what to avoid.
5. **Explain the why.** Providing motivation behind constraints enables generalization.
   A model that understands *why* ellipses are prohibited (text-to-speech) will also
   avoid other TTS-unfriendly constructs.
6. **Prefer general reasoning directives over prescriptive step lists.** "Think thoroughly"
   often beats a hand-written step-by-step plan. Reserve explicit CoT scaffolding for
   tasks where models consistently fail.
7. **Guard against known anti-patterns:** task overloading, unconditional tool mandates,
   ALL-CAPS escalation, implicit assumptions, and stale calibration.
8. **Re-evaluate prompts on every model upgrade.** Newer models follow instructions more
   literally — aggressive language that compensated for older model weaknesses will
   overtrigger on current models.
