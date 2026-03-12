---
name: "Show Your Work Patterns for Agent Systems"
description: "Four patterns that make agent reasoning inspectable: search protocol recording, checkpoint annotations, flight recorders, and ReAct reasoning traces"
type: reference
sources:
  - https://github.com/agentkitai/agentlens
  - https://blog.langchain.com/debugging-deep-agents-with-langsmith/
  - https://langfuse.com/docs/observability/overview
  - https://arxiv.org/html/2508.02866v2
  - https://allen.hutchison.org/2026/02/17/the-observability-gap/
related:
  - docs/research/observability-audit-trails.md
  - docs/context/agent-observability-tracing.md
  - docs/context/observability-trust-debuggability.md
  - docs/context/feedback-loop-design.md
  - docs/context/research-methodology.md
---

Agent systems need more than metrics and traces. They need inspectable records of reasoning -- what the agent searched for, what it decided, and why. Four patterns address this, each at a different granularity.

## Search Protocol Recording

Log every search query, source, date range, results found, and results used. This creates an auditable record of information gathering that directly supports provenance: each entry documents what was looked for, where, and what was selected.

WOS implements this pattern in its research skill with structured JSON protocols embedded in document comments. The pattern generalizes: any agent that retrieves information should record its retrieval strategy, not just its results. This is cheap to implement and high-value for post-hoc analysis, enabling questions like "did the agent look in the right places?" and "what did it ignore?"

## Checkpoint Annotations

Mark decision points in long-running workflows: draft produced, review requested, approval received, phase gate passed. LangSmith implements this for regulated workflows with draft-review-publish decision points. LangGraph uses state checkpointing with persistence backends so multi-step workflows survive infrastructure failures.

For plugin-style agent systems, phase transitions already function as natural checkpoints. Annotating these transitions in traces (phase entry, gate condition, pass/fail) creates a high-level summary of agent progress readable without inspecting the full execution trace. The value is compression: a 200-span trace becomes a 5-checkpoint narrative.

## Flight Recorder Pattern

Borrowed from aviation black boxes: continuously capture every LLM call, tool invocation, approval decision, and error with low overhead. The recording is inspected after the fact, not during execution.

AgentLens exemplifies this as an MCP server that organizes events into sessions with metadata (agent ID, timestamps, duration, status). It adds tamper-evident properties through append-only storage with SHA-256 hash chains per session, where each event references the previous event's hash to detect post-hoc modification.

The flight recorder works best when capture is always on but lightweight -- structure and metadata only, with content capture (full prompts and completions) activated on-demand for specific debugging sessions.

## ReAct Reasoning Traces

The ReAct pattern (Reasoning and Acting) generates explicit Thought-Action-Observation traces at each step. The agent records its reasoning (Thought), the action it takes (Action), and what it observes (Observation). This cycle repeats until task completion.

Multiple observability tools (LangSmith, Langfuse, Arize Phoenix) render these traces as visual trees. The pattern's value is that it externalizes the agent's chain of thought into a structured, inspectable artifact rather than leaving reasoning implicit in the gap between tool calls.

## When to Use Each

**Search protocol recording** suits information-gathering workflows where retrieval quality matters. **Checkpoint annotations** suit multi-phase workflows with clear gate conditions. **Flight recorders** suit production systems that need post-incident debugging. **ReAct traces** suit complex reasoning tasks where understanding the decision path is as important as the outcome. Most production agent systems benefit from combining at least two of these patterns.
