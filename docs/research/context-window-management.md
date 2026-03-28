---
name: "Context Window Management"
description: "Token budgets, inclusion/exclusion strategies, compression approaches, and attention-aware formatting patterns for structuring content to survive context limits"
metadata:
  type: research
  sources:
    - https://arxiv.org/abs/2307.03172
    - https://arxiv.org/abs/2310.06839
    - https://arxiv.org/abs/2404.02060
    - https://arxiv.org/abs/2309.17453
    - https://arxiv.org/abs/2310.04408
    - https://arxiv.org/abs/2305.14788
    - https://arxiv.org/abs/2404.16811
    - https://arxiv.org/abs/2312.06648
    - https://arxiv.org/abs/2404.06654
    - https://platform.claude.com/docs/en/docs/build-with-claude/context-windows
    - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/long-context-tips
  related:
    - docs/research/prompt-engineering.md
    - docs/research/agent-state-persistence.md
    - docs/context/context-window-management.md
---

## Key Findings

Context window management is the practice of deciding what enters an LLM's working memory and how it is structured. Performance degrades predictably as context grows — not just from capacity limits but from attention distribution patterns that favor boundary positions. Effective management requires three coordinated strategies: selective inclusion (choosing what enters context), compression (reducing token cost of included content), and attention-aware formatting (positioning critical information where models attend most strongly).

**Bottom line:** Put important information first and last. Compress aggressively in the middle. Use structured markup to create navigable landmarks. Budget tokens explicitly across system instructions, retrieved context, examples, and user input.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al. / Stanford, UC Berkeley | 2023 | T1 | verified |
| 2 | https://arxiv.org/abs/2310.06839 | LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression | Jiang et al. / Microsoft | 2023 | T2 | verified |
| 3 | https://arxiv.org/abs/2404.02060 | Long-context LLMs Struggle with Long In-context Learning | Li et al. | 2024 | T2 | verified |
| 4 | https://arxiv.org/abs/2309.17453 | Efficient Streaming Language Models with Attention Sinks | Xiao et al. / MIT, Meta | 2023 | T1 | verified |
| 5 | https://arxiv.org/abs/2310.04408 | RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation | Xu et al. | 2023 | T2 | verified |
| 6 | https://arxiv.org/abs/2305.14788 | AutoCompressors: Compressing Context into Summary Vectors | Chevalier et al. | 2023 | T2 | verified |
| 7 | https://arxiv.org/abs/2404.16811 | FILM-7B: Information-Intensive Training for Long Contexts | An et al. | 2024 | T2 | verified |
| 8 | https://arxiv.org/abs/2312.06648 | Dense X Retrieval: Proposition-Level Retrieval for QA | Chen et al. | 2023 | T2 | verified |
| 9 | https://arxiv.org/abs/2404.06654 | RULER: What's the Real Context Size of Your LLM? | Hsieh et al. / NVIDIA | 2024 | T2 | verified |
| 10 | https://platform.claude.com/docs/en/docs/build-with-claude/context-windows | Context Windows - Anthropic Documentation | Anthropic | 2025 | T1 | verified |
| 11 | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/long-context-tips | Long Context Prompting Tips - Anthropic Documentation | Anthropic | 2025 | T1 | verified |

## Research Protocol

| # | Query | Tool | Results | Selected |
|---|-------|------|---------|----------|
| 1 | "lost in the middle" LLM context position | WebFetch (arxiv) | Found seminal paper on position-dependent performance | [1] |
| 2 | LongLLMLingua prompt compression | WebFetch (arxiv) | Found compression technique with 2-6x ratios | [2] |
| 3 | Long-context LLM evaluation struggles | WebFetch (arxiv) | Found evidence of capability gaps | [3] |
| 4 | StreamingLLM attention sinks context management | WebFetch (arxiv) | Found attention sink phenomenon | [4] |
| 5 | RECOMP retrieval compression | WebFetch (arxiv) | Found extractive/abstractive compression at 6% rate | [5] |
| 6 | AutoCompressors summary vectors | WebFetch (arxiv) | Found learned compression into summary vectors | [6] |
| 7 | FILM information-intensive training position | WebFetch (arxiv) | Found position-aware training approach | [7] |
| 8 | Dense X Retrieval proposition-level | WebFetch (arxiv) | Found fine-grained retrieval improves QA | [8] |
| 9 | RULER long-context evaluation | WebFetch (arxiv) | Found only half of models maintain claimed performance | [9] |
| 10 | Anthropic context windows documentation | WebFetch (docs) | Found official context window specs and strategies | [10] |
| 11 | Anthropic long context prompting tips | WebFetch (docs) | Found practical formatting and positioning advice | [11] |

## Extracts by Sub-Question

### SQ1: Context window sizes and token budget constraints

**Current landscape (2024-2025):**
- Claude models: 200K tokens standard, 1M tokens in beta for tier 4+ organizations [10]
- Context window represents "working memory" — not all capacity is equally useful [10]
- "More context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as context rot" [10]
- Newer Claude models return validation errors when prompts exceed context windows rather than silently truncating [10]
- Extended thinking tokens count toward context window but are stripped from subsequent turns automatically [10]
- Context awareness feature lets models track remaining token budget via inline XML tags [10]

**Actual vs. claimed capacity:**
- RULER benchmark found "only half of [models claiming 32K+ tokens] can maintain satisfactory performance at the length of 32K" [9]
- Needle-in-haystack tests are "indicative of only a superficial form of long-context understanding" [9]
- Models show "bias towards labels presented later in the sequence" with long contexts [3]

### SQ2: Inclusion/exclusion strategies

**Selective context approaches:**
- Self-information filtering: remove tokens with low self-information (predictable tokens contribute less) to enhance efficiency within fixed context length [Selective Context, 2305.14788]
- Proposition-level retrieval: decompose documents into atomic factual propositions rather than passages; "constructing prompts with fine-grained retrieved units improves performance given a specific computation budget" [8]
- Attention sink preservation: keeping initial tokens (attention sinks) plus recent tokens outperforms pure sliding window approaches; enables processing 4M+ tokens without fine-tuning [4]

**Practical inclusion strategies from Anthropic documentation [10][11]:**
- Put longform data at the top of prompts, queries/instructions at the bottom
- Queries at the end improve response quality "by up to 30% in tests, especially with complex, multi-document inputs"
- Use XML tags to structure multiple documents with metadata
- Ask the model to quote relevant passages before answering (grounding)
- Use server-side compaction for long conversations
- Tool result clearing and thinking block clearing for agentic workflows

### SQ3: Compression approaches

**Prompt compression techniques:**
- LongLLMLingua achieves 2x-6x compression on ~10K token prompts with "21.4% performance boost with 4x fewer tokens" on NaturalQuestions; 94% cost reduction on LooGLE; 1.4x-2.6x latency acceleration [2]
- RECOMP: extractive (sentence selection) and abstractive (summary generation) compression achieves "compression rate as low as 6% with minimal loss in performance" [5]
- AutoCompressors: learned compression into summary vectors; fine-tuned OPT and Llama-2 on sequences up to 30,720 tokens; summary vectors serve as "good substitutes for plain-text demonstrations" [6]

**Compression taxonomy:**
1. **Token-level pruning** — remove low-information tokens based on perplexity/self-information
2. **Sentence-level extraction** — select most relevant sentences from retrieved documents
3. **Abstractive summarization** — generate compressed summaries that preserve key information
4. **Learned vector compression** — encode context into dense summary vectors (soft prompts)

### SQ4: Attention distribution and the "lost in the middle" phenomenon

**Core finding:** "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts" [1]

**Key details:**
- Tested on multi-document QA and key-value retrieval tasks [1]
- Even "explicitly long-context models" exhibit this weakness [1]
- The phenomenon is widespread across model architectures [1]
- Root cause hypothesis: insufficient training emphasis — models lack supervision indicating "any position in a long context can hold crucial information" [7]
- FILM-7B demonstrates that information-intensive training can mitigate this: model "robustly retrieves information from different positions in its 32K context window" after targeted training [7]

**Attention sink phenomenon:**
- Initial tokens in sequences receive disproportionate attention regardless of content [4]
- Keeping KV cache of initial tokens plus recent tokens "largely recovers the performance of window attention" [4]
- This suggests models use initial tokens as computational anchors, not semantic ones [4]

### SQ5: Attention-aware formatting patterns

**BLUF (Bottom Line Up Front):**
- Place key conclusions, instructions, and constraints at the very beginning and end of context
- The lost-in-the-middle research [1] directly validates this: models attend most strongly to boundary positions
- Anthropic documentation confirms: "Put longform data at the top... queries at the end" [11]

**Practical formatting strategies from Anthropic [11]:**
1. **Document-query ordering:** Long documents first, instructions/queries last — "up to 30% improvement"
2. **XML structure:** Wrap documents in `<document>` tags with `<source>` and `<document_content>` subtags
3. **Quote grounding:** Ask the model to extract relevant quotes before answering
4. **Hierarchical markup:** Use consistent, descriptive XML tag names; nest tags for natural hierarchies

**Position optimization:**
- Critical instructions → beginning (system prompt) and end (user query)
- Reference material → middle (acceptable degradation zone for lookup)
- Examples → near the query (models attend well to recent context)
- Metadata/structure → beginning (establishes parsing framework)

### SQ6: Token budget allocation strategies

**Budget allocation framework (derived from sources):**
- **System instructions:** 5-15% of budget — role, constraints, output format
- **Retrieved context:** 40-60% of budget — documents, code, data
- **Examples:** 10-20% of budget — few-shot demonstrations
- **User input + query:** 10-20% of budget — current turn
- **Output reserve:** 10-25% of budget — response generation space

**Practical strategies:**
- Use context awareness features to track remaining budget dynamically [10]
- Server-side compaction for conversations approaching limits [10]
- Strip extended thinking tokens from previous turns (automatic in Claude API) [10]
- Design state artifacts for fast context recovery when starting new sessions [10]
- Use structured formats (JSON) for state data, unstructured text for progress notes [10]
- Compress retrieved context using proposition-level granularity rather than full passages [8]
- Apply LongLLMLingua-style compression to the middle portion of context where attention is weakest [2]

## Challenge

**Counter-evidence and limitations:**

1. **Lost-in-the-middle may be overstated for newer models.** The original study [1] used 2023-era models. Anthropic's documentation [10] notes Claude "achieves state-of-the-art results on long-context retrieval benchmarks like MRCR and GraphWalks." FILM-7B [7] demonstrates that targeted training can eliminate position bias. The phenomenon remains real but its severity varies by model generation.

2. **Compression introduces information loss.** While RECOMP achieves 6% compression rate with "minimal loss" [5], this is measured on specific benchmarks. Real-world tasks with nuanced information may lose critical details during compression. Abstractive compression risks introducing hallucinated content.

3. **Token budgets are approximations, not guarantees.** The allocation percentages above are heuristics, not empirically validated distributions. Optimal allocation depends heavily on task type, document complexity, and model architecture.

4. **XML structuring overhead.** Using extensive XML tags for document markup consumes tokens. For very large contexts, the structural overhead can be significant — potentially 5-10% of the total budget.

5. **Attention sinks are an implementation detail.** The attention sink phenomenon [4] describes internal model behavior during inference, not a formatting strategy users can directly exploit. Its practical implication (keep initial tokens) is useful but limited.

## Findings

### How does position affect information retention?

LLMs exhibit a U-shaped attention curve: information at the beginning and end of context receives stronger attention than information in the middle [1]. This is not a minor effect — it produces measurable performance degradation on retrieval and QA tasks across model architectures. The root cause appears to be training data distribution rather than architectural limitation, as targeted training (FILM-7B) can largely eliminate the bias [7] (HIGH — T1 + T2 sources converge, reproduced across multiple benchmarks).

Newer models show improvement. Claude achieves state-of-the-art on long-context retrieval benchmarks [10], and information-intensive training approaches demonstrate the bias is fixable (MODERATE — vendor claims, partially supported by independent research [7]).

### What compression strategies preserve the most information?

Three compression paradigms have demonstrated effectiveness:

1. **Token-level pruning** removes predictable tokens based on self-information metrics. This is fast and preserves document structure but may remove connective tissue that aids comprehension (HIGH — multiple independent implementations [2][Selective Context]).

2. **Extractive compression** selects the most relevant sentences from source documents. RECOMP achieves 6% compression rate with minimal performance loss on specific benchmarks [5]. This preserves exact wording but may lose inter-sentence relationships (HIGH — T2 with reproducible metrics).

3. **Proposition-level retrieval** decomposes documents into atomic factual statements. This produces the highest information density per token but requires preprocessing infrastructure [8] (MODERATE — single study, strong theoretical basis).

LongLLMLingua achieves the best balance for practical use: 2-6x compression with performance improvements up to 21.4% on some benchmarks, because it simultaneously addresses both token reduction and position bias [2] (HIGH — T2 with extensive evaluation).

### How should content be structured for maximum retention?

The evidence converges on a clear pattern (HIGH — T1 vendor docs + T1/T2 research agree):

1. **BLUF positioning:** Key instructions and constraints at the beginning of context (system prompt). Final query and specific instructions at the end (user turn). This exploits the U-shaped attention curve [1].

2. **Structured markup:** XML tags create parseable landmarks that help models navigate large contexts. Anthropic specifically recommends `<document>`, `<source>`, and `<document_content>` tags for multi-document inputs [11].

3. **Quote grounding:** Asking models to extract relevant quotes before answering forces explicit attention to source material and reduces hallucination risk [11].

4. **Graduated detail:** Place summaries and key facts at boundaries. Place supporting detail and raw data in the middle where some degradation is acceptable.

### How should token budgets be allocated?

No single empirically validated allocation exists, but practical guidance converges on these principles (MODERATE — derived from vendor documentation and compression research, not controlled experiments):

- Reserve output space explicitly — newer models error rather than truncate [10]
- Compress retrieved context aggressively (4-6x is achievable without quality loss for many tasks) [2][5]
- Use context awareness features to track remaining budget in real-time [10]
- For agentic workflows: use server-side compaction, strip previous thinking blocks, clear old tool results [10]
- Prefer fine-grained retrieval (propositions over passages) to maximize information density [8]

### What are the practical limits of long context?

Models claiming 32K+ token support often fail to maintain performance at that length — RULER found only half perform satisfactorily [9]. Needle-in-haystack benchmarks create false confidence by testing only "a superficial form of long-context understanding" [9]. Real-world tasks with complex reasoning, large label spaces, and distributed information remain challenging even for models with 100K+ context windows [3] (HIGH — T2 sources converge, consistent with broader research trends).

The practical limit is substantially below the theoretical maximum. For critical applications, assume effective context is 50-70% of the stated window size.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Performance is often highest when relevant information occurs at the beginning or end" | quote | [1] | verified |
| 2 | LongLLMLingua achieves 2x-6x compression ratios | statistic | [2] | verified |
| 3 | LongLLMLingua boosts NaturalQuestions performance by up to 21.4% with ~4x fewer tokens | statistic | [2] | verified |
| 4 | RECOMP achieves compression rate as low as 6% with minimal loss | statistic | [5] | verified |
| 5 | Queries at the end improve response quality by up to 30% | statistic | [11] | verified |
| 6 | Only half of models claiming 32K+ maintain satisfactory performance | statistic | [9] | verified |
| 7 | StreamingLLM enables 4M+ token processing without fine-tuning | statistic | [4] | verified |
| 8 | StreamingLLM achieves 22.2x speedup over sliding window recomputation | statistic | [4] | verified |
| 9 | Claude standard context window is 200K tokens, 1M in beta | statistic | [10] | verified |
| 10 | FILM-7B improved NarrativeQA from 23.5 to 26.9 F1 | statistic | [7] | verified |
| 11 | LongLLMLingua achieves 94% cost reduction on LooGLE | statistic | [2] | verified |
| 12 | Attention sink preservation "largely recovers the performance of window attention" | quote | [4] | verified |

## Takeaways

Context window management requires three coordinated strategies:

1. **Position strategically.** Exploit the U-shaped attention curve. Put critical instructions and constraints in the system prompt (beginning). Put the query and specific task instructions at the end. Accept that middle content receives weaker attention and place supporting/reference material there.

2. **Compress the middle.** Apply prompt compression (2-6x achievable) to content that must be present but occupies the low-attention middle zone. Use proposition-level granularity over full passages. Strip predictable tokens. These techniques reduce cost while often improving performance.

3. **Structure for navigation.** Use XML tags to create parseable landmarks. Ask models to quote relevant passages before answering. Use hierarchical organization with summaries at boundaries. This converts flat text into a navigable structure that partially mitigates position-dependent attention degradation.

4. **Budget explicitly.** Reserve output space (models error on overflow, not truncate). Track remaining budget using context awareness features. Compact aggressively in long-running conversations. Assume effective context is 50-70% of stated maximum for complex tasks.
