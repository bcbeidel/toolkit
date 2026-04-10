---
name: Knowledge Base Rebuild
description: Clean-sweep rebuild of the WOS knowledge base — archive existing docs, research 72 topics with fresh sources, distill into focused context files
type: plan
status: executing
branch: feat-rebuild-knowlege-base
related:
---

## Goal

Rebuild the entire WOS knowledge base from scratch. Archive all existing
context and research files, conduct fresh research across 72 topics that
fully cover every codebase component, and distill findings into focused
context files. The result is a current, comprehensive knowledge base
built on 2025-2026 sources.

## Scope

**Must have:**

- Pre-flight permission and branch setup
- Archive existing context and research files (recoverable via git)
- 72 fresh research documents covering all codebase components
- ~90-140 distilled context files (200-800 words each)
- Research briefs pre-approved in this plan (user confirms when skill gate fires)
- Distillation follows standard pattern with explicit naming/dedup rules
- Clean audit at completion

**Won't have:**

- Preserving any existing research or context files (git history is the archive)
- Rebuilding `docs/context/eval/` (separate initiative, preserved as-is)
- Interactive distillation mapping per cluster (standard pattern applies)
- Designs or plans beyond this one
- Changes to Python code, skills, or scripts

## Approach

**Five-phase sequential execution via WOS skills:**

1. **Setup** — archive existing docs to a git tag, delete from working tree
2. **Research** — 13 cluster tasks executed sequentially. Within each
   cluster, invoke `/wos:research` sequentially for each topic (one
   skill invocation at a time). The skill handles the full pipeline
   internally (framer → gatherer → evaluator → challenger → synthesizer
   → verifier → finalizer).
3. **Validate & Review Research** — audit all research documents, then
   present summaries for user review. **Hard gate:** user must approve
   research batch before distillation begins.
4. **Distill** — 13 cluster tasks executed sequentially. Within each
   cluster, invoke `/wos:distill` with the completed research documents.
   The skill handles mapping, writing, and per-file validation.
5. **Validate & Cleanup** — audit distilled context files, verify links
   and index sync, delete research docs, final audit.

**Research briefs:** Each research topic below includes the exact brief
(mode, sub-questions, search strategy). Plan approval = bulk approval
of all briefs. The `/wos:research` skill will fire its brief approval
gate — the user should confirm when prompted since the briefs are
already reviewed in this plan.

**Distillation rules:**
- Each research document produces 1-2 context files in `docs/context/`
- Use `.context.md` compound suffix (e.g., `prompt-engineering.context.md`)
- Derive filenames from the finding, not the research topic
- 200-800 words per file, one atomic concept per file
- Carry `sources:` URLs forward from research into context files
- Link context files to EACH OTHER via `related:`, NOT to research docs
  (research docs are deleted in cleanup — linking to them creates breakage)
- When two research docs in the same cluster cover overlapping territory,
  merge overlapping findings into a single context file citing both sources

**Branch:** `feat-rebuild-knowlege-base`

**Freshness requirement:** All research must prioritize 2025-2026 sources.
When older foundational sources are cited, note what has changed since.

**Multi-session execution:** This plan is designed for execution across
multiple sessions. The checkpoint structure (checkboxes + commit SHAs)
supports resumption at any point. Each cluster is a natural session
boundary.

## Pre-Flight (before executing)

Before starting execution, the user should:

1. **Configure tool permissions.** Add auto-approve for research tools
   to reduce interruptions during sequential research execution:
   ```json
   // .claude/settings.json
   {
     "permissions": {
       "allow": ["WebSearch", "WebFetch", "Write", "Edit", "Read", "Glob", "Grep"]
     }
   }
   ```
   Alternatively, approve each tool type once during the session using
   "allow for this session" when first prompted.

2. **Expect research brief confirmations.** The `/wos:research` skill
   has a hard gate requiring brief approval. The briefs are pre-approved
   in this plan, so confirm promptly when prompted. Expect 72 brief
   confirmation prompts (one per topic, sequential).

3. **Budget for multi-session execution.** 72 sequential research skill
   invocations, each running the full 6-agent pipeline. This will span
   multiple sessions. Each cluster is a natural session boundary — use
   the checkpoint structure to resume.

## File Changes

### Delete (Task 1)

All files in `docs/context/*.md` (except `_index.md` and `eval/`)
All files in `docs/research/*.md` (except `_index.md`)

### Create (Tasks 2-14)

72 research documents in `docs/research/`

### Create (Tasks 17-29)

~90-140 context files in `docs/context/`

### Delete (Task 31)

All research documents created in Tasks 2-14 (value captured in context)

## Tasks

### Phase 1: Setup

- [x] **Task 1: Archive existing knowledge base, remove deprecated skills, and clean directories.** <!-- sha:14259c6 -->
  Create a git tag `knowledge-base-v1-archive` on the current commit to
  preserve the existing knowledge base in git history. Then:
  1. Delete deprecated skills: `skills/report-issue/`, `skills/principles/`,
     `skills/challenge/` (including all SKILL.md, references/, scripts/).
  2. Delete all files in `docs/context/` (except `_index.md` and the `eval/`
     subdirectory — eval is out of scope for this rebuild).
  3. Delete all files in `docs/research/` (except `_index.md`). Also delete
     any untracked research files (the `2026-03-23-eval-*.research.md` files).
  Run `python scripts/reindex.py --root .` to update indexes. Commit
  with message: `chore: archive knowledge base, remove deprecated skills`.
  Verify: `docs/context/` contains only `_index.md` and `eval/`;
  `docs/research/` contains only `_index.md`; `skills/report-issue/`,
  `skills/principles/`, and `skills/challenge/` no longer exist.

### Phase 2: Research (13 cluster tasks, sequential via `/wos:research`)

For each topic within each cluster, invoke `/wos:research` sequentially.
The skill handles the full pipeline internally (framer → gatherer →
evaluator → challenger → synthesizer → verifier → finalizer) with gate
validation between each agent. Briefs below are pre-approved — confirm
when the skill fires its brief approval gate.

Execute clusters in order (Task 2 → Task 14). Within each cluster,
execute topics in order. Commit after each cluster completes.

All research must prioritize 2025-2026 sources. Use `landscape`
mode for broad surveys, `deep-dive` for focused investigations,
`technical` for implementation-specific topics.

**Canonical tooling requirement:** Where relevant, each research document
should identify high-quality open-source tools, libraries, or reference
implementations that exemplify the topic's best practices. Include links
to repositories, documentation, or examples with a brief note on why
they're considered high-quality (adoption, design, documentation, test
coverage). These serve as both implementation references and exemplars
for WOS's own development.

- [x] **Task 2: Research Cluster 1 — Core LLM Patterns (8 topics).** <!-- sha:19f80ab -->
  Invoke `/wos:research` sequentially for each topic:

  **Topic 1.1: Prompt Engineering & Instruction Design**
  Mode: deep-dive. Output: `2026-04-07-prompt-engineering.research.md`
  Sub-questions:
  - What prompt structures produce the most reliable LLM instruction-following for system-level prompts (skill definitions, tool instructions)?
  - How do few-shot examples, XML tags, and structured sections affect compliance rates across Claude, GPT, and Gemini?
  - What are the current best practices for writing CLAUDE.md and AGENTS.md files that agents consistently follow?
  - How does prompt length affect instruction adherence, and what are the practical limits?
  - What techniques (prompt repetition, role assignment, self-check instructions) have the strongest empirical backing?
  Search: Anthropic prompt engineering docs, "Principled Instructions" (Bsharat 2023), Repeat After Me (Google 2025), CLAUDE.md best practices blogs, prompt engineering surveys 2025-2026.

  **Topic 1.2: Context Engineering & Window Management**
  Mode: deep-dive. Output: `2026-04-07-context-engineering.research.md`
  Sub-questions:
  - How should project context be structured for optimal LLM retrieval and comprehension (document size, format, organization)?
  - What context injection strategies do current AI coding tools use (Aider's repo maps, Cursor's semantic indexing, Windsurf's flow tracking)?
  - How do context window limits affect agent performance, and what strategies mitigate degradation at scale?
  - What is the optimal document size for RAG retrieval precision (empirical findings)?
  - How does the "lost in the middle" attention pattern affect context file design?
  Search: context engineering blogs 2025-2026, Aider architecture docs, Cursor technical posts, Claude context window research, RAG retrieval optimization papers.

  **Topic 1.3: LLM-as-Judge Evaluation Patterns**
  Mode: deep-dive. Output: `2026-04-07-llm-as-judge.research.md`
  Sub-questions:
  - What evaluation modes (pointwise, pairwise, binary) produce the most reliable LLM judgments for code compliance tasks?
  - How do rubric specificity, locked rubrics, and chain-of-thought affect evaluation consistency?
  - What are the known biases in LLM-as-judge systems (position, verbosity, self-enhancement) and how are they mitigated?
  - How do rule-specific evaluation patterns differ from general LLM-as-judge patterns?
  - What eval frameworks (promptfoo, DeepEval, Langfuse, Braintrust) are current best-in-class and how do they structure evaluations?
  Search: LLM-as-judge surveys 2024-2026, Anthropic eval guidance, Rulers (Hong 2026), promptfoo/DeepEval docs, rule-based enforcement research.

  **Topic 1.4: Writing for LLM Consumption**
  Mode: technical. Output: `2026-04-07-writing-for-llm-consumption.research.md`
  Sub-questions:
  - How should documents be structured for optimal LLM comprehension (key insights first/last, section ordering, heading depth)?
  - What formatting choices (markdown vs. plain text vs. XML) affect LLM parsing accuracy?
  - How should abstraction levels be calibrated for agent-facing artifacts vs. human-facing docs?
  - What document length and complexity thresholds trigger comprehension degradation?
  Search: writing for AI consumption guides, Anthropic documentation best practices, LLM reading comprehension research, agent-facing documentation patterns.

  **Topic 1.5: Cross-Model Prompt Portability**
  Mode: technical. Output: `2026-04-07-cross-model-portability.research.md`
  Sub-questions:
  - What prompt constructs are portable across Claude, GPT, Gemini, and Llama vs. model-specific?
  - How do XML tags, markdown headers, and JSON structured output perform across model families?
  - What abstraction strategies let skill authors write once and run across models?
  - How do reasoning/thinking modes differ across models and what portability concerns arise?
  Search: cross-model prompt portability 2025-2026, XML tags Claude vs GPT, structured output across models, reasoning mode differences Claude/GPT/Gemini.

  **Topic 1.6: LLM Capabilities & Limitations**
  Mode: landscape. Output: `2026-04-07-llm-capabilities.research.md`
  Sub-questions:
  - What are the current practical limits of frontier LLMs for agent tasks (instruction following, tool use, long context, code generation)?
  - How do capabilities differ across Claude, GPT, Gemini for coding agent use cases?
  - What tasks do LLMs reliably fail at, and what workarounds exist (decomposition, verification, human escalation)?
  - How has the capability frontier shifted in 2025-2026, and what previously-impossible tasks are now viable?
  Search: LLM benchmark comparisons 2025-2026, Claude capabilities documentation, GPT-4o/o3 capabilities, frontier model limitations, LLM failure modes for agents.

  **Topic 1.7: LLM Anti-Patterns & Failure Modes**
  Mode: deep-dive. Output: `2026-04-07-llm-antipatterns.research.md`
  Sub-questions:
  - What are the most impactful LLM behavioral anti-patterns (sycophancy, hallucination, instruction drift, verbosity bias, premature agreement)?
  - How does sycophancy manifest in code review and validation tasks, and what prompting techniques mitigate it?
  - What patterns cause LLMs to silently fail (confident wrong answers, skipped steps, partial compliance)?
  - How should skill authors design prompts that resist common failure modes (chain-of-thought forcing, self-verification, adversarial framing)?
  - What research exists on calibrating LLM confidence and detecting when an LLM doesn't know something?
  Search: LLM sycophancy research 2024-2026, LLM hallucination mitigation, instruction drift in long prompts, LLM failure modes for agents, calibration and uncertainty in LLMs, adversarial prompting for robustness.

  **Topic 1.8: Prompting Best Practices (Comprehensive)**
  Mode: deep-dive. Output: `2026-04-07-prompting-best-practices.research.md`
  Sub-questions:
  - What is the current evidence-backed canon of prompting techniques (chain-of-thought, few-shot, role assignment, structured output, self-consistency)?
  - How do prompting techniques compose — which combinations are synergistic vs. redundant?
  - What are the most common prompting mistakes that degrade output quality?
  - How do prompting best practices differ by task type (classification, generation, analysis, code writing)?
  - What prompt evaluation and iteration methodologies exist (A/B testing, rubric scoring, regression detection)?
  Search: Anthropic prompting best practices 2025-2026, OpenAI prompt engineering guide, chain-of-thought research, few-shot learning surveys, prompt optimization methodologies, Prompt Report (Schulhoff 2024).

  Verify: 8 research documents exist in `docs/research/` with valid
  frontmatter (`type: research`, non-empty `sources:`), findings
  sections, and no `<!-- DRAFT -->` markers.

- [x] **Task 3: Research Cluster 2 — Developer Tool Architecture (6 topics).** <!-- sha:3e37105 -->
  Invoke `/wos:research` sequentially for each topic:

  **Topic 2.1: Instruction File Conventions & Cross-Platform Standards**
  Mode: landscape. Output: `2026-04-07-instruction-file-conventions.research.md`
  Sub-questions:
  - How do AI coding tools (Claude Code, Cursor, Copilot, Windsurf, Codex, Cline, Aider) structure their instruction files in 2026?
  - What is the current adoption and governance status of AGENTS.md as a cross-platform standard?
  - How do hierarchical instruction files (root + subdirectory overrides) work across tools?
  - What metadata fields are supported and how do they vary across platforms?
  Search: AGENTS.md Linux Foundation governance, Claude Code CLAUDE.md docs, Cursor .cursorrules, GitHub Copilot instructions, Windsurf rules, Codex AGENTS.md support.

  **Topic 2.2: Skill Ecosystem Design & Composition**
  Mode: deep-dive. Output: `2026-04-07-skill-ecosystem-design.research.md`
  Sub-questions:
  - How do AI coding tools implement skill/command systems (Claude Code skills, Codex skills, Cursor rules, Cline MCP-first)?
  - What patterns exist for skill composition (skills referencing other skills, shared references, skill chains)?
  - How should skill granularity be calibrated (too fine = overhead, too coarse = inflexible)?
  - What is the relationship between skills, agents, tools, and MCP servers in the current landscape?
  - How do intent classification and mode selection work in skill-based systems?
  Search: Claude Code skills documentation, Codex AGENTS.md skills, MCP skill patterns, intent classification for developer tools, skill vs agent vs tool taxonomy.

  **Topic 2.3: Plugin Architecture & Distribution**
  Mode: landscape. Output: `2026-04-07-plugin-architecture.research.md`
  Sub-questions:
  - How do AI coding tool plugins get discovered, installed, and updated (Claude Code plugins, VS Code extensions, Cursor extensions)?
  - What manifest formats and metadata schemas do plugin systems use?
  - How do plugins handle versioning, compatibility, and dependency management?
  - What deployment patterns exist (symlinks, package managers, git-based, marketplace)?
  Search: Claude Code plugin system docs, VS Code extension API, plugin distribution patterns 2025-2026, marketplace design for developer tools.

  **Topic 2.4: CLI & Tool Design for LLM Agents**
  Mode: technical. Output: `2026-04-07-cli-tool-design.research.md`
  Sub-questions:
  - How should CLI scripts be designed for both human and LLM agent consumption?
  - What output formats (JSON, structured text, exit codes) work best for LLM tool integration?
  - How do tool registration patterns (JSON Schema, function-as-tool) work across agent frameworks?
  - What are MCP's current capabilities for tool exposure and how does the protocol structure tool definitions?
  Search: MCP specification 2025-2026, Claude Code tool use docs, function calling best practices, CLI design for automation.

  **Topic 2.5: Model Context Protocol (MCP) Deep Dive**
  Mode: deep-dive. Output: `2026-04-07-mcp-protocol.research.md`
  Sub-questions:
  - What is MCP's current specification, adoption trajectory, and governance (AAIF donation, monthly download stats)?
  - How do MCP servers expose tools, resources, and prompts, and what are the protocol's design principles?
  - What patterns exist for building MCP servers vs. consuming them as a client?
  - How does MCP relate to other tool protocols (OpenAI function calling, LangChain tools, Semantic Kernel plugins)?
  - What are MCP's current limitations and where is the spec heading?
  Search: MCP specification 2025-2026, MCP GitHub repository, AAIF governance, MCP server examples, MCP adoption statistics, MCP vs function calling comparisons.

  **Topic 2.6: Claude Code Hooks Ecosystem & Best Practices**
  Mode: deep-dive. Output: `2026-04-07-hooks-ecosystem.research.md`
  Sub-questions:
  - What hook types does Claude Code support (PreToolUse, PostToolUse, Notification, etc.) and what are their execution models?
  - How can hooks be used to improve agent output quality (pre-commit validation, file-save checks, rule enforcement, auto-formatting)?
  - What patterns exist for deterministic guardrails via hooks vs. advisory guidance via CLAUDE.md?
  - How should hooks balance enforcement strictness with developer experience (latency, noise, override mechanisms)?
  - What are real-world examples of effective hook configurations for code quality, security scanning, and convention enforcement?
  Search: Claude Code hooks documentation 2025-2026, Claude Code settings.json hooks configuration, pre-commit hook patterns for AI agents, deterministic vs advisory enforcement, hook-based code quality automation.

  Verify: 6 research documents exist with valid frontmatter and sources.

- [ ] **Task 4: Research Cluster 3 — Knowledge Management (4 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 3.1: Information Architecture & Retrieval**
  Mode: deep-dive. Output: `2026-04-07-information-architecture.research.md`
  Sub-questions:
  - How should project knowledge bases be organized for optimal agent navigation (flat vs. hierarchical, indexes, cross-references)?
  - What navigation patterns (auto-generated indexes, description-first scanning, bidirectional linking) improve retrieval?
  - How do current RAG systems and agent context assembly affect information architecture decisions?
  - What is the optimal granularity for knowledge files (one concept per file vs. topic clusters)?
  Search: knowledge management for AI agents, RAG architecture patterns, developer documentation organization, Zettelkasten for agent systems.

  **Topic 3.2: Knowledge Synthesis & Distillation**
  Mode: technical. Output: `2026-04-07-knowledge-synthesis.research.md`
  Sub-questions:
  - What processes reliably convert research findings into actionable reference documents?
  - How should confidence levels and source attribution carry forward through distillation?
  - What document structures optimize for both human readability and LLM retrieval?
  - How do summary-then-detail (BLUF) patterns compare to other structures for agent consumption?
  Search: knowledge distillation for AI systems, technical writing best practices for LLMs, BLUF writing patterns, research-to-practice pipelines.

  **Topic 3.3: Research Methodology & Source Evaluation**
  Mode: technical. Output: `2026-04-07-research-methodology.research.md`
  Sub-questions:
  - How should the SIFT framework (Stop, Investigate, Find better, Trace) be applied to LLM-assisted research?
  - What source tier systems effectively classify reliability (academic, vendor docs, practitioner blogs, forums)?
  - How should claims be verified when LLMs may hallucinate or misattribute sources?
  - What search strategies maximize coverage while minimizing redundancy?
  Search: SIFT framework original source, lateral reading research, source evaluation frameworks, LLM fact verification methods 2025-2026.

  **Topic 3.4: Convention-Driven Design, YAGNI & Complexity Budgets**
  Mode: deep-dive. Output: `2026-04-07-convention-driven-design.research.md`
  Sub-questions:
  - How does convention-over-configuration apply to LLM-consumable project structures?
  - What are the empirical costs of premature abstraction in agent tooling (build, delay, carry, repair)?
  - How do complexity budgets work when every feature competes for LLM context tokens?
  - What principle engineering practices help teams extract, maintain, and enforce design principles?
  - How should idempotent, convergent operations be designed for agent-driven automation?
  Search: convention over configuration (Ruby on Rails, Django patterns), YAGNI empirical evidence, complexity budget frameworks, principle-driven development, idempotency patterns.

  Verify: 4 research documents exist with valid frontmatter and sources.

- [ ] **Task 5: Research Cluster 4 — Agent System Design (6 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 4.1: Agent Frameworks, Portability & MCP**
  Mode: landscape. Output: `2026-04-07-agent-frameworks.research.md`
  Sub-questions:
  - What is the current state of the agent framework landscape (LangChain, CrewAI, AutoGen, Semantic Kernel, Claude Agent SDK) in 2026?
  - How has MCP adoption progressed and what is its current role as a convergence layer?
  - What patterns make agent tools portable across frameworks (target tool layer, avoid orchestration coupling)?
  - How do agent memory tiers (short-term, long-term, semantic) work across frameworks?
  Search: MCP specification and adoption 2026, agent framework comparisons 2025-2026, Claude Agent SDK docs, LangChain/CrewAI architecture updates, portable agent design.

  **Topic 4.2: Multi-Agent Coordination & Workflow Orchestration**
  Mode: deep-dive. Output: `2026-04-07-multi-agent-coordination.research.md`
  Sub-questions:
  - What orchestration topologies (sequential, parallel, hierarchical, swarm) are used in production agent systems?
  - How should multi-phase workflows be modeled (state machines, DAGs, event-driven)?
  - What patterns exist for agent-to-agent delegation, context passing, and result aggregation?
  Search: multi-agent orchestration patterns 2025-2026, state machine patterns for agents, Claude Code subagent dispatch, swarm architectures.

  **Topic 4.3: Error Handling, Escalation & Resilience**
  Mode: deep-dive. Output: `2026-04-07-error-handling.research.md`
  Sub-questions:
  - How should agent errors be classified (retryable vs. design-level, by origin phase)?
  - What escalation patterns work for LLM agents (retry, mutate, fallback, peer escalate, human escalate)?
  - How do circuit breaker patterns adapt for non-deterministic LLM systems?
  - How do idempotent and convergent operations improve agent resilience?
  - What distinguishes LLM errors from traditional software errors (silent failures, cost-per-attempt)?
  Search: agent error handling patterns 2025-2026, circuit breaker for AI systems, LLM retry strategies, Anthropic agent best practices, graceful degradation in agent systems.

  **Topic 4.4: Human-in-the-Loop Design & Approval Gates**
  Mode: deep-dive. Output: `2026-04-07-human-in-the-loop.research.md`
  Sub-questions:
  - How should approval gates be designed for agent workflows (when to pause, what to present, how to resume)?
  - What is progressive disclosure in agent UX and how does it apply to onboarding new users?
  - How do preview-before-execute patterns (Terraform plan, Ansible check mode) apply to LLM agents?
  - What are best practices for calibrating agent autonomy vs. human oversight?
  Search: human-in-the-loop AI design 2025-2026, preview-before-execute patterns, agent autonomy calibration, progressive disclosure in developer tools, Anthropic effective harnesses.

  **Topic 4.5: Git Workflow Integration**
  Mode: technical. Output: `2026-04-07-git-workflow.research.md`
  Sub-questions:
  - How do AI coding agents integrate with git (branching strategies, commit conventions, PR creation)?
  - What patterns exist for commit-per-task boundaries that enable rollback?
  - How should agents handle merge conflicts, worktrees, and concurrent branch work?
  - What git-based verification patterns (SHA annotations, diff-based validation) support agent workflows?
  Search: git workflow for AI agents 2025-2026, Claude Code git integration docs, Codex git patterns, agent-driven PR workflows, worktree patterns for parallel agents.

  **Topic 4.6: Agentic Planning & Execution Patterns**
  Mode: deep-dive. Output: `2026-04-07-agentic-planning.research.md`
  Sub-questions:
  - How should agent plans be structured for resumability across sessions (checkpoint state, task decomposition, progress tracking)?
  - What is "middle altitude" task specification and how does it balance prescriptiveness vs. agent autonomy?
  - How do commit-per-task boundaries create rollback points, and what patterns exist for failure recovery within plans?
  - What are the tradeoffs between plan-as-specification (agent follows exactly) vs. plan-as-guidance (agent adapts)?
  - How should plan lifecycle states (draft, approved, executing, completed, abandoned) be managed and what gates govern transitions?
  - What parallel dispatch patterns exist for independent tasks within a plan?
  Search: agentic planning research 2025-2026, Codex PLANS.md patterns, Anthropic effective harnesses for long-running agents, task decomposition for AI agents, plan lifecycle management, parallel agent dispatch.

  Verify: 6 research documents exist with valid frontmatter and sources.

- [ ] **Task 6: Research Cluster 5A — Quality & Validation (5 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 5.1: Validation Architecture & Structural Checks**
  Mode: technical. Output: `2026-04-07-validation-architecture.research.md`
  Sub-questions:
  - How should validation be separated into structural (deterministic) and quality (LLM-driven) checks?
  - What patterns exist for composable validation pipelines (check functions returning issue lists)?
  - How do reads-vs-writes separation patterns (CQS/CQRS) apply to agent validation systems?
  - What severity models (warn/fail, multi-level) work best for developer-facing validation?
  Search: validation architecture patterns, CQS/CQRS for agent systems, composable linter design, severity models in linting tools 2025-2026.

  **Topic 5.2: Agent Testing & Non-Deterministic Systems**
  Mode: deep-dive. Output: `2026-04-07-agent-testing.research.md`
  Sub-questions:
  - What is the current best practice testing pyramid for agent systems (deterministic base, LLM-as-judge middle, e2e top)?
  - How do record-and-replay, property-based, and snapshot testing apply to non-deterministic outputs?
  - What eval pipeline designs support continuous regression detection for LLM-based tools?
  - How should test fixtures be designed for systems with natural language inputs/outputs?
  Search: agent testing strategies 2025-2026, LLM testing pyramid, non-deterministic system testing, eval pipelines for prompt regression, Anthropic eval methodology.

  **Topic 5.3: Structured Decision Frameworks & Mental Models**
  Mode: deep-dive. Output: `2026-04-07-decision-frameworks.research.md`
  Sub-questions:
  - Which mental models (first principles, inversion, second-order thinking, Eisenhower matrix) are most effective for software engineering decisions?
  - How should structured thinking frameworks be selected based on problem type?
  - What cognitive biases most commonly affect software design decisions, and which frameworks counter them?
  - How can LLM agents apply decision frameworks systematically rather than ad hoc?
  Search: mental models for software engineering, cognitive bias in technical decisions, structured decision making frameworks, first principles thinking applications, Charlie Munger latticework.

  **Topic 5.4: Observability, Tracing & Show-Your-Work**
  Mode: technical. Output: `2026-04-07-observability.research.md`
  Sub-questions:
  - How should agent activity be instrumented for debugging and trust (OpenTelemetry GenAI semantic conventions)?
  - What is the three-layer span model for agent tracing (agent invocation, LLM calls, tool execution)?
  - How do show-your-work patterns (search protocol logging, reasoning traces) improve agent trustworthiness?
  - What distinguishes observability (debugging) from trust (auditability) in agent systems?
  Search: OpenTelemetry GenAI conventions 2025-2026, agent observability patterns, show-your-work for AI systems, agent audit trail design, Traceloop/Langfuse tracing.

  **Topic 5.5: Feedback Loops & Continuous Improvement**
  Mode: technical. Output: `2026-04-07-feedback-loops.research.md`
  Sub-questions:
  - How should feedback loops be designed for iterative agent system improvement?
  - What retrospective methodologies work for human-agent collaboration sessions?
  - How do design-build-test-feedback cycles differ for LLM-based tools vs. traditional software?
  - What patterns exist for capturing and incorporating user corrections into system behavior?
  Search: feedback loops in AI systems 2025-2026, retrospective practices for AI tools, continuous improvement for agent systems, user feedback integration patterns.

  Verify: 5 research documents exist with valid frontmatter and sources.

- [ ] **Task 7: Research Cluster 5B — Practices & Standards (5 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 5.6: Rule-Based LLM Enforcement**
  Mode: deep-dive. Output: `2026-04-07-rule-enforcement.research.md`
  Sub-questions:
  - What structural characteristics (specificity, examples, scope precision) make rules effective for LLM-based enforcement?
  - How do established rule systems (ESLint, Semgrep, Ruff, dbt, OPA) structure rule definitions, and what transfers to LLM evaluation?
  - What pitfalls (false positives, alert fatigue, enforcement without education) kill rule-based systems?
  - What level of rule granularity produces the most consistent LLM evaluation results?
  - What are best practices for rule template libraries (start conservative, organize by concern, test with positive/negative cases)?
  Search: LLM rule following evaluation, LLM content classification, rule system design patterns, ESLint/Semgrep rule architecture, alert fatigue research, rule template best practices.

  **Topic 5.7: Brainstorming & Design Thinking**
  Mode: deep-dive. Output: `2026-04-07-design-thinking.research.md`
  Sub-questions:
  - What divergent-then-convergent thinking patterns are most effective for software design exploration?
  - How should problem spaces be explored before converging on a solution (multiple approaches with tradeoffs)?
  - What anti-patterns in design thinking lead to premature convergence or analysis paralysis?
  - How can LLM agents facilitate structured brainstorming (generating options, evaluating tradeoffs, reaching consensus)?
  Search: design thinking for software engineering, divergent convergent thinking patterns, brainstorming methodologies, structured exploration for technical design, double diamond design process.

  **Topic 5.8: Specification & Design Document Patterns**
  Mode: technical. Output: `2026-04-07-specification-patterns.research.md`
  Sub-questions:
  - What makes a good software design specification (structure, level of detail, acceptance criteria)?
  - How do specs differ from plans — what belongs in each and where is the boundary?
  - What specification formats (ADRs, RFCs, design docs, one-pagers) are used in practice and what are their tradeoffs?
  - How should specs be calibrated for different task complexities (paragraph for simple, full doc for complex)?
  Search: software design document best practices, ADR architecture decision records, RFC process for engineering teams, specification writing for AI-assisted development, design doc templates 2025-2026.

  **Topic 5.9: Secure Development With & For LLMs**
  Mode: deep-dive. Output: `2026-04-07-llm-security.research.md`
  Sub-questions:
  - What are the OWASP Top 10 for LLM applications, and which are most relevant to coding agents?
  - How do prompt injection attacks work (direct, indirect) and what defenses exist?
  - What security patterns should agent-generated code follow (input validation, secret handling, sandbox execution)?
  - How should LLM-based tools handle sensitive data (credentials, PII, proprietary code) in context?
  - What secure development lifecycle practices apply when the developer is an LLM agent?
  Search: OWASP LLM Top 10 2025, prompt injection defense 2025-2026, LLM application security, secure AI coding agent design, sensitive data handling in LLM context, agent sandboxing patterns.

  **Topic 5.10: CI/CD Best Practices, GitHub Actions & Pre-Commit Hooks**
  Mode: deep-dive. Output: `2026-04-07-cicd-best-practices.research.md`
  Sub-questions:
  - What are current best practices for GitHub Actions workflows in Python projects (linting, testing, type checking, security scanning)?
  - How should pre-commit hooks be designed to catch issues early without slowing the development loop (ruff, mypy, shellcheck, secret scanning)?
  - What CI/CD patterns reduce feedback loop time (parallel jobs, caching, incremental checks, "hold the line" for new violations)?
  - How should CI pipelines validate LLM-generated code differently from human-written code?
  - What patterns exist for integrating agent-driven development into CI/CD (auto-PR checks, commit-per-task verification, plan validation)?
  Search: GitHub Actions best practices 2025-2026, pre-commit hook design, CI/CD for Python projects, hold-the-line linting strategy, fast feedback loops in CI, AI-assisted development CI patterns.

  Verify: 5 research documents exist with valid frontmatter and sources.

- [ ] **Task 8: Research Cluster 5C — Engineering Disciplines (6 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 5.11: AI-Assisted Code Review**
  Mode: deep-dive. Output: `2026-04-07-ai-code-review.research.md`
  Sub-questions:
  - How should LLMs be used for structured code review (PR review, design review, security review)?
  - What review dimensions are LLMs most/least reliable at evaluating (logic, style, security, performance)?
  - How do current AI code review tools (CodeRabbit, Codium, GitHub Copilot review) structure their evaluation?
  - What patterns prevent sycophantic reviews (where the LLM approves everything)?
  - How should review feedback be structured for maximum developer actionability?
  Search: AI code review tools 2025-2026, LLM code review accuracy, CodeRabbit architecture, structured code review with LLMs, PR review automation patterns.

  **Topic 5.12: Prompt Versioning & Lifecycle Management**
  Mode: deep-dive. Output: `2026-04-07-prompt-versioning.research.md`
  Sub-questions:
  - How should prompts (skill instructions, system prompts) be versioned, tracked, and evolved over time?
  - What patterns exist for detecting prompt regression (a change that degrades output quality)?
  - How do prompt management platforms (Humanloop, PromptLayer, Langfuse) handle versioning and A/B testing?
  - What is the relationship between prompt versioning and eval pipelines?
  - How should prompt drift (gradual degradation from incremental edits) be detected and prevented?
  Search: prompt versioning best practices 2025-2026, prompt management platforms, prompt regression detection, prompt lifecycle management, prompt drift detection.

  **Topic 5.13: Token Economics & Cost Optimization**
  Mode: technical. Output: `2026-04-07-token-economics.research.md`
  Sub-questions:
  - What are the cost structures of major LLM APIs (input/output tokens, caching, batching) and how do they affect agent design?
  - How should context loading be optimized to minimize token spend (lazy loading, scope-based filtering, summarization)?
  - What caching strategies (prompt caching, response caching, semantic caching) reduce redundant API calls?
  - How should model selection be tiered (use cheaper models for simple tasks, expensive models for complex ones)?
  - What monitoring and budgeting patterns exist for controlling LLM API costs in production?
  Search: LLM API pricing comparison 2025-2026, token optimization strategies, prompt caching (Anthropic, OpenAI), model routing and tiering, LLM cost monitoring tools.

  **Topic 5.14: AI Pair Programming Patterns**
  Mode: deep-dive. Output: `2026-04-07-ai-pair-programming.research.md`
  Sub-questions:
  - How do effective human-AI coding collaboration sessions differ from traditional pair programming?
  - What communication patterns between humans and AI agents produce the best outcomes (directive vs. collaborative vs. autonomous)?
  - How should task handoffs between human and agent be structured (agent proposes, human decides vs. human describes, agent implements)?
  - What session management patterns (context priming, progress checkpointing, session retrospectives) improve collaboration quality?
  Search: AI pair programming research 2025-2026, human-AI collaboration patterns, Claude Code best practices, effective AI coding sessions, task delegation to AI agents.

  **Topic 5.15: Documentation-Driven Development**
  Mode: technical. Output: `2026-04-07-docs-driven-development.research.md`
  Sub-questions:
  - What is documentation-driven development (write docs/specs before code) and what evidence supports its effectiveness?
  - How does the brainstorm→design→plan→execute workflow compare to other development methodologies (TDD, BDD, DDD)?
  - How should documentation artifacts (designs, plans, research) relate to code artifacts (implementations, tests)?
  - What practices ensure documentation stays synchronized with implementation as code evolves?
  Search: documentation-driven development, readme-driven development, design docs before code, spec-first development, documentation as specification, docs-code synchronization.

  **Topic 5.16: Technical Debt Identification & Management**
  Mode: deep-dive. Output: `2026-04-07-technical-debt.research.md`
  Sub-questions:
  - How should technical debt be systematically identified in codebases (automated detection, code health metrics, architecture fitness functions)?
  - What frameworks exist for prioritizing technical debt repayment (cost of delay, risk-based, opportunity-cost)?
  - How can AI agents assist with technical debt identification and remediation?
  - What patterns prevent debt accumulation (architectural guardrails, convention enforcement, regular audits)?
  - How do "hold the line" strategies apply to managing existing debt while preventing new debt?
  Search: technical debt management 2025-2026, code health metrics, architecture fitness functions, AI-assisted debt detection, technical debt prioritization frameworks, hold the line strategy.

  Verify: 6 research documents exist with valid frontmatter and sources.

- [ ] **Task 9: Research Cluster 6 — Application Engineering (6 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 6.1: Data Engineering**
  Mode: deep-dive. Output: `2026-04-07-data-engineering.research.md`
  Sub-questions:
  - What are current best practices for ETL/ELT pipeline architecture (dbt, Airflow, Dagster, Prefect)?
  - How should data transformation layers be structured (raw, staging, intermediate, marts) and what belongs in each?
  - What data quality frameworks and testing patterns ensure pipeline reliability (Great Expectations, dbt tests, Elementary)?
  - How should schema evolution and data contracts be managed across teams?
  - What conventions for naming, documentation, and code organization are standard in modern data engineering?
  Search: dbt best practices 2025-2026, data pipeline architecture patterns, data quality frameworks, data contracts, ELT layer conventions, modern data stack.

  **Topic 6.2: Frontend Engineering**
  Mode: deep-dive. Output: `2026-04-07-frontend-engineering.research.md`
  Sub-questions:
  - What are current best practices for component architecture (React, Vue, Svelte, web components)?
  - How should state management be structured (local vs. global, server state, URL state)?
  - What design system patterns produce maintainable, accessible UIs at scale?
  - How should frontend testing be layered (unit, component, integration, visual regression, e2e)?
  - What build tooling and bundling patterns are current (Vite, Turbopack, esbuild) and how do they affect developer workflows?
  Search: React best practices 2025-2026, component architecture patterns, design systems at scale, frontend testing pyramid, Vite/Turbopack ecosystem, state management patterns.

  **Topic 6.3: Backend/API Engineering**
  Mode: deep-dive. Output: `2026-04-07-backend-api-engineering.research.md`
  Sub-questions:
  - What are current best practices for API design (REST, GraphQL, gRPC, tRPC) and when to use each?
  - How should microservices be structured, sized, and communicate (sync vs. async, event-driven)?
  - What authentication and authorization patterns are standard (OAuth2, JWT, RBAC, ABAC)?
  - How should API versioning, deprecation, and backwards compatibility be managed?
  - What backend framework conventions produce maintainable codebases (project structure, dependency injection, middleware patterns)?
  Search: API design best practices 2025-2026, microservices patterns, REST vs GraphQL decision framework, authentication patterns, backend project structure conventions.

  **Topic 6.4: Mobile Engineering**
  Mode: landscape. Output: `2026-04-07-mobile-engineering.research.md`
  Sub-questions:
  - What are current best practices for native (Swift/Kotlin) vs. cross-platform (React Native, Flutter, Kotlin Multiplatform) development?
  - How should mobile app architecture be structured (MVVM, MVI, clean architecture, composable patterns)?
  - What testing and CI/CD patterns are specific to mobile (device farms, screenshot testing, staged rollouts)?
  - How do app lifecycle, state restoration, and offline-first patterns affect mobile architecture?
  - What mobile-specific performance patterns matter (launch time, memory, battery, network efficiency)?
  Search: mobile engineering best practices 2025-2026, React Native vs Flutter, mobile app architecture, mobile CI/CD, offline-first patterns, mobile performance optimization.

  **Topic 6.5: Database Engineering & Data Modeling**
  Mode: deep-dive. Output: `2026-04-07-database-engineering.research.md`
  Sub-questions:
  - What are current best practices for relational schema design (normalization, denormalization tradeoffs, indexing strategy)?
  - How should database migrations be managed safely (zero-downtime migrations, rollback strategies, schema versioning)?
  - What query optimization patterns are most impactful (query plans, index design, materialized views, partitioning)?
  - How should database selection be approached (relational, document, graph, time-series, vector) based on workload patterns?
  - What ORM patterns and data access conventions produce maintainable code?
  Search: database design best practices 2025-2026, zero-downtime migrations, query optimization patterns, database selection guide, ORM best practices, schema migration strategies.

  **Topic 6.6: Distributed Systems Engineering**
  Mode: deep-dive. Output: `2026-04-07-distributed-systems.research.md`
  Sub-questions:
  - What are the foundational patterns for building reliable distributed systems (consensus, replication, partitioning)?
  - How should eventual consistency be handled in practice (CRDTs, event sourcing, saga patterns)?
  - What patterns exist for distributed system observability and debugging (distributed tracing, correlation IDs)?
  - How should distributed systems handle failure modes (circuit breakers, bulkheads, retry with backoff, dead letter queues)?
  - What modern infrastructure patterns (service mesh, cell-based architecture, edge computing) are emerging?
  Search: distributed systems patterns 2025-2026, event sourcing best practices, saga pattern, CAP theorem practical applications, service mesh patterns, cell-based architecture.

  Verify: 6 research documents exist with valid frontmatter and sources.

- [ ] **Task 10: Research Cluster 7 — Operations & Platform (5 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 7.1: Site Reliability Engineering (SRE)**
  Mode: deep-dive. Output: `2026-04-07-sre.research.md`
  Sub-questions:
  - What are current SRE best practices for defining and measuring SLOs, SLIs, and error budgets?
  - How should incident management be structured (detection, triage, response, postmortem, prevention)?
  - What chaos engineering practices are most effective for proactive reliability testing?
  - How should toil be identified, measured, and systematically reduced?
  - What runbook and playbook patterns enable effective incident response?
  Search: SRE best practices 2025-2026, Google SRE book updates, SLO implementation patterns, incident management frameworks, chaos engineering tools and practices, toil reduction strategies.

  **Topic 7.2: Platform Engineering**
  Mode: deep-dive. Output: `2026-04-07-platform-engineering.research.md`
  Sub-questions:
  - What is platform engineering and how does it differ from DevOps and SRE?
  - How should internal developer platforms (IDPs) be designed (golden paths, self-service, guardrails)?
  - What developer experience (DX) metrics and practices improve platform adoption?
  - How should platform teams balance standardization with team autonomy?
  - What platform tooling (Backstage, Port, Humanitec) represents current best-in-class?
  Search: platform engineering 2025-2026, internal developer platforms, golden paths, developer experience metrics, Backstage IDP, Team Topologies platform patterns.

  **Topic 7.3: DevOps & Infrastructure as Code**
  Mode: deep-dive. Output: `2026-04-07-devops-iac.research.md`
  Sub-questions:
  - What are current best practices for Infrastructure as Code (Terraform, Pulumi, CDK, OpenTofu)?
  - How should containerization and orchestration be approached (Docker, Kubernetes, ECS, serverless containers)?
  - What deployment strategies minimize risk (blue-green, canary, rolling, feature flags)?
  - How should GitOps workflows be structured (ArgoCD, Flux, pull-based vs. push-based)?
  - What infrastructure testing patterns ensure IaC reliability (Terratest, Checkov, policy-as-code)?
  Search: Infrastructure as Code best practices 2025-2026, Terraform vs Pulumi, Kubernetes patterns, GitOps workflows, deployment strategies, infrastructure testing.

  **Topic 7.4: Cloud Architecture**
  Mode: landscape. Output: `2026-04-07-cloud-architecture.research.md`
  Sub-questions:
  - What are the current well-architected framework principles across AWS, GCP, and Azure?
  - How should multi-cloud and cloud-agnostic strategies be evaluated?
  - What serverless architecture patterns are mature and when should they be used vs. containers?
  - How should cloud cost management and FinOps practices be implemented?
  - What cloud-native security patterns (IAM, network policies, secrets management) are standard?
  Search: AWS well-architected 2025-2026, cloud architecture patterns, serverless best practices, FinOps practices, cloud security patterns, multi-cloud strategy.

  **Topic 7.5: Machine Learning Engineering & MLOps**
  Mode: deep-dive. Output: `2026-04-07-mlops.research.md`
  Sub-questions:
  - What are current best practices for the ML model lifecycle (training, evaluation, deployment, monitoring)?
  - How should feature stores, experiment tracking, and model registries be structured?
  - What MLOps patterns enable reliable model deployment (A/B testing, shadow mode, gradual rollout)?
  - How should data and model drift be detected and handled in production?
  - What ML pipeline orchestration tools (MLflow, Kubeflow, Weights & Biases, Metaflow) are current best-in-class?
  Search: MLOps best practices 2025-2026, ML model lifecycle management, feature store patterns, experiment tracking, model monitoring and drift detection, ML pipeline tools.

  Verify: 5 research documents exist with valid frontmatter and sources.

- [ ] **Task 11: Research Cluster 8 — Cross-Cutting & Management (5 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 8.1: Quality Assurance Engineering**
  Mode: deep-dive. Output: `2026-04-07-qa-engineering.research.md`
  Sub-questions:
  - What are current best practices for test strategy design (test pyramid, trophy, honeycomb)?
  - How should test automation frameworks be selected and structured for different project types?
  - What contract testing patterns (Pact, Prism) ensure API compatibility across services?
  - How should QA processes integrate with CI/CD pipelines for fast feedback?
  - What shift-left testing practices effectively prevent defects rather than detecting them?
  Search: QA engineering best practices 2025-2026, test strategy design, test automation frameworks, contract testing, shift-left testing, QA in CI/CD pipelines.

  **Topic 8.2: Performance Engineering**
  Mode: technical. Output: `2026-04-07-performance-engineering.research.md`
  Sub-questions:
  - What are current best practices for performance testing (load, stress, soak, spike testing)?
  - How should performance profiling and bottleneck identification be structured for different tech stacks?
  - What performance budgets and metrics (Core Web Vitals, P95/P99 latency, throughput) should be tracked?
  - How should performance regression detection be integrated into CI/CD?
  - What tools and frameworks (k6, Locust, Lighthouse, continuous profiling) are current best-in-class?
  Search: performance engineering best practices 2025-2026, load testing patterns, Core Web Vitals optimization, performance budgets, continuous profiling, performance regression detection.

  **Topic 8.3: Accessibility Engineering**
  Mode: deep-dive. Output: `2026-04-07-accessibility-engineering.research.md`
  Sub-questions:
  - What are the current WCAG guidelines (2.2+) and how should they be implemented systematically?
  - How should accessibility testing be automated (axe-core, Lighthouse, screen reader testing)?
  - What design and development patterns produce inherently accessible interfaces?
  - How should accessibility be integrated into CI/CD and design review processes?
  - What organizational patterns ensure accessibility is sustained (champions, audits, training)?
  Search: accessibility engineering 2025-2026, WCAG 2.2 implementation, automated accessibility testing, inclusive design patterns, accessibility in CI/CD, axe-core integration.

  **Topic 8.4: Project Management**
  Mode: deep-dive. Output: `2026-04-07-project-management.research.md`
  Sub-questions:
  - What are current best practices for Agile project management (Scrum, Kanban, Scrumban, Shape Up)?
  - How should estimation and velocity tracking be approached in modern software teams?
  - What sprint planning, backlog grooming, and prioritization frameworks are most effective?
  - How should project management adapt for AI-augmented development (shorter cycles, different estimation)?
  - What project management tools and practices improve delivery predictability?
  Search: Agile best practices 2025-2026, Shape Up methodology, estimation in software, sprint planning patterns, project management for AI-augmented teams, delivery predictability.

  **Topic 8.5: Program Management**
  Mode: landscape. Output: `2026-04-07-program-management.research.md`
  Sub-questions:
  - How should cross-team coordination be structured for multi-team engineering organizations?
  - What dependency tracking and risk management frameworks are most effective?
  - How should portfolio management and investment allocation across projects be approached?
  - What stakeholder communication patterns keep leadership aligned without micromanagement?
  - How do OKRs, roadmaps, and strategy documents connect program goals to team execution?
  Search: program management best practices 2025-2026, cross-team coordination, dependency management, portfolio management, OKR frameworks, engineering program management.

  Verify: 5 research documents exist with valid frontmatter and sources.

- [ ] **Task 12: Research Cluster 8B — Product, Content & Revenue (4 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 8.6: Product Design & UX Research**
  Mode: deep-dive. Output: `2026-04-07-product-design-ux.research.md`
  Sub-questions:
  - What are current best practices for product design processes (discovery, ideation, prototyping, validation)?
  - How should UX research be structured (qualitative vs. quantitative, usability testing, A/B testing, analytics-informed design)?
  - What design system patterns produce consistent, accessible, and scalable UI at the component level?
  - How should design and engineering collaborate effectively (design tokens, handoff processes, shared component libraries)?
  - How are AI tools changing product design workflows (AI-assisted prototyping, design-to-code, generative UI)?
  Search: product design best practices 2025-2026, UX research methods, design systems at scale, design-engineering collaboration, AI in product design, Figma design system patterns.

  **Topic 8.7: Content Strategy & Content Operations**
  Mode: deep-dive. Output: `2026-04-07-content-strategy.research.md`
  Sub-questions:
  - What are current best practices for content strategy at scale (editorial workflows, content governance, content models)?
  - How should content operations be structured (content calendars, production pipelines, quality gates, style guides)?
  - What content management patterns work for multi-brand, multi-channel publishing?
  - How are AI tools transforming content creation, editing, and optimization (AI-assisted writing, content personalization)?
  - What content performance measurement frameworks connect content investment to business outcomes?
  Search: content strategy best practices 2025-2026, content operations at scale, editorial workflow design, AI content creation, content governance, multi-brand content management.

  **Topic 8.8: AI Product Management**
  Mode: deep-dive. Output: `2026-04-07-ai-product-management.research.md`
  Sub-questions:
  - How does AI product management differ from traditional PM (probabilistic outputs, eval-driven development, non-deterministic roadmaps)?
  - What frameworks exist for prioritizing AI features (value vs. feasibility vs. risk, responsible AI considerations)?
  - How should AI product managers work with engineering on model selection, prompt engineering, and eval pipelines?
  - What are best practices for defining success metrics for AI-powered products (beyond accuracy — user trust, adoption, business impact)?
  - How should AI product managers handle the "agentic" product category (autonomous workflows, human-in-the-loop design)?
  Search: AI product management 2025-2026, product management for LLM applications, agentic product design, AI product metrics, responsible AI product development, AI PM frameworks.

  **Topic 8.9: Sales & Revenue Operations**
  Mode: landscape. Output: `2026-04-07-revenue-operations.research.md`
  Sub-questions:
  - What are current best practices for revenue operations (RevOps) — aligning sales, marketing, and customer success?
  - How should sales pipelines, forecasting, and account management be structured and measured?
  - What CRM and sales tooling patterns (Salesforce, HubSpot) produce reliable revenue data?
  - How do marketplace and affiliate revenue models work (comparison shopping, lead generation, performance marketing)?
  - What client delivery and account management patterns maximize retention and expansion?
  Search: revenue operations best practices 2025-2026, RevOps frameworks, sales pipeline management, marketplace revenue models, affiliate marketing operations, account management patterns.

  Verify: 4 research documents exist with valid frontmatter and sources.

- [ ] **Task 13: Research Cluster 9 — Digital Marketing (6 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 9.1: Marketing Analytics & Attribution**
  Mode: deep-dive. Output: `2026-04-07-marketing-analytics.research.md`
  Sub-questions:
  - What are current best practices for multi-touch attribution modeling (data-driven, algorithmic, Shapley value)?
  - How should marketing mix modeling (MMM) be implemented and what tools are current (Meridian, Robyn, LightweightMMM)?
  - What incrementality testing frameworks measure true causal impact of marketing spend?
  - How should marketing measurement adapt to privacy changes (cookie deprecation, iOS ATT, GA4)?
  - What marketing analytics platforms and data infrastructure patterns support cross-channel measurement?
  Search: marketing attribution 2025-2026, marketing mix modeling tools, incrementality testing, privacy-first measurement, GA4 best practices, Meridian MMM.

  **Topic 9.2: SEO & Content Strategy**
  Mode: deep-dive. Output: `2026-04-07-seo-content-strategy.research.md`
  Sub-questions:
  - What are current technical SEO best practices (Core Web Vitals, structured data, crawl optimization, JS rendering)?
  - How has AI-generated content and AI search (Google AI Overviews, Perplexity, ChatGPT search) changed SEO strategy?
  - What content optimization patterns maximize organic visibility (topical authority, entity optimization, EEAT)?
  - How should programmatic SEO be approached for large-scale content operations?
  - What SEO tooling (Ahrefs, Semrush, Screaming Frog, Surfer) and workflows are current best-in-class?
  Search: SEO best practices 2025-2026, AI impact on SEO, technical SEO patterns, programmatic SEO, content optimization for AI search, EEAT guidelines.

  **Topic 9.3: Paid Media & Ad Tech**
  Mode: deep-dive. Output: `2026-04-07-paid-media.research.md`
  Sub-questions:
  - What are current best practices for paid search (Google Ads, Bing Ads) — bidding strategies, campaign structure, automation?
  - How should paid social campaigns be structured across platforms (Meta, TikTok, LinkedIn, Reddit)?
  - What programmatic advertising patterns and ad tech infrastructure are current (DSPs, SSPs, header bidding)?
  - How should creative testing and optimization be systematized (DCO, creative analytics, fatigue detection)?
  - What measurement and reporting patterns connect paid media spend to business outcomes?
  Search: paid media best practices 2025-2026, Google Ads automation, paid social strategy, programmatic advertising, creative optimization, media measurement.

  **Topic 9.4: Customer Data Platforms & Martech Stack**
  Mode: landscape. Output: `2026-04-07-cdp-martech.research.md`
  Sub-questions:
  - What are current CDP architectures and how should they be evaluated (Segment, mParticle, composable CDPs)?
  - How should identity resolution work across channels and devices in a privacy-first environment?
  - What consent management and data governance patterns comply with GDPR, CCPA, and emerging privacy regulations?
  - How should martech stacks be architected for composability vs. all-in-one platforms?
  - What data activation patterns connect customer data to marketing channels effectively?
  Search: CDP architecture 2025-2026, identity resolution, consent management, martech stack architecture, composable CDP, data activation patterns.

  **Topic 9.5: Marketing Automation & CRM**
  Mode: deep-dive. Output: `2026-04-07-marketing-automation.research.md`
  Sub-questions:
  - What are current best practices for lifecycle marketing (onboarding, engagement, retention, win-back)?
  - How should email deliverability, authentication (DKIM, SPF, DMARC, BIMI), and sender reputation be managed?
  - What segmentation and personalization patterns produce measurable lift?
  - How should marketing automation platforms (HubSpot, Marketo, Braze, Iterable) be evaluated and implemented?
  - What AI-powered personalization and predictive marketing patterns are emerging?
  Search: marketing automation best practices 2025-2026, lifecycle marketing, email deliverability, personalization at scale, Braze/Iterable architecture, AI personalization.

  **Topic 9.6: Conversion Rate Optimization & Experimentation**
  Mode: deep-dive. Output: `2026-04-07-cro-experimentation.research.md`
  Sub-questions:
  - What are current best practices for A/B testing (statistical rigor, sample size, duration, multiple testing correction)?
  - How should experimentation platforms be structured (client-side vs. server-side, feature flags, holdout groups)?
  - What CRO frameworks systematically identify and prioritize optimization opportunities?
  - How should experimentation culture be built and maintained across organizations?
  - What tools (Optimizely, LaunchDarkly, Statsig, Eppo) are current best-in-class and how do they differ?
  Search: A/B testing best practices 2025-2026, experimentation platforms, CRO frameworks, statistical rigor in testing, feature flag architecture, experimentation culture.

  Verify: 6 research documents exist with valid frontmatter and sources.

- [ ] **Task 14: Research Cluster 10 — Data Science & Analytics (6 topics).**
  Invoke `/wos:research` sequentially for each topic:

  **Topic 10.1: Statistical Modeling & Inference**
  Mode: deep-dive. Output: `2026-04-07-statistical-modeling.research.md`
  Sub-questions:
  - What are current best practices for applied statistical modeling (regression, GLMs, mixed models, survival analysis)?
  - How should causal inference be approached in observational data (propensity scoring, DiD, instrumental variables, synthetic control)?
  - What Bayesian methods are practical for business applications (hierarchical models, A/B test analysis, demand forecasting)?
  - How should experimental design be structured for maximum statistical power with minimum sample?
  - What statistical computing tools (R, Python statsmodels/scipy, Stan, PyMC) are current best-in-class?
  Search: applied statistics best practices 2025-2026, causal inference methods, Bayesian methods for business, experimental design, statistical computing tools.

  **Topic 10.2: Machine Learning for Business Applications**
  Mode: deep-dive. Output: `2026-04-07-ml-business-applications.research.md`
  Sub-questions:
  - What ML techniques are most effective for common business problems (classification, recommendation, forecasting, NLP)?
  - How should model selection balance accuracy, interpretability, and operational complexity?
  - What feature engineering and selection practices produce robust production models?
  - How should LLMs/foundation models be applied to business problems (fine-tuning vs. prompting, RAG, agents)?
  - What model monitoring and retraining patterns maintain production model quality?
  Search: ML for business 2025-2026, recommendation systems, demand forecasting ML, NLP for marketing, LLM business applications, model monitoring best practices.

  **Topic 10.3: Data Visualization & Storytelling**
  Mode: technical. Output: `2026-04-07-data-visualization.research.md`
  Sub-questions:
  - What are current best practices for dashboard design (information hierarchy, progressive disclosure, interactivity)?
  - How should data narratives be structured for different audiences (executives, analysts, operations)?
  - What visualization tools (Tableau, Looker, Power BI, Observable, Streamlit) are current and how do they compare?
  - What chart selection and design principles produce accurate, actionable visualizations?
  - How are AI-assisted analytics and natural language querying changing dashboard design?
  Search: data visualization best practices 2025-2026, dashboard design, data storytelling, BI tool comparison, chart selection guide, AI-assisted analytics.

  **Topic 10.4: Customer Analytics**
  Mode: deep-dive. Output: `2026-04-07-customer-analytics.research.md`
  Sub-questions:
  - What are current best practices for customer segmentation (behavioral, value-based, needs-based, ML-driven)?
  - How should customer lifetime value (LTV/CLV) be modeled (contractual vs. non-contractual, probabilistic models)?
  - What churn prediction approaches are most effective and how should prevention programs be structured?
  - How should cohort analysis and customer journey analytics inform product and marketing decisions?
  - What customer analytics platforms and techniques enable real-time personalization?
  Search: customer analytics 2025-2026, customer segmentation ML, CLV modeling, churn prediction, cohort analysis, customer journey analytics.

  **Topic 10.5: Data Governance & Ethics**
  Mode: deep-dive. Output: `2026-04-07-data-governance.research.md`
  Sub-questions:
  - What are current data governance frameworks and how should they be implemented (data catalogs, lineage, quality)?
  - How should privacy regulations (GDPR, CCPA, emerging state laws) be operationalized in data systems?
  - What ethical AI frameworks address bias detection, fairness, and transparency in business applications?
  - How should data access controls, classification, and retention policies be structured?
  - What data governance tooling (Atlan, Collibra, DataHub, OpenMetadata) is current best-in-class?
  Search: data governance best practices 2025-2026, privacy regulation compliance, ethical AI frameworks, bias detection tools, data catalog platforms, data lineage.

  **Topic 10.6: Analytics Engineering**
  Mode: technical. Output: `2026-04-07-analytics-engineering.research.md`
  Sub-questions:
  - What is analytics engineering and how does it bridge data engineering and data analysis?
  - How should metrics layers and semantic layers be designed (dbt metrics, MetricFlow, Cube)?
  - What data modeling patterns for analytics produce self-service-ready datasets (star schema, wide tables, activity schema)?
  - How should data testing and documentation be integrated into analytics workflows?
  - What analytics engineering tools and workflows are current best-in-class?
  Search: analytics engineering 2025-2026, metrics layer design, semantic layer, dbt MetricFlow, data modeling for analytics, analytics engineering workflow.

  Verify: 6 research documents exist with valid frontmatter and sources.

### Phase 3: Validate & Review Research (human gate)

- [ ] **Task 15: Validate all research documents.**
  Run `python scripts/audit.py --root . --no-urls` to check structural
  validity of all research documents. For each document, verify:
  1. Frontmatter present with `type: research`
  2. `sources:` non-empty
  3. `<!-- DRAFT -->` marker removed
  4. `## Findings` section exists
  Fix any failures before proceeding to review.
  Verify: 0 audit failures related to research documents.

- [ ] **Task 16: Present research summaries for user review (HARD GATE).**
  Present a summary of each research document:
  - Title and research question
  - Key findings (count and confidence levels)
  - Source count
  - Limitations or gaps noted
  Ask the user to review research quality and completeness. If the user
  provides feedback on specific documents, apply corrections before
  proceeding. **Do not begin distillation until the user explicitly
  approves the research batch.**
  Verify: User has explicitly approved the research batch.

### Phase 4: Distill (13 cluster tasks, sequential via `/wos:distill`)

For each cluster, invoke `/wos:distill` with the completed research
document paths. The skill handles mapping, writing, and per-file
validation. Execute clusters in order (Task 17 → Task 29). Commit
after each cluster completes.

Follow the distillation rules from the Approach section:
- 1-2 context files per research document, `.context.md` suffix
- 200-800 words, one atomic concept per file
- `sources:` URLs carried forward from research
- `related:` links to sibling context files ONLY (not to research docs)
- Merge overlapping findings across research docs into single context files
- Derive filenames from finding content, not research topic name

- [ ] **Task 17: Distill Cluster 1 — Core LLM Patterns.**
  Invoke `/wos:distill` with the 8 research documents from Task 2.
  Expected output: 10-16 context files covering prompt engineering,
  context engineering, LLM-as-judge evaluation, writing for LLM
  consumption, cross-model portability, LLM capabilities/limitations,
  LLM anti-patterns, and prompting best practices.
  Verify: context files exist with valid frontmatter, 200-800 words each,
  `sources:` populated, `related:` links to sibling context files.

- [ ] **Task 18: Distill Cluster 2 — Developer Tool Architecture.**
  Invoke `/wos:distill` with the 6 research documents from Task 3.
  Expected output: 7-12 context files covering instruction file conventions,
  skill ecosystem design, plugin architecture, CLI/tool design, MCP, and
  hooks ecosystem.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 19: Distill Cluster 3 — Knowledge Management.**
  Invoke `/wos:distill` with the 4 research documents from Task 4.
  Expected output: 5-8 context files covering information architecture,
  knowledge synthesis, research methodology, and convention-driven design.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 20: Distill Cluster 4 — Agent System Design.**
  Invoke `/wos:distill` with the 6 research documents from Task 5.
  Expected output: 8-14 context files covering agent frameworks, multi-agent
  coordination, error handling, human-in-the-loop, git workflow, and
  agentic planning/execution.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 21: Distill Cluster 5A — Quality & Validation.**
  Invoke `/wos:distill` with the 5 research documents from Task 6.
  Expected output: 6-10 context files covering validation, testing,
  decision frameworks, observability, and feedback loops.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 22: Distill Cluster 5B — Practices & Standards.**
  Invoke `/wos:distill` with the 5 research documents from Task 7.
  Expected output: 6-10 context files covering rule enforcement,
  design thinking, specification patterns, LLM security, and CI/CD.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 23: Distill Cluster 5C — Engineering Disciplines.**
  Invoke `/wos:distill` with the 6 research documents from Task 8.
  Expected output: 8-12 context files covering AI code review, prompt
  versioning, token economics, AI pair programming, documentation-driven
  development, and technical debt management.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 24: Distill Cluster 6 — Application Engineering.**
  Invoke `/wos:distill` with the 6 research documents from Task 9.
  Expected output: 8-12 context files covering data engineering, frontend,
  backend/API, mobile, database, and distributed systems engineering.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 25: Distill Cluster 7 — Operations & Platform.**
  Invoke `/wos:distill` with the 5 research documents from Task 10.
  Expected output: 6-10 context files covering SRE, platform engineering,
  DevOps/IaC, cloud architecture, and ML engineering/MLOps.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 26: Distill Cluster 8A — Cross-Cutting & Management.**
  Invoke `/wos:distill` with the 5 research documents from Task 11.
  Expected output: 6-10 context files covering QA engineering, performance
  engineering, accessibility, project management, and program management.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 27: Distill Cluster 8B — Product, Content & Revenue.**
  Invoke `/wos:distill` with the 4 research documents from Task 12.
  Expected output: 5-8 context files covering product design/UX, content
  strategy/operations, AI product management, and sales/revenue operations.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 28: Distill Cluster 9 — Digital Marketing.**
  Invoke `/wos:distill` with the 6 research documents from Task 13.
  Expected output: 8-12 context files covering marketing analytics,
  SEO/content, paid media, CDPs/martech, marketing automation, and CRO.
  Verify: context files exist with valid frontmatter, 200-800 words each.

- [ ] **Task 29: Distill Cluster 10 — Data Science & Analytics.**
  Invoke `/wos:distill` with the 6 research documents from Task 14.
  Expected output: 8-12 context files covering statistical modeling,
  ML for business, data visualization, customer analytics, data governance,
  and analytics engineering.
  Verify: context files exist with valid frontmatter, 200-800 words each.

### Phase 5: Validate Distill & Cleanup

- [ ] **Task 30: Validate all distilled context files.**
  Run `python scripts/reindex.py --root .` to regenerate indexes.
  Run `python scripts/audit.py --root . --no-urls` to check structural
  validity of all context files. Verify:
  1. Each context file has valid frontmatter (name, description, sources)
  2. `related:` links point to sibling context files ONLY (not research docs)
  3. `_index.md` files match directory contents
  4. Word counts are 200-800 per context file
  Present results to user. Fix any failures before cleanup.
  Verify: 0 audit failures related to context files.

- [ ] **Task 31: Delete research docs, final audit.**
  Delete all research documents created in Tasks 2-14 (their value is
  captured in the distilled context files). Context files should have
  no `related:` links to research docs (distillation rules prevent this),
  so deletion should cause zero broken links. Run:
  ```
  python scripts/reindex.py --root .
  python scripts/audit.py --root . --no-urls
  python -m pytest tests/ -v
  ```
  If any audit issues arise, fix them (likely index sync only).
  Verify: 0 audit failures related to new content. All tests pass.
  No research documents remain in `docs/research/` (except `_index.md`).
  `grep -r "docs/research/" docs/context/` returns no results.

## Validation

1. **Coverage complete:** Every WOS skill and Python module maps to at
   least one context file. Verify by listing skills and confirming each
   has a supporting context document.

2. **Audit clean:** `python scripts/audit.py --root . --no-urls` produces
   0 failures and 0 warnings related to context files.

3. **Tests pass:** `python -m pytest tests/ -v` — no regressions.

4. **No stale references:** `grep -r "docs/research/" docs/context/`
   returns no results (all research links removed after deletion).

5. **Word count targets:** All context files are 200-800 words.
   `find docs/context -name "*.md" -exec wc -w {} \;` shows no outliers.

6. **Source freshness:** Spot-check 5 random context files — each should
   cite at least one 2025-2026 source.
