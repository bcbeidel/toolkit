---
name: "LLM Error Handling Fundamentals"
description: "Five ways error handling differs when the failing component is an LLM -- probabilistic failures, semantic detection, multiplicative compounding, prompt-based recovery, and per-attempt cost"
type: reference
sources:
  - https://stackoverflow.blog/2025/06/30/reliability-for-unreliable-llms/
  - https://arxiv.org/abs/2503.13657
  - https://www.sitepoint.com/error-handling-strategies-for-probabilistic-code-execution/
  - https://medium.com/@michael.hannecke/resilience-circuit-breakers-for-agentic-ai-cc7075101486
  - https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them
related:
  - docs/research/error-handling-agent-systems.md
  - docs/context/error-classification-agent-systems.md
  - docs/context/escalation-circuit-breakers.md
  - docs/context/validation-architecture.md
  - docs/context/llm-capabilities-limitations.md
---

Error handling for LLM-based agents requires fundamentally different assumptions than traditional software. The failing component is non-deterministic, failures often look like successes, and the same input can produce different failure modes across runs. Five differences change everything about how error handling systems should be designed.

## Five Key Differences

**1. Failures look like successes.** A hallucinated answer returns HTTP 200 with well-formed JSON. Error detection cannot rely on status codes or exception types alone. Every LLM output needs validation -- either deterministic (schema checks, type validation, assertion on expected fields) or probabilistic (LLM-as-judge, semantic similarity). This is the single biggest departure from traditional error handling, where failures announce themselves.

**2. Retries have value, but only with mutation.** Non-determinism means a retry might succeed where deterministic code would fail identically. However, bare retries -- repeating the same prompt unchanged -- are nearly as useless as retrying a deterministic bug. What makes LLM retries effective is context mutation: feeding the error message, traceback, and previous output back into the prompt so the model generates a corrected approach. The pattern is "observe, classify, mutate, bound."

**3. Errors compound multiplicatively.** A dialog system with four classifiers at 95% reliability produces .95^4 = 81.4% pipeline reliability. Each additional LLM step in an agent pipeline multiplies failure probability. A five-step agent pipeline where each step is 90% reliable yields only 59% end-to-end reliability. Error handling must account for this compounding, not just individual step reliability. Validation checkpoints between pipeline stages catch cascading errors before they compound further.

**4. Recovery means changing the prompt, not the code.** Traditional software fixes bugs by modifying source code and redeploying. LLM agent recovery means mutating context, adjusting prompts, switching models, or reducing capability scope. The "fix" is often architectural -- adding a validation step, decomposing into smaller tasks, or constraining the output format -- rather than changing a line of code.

**5. Cost is per-attempt.** Every retry, fallback evaluation, and circuit breaker probe costs tokens with direct monetary cost. A reliability architecture with 3 retries, context mutation, and LLM-as-judge validation may spend 5-10x the tokens of a single attempt. Error handling must be budget-aware: set explicit token budgets per task, track spend across retry attempts, and escalate to cheaper strategies (or humans) when the budget is exhausted.

## The Control Loop Architecture

Reliable LLM systems are built as pipelines with three components: a **generation step** (produce candidate output), an **evaluation step** (assess the output for correctness), and a **routing layer** (accept, reject, or retry based on evaluation). This is not optional architecture -- it is the minimum viable reliability pattern. Systems that skip evaluation and route LLM output directly to downstream consumers inherit the full compounding error rate.

The evaluation step itself can fail. Deterministic evaluation (schema validation, type checks, assertion tests) is cheap and reliable but catches only structural errors. Probabilistic evaluation (LLM-as-judge, semantic checks) catches semantic errors but adds its own failure probability to the pipeline. The practical approach combines both: deterministic checks first as a filter, probabilistic checks only for outputs that pass structural validation.

## The Graceful Degradation Ladder

When full capability fails, agents should step down through decreasing levels of capability rather than failing outright:

1. **Full capability** -- primary model with all tools and full reasoning
2. **Reduced reasoning** -- simpler/faster model, full tool access
3. **Reduced tools** -- primary model, limited tool access
4. **Cached/templated responses** -- no LLM, deterministic fallback
5. **Human handoff** -- structured context transfer to a human operator
6. **Graceful failure** -- structured error report, no output attempted

Each step down trades capability for reliability. The system should descend the ladder automatically based on failure type and budget remaining, not require manual intervention at each level.
