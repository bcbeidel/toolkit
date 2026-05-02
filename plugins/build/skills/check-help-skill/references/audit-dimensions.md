---
name: Audit Dimensions — Help-Skill
description: The complete check inventory for check-help-skill — Tier-1 deterministic checks, Tier-2 judgment dimensions, and Tier-3 cross-entity trigger-collision check. Every dimension cites its source principle in help-skill-best-practices.md. Referenced by the check-help-skill workflow and the repair playbook.
---

# Audit Dimensions

The check-help-skill audit runs in three tiers. This document is the
inventory: every deterministic check Tier-1 emits, every judgment
dimension Tier-2 evaluates, and the cross-entity collision check
Tier-3 runs. Every dimension cites the source principle from
[help-skill-best-practices.md](../../../_shared/references/help-skill-best-practices.md)
that it audits.

## Tier-1 — Deterministic Checks

Each check has an ID, severity, and the source principle it enforces.
Tier-1 is implemented as scripts (Python, per *Language Selection* in
`primitive-routing.md` — frontmatter parsing is structured-data work,
testable against `pytest`); scaffolding the scripts is a follow-on
handoff to `/build:build-python-script`. Until the scripts land, the
check-help-skill SKILL.md performs Tier-1 inline against the
inventory below.

| Check ID | What | Severity | Source principle |
|---|---|---|---|
| `slug-mismatch` | Frontmatter `name` is the literal string `help`, and the directory basename is `help` | FAIL | Use `name: help` literally — the slug is fixed |
| `frontmatter-shape` | Required frontmatter keys present: `name`, `description`, `version`, `owner`, `license`, `references:` (with at least the help-skill-best-practices.md path) | WARN | Anatomy — required frontmatter |
| `frontmatter-invented-key` | No top-level frontmatter keys outside the documented set (cross-checked against `skill-best-practices.md`) | WARN | Invent no keys the skill spec does not sanction |
| `body-line-count` | Body length ≤150 lines target, ≤200 lines hard ceiling | WARN | Keep the body short |
| `secret` | No API keys, tokens, credentials, internal hostnames, or private URLs in the file | FAIL | No embedded secrets |
| `tls-disable` | No instructions to disable TLS verification, SELinux, or firewalls | FAIL | No instructions to disable security posture |
| `pipe-to-shell` | No `curl ... \| bash` / `wget ... \| sh` / `iex (iwr ...)` invocations | FAIL | No `curl … \| bash` invitations |
| `synopsis-present` | A one-sentence synopsis appears below the H1, before the first H2 | WARN | One-sentence synopsis below the H1 is the most-read line |
| `managed-region-present` | The skill-index section contains a matching pair of `<!-- generated: ... -->` and `<!-- /generated -->` markers wrapping a markdown table | FAIL | Generate the skill table from sibling frontmatter |
| `managed-region-tampered` | Content inside the managed region matches a regeneration from current sibling frontmatter (no hand edits) | WARN | Hand-editing the table inside the managed region is the failure mode the marker exists to flag |
| `skill-index-coverage` | Every sibling skill at `plugins/<plugin>/skills/*/SKILL.md` (excluding `help`) appears as a row in the skill-index table; no rows for non-existent skills | FAIL | The skill table is the most-read part of the document and the most likely to drift |
| `skill-index-no-self` | The `help` skill does not appear in its own table | WARN | The generator must exclude `help` |
| `description-fidelity` | Each table row's trigger text matches the first ~12 words of the corresponding sibling skill's current `description` (substantive drift, not whitespace) | WARN | Description fidelity — entries reflect actual frontmatter |
| `workflow-section-present` | A `## Common workflows` section exists with at least one curated chain | WARN | Curate workflow chains; do not auto-generate |
| `workflow-freshness` | Every skill name referenced in `## Common workflows` resolves to a sibling SKILL.md on disk | WARN | A curated workflow chain that referenced the removed skill becomes a broken pointer |
| `workflow-chain-cross-plugin` | Workflow chains reference only skills inside this plugin (no cross-plugin compositions) | WARN | Workflow chains scoped to this plugin only |
| `pointer-resolution` | Every relative link in `## Where to look next` resolves to a file on disk | WARN | Pointers, not duplications — but pointers must work |
| `pointer-broken-fail` | Pointers to load-bearing navigation (AGENTS.md, RESOLVER.md, plugin README) resolve | FAIL | Pointers to canonical navigation are load-bearing |
| `description-trigger-shape` | The `description` frontmatter leads with "Use when" and includes at least one concrete trigger phrase ("what's in", "list skills", "how do I use", "which skill fits") | WARN | Lead the description with the caller's situation, not the skill's function |

**FAIL exclusions from Tier-2.** Any `slug-mismatch`, `secret`,
`tls-disable`, `pipe-to-shell`, `managed-region-missing`,
`skill-index-coverage` (rows for skills that don't exist on disk), or
`pointer-broken-fail` finding excludes the file from Tier-2.
Structural failures must be repaired before judgment evaluation runs.

**Missing-tool degradation.** Tier-1 inline (until the Python helper
scripts land) reads sibling SKILL.md files via the Read tool. If a
sibling file cannot be parsed, the affected check (coverage,
fidelity) emits `tool-degraded` INFO and continues; the help-skill
audit is downstream of sibling validity.

## Tier-2 — Judgment Dimensions

One LLM evaluation per file. All five dimensions run every time. A
dimension that doesn't apply returns PASS silently. Findings carry
WARN severity unless explicitly noted — judgment-level drift is
coaching, not blocking.

### D1 Workflow Curation

**Source principle:** *Curate workflow chains; do not auto-generate
them. List two or three chains the plugin's authors actually expect
callers to follow.*

**Judges:** Does `## Common workflows` contain at least one
*composed* chain (skill-a → skill-b → skill-c), not just a flat list
of skills? Are the chains specific to actual user tasks, or are they
abstract enumerations? Does each chain include a one-sentence "when
this chain applies" qualifier? A workflows section that is just a
re-listing of the skill table FAILs this dimension.

### D2 Triage Scaffolding

**Source principle:** *Triage scaffolding — task → skill mapping is
actionable.*

**Judges:** Can a caller with a specific task ("I want to fix a bug
in this codebase", "I want to plan a feature") read the help-skill
and unambiguously identify which sibling skill to invoke next? Or
does the help-skill list skills without scaffolding the choice
between them? A help-skill that names siblings without telling the
caller how to choose between them WARNs this dimension.

### D3 Dual Audience

**Source principle:** *Two audiences read it: a human typing
`/<plugin>:help` who wants a readable index, and an agent that has
matched the trigger and needs triage scaffolding.*

**Judges:** Does the document read cleanly for both audiences? A
help-skill written purely for an LLM (terse, abbreviated, optimized
for token cost) will fail the human-readability check; a help-skill
written purely for human reading (long-form, narrative, marketing-
flavored) will fail the agent-routing check. The pass criterion is
both — short, scannable, with the right amount of context to route
without requiring the reader to load adjacent files.

### D4 Scope Discipline

**Source principles:** *Pointers, not duplications.* *Architectural
prose in the help-skill body* (anti-pattern). *Keep the body short.*

**Judges:** Does the help-skill stay inside its scope (synopsis,
index, workflows, pointers) without spilling into AGENTS.md
territory (architectural prose, design philosophy, plugin-
composition rationale) or README territory (install instructions,
contributing guidelines, license text)? A help-skill that grows a
"Why this plugin exists" section or an "Installation" section WARNs
this dimension; the content belongs elsewhere.

### D5 Trigger Quality

**Source principle:** *Lead the description with the caller's
situation, not the skill's function.* *Trigger description must not
collide with sibling-skill triggers.*

**Judges:** Does the `description` frontmatter retrieve on
*meta-questions about the plugin* ("what's in this plugin", "list
skills", "how do I use it", "which skill fits") and not on *the
plugin's own workflows* (e.g., for the `build` plugin, not on "build
a skill" — that fires the actual sibling)? A description shaped like
"Use when the user wants to use the X plugin's features" is too
generic and competes with siblings. A description shaped like "Use
when the caller asks 'what's in the X plugin' or 'list X skills'" is
specific to the help-skill's role.

This dimension overlaps with Tier-3 cross-entity collision but is
distinct: Tier-2 judges the description in isolation (does it read
as a meta-trigger?), Tier-3 measures collision against actual
siblings.

## Tier-3 — Cross-Entity Trigger Collision

### trigger-collision

**Source principle:** *Trigger description must not collide with
sibling-skill triggers. The router cannot disambiguate two skills
that match the same trigger.*

**Severity:** WARN (INFO when only token-overlap heuristic fires;
WARN when identical trigger-phrase heuristic fires).

**Method.** For every sibling skill in the plugin, compare its
`description` against the help-skill's `description`. Two heuristics:

- **Token overlap.** Tokenize both descriptions; flag pairs whose
  shared trigger-phrase tokens (verbs + nouns from "Use when…"
  clauses) exceed a threshold. Severity: INFO if 3+ shared trigger
  tokens, WARN if 5+.
- **Identical trigger phrasing.** Flag pairs where both descriptions
  contain the same exact trigger phrase (e.g., both fire on "list
  skills"). Severity: WARN.

**Output.** For each collision, surface both descriptions and the
shared tokens. The user resolves by narrowing either side; the
auditor does not pick a winner automatically.

**Why this tier exists.** A help-skill in isolation can pass Tier-1
and Tier-2 cleanly while being fundamentally broken — when the
router is presented with the help-skill alongside its siblings, it
cannot pick correctly. This is the load-bearing check. Skipping
Tier-3 leaves the highest-value defect undetected.
