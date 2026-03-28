---
name: "Convention-Driven Design"
description: "How implicit contracts — naming, file layout, metadata formats — enable agents to discover and follow patterns without configuration, and the 'derive from disk, never hand-curate' philosophy"
metadata:
  type: research
  sources:
    - https://rubyonrails.org/doctrine
    - https://en.wikipedia.org/wiki/Convention_over_configuration
    - https://go.dev/doc/modules/layout
    - https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
    - https://nextjs.org/docs/app/getting-started/project-structure
    - https://guides.emberjs.com/v1.11.0/concepts/naming-conventions/
    - https://peps.python.org/pep-0020/
    - https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9
    - https://pnote.eu/notes/agents-md/
    - https://github.com/golang-standards/project-layout
  related:
    - docs/context/convention-driven-design.md
    - docs/context/information-architecture.md
    - docs/context/tool-design-for-llms.md
---

Convention-driven design is the practice of encoding behavioral contracts in naming, file layout, and metadata formats so that consumers — human developers, build tools, or LLM agents — can discover and follow patterns without explicit configuration. The principle traces from Maven and Rails through Go and Next.js to the emerging convention of AGENTS.md and CLAUDE.md files that LLM agents read to orient themselves in a codebase. The central insight: when structure is predictable, configuration becomes unnecessary, and tooling can derive behavior from disk state alone.

## Sub-Questions

1. Where does convention-over-configuration originate, and what problem does it solve?
2. How do specific frameworks (Rails, Go, Maven, Next.js, Ember) implement conventions?
3. What makes a convention discoverable — what turns a naming pattern into an implicit contract?
4. How does the "derive from disk, never hand-curate" principle work in practice?
5. What are the trade-offs between implicit conventions and explicit configuration?
6. How do LLM agent systems use file-based conventions for behavior discovery?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://rubyonrails.org/doctrine | The Rails Doctrine | DHH / Rails Core | 2016 | T1 | verified |
| 2 | https://en.wikipedia.org/wiki/Convention_over_configuration | Convention over Configuration | Wikipedia | 2024 | T3 | verified |
| 3 | https://go.dev/doc/modules/layout | Organizing a Go Module | Go Team | 2024 | T1 | verified |
| 4 | https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html | Introduction to the Standard Directory Layout | Apache Maven | 2024 | T1 | verified |
| 5 | https://nextjs.org/docs/app/getting-started/project-structure | Project Structure and Organization | Vercel / Next.js | 2026 | T1 | verified |
| 6 | https://guides.emberjs.com/v1.11.0/concepts/naming-conventions/ | Naming Conventions | Ember.js | 2015 | T1 | verified |
| 7 | https://peps.python.org/pep-0020/ | PEP 20 — The Zen of Python | Tim Peters | 2004 | T1 | verified |
| 8 | https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9 | The Complete Guide to AI Agent Memory Files | Data Science Collective | 2025 | T3 | verified |
| 9 | https://pnote.eu/notes/agents-md/ | AGENTS.md Becomes the Convention | pnote.eu | 2025 | T3 | verified |
| 10 | https://github.com/golang-standards/project-layout | Standard Go Project Layout | golang-standards | 2024 | T3 | verified |

## Findings

### 1. Origins: Convention Over Configuration

Convention over configuration (CoC) emerged as a named principle with Ruby on Rails in 2004, though the underlying idea — sensible defaults that reduce boilerplate — predates it. David Heinemeier Hansson extracted Rails from Basecamp and articulated CoC as a direct response to the XML configuration sprawl of Java frameworks like EJB and early Spring [1][2]. The insight was that hundreds of small decisions developers make daily are "borderline arbitrary" and can be made upfront by the framework, freeing developers to specify only what deviates from the norm.

The Rails Doctrine frames CoC not as a mere convenience but as a design philosophy with second-order effects [1]. When a framework makes decisions for you, it creates a shared vocabulary. Every Rails developer knows that a `Post` model maps to a `posts` table, that controllers live in `app/controllers/`, and that `app/views/posts/show.html.erb` renders the show action. This shared vocabulary reduces onboarding time, enables code review across unfamiliar codebases, and makes tooling possible — generators, linters, and debuggers can all rely on predictable structure.

Maven formalized a similar principle for Java builds. Its standard directory layout (`src/main/java/`, `src/test/java/`, `src/main/resources/`) means that Maven knows where to find source code, tests, and resources without any configuration in the POM file [4]. The location of files within the standard layout determines how they are processed — Java files under `src/main/java/` are compiled; files under `src/main/resources/` are bundled into the JAR. The convention is the configuration.

**Key principle:** CoC works when the convention encodes a decision that is (a) frequently needed, (b) has a sensible default, and (c) can be overridden when necessary. Conventions that cannot be overridden become constraints; conventions that are rarely needed become clutter (HIGH — T1 sources converge) [1][2][4].

### 2. How Frameworks Implement Conventions

Four distinct implementation strategies emerge from studying major frameworks:

**Name-to-behavior mapping (Rails, Ember).** A file's name or class name determines its role. Rails maps the `PostsController` class to `/posts` routes automatically. Ember's resolver takes this further: a file at `app/routes/user.js` is automatically wired as the route handler for `/user` without any import statement or registration [1][6]. The resolver uses filenames to create associations, eliminating manual wiring. This strategy is powerful but creates discoverability challenges — IDE "find all references" may return nothing because the wiring happens through naming conventions and reflection, not explicit code [6].

**Directory-as-contract (Go, Maven).** Directory placement determines visibility and behavior. Go enforces that packages in `internal/` cannot be imported by external modules — this is not merely a convention but a constraint enforced by the Go toolchain [3][10]. Maven's `src/main/` vs. `src/test/` split determines whether code ships in the production artifact or exists only for testing [4]. The directory path itself is the declaration of intent.

**File-presence-as-behavior (Next.js).** The existence of a file with a specific name activates framework behavior. Adding `page.tsx` to a directory makes it a route. Adding `loading.tsx` adds a loading skeleton. Adding `error.tsx` adds an error boundary [5]. No configuration file references these; the framework scans the filesystem and derives behavior from what it finds. This is the purest expression of "derive from disk" — the filesystem is the configuration.

**Metadata-driven discovery (AGENTS.md, CLAUDE.md, frontmatter).** Files contain structured metadata (YAML frontmatter, Markdown headers) that consumers parse to understand purpose and relationships. AGENTS.md files are now supported by Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, and others [8][9]. The closest AGENTS.md to the file being edited takes precedence, creating a hierarchical convention where directory placement determines scope. This pattern combines file-presence (the file must exist) with metadata-driven behavior (the content determines the instructions).

### 3. What Makes a Convention Discoverable

Not all naming patterns become conventions. The ones that succeed share specific properties:

**Predictability.** A developer (or agent) who has seen the convention once can predict where to find or place new items. Rails' pluralization rule (model `Post`, table `posts`, controller `PostsController`) is predictable because it follows a single, consistent transformation. Go's `internal/` directory is predictable because it uses a single reserved name with a single meaning [1][3].

**Locality.** The convention's effect is visible at the point of use. In Next.js, the `page.tsx` file sits in the same directory as the route it defines — you do not need to consult a separate routing configuration to understand the mapping [5]. In Maven, the relationship between `src/main/java/com/example/Foo.java` and the compiled `com.example.Foo` class is visible in the path itself [4].

**Consistency.** The convention applies uniformly across the entire codebase. Ember's resolver works because every route, controller, component, and service follows the same naming pattern [6]. When conventions have exceptions, they stop being conventions and become traps.

**Self-documentation.** The convention communicates intent through names alone. `_index.md` signals "this is a directory index." `SKILL.md` signals "this defines a skill." The underscore prefix in Next.js (`_components/`, `_lib/`) signals "this is private, not routable" [5]. Good conventions are legible without documentation — but should still be documented for newcomers.

**Tooling support.** A convention becomes entrenched when tools rely on it. Go's `internal/` directory started as a convention and was then enforced by the compiler. Next.js file conventions are enforced by the build system. Maven's directory layout is enforced by the build lifecycle. When tooling validates conventions, violations become errors rather than drift (HIGH — pattern across all examined frameworks) [3][4][5].

### 4. Derive from Disk, Never Hand-Curate

The "derive from disk" principle states that navigation artifacts, indexes, and structural metadata should be generated from the filesystem rather than maintained by hand. This is a specific application of the broader "single source of truth" principle: the filesystem is the source of truth; everything else is derived.

**Why hand-curation fails:** Hand-maintained indexes, tables of contents, and navigation files drift from reality the moment a file is added, renamed, or deleted. The drift is silent — no error is raised, no test fails. Over time, the curated artifact becomes unreliable, and consumers learn to distrust it. For LLM agents, an index that lists a file that does not exist or omits a file that does exist is worse than no index at all, because it introduces incorrect context into the agent's reasoning.

**How derivation works in practice:**

- **Auto-generated indexes.** Each directory has an `_index.md` generated by scanning the directory and extracting frontmatter descriptions. When a file is added or removed, re-running the indexer produces an accurate index. The index is never edited by hand.
- **Convention-driven routing.** Next.js scans `app/` and builds routes from the filesystem. No routing configuration file exists to go stale [5].
- **Package discovery.** Go discovers packages by directory structure. Python discovers packages by `__init__.py` presence. No manifest lists packages.
- **Navigation from structure.** AGENTS.md contains a WOS-managed section generated from project state. The content between `<!-- wos:begin -->` and `<!-- wos:end -->` markers is machine-maintained.

**The derivation contract:** For this principle to work, two conditions must hold: (1) the filesystem conventions must be complete — every piece of information needed to generate the derived artifact must exist on disk, and (2) the generation process must be deterministic — the same disk state must always produce the same derived output. When these conditions hold, the derived artifact is always trustworthy because it can always be regenerated.

### 5. Trade-offs: Implicit vs. Explicit

The tension between implicit conventions and explicit configuration is real and well-documented. Python's Zen captures one side: "Explicit is better than implicit" [7]. Rails captures the other: "Convention over configuration" [1]. Both are right in their context.

**Arguments for conventions (implicit contracts):**

- **Reduced boilerplate.** Developers specify only what differs from the default. A new Rails model requires no configuration to get database mapping, routing, and views.
- **Shared vocabulary.** Conventions create a common language. Any Rails developer can navigate any Rails project. Any Go developer knows what `internal/` means.
- **Tooling enablement.** Conventions make automated tooling possible. Generators, linters, indexers, and agents can all operate on predictable structure.
- **Reduced decision fatigue.** Conventions answer "where does this go?" before the question is asked [1][2].

**Arguments for configuration (explicit contracts):**

- **Discoverability.** Explicit configuration is greppable. Conventions discovered through reflection or naming patterns may not appear in IDE searches [6].
- **Transparency.** Explicit configuration shows exactly what is happening. Conventions can feel like "magic" — behavior appears without visible cause, making debugging harder for newcomers [2].
- **Flexibility.** Configuration allows arbitrary customization. Conventions work only when the default is right; when it is not, overriding a convention can be harder than writing configuration from scratch.
- **The Python argument.** When reading code, explicit imports, explicit type annotations, and explicit configuration make the code's behavior self-evident [7].

**The practical resolution:** The most successful systems use conventions for common cases and configuration for exceptions. Rails provides conventions for the 80% case and configuration hooks for the 20%. Go enforces `internal/` by convention (and compiler) but allows arbitrary package naming otherwise. Next.js derives routes from the filesystem but allows `next.config.js` for custom behavior [1][3][5].

**For agent systems specifically**, conventions are strongly preferred over configuration because agents discover structure by reading files, not by being pre-programmed. An agent that encounters a `docs/research/` directory can infer its purpose from the name. An agent that reads `_index.md` gets a machine-readable manifest. An agent that finds AGENTS.md gets behavioral instructions. All of this works without the agent being configured to look for these specific patterns — the conventions are self-describing (HIGH — convergence across agent tooling ecosystem) [8][9].

### 6. Agent Systems and Convention-Based Discovery

The emergence of AGENTS.md as a cross-tool standard illustrates how conventions propagate in the agent ecosystem. The pattern started with Claude Code's CLAUDE.md — a single Markdown file that the agent reads at session start to understand project structure, conventions, and instructions [8]. Other tools adopted the same concept: Cursor, GitHub Copilot, Gemini CLI, Windsurf, Aider, Zed, and others now support AGENTS.md [9].

**Key properties of the AGENTS.md convention:**

- **File-presence-as-activation.** The agent looks for the file by name. If it exists, the agent reads it. No configuration tells the agent to look — the convention is hardcoded into the agent's behavior.
- **Hierarchical scoping.** Multiple AGENTS.md files can exist at different directory levels. The closest file to the work being done takes precedence. This mirrors how `.gitignore` and `.editorconfig` work — directory placement determines scope [8][9].
- **Plain Markdown.** No special schema, no YAML configuration, no tooling-specific format. The convention is the file name and location; the content is human-readable Markdown that agents also understand.
- **Complementary files.** README.md is for humans, AGENTS.md is the universal agent brief, CLAUDE.md adds tool-specific instructions on top [8]. The convention stack uses file naming to determine audience and purpose.

**Convention-driven skill discovery** extends this pattern further. In plugin systems like WOS, skills are discovered by directory structure: each subdirectory of `skills/` that contains a `SKILL.md` file is a skill. The skill's name comes from the directory name. Its instructions come from the SKILL.md content. Its references come from a `references/` subdirectory. No manifest or registry lists the available skills — the filesystem is the registry.

**Frontmatter as implicit contract.** YAML frontmatter at the top of Markdown files creates a metadata layer that agents parse for navigation. The `name` and `description` fields serve as the agent's "information scent" — structured signals that answer "is this document relevant?" without requiring full content reads. The `type` field enables filtering. The `related` field enables graph traversal. The `sources` field enables provenance checking. All of this metadata follows a convention (field names, format, position) that agents can rely on without per-project configuration.

## Challenge

**What if conventions become invisible constraints?** The risk of implicit contracts is that they constrain without being visible. A developer who does not know that `internal/` has special meaning in Go may place code there accidentally and be confused when external packages cannot import it. A user who names a file `page.tsx` in a Next.js project activates routing behavior they may not have intended. Conventions must be documented to be discoverable — and documentation itself can drift from reality unless it too is derived from the conventions it describes.

**What about convention conflicts across tools?** As more tools adopt file-based conventions, naming conflicts become possible. A `.cursor/` directory, a `.claude/` directory, and an AGENTS.md file may contain contradictory instructions. The emerging resolution is layered precedence (AGENTS.md as universal base, tool-specific files for overrides), but this itself is a convention that must be learned.

**Does convention-driven design scale?** Small projects benefit from conventions because the entire convention set fits in a developer's (or agent's) working memory. Large projects may accumulate dozens of conventions across different subsystems. At some point, the mental overhead of learning all conventions exceeds the overhead of reading configuration files. The counter-argument: conventions are learnable once and applicable everywhere, while configuration must be read per-project.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | DHH extracted Rails from Basecamp in 2004 and articulated CoC as a core principle | attribution | [1][2] | verified |
| 2 | Rails' CoC was a direct response to XML configuration sprawl in Java frameworks | motivation | [1][2] | verified |
| 3 | Go's `internal/` directory convention is enforced by the Go toolchain, not just by custom | mechanism | [3] | verified |
| 4 | Maven's standard directory layout eliminates build configuration for file location | mechanism | [4] | verified |
| 5 | Next.js derives route behavior from file presence (`page.tsx`, `loading.tsx`, `error.tsx`) | mechanism | [5] | verified |
| 6 | Ember's resolver auto-wires components by filename without explicit imports | mechanism | [6] | verified |
| 7 | AGENTS.md is supported by Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, and others | adoption | [8][9] | verified |
| 8 | "Explicit is better than implicit" is from PEP 20, written by Tim Peters in 1999/2004 | attribution | [7] | verified |

## Search Protocol

| # | Query | Tool | Results | Useful |
|---|-------|------|---------|--------|
| 1 | "convention over configuration Rails philosophy origin David Heinemeier Hansson" | WebSearch | 10 | 4 |
| 2 | "Go project layout conventions standard structure golang-standards" | WebSearch | 10 | 3 |
| 3 | "implicit contracts software design naming conventions file layout metadata discovery" | WebSearch | 10 | 2 |
| 4 | "agent systems derive behavior from disk layout convention-driven LLM agents" | WebSearch | 10 | 2 |
| 5 | "CLAUDE.md AGENTS.md convention file-based agent configuration Claude Code" | WebSearch | 10 | 5 |
| 6 | "derive from disk convention over configuration implicit contracts software architecture" | WebSearch | 10 | 3 |
| 7 | "Next.js file-based routing convention over configuration framework examples" | WebSearch | 10 | 4 |
| 8 | "Maven standard directory layout convention over configuration" | WebSearch | 10 | 3 |
| 9 | "Ember.js convention over configuration resolver patterns file naming automatic discovery" | WebSearch | 10 | 4 |
| 10 | "Zen of Python explicit is better than implicit convention configuration trade-off" | WebSearch | 10 | 3 |

## Takeaways

Convention-driven design is the pattern that connects Rails routing to Go's `internal/` directory to Next.js file-based routing to AGENTS.md agent configuration. Six principles emerge:

1. **Conventions encode frequently-needed decisions as defaults.** The convention must solve a decision that arises in nearly every project. Rails' model-to-table mapping, Maven's directory layout, and AGENTS.md's agent instructions all address universal needs. Conventions for rare cases add complexity without payoff.

2. **The filesystem is the most universal configuration surface.** Every tool can read the filesystem. File names, directory structure, and file presence work across languages, build systems, and agent frameworks. This is why file-based conventions (Next.js routes, AGENTS.md, `_index.md`) propagate more readily than framework-specific configuration formats.

3. **Derive, never hand-curate.** Any artifact that can be computed from disk state should be computed from disk state. Hand-maintained indexes, navigation files, and manifests drift silently. Auto-generated artifacts stay accurate by construction. The generation process must be deterministic and the filesystem conventions must be complete.

4. **Conventions require tooling to become contracts.** A naming pattern becomes a convention when people follow it. A convention becomes a contract when tooling enforces it. Go's compiler enforcing `internal/`, Next.js's build enforcing file conventions, and WOS's audit checking index sync all convert soft conventions into hard contracts with error feedback.

5. **Layer conventions for different audiences.** README.md serves humans, AGENTS.md serves agents universally, CLAUDE.md serves a specific tool. Frontmatter serves machine parsers, document body serves readers. Each layer follows its own conventions, and the layers compose without conflict because naming determines audience.

6. **Document conventions, but derive the documentation.** The bootstrapping problem — conventions must be documented to be discovered, but documentation drifts — resolves when the documentation itself is derived from the conventions. AGENTS.md sections generated from project state, indexes generated from disk, and skill manifests generated from directory structure close the loop.
