---
name: "Subagent Cross-Platform Format Comparison"
description: "How Claude Code's .claude/agents/*.md format compares to Cursor, GitHub Copilot, Codex CLI, Windsurf, and LangChain Deep Agents — structural similarities, key differences, and portability implications"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot
  - https://developers.openai.com/codex/subagents
  - https://cursor.com/docs/subagents
  - https://docs.windsurf.com/windsurf/cascade/agents-md
  - https://docs.langchain.com/oss/python/deepagents/subagents
related:
  - docs/research/2026-04-13-claude-code-subagent-mechanics-cross-platform.research.md
  - docs/context/claude-code-subagent-definition-format.context.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
  - docs/context/claude-code-subagent-permission-and-security-model.context.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
---

# Subagent Cross-Platform Format Comparison

Claude Code's Markdown+YAML subagent format is directly readable by Cursor. GitHub Copilot uses the same structural pattern with a different storage location. Codex requires format conversion. Windsurf is a different primitive entirely.

## Cursor — Closest Analog

Cursor uses the same Markdown + YAML frontmatter format. Critically, Cursor explicitly reads `.claude/agents/` (labeled "Claude compatibility") and `.codex/agents/` (labeled "Codex compatibility") in addition to its native `.cursor/agents/`. Agent files authored for Claude Code are directly usable in Cursor with no modification.

Key differences:
- `readonly` boolean instead of Claude Code's granular `tools`/`disallowedTools`
- `fast` model alias instead of `haiku`
- No equivalents for `hooks`, `mcpServers`, `memory`, `effort`, `isolation`, `initialPrompt`
- No fields are required (name defaults to filename)

Context isolation works the same way: subagents start with a clean context; parent passes relevant information in the prompt.

## GitHub Copilot — Same Structure, Cloud Execution

GitHub Copilot custom agents use Markdown files with YAML frontmatter in `.github/agents/AGENT-NAME.md` (repo level) or `/agents/AGENT-NAME.md` in a `.github-private` repo (org/enterprise level). The Markdown body contains agent instructions (up to 30,000 characters) — same structure as Claude Code. Only `description` is required.

Confirmed frontmatter fields: `name`, `description`, `tools`, `model`, `target`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, `metadata`. No `prompt` frontmatter key — instructions go in the body.

Key architectural differences:
- Runs in an ephemeral GitHub Actions environment, not the developer's local machine
- Scoped to one repository per run (no multi-directory access)
- Task assignment through GitHub interfaces (Issues, PRs, Agents panel) — not terminal-first
- No equivalents for `permissionMode`, `hooks`, `memory`, `isolation`, `background`, `effort`, `color`

## Codex CLI — TOML Format, Explicit-Only Invocation

Codex uses TOML files (not Markdown) in `.codex/agents/`. Required fields: `name`, `description`, `developer_instructions` (the behavioral spec, equivalent to the Markdown body in Claude Code).

Optional fields inherit from parent when omitted: `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`, `nickname_candidates`.

Key differences:
- No automatic delegation — explicit invocation only (design choice, not limitation)
- Global `max_depth` (default 1) and `max_threads` (default 6) caps as config settings
- `sandbox_mode` as the tool restriction mechanism (vs. per-tool lists)
- Batch workflows via `spawn_agents_on_csv` (maps CSV rows to workers)

## Windsurf — Different Primitive Entirely

Windsurf's `AGENTS.md` is a rules/instructions file, not a subagent definition format. It is part of the Rules engine — its content is included in Cascade's system prompt on every message. Root-level `AGENTS.md` is always-on; subdirectory `AGENTS.md` files apply as glob rules.

Comparing Windsurf AGENTS.md to Claude Code subagents is a category error. The `#runSubagent` tool is experimental. Workflow agents in `.windsurf/workflows/` are a separate, distinct concept.

## LangChain Deep Agents — Different Category, Important Contrast

LangChain Deep Agents is a Python framework (not a coding assistant), but it is the dominant multi-agent runtime and has a fundamentally different design that highlights what Claude Code's isolation model is optimizing against.

**Context model: propagation, not isolation.** Runtime context flows automatically from parent to all subagents in LangChain — tools, model, skills, and invocation context are passed down by default. This is the opposite of Claude Code. Claude Code's complete isolation means every subagent starts clean; LangChain's propagation means subagents share the parent's ambient state unless explicitly scoped.

**Two definition types:**
- `SubAgent` (dict-based) — equivalent to Claude Code's `.md` file: `name`, `description`, `system_prompt`, `tools`, and optional `model`, `middleware`, `interrupt_on`, `skills`, `permissions`.
- `CompiledSubAgent` — wraps a prebuilt LangGraph compiled graph, requiring only `name`, `description`, and a `runnable`. Closest analog would be a skill-chained agent in Claude Code.

**Default general-purpose subagent.** All Deep Agents automatically have a fallback agent that inherits the main agent's system prompt, tools, model, and skills. Override by defining an agent with `name="general-purpose"`. Claude Code has no equivalent — there is no ambient fallback.

**`interrupt_on` for HITL.** Subagent definitions can declare interrupt conditions to pause for human review before completing. Claude Code has no declarative equivalent at the definition level — HITL requires prompting design in the body.

**Skill inheritance contrast.** In LangChain, the general-purpose agent inherits parent skills automatically; custom subagents do not (must list via `skills`). In Claude Code, *no* subagents inherit parent skills — all skills must be listed explicitly in `skills` frontmatter or they are absent.

**Shared principle: concise results.** LangChain's official guidance states subagent system prompts should include explicit output length limits (e.g., "keep your response under 500 words") and instruct the subagent to exclude raw data, intermediate calculations, and detailed outputs. This directly matches Claude Code's context consumption warning — but LangChain's docs give a concrete word-count target that Claude Code docs omit.

## Portability Summary

| Feature | Claude Code | Cursor | GitHub Copilot | Codex CLI | Windsurf | LangChain |
|---|---|---|---|---|---|---|
| Format | Markdown+YAML | Markdown+YAML | Markdown+YAML | TOML | Plain Markdown (rules) | Python dict / LangGraph |
| Required fields | name, description | none | description | name, description, developer_instructions | none | name, description, system_prompt/runnable |
| Reads `.claude/agents/` | yes | yes (explicit) | no | no | no | no |
| Auto-delegation | yes (unreliable) | yes | via GitHub UI | no (explicit only) | experimental | yes (`task()` tool) |
| Context model | isolation | isolation | isolation | isolation | n/a (rules file) | propagation |
| Nesting | blocked | not specified | n/a (cloud) | max_depth=1 | n/a | supported |
| Default fallback agent | no | no | no | no | n/a | yes (general-purpose) |
| HITL at definition level | no | no | no | no | no | yes (`interrupt_on`) |

## Takeaway

Portability floor: Claude Code files (Markdown+YAML, `name`+`description` required) are directly readable by Cursor. Copilot uses the same structural pattern with different storage and cloud execution. Codex requires format conversion (TOML). Windsurf is not in the same category. LangChain is a different kind of tool entirely — its propagation-by-default model is the architectural inverse of Claude Code's isolation-by-default, and that contrast explains why both Claude Code and LangChain recommend keeping subagent outputs concise: the problem is context accumulation regardless of how context flows.
