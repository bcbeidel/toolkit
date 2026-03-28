---
name: "AGENTS.md as Cross-Tool Standard"
description: "How AGENTS.md emerged as the universal instruction file for AI coding tools — adoption trajectory, Linux Foundation governance, and practical layering with tool-specific files"
metadata:
  type: reference
  sources:
    - https://agents.md/
    - https://developers.openai.com/codex/guides/agents-md/
    - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
    - https://www.agentrulegen.com/guides/cursorrules-vs-claude-md
  related:
    - docs/research/ai-coding-assistant-conventions.md
    - docs/context/instruction-file-conventions.md
    - docs/context/convention-driven-design.md
    - docs/context/information-architecture.md
---

AGENTS.md is the closest thing to a universal instruction file for AI coding tools. Released by OpenAI as part of Codex CLI in August 2025, it reached 60,000+ open source projects by December 2025 and is now supported by Codex, Cursor, Copilot, Claude Code, Gemini CLI, Devin, Jules (Google), Factory, Amp, and VS Code.

## Design Properties

AGENTS.md succeeds through simplicity:

- **Plain markdown.** No required metadata schema, no proprietary format. Any tool that reads markdown can consume it.
- **Hierarchical.** Subdirectory `AGENTS.md` files override root-level ones. This mirrors the universal precedence pattern across all tools.
- **Version-controlled.** Lives in the repo alongside code. Instructions evolve with the codebase.
- **Cross-tool by default.** A single file serves all tools that support it, eliminating the need to maintain parallel instruction files.

The format deliberately avoids features that would tie it to a specific tool. No `@path` imports (Claude Code), no glob-based auto-attachment (Cursor), no rule-type metadata (Windsurf). This is a feature, not a limitation — it ensures portability.

## Governance and Standardization

In December 2025, OpenAI donated AGENTS.md to the Agentic AI Foundation (AAIF) under the Linux Foundation, alongside MCP and Goose. Platinum members include AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI. This governance structure signals that AGENTS.md is intended as an industry standard, not a vendor-controlled format.

The Linux Foundation stewardship reduces the risk that any single vendor can unilaterally change the specification. It also provides a neutral forum for evolution as tool capabilities expand.

## Practical Layering Strategy

The emerging practitioner consensus: put shared conventions in AGENTS.md, use tool-specific files only for features that AGENTS.md cannot express.

**What belongs in AGENTS.md:**
- Build and test commands
- Coding conventions and style guidelines
- Architecture overview and navigation hints
- Behavioral directives (verbosity, directness, etc.)

**What stays in tool-specific files:**
- Claude Code's `@path` imports and `CLAUDE.md` composition
- Cursor's glob-scoped auto-attachment rules
- Copilot's `applyTo` path-specific instructions
- Windsurf's rule-type metadata

This layering means teams maintain one shared instruction file plus thin tool-specific overlays. The shared file covers 90%+ of content; tool-specific files handle the remaining 10% of proprietary features.

## Adoption Caveats

The 60,000-project adoption figure comes from AAIF announcements and has not been independently verified. Many adopted files may be trivial or auto-generated. The quality and maintenance level of these files varies widely.

There is also a risk that tool vendors may resist ceding control to an open standard if it limits their ability to differentiate. The current broad adoption may reflect the standard's simplicity rather than deep commitment from vendors.

## Relevance to WOS

WOS already generates and manages AGENTS.md sections using marker-based insertion (`<!-- wos:begin -->` / `<!-- wos:end -->`). The cross-tool standard validates WOS's approach of treating AGENTS.md as a managed artifact. As the standard evolves under AAIF governance, WOS can adapt its AGENTS.md generation to track specification changes while maintaining backward compatibility.
