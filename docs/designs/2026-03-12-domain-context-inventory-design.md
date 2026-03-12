---
name: Domain Context Inventory
description: Exhaustive inventory of 36 knowledge domains required to build WOS from scratch, organized into 10 categories.
type: design
status: draft
related:
  - docs/prompts/domain-context-pipeline.md
---

## Purpose

Identify every knowledge domain needed to effectively design and build a
system like WOS — a Claude Code plugin for structured project context. This
inventory drives a research-distill pipeline that produces context files for
each domain, enabling systematic codebase review and improvement.

## Framing

The question isn't "what does the code do" but "what do you need to know to
build this." Domains represent areas of expertise, not code modules.

## Domain Inventory

### LLM Foundations

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 1 | LLM Capabilities & Limitations | What LLMs can do reliably vs. what they can't — hallucination patterns, attention decay, reasoning failure modes. | Every design decision is shaped by what you can and can't trust an LLM to do. The code/skill boundary, BLUF formatting, 500-line limits all stem from this. |
| 2 | Prompt Engineering | Writing instructions that produce reliable LLM behavior — constraint specification, output formatting, anti-pattern guards, calibrating specificity vs. flexibility. | Skills are system-level prompts. The difference between 60% and 95% reliability is prompt craft. |
| 3 | Context Window Management | Token budgets, inclusion/exclusion strategies, compression, structuring content so important information survives context limits. | The entire document model (200-800 words, one concept per file, frontmatter-first, BLUF) is a context window management strategy. |

### Agent Architecture

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 4 | Agentic Planning & Execution | How agents decompose goals into tasks, sequence work, track progress via artifacts, handle failures, and resume across sessions. | The delivery pipeline. Getting task granularity, state persistence, and recovery wrong makes multi-step execution unreliable. |
| 5 | Multi-Agent Coordination | Parallel dispatch, context sharing, conflict detection (file overlap), scoping agent work to avoid interference. | Execute-plan dispatches parallel subagents. Without coordination, agents overwrite each other's work. |
| 6 | Tool Design for LLMs | What makes a good tool interface — input/output contracts, error signaling, idempotency, how tool design affects agent reasoning. | Every script is a tool. Poorly designed interfaces cause agents to misuse them or misinterpret results. |
| 7 | Agent State & Persistence | How agents maintain context across sessions when conversation history is lost — disk-as-truth, checkpoint annotations, artifact-based resumption. | Multi-session execution depends on plan files and git history as state, not conversation memory. |

### Knowledge Engineering

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 8 | Information Architecture | How to organize knowledge for retrieval — taxonomy design, flat vs. hierarchical structures, navigation patterns, discoverability. | The docs/ structure, _index.md system, and AGENTS.md navigation are information architecture. Wrong choices mean agents can't find what they need. |
| 9 | Context Engineering | How to structure, store, and surface project knowledge so LLMs can consume it effectively — document models, frontmatter, indexing, attention-aware formatting. | This is the core problem WOS solves. Every other domain serves this one. |
| 10 | Research Methodology | Systematic information gathering — source discovery, evaluation frameworks, cross-referencing, confidence assessment. | The research skill is complex because research is genuinely hard. Verification quality determines knowledge base trustworthiness. |
| 11 | Source Evaluation & Claim Verification | SIFT framework, six-tier source hierarchy (T1-T6), claim verification types, Chain-of-Verification to prevent confirmation bias. | Bad source evaluation poisons the entire knowledge pipeline. This goes beyond generic research methodology into specific techniques. |
| 12 | Knowledge Synthesis & Distillation | Compressing raw research into focused, actionable context — what to keep, what to discard, preserving provenance while reducing volume. | Bad distillation loses critical nuance or buries it in noise. |
| 13 | Writing for LLM Consumption | How agent-facing docs differ from human-facing — BLUF structure, explicit over implicit, self-contained sections, navigable metadata. | Documents are primarily consumed by agents. Human-optimized patterns actively hurt agent comprehension. |

### Workflow & Orchestration

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 14 | Workflow Orchestration | State machines for multi-phase processes — lifecycle management, phase gates, transition rules, resumable and auditable workflows. | Without formal state management, workflows break silently or skip critical steps. |
| 15 | Human-in-the-Loop Design | When to gate on user approval vs. automate, how to present decisions, trust calibration, cost/benefit of autonomy. | WOS deliberately chooses explicit handoffs. Understanding when autonomy helps vs. when it's dangerous is a design skill. |
| 16 | Feedback Loop Design | Capturing what works and what doesn't, closing the loop between execution and design, operationalizing learnings. | Without feedback loops, the system can't improve. Infeasibility feedback and retrospectives are examples. |
| 17 | Intent Classification & Mode Selection | Detecting user intent and adapting behavior — research modes, complexity calibration, plan-mode vs. ad-hoc switching. | Skills must classify the situation and select the right operating mode before doing anything. |

### Decision & Principles

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 18 | Structured Thinking & Decision Frameworks | Mental models (first principles, inversion, Eisenhower, Pareto) and how to operationalize them as agent-usable tools. | Making frameworks useful to an LLM — not just listing them — requires understanding both the models and agent reasoning. |
| 19 | Principle Engineering | Extracting, classifying, and maintaining design principles — five-criteria filter, verification criteria, drift detection, density-performance correlation. | Distinct from applying frameworks. Creating and maintaining the decision frameworks themselves. |
| 20 | Abstraction Level Design | Choosing the right altitude for each artifact — specs (WHAT/WHY), plans (middle altitude), research (mode intensity), instructions (specificity calibration). | The meta-skill of matching detail level to artifact purpose. A design skill, not a writing skill. |

### Software Design

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 21 | Convention-Driven Design | Establishing implicit contracts (naming, layout, metadata) that agents discover and follow without configuration. Derive from disk, never hand-curate. | The alternative is configuration schemas, which add complexity and drift. |
| 22 | Plugin & Extension Architecture | How host systems discover, load, and invoke plugins — registration, script execution, sandboxing, version management. | You can't build the tool without understanding the platform. |
| 23 | Validation Architecture | Separating deterministic structure checks from heuristic quality assessment, severity models, what to validate at which layer. | The code/LLM judgment boundary is load-bearing. Getting it wrong produces brittle enforcement or no guardrails. |
| 24 | Idempotency & Convergent Operations | Designing operations safe to run repeatedly — init, reindex, audit converge to correct state regardless of starting state. | Non-idempotent operations in agent systems cause cascading failures on retry. |

### Developer Experience

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 25 | Onboarding & Progressive Disclosure | Layering complexity for different contexts — empty-repo first-run vs. mature project, guiding first actions without overwhelming. | Init's guided onboarding and brainstorm-plan-execute progression are progressive disclosure. |
| 26 | Git Workflow Integration | Commits as rollback boundaries, branch naming, PR automation, making agent-driven development compatible with team workflows. | Agents producing unstructured git history are unusable in team contexts. |
| 27 | CLI Design | Argument patterns, output formatting (human vs. JSON), exit codes, making scripts usable by both humans and agents. | Every script serves two audiences. Bad CLI design means agents can't parse output or humans can't debug. |
| 28 | Issue Tracking & External System Integration | Filing issues (templates, deduplication), session anonymization, gh CLI integration, closing loops with external systems. | How WOS communicates with the outside world. |

### Quality & Reliability

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 29 | Testing Non-Deterministic Systems | Testing agent-driven workflows — behavioral testing, structural assertions, testing deterministic and LLM layers independently. | The code layer tests deterministically; skill behavior needs different strategies. |
| 30 | Error Handling in Agent Systems | Escalation thresholds, structured failure reporting, distinguishing retryable errors from design-level blockers. | Traditional try/catch doesn't work when the "code" is an LLM. |
| 31 | Observability & Audit Trails | Making agent activity inspectable — search protocol logging, SHA annotations, plan checkpoints, "show your work." | When an agent makes a bad decision, you need to trace why. |

### Platforms & Portability

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 32 | Agent Framework Landscape | How agent frameworks (LangChain, CrewAI, AutoGen, Semantic Kernel, DSPy, etc.) handle tool registration, memory, planning, and orchestration. Universal patterns vs. framework-specific abstractions. | Reveals which WOS patterns are genuinely portable and which accidentally couple to a specific framework's assumptions. |
| 33 | AI Coding Assistant Conventions | How AI coding tools (Claude Code, GitHub Copilot, Cursor, Windsurf, Codex CLI, Cline, Aider) handle project context, instruction files (CLAUDE.md, .cursorrules, .github/copilot-instructions.md, AGENTS.md), tool invocation, and skill/command systems. | WOS currently targets Claude Code. Understanding how other coding assistants discover and consume context reveals what's portable and what needs abstraction layers. |
| 34 | Cross-Model Prompt Portability | How instruction styles, formatting preferences, and reasoning patterns differ across model families — Claude (XML tags), GPT/Codex (Markdown, system messages), Gemini (mixed), Llama/open-source (sensitivity to prompt structure). What's universal vs. model-specific. | If WOS skills and context files only work well with Claude, the system isn't truly portable. Understanding model-specific behaviors lets you write for the intersection or provide model-aware adapters. |

### Meta / Philosophy

| # | Domain | Description | Why You Need It |
|---|--------|-------------|-----------------|
| 35 | Scope Management & YAGNI | Resisting feature creep — every field, abstraction, and feature must justify itself. Tool vs. framework spectrum. | Agent tool complexity has multiplicative cost. Every unnecessary feature is a source of misuse. |
| 36 | Reads vs. Writes Separation | Separating observation from mutation — audit observes, fixes require explicit action. | An agent that silently "fixes" things is dangerous. This is safety architecture. |

## Scope

- **Must have:** Research-distill pipeline for all 36 domains
- **Won't have:** Implementation changes — this pipeline produces context, not code

## Next Step

Use /wos:write-plan to sequence research-distill pipelines for each domain,
grouping by category to research foundational topics first.
