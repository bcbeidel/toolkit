---
name: "Skill Authoring Rubric"
description: "Evidence-based rubric for writing effective LLM agent skills — structure, density, progressive disclosure, testing, and quality criteria derived from Anthropic T1 documentation, platform conventions, and instruction design research"
type: research
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
  - https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
  - https://code.visualstudio.com/docs/copilot/customization/agent-skills
  - https://openai.github.io/openai-agents-python/multi_agent/
  - https://www.anup.io/ship-prompts-like-software-regression-testing-for-llms/
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
  - https://www.promptingguide.ai/techniques/prompt_chaining
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/workflow-for-prompt-chaining.html
  - https://arxiv.org/html/2508.01523v1
  - https://arxiv.org/html/2507.11538v1
related:
  - PRINCIPLES.md
---

# Skill Authoring Rubric

**Bottom line:** Effective skills follow a three-level loading model, stay
under 500 lines in SKILL.md, use imperative voice with concrete examples,
keep references one level deep, and measure quality by outcome rather than
word count. The rubric below synthesizes T1 sources (Anthropic, VS Code
Copilot) with instruction design research into actionable criteria for
writing and evaluating skills.

## Sources

| # | URL | Title | Tier | Status |
|---|-----|-------|------|--------|
| 1 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Anthropic Skill Best Practices | T1 | verified |
| 2 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Anthropic Skills Overview | T1 | verified |
| 3 | https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills | Anthropic Engineering Blog | T1 | verified |
| 4 | https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/ | Lee Han Chung Deep Dive | T4 | verified |
| 5 | https://code.visualstudio.com/docs/copilot/customization/agent-skills | VS Code Copilot Skills | T1 | verified |
| 6 | https://openai.github.io/openai-agents-python/multi_agent/ | OpenAI Agents SDK Multi-Agent | T1 | verified |
| 7 | https://www.anup.io/ship-prompts-like-software-regression-testing-for-llms/ | Prompt Regression Testing | T4 | verified |
| 8 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags | Anthropic Prompt Engineering | T1 | verified |
| 9 | https://www.promptingguide.ai/techniques/prompt_chaining | Prompt Chaining Guide | T4 | verified |
| 10 | https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/workflow-for-prompt-chaining.html | AWS Prompt Chaining Patterns | T2 | verified |
| 11 | https://arxiv.org/html/2508.01523v1 | LLM Code Modification Prompting | T3 | verified |
| 12 | https://arxiv.org/html/2507.11538v1 | IFScale: Instruction Density Limits | T3 | verified |

## Search Protocol

6 searches across 2 sources, 36 results found, 9 used

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| skill authoring best practices Anthropic Claude | google | 2025-2026 | 5 | 4 |
| VS Code Copilot agent skills specification | google | 2025-2026 | 3 | 1 |
| OpenAI agents multi-agent orchestration patterns | google | 2025-2026 | 3 | 1 |
| LLM prompt regression testing evaluation | google | 2025-2026 | 4 | 2 |
| IFScale benchmark LLM instruction density limits | google | 2025 | 10 | 1 |
| LLM prompt instruction optimal length density token budget | google | 2025-2026 | 10 | 0 |

Not searched: Google Scholar (covered by direct arXiv fetching), PubMed (not biomedical)

## Findings

### 1. The Three-Level Loading Model Is the Universal Architecture

**Confidence: HIGH** — Converging T1 sources (Anthropic, VS Code Copilot)

Every major platform implements the same progressive disclosure model for
skill loading:

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| L1: Metadata | Always (startup) | ~100 tokens/skill | `name` + `description` from YAML frontmatter |
| L2: Instructions | When skill triggered | <5K tokens | SKILL.md body |
| L3: Resources | As needed | Unbounded | Reference files, scripts, assets |

Anthropic's documentation states: "Progressive disclosure ensures only
relevant content occupies the context window at any given time." The system
applies a 15,000-character token budget to the skill discovery section,
making concise L1 descriptions critical.

**Implication for WOS:** The L1/L2/L3 model maps directly to WOS's existing
structure (SKILL.md frontmatter → SKILL.md body → references/). No
structural changes needed — but the model should be documented explicitly.

### 2. SKILL.md Body Should Stay Under 500 Lines

**Confidence: HIGH** — T1 source (Anthropic best practices)

Anthropic's best practices documentation states: "Keep SKILL.md body under
500 lines for optimal performance. If your content exceeds this, split it
into separate files using the progressive disclosure patterns."

This aligns with the existing WOS skill density research finding of 200
instruction lines (non-structural lines after frontmatter). The 500-line
raw limit and 200 instruction-line limit are complementary: 500 raw lines
typically yields 200-250 instruction lines after excluding headers, blank
lines, code fences, and table separators.

**Implication for WOS:** The research skill at ~721 instruction lines
across 9 files significantly exceeds both thresholds, confirming #124's
premise.

### 3. Description Is the Most Critical Field

**Confidence: HIGH** — Converging T1 sources

The `description` field serves as the semantic filter for skill selection.
Anthropic warns: "Claude uses it to choose the right Skill from potentially
100+ available Skills." Key conventions:

- Write in third person (description is injected into system prompt)
- Include both what the skill does AND when to use it
- Be specific — include key terms that trigger discovery
- Maximum 1024 characters

**Bad:** "Helps with documents"
**Good:** "Extract text and tables from PDF files, fill forms, merge
documents. Use when working with PDF files or when the user mentions PDFs,
forms, or document extraction."

**Implication for WOS:** WOS skill descriptions should follow this pattern.
Current descriptions are functional but could be more explicit about
trigger conditions.

### 4. Conciseness Is a First-Class Design Principle

**Confidence: HIGH** — T1 source (Anthropic best practices)

Anthropic's documentation leads with: "The context window is a public good.
Your Skill shares the context window with everything else Claude needs to
know." The default assumption is that Claude is already smart — only add
context it doesn't already have.

The recommended self-test for every instruction: "Does Claude really need
this explanation? Can I assume Claude knows this? Does this paragraph
justify its token cost?"

This directly maps to WOS P6 ("omit needless words") but adds a concrete
evaluation method: challenge each piece of information against what the
model already knows.

### 5. Degrees of Freedom Should Match Task Fragility

**Confidence: HIGH** — T1 source (Anthropic best practices)

Not all instructions need the same specificity:

| Freedom Level | When to Use | Example |
|--------------|-------------|---------|
| High (text guidance) | Multiple valid approaches, context-dependent | Code review process |
| Medium (pseudocode) | Preferred pattern exists, some variation OK | Report generation with parameters |
| Low (exact scripts) | Fragile operations, consistency critical | Database migrations, exact commands |

The bridge/field analogy: narrow bridge with cliffs = low freedom (exact
instructions); open field = high freedom (general direction).

**Implication for WOS:** The research skill's 8-phase workflow is a "narrow
bridge" — phases must execute in order with gates. But within each phase,
many steps could use higher freedom. This is the key lever for #124:
identify which instructions are guardrails (keep) vs. explanations of what
Claude already knows (cut).

### 6. References Must Be One Level Deep

**Confidence: HIGH** — T1 source (Anthropic best practices)

Anthropic warns: "Claude may partially read files when they're referenced
from other referenced files." Nested references (SKILL.md → advanced.md →
details.md) cause Claude to use `head -100` previews instead of full reads.

All reference files should link directly from SKILL.md.

**Implication for WOS:** WOS skills already follow this convention — all
references are one level deep from SKILL.md. This is a strength to
preserve and document.

### 7. Examples Are Among the Most Reliable Steering Mechanisms

**Confidence: HIGH** — T1 source (Anthropic prompt engineering)

Anthropic states: "Examples are one of the most reliable ways to steer
Claude's output format, tone, and structure." Recommendations:

- 3-5 diverse examples in `<example>` tags
- Examples should mirror actual use cases
- Cover edge cases
- Show expected depth and specificity

This has a tension with conciseness (P6): examples consume tokens. The
resolution from the prompt engineering guide is that well-chosen examples
replace verbose explanations — one good example often replaces a paragraph
of description.

### 8. Evaluation-Driven Development Prevents Instruction Bloat

**Confidence: HIGH** — Converging T1 (Anthropic) and T4 sources

Anthropic recommends: "Create evaluations BEFORE writing extensive
documentation. This ensures your Skill solves real problems rather than
documenting imagined ones." The workflow:

1. Run Claude on tasks without a skill — document failures
2. Build 3 evaluation scenarios testing those gaps
3. Measure baseline without the skill
4. Write minimal instructions addressing the gaps
5. Iterate: run evals, compare to baseline, refine

The regression testing literature (Anup.io) adds: "Overall averages hide
regressions. A 2% overall dip can mask a 15% collapse in a single
category." Track scores per category, not just aggregates.

**Implication for WOS:** This is the missing piece for #124. Before cutting
research skill instructions, we need evaluation scenarios that define
"working correctly." Without them, we can't measure whether cuts degrade
output quality (per PRINCIPLES.md P6 vs P2 tension).

### 9. Feedback Loops and Validation Steps Improve Output Quality

**Confidence: HIGH** — Converging T1 sources

The pattern "run validator → fix errors → repeat" appears across all
platforms. AWS describes it as "summarize → critique → rewrite." Anthropic
recommends checklist-based progress tracking for complex workflows.

For skills with code, verifiable intermediate outputs (plan → validate →
execute) catch errors before they propagate.

**Implication for WOS:** The research skill's phase gates are a strong
implementation of this pattern. They should be preserved during #124
density reduction.

### 10. XML Tags Provide Unambiguous Structure

**Confidence: HIGH** — T1 source (Anthropic prompt engineering)

Anthropic recommends XML tags for structuring complex prompts: "XML tags
help Claude parse complex prompts unambiguously, especially when your
prompt mixes instructions, context, examples, and variable inputs."

Best practices: use consistent, descriptive tag names; nest tags when
content has natural hierarchy.

**Implication for WOS:** WOS skills already use XML tags effectively
(e.g., `<example>`, `<output_format>`). However, portability note: XML
tag effectiveness may vary across non-Anthropic models.

### 11. Iterative Refinement With Two Claude Instances Is the Recommended Development Method

**Confidence: MODERATE** — T1 source (Anthropic best practices)

Anthropic recommends a "Claude A / Claude B" workflow: one instance helps
design and refine the skill, another tests it in real tasks. Key insight:
"Claude models understand the Skill format and structure natively."

The cycle: observe Claude B's behavior → return to Claude A with specifics
→ refine → retest.

**Implication for WOS:** This maps to the existing pattern of using Claude
Code to develop skills, then testing them in fresh sessions. Worth
documenting as a recommended workflow.

### 12. Instruction Density Has Measurable Limits

**Confidence: HIGH** (research finding) / **LOW** (direct applicability)

IFScale (Jaroslawicz et al., 2025) established that instruction-following
degrades with density:

| Instructions | Accuracy |
|-------------|----------|
| 10 | 94-100% |
| 100 | 94-98% |
| 250 | 80-85% |
| 500 | 68% best |

However, IFScale constraints are keyword-inclusion directives (~8 words
each), not behavioral instructions. The direction transfers ("more =
worse"), but no specific threshold number does.

Primacy bias peaks at 150-200 instructions, then flattens into uniform
failure at 300+.

**Implication for WOS:** This reinforces the "fewer is better" direction
but doesn't tell us where exactly to cut. The existing 200 instruction-
line threshold from skill density research remains the best anchor.

## Challenge

### Assumptions Check

| Assumption | Evidence | Impact if Wrong |
|------------|----------|-----------------|
| Anthropic's guidance applies to Claude Code skills | T1 documentation explicitly covers Claude Code | Low — same ecosystem |
| 500-line / 200-instruction thresholds are aligned | 500 raw ≈ 200-250 instruction lines empirically | Low — both catch the same skills |
| Examples replace verbose explanation | T1 guidance says examples are "most reliable" | Medium — some domain knowledge may still need explicit statement |
| Evaluation-driven approach prevents regression | T1 + T4 sources converge on this | Medium — requires investment in evaluation scenarios |
| One-level-deep references are sufficient | T1 warns about partial reads of nested refs | Low — WOS already follows this |

### Premortem

- **Rubric is too prescriptive:** Authors follow letter not spirit,
  producing skills that pass metrics but miss the point. Mitigation:
  rubric emphasizes outcome measurement, not just line counts.
- **Evaluation scenarios are hard to write:** For judgment-heavy skills
  like research, defining "correct output" is subjective. Mitigation:
  evaluate structural compliance (phases present, sources verified) not
  content quality.
- **Cross-model variation ignored:** What works for Opus may need more
  detail for Haiku. Mitigation: WOS primarily targets Claude Code which
  uses a single model per session; document the model-sensitivity caveat.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Keep SKILL.md body under 500 lines for optimal performance" | quote | Source 1 | verified |
| 2 | "Progressive disclosure ensures only relevant content occupies the context window" | quote | Source 2 | verified |
| 3 | 15,000-character token budget for skill discovery section | statistic | Source 4 | verified |
| 4 | "Claude uses it to choose the right Skill from potentially 100+ available Skills" | quote | Source 1 | verified |
| 5 | "The context window is a public good" | quote | Source 1 | verified |
| 6 | "Claude may partially read files when they're referenced from other referenced files" | quote | Source 1 | verified |
| 7 | "Examples are one of the most reliable ways to steer output format, tone, and structure" | quote | Source 8 | verified |
| 8 | "Create evaluations BEFORE writing extensive documentation" | quote | Source 1 | verified |
| 9 | IFScale: 68% accuracy at 500 instructions for best model | statistic | Source 12 | verified |
| 10 | Primacy bias peaks at 150-200 instructions | statistic | Source 12 | verified |
| 11 | ~100 tokens per skill for L1 metadata | statistic | Source 2 | verified |
| 12 | L2 instructions target under 5K tokens | statistic | Source 2 | verified |

## Rubric: Skill Quality Criteria

The following rubric synthesizes the findings into actionable criteria.
Each criterion includes its evidence basis and how to evaluate it.

### Structure

| Criterion | Standard | How to Check |
|-----------|----------|-------------|
| Frontmatter has `name` and `description` | Required | Automated (existing validator) |
| `name` is lowercase, hyphens, ≤64 chars | Required | Automated |
| `description` includes what + when, ≤1024 chars | Required | Manual review |
| `description` uses third person | Required | Manual review |
| SKILL.md body ≤500 raw lines | Recommended | Automated (skill_audit.py) |
| Instruction lines ≤200 (configurable) | Recommended | Automated (skill_audit.py) |
| References one level deep from SKILL.md | Required | Manual review |
| Long reference files (>100 lines) have TOC | Recommended | Manual review |

### Content

| Criterion | Standard | How to Check |
|-----------|----------|-------------|
| Only includes context Claude doesn't already know | Required | Self-test: "Does Claude need this?" |
| Freedom level matches task fragility | Required | Review: guardrails for fragile ops, guidance for flexible ones |
| Imperative voice for instructions | Recommended | Manual review |
| Consistent terminology throughout | Required | Manual review |
| No time-sensitive information | Required | Manual review |
| XML tags for structured sections | Recommended | Manual review |

### Workflow

| Criterion | Standard | How to Check |
|-----------|----------|-------------|
| Complex tasks have sequential steps | Required | Manual review |
| Phase gates for multi-step workflows | Recommended | Manual review |
| Validation/feedback loops for quality-critical ops | Recommended | Manual review |
| Checklist pattern for progress tracking | Recommended | Manual review |

### Examples

| Criterion | Standard | How to Check |
|-----------|----------|-------------|
| Concrete examples present (not abstract) | Recommended | Manual review |
| Examples demonstrate expected depth/specificity | Recommended | Manual review |
| 3-5 diverse examples for output-sensitive skills | Recommended | Manual review |

### Testing

| Criterion | Standard | How to Check |
|-----------|----------|-------------|
| Evaluation scenarios defined before optimization | Recommended | Scenarios exist in docs/plans or tests/ |
| Category-level regression tracking | Recommended | Eval results tracked per dimension |
| Tested with real usage scenarios | Required | Manual verification |

## Key Takeaways

1. **The loading model is settled.** L1/L2/L3 progressive disclosure is
   the universal pattern. Document it, follow it, don't reinvent it.

2. **Description is the gateway.** A poor description means the skill
   never triggers. Invest disproportionate effort in the `description`
   field.

3. **Conciseness is measurable.** For every instruction, ask: "Does Claude
   need this?" If the answer is no, cut it. Measure by outcome, not by
   word count.

4. **Freedom should vary within a skill.** Phase gates need low freedom
   (exact sequences). Within phases, many steps can use high freedom
   (general guidance). This is the primary lever for density reduction.

5. **Evaluate before optimizing.** Define what "working correctly" means
   before cutting. Without evaluation scenarios, you can't distinguish
   signal from noise.

6. **Examples beat explanations.** One concrete example often replaces a
   paragraph of description. This is the most reliable way to reduce
   volume without reducing capability.
