---
name: Skill Platform Nuances Across 19 AI Agent Platforms
description: Competitive research covering skill/instruction format alignment, capability differences, output file placement constraints, and minimum common denominator across 19 AI assistant and agent framework platforms.
type: research
sources:
  - https://agentskills.io/specification
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://geminicli.com/docs/cli/skills/
  - https://docs.crewai.com/en/concepts/skills
  - https://docs.langchain.com/oss/python/deepagents/skills
  - https://agentskills.io/skill-creation/evaluating-skills
  - https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-skills
related: []
---

## Key Findings

The Agent Skills open standard (`name` + `description` + Markdown SKILL.md) has been adopted by 18 confirmed platforms (ChatGPT Skills unconfirmed as of April 2026). Format compliance is real; **behavioral portability is not** — the best-supported hypothesis from the ACH analysis. Three things drive the divergence: different discovery paths, different `allowed-tools` semantics, and Claude Code's 17 proprietary extensions with no equivalents elsewhere.

**What works everywhere (MCD):** `SKILL.md` with `name` (≤64 chars) and `description` (≤1024 chars), `scripts/`/`references/`/`assets/` layout, progressive disclosure, Markdown body. [HIGH — 18 T1 sources converge]

**Discovery path problem:** No single path is discovered by all platforms. `.claude/skills/` = Claude Code only. `.agents/skills/` = 9 other platforms. Cross-platform skills require both. [HIGH]

**Capability split by environment:**
- Full filesystem: CLI/IDE tools (Claude Code, Codex, Gemini CLI, Cursor, Windsurf, Kiro, Copilot)
- Sandboxed VM: Claude API and Claude.ai
- Directory-scoped: Claude Cowork (user-designated directories via Apple Virtualization)
- Upload-based: ChatGPT (no direct filesystem)

**`allowed-tools` behavior diverges critically:** permission-grant (Claude Code) vs. confirmation-bypass (Copilot) vs. metadata-only with no enforcement (CrewAI). [HIGH]

**Gemini CLI is the outlier:** requires explicit per-session user consent before skill activation. All other platforms activate automatically. [HIGH]

**Eval workspace layout (agentskills.io spec):** `<skill>-workspace/iteration-N/eval-<name>/{with_skill,without_skill}/outputs/` with `timing.json`, `grading.json`, `benchmark.json`. Not platform-enforced but the canonical layout. [HIGH]

*25 searches · 35 sources · 26 T1 · 7 T4-T5 · 3 corrections in verification*

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://agentskills.io/specification | Specification - Agent Skills | agentskills.io | 2025-12 | T1 | verified |
| 2 | https://github.com/anthropics/skills/blob/main/spec/agent-skills-spec.md | skills/spec/agent-skills-spec.md at main | Anthropic / GitHub | 2025-12 | T1 | verified (redirects to agentskills.io) |
| 3 | https://code.claude.com/docs/en/skills | Extend Claude with skills - Claude Code Docs | Anthropic | 2026-04 | T1 | verified |
| 4 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Agent Skills - Claude API Docs | Anthropic | 2026-04 | T1 | verified |
| 5 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill authoring best practices - Claude API Docs | Anthropic | 2026-04 | T1 | verified |
| 6 | https://code.visualstudio.com/docs/copilot/customization/agent-skills | Use Agent Skills in VS Code | Microsoft / VS Code Docs | 2026-01 | T1 | verified |
| 7 | https://docs.github.com/en/copilot/concepts/agents/about-agent-skills | About agent skills - GitHub Docs | GitHub | 2026-01 | T1 | verified |
| 8 | https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-skills | Creating agent skills for GitHub Copilot - GitHub Docs | GitHub | 2026-01 | T1 | verified |
| 9 | https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/ | GitHub Copilot now supports Agent Skills | GitHub Changelog | 2025-12-18 | T1 | verified |
| 10 | https://developers.openai.com/codex/skills | Agent Skills – Codex | OpenAI Developers | 2026-01 | T1 | verified |
| 11 | https://github.com/openai/codex/blob/main/docs/skills.md | codex/docs/skills.md at main | OpenAI / GitHub | 2025-12 | T1 | verified |
| 12 | https://cursor.com/docs/skills | Agent Skills | Cursor Docs | 2026-01 | T1 | verified |
| 13 | https://geminicli.com/docs/cli/skills/ | Agent Skills | Gemini CLI | 2026-01 | T1 | verified |
| 14 | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials/skills-getting-started.md | gemini-cli/docs/cli/tutorials/skills-getting-started.md | Google / GitHub | 2026-01 | T1 | verified |
| 15 | https://ai.google.dev/gemini-api/docs/coding-agents | Set up your coding assistant with Gemini MCP and Skills | Google AI for Developers | 2026-01 | T1 | verified |
| 16 | https://developer.android.com/studio/gemini/skills | Extend Agent Mode with skills | Android Studio / Android Developers | 2026-01 | T1 | verified |
| 17 | https://docs.windsurf.com/windsurf/cascade/skills | Cascade Skills | Windsurf (Codeium) Docs | 2026-01 | T1 | verified |
| 18 | https://learn.microsoft.com/en-us/agent-framework/agents/skills | Agent Skills | Microsoft Learn | 2026-04-10 | T1 | verified |
| 19 | https://devblogs.microsoft.com/semantic-kernel/give-your-agents-domain-expertise-with-agent-skills-in-microsoft-agent-framework/ | Give Your Agents Domain Expertise with Agent Skills in Microsoft Agent Framework | Microsoft Dev Blog | 2026-03 | T1 | verified |
| 20 | https://docs.crewai.com/en/concepts/skills | Skills - CrewAI | CrewAI Docs | 2026-01 | T1 | verified |
| 21 | https://docs.langchain.com/oss/python/deepagents/skills | Skills - Docs by LangChain | LangChain Docs | 2026-01 | T1 | verified |
| 22 | https://kiro.dev/docs/skills/ | Agent Skills - IDE - Docs - Kiro | Kiro / AWS | 2026-02 | T1 | verified |
| 23 | https://kiro.dev/docs/cli/skills/ | Agent Skills - CLI - Docs - Kiro | Kiro / AWS | 2026-02 | T1 | verified |
| 24 | https://opencode.ai/docs/skills/ | Agent Skills | OpenCode | 2026-01 | T1 | verified |
| 25 | https://agentskills.io/skill-creation/evaluating-skills | Evaluating skill output quality - Agent Skills | agentskills.io | 2026-01 | T1 | verified |
| 26 | https://developer.tenten.co/claude-cowork-anthropic-brings-ai-agent-capabilities-to-non-technical-users | Claude Cowork: Anthropic Brings AI Agent Capabilities to Non-Technical Users | developer.tenten.co | 2026-01 | T5 | unverified — sole source for Cowork sandbox details |
| 27 | https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills | Equipping agents for the real world with Agent Skills | Anthropic | 2025-12 | T1 | verified |
| 28 | https://help.apiyi.com/en/agents-vs-claude-folder-skills-ai-agent-development-guide-en.html | Understand the 5 Core Differences Between .agents and .claude Folders | apiyi.com | 2026-01 | T5 | unverified — ⚠️ conflicts with T1 spec: claims .agents/ uses SKILL.yaml, not SKILL.md |
| 29 | https://inference.sh/blog/skills/agent-skills-overview | Agent Skills: The Open Standard for AI Capabilities | inference.sh | 2026-01 | T4 | unverified — vendor perspective |
| 30 | https://alexop.dev/posts/understanding-claude-code-full-stack/ | Understanding Claude Code's Full Stack | alexop.dev | 2026-02 | T4 | unverified — independent developer |
| 31 | https://visualstudiomagazine.com/articles/2026/01/11/hand-on-with-new-github-copilot-agent-skills-in-vs-code.aspx | Hands On with New GitHub Copilot 'Agent Skills' in VS Code | Visual Studio Magazine | 2026-01-11 | T4 | unverified — trade press |
| 32 | https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/ | Agent Skills: Anthropic's Next Bid to Define AI Standards | The New Stack | 2025-12 | T4 | unverified — trade press |
| 33 | https://www.mindstudio.ai/blog/agent-skills-open-standard-claude-openai-google | What Is Agent Skills as an Open Standard? | MindStudio | 2026-01 | T4 | unverified — ⚠️ vendor perspective, potential bias |
| 34 | https://www.infoq.com/news/2026/01/claude-cowork/ | Anthropic Announces Claude CoWork | InfoQ | 2026-01 | T4 | unverified — trade press |
| 35 | https://medium.com/@richardhightower/from-approval-hell-to-just-do-it-how-agent-skills-fork-governed-sub-agents-in-claude-code-2-1-c0438416433a | From Approval Hell to Just Do It: Agent Skills Fork in Claude Code 2.1 | Rick Hightower / Medium | 2026-02 | T4 | unverified — independent developer |

**SIFT notes:**
- Sources 1–25, 27: Official documentation (T1). High confidence for all claims sourced from these.
- Source 26 (T5): Sole source for Cowork sandbox directory paths and virtualization details. No T1 source available for Cowork internals (no official Cowork developer docs found). Treat Cowork-specific claims as LOW confidence.
- Source 28 (T5): ⚠️ **Conflicting claim** — asserts `.agents/skills/` uses `SKILL.yaml` format, contradicted by T1 sources (agentskills.io spec [1], official platform docs [6–16]) which all specify `SKILL.md`. Discard this claim; use only the T1-sourced clarification in Sub-question 4.
- ChatGPT Skills (sources 10–11 are Codex-specific; ChatGPT Skills feature sources are unverified T5 search results): No T1 official documentation found for ChatGPT Skills / "Hazelnut". Treat as LOW confidence; flag as preliminary/beta.
- Source 33 (MindStudio T4): Vendor with competing interests. Use only for corroboration of T1-established facts.

---

## Sub-question 1: Skill/instruction format alignment with the Agent Skills open standard

### Agent Skills Open Standard (agentskills.io) — verbatim extracts

From https://agentskills.io/specification (fetched 2026-04-12):

> A skill is a directory containing, at minimum, a `SKILL.md` file:
> ```
> skill-name/
> ├── SKILL.md          # Required: metadata + instructions
> ├── scripts/          # Optional: executable code
> ├── references/       # Optional: documentation
> ├── assets/           # Optional: templates, resources
> └── ...               # Any additional files or directories
> ```

> The `SKILL.md` file must contain YAML frontmatter followed by Markdown content.
>
> | Field           | Required | Constraints                                                                                                       |
> | --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
> | `name`          | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen.             |
> | `description`   | Yes      | Max 1024 characters. Non-empty. Describes what the skill does and when to use it.                                 |
> | `license`       | No       | License name or reference to a bundled license file.                                                              |
> | `compatibility` | No       | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
> | `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                                              |
> | `allowed-tools` | No       | Space-separated string of pre-approved tools the skill may use. (Experimental)                                   |

> The required `name` field:
> * Must be 1-64 characters
> * May only contain unicode lowercase alphanumeric characters (`a-z`) and hyphens (`-`)
> * Must not start or end with a hyphen (`-`)
> * Must not contain consecutive hyphens (`--`)
> * Must match the parent directory name

> Skills should be structured for efficient use of context:
> 1. **Metadata** (~100 tokens): The `name` and `description` fields are loaded at startup for all skills
> 2. **Instructions** (< 5000 tokens recommended): The full `SKILL.md` body is loaded when the skill is activated
> 3. **Resources** (as needed): Files (e.g. those in `scripts/`, `references/`, or `assets/`) are loaded only when required
>
> Keep your main `SKILL.md` under 500 lines. Move detailed reference material to separate files.

The spec was moved from `github.com/anthropics/skills/spec/agent-skills-spec.md` to agentskills.io. The GitHub file now contains only a redirect notice: "The spec is now located at https://agentskills.io/specification".

---

### Platform 1: Claude Code CLI

From https://code.claude.com/docs/en/skills (fetched 2026-04-12):

> Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools. Claude Code extends the standard with additional features like [invocation control](#control-who-invokes-a-skill), [subagent execution](#run-skills-in-a-subagent), and [dynamic context injection](#inject-dynamic-context).

Frontmatter fields supported (Claude Code extends the open standard):

| Field                      | Required    | Description |
| :------------------------- | :---------- | :---------- |
| `name`                     | No          | Display name. If omitted, uses directory name. Lowercase letters, numbers, hyphens (max 64 chars). |
| `description`              | Recommended | What the skill does. If omitted, uses first paragraph. Front-load key use case; truncated at 250 chars in listing. |
| `argument-hint`            | No          | Hint shown during autocomplete. |
| `disable-model-invocation` | No          | Set to `true` to prevent Claude from auto-loading. Default: `false`. |
| `user-invocable`           | No          | Set to `false` to hide from `/` menu. Default: `true`. |
| `allowed-tools`            | No          | Tools Claude can use without permission prompt when skill is active. Space-separated or YAML list. |
| `model`                    | No          | Model to use when this skill is active. |
| `effort`                   | No          | Effort level. Options: `low`, `medium`, `high`, `max`. |
| `context`                  | No          | Set to `fork` to run in a forked subagent context. |
| `agent`                    | No          | Subagent type when `context: fork` is set. |
| `hooks`                    | No          | Hooks scoped to this skill's lifecycle. |
| `paths`                    | No          | Glob patterns limiting when skill is auto-activated. |
| `shell`                    | No          | Shell for `!`command`` and ` ```! ` blocks. Accepts `bash` (default) or `powershell`. |

> **Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to [control whether you or Claude invokes them](#control-who-invokes-a-skill), and the ability for Claude to load them automatically when relevant.

Skill location table from Claude Code docs:

| Location   | Path                                                | Applies to                     |
| :--------- | :-------------------------------------------------- | :----------------------------- |
| Enterprise | See [managed settings] | All users in your organization |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md`            | All your projects              |
| Project    | `.claude/skills/<skill-name>/SKILL.md`              | This project only              |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`             | Where plugin is enabled        |

> When skills share the same name across levels, higher-priority locations win: enterprise > personal > project. Plugin skills use a `plugin-name:skill-name` namespace, so they cannot conflict with other levels.

Dynamic context injection (Claude Code-specific):

> The `` !`<command>` `` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself.

> To disable this behavior for skills and custom commands from user, project, plugin, or additional-directory sources, set `"disableSkillShellExecution": true` in settings. Each command is replaced with `[shell command execution disabled by policy]` instead of being run.

String substitutions supported:

| Variable               | Description |
| :--------------------- | :---------- |
| `$ARGUMENTS`           | All arguments passed when invoking the skill. |
| `$ARGUMENTS[N]`        | Specific argument by 0-based index. |
| `$N`                   | Shorthand for `$ARGUMENTS[N]`. |
| `${CLAUDE_SESSION_ID}` | Current session ID. |
| `${CLAUDE_SKILL_DIR}`  | Directory containing the skill's `SKILL.md` file. |

Skill content lifecycle:

> When you or Claude invoke a skill, the rendered `SKILL.md` content enters the conversation as a single message and stays there for the rest of the session. Claude Code does not re-read the skill file on later turns.
>
> [Auto-compaction] carries invoked skills forward within a token budget. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens.

---

### Platform 2: Claude Code Desktop

No separate documentation found for Claude Code Desktop as distinct from the CLI. Claude Code Desktop appears to be the same underlying agent accessed via a desktop GUI wrapper rather than a separate product. The claude.ai docs note:

> **Claude Code**: [Claude Code](https://code.claude.com/docs/en/overview) supports only Custom Skills. **Custom Skills**: Create Skills as directories with SKILL.md files. Claude discovers and uses them automatically. Custom Skills in Claude Code are filesystem-based and don't require API uploads.

---

### Platform 3: claude.ai/code

From the Claude API docs overview (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):

> ### Claude.ai
> [Claude.ai](https://claude.ai) supports both pre-built Agent Skills and custom Skills.
>
> **Pre-built Agent Skills**: These Skills are already working behind the scenes when you create documents. Claude uses them without requiring any setup.
>
> **Custom Skills**: Upload your own Skills as zip files through Settings > Features. Available on Pro, Max, Team, and Enterprise plans with code execution enabled. Custom Skills are individual to each user; they are not shared organization-wide and cannot be centrally managed by admins.

Runtime constraints for Claude.ai:

> **Claude.ai**:
>    - **Varying network access**: Depending on user/admin settings, Skills may have full, partial, or no network access.

Cross-surface availability note:

> **Custom Skills do not sync across surfaces**. Skills uploaded to one surface are not automatically available on others:
> - Skills uploaded to Claude.ai must be separately uploaded to the API
> - Skills uploaded via the API are not available on Claude.ai
> - Claude Code Skills are filesystem-based and separate from both Claude.ai and API

Sharing scope for Claude.ai:

> **Claude.ai**: Individual user only; each team member must upload separately
>
> Claude.ai does not currently support centralized admin management or org-wide distribution of custom Skills.

---

### Platform 4: Claude.ai standard (web)

Same as Platform 3 (claude.ai/code is the same surface as Claude.ai standard with code execution enabled). Pre-built skills available to all claude.ai users:

> **Pre-built Agent Skills** are available to all users on claude.ai and via the Claude API. See the [Available Skills](#available-skills) section below for the complete list.
>
> - **PowerPoint (pptx)**: Create presentations, edit slides, analyze presentation content
> - **Excel (xlsx)**: Create spreadsheets, analyze data, generate reports with charts
> - **Word (docx)**: Create documents, edit content, format text
> - **PDF (pdf)**: Generate formatted PDF documents and reports

Skills run in a VM/container environment:

> Skills leverage Claude's VM environment to provide capabilities beyond what's possible with prompts alone. Claude operates in a virtual machine with filesystem access, allowing Skills to exist as directories containing instructions, executable code, and reference materials.

---

### Platform 5: Claude Cowork

From https://developer.tenten.co/claude-cowork-anthropic-brings-ai-agent-capabilities-to-non-technical-users (fetched 2026-04-12):

> **Sandboxed Permission Model:**
> "Users designate specific directories, and Claude gains read, edit, and create capabilities only within those boundaries."
>
> The system uses Apple's Virtualization Framework to create isolated Linux environments.

> **Accessibility Gap:**
> "Claude Code requires terminal proficiency, while Cowork delivers a graphical interface that removes technical barriers for knowledge workers."
>
> Claude Code is a command-line tool; Cowork operates through a desktop GUI within Claude's macOS application.

From the InfoQ article (search result, unverified, 2026-01):

> Claude Cowork, launched January 2026, extends agent capabilities to everyone else. On January 12, 2026, Anthropic announced Claude Cowork, a general-purpose AI agent designed to automate file management and document processing tasks on macOS.

> **Skills Integration**: The tool integrates with Agent Skills, Anthropic's open standard for modular AI capabilities. Skills provide specialized handling for office file formats, including XLSX, PPTX, DOCX, and PDF.

> **Sub-agent Coordination**: The architecture implements sub-agent coordination for parallelizable tasks. When presented with independent subtasks, Cowork spawns multiple Claude instances that execute concurrently and aggregate results.

---

### Platform 6: GitHub Copilot (editor — VS Code)

From https://code.visualstudio.com/docs/copilot/customization/agent-skills (fetched 2026-04-12):

> Skills must be stored in specific locations:
>
> **Project skills:** `".github/skills/"`, `".claude/skills/"`, or `".agents/skills/"` within repositories
>
> **Personal skills:** `"~/.copilot/skills/"`, `"~/.claude/skills/"`, or `"~/.agents/skills/"` in user profiles
>
> Additional project skill directories can be configured via the `chat.skillsLocations` setting.

> Each skill requires a markdown file with YAML frontmatter containing:
>
> - `name` (required): Lowercase identifier using hyphens, maximum 64 characters, must match parent directory name
> - `description` (required): What the skill does and when to use it, maximum 1024 characters
> - `argument-hint` (optional)
> - `user-invocable` (optional): Defaults to true
> - `disable-model-invocation` (optional): Defaults to false

From GitHub Docs about Copilot (search result, unverified):

> Agent Skills follows an open standard enabling portability across:
> - GitHub Copilot in VS Code
> - GitHub Copilot CLI
> - GitHub Copilot coding agent

From the VS Magazine article (search result, unverified, 2026-01-11):

> Visual Studio Code 1.108 introduces Agent Skills for GitHub Copilot, enabling developers to define reusable, domain-specific automation that can handle everything from code refactoring to custom text and formatting cleanup.

> Support for organization-level and enterprise-level skills is coming soon.

---

### Platform 7: GitHub Copilot CLI

From https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills (search result, unverified):

> Agent Skills is an open standard that works across multiple AI agents, including GitHub Copilot in VS Code, GitHub Copilot CLI, and GitHub Copilot coding agent.

Skill locations for GitHub Copilot CLI (same as cloud agent):

> **Project skills** (repository-specific):
> - `.github/skills/`
> - `.claude/skills/`
> - `.agents/skills/`
>
> **Personal skills** (cross-project):
> - `~/.copilot/skills/`
> - `~/.claude/skills/`
> - `~/.agents/skills/`

Format:

> Skills require a `SKILL.md` file formatted as Markdown with YAML frontmatter. The required frontmatter fields are:
> - **name** (required): "A unique identifier for the skill. This must be lowercase, using hyphens for spaces."
> - **description** (required): "A description of what the skill does, and when Copilot should use it."
> - **license** (optional)

> In your SKILL.md frontmatter, you can use the `allowed-tools` field to list the tools Copilot may use without asking for confirmation each time, and if a tool is not listed in the `allowed-tools` field, Copilot will prompt you for permission before using it.

Security note from Copilot cloud agent docs:

> Pre-approving shell/bash tools should only occur after reviewing trusted skill sources, as this "can allow attacker-controlled skills or prompt injections to execute arbitrary commands in your environment."

---

### Platform 8: GitHub Copilot Workspace (cloud agent)

From https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-skills (fetched 2026-04-12):

> "Agent skills work with Copilot cloud agent, the GitHub Copilot CLI, and agent mode in Visual Studio Code."

Format same as CLI and VS Code (SKILL.md with `name` + `description` required). The cloud agent additionally supports:

> An agent can invoke other agents as subagents for specialized sub-tasks, which is useful for orchestration agents that coordinate multiple specialists. You can use `agents: ['*']` to allow invocation of any available agent, or `agents: []` to prevent any subagent use.

---

### Platform 9: OpenAI Codex CLI

From https://developers.openai.com/codex/skills (fetched 2026-04-12):

Directory structure:

> ```
> my-skill/
> ├── SKILL.md (required)
> ├── scripts/ (optional)
> ├── references/ (optional)
> ├── assets/ (optional)
> └── agents/openai.yaml (optional)
> ```

Filesystem discovery:

| Scope | Path | Use Case |
|-------|------|----------|
| Repository (CWD) | `.agents/skills` | Folder-specific workflows |
| Repository (parent) | `../.agents/skills` | Nested folder organization |
| Repository (root) | `$REPO_ROOT/.agents/skills` | Organization-wide skills |
| User | `$HOME/.agents/skills` | Personal, cross-project skills |
| Admin | `/etc/codex/skills` | System-level defaults |
| System | Bundled with Codex | Built-in skills |

> "Codex supports symlinked skill folders and follows the symlink target when scanning."

Optional OpenAI-specific metadata file `agents/openai.yaml`:

> Configuration supports UI presentation, invocation policy, and tool dependencies. The `allow_implicit_invocation` field (default: `true`) prevents implicit triggering when set to `false`.

Activation methods:

> 1. **Explicit**: Direct mention via `/skills` or `$` prefix
> 2. **Implicit**: Automatic selection when task matches skill description

From the Codex blog post (search result, unverified, 2025-12-19):

> You can drop your own global skills into `~/.codex/skills/`. They're looking for any directory in that tree with a 'SKILL.md' file and going from there.

---

### Platform 10: ChatGPT custom GPTs / ChatGPT Skills

From search results (unverified, 2025-12-25):

> OpenAI is transitioning from custom GPTs to a new modular system. Developers report OpenAI is testing a new Skills system that replaces role-based GPTs with modular abilities, supporting code execution, on-demand loading and slash-command interaction across ChatGPT.

> Reports suggest the project, internally codenamed Hazelnut, will allow users and developers to teach the AI model standalone abilities, workflows and domain knowledge instead of relying only on role-based configurations.

> The actual workflow steps/instructions are usually written in a simple file called SKILL.md. Further features are expected to include slash-command interactions, a dedicated Skill editor and one-click conversion from existing GPTs.

> Custom GPTs will be transitioned to GPT-5.2 on January 12, 2026.

> Market expectations point to an early 2026 launch, signalling a move toward ChatGPT operating as an intelligent platform rather than a traditional chatbot.

> Skills can also be used across experiences like custom GPTs and projects and can incorporate apps. Skills can be exported and imported into other tools that support the Agent Skills format, including in OpenAI tools like Codex.

Note: As of research date (2026-04-12), ChatGPT Skills appear to be in late beta/early release. Custom GPTs remain the established format; the SKILL.md-based Skills feature is new as of early 2026. (All sources on this topic: **unverified**.)

---

### Platform 11: Gemini CLI

From https://geminicli.com/docs/cli/skills/ (fetched 2026-04-12):

> Skills are discovered from three tiers:
>
> 1. **Workspace Skills**: `.gemini/skills/` or `.agents/skills/`
> 2. **User Skills**: `~/.gemini/skills/` or `~/.agents/skills/`
> 3. **Extension Skills**: Bundled within installed extensions

> Within tiers, the `.agents/skills/` alias takes precedence over `.gemini/skills/`.

> The activation workflow follows these steps:
>
> - **Discovery phase**: "Gemini CLI scans the discovery tiers and injects the name and description of all enabled skills into the system prompt"
> - **Activation phase**: When matched to a task, Gemini calls the `activate_skill` tool
> - **Consent phase**: Users receive "a confirmation prompt in the UI detailing the skill's name, purpose, and the directory path"
> - **Injection phase**: Upon approval, "The `SKILL.md` body and folder structure is added to the conversation history. The skill's directory is added to the agent's allowed file paths"

> Activated skills gain "permission to read any bundled assets" within their directory after user approval.

Notable: Gemini CLI requires **explicit user consent** before activating each skill. This is distinct from Claude Code's model-driven automatic activation.

---

### Platform 12: Gemini Code Assist (VS Code / JetBrains / Android Studio)

From search results (unverified):

> If you write a skill and place it in `.agents/skills/`, both Claude Code and Gemini Code Assist can theoretically discover and utilize it, making your custom developer tools perfectly portable across different AI ecosystems.

From https://developer.android.com/studio/gemini/skills (search result, unverified):

> The agent looks for skills starting from the `.skills/` or `.agent/skills/` directories located at your project root.

From the Medium article about Gemini Code Assist (search result, unverified, 2026-04):

> Skills represent on-demand expertise that allows agents to maintain a vast library of specialized capabilities—such as security auditing, cloud deployments, or codebase migrations—without cluttering the model's immediate context window.

From the Google Codelabs page (search result, unverified):

> Gemini autonomously decides when to employ a skill based on your request and the skill's description. When a relevant skill is identified, the model "pulls in" the full instructions and resources required to complete the task using the `activate_skill` tool.

Note: Gemini Code Assist documentation does not appear to have a standalone official skills reference page; it is documented alongside Gemini CLI and Android Studio with partial overlap.

---

### Platform 13: Cursor

From https://cursor.com/docs/skills (fetched 2026-04-12):

> Skills are defined using `SKILL.md` files with YAML frontmatter. The required fields are:
> - `name`: "Skill identifier. Lowercase letters, numbers, and hyphens only."
> - `description`: "Describes what the skill does and when to use it."
>
> Optional frontmatter includes `license`, `compatibility`, `metadata`, and `disable-model-invocation`.

Directory structure:

> ```
> .agents/skills/my-skill/
> ├── SKILL.md (required)
> ├── scripts/ (optional)
> ├── references/ (optional)
> └── assets/ (optional)
> ```

Discovery locations:

> Cursor automatically discovers skills from three locations:
> - `.agents/skills/` (project-level)
> - `.cursor/skills/` (project-level)
> - `~/.cursor/skills/` (user-level/global)

> Scripts support "any language—Bash, Python, JavaScript, or any other executable format."

From the changelog entry (search result, unverified):

> Subagents, Skills, and Image Generation · Cursor changelog 2-4

From cursor-setup.md (search result, unverified):

> **Dynamic Loading vs. Rules**
>
> Unlike Rules which are always included, Skills are loaded dynamically when the agent decides they're relevant, which keeps your context window clean while giving the agent access to specialized capabilities.

Note: Cursor previously used `.cursorrules` for always-loaded context. Skills represent the progressive-disclosure approach replacing that pattern.

---

### Platform 14: Windsurf / Codeium

From https://docs.windsurf.com/windsurf/cascade/skills (fetched 2026-04-12):

> Skills require a `SKILL.md` file with YAML frontmatter. The documentation states: **"Each skill requires a `SKILL.md` file with YAML frontmatter containing the skill's metadata."**
>
> Required frontmatter fields:
> - **name**: "Unique identifier for the skill (displayed in UI and used for @-mentions)"
> - **description**: "Brief explanation shown to the model to help it decide when to invoke the skill"

Directory structure:

> **Workspace-level skills** are stored at `.windsurf/skills/<skill-name>/` and are "Committed with your repo."
>
> **Global skills** reside at `~/.codeium/windsurf/skills/<skill-name>/` and are "Not committed."
>
> **Enterprise system-level skills** use OS-specific paths:
> - macOS: `/Library/Application Support/Windsurf/skills/`
> - Linux/WSL: `/etc/windsurf/skills/`
> - Windows: `C:\ProgramData\Windsurf\skills\`
>
> Cross-agent compatibility includes `.agents/skills/`, `~/.agents/skills/`, `.claude/skills/`, and `~/.claude/skills/`.

Loading behavior:

> Cascade employs **"progressive disclosure"**: "only the skill's `name` and `description` are shown to the model by default. The full `SKILL.md` content and supporting files are loaded **only when Cascade decides to invoke the skill**."

---

### Platform 15: Amazon Q Developer / Kiro

From https://kiro.dev/docs/skills/ (fetched 2026-04-12):

> Skills can have two scopes:
>
> - **Workspace skills**: Located at `.kiro/skills/` within a project; apply only to that workspace
> - **Global skills**: Located at `~/.kiro/skills/` in the home directory; available across all workspaces
>
> When naming conflicts occur, workspace skills take precedence over global skills.

Format:

> The file uses frontmatter to define metadata:
>
> Required frontmatter fields:
>
> | Field | Purpose |
> |-------|---------|
> | **name** | Must match folder name; lowercase, numbers, hyphens only (max 64 characters) |
> | **description** | Specifies when to activate; Kiro matches this against user requests (max 1024 chars) |
>
> Optional fields: `license`, `compatibility`, and `metadata`.

From search result for Amazon Q Developer (unverified):

> Amazon Q Developer CLI has added Model Context Protocol (MCP) support that standardizes how applications provide context to Large Language Models, allowing developers to seamlessly integrate additional tools and data sources into their AI-assisted workflow.

> Skills are portable packages following an open standard. The SKILL.md format has become the de facto standard across major AI coding platforms including Claude Code.

Note: "Amazon Q Developer" and "Kiro" appear to be distinct products. Kiro is AWS's new IDE that launched in early 2026; Amazon Q Developer is the existing assistant that predates Kiro. Kiro's skills documentation is available; Amazon Q Developer's native SKILL.md support is unclear and its documentation is primarily about MCP integration.

---

### Platform 16: LangChain / LangGraph (Deep Agents)

From https://docs.langchain.com/oss/python/deepagents/skills (fetched 2026-04-12):

> Skills organize as directories containing specialized files. As stated, "Skills are a directory of folders, where each folder has one or more files that contain context the agent can use." Each skill folder requires:
>
> - `SKILL.md` file (instructions and metadata)
> - Optional scripts, reference docs, templates, and assets

> The `SKILL.md` file follows a consistent pattern beginning with YAML frontmatter. Required fields include `name` and `description`. Optional frontmatter fields encompass `license`, `compatibility`, `metadata`, and `allowed-tools`. Notably, the "description field is truncated to 1024 characters if it exceeds that length."

Loading constraints:

> When creating a deep agent, pass skill source paths via the `skills` parameter. The documentation explains that "Paths must be specified using forward slashes and are relative to the backend's root." Different backends handle skills differently—`StateBackend` requires formatted file data, `FilesystemBackend` loads from disk, and `StoreBackend` retrieves from configured storage.

> A critical constraint: "In Deep Agents, `SKILL.md` files must be under 10 MB. Files exceeding this limit are skipped during skill loading."

> The agent employs "progressive disclosure"—it only reviews skill details when determining relevance.

Note: LangChain supports skills via the `deepagents` module. Standard LangChain tools are Python `@tool` decorated functions; the SKILL.md format is implemented through the separate deep agents layer. LangGraph 1.0 and LangChain 1.0 were released in late 2025.

---

### Platform 17: AutoGen / Microsoft Agent Framework

From https://learn.microsoft.com/en-us/agent-framework/agents/skills (fetched 2026-04-12):

> [Agent Skills](https://agentskills.io/) are portable packages of instructions, scripts, and resources that give agents specialized capabilities and domain expertise. Skills follow an open specification and implement a progressive disclosure pattern so agents load only the context they need, when they need it.

Directory structure:

> ```
> expense-report/
> ├── SKILL.md                          # Required — frontmatter + instructions
> ├── scripts/
> │   └── validate.py
> ├── references/
> │   └── POLICY_FAQ.md
> └── assets/
>     └── expense-report-template.md
> ```

The framework exposes tools to the agent:

> - `load_skill` — Retrieves the full SKILL.md instructions when the agent determines a user's request matches a skill's domain.
> - `read_skill_resource` — Fetches supplementary files (references, templates, assets) bundled with a skill.

Note: `run_skill_script` is a third tool. "`load_skill` is always advertised. `read_skill_resource` is advertised only when at least one skill has resources. `run_skill_script` is advertised only when at least one skill has scripts."

Four-stage progressive disclosure pattern:

> 1. **Advertise** (~100 tokens per skill) — Skill names and descriptions are injected into the system prompt at the start of each run.
> 2. **Load** (< 5000 tokens recommended) — Agent calls the `load_skill` tool.
> 3. **Read resources** (as needed) — Agent calls the `read_skill_resource` tool.
> 4. **Run scripts** (as needed) — Agent calls the `run_skill_script` tool.

Script execution:

> `SubprocessScriptRunner.RunAsync` runs each discovered script as a local subprocess, forwarding the JSON arguments provided by the agent as command-line flags.

Customizable resource discovery:

> By default, the provider recognizes resources with extensions `.md`, `.json`, `.yaml`, `.yml`, `.csv`, `.xml`, and `.txt` in `references` and `assets` subdirectories.

Script discovery defaults:

> By default, the provider recognizes scripts with extensions `.py`, `.js`, `.sh`, `.ps1`, `.cs`, and `.csx` in the `scripts` subdirectory.

Note: Microsoft Agent Framework is described as "the enterprise-ready successor to AutoGen" combining Semantic Kernel foundations and AutoGen orchestration. "Semantic Kernel + AutoGen = Open-Source 'Microsoft Agent Framework'" (Visual Studio Magazine, 2025-10-01, unverified). AutoGen 0.2 documentation still exists separately.

Three skill source types in Microsoft Agent Framework:

> - **File-based** — skills discovered from `SKILL.md` files in filesystem directories
> - **Code-defined** — skills defined inline in code using `AgentInlineSkill` (C#) or `Skill` (Python)
> - **Class-based** — skills encapsulated in a C# class deriving from `AgentClassSkill<T>` (C# only)

---

### Platform 18: CrewAI

From https://docs.crewai.com/en/concepts/skills (fetched 2026-04-12):

> Skills are self-contained directories that provide agents with domain-specific instructions, guidelines, and reference material. Each skill is defined by a SKILL.md file with YAML frontmatter and a markdown body.

> Required frontmatter: `name` (1–64 chars, lowercase alphanumeric and hyphens, must match directory name), `description` (1–1024 chars).

Key distinction from other platforms:

> The `allowed-tools` field represents "experimental metadata only — it does not provision or inject any tools." Developers must separately configure tools through `tools=[]`, `mcps=[]`, or `apps=[]` parameters.

> A "soft warning" appears at 50,000 characters for SKILL.md body size, though no hard limit exists.

> "During typical agent setup (passing directory paths), both stages execute automatically. The markdown body gets 'injected directly into the agent's task prompt.'"

Notable difference: CrewAI injects skills directly into the agent's task prompt (not loaded on demand via a tool call), which differs from Claude Code's progressive disclosure model. Also, tools are provisioned separately from the skill file.

---

### Platform 19: Semantic Kernel

From search results (unverified) and Microsoft Learn (Platform 17 / Microsoft Agent Framework covers Semantic Kernel as its foundation):

> Microsoft has released version 1.0 of its open-source Agent Framework, positioning it as the production-ready evolution of the project introduced in October 2025 by combining Semantic Kernel foundations, AutoGen orchestration concepts, and stable APIs for .NET and Python.

Semantic Kernel's native plugin format (predating Agent Skills) used XML-annotated C# functions or YAML prompt templates. As of late 2025, Microsoft has unified under the Agent Skills standard in the Microsoft Agent Framework. From the blog post (unverified, 2026-03):

> Agent Skills extend agent capabilities without modifying core instructions, turn multi-step tasks into repeatable, auditable workflows, and enable interoperability across different Agent Skills-compatible products.

---

## Sub-question 2: Capability differences across platforms

### Filesystem access

**Full filesystem access (subject to user permissions):**
- Claude Code CLI: Full filesystem access. "Skills have the same network access as any other program on the user's computer."
- GitHub Copilot (VS Code, CLI, Workspace): Full filesystem access within the repository and user home.
- OpenAI Codex CLI: Full filesystem access.
- Gemini CLI: Activated skills gain permission to read bundled assets; general filesystem access follows CLI permissions.
- Cursor: Full filesystem access within workspace.
- Windsurf/Codeium: Full filesystem access within workspace.
- Amazon Q Developer / Kiro: Full filesystem access within workspace.
- LangChain Deep Agents: Backend-dependent (`FilesystemBackend` for disk access).
- Microsoft Agent Framework / AutoGen: Filesystem access via `AgentSkillsProvider` pointing to configured directories.
- CrewAI: Framework-level filesystem access.

**Sandboxed / restricted filesystem access:**
- Claude API: "No network access: Skills cannot make external API calls or access the internet. No runtime package installation: Only pre-installed packages are available."
- Claude.ai (web): "Varying network access: Depending on user/admin settings, Skills may have full, partial, or no network access." Runs in VM/container environment.
- Claude Cowork: "Users designate specific directories, and Claude gains read, edit, and create capabilities only within those boundaries." Uses Apple's Virtualization Framework.

**Upload-based (no direct filesystem):**
- ChatGPT custom GPTs / ChatGPT Skills: Upload-based. Skills uploaded as zip files or via API. ChatGPT skills have code interpreter container access (`/home/oai/skills`).

---

### Subagent spawning

**Supported natively:**
- Claude Code CLI: `context: fork` spawns isolated subagent. `agent:` field selects subagent type (`Explore`, `Plan`, `general-purpose`, or custom). Worktree isolation (2026) supports multiple subagents with parallel git worktrees.
- Claude Cowork: "Sub-agent Coordination: The architecture implements sub-agent coordination for parallelizable tasks. When presented with independent subtasks, Cowork spawns multiple Claude instances that execute concurrently."
- GitHub Copilot Workspace (cloud agent): `agents: ['*']` to allow invocation of any available agent.
- Microsoft Agent Framework: Multi-agent orchestration is a first-class feature.
- LangGraph: Supervisor agent patterns for multi-agent orchestration.

**Not part of the skill format (external to skill):**
- CrewAI: Multi-agent coordination is a framework concern (Crew + Process), not a skill frontmatter concern.
- OpenAI Codex CLI: No subagent field in SKILL.md standard; team-level coordination is external.

**Unclear/not documented in skills context:**
- Gemini CLI, Cursor, Windsurf: Subagent spawning is not mentioned in skills documentation.

---

### Tool availability

**Tools managed via `allowed-tools` frontmatter field:**
- Claude Code CLI: `allowed-tools` grants permission for listed tools while skill is active, but does NOT restrict other tools. "Your permission settings still govern tools that are not listed."
- GitHub Copilot (all surfaces): `allowed-tools` determines what Copilot can use without per-use confirmation.
- OpenAI Codex CLI: `agents/openai.yaml` controls tool dependencies.
- Windsurf/Codeium: `allowed-tools` supported.
- Kiro/Amazon Q: Standard `allowed-tools` field.

**`allowed-tools` is metadata-only (no enforcement):**
- CrewAI: "The `allowed-tools` field represents 'experimental metadata only — it does not provision or inject any tools.' Developers must separately configure tools through `tools=[]`, `mcps=[]`, or `apps=[]` parameters."

**Tool availability via explicit tool registration:**
- LangChain: `@tool` decorator. Agent Skills SKILL.md `allowed-tools` is read but tools still need Python registration.
- Microsoft Agent Framework: `load_skill`, `read_skill_resource`, `run_skill_script` are the skill-specific tools advertised by the framework.

---

### Browser/display access

- Claude Code CLI: No built-in browser. Visual output (HTML) can be generated and opened via `webbrowser.open()` in scripts. "Claude in Chrome" (beta integration) allows Claude Code CLI to interact with Chrome extension.
- Claude.ai / Claude Cowork: Claude.ai runs in browser; Cowork is macOS desktop app.
- ChatGPT / custom GPTs: Web interface; code interpreter environment has no browser automation built in.
- GitHub Copilot Workspace: Web-based interface; no browser automation.
- All CLI tools (Gemini CLI, Codex CLI, etc.): Terminal only; no display capability.
- Cursor / Windsurf: IDE-embedded; preview panes, not browser automation.

---

## Sub-question 3: Constraints on where skill outputs should be placed

### Eval workspace layout (agentskills.io specification)

From https://agentskills.io/skill-creation/evaluating-skills (fetched 2026-04-12):

> Organize eval results in a workspace directory alongside your skill directory. Each pass through the full eval loop gets its own `iteration-N/` directory. Within that, each test case gets an eval directory with `with_skill/` and `without_skill/` subdirectories:
>
> ```
> csv-analyzer/
> ├── SKILL.md
> └── evals/
>     └── evals.json
> csv-analyzer-workspace/
> └── iteration-1/
>     ├── eval-top-months-chart/
>     │   ├── with_skill/
>     │   │   ├── outputs/       # Files produced by the run
>     │   │   ├── timing.json    # Tokens and duration
>     │   │   └── grading.json   # Assertion results
>     │   └── without_skill/
>     │       ├── outputs/
>     │       ├── timing.json
>     │       └── grading.json
>     ├── eval-clean-missing-emails/
>     │   ...
>     └── benchmark.json         # Aggregated statistics
> ```
>
> The main file you author by hand is `evals/evals.json`. The other JSON files (`grading.json`, `timing.json`, `benchmark.json`) are produced during the eval process.

> In environments that support subagents (Claude Code, for example), this isolation comes naturally: each child task starts fresh. Without subagents, use a separate session for each run.

> For each run, provide:
> * The skill path (or no skill for the baseline)
> * The test prompt
> * Any input files
> * The output directory

Sample run instruction format from eval spec:

> ```
> Execute this task:
> - Skill path: /path/to/csv-analyzer
> - Task: I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?
> - Input files: evals/files/sales_2025.csv
> - Save outputs to: csv-analyzer-workspace/iteration-1/eval-top-months-chart/with_skill/outputs/
> ```

`timing.json` schema:

> ```json
> {
>   "total_tokens": 84852,
>   "duration_ms": 23332
> }
> ```

> In Claude Code, when a subagent task finishes, the task completion notification includes `total_tokens` and `duration_ms`.

`benchmark.json` schema:

> ```json
> {
>   "run_summary": {
>     "with_skill": {
>       "pass_rate": { "mean": 0.83, "stddev": 0.06 },
>       "time_seconds": { "mean": 45.0, "stddev": 12.0 },
>       "tokens": { "mean": 3800, "stddev": 400 }
>     },
>     "without_skill": { ... },
>     "delta": { "pass_rate": 0.50, "time_seconds": 13.0, "tokens": 1700 }
>   }
> }
> ```

---

### Platform-specific output placement constraints

**Claude Code CLI:**

> Skills can include scripts that produce output. The `${CLAUDE_SKILL_DIR}` variable references the skill directory at runtime. Output files from skills go to CWD unless paths are specified explicitly. No hard restriction on output placement within permitted directories.

**Claude API (VM environment):**

> **No runtime package installation**: Only pre-installed packages are available. You cannot install new packages during execution.

**Claude.ai:**

> **Varying network access**: Depending on user/admin settings, Skills may have full, partial, or no network access.

**Claude Cowork:**

> Users designate specific directories, and Claude gains read, edit, and create capabilities only within those boundaries. File paths like `/sessions/zealous-bold-ramanujan/mnt/blog-drafts` demonstrate the containerization approach.

**Windsurf/Codeium:**

> "Never hard-code machine-specific paths like `/Users/alice/`. Use relative paths or well-known variables (`$HOME`, `$PROJECT_ROOT`)."

**Microsoft Agent Framework:**

> By default, the provider recognizes resources with extensions `.md`, `.json`, `.yaml`, `.yml`, `.csv`, `.xml`, and `.txt` in `references` and `assets` subdirectories.

**LangChain Deep Agents:**

> "In Deep Agents, `SKILL.md` files must be under 10 MB. Files exceeding this limit are skipped during skill loading."

> "Paths must be specified using forward slashes and are relative to the backend's root."

**Folder naming convention guidance (from apiyi.com, unverified):**

> `.claude/skills/` uses `SKILL.md` format — "Markdown files with YAML front matter" where instructions are human-readable and Claude Code automatically discovers them.
>
> `.agents/skills/` uses `SKILL.yaml` format — pure YAML structure designed for machine parsing and cross-tool compatibility. (Note: this is an unverified claim about `.agents/` using a different format; the open standard specifies SKILL.md for all compliant platforms.)

---

## Sub-question 4: Minimum common denominator vs. platform-specific

### What works everywhere (minimum common denominator)

From https://inference.sh/blog/skills/agent-skills-overview (fetched 2026-04-12):

> "The SKILL.md format is universal. The metadata format is universal. The progressive disclosure pattern is universal."

> All platforms support:
> - SKILL.md files with YAML frontmatter (name, description)
> - Progressive context loading (metadata → full content → additional files)
> - Executable code within skills
> - Agent-driven skill discovery based on descriptions

Spec-compliant minimum common denominator (verified against agentskills.io spec):

1. `SKILL.md` file with YAML frontmatter at minimum containing `name` (1-64 chars, lowercase alphanumeric + hyphens, matches directory name) and `description` (1-1024 chars).
2. Directory layout: `skill-name/SKILL.md` with optional `scripts/`, `references/`, `assets/`.
3. Progressive disclosure: metadata at startup (~100 tokens), full body on activation (< 5000 tokens recommended), resources on demand.
4. Body in Markdown (no format restrictions).
5. Invocable via `/skill-name` slash command on platforms supporting it.

Optional fields with broad-but-not-universal support: `license`, `compatibility`, `metadata`, `allowed-tools` (experimental across all platforms).

---

### Claude Code CLI-specific features (not in the open standard)

From https://code.claude.com/docs/en/skills:

1. **`context: fork`** — Runs skill in an isolated subagent. No equivalent in the open standard or most other platforms.
2. **`agent:` field** — Specifies subagent type when `context: fork` is set. Claude Code-specific.
3. **`model:` field** — Override model per skill. Claude Code-specific.
4. **`effort:` field** — Override effort level. Claude Code-specific.
5. **`hooks:` field** — Lifecycle hooks scoped to a skill. Claude Code-specific.
6. **`paths:` field** — Glob patterns for path-gated activation. Claude Code-specific.
7. **`shell:` field** — Shell selection (`bash` or `powershell`). Claude Code-specific.
8. **`user-invocable:` field** — Hide from `/` menu. Claude Code-specific extension.
9. **`disable-model-invocation:` field** — Not in the open standard spec (present as extension).
10. **`argument-hint:` field** — Not in open standard.
11. **Dynamic shell injection** — `` !`command` `` and ` ```! ` blocks. Claude Code-specific.
12. **`$ARGUMENTS`, `$N`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_SKILL_DIR}`** string substitutions. Claude Code-specific.
13. **Plugin-level skills** with `plugin-name:skill-name` namespace. Claude Code-specific.
14. **Worktree isolation** (`isolation: worktree`) for parallel subagents. Claude Code-specific (2026).
15. **Hot-reloading** (skills activate immediately without session restart, from 2026-01-07 release).
16. **Skill content lifecycle** — Re-attachment after compaction (first 5,000 tokens per skill, 25,000 token combined budget). Claude Code-specific behavior.
17. **`SLASH_COMMAND_TOOL_CHAR_BUDGET` env var** for controlling description truncation. Claude Code-specific.

---

### Platform-specific extensions (not Claude Code, not universal)

**OpenAI Codex CLI only:**
- `agents/openai.yaml` inside skill directory for OpenAI-specific metadata.
- `/etc/codex/skills` admin-level discovery path.
- `$` prefix for explicit skill invocation.

**Microsoft Agent Framework / AutoGen only:**
- Code-defined skills (`AgentInlineSkill`, `Skill` class, `AgentClassSkill<T>`).
- Builder pattern (`AgentSkillsProviderBuilder`).
- Script approval (`ScriptApproval = true`).
- DI injection via `IServiceProvider`.
- Caching control (`DisableCaching`).
- `read_skill_resource`, `run_skill_script` as explicit tool names.

**CrewAI only:**
- Skills inject directly into agent task prompt (not loaded via tool call).
- 50,000-character soft warning (no hard limit, unlike the 500-line/5000-token guidance in other platforms).
- `allowed-tools` is metadata-only.

**LangChain Deep Agents only:**
- 10 MB hard limit on `SKILL.md` files.
- `StateBackend`, `FilesystemBackend`, `StoreBackend` backend selection.
- Paths must use forward slashes, relative to backend root.

**Gemini CLI only:**
- Explicit user consent prompt before each skill activation.
- `activate_skill` tool call visible to user.
- Extension Skills tier (bundled with Gemini CLI extensions).

**Windsurf/Codeium only:**
- Enterprise OS-level skill paths (`/Library/Application Support/Windsurf/skills/`, `/etc/windsurf/skills/`, `C:\ProgramData\Windsurf\skills\`).
- `@-mention` invocation.

**Kiro (Amazon Q Developer) only:**
- `.kiro/skills/` as the native project-level path.
- `skill://` URI scheme for direct skill references.

---

### Portability risks and anti-patterns

From Claude API docs:

> **Custom Skills do not sync across surfaces.** Skills uploaded to one surface are not automatically available on others.

From apiyi.com (unverified):

> Claude Code natively discovers and loads Skills only from the `.claude/skills/` directory, and content within `.agents/skills/` is not automatically recognized, so skills must currently be placed in `.claude/skills/` to work in Claude Code.

Note: This claim conflicts with the official Claude Code docs which list `.claude/skills/` as the canonical path but also accept skills from `--add-dir` flag directories. The `.agents/skills/` path is supported by most other platforms (Codex, Cursor, Windsurf, Kiro, GitHub Copilot) but is NOT the primary path for Claude Code. **Claude Code's primary path is `.claude/skills/`; `.agents/skills/` support is inconsistent or secondary.**

From agentskills.io spec:

> "Platform-specific differences mainly concern where skills are stored and how they are triggered."

Best practices for cross-platform skills (from multiple sources):

> - Never hard-code machine-specific paths (e.g., `/Users/alice/`). Use relative paths or `$HOME`, `$PROJECT_ROOT`.
> - Keep SKILL.md under 500 lines / 5000 tokens for broadest compatibility.
> - Use only `name` and `description` in frontmatter for maximum portability; treat all other fields as platform extensions.
> - Avoid Claude Code-specific syntax (`` !`command` ``, `$ARGUMENTS`, `context: fork`) in skills intended for other platforms.
> - Store the `compatibility` field to declare platform requirements.

---

## Challenge

*Challenger agent analysis — competitive mode. Assumptions Check + ACH + Premortem.*

---

### Assumptions Check

The draft's emerging findings rest on five key assumptions. Each is examined below.

---

**Assumption A1: The Agent Skills open standard achieves genuine cross-platform portability**

*Claim:* A skill authored with `name` + `description` and stored in a spec-compliant directory will work portably across all 19 platforms with no meaningful behavioral difference.

*Supporting evidence:* All 19 platforms document SKILL.md with `name`/`description` as required. The agentskills.io specification is explicit about the minimum schema. Multiple T1 sources describe it as a universal format.

*Counter-evidence:* Simon Willison (independent, credible technical observer) called the spec "quite heavily under-specified" at launch — the `metadata` field has no enforcement, and `allowed-tools` is labeled "Experimental" with "varying support between implementations" (simonwillison.net, Dec 2025). Actual behavioral differences are significant and not cosmetic: on the Claude API, skills have no network access; on Claude Code CLI they have full network access; on Claude.ai it varies by admin settings. The draft itself documents that CrewAI injects skills directly into task prompts instead of loading them on demand, that `allowed-tools` is metadata-only in CrewAI, and that LangChain imposes a 10 MB hard file limit. A skill using shell scripts may execute on Claude Code and fail silently on Claude.ai or the API entirely. The "portability" the standard provides is syntactic (same file format), not semantic (same runtime behavior).

*Impact if false:* The minimum-common-denominator guidance understates the risk. "Write once, run everywhere" fails in practice for any skill that relies on network access, shell execution, subagent spawning, or `allowed-tools` enforcement. The portability claim would need significant qualification.

---

**Assumption A2: The `.agents/skills/` path is a reliable cross-platform discovery location**

*Claim:* Placing skills in `.agents/skills/` ensures they are discovered by most platforms as a neutral cross-platform path.

*Supporting evidence:* GitHub Copilot (VS Code, CLI, Workspace), OpenAI Codex, Cursor, Windsurf, and Kiro all support `.agents/skills/` as a discovery path.

*Counter-evidence:* The draft itself flags this: "Claude Code's primary path is `.claude/skills/`; `.agents/skills/` support is inconsistent or secondary." The official Claude Code docs list four discovery paths (Enterprise, Personal, Project, Plugin) and none of them is `.agents/skills/`. The only way `.agents/skills/` reaches Claude Code is via the `--add-dir` flag or equivalent configuration, which is not automatic. This means the most popular CLI agent (Claude Code, 82K+ stars as of March 2026) does not auto-discover from `.agents/skills/` without extra configuration. The draft's portability anti-patterns section notes this inconsistency but the Sub-question 4 summary minimizes it.

*Impact if false:* The recommendation to use `.agents/skills/` for cross-platform skills is misleading for teams whose primary runtime is Claude Code. The correct guidance would require maintaining two directories (`.agents/skills/` and `.claude/skills/`) or accepting that Claude Code users need manual configuration.

---

**Assumption A3: The standard's governance is stable and independent**

*Claim:* Agent Skills is an open standard with governance independent enough that competitors can adopt it without strategic risk, similar to how MCP became ubiquitous.

*Supporting evidence:* The spec was migrated from `github.com/anthropics/skills` to `agentskills.io` (nominally independent). Microsoft, OpenAI, Google, and GitHub have all adopted it. The Anthropic launch blog emphasizes openness and references community governance.

*Counter-evidence:* The `agentskills.io` domain and the `agentskills/agentskills` GitHub org are both Anthropic-controlled in practice (redirect from `anthropics/skills`). Simon Willison noted in December 2025 that governance structure is undefined — it is unclear whether this will fall under the Agentic AI Foundation or require its own structure. The draft cites The New Stack characterizing Agent Skills as "Anthropic's next bid to define AI standards," framing adoption by competitors as Anthropic gaining infrastructure control rather than true community governance. There is an independent alternative spec appearing at `openagentskills.dev` (found in search results), suggesting community tension. The MCP analogy is imperfect: MCP predates Agent Skills by over a year, has wider formal adoption, and has been submitted to the Linux Foundation. Agent Skills governance remains informal as of April 2026.

*Impact if false:* If the standard is effectively Anthropic-controlled, enterprise adopters face the same vendor lock-in risk that the standard purportedly solves. Competitors may eventually fork or diverge to avoid strategic dependence. The "open standard" framing would be marketing rather than technical reality.

---

**Assumption A4: The `allowed-tools` field provides meaningful security control**

*Claim:* The `allowed-tools` frontmatter field, when populated, gives meaningful pre-approval to tool invocations and can be used as part of a security model.

*Supporting evidence:* Claude Code docs state `allowed-tools` grants permission for listed tools while skill is active. GitHub Copilot uses it to determine what Copilot can use without per-use confirmation.

*Counter-evidence:* The draft itself documents that in CrewAI, `allowed-tools` is "experimental metadata only — it does not provision or inject any tools." The Snyk ToxicSkills study (Feb 2026) found 91% of malicious skills use prompt injection techniques and that Agent Skills inherit full agent permissions — including shell access, file system write, and credential access. The GitHub Copilot security note warns that pre-approving shell/bash tools in `allowed-tools` "can allow attacker-controlled skills or prompt injections to execute arbitrary commands." The `allowed-tools` field is a whitelist, not a permission boundary: platforms that honor it still execute whatever the agent decides to call if the field is absent, meaning omission provides no restriction. The Snyk study found 36.82% of ClawHub skills contain at least one vulnerability.

*Impact if false:* Authors and enterprises relying on `allowed-tools` for security posture are exposed. The field works differently (or not at all) across platforms and provides no supply-chain protection. Any recommendation to use `allowed-tools` for security should be accompanied by a supply-chain trust warning.

---

**Assumption A5: ChatGPT Skills (Hazelnut) is in scope as a real platform for SKILL.md-based skills**

*Claim:* ChatGPT Skills is an emerging 19th platform that will adopt the Agent Skills SKILL.md format and is properly included in the platform matrix.

*Supporting evidence:* Multiple sources (BleepingComputer, Aibase) reported internal codenamed "Hazelnut" project that will use SKILL.md and support slash-command invocation. OpenAI's Codex CLI (sources 10–11) already uses SKILL.md.

*Counter-evidence:* As of April 2026, no T1 source confirms ChatGPT Skills has shipped to GA. All ChatGPT-specific claims are sourced from leaks and beta reports. OpenAI's official Codex CLI documentation is available and verified, but that is a separate product from ChatGPT. The claim "Custom GPTs will be transitioned to GPT-5.2 on January 12, 2026" did not appear to come true as announced — OpenAI's release notes (from releasebot.io and help.openai.com) do not reference a Skills GA launch. The draft correctly flags this as LOW confidence but includes ChatGPT as Platform 10 in the capability matrix without adequate qualification in the summary.

*Impact if false:* The "19 platforms" headline is partially inflated. If ChatGPT Skills has not shipped, the actual cross-platform count is 18 confirmed platforms. More critically, any guidance written for "ChatGPT Skills" may not match the eventual GA product.

---

### ACH (Analysis of Competing Hypotheses)

Three hypotheses are evaluated against the evidence items.

**Evidence items:**
- E1: All 19 documented platforms use SKILL.md with name/description (T1 sources)
- E2: Simon Willison: spec is "quite heavily under-specified"; `allowed-tools` has "varying support" (T1 observer)
- E3: Runtime behavior diverges significantly: no-network API vs. full-network CLI vs. variable claude.ai (T1)
- E4: Claude Code does not auto-discover `.agents/skills/`; its primary path is `.claude/skills/` (T1)
- E5: CrewAI injects skills into task prompt rather than loading on-demand; `allowed-tools` is metadata-only (T1)
- E6: 36.82% of ClawHub skills contain vulnerabilities; 13.4% critical-level (Snyk ToxicSkills study, T2)
- E7: Governance of agentskills.io is undefined; alternative spec at openagentskills.dev exists (T3/T4)
- E8: ChatGPT Skills (Hazelnut) has no confirmed GA release as of April 2026 (T4/T5 only)
- E9: Over 30 platforms adopted the standard; Microsoft, OpenAI, Google all formally participate (T1)
- E10: Cross-platform skill portability requires two directories for Claude Code + other platforms (T1 inference)

**H1 (Supports draft): Agent Skills is a genuine open standard achieving substantial cross-platform portability. Syntactic convergence (SKILL.md format) is sufficient for practical use; behavioral differences are edge cases handled by the `compatibility` field.**

| Evidence | Rating | Notes |
|---|---|---|
| E1 | C | All platforms use SKILL.md — strong format convergence |
| E2 | I | Under-specification creates behavioral gaps |
| E3 | I | Runtime divergence is significant, not an edge case |
| E4 | I | Primary portability path breaks for Claude Code |
| E5 | I | CrewAI's semantic difference undermines "universal behavior" |
| E6 | N | Supply-chain security is orthogonal to portability |
| E7 | I | Governance gap weakens "open standard" claim |
| E8 | I | 19-platform count is inflated |
| E9 | C | Major platform adoption confirms real traction |
| E10 | I | Dual-directory requirement is a real friction |

H1 inconsistencies: 6 | Consistent: 2

---

**H2 (Challenger): Agent Skills achieves syntactic standardization but not behavioral standardization. The standard is better described as a lowest-common-denominator file format than a portable skill runtime. Platform-specific extensions dominate in practice.**

| Evidence | Rating | Notes |
|---|---|---|
| E1 | C | Format is converged — consistent with "syntactic standard" |
| E2 | C | Under-specification confirms limited behavioral guarantees |
| E3 | C | Runtime divergence directly supports this framing |
| E4 | C | Claude Code's path divergence is a concrete example |
| E5 | C | CrewAI's prompt-injection model vs. progressive disclosure is exactly this gap |
| E6 | N | Orthogonal to format vs. behavior question |
| E7 | C | Governance ambiguity is consistent with "industry-specific extensions dominating" |
| E8 | C | ChatGPT inclusion is consistent with loose standard definition |
| E9 | I | Major platform adoption with broad participation is harder to explain if standard is hollow |
| E10 | C | Dual-directory requirement is evidence of behavioral non-convergence |

H2 inconsistencies: 1 | Consistent: 8

---

**H3 (Alternative): Agent Skills adoption is an Anthropic strategic infrastructure play. Competitors adopt the format to avoid being excluded from an emerging ecosystem, not because the standard solves their problems. Long-term, expect divergence as each vendor extends their implementation.**

| Evidence | Rating | Notes |
|---|---|---|
| E1 | C | Quick cross-competitor adoption is consistent with competitive pressure |
| E2 | C | Under-specification leaves room for vendor-specific extensions |
| E3 | C | Runtime divergence is already starting |
| E4 | C | Claude Code's primary path being `.claude/` not `.agents/` suggests Anthropic's own interest in Claude-specific discovery |
| E5 | C | CrewAI's divergent injection model is consistent with vendors adapting spec to their architecture |
| E6 | N | Security problems are orthogonal |
| E7 | C | Undefined governance and alternative spec at openagentskills.dev are consistent with strategic tension |
| E8 | N | ChatGPT GA status is orthogonal to strategic framing |
| E9 | I | Genuine adoption by competitors like Microsoft and OpenAI is harder to explain as purely defensive |
| E10 | C | Platform-specific path preferences are consistent with controlled divergence |

H3 inconsistencies: 1 | Consistent: 7

---

**ACH verdict:** H2 has the fewest inconsistencies and best accounts for the evidence. H3 is close (1 inconsistency, same as H2) and acts as a causal explanation for H2's observation. H1, the draft's implicit hypothesis, carries 6 inconsistencies and requires E2/E3/E4/E5/E7/E10 to be dismissed as edge cases.

**Selected hypothesis:** H2 — Agent Skills achieves syntactic but not behavioral standardization. The SKILL.md format is universal; the runtime semantics are not.

The practical implication: skills must be designed for a target platform first and portability second. The "minimum common denominator" section in Sub-question 4 is accurate but undersells how much work is required to achieve actual cross-platform behavior parity.

---

### Premortem

*Assume the main conclusion is wrong: assume that Agent Skills does NOT represent a meaningful common denominator across the 19 platforms, and the "open standard" framing leads developers astray. Why might this be true?*

---

**Reason 1: The standard is a marketing coordination artifact, not a technical interoperability mechanism**

Major platform adopters (GitHub Copilot, OpenAI Codex, Google Gemini CLI) may have adopted SKILL.md primarily to signal ecosystem participation in a high-momentum moment, not because the format solves a real portability problem they faced. Each platform already had its own instruction/rules mechanism (`.cursorrules`, Copilot instructions, Gemini system instructions). SKILL.md is an additive layer on top of their existing systems, not a replacement. In 12–18 months, if usage data shows that skills written for Claude Code fail in Copilot without modification (due to dynamic shell injection, `context: fork`, path divergences), developers may stop attempting cross-platform authoring and treat the standard as a per-platform convention rather than a portability guarantee.

*Plausibility:* Medium-high. The under-specification evidence (E2) and behavioral divergence (E3, E5) support this. The MCP comparison cuts both ways: MCP also took 18+ months to achieve real semantic interoperability, not just syntactic adoption.

*Impact on conclusion:* High. If true, Sub-question 4's "minimum common denominator" section should be titled "minimum common denominator syntax" with an explicit warning that runtime portability requires per-platform testing.

---

**Reason 2: Security risks make community-published skills non-viable, collapsing the ecosystem**

The ToxicSkills study found 36.82% of ClawHub skills contain vulnerabilities and 91% of malicious skills use prompt injection. If skill distribution platforms (ClawHub, the hypothetical skill registries mentioned in research) become synonymous with supply-chain risk, enterprise adoption will stall or be restricted to internally authored skills only. This would fragment the ecosystem: enterprises maintain internal skill inventories that differ per platform (because each team develops for their primary agent), negating the portability promise. The "thousands of community-contributed skills" framing in the broader ecosystem narrative would be revealed as a vulnerability surface, not a feature.

*Plausibility:* Medium. The security finding is from a single study (Snyk, February 2026) and reflects an early ecosystem with poor curation. Python's early PyPI had similar supply-chain issues that were eventually addressed by tooling. However, agent skills inherit full shell/credential permissions, which is qualitatively worse than a rogue npm package.

*Impact on conclusion:* Medium. Portability between platforms is moot if security posture prevents adoption of community skills entirely. The research does not address supply-chain risk at all in its findings, leaving a material gap.

---

**Reason 3: Claude Code's growing extension surface will create a de facto Claude-specific skill dialect**

Claude Code already has 17 documented extensions beyond the open standard (Sub-question 4): `context: fork`, `model:`, `effort:`, `hooks:`, `paths:`, dynamic shell injection, `$ARGUMENTS` substitution, worktree isolation, and more. Skills written to leverage Claude Code's capabilities will increasingly depend on these extensions, because they solve real problems (subagent isolation, dynamic context injection, path-gated activation) that the base spec does not address. As Claude Code's user base grows, the dominant skill authoring pattern will target Claude Code first. When such skills are used on other platforms, the unsupported frontmatter fields will be silently ignored (or cause errors), and the dynamic shell blocks will be treated as literal Markdown. Over time, the practical "Claude Code skill dialect" diverges from the spec, even if every platform nominally supports SKILL.md. This mirrors what happened with HTML "standards" in the IE6 era.

*Plausibility:* Medium. Claude Code's extension count is already significant (17 items listed in Sub-question 4). The "hot-reloading," `context: fork`, and dynamic shell injection features are genuinely compelling and have no equivalents in the open standard. The countervailing force is the developer community actively maintaining cross-platform skills (e.g., VoltAgent's awesome-agent-skills repo listing 1000+ compatible skills), but this community effort requires active maintenance discipline.

*Impact on conclusion:* High. If the Claude Code dialect becomes the dominant authoring target, the research's portability recommendations in Sub-question 4 would need to be reframed as "how to avoid Claude Code lock-in when writing skills" rather than "what works everywhere."

## Findings

### Sub-question 1: Format alignment with the Agent Skills open standard

**F1.1** — The SKILL.md format (`name` + `description` + Markdown body) has been confirmed across all 18 GA platforms. ChatGPT Skills (Platform 10) has no confirmed GA release as of April 2026 and is excluded from HIGH-confidence claims. [HIGH — T1 sources 1–24 converge; LOW for ChatGPT Skills]

**F1.2** — The open standard requires only 2 fields (`name`, `description`). Optional standard fields with broad but non-universal support: `license`, `compatibility`, `metadata`, `allowed-tools` (experimental). All other fields encountered in this research are platform extensions. [HIGH — T1 source 1]

**F1.3** — Claude Code adds 17 proprietary frontmatter fields and behaviors not in the spec (full list in Sub-question 4 extracts). These are silently ignored by other platforms — they do not error. However, any skill behavior that depends on them (subagent forking, dynamic shell injection, path-gated activation) will not function on other platforms. [HIGH — T1 sources 1, 3]

**F1.4** — Semantic Kernel and AutoGen have been unified under Microsoft Agent Framework, which adopted SKILL.md in late 2025. They share a single skill format and documentation surface. [MODERATE — T1 sources 18, 19]

**F1.5** — Kiro (AWS) is a distinct product from Amazon Q Developer. Kiro has documented SKILL.md support with `.kiro/skills/` as its native path. Amazon Q Developer's native SKILL.md support is unclear; its documentation focuses on MCP integration. [MODERATE — T1 sources 22, 23]

---

### Sub-question 2: Capability differences across platforms

**F2.1 — Filesystem access splits into three tiers:**
- **Full access** (CLI/IDE tools): Claude Code CLI, GitHub Copilot (VS Code/CLI/Workspace), OpenAI Codex CLI, Gemini CLI, Cursor, Windsurf, Kiro — full filesystem within workspace and user home. [HIGH — T1 sources 3, 6–8, 10, 12, 13, 17, 22]
- **Sandboxed/VM** (cloud surfaces): Claude API — no external network, no runtime package installation; Claude.ai — variable network access, VM-scoped. ChatGPT Skills container path is not confirmed from T1 sources. [HIGH — T1 sources 4, 5]
- **Directory-scoped** (desktop agent): Claude Cowork — user-designated directories only, Apple Virtualization Framework. [MODERATE — T5 source 26; no T1 Cowork docs available]

**F2.2** — Subagent spawning is a skill-level feature in Claude Code (`context: fork`, `agent:` field). GitHub Copilot Workspace supports agent invocation but the `agents:` frontmatter field was not confirmed in the T1 source (source 8 lists only `name`, `description`, `license`, `allowed-tools`). On all other platforms, multi-agent coordination is a framework concern external to the skill format. [HIGH — T1 source 3; MODERATE for GitHub Copilot Workspace subagent frontmatter — not confirmed in source 8]

**F2.3** — `allowed-tools` semantics diverge critically:
- Claude Code: permission-grant while skill is active; does not restrict other tools [T1 source 3]
- GitHub Copilot: confirmation-bypass; listed tools run without per-use prompts [T1 source 6]
- CrewAI: metadata-only; no enforcement; tools must be registered separately [T1 source 20]
- LangChain: `allowed-tools` field is present in examples but no explicit enforcement mechanism is documented; tools must be pre-registered in the agent framework independently of the SKILL.md field [T1 source 21 — enforcement not explicitly confirmed]
Skills that rely on `allowed-tools` for tool provisioning will fail silently on CrewAI; LangChain behavior is underdocumented but consistent with metadata-only treatment. [HIGH for CrewAI — T1 source 20; MODERATE for LangChain — T1 source 21]

**F2.4** — Gemini CLI requires explicit user consent before a skill's initial activation in a session via a visible `activate_skill` tool call. Once approved, the skill remains active for the duration of the session without re-prompting. This is unique among all platforms — all others activate skills silently when description matches. Any workflow assuming silent automatic activation will behave differently on Gemini CLI for first-use. [HIGH — T1 source 13]

**F2.5** — No platform provides browser automation as a general skill capability. CLI tools are terminal-only. IDE tools have preview panes only. `webbrowser.open()` works for Claude Code CLI scripts in local environments but not in sandboxed/cloud surfaces. [HIGH — T1 sources 3, 12, 13, 17]

---

### Sub-question 3: Output placement constraints

**F3.1** — The canonical eval workspace layout from the agentskills.io spec: `<skill>-workspace/iteration-N/eval-<name>/{with_skill,without_skill}/outputs/` with `timing.json`, `grading.json`, and `benchmark.json`. This is documented but not enforced by any platform runtime. [HIGH — T1 source 25]

**F3.2** — Hard-coding absolute paths is an anti-pattern across all platforms. All platforms encountering absolute paths will fail on machines with different user directories. Use relative paths or well-known variables: `$HOME`, `$PROJECT_ROOT`, `${CLAUDE_SKILL_DIR}` (Claude Code only). [HIGH — T1 sources 3, 17, 21, 22]

**F3.3** — Platform-specific constraints on output placement:
- **Claude API/claude.ai**: No runtime package installation; VM-scoped writes only; no external network. Eval workspaces must stay within the VM's writable scope. [HIGH — T1 source 4]
- **Claude Cowork**: Writes only to user-designated directories. Eval workspaces must be placed there explicitly. [MODERATE — T5 source 26]
- **LangChain Deep Agents**: 10 MB hard limit on SKILL.md; forward-slash paths relative to backend root required. Large eval workspace outputs should not be co-located with SKILL.md. [HIGH — T1 source 21]
- **CLI/IDE platforms**: No platform-enforced path constraints. Follow workspace-relative conventions. [HIGH — T1 sources 3, 6, 10, 12, 17]

**F3.4** — Custom Skills do not sync across Claude surfaces. A skill uploaded to Claude.ai is not available via the Claude API or Claude Code — these are separate inventories requiring separate deployment. [HIGH — T1 source 4]

---

### Sub-question 4: Minimum common denominator vs. Claude Code-specific

**F4.1 — Minimum common denominator (confirmed works everywhere):**
- `SKILL.md` with `name` (≤64 chars, lowercase alphanumeric + hyphens, matches directory name) and `description` (≤1024 chars)
- Directory layout: `skill-name/SKILL.md` with optional `scripts/`, `references/`, `assets/`
- Progressive disclosure: metadata (~100 tokens at startup), full body on activation (≤500 lines / 5000 tokens recommended), resources on demand
- Markdown body with no format restrictions
[HIGH — T1 sources 1, 3, 6, 10, 12, 13, 17, 18, 20, 21, 22]

**F4.2 — Discovery path problem**: No single path is discovered by all platforms. To maximize coverage, skills should exist in both `.claude/skills/<name>/` (Claude Code) and `.agents/skills/<name>/` (Codex, Cursor, Windsurf, Kiro, GitHub Copilot, Gemini). The claim from source 28 (apiyi.com) that `.agents/skills/` uses `SKILL.yaml` format is contradicted by T1 sources and should be disregarded. [HIGH — T1 sources 3, 6, 10, 12, 13, 17, 22]

**F4.3 — Claude Code-specific features not in the open standard** (17 items; silently ignored by other platforms):
`context: fork`, `agent:`, `model:`, `effort:`, `hooks:`, `paths:`, `shell:`, `user-invocable:`, `disable-model-invocation:`, `argument-hint:`, dynamic shell injection (`` !`cmd` ``), `$ARGUMENTS`, `$N`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_SKILL_DIR}`, plugin namespacing (`plugin:skill`), worktree isolation. [HIGH — T1 source 3]

**F4.4 — Cross-platform portability is syntactic, not behavioral.** Skills can be structured to pass validation on all platforms, but execution behavior diverges materially. Subagent spawning, dynamic context injection, path-gated activation, and shell injection are Claude Code-only capabilities with no equivalents in the standard. A skill that uses `context: fork` and `!`date`` will parse on Cursor but do nothing there. The ACH analysis identified this as the best-supported hypothesis (1 inconsistency vs. 6 for the optimistic "universal portability" framing). [HIGH — T1 sources 1, 3, 13; supported by challenge analysis]

---

### Gaps and follow-ups

- No T1 documentation exists for Claude Cowork developer internals. The sandbox directory structure and virtualization behavior rely on a single T5 source.
- ChatGPT Skills / Hazelnut has no confirmed GA release. Treat Platform 10 as 18 confirmed + 1 pending.
- Gemini Code Assist (Platform 12) lacks a standalone skills reference. Coverage overlaps with Gemini CLI and Android Studio.
- The `openagentskills.dev` alternative spec signal warrants monitoring for ecosystem fragmentation.
- Supply-chain security (36.82% vulnerability rate in published skills per Snyk ToxicSkills study) is a material gap not addressed by the format research.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| C1 | SKILL.md format (name + description + Markdown body) confirmed across all 18 GA platforms | Attribution/Count | T1 sources 1–24 | verified |
| C2 | ChatGPT Skills (Platform 10) has no confirmed GA release as of April 2026 | Attribution | T4/T5 only | human-review |
| C3 | The open standard requires only 2 fields: `name` and `description` | Spec fact | Source 1 | verified |
| C4 | Claude Code adds 17 proprietary frontmatter fields/behaviors not in the open standard | Statistic | Source 3 | verified |
| C5 | Semantic Kernel and AutoGen unified under Microsoft Agent Framework, which adopted SKILL.md in late 2025 | Attribution | Sources 18, 19 | verified |
| C6 | Kiro is distinct from Amazon Q Developer; Kiro native path is `.kiro/skills/` | Attribution | Sources 22, 23 | verified |
| C7 | Claude Code: "Full network access: Skills have the same network access as any other program on the user's computer." | Quote | Source 4 | verified |
| C8 | Claude API: "No network access: Skills cannot make external API calls or access the internet. No runtime package installation: Only pre-installed packages are available." | Quote | Source 4 | verified |
| C9 | Claude.ai: "Varying network access: Depending on user/admin settings, Skills may have full, partial, or no network access." | Quote | Source 4 | verified |
| C10 | ChatGPT skills have code interpreter container access at `/home/oai/skills` | Attribution | Unverified T5 | removed |
| C11 | Claude Cowork uses Apple's Virtualization Framework and user-designated directories | Attribution | Source 26 (T5 sole) | human-review |
| C12 | Subagent spawning: Claude Code uses `context: fork` / `agent:` field; GitHub Copilot Workspace `agents:` frontmatter field | Spec fact | Sources 3, 8 | corrected |
| C13 | CrewAI `allowed-tools`: "experimental metadata only — it does not provision or inject any tools" | Quote | Source 20 | verified |
| C14 | LangChain: `allowed-tools` read but tools must be pre-registered independently in the framework | Attribution | Source 21 | human-review |
| C15 | Gemini CLI requires explicit user consent before each skill activation via a visible `activate_skill` tool call | Attribution | Source 13 | corrected |
| C16 | All other platforms (besides Gemini CLI) activate skills silently/automatically when description matches | Superlative | Multiple T1 | human-review |
| C17 | Canonical eval workspace: `<skill>-workspace/iteration-N/eval-<name>/{with_skill,without_skill}/outputs/` with `timing.json`, `grading.json`, `benchmark.json` | Spec fact | Source 25 | verified |
| C18 | Claude API VM: no runtime package installation; VM-scoped writes; no external network | Attribution | Source 4 | verified |
| C19 | LangChain Deep Agents: 10 MB hard limit on SKILL.md; forward-slash paths relative to backend root | Spec fact | Source 21 | verified |
| C20 | "Custom Skills do not sync across surfaces. Skills uploaded to one surface are not automatically available on others." | Quote | Source 4 | verified |
| C21 | `name` ≤64 chars, `description` ≤1024 chars; ≤500 lines / 5000 tokens body recommended | Spec fact | Source 1 | verified |
| C22 | No single discovery path works for all platforms; `.claude/skills/` for Claude Code; `.agents/skills/` for Codex, Cursor, Windsurf, Kiro, GitHub Copilot, Gemini | Attribution | Sources 3, 6, 10, 12, 13, 17, 22 | verified |
| C23 | Claude Code-specific features: 17 items including `context: fork`, `model:`, `effort:`, `hooks:`, `paths:`, `shell:`, dynamic shell injection, worktree isolation, plugin namespacing | Statistic | Source 3 | verified |
| C24 | A skill using `context: fork` parses on Cursor but does nothing there (unsupported fields silently ignored) | Attribution | Sources 1, 3, 13 | verified |

**Notes on corrected/removed/human-review entries:**
- **C10 (removed)**: The ChatGPT code interpreter path `/home/oai/skills` appeared only in unverified T5 search results and is not corroborated by any T1 source. Removed from F2.1. (Original: "ChatGPT — code interpreter container at `/home/oai/skills` only.")
- **C12 (corrected)**: Source 8 (GitHub Docs — create-skills) lists only `name`, `description`, `license`, `allowed-tools` as supported frontmatter. No `agents:` field was found. F2.2 updated to flag this as unconfirmed. (Original: "GitHub Copilot Workspace (`agents:` field)".)
- **C15 (corrected)**: Source 13 (Gemini CLI docs) states "A skill remains active...for the duration of the session" after initial consent — consent is per-session initial activation, not before each invocation. F2.4 updated accordingly. (Original: "before each skill activation".)
- **C2 (human-review)**: No T1 source confirms or denies GA status; all ChatGPT Skills information is T4/T5 only.
- **C11 (human-review)**: Sole T5 source (source 26); no T1 Cowork documentation available for cross-check.
- **C14 (human-review)**: LangChain source 21 shows `allowed-tools` in frontmatter examples but provides no explicit statement about `@tool` registration being required; framework architecture implies it but is not confirmed verbatim.
- **C16 (human-review)**: "All other platforms" is a superlative that could not be individually verified for every platform; directionally supported by the evidence but inherently risky as a blanket claim.

## Key Takeaways

1. **Format portability is real; behavioral portability is not.** All 18 confirmed platforms parse SKILL.md. Only Claude Code supports subagent forking, dynamic shell injection, and path-gated activation from within the skill format.

2. **Use both discovery paths for cross-platform skills.** `.claude/skills/` for Claude Code; `.agents/skills/` for everything else. There is no single path that works everywhere.

3. **`allowed-tools` cannot be trusted for tool provisioning.** CrewAI ignores it entirely; LangChain requires separate Python registration. Use it only for permission grants on platforms where it is enforced.

4. **Claude Cowork and the Claude API are the most constrained environments.** Eval workspaces, result files, and any writes must stay within designated directories or VM scope. Absolute paths and network calls will fail.

5. **Gemini CLI requires a UX accommodation.** Skills do not activate silently — users see a consent prompt per session. Skill descriptions must be clear enough to justify activation to a user who may not know what the skill is.

6. **Never hard-code absolute paths.** Use relative paths, `$HOME`, `$PROJECT_ROOT`, or `${CLAUDE_SKILL_DIR}` (Claude Code only). This is documented by Windsurf, Kiro, and LangChain as an explicit anti-pattern.

7. **ChatGPT Skills (Platform 10) is unconfirmed GA.** Exclude from deployment planning until official documentation is available.

## Limitations

- No T1 documentation for Claude Cowork developer internals. Cowork sandbox details (virtualization, directory paths) rely on a single T5 source.
- Gemini Code Assist (Platform 12) lacks a standalone skills reference; coverage inferred from Gemini CLI and Android Studio docs.
- The `openagentskills.dev` alternative spec signal was identified in the Challenge phase but not further investigated.
- Supply-chain security (36.82% vulnerability rate, Snyk ToxicSkills study) is not addressed by format research but is a material deployment risk.

## Search Protocol

| Query | Engine | Date Range | Results | Used |
|-------|--------|------------|---------|------|
| Agent Skills open standard SKILL.md format specification | web | 2025–2026 | 10 | 3 |
| Claude Code CLI skills .claude/skills SKILL.md format documentation | web | 2025 | 10 | 2 |
| GitHub Copilot agent skills VS Code custom instructions format | web | 2025–2026 | 10 | 3 |
| OpenAI Codex CLI agent skills SKILL.md format | web | 2025 | 10 | 2 |
| Cursor AI agent skills SKILL.md custom instructions format | web | 2025–2026 | 10 | 2 |
| Gemini CLI agent skills format custom instructions | web | 2025–2026 | 10 | 3 |
| Windsurf Codeium agent skills SKILL.md format capabilities | web | 2025–2026 | 10 | 2 |
| ChatGPT custom GPTs skills format capabilities tools | web | 2025–2026 | 10 | 2 |
| Amazon Q Developer agent skills SKILL.md format capabilities | web | 2025–2026 | 10 | 2 |
| LangChain LangGraph agent skills format custom tools capabilities | web | 2025–2026 | 10 | 2 |
| AutoGen Microsoft agent skills SKILL.md format capabilities | web | 2025–2026 | 10 | 2 |
| CrewAI SKILL.md agent skills directory format integration | web | 2025 | 10 | 2 |
| Semantic Kernel agent skills SKILL.md format capabilities | web | 2025–2026 | 10 | 2 |
| Gemini Code Assist agent skills SKILL.md format VS Code JetBrains | web | 2025–2026 | 10 | 2 |
| GitHub Copilot Workspace agent skills format capabilities subagent | web | 2025–2026 | 10 | 2 |
| OpenCode agent skills SKILL.md format capabilities platform | web | 2025–2026 | 10 | 1 |
| Amazon Q Developer Kiro agent skills SKILL.md format skill locations | web | 2025–2026 | 10 | 2 |
| agent skills output files placement constraints eval workspace | web | 2025–2026 | 10 | 2 |
| minimum common denominator agent skills cross-platform portability | web | 2025–2026 | 10 | 2 |
| agent skills cross-platform Claude Code specific features subagent | web | 2025–2026 | 10 | 3 |
| agent skills platform capability matrix filesystem subagent browser | web | 2025–2026 | 10 | 2 |
| Cowork AI agent skills platform capabilities format tools | web | 2025–2026 | 10 | 2 |
| claude.ai standard web skills format upload custom skills constraints | web | 2025–2026 | 10 | 2 |
| GitHub Copilot CLI agent skills SKILL.md format capabilities | web | 2025 | 10 | 2 |
| agent skills Claude Code specific vs universal standard context fork | web | n/a | 10 | 2 |

*25 searches · 35 sources identified · 9 sources fetched in verification*

<!-- search-protocol [
  {"query": "Agent Skills open standard SKILL.md format specification 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Claude Code CLI skills .claude/skills SKILL.md format documentation 2025", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "GitHub Copilot agent skills VS Code custom instructions format 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "OpenAI Codex CLI agent skills SKILL.md format 2025", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Cursor AI agent skills SKILL.md custom instructions .cursorrules format 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Gemini CLI agent skills format custom instructions 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Windsurf Codeium agent skills SKILL.md format capabilities filesystem 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "ChatGPT custom GPTs skills format capabilities tools 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Amazon Q Developer agent skills SKILL.md format capabilities 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "LangChain LangGraph agent skills format custom tools capabilities 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "AutoGen Microsoft agent skills SKILL.md format capabilities tools filesystem 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "CrewAI SKILL.md agent skills directory format integration 2025", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Semantic Kernel agent skills SKILL.md format capabilities 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Gemini Code Assist agent skills SKILL.md format capabilities VS Code JetBrains 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "GitHub Copilot Workspace agent skills format capabilities tools subagent 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "OpenCode agent skills SKILL.md format capabilities platform 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Amazon Q Developer Kiro agent skills SKILL.md format skill locations filesystem 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "agent skills output files placement location constraints eval workspace result files platform 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "minimum common denominator agent skills cross-platform portability SKILL.md limitations 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "agent skills cross-platform what works everywhere claude code specific features subagent spawning browser display 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "agent skills platform capability matrix filesystem subagent browser tool differences platforms 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "Cowork AI agent skills platform capabilities format tools 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "claude.ai standard web skills format upload custom skills capabilities constraints 2025 2026", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "GitHub Copilot CLI agent skills SKILL.md format capabilities filesystem tools 2025", "engine": "web", "timestamp": "2026-04-12", "results_count": 10},
  {"query": "agent skills what is claude code specific vs universal standard context fork subagent allowed-tools platform differences", "engine": "web", "timestamp": "2026-04-12", "results_count": 10}
] -->
