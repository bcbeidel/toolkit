# WOS Workflow Guide

WOS has five canonical workflows. Everything you build, learn, or improve fits
one of them. This document shows the skill sequences, gates, and handoffs —
use it to orient quickly without reading individual SKILL.md files.

## 1. Development Lifecycle

Primary pipeline from idea to merged code:

```
/wos:consider → /wos:scope-work → /wos:plan-work → /wos:start-work → /wos:check-work → /wos:finish-work
```

| Step | Skill | Gate / Output |
|------|-------|---------------|
| Think it through | `/wos:consider` | Optional. Apply a mental model (16 available) before designing. Produces a framed problem statement. |
| Design | `/wos:scope-work` | Receives: topic or problem. **Gate:** user approves design doc. Produces: `docs/designs/*.design.md` |
| Plan | `/wos:plan-work` | Receives: design doc or description. **Gate:** user approves plan. Produces: `docs/plans/*.plan.md` (`status: approved`) |
| Execute | `/wos:start-work` | Receives: plan with `status: approved`. **Gate:** all tasks `[x]` with commit SHAs. Produces: implemented code on feature branch |
| Validate | `/wos:check-work` | Receives: plan (or ad-hoc). **Gate:** all validation criteria pass. Produces: pass/fail report per criterion |
| Integrate | `/wos:finish-work` | Receives: validated implementation on feature branch. **Gate:** tests pass. Produces: PR opened or merge completed |

**Supporting skills at any stage:**
- `/wos:research` — gather evidence before scoping; chains to `/wos:plan-work` with verified findings
- `/wos:refine-prompt` — improve a SKILL.md, plan task, or prompt before acting on it
- `/wos:retrospective` — review the session and submit feedback; offered as a nudge at the end of `/wos:finish-work`

If `/wos:plan-work` finds the design infeasible, it returns structured feedback to `/wos:scope-work`
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
/wos:audit → gaps identified → /wos:build-* → /wos:check-* → /wos:check-skill-chain → clean
```

| Step | Skill | Gate / Output |
|------|-------|---------------|
| Diagnose | `/wos:audit` | Orchestrates lint + check-skill + check-rule + check-skill-chain + wiki validation. Produces: prioritized health report |
| Build | `/wos:build-*` | Create the missing or broken primitive — skill, rule, subagent, command, or hook |
| Verify primitive | `/wos:check-*` | Check the new primitive in isolation. **Gate:** no failing checks |
| Verify skill-chains | `/wos:check-skill-chain` | Confirm skill-chains remain well-formed after changes. **Gate:** "well-formed" confirmation |

See [Primitive Taxonomy](#5-primitive-taxonomy) for the full build/check pairing.

## 4. Skill-Chain Design

How to design multi-skill workflows and verify they're coherent:

**Goal mode — design a new skill-chain from scratch:**
```
workflow goal → /wos:check-skill-chain → *.chain.md manifest
```

**Manifest mode — check and repair an existing skill-chain:**
```
*.chain.md → /wos:check-skill-chain → findings table → targeted edits → re-check → clean
```

| Input | Mode | Output |
|-------|------|--------|
| Free-text workflow goal | Goal mode | `docs/plans/YYYY-MM-DD-<name>.chain.md` manifest |
| Path to `*.chain.md` | Manifest mode | Findings table; optionally, targeted edits to manifest or referenced SKILL.md files |

**Goal mode** is design-only — `/wos:check-skill-chain` creates the manifest but
never executes skill-chain steps. The manifest is the deliverable; pass it to
`/wos:start-work` to run the steps manually.

**Manifest mode** runs five structural checks: skills exist, contracts
declared, gates on consequential steps, termination condition, no cycles.
Fixes are applied one at a time with confirmation; cross-reference mismatches
are flagged as `warn` and the user decides what to fix.

## 5. Primitive Taxonomy

The complete build/check pairing for every WOS primitive:

| Goal | Build | Check |
|------|-------|-------|
| Create or improve a skill | `/wos:build-skill` | `/wos:check-skill` |
| Create or improve a rule | `/wos:build-rule` | `/wos:check-rule` |
| Create or improve a subagent | `/wos:build-subagent` | `/wos:check-subagent` |
| Create or improve a command | `/wos:build-command` | `/wos:check-command` |
| Create or improve a hook | `/wos:build-hook` | `/wos:check-hook` |
| Design or check a skill-chain | — | `/wos:check-skill-chain` |
| Project-wide health check | — | `/wos:audit` |
| Content quality validation | — | `/wos:lint` |

**Build** skills scaffold a new primitive from a description and I/O contract.
**Check** skills surface quality issues in existing primitives — structure,
coverage, anti-patterns, and specificity.

Chain each build step directly into the matching check: create with
`/wos:build-*`, verify with `/wos:check-*`, confirm skill-chains are clean
with `/wos:check-skill-chain`, then confirm project health with `/wos:audit`.

---

**Quick reference:** Development work starts at `/wos:scope-work`. Knowledge
capture starts at `/wos:ingest` (fast) or `/wos:research` (rigorous). WOS
self-improvement starts at `/wos:audit`. Skill-chain design starts at
`/wos:check-skill-chain`. Build anything new with the appropriate `/wos:build-*`
skill; verify it with the matching `/wos:check-*`.
