# WOS Workflow Guide

WOS has five canonical workflows. Everything you build, learn, or improve fits
one of them. This document shows the skill sequences, gates, and handoffs —
use it to orient quickly without reading individual SKILL.md files.

## 1. Development Lifecycle

Primary pipeline from idea to merged code:

```
/wos:consider → /wos:brainstorm → /wos:write-plan → /wos:execute-plan → /wos:validate-work → /wos:finish-work
```

| Step | Skill | Gate / Output |
|------|-------|---------------|
| Think it through | `/wos:consider` | Optional. Apply a mental model (16 available) before designing. Produces a framed problem statement. |
| Design | `/wos:brainstorm` | Receives: topic or problem. **Gate:** user approves design doc. Produces: `docs/designs/*.design.md` |
| Plan | `/wos:write-plan` | Receives: design doc or description. **Gate:** user approves plan. Produces: `docs/plans/*.plan.md` (`status: approved`) |
| Execute | `/wos:execute-plan` | Receives: plan with `status: approved`. **Gate:** all tasks `[x]` with commit SHAs. Produces: implemented code on feature branch |
| Validate | `/wos:validate-work` | Receives: plan (or ad-hoc). **Gate:** all validation criteria pass. Produces: pass/fail report per criterion |
| Integrate | `/wos:finish-work` | Receives: validated implementation on feature branch. **Gate:** tests pass. Produces: PR opened or merge completed |

**Supporting skills at any stage:**
- `/wos:research` — gather evidence before brainstorming; chains to `/wos:write-plan` with verified findings
- `/wos:refine-prompt` — improve a SKILL.md, plan task, or prompt before acting on it

If `/wos:write-plan` finds the design infeasible, it returns structured feedback to `/wos:brainstorm`
for revision. The plan's `status` field tracks position in the lifecycle:
`draft → approved → executing → completed`.

## 2. Knowledge Management Lifecycle

How external knowledge enters the wiki and stays healthy:

**Fast path (authoritative source, well-understood topic):**
```
source → /wos:ingest → docs/context/ → /wos:lint
```

**High-rigor path (topic needs investigation before committing findings):**
```
question → /wos:research → docs/research/*.research.md → /wos:distill → docs/context/ → /wos:ingest → /wos:lint
```

| Step | Skill | Gate / Output |
|------|-------|---------------|
| Initialize | `/wos:setup` | Creates `docs/` structure, AGENTS.md, `_index.md` files. Required once per project. |
| Ingest (fast) | `/wos:ingest` | Receives: URL, file path, or pasted text. Append-only. Produces: wiki pages in `docs/context/` |
| Research (rigor) | `/wos:research` | Receives: question. SIFT framework. Produces: `docs/research/*.research.md` with sources and confidence ratings |
| Distill | `/wos:distill` | Receives: research artifact. Produces: focused context doc (200–800 words) in `docs/context/` |
| Validate | `/wos:lint` | Receives: project root. Produces: validation report (frontmatter, URLs, index sync, content length). Read-only. |

Run `/wos:lint` after any batch of ingest or distill operations to catch
frontmatter errors, broken URLs, and index drift before they accumulate.

## 3. Self-Improvement Loop

How WOS improves itself — or how you improve your own WOS configuration:

```
/wos:audit → gaps identified → /wos:build-* → /wos:audit-* → /wos:audit-chain → clean
```

| Step | Skill | Gate / Output |
|------|-------|---------------|
| Diagnose | `/wos:audit` | Orchestrates lint + audit-skill + audit-rule + audit-chain + wiki validation. Produces: prioritized health report |
| Build | `/wos:build-*` | Create the missing or broken primitive — skill, rule, subagent, command, or hook |
| Verify primitive | `/wos:audit-*` | Audit the new primitive in isolation. **Gate:** no failing checks |
| Verify chains | `/wos:audit-chain` | Confirm workflow chains remain well-formed after changes. **Gate:** "well-formed" confirmation |

See [Primitive Taxonomy](#5-primitive-taxonomy) for the full build/audit pairing.

## 4. Skill Chain Design

How to design multi-skill workflows and verify they're coherent:

**Goal mode — design a new chain from scratch:**
```
workflow goal → /wos:audit-chain → *.chain.md manifest
```

**Manifest mode — audit and repair an existing chain:**
```
*.chain.md → /wos:audit-chain → findings table → targeted edits → re-audit → clean
```

| Input | Mode | Output |
|-------|------|--------|
| Free-text workflow goal | Goal mode | `docs/plans/YYYY-MM-DD-<name>.chain.md` manifest |
| Path to `*.chain.md` | Manifest mode | Findings table; optionally, targeted edits to manifest or referenced SKILL.md files |

**Goal mode** is design-only — `/wos:audit-chain` creates the manifest but
never executes chain steps. The manifest is the deliverable; pass it to
`/wos:execute-plan` to run the steps manually.

**Manifest mode** runs five structural checks: skills exist, contracts
declared, gates on consequential steps, termination condition, no cycles.
Fixes are applied one at a time with confirmation; cross-reference mismatches
are flagged as `warn` and the user decides what to fix.

## 5. Primitive Taxonomy

The complete build/audit pairing for every WOS primitive:

| Goal | Build | Audit |
|------|-------|-------|
| Create or improve a skill | `/wos:build-skill` | `/wos:audit-skill` |
| Create or improve a rule | `/wos:build-rule` | `/wos:audit-rule` |
| Create or improve a subagent | `/wos:build-subagent` | `/wos:audit-subagent` |
| Create or improve a command | `/wos:build-command` | `/wos:audit-command` |
| Create or improve a hook | `/wos:build-hook` | `/wos:audit-hook` |
| Design or audit a skill chain | — | `/wos:audit-chain` |
| Project-wide health check | — | `/wos:audit` |
| Content quality validation | — | `/wos:lint` |

**Build** skills scaffold a new primitive from a description and I/O contract.
**Audit** skills surface quality issues in existing primitives — structure,
coverage, anti-patterns, and specificity.

Chain each build step directly into the matching audit: create with
`/wos:build-*`, verify with `/wos:audit-*`, confirm chains are clean
with `/wos:audit-chain`, then confirm project health with `/wos:audit`.

---

**Quick reference:** Development work starts at `/wos:brainstorm`. Knowledge
capture starts at `/wos:ingest` (fast) or `/wos:research` (rigorous). WOS
self-improvement starts at `/wos:audit`. Chain design starts at
`/wos:audit-chain`. Build anything new with the appropriate `/wos:build-*`
skill; verify it with the matching `/wos:audit-*`.

*Deprecated:* `/wos:retrospective` (use `/wos:finish-work` Step 6).
