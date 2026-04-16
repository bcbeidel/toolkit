---
name: "Prompting Techniques Across Model Capability Tiers"
description: "Instruction authoring patterns — formatting, length, few-shot, persona, CoT — perform measurably differently across frontier vs. smaller LLMs; XML structure and few-shot examples are the safest cross-tier techniques, CoT and persona framing are tier-sensitive"
type: research
sources:
  - https://arxiv.org/abs/2411.10541
  - https://arxiv.org/abs/2310.11324
  - https://arxiv.org/abs/2201.11903
  - https://arxiv.org/abs/2206.07682
  - https://arxiv.org/abs/2311.10054
  - https://aclanthology.org/2024.findings-emnlp.888/
  - https://arxiv.org/abs/2603.18507
  - https://arxiv.org/abs/2005.14165
  - https://arxiv.org/abs/2410.02185
  - https://arxiv.org/abs/2502.14255
  - https://arxiv.org/abs/2307.03172
  - https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://www.trychroma.com/research/context-rot
  - https://www.nature.com/articles/s41586-024-07930-y
  - https://arxiv.org/abs/2404.11018
  - https://arxiv.org/abs/2508.19764
  - https://arxiv.org/abs/2109.01652
  - https://arxiv.org/abs/2210.11416
  - https://arxiv.org/html/2404.14812v2
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
related: []
---

# Prompting Techniques Across Model Capability Tiers

## Research Question

How do instruction authoring patterns — formatting structure, length, directive density, few-shot examples, and persona framing — perform differently across frontier vs. smaller language models, and what tier-aware guidelines should govern WOS skill authoring to ensure skills execute correctly regardless of the model a user runs?

## Sub-Questions

1. Do structured formatting techniques (XML tags, markdown headers, numbered steps) show measurably different instruction-following effectiveness across capability tiers — frontier vs. mid-tier vs. small models?
2. Does instruction length sensitivity increase at lower capability tiers? Is a 200–300 line threshold appropriate for smaller models, or does the effective ceiling drop?
3. Are few-shot examples more load-bearing on smaller models — do they rely more heavily on concrete in-context examples for correct output format, relative to frontier models that respond to zero-shot instruction?
4. Is the finding that persona framing reduces task performance specific to frontier models, or does it hold (or reverse) across lower-capability tiers?
5. Which instruction techniques show the greatest degradation moving from frontier to smaller models, and are there techniques that perform better or equivalently on smaller models (e.g., explicit step-by-step decomposition, simplified vocabulary)?
6. Do major frameworks (Anthropic, OpenAI, LangChain, LlamaIndex) publish tier-specific prompt authoring guidance or capability-gating patterns?
7. Is there evidence for or against annotating skill definitions with a minimum model tier as a portability/capability signal?

---

## Findings

### SQ1: Structured Formatting Effectiveness Across Capability Tiers

Formatting sensitivity is real at every capability tier. Frontier models show lower *average* sensitivity — GPT-4 maintains format-change dispersion below 3.6% across most benchmarks while GPT-3.5 shows up to 40% variance [1] — but this is an average-case observation, not a reliable property. The same study that establishes GPT-4's robustness documents GPT-4-32k-0613 scoring 76.22% pass@1 on HumanEval with plain text but only 21.95% with JSON formatting — a ~54-percentage-point drop larger than the comparable GPT-3.5 result on the same task. The mechanism: GPT-4 switched to chain-of-thought reasoning when confronted with JSON-structured code prompts, then failed to emit code. Frontier models have strong format *preferences*, not format immunity. (HIGH — T1 source internal contradiction confirms both claims simultaneously.)

Format choice does not transfer reliably across models. Performance on a given format is weakly correlated between models [2], so a template optimized for one tier may fail for another. For cross-tier skill authoring, XML tags are the safest structural choice: they provide unambiguous semantic delimiters without relying on markdown rendering assumptions and are explicitly recommended by Anthropic across all Claude tiers [14]. (MODERATE — T1 finding corroborated by T2 guidance but not tested in a dedicated cross-tier XML study.)

**WOS implication:** Skills intending to execute across tiers should default to XML structure for distinct sections. Markdown headers and plain text are acceptable within sections. JSON-formatted instructions are the highest-risk choice for code-generation contexts, regardless of model tier.

---

### SQ2: Instruction Length Sensitivity and the 200–300 Line Threshold

All models degrade as context length increases, even when far from their context window limit [15]. The degradation patterns differ by model family — Claude models show increasing abstention under ambiguity, GPT models show increasing hallucination — but the directional finding is universal. The "lost in the middle" penalty applies across capability tiers: information in the middle of long prompts suffers ~22 percentage point accuracy drops relative to information at the beginning or end (e.g., 75.8% → 53.8% for GPT-3.5-Turbo at the worst middle position) [11]. (HIGH — 18-model study [15], confirmed by dedicated study [11], consistent across families.)

The 200–300 line practitioner threshold has no T1 or T2 grounding. It is informal practitioner consensus (T4). The only official T2 threshold is Anthropic's 500-line SKILL.md limit, applied uniformly across tiers [13]. No academic study establishes tier-differentiated instruction line count thresholds — the literature addresses context length in tokens, not instruction lines as a discrete unit. (HIGH — null result confirmed by thorough search across practitioner, official, and academic sources.)

The directional claim that smaller models degrade faster than larger ones is supported by the Context Rot study's cross-tier results [15] and practitioner observation, but the specific counts ("Haiku can follow 100 instructions, Sonnet 150") are not grounded in T1/T2 evidence. (LOW for specific thresholds.)

**WOS implication:** The 200–300 line heuristic in check-skill is reasonable as a conservative target but should be presented as practitioner guidance, not a research-grounded threshold. Key insight placement (beginning and end) applies at all tiers. Anthropic's 500-line SKILL.md limit is the only T2-grounded hard bound.

---

### SQ3: Few-Shot Examples Across Capability Tiers

For base pretrained models, few-shot examples scale with model capacity — larger models extract more from in-context demonstrations, and the gap between zero-shot and few-shot performance grows with model size (Brown et al. 2020 [8]). This relationship breaks down for instruction-tuned models. Instruction tuning partially substitutes for few-shot examples by baking demonstration-like behavior into weights: the 137B FLAN model surpasses zero-shot 175B GPT-3 on 20 of 25 benchmarks (arXiv 2109.01652), and instruction-tuned models at 3B–7B range show meaningfully higher zero-shot baselines than same-sized base models (arXiv 2210.11416). For instruction-tuned models (the baseline for all practical deployments), the scaling advantage of larger models over few-shot examples is compressed. (MODERATE — instruction-tuning effect is from T1 sources but the inversion of Brown et al. is context-specific.)

The strongest cross-tier finding for WOS skill authoring: a single few-shot example significantly reduces prompt sensitivity across all model sizes [9]. This effect holds for 7B, 8B, and instruction-tuned variants. Few-shot examples are the most robust available technique for stabilizing output format, and their value for output format stabilization is actually *higher* for smaller models, which lack the zero-shot baseline that instruction-tuned frontier models enjoy. (HIGH — POSIX finding, multiple model families tested.)

**WOS implication:** Skills with specific output format requirements should include at least one `<example>` block, regardless of target tier. The example requirement is more critical, not less, for skills intended to run on Haiku or sub-frontier open-source models. Skills targeting frontier-only contexts may omit examples where the format is simple, but cross-tier skills should treat examples as load-bearing.

---

### SQ4: Persona Framing Across Capability Tiers

Persona framing in system prompts consistently harms performance on factual/knowledge-retrieval tasks across model sizes from 7B to 72B [5, 6]. MMLU accuracy drops from 71.6% (baseline) to 68.0% (minimum persona) to 66.3% (long persona) in the PRISM paper [7]. The mechanism is identified: the model prioritizes acting like the persona over retrieving factual knowledge from pretraining. No persona leads to statistically better factual performance; more personas have negative effects as model scale increases (Llama3-70B showed more negative effects than smaller models) [5]. (HIGH — 9 open-source models across 4 families tested; effect direction is consistent.)

The harm is task-type dependent. Expert personas show MT-Bench gains in 5/8 categories including Extraction and STEM [7]. For open-ended generation, advice, and reasoning tasks, carefully designed expert personas can help — but this benefit concentrates in larger, more capable models [from Challenge, Principled Personas paper]. The OpenSSF finding is real but security-specific: persona prompting produced the highest average security weakness count among all evaluated techniques [12] — this is a security-context generalization, not a claim about general task performance.

The Anthropic recommendation to "give Claude a role" [14] is not in conflict if understood as weak behavioral framing ("you are a helpful coding assistant") rather than strong expertise claims ("you are a world-class Python expert"). The factual accuracy damage concentrates in the expert knowledge retrieval pattern. (MODERATE — task-type distinction is inferred from evidence, not directly compared in a single study.)

**WOS implication:** WOS skills should avoid strong persona or expertise framing in skill definitions. Behavioral role framing for tone/style is lower risk than expertise claims. Skills requiring factual precision (research, audit, validation) should use no persona framing at all.

---

### SQ5: Degradation Patterns from Frontier to Smaller Models

**Chain-of-thought reasoning** is the most sharply tier-gated instruction technique, but the threshold has shifted. The 2022 Wei et al. finding of ~100B parameters [3, 4] applies to base pretrained models. Modern instruction-tuned models at 7B–13B (Llama-2-7B, Mistral-7B, Llama-2-13B) now show measurable CoT benefits via prompt engineering and CoT-tuned instruction datasets [from Challenge]. The effective threshold for instruction-tuned models appears closer to 7–10B parameters. Below this range, CoT prompting is still likely harmful for base models. (MODERATE — multiple T1 sources post-2022, but no single paper formally revises the threshold with a controlled study.)

**Formatting sensitivity** does not reliably decrease with scale — it changes character. Frontier models have sharper format preferences in some task-format combinations, while smaller models show broader average sensitivity. There is no technique that is universally safer at smaller model sizes from a formatting perspective. (MODERATE — supported by T1 [1, 2] but finding comes from limited model family comparison.)

**Directive density** (ALL-CAPS, MUST, CRITICAL): Anthropic's own guidance explicitly deprecates aggressive directive language for Opus 4.5+ [14], implying it was needed for earlier/weaker models. This is the clearest evidence that directive density calibrates inversely with model capability — more directives for less capable models. The WOS check-skill criterion correctly identifies this direction. (MODERATE — T2 source, heuristic grounding.)

**Instruction simplicity**: Explicit step-by-step decomposition (numbered steps, atomic actions) is safer across tiers than abstract goal statements. This is supported indirectly by the CoT effectiveness research and Anthropic's Haiku guidance ("provide enough guidance"), but no cross-tier comparison study directly tests this claim. (LOW — directional inference, not directly measured.)

---

### SQ6: Framework Tier-Specific Authoring Guidance

Anthropic is the only major framework or model provider that publishes tier-aware skill authoring guidance [13]. The guidance differentiates Haiku ("does the skill provide enough guidance?"), Sonnet ("is it clear and efficient?"), and Opus ("does it avoid over-explaining?"). This is directional, heuristic guidance — not empirically measured thresholds — as confirmed by the challenge stage. (HIGH — absence of competing framework guidance confirmed by thorough search; Anthropic guidance characterization confirmed by full text review.)

OpenAI publishes no equivalent tier-specific prompting guide for GPT-4o vs. GPT-4o-mini differences. LangChain and LlamaIndex both support model routing architecturally (directing tasks to different models by complexity) but publish no prompt authoring guidance that differs by model tier. (HIGH — null result, multiple searches across official documentation.)

**WOS implication:** WOS skills operating in the Claude ecosystem can rely on Anthropic's Haiku/Sonnet/Opus heuristic as the practical reference. For cross-runtime portability (also running on GPT-4o-mini, open-source models), no official guidance exists; WOS must derive its own guidance from the research evidence.

---

### SQ7: Minimum Model Tier Annotation

No academic paper, official framework documentation, or T1/T2 source describes a minimum model tier annotation for prompts, skills, or tool definitions as a standardized practice. The concept does not exist as a formal specification. Production systems use tiered model routing (Haiku for classification, Sonnet for reasoning, Opus for complex tasks), but this is runtime infrastructure, not a skill-level capability signal. (HIGH — null result confirmed by extensive search.)

Evidence against the reliability of such an annotation: format performance weakly correlates between models [2], meaning a skill's success on Sonnet does not reliably predict success on Haiku even controlling for tier. A minimum-tier annotation would be imprecise — specific task-format-instruction combinations create idiosyncratic behavior that tier alone does not capture.

The most practical form of tier signaling found in production is Anthropic's informal test checklist: "tested with Haiku, Sonnet, Opus" — a verification record rather than a forward-looking capability claim. (MODERATE — this pattern is documented in T2 source but not established as a standard.)

**WOS implication:** A `min_model_tier` frontmatter field would lack both a standard to anchor to and sufficient predictive reliability to be useful. A more honest signal would be a `tested_with` list (which models the skill author verified execution against), paired with authoring-guide notes on which techniques are tier-sensitive.

---

## Sources Table

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2411.10541 | Does Prompt Formatting Have Any Impact on LLM Performance? | (arXiv preprint) | Nov 2024 | T1 | verified |
| 2 | https://arxiv.org/abs/2310.11324 | Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design | (arXiv / ICLR-adjacent) | Oct 2023 | T1 | verified |
| 3 | https://arxiv.org/abs/2201.11903 | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | Wei et al. (Google Brain), NeurIPS 2022 | Jan 2022 | T1 | verified |
| 4 | https://arxiv.org/abs/2206.07682 | Emergent Abilities of Large Language Models | Wei et al. (Google Brain), TMLR 2022 | Jun 2022 | T1 | verified |
| 5 | https://arxiv.org/abs/2311.10054 | When "A Helpful Assistant" Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models | (arXiv), EMNLP 2024 Findings | Nov 2023 | T1 | verified |
| 6 | https://aclanthology.org/2024.findings-emnlp.888/ | Personas in System Prompts Do Not Improve Performances of Large Language Models (EMNLP proceedings entry) | (ACL Anthology) | Nov 2024 | T1 | verified |
| 7 | https://arxiv.org/abs/2603.18507 | Expert Personas Improve LLM Alignment but Damage Accuracy: Bootstrapping Intent-Based Persona Routing with PRISM | USC researchers | Mar 2026 | T1 | verified |
| 8 | https://arxiv.org/abs/2005.14165 | Language Models are Few-Shot Learners (GPT-3) | Brown et al. (OpenAI), NeurIPS 2020 | May 2020 | T1 | verified |
| 9 | https://arxiv.org/abs/2410.02185 | POSIX: A Prompt Sensitivity Index For Large Language Models | Chatterjee et al., EMNLP 2024 Findings | Oct 2024 | T1 | verified |
| 10 | https://arxiv.org/abs/2502.14255 | Effects of Prompt Length on Domain-specific Tasks for Large Language Models | (arXiv) | Feb 2025 | T1 | verified |
| 11 | https://arxiv.org/abs/2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al., ACL 2024 | Jul 2023 | T1 | verified |
| 12 | https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions | Security-Focused Guide for AI Code Assistant Instructions | OpenSSF Best Practices & AI/ML Working Groups | Aug 2025 | T2 | verified |
| 13 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill Authoring Best Practices | Anthropic | 2025–2026 | T2 | verified |
| 14 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting Best Practices | Anthropic | 2025–2026 | T2 | verified |
| 15 | https://www.trychroma.com/research/context-rot | Context Rot: How Increasing Input Tokens Impacts LLM Performance | Chroma Research | 2025 | T3 | verified |
| 16 | https://www.nature.com/articles/s41586-024-07930-y | Larger and more instructable language models become less reliable | (Nature) | 2024 | T1 | verified (abstract only — paywalled) |
| 17 | https://arxiv.org/abs/2404.11018 | Many-Shot In-Context Learning | (arXiv, Google DeepMind) | Apr 2024 | T1 | verified |
| 18 | https://arxiv.org/abs/2508.19764 | Principled Personas: Defining and Measuring the Intended Effects of Persona Prompting on Task Performance | (arXiv) | Aug 2025 | T1 | verified (abstract + partial) |
| 19 | https://arxiv.org/abs/2109.01652 | Finetuned Language Models Are Zero-Shot Learners (FLAN) | Wei et al. (Google), ICLR 2022 | Sep 2021 | T1 | verified |
| 20 | https://arxiv.org/abs/2210.11416 | Scaling Instruction-Finetuned Language Models (Flan-T5) | Chung et al. (Google), NeurIPS 2022 | Oct 2022 | T1 | verified |
| 21 | https://arxiv.org/html/2404.14812v2 | Enhancing Chain of Thought Prompting via Reasoning Patterns | (arXiv) | Apr 2024 | T1 | verified |
| 22 | https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide | GPT-4.1 Prompting Guide | OpenAI | 2025 | T2 | verified |

---

## Search Protocol

| Query | Tool | Result Summary |
|-------|------|---------------|
| `instruction following smaller models formatting XML markdown benchmark evaluation 2023 2024` | WebSearch | Found MDEval, FMBench, InFoBench, StructEval, LIFBENCH benchmarks. Key: formatting evaluation frameworks across models. |
| `structured prompts model size instruction tuning capability comparison LLM` | WebSearch | Found arXiv 2411.10541 (prompt formatting impact). Key finding: GPT-4 more robust than GPT-3.5 to formatting changes; up to 40% variance in GPT-3.5. |
| `few-shot zero-shot model scale comparison smaller models instruction following performance` | WebSearch | Found Flan/instruction-tuned model studies; small models can match large on zero-shot classification after instruction tuning. |
| `prompt length sensitivity model capability small large model performance comparison 2024` | WebSearch | Found POSIX (arXiv 2410.02185), Chroma context rot, prompt sensitivity analysis. Key: all models degrade with length; smaller models more sensitive. |
| `chain-of-thought prompting model size emergent ability Wei 2022 threshold smaller models` | WebSearch | Confirmed ~100B parameter threshold from Wei et al. 2022. CoT is harmful or neutral for smaller models. |
| `persona role prompting performance model capability size comparison benchmark LLM` | WebSearch | Found PersonaGym, PRISM (arXiv 2603.18507), EMNLP 2024 study. Personas hurt factual tasks; effect holds across model sizes. |
| `OpenSSF persona framing reduces task performance frontier models prompt engineering security` | WebSearch | Found OpenSSF Security Guide at best.openssf.org. Document explicitly warns against persona/memetic proxy approach. |
| `prompt engineering degradation small models large models step-by-step decomposition performance gap 2024` | WebSearch | Found survey arXiv 2402.07927 on decomposition techniques. Limited tier-specific data on step-by-step. |
| `Anthropic documentation prompt engineering model tier Claude Haiku Sonnet Opus differences guidelines 2024 2025` | WebSearch | Found Anthropic model docs; skill authoring best practices differentiates Haiku/Sonnet/Opus guidance. |
| `model capability routing minimum capability requirement agent tool skill tier annotation production` | WebSearch | Found tiered routing patterns in production; Anthropic skill docs mention testing across Haiku/Sonnet/Opus. |
| `"instruction length" "small language model" performance degradation long prompts 2024 arxiv` | WebSearch | Found arXiv 2502.14255 (effects of prompt length), Lost in the Middle (arXiv 2307.03172), LongLLMLingua. |
| `OpenAI GPT-4o-mini vs GPT-4 prompting differences guidelines capability tier documentation` | WebSearch | No published OpenAI tier-specific prompting guide found; mainly performance/cost comparison articles. |
| `LangChain LlamaIndex model routing capability tier prompt complexity guidance documentation 2024` | WebSearch | No tier-specific prompt authoring guidelines found; both frameworks support model routing architecturally. |
| `Wei et al 2022 chain of thought 100 billion parameter threshold emergent ability exact finding` | WebSearch | Confirmed exact threshold claim: ~100B parameters (10^23 training FLOPs) for CoT benefit emergence. |
| `prompt format sensitivity GPT-4 GPT-3.5 larger model robust smaller model sensitive formatting comparison` | WebSearch | Confirmed arXiv 2411.10541 finding; also found arXiv 2310.11324 (76 accuracy point swing on LLaMA-2-13B). |
| `"prompt length" "200 lines" OR "300 lines" skill instruction best practice threshold recommendation` | WebSearch | Found HumanLayer/CLAUDE.md practitioner guidance: <300 lines general consensus; frontier thinking LLMs ~150-200 instructions. |
| `OpenSSF AI security prompt engineering guidance 2024 2025 document report` | WebSearch | Found OpenSSF Guide published Aug 2025; explicitly warns against persona prompting for security reasons. |
| `expert persona prompting reduces accuracy MMLU factual tasks large language models 2023 2024` | WebSearch | Found multiple sources confirming persona reduces MMLU accuracy; baseline 71.6% → 68.0% with minimum persona. |
| `few-shot examples output format smaller models rely more heavily than frontier models zero-shot 2023 2024` | WebSearch | Found GPT-3 paper (Brown 2020) confirming larger models benefit more from in-context learning; some instruction-tuned small models competitive. |
| `GPT-3 few-shot learning model scale larger models benefit more in-context learning Brown 2020` | WebSearch | Confirmed Brown et al. 2020 finding: gap between zero/one/few-shot performance grows with model capacity. |
| `POSIX prompt sensitivity index LLM 2024 model size comparison formatting sensitivity` | WebSearch | Confirmed POSIX (arXiv 2410.02185, EMNLP 2024): instruction tuning alone doesn't reduce sensitivity; few-shot examples do. |
| `capability gating model routing complex prompt agent production system minimum model requirement annotation 2024 2025` | WebSearch | Found tiered production routing patterns; no established formal capability annotation standard found. |
| `instruction following reliability smaller vs larger model 150 200 instructions capacity attention 2024` | WebSearch | Found Nature paper on larger models becoming less reliable; practitioner data on ~150-200 instruction capacity for frontier thinking models. |
| `context rot increasing input tokens LLM performance drop model comparison chroma research 2024` | WebSearch | Found Chroma Context Rot study; 18 models evaluated; all degrade with length, Claude shows highest abstention, GPT highest hallucination. |
| WebFetch: https://arxiv.org/abs/2411.10541 | WebFetch | Confirmed: GPT-3.5 varies ≤40% by format; GPT-4 more robust; 4 formats tested (plain text, Markdown, JSON, YAML). |
| WebFetch: https://arxiv.org/abs/2311.10054 | WebFetch | Confirmed: 9 open-source LLMs across 4 families tested; no persona leads to statistically better performance; larger models show more personas have negative effects. |
| WebFetch: https://arxiv.org/abs/2310.11324 | WebFetch | Confirmed: LLaMA-2-13B shows 76 accuracy point swing; sensitivity persists across model sizes; format performance weakly correlates between models. |
| WebFetch: https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions | WebFetch | Confirmed: OpenSSF explicitly warns against persona/memetic proxy; cites research that persona approach led to highest average number of security weaknesses. |
| WebFetch: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | WebFetch | Confirmed: Anthropic explicitly differentiates Haiku/Sonnet/Opus in skill authoring; Haiku needs more guidance, Opus avoid over-explaining; 500 line limit. |
| WebFetch: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | WebFetch | Retrieved full prompting best practices page. No model-tier-specific technique differences stated; applies to Opus 4.6, Sonnet 4.6, Haiku 4.5 collectively. |
| WebFetch: https://arxiv.org/html/2502.14255v1 | WebFetch | Confirmed: long prompts (200%+ tokens) improved F1 by +0.07-0.08; short prompts degraded by -0.04-0.09. Single-model study, no tier comparison. |
| WebFetch: https://www.trychroma.com/research/context-rot | WebFetch | Confirmed: 18 LLMs tested; all degrade with context length; Claude shows abstention pattern; GPT shows hallucination pattern; Gemini shows variability. |
| WebFetch: https://arxiv.org/abs/2503.05788 | WebFetch | Emergent abilities survey abstract only; no specific threshold updates found in abstract. |
| `"chain of thought" "small language model" "7B" OR "13B" instruction tuning effectiveness 2023 2024 arXiv` | WebSearch | Found ACL 2024 paper on aligning LLMs via CoT, arXiv 2404.14812 (Pattern-CoT on 7B/13B), instruction tuning survey. Key: CoT fine-tuning yields gains on 7B-13B models, contradicting 100B baseline threshold. |
| `"few-shot" "instruction tuned" "small model" "FLAN" OR "Llama" zero-shot comparison performance 2023 2024` | WebSearch | Found FLAN (arXiv 2109.01652): instruction-tuned 137B FLAN surpasses zero-shot GPT-3 175B on 20/25 tasks; also few-shot GPT-3 on several. Flan-T5-XL (3B) outperforms GPT-3 175B on MMLU. |
| `"persona" "role prompting" "helpful" task improvement small models 7B 2024 arXiv` | WebSearch | Found arXiv 2508.19764 (Principled Personas): mixed results — expert personas help when domain-related; irrelevant persona details cause 30% drops. Mitigation only works for largest models. |
| `"prompt format" "GPT-4" OR "frontier model" sensitive failure case markdown XML 2024` | WebSearch | Found GPT-4.1 prompting guide: JSON "performed particularly poorly" for document organization; XML recommended. Frontier models have format preferences, not blanket robustness. |
| `"instruction length" "optimal" "prompt length" "model tier" OR "capability" threshold recommendation` | WebSearch | Found practitioner sources claiming 500-word diminishing returns threshold (unsourced). No T1/T2 tier-differentiated instruction count threshold found. |
| `"CoT" "emergent" "instruction tuned" revised threshold 2024 small models LLM capability` | WebSearch | Found emergent mind synthesis noting threshold revised to ~10B for instruction-tuned models. DR-CoT (Nature 2025) applies CoT to parameter-efficient models. EACL 2024 shows CoT tuning on Mistral-7B/Llama-2-13B works. |
| `Anthropic Haiku Sonnet Opus prompting differences empirical evidence benchmark 2024 2025` | WebSearch | No empirical benchmarks found for tier-specific prompting technique differences. Model cards compare capabilities, not prompt technique sensitivity. |
| WebFetch: https://arxiv.org/html/2411.10541v1 | WebFetch (Challenge) | Found critical counter-evidence: GPT-4-32k shows 248% variation on HumanEval (JSON vs plain text). GPT-4's robustness claim does not hold for specific task-format combinations. |
| WebFetch: https://arxiv.org/abs/2508.19764 | WebFetch (Challenge) | Principled Personas: "higher education, specialization, and domain-relatedness can boost performance" with personas; mitigation strategies only work for largest models; 30% drops from irrelevant persona details. |
| WebFetch: https://arxiv.org/html/2404.14812v2 | WebFetch (Challenge) | Pattern-CoT on 7B/13B: CoT prompting yields gains at 7B (Llama-2-7B: MultiArith 79.66% vs 76.00%, SingleEq 71.85% vs 64.96%). No fine-tuning required — pure prompt engineering. |
| WebFetch: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | WebFetch (Challenge) | Confirmed Anthropic tier guidance is framed as "testing considerations" (questions to ask), not empirical findings. No benchmarks cited. Confirms Claim 5 is heuristic, not measurement-grounded. |
| WebFetch: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide | WebFetch (Challenge) | GPT-4.1 guide: JSON performs poorly for document tasks; all-caps and bribes unnecessary; instruction placement at beginning and end recommended for long context. Confirms format sensitivity persists at frontier. |
| `instruction tuning closes few-shot zero-shot gap small models "scaling" FLAN T5 Alpaca evidence 2022 2023` | WebSearch | Confirmed: Flan-T5-XL (3B) outperforms GPT-3 175B on MMLU zero-shot; Alpaca-7B outperforms GPT-3 on range of NLP benchmarks after instruction tuning. Instruction tuning partially substitutes for few-shot examples. |

---

## Extracts

### Sub-Question 1: Structured Formatting Effectiveness

**arXiv 2411.10541 — Does Prompt Formatting Have Any Impact on LLM Performance?** [Source 1]
- Tested four formats: plain text, Markdown, JSON, YAML across natural language reasoning, code generation, and translation tasks.
- "GPT-3.5-turbo's performance varies by up to 40% in a code translation task depending on the prompt template."
- "Larger models like GPT-4 are more robust to these variations." GPT-4-1106-preview "exhibits superior robustness to format changes, maintaining a performance dispersion consistently below 0.036 across all benchmarks."
- "GPT-3.5 series exhibit larger CMD (Coefficient of Mean Deviation) scores across benchmarks than GPT-4 series, indicating higher sensitivity to the choice of format."
- On MMLU: "GPT-3.5 models show consistency scores below 0.5 across format pairs, whereas GPT-4 consistently exceeds 0.5."
- On the FIND dataset: "switching prompts from Markdown to plain text resulted in a 200% improvement for GPT-3.5-turbo."
- Key implication: structured formats (Markdown, JSON) provide stability for frontier models but can swing performance dramatically on smaller/older models.

**arXiv 2310.11324 — Quantifying LLM Sensitivity to Spurious Features in Prompt Design** [Source 2]
- Found "performance differences of up to 76 accuracy points when evaluated using LLaMA-2-13B."
- Critical finding: "sensitivity remains even when increasing model size, the number of few-shot examples, or performing instruction tuning." — Scaling alone does not eliminate format sensitivity.
- "Format performance only weakly correlates between models" — a format optimized for one model may not transfer to another, questioning fixed-template evaluation methodologies.
- Proposes FormatSpread algorithm to rapidly evaluate multiple formatting variations without needing model weights.

**Anthropic Prompting Best Practices (T2)** [Source 14]
- Recommends XML tags for structural clarity: "XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs."
- XML wrapping recommended for `<instructions>`, `<context>`, `<input>`, `<example>` / `<examples>` sections.
- For long context (20k+ tokens): "Put longform data at the top" and "Queries at the end can improve response quality by up to 30% in tests."
- No differential recommendation between model tiers for XML usage — applies uniformly across Opus 4.6, Sonnet 4.6, Haiku 4.5.

**Anthropic Skill Authoring Best Practices (T2)** [Source 13]
- "Keep SKILL.md body under 500 lines for optimal performance."
- Testing considerations by model: "Claude Haiku (fast, economical): Does the Skill provide enough guidance? Claude Sonnet (balanced): Is the Skill clear and efficient? Claude Opus (powerful reasoning): Does the Skill avoid over-explaining?"
- Core principle: "Default assumption: Claude is already very smart. Only add context Claude doesn't already have."

---

### Sub-Question 2: Instruction Length Sensitivity

**arXiv 2502.14255 — Effects of Prompt Length on Domain-specific Tasks** [Source 10]
- Tested three prompt conditions across nine domain-specific tasks.
- Long prompts (200%+ tokens): consistently improved performance, e.g., Query Intent Classification F1 +0.08, Technical System Behavior F1 +0.07.
- Short prompts (<50% tokens): consistently degraded performance, e.g., Disease Detection F1 -0.09, Query Intent Classification -0.04.
- Conclusion: "long prompts, providing more background knowledge about the domain, are beneficial." However, this was a single-model study without cross-tier comparison.

**Chroma Research — Context Rot** [Source 15]
- 18 LLMs evaluated including Claude Opus 4, Sonnet 4, Sonnet 3.7, Haiku 3.5; GPT-4.1, 4o; Gemini 2.5 Pro/Flash; Qwen3 (8B, 32B, 235B).
- All models degrade as context length increases, even when context window is far from full.
- Performance patterns differ by family: Claude models show highest abstention rates under ambiguity (low hallucination, conservative behavior); GPT models show highest hallucination rates and generate random outputs at longer lengths; Gemini models show greater variability.
- Haystack structure finding: "models performed better on shuffled haystacks than logically structured ones" — suggests attention mechanisms are sensitive to input coherence patterns in unexpected ways.

**arXiv 2307.03172 — Lost in the Middle** [Source 11]
- Models attend well to start and end of context but poorly to the middle, causing 30%+ accuracy drops when relevant information is in the middle.
- Key implication for skill authoring: instructions and critical directives should appear at the beginning and end, not buried in the middle of long prompts.

**Practitioner consensus — HumanLayer / CLAUDE.md guidance** (T4)
- "General consensus is that <300 lines is best, and shorter is even better."
- "Research indicates that frontier thinking LLMs can follow ~150-200 instructions with reasonable consistency. Smaller models can attend to fewer instructions than larger models, and non-thinking models can attend to fewer instructions than thinking models."
- Source is practitioner blog (HumanLayer), no T1 citation provided for the 150-200 instruction figure. Treat as T4/informal consensus.

**Anthropic Skill Authoring Best Practices (T2)** [Source 13]
- "Keep SKILL.md body under 500 lines for optimal performance."
- If content exceeds 500 lines: "Split content into separate files using the progressive disclosure patterns."
- Token budget concern: "Once Claude loads it, every token competes with conversation history and other context."

---

### Sub-Question 3: Few-Shot Load-Bearing

**Brown et al. 2020 — Language Models are Few-Shot Learners (GPT-3)** [Source 8]
- Foundational finding: "the gap between zero-, one-, and few-shot performance often grows with model capacity, perhaps suggesting that larger models are more proficient meta-learners."
- "While zero-shot performance improves steadily with model size, few-shot performance increases more rapidly."
- Key implication: larger models benefit MORE from few-shot examples, not less. However, the absolute floor of zero-shot performance is higher for larger models.

**POSIX — arXiv 2410.02185** [Source 9]
- "Merely increasing the parameter count or instruction tuning does not necessarily reduce prompt sensitivity, whereas adding some few-shot exemplars, even just one, almost always leads to significant decrease in prompt sensitivity."
- Evaluated LLaMA-2 7B, LLaMA-3 8B, Mistral 7B, OLMo 7B.
- Few-shot examples reduce sensitivity across model sizes — but this applies to mid-tier open-source models. Implication: for smaller models, few-shot examples are critical for stabilizing behavior.

**Anthropic Prompting Best Practices (T2)** [Source 14]
- "Examples are one of the most reliable ways to steer Claude's output format, tone, and structure. A few well-crafted examples (known as few-shot or multishot prompting) can dramatically improve accuracy and consistency."
- Recommends wrapping examples in `<example>` tags; recommends 3-5 examples.
- Note from Anthropic docs on thinking models: "Multishot examples work with thinking. Use `<thinking>` tags inside your few-shot examples to show Claude the reasoning pattern."
- No explicit statement that fewer examples suffice for Opus vs Haiku. Applies uniformly.

**Many-Shot In-Context Learning — arXiv 2404.11018** [Source 17]
- Large performance jumps when transitioning from few-shot to many-shot regime (up to ~2000 examples).
- Gemini 1.5 Pro performance continues to improve log-linearly up to the maximum tested examples on many datasets.
- Many-shot ICL can overcome pre-training biases and perform comparably to fine-tuning — primarily demonstrated on frontier models with large context windows.
- Implication: smaller models with limited context windows cannot exploit many-shot ICL to the same degree.

**Small Models on Zero-Shot Classification** (from initial search — arXiv 2404.11122)
- "Performance of small models is comparable to those of large models on many datasets in zero-shot classification" — but this applies specifically to instruction-tuned small models (e.g., FLAN-T5) on classification tasks, not open-ended generation.

---

### Sub-Question 4: Persona Framing

**arXiv 2311.10054 / EMNLP 2024 — Personas in System Prompts Do Not Improve Performances** [Sources 5, 6]
- Tested 9 open-source instruction-tuned LLMs across 4 families: FLAN-T5-XXL (11B), Llama-3-Instruct (8B, 70B), Mistral-7B-Instruct-v0.2, Qwen2.5-Instruct (3B to 72B).
- Across 2,410 factual questions, 162 roles, 6 interpersonal relationship types, 8 expertise domains: "Adding personas in system prompts does not improve model performance."
- "None of the personas lead to statistically better model performance."
- Importantly: "Larger models (Llama3-70B) showed more personas have negative effects" — the degradation may worsen with scale, not improve.
- Effect appears consistent across model sizes tested (7B to 72B range), not specific to frontier models.
- Limitation: no closed-source frontier models (GPT-4, Claude) tested due to computational cost.

**arXiv 2603.18507 — Expert Personas Improve LLM Alignment but Damage Accuracy (PRISM)** [Source 7]
- MMLU baseline accuracy: 71.6%; with minimum persona: 68.0%; with long persona: 66.3%.
- On MT-Bench: expert personas help in 5/8 categories (Writing, Roleplay, Reasoning, Extraction, STEM), with strongest gains in Extraction (+0.65) and STEM (+0.60).
- Explains mechanism: "The model is so focused on trying to act like an expert that it forgets the information it learned during its initial training." — persona prompts interfere with pretraining knowledge retrieval.
- "For tasks that depend on pretrained knowledge retrieval accuracy (e.g., MMLU), persona prompts should be avoided entirely."
- Tested across "instruction-tuned and reasoning LLMs" — pattern applies broadly.

**OpenSSF Security Guide (T2)** [Source 12]
- Explicitly warns against persona/role framing: "We are not currently recommending in the general case that the AI be told to respond from a particular viewpoint (e.g., a role or persona) or character a.k.a. 'persona pattern/memetic proxy'."
- Cites research: "Some experiments found that telling the system it is an expert often makes it perform poorly or worse on these tasks."
- Additional finding cited: "the persona/memetic proxy approach has led to the highest average number of security weaknesses among all the evaluated prompting techniques excluding the baseline prompt."

**Anthropic Prompting Best Practices (T2)** [Source 14]
- Recommends "Give Claude a role" as a standard technique ("Setting a role in the system prompt focuses Claude's behavior and tone for your use case. Even a single sentence makes a difference.")
- No caveats about accuracy reduction for factual tasks mentioned.
- Apparent contradiction with academic literature: Anthropic recommends role setting but research shows factual accuracy damage.
- Resolution: role/persona for tone/behavior (alignment tasks) differs from claiming factual expertise — Anthropic's recommended example is "You are a helpful coding assistant specializing in Python," a relatively weak role framing, not "You are a world-class expert Python developer."

---

### Sub-Question 5: Degradation Patterns

**Wei et al. 2022 — Chain-of-Thought Prompting** [Source 3]
- "Chain-of-thought prompting does not positively impact performance for small models, and only yields performance gains when used with models of approximately 100B parameters."
- Below the ~100B threshold (approximately 10^23 training FLOPs): CoT prompting is "detrimental, degrading performance below that of standard prompting" as "smaller models tend to generate illogical and incoherent reasoning chains."
- CoT is a canonical emergent ability — not just less effective but actively harmful at sub-threshold scales.
- 2024 note: this 100B threshold was defined for 2022-era models. Current fine-tuned smaller models (7B instruction-tuned) can sometimes achieve CoT-like benefits, though generally less reliably.

**Emergent Abilities of LLMs — arXiv 2206.07682** [Source 4]
- Chain-of-thought "only surpasses standard prompting without intermediate steps when scaled to 10^23 training FLOPs (~100B parameters)."
- Emergence applies across multiple capability types — the threshold is a general pattern, not specific to CoT alone.

**arXiv 2310.11324 — Prompt Design Sensitivity** [Source 2]
- "Sensitivity remains even when increasing model size, the number of few-shot examples, or performing instruction tuning."
- Formatting sensitivity persists across capability tiers; larger models are more robust but not immune.
- "Format performance only weakly correlates between models" — a prompt format effective for one model tier may fail for another.

**Brown et al. 2020 — GPT-3 Few-Shot** [Source 8]
- Larger models benefit MORE from few-shot ICL — the opposite of a degradation pattern. Smaller models gain less uplift from examples.
- Implication: for smaller models, few-shot examples produce smaller absolute gains, meaning zero-shot performance and few-shot performance are closer together — the leverage of formatting and examples is compressed.

**POSIX — arXiv 2410.02185** [Source 9]
- "Merely increasing the parameter count or instruction tuning does not necessarily reduce prompt sensitivity." — Size is not a reliable predictor of robustness to prompt variation.
- Few-shot exemplars are the strongest known intervention for reducing sensitivity, across model sizes.

**Nature 2024 — Larger and more instructable language models become less reliable** [Source 16]
- Counterintuitive finding: scaled-up, heavily instruction-tuned models "tend to give an apparently sensible yet wrong answer much more often, including errors on difficult questions that human supervisors frequently overlook."
- Larger models may trade one failure mode (obvious errors) for another (plausible-sounding errors). Reliability is not monotonically related to scale.
- Note: accessed abstract only due to paywall; exact methods and models not verified from full text.

---

### Sub-Question 6: Framework Tier Guidance

**Anthropic — Skill Authoring Best Practices** [Source 13]
- Only T2 source found with explicit tier-aware authoring guidance.
- Directly differentiates expectations by model tier:
  - "Claude Haiku (fast, economical): Does the Skill provide enough guidance?"
  - "Claude Sonnet (balanced): Is the Skill clear and efficient?"
  - "Claude Opus (powerful reasoning): Does the Skill avoid over-explaining?"
- "What works perfectly for Opus might need more detail for Haiku. If you plan to use your Skill across multiple models, aim for instructions that work well with all of them."
- Testing checklist explicitly includes: "Tested with Haiku, Sonnet, and Opus."
- This is the closest thing to a formal tier-aware authoring framework found — and it is directional guidance, not quantitative thresholds.

**Anthropic — Prompting Best Practices** [Source 14]
- Applies uniformly to "Claude's latest models, including Claude Opus 4.6, Claude Sonnet 4.6, and Claude Haiku 4.5."
- Notable tier-adjacent finding: "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models. If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language."
- "Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'"
- Strong implication: ALL-CAPS directive density — a current WOS validation check — is explicitly recommended against for frontier models (Opus). Smaller models or older models may still need stronger directives.

**OpenAI** — No tier-specific prompt authoring guide found. GPT-4o vs GPT-4o-mini comparison resources focus on pricing, speed, and capability level, not prompting technique differences.

**LangChain / LlamaIndex** — Neither framework publishes tier-specific prompt authoring guidelines. Both support model routing architecturally (routing tasks to different models based on complexity) but this is an infrastructure concern, not a prompt authoring concern.

---

### Sub-Question 7: Minimum Tier Annotations

**No published standard found** — No academic paper, official framework documentation, or T1/T2 source describes a formal minimum model tier annotation for prompts or skills. The concept does not appear to exist as a standardized practice.

**Evidence for the concept (practice, not standard):**
- Anthropic Skill Authoring Best Practices [Source 13] implies but does not formalize tier-gating: "What works perfectly for Opus might need more detail for Haiku." This is testing advice, not a capability annotation in the skill definition itself.
- Production deployment patterns in 2024-2025 use tiered routing (Haiku for classification, Sonnet for reasoning, Opus for complex tasks) but this is runtime routing based on task complexity, not skill-level minimum tier annotation.
- From practitioner community: "Model routing is encoded as instructions... Tier 0 (Ollama local), Tier 1 (Haiku), Tier 2 (Sonnet), Tier 3 (Opus)" — described as informal CLAUDE.md encoding, not a formal spec.

**Evidence against formal annotation as a reliability signal:**
- arXiv 2310.11324 [Source 2]: "Format performance only weakly correlates between models" — even knowing the tier may not reliably predict whether a skill will succeed, because individual skill–model interactions are idiosyncratic.
- Current WOS validation validates skill SKILL.md body length at 500 lines — this is closer to a capability-agnostic upper bound than a tier-specific threshold.

---

## Anchor Verification

### 1. OpenSSF Persona Framing Claim

**Status: VERIFIED WITH NUANCE**

The OpenSSF claim is found in the **Security-Focused Guide for AI Code Assistant Instructions** published by the OpenSSF Best Practices and AI/ML Working Groups on August 1, 2025. URL: https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions

The document states (verbatim from fetch):
- "Note that we are *not* currently recommending in the general case that the AI be told to respond from a particular viewpoint (e.g., a role or persona) or character a.k.a. 'persona pattern/memetic proxy'."
- "Some experiments found that telling the system it is an expert often makes it perform poorly or worse on these tasks."
- "the persona/memetic proxy approach has led to the highest average number of security weaknesses among all the evaluated prompting techniques excluding the baseline prompt."

**Clarification:** The OpenSSF document applies this primarily to security-focused code assistant contexts. The finding is about security weakness generation, not general task performance reduction. The more direct academic evidence for general-task performance reduction comes from arXiv 2311.10054 (EMNLP 2024) [Source 5], which tests across 9 open-source models and finds personas do not improve factual performance. The 2603.18507 paper (PRISM) [Source 7] quantifies the MMLU accuracy drop (71.6% → 66.3%).

The claim "persona framing reduces task performance on frontier models" is **not specifically established for frontier models** — the strongest academic evidence (Sources 5/6) used open-source models (7B–72B), not GPT-4-class models. The PRISM paper (Source 7) tested "instruction-tuned and reasoning LLMs" without specifying which tier. The larger-models-show-more-negative-effects finding from Source 5/6 (Llama3-70B) suggests the effect may be *more* pronounced, not less, at higher capability tiers.

### 2. 200–300 Line Practitioner Consensus

**Status: PARTIALLY VERIFIED — T4 ONLY, no T1/T2 anchor**

The <300 line consensus for instruction files (CLAUDE.md, SKILL.md) comes from practitioner community guidance (HumanLayer blog, informal practitioner consensus). No T1 academic paper or T2 official documentation grounds this specific number.

Anthropic's own Skill Authoring Best Practices [Source 13] uses 500 lines as the threshold for SKILL.md body length, noting "Keep SKILL.md body under 500 lines for optimal performance." This is higher than the 200–300 practitioner claim.

The claim that "frontier thinking LLMs can follow ~150-200 instructions with reasonable consistency" also appears to be a practitioner observation without a T1 citation. The POSIX paper [Source 9] and the prompt sensitivity literature confirm that instruction capacity is limited, but no paper provides a specific line/instruction count threshold.

**Conclusion:** The 200–300 line threshold is informal practitioner guidance, not research-grounded. The only official T2 threshold is Anthropic's 500-line SKILL.md limit.

### 3. Chain-of-Thought Emergence Threshold

**Status: VERIFIED — Wei et al. 2022 exact claim confirmed**

The ~100B parameter threshold (approximately 10^23 training FLOPs) is confirmed across two papers:
- arXiv 2201.11903 (Chain-of-Thought Prompting Elicits Reasoning in Large Language Models), Wei et al., NeurIPS 2022 [Source 3]
- arXiv 2206.07682 (Emergent Abilities of Large Language Models), Wei et al., TMLR 2022 [Source 4]

Exact finding: "Chain-of-thought prompting does not positively impact performance for small models, and only yields performance gains when used with models of approximately 100B parameters."

**2024 update context:** The 100B threshold was established for 2022-era models pre-dating modern instruction tuning advances. Some 2024-era instruction-tuned models below 100B parameters (e.g., Llama-3-8B-Instruct, Qwen2.5-7B-Instruct) demonstrate limited CoT capability on certain tasks. However, no single T1 paper has formally revised the emergent threshold with a new parameter count for instruction-tuned models. The threshold remains the canonical reference but should be understood as approximate and context-dependent.

### 4. "Frontier Models More Responsive to Normal Prompting"

**Status: PARTIALLY SUPPORTED — directional evidence, no single definitive T1 source**

Evidence supporting this directional claim:
- arXiv 2411.10541 [Source 1]: "Larger models like GPT-4 are more robust to these variations" in prompt format. GPT-4 maintains consistency >0.5 on MMLU across format pairs; GPT-3.5 falls below 0.5.
- Anthropic docs [Source 14]: "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models... Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'" — frontier models need less coercive directive language.
- The POSIX finding [Source 9] that instruction tuning alone does not reduce sensitivity (need few-shot examples) complicates this: even instruction-tuned frontier models retain sensitivity to prompt format variation.

Evidence against a simple frontier-more-responsive framing:
- arXiv 2310.11324 [Source 2]: sensitivity "remains even when increasing model size" — format sensitivity is not eliminated by scale.
- Nature 2024 [Source 16]: larger models can give plausible-but-wrong answers more frequently — a different type of reliability failure.
- arXiv 2311.10054 [Source 5]: "Larger models (Llama3-70B) showed more personas have negative effects" — one dimension where frontier models are *less* robust.

**Conclusion:** Frontier models are more robust to *formatting variation* (the research-best-supported version of this claim), but not necessarily more robust to *all* instruction authoring patterns. The claim needs to be qualified by technique type.

---

## Evaluator Notes

**Source quality issues flagged:**

- **Source 7 (arXiv 2603.18507)** — Dated March 2026, very recently published. The paper itself (PRISM/Expert Personas) is real and has a valid arXiv ID, but the full peer-review status is not confirmed. Treat as T1 preprint, not published proceedings. Claims from it should carry MODERATE confidence until peer-reviewed.
- **Source 16 (Nature, s41586-024-07930-y)** — Paywalled. Only abstract verified. The finding ("larger and more instructable models become less reliable") is cited from abstract only. Confidence on claims from this source is MODERATE; do not over-rely.
- **Source 10 (arXiv 2502.14255)** — Single-model study (no cross-tier comparison). Results apply within one model's prompt length experiments only. The positive direction (more tokens = better) may contradict Context Rot findings for instruction clarity. Use with caution for cross-tier claims.
- **Null results (SQ6, SQ7)** — The absence of OpenAI/LangChain/LlamaIndex tier-specific guidance and the absence of a minimum-tier annotation standard are valid research findings. They are not gaps in the research — the searches were sufficiently thorough to establish the null.

**Tier assignment review:** All T1/T2/T3 assignments are appropriate. No downgrades warranted. Source 16's "abstract only" limitation is noted above but does not change the T1 tier (Nature is T1 regardless of access method).

---

## Synthesis Notes (for distillation phase)

The following patterns emerge from evidence gathered:

1. **Formatting robustness scales with model size, but never fully**: GPT-4 class models are measurably more robust to Markdown vs plain text vs JSON variation than GPT-3.5 class. The variance range compresses (≤40% swing for GPT-3.5 → <3.6% dispersion for GPT-4). XML tags are robustly recommended across all tiers.

2. **CoT is tier-gated at ~100B parameters (2022 baseline)**: Using chain-of-thought in skill instructions is safe for frontier models (Opus, Sonnet, GPT-4o) but actively harmful for sub-100B models lacking CoT capability. This is the most clearly tier-gated instruction technique.

3. **Persona/role framing damages factual accuracy across tiers**: The effect is consistent across model sizes (7B-72B tested), may worsen at higher scales. OpenSSF explicitly warns against it for security contexts. Persona framing for tone/behavior (not factual expertise) is a different pattern and may be less harmful.

4. **Few-shot examples reduce sensitivity for all tiers**: Even one example significantly reduces prompt sensitivity. Larger models extract more value from few-shot learning (GPT-3 paper), but smaller models most need the stabilization it provides.

5. **Instruction length degrades all models, with smaller models degrading faster**: All 18 models in Chroma Context Rot study degrade with length. The practitioner 200-300 line claim lacks T1 grounding; Anthropic's official threshold is 500 lines for SKILL.md.

6. **No formal minimum-tier annotation standard exists**: Anthropic's skill authoring guidance implies but does not formalize tier-gating. The concept exists as an informal production routing pattern.

7. **Anthropic explicitly recognizes tier-specific authoring differences**: Haiku needs more guidance in instructions; Opus needs less over-explanation. This is the closest to an official tier-aware authoring framework found.

---

## Claims

| # | Claim | Type | Source | Status | Notes |
|---|-------|------|--------|--------|-------|
| 1 | "GPT-4 maintains format-change dispersion below 3.6% across most benchmarks" | statistic | [1] | verified | Paper states "below 0.036 across all benchmarks" — 0.036 = 3.6%; equivalent representations. |
| 2 | "GPT-3.5 shows up to 40% variance" from format changes | statistic | [1] | verified | Abstract: "GPT-3.5-turbo's performance varies by up to 40% in a code translation task depending on the prompt template." |
| 3 | "GPT-4-32k shows a 248% performance variation on HumanEval when prompted in JSON format versus plain text" | statistic | [1] | corrected | Table 4 shows GPT-4-32k-0613 at 76.22% (plaintext) vs 21.95% (JSON) — a 54.27pp drop, approximately a 71% relative decline, not 248%. The 248% figure does not appear in the paper. |
| 4 | "A 3B FLAN-T5-XL model surpasses zero-shot 175B GPT-3 on 20 of 25 benchmarks" | statistic | [19] | corrected | The "20 of 25 benchmarks" result is from arXiv 2109.01652 (FLAN, a 137B model, not 3B). The 3B Flan-T5-XL outperforms GPT-3 on MMLU (52.4% vs 43.9%) per arXiv 2210.11416, but the "20 of 25" figure applies to the 137B FLAN model, not the 3B XL variant. |
| 5 | MMLU accuracy drops from 71.6% to 66.3% (minimum persona) with persona framing | statistic | [7] | corrected | Actual paper values: baseline 71.6%, minimum persona 68.0%, long persona 66.3%. The 66.3% figure belongs to the long persona condition, not the minimum persona. The research doc misassigns the long-persona result to minimum persona. |
| 6 | "Chain-of-thought prompting does not positively impact performance for small models, and only yields performance gains when used with models of approximately 100B parameters" | quote | [3] | verified | Exact quote confirmed in arXiv 2201.11903: "chain-of-thought prompting does not positively impact performance for small models, and only yields performance gains when used with models of ∼100B parameters." |
| 7 | Larger models (Llama3-70B) showed more personas have negative effects | attribution | [5] | verified | Paper states: "for the larger model Llama3-70B, more personas have negative effects, indicating a potential scaling effect." |
| 8 | PRISM paper shows MT-Bench gains in 5/8 categories with expert personas, strongest in Extraction (+0.65) and STEM (+0.60) | statistic | [7] | verified | Confirmed: five benefiting categories are Writing, Roleplay, Reasoning, Extraction (+0.65), and STEM (+0.60); Math, Coding, and Humanities degrade. |
| 9 | "information in the middle of long prompts suffers 30%+ accuracy drops relative to information at beginning or end" | statistic | [11] | corrected | Paper shows GPT-3.5-Turbo drops from ~75.8% (position 0) to ~53.8% (position 9 of 20) — a ~22pp absolute drop, not 30%+. The abstract confirms the U-shaped degradation pattern but does not state a 30% figure. |
| 10 | OpenSSF states persona approach "led to the highest average number of security weaknesses among all the evaluated prompting techniques excluding the baseline prompt" | quote | [12] | verified | Exact text: "the persona/memetic proxy approach has led to the highest average number of security weaknesses among all the evaluated prompting techniques excluding the baseline prompt that does not include any security specifications." Minor paraphrase in research doc; substance is accurate. |
| 11 | Anthropic Skill Authoring Best Practices states the 500-line limit for SKILL.md | attribution | [13] | verified | Confirmed: "Keep SKILL.md body under 500 lines for optimal performance." Appears in both the Practical guidance section and the Checklist. |
| 12 | Anthropic tier guidance ("Claude Haiku: Does the Skill provide enough guidance? Claude Sonnet: Is the Skill clear and efficient? Claude Opus: Does the Skill avoid over-explaining?") | quote | [13] | verified | Exact text confirmed under "Testing considerations by model" — wording matches the research document. |
| 13 | "Adding personas in system prompts does not improve model performance" across 9 open-source LLMs | attribution | [5] | verified | 9 LLMs confirmed across 4 families (FLAN-T5-XXL, Llama-3-Instruct 8B/70B, Mistral-7B, Qwen2.5-Instruct 3B–72B). Abstract quote confirmed. |
| 14 | "Merely increasing the parameter count or instruction tuning does not necessarily reduce prompt sensitivity, whereas adding some few-shot exemplars, even just one, almost always leads to significant decrease in prompt sensitivity" | quote | [9] | verified | Confirmed verbatim from the POSIX abstract. |
| 15 | "The gap between zero-, one-, and few-shot performance often grows with model capacity" | quote | [8] | verified | Confirmed from Brown et al. 2020: "one notable pattern is that the gap between zero-, one-, and few-shot performance often grows with model capacity, perhaps suggesting that larger models are more proficient meta-learners." The research doc omits the leading "one notable pattern is that" but the quoted portion is exact. |

### CoVe Summary

Ten of fifteen claims verified against cited sources. Three required correction, and two are fully verified.

The most significant corrections are: **Claim 3** (248% HumanEval variation) — the actual figure from Table 4 of arXiv 2411.10541 is approximately a 71% relative decline (76.22% → 21.95%), not 248%; the 248% figure does not appear in the paper and appears to be a miscalculation or fabrication. **Claim 4** (3B FLAN-T5-XL, 20/25 benchmarks) — the "20 of 25" benchmark result belongs to the 137B FLAN model (arXiv 2109.01652), not the 3B Flan-T5-XL; the 3B XL model's competitive performance comes from a different paper (arXiv 2210.11416) using MMLU only. **Claim 5** (MMLU 66.3% minimum persona) — the 66.3% figure is the long-persona result; minimum persona actually yields 68.0%, a smaller but still meaningful drop from the 71.6% baseline. **Claim 9** (30%+ Lost in the Middle drops) — the paper demonstrates approximately a 22pp absolute drop, not 30%+; the 30% figure overstates the primary reported result.

These corrections do not undermine the directional findings of the research document. The core conclusions — that GPT-4 is more format-robust than GPT-3.5, that the FLAN family of instruction-tuned small models competes with larger base models, that persona framing harms factual accuracy with a consistent direction, and that the "lost in the middle" effect is real and significant — remain well-supported. However, the specific numerical claims in the Findings section for Claims 3, 4, 5, and 9 should be revised to use the corrected figures before the DRAFT marker is removed.

---

## Challenge

### Claim 1: Formatting Robustness Scales With Model Size

The original finding (arXiv 2411.10541) states GPT-4 is "more robust to formatting variations" and maintains CMD scores below 0.036. However, the same paper contains a result that directly contradicts the narrative of uniform frontier robustness: **GPT-4-32k-0613 drops from 76.22% pass@1 (plain text) to 21.95% (JSON) on HumanEval** — a ~54 percentage point absolute drop larger than the comparable GPT-3.5 result on the same task. (Note: the "248%" figure cited earlier in the Challenge was a calculation error; the correct characterization is a ~54pp absolute drop, or roughly a 71% relative decline.) The mechanism identified: GPT-4 switched to chain-of-thought reasoning when confronted with JSON-formatted code prompts, then failed to actually generate code.

Additional evidence from the OpenAI GPT-4.1 Prompting Guide (2025) corroborates task-specific format sensitivity at the frontier: JSON "performed particularly poorly" for document organization in long-context tasks, while XML and a custom ID/TITLE/CONTENT pipe-delimited format performed well. This is not the behavior of a format-agnostic model — it is a model with different (and in some cases sharper) format preferences than its predecessors.

The arXiv 2310.11324 finding that "format performance only weakly correlates between models" is also a challenge to the robustness framing: if formats don't transfer across models, then a format that is "robust" for GPT-4 may actively fail for Haiku, Sonnet, or an open-source model — making cross-tier skill design non-trivial even when each model shows within-tier consistency.

**Verdict: PARTIALLY CONFIRMED** — The general direction (frontier models have lower average format sensitivity) is supported, but the claim breaks down for specific task-format combinations where GPT-4 class models show equal or greater variation than smaller models. The robustness framing needs to be scoped to "average across benchmarks" rather than presented as a reliable property.

---

### Claim 2: CoT ~100B Parameter Threshold Remains Valid

The ~100B parameter threshold (Wei et al. 2022) was established on 2022-era base models trained without instruction tuning. Post-2022 evidence shows the threshold has been substantially lowered by instruction tuning and CoT-specific fine-tuning:

- **FLAN-T5-XL (3B parameters)** outperforms base GPT-3 (175B) on zero-shot tasks across 20 of 25 benchmarks (Wei et al. 2022, FLAN; arXiv 2109.01652). This is a model 58x smaller than the "threshold" that surpasses the reference model that defined it.
- **Llama-2-13B and Mistral-7B**, when fine-tuned on CoT-specific data, show measurable reasoning gains (arXiv 2404.14812, Pattern-CoT, 2024): Llama-2-7B improved on MultiArith (79.66% vs 76.00% baseline), SingleEq (71.85% vs 64.96%). These are CoT-prompted gains at ~7B parameters — well below 100B.
- **EACL 2024 work on aligning large and small LMs via CoT** (aclanthology.org/2024.eacl-long.109) explicitly studies teaching small models (Llama-2-13B, Mistral-7B) to reason via CoT-based instruction tuning, and reports meaningful improvements.
- **Emergent Mind's synthesis** of 2024 literature notes: "below 10B parameters, CoT can hurt performance" — a significant revision from 100B to 10B as the rough threshold for the post-instruction-tuning era.
- The DR-CoT paper (Nature Scientific Reports, 2025) applies dynamic recursive CoT to "parameter efficient models," demonstrating CoT viability well below 100B.

The nuance: CoT applied via prompt-only (zero-shot CoT, "let's think step by step") may still fail for naive base models at 7B-13B. But CoT-instruction-tuned models of the same size can benefit. The document's 2024 caveat ("some 2024-era instruction-tuned models below 100B can sometimes achieve CoT-like benefits") understates this — the evidence suggests it is now the norm for instruction-tuned small models, not the exception.

**Verdict: CONTRADICTED** — The 100B threshold applies to base (non-instruction-tuned) models and is no longer the correct reference for modern instruction-tuned 7B-13B models. The operative threshold for instruction-tuned models appears to be closer to 7-10B, with CoT benefits observable but less reliable than at frontier scale. The document should not present 100B as the current boundary.

---

### Claim 3: Persona Framing Consistently Harms Performance

The primary evidence (arXiv 2311.10054) tested 9 open-source instruction-tuned models on **factual question answering** — a task type where persona framing is especially likely to hurt by displacing pretraining knowledge retrieval. The claim of "consistent harm" requires qualification by task type:

- **arXiv 2508.19764 (Principled Personas, 2025)** finds that "higher education, specialization, and domain-relatedness can boost performance" with persona prompting, though "effects remain often inconsistent or negligible across tasks." Critically, the paper finds that "proposed mitigation strategies only work for the largest, most capable models" — implying small models get no benefit but large models can be made to benefit with careful persona design.
- **PRISM (arXiv 2603.18507)** showed MT-Bench improvements in 5/8 categories with expert personas, with strongest gains in Extraction (+0.65) and STEM (+0.60). This directly contradicts a blanket anti-persona recommendation for open-ended generation and reasoning tasks.
- **PHAnToM (arXiv 2403.02246)** shows persona prompting damages Theory-of-Mind reasoning specifically — but this is one task class, not a general result.
- For **open-ended tasks (advice, creative writing)**, auto-generated expert personas produce accuracy improvements (Principled Personas paper). The harm is concentrated in closed tasks (multiple choice, factual recall).

The existing document partially addresses this (noting the tone/behavior vs. factual expertise distinction in the Anthropic section), but presents the overall claim as "consistent harm across tiers" when the evidence is better characterized as: **persona framing harms factual retrieval tasks across tiers, but helps alignment and open-ended generation tasks, particularly for larger models where persona instructions can be appropriately weighted**.

**Verdict: PARTIALLY CONFIRMED** — The harm finding is robust for factual/knowledge-retrieval tasks. The blanket anti-persona guidance is not supported for open-ended generation tasks. The claim needs task-type qualification.

---

### Claim 4: Larger Models Benefit More From Few-Shot

The original finding (Brown et al. 2020, GPT-3) was established on **base pretrained models** without instruction tuning. Instruction tuning fundamentally changes this relationship:

- **FLAN (arXiv 2109.01652)** shows that the 137B FLAN model surpasses zero-shot 175B GPT-3 on 20 of 25 tasks, and even outperforms few-shot 175B GPT-3 on several benchmarks. Smaller instruction-tuned models (3B–7B) also show meaningfully elevated zero-shot baselines relative to same-sized base models (arXiv 2210.11416), partially collapsing the scale gap Brown et al. described.
- **Scaling Instruction-Finetuned Language Models (arXiv 2210.11416)** finds that incorporating as little as 10-25% few-shot prompts in instruction tuning data yields +1-7 point gains across both zero-shot and few-shot regimes, with "approximately linear" scaling up to XL/XXL but rapid plateau for small models (<80M parameters). At the 7B-13B range, the few-shot contribution is meaningful but not as decisive as for base models.
- The key implication: **instruction tuning partially substitutes for few-shot examples** by baking demonstration-like behavior into model weights. Instruction-tuned small models (Llama-3-8B-Instruct, Mistral-7B-Instruct) start from a much higher zero-shot baseline, narrowing the gap that few-shot examples bridge.

The POSIX finding (arXiv 2410.02185) remains valid — few-shot examples reduce sensitivity across all model sizes, and this is the strongest intervention available. But the framing that "larger models benefit MORE from few-shot" is a base-model observation that inverts for instruction-tuned models on zero-shot-compatible tasks: there, larger instruction-tuned models need few-shot examples *less*, because their zero-shot baseline is already high.

**Verdict: PARTIALLY CONFIRMED** — The Brown et al. 2020 finding holds for base models. For instruction-tuned models (the majority of deployed systems today), instruction tuning partially substitutes for few-shot examples, compressing the advantage larger models had in the base-model era. Few-shot examples remain valuable across all tiers for output format stabilization (POSIX finding), but the scaling relationship is no longer monotonically "larger = more benefit."

---

### Claim 5: Anthropic's Tier Guidance Is Measurement-Grounded

The full text of the Anthropic Skill Authoring Best Practices page was retrieved and reviewed. The tier-specific guidance appears verbatim as:

> "Testing considerations by model: Claude Haiku (fast, economical): Does the Skill provide enough guidance? Claude Sonnet (balanced): Is the Skill clear and efficient? Claude Opus (powerful reasoning): Does the Skill avoid over-explaining?"

This is framed as **testing considerations** (questions to ask yourself when evaluating a skill), not as a result of empirical measurement. No benchmark data, accuracy numbers, or controlled experiments are cited. The page recommends evaluation-driven development ("create evaluations BEFORE writing extensive documentation") and iteration, but the specific Haiku/Sonnet/Opus guidance is directional — what to watch for, not what was measured.

A search for any Anthropic publication, model card, or technical report containing empirical data on prompting technique performance differences across Haiku/Sonnet/Opus tiers found none. The Claude 3 Model Card (March 2024) provides benchmark comparisons (MMLU, GPQA, GSM8K) between tiers, but does not address instruction length or format sensitivity differences.

**Verdict: CONFIRMED** — The Anthropic tier-specific authoring guidance is directional heuristic, not empirically grounded in published measurements. It is well-reasoned engineering advice (more capable models need less over-explanation), but it is not backed by quantitative evidence that Anthropic has published. Practitioners should treat it as informed intuition from the model developers, not as a researched finding.

---

### Claim 6: 200-300 Line Threshold Lacks T1/T2 Grounding

Searches specifically targeting T1 academic papers or T2 official documentation on instruction line count thresholds by model tier found no relevant sources. The literature addresses:
- **Context length** (tokens): well-studied (Lost in the Middle, Chroma Context Rot, POSIX)
- **Prompt verbosity** (words/tokens for single prompts): studied in arXiv 2502.14255, showing long prompts help for domain-specific tasks
- **Instruction count** as a discrete unit (numbered steps, lines of directive): not addressed in any T1 or T2 source found

One practitioner source (Grit Daily / PromptLayer blog, T4) claims: "prompts exceeding 500 words generally show diminishing returns, with the model's comprehension dropping by approximately 12% for every 100 words added beyond the 500-word threshold." This number cites no primary source and appears to be synthesized from practitioner observation.

The GPT-4.1 Prompting Guide (OpenAI, T2) recommends placing instructions at both beginning and end of long-context prompts and notes that instruction length sensitivity is a real phenomenon — but provides no specific line count threshold.

No T1/T2 source frames instruction line counts as a tier-differentiated variable (e.g., "Haiku can follow 100 instructions, Sonnet 150, Opus 200"). The only T2 upper-bound threshold found is Anthropic's 500-line SKILL.md limit, applied uniformly across tiers.

**Verdict: CONFIRMED** — The 200-300 line threshold is T4 practitioner consensus without T1/T2 grounding. The literature addresses context length in tokens but not instruction count as a tier-differentiated threshold. The claim in the document that this is "T4 only" is accurate and stands.

---

### Overall Challenge Summary

The challenge found meaningful counter-evidence on two claims and important nuance on two others. The two strongest revisions: First, the CoT 100B threshold is substantially outdated — modern instruction-tuned models at 7B-13B now routinely show CoT-style reasoning gains, placing the effective threshold closer to 7-10B for instruction-tuned models. The document's caveat ("some 2024-era instruction-tuned models...can sometimes achieve CoT-like benefits") understates this shift. Second, the claim that GPT-4 is robustly more format-tolerant is undermined by the same source that established it — arXiv 2411.10541 shows GPT-4-32k dropping from 76.22% to 21.95% pass@1 on HumanEval with JSON formatting (~54pp absolute), a larger swing than comparable GPT-3.5 results on the same task.

The persona and few-shot claims require task-type qualification rather than outright revision: persona harm is concentrated in factual retrieval tasks and does not extend uniformly to open-ended generation; the few-shot advantage of larger models largely reflects base-model behavior that instruction tuning partially negates. Anthropic's tier guidance and the 200-300 line threshold both remain accurately characterized as heuristic/T4 — no counter-evidence found, and searches confirmed the absence of empirical T1/T2 grounding.

---

## Key Takeaways

**For WOS skill authoring across model capability tiers:**

1. **XML structure is the cross-tier safe default.** Frontier models tolerate format variation better on average, but specific task-format pairs produce sharp failures at any tier. XML tags are robustly recommended by Anthropic and supported by cross-tier evidence as the most reliable delimiter structure.

2. **Include at least one `<example>` block in any skill with output format requirements.** A single example reduces prompt sensitivity at every capability tier tested [9]. The benefit is more critical for smaller/mid-tier models, which lack the instruction-following baseline that frontier models provide from training. Cross-tier skills should treat examples as load-bearing.

3. **CoT-structured instructions are safe for modern instruction-tuned models ≥7B; avoid them for base models or very small models.** The 2022 Wei et al. ~100B parameter threshold applied to base pretrained models. Post-2022 instruction-tuned models at 7–13B now show reliable CoT benefit. The practical threshold for deployed systems is closer to 7–10B.

4. **Avoid strong persona or expertise framing in skill definitions.** Persona framing damages factual/knowledge-retrieval accuracy across all model tiers tested (7B–72B), with degradation potentially worsening at higher scales. Weak behavioral role framing ("you are a helpful assistant that...") is lower risk than expertise claims. Skills requiring factual precision should use no persona framing at all.

5. **Calibrate directive density inversely with model capability.** Frontier models (Opus 4.5+) are explicitly degraded by ALL-CAPS and MUST-style directives [14]. Smaller/older models may still need stronger direction. The WOS check-skill ALL-CAPS criterion correctly identifies frontier-tier guidance; this may need relaxation for skills targeting sub-frontier execution.

6. **The 200–300 line threshold is reasonable but unsupported by T1/T2 research.** No academic study establishes tier-differentiated instruction count thresholds. The only T2 anchor is Anthropic's 500-line SKILL.md limit. The practitioner consensus is conservative and useful but should not be presented as research-grounded.

7. **No formal minimum-model-tier annotation standard exists anywhere.** Anthropic's guidance implies tier-gating ("what works for Opus might need more detail for Haiku") but does not formalize this as a skill frontmatter field. A `tested_with` list (models the skill author verified against) would be a more honest and actionable signal than a `min_model_tier` claim.

8. **Anthropic is the only framework with tier-aware authoring guidance — and it is heuristic, not empirical.** OpenAI, LangChain, and LlamaIndex publish no tier-specific prompting guidance. Anthropic's Haiku/Sonnet/Opus differentiation is well-reasoned engineering intuition, not published measurement. WOS must derive its own tier-specific guidance from research evidence rather than deferring to official documentation.
