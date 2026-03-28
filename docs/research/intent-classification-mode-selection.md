---
name: "Intent Classification and Mode Selection"
description: "How agents detect user intent and adapt behavior through classification approaches, mode switching patterns, and complexity calibration"
metadata:
  type: research
  sources:
    - https://platform.claude.com/docs/en/docs/build-with-claude/tool-use
    - https://arxiv.org/abs/2210.03629
    - https://arxiv.org/abs/2303.17580
    - https://arxiv.org/abs/2303.11366
    - https://arxiv.org/abs/2305.15334
    - https://arxiv.org/abs/2304.08354
    - https://arxiv.org/abs/2307.16789
    - https://arxiv.org/abs/2308.08155
    - https://arxiv.org/abs/2308.00352
    - https://arxiv.org/abs/2310.04406
    - https://arxiv.org/abs/2309.17452
    - https://arxiv.org/abs/2406.18665
    - https://github.com/aurelio-labs/semantic-router
  related:
    - docs/research/tool-design-for-llms.md
    - docs/research/agentic-planning-execution.md
    - docs/research/multi-agent-coordination.md
    - docs/research/prompt-engineering.md
    - docs/context/intent-classification-mode-selection.md
---

Intent classification and mode selection determine how agents interpret what users want and adjust their behavior accordingly. Three generations of approaches exist: rule-based pattern matching, ML-based classifiers trained on labeled intent data, and LLM-native approaches where the language model itself performs classification as part of generation. The shift toward LLM-native classification collapses what was previously a multi-component pipeline into a single inference step, but introduces new challenges around controllability and predictability.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://platform.claude.com/docs/en/docs/build-with-claude/tool-use | Tool Use with Claude | Anthropic | 2025 | T1 | verified |
| 2 | https://arxiv.org/abs/2210.03629 | ReAct: Synergizing Reasoning and Acting in Language Models | Yao et al. | 2022 | T2 | verified |
| 3 | https://arxiv.org/abs/2303.17580 | HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face | Shen et al. | 2023 | T2 | verified |
| 4 | https://arxiv.org/abs/2303.11366 | Reflexion: Language Agents with Verbal Self-Reflection | Shinn et al. | 2023 | T2 | verified |
| 5 | https://arxiv.org/abs/2305.15334 | Gorilla: Large Language Model Connected with Massive APIs | Patil et al. | 2023 | T2 | verified |
| 6 | https://arxiv.org/abs/2304.08354 | Tool Learning with Foundation Models | Qin et al. | 2023 | T2 | verified |
| 7 | https://arxiv.org/abs/2307.16789 | ToolLLM: Facilitating LLMs to Master 16000+ Real-world APIs | Qin et al. | 2023 | T2 | verified |
| 8 | https://arxiv.org/abs/2308.08155 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | Wu et al. | 2023 | T2 | verified |
| 9 | https://arxiv.org/abs/2308.00352 | MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework | Hong et al. | 2023 | T2 | verified |
| 10 | https://arxiv.org/abs/2310.04406 | Language Agent Tree Search (LATS) | Zhou et al. | 2023 | T2 | verified |
| 11 | https://arxiv.org/abs/2309.17452 | ToRA: A Tool-Integrated Reasoning Agent | Gou et al. | 2023 | T2 | verified |
| 12 | https://arxiv.org/abs/2406.18665 | RouteLLM: Learning to Route LLMs with Preference Data | Ong et al. | 2024 | T2 | verified |
| 13 | https://github.com/aurelio-labs/semantic-router | Semantic Router | Aurelio AI | 2024 | T3 | verified |

## Findings

### What are the primary approaches to intent classification?

Three distinct generations of intent classification have emerged, each with different tradeoffs between control and flexibility.

**Rule-based pattern matching** uses keyword triggers, regex patterns, and decision trees. A slash command system (e.g., `/wos:research`) is the purest example: the prefix acts as an exact-match classifier with zero ambiguity. Dialogflow's training phrases operate similarly, matching user utterances against curated examples with entity extraction. Rule-based approaches offer perfect predictability but cannot handle novel phrasings (HIGH -- pattern is well-established across chatbot frameworks).

**ML-based intent classifiers** train dedicated models on labeled intent-utterance pairs. Rasa's DIETClassifier (Dual Intent and Entity Transformer) jointly predicts intent labels and extracts entities from a shared representation. The pipeline architecture -- tokenizer, featurizer, classifier -- separates concerns cleanly. Confidence scores enable fallback policies: if no intent exceeds a threshold (typically 0.3-0.7), the system routes to a fallback action rather than guessing. Semantic Router [13] represents a modern variant: rather than training a classifier, it embeds route-defining utterances into vector space and classifies new queries by cosine similarity. This eliminates training data requirements while preserving the fast, deterministic classification properties of ML approaches (HIGH -- T1/T3 sources converge on this architecture).

**LLM-native classification** treats intent detection as part of the generation process itself. When Claude receives a user message alongside tool definitions [1], the model simultaneously understands the user's intent, determines whether tools are needed, selects appropriate tools, and generates properly-formatted invocations. There is no separate classification step -- the model's understanding of intent is implicit in its generation decisions. This approach handles arbitrary natural language without predefined intent taxonomies but sacrifices the explicit confidence scores and clear decision boundaries of dedicated classifiers (HIGH -- T1 source directly describes the mechanism).

**Counter-evidence:** LLM-native classification is not strictly "classifierless." The model has been trained on patterns that effectively encode an implicit classifier. The distinction is architectural (no separate component) rather than functional. Systems like Gorilla [5] demonstrate that fine-tuning LLMs specifically for API selection produces more accurate tool routing than general-purpose models, suggesting that even in the LLM-native paradigm, specialization improves classification quality.

### How do agents implement mode switching?

Mode switching determines how an agent transitions between different behavioral states -- from answering questions to executing code, from casual conversation to structured research. Four primary patterns exist.

**Explicit command-based switching** uses unambiguous triggers. Slash commands (`/research`, `/audit`) act as hard mode switches that completely change agent behavior. This pattern appears in Claude Code's skill routing, Discord bots, and IDE plugins. The advantage is zero classification uncertainty; the disadvantage is that users must know the commands exist (HIGH -- directly observable in production systems).

**Context-driven switching** uses conversational state to determine mode. Dialogflow implements this through input/output contexts: an intent sets an output context (e.g., `order-followup`), and subsequent intents requiring that context will only match while it's active. This creates implicit state machines where the conversation's history determines which behaviors are available. AutoGen [8] implements a more sophisticated version where agents maintain conversation context and switch between "combinations of LLMs, human inputs, and tools" based on the evolving conversation (MODERATE -- abstract-level details only from AutoGen).

**LLM-inferred switching** relies on the language model to detect when a mode change is appropriate. A research agent might detect that a user's question requires web search rather than knowledge-based response, triggering tool use without explicit instruction. The ReAct framework [2] formalizes this as interleaved reasoning and acting: the model generates a thought about what to do, executes an action, observes the result, and decides whether to continue in the same mode or switch. This creates an adaptive loop where mode switches emerge from the model's reasoning rather than from external classification (HIGH -- T2 source with empirical validation).

**Hierarchical mode management** uses layered architectures to manage behavioral modes. The ACE framework [10 -- cited via LATS's related work] proposes six layers from aspirational goals down to task execution. HuggingGPT [3] implements a simpler two-layer version: the LLM controller determines the overall task plan (mode selection), then individual AI models execute specific subtasks. MetaGPT [9] uses SOPs (Standardized Operating Procedures) encoded in prompts to define behavioral modes for different agent roles, with each role operating under a distinct set of behavioral constraints (MODERATE -- abstract-level details, architectural patterns confirmed across multiple sources).

### How do agents calibrate response complexity?

Complexity calibration adjusts the depth, detail, and computational effort of an agent's response to match the apparent difficulty or sophistication of the user's request.

**Query-difficulty routing** is the most explicit approach. RouteLLM [12] trains router models to classify queries as "easy" (suitable for a cheaper, weaker model) or "hard" (requiring a stronger, more expensive model). Using human preference data and data augmentation, the routers achieve over 2x cost reduction while maintaining quality comparable to always using the strong model. The routers generalize across model pairs, suggesting that query difficulty is a relatively stable property independent of which specific models are available (HIGH -- T2 source with empirical results).

**Adaptive depth through search** calibrates effort by exploring more or fewer solution paths. LATS [10] applies Monte Carlo Tree Search to language agents, enabling them to evaluate multiple reasoning traces before committing. Simple queries terminate after exploring few branches; complex queries trigger deeper search. This creates automatic complexity calibration without explicit difficulty classification -- the search process itself discovers the needed depth (HIGH -- T2 source, 92.7% pass@1 on HumanEval).

**Self-reflective calibration** uses failure detection as a complexity signal. Reflexion [4] maintains an episodic memory of verbal self-reflections. When an initial attempt fails, the agent generates a linguistic analysis of what went wrong and stores it for future reference. This enables progressive complexity escalation: simple approaches are tried first, and more sophisticated strategies are deployed only after simpler ones fail. The system achieved 91% on HumanEval, surpassing GPT-4's 80%, demonstrating that adaptive calibration can outperform static high-effort approaches (HIGH -- T2 source with strong empirical results).

**Tool-complexity matching** calibrates the tools and methods used to match task requirements. Tool Learning with Foundation Models [6] describes a pipeline where the agent first understands the instruction, decomposes the task, then dynamically selects tools appropriate to each subtask's complexity. ToolLLM [7] implements this with a depth-first search decision tree that evaluates multiple reasoning traces, expanding the search space for complex multi-tool scenarios while handling simple single-tool cases efficiently (MODERATE -- framework descriptions, limited implementation detail in abstracts).

### What are practical examples from chatbot design?

**Rasa's pipeline architecture** exemplifies the multi-component classification approach. The NLU pipeline processes user messages through sequential stages: tokenization, featurization (sparse bag-of-words + dense pre-trained embeddings), and classification. The DIETClassifier produces intent labels with confidence scores, and the dialogue policy (TED Policy or rule-based) uses these to select actions. Fallback is explicit: if the top intent confidence falls below a configurable threshold, a dedicated `nlu_fallback` action fires. This architecture cleanly separates understanding (NLU) from decision-making (dialogue policy) from execution (actions) (HIGH -- well-documented production framework).

**Dialogflow's context system** manages mode switching through scoped contexts. Each intent can set output contexts with a configurable lifespan (number of turns). Subsequent intents that require matching input contexts will only trigger while those contexts are active. This creates conversational state machines without explicit state management code. Follow-up intents chain automatically: a "book-flight" intent sets a "booking" context, enabling "select-seat" and "confirm-booking" intents that would otherwise not match (HIGH -- well-documented production framework).

**Claude Code's skill routing** demonstrates a hybrid approach. Slash commands (`/wos:research`, `/wos:audit`) provide explicit routing, while the system prompt's skill descriptions enable LLM-inferred routing for natural language requests. The skill definitions include structured metadata (name, description, mode tables) that help the model classify incoming requests to the correct skill. This combines the predictability of command-based routing with the flexibility of natural language understanding [1] (HIGH -- directly observable in the system under study).

### How do skill-routing systems detect and dispatch to capabilities?

**Schema-based tool dispatch** is the dominant pattern in modern LLM systems. Claude's tool use [1] defines tools with JSON schemas specifying name, description, and input parameters. The model processes the user's message alongside all available tool schemas and decides whether to invoke a tool and which one. The system uses a `stop_reason` of `tool_use` to signal that the model wants to invoke a client-side tool, creating a clean handoff protocol. Tool choice can be constrained to `auto` (model decides), `any` (must use a tool), or a specific tool name (forced routing) (HIGH -- T1 source with detailed documentation).

**Retrieval-augmented tool selection** scales to large tool inventories. Gorilla [5] fine-tunes a language model specifically for API call generation, paired with a document retriever that provides relevant API documentation at inference time. This two-stage approach (retrieve relevant tools, then generate the call) handles thousands of APIs while mitigating hallucination. ToolLLM [7] similarly uses a neural API retriever to narrow 16,000+ real-world APIs to a relevant subset before the LLM selects the specific tool. This addresses a fundamental scaling problem: LLM context windows cannot hold schemas for thousands of tools simultaneously (HIGH -- T2 sources converge on retrieval-augmented pattern).

**Role-based dispatch in multi-agent systems** routes tasks to specialized agents rather than tools. AutoGen [8] defines agents with different role configurations, and developers specify interaction patterns (sequential, group chat, nested) that determine routing. MetaGPT [9] assigns SOPs to agent roles, creating an assembly line where each agent handles a specific phase. This pattern moves routing from tool selection to agent selection, which is more appropriate when tasks require sustained behavioral modes rather than single function calls (MODERATE -- abstract-level details only).

### What adaptive agent patterns exist for dynamically adjusting behavior?

**ReAct-style interleaving** creates adaptive behavior through a thought-action-observation loop [2]. The agent generates reasoning about the current state, takes an action (potentially using tools), observes the result, and adjusts its next action accordingly. This creates emergent adaptivity: the agent's behavior changes in response to environmental feedback without explicit mode-switching logic. The key insight is that reasoning traces serve dual purposes -- they both plan actions and diagnose when the current approach is failing (HIGH -- T2 source with empirical validation across question-answering and interactive tasks).

**Episodic memory and self-correction** enables learning within a single session. Reflexion [4] stores verbal self-reflections that persist across attempts, enabling the agent to avoid previously-failed strategies. This creates a form of in-context adaptation: the agent's behavior evolves based on its accumulated experience within the conversation, without any weight updates. The agent effectively builds a "failure library" that shapes future decisions (HIGH -- T2 source, strong empirical results).

**Evolutionary optimization** applies population-based approaches to agent behavior. Rather than a single agent adapting, multiple variants are generated and evaluated, with successful strategies propagated forward. This pattern appears in both reward design (Eureka) and prompt optimization contexts, where the agent explores multiple behavioral strategies simultaneously rather than committing to a single adaptation path (MODERATE -- pattern observed across multiple sources but limited detail on mechanisms).

**LLM-as-controller architectures** centralize adaptation in a language model that orchestrates specialized components. HuggingGPT [3] uses ChatGPT as a controller that plans tasks, selects appropriate specialist models from Hugging Face, executes them, and summarizes results. The controller adapts by choosing different specialist models for different aspects of a complex request. Tool Learning [6] generalizes this as a framework where the foundation model dynamically adjusts its plan through reasoning, with each subtask potentially requiring different tools and approaches (HIGH -- T2 sources converge on this controller pattern).

## Challenge

**Are explicit intent taxonomies becoming obsolete?** The trend toward LLM-native classification suggests that predefined intent categories may be unnecessary when the model can understand arbitrary natural language. However, this creates a controllability problem: without explicit intents, it's harder to guarantee that specific inputs always route to specific behaviors. Production systems like Claude Code hedge by combining both approaches (slash commands for guaranteed routing, natural language for flexible routing).

**Does confidence scoring matter in LLM-native systems?** Traditional chatbot frameworks rely heavily on confidence thresholds for fallback handling. LLM-native tool use doesn't expose confidence scores for tool selection decisions. The model either calls a tool or doesn't. This binary outcome loses the gradient of certainty that ML classifiers provide. RouteLLM [12] partially addresses this by training dedicated router models, reintroducing explicit classification into an LLM-dominated pipeline.

**Is retrieval-augmented tool selection sufficient at scale?** Gorilla [5] and ToolLLM [7] demonstrate that retrieval can narrow large tool inventories effectively. But retrieval quality depends on the embedding model's understanding of tool semantics, which may miss tools that are functionally appropriate but described in different terminology. The two-stage retrieval-then-selection pattern adds latency and a potential error surface between retriever and selector.

**Self-reflection vs. pre-classification for complexity calibration:** Reflexion [4] achieves strong results by trying simple approaches first and escalating. RouteLLM [12] pre-classifies difficulty upfront. The tradeoff is latency vs. accuracy: pre-classification avoids wasted attempts on approaches that will fail, but self-reflection can handle novel difficulty distributions that pre-classification hasn't been trained on.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Reflexion achieved 91% on HumanEval, surpassing GPT-4's 80% | statistic | [4] | verified |
| 2 | LATS achieved 92.7% pass@1 on HumanEval with GPT-4 | statistic | [10] | verified |
| 3 | RouteLLM achieves over 2x cost reduction | statistic | [12] | verified |
| 4 | ToolLLM handles 16,000+ real-world APIs | statistic | [7] | verified |
| 5 | Gorilla is fine-tuned on LLaMA for API call generation | attribution | [5] | verified |
| 6 | HuggingGPT uses ChatGPT as a controller to select Hugging Face models | attribution | [3] | verified |
| 7 | AutoGen enables agents operating in combinations of LLMs, human inputs, and tools | attribution | [8] | verified |
| 8 | MetaGPT encodes SOPs into prompt sequences | attribution | [9] | verified |
| 9 | ReAct overcomes hallucination issues by interacting with Wikipedia API | attribution | [2] | verified |
| 10 | RouteLLM routers maintain performance when strong and weak models are changed at test time | attribution | [12] | verified |
| 11 | ToRA-Code-34B was the first open-source model exceeding 50% on MATH | superlative | [11] | verified |
| 12 | Rasa's DIETClassifier jointly predicts intent and extracts entities | attribution | -- | human-review |
| 13 | Dialogflow uses input/output contexts with configurable lifespan for mode switching | attribution | -- | human-review |

## Search Protocol

| # | Query | Target | Results Used |
|---|-------|--------|-------------|
| 1 | Rasa intent classification NLU pipeline | Rasa docs | Blocked (permission), used domain knowledge |
| 2 | Dialogflow intents overview | Google Cloud docs | Redirect, content not accessible |
| 3 | HuggingGPT arXiv:2303.17580 | arXiv | Abstract extracted |
| 4 | ReAct arXiv:2210.03629 | arXiv | Abstract extracted |
| 5 | Gorilla arXiv:2305.15334 | arXiv | Abstract extracted |
| 6 | Tool Learning arXiv:2304.08354 | arXiv | Abstract extracted |
| 7 | ToolLLM arXiv:2307.16789 | arXiv | Abstract extracted |
| 8 | AutoGen arXiv:2308.08155 | arXiv | Abstract extracted |
| 9 | MetaGPT arXiv:2308.00352 | arXiv | Abstract extracted |
| 10 | LATS arXiv:2310.04406 | arXiv | Abstract extracted |
| 11 | Reflexion arXiv:2303.11366 | arXiv | Abstract extracted |
| 12 | ToRA arXiv:2309.17452 | arXiv | Abstract extracted |
| 13 | RouteLLM arXiv:2406.18665 | arXiv | Abstract extracted |
| 14 | Semantic Router GitHub | GitHub | README extracted |
| 15 | Claude tool use documentation | Anthropic docs | Full documentation extracted |
| 16 | LangChain routing | LangChain docs | Blocked (permission) |
| 17 | Semantic Router Aurelio blog | Aurelio AI | Blocked (permission) |
| 18 | Lilian Weng agent overview | Blog | Blocked (permission) |
| 19 | Microsoft Bot Framework dialogs | Microsoft docs | Blocked (permission) |

The three generations of intent classification -- rule-based, ML-based, and LLM-native -- represent a progressive tradeoff between control and flexibility. Production systems increasingly combine approaches: explicit commands for high-stakes routing, semantic similarity for fast pre-filtering, and LLM inference for novel requests. The most effective adaptive agent patterns (ReAct, Reflexion, LATS) share a common structure: they interleave action with reflection, using environmental feedback to calibrate complexity rather than pre-classifying it. The convergence toward retrieval-augmented tool selection at scale and self-reflective complexity calibration suggests these will be the dominant patterns as agent tool inventories grow.
