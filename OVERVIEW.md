# WOS Overview

WOS is a Claude Code plugin that helps build and maintain structured project
context — turning research into evidence-based context files, and using that
substrate to plan, execute, and deliver work.

## How It Works

```mermaid
flowchart TB
    subgraph Knowledge["Knowledge Layer"]
        research["/wos:research"] --> distill["/wos:distill"]
    end

    distill --> context[("docs/context/\ndocs/research/")]

    subgraph Delivery["Delivery Layer"]
        scopework["/wos:scope-work"] --> planwork["/wos:plan-work"]
        planwork --> startwork["/wos:start-work"]
        startwork --> checkwork["/wos:check-work"]
        checkwork --> finishwork["/wos:finish-work"]
        planwork -."infeasibility\nfeedback".-> scopework
    end

    context --> scopework

    subgraph Infrastructure["Infrastructure Layer"]
        init["/wos:setup"] -."creates".-> discovery["Frontmatter\n_index.md\nAGENTS.md"]
        lint["/wos:lint"] -."validates".-> discovery
    end

    discovery -."enables navigation".-> context

    subgraph Feedback["Feedback Layer"]
        principles["/wos:principles"]
        refineprompt["/wos:refine-prompt"]
        retrospective["/wos:retrospective (standalone)"]
        reportissue["/wos:report-issue"]
    end
```

### Knowledge Layer

**Research** conducts structured investigations using the SIFT framework (Stop,
Investigate, Find better coverage, Trace claims) and produces verified research
documents with confidence-rated findings. **Distill** converts those research
artifacts into focused context files (200-800 words each) stored in `docs/context/`.
Together they build the evidence-based substrate that planning draws from.

### Delivery Layer

A linear pipeline from idea to merged code:

1. **Scope Work** — divergent-then-convergent design dialogue; produces an approved design doc
2. **Plan Work** — converts the design into a structured implementation plan with tasks, file changes, and validation criteria; includes an infeasibility check that can loop back to scope-work
3. **Start Work** — implements each task, commits with SHA-tracked checkboxes, supports multi-session resumption
4. **Check Work** — verifies completed work meets validation criteria, either from a plan's Validation section or ad-hoc (built from git diff, project config, and project docs); in plan mode, plan stays in `executing` until all criteria pass
5. **Finish Work** — presents integration options (merge, PR, keep, discard) after tests pass; nudges `/wos:retrospective`

### Infrastructure Layer

**Init** creates the discovery infrastructure: directory structure (`docs/context/`,
`docs/research/`, `docs/plans/`, `docs/designs/`), the WOS-managed section in AGENTS.md with
navigation instructions, and auto-generated `_index.md` files. **Audit** validates
that infrastructure stays healthy — checking frontmatter, content quality, URL
reachability, index sync, and skill quality.

The discovery mechanism is what makes context files usable: frontmatter makes each
document self-describing, `_index.md` files make directories browsable, and AGENTS.md
teaches agents how to navigate the project.

### Feedback Layer

Skills that operate independently at any point in the lifecycle:

- **Principles** — captures and maintains project principles in `PRINCIPLES.md`; detects drift over time
- **Refine Prompt** — assesses and improves prompts (including SKILL.md files) using evidence-backed techniques
- **Retrospective** — reviews the current session and submits structured feedback as a GitHub Issue; offered as a nudge at the end of `/wos:finish-work`
- **Report Issue** — files bugs, feature requests, and feedback against the WOS repo

## Skills Reference

| Skill | Purpose |
|-------|---------|
| `/wos:audit` | Full project health check — orchestrates lint, check-skill, check-rule, check-skill-chain, and wiki validation into a prioritized report |
| `/wos:setup` | Initialize or update WOS project context |
| `/wos:lint` | Validate project health (8 checks + auto-fix) |
| `/wos:research` | SIFT-based research with source verification |
| `/wos:distill` | Convert research artifacts into focused context files |
| `/wos:scope-work` | Collaborative design dialogue before planning |
| `/wos:plan-work` | Convert approved designs into implementation plans |
| `/wos:start-work` | Execute plans with lifecycle enforcement |
| `/wos:check-work` | Verify completed work (plan-based or ad-hoc) |
| `/wos:finish-work` | Structured work integration (merge/PR/keep/discard) |
| `/wos:principles` | Capture and maintain project principles |
| `/wos:refine-prompt` | Assess and refine prompts using evidence-backed techniques |
| `/wos:retrospective` | Session review and feedback submission (standalone) |
| `/wos:report-issue` | File GitHub issues against WOS repo |

### Commands

| Command | Purpose |
|---------|---------|
| `/wos:consider` | Mental models for problem analysis (16 models) |
| `/wos:consider:{model}` | Apply a specific mental model (e.g., `first-principles`, `inversion`) |
