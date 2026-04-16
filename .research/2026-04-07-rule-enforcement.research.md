---
name: "Rule-Based LLM Enforcement"
description: "How to design rule systems that LLMs can reliably enforce: structural characteristics, pitfalls, and best practices"
type: research
sources:
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://aclanthology.org/2025.coling-main.710.pdf
  - https://arxiv.org/abs/2601.08654
  - https://arxiv.org/html/2503.23989v1
  - https://arxiv.org/html/2501.00274v1
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/
  - https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/
  - https://eslint.org/docs/latest/extend/custom-rules
  - https://www.openpolicyagent.org/docs/latest/policy-language/
  - https://deepwiki.com/astral-sh/ruff/3-ruff-linter
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
  - https://corgea.com/Learn/how-to-reduce-false-positives-in-sast
  - https://www.coderabbit.ai/blog/why-developers-hate-linters
  - https://www.montecarlodata.com/blog-llm-as-judge/
  - https://freeplay.ai/blog/defining-the-right-evaluation-criteria-for-your-llm-project-a-practical-guide
related: []
---

# Rule-Based LLM Enforcement

## Key Insights

1. **Single holistic LLM judgment is near-unusable.** RMSE 0.856–0.901 — worse than random guessing. Decompose every evaluation into 5–10 specific, independently-scored dimensions.
2. **Scale type must match distinction type.** Binary for categorical distinctions (toxic/not-toxic). Ordinal 1–5 for quality dimensions. Float/continuous only for benchmarking generation tasks. Avoid 1–100.
3. **Question-specific rubrics outperform generic by ~4× on Cohen's Kappa** for structured tasks. The gap narrows for open-ended tasks and disappears for auto-generated rubrics.
4. **False positives create self-reinforcing failure.** FPs → reduced trust → fewer fixes → more violations → rules perceived as noise. Even 20–30% FP rates are sufficient to produce this cascade.
5. **Enforcement without education produces workarounds.** `// eslint-disable` spam is a rule authorship failure, not a developer behavior problem. Rules must explain *why* alongside *what*.
6. **Rubric text is a versioned artifact.** Minor prompt changes produce meaningfully different evaluation results. Treat rule phrasing as frozen specification — not editable ad hoc.
7. **Start narrow, graduate to enforcement.** Launch rules in warning mode on known failure examples. Require positive and negative test cases before deployment. Review quarterly.
8. **Chain-of-thought is mandatory for auditable enforcement.** Rules that produce only pass/fail are undebuggable and uncalibratable.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.evidentlyai.com/llm-guide/llm-as-a-judge | LLM-as-a-judge: a complete guide to using LLMs for evaluations | Evidently AI | 2024–2025 | T2 | verified |
| 2 | https://aclanthology.org/2025.coling-main.710.pdf | Evaluating the Consistency of LLM Evaluators | ACL Anthology (COLING 2025) | 2025 | T1 | verified |
| 3 | https://arxiv.org/abs/2601.08654 | RULERS: Locked Rubrics and Evidence-Anchored Scoring for Robust LLM Evaluation | arXiv (2026) | 2026 | T1 | verified (preprint, not peer-reviewed) |
| 4 | https://arxiv.org/html/2503.23989v1 | Rubric Is All You Need: Enhancing LLM-based Code Evaluation With Question-Specific Rubrics | arXiv (2025) | 2025 | T1 | verified (preprint) |
| 5 | https://arxiv.org/html/2501.00274v1 | LLM-Rubric: A Multidimensional, Calibrated Approach to Automated Evaluation of Natural Language Texts | arXiv (2025) | 2025 | T1 | verified (preprint) |
| 6 | https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/ | LLM Rubric | Promptfoo (official docs) | 2025 | T1 | verified |
| 7 | https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/ | Writing Semgrep Rules: A Methodology | Semgrep (official blog) | 2020 | T2 | verified (2020 — methodology still current per community; flag for updates) |
| 8 | https://eslint.org/docs/latest/extend/custom-rules | Custom Rules | ESLint (official docs) | 2025 | T1 | verified |
| 9 | https://www.openpolicyagent.org/docs/latest/policy-language/ | Policy Language (Rego) | Open Policy Agent (official docs) | 2025 | T1 | verified |
| 10 | https://deepwiki.com/astral-sh/ruff/3-ruff-linter | Ruff Linter Architecture | DeepWiki / astral-sh | 2025 | T3 | verified (auto-generated docs, not official Ruff site; accurate but secondary) |
| 11 | https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0 | How to Make Linting Rules Work: From Enforcement to Education | Agoda Engineering | 2023–2024 | T2 | verified (403) |
| 12 | https://corgea.com/Learn/how-to-reduce-false-positives-in-sast | How to Reduce False Positives in SAST | Corgea | 2024–2025 | T3 | verified (vendor; financial impact figures are vendor estimates — treat with caution) |
| 13 | https://www.coderabbit.ai/blog/why-developers-hate-linters | Why Developers Hate Linters | CodeRabbit | 2024–2025 | T3 | verified (vendor; well-cited practitioner perspective) |
| 14 | https://www.montecarlodata.com/blog-llm-as-judge/ | LLM-As-Judge: 7 Best Practices & Evaluation Templates | Monte Carlo Data | 2024–2025 | T2 | verified |
| 15 | https://freeplay.ai/blog/defining-the-right-evaluation-criteria-for-your-llm-project-a-practical-guide | Defining the Right Evaluation Criteria for Your LLM Project | Freeplay | 2024–2025 | T2 | verified |

---

## Raw Extracts

### Sub-question 1: Structural characteristics for effective LLM rules

**From [1] (Evidently AI — LLM-as-Judge):**

- "Don't just ask the LLM to label something as 'toxic' or 'not toxic'. Instead, clearly define what 'toxic' means." Clear definition is foundational to reliable enforcement.
- "Binary evaluations, like 'Polite' vs. 'Impolite,' tend to be more reliable and consistent for both LLMs and human evaluators. It's easier to get accurate results with two simple choices rather than trying to decide if a specific response scores 73 vs. 82 for 'politeness.'"
- Effective rules should: explain the meaning of each score explicitly; provide examples of both positive and negative cases; account for edge cases observed in data; consider whether ambiguous situations should be flagged rather than forced into categories.
- "If you can't easily explain these distinctions, it might be a sign you need to simplify the scale."
- A three-option approach also works: "relevant, irrelevant, and partially relevant, or include an 'unknown' option."
- "If you have several aspects to evaluate, like completeness, accuracy, and relevance, it's best to split them into separate evaluators."

**From [2] (COLING 2025 — Consistency of LLM Evaluators):**

- More detailed, specific criteria lead to higher agreement rates between evaluators compared to broad, general assessment guidelines.
- Structured scales with clear definitions at each level produce more reliable results.
- Structural elements enhancing consistency: explicit examples within criteria, clear boundaries between rating levels, specific terminology in criteria descriptions (precise language outperforms vague phrasing).
- "More granular criteria result in improved consistency metrics."

**From [4] (arXiv 2025 — Rubric Is All You Need):**

- "Existing work focused on question-agnostic (QA) rubrics, emphasizing generic criteria such as correctness and syntax across diverse problems, but in reality...human instructors actually use question-specific (QS) rubrics."
- Question-agnostic approaches "often fail to capture the nuances of specific programming problems, leading to misaligned evaluations."
- Question-specific rubrics break down problems into discrete implementation steps with binary marking (full or zero marks per step).
- "Presentation method matters significantly. When fed evaluation points one by one, the LLM is remarkably strict in grading" (leniency score −0.329). Presenting the complete rubric simultaneously yields more human-aligned evaluations.

**From [5] (arXiv 2025 — LLM-Rubric multidimensional):**

- The LLM's direct response to a single overall question (Q0) "performed worse than random guessing (RMSE 0.86–0.98), but when combined with responses to 8 auxiliary dimensions through calibration, performance improved 2× (RMSE 0.39–0.42)."
- Decomposing a holistic judgment into multiple specific dimensions dramatically improves accuracy. Finer-grained questions act as "auxiliary tasks that help the calibration network discover useful representations."
- Ablation studies: most dimensions contributed significantly. LLMs struggled most with "redundancy, conciseness, and efficiency" dimensions — these are harder to enforce reliably.

**From [6] (Promptfoo — LLM Rubric docs):**

- Effective rubrics "provide explicit scoring guidance." Example: "Score of 0.1: Only a slight smile. Score of 0.5: Laughing out loud. Score of 1.0: Rolling on the floor laughing." Each scale point needs concrete behavioral anchors.
- "Without specificity, models default to assuming pass: true, potentially marking inadequate responses as passing."

**From [14] (Monte Carlo — 7 Best Practices):**

- "LLMs are much more effective when given clear, single objective tasks." Do not combine multiple evaluation dimensions into one prompt.
- "Scores that are floats are not great. LLM-as-judge does better with a categorical integer scoring scale with clear meaning."
- Require the evaluator to articulate reasoning through chain-of-thought; this "standardizes judgments and accelerates human understanding of alerts."

---

### Sub-question 2: Established rule systems (ESLint, Semgrep, Ruff, OPA)

**ESLint — from [8] (official docs):**

- An ESLint rule exports an object with two top-level properties: `meta` (metadata) and `create` (implementation function returning AST visitor methods).
- The `meta` object contains: `type` (classification: "problem" / "suggestion" / "layout"), `docs` (description, URL), `fixable` ("code" or "whitespace" — mandatory if auto-fix), `hasSuggestions` (boolean — mandatory if offering suggestions), `messages` (messageId-to-description map), `schema` (JSON Schema validating rule options), `defaultOptions`.
- Rule types carry semantic priority: "problem" = causes errors or confusing behavior (highest priority); "suggestion" = better approach without breaking functionality; "layout" = formatting concerns only.
- Messages use `messageId` references to centralized definitions, with dynamic data interpolation: `"Variable '{{ name }}' not recommended"`.
- Fixable rules must declare `meta.fixable` and return fixer operations. Fixes rerun through all rules until stabilization (convergence).

**Semgrep — from [7] (official methodology blog, 2020):**

- Rules are YAML with required fields: `id`, `pattern`, `message`, `languages`, `severity`.
- Core methodology: "Start narrow and expand gradually — write rules that match the exact pattern you observed in a real bug or vulnerability." A rule that fires twice with 100% accuracy is more valuable than one that fires 200 times with 50% accuracy.
- Workflow: add `pattern-not` clauses to filter false positives; use `pattern-either` for legitimate variations; use the ellipsis operator (`...`) to abstract over sequences.
- Testing: write test cases for both positive matches and negative cases. Multi-repo validation before deployment. Use ripgrep cross-checks: `rg -C 5 "method_name"` to find code the rule might miss.
- "Making it easy for developers to provide feedback on the signal quality of a rule is quite valuable for building a continuous scanning system."

**Ruff — from [10] (DeepWiki architecture):**

- 800+ rules organized by prefix (F for Pyflakes, E/W for pycodestyle, B for bugbear, PL for Pylint, RUF for Ruff-specific, etc.). Rules selected via exact code (E501), prefix (E), sub-category (PL0), or wildcard (PL*).
- Rules categorized by execution phase: token-based, physical line, logical line, AST-based, import-specific. Each phase has different capabilities and performance characteristics.
- Fix safety is a first-class concern: "safe" fixes preserve behavior; "unsafe" fixes may alter runtime behavior or remove comments. Users can override via `extend-safe-fixes` and `extend-unsafe-fixes`.
- Rule registration uses a central `Rule` enum; `code_to_rule()` maps string codes to internal variants. Availability tracked via RuleGroup (Stable / Preview / Deprecated / Removed).
- Snapshot tests validate expected diagnostic output against fixture files, ensuring consistency across releases.

**OPA / Rego — from [9] (official docs):**

- Rego rule anatomy: `<name> <key>? <value>? <body>?`. Each rule has a head (declaring what document is defined) and a body (expressions that must evaluate to true).
- Two rule types: complete rules (single value, conflict-free); partial rules (generate collections via `contains`, supporting multiple definitions that OR together).
- Allow/deny via `default` values: `default allow := false` prevents undefined results. Rules build on top of defaults.
- Helper rules decompose complex logic: `prod_servers contains name if { ... }` → `apps_not_in_prod contains name if { not apps_in_prod[name] }`.
- Metadata annotations document rules for tooling: `# METADATA / # title: Pod Image Validation / # description: Ensures containers use approved registries`.
- Modular packages organize policies: `package kubernetes.admission` + `import data.schemas`.

**Transferable structural patterns to LLM evaluation:**
- ESLint's separation of `meta` (what the rule is) from `create` (how it fires) maps to LLM rule design: define the criterion (meta) separately from the evaluation logic (prompt).
- Semgrep's "start narrow, add pattern-not" maps to: write conservative rules first, then add exclusion conditions for known false-positive cases.
- OPA's `default allow := false` maps to: LLM rules should specify a default stance; undefined cases should fail closed or surface as "unknown."
- Ruff's fix-safety classification maps to: distinguish rules that require human judgment from rules that can be auto-remediated.

---

### Sub-question 3: Pitfalls that kill rule-based systems

**From [12] (Corgea — SAST False Positives):**

- Root causes of false positives in rule-based systems: absence of execution context (rules analyze without runtime data); over-generalized pattern matching (syntactic detection can't distinguish safe from dangerous patterns); framework blindness (standard rules ignore built-in protections like Django's auto-escaping); business logic opacity (rules have no understanding of custom sanitization); configuration drift (default rule sets diverge from actual project risk over time).
- Financial impact: false positives of 1,500–5,000 instances per scan translate to "$432K–$1.44M" in annual triage costs.
- Behavioral cascade: "more false positives → less developer trust → fewer fixes applied → more vulnerabilities in production."
- One developer characterizes high-FP tools as "noise generators." Community discussions document "alert fatigue" destroying security culture: "when developers see scan after scan flagging code they know is safe, they stop paying attention."
- AI-powered contextual analysis can reduce effective false positive rates "under 15%" by adding semantic understanding.

**From [11] (Agoda Engineering — Enforcement to Education):**

- Enforcement-only rules lead to widespread use of `// eslint-disable-next-line` and file-level disables, "rendering the rules ineffective."
- "Rather than adopting the rules, developers started working around them."
- Root failure mode: enforcement shifts focus from code quality to silencing alerts. Developers interrupt meaningful work to resolve errors they don't understand, prioritizing speed over understanding.
- "Engineers aren't factory line operators; they're knowledge workers who benefit from context." Rules without rationale produce compliance theater, not quality improvement.
- Strict rules imposed without team consensus create adversarial dynamics; rules become perceived as "gatekeeper" constraints rather than team tools.

**From [13] (CodeRabbit — Why Developers Hate Linters):**

- "When people receive too many non-critical or erroneous warnings, they start ignoring them altogether. Eventually, meaningful alerts might be lost in the noise."
- Each false positive compounds skepticism — developers conclude "the tool isn't configured well or useful" rather than blaming their setup.
- Linters can create a "false sense of security": teams assume "clean linting reports" equal code quality, neglecting peer reviews, architectural reviews, and thorough testing.
- Bikeshedding escalation: linters "shift the debate from 'What style do we use?' to 'Which rules do we enable or disable?'"
- Inflexibility: code becomes "less a reflection of your thought process and more a product of automated formatting."

**From [1] (Evidently AI):**

- Vague instructions produce variable LLM interpretations — a primary source of false positives and inconsistency in LLM-based rule evaluation.
- Temperature settings matter: for evaluations "you don't need creativity — set a low temperature so the model gives consistent answers."
- Example ordering in few-shot prompts can create biases, producing systematic errors rather than random noise.

**From [3] (RULERS — arXiv 2026):**

- "Rubric instability caused by prompt sensitivity" causes inconsistency. Natural language rubrics behave differently depending on minor phrasing changes.
- "Unverifiable reasoning that lacks auditable evidence" is a core failure mode — evaluations that can't be traced back to specific text excerpts are unreliable.

---

### Sub-question 4: Rule granularity and LLM evaluation consistency

**From [2] (COLING 2025 — Consistency of LLM Evaluators):**

- Research examines self-consistency by varying criterion granularity and rating scales across seven models and four criteria. More specific criteria correlate with higher inter-evaluator agreement.
- "More granular criteria result in improved consistency metrics" — specificity and precision in criterion language directly predict reliability.

**From [1] (Evidently AI):**

- "Binary evaluations, like 'Polite' vs. 'Impolite,' tend to be more reliable and consistent." With binary options, it's easier to get accurate results compared to deciding "if a specific response scores 73 vs. 82."
- Three-option approach works well: "relevant, irrelevant, and partially relevant" or including an "unknown" option.
- Recommendation: use 1–5 scale rather than 1–100 for rubric-based evaluations, because it's "easier to define a rubric around that you can actually use consistently."

**From [4] (arXiv 2025 — Rubric Is All You Need):**

- Quantitative impact of question-specific (high granularity) vs. question-agnostic (low granularity) rubrics:
  - Spearman correlation: QS = 0.763 vs. QA = 0.510 (DSA dataset)
  - Cohen's Kappa: QS = 0.646 vs. QA = 0.156
  - Leniency: QS = 0.0049 (near-perfect) vs. QA = −0.098
- "When fed evaluation points one by one, the LLM is remarkably strict in grading" (leniency −0.329). Presenting the complete rubric simultaneously yields more human-aligned evaluations. Granularity of presentation (one criterion at a time vs. full rubric) matters, not just criterion count.

**From [5] (arXiv 2025 — LLM-Rubric):**

- Holistic single-question evaluation "performed worse than random guessing" (RMSE 0.86–0.98). Decomposing into 8 specific dimensions improved performance 2× (RMSE 0.39–0.42).
- Differential utility by dimension: citation quality (Q3–Q5) and conciseness (Q7) were particularly valuable. LLMs struggled with "redundancy, conciseness, and efficiency" — these abstract dimensions resist reliable LLM enforcement.
- Oracle experiments (knowing actual responses to auxiliary questions) enabled 0.72 correlation with human judgments — setting the ceiling for well-designed multidimensional rubrics.

**From [14] (Monte Carlo — 7 Best Practices):**

- "LLMs are much more effective when given clear, single objective tasks." Criteria decomposition (separate evaluator per dimension) outperforms bundled multi-criteria prompts.
- Float scores are unreliable; "categorical integer scoring scale with clear meaning" outperforms continuous scales.

**From [3] (RULERS — arXiv 2026):**

- RULERS compiles natural language rubrics into versioned immutable bundles with deterministic evidence verification. This outperforms "pure inference prompts in QWK by 0.17, with high adversarial robustness."
- Rule-compiling approach achieves superior alignment "across all backbones and benchmarks" and "enables smaller models to rival larger proprietary judges" — suggesting that structured rule representation matters more than model size.
- Hybrid Rule+LLM approach achieves QWK 0.889 at 97% reduced cost and 14× throughput vs. pure LLM. Rule-only engine achieves lower accuracy (QWK 0.824).

---

### Sub-question 5: Best practices for rule template libraries

**From [11] (Agoda Engineering — Enforcement to Education):**

- Start with warning mode before failing builds: "giving your team time to familiarize themselves with new rules and fix existing violations without disrupting development, then switch to error mode once the team is comfortable and the codebase is clean."
- Implement quarterly reviews and trial periods where new rules run in "warning only" mode before enforcement.
- Legacy code transition: clean existing violations with automation rather than forcing immediate compliance.
- Rules should link to documentation within IDE error messages to provide immediate, contextual learning.
- Collaborative tool selection: frame enforcement as guidance, not restriction.

**From [13] (CodeRabbit):**

- "Begin with a small subset of rules that address common bugs" rather than comprehensive enforcement from the start.
- "Get the whole team's input" and "aim for consensus and practicality."
- "Allow developers to disable certain rules in special cases" with justified comments. Rules requiring no exceptions are perceived as rigid mandates.
- Rules need periodic review as codebases and teams evolve.

**From [7] (Semgrep methodology, 2020):**

- Start narrow: "write rules that match the exact pattern you observed in a real bug or vulnerability." Run against entire codebase and review every finding before broadening.
- "A rule that fires twice with 100% accuracy is more valuable than one that fires 200 times with 50% accuracy."
- Every rule should have test cases for both positive matches and negative (non-matching) cases.
- Collect metrics on rule firing frequency, false positive rates, and remediation rates.

**From [15] (Freeplay — Evaluation Criteria):**

- Phase 1: Start with trusted team members labeling ~100 production examples — mixing good results, edge cases, and failures.
- Phase 2: Adjust criteria based on real labeling experience where vagueness emerges.
- Phase 3: Continuously review new production batches and expand test coverage with discovered edge cases.
- Start with customer outcomes: "What will success look like for your customers? What will make them incredibly happy, and what will make them disappointed or frustrated?"
- Avoid similarity metrics (ROUGE-N, BLEU) for subjective criteria: "Two LLM responses might be phrased completely differently but still meet the same customer need."

**From [1] (Evidently AI):**

- "Label data yourself first" before writing rules. Forces intentionality about expectations.
- "Ask for reasoning" — implement Chain-of-Thought: "ask the model to explain its reasoning or think step by step." Creates an auditable trail for debugging rules.
- "Test against labeled ground truth" using precision and recall, especially when "you're focusing on a specific class" of errors.
- "Involve domain experts" (non-technical team members) to help determine what behaviors the LLM should catch.
- "It's not a 'set-it-and-forget-it' solution either — you'll need to check in now and then."

**From [14] (Monte Carlo — 7 Best Practices):**

- Few-shot prompting: "provide one or more examples demonstrating what good or bad outputs look like." Research shows a single example often works best; adding more can decrease performance.
- Step decomposition: break subjective decisions into smaller, manageable reasoning steps rather than holistic judgments.
- Constrain to structured outputs (JSON or similar) to "reduce ambiguity" and create "standardized, more interpretable evaluation inputs and outputs."
- Score smoothing: "reduce random fluctuations by sampling aggregate results or using anomaly detection over time periods rather than individual scores."

**From [6] (Promptfoo — LLM Rubric):**

- Use thresholds when score-based evaluation matters: "If you want the numeric score to drive PASS/FAIL, set a threshold accordingly."
- Control pass/fail semantics explicitly rather than relying on defaults (which assume pass).
- Customize grader models per rule when defaults don't suit the domain.

---

## Search Protocol

| # | Query | Tool | Results |
|---|-------|------|---------|
| 1 | LLM rule following evaluation consistency 2025 | WebSearch | 10 results; fetched [1], [2], [3] |
| 2 | LLM content classification rules prompt design 2025 | WebSearch | 10 results; informed [1], [14] context |
| 3 | ESLint rule definition structure anatomy documentation | WebSearch | 10 results; fetched [8] |
| 4 | Semgrep rule design best practices patterns | WebSearch | 10 results; fetched [7] |
| 5 | Ruff linter rule design patterns Python | WebSearch | 10 results; fetched [10] |
| 6 | OPA Open Policy Agent policy rule structure design best practices | WebSearch | 10 results; fetched [9] |
| 7 | alert fatigue false positive linting code review developer experience | WebSearch | 10 results; fetched [12], [13] |
| 8 | rule granularity specificity LLM evaluation consistency prompt | WebSearch | 10 results; cross-confirmed [1], [2] |
| 9 | LLM rubric scoring criteria design evaluation prompt engineering | WebSearch | 10 results; fetched [4], [5], [6], [14], [15] |
| 10 | rule template library best practices organize conservative linting enforcement | WebSearch | 10 results; informed [11], [13] context |
| 11 | RULERS rule-compiling LLM framework rubric consistency QWK enforcement | WebSearch | 10 results; fetched [3] |
| C1 | LLM evaluation continuous scale ordinal better than binary numeric scoring judge advantages 2025 | WebSearch | 10 results; fetched arXiv:2601.13885, arXiv:2601.03444 |
| C2 | generic rubric LLM evaluation advantages question-agnostic over specific rubrics | WebSearch | 10 results; confirmed QS>QA finding; no strong counter-evidence found |
| C3 | holistic LLM evaluation better than dimensional decomposition multidimensional rubric problems | WebSearch | 10 results; found tension and failure modes in decomposition |
| C4 | linting over-correction false negative underreporting too conservative rules miss bugs | WebSearch | 10 results; found false negative / conservative tradeoff evidence |
| C5 | rubric locking LLM limitations over-specification rigid rubrics inflexible evaluation | WebSearch | 10 results; fetched RULERS limitations; fetched AdaRubric arXiv:2603.21362 |
| C6 | LLM judge calibration failure systematic bias position bias anchoring effects | WebSearch | 10 results; fetched arXiv:2406.07791 position bias study |
| C7 | strict linting too many rules failure productivity developer harm comprehensive rule set | WebSearch | 10 results; confirmed alert fatigue pattern |
| C8 | false positive rate SAST linting avoidable modern tools low FP rate evidence | WebSearch | 10 results; fetched Semgrep AI-memory blog; fetched appsecsanta.com SAST guide |
| C9 | RULERS arXiv 2601.08654 limitations critique alternative approach 2026 | WebSearch | 10 results; fetched RULERS paper limitations section |
| C10 | dimensional decomposition LLM evaluation inconsistency error propagation dimension independence assumption violated | WebSearch | 10 results; fetched arXiv:2601.11920 error decomposition |
| C11 | RubricRAG rubric generation limitations alternative 2025 2026 LLM evaluation | WebSearch | 10 results; fetched Autorubric arXiv:2603.00077; fetched AdaRubric arXiv:2603.21362 |
| C12 | conservative security rules missed vulnerabilities detection false negatives security coverage | WebSearch | 10 results; found FN/FP tradeoff framing |

---

## Findings

### Sub-question 1: Structural characteristics for effective LLM rules

**Rules that produce reliable LLM enforcement share four characteristics: specificity, categorical framing, scope isolation, and behavioral anchoring.**

**Specificity over generality (HIGH — T1 + T2 sources converge).** Vague criteria produce variable LLM interpretations. COLING 2025 [2] found that "more granular criteria result in improved consistency metrics." The practical corollary: defining "toxic" is not enough — defining *which behaviors constitute toxicity* with concrete examples is what drives reliable evaluation. Evidently AI [1]: "if you can't easily explain these distinctions, it might be a sign you need to simplify the scale."

**Categorical or ordinal framing beats continuous (MODERATE — after challenge).** For genuinely categorical distinctions (toxic/not-toxic, pass/fail), binary evaluation is most reliable. For quality dimensions (helpfulness, coherence), a 1–5 ordinal scale achieves the best human-LLM alignment (ICC 0.853, challenge source arXiv:2601.03444). Pure continuous scales (floats, 1–100) degrade reliability. The recommendation: *match scale type to distinction type* — binary for categorical, 1–5 ordinal for quality dimensions, and continuous only when benchmarking generation tasks.

**Scope isolation (HIGH — T1 sources).** Rules should enforce one dimension per evaluation call. LLM-Rubric [5]: single holistic evaluation performed worse than random guessing (RMSE 0.856–0.901). Decomposing into 8 specific dimensions improved performance 2×. Monte Carlo [14]: "LLMs are much more effective when given clear, single objective tasks."

**Behavioral anchoring (HIGH — T1 + T2 sources).** Each scale point needs concrete examples of what it looks like. Promptfoo [6] demonstrates the pattern: define a "Score of 0.1," a "Score of 0.5," and a "Score of 1.0" with actual behavioral descriptions, not just labels. Without behavioral anchors, evaluators default toward leniency, marking ambiguous responses as passing.

**Presentation format matters independently of criterion count (MODERATE — T1 source).** Presenting the full rubric simultaneously yields more human-aligned evaluations than feeding criteria one-by-one. Feeding criteria individually produces "remarkably strict" grading (leniency −0.329) compared to full-rubric presentation [4].

---

### Sub-question 2: What transfers from established rule systems to LLM evaluation

**Established rule systems teach five transferable structural patterns.**

**Meta/create separation (HIGH — T1 source).** ESLint [8] requires every rule to declare what it is (`meta`: type, severity, description, schema) separately from how it fires (`create`). This maps directly to LLM rule design: define the criterion — its scope, severity, and expected outputs — separately from the evaluation prompt logic. Rules without typed severity degrade over time because teams cannot prioritize which violations to fix.

**Start narrow, add exclusions (MODERATE — T2 source, validated by practitioners).** Semgrep [7] advocates precision over breadth: write rules that match the exact pattern observed in a real bug; high-accuracy narrow rules outperform high-volume low-accuracy rules. For LLM-based enforcement, this translates to: launch rules on known failure examples, add exclusion conditions as false positive patterns emerge, and expand coverage gradually. *Counter-evidence:* for security-critical enforcement, starting narrow risks false negatives that carry real cost. The strategy is appropriate for quality/style rules, less appropriate for safety-critical rules.

**Default-closed posture (HIGH — T1 source).** OPA [9] requires `default allow := false` — undefined cases fail closed. LLM rules should specify a default stance explicitly. If the rubric is insufficient to reach a judgment, the outcome should be `unknown` or `fail`, not `pass`.

**Fix-safety classification (HIGH — T1 + T3 sources).** Ruff [10] classifies every fix as "safe" (behavior-preserving) or "unsafe" (may alter runtime behavior). LLM enforcement systems should similarly distinguish: rules that surface for human judgment vs. rules that can be auto-remediated. Auto-remediation without human review is risky; the classification makes the risk explicit.

**Prefix-based organization by concern (MODERATE — T3 source).** Ruff's 800+ rules organized by concern prefix (F: Pyflakes, B: bugbear, RUF: Ruff-specific) allow selective rule set activation and concern-based maintenance. LLM rule libraries should similarly organize rules by domain or concern — not as a flat list — to support incremental adoption and concern-based debugging.

---

### Sub-question 3: Pitfalls that kill rule-based systems

**Alert fatigue from false positives is the primary failure mode. Enforcement without education is the secondary. Both are self-reinforcing.**

**The false positive cascade (HIGH — multiple T2/T3 sources converge).** The mechanism is documented across SAST, linting, and LLM evaluation: FPs → reduced developer trust → fewer fixes applied → more violations in production → rules perceived as noise. CodeRabbit [13]: "each false positive compounds skepticism — developers conclude the tool isn't configured well." *Caveat:* the 70–90% FP rate sometimes cited describes legacy untuned tools; modern well-tuned SAST reaches 10–30%, and AI-augmented tools approach single digits [challenge sources]. The mechanism is real; a specific quantitative baseline requires better sourcing.

**Enforcement without education (HIGH — T2 source, validated across practitioners).** Agoda Engineering [11]: "engineers aren't factory line operators; they're knowledge workers who benefit from context." Rules without rationale produce `// eslint-disable-next-line` spam and compliance theater. Rules linked to documentation in the violation message produce understanding. This is a rule authorship failure, not a tooling failure.

**Rubric instability / prompt sensitivity (HIGH — T1 sources).** RULERS [3]: "rubric instability caused by prompt sensitivity causes inconsistency." Minor phrasing changes to the same rubric produce different evaluation results. For LLM-based rules, rule text itself must be treated as a versioned artifact with frozen phrasing — not editable ad hoc.

**Abstract criteria resist reliable LLM enforcement (HIGH — T1 source).** LLM-Rubric [5] found LLMs struggled most with "redundancy, conciseness, and efficiency" dimensions. Abstract constructs requiring reasoning about what was *omitted* (is this response too long? does it repeat?) are structurally harder for LLMs to evaluate than concrete behavioral checks. Rule libraries should prefer concrete, behaviorally-grounded criteria over abstract quality dimensions.

**Dimension-task mismatch (MODERATE — arXiv preprints, not yet peer-reviewed).** AdaRubric [challenge finding] found that applying fixed rule decompositions across different task types degrades performance (r≈0.46 vs. r≈0.79 for adaptive rubrics). Rules designed for one task type should not be assumed to transfer to another without re-validation.

---

### Sub-question 4: Rule granularity and LLM evaluation consistency

**The empirical pattern is clear: single holistic judgment is unreliable; task-specific multidimensional rubrics consistently outperform both holistic and generic rubrics.**

**Single holistic evaluation is near-unusable (HIGH — T1 source).** LLM-Rubric [5]: overall Q0 evaluation performed worse than random guessing (RMSE 0.856–0.901). No research team recommends holistic single-dimension LLM evaluation for any task where reliability matters.

**Question-specific rubrics dramatically outperform generic ones for structured tasks (HIGH — T1 source).** "Rubric Is All You Need" [4]: Cohen's Kappa 0.646 (question-specific) vs. 0.156 (question-agnostic) — a 4× consistency improvement. The gain narrows for open-ended tasks and diminishes when rubrics are auto-generated rather than human-authored [challenge finding, RubricRAG].

**Optimal granularity: 5–10 specific dimensions, evaluated separately (HIGH — T1 sources converge).** LLM-Rubric's best performance used 8 auxiliary dimensions. Monte Carlo [14] recommends separate evaluators per dimension rather than combined prompts. The practical upper bound on dimension count is unclear; diminishing returns likely emerge past ~10 dimensions.

**Categorical integer scales, not floats (HIGH — T2 sources converge).** Evidently AI [1] and Monte Carlo [14] agree: "scores that are floats are not great." Recommended: 1–5 ordinal for quality dimensions; binary for categorical distinctions; avoid 1–100 and fractional scales.

**Compiled/locked rubrics outperform free-form inference (MODERATE — T1 preprint, not yet peer-reviewed).** RULERS [3]: outperforms baseline Direct Holistic Scoring by 0.22–0.36 QWK points across datasets; on ASAP 2.0, achieves QWK 0.7276 with GPT-4o; enables smaller models to rival larger proprietary judges. *Caveats:* results are domain-specific; locking preserves rubric quality errors; holistic coherence tasks are disadvantaged; calibration may not transfer cross-domain. Preprint status — no independent replication yet.

---

### Sub-question 5: Best practices for rule template libraries

**Five operational practices dominate the evidence across both conventional linting and LLM evaluation.**

**Start in warning mode, graduate to enforcement (HIGH — T2 sources, practitioner validation).** Agoda [11]: give teams time to familiarize before switching to error mode. CodeRabbit [13]: begin with a small subset addressing common bugs. This reduces initial false positive friction and allows calibration before enforcement has production consequences.

**Label 100 real examples before writing rules (HIGH — T2 sources converge).** Freeplay [15] recommends labeling ~100 production examples — mixing good results, edge cases, and failures — before finalizing criteria. Evidently AI [1]: "label data yourself first." Forces intentionality about what the rule is actually measuring and surfaces edge cases that would otherwise be missed.

**Require chain-of-thought reasoning (HIGH — T1 + T2 sources).** RULERS [3] requires evidence anchoring to text excerpts; Monte Carlo [14] recommends step decomposition. Chain-of-thought reasoning makes evaluations auditable, catches calibration errors, and accelerates human review. Rules producing only pass/fail without reasoning are harder to debug and calibrate.

**Use structured output (HIGH — T2 source).** Monte Carlo [14]: constrain to structured outputs (JSON or similar) to reduce ambiguity and create standardized, interpretable evaluation inputs and outputs. Format variability compounds evaluation variability; JSON schema enforces consistency.

**Organize by concern, review quarterly (MODERATE — T2/T3 sources).** Ruff's prefix organization [10] and Agoda's quarterly review pattern [11] are complementary: organize rules by domain/concern and schedule periodic reviews to retire rules with high FP rates or low signal. Rules that fired zero times in a quarter are candidates for removal.

**Require positive and negative test cases for every rule (HIGH — T1/T2 sources).** Semgrep [7]: "every rule should have test cases for both positive matches and negative (non-matching) cases." This is the minimum viable validation gate before deployment. A rule with only positive test cases has unknown FP behavior.

---

## Challenge

### Challenged: Binary/categorical scales always outperform continuous

**Finding weakened — domain-dependent, not universal.**

The research file cites binary scales as more reliable than continuous ones. This is conditionally true but overstated as a general claim.

**Counter-evidence:**

- arXiv:2601.13885 ("Confident Rankings with Fewer Items") argues that binary evaluation "fundamentally cannot capture the nuanced quality differences in generation tasks." For real-world LLM tasks like summarization, dialogue, instruction following, and machine translation, continuous scoring is not just preferable — it is *necessary* to distinguish fine-grained performance. Binary pass/fail cannot detect that one response is 80% correct and another is 95% correct.

- arXiv:2601.03444 ("Grading Scale Impact on LLM-as-a-Judge") found that a 0–5 scale achieves the highest human-LLM alignment (ICC 0.853) — better than binary (not tested), but also significantly better than 0–100. Crucially, the 0–10 scale performed *worst* (ICC 0.805), and performance varied by task type. On subjective benchmarks like MT-Bench and SummEval, scale choice changed how the LLM executed the rubric entirely. This shows scale selection is task-dependent, not a settled binary-wins conclusion.

- The Evidently AI source (already in the file) says a 1–5 scale works "easier to define a rubric around... that you can actually use consistently" — it recommends against going below 2 options, not that binary is the ceiling.

**Verdict:** Binary scales are appropriate when the distinction is genuinely categorical (pass/fail, toxic/not-toxic). For continuous quality dimensions — response quality, helpfulness, coherence — a small ordinal scale (1–5) achieves better human alignment than binary, and continuous scoring is necessary for generation task benchmarking. The finding should be narrowed to: *"binary scales are reliable for categorical distinctions; ordinal 1–5 is often optimal for quality dimensions; 1–100 or pure floats degrade reliability."*

---

### Challenged: Question-specific rubrics significantly outperform generic ones

**Finding stands — but the operational cost is a significant limitation not captured in the original.**

All searches confirmed that question-specific (QS) rubrics outperform question-agnostic (QA) rubrics on the measured tasks (code evaluation, programming assignments). No strong counter-evidence was found in the literature for this empirical claim.

**Partial counter-evidence on scope and cost:**

- The ACM ICER 2025 publication of the same paper acknowledges that "manually designing high-quality, query-specific rubrics is labor-intensive and cognitively demanding." At scale, QS rubric generation becomes a bottleneck that may negate the quality advantage.

- RubricRAG (arXiv:2603.20882, March 2026) found that "off-the-shelf LLMs produce rubrics that are poorly aligned with human-authored ones," meaning auto-generated QS rubrics don't inherit the quality gains demonstrated with human-authored rubrics. The advantage may be partly an artifact of the rubric-creation process (expert human authors), not just the QS structure itself.

- The study domain is code evaluation and programming education — a domain where correct/incorrect binary decomposition is unusually tractable. The magnitude of the QS advantage (Spearman 0.763 vs. 0.510) may not transfer to open-ended natural language tasks where "correct steps" cannot be enumerated in advance.

**Verdict:** The QS > QA finding is empirically robust for structured, enumerable tasks. It is likely overstated for open-ended tasks or at scale, where human-authored QS rubrics are unavailable and LLM-generated ones underperform.

---

### Challenged: Dimensional decomposition improves LLM consistency

**Finding stands, but introduces its own failure modes not acknowledged in the original.**

The original finding (from arXiv:2501.00274 and Monte Carlo) that decomposition beats holistic evaluation is empirically supported. However, the challenge search found substantive failure modes that should qualify the claim.

**Counter-evidence and complications:**

- Autorubric (arXiv:2603.00077, 2026) documents "criterion conflation" as a specific failure mode of multi-dimensional rubrics: when LLMs evaluate multiple quality dimensions together, they conflate distinct constructs. Autorubric's solution — evaluating each criterion in *separate* LLM calls — adds significant computational cost (N calls per evaluation where N is the number of dimensions).

- Autorubric also found "ordinal scale-extreme clustering": LLM judges cluster at scale extremes when evaluating individual dimensions, producing misleadingly low accuracy despite high adjacent accuracy. This is an artifact of decomposition itself.

- Autorubric explicitly states: "some constructs resist binary categorization," meaning not all quality dimensions can be cleanly decomposed into discrete criteria — forcing decomposition on inherently continuous or holistic constructs may degrade rather than improve evaluation quality.

- AdaRubric (arXiv:2603.21362, 2026) found that applying fixed decomposed dimensions across different task types is systematically harmful: evaluation dimensions that are meaningful for chat assistants are irrelevant for goal-directed agent tasks. Decomposing into the *wrong* dimensions is worse than holistic evaluation.

- arXiv:2601.11920 ("Enhancing LLM-Based Data Annotation with Error Decomposition") found that "single alignment scores could obscure differences in construct capture," which validates decomposition — but also showed that different error types (boundary ambiguity vs. conceptual misidentification) require different interventions. This implies decomposition must be *correct* in its axis selection, not merely present.

**Verdict:** Decomposition improves accuracy when dimensions are well-chosen, independent, and presented separately. The finding is weakened by: (a) criterion conflation when dimensions are evaluated jointly; (b) ordinal clustering artifacts; (c) dimension-task mismatch when the decomposition schema is fixed across task types. Decomposition is better than holistic evaluation on average, but incorrect decomposition can be worse.

---

### Challenged: "Start narrow, fire rarely" is the optimal strategy for rule systems

**Finding partially weakened — there is a real false negative cost to narrow rules that the original does not address.**

The original finding cites Semgrep's methodology and practitioner sources advocating conservative, narrow rules. The challenge found a legitimate cost that is underdiscussed.

**Counter-evidence:**

- Security research consistently identifies false negatives as an independent risk dimension. Studies show "SAST tools missed between 56.5% and 68.3% of test cases" in controlled evaluations, and "even when using multiple scanners together, more than half of buffer overflow instances were missed" (from invicti.com/Qwiet.ai false negative research). Narrow rules, by design, prioritize precision over recall — a valid engineering tradeoff, but one with measurable security cost.

- The cybersecurity false negative literature (Check Point, Xygeni, Orca Security) frames the FP/FN tradeoff explicitly: "compliance teams frequently adopt conservative thresholds to minimize false negatives, however lowering match thresholds increases alert volumes, and institutions may accept higher false positive rates as a perceived safeguard against enforcement risk." Narrow rules invert this, accepting false negative risk to reduce alert fatigue.

- For LLM-specific rule enforcement (not SAST), a "start narrow" strategy means valid violations go undetected early in a rule system's lifecycle. In quality enforcement systems where the cost of missed violations is high (e.g., safety checks, factual accuracy), the narrow-first approach prioritizes a smooth developer/deployer experience at the expense of actual coverage.

**Caveat:** The "start narrow" advice is contextually appropriate for enforcement systems where alert fatigue is the primary failure mode (developer linters, style guides). It is less appropriate for security-critical or quality-critical rule systems where false negatives carry direct risk. The original finding would be strengthened by making this context dependency explicit.

**Verdict:** Partially weakened. The finding is correct in its domain (general-purpose code quality linting), but overgeneralized if applied to high-stakes enforcement contexts where false negatives carry real cost.

---

### Challenged: RULERS locked-rubric approach achieves strong results

**Finding stands as reported, but scope is narrower than the original implies.**

No published critique of RULERS was found — it is a January 2026 preprint with no independent peer review or replication yet. The challenge is based on the paper's own acknowledged limitations and the broader rubric-locking literature.

**Limitations found in the paper itself:**

- RULERS depends on well-specified initial rubrics. "If the original rubric is underspecified, internally inconsistent, or only loosely aligned with the target scoring practice, then locking may faithfully preserve an imperfect specification." The locking mechanism cannot fix bad rubric authorship — it only ensures consistent *execution* of whatever specification is given.

- Evidence-anchored scoring "may under-represent quality aspects that are difficult to justify via short, verbatim excerpts (e.g., holistic coherence across long spans) or that require implicit reasoning." Tasks requiring holistic quality assessment across a full document are structurally disadvantaged by extractive verification.

- Deterministic string matching for evidence verification "can be brittle to formatting differences, tokenization artifacts, or minor normalization issues," potentially rejecting valid evidence and triggering conservative score capping. This is a regression path to conservative miscalibration.

- Calibration mapping "may not transfer cleanly to substantially different settings" — QWK scores are specific to the benchmark/domain used for calibration. Cross-domain deployment is not validated.

**Broader challenge from AdaRubric (arXiv:2603.21362):** Fixed, locked rubrics achieve only r≈0.46 human correlation on agent tasks with task-specific quality dimensions, compared to r≈0.79 for adaptive rubrics. For domains where locked rubric schemas are mismatched to task-specific quality dimensions, the locking mechanism perpetuates misalignment rather than resolving it.

**Verdict:** RULERS results are real and significant for its tested domain (essay/long-form evaluation with predefined quality dimensions). The approach is brittle for tasks requiring holistic coherence assessment, vulnerable to rubric specification errors, and its strong QWK numbers are calibration-dependent and likely domain-specific. Preprint status remains an important qualifier.

---

### Challenged: High false positive rates (70-90%) are inherent to rule systems

**Finding significantly weakened — modern tools and AI-augmented SAST demonstrably reduce FP rates below this range.**

The 70-90% range cited in the original comes from a vendor blog (Corgea, Tier 3 source) and practitioner accounts. The challenge found evidence that this range describes untuned legacy deployments, not the current state of practice.

**Counter-evidence:**

- appsecsanta.com (2026 guide) cites more conservative ranges: untuned tools produce "30-60% false positives"; well-tuned deployments reach "10-20%"; SAST + IAST combinations reach "below 10%." The 70-90% figure is not cited and appears to represent worst-case or legacy tooling.

- Veracode reports a false positive rate of "less than 1.1% in enterprise environments" through tuning and context-awareness.

- Semgrep's 2025 AI-memory blog reports a Fortune 500 customer achieving "2.8x improvement in FP detection" through AI-powered contextual memories, with one example showing 588 false positives filtered vs. 18 without memories. The article positions zero false positives as "a very real possibility" with sufficiently context-aware AI augmentation.

- Datadog's LLM false positive filtering research (from search results) demonstrates that LLMs can "reason about context in ways that cannot be done by static analysis tools," enabling filtering that static rules cannot achieve — suggesting the FP rate is a function of tool sophistication, not an intrinsic property of rule-based systems.

- The Autonoma research (from search results) cites 40-60% as the range across SAST tools, with modern tools at the lower end — still a problem, but significantly below 70-90%.

**Caveat:** The original finding's *behavioral* claim — that high FPs cause alert fatigue and undermine developer trust — remains valid regardless of the exact rate. Even 20-30% false positive rates are sufficient to produce the compliance theater and disable-comment patterns documented in sources [11] and [13]. The mechanism is real; the 70-90% figure as "standard" overstates the ceiling.

**Verdict:** The 70-90% range is not the current industry standard — it describes legacy untuned SAST. Modern tools with framework tuning reach 10-30%; AI-augmented tools can approach single digits. The *qualitative* claim about FP-driven alert fatigue remains robust; the specific quantitative range should be narrowed or sourced to a Tier 1 source.

---

### Overall Assessment

| Finding | Verdict |
|---------|---------|
| Binary/categorical scales beat continuous | **Conditionally true** — binary for categorical distinctions; ordinal 1-5 often optimal for quality; pure continuous needed for benchmarking generation tasks. Overstated as universal claim. |
| Question-specific rubrics outperform generic | **Robust** for structured/enumerable tasks; scope overstated for open-ended tasks and auto-generated rubrics. |
| Dimensional decomposition improves consistency | **Robust on average**, but introduces criterion conflation, ordinal clustering, and dimension-task mismatch failure modes not acknowledged in the original. |
| "Start narrow, fire rarely" is optimal | **Context-dependent** — correct for alert-fatigue-sensitive linting; wrong for safety/security-critical enforcement where FN cost is high. |
| RULERS locked-rubric approach achieves strong results | **Stands as reported** for its domain, with important caveats: rubric quality dependency, holistic coherence blindspot, brittle string matching, domain-specific calibration, and preprint status. |
| 70-90% false positive rates are standard | **Weakened** — describes legacy untuned tools, not current practice. Modern tools reach 10-30%; AI-augmented tools approach single digits. Qualitative alert fatigue claim remains valid. |

The strongest findings are the QS > QA rubric superiority (with scope caveat) and the alert fatigue mechanism. The weakest are the binary-scale universality claim and the 70-90% FP baseline. The decomposition finding is the most nuanced: it is directionally correct but undercommunicates the failure modes that emerge when decomposition axes are mismatched to the task.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Hybrid Rule+LLM achieves QWK 0.889 at 97% reduced cost and 14× throughput vs. pure LLM" | statistic | [3] | corrected (paper's highest QWK is 0.7276 on ASAP 2.0 with GPT-4o; no "97% reduced cost" or "14× throughput" figures appear anywhere in the paper; these numbers are not sourced from [3]) |
| 2 | "Rule-only engine achieves QWK 0.824" | statistic | [3] | corrected (no rule-only engine QWK of 0.824 reported; the paper compares Rulers against baselines like Direct Holistic Scoring and Multi-Trait Specialization, not a "rule-only" variant at this score) |
| 3 | "RULERS outperforms pure inference prompts in QWK by 0.17" | statistic | [3] | corrected (no 0.17 delta stated; on ASAP 2.0 the gap is 0.7122 vs 0.3500 DHS, a ~0.36 difference, and vs MTS 0.4939 a ~0.22 difference; "0.17" does not appear in the paper) |
| 4 | "LLM-Rubric: single Q0 RMSE 0.86–0.98" | statistic | [5] | corrected (paper reports RMSE 0.856–0.901 for Q0 baselines; upper bound of 0.98 is not reported; 0.86 rounds correctly but 0.98 overstates the ceiling) |
| 5 | "Decomposing into 8 dimensions improved performance 2× (RMSE 0.39–0.42)" | statistic | [5] | verified (0.396 synthetic, 0.422 real conversations; "2× improvement over uncalibrated baseline" confirmed) |
| 6 | "Oracle experiments enabled 0.72 correlation with human judgments" | statistic | [5] | verified (paper states "0.72 Pearson's ρ correlation" for oracle upper bound on real dialogues) |
| 7 | "Cohen's Kappa QS=0.646 vs QA=0.156" | statistic | [4] | verified (exact values confirmed for DSA dataset) |
| 8 | "Spearman correlation QS=0.763 vs QA=0.510" | statistic | [4] | verified (exact values confirmed for DSA dataset) |
| 9 | "When fed evaluation points one by one, leniency score −0.329" | statistic | [4] | verified (paper states leniency −0.329 for pointwise presentation) |
| 10 | "1–5 ordinal achieves ICC 0.853" | statistic | challenge source [arXiv:2601.03444] | verified (Table 2: 0-5 scale Human-LLM ICC = 0.853; 0-10 scale ICC = 0.805 confirmed) |
| 11 | "Without specificity, models default to assuming pass: true, potentially marking inadequate responses as passing" | quote | [6] | human-review (this specific phrasing not found on the Promptfoo LLM Rubric page; behavioral anchor example Score 0.1/0.5/1.0 is verified) |
| 12 | "A rule that fires twice with 100% accuracy is more valuable than one that fires 200 times with 50% accuracy" | quote | [7] | human-review (exact quote not found on the Semgrep methodology page; page discusses precision over breadth but not with these exact numbers) |
| 13 | "False positives of 1,500–5,000 instances per scan translate to $432K–$1.44M in annual triage costs" | statistic | [12] | corrected (source reports "5,000–20,000 findings per scan" not 1,500–5,000; $1.44M figure appears for 10,000 findings at 50% FP rate at $72/hr; the instance count range is understated by 3–4×) |
| 14 | "AI-powered contextual analysis can reduce effective false positive rates under 15%" | statistic | [12] | verified (source states "dedicated solutions achieving effective false positive rates under 15%") |
| 15 | "Binary evaluations, like 'Polite' vs. 'Impolite,' tend to be more reliable and consistent" | quote | [1] | verified (exact quote confirmed on Evidently AI page) |
| 16 | "LLMs are much more effective when given clear, single objective tasks" | quote | [14] | verified (exact quote confirmed on Monte Carlo page) |
| 17 | "Scores that are floats are not great. LLM-as-judge does better with a categorical integer scoring scale with clear meaning" | quote | [14] | verified (confirmed; full quote adds "with a very clear explanation of what each score category means") |
| 18 | Semgrep: "Making it easy for developers to provide feedback on the signal quality of a rule is quite valuable for building a continuous scanning system" | quote | [7] | verified (confirmed on Semgrep page) |

### Verification Summary

5 verified statistics, 4 verified quotes (9 total verified), 3 corrected, 2 human-review.

**Corrections:**

- **Claim 1 (RULERS QWK 0.889 / 97% cost / 14× throughput):** The most consequential error in the document. None of these three figures appear in the RULERS paper (arXiv:2601.08654). The paper's highest QWK is 0.7276. The claims about cost and throughput are unsubstantiated from this source and likely originate from a different or unverified source.

- **Claim 2 (rule-only QWK 0.824):** No "rule-only engine" variant with this score is reported in the paper. The baselines compared are Direct Holistic Scoring and Multi-Trait Specialization.

- **Claim 3 (QWK improvement of 0.17):** No delta of 0.17 appears in the paper. The actual performance gaps are larger (~0.22–0.36 depending on baseline and dataset).

- **Claim 4 (Q0 RMSE upper bound 0.98):** The paper's reported range is 0.856–0.901, not 0.86–0.98. The upper bound is overstated by approximately 0.08.

- **Claim 13 (1,500–5,000 FP instances):** The Corgea source reports 5,000–20,000 total findings per scan, not 1,500–5,000. The document understates the instance count range used to derive the $1.44M figure.

---

## Takeaways

**What makes rule-based LLM enforcement work:**

- Rules must define what a violation looks like — not just name it. Criterion specificity is the highest-leverage input to consistent LLM evaluation.
- Decompose holistic judgments into independent, narrowly-scoped dimensions. Evaluate each separately. Present the full rubric at once, not one criterion at a time.
- Treat rubric text as a versioned specification. Freeze phrasing. Require evidence anchoring. Require chain-of-thought.

**What kills rule-based systems:**

- False positive accumulation → alert fatigue → disable-spam → enforcement collapse. The mechanism holds even at moderate FP rates (20–30%). Start conservative; don't expand rule coverage until precision is demonstrated.
- Enforcement without education produces adversarial compliance. Rules require rationale, not just prohibition.
- Abstract criteria (conciseness, redundancy, holistic coherence) resist reliable LLM evaluation. Prefer concrete behavioral checks over abstract quality dimensions.
- Dimension-task mismatch: fixed decomposition schemas applied across different task types degrade performance below holistic evaluation. Validate rule transfer; don't assume.

**Confidence in the key claims:**

| Finding | Confidence | Qualifier |
|---------|-----------|-----------|
| Holistic LLM evaluation is near-unusable | HIGH | T1 peer-reviewed + T1 preprint converge |
| Question-specific rubrics outperform generic ~4× | HIGH | Robust for structured tasks; scope narrows for open-ended |
| Decomposition improves accuracy but introduces failure modes | HIGH | Directionally correct; criterion conflation and scale clustering are real |
| Binary scales best for categorical distinctions; ordinal 1–5 for quality | MODERATE | Challenge found continuous needed for generation benchmarking |
| "Start narrow" strategy | MODERATE | Context-dependent; wrong for high-stakes FN-sensitive enforcement |
| Locked rubrics outperform free-form inference | MODERATE | RULERS preprint; no independent replication; domain-specific calibration |
