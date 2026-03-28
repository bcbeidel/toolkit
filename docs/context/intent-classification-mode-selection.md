---
name: "Intent Classification and Mode Selection"
description: "Three generations of intent classification (rule-based, ML-based, LLM-native), four mode-switching patterns, and complexity calibration strategies that production agents combine into hybrid routing architectures"
metadata:
  type: reference
  sources:
    - https://platform.claude.com/docs/en/docs/build-with-claude/tool-use
    - https://arxiv.org/abs/2210.03629
    - https://arxiv.org/abs/2303.11366
    - https://arxiv.org/abs/2406.18665
    - https://arxiv.org/abs/2305.15334
    - https://arxiv.org/abs/2307.16789
  related:
    - docs/research/intent-classification-mode-selection.md
    - docs/context/tool-design-for-llms.md
    - docs/context/agentic-planning-execution.md
    - docs/context/multi-agent-coordination.md
---

Production agents must solve three interrelated problems: classifying what the user wants, switching into the right behavioral mode, and calibrating response complexity. The dominant pattern is hybrid routing -- combining explicit commands for predictable dispatch with LLM-native classification for flexible natural language handling.

## Three Generations of Intent Classification

**Rule-based pattern matching** uses keywords, regex, and exact triggers. Slash commands (e.g., `/research`) are the purest form: zero ambiguity, zero flexibility. This approach offers perfect predictability but cannot handle novel phrasings.

**ML-based classifiers** train on labeled intent-utterance pairs. Rasa's DIETClassifier jointly predicts intents and extracts entities, producing confidence scores that enable explicit fallback policies when no intent exceeds a threshold. Semantic Router represents a modern variant that embeds route-defining utterances into vector space, classifying by cosine similarity without training data. Both preserve fast, deterministic classification.

**LLM-native classification** treats intent detection as part of generation itself. When a model receives a message alongside tool definitions, it simultaneously understands intent, selects tools, and generates invocations -- no separate classification step. This handles arbitrary language without predefined taxonomies but sacrifices explicit confidence scores and clear decision boundaries. Fine-tuning for specific APIs (as Gorilla demonstrates) improves accuracy even within this paradigm.

## Mode-Switching Patterns

Four patterns govern how agents transition between behavioral states:

1. **Command-based switching** -- slash commands and explicit triggers provide zero-ambiguity mode changes. Users must know commands exist, but routing is guaranteed correct.

2. **Context-driven switching** -- conversational state determines available behaviors. Dialogflow's input/output context system creates implicit state machines where conversation history controls which intents can match.

3. **LLM-inferred switching** -- the model detects when mode changes are appropriate through reasoning. ReAct formalizes this as interleaved thought-action-observation loops where mode switches emerge from the model's reasoning rather than external classification.

4. **Hierarchical management** -- layered architectures where a controller (often an LLM) orchestrates specialized components. HuggingGPT uses this pattern: an LLM controller plans tasks, selects specialist models, executes them, and synthesizes results.

## Complexity Calibration

Agents adjust response depth through four mechanisms:

**Pre-classification routing** (RouteLLM) trains router models on preference data to classify queries as easy or hard, achieving 2x cost reduction while maintaining quality. Routers generalize across model pairs, suggesting query difficulty is a stable property.

**Adaptive search depth** (LATS) applies Monte Carlo Tree Search to explore more branches for harder problems. Complexity calibration happens automatically -- the search process discovers the needed depth without explicit difficulty classification.

**Self-reflective escalation** (Reflexion) tries simple approaches first, stores verbal self-reflections on failure, and escalates to more sophisticated strategies. This outperformed static high-effort approaches, achieving 91% on HumanEval versus GPT-4's 80%.

**Retrieval-augmented tool selection** (Gorilla, ToolLLM) solves the scaling problem: retrieve relevant tools from large inventories first, then let the LLM select from the narrowed set. This two-stage pattern handles 16,000+ APIs where context windows cannot hold all schemas simultaneously.

## The Hybrid Convergence

Production systems combine approaches rather than choosing one. Claude Code exemplifies this: slash commands provide guaranteed routing for known operations, while skill descriptions in the system prompt enable LLM-inferred routing for natural language requests. The open question is whether explicit intent taxonomies are becoming obsolete -- LLM-native classification handles arbitrary input, but sacrifices the controllability and auditability that explicit classification provides. The most resilient architectures hedge by layering both.
