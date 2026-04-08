---
name: Effective Rules for LLM Enforcement
description: Research into what makes rules effective for LLM-based code enforcement — rule anatomy, evaluation consistency, pitfalls, and template design patterns
type: research
sources:
  - https://arxiv.org/html/2407.08440v1
  - https://www.techpolicy.press/using-llms-for-policy-driven-content-classification/
  - https://arxiv.org/abs/2603.01896
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://code.claude.com/docs/en/best-practices
  - https://arxiv.org/html/2503.23989v1
  - https://arxiv.org/abs/2411.15594
  - https://arxiv.org/abs/2412.12509
  - https://arxiv.org/html/2601.03444v1
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://eugeneyan.com/writing/llm-evaluators/
  - https://arxiv.org/html/2412.05579v2
  - https://arxiv.org/html/2601.08654
  - https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/
  - https://eslint.org/docs/latest/extend/custom-rules
  - https://semgrep.dev/docs/writing-rules/rule-syntax
  - https://docs.astral.sh/ruff/linter/
  - https://docs.getdbt.com/docs/build/data-tests
  - https://www.openpolicyagent.org/docs/latest/policy-language/
  - https://ast-grep.github.io/guide/project/lint-rule.html
  - https://cardinalops.com/blog/rethinking-false-positives-alert-fatigue/
  - https://www.coderabbit.ai/blog/why-developers-hate-linters
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
related:
  - docs/context/effective-rule-anatomy.context.md
  - docs/context/rule-system-pitfalls.context.md
  - docs/context/llm-rule-evaluation-reliability.context.md
---

## Key Takeaways

1. **Rules must be specific, scoped, and example-rich.** Context-specific rules improve evaluation reliability by 4x (Cohen's Kappa 0.156→0.646). Examples are the single highest-leverage addition. Generic rules fail.
2. **Binary pass/fail with chain-of-thought reasoning.** Binary evaluation is more reliable than graded scales. Requiring reasoning before the verdict improves consistency by 10-15 percentage points.
3. **One rule, one file, one verdict.** Evaluate dimensions independently. Loading all rules into a single prompt degrades all of them (150-200 instruction limit). Scope-based matching is essential.
4. **False positives kill rule systems.** Trust is the currency. Default to `warn`, keep active rule counts low per file, and ensure rules fire only on relevant files.
5. **Intent sections prevent bypass.** Enforcement without education causes developers to disable rules. Every rule needs a "why."
6. **Template libraries should start small and conservative.** Ship a curated, high-confidence set. Let users expand. Copy-into-project enables full customization.
7. **LLM-based enforcement complements, not replaces, deterministic linting.** CLAUDE.md instructions are advisory. Use hooks for deterministic checks, LLM evaluation for semantic understanding.
8. **The rule file IS the locked rubric.** Include the full rule verbatim in the evaluation prompt — never summarize. This prevents interpretation drift across evaluations.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | arxiv.org/html/2407.08440v1 | Beyond Instruction Following: Evaluating Rule Following of LLMs | Sun et al. | 2024-07 | T1 | verified |
| 2 | techpolicy.press | Using LLMs for Policy-Driven Content Classification | Willner & Chakrabarti (Stanford) | 2024-01 | T2 | verified |
| 3 | arxiv.org/abs/2603.01896 | Agentic Code Reasoning (Semi-Formal Reasoning) | Ugare & Chandra (Meta) | 2026-03 | T1 | verified |
| 4 | humanlayer.dev | Writing a Good CLAUDE.md | Kyle (HumanLayer) | 2025-11 | T3 | verified |
| 5 | arize.com | CLAUDE.md Best Practices from Prompt Learning | Jindal (Arize) | 2025-11 | T3 | verified |
| 6 | platform.claude.com | Prompting Best Practices | Anthropic | 2025-2026 | T1 | verified |
| 7 | code.claude.com | Best Practices for Claude Code | Anthropic | 2025-2026 | T1 | verified |
| 8 | arxiv.org/html/2503.23989v1 | Rubric Is All You Need | Pathak et al. (BITS Pilani) | 2025 | T1 | verified |
| 9 | arxiv.org/abs/2411.15594 | A Survey on LLM-as-a-Judge | Gu et al. | 2024-11 | T1 | verified |
| 10 | arxiv.org/abs/2412.12509 | Can You Trust LLM Judgments? Reliability of LLM-as-a-Judge | Schroeder & Wood-Doughty | 2024-12 | T1 | verified |
| 11 | arxiv.org/html/2601.03444v1 | Grading Scale Impact on LLM-as-a-Judge | Li et al. (Harvard, CMU, Stanford) | 2025-01 | T1 | verified |
| 12 | anthropic.com/engineering | Demystifying Evals for AI Agents | Grace et al. (Anthropic) | 2026-01 | T1 | verified |
| 13 | eugeneyan.com | Evaluating the Effectiveness of LLM-Evaluators | Eugene Yan | 2024-08 | T2 | verified |
| 14 | arxiv.org/html/2412.05579v2 | LLMs-as-Judges: Comprehensive Survey | Li et al. | 2024-12 | T1 | verified |
| 15 | arxiv.org/html/2601.08654 | Rulers: Locked Rubrics and Evidence-Anchored Scoring | Hong et al. (WashU, ASU, FSU) | 2026-01 | T1 | verified |
| 16 | confident-ai.com | LLM-as-a-Judge: Complete Guide | Confident AI | 2024-2025 | T3 | verified |
| 17 | evidentlyai.com | LLM-as-a-Judge Guide | Evidently AI | 2024-2025 | T3 | verified |
| 18 | promptfoo.dev | LLM Rubric Documentation | Promptfoo | 2024-2025 | T2 | verified |
| 19 | eslint.org | Custom Rules - ESLint | OpenJS Foundation | current | T1 | verified |
| 20 | semgrep.dev | Rule Structure Syntax | Semgrep Inc. | current | T1 | verified |
| 21 | docs.astral.sh | The Ruff Linter | Astral | current | T1 | verified |
| 22 | docs.getdbt.com | Data Tests | dbt Labs | current | T1 | verified |
| 23 | openpolicyagent.org | Policy Language | CNCF/Styra | current | T1 | verified |
| 24 | ast-grep.github.io | Lint Rule | ast-grep project | current | T2 | verified |
| 25 | cardinalops.com | Rethinking False Positives and Alert Fatigue | CardinalOps | undated | T3 | verified |
| 26 | coderabbit.ai | Why Developers Hate Linters | CodeRabbit | 2024 | T3 | verified |
| 27 | medium.com/agoda-engineering | How to Make Linting Rules Work | Agoda Engineering | 2024 | T3 | verified (403) |

## Findings

### 1. What structural characteristics make rules effective for LLM enforcement?

**Natural language rules dramatically outperform formal logic.** Sun et al. [1] found that LLMs handle natural language rules far better than first-order logic equivalents. This validates the design choice of markdown-based rule files over formal specifications. However, LLM failures decompose into two distinct types: **Triggering Errors** (selecting the wrong rule for a context) and **Execution Errors** (correct rule, wrong conclusion). Scope precision directly addresses triggering errors by reducing the number of irrelevant rules an LLM must filter through (HIGH — T1, directly measured).

**Context-specific rules massively outperform generic ones.** Pathak et al. [8] measured Cohen's Kappa jumping from 0.156 to 0.646 when switching from generic to context-specific rubrics for code evaluation. Jindal [5] found repository-specific rules achieved up to 10.87% accuracy improvement vs. 5.19% for generic rules. Both findings converge: rules scoped to specific file types, code patterns, and architectural layers will produce far more reliable judgments than broad, generic rules (HIGH — T1 + T3 convergence).

**Examples are the single highest-leverage addition to a rule.** Anthropic's prompting best practices [6] document that 3-5 few-shot examples "dramatically improve classification accuracy." Willner & Chakrabarti [2] found that defining both inclusions AND exclusions with examples (placing exclusions first) significantly reduces misclassification. The pattern is consistent: compliant and non-compliant examples serve as concrete anchors that disambiguate intent far more effectively than additional prose (HIGH — T1 + T2 convergence).

**Structured evaluation templates improve accuracy over free-form judgment.** Ugare & Chandra [3] found that requiring explicit premises and formal conclusions boosted code review accuracy from 78% to 88% on curated examples and 93% on real-world patches. This suggests the check-rules skill should provide structured evaluation prompts, not just "does this file comply with this rule?" (HIGH — T1).

**Rule count has hard limits.** Kyle [4] documents that frontier LLMs reliably follow approximately 150-200 instructions, with performance declining uniformly as count increases. Claude Code's system prompt already consumes ~50 instruction slots. Anthropic [7] confirms: "if Claude keeps doing something wrong despite a rule, the file is probably too long." This means the rule system must avoid loading all rules into a single prompt — the scope-based matching design is essential, not optional (HIGH — T1 + T3 convergence).

**Markdown formatting matters for LLM rule processing.** Willner & Chakrabarti [2] found policy documents not using markdown yield worse results. Anthropic [6] recommends XML tags for unambiguous structure. Combined with the rule count limit, this implies each rule should be a self-contained, well-formatted markdown document evaluated individually (MODERATE — T2, single source but practitioner-validated).

### 2. How do existing rule systems structure their rule definitions?

**Universal rule anatomy across all systems.** Every system examined (ESLint, Semgrep, Ruff, Spectral, dbt, OPA, ast-grep, SQLFluff, Biome) shares the same core fields: identifier, description/message, severity, and a targeting mechanism [19-24]. This convergence is strong evidence that the proposed rule format (name, description, scope, severity) captures the essential structure (HIGH — 9 independent systems converge).

**Scoping mechanisms fall into two categories.** File-path globs (Semgrep `paths.include/exclude`, Ruff `per-file-ignores`, ast-grep `files/ignores`) and structural targeting (ESLint AST visitors, Spectral JSONPath, OPA input schemas). For LLM-based evaluation, file-path globs are the natural fit — structural targeting requires AST parsing that the LLM evaluation approach deliberately avoids (HIGH — pattern across all systems).

**Severity taxonomies cluster around 2-3 effective levels.** Despite systems offering 3-5 levels (ESLint: off/warn/error; Semgrep: LOW/MEDIUM/HIGH/CRITICAL; Spectral: error/warn/info/hint/off), practical usage collapses to binary: things that block and things that advise. dbt uses exactly two levels: `warn` and `error`. The proposed `fail`/`warn` binary is well-supported (HIGH — convergent across systems and confirmed by practitioner behavior).

**Custom rules use the same format as built-in rules.** ESLint, Semgrep, Spectral, ast-grep, and OPA all use identical formats for user-authored and built-in rules [19-24]. This is the dominant pattern. Ruff and Biome are exceptions, requiring Rust code, but they are compile-time systems with different constraints. For a template-based system, identical format between templates and custom rules is the clear standard (HIGH — 5/7 systems converge).

**Message quality varies widely.** Semgrep requires rules to explain "why the pattern matched and how to remediate." ESLint supports template variables in messages (`{{placeholder}}`). ast-grep separates `message` (concise) from `note` (detailed actionable advice). The best rule systems distinguish between the violation statement and the remediation guidance (MODERATE — pattern visible but not universal).

**Rule organization uses flat categories, not deep hierarchies.** Biome uses 8 groups (a11y, complexity, correctness, performance, security, style, suspicious, nursery). Ruff uses prefix codes (F for Pyflakes, E for pycodestyle). Semgrep uses namespace paths. None use deep hierarchies — one level of categorization is the pattern (HIGH — universal across systems).

### 3. What pitfalls and failure modes emerge in rule-based systems?

**False positives erode trust faster than false negatives.** CardinalOps [25] documents organizations with false positive rates exceeding 95%. Lebrero documents how "one flaky test at a time" leads to entire test suites being abandoned. Maxham cites a mining company whose monitoring generated thousands of false positives until alerts meant "this can be ignored." The pattern is consistent: trust is the currency of enforcement systems, and false positives spend it rapidly (HIGH — multiple independent practitioner reports converge).

**Alert fatigue is the primary killer of rule systems.** CodeRabbit [26] identifies "warning fatigue from excessive non-critical alerts" as the top developer complaint. Agoda Engineering [27] documents a team that received 140 code review comments on a 500-line PR, 80% style-related. The OODA loop breaks: when every file triggers warnings, developers disable the system rather than fix violations. The implication for our system: severity defaults should be conservative (`warn`), and the number of rules active on any file should be small (HIGH — T3, multiple independent sources).

**Enforcement without education backfires.** Agoda Engineering [27] found that enforcement-first strategies cause developers to bypass rules with disable comments rather than understanding the intent. "If the team doesn't believe in the linting rules, they won't follow them, at least not in the spirit they were intended." This validates the rule format requiring an Intent section — understanding *why* a rule exists is prerequisite to accepting enforcement (HIGH — T3, directly measured).

**Legacy code creates an adoption barrier.** Marinacci documents teams avoiding new rules because applying them to existing code would "swamp with a backlog of issues." The "Hold the Line" principle — only checking changed files, not the full codebase — is widely recommended. The hook-based enforcement design (checking only changed files) naturally addresses this (MODERATE — T3, single source but widely cited principle).

**Rule conflicts compound as rule count grows.** Secoda documents how "multiple rules applying simultaneously produce inconsistent or incorrect outcomes." Maintenance burden compounds: performance degrades, verification across hundreds of rules becomes untenable, updates create unforeseen conflicts. This reinforces the scope-based isolation model: each rule evaluated independently against matching files, with no cross-rule interaction (MODERATE — T3, single source but consistent with system design literature).

**Developers perceive rigid rules as micromanagement.** CodeRabbit [26] identifies rules as undermining "trust, respect, and autonomy." The counterpoint from Agoda [27]: consensus-building before enforcement, warning-before-failure rollout, and trial periods. For the extract-rules skill, this suggests user confirmation before writing and `warn` as default severity (MODERATE — T3, sentiment data).

### 4. What level of rule granularity produces consistent LLM evaluation?

**Binary evaluation is more reliable than graded scales.** Evidently AI [17] and Confident AI [16] both recommend binary pass/fail over numeric scales. Schroeder & Wood-Doughty [10] found single-shot evaluation unreliable — multiple sampling improves dependability. Li et al. [11] found the 0-5 scale produced strongest human-LLM agreement, but binary outperforms all scales for objective tasks. For code rule enforcement, where compliance is typically binary (compliant or not), pass/fail is the right evaluation mode (HIGH — T1 + T3 convergence).

**One rule, one file, one verdict.** Anthropic [12] advises grading "individual dimensions separately with separate LLM judges rather than assessing everything simultaneously." Li et al. [14] found transformations between evaluation modes unreliable. The proposed design of independent rule×file evaluation aligns with this: each evaluation is a single binary judgment on a single dimension (HIGH — T1, directly recommended by Anthropic).

**Chain-of-thought before verdict improves consistency.** Confident AI [16] found few-shot prompting increased GPT-4's consistency from 65.0% to 77.5%. The G-Eval framework [16] (generating evaluation steps before scoring) demonstrates superior performance. Ugare & Chandra [3] found structured reasoning boosted accuracy by 10-15 percentage points. The check-rules evaluation prompt should require reasoning before the pass/fail verdict (HIGH — T1 + T3 convergence).

**Locked rubrics eliminate interpretation drift.** Hong et al. [15] reframed LLM evaluation as a "criteria transfer problem" — compiling criteria into immutable specifications prevents the LLM from reinterpreting rules across evaluations. Achieved QWK of 0.7276 vs. 0.5566 baseline. For rule enforcement, the rule file itself serves as the locked rubric — the evaluation prompt should include the full rule verbatim, not a summary (HIGH — T1).

**Ambiguous rules produce measurement noise.** Anthropic [12] states "a good task is one where two domain experts would independently reach the same pass/fail verdict." Eugene Yan [13] found even GPT-4 achieved Cohen's kappa of only 0.84, significantly below human-human agreement of 0.97. The gap is largest for ambiguous criteria. Rules must be specific enough that two humans would agree on compliance (HIGH — T1 + T2 convergence).

### 5. Best practices for rule templates and rule libraries

**Start conservative, expand methodically.** Ruff defaults to only Pyflakes (`F`) and a subset of pycodestyle (`E`), omitting stylistic rules [21]. ESLint's `recommended` config is a curated subset. Elementary Data [dbt] recommends leveraging existing packages before writing custom tests. The template library should ship with a small, high-confidence set and let users expand (HIGH — convergent across ecosystems).

**Layered composition enables customization without forking.** ESLint's shareable configs use `extends` for layered overrides — "later objects overriding previous objects when there is a conflict" [19]. PMD's category references auto-inherit new rules as the system evolves. Templates should be copyable into the user's `docs/rules/` for full customization, with no runtime dependency on the original (HIGH — T1, dominant pattern).

**Test every template rule with positive and negative cases.** Semgrep requires every contributed rule to include at least one true positive (`// ruleid:`) and one true negative (`// ok:`) test case [20]. This directly maps to the rule format's compliant/non-compliant examples — they serve double duty as both documentation and testable expectations (HIGH — T1, enforced by Semgrep's contribution process).

**Organize by concern, not by language or technology.** The proposed categories (naming, layer boundaries, tests, documentation, code organization) align with how developers think about conventions. Biome's 8 groups (correctness, complexity, style, security, etc.) and Ruff's prefix system both organize semantically. Flat categorization (one level) is the universal pattern (HIGH — convergent).

**Convention over configuration — but document the conventions.** Miller [MSDN] notes convention-over-configuration "can be a near disaster if developers aren't familiar with the existing conventions." Templates must be self-documenting: the Intent section explains why, the examples show what compliance looks like, and the scope makes applicability explicit (MODERATE — T2, single source but a well-established principle).

## Challenge

### Potential weaknesses in findings

**Cost at scale is under-examined.** The research validates the one-rule-one-file-one-verdict model for accuracy, but every evaluation is an LLM call. A project with 20 rules and a 10-file changeset produces 200 evaluations (before scope filtering). The research doesn't address whether scope filtering alone provides sufficient throttling, or whether rule batching (multiple rules per call) is viable despite the "grade dimensions separately" guidance.

**Binary evaluation may miss graduated compliance.** The findings strongly favor pass/fail, but some rules have degrees of violation. A staging model with one line of business logic is different from one that's entirely business logic. The research suggests binary is more reliable, but doesn't address whether the explanation field in the output format adequately captures these nuances.

**Template adoption friction is not well-studied.** The research covers how existing systems distribute rules (npm packages, registries, dbt packages), but the proposed copy-into-project model is different from any of these. No evidence was found on whether copy-and-customize is more or less effective than reference-and-override for rule adoption.

**LLM-as-judge research is mostly on text evaluation, not code.** Most LLM-as-judge studies evaluate text quality, summarization, or content moderation. The code-specific evidence (Ugare & Chandra [3], Pathak et al. [8]) is limited to two papers. Transferability of findings from text evaluation to code rule enforcement is assumed but not directly validated.

### Counter-evidence

**Hooks as advisory, not deterministic.** Anthropic [7] explicitly states CLAUDE.md instructions are "advisory, not guaranteed" and recommends hooks for deterministic enforcement. This creates a tension: the LLM-based check provides semantic understanding (its advantage) but cannot guarantee enforcement (its limitation). Traditional linters offer the inverse tradeoff. The system should be positioned as complementary to, not a replacement for, deterministic linting.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Natural language rules outperform formal logic for LLM evaluation | finding | [1] | verified |
| 2 | Context-specific rubrics improve Cohen's Kappa from 0.156 to 0.646 | statistic | [8] | verified |
| 3 | Repository-specific rules achieve up to 10.87% accuracy improvement | statistic | [5] | verified |
| 4 | 3-5 few-shot examples dramatically improve classification accuracy | finding | [6] | verified |
| 5 | Structured reasoning boosts code review accuracy from 78% to 88% | statistic | [3] | verified |
| 6 | Frontier LLMs reliably follow ~150-200 instructions | statistic | [4] | human-review |
| 7 | Organizations experience false positive rates exceeding 95% | statistic | [25] | verified |
| 8 | Few-shot prompting increased GPT-4 consistency from 65% to 77.5% | statistic | [16] | verified |
| 9 | Locked rubrics achieved QWK of 0.7276 vs. 0.5566 baseline | statistic | [15] | verified |
| 10 | GPT-4 achieves Cohen's kappa of 0.84 vs. human-human 0.97 | statistic | [13] | verified |

## Search Protocol

### Queries executed
1. "LLM rule following evaluation" — found [1]
2. "LLM content classification policy rules" — found [2]
3. "LLM code review structured reasoning" — found [3]
4. "CLAUDE.md best practices effective rules" — found [4], [5]
5. "Claude prompting best practices examples" — found [6], [7]
6. "LLM rubric code evaluation" — found [8]
7. "LLM as judge survey reliability" — found [9], [10], [11]
8. "AI agent evaluation best practices" — found [12]
9. "LLM evaluator effectiveness" — found [13], [14]
10. "LLM rubric locked scoring" — found [15]
11. "LLM judge guide binary evaluation" — found [16], [17]
12. "promptfoo LLM rubric" — found [18]
13. "ESLint custom rule structure" — found [19]
14. "Semgrep rule syntax YAML" — found [20]
15. "Ruff linter rule configuration" — found [21]
16. "dbt data tests generic custom" — found [22]
17. "OPA Rego policy language" — found [23]
18. "ast-grep lint rule YAML" — found [24]
19. "alert fatigue false positive rule systems" — found [25]
20. "developers hate linters why" — found [26], [27]
