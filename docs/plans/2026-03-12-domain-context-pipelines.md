---
name: Domain Context Pipelines
description: Research and distill 36 knowledge domains into context files under docs/context/
type: plan
status: executing
related:
  - docs/designs/2026-03-12-domain-context-inventory-design.md
  - docs/prompts/domain-context-pipeline.md
---

# Domain Context Pipelines

**Goal:** Build comprehensive domain context for WOS by running a
research-distill pipeline for each of 36 knowledge domains. The resulting
context files in `docs/context/` provide the analytical baseline for
systematic codebase review and improvement prioritization.

**Scope:**

Must have:
- One context file per domain in `docs/context/` (36 files total)
- Each context file follows WOS conventions (frontmatter, 200-800 words, one concept per file)
- Research documents in `docs/research/` backing each context file
- Foundational domains researched first so later domains can reference them

Won't have:
- Code changes or implementation improvements (context only)
- Codebase review or issue filing (that's Phases 4-7 of the pipeline prompt)
- Merging or PR creation (deferred to pipeline completion)

**Approach:** Execute 36 research-distill pipelines grouped into 10 chunks
by category. Each task runs `/wos:research` (landscape or technical mode)
for a domain, then `/wos:distill` to produce a context file. Chunks are
sequenced so foundational topics (LLM Foundations, Agent Architecture) come
first — later domains can reference earlier context files. Domains within
a chunk are independent and eligible for parallel execution.

**File Changes:**
- Create: `docs/research/` — 36 research documents (one per domain)
- Create: `docs/context/` — 36 context files (one per domain)
- Modify: `docs/context/_index.md` — updated by reindex after each chunk

**Branch:** `feat/recursive-research-to-enhancment-pipeline`
**PR:** TBD

---

## Chunk 1: LLM Foundations

Foundational understanding of LLM behavior that informs every other domain.
Research these first — all later chunks reference these concepts.

### Task 1: Research & distill — LLM Capabilities & Limitations

**Files:**
- Create: `docs/research/llm-capabilities-limitations.md`
- Create: `docs/context/llm-capabilities-limitations.md`

- [x] Run `/wos:research` (landscape mode): What LLMs can do reliably vs. what they can't — hallucination patterns, attention decay ("lost in the middle"), reasoning failure modes, calibration issues. Focus on findings relevant to agent system design, not general ML. <!-- sha:f0ad314 -->
- [x] Run `/wos:distill` to produce `docs/context/llm-capabilities-limitations.md` <!-- sha:f0ad314 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words, `related` links to research doc <!-- sha:f0ad314 -->
- [x] Commit <!-- sha:f0ad314 -->

---

### Task 2: Research & distill — Prompt Engineering

**Files:**
- Create: `docs/research/prompt-engineering.md`
- Create: `docs/context/prompt-engineering.md`

- [x] Run `/wos:research` (landscape mode): Techniques for reliable LLM instruction — constraint specification, output formatting, anti-pattern guards, few-shot examples, chain-of-thought, calibrating specificity vs. flexibility. Focus on system-level prompt design (skill authoring), not conversational prompting. <!-- sha:f0ad314 -->
- [x] Run `/wos:distill` to produce `docs/context/prompt-engineering.md` <!-- sha:f0ad314 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words, `related` links to research doc <!-- sha:f0ad314 -->
- [x] Commit <!-- sha:f0ad314 -->

---

### Task 3: Research & distill — Context Window Management

**Files:**
- Create: `docs/research/context-window-management.md`
- Create: `docs/context/context-window-management.md`

- [x] Run `/wos:research` (technical mode): Token budgets, inclusion/exclusion strategies, compression approaches, how to structure content so important information survives context limits. Include attention-aware formatting patterns (BLUF, first/last positioning). <!-- sha:f0ad314 -->
- [x] Run `/wos:distill` to produce `docs/context/context-window-management.md` <!-- sha:f0ad314 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words, `related` links to research doc <!-- sha:f0ad314 -->
- [x] Commit <!-- sha:f0ad314 -->

---

## Chunk 2: Agent Architecture

Core patterns for building agent systems. Depends on Chunk 1 (LLM
Foundations) for understanding what agents can reliably do.

### Task 4: Research & distill — Agentic Planning & Execution

**Files:**
- Create: `docs/research/agentic-planning-execution.md`
- Create: `docs/context/agentic-planning-execution.md`

- [x] Run `/wos:research` (landscape mode): How LLM agents decompose goals into tasks, sequence work, track progress via artifacts (not memory), handle failures, and resume across sessions. Include plan formats, approval gates, checkpoint/rollback patterns. Compare approaches (ReAct, plan-and-execute, tree-of-thought). <!-- sha:5916ce0 -->
- [x] Run `/wos:distill` to produce `docs/context/agentic-planning-execution.md` <!-- sha:5916ce0 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:5916ce0 -->
- [x] Commit <!-- sha:5916ce0 -->

---

### Task 5: Research & distill — Multi-Agent Coordination

**Files:**
- Create: `docs/research/multi-agent-coordination.md`
- Create: `docs/context/multi-agent-coordination.md`

- [x] Run `/wos:research` (landscape mode): Parallel dispatch patterns, context sharing between agents, conflict detection (file/resource overlap), scoping agent work to avoid interference. Include both framework-level coordination (CrewAI, AutoGen) and low-level patterns (fork-join, wave-based execution). <!-- sha:5916ce0 -->
- [x] Run `/wos:distill` to produce `docs/context/multi-agent-coordination.md` <!-- sha:5916ce0 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:5916ce0 -->
- [x] Commit <!-- sha:5916ce0 -->

---

### Task 6: Research & distill — Tool Design for LLMs

**Files:**
- Create: `docs/research/tool-design-for-llms.md`
- Create: `docs/context/tool-design-for-llms.md`

- [x] Run `/wos:research` (technical mode): What makes a good tool interface for an agent — input/output contracts, error signaling, idempotency requirements, how tool design affects agent reasoning. Include examples from Claude tool use, OpenAI function calling, and agent frameworks. <!-- sha:5916ce0 -->
- [x] Run `/wos:distill` to produce `docs/context/tool-design-for-llms.md` <!-- sha:5916ce0 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:5916ce0 -->
- [x] Commit <!-- sha:5916ce0 -->

---

### Task 7: Research & distill — Agent State & Persistence

**Files:**
- Create: `docs/research/agent-state-persistence.md`
- Create: `docs/context/agent-state-persistence.md`

- [x] Run `/wos:research` (technical mode): How agents maintain context across sessions — disk-as-truth patterns, checkpoint annotations, artifact-based resumption, memory systems (short-term, long-term, episodic). Compare conversation-based vs. file-based vs. database-backed persistence. <!-- sha:5916ce0 -->
- [x] Run `/wos:distill` to produce `docs/context/agent-state-persistence.md` <!-- sha:5916ce0 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:5916ce0 -->
- [x] Commit <!-- sha:5916ce0 -->

---

## Chunk 3: Knowledge Engineering

How to organize, build, and maintain knowledge. Depends on Chunks 1-2 for
understanding what agents need and how they consume information.

### Task 8: Research & distill — Information Architecture

**Files:**
- Create: `docs/research/information-architecture.md`
- Create: `docs/context/information-architecture.md`

- [x] Run `/wos:research` (landscape mode): How to organize knowledge for retrieval — taxonomy design, flat vs. hierarchical structures, navigation patterns, discoverability. Include both traditional IA and agent-specific patterns (index files, metadata-first navigation). <!-- sha:0add835 -->
- [x] Run `/wos:distill` to produce `docs/context/information-architecture.md` <!-- sha:0add835 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:0add835 -->
- [x] Commit <!-- sha:0add835 -->

---

### Task 9: Research & distill — Context Engineering

**Files:**
- Create: `docs/research/context-engineering.md`
- Create: `docs/context/context-engineering.md`

- [x] Run `/wos:research` (deep-dive mode): How to structure, store, and surface project knowledge so LLMs can consume it effectively — document models, frontmatter conventions, indexing strategies, attention-aware formatting. This is the core problem WOS solves; research thoroughly. <!-- sha:0add835 -->
- [x] Run `/wos:distill` to produce `docs/context/context-engineering.md` <!-- sha:0add835 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:0add835 -->
- [x] Commit <!-- sha:0add835 -->

---

### Task 10: Research & distill — Research Methodology

**Files:**
- Create: `docs/research/research-methodology.md`
- Create: `docs/context/research-methodology.md`

- [x] Run `/wos:research` (landscape mode): Systematic information gathering — source discovery strategies, evaluation frameworks, cross-referencing techniques, confidence assessment. Include academic and practitioner approaches relevant to agent-driven research. <!-- sha:0add835 -->
- [x] Run `/wos:distill` to produce `docs/context/research-methodology.md` <!-- sha:0add835 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:0add835 -->
- [x] Commit <!-- sha:0add835 -->

---

### Task 11: Research & distill — Source Evaluation & Claim Verification

**Files:**
- Create: `docs/research/source-evaluation-claim-verification.md`
- Create: `docs/context/source-evaluation-claim-verification.md`

- [x] Run `/wos:research` (technical mode): SIFT framework (Stop, Investigate, Find better, Trace), source tier hierarchies, claim verification types (quotes, statistics, attributions), Chain-of-Verification (CoVe) to prevent confirmation bias. Include how these apply specifically to LLM-assisted research. <!-- sha:0add835 -->
- [x] Run `/wos:distill` to produce `docs/context/source-evaluation-claim-verification.md` <!-- sha:0add835 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:0add835 -->
- [x] Commit <!-- sha:0add835 -->

---

### Task 12: Research & distill — Knowledge Synthesis & Distillation

**Files:**
- Create: `docs/research/knowledge-synthesis-distillation.md`
- Create: `docs/context/knowledge-synthesis-distillation.md`

- [x] Run `/wos:research` (technical mode): How to compress raw research into focused, actionable context — what to keep, what to discard, preserving provenance while reducing volume. Include information compression theory and practical heuristics for agent-facing documents. <!-- sha:0add835 -->
- [x] Run `/wos:distill` to produce `docs/context/knowledge-synthesis-distillation.md` <!-- sha:0add835 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:0add835 -->
- [x] Commit <!-- sha:0add835 -->

---

### Task 13: Research & distill — Writing for LLM Consumption

**Files:**
- Create: `docs/research/writing-for-llm-consumption.md`
- Create: `docs/context/writing-for-llm-consumption.md`

- [x] Run `/wos:research` (technical mode): How agent-facing documentation differs from human-facing — BLUF structure, explicit over implicit, self-contained sections, navigable metadata. Include research on LLM reading comprehension patterns and document structure effects on output quality. <!-- sha:0add835 -->
- [x] Run `/wos:distill` to produce `docs/context/writing-for-llm-consumption.md` <!-- sha:0add835 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:0add835 -->
- [x] Commit <!-- sha:0add835 -->

---

## Chunk 4: Workflow & Orchestration

Patterns for multi-phase processes and human-agent collaboration.
Depends on Chunks 1-3.

### Task 14: Research & distill — Workflow Orchestration

**Files:**
- Create: `docs/research/workflow-orchestration.md`
- Create: `docs/context/workflow-orchestration.md`

- [x] Run `/wos:research` (landscape mode): State machines for multi-phase agent processes — lifecycle management, phase gates, transition rules, resumable and auditable workflows. Include both theoretical (Petri nets, state charts) and practical (agent workflow engines, DAG-based systems). <!-- sha:106f0f8 -->
- [x] Run `/wos:distill` to produce `docs/context/workflow-orchestration.md` <!-- sha:106f0f8 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:106f0f8 -->
- [x] Commit <!-- sha:106f0f8 -->

---

### Task 15: Research & distill — Human-in-the-Loop Design

**Files:**
- Create: `docs/research/human-in-the-loop-design.md`
- Create: `docs/context/human-in-the-loop-design.md`

- [x] Run `/wos:research` (landscape mode): When to gate on user approval vs. automate, how to present decisions that need input, trust calibration, cost/benefit of autonomy at each step. Include research on human-AI teaming, appropriate reliance, and automation bias. <!-- sha:106f0f8 -->
- [x] Run `/wos:distill` to produce `docs/context/human-in-the-loop-design.md` <!-- sha:106f0f8 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:106f0f8 -->
- [x] Commit <!-- sha:106f0f8 -->

---

### Task 16: Research & distill — Feedback Loop Design

**Files:**
- Create: `docs/research/feedback-loop-design.md`
- Create: `docs/context/feedback-loop-design.md`

- [x] Run `/wos:research` (technical mode): Capturing what works and what doesn't, closing the loop between execution and design, operationalizing learnings. Include structured feedback formats, retrospective patterns, and the supersede-don't-edit pattern for immutable artifacts. <!-- sha:106f0f8 -->
- [x] Run `/wos:distill` to produce `docs/context/feedback-loop-design.md` <!-- sha:106f0f8 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:106f0f8 -->
- [x] Commit <!-- sha:106f0f8 -->

---

### Task 17: Research & distill — Intent Classification & Mode Selection

**Files:**
- Create: `docs/research/intent-classification-mode-selection.md`
- Create: `docs/context/intent-classification-mode-selection.md`

- [x] Run `/wos:research` (technical mode): How agents detect user intent and adapt behavior — classification approaches, mode switching patterns, complexity calibration. Include examples from chatbot design, skill routing, and adaptive agent systems. <!-- sha:106f0f8 -->
- [x] Run `/wos:distill` to produce `docs/context/intent-classification-mode-selection.md` <!-- sha:106f0f8 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:106f0f8 -->
- [x] Commit <!-- sha:106f0f8 -->

---

## Chunk 5: Decision & Principles

Frameworks for structured thinking and principled design.
Depends on Chunks 1-2.

### Task 18: Research & distill — Structured Thinking & Decision Frameworks

**Files:**
- Create: `docs/research/structured-thinking-decision-frameworks.md`
- Create: `docs/context/structured-thinking-decision-frameworks.md`

- [x] Run `/wos:research` (landscape mode): Mental models (first principles, inversion, Eisenhower, Pareto, second-order effects) and how to operationalize them as agent-usable tools rather than reference material. Include research on LLM reasoning with structured frameworks. <!-- sha:dc1ca86 -->
- [x] Run `/wos:distill` to produce `docs/context/structured-thinking-decision-frameworks.md` <!-- sha:dc1ca86 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:dc1ca86 -->
- [x] Commit <!-- sha:dc1ca86 -->

---

### Task 19: Research & distill — Principle Engineering

**Files:**
- Create: `docs/research/principle-engineering.md`
- Create: `docs/context/principle-engineering.md`

- [x] Run `/wos:research` (technical mode): How to extract, classify, and maintain design principles as living documents — classification criteria, verification requirements, drift detection, density-performance correlation (~150-200 effective instructions per agent session). Include ADR patterns, RFC processes, and constitutional AI approaches. <!-- sha:dc1ca86 -->
- [x] Run `/wos:distill` to produce `docs/context/principle-engineering.md` <!-- sha:dc1ca86 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:dc1ca86 -->
- [x] Commit <!-- sha:dc1ca86 -->

---

### Task 20: Research & distill — Abstraction Level Design

**Files:**
- Create: `docs/research/abstraction-level-design.md`
- Create: `docs/context/abstraction-level-design.md`

- [x] Run `/wos:research` (technical mode): Choosing the right altitude for different artifacts — specs (WHAT/WHY), plans (middle altitude observable outcomes), research (mode intensity), instructions (specificity calibration). How abstraction level affects agent execution reliability. <!-- sha:dc1ca86 -->
- [x] Run `/wos:distill` to produce `docs/context/abstraction-level-design.md` <!-- sha:dc1ca86 -->
- [x] Verify: context file exists, has frontmatter (name, description), 200-800 words <!-- sha:dc1ca86 -->
- [x] Commit <!-- sha:dc1ca86 -->

---

## Chunk 6: Software Design

Design patterns specific to agent tooling systems.
Depends on Chunks 1-3.

### Task 21: Research & distill — Convention-Driven Design

**Files:**
- Create: `docs/research/convention-driven-design.md`
- Create: `docs/context/convention-driven-design.md`

- [ ] Run `/wos:research` (technical mode): How to establish implicit contracts (naming, file layout, metadata formats) that agents discover and follow without configuration. The "derive from disk, never hand-curate" philosophy. Include convention-over-configuration in Rails, Go, and agent systems.
- [ ] Run `/wos:distill` to produce `docs/context/convention-driven-design.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 22: Research & distill — Plugin & Extension Architecture

**Files:**
- Create: `docs/research/plugin-extension-architecture.md`
- Create: `docs/context/plugin-extension-architecture.md`

- [ ] Run `/wos:research` (landscape mode): How host systems discover, load, and invoke plugins — registration mechanisms, script execution patterns, sandboxing constraints, version management. Include Claude Code plugins, VS Code extensions, Vim plugins, and other extension models.
- [ ] Run `/wos:distill` to produce `docs/context/plugin-extension-architecture.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 23: Research & distill — Validation Architecture

**Files:**
- Create: `docs/research/validation-architecture.md`
- Create: `docs/context/validation-architecture.md`

- [ ] Run `/wos:research` (technical mode): How to separate deterministic structure checks from heuristic quality assessment, severity models (warn/fail), what to validate at which layer. Include validation patterns from compilers, linters, CI pipelines, and how they apply to agent-produced content.
- [ ] Run `/wos:distill` to produce `docs/context/validation-architecture.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 24: Research & distill — Idempotency & Convergent Operations

**Files:**
- Create: `docs/research/idempotency-convergent-operations.md`
- Create: `docs/context/idempotency-convergent-operations.md`

- [ ] Run `/wos:research` (technical mode): Designing operations safe to run repeatedly — convergent state, idempotent writes, safe retries in agent systems. Include infrastructure-as-code parallels (Terraform, Ansible), database migrations, and how these patterns apply to document/context management.
- [ ] Run `/wos:distill` to produce `docs/context/idempotency-convergent-operations.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

## Chunk 7: Developer Experience

How users interact with and adopt agent tooling.
Depends on Chunks 1-4.

### Task 25: Research & distill — Onboarding & Progressive Disclosure

**Files:**
- Create: `docs/research/onboarding-progressive-disclosure.md`
- Create: `docs/context/onboarding-progressive-disclosure.md`

- [ ] Run `/wos:research` (landscape mode): How to layer complexity for different contexts — empty-repo first-run vs. mature project, guiding first actions without overwhelming. Include UX research on progressive disclosure, CLI onboarding patterns, and developer tool adoption.
- [ ] Run `/wos:distill` to produce `docs/context/onboarding-progressive-disclosure.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 26: Research & distill — Git Workflow Integration

**Files:**
- Create: `docs/research/git-workflow-integration.md`
- Create: `docs/context/git-workflow-integration.md`

- [ ] Run `/wos:research` (technical mode): Commits as rollback boundaries, branch naming conventions, PR automation, making agent-driven development compatible with team git workflows. Include git worktree patterns, conventional commits, and how CI/CD interacts with agent-produced code.
- [ ] Run `/wos:distill` to produce `docs/context/git-workflow-integration.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 27: Research & distill — CLI Design

**Files:**
- Create: `docs/research/cli-design.md`
- Create: `docs/context/cli-design.md`

- [ ] Run `/wos:research` (technical mode): Argument patterns, output formatting (human-readable vs. JSON), exit codes, making scripts usable by both humans and agents. Include POSIX conventions, 12-factor CLI patterns, and agent-specific considerations (parseable output, deterministic formatting).
- [ ] Run `/wos:distill` to produce `docs/context/cli-design.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 28: Research & distill — Issue Tracking & External System Integration

**Files:**
- Create: `docs/research/issue-tracking-external-integration.md`
- Create: `docs/context/issue-tracking-external-integration.md`

- [ ] Run `/wos:research` (landscape mode): How agent systems file issues (templates, deduplication), interact with external APIs, handle authentication, and close feedback loops with project management tools. Include GitHub Issues/Actions, Linear, Jira patterns.
- [ ] Run `/wos:distill` to produce `docs/context/issue-tracking-external-integration.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

## Chunk 8: Quality & Reliability

Testing, error handling, and observability for agent systems.
Depends on Chunks 1-4.

### Task 29: Research & distill — Testing Non-Deterministic Systems

**Files:**
- Create: `docs/research/testing-non-deterministic-systems.md`
- Create: `docs/context/testing-non-deterministic-systems.md`

- [ ] Run `/wos:research` (technical mode): How to test agent-driven workflows when outputs aren't identical — behavioral testing, structural assertions, property-based testing, testing deterministic and LLM layers independently. Include eval frameworks, snapshot testing, and contract testing patterns.
- [ ] Run `/wos:distill` to produce `docs/context/testing-non-deterministic-systems.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 30: Research & distill — Error Handling in Agent Systems

**Files:**
- Create: `docs/research/error-handling-agent-systems.md`
- Create: `docs/context/error-handling-agent-systems.md`

- [ ] Run `/wos:research` (technical mode): How agents should handle failures — escalation thresholds, structured failure reporting, distinguishing retryable errors from design-level blockers. Include graceful degradation, circuit breaker patterns, and how error handling differs when the "code" is an LLM.
- [ ] Run `/wos:distill` to produce `docs/context/error-handling-agent-systems.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 31: Research & distill — Observability & Audit Trails

**Files:**
- Create: `docs/research/observability-audit-trails.md`
- Create: `docs/context/observability-audit-trails.md`

- [ ] Run `/wos:research` (technical mode): Making agent activity inspectable — logging strategies, search protocol recording, checkpoint annotations, trace formats. Include OpenTelemetry for agents, structured logging, and "show your work" patterns that enable debugging and trust.
- [ ] Run `/wos:distill` to produce `docs/context/observability-audit-trails.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

## Chunk 9: Platforms & Portability

Understanding the landscape of agent frameworks, coding assistants, and
model-specific conventions to ensure WOS remains portable.
Depends on Chunks 1-2.

### Task 32: Research & distill — Agent Framework Landscape

**Files:**
- Create: `docs/research/agent-framework-landscape.md`
- Create: `docs/context/agent-framework-landscape.md`

- [ ] Run `/wos:research` (landscape mode): How agent frameworks (LangChain, CrewAI, AutoGen, Semantic Kernel, DSPy, etc.) handle tool registration, memory, planning, and orchestration. Identify universal patterns vs. framework-specific abstractions. Focus on what WOS can learn or must remain compatible with.
- [ ] Run `/wos:distill` to produce `docs/context/agent-framework-landscape.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 33: Research & distill — AI Coding Assistant Conventions

**Files:**
- Create: `docs/research/ai-coding-assistant-conventions.md`
- Create: `docs/context/ai-coding-assistant-conventions.md`

- [ ] Run `/wos:research` (landscape mode): How AI coding tools (Claude Code, GitHub Copilot, Cursor, Windsurf, Codex CLI, Cline, Aider) handle project context, instruction files (CLAUDE.md, .cursorrules, .github/copilot-instructions.md, AGENTS.md), tool invocation, and skill/command systems. Map the common patterns and divergences.
- [ ] Run `/wos:distill` to produce `docs/context/ai-coding-assistant-conventions.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 34: Research & distill — Cross-Model Prompt Portability

**Files:**
- Create: `docs/research/cross-model-prompt-portability.md`
- Create: `docs/context/cross-model-prompt-portability.md`

- [ ] Run `/wos:research` (technical mode): How instruction styles, formatting preferences, and reasoning patterns differ across model families — Claude (XML tags), GPT/Codex (Markdown, system messages), Gemini (mixed), Llama/open-source (prompt sensitivity). What's universal vs. model-specific. Include benchmarks on format effects.
- [ ] Run `/wos:distill` to produce `docs/context/cross-model-prompt-portability.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

## Chunk 10: Meta / Philosophy

Cross-cutting design philosophies that constrain all other decisions.
Can run in parallel with Chunks 5-9.

### Task 35: Research & distill — Scope Management & YAGNI

**Files:**
- Create: `docs/research/scope-management-yagni.md`
- Create: `docs/context/scope-management-yagni.md`

- [ ] Run `/wos:research` (technical mode): How to resist feature creep in agent tooling — every field, abstraction, and feature must justify itself. The tool vs. framework spectrum. Include XP/lean perspectives, complexity budgets, and how YAGNI applies differently when the consumer is an LLM.
- [ ] Run `/wos:distill` to produce `docs/context/scope-management-yagni.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

### Task 36: Research & distill — Reads vs. Writes Separation

**Files:**
- Create: `docs/research/reads-vs-writes-separation.md`
- Create: `docs/context/reads-vs-writes-separation.md`

- [ ] Run `/wos:research` (technical mode): The architectural pattern of separating observation from mutation in agent systems — CQRS parallels, why agents that silently "fix" things are dangerous, safety architecture for automated systems. Include examples from infrastructure automation and database design.
- [ ] Run `/wos:distill` to produce `docs/context/reads-vs-writes-separation.md`
- [ ] Verify: context file exists, has frontmatter (name, description), 200-800 words
- [ ] Commit

---

## Validation

- [ ] All 36 context files exist in `docs/context/` with valid frontmatter (name, description fields present)
- [ ] All 36 research documents exist in `docs/research/` with valid frontmatter
- [ ] Each context file is 200-800 words
- [ ] `uv run scripts/audit.py --root . --no-urls` — no failures for new files
- [ ] `uv run scripts/reindex.py --root .` — indexes regenerated successfully
- [ ] Each context file's `related` field links back to its research document
