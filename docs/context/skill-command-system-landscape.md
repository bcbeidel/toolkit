---
name: "Skill and Command System Landscape"
description: "How AI coding tools diverge most sharply in their extensibility models — Claude Code skills, Codex skills, Cursor rules, Copilot agents, and Cline's MCP-first approach reflect fundamentally different interaction philosophies"
metadata:
  type: reference
  sources:
    - https://code.claude.com/docs/en/skills
    - https://developers.openai.com/codex/skills/
    - https://docs.cursor.com/context/rules
    - https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
    - https://docs.cline.bot/prompting/cline-memory-bank
  related:
    - docs/research/ai-coding-assistant-conventions.md
    - docs/context/plugin-extension-architecture.md
    - docs/context/mcp-extensibility-standard.md
    - docs/context/instruction-file-conventions.md
---

Skill and command systems are the most divergent area across AI coding tools. Unlike instruction files (converged on markdown) and extensibility protocols (converged on MCP), the approaches to user-defined workflows and commands reflect genuinely different interaction models. No convergence is expected because the differences are architectural, not accidental.

## The Six Models

### Claude Code: Skills + Commands + Hooks

Claude Code has the richest extensibility surface. **Skills** are `SKILL.md` files with YAML frontmatter, auto-discovered and loaded by context match. They provide persistent instructions, not one-shot actions. **Commands** are markdown files in `.claude/commands/` that become `/slash-commands` for explicit user invocation. **Hooks** are event-driven scripts triggered by lifecycle events (pre-tool-use, post-tool-use). **Subagents** handle parallel subtask processing — up to 10 concurrent instances, each with 200K token context.

This model treats the AI as a skilled practitioner that carries knowledge (skills) and follows procedures (commands) while responding to events (hooks).

### Codex CLI: Directory-Based Skills

Codex skills are directories with `SKILL.md` plus optional scripts and references, stored in `~/.codex/skills/`. Two invocation modes: explicit (user invokes via `/skills` or `$` mention) and implicit (agent auto-selects based on task-description match). Skills can declare MCP server dependencies. Currently gated behind `--enable skills` feature flag.

This model is closest to Claude Code's but more file-system-centric and less mature.

### Cursor: Rules as Implicit Skills

Cursor has no separate skill concept — `.cursor/rules/` files are the primary customization mechanism. Agent-requested rules function like implicit skills: the agent reads the description and decides whether to load them. CLI commands (`/rules`, `/models`, `/mcp`) handle management tasks.

This model collapses skills into the instruction layer, using rule metadata (globs, descriptions) to provide context-sensitive behavior.

### GitHub Copilot: Agents + Extensions

Copilot's extensibility is through configurable agents, extensions that bundle MCP servers and skills, and a coding agent that handles multi-file editing with self-healing. The Copilot CLI (GA February 2026) ships with GitHub's MCP server built in. Extensions are the highest-level abstraction — they can package agents, skills, hooks, and MCP servers together.

This model favors platform-level integration over user-defined customization.

### Windsurf: Rules + Auto-Generated Memories

Windsurf has no explicit skill system. Rules files define workflow patterns, and Cascade automatically generates Memories from observed development patterns. Extensibility is primarily through MCP and rules.

This model relies on the tool learning from behavior rather than being explicitly taught.

### Cline: MCP-First Extensibility

Cline has no built-in skill system. When a user asks Cline to "add a tool," it creates an MCP server automatically. All extensibility flows through MCP. `.clinerules` provides static instructions but no dynamic invocation.

This model bets on MCP as the universal answer to extensibility, avoiding a proprietary skill layer.

## Why Convergence Is Unlikely

The fragmentation reflects three distinct philosophies about how users should customize AI behavior:

1. **Persistent knowledge** (Claude Code, Codex): Skills are knowledge the AI carries. They define how to approach categories of tasks.
2. **Contextual rules** (Cursor, Windsurf): Rules are conditional instructions loaded based on what files or patterns are active.
3. **Protocol-mediated tools** (Cline, Copilot): External capabilities are exposed through standardized protocols, not custom skill formats.

These philosophies serve different interaction models. Persistent skills work best for deep, long-running tasks. Contextual rules work best for IDE-embedded editing. Protocol-mediated tools work best for integrating external services.

## Practical Implication

Teams building cross-tool workflows should invest in AGENTS.md (for shared instructions) and MCP (for shared tools) rather than tool-specific skill systems. Skill-layer customization should be treated as tool-specific optimization, not as the primary extensibility strategy.
