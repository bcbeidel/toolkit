---
name: "Instruction File Fragmentation and Convergence"
description: "The AI coding tool instruction file ecosystem is fragmented across incompatible filenames, but converging toward AGENTS.md as the cross-platform baseline under AAIF/Linux Foundation governance"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://agents.md/
  - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
  - https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/
  - https://arxiv.org/html/2601.18341v1
related:
  - docs/context/instruction-file-hierarchy-and-path-scoping.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/format-sensitivity-and-cross-model-defaults.context.md
---
Every major AI coding tool uses a different primary instruction filename. As of 2026: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex, cross-platform target), `.github/copilot-instructions.md` (GitHub Copilot), `.cursor/rules/*.mdc` (Cursor), `.windsurf/rules/*.md` (Windsurf), `.clinerules/` (Cline), `CONVENTIONS.md` (Aider), `GEMINI.md` (Gemini CLI). All evolved from single files to directory-based structures between 2024 and 2026.

The fragmentation creates a practical problem: teams using multiple tools must maintain duplicate instructions. AGENTS.md emerged as the convergence point — plain Markdown with no required fields, no frontmatter schema. Its simplicity is both its strength (zero migration cost) and weakness (no validation, no schema enforcement, quality depends entirely on the author).

**AAIF governance (December 9, 2025).** The Linux Foundation announced the Agentic AI Foundation (AAIF) with three founding projects: Anthropic's Model Context Protocol (MCP), Block's goose, and OpenAI's AGENTS.md. Platinum members: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. This moved AGENTS.md from a vendor-controlled convention to neutral foundation governance — the same structural move the Language Server Protocol made under Eclipse Foundation.

**Adoption is real but early.** 60,000+ open-source GitHub repositories have adopted AGENTS.md; 25+ tools list support for it. However, an academic study (arxiv 2601.18341, January 2026) measured only 7.89% of 129,134 studied GitHub projects with any visible agent configuration file. "Cross-platform standard" describes governance aspiration more than current deployment reality.

**The practical coexistence pattern** for teams running multiple tools: maintain one AGENTS.md for the cross-platform baseline and have `CLAUDE.md` start with `@AGENTS.md`, adding Claude-specific extensions below. Gemini CLI can be configured via `settings.json` to read `AGENTS.md` natively alongside `GEMINI.md`. This avoids duplicating shared conventions.

**What AGENTS.md is not:** a technical specification with enforced semantics. It is a free-form Markdown convention. No linting, no required sections, no schema validation. The 2026 review identified four weaknesses: no validation schema, quality dependence on human authorship (auto-generated files degrade performance), token cost from large files, and unsettled best practices. These are not bugs in the governance process — they reflect a deliberate choice to minimize friction to adoption.

The fragmentation problem is not fully solved. Cursor's `.mdc` format, Windsurf's directory system, and Claude Code's `CLAUDE.md` are all actively maintained separately. AGENTS.md is the best available cross-platform baseline today — not because every tool has adopted it as primary, but because most tools will read it alongside their native format.
