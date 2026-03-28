---
name: "Instruction File Conventions Across AI Coding Tools"
description: "How all major AI coding assistants converged on markdown-in-repo instruction files with hierarchical precedence, while diverging on file naming, metadata schemas, and loading semantics"
metadata:
  type: reference
  sources:
    - https://claude.com/blog/using-claude-md-files
    - https://docs.cursor.com/context/rules
    - https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
    - https://docs.windsurf.com/windsurf/cascade/memories
    - https://developers.openai.com/codex/guides/agents-md/
    - https://docs.cline.bot/prompting/cline-memory-bank
    - https://aider.chat/docs/usage/conventions.html
    - https://agents.md/
  related:
    - docs/research/ai-coding-assistant-conventions.md
    - docs/context/agents-md-standard.md
    - docs/context/convention-driven-design.md
    - docs/context/context-engineering.md
    - docs/context/writing-for-llm-consumption.md
---

Every major AI coding assistant uses markdown files committed to the repository to provide project-specific instructions. This is the most significant convergence in the ecosystem: the pattern is settled, even though naming, location, and metadata differ across tools.

## The Universal Pattern

All seven major tools — Claude Code, GitHub Copilot, Cursor, Windsurf, Codex CLI, Cline, and Aider — implement the same core concept: a markdown document in the repository that tells the AI how the codebase works. The content across formats is 90%+ identical. Teams typically write build commands, coding conventions, architecture notes, and behavioral directives.

The instruction files share three properties:

1. **Version-controlled.** Files live in the repo alongside code, so instructions evolve with the codebase.
2. **Markdown-formatted.** Plain text with optional structure. No proprietary formats required.
3. **Automatically loaded.** Tools discover and inject these files without explicit user action.

## File Names and Locations

| Tool | Primary File | Location |
|------|-------------|----------|
| Claude Code | `CLAUDE.md` | Project root |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/` dir |
| Cursor | `.cursor/rules/*.md` | `.cursor/rules/` dir |
| Windsurf | `.windsurf/rules/*.md` | `.windsurf/rules/` dir |
| Codex CLI | `AGENTS.md` | Project root + subdirs |
| Cline | `.clinerules` | Project root |
| Aider | `CONVENTIONS.md` | Project root |

Cursor and Windsurf have both migrated from single root files (`.cursorrules`, `.windsurfrules`) to directory-based rule systems, mirroring a broader trend toward modular, per-concern instruction files. Copilot followed the same trajectory, adding path-specific `.instructions.md` files with YAML frontmatter in July 2025.

## Hierarchical Precedence

Every tool implements layered instructions where specificity increases with proximity to the working file. More specific instructions override more general ones.

Claude Code layers five levels: enterprise policies, personal `~/.claude/CLAUDE.md`, project root, subdirectory files, and user prompt. Codex concatenates `AGENTS.md` files from root down through subdirectories, with a 32 KiB combined limit. Cursor uses four rule types (Always, Auto-Attached, Agent-Requested, Manual) with different loading triggers.

The consistent principle: root-level files set project-wide conventions; directory-level files add or override for specific areas.

## Metadata Divergence

Where tools diverge most is in metadata schemas. Cursor rules use MDC format with YAML frontmatter (`description`, `globs`, `alwaysApply`). Copilot's path-specific instructions use `applyTo` glob patterns. Claude Code supports `@path` imports for composing instructions from multiple files. Codex and Aider use plain markdown with no required metadata.

This metadata divergence is why a single instruction file cannot fully serve all tools. The practical recommendation: put shared conventions in AGENTS.md (which most tools now read), and use tool-specific files only for features AGENTS.md cannot express.

## Implications for WOS

WOS generates both `CLAUDE.md` and `AGENTS.md`. The instruction file convergence validates the approach of maintaining structured context in markdown files with frontmatter metadata. The hierarchical precedence pattern aligns with WOS's directory-level `_index.md` files. The trend toward modular, per-concern instruction files supports the one-concept-per-file convention.
