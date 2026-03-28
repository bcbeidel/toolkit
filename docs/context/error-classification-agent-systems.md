---
name: "Error Classification for Agent Systems"
description: "Two-axis failure taxonomy (retryability x origin phase) and structured failure reporting for LLM-based agents, where failures are probabilistic and may look like successes"
metadata:
  type: reference
  sources:
    - https://arxiv.org/abs/2508.07935
    - https://arxiv.org/abs/2503.13657
    - https://galileo.ai/blog/agent-failure-modes-guide
    - https://www.sitepoint.com/error-handling-strategies-for-probabilistic-code-execution/
  related:
    - docs/research/error-handling-agent-systems.md
    - docs/context/escalation-circuit-breakers.md
    - docs/context/llm-error-handling-fundamentals.md
    - docs/context/validation-architecture.md
---

Traditional exception hierarchies assume deterministic failures with static types. Agent systems need a taxonomy that captures two orthogonal dimensions: whether the failure can be retried and where it originated. This two-axis model draws from SHIELDA's 36-type taxonomy and MAST's 14 failure modes, distilling them into a practical classification scheme.

## Two-Axis Taxonomy

**Retryability axis** -- can this succeed on retry?

- **Transient**: Likely succeeds on immediate retry. Rate limits (429), timeouts, transient API errors (503). Bare retry with backoff is sufficient.
- **Correctable**: Succeeds with a modified approach. Parsing errors, schema mismatches, context insufficiency. Requires context mutation -- feeding error information back into the prompt -- not just repetition.
- **Structural**: Cannot succeed without design changes. Missing capabilities, protocol mismatches, specification gaps, fundamental task impossibility. Retrying wastes budget.

**Origin phase axis** -- where did the failure originate?

- **Reasoning**: Goal misinterpretation, flawed planning, incorrect task decomposition.
- **Execution**: Tool failures, API errors, state corruption.
- **Verification**: Incorrect self-assessment, premature termination, infinite loops.

The critical insight: execution-phase errors often have reasoning-phase root causes. An agent that repeatedly fails at a tool call may have a flawed plan, not a tool problem. Tracing errors back to their originating phase prevents wasted retries on symptoms.

## Structured Failure Reporting

Failure reports should capture the full error lifecycle, not just the terminal state. Minimum fields:

- **Error classification**: Taxonomy category from the two axes above
- **Affected artifacts**: Which agent components were impacted (memory, plan, tool call, output)
- **Attempt history**: Each attempt's strategy (direct, context mutation, fallback), outcome, and token spend
- **Escalation path taken**: The sequence of recovery strategies attempted
- **Resolution**: Resolved, escalated, or terminal failure
- **Total cost**: Tokens, API calls, wall time across all attempts

Every agent execution should be instrumented with spans. Errors are classified dynamically against the taxonomy at runtime rather than mapped to static exception types. Retry history is preserved -- each attempt's input, output, and mutation is recorded. Cost accounting happens at every level because each retry has monetary cost.

## When to Use Which Axis

The retryability axis drives immediate recovery decisions: transient errors retry, correctable errors mutate, structural errors escalate. The origin phase axis drives root cause analysis: repeated execution failures should prompt inspection of the reasoning phase that produced the failing plan. Both axes together determine the structured report -- a correctable execution error gets different handling than a structural reasoning error.
