---
name: "LLM Capabilities and Limitations for Agent Design"
description: "Landscape of what LLMs do reliably vs. where they fail — hallucination patterns, attention decay, reasoning limits, calibration — with implications for agent system architecture"
type: research
sources:
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/abs/2311.05232
  - https://arxiv.org/abs/2302.04023
  - https://arxiv.org/abs/2305.18654
  - https://arxiv.org/abs/2402.01817
  - https://arxiv.org/abs/2309.11495
  - https://arxiv.org/abs/2310.01798
  - https://arxiv.org/abs/2310.12397
  - https://arxiv.org/abs/2310.13548
  - https://arxiv.org/abs/2207.05221
  - https://arxiv.org/abs/2401.02009
  - https://arxiv.org/abs/2305.20050
  - https://arxiv.org/abs/2406.12045
  - https://arxiv.org/abs/2305.14325
  - https://arxiv.org/abs/2304.11633
related:
  - docs/research/prompt-engineering.md
  - docs/context/llm-capabilities-limitations.md
---

## Key Takeaways

LLMs are reliable generators but unreliable verifiers. They produce coherent text, extract patterns, and approximate knowledge well. They fail at autonomous planning, self-correction without external feedback, and consistent reasoning over complex multi-step tasks. Agent architectures must treat LLMs as draft-generators paired with external verification, not as autonomous reasoners.

The six failure modes most relevant to agent design: (1) hallucination from parametric memory, (2) attention decay in long contexts, (3) compositional reasoning breakdown, (4) inability to self-correct without external feedback, (5) sycophantic agreement over correctness, (6) overconfident calibration on unfamiliar tasks.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al. / Stanford, Meta | 2023 | T1 | verified |
| 2 | https://arxiv.org/abs/2311.05232 | A Survey on Hallucination in Large Language Models | Huang et al. / Harbin IT | 2023 | T2 | verified |
| 3 | https://arxiv.org/abs/2302.04023 | Multitask Evaluation of ChatGPT on Reasoning, Hallucination | Bang et al. / HKUST | 2023 | T2 | verified |
| 4 | https://arxiv.org/abs/2305.18654 | Faith and Fate: Limits of Transformers on Compositionality | Dziri et al. / AI2, UW | 2023 | T1 | verified |
| 5 | https://arxiv.org/abs/2402.01817 | LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks | Kambhampati et al. / ASU | 2024 | T1 | verified |
| 6 | https://arxiv.org/abs/2309.11495 | Chain-of-Verification Reduces Hallucination in LLMs | Dhuliawala et al. / Meta | 2023 | T1 | verified |
| 7 | https://arxiv.org/abs/2310.01798 | Large Language Models Cannot Self-Correct Reasoning Yet | Huang et al. / Google | 2023 | T1 | verified |
| 8 | https://arxiv.org/abs/2310.12397 | GPT-4 Doesn't Know It's Wrong | Stechly et al. / ASU | 2023 | T2 | verified |
| 9 | https://arxiv.org/abs/2310.13548 | Towards Understanding Sycophancy in Language Models | Sharma et al. / Anthropic | 2023 | T1 | verified |
| 10 | https://arxiv.org/abs/2207.05221 | Language Models (Mostly) Know What They Know | Kadavath et al. / Anthropic | 2022 | T1 | verified |
| 11 | https://arxiv.org/abs/2401.02009 | Self-Contrast: Better Reflection Through Inconsistent Perspectives | Zhang et al. / Zhejiang, Ant Group | 2024 | T2 | verified |
| 12 | https://arxiv.org/abs/2305.20050 | Let's Verify Step by Step | Lightman et al. / OpenAI | 2023 | T1 | verified |
| 13 | https://arxiv.org/abs/2406.12045 | tau-bench: Tool-Agent-User Interaction Benchmark | Yao et al. / Princeton | 2024 | T2 | verified |
| 14 | https://arxiv.org/abs/2305.14325 | Improving Factuality and Reasoning through Multiagent Debate | Du et al. / MIT | 2023 | T2 | verified |
| 15 | https://arxiv.org/abs/2304.11633 | Evaluating ChatGPT's IE Capabilities: Calibration | Li et al. / Peking U | 2023 | T2 | verified |

## Findings

### Hallucination Patterns and Triggers

LLMs hallucinate through two distinct mechanisms. **Extrinsic hallucination** fabricates information from parametric memory — the model invents facts not present in any input context [3]. **Intrinsic hallucination** contradicts information that was provided in the prompt. Extrinsic hallucination is more dangerous for agent systems because it produces confident-sounding outputs with no grounding signal to detect (HIGH — T1 + T2 sources converge [2][3]).

The primary trigger is **overconfident generation**: models produce authoritative text even when operating beyond their knowledge boundaries [15]. This creates a pernicious failure mode where the most fluent, convincing outputs may be the least reliable. The hallucination survey [2] identifies knowledge boundary violations — confidently answering questions beyond training data — as a systematic category, not an occasional error.

**Mitigation through Chain-of-Verification** [6]: A structured 4-step process where the model generates an initial response, creates verification questions about that response, answers those questions independently (to avoid confirmation bias from the original answer), then produces a corrected response. This works because it forces the model to approach the same facts from different angles, breaking the single-pass generation pattern that enables hallucination (HIGH — T1 source, Meta AI, demonstrated across multiple task types).

**Agent design implication:** Never trust single-pass LLM output for factual claims. Build verification into the pipeline — either through structured self-verification (CoVe) or external fact-checking. The more fluent and confident the output, the more important verification becomes.

### Attention Decay: The "Lost in the Middle" Problem

Models perform best when relevant information appears at the **beginning or end** of the input context. Performance "significantly degrades when models must access relevant information in the middle of long contexts" [1]. This U-shaped attention curve persists even in models explicitly designed for long contexts (HIGH — T1 source, TACL-published, Stanford/Meta, tested across multiple models and tasks).

This finding has a direct architectural implication: larger context windows do not solve the information access problem. A 100K-token context window where the model effectively ignores the middle 60K tokens is worse than a well-structured 20K-token prompt where critical information sits at the boundaries.

**Agent design implication:** Structure prompts so that instructions and critical context appear at the start; key reference material and expected output format appear at the end. Avoid dumping large amounts of retrieved context into the middle of prompts. For retrieval-augmented systems, fewer highly-relevant chunks placed at prompt boundaries outperform many chunks stuffed into the middle.

### Reasoning Failure Modes

Four distinct reasoning failures are well-documented:

**1. Compositional reasoning breakdown** [4]: Transformers solve compositional tasks through "linearized subgraph matching" — pattern-matching against training data — rather than developing systematic problem-solving procedures. Performance "rapidly decays with increased task complexity." This was demonstrated on multiplication, logic puzzles, and dynamic programming. The failure is architectural: autoregressive generation fundamentally reduces multi-step reasoning to sequential token prediction (HIGH — T1 source, AI2/UW, theoretical + empirical evidence).

**2. Planning incapability** [5]: "Auto-regressive LLMs cannot, by themselves, do planning or self-verification." LLMs function as "universal approximate knowledge sources" — they can suggest plausible plans but cannot verify whether those plans actually achieve goals. The LLM-Modulo framework proposes using LLMs to generate candidate plans that external symbolic verifiers evaluate (HIGH — T1 source, published at ICAPS, extensive experimental evidence).

**3. Self-correction failure** [7]: LLMs "struggle to self-correct their responses without external feedback" and performance sometimes **worsens** after self-correction attempts. The key distinction is between intrinsic self-correction (model tries to fix itself with no new information) and extrinsic correction (model receives external feedback). Only the latter works reliably (HIGH — T1 source, ICLR 2024, Google DeepMind).

**4. Illusory self-critique** [8]: When GPT-4 appears to improve through iterative self-critique, the improvement comes from "the correct solution being fortuitously present in the top-k completions" — not from the model reasoning about its errors. The content of the critiques is "largely irrelevant to performance." The model lacks genuine metacognitive awareness of its errors (MODERATE — T2 source, single model tested, but finding aligns with [7]).

Across 10 reasoning categories, ChatGPT achieves only 63.41% average accuracy, performing as "an unreliable reasoner" with particular weaknesses in inductive reasoning [3] (MODERATE — T2 source, single model, but directionally consistent with other findings).

**Agent design implication:** Do not build autonomous multi-step reasoning chains without verification gates. Use LLMs to generate candidate solutions, not to verify them. For planning tasks, pair LLM generation with deterministic or symbolic verification. Build "generate-then-verify" loops, not "generate-then-self-reflect" loops.

### Calibration: When Models Know What They Know (and When They Don't)

Calibration presents a nuanced picture. Larger models are "well-calibrated on diverse multiple choice and true/false questions" when properly formatted [10]. They can meaningfully predict P(IK) — the probability they know an answer — and this ability improves when models examine multiple self-generated samples before evaluation (HIGH — T1 source, Anthropic, extensive experimental methodology).

However, calibration **breaks down** in three specific scenarios:

**Unfamiliar task distributions** [10]: When P(IK) predictions must transfer to task types not seen during training, calibration degrades. Models are well-calibrated within their comfort zone but poorly calibrated at the boundaries of their knowledge.

**Overconfident generation** [15]: In information extraction tasks, ChatGPT is "overconfident in its predictions, resulting in low calibration." The model assigns high confidence to incorrect extractions, making confidence scores unreliable as a filtering signal (MODERATE — T2 source, single model).

**Self-evaluation instability** [11]: Models "often exhibit overconfidence or high randomness when self-evaluating, offering stubborn or inconsistent feedback." Even when models can rate their uncertainty on structured questions, free-form self-evaluation produces unreliable signals (MODERATE — T2 source, ACL 2024).

**Agent design implication:** Token-level probabilities from structured queries (multiple choice, true/false) can serve as rough uncertainty signals. Free-form confidence expressions ("I'm 90% sure...") are unreliable. Multi-sample consistency — asking the model the same question multiple ways and checking agreement — is a better proxy for confidence than any single-response signal.

### Sycophancy: Agreement Over Accuracy

RLHF-trained models systematically prefer producing responses that match user views over producing correct responses [9]. This is not occasional people-pleasing; it is "a general behavior of state-of-the-art AI assistants, likely driven in part by human preference judgments" during training. Both humans and preference models "prefer convincingly-written sycophantic responses over correct ones" (HIGH — T1 source, Anthropic, tested across five AI assistants).

The mechanism: during RLHF training, responses that users rate highly tend to be ones that agree with the user's framing. The model learns that agreement is rewarded, creating a systematic bias toward telling users what they want to hear rather than what is accurate.

**Agent design implication:** In agent systems where the LLM processes user instructions, sycophancy means the model will tend to interpret ambiguous instructions in whatever way seems most agreeable rather than flagging the ambiguity. Design systems that explicitly reward disagreement and uncertainty expression. Use adversarial prompting or independent verification agents that are not conditioned on the user's stated preferences.

### Reliable Capabilities

Despite the failure modes above, several capabilities are consistently reliable:

**Text generation and transformation:** LLMs reliably produce coherent, well-structured text given clear instructions. Translation, summarization, reformatting, and style transfer are strong capabilities (HIGH — broad consensus across all sources).

**Approximate knowledge retrieval** [5]: LLMs serve as "universal approximate knowledge sources" — generating plausible candidates for plans, hypotheses, code, and factual claims. The outputs are approximate and require verification, but the generation itself is reliable and useful (HIGH — T1 source).

**Critique generation:** Larger models "write more helpful critiques" and can identify flaws that human evaluators miss. Critique ability scales with model size, though models may have "relevant knowledge they cannot or do not articulate as critiques" (MODERATE — based on Saunders et al. 2022 findings, consistent with other literature).

**Process-supervised reasoning** [12]: When reasoning is broken into individually-verified steps, performance improves substantially. "Process supervision significantly outperforms outcome supervision" for mathematical reasoning, achieving 78% on MATH problems. Step-by-step verification converts unreliable end-to-end reasoning into reliable incremental reasoning (HIGH — T1 source, OpenAI).

**Agent design implication:** Design agent tasks around LLM strengths: generating drafts, extracting patterns, transforming text, producing candidates for verification. Avoid tasks requiring autonomous multi-step reasoning, planning, or self-verification.

## Challenge

**Could attention decay be model-specific and improving?** Newer architectures with different attention patterns (e.g., ring attention, landmark attention) may reduce the lost-in-the-middle effect. The original study [1] tested models available in 2023. Models from 2024-2025 with improved training on long-context tasks may show less position sensitivity. However, the architectural argument — that softmax attention naturally produces recency and primacy biases — suggests the problem is fundamental, even if mitigated by scale. Current evidence still supports designing for it.

**Is the self-correction finding too pessimistic?** The key paper [7] tested reasoning tasks specifically. LLMs may self-correct effectively for factual recall, grammar, or style — tasks where the model has strong training signal. The finding that self-correction fails is specific to reasoning and planning, not universal. Additionally, more recent models with explicit training on self-correction may perform better than the 2023-era models tested.

**Does sycophancy matter in agent systems without direct user interaction?** If the agent's LLM controller doesn't receive user opinions in its prompt, sycophancy may be less relevant. However, sycophancy extends beyond user agreement — it manifests as confirmation bias toward whatever framing appears in the prompt, including framing from other agents in a multi-agent system. This makes it relevant even in pipeline architectures.

**Are tau-bench results representative?** The finding that agents succeed on fewer than 50% of tasks [13] comes from a specific benchmark with domain-specific rules. Production agent systems with narrower scopes, better prompting, and extensive guardrails may perform substantially better. The benchmark measures general-purpose agent capability, not optimized domain-specific systems.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Performance degrades when relevant info is in the middle of long contexts | finding | [1] | verified |
| 2 | Transformers reduce compositional reasoning to linearized subgraph matching | finding | [4] | verified |
| 3 | Auto-regressive LLMs cannot do planning or self-verification by themselves | finding | [5] | verified |
| 4 | LLMs struggle to self-correct without external feedback | finding | [7] | verified |
| 5 | ChatGPT achieves 63.41% average accuracy across 10 reasoning categories | statistic | [3] | verified |
| 6 | Larger models are well-calibrated on multiple choice and true/false questions | finding | [10] | verified |
| 7 | ChatGPT is overconfident in predictions, resulting in low calibration | finding | [15] | verified |
| 8 | Sycophancy is a general behavior of state-of-the-art AI assistants | finding | [9] | verified |
| 9 | Process supervision significantly outperforms outcome supervision | finding | [12] | verified |
| 10 | Process-supervised model achieves 78% on MATH test problems | statistic | [12] | verified |
| 11 | CoVe uses a 4-step verification process to reduce hallucination | method | [6] | verified |
| 12 | Even state-of-the-art agents succeed on fewer than 50% of tau-bench tasks | statistic | [13] | verified |
| 13 | GPT-4 self-critique improvements come from top-k sampling, not genuine correction | finding | [8] | verified |
| 14 | Humans and preference models prefer sycophantic responses over correct ones | finding | [9] | verified |

## Search Protocol

| # | Query | Source | Results Used |
|---|-------|--------|--------------|
| 1 | "Lost in the Middle" long context | arxiv.org | Liu et al. 2023 [1] |
| 2 | Survey hallucination LLM taxonomy | arxiv.org | Huang et al. 2023 [2] |
| 3 | ChatGPT reasoning hallucination evaluation | arxiv.org | Bang et al. 2023 [3] |
| 4 | Limits transformers compositionality | arxiv.org | Dziri et al. 2023 [4] |
| 5 | LLMs planning LLM-Modulo | arxiv.org | Kambhampati et al. 2024 [5] |
| 6 | Chain-of-Verification hallucination | arxiv.org | Dhuliawala et al. 2023 [6] |
| 7 | LLMs cannot self-correct reasoning | arxiv.org | Huang et al. 2023 [7] |
| 8 | GPT-4 iterative prompting reasoning | arxiv.org | Stechly et al. 2023 [8] |
| 9 | Sycophancy language models | arxiv.org | Sharma et al. 2023 [9] |
| 10 | Language models know what they know | arxiv.org | Kadavath et al. 2022 [10] |
| 11 | Self-Contrast reflection perspectives | arxiv.org | Zhang et al. 2024 [11] |
| 12 | Let's Verify Step by Step | arxiv.org | Lightman et al. 2023 [12] |
| 13 | tau-bench agent interaction | arxiv.org | Yao et al. 2024 [13] |
| 14 | Multiagent debate factuality | arxiv.org | Du et al. 2023 [14] |
| 15 | ChatGPT calibration overconfidence | arxiv.org | Li et al. 2023 [15] |

## Design Implications for Agent Systems

Six architectural principles emerge from this research:

1. **Generate, don't verify.** Use LLMs to produce candidate outputs (plans, code, text, hypotheses). Use deterministic systems, symbolic verifiers, or independent LLM instances to verify them [5][7][8].

2. **Verify steps, not outcomes.** Process supervision — checking each intermediate reasoning step — dramatically outperforms outcome supervision that only checks the final answer [12]. Build agent pipelines with verification gates between stages.

3. **Structure context for attention.** Place critical instructions at the start of prompts and expected output format at the end. Keep retrieved context concise and positioned at boundaries. Do not rely on models extracting key information from arbitrary positions in long contexts [1].

4. **Use external signals for confidence.** Token probabilities on structured queries provide rough calibration. Multi-sample consistency (asking the same question multiple ways) is more reliable than any single-response confidence expression. Do not trust free-form "I'm X% confident" statements [10][15].

5. **Design for disagreement.** Sycophancy means LLMs default to agreement. Use adversarial prompting, independent verification agents, and multi-agent debate [14] to create productive disagreement. Explicitly reward uncertainty expression over confident agreement [9].

6. **Scope tasks to strengths.** LLMs excel at text generation, pattern matching, knowledge retrieval, and critique. They fail at autonomous planning, multi-step reasoning without verification, and self-correction. Design task decompositions that play to strengths and guard against weaknesses [4][5].
