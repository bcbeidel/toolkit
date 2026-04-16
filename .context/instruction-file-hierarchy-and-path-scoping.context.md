---
name: "Instruction File Hierarchy and Path Scoping"
description: "All major AI coding tools load instruction files broad-to-specific via concatenation; path-scoping metadata exists in three tools but uses incompatible field names"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://code.claude.com/docs/en/memory
  - https://developers.openai.com/codex/guides/agents-md
  - https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
  - https://www.agentrulegen.com/guides/cursor-rules-guide
  - https://docs.cline.bot/features/cline-rules
  - https://geminicli.com/docs/cli/gemini-md/
related:
  - docs/context/instruction-file-fragmentation-and-convergence.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
---
Every major AI coding tool concatenates instruction files from broad scope to specific scope. Global/user instructions load first, then project root, then subdirectory instructions closest to the work. More specific files appear later in the context window, giving them higher effective priority. This pattern holds universally — though the mechanisms differ significantly across tools.

**Claude Code** implements a 5-tier hierarchy: managed policy (cannot be excluded) → user global (`~/.claude/CLAUDE.md`) → project root → local gitignored override (`CLAUDE.md.local`) → subdirectory. Ancestor files load at session start; descendant files load on-demand when Claude accesses files in those directories. `.claude/rules/*.md` adds path-scoped rules loaded conditionally.

**OpenAI Codex** walks from git root to CWD, checking each level for `AGENTS.override.md` then `AGENTS.md` then configurable fallback filenames. Pure concatenation — no override or merge semantics. All found files contribute. Default size cap: 32 KiB, configurable to 65 KiB.

**Gemini CLI** uses just-in-time loading: when any tool accesses a directory, Gemini CLI scans that directory and its ancestors for `GEMINI.md` files. This enables lazy loading of deep project-specific instructions without loading everything at session start — uniquely suited for large monorepos.

**Cursor** diverges from the hierarchy pattern entirely. Instead of a loading order, it uses four activation modes per rule file: always apply, auto-attach (via glob patterns on active file), agent-requested (description-based routing), or manual (explicit @-mention). Rules coexist; multiple may be active simultaneously. This is selection by activation mode, not hierarchical inheritance.

**Path-scoping metadata exists but is incompatible.** Three tools support conditional rule activation via YAML frontmatter, each using a different field name:
- Claude Code and Cline: `paths` (glob patterns)
- GitHub Copilot: `applyTo` (plus optional `excludeAgent` to restrict by agent type)
- Cursor: `globs` (plus `alwaysApply` boolean and `description` for routing)

AGENTS.md itself has no metadata schema — it is plain Markdown. A rule file cannot be shared across tools without modification. No cross-tool standardization of path-scoping exists as of 2026.

**Practical implications for plugin and skill authors.** Rules scoped to specific paths reduce context noise. Claude Code's `paths` frontmatter in `.claude/rules/` is the mechanism to scope rules to file types (e.g., TypeScript rules only when editing `.ts` files). Without path-scoping, all rules load unconditionally and compete for attention in the context window — a key source of instruction capacity waste.
