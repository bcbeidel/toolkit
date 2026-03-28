---
name: Flexible Document Layout
description: Decouple WOS document management from fixed directory hierarchies — discover documents by frontmatter, type by suffix/metadata, let users organize freely
metadata:
  type: design
  status: completed
  related:
    - docs/designs/cross-platform-deploy-design.md
---

## Purpose

Decouple WOS document management from fixed directory hierarchies. Documents
are identified by frontmatter presence, typed by suffix or frontmatter
metadata, and discovered by walking the project tree. Users organize files
however they want — WOS observes and adapts.

## Behavior

### Discovery

- On any operation that needs to find documents (audit, reindex, navigation
  update), WOS walks from the project root.
- Skips `.git/` unconditionally. Skips paths matching `.gitignore` rules.
- Any `.md` file with valid WOS frontmatter (`name` + `description` between
  `---` fences) is a managed document.
- `_index.md` files are never treated as managed documents (they're generated
  artifacts).

### Type Resolution

- File suffix wins first: `foo.plan.md` → type `plan`.
- Frontmatter `type` field wins second: `type: research` in frontmatter.
- If both present, frontmatter takes precedence (explicit over inferred).
- If neither, document is managed but untyped — still validated for
  frontmatter, related paths, etc.

### Validation

- Rules bind to document type, not path. Context-type docs get word-count
  checks. Research-type docs require sources. Plans get structure checks.
- Path-based filtering (`doc.path.startswith("docs/context/")`) is eliminated
  entirely.

### Navigation

- AGENTS.md navigation section is generated from discovered documents,
  reflecting actual directory structure.
- `_index.md` generated for any directory that contains at least one managed
  document or subdirectory with managed documents.

### Pattern Hint

- During `/wos:init-wos`, user selects from four layout patterns: separated,
  co-located, flat, none.
- Choice is recorded in the AGENTS.md WOS-managed section (e.g.,
  `<!-- wos:layout: co-located -->`).
- Skills read this hint to suggest default save locations. User can always
  override.

## Layout Patterns

### Separated (current default)

Group by artifact type. `docs/context/`, `docs/plans/`, `docs/designs/`,
`docs/research/`. Good for teams that want clear separation.

### Co-located

`docs/{project-name}/` contains all artifact types together. Design, plan,
research, context for a feature live side-by-side. Good for feature-driven
work.

### Flat

Everything in `docs/`. No subdirectories. Rely on suffixes (`.plan.md`,
`.research.md`) to distinguish types. Good for small projects.

### None

Just `AGENTS.md` and `CLAUDE.md`, no `docs/` directory. User builds
structure organically as they go.

## Components

### New modules

- `wos/discovery.py` — tree walker with `.gitignore` support and
  frontmatter-based document detection.

### Modified modules

- `wos/validators.py` — remove path-based filtering, key all rules off
  document type.
- `wos/agents_md.py` — generate navigation from discovered documents instead
  of hardcoded paths; read/write layout hint.
- `wos/index.py` — no structural changes, but callers change (index generated
  for directories with managed docs, not just `docs/` subdirs).
- `scripts/audit.py` — use discovery instead of `docs/` walk.
- `scripts/reindex.py` — use discovery to find directories needing indexes.

### Modified skills

- `init` → renamed to `init-wos`; adds pattern selection during setup;
  records choice in AGENTS.md.
- `brainstorm`, `write-plan`, `research`, `distill` — use pattern hint +
  existing file locations to suggest save paths instead of hardcoding
  directories.

### Unchanged

- `wos/document.py`, `wos/frontmatter.py`, `wos/suffix.py` — already
  location-independent.
- `wos/url_checker.py`, `wos/markers.py` — no directory assumptions.

## Constraints

- **Stdlib only** — `.gitignore` parsing implemented without third-party
  libraries. Support common cases (globs, negation, directory markers), not
  every edge case.
- **Backwards compatible** — projects using the current `docs/` layout
  continue to work with zero changes. Their files have frontmatter, so
  discovery finds them.
- **No new config files** — AGENTS.md is the only configuration surface. The
  layout hint is a comment marker, not a new metadata format.
- **Performance** — tree walk must be fast enough for interactive use.
  `.gitignore` filtering is the primary performance lever.

## Acceptance Criteria

1. A `.plan.md` file in `project-x/` is discovered, typed as `plan`, and
   validated with plan rules — without any configuration.
2. A `.md` file with `type: research` frontmatter in an arbitrary directory
   gets research validation (sources required, draft marker check).
3. `/wos:init-wos` presents four layout patterns, creates initial structure
   matching the selection, and records the choice in AGENTS.md.
4. `/wos:audit-wos` finds and validates all managed documents regardless of
   location.
5. `scripts/reindex.py` generates `_index.md` for directories containing
   managed documents, wherever they are.
6. AGENTS.md navigation section reflects actual document locations, not
   hardcoded paths.
7. Files matching `.gitignore` patterns and `.git/` are never walked.
8. Existing projects using `docs/` layout work without changes after upgrade.
