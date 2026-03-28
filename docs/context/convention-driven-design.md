---
name: "Convention-Driven Design"
description: "How implicit contracts in naming, file layout, and metadata enable agents and tools to discover behavior from disk structure without configuration"
metadata:
  type: reference
  sources:
    - https://rubyonrails.org/doctrine
    - https://en.wikipedia.org/wiki/Convention_over_configuration
    - https://go.dev/doc/modules/layout
    - https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
    - https://nextjs.org/docs/app/getting-started/project-structure
  related:
    - docs/research/convention-driven-design.md
    - docs/context/information-architecture.md
    - docs/context/tool-design-for-llms.md
---

Convention-driven design encodes behavioral contracts in naming, file layout, and metadata formats so that consumers -- developers, build tools, or LLM agents -- discover and follow patterns without explicit configuration. The central insight: when structure is predictable, configuration becomes unnecessary, and tooling can derive behavior from disk state alone.

## When Conventions Work

A convention succeeds when it encodes a decision that is (a) frequently needed, (b) has a sensible default, and (c) can be overridden when necessary. Rails' model-to-table mapping, Maven's directory layout, and AGENTS.md agent instructions all address universal needs. Conventions that cannot be overridden become constraints; conventions for rare cases add complexity without payoff.

## Four Implementation Strategies

Frameworks implement conventions through four distinct patterns:

**Name-to-behavior mapping.** A file or class name determines its role. Rails maps `PostsController` to `/posts` routes. Ember's resolver wires `app/routes/user.js` as the `/user` handler without explicit registration. Powerful, but IDE "find all references" may miss connections made through naming and reflection.

**Directory-as-contract.** Directory placement determines visibility and behavior. Go's `internal/` packages cannot be imported externally -- enforced by the compiler, not just convention. Maven's `src/main/` vs `src/test/` split determines what ships in production.

**File-presence-as-behavior.** File existence activates framework behavior. Adding `page.tsx` in Next.js creates a route. Adding `loading.tsx` adds a loading skeleton. No configuration references these files; the framework scans the filesystem and derives behavior from what it finds. This is the purest expression of derive-from-disk.

**Metadata-driven discovery.** Files contain structured metadata (YAML frontmatter, Markdown headers) that consumers parse for purpose and relationships. AGENTS.md is now supported across Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, and others. The closest AGENTS.md to the file being edited takes precedence, creating hierarchical scoping through directory placement.

## What Makes Conventions Discoverable

Five properties distinguish conventions that stick from naming patterns that fade:

- **Predictability.** Seeing the pattern once lets you predict where new items go. Rails' pluralization rule, Go's `internal/` directory -- one transformation, universally applied.
- **Locality.** The convention's effect is visible at the point of use. Next.js `page.tsx` sits in the directory of the route it defines, not in a separate config.
- **Consistency.** The convention applies uniformly. Exceptions turn conventions into traps.
- **Self-documentation.** Names communicate intent. `_index.md` signals directory index, `SKILL.md` signals skill definition, underscore prefix signals private.
- **Tooling enforcement.** A naming pattern becomes a convention when people follow it. It becomes a contract when tooling enforces it -- Go's compiler enforcing `internal/`, audit checks verifying index sync.

## Derive from Disk, Never Hand-Curate

Navigation artifacts, indexes, and structural metadata should be generated from the filesystem rather than maintained by hand. Hand-curated indexes drift silently the moment a file is added, renamed, or deleted. For agents, an index listing a nonexistent file is worse than no index, because it introduces incorrect context into reasoning.

The derivation contract requires two conditions: (1) filesystem conventions must be complete -- every piece of information needed exists on disk, and (2) generation must be deterministic -- same disk state always produces the same output. When both hold, derived artifacts are always trustworthy because they can always be regenerated.

## Conventions vs. Configuration

The practical resolution is not either/or. Conventions handle the common case; configuration handles exceptions. Rails provides conventions for the 80% and configuration hooks for the 20%. Go enforces `internal/` by convention but allows arbitrary package naming otherwise.

For agent systems specifically, conventions are strongly preferred because agents discover structure by reading files, not by being pre-programmed. An agent encountering `docs/research/` infers purpose from the name. Reading `_index.md` provides a machine-readable manifest. Finding AGENTS.md delivers behavioral instructions. All of this works without per-project configuration -- the conventions are self-describing.

## Agent Convention Patterns

Frontmatter fields (name, description, type, related) serve as the agent's information scent -- structured signals answering "is this relevant?" without full content reads. Skill discovery follows the same principle: each `skills/` subdirectory containing `SKILL.md` is a skill. The directory name is the skill name. The filesystem is the registry.

The bootstrapping problem -- conventions must be documented to be discovered, but documentation drifts -- resolves when documentation itself is derived from conventions. Auto-generated AGENTS.md sections, disk-derived indexes, and directory-scanned skill manifests close the loop.
