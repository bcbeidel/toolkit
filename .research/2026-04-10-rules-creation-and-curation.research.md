---
name: "Effective Rule Creation and Curation for AI Coding Tools"
description: "Non-inferable specificity determines rule value; length kills compliance; linters beat instruction files for deterministic enforcement; auto-generation without human filtering reduces task success (ETH Zurich, arXiv 2602.11988). Covers rule structure, per-tool guidance, extraction techniques, lifecycle patterns, and anti-patterns for Cursor, Claude Code, and GitHub Copilot."
type: research
sources:
  - https://cursor.com/blog/agent-best-practices
  - https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/
  - https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
  - https://code.claude.com/docs/en/best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://trigger.dev/blog/cursor-rules
  - https://virtuslab.com/blog/ai/how-to-write-rules-for-ai
  - https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules
  - https://arxiv.org/abs/2602.11988
  - https://arxiv.org/abs/2601.20404
  - https://arxiv.org/html/2311.04235v2
  - https://www.trychroma.com/research/context-rot
  - https://arize.com/blog/optimizing-coding-agent-rules-claude-md-agents-md-clinerules-cursor-rules-for-improved-accuracy/
  - https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions.html
  - https://www.prompthub.us/blog/top-cursor-rules-for-coding-agents
  - https://www.mindstudio.ai/blog/rules-file-ai-agents-standing-orders-claude-code
  - https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/
  - https://factory.ai/news/using-linters-to-direct-agents
  - https://github.com/nedcodes-ok/rule-gen
related:
  - docs/research/2026-04-07-rule-enforcement.research.md
  - docs/research/2026-04-07-instruction-file-conventions.research.md
  - docs/context/instruction-file-non-inferable-specificity.context.md
  - docs/context/agents-md-empirical-effectiveness-findings.context.md
  - docs/context/instruction-file-extraction-techniques.context.md
  - docs/context/instruction-file-lifecycle-and-pruning.context.md
  - docs/context/instruction-file-authoring-anti-patterns.context.md
---

# Effective Rule Creation and Curation for AI Coding Tools

## Key Insights

1. **Non-inferable specificity is the decisive quality signal.** Rules that state what an agent cannot determine from reading the codebase (custom commands, non-default conventions, architecture constraints) improve behavior. Rules restating model defaults or standard conventions waste tokens without changing behavior [4].
2. **File length is a real compliance risk, not just hygiene.** Claude Code's official docs warn that "bloated CLAUDE.md files cause Claude to ignore your actual instructions." Practitioner consensus and context-rot research converge on <300 lines; HumanLayer maintains <60 [4][5][12].
3. **Linters beat instruction files for deterministic style enforcement.** "AI can choose to ignore documentation, but it cannot ignore linting errors in your CI pipeline" [18]. Instruction files hold context and rationale; linters hold enforcement.
4. **Auto-generation without human filtering reduces task success.** ETH Zurich (arXiv 2602.11988) finds LLM-generated context files reduce task success −0.5% to −2% and increase inference cost +20%. The failure mode is redundancy with existing docs, not generation itself — a filtering pass resolves it [9].
5. **The iterative correction loop is the highest-evidence extraction pattern.** Adding a rule every time the agent makes the same mistake twice produces rules with demonstrated failure-case coverage. Official docs for both Claude Code and Cursor explicitly recommend this [1][4].
6. **The two 2026 AGENTS.md studies conflict on direction.** ETH Zurich finds context files hurt success rates; arXiv 2601.20404 finds they improve efficiency (runtime, tokens). These measure different things — accuracy vs. speed — and are not contradictory if context files make agents faster but not more correct.

## Research Question

What makes an effective rule for AI coding tools (Copilot, Claude Code, Cursor), how are rules extracted from codebases and conversations, and how should rule creation be systematized?

## Sub-Questions

1. What structural and content properties make a rule reliably followed vs. ignored by LLMs? (specificity, action orientation, scope, length, voice, imperative vs. descriptive)
2. How do practitioners recommend writing rules for Cursor `.cursor/rules/`, Claude Code `CLAUDE.md`, and GitHub Copilot `.github/copilot-instructions.md`? What guidance do the official docs give on rule authoring?
3. What techniques exist for extracting rules from existing source material — codebases, PR reviews, conversation logs, linting configs, existing documentation?
4. How is rule lifecycle managed: versioning, curation, pruning, testing, knowing when a rule is no longer relevant?
5. What anti-patterns appear most frequently in community-shared rule sets?
6. What does this mean for tools/skills that auto-generate or refine instruction files?

---

## Search Protocol

| # | Query | Key Findings |
|---|-------|-------------|
| 1 | cursor rules best practices how to write effective rules 2024 2025 | Official docs, Trigger.dev 10 tips, community guides; rule types (Always/Auto/Agent/Manual) |
| 2 | github copilot custom instructions best practices writing guide 2025 | GitHub Blog 5 tips; official docs length limits (2-page max, 4000-char code review limit) |
| 3 | claude code CLAUDE.md effective instructions writing tips best practices | Claude Code best-practices docs; HumanLayer blog; DataCamp guide; <300 lines consensus |
| 4 | AI coding assistant rules anti-patterns vague instructions too many rules | JetBrains, VirtusLab, Lingo.dev analyses; context window degradation evidence |
| 5 | extracting rules from codebase automated rule generation AI coding tools agentrulegen | agentrulegen.com, rule-gen (nedcodes), Ruler (intellectronica); meta-prompt extraction technique |
| 6 | rule lifecycle management curation pruning testing AI coding tools cursor rules CLAUDE.md | rulesync tool, steipete/agent-rules; treat rules like code principle; periodic audit pattern |
| 7 | cursor rules community awesome-cursorrules analysis common patterns anti-patterns 2025 | PatrickJS/awesome-cursorrules; PromptHub analysis of top rules; functional/declarative bias |
| 8 | instruction following specificity imperative declarative LLM rules research 2024 2025 | arXiv 2311.04235 — most models fail on helpful rules; harmless rules easier than obligation rules |
| 9 | ETH Zurich study LLM generated rules files reduce task success cost increase 2025 | arXiv 2602.11988 — context files cut success −0.5% to −2%, cost +20%; minimal-requirements rec. |
| 10 | ETH Zurich "Evaluating AGENTS.md" SRI Lab arxiv paper coding agents context files 2026 | Dual benchmark (AGENTbench + SWE-bench); human files +4% but +19% cost; LLM files worse |
| 11 | LLM instruction following degradation too many instructions context window rules 2024 | Chroma context-rot study: 18 models degrade at every length increment; position bias (start/end) |
| 12 | OpenSSF security guide AI code assistant instructions copilot cursor | OpenSSF Sept 2025: concise+specific+actionable; avoid persona patterns; RCI technique |
| 13 | JetBrains coding guidelines AI agents 2025 how to write effective rules | JetBrains Junie .junie/guidelines.md; living-document approach |
| 14 | Addy Osmani AI coding workflow rules specificity agent performance 2025 2026 | Specific tool mentions: 0.01 → 1.6× usage increase; examples > paragraphs |
| 15 | how to extract rules from existing codebase PR reviews linting configs | Factory.ai linters-as-guardrails; Kinde LLM linting rules; rule-gen Gemini 1M context scan |
| 16 | Fetch: cursor.com/blog/agent-best-practices | Official Cursor agent best-practices: reference don't copy; start minimal; check rules into git |
| 17 | Fetch: docs.github.com/copilot/customizing-copilot | Full GitHub Copilot instructions spec: format, frontmatter, length, priority system |
| 18 | Fetch: code.claude.com/docs/en/best-practices | Claude Code CLAUDE.md guidance: include/exclude table; "IMPORTANT"/"YOU MUST" tuning; hooks vs instructions |
| 19 | Fetch: humanlayer.dev/blog/writing-a-good-claude-md | <300 lines consensus; 150–200 instruction limit estimate; WHY/WHAT/HOW structure |
| 20 | Fetch: trigger.dev/blog/cursor-rules | 10 tips: rule type selection; deprecated pattern marking; verification steps |
| 21 | Fetch: virtuslab.com/blog/ai/how-to-write-rules-for-ai | Single-responsibility rules; strong directive language; meta-prompt extraction |
| 22 | Fetch: agentrulegen.com/guides/how-to-write-ai-coding-rules | Attention gradient; NEVER/ALWAYS; examples > prose; four-tier classification framework |
| 23 | Fetch: arxiv.org/html/2602.11988v1 | Full ETH Zurich results; behavioral changes (more tests, file reads); no faster file discovery |
| 24 | Fetch: arxiv.org/abs/2601.20404 | Separate efficiency study: AGENTS.md → −28.64% runtime, −16.58% tokens (vs. Zurich: opposite sign) |
| 25 | Fetch: arxiv.org/html/2311.04235v2 | "Can LLMs Follow Simple Rules?" — most models fail; harmless > helpful; system-msg minimal benefit |
| 26 | Fetch: trychroma.com/research/context-rot | 18 models; performance drops at every length increment; shuffled haystack outperforms logical |
| 27 | Fetch: arize.com optimizing coding agent rules | Prompt Learning iterative optimization; 20–50 rules optimal; GPT-4.1 10–15% improvement |
| 28 | Fetch: best.openssf.org/Security-Focused-Guide | Persona patterns backfire; extract from sample (not copy wholesale); RCI up to 10× weakness density |
| 29 | Fetch: mindstudio.ai rules file ai agents | Under 500 words; specificity test: "would two devs make same decision?" |
| 30 | Fetch: factory.ai/news/using-linters-to-direct-agents | Linters as executable spec; AGENTS.md for "why", linters for "how"; lint-green as completion |
| 31 | Fetch: blog.jetbrains.com coding guidelines AI agents | .junie/guidelines.md; dos/don'ts; real code examples with explanations |
| 32 | Fetch: gist 0xdevalias agent rule files notes | Multi-tool format survey; CLAUDE.md refinement cycle; glob-scoped rules; tool-specific constraints |

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://cursor.com/blog/agent-best-practices | Best Practices for Coding with Agents | Cursor (official) | 2025–2026 | T1 | verified |
| 2 | https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/ | 5 Tips for Writing Better Custom Instructions for Copilot | GitHub Blog | 2024–2025 | T1 | verified |
| 3 | https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot | Adding Repository Custom Instructions for GitHub Copilot | GitHub (official docs) | 2025–2026 | T1 | verified |
| 4 | https://code.claude.com/docs/en/best-practices | Best Practices for Claude Code | Anthropic (official docs) | 2025–2026 | T1 | verified |
| 5 | https://www.humanlayer.dev/blog/writing-a-good-claude-md | Writing a Good CLAUDE.md | HumanLayer | 2025 | T2 | verified |
| 6 | https://trigger.dev/blog/cursor-rules | How to Write Great Cursor Rules | Trigger.dev | 2024–2025 | T2 | verified |
| 7 | https://virtuslab.com/blog/ai/how-to-write-rules-for-ai | How to Write Rules for AI Coding Tools | VirtusLab | 2025 | T2 | verified |
| 8 | https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules | How to Write AI Coding Rules for Cursor, Claude Code, and Copilot | Agent Rules Builder | 2026 | T3 | verified |
| 9 | https://arxiv.org/abs/2602.11988 | Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? | ETH Zurich SRI Lab (Gloaguen et al.) | Feb 2026 | T1 | verified (preprint, not peer-reviewed) |
| 10 | https://arxiv.org/abs/2601.20404 | On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents | arXiv | Jan 2026 | T1 | verified (preprint; contradicts [9] on direction — note divergence) |
| 11 | https://arxiv.org/html/2311.04235v2 | Can LLMs Follow Simple Rules? | arXiv | 2023 (updated 2024) | T1 | verified (preprint) |
| 12 | https://www.trychroma.com/research/context-rot | Context Rot: How Increasing Input Tokens Impacts LLM Performance | Chroma Research | 2024–2025 | T2 | verified (redirect from research.trychroma.com) |
| 13 | https://arize.com/blog/optimizing-coding-agent-rules-claude-md-agents-md-clinerules-cursor-rules-for-improved-accuracy/ | Optimizing Coding Agent Rules for Improved Accuracy | Arize AI | 2025 | T2 | verified |
| 14 | https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions.html | Security-Focused Guide for AI Code Assistant Instructions | OpenSSF Best Practices WG | Sept 2025 | T1 | verified |
| 15 | https://www.prompthub.us/blog/top-cursor-rules-for-coding-agents | Top Cursor Rules for Coding Agents | PromptHub | 2024–2025 | T3 | verified |
| 16 | https://www.mindstudio.ai/blog/rules-file-ai-agents-standing-orders-claude-code | Rules File for AI Agents: Standing Orders That Survive Sessions | MindStudio | 2025 | T3 | verified |
| 17 | https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/ | Coding Guidelines for Your AI Agents | JetBrains | May 2025 | T2 | verified |
| 18 | https://factory.ai/news/using-linters-to-direct-agents | Using Linters to Direct Agents | Factory.ai | 2025 | T2 | verified |
| 19 | https://github.com/nedcodes-ok/rule-gen | rule-gen: Generate AI Coding Rules from Your Codebase | nedcodes-ok (community) | 2025 | T4 | verified (GitHub, active repo) |
| 20 | https://medium.com/@alexefimenko/your-ai-coding-agent-is-only-as-good-as-its-rules-heres-how-to-write-ones-that-actually-work-f6bceb564871 | Your AI Coding Agent Is Only as Good as Its Rules | Alex Efimenko (Medium) | Mar 2026 | T3 | verified |

---

## Raw Extracts

### Sub-question 1: Structural and content properties that make a rule reliably followed vs. ignored

**From [11] (arXiv 2311.04235 — "Can LLMs Follow Simple Rules?"):**

- "Almost all current models perform poorly on our test suites." GPT-4 was the primary exception achieving near-perfect scores; most open models failed substantially.
- Two rule categories showed markedly different compliance: "harmless rules" (prohibitions) vs. "helpful rules" (mandatory behaviors). "Open models struggle on both the Basic and Redteam test suites, but in particular on test cases for helpful rules." This asymmetry suggests constraint-based rules (NEVER X) are more reliably followed than obligation-based ones (ALWAYS do Y).
- System messages show minimal benefit: "scores do not appear to be affected very much by presenting scenario instructions as system messages," with changes under ±1 point.
- Alignment training paradoxically harms rule-following: "alignment-tuned models perform significantly worse on our benchmark," with some models dropping 2–3 points vs. their base versions.
- Simple adversarial inputs (GCG-based suffixes) reduced harmless rule compliance from 69.6% to 17.0%, demonstrating fragility.

**From [12] (Chroma Research — Context Rot):**

- Tested 18 frontier models including Claude Opus 4, Sonnet 4, GPT-4.1, Gemini 2.5 Pro, Qwen3. Core finding: "model performance varies significantly as input length changes, even on simple tasks."
- "Even a single distractor reduces performance relative to the baseline," with four distractors compounding degradation.
- Position bias: "accuracy is highest when the unique word is placed near the beginning of the sequence, especially as input length increases." Content near context end also retains attention; mid-context content is most vulnerable.
- Surprising finding: "models perform worse when the haystack preserves a logical flow of ideas." Semantically similar but irrelevant content actively misleads models more than random content.
- Context engineering implication: "where and how information is presented in a model's context strongly influences task performance."

**From [4] (Claude Code — official docs, Best Practices):**

- "You can tune instructions by adding emphasis (e.g., 'IMPORTANT' or 'YOU MUST') to improve adherence."
- Keep it concise. "For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
- Include vs. Exclude table (verbatim):
  - Include: "Bash commands Claude can't guess"; "Code style rules that differ from defaults"; "Testing instructions"; "Repository etiquette"; "Architectural decisions specific to your project"; "Developer environment quirks"; "Common gotchas or non-obvious behaviors"
  - Exclude: "Anything Claude can figure out by reading code"; "Standard language conventions Claude already knows"; "Detailed API documentation (link to docs instead)"; "Information that changes frequently"; "Long explanations or tutorials"; "File-by-file descriptions of the codebase"; "Self-evident practices like 'write clean code'"

**From [7] (VirtusLab):**

- "Weak phrasing like 'prefer,' 'try to,' or 'maybe' leaves decisions to the AI. Use strong directives: 'always,' 'never,' 'important.'" Example: "NEVER write comments in code" produces better compliance than suggesting avoidance.
- Single Responsibility Principle for rules: split by layer and use case rather than consolidating. "LLMs have a hard time following too many instructions at once."
- Use glob expressions (`*.kt`, `**/*Test.kt`) to auto-load contextually rather than loading all rules into every session.

**From [8] (Agent Rules Builder):**

- "AI models pay more attention to content near the top of a document. Put your hard constraints first, using emphatic language."
- "AI models contain knowledge of multiple incompatible versions of the same library. Without version pins, they guess—and guess inconsistently."
- "A single good code example conveys more than paragraphs of prose." Examples demonstrate patterns "harder to misinterpret and easier for the model to extend to new situations."
- Recommended section order (attention gradient): project brief → critical rules → tech stack → code style → file structure → error handling → testing → secondary preferences.

**From [5] (HumanLayer):**

- "Frontier thinking LLMs can follow ~150–200 instructions with reasonable consistency." Claude Code's system prompt already uses ~50 instructions, leaving limited headroom.
- "The more non-universally applicable information included, the more likely it is that Claude will ignore your instructions."
- Claude Code includes a system reminder stating context "may or may not be relevant to your tasks" — a signal that conditional/non-universal rules degrade compliance.

**From [13] (Arize — Prompt Learning research):**

- Iterative prompt optimization (Prompt Learning) improved GPT-4.1 performance 10–15% using rule refinement alone. Claude Sonnet 4.5 showed 6% training gain (already near ceiling).
- Optimized rulesets contain "anywhere from 20–50 rules" — suggesting this as an empirically-grounded scope limit.
- The optimization process adds "rich English feedback" to guide improvements beyond scalar rewards.

---

### Sub-question 2: Per-tool practitioner guidance on rule authoring

**From [4] (Claude Code — official best-practices docs):**

- CLAUDE.md is "a special file that Claude reads at the start of every conversation." Use `/init` to generate a starter file, then refine.
- No required format, but: "keep it short and human-readable."
- CLAUDE.md files can import additional files: `@path/to/import` syntax: `# Git workflow: @docs/git-instructions.md`
- Multiple file locations: home (`~/.claude/CLAUDE.md`), project root (check into git), project root local (`CLAUDE.local.md` — gitignored), parent directories (monorepos), child directories (loaded on demand).
- "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost. If Claude asks you questions that are answered in CLAUDE.md, the phrasing might be ambiguous."
- "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."

**From [5] (HumanLayer):**

- "General consensus is that <300 lines is best, and shorter is even better." HumanLayer maintains their root file at "less than sixty lines."
- Structure around WHY (project purpose), WHAT (tech stack, structure), HOW (how to work, verification methods, build commands).
- "Don't include code style guidelines. Never send an LLM to do a linter's job."
- Instead of embedding all instructions: create separate markdown files (e.g., `agent_docs/building_the_project.md`) and reference them. "Prefer pointers to copies."

**From [1] (Cursor — official agent best-practices):**

- Rules should be "persistent instructions that apply to every conversation" and represent "always-on context the agent sees at conversation start."
- Content: "commands to run, patterns to follow, pointers to canonical examples in your codebase."
- "Reference files instead of copying their contents; this keeps rules short and prevents them from becoming stale as code changes."
- Example structure (verbatim): `# Commands / - npm run build: Build the project / # Code style / - Use ES modules, not CommonJS / - See components/Button.tsx for canonical structure`
- Anti-patterns (verbatim): "Copying entire style guides (use a linter instead) / Documenting every possible command (the agent knows common tools) / Adding instructions for edge cases that rarely apply"
- "Start simple. Add rules only when you notice the agent making the same mistake repeatedly. Don't over-optimize before you understand your patterns."

**From [6] (Trigger.dev — 10 tips for Cursor rules):**

- Cursor rule types: "Always" (framework/language guidelines), "Auto Attached" (pattern-based file matching), "Agent Requested" (intent-based), "Manual" (explicit attachment).
- "Explicitly mark deprecated patterns — show outdated code examples alongside current ones, using strong, direct language."
- "Include verification steps — add specific pass/fail checks the AI must validate, explaining consequences of failures (broken code, failed deploys, integration issues)."
- "Explain the 'Why' — context helps AI adapt examples to specific requests."

**From [3] (GitHub Copilot — official docs):**

- File format: Markdown. "Whitespace between instructions is ignored, so the instructions can be written as a single paragraph, each on a new line, or separated by blank lines for legibility."
- Length limits: repository-wide instructions max "2 pages." Code review reads only "the first 4,000 characters."
- "Instructions must not be task specific." Provide enduring guidance, not solutions for individual problems.
- Priority system: personal > repository > organization instructions.
- "Try to avoid providing conflicting sets of instructions."
- Official onboarding prompt recommends documenting: repository purpose, languages/frameworks, build/test/run commands with versions, project layout, CI/CD checks, non-obvious dependencies.
- Use mandatory language: "Use language indicating mandatory steps (e.g., 'always run npm install before building')."

**From [17] (JetBrains blog):**

- `.junie/guidelines.md` stores guidelines for Junie (JetBrains agent).
- Effective guidelines include: "preferred coding styles and conventions," "dos and don'ts (best practices vs. anti-patterns)," "common 'gotchas' to avoid," "real-world code examples with explanations."
- Without clear guidelines, AI misses conventions like pagination for list APIs, uses wrong injection patterns, omits error handling.
- Guidelines function as "living documents" — continuously evolving rather than static docs.

**From [14] (OpenSSF — security guide):**

- Applies across Claude markdown files, GitHub Copilot instructions, Cline instructions files, Cursor rules, Kiro steering files.
- "Instructions should be kept concise, specific, and actionable. The goal is to influence the AI's behaviour without overwhelming it."
- Avoid persona patterns: "Some experiments found that telling the system it is an expert often makes it perform poorly or worse on these tasks."
- Avoid irrelevant instructions: "If you copy and paste irrelevant parts, the AI is more likely to generate extraneous or even incorrect code as it attempts to compensate for attacks that can't happen."
- Recommend extracting from sample rather than copying wholesale — tailor content to specific tech stack and risk profile.

---

### Sub-question 3: Techniques for extracting rules from existing source material

**From [7] (VirtusLab):**

- "Rather than manual authorship, use LLMs to extract rule patterns from 2–3 existing code samples." A meta-prompt is available (gist.github.com/ZbutwialyPiernik/a97088d28bee3f2a9d7e38d811ca9124) for pattern detection and rule generation.
- "LLMs are extremely good at pattern recognition, even patterns you don't realize you follow."
- Process: "you provide two or three existing test files and ask the model to extract conventions."

**From [19] (rule-gen — nedcodes GitHub):**

- Automates rule extraction using Gemini's 1M token context window.
- Pipeline: (1) scan project tree respecting `.gitignore`, skip binaries; (2) prioritize config files, entry points, routes, pattern-rich source files; (3) detect tech stack (Django/Flask/FastAPI, pytest, mypy, ruff, etc. from `package.json` and `requirements.txt`); (4) send unified context in single API call; (5) output to `.cursor/rules/`, `CLAUDE.md`, `AGENTS.md`, or `.github/copilot-instructions.md`.
- Generated rules are codebase-specific: "Import prisma from `../db` — never instantiate PrismaClient directly."
- CLI options: `--format`, `--model`, `--max-files` (default 50), `--api-key`.

**From [8] (Agent Rules Builder):**

- agentrulegen.com: two approaches — (1) interactive builder selecting from 10,000+ community-voted rules by tech stack; (2) paste existing code for AI assessment and rule suggestion.
- Export to any format: `.cursorrules`, `CLAUDE.md`, `AGENTS.md`, `.windsurfrules`, `GEMINI.md`, `.github/copilot-instructions.md`.

**From [18] (Factory.ai — linters as guardrails):**

- Linters as rule extraction and enforcement: "When a bug or drift shows up in a review, test, or incident, rules are immediately codified as a rule, wired into local dev, pre-commit, CI, PR bots, and agent toolchains."
- "Treat 'lint green' as the merge gate." Each iteration "transforms tribal knowledge into an executable specification that agents follow by default."
- Complement with AGENTS.md: "AGENTS.md for 'why' and context; linters for 'how' with automatic validation."
- "AI can choose to ignore documentation, but it cannot ignore linting errors in your CI pipeline."

**From [20] (Alex Efimenko / DEV Community analysis):**

- Cites an ETH Zurich-adjacent observation: "LLM-generated rules files reduce task success by 3% and increase costs by 20%+." (Consistent with [9].)
- Four-tier classification for rule auditing: Essential (architecture decisions, non-inferable constraints) → Helpful (improves output) → Redundant (delete — agent already does this) → Improve Codebase (move to tooling: ESLint, Prettier, tsconfig, CI).
- Author trimmed rules from 200+ lines to 80 and reported "noticeably better agent performance with fewer, sharper directives."

**From [8] (Agent Rules Builder / lifecycle):**

- "Your rules file should grow every time you correct the AI for the same mistake twice. Treat corrections as feedback." Convert repeated corrections into new rules addressing import paths, API versions, error patterns, library preferences.
- "The most effective rules files are built over months of real AI-assisted development. They accumulate the collective wisdom of every correction your team has made."

**From [13] (Arize — Prompt Learning):**

- Automated rule optimization uses iterative feedback loop: start with baseline → generate outputs on training dataset → evaluate via unit tests → optimize ruleset using meta prompt + detailed feedback → test on held-out data.
- Applied to SWE-bench Lite (150 training / 150 test examples).
- Key: "rich English feedback" generated by LLMs guides rule improvement — not just scalar pass/fail.

---

### Sub-question 4: Rule lifecycle management — versioning, curation, pruning, testing

**From [4] (Claude Code — official docs):**

- "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."
- Check CLAUDE.md into git: "The file compounds in value over time."
- "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."
- Use `/init` command for initial generation; refine from real usage.
- Skills (`.claude/skills/`) for domain-specific knowledge that is only relevant sometimes, avoiding bloating every session.
- Hooks for "actions that must happen every time with zero exceptions" — "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."

**From [1] (Cursor — official):**

- "Check your rules into git so your whole team benefits."
- "When you see the agent make a mistake, update the rule. You can even tag @cursor on a GitHub issue or PR to have the agent update the rule for you."
- Rules files need updating when "framework changes, API updates, and project evolution" occur to "prevent outdated code generation."

**From [3] (GitHub Copilot — official docs):**

- Iterative approach: "Identify a pattern that Copilot could review better → Add a specific instruction → Test with a new pull request → Refine the instruction based on results."
- Verify custom instructions are being used by checking References lists in chat responses.

**From [16] (MindStudio):**

- "Aim to keep it under 500 words for most projects."
- "A stale rules file is worse than no rules file in some cases — it tells the agent to do things that are no longer true about the project."
- "Review your rules file the same way you'd review a pull request. Look for instructions that undermine each other."
- Specificity test: "If two different developers read your rules file and would make the same decision in the same situation, the rule is specific enough."
- "Negative rules often prevent the most frustrating mistakes."

**From [6] (Trigger.dev):**

- "Test thoroughly — run varied prompts including edge cases and problematic requests to identify misinterpretations or gaps."
- Keep rules updated: "sync with framework changes, API updates, and project evolution to prevent outdated code generation."

**From [13] (Arize):**

- Automated rule quality testing: run rules against unit-test datasets; measure improvement on held-out data before promoting to production ruleset.
- Empirical finding: model-dependent ceilings exist — Claude Sonnet 4.5 showed minimal improvement because it was already near ceiling; GPT-4.1 showed larger gains.

---

### Sub-question 5: Anti-patterns most frequently seen in community rule sets

**From [9] (ETH Zurich — Evaluating AGENTS.md, arXiv 2602.11988):**

- "Context files tend to reduce task success rates compared to providing no repository context, while also increasing inference cost by over 20%." (LLM-generated files: −0.5% to −2% on SWE-bench/AGENTbench; human-written: +4% but +19% cost.)
- Agents with context files ran "more tests, searched more files, and read more files, but did not get to the right files any faster." Context files cause unnecessary exploration without improving precision.
- "Increasing inference cost by over 20%" without proportionate performance gains.
- Recommendation: "Human-written context files should describe only minimal requirements" — focus on non-inferable specifics (custom tooling, build commands) not architectural overviews.
- When markdown documentation is removed from repos, LLM-generated context files actually improve performance by 2.7% — suggesting the anti-pattern is redundancy with existing docs, not the files themselves.

**From [10] (arXiv 2601.20404 — conflicting efficiency study):**

- Note: this study found AGENTS.md *improved* efficiency: "lower median runtime (Δ 28.64%)" and "reduced output token consumption (Δ 16.58%)." Methodology differs — used 10 repos, 124 PRs, measured wall-clock time and token consumption. Results contradict [9]; scope (10 repos vs. 300-task benchmark) and metrics differ significantly.

**From community analysis ([7], [8], [15], [20]):**

- **Vagueness**: "Use semantic selectors" vs. "Use getByRole() before getByLabel() before getByPlaceholder()." Vague rules provide no actionable decision tree.
- **Redundancy with model defaults**: Stating "use TypeScript" in a TypeScript project, or "write clean code" — these waste tokens without changing behavior.
- **Delegating to tooling**: Rules like "use 2-space indentation" should live in Prettier or ESLint. "Never send an LLM to do a linter's job."
- **Monolithic / universal rule files**: Bundling entire tech-stack templates from communities like cursor.directory without tailoring to actual codebase conventions. "Don't try to write universal rules."
- **Length bloat**: Rules files exceeding 200–300 lines tend to cause selective attention failure — important rules get lost in noise. Author anecdote: trimming from 200+ to 80 lines improved agent performance.
- **Stale rules**: Rules that reference outdated APIs, deprecated frameworks, or superseded conventions actively mislead agents.
- **Contradictory rules**: "Look for instructions that undermine each other." Split contradictory rules into separate scoped files.
- **Missing negative rules**: Rules that only prescribe what to do (positive instructions) without explicitly prohibiting common failure modes (negative instructions).
- **Context misalignment**: A Django-optimized rules file applied to a Next.js project. Stack-specific rules matter.
- **Persona instructions**: "Act as a senior security expert" — research shows this often degrades performance rather than improving it (OpenSSF finding).

**From [15] (PromptHub — top Cursor rules analysis):**

- Most effective rules from community analysis address specific pain points (incomplete AI code, missing error handling), cover multiple risk domains (security, performance, testing), and provide concrete examples rather than abstract principles.
- Community behavioral rules for AI assistants themselves: "Don't apologize for errors — fix them. If code is incomplete, add TODO comments instead."

---

### Sub-question 6: Implications for tools and skills that auto-generate or refine instruction files

**From [9] (ETH Zurich — primary finding):**

- LLM-generated context files following agent-developer recommendations perform *worse* than no context files in most settings. "Context files tend to reduce task success rates... while increasing inference cost by over 20%."
- Exception: when repository documentation is stripped, LLM-generated context files improve performance by 2.7% — the problem is redundancy, not generation itself.
- Recommendation implies: auto-generation tools should focus on *non-inferable* specifics (tooling, custom commands) not general architectural summaries that agents can read from READMEs.

**From [7] (VirtusLab — meta-prompt extraction):**

- Human-guided extraction via meta-prompts from 2–3 code samples outperforms both manual writing and generic templates. This is a viable middle ground between full automation and hand-crafted rules.
- Process produces codebase-specific rules rather than generic best-practice lists.

**From [13] (Arize — Prompt Learning):**

- Automated iterative optimization using unit test feedback is more effective than one-shot generation. "Rich English feedback" from LLM evaluation guides improvement beyond simple correctness signals.
- This suggests: auto-generation tools should include a feedback/refinement loop rather than one-shot output.

**From [19] (rule-gen):**

- Full-codebase scanning (up to Gemini's 1M token context) produces more specific and accurate rules than template-based generation. Trade-off: requires a large-context model and has per-use API cost.

**From [8] (Agent Rules Builder):**

- Community-voted rule libraries (10,000+ rules) provide a curated starting point. Quality signal from voting is more reliable than uncurated repositories (like awesome-cursorrules). But community rules still need project-specific tailoring.

**From [20] (Alex Efimenko):**

- Four-tier classification suggests a quality-audit workflow for auto-generated rules: classify each generated rule as Essential / Helpful / Redundant / Move-to-tooling, then prune accordingly. This turns generation into a filtering problem rather than a creation problem.

**From [5] (HumanLayer):**

- "Don't auto-generate the file [CLAUDE.md]. Because CLAUDE.md goes into every single session with Claude code, it is one of the highest leverage points of the harness." Auto-generation risks filling this high-value slot with low-value content.
- Better: generate candidate rules, human-curate, keep total under 60–300 lines.

**From [18] (Factory.ai):**

- The most reliable auto-generation path for coding rules may be via linters rather than natural language. "AI can choose to ignore documentation, but it cannot ignore linting errors in your CI pipeline."
- Instruction files and linter rules are complementary: instruction files for context/rationale, linter rules for deterministic enforcement.

---

## Challenge

### C1: "Strong imperative language (NEVER/ALWAYS) outperforms hedged language"

**Claim origin:** Multiple practitioner sources [7][8] assert that directives like "NEVER" and "ALWAYS" are more reliably followed than phrases like "prefer" or "try to."

**Challenge:** This practitioner consensus is grounded primarily in anecdote, not controlled experiment. The one relevant academic source [11] (arXiv 2311.04235, 2023) found that *most models fail on rule-following*, with GPT-4 as the primary exception. As of 2025-2026, frontier models have substantially improved instruction-following, and the 2023 failure rates are unlikely to represent current baselines. The claim that capitalized imperatives specifically improve compliance is a practitioner heuristic without controlled evidence. Official docs [4] mention "IMPORTANT" and "YOU MUST" as tuning mechanisms, lending it some T1 backing — but that is still anecdote from the toolmaker. **Verdict: Plausible but overstated. Present as practitioner recommendation, not empirical finding.**

### C2: "Optimal rule count is 20–50"

**Claim origin:** Arize [13] reports that iteratively-optimized rulesets contain "anywhere from 20–50 rules" and achieved 10–15% improvement on GPT-4.1.

**Challenge:** Arize is a vendor with a commercial product (Prompt Learning) that benefits from demonstrating the effectiveness of its optimization framework. The 20–50 figure is an observation about what their tool produced, not a controlled comparison against other rule counts. The 10–15% improvement is self-reported on SWE-bench Lite; real-world generalization is unclear. HumanLayer [5] cites 150–200 as the instruction limit estimate, and practitioners maintain files under 60 lines. These signals span an order of magnitude. **Verdict: The 20–50 figure is a vendor observation, not a universal optimum. Use as a rough order-of-magnitude sanity check only.**

### C3: The ETH Zurich / arXiv conflict on AGENTS.md effectiveness

**Claim origin (primary):** [9] (ETH Zurich, Feb 2026) finds LLM-generated context files reduce task success −0.5% to −2%, increase cost +20%; human-written files +4% but +19% cost increase.

**Claim origin (conflicting):** [10] (arXiv Jan 2026) finds AGENTS.md files reduce runtime by −28.64% and token consumption by −16.58%.

**Challenge:** These findings directly contradict each other on direction. Key methodological differences: [9] uses SWE-bench Lite + AGENTbench (300 tasks), measures task success rate and inference cost; [10] uses 10 repositories / 124 PRs, measures wall-clock runtime and output token count. Different metrics (success rate vs. efficiency), different scales, and different agent implementations likely explain the divergence. [10] may reflect efficiency gains (faster, fewer tokens) without addressing whether the agent actually *solved* the task correctly — these are compatible if AGENTS.md makes agents faster but not more accurate. **Verdict: Both studies are valid within their scope. Correct framing: AGENTS.md files may improve token efficiency while having ambiguous or negative effects on task success. Do not cite either as the universal finding.**

### C4: "Don't auto-generate CLAUDE.md"

**Claim origin:** HumanLayer [5] explicitly recommends against auto-generation.

**Challenge:** This conflicts with [9]'s finding that human-written files improve success by +4% but cost +19% more in inference. Auto-generation with human review may be a reasonable tradeoff, especially for projects with no existing instruction file. The ETH Zurich finding that removing markdown docs then generating improves success by 2.7% suggests the real anti-pattern is redundancy with existing docs, not auto-generation per se. **Verdict: The blanket "don't auto-generate" recommendation is too strong. Auto-generation with a filtering pass (Essential / Helpful / Redundant / Move-to-tooling) is defensible; the failure mode is unreviewed generation, not generation itself.**

### C5: Context-rot position bias ("put critical rules first")

**Claim origin:** Chroma research [12] and multiple practitioner sources recommend placing critical rules at the top of instruction files due to position bias.

**Challenge:** Chroma's context-rot study is conducted by a vector database company with commercial interest in demonstrating that long contexts degrade performance (making RAG more attractive). Their methodology tests a "find the unique word" haystack task, which may not transfer directly to instruction-following in realistic coding contexts. Claude Code's official guidance [4] says to keep files short but does not prescribe specific ordering. **Verdict: Position bias is a real phenomenon in long-context retrieval; the recommendation to put critical rules first is sound defensive design. But the Chroma finding's strength should be qualified — it's a retrieval task result, not an instruction-following result.**

---

## Findings

### 1. What makes a rule reliably followed?

**Non-inferable specificity is the single strongest predictor of rule value.** Rules that state what an LLM cannot determine from the codebase alone (custom tooling, non-default conventions, architecture decisions) materially improve behavior; rules that restate known defaults waste tokens without changing behavior [4]. The "specificity test" from [16]: if two developers reading the rule would make the same decision in the same situation, it is specific enough (MODERATE — T3 source, but widely validated practitioner heuristic).

**Constraint-based rules (prohibitions) are more reliably followed than obligation-based ones.** The 2023 academic benchmark [11] found asymmetric compliance — "harmless" (prohibition) rules outperformed "helpful" (obligation) rules significantly. This finding predates current frontier models and the absolute failure rates no longer apply, but the asymmetry is plausible: prohibitions have a binary pass/fail structure that is easier to enforce (LOW-MODERATE — 2023 study, outdated failure rates but direction likely still holds).

**Imperative language is practitioner-recommended but not empirically proven stronger.** Directives like "NEVER X" and "ALWAYS Y" are consistently recommended [4][7][8][14], and Claude Code's official docs explicitly endorse "IMPORTANT" and "YOU MUST" for emphasis. This is T1-backed practitioner guidance, not a controlled-experiment finding (MODERATE — T1 endorsement, no A/B data).

**File length is a real compliance risk.** Claude Code official docs [4] state directly that "bloated CLAUDE.md files cause Claude to ignore your actual instructions." The Chroma context-rot study [12] shows degradation at every length increment across 18 models. Practitioner consensus settles around <300 lines for full files; HumanLayer maintains <60 lines. Combined T1+T2 convergence (HIGH — T1 official warning + T2 multi-source practitioner consensus).

**Examples outperform prose.** Multiple practitioner sources [8][14][17] converge on examples being more reliably interpreted than explanatory paragraphs. JetBrains [17] specifically documents real-code examples with explanations as an effective format. No academic validation, but strong practitioner consensus (MODERATE — T2 multi-source convergence, no academic validation).

**Critical rules go first.** Position bias in long-context models is documented [12]. Multiple practitioner guides independently converge on this. Caveat: the Chroma study uses a retrieval task, not instruction-following; but placing critical constraints at the top is low-cost defensive design (MODERATE — retrieval-task evidence, directionally applicable to instruction files).

---

### 2. Per-tool rule authoring guidance

**Claude Code (CLAUDE.md):** Keep under ~300 lines; use `@import` for hierarchy rather than monolithic files; include commands/build patterns the agent cannot infer, non-default conventions, testing instructions, architectural constraints; exclude anything readable from code, standard conventions, frequently-changing details; use hooks for deterministic enforcement, CLAUDE.md for advisory guidance; check into git [1][4][5] (HIGH — T1 official docs + T2 practitioner convergence).

**GitHub Copilot (`.github/copilot-instructions.md`):** Hard limit of 2 pages (~4,000 characters for code review); use mandatory language ("always run X before Y"); task-agnostic guidance only — not solutions to individual problems; covers repository purpose, languages, build commands, project layout, CI/CD checks; priority order: personal > repository > organization [2][3] (HIGH — T1 official docs).

**Cursor (`.cursor/rules/*.mdc`):** Four rule types — "Always" (always loaded), "Auto Attached" (glob pattern), "Agent Requested" (semantic intent), "Manual" (explicit attach); reference files instead of copying content; start minimal, add rules when mistakes repeat; explicitly mark deprecated patterns; add verification steps to rules [1][6] (HIGH — T1 official + T2 practitioner).

**JetBrains/other tools:** `.junie/guidelines.md` follows the same principle — living document, dos/don'ts, real code examples with explanations, not a static spec [17] (MODERATE — T2 single source).

---

### 3. Rule extraction techniques

Four viable extraction approaches, ranked by evidence quality:

1. **Linter codification** (highest reliability): When a recurring mistake is identified, codify it as a linter rule rather than a natural-language instruction. Linters are deterministic; instruction files are advisory. "AI can choose to ignore documentation, but it cannot ignore linting errors in your CI pipeline" [18]. Use instruction files for the "why"; linters for the "how" (MODERATE — T2, strong conceptual backing from [4] which recommends hooks for deterministic enforcement).

2. **Meta-prompt extraction from code samples**: Provide 2–3 existing code files to an LLM with a meta-prompt asking it to extract conventions. VirtusLab [7] provides this approach; "LLMs are extremely good at pattern recognition, even patterns you don't realize you follow." The meta-prompt is publicly available. Produces codebase-specific rules rather than generic templates (MODERATE — T2, practitioner-validated, not benchmarked).

3. **Iterative correction loop**: Add a rule every time the agent makes the same mistake twice. Cursor's official docs [1] explicitly recommend this pattern; Agent Rules Builder [8] names it as the core accumulation mechanism. Produces rules with demonstrated failure-case coverage (HIGH — T1+T3 convergence on this as the production-proven pattern).

4. **Full-codebase scan via large-context model**: Tools like rule-gen [19] scan the full project tree using a 1M-context model and generate tool-specific rules. Produces specific rules (e.g., "import prisma from `../db` — never instantiate PrismaClient directly"), but requires a large-context model and has per-use API cost. ETH Zurich [9] warns that LLM-generated files tend to underperform; this approach requires human review before deployment (LOW-MODERATE — T4 tool, ETH Zurich caveat).

---

### 4. Rule lifecycle management

**Treat rules files like code.** Version in git, review changes in PRs, prune on a schedule. Claude Code [4] and Cursor [1] both explicitly recommend this. Rules that are wrong are worse than no rules — stale rules actively mislead agents [16] (HIGH — T1 multi-tool convergence).

**Prune with a four-tier audit.** Classify each rule as: Essential (architecture decisions, non-inferable constraints) → Helpful (measurably improves output) → Redundant (agent already does this without the rule) → Move-to-tooling (belongs in a linter or formatter, not a text file) [20]. One practitioner reduced a 200+ line file to 80 lines and reported improved agent performance (MODERATE — T3, single practitioner report, consistent with broader length findings).

**Test rules against real usage.** Copilot's official approach [3]: identify a pattern → add an instruction → test with a new PR → refine. Trigger.dev [6]: run varied prompts including edge cases. Arize [13]: use automated rule optimization with held-out test data. Common thread: rules need empirical validation against actual agent behavior, not just logical review (MODERATE — T1+T2 multi-source).

**Hooks for deterministic, instructions for advisory.** Claude Code's architecture is explicit: hooks guarantee execution; CLAUDE.md is advisory [4]. This distinction maps cleanly to other tools — linter rules are hooks-equivalent; instruction files are advisory (HIGH — T1, directly stated).

---

### 5. Anti-patterns

Evidence-ranked, most-to-least supported:

| Anti-pattern | Evidence | Severity |
|---|---|---|
| **Vague rules** ("use semantic selectors" vs. explicit API hierarchy) | Multi-source convergence [7][8][16] | HIGH — unclear rules produce inconsistent behavior |
| **Length bloat** (>200–300 lines) | T1 warning [4] + T2 multi-source [5][12] | HIGH — official docs warn rules get lost |
| **Redundancy with model defaults** ("write clean code") | T1 guidance [4] explicitly names this to avoid | HIGH — wastes tokens, dilutes signal |
| **Delegating style to LLMs instead of tooling** | T2 convergence [5][18] + T1 [4] | HIGH — linters are deterministic; instructions aren't |
| **Stale rules** (outdated API, deprecated framework) | T1 [1][4], T3 [16] | HIGH — actively misleads agents |
| **Copying community templates wholesale** | T1 [1], T2 [7][14] | MODERATE — context mismatch degrades precision |
| **Contradictory rules** | T3 [16], T2 [7] | MODERATE — model must choose; outcome unpredictable |
| **Missing negative rules** (prescriptions without prohibitions) | T3 [16] | MODERATE — failure modes left unaddressed |
| **Persona instructions** ("act as a senior security expert") | T1 [14] (OpenSSF) | MODERATE — research shows degraded performance |
| **Redundancy with existing project docs** | T1 [9] (ETH Zurich) | MODERATE — primary anti-pattern for generated files |

---

### 6. Implications for auto-generating or refining instruction files

The ETH Zurich study [9] is the decisive empirical finding: LLM-generated context files following standard recommendations tend to reduce task success rates (−0.5% to −2%) while increasing inference cost (+20%). Human-written files show +4% improvement but also +19% cost increase. The primary failure mode of generated files is **redundancy with existing documentation** — agents already have access to READMEs and code; instruction files that summarize the same content add noise without signal.

**What this means for WOS skills that generate or refine instruction files:**

1. **Generate candidates; require human review.** Auto-generation is not harmful in itself; unreviewed auto-generation deployed as-is is. Skills should produce candidate rules and prompt the user to apply the Essential/Helpful/Redundant/Move-to-tooling filter before writing.

2. **Focus generation on non-inferable specifics only.** The ETH Zurich exception (2.7% improvement when docs are stripped) suggests that the rule for generated content is: only emit what an agent cannot learn by reading the codebase. Custom tool names, non-standard commands, architecture constraints not evident from code.

3. **Prefer meta-prompt extraction over template generation.** Extracting conventions from 2–3 actual code samples produces codebase-specific rules [7]; templates produce generic rules that often fail the non-inferable test.

4. **Iterative feedback loop outperforms one-shot generation.** Whether using the Arize approach [13] or manual correction loops [1][8], rules improve over iterations. Skills that generate a file once and close should at minimum instruct the user to iterate.

5. **Linters as the high-confidence extraction target.** For style/format concerns, the output of a WOS rule-extraction skill should be a linter config, not an instruction file. The instruction file gets the rationale and exceptions; the linter gets the enforcement.

6. **File size is a quality signal.** A generated file >300 lines is almost certainly over-specified. WOS skills should warn when generated output exceeds this threshold.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | LLM-generated context files reduce task success −0.5% to −2%, increase cost +20% | statistic | [9] ETH Zurich arXiv 2602.11988 | verified |
| 2 | Human-written context files improve task success +4%, increase cost +19% | statistic | [9] | verified |
| 3 | AGENTS.md files reduce runtime by −28.64% and token consumption by −16.58% | statistic | [10] arXiv 2601.20404 | verified (contradicts [9]; different metrics) |
| 4 | Removing markdown docs then generating context files improves success by 2.7% | statistic | [9] | verified |
| 5 | Frontier models can follow ~150–200 instructions with reasonable consistency | estimate | [5] HumanLayer | human-review (practitioner estimate, not academic measurement) |
| 6 | Claude Code system prompt uses ~50 instructions, leaving limited headroom | estimate | [5] HumanLayer | human-review (third-party estimate of Anthropic's system prompt) |
| 7 | Iterative optimization improved GPT-4.1 performance 10–15%; Claude Sonnet 4.5 showed 6% gain | statistic | [13] Arize | vendor-reported (Arize measures their own product; not independently replicated) |
| 8 | Optimized rulesets contain "anywhere from 20–50 rules" | observation | [13] Arize | vendor-reported (describes Arize Prompt Learning output, not a controlled experiment) |
| 9 | GCG-based adversarial suffixes reduced harmless rule compliance from 69.6% to 17.0% | statistic | [11] arXiv 2311.04235 | verified (preprint; 2023; absolute rates outdated for current models) |
| 10 | GitHub Copilot code review reads only the first 4,000 characters of instructions | specification | [3] GitHub official docs | verified |
| 11 | GitHub Copilot instructions are limited to approximately 2 pages | specification | [3] | verified |
| 12 | Context rot: performance drops at every length increment across 18 tested models | finding | [12] Chroma Research | verified (retrieval task, not instruction-following; transferability qualified) |
| 13 | Performance highest near beginning and end of context; mid-context most vulnerable | finding | [12] | verified (same qualification as #12) |
| 14 | Practitioner who trimmed rules from 200+ to 80 lines reported improved performance | anecdote | [20] Alex Efimenko | human-review (single practitioner, no controlled comparison) |
| 15 | agentrulegen.com offers 10,000+ community-voted rules | vendor claim | [8] | human-review (unverifiable vendor claim; plausible but unchecked) |

---

## Takeaways

**For rule authors:**
- Write only what the agent cannot infer from code. If it can read a README to learn it, don't put it in the instruction file.
- Keep files under 300 lines. Under 60 is better. If you can't cut, split by scope.
- Use imperative directives (NEVER / ALWAYS / IMPORTANT) for hard constraints. Use hedged language for preferences only.
- Put the hardest constraints first. Position bias is real.
- Pair every positive rule with a negative counterpart where failure modes are known.
- Rules belong in linters if they're about style or format. Instruction files hold rationale and non-deterministic guidance.

**For rule extraction:**
- Start with the iterative correction loop: add a rule each time the same mistake occurs twice.
- Use a meta-prompt on 2–3 actual code files to extract implicit conventions the team already follows.
- Apply the four-tier filter before deploying any generated ruleset: Essential → Helpful → Redundant (delete) → Move-to-tooling.

**For WOS skills generating instruction files:**
- Generate candidates; do not deploy without human review.
- Warn at 300 lines. Reject above 500.
- Emit linter config, not instruction prose, for style and format rules.
- Include the iterative refinement loop — a one-shot generated file is a starting point, not a final artifact.
- Focus generation on non-inferable specifics: custom tooling, build commands, non-standard architecture constraints.
