---
name: "Rule Type Taxonomy and Intent Section Quality for LLM Semantic Enforcement"
description: "A rule type taxonomy derived from mature linting ecosystems and LLM tool studies, plus structural signals that make Intent sections educationally effective rather than formally present."
type: research
sources:
  - https://arxiv.org/abs/2512.18925
  - https://eslint.org/docs/latest/extend/custom-rules
  - https://biomejs.dev/linter/
  - https://semgrep.dev/docs/semgrep-code/policies
  - https://semgrep.dev/docs/kb/rules/understand-severities
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
  - https://www.joshuakgoldberg.com/blog/if-i-wrote-a-linter-part-2-developer-experience/
  - https://7tonshark.com/posts/lint-rules-for-engineers/
  - https://rustc-dev-guide.rust-lang.org/diagnostics.html
  - https://github.com/eslint/eslint/discussions/16643
  - https://aicodingrules.com/blog/cursor-vs-claude-vs-copilot-rules
  - https://cursor.com/docs/context/rules
  - https://code.claude.com/docs/en/best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://gitnation.com/contents/road-to-zero-lint-failures-tackling-code-quality-challenges-at-scale
  - https://deepwiki.com/biomejs/biome/5.3-rule-groups-and-categories
related:
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/research/2026-04-07-rule-enforcement.research.md
---

# Rule Type Taxonomy and Intent Section Quality for LLM Semantic Enforcement

## Key Findings

Two findings with the most design leverage for the build-rule skill:

1. **Mature linting ecosystems converge on seven natural rule categories** organized by the nature of the harm they prevent: correctness (bug/error), suspicious (likely wrong), security, complexity, performance, style/convention, and accessibility. LLM rule tooling (Cursor, Claude Code, Copilot) adds a distinct eighth: **LLM behavioral directives** — instructions targeting AI response generation, not code correctness. This split matters structurally: traditional rule categories can be verified mechanically; LLM directives require semantic evaluation.

2. **Intent sections fail educationally in a predictable pattern**: they name *what* the rule catches but not *why the cost is real*, *who bears it*, or *what the valid exception is*. The three components that transform formal presence into educational effectiveness are: (a) naming the failure cost, not just the violation; (b) linking the rule to a principle the developer already accepts; (c) providing an explicit exception policy that legitimizes disabling over silencing.

---

## Background and Scope

This investigation serves two knowledge gaps for rebuilding the build-rule skill:

- **No taxonomy of rule types.** Without one, rule authors default to ad-hoc structure, and the skill cannot prompt for the right structural properties per type.
- **Thin guidance on Intent section quality.** The skill collects an Intent field but provides no criteria distinguishing educationally effective rationale from boilerplate.

The investigation covers: (A) how mature linting ecosystems and LLM tool research classify rules, and (B) what the linting community, compiler design literature, and developer-behavior research reveal about writing rule rationale that prevents workaround behavior.

---

## Search Protocol

| Query | Source | Date | Results |
|-------|--------|------|---------|
| ESLint rule categories problem suggestion layout classification taxonomy | Web | 2026-04-13 | 10 |
| Cursor rules Claude Code GitHub Copilot instructions taxonomy categories | Web | 2026-04-13 | 10 |
| Semgrep rule classification categories severity triage enforcement | Web | 2026-04-13 | 10 |
| OPA Open Policy Agent rule classification categories enforcement | Web | 2026-04-13 | 10 |
| Developer compliance linting rules workaround behavior eslint-disable | Web | 2026-04-13 | 10 |
| arxiv "cursor rules" empirical study taxonomy 2024 2025 | Web | 2026-04-13 | 4 |
| Biome linter rule categories correctness nursery suspicious design rationale | Web | 2026-04-13 | 10 |
| Writing effective lint rule messages documentation developer experience rationale | Web | 2026-04-13 | 10 |
| Linting rule education compliance research study developer behavior | Web | 2026-04-13 | 10 |
| Rust compiler error messages design educational diagnostic quality | Web | 2026-04-13 | 10 |
| ESLint rule documentation "when not to use" intent rationale structure | Web | 2026-04-13 | 10 |
| Policy as code rule intent rationale documentation writing quality | Web | 2026-04-13 | 10 |
| Static analysis rule documentation failure cost compliance | Web | 2026-04-13 | 10 |
| Cursor rules mdc frontmatter alwaysApply autoAttached agentRequested | Web | 2026-04-13 | 10 |
| Claude Code CLAUDE.md rule types categories semantic enforcement taxonomy | Web | 2026-04-13 | 10 |

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2512.18925 | Beyond the Prompt: An Empirical Study of Cursor Rules | Jiang & Nam (MSR 2026) | 2025/2026 | T1 | verified |
| 2 | https://eslint.org/docs/latest/extend/custom-rules | Custom Rules — ESLint | ESLint Project | 2024 | T1 | verified |
| 3 | https://biomejs.dev/linter/ | Linter — Biome | Biome Project | 2024 | T1 | verified |
| 4 | https://semgrep.dev/docs/semgrep-code/policies | Manage rules and policies — Semgrep | Semgrep | 2024 | T1 | verified |
| 5 | https://semgrep.dev/docs/kb/rules/understand-severities | Semgrep Severity Levels | Semgrep | 2024 | T1 | verified |
| 6 | https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0 | How to Make Linting Rules Work: From Enforcement to Education | Agoda Engineering | 2023 | T3 | verified |
| 7 | https://www.joshuakgoldberg.com/blog/if-i-wrote-a-linter-part-2-developer-experience/ | If I Wrote a Linter, Part 2: Developer Experience | Joshua Goldberg (typescript-eslint maintainer) | 2023 | T2 | verified |
| 8 | https://7tonshark.com/posts/lint-rules-for-engineers/ | Lint Rules Should Help Engineers, Not Just Programmers | 7tonshark | 2023 | T3 | verified |
| 9 | https://rustc-dev-guide.rust-lang.org/diagnostics.html | Errors and Lints — Rustc Development Guide | Rust Project | 2024 | T1 | verified |
| 10 | https://github.com/eslint/eslint/discussions/16643 | Standardize Rule Documentation | ESLint community | 2022 | T2 | verified |
| 11 | https://aicodingrules.com/blog/cursor-vs-claude-vs-copilot-rules | Cursor vs Claude vs Copilot Rules | AI Coding Rules | 2024 | T3 | verified |
| 12 | https://cursor.com/docs/context/rules | Rules — Cursor Docs | Cursor | 2024–2025 | T1 | verified |
| 13 | https://code.claude.com/docs/en/best-practices | Best Practices for Claude Code | Anthropic | 2025 | T1 | verified |
| 14 | https://www.humanlayer.dev/blog/writing-a-good-claude-md | Writing a Good CLAUDE.md | HumanLayer | 2025 | T3 | verified |
| 15 | https://gitnation.com/contents/road-to-zero-lint-failures-tackling-code-quality-challenges-at-scale | Road to Zero Lint Failures | LinkedIn/GitNation | 2023 | T2 | verified |
| 16 | https://deepwiki.com/biomejs/biome/5.3-rule-groups-and-categories | Biome Rule Groups and Categories | DeepWiki (Biome source) | 2024 | T2 | verified |

---

## Challenge

**Counter-evidence on taxonomy universality:** The Cursor rules empirical study [1] found that 37% of repositories include all five content categories. But the study also found that rules are "primarily based on developer intuition; their actual impact on LLM performance remains an open question." This undermines any taxonomy built from observed practice — observed categories may reflect developer habit rather than principled effectiveness.

**Counter-evidence on Intent section efficacy:** The HumanLayer research [14] found that frontier models can follow ~150–200 instructions with reasonable consistency but "instruction-following quality decreases uniformly" as instruction count increases. Educational quality of individual rules is bounded by total instruction budget. Rule quality and rule count are in tension.

**Counter-evidence on rule categorization and compliance:** No empirical study was found directly measuring whether rule categorization improves LLM compliance rates. The compliance benefits of categorization seen in human linting (Semgrep's Monitor → Comment → Block graduation, Biome's nursery system) are documented for human developers; transfer to LLMs is assumed, not demonstrated.

**Counter-evidence on educational rationale preventing workarounds:** The LinkedIn study [15] found that the primary driver of workaround behavior was not rationale absence but perceived fairness — when a codebase already contains thousands of existing failures, adding new rules feels punitive regardless of how well-explained they are. Rationale quality is necessary but not sufficient.

---

## Findings

### Part A: Rule Type Taxonomy

#### A1. What natural categories of semantic rules exist across LLM coding tools?

The empirical study of 401 Cursor rule repositories [1] identified five high-level content categories:

| Category | Repo Prevalence | What it contains |
|----------|----------------|-----------------|
| Project | 85% | Environment (stack, build commands), Functionality (architecture), Change (dependency updates) |
| Convention | 84% | Code Style (formatting, naming), Language/Framework patterns, Structure (directory organization) |
| Guideline | 89% | Quality Assurance, General Programming, Performance, Security, Communication, UI, Dependency |
| LLM Directive | 50% | Behavior (response generation), Workflow (multi-step processes), Persona, Formatting, Granularity |
| Example | 50% | Demonstrations of good/bad practices, templates |

**LLM Directive** is the category unique to AI tools — it targets AI response-generation behavior, not code semantics. Newer repositories (post-2024) include proportionally more LLM directives [1].

Cross-tool structural differences follow scope and enforcement point [11, 12, 13]:
- **Cursor**: IDE-first, file-scope, immediate — rules fire during editing sessions
- **Claude Code**: Project-scope, multi-file — rules guide architectural reasoning across sessions
- **Copilot**: Organizational-scope — team-wide conventions applied via GitHub workflows

#### A2. Do different rule types warrant different structural approaches?

Yes. The nature of harm determines the appropriate structure, consistent across all ecosystems studied.

**Binary vs. ordinal framing:**
- Correctness rules (code that *will* be wrong) → binary: violated or not. Deterministic issues have no useful gradation.
- Quality rules (code that *could* be better) → ordinal: warning first, error only after team consensus.
- This is consistent across ESLint (problem vs. suggestion vs. layout) [2], Biome (correctness → error by design; style → configurable) [3, 16], and Semgrep (severity × confidence matrix) [4, 5].

**Fix-safety defaults by type:**
- Machine-safe fix: correctness rules with deterministic corrections, layout/style rules
- User-guided fix: security and suspicious rules where the fix requires semantic judgment
- No auto-fix: LLM directives (behavioral, not code)

**Scope strategies:**
- Correctness, Security: enforce file-wide, no glob restriction
- Convention/Style: may warrant directory or file-type scoping
- LLM Directives (Cursor): application mode is a structural choice — Always Apply competes for attention budget; glob-scoped or Agent Requested loads on demand with higher effective weight per token [12]

#### A3. How do mature linting ecosystems classify rules, and what does classification enable?

**ESLint (problem / suggestion / layout)** [2]:
- `problem`: Code causing errors or confusing behavior. High-priority to resolve.
- `suggestion`: Code that could be better; no errors if unchanged.
- `layout`: Whitespace, semicolons, formatting. No semantic impact.
- Enables: CLI `--fix-type` filtering — teams auto-apply layout fixes while reviewing problem fixes manually.

**Biome (eight categories)** [3, 16]:
- `correctness`, `suspicious`, `security`, `complexity`, `performance`, `style`, `a11y`, `nursery`
- Enables: Category-level configuration, severity floors (`correctness`/`security`/`a11y` must be error-severity), experimental differentiation via `nursery`. Biome's `suspicious` category handles probabilistic rules — "likely wrong" is its own category distinct from "guaranteed wrong."
- `nursery`: experimental rules requiring explicit opt-in; graduate to stable categories after validation.

**Semgrep (severity × confidence matrix)** [4, 5]:
- Severity: Critical, High, Medium, Low (vulnerability criticality)
- Confidence: High, Medium, Low (pattern accuracy / false-positive likelihood)
- Enables: Progressive enforcement modes — Monitor (observation only), Comment (PR annotation), Block (CI failure). New rules start in Monitor; teams graduate them as accuracy is validated.

#### A4. Is there research on whether rule categorization improves compliance?

For human developers: indirect evidence exists. LinkedIn [15] found that per-team visibility into rule categories and failures enabled compliance improvement — but the mechanism was ownership and incentive alignment, not categorization per se.

For LLMs: no empirical evidence found. Jiang & Nam [1] explicitly state that rule effects on LLM performance "remain an open question." No study measured whether labeled rule types affect LLM adherence rates.

**Implication:** Categorization's compliance benefit for LLMs is an unvalidated assumption. Its value is authoring clarity and user communication, not proven LLM adherence improvement.

---

### Part B: Intent Section Quality

#### B1. What makes rule rationale educationally effective?

Three characteristics distinguish educational from formal rationale:

**1. Names the failure cost, not just the violation.**
Agoda [6]: "unhelpful errors like 'don't do this' promote compliance without understanding." Developers respond to cost, not category. Naming the consequence ("could lead to denial of service") is more effective than naming the vulnerability type ("buffer overflow").

**2. Links the rule to a principle the developer already accepts.**
7tonshark [8]: effective rationale connects to a principle — type safety, future maintainability, readability divergence — that the reader already values. Rules that enforce stylistic alternatives without naming the underlying principle are perceived as arbitrary.

**3. Includes an explicit exception policy.**
Goldberg [7]: the "When Not to Use" section is critical — it manages expectations by stating when a rule legitimately shouldn't apply. Without it, developers reach for blanket disable rather than legitimate exceptions.

#### B2. What prevents the "enforcement without education" failure mode?

Four characteristics prevent workaround behavior (`eslint-disable` comments, blanket rule disabling):

**Automated fix availability.** Agoda [6] and Goldberg [7]: auto-fixes change the developer's relationship to a rule — compliance requires less effort than bypass. Fixes must be machine-safe for this effect; unsafe auto-fixes cause more frustration than no fix.

**IDE-level surfacing before CI failure.** Agoda [6]: warnings surfaced "as close to the development process as possible" reduce disruption. A CI failure requires branch surgery; an IDE underline is corrected in place.

**Trial periods before enforcement.** Agoda [6]: rules introduced as warnings before errors prevent the shock response that triggers mass disabling. Semgrep's Monitor → Comment → Block graduation formalizes this [4].

**Rationale that names the failure cost.** LinkedIn [15]: developers disabled rules through rational cost-benefit analysis. When enforcement cost exceeds perceived value, bypass wins. Naming the consequence raises the perceived value side of that equation.

**What does NOT prevent workaround behavior on its own:** existing technical debt. LinkedIn [15]: when a codebase already contains thousands of failures, even well-explained rules feel punitive. Educational quality of Intent sections cannot overcome incentive structure created by existing violations.

#### B3. What does the linting community know about writing rule messages developers act on?

**ESLint standards** [2, 10]:
- Primary message: single sentence, stands alone in isolation (e.g., IDE tooltip without surrounding context).
- `docs.url` field: links from violation to full documentation; code editors surface this as a clickable link.
- Proposed documentation structure [10]: High-level overview → Rule Details (free-form why) → Options → Examples → Known Limitations → When Not to Use.

**Rust compiler diagnostic philosophy** [9]:
- Primary message: succinct but not terse to the point of obscurity.
- Help sub-diagnostic: what the developer *can* do. Separate from the error statement.
- Note sub-diagnostic: context and facts without prescriptive solutions.
- Applicability on suggestions: explicit confidence in the fix (machine-safe, has-placeholders, maybe-incorrect, unspecified).
- "The error or warning portion should *not* suggest how to fix the problem, only the 'help' sub-diagnostic should."

**Goldberg's linter DX principles** [7]:
- Messages describe the problem, not prescribe behavior ("This number literal will lose precision at runtime" vs. "Unexpected numeric literal").
- Three-layer messages: Primary (what's wrong) → Secondary (why it matters) → Suggestions (how to fix).
- Avoid "dogmatic or overly prescriptive" phrasing — this linguistic signal causes developers to distrust the rule.

#### B4. Structural signals of strong vs. weak Intent sections

**Strong Intent section — five required components:**
1. **Failure cost named** — specific, attributable consequence, not hedged ("causes runtime precision loss," not "might cause issues")
2. **Principle stated** — linked to a value the reader already holds (type safety, security, maintainability)
3. **Exception policy present** — at least one named condition under which the rule legitimately does not apply
4. **Scope of harm named** — who bears the cost (end user, future maintainer, security reviewer)
5. **Fix-safety signaled** — whether auto-fix is always safe or requires human review

**Weak Intent section — five failure signals:**
1. States only *what* the rule catches, not *why* it matters
2. Hedging language: "generally," "often," "might," "could" — signals low-confidence rules
3. No exception policy — trains developers to reach for blanket disable
4. Prohibition without consequence: "do not use `var`" without naming hoisting and TDZ problems
5. Rationale citing only the rule author's preference without principle grounding

**Worked example:**

Weak: *"Avoid using `console.log` in production code. It creates noise."*

Strong: *"`console.log` in production builds exposes internal state to end users via browser developer tools, and adds measurable latency in high-frequency call paths. Exception: `console.error` for critical runtime errors where structured logging is unavailable. Fix-safety: auto-remediable — removes statement without semantic change."*

---

## Takeaways

**For the build-rule skill — rule taxonomy:**

An eight-category taxonomy separating harm type from enforcement approach:

| Category | ESLint analog | Biome analog | Fix-safety default | Binary/Ordinal |
|----------|--------------|-------------|-------------------|----------------|
| Correctness | problem | correctness | auto-remediable | Binary |
| Suspicious | problem | suspicious | requires-review | Binary |
| Security | problem | security | requires-review | Binary |
| Complexity | suggestion | complexity | requires-review | Ordinal |
| Performance | suggestion | performance | requires-review | Ordinal |
| Convention/Style | layout + suggestion | style | auto-remediable | Ordinal |
| Accessibility | problem | a11y | requires-review | Binary |
| LLM Directive | n/a | n/a | n/a (behavioral) | Binary |

**For the build-rule skill — Intent section prompting:**

Require five structural components before publishing:
1. **Violation** — what pattern does the rule catch?
2. **Failure cost** — what goes wrong when the pattern occurs, and who bears it?
3. **Principle** — what underlying value does this rule enforce?
4. **Exception policy** — when is disabling legitimate? Name at least one case.
5. **Fix-safety** — is the auto-fix always safe, or does it require human review?

Rules that cannot answer (2) and (4) should not be published. They create enforcement pressure without the educational support that prevents workaround behavior.
