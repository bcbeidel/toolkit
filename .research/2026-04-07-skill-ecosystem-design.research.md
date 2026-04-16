---
name: "Skill Ecosystem Design & Composition"
description: "How AI coding tools implement skill/command systems and patterns for skill composition, granularity, and the skill/agent/tool taxonomy"
type: research
sources:
  - https://code.claude.com/docs/en/skills
  - https://agentskills.io/specification
  - https://agentskills.io
  - https://developers.openai.com/codex/skills
  - https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
  - https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/
  - https://docs.cursor.com/context/rules-for-ai
  - https://arxiv.org/html/2602.12430v3
  - https://www.llamaindex.ai/blog/skills-vs-mcp-tools-for-agents-when-to-use-what
  - https://dev.to/phil-whittaker/mcp-vs-agent-skills-why-theyre-different-not-competing-2bc1
  - https://cra.mr/mcp-skills-and-agents/
  - https://medium.com/data-science-collective/using-skills-with-cline-3acf2e289a7c
  - https://www.patronus.ai/ai-agent-development/ai-agent-routing
  - https://medium.com/data-science-collective/intent-driven-natural-language-interface-a-hybrid-llm-intent-classification-approach-e1d96ad6f35d
  - https://calmops.com/ai/ai-agent-skills-complete-guide-2026/
  - https://spring.io/blog/2026/01/13/spring-ai-generic-agent-skills/
related:
  - docs/research/2026-04-07-instruction-file-conventions.research.md
---

## Research Question

How should skill ecosystems for AI coding tools be designed? What patterns govern skill composition, granularity calibration, and the relationship between skills, agents, tools, and MCP servers?

## Sub-Questions

1. How do AI coding tools implement skill/command systems (Claude Code skills, Codex skills, Cursor rules, Cline MCP-first)?
2. What patterns exist for skill composition (skills referencing other skills, shared references, skill chains)?
3. How should skill granularity be calibrated (too fine = overhead, too coarse = inflexible)?
4. What is the relationship between skills, agents, tools, and MCP servers in the current landscape?
5. How do intent classification and mode selection work in skill-based systems?

## Search Protocol

| # | Query | Key Finding |
|---|-------|-------------|
| 1 | `Claude Code custom skills slash commands implementation 2025 2026` | Official docs at code.claude.com/docs/en/skills; Agent Skills open standard published Dec 2025 |
| 2 | `MCP Model Context Protocol skill patterns tools servers 2025` | MCP primitives (tools/resources/prompts); 97M+ monthly SDK downloads; donated to Linux Foundation AAIF Dec 2025 |
| 3 | `Cursor rules AI coding tool command system 2025` | .cursor/rules directory; project-level + team-level rules; .cursorrules file |
| 4 | `OpenAI Codex AGENTS.md skills section agent instructions 2025` | AGENTS.md skills format; $-notation invocation; if/then rule patterns; openai/skills GitHub catalog |
| 5 | `skill granularity AI agents composition patterns 2025` | Limited direct results; redirected to tool-calling and orchestration literature |
| 6 | `agent skill composition chain orchestration patterns LLM tool calling 2025 2026` | arxiv 2602.12430 survey on skill architecture; Spring AI modular skills; LangGraph orchestration |
| 7 | `skills vs tools vs agents vs MCP taxonomy AI coding assistant architecture 2025` | Multiple practitioner comparisons; consensus taxonomy emerging |
| 8 | `Cline MCP first approach skill tools agent architecture 2025` | Cline added Agent Skills experimentally; MCP-first converted to skills via modular decomposition |
| 9 | `GitHub Copilot agent skills VS Code implementation 2025 2026` | VS Code 1.108 Dec 2025 added experimental Agent Skills; .github/skills discovery |
| 10 | `intent classification mode selection "developer tools" "routing" LLM skill activation 2025 2026` | Three routing approaches: rule-based, ML-based, LLM-based; semantic embedding routing; hybrid FAISS pattern |
| 11 | `"skill chaining" OR "skill composition" AI coding agent workflow 2025 2026` | SkillComposer/Workflow patterns; Superpowers framework; sequential and conditional chaining |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/skills | Extend Claude with skills | Anthropic | 2025-2026 | T1 | verified |
| 2 | https://agentskills.io/specification | Specification - Agent Skills | Anthropic / agentskills.io | Dec 2025 | T1 | verified |
| 3 | https://agentskills.io | Agent Skills Open Standard Overview | Anthropic / agentskills.io | Dec 2025 | T1 | verified |
| 4 | https://developers.openai.com/codex/skills | Agent Skills - Codex | OpenAI | 2025-2026 | T1 | verified |
| 5 | https://docs.github.com/en/copilot/concepts/agents/about-agent-skills | About agent skills | GitHub (Microsoft) | Dec 2025 | T1 | verified |
| 6 | https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/ | GitHub Copilot now supports Agent Skills | GitHub | Dec 18, 2025 | T1 | verified |
| 7 | https://docs.cursor.com/context/rules-for-ai | Cursor - Rules for AI | Cursor | 2025 | T1 | verified |
| 8 | https://arxiv.org/html/2602.12430v3 | Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward | arxiv (academic survey) | Feb 2026 | T2 | verified |
| 9 | https://www.llamaindex.ai/blog/skills-vs-mcp-tools-for-agents-when-to-use-what | Skills vs MCP tools for agents: when to use what | LlamaIndex | 2025 | T3 | verified |
| 10 | https://dev.to/phil-whittaker/mcp-vs-agent-skills-why-theyre-different-not-competing-2bc1 | MCP vs Agent Skills: Why They're Different, Not Competing | Phil Whittaker / DEV.to | 2025-2026 | T3 | verified |
| 11 | https://cra.mr/mcp-skills-and-agents/ | MCP, Skills, and Agents | cra.mr | 2025-2026 | T3 | verified |
| 12 | https://medium.com/data-science-collective/using-skills-with-cline-3acf2e289a7c | Using Skills with Cline. And converting an MCP server to Skills | Harry Snart / Medium | 2025-2026 | T3 | verified |
| 13 | https://www.patronus.ai/ai-agent-development/ai-agent-routing | AI Agent Routing: Tutorial & Best Practices | Patronus AI | 2025 | T3 | verified |
| 14 | https://medium.com/data-science-collective/intent-driven-natural-language-interface-a-hybrid-llm-intent-classification-approach-e1d96ad6f35d | Intent-Driven Natural Language Interface: A Hybrid LLM + Intent Classification Approach | Anil Malkani / Medium | 2025 | T3 | verified |
| 15 | https://calmops.com/ai/ai-agent-skills-complete-guide-2026/ | AI Agent Skills Complete Guide 2026 | CalmOps | 2026 | T3 | verified |
| 16 | https://spring.io/blog/2026/01/13/spring-ai-generic-agent-skills/ | Spring AI Agentic Patterns (Part 1): Agent Skills | Spring.io | Jan 2026 | T3 | verified |

## Raw Extracts

### Sub-question 1: How do AI coding tools implement skill/command systems?

**Claude Code (Anthropic)**

Skills are the primary extensibility mechanism. A skill is a directory with a required `SKILL.md` (YAML frontmatter + markdown instructions) and optional supporting files (`scripts/`, `references/`, `assets/`). The `name` field (becomes `/slash-command`) and `description` field (Claude uses this for auto-invocation matching) are the core routing metadata.

Key design decisions:
- **Unified custom commands**: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. Skills are preferred going forward as they support additional features.
- **Discovery scopes**: enterprise > personal (`~/.claude/skills/`) > project (`.claude/skills/`) > plugin. Same-name skills at higher-priority levels win.
- **Monorepo support**: Nested `.claude/skills/` in subdirectories are auto-discovered when working in those paths.
- **Bundled skills**: Anthropic ships 5 bundled skills (`/batch`, `/claude-api`, `/debug`, `/loop`, `/simplify`) as prompt-based playbooks, not fixed-logic commands.
- **Progressive loading**: Skill descriptions always in context; full `SKILL.md` body loads only when invoked. This is the critical token-efficiency mechanism.
- **Subagent execution**: `context: fork` in frontmatter runs skill in an isolated subagent with separate context window.
- **Dynamic context injection**: `` !`command` `` syntax executes shell commands before the skill content reaches Claude, injecting live output.
- **Invocation control**: `disable-model-invocation: true` = human-only; `user-invocable: false` = Claude-only background knowledge.

**OpenAI Codex**

Codex skills follow the same Agent Skills open standard but add `agents/openai.yaml` for UI metadata. Invocation happens via explicit `/skills` command or `$skill-name` notation in AGENTS.md. AGENTS.md can contain if/then rules mandating skill use: "call $implementation-strategy before editing runtime changes." Best practice: keep each skill focused on one job, prefer instructions over scripts unless deterministic behavior is needed.

**GitHub Copilot / VS Code**

Added experimental Agent Skills in VS Code 1.108 (December 2025). Discovery from `.github/skills/`, `.claude/skills/`, or `.agents/skills/`. Works across Copilot cloud agent, CLI, and VS Code agent mode. Implementation follows the same open standard.

**Cursor**

Cursor adopted full Agent Skills support in version 2.4 (January 22, 2026) and is listed on agentskills.io. Prior to this, Cursor used a rules-based system: `.cursor/rules/` directory and `.cursorrules` at root. As of v2.4, both systems are supported—the rules system for contextual guidelines and Agent Skills for on-demand loadable skill packages. Team admins can create organization-wide rules via dashboard.

**Cline**

Cline added experimental Agent Skills support in 2025-2026. Supports three directory levels: global (`~/.cline/skills`), project (`.cline/skills/`), legacy (`.clinerules/skills/`, `.claude/skills/`). Cline's original architecture was MCP-first (tool-use at its core), but skills were added as a complementary layer. Skills are preferred over MCP for local, context-efficient workflows.

**Agent Skills Open Standard (agentskills.io)**

Anthropic published Agent Skills as an open standard on December 18, 2025. The standard is now supported by 30+ tools including: Claude Code, OpenAI Codex, GitHub Copilot, VS Code, Cursor, Gemini CLI, Cline, JetBrains Junie, Roo Code, OpenHands, Letta, Goose, Spring AI, Databricks Genie Code, Snowflake Cortex Code, Kiro, and many others.

Minimal required fields per spec: `name` (max 64 chars, lowercase+hyphens only) and `description` (max 1024 chars). Optional: `license`, `compatibility`, `metadata`, `allowed-tools`. The spec deliberately avoids composition primitives at the standard level—each agent implementation handles chaining.

---

### Sub-question 2: What patterns exist for skill composition?

**Composition via subagents (Claude Code)**

The primary composition mechanism in Claude Code is `context: fork`. A skill runs in an isolated subagent, and results are summarized back to the main conversation. The subagent can itself invoke other skills (if preloaded via the `skills` field on the subagent definition). This enables **skill → subagent → skill chains**, but the orchestration is LLM-driven rather than declarative.

**Composition via AGENTS.md if/then rules (Codex)**

Codex AGENTS.md supports conditional mandatory composition: rules like "call $implementation-strategy before editing runtime changes" create enforced skill sequences. This is a deterministic, rule-authored composition layer sitting above the LLM's own routing choices.

**Composition via SkillComposer/Workflow pattern (practitioner)**

The CalmOps guide documents a code-level `SkillComposer` pattern with `Workflow` classes where multi-step workflows map outputs from previous steps as inputs to subsequent ones. Skills chain sequentially with conditional execution and configurable error-handling (stop vs. continue). Example pipeline: data collection → analysis → document generation → formatting.

**Composition via shared references**

The Agent Skills spec recommends keeping file references one level deep from `SKILL.md` and avoiding deeply nested reference chains. Skills can reference shared documentation or scripts in a plugin's shared directory, but there is no standard mechanism for one SKILL.md to declaratively call another SKILL.md. Composition is achieved through:
- Mentioning other skills by name in instructions (LLM interprets and invokes)
- Running scripts that trigger skill invocations
- Subagent patterns that preload multiple skills

**Composition via plugin namespacing**

Claude Code plugin skills use `plugin-name:skill-name` namespace. This prevents collision with project/personal skills and enables co-deployment of composable skill suites as a single distributable unit.

**arxiv survey finding on composition**

The 2026 survey (arxiv 2602.12430) identifies composition mechanisms as "underdeveloped" but promising:
- CUA-Skill uses **composition graphs** with typed parameters and preconditions (structured, declared composition)
- Agentic Proposing uses **dynamic composition** during problem-solving (LLM-driven)
- Key gap: "multi-skill orchestration—including conflict resolution, resource sharing, and failure recovery—remain underdeveloped"

---

### Sub-question 3: How should skill granularity be calibrated?

**Official guidance (Agent Skills spec)**

- Keep `SKILL.md` under 500 lines—move detailed reference material to separate files
- Progressive disclosure: metadata (~100 tokens) at startup, instructions (<5000 tokens recommended) when activated, resources only on-demand
- Good description front-loads the key use case; descriptions >250 characters are truncated in skill listings

**Official guidance (Codex)**

"Keep each skill focused on one job." Prefer instructions over scripts unless deterministic behavior or external tooling is required. Write imperative steps with explicit inputs and outputs.

**arxiv survey finding (2602.12430)**

Identifies a **critical scaling limitation**: "a phase transition in skill selection accuracy as library size grows." Beyond certain library sizes, routing accuracy degrades sharply. This creates an upper bound on effective ecosystem size and argues against excessive fine-grained decomposition that multiplies skill count without improving coverage.

**Practitioner experience (Cline MCP→Skills conversion)**

Converting an OCI Data Science MCP server to skills: created domain-specific skills (projects, notebooks, jobs/pipelines) rather than monolithic or per-function implementations. Enabling granularity at the domain level (not the tool level) enabled selective toggling and independent updates while avoiding the overhead of matching each MCP tool to a skill.

**LlamaIndex finding**

Skills "were rarely invoked, and often did not yield substantially better results" when MCP documentation access was already available. This suggests skills at the micro-task level add overhead without proportional benefit—granularity should match the boundary of meaningful procedural knowledge, not API surface area.

**Calibration heuristics (synthesized from sources)**

- Too fine: one skill per API endpoint or per file type → excessive skill count, routing degradation, context pollution with many descriptions
- Too coarse: one skill per major domain (e.g., "all deployment tasks") → inflexible, can't selectively disable or update parts
- Sweet spot: one skill per **coherent workflow or domain of expertise** that a practitioner would naturally hand off as a unit of work
- Use `user-invocable: false` for sub-workflow reference knowledge; reserve explicitly invocable skills for actionable, user-facing workflows

---

### Sub-question 4: Relationship between skills, agents, tools, and MCP servers

**Consensus taxonomy (2025-2026)**

The following definitions have emerged as a rough consensus across Anthropic, OpenAI, LlamaIndex, and multiple practitioners:

| Layer | What it is | Context cost | Determinism | Primary use |
|-------|-----------|--------------|-------------|-------------|
| Tools | Atomic functions (single input/output API call) | Low per-call | High | Discrete actions: read file, search, run command |
| MCP servers | Protocol-based service adapters exposing tools/resources/prompts | Medium (per-use) | High | Third-party service integration, auth, data access |
| Skills | Instruction bundles with progressive disclosure | Low at rest, medium when active | Low (LLM-driven) | Procedural knowledge, workflows, behavioral guidance |
| Sub-agents | Isolated agents with separate context windows | High (full fork) | Medium | Complex isolated tasks, parallel workstreams |

**Key architectural insight from cra.mr**

"Both skills and MCP—when used incorrectly—will cause context pollution." The right model:
- **Skills** = the brain (procedural knowledge, decision criteria, standing instructions)
- **MCP** = the muscle (deterministic execution, service connectivity)
- **Sub-agents** = map/reduce for complex, isolated subtasks

**MCP progressive discovery (Jan 2026)**

MCPs adopted progressive discovery in January 2026, reducing token overhead by 85% for 50+ tool setups. This eliminated Skills' original token-efficiency advantage, making the choice between MCP and Skills primarily about determinism vs. adaptability, not context overhead.

**LlamaIndex comparison**

- MCP: "functional interface, executes specific logic under specific conditions"
- Skills: "contextual modification, injecting custom instructions to the agent's context"

MCP wins for fast-evolving codebases needing current examples. Skills win for stable, infrequently-changing contexts where behavioral guidance matters.

**A skill may invoke MCP**

Skills and MCP are orthogonal and composable: "A skill might instruct the agent to use a particular MCP server, specify how to interpret its outputs, and define fallback strategies if the connection fails." Skills provide the procedural intelligence; MCP provides the connectivity.

**Security finding (arxiv survey)**

26.1% of 42,447 community skills contain vulnerabilities. Skills with executable scripts are 2.12× more likely to contain vulnerabilities. Attack vectors: prompt injection, data exfiltration (13.3%), privilege escalation (11.8%). The survey proposes a four-tier Skill Trust and Lifecycle Governance Framework with verification gates (static analysis, semantic classification, behavioral sandboxing, permission validation).

---

### Sub-question 5: Intent classification and mode selection in skill-based systems

**How Claude Code routes to skills**

Claude Code uses two mechanisms:
1. **Auto-invocation**: All skill descriptions are loaded into context at session start. Claude matches the user's message against descriptions and loads relevant skills. This is a context-window-based semantic match, not a separate classifier.
2. **Explicit invocation**: User types `/skill-name`; bypasses auto-routing entirely.

`disable-model-invocation: true` removes the skill from context entirely (description not shown), preventing auto-routing. This is the mechanism to opt a skill out of the routing pool.

**Three routing approaches in the broader literature**

1. **Rule-based**: Hard-coded keyword/pattern matching. Fast and deterministic; brittle to novel phrasings.
2. **ML-based**: Supervised classifier trained on routing datasets. More flexible; requires labeled data.
3. **LLM-based** (current state-of-the-art): Pre-trained knowledge + prompt engineering. Best generalization; highest latency and cost for the routing call itself.

**Semantic embedding routing (emerging 2025-2026)**

Pre-encode example utterances per intent; route by nearest-neighbor in embedding space (FAISS-style). This decouples routing from LLM inference: "Zero-shot generalization: Easily extensible by adding more labeled examples without retraining." Lower latency than full LLM call; portable across model providers.

**Hybrid architecture pattern (Malkani 2025)**

1. Embedding-based intent classification (semantic routing)
2. FAISS-based semantic retrieval (template matching)
3. Template-driven output (deterministic for high-confidence matches)
4. Schema-guided LLM fallback (for ambiguous cases)

Reserves LLM invocation only when templates cannot safely resolve queries—preventing hallucinated outputs while maintaining flexibility.

**SkillRouter pattern (CalmOps)**

A `SkillRouter` class matches requests to skills through routing rules based on detected intent or context conditions. Enables dynamic skill selection for multi-step workflows where the correct skill sequence cannot be predetermined.

**Key design principle for skill descriptions**

The description is the routing signal. Claude Code: "Front-load the key use case; each description entry is capped at 250 characters regardless of budget." OpenAI Codex: "Include specific keywords that help agents identify relevant tasks." The description IS the classifier input—quality of routing is directly coupled to description quality.

**Routing degradation at scale**

The arxiv survey identifies a phase transition in skill selection accuracy as skill library size grows. This creates a practical ceiling on how large a skill ecosystem can be before routing reliability degrades. Mitigation strategies: aggressive description front-loading, scoping skills to paths/contexts (Claude Code `paths:` field), and using `user-invocable: false` to remove reference skills from the routing pool.

---

## Findings

### Agent Skills is the emerging cross-platform skill standard, published December 2025

Anthropic published the Agent Skills open standard on December 18, 2025 (donated to AAIF alongside MCP). As of April 2026, 30+ tools support it including Claude Code, Codex, GitHub Copilot, VS Code, Cursor (v2.4, Jan 2026), Cline, Gemini CLI, and many others [1][2][3]. The standard requires only `name` and `description` frontmatter in a SKILL.md file. HIGH confidence for the standard's existence and adoption; MODERATE confidence for breadth (some listed tools may not implement the full spec).

### Progressive loading is the token-efficiency mechanism: descriptions in context, bodies loaded on activation

All tools implementing Agent Skills use progressive loading — skill descriptions (~100 tokens) are loaded into context at session start; the full SKILL.md body (~5000 tokens) only loads when the skill is invoked [1][2]. This is the core design that makes large skill ecosystems feasible. HIGH confidence (T1 sources converge). Implication for skill authors: the description IS the routing signal and must front-load the key use case clearly.

### Skills, MCP servers, tools, and sub-agents are orthogonal layers

The consensus taxonomy (2025-2026): Tools = atomic functions; MCP servers = protocol-based service adapters; Skills = instruction bundles with progressive disclosure; Sub-agents = isolated context forks [9][10][11]. A skill may instruct use of an MCP server — they are composable, not competing. The correct mental model: skills are the brain (procedural knowledge), MCP is the muscle (deterministic execution), sub-agents are map/reduce for complex isolated tasks. HIGH confidence.

### Skill granularity: one skill per coherent workflow, not per API endpoint

Too fine (one skill per function) causes routing degradation as library size grows — the arxiv 2026 survey [8] identifies a phase transition in skill selection accuracy beyond certain library sizes. Too coarse (one skill per domain) makes selective toggling impossible. The sweet spot: one skill per coherent workflow that a practitioner would naturally hand off as a unit of work. Keep SKILL.md under 500 lines; use `user-invocable: false` for reference knowledge not intended for the routing pool. HIGH confidence from multiple sources converging.

### Skill composition has no standard primitive; it happens via LLM routing or code patterns

The Agent Skills spec deliberately omits composition primitives — no declarative "skill A calls skill B" mechanism exists in the standard [2]. Composition patterns: `context: fork` (subagent-based, Claude Code), AGENTS.md if/then rules (Codex), code-level SkillComposer/Workflow patterns (practitioner), and implicit LLM routing by name. MODERATE confidence; this is an active gap identified by both the arxiv survey and practitioners.

### Security: over a quarter of community skills contain vulnerabilities

An empirical study (arxiv 2601.10338) analyzed 31,132 community skills and found 26.1% contain vulnerabilities [8]. Skills with executable scripts are 2.12× more likely to be vulnerable. Primary attack vectors: prompt injection, data exfiltration (13.3%), privilege escalation (11.8%). HIGH confidence for the directional finding; MODERATE for specific percentages (single study).

### Key canonical tools and references

- **Agent Skills spec:** https://agentskills.io/specification — minimal required fields, routing design rationale
- **Claude Code skills docs:** https://code.claude.com/docs/en/skills — progressive loading, `context: fork`, invocation control
- **arxiv survey:** https://arxiv.org/html/2602.12430v3 — architecture, scaling, security landscape
- **Routing patterns:** https://www.patronus.ai/ai-agent-development/ai-agent-routing — embedding-based vs LLM-based routing tradeoffs

## Challenge

### Claim 1: "Agent Skills open standard is supported by 30+ tools" — MODERATE confidence

**Finding:** The "30+" count is broadly accurate but requires qualification. The agentskills.io homepage carousel currently lists 33 named tools, confirming the numeric claim. However, the count conflates meaningfully different levels of support:

- Several entries (Piebald, Agentman) link to documentation pages with no `instructionsUrl` pointing to a specific skills implementation guide — presence in the carousel does not confirm the spec is actually implemented.
- Third-party aggregators (serenities.ai, inference.sh) report "16+" and "26+" in articles from early 2026, suggesting the 30+ number reflects recent additions and the count was lower for most of the period covered by this research.
- The carousel is a marketing artifact controlled by agentskills.io (an Anthropic-originated site). Tools self-submit for listing; there is no independent verification gate.

**Assessment:** The headline figure is directionally correct as of April 2026 but was lower (16-26) through most of the period this document covers. Describing all listed tools as "supporting" the spec overstates the depth of implementation for several entries.

---

### Claim 2: "Skills are preferred over MCP for local, context-efficient workflows" — LOW consensus signal

**Finding:** This framing is Cline/Anthropic-ecosystem-specific and does not represent broad industry consensus.

- The document states this as a general finding, but the sourced claim originates from a single Medium article about Cline (Source 12) and the LlamaIndex blog (Source 9) — both ecosystem-adjacent perspectives.
- The LlamaIndex source actually undermines the claim: it found that when MCP documentation access was already available, skills "were rarely invoked and often did not yield substantially better results."
- Simon Willison's widely-read analysis framed skills as complementary to MCP, not preferred over it. Armin Ronacher (lucumr.pocoo.org) argued the choice is architectural, not a preference hierarchy.
- MCP's progressive discovery adoption in Jan 2026 (see Claim 4) specifically eliminated the token-efficiency basis for this preference, making it even less defensible as a general recommendation.
- OpenAI, GitHub Copilot, and VS Code do not express a preference for skills over MCP; they treat them as orthogonal layers.

**Assessment:** "Preferred over MCP" reflects Cline's original MCP-first architecture being supplemented by skills, and Anthropic's incentive to promote skills adoption. It should not be presented as cross-platform consensus.

---

### Claim 3: "AGENTS.md was released by OpenAI in August 2025" — LOW verifiability

**Finding:** The August 2025 date cannot be independently confirmed from primary sources and is likely imprecise.

- OpenAI's Codex research preview launched May 16, 2025, with AGENTS.md featured from the initial launch announcement — making May 2025 the earliest documented public appearance, not August.
- The agents.md website and the Linux Foundation AAIF announcement (December 2025) both describe AGENTS.md as emerging from "collaborative efforts" without attributing first publication to a specific date or organization.
- No primary source (OpenAI blog, GitHub commit history, changelog) surfaces "August 2025" as a release date. The document cites no source for this specific claim.
- The distinction matters: if AGENTS.md was present at Codex's May 2025 launch, then the "August 2025" date is off by ~3 months and misattributes the origin story.

**Assessment:** The claim is unverified against primary sources. May 2025 (Codex launch) is better supported. The document should flag this date as unconfirmed.

---

### Claim 4: "MCP progressive discovery in Jan 2026 reduced token overhead by 85%" — MODERATE; specific attribution unverified

**Finding:** The 85% figure and the "Jan 2026" date reflect real patterns but the specific attribution is a synthesis inference, not a verifiable primary source claim.

- Progressive disclosure patterns for MCP are real and well-documented. The matthewkruczek.ai benchmark shows an 85% reduction (77,000 → 8,700 tokens) for 50+ tool setups using a progressive disclosure meta-tool pattern.
- The GitHub jchip/mcpu project (independent, not Anthropic) claims "up to 90% token reduction" via progressive discovery.
- However, there is no Anthropic announcement or MCP spec update dated "January 2026" that formally adopted progressive discovery. The 85% stat comes from a practitioner benchmark, not an official MCP protocol change.
- Multiple independent implementations achieve 85-100x reductions, suggesting the technique works — but attributing it to a specific "MCP adopted X in Jan 2026" event overstates the formality of adoption.

**Assessment:** The efficiency gain is real and the 85% figure is plausible, but the framing as a discrete "MCP adopted progressive discovery in January 2026" event is not traceable to a primary source. It reads as a synthesis of practitioner blog posts rather than a documented protocol change.

---

### Claim 5: "26.1% of 42,447 community skills contain vulnerabilities" — MODERATE; denominator is wrong

**Finding:** This is a partial mischaracterization of the source paper. The 26.1% rate applies to the 31,132 analyzed skills, not the 42,447 collected.

- arxiv 2601.10338 (the empirical security study) collected 42,447 skills from two marketplaces but analyzed 31,132 using the SkillScan framework. The 26.1% vulnerability rate applies to the analyzed subset.
- Saying "26.1% of 42,447" implies ~11,080 vulnerable skills; the correct reading is 26.1% of 31,132 ≈ 8,125 vulnerable skills — a meaningful numerical difference.
- The core security finding (over a quarter of analyzed skills contain vulnerabilities, skills with scripts are 2.12× more likely) is accurately represented.
- Note: the document cites 2602.12430 (the survey paper) as the source, but this finding actually originates in a different paper, 2601.10338 ("Agent Skills in the Wild"). The survey paper cites the empirical study; this is a citation chain issue.

**Assessment:** The directional finding (serious vulnerability prevalence) is accurate. The denominator is wrong (31,132 analyzed, not 42,447 collected), and the source citation should point to 2601.10338, not 2602.12430.

---

### Claim 6: "Cursor remains a rule-based outlier" — INACCURATE as of early 2026

**Finding:** Cursor adopted the Agent Skills standard in version 2.4, released January 22, 2026. This directly contradicts the claim.

- Cursor 2.4 (January 22, 2026) added full Agent Skills support in both the editor and CLI. SKILL.md files are now supported including frontmatter fields, scripts directory, and slash command invocation.
- Cursor is listed on agentskills.io with a dedicated `instructionsUrl` pointing to `cursor.com/docs/context/skills`.
- Cursor forum posts from January-February 2026 confirm active user adoption and official support.
- The document's characterization of Cursor as a "rule-based outlier" and "pre-skills-standard approach" was accurate when researched but became inaccurate before the document was completed (the research period overlaps the Cursor 2.4 release).

**Assessment:** This claim is factually wrong as of January 22, 2026. Cursor is no longer a rule-based outlier — it fully implements the Agent Skills standard. The document needs correction, not just a caveat.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Agent Skills open standard published December 18, 2025 | date | [2][3][6] | verified |
| 2 | 30+ tools support the Agent Skills standard as of April 2026 | statistic | [2][3] | verified — directionally correct; count was 16–26 for most of the research period; carousel is self-reported, not independently verified (see Challenge §1) |
| 3 | Skill descriptions load ~100 tokens at startup; full SKILL.md body ~5000 tokens on activation | statistic | [1][2] | verified — T1 sources converge on progressive loading design |
| 4 | GitHub Copilot / VS Code added experimental Agent Skills in VS Code 1.108, December 2025 | date/attribution | [5][6] | verified — GitHub Copilot changelog dated Dec 18, 2025 confirms VS Code 1.108 |
| 5 | Cursor adopted Agent Skills in version 2.4, January 22, 2026 | date/attribution | [7] + Challenge §6 | verified — corrected in Challenge §6; earlier claim of "rule-based outlier" was inaccurate |
| 6 | MCP SDK has 97M+ monthly downloads | statistic | Search Protocol row 2 (no numbered source) | human-review — cited in Search Protocol only; no numbered source entry; T-tier unassigned |
| 7 | 26.1% of 31,132 analyzed community skills contain vulnerabilities | statistic | arxiv 2601.10338 (cited via [8]) | corrected — original text said "42,447"; correct denominator is 31,132 analyzed skills; 42,447 was total collected (see Challenge §5) |
| 8 | Skills with executable scripts are 2.12× more likely to contain vulnerabilities | statistic | arxiv 2601.10338 (cited via [8]) | verified — directional finding accurately represented; primary citation should be 2601.10338 not 2602.12430 |
| 9 | Data exfiltration accounts for 13.3% of attack vectors; privilege escalation 11.8% | statistic | arxiv 2601.10338 (cited via [8]) | human-review — figures appear in Findings but source citation points to survey paper [8] not the primary empirical paper 2601.10338 |
| 10 | AGENTS.md released by OpenAI in August 2025 | date/attribution | none cited | corrected — no primary source supports August 2025; OpenAI Codex launched May 16, 2025 with AGENTS.md present from launch; May 2025 is better supported (see Challenge §3) |
| 11 | MCP progressive discovery in January 2026 reduced token overhead by 85% for 50+ tool setups | statistic/date | practitioner benchmark (matthewkruczek.ai), no numbered source | corrected — 85% figure is a practitioner benchmark, not an official MCP spec change; no Anthropic announcement dated January 2026 exists for this (see Challenge §4) |
| 12 | Agent Skills spec requires name ≤ 64 chars (lowercase + hyphens) and description ≤ 1024 chars | statistic | [2] | verified — T1 spec source |
| 13 | Anthropic ships 5 bundled skills: /batch, /claude-api, /debug, /loop, /simplify | statistic/attribution | [1] | verified — T1 official Claude Code docs |
| 14 | arxiv 2026 survey identifies a "phase transition" in skill selection accuracy as library size grows | attribution | [8] | verified — T2 academic source; framing as "phase transition" matches survey language |
| 15 | MCP donated to the Linux Foundation AAIF alongside Agent Skills in December 2025 | date/attribution | Search Protocol row 2 (no numbered source) | human-review — noted in Search Protocol but no numbered source entry covers the AAIF donation; agentskills.io [2][3] covers the standard's publication without explicitly confirming the Linux Foundation donation date |

---

### What This Research Does Not Cover

- **Skill revocation and versioning**: No discussion of how skills are updated, deprecated, or rolled back across tools once distributed.
- **Enterprise governance**: The four-tier security framework from the arxiv survey is described but not evaluated for practical implementability in enterprise contexts.
- **Non-coding domains**: All sources focus on software development agents. The skill ecosystem for non-coding agents (customer service, data analysis, legal) is entirely absent.
- **Quantitative composition benchmarks**: Claims about composition patterns are qualitative. No benchmarks compare composition approaches (subagent vs. if/then vs. SkillComposer) on latency, accuracy, or reliability.
- **OpenAI's AGENTS.md skills vs. agentskills.io skills**: The document conflates these two concepts throughout. OpenAI's AGENTS.md is an instruction file; the `$skill-name` notation within it references a separate OpenAI skill catalog format. The relationship between these two systems is underexplored.
- **Cline's current position post-Agent Skills adoption**: The document's Cline section was written during a transitional period. Cline's "MCP-first, skills added as complementary" framing may not reflect its current recommended architecture.
