# Context


Project context documents covering domain knowledge, patterns, and conventions.

| File | Description |
| --- | --- |
| [abstraction-level-design.md](abstraction-level-design.md) | "How calibrating abstraction altitude — WHAT/WHY vs. HOW — across specifications, plans, and instructions affects agent execution reliability, with empirical thresholds for the specificity-flexibility tradeoff" |
| [agent-state-persistence.md](agent-state-persistence.md) | "Architectural patterns for carrying agent knowledge across session boundaries: file-based, checkpoint-based, and database-backed persistence with tradeoffs" |
| [agentic-planning-execution.md](agentic-planning-execution.md) | "Three dominant paradigms for LLM agent planning — ReAct, Plan-and-Execute, and Tree-of-Thought — with trade-offs for decomposition, failure recovery, and session persistence" |
| [context-engineering.md](context-engineering.md) | "The discipline of structuring, storing, and surfacing project knowledge so LLMs consume it effectively — document models, indexing strategies, and the curation hierarchy" |
| [context-window-management.md](context-window-management.md) | "Strategies for maximizing LLM performance within token limits: position-aware formatting, compression, structured markup, and budget allocation" |
| [feedback-loop-design.md](feedback-loop-design.md) | "Structured feedback formats, the supersede-don't-edit pattern, and operationalization mechanisms that close the loop between execution and design so systems improve through use" |
| [human-in-the-loop-design.md](human-in-the-loop-design.md) | "When AI agents should gate on human approval vs. act autonomously, based on reversibility, confidence, and trust calibration research" |
| [information-architecture.md](information-architecture.md) | "Structural patterns for organizing knowledge that LLM agents can navigate efficiently: shallow hierarchy, metadata-first discovery, index files, and faceted classification through frontmatter" |
| [intent-classification-mode-selection.md](intent-classification-mode-selection.md) | "Three generations of intent classification (rule-based, ML-based, LLM-native), four mode-switching patterns, and complexity calibration strategies that production agents combine into hybrid routing architectures" |
| [knowledge-synthesis-distillation.md](knowledge-synthesis-distillation.md) | "How to compress raw research into focused, actionable context: purpose-driven compression, structured preservation, provenance separation, and practical keep/discard heuristics" |
| [llm-capabilities-limitations.md](llm-capabilities-limitations.md) | "What LLMs do reliably vs. where they fail, and six architectural principles for agent design" |
| [multi-agent-coordination.md](multi-agent-coordination.md) | "Dispatch, context sharing, conflict prevention, and isolation patterns that have converged across major LLM agent frameworks (2024-2026)" |
| [principle-engineering.md](principle-engineering.md) | "Methods for classifying, verifying, and maintaining design principles as living documents — taxonomy dimensions, fitness functions, drift detection, instruction density limits, and governance lifecycles" |
| [prompt-engineering.md](prompt-engineering.md) | "Practical patterns for writing reliable system-level LLM instructions: layered structure, selective specification, few-shot examples, and anti-pattern avoidance" |
| [research-methodology.md](research-methodology.md) | "Layered evaluation, breadth-before-depth discovery, disagreement-as-signal, and three-layer confidence — convergent principles from academic, intelligence, and agent-driven research traditions" |
| [source-evaluation-claim-verification.md](source-evaluation-claim-verification.md) | "SIFT framework, source tier hierarchies, claim verification types, and Chain-of-Verification composed into a verification pipeline for LLM-assisted research" |
| [structured-thinking-decision-frameworks.md](structured-thinking-decision-frameworks.md) | "How to convert classical mental models into executable agent procedures — trigger conditions, structured steps, verification criteria, and the reasoning substrate that makes them work" |
| [tool-design-for-llms.md](tool-design-for-llms.md) | "How to design tool interfaces that LLM agents can select, invoke, and recover from reliably: schemas, descriptions, error signaling, idempotency, and scaling" |
| [workflow-orchestration.md](workflow-orchestration.md) | "State machine models, durable execution engines, phase gates, and resumability patterns for managing multi-phase agent workflows — from FSMs to Temporal and LangGraph" |
| [writing-for-llm-consumption.md](writing-for-llm-consumption.md) | "Six structural principles for agent-facing documentation: BLUF positioning, explicit conventions, self-contained sections, navigable metadata, consistent formatting, and token efficiency" |
