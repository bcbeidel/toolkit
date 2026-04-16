---
name: "Rule Repair and Evaluation Prompt Patterns"
description: "What prompt structures reliably detect rule quality deficiencies and generate actionable repair recommendations — evidence from LLM-as-judge research, rubric design studies, and rule engineering practice. Covers evaluation prompt anatomy, repair generation patterns, locked-rubric vs. free-form tradeoffs, and anti-patterns in rule audit prompting."
type: research
sources:
  - https://arxiv.org/abs/2601.08654
  - https://arxiv.org/html/2503.23989v1
  - https://arxiv.org/html/2501.00274v1
  - https://aclanthology.org/2025.coling-main.710.pdf
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/
  - https://arxiv.org/html/2603.00077v1
  - https://arxiv.org/html/2602.05125v1/
  - https://arxiv.org/html/2506.13639v1
  - https://arxiv.org/abs/2303.16634
  - https://arxiv.org/abs/2409.15268
  - https://arxiv.org/html/2410.02736v1
  - https://freeplay.ai/blog/defining-the-right-evaluation-criteria-for-your-llm-project-a-practical-guide
  - https://www.montecarlodata.com/blog-llm-as-judge/
  - https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/
related:
  - docs/research/2026-04-07-rule-enforcement.research.md
  - docs/research/2026-04-07-llm-as-judge.research.md
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
---

The check-rule skill performs a five-dimension semantic audit using a locked rubric. The build-rule skill generates rules from patterns. What's underspecified is the intermediate operation: **rule repair** — taking a rule that has been flagged with quality issues and generating a corrective prompt that produces a well-formed replacement. This investigation focuses on the prompt structures that best serve evaluation (detecting flaws) and repair (generating actionable fixes), drawing from LLM-as-judge research, rubric design literature, and linter engineering practice.

## Research Question

What prompt structures reliably detect deficiencies in LLM evaluation rules and generate actionable repair recommendations, and what patterns of prompting produce evaluation stability across repeated audits?

## Sub-Questions

1. What prompt anatomy elements are required for reliable rule quality evaluation — and which elements are responsible for instability when missing?
2. How should repair prompts be structured: what makes a repair recommendation actionable vs. advisory?
3. What are the documented failure modes of evaluation prompts that audit other prompts (meta-evaluation), and how do they differ from first-order LLM evaluation?
4. What does the empirical literature say about locked vs. open rubric formats for rule evaluation, and when does each apply?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2601.08654 | RULERS: Locked Rubrics and Evidence-Anchored Scoring for Robust LLM Evaluation | Hong et al. | 2026-01 | T1 | verified (preprint) |
| 2 | https://arxiv.org/html/2503.23989v1 | Rubric Is All You Need: Enhancing LLM-based Code Evaluation With Question-Specific Rubrics | (authors) | 2025-03 | T1 | verified (preprint) |
| 3 | https://arxiv.org/html/2501.00274v1 | LLM-Rubric: A Multidimensional, Calibrated Approach to Automated Evaluation of Natural Language Texts | (authors) | 2025-01 | T1 | verified (preprint) |
| 4 | https://aclanthology.org/2025.coling-main.710.pdf | Evaluating the Consistency of LLM Evaluators | ACL Anthology (COLING 2025) | 2025 | T1 | verified |
| 5 | https://www.evidentlyai.com/llm-guide/llm-as-a-judge | LLM-as-a-judge: a complete guide to using LLMs for evaluations | Evidently AI | 2025 | T3 | verified |
| 6 | https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/ | LLM Rubric | Promptfoo (official docs) | 2025 | T1 | verified |
| 7 | https://arxiv.org/html/2603.00077v1 | AutoRubric: A Unified Framework for Rubric-Based LLM Evaluation | (authors) | 2026-03 | T1 | verified (preprint) |
| 8 | https://arxiv.org/html/2602.05125v1/ | Rethinking Rubric Generation for Improving LLM Judge and Reward Modeling | (authors) | 2026-02 | T1 | verified (preprint) |
| 9 | https://arxiv.org/html/2506.13639v1 | An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability | (authors) | 2025-06 | T1 | verified (preprint) |
| 10 | https://arxiv.org/abs/2303.16634 | G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment | Liu et al. | 2023-12 | T1 | verified |
| 11 | https://arxiv.org/abs/2409.15268 | Style Outweighs Substance: Failure Modes of LLM Judges in Alignment Benchmarking | Feuer et al. | 2025-01 | T1 | verified |
| 12 | https://arxiv.org/html/2410.02736v1 | Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge | Ye et al. | 2024-10 | T1 | verified |
| 13 | https://freeplay.ai/blog/defining-the-right-evaluation-criteria-for-your-llm-project-a-practical-guide | Defining the Right Evaluation Criteria for Your LLM Project | Freeplay | 2025 | T3 | verified |
| 14 | https://www.montecarlodata.com/blog-llm-as-judge/ | LLM-As-Judge: 7 Best Practices & Evaluation Templates | Monte Carlo Data | 2025 | T2 | verified |
| 15 | https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/ | Writing Semgrep Rules: A Methodology | Semgrep | 2020 | T2 | verified |

## Raw Extracts

### Sub-question 1: Prompt anatomy for reliable rule evaluation

**Locked rubric outperforms free-form rubric by +0.17 QWK on human agreement (T1, RULERS [1]):**

The RULERS framework identifies three failure modes in natural language rubrics used as evaluation prompts:

1. **Rubric instability from prompt sensitivity** — minor phrasing changes produce measurably different evaluation outputs. Two rubrics that are semantically equivalent to a human produce divergent LLM scoring.
2. **Unverifiable reasoning** — evaluation produces a verdict without citable evidence, making errors undebuggable.
3. **Scale misalignment** — LLM score distributions do not match human grading boundaries (e.g., LLMs cluster at the middle of a 1-5 scale).

RULERS addresses these by compiling rubrics into "versioned immutable bundles" with structured decoding and deterministic evidence verification. The compiled format prevents drift by making the rubric a frozen specification rather than a freeform instruction. Smaller models using RULERS-style compiled rubrics rival larger proprietary judges.

**Required anatomy for a stable evaluation prompt (T1 synthesis across [1][2][3][4]):**

The empirical evidence across four studies converges on six structural elements that must appear in a rule evaluation prompt to produce consistent verdicts:

1. **Criterion statement** — a single, precise behavioral definition of what is being evaluated (not what good looks like — what the criterion detects)
2. **Anchor examples** — at minimum one non-compliant and one compliant example; without these, LLMs "default to assuming pass:true, potentially marking inadequate responses as passing" [6]
3. **Evidence requirement** — explicit instruction to cite the specific text or element that triggered the verdict, before emitting the verdict
4. **Verdict format** — binary (PASS/FAIL or WARN/PASS) with no intermediate options for compliance decisions; intermediate scales are "more likely to produce arbitrary scores" [5]
5. **Default-closed declaration** — explicit handling of borderline cases: "When evidence is borderline, surface as WARN, not PASS." Without this, models default to PASS [6].
6. **Scope statement** — what the criterion applies to (file type, rule format, specific section)

**The order of elements within the prompt matters (T1, RULERS [1]; T3, EvidentlyAI [5]):**

RULERS enforces a structured output template: `[evidence] → [reasoning] → [verdict]`. This ordering is significant: requiring evidence before verdict prevents post-hoc rationalization. A prompt that asks for `[verdict] → [reasoning]` produces verdict-first confirmation bias where the reasoning rationalizes the already-emitted verdict. Evidence-anchored scoring (evidence before verdict) "significantly outperforms representative baselines in human agreement."

**Removing evaluation criteria drops correlation from 0.666 to 0.487 (T1, empirical study [9]):**

The empirical design study tested what happens when criterion descriptions are stripped from evaluation prompts. Removing criteria reduced GPT-4o correlation with human graders from 0.666 to 0.591 (criteria removed) and further to 0.487 (criteria and reference answers removed). The impact of evaluation criteria exceeded that of reference answers. This establishes the criterion statement as the highest-leverage element of an evaluation prompt.

**Specificity of criterion language predicts inter-evaluator agreement (T1, COLING [4]):**

> "More detailed, specific criteria lead to higher agreement rates between evaluators compared to broad, general assessment guidelines."

Concrete behavioral definitions outperform abstract quality descriptors. "Good", "clean", "clear", "appropriate" produce variable interpretations. Observable behavioral definitions ("the function exports exactly one value at the module boundary") produce consistent results.

**Full rubric in one call outperforms per-criterion calls (T1 [2]):**

"When fed evaluation points one by one, the LLM is remarkably strict in grading" (leniency score −0.329). Presenting the complete rubric simultaneously yields "more human-aligned evaluations." Separate calls per criterion score 11.5 points lower on average. This is a documented penalty for splitting evaluation into individual criterion calls.

---

### Sub-question 2: Repair prompt structure — actionable vs. advisory

**The distinction between advisory and actionable repair output (T2, Semgrep methodology [15]; T3, Freeplay [13]):**

Semgrep's rule authoring methodology distinguishes between a finding (what was detected and why) and a fix (what the author should change). Applied to rule repair prompts:

- **Advisory output:** "This rule's scope is too broad." → No executable path to fix.
- **Actionable output:** "Change scope from `**/*.py` to `src/models/**/*.py` — the rule's Intent section references only model-layer files, and firing on test fixtures and scripts adds false positives." → Specific substitution with justification.

The critical difference is that an actionable repair includes:
1. **The specific element to change** (field name, section, phrasing)
2. **The proposed replacement** (a concrete value, not a description of what the value should be)
3. **The evidence that requires the change** (what in the rule triggered the finding)

**Repair prompts must separate diagnosis from prescription (T1, RULERS [1]; T3, EvidentlyAI [5]):**

Combining diagnosis and repair in one prompt degrades the quality of both. The evaluation phase should establish evidence first, then verdict, then recommendation. Interleaving repair suggestions within the evaluation reasoning interferes with the evidence-anchoring that makes evaluation reliable. A clean two-phase structure:

Phase 1 (evaluation): evidence → verdict (PASS/WARN/FAIL per dimension)
Phase 2 (repair): verdict evidence → specific change recommendation (only for WARN/FAIL verdicts)

**Rule repair requires the existing rule file verbatim, not a summary (T1 [2]; check-rule skill):**

Summarizing a rule for a repair prompt introduces paraphrase drift — the LLM evaluates a restatement, not the rule itself. This produces repair recommendations that address the restatement rather than the actual text. The full rule file must appear verbatim in the repair prompt. This parallels the evaluation finding: question-specific rubrics that include full context outperform generic rubrics by ~4× on Cohen's Kappa [2].

**Repair recommendations must include the target section and field (T3, Freeplay [13]):**

> "If you have several aspects to evaluate — completeness, accuracy, relevance — split them into separate evaluators."

Applied to repair: when multiple dimensions fail, each must generate a separate, targeted repair recommendation anchored to its specific location in the rule file. A single compound recommendation addressing multiple dimensions produces ambiguous output where authors cannot determine which change addresses which finding.

**The repair prompt should constrain output format to a diff-style structure:**

Given that the goal is a rewritten rule file (or a section of one), an effective repair prompt constrains the output to:
- `CHANGE [field/section name]:`
- `FROM: [current value, quoted verbatim]`
- `TO: [proposed value]`
- `REASON: [evidence from evaluation that drives this change]`

This format enables deterministic application and review. Free-form repair prose produces recommendations that authors must interpret before they can act.

---

### Sub-question 3: Meta-evaluation failure modes — evaluating evaluators

**Meta-evaluation (evaluating a rule that is itself an evaluator) has distinct failure modes not present in first-order evaluation:**

When a rule audit prompt evaluates a rule that is itself an LLM evaluation prompt, several compounding effects emerge:

**Style-over-substance bias at the meta level (T1, Feuer et al. [11]):**

At the first-order level, Feuer et al. found that "LLM-judge preferences do not correlate with concrete measures of safety, world knowledge, and instruction following — judges prioritize stylistic preferences over factuality and safety." At the meta-evaluation level, this means an audit prompt may rate a fluent, well-formatted rule that is semantically broken as PASS, while rating a terse but correct rule as WARN. Audit prompts must explicitly de-prioritize fluency and formatting in favor of structural completeness.

Mitigation: the evaluation rubric for a rule audit should include negative anchors for fluency-but-broken rules ("A rule with professional prose but no non-compliant example should receive WARN on behavioral anchoring, regardless of how clear the Intent section reads").

**Self-consistency failure under scope isolation (T1, empirical study [9]; T3, EvidentlyAI [5]):**

An audit prompt that combines multiple evaluation dimensions (specificity, staleness, fix-safety, rubric instability) in a single holistic call produces internally inconsistent verdicts. The same rule may receive PASS on one implicit dimension and FAIL on another within the same output, with no separate verdict per dimension. Forcing per-dimension scoring with explicit output slots prevents this: each dimension must have its own evidence block and verdict.

**Evidence hallucination in meta-evaluation (T1, RULERS [1]):**

The RULERS paper identifies "unverifiable reasoning" — evaluation produces a verdict with reasoning that does not cite the text being evaluated. At the meta level, this manifests as: "This rule has unclear scope" without quoting the scope value. The repair prompt then cannot anchor to the evidence. Evidence requirements must be made mandatory, not optional, in the evaluation output template:

```
Dimension: Specificity
Evidence: [quote from rule file]
Verdict: WARN
Recommendation: [specific change]
```

**False positive cascade from overly strict sequential evaluation (T1 [2]):**

Sequential dimension evaluation (separate prompt per dimension) scores 11.5 points lower on average than simultaneous rubric evaluation. An audit system that makes one call per dimension will systematically over-report WARN findings. This false-positive cascade erodes trust in the audit system — analogous to the 20-30% false positive rate that Agoda Engineering [referenced in rule-enforcement.research] identified as sufficient to cause developer bypass behavior. The full rubric must be presented simultaneously.

**Rubric drift when the audit prompt itself is not locked (T1, RULERS [1]):**

A rule audit prompt is subject to the same instability it was designed to detect. If the audit prompt is stored as a freeform natural language string and edited ad hoc, evaluation results will drift across versions. The same structural discipline (locking, versioning, treating as a frozen specification) that applies to domain rules applies to audit rubrics themselves. This is a meta-recursive requirement: the evaluator of rules must be governed by the same standards as the rules it evaluates.

---

### Sub-question 4: Locked vs. open rubric formats for rule evaluation

**Locked rubrics are superior for rule audit stability; open rubrics are appropriate for rubric generation (T1 [1][8]):**

The RULERS paper [1] establishes that locked rubrics outperform open natural language rubrics for evaluation stability. However, Rethinking Rubric Generation [8] identifies a complementary pattern: rubrics "often lack coverage, conflate dimensions, misalign preference direction, and contain redundant or highly correlated criteria." This creates a tension:

- **Locked rubrics** are needed for stable, repeatable evaluation (the audit phase)
- **Open generation** is needed to produce rubrics that cover the right dimensions (the initial creation phase)

For rule audit prompts specifically, the resolution is:

1. **Fixed evaluation dimensions** (locked): the five dimensions of the check-rule skill (specificity, research grounding, staleness, fix-safety, rubric instability) are frozen and versioned; not generated per-audit
2. **Generated repair recommendations** (open, then constrained): the repair phase produces free-form recommendations that are then validated against the locked repair output schema

This mirrors the RULERS compiler-executor model: the rubric specification is locked; the evaluation itself is constrained decoding; the output is structured.

**Question-specific rubrics outperform question-agnostic rubrics by ~4× on Cohen's Kappa (T1 [2]):**

For rule evaluation, "question-specific" means the evaluation prompt includes the full rule file being evaluated, not a generic rule format template. Evaluation prompts that operate on an abstract "generic rule" rather than the specific rule text being audited produce misaligned verdicts.

> "Existing work focused on question-agnostic rubrics, emphasizing generic criteria such as correctness and syntax across diverse problems, but in reality...human instructors actually use question-specific rubrics."

Applied: every evaluation call must include the specific rule text. Never audit a rule against a generic rubric alone — the rule text must appear verbatim in the prompt.

**AutoRubric's per-criterion atomic evaluation (T1 [7]):**

AutoRubric enforces per-criterion atomic evaluation in separate LLM calls to prevent "halo effects" — the tendency for a positive impression on one dimension to inflate scores on others. However, this conflicts with the finding from [2] that sequential per-criterion calls score 11.5 points lower. The resolution is structural: **atomic evaluation within one call using explicit output slots per dimension**, not sequential calls. AutoRubric's benefit (no halo effects) can be achieved by requiring each dimension to produce evidence and verdict independently within a single multi-dimension prompt.

**Open rubric generation failure modes (T1 [8]):**

Rethinking Rubric Generation identifies five ways auto-generated rubrics fail that are relevant to rule audit prompt design:

1. **Coverage gaps** — generated rubrics miss entire failure categories (e.g., staleness is frequently absent from auto-generated rule rubrics)
2. **Dimension conflation** — two dimensions that should be evaluated independently get merged (e.g., specificity and scope isolation conflated)
3. **Preference direction misalignment** — the rubric identifies a property but flips the scoring direction (penalizing a feature that should be rewarded)
4. **Redundant criteria** — multiple dimensions measure the same property with slight wording variation, inflating WARN counts
5. **Reward hacking risk** — rubrics that can be "satisfied" by surface changes without addressing the underlying issue (e.g., adding a fix-safety field with an empty value)

These five failure modes are why audit rubrics must be authored and locked by practitioners, not auto-generated per rule.

## Challenge

### Assumption Check

**Assumption:** The five evaluation dimensions of the check-rule skill are exhaustive.

**Challenge:** The rule enforcement research [rule-enforcement.research.md] establishes that false positives create a self-reinforcing failure cascade at 20-30% FP rates. The current five dimensions (specificity, research grounding, staleness, fix-safety, rubric instability) do not include a **false-positive risk dimension** — evaluating whether the rule's scope and criterion are likely to fire on correct code. A rule that is structurally complete but fires on 40% of compliant code is harmful despite passing all five dimensions.

**Resolution:** A sixth audit dimension — "false-positive risk" — may be warranted: does the scope glob combined with the criterion produce identifiable false-positive patterns? This is distinct from specificity (which asks whether the criterion is precise) and from staleness (which asks whether examples are current). It asks whether the rule, as written, would fire on code that is actually compliant.

**Assumption:** Repair recommendations can be generated in the same call as evaluation findings.

**Challenge:** The RULERS evidence-anchored scoring model [1] establishes that generating the verdict before the evidence produces confirmation bias. If repair recommendations are generated in the same call as evaluation, the output sequence becomes: evidence → verdict → repair. But repair recommendations require reasoning about the verdict's root cause — which is downstream of the verdict itself. Interleaving repair reasoning into the evaluation call potentially corrupts the evaluation's evidence-anchored structure by introducing future-state (what should be) into the assessment of current-state (what is).

**Resolution:** Repair generation should be a separate call that receives the evaluation output (with evidence and verdict) as input, not a co-located section of the evaluation prompt. This preserves the integrity of evidence-anchored evaluation while enabling high-quality repair output.

### Premortem

**Scenario:** The repair prompt generates technically correct replacements that pass all five audit dimensions, but the repaired rule no longer enforces the original intent.

This is the most dangerous repair failure mode: the rule passes the audit but has been semantically rewritten to be easier to pass rather than to enforce the original constraint. Observed mechanisms:

- **Scope narrowing to avoid staleness findings:** the repair narrows scope from `models/**/*.sql` to `models/staging/**/*.sql` to resolve a staleness finding, but the original rule's intent was to enforce a constraint across all model layers.
- **Example replacement to fix rubric instability:** synthetic examples are replaced with real code examples, but the real code examples are drawn from compliant code and do not illustrate the failure mode clearly.
- **Hedging removal that changes meaning:** hedging language like "usually" is removed from the criterion to satisfy the rubric instability dimension, but "usually" was load-bearing — it acknowledged intentional exceptions.

**Implication:** Repair prompts must include the rule's original intent (from the Intent section) as a constraint on generated repairs: "The proposed repair must preserve the behavioral constraint described in the Intent section. If any repair changes what files are in scope or what behavior is required, flag the change as requiring human review before applying."

## Findings

### SQ1: Evaluation prompt anatomy for reliable rule quality assessment

**Six structural elements are required for stable rule evaluation; the criterion statement is the highest-leverage element (HIGH — T1 converge across [1][2][3][4][9]).**

Evidence from five independent T1 studies converges on six required prompt elements (criterion statement, anchor examples, evidence requirement, binary verdict format, default-closed declaration, scope statement). Removing the criterion statement drops correlation with human judgment by 26% (0.666 → 0.487). Removing anchor examples causes the model to default to PASS. The evidence requirement (evidence before verdict) prevents post-hoc rationalization. Binary formats outperform ordinal scales for compliance decisions. Default-closed handling prevents silent pass-through on borderline cases.

**Evidence-before-verdict ordering is not a stylistic preference — it is a structural requirement (HIGH — T1 [1]).**

Prompts that elicit verdict before evidence produce confirmation bias: the reasoning rationalizes the pre-emitted verdict rather than deriving from evidence. RULERS enforces evidence → reasoning → verdict as a hard constraint. This ordering applies to both rule evaluation prompts and repair generation prompts.

**Full rubric in one call outperforms per-dimension sequential calls by 11.5 points; atomic per-dimension output slots within one call capture both benefits (HIGH — T1 [2]; T1 [7]).**

The penalty for sequential calls is large and documented. AutoRubric's goal (preventing halo effects) can be achieved through separate output slots within one call rather than separate calls. The check-rule skill's instruction to "score all five dimensions in one pass, never split into per-dimension calls" is empirically validated.

---

### SQ2: Repair prompt structure for actionable vs. advisory output

**Actionable repair output requires three elements: specific element to change, proposed replacement verbatim, and evidence that requires the change (MODERATE — T2 Semgrep [15]; T3 Freeplay [13]; consistent with T1 principles).**

Advisory output ("the scope is too broad") does not enable repair. Actionable output identifies the field, provides the replacement value, and cites the evidence that requires it. A structured diff-style output format (CHANGE/FROM/TO/REASON) makes repair mechanically applicable without interpretation.

**Repair generation must be a separate call from evaluation — not co-located in the evaluation prompt (MODERATE — derived from T1 [1] evidence-anchoring principle; no direct empirical study of this specific split).**

Interleaving repair reasoning with evaluation reasoning corrupts the evidence-anchored structure that makes evaluation reliable. The evaluation phase must complete (producing evidence → verdict per dimension) before repair generation begins. This is a structural inference from RULERS rather than a directly studied finding — flag for validation.

**The full rule file verbatim must appear in both the evaluation and repair prompts (HIGH — T1 [2]).**

Summarizing or paraphrasing the rule for either evaluation or repair generates misaligned output. Question-specific rubrics (which include the full artifact being evaluated) outperform question-agnostic rubrics by ~4× on Cohen's Kappa. The repair prompt must include the full original rule, the evaluation findings with evidence, and the repair schema constraint.

**Repair prompts must include an intent-preservation constraint (MODERATE — derived from premortem analysis; no direct empirical study).**

Without an explicit constraint that repairs must preserve the original behavioral intent, repair generation will optimize for passing the audit dimensions rather than preserving enforcement correctness. This is particularly risky for staleness and rubric instability findings, where the easiest "repair" may narrow scope or swap examples in ways that undermine the rule's original purpose.

---

### SQ3: Meta-evaluation failure modes

**Style-over-substance bias is the dominant meta-evaluation failure and must be actively counteracted (HIGH — T1 [11]).**

At the meta level, well-formatted but structurally broken rules receive false PASS verdicts. Audit prompts must include explicit negative anchors for fluency-but-broken patterns. The evidence requirement (demanding quoted evidence before verdict) is the primary mitigating structure — it forces engagement with content rather than surface presentation.

**False-positive cascade from sequential per-dimension calls is the most operationally dangerous failure mode (HIGH — T1 [2]).**

An audit system that makes separate calls per dimension will systematically over-report WARN findings (scoring 11.5 points lower than simultaneous rubric evaluation). At 20-30% false positive rates, rule enforcement systems enter a trust-degradation spiral. This makes the single-call constraint not just an efficiency choice but a quality imperative.

**Audit rubrics are subject to the same instability they detect and must be locked (HIGH — T1 [1]).**

The audit rubric is itself a prompt artifact. If it is edited ad hoc, evaluation results drift across versions. The five audit dimensions must be versioned and frozen — treated as locked specifications, not living documents. This is a meta-recursive application of the primary finding from RULERS.

---

### SQ4: Locked vs. open rubric formats

**Locked rubric for evaluation dimensions; open generation for repair recommendations; structured constraint on repair output format (HIGH — T1 synthesis [1][7][8]).**

The empirical evidence supports a three-layer model: (1) audit dimensions are locked and versioned by practitioners, never auto-generated; (2) repair recommendations are generated per-finding, but constrained to a structured schema; (3) the generated repair output is validated against the locked repair schema before being presented to the author. This mirrors the RULERS compiler-executor model applied to the rule lifecycle.

**Five failure modes of auto-generated rubrics must be guarded against in audit dimension design: coverage gaps, dimension conflation, preference direction misalignment, redundant criteria, and reward hacking (HIGH — T1 [8]).**

These failure modes appear in auto-generated rubrics and must be avoided when authoring locked audit dimensions. Coverage gaps (missing the staleness dimension entirely) are particularly common. Dimension conflation (merging specificity with scope isolation) produces audit rubrics that cannot distinguish two distinct failure types. Reward hacking risk (adding an empty fix-safety field to pass the audit) requires the audit rubric to check for meaningful values, not mere presence.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Evidence-before-verdict ordering prevents confirmation bias in evaluation prompts | structural | [1] RULERS | verified — RULERS framework; widely supported by evaluation literature |
| 2 | Removing criterion statements from evaluation prompts drops human correlation from 0.666 to 0.487 | empirical | [9] empirical study | verified (preprint, not peer-reviewed) |
| 3 | Per-dimension sequential calls score 11.5 points lower than simultaneous rubric evaluation | empirical | [2] Rubric Is All You Need | verified (preprint, not peer-reviewed) |
| 4 | Question-specific rubrics outperform question-agnostic rubrics by ~4× on Cohen's Kappa | empirical | [2] | verified (preprint; OOP programming domain; generalizability uncertain) |
| 5 | Style-over-substance bias causes LLM judges to prioritize fluency over structural correctness | empirical | [11] Feuer et al. | verified (ICLR 2025; specifically tested in alignment benchmarking context) |
| 6 | False positives at 20-30% rates produce trust-degradation cascades in rule enforcement systems | empirical | rule-enforcement.research.md (Agoda) | verified (T2 practitioner, not experimental) |
| 7 | Locked rubrics outperform open rubrics by +0.17 QWK on human agreement | empirical | [1] RULERS | verified (preprint, single study) |
| 8 | Repair generation should be a separate call from evaluation | structural inference | [1] RULERS principle | human-review — derived from evidence-anchoring principle, not directly tested |
| 9 | Repair prompts must include an intent-preservation constraint to prevent scope-narrowing repair | structural inference | premortem analysis | human-review — no empirical study; derived from linter false-positive literature |
| 10 | Auto-generated audit rubrics produce coverage gaps, dimension conflation, and reward hacking risk | empirical | [8] Rethinking Rubric Generation | verified (preprint; rubric generation in reward modeling context) |

## Search Protocol

<!-- search-protocol
{"entries": [
  {"query": "LLM evaluation prompt anatomy rubric structure elements reliability 2025 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 4},
  {"query": "rule repair evaluation prompt LLM automatic rule fixing correction feedback 2024 2025", "source": "google", "date_range": "2024-2026", "results_found": 8, "results_used": 2},
  {"query": "meta-evaluation LLM judge evaluating prompts rubrics auditing instruction quality 2025 2026", "source": "google", "date_range": "2024-2026", "results_found": 7, "results_used": 3},
  {"query": "locked rubric vs open rubric LLM evaluation comparison empirical 2025 2026", "source": "google", "date_range": "2024-2026", "results_found": 9, "results_used": 3},
  {"query": "actionable vs advisory LLM repair recommendation output format structured diff 2025", "source": "google", "date_range": "2024-2026", "results_found": 5, "results_used": 1},
  {"query": "RULERS locked rubric evidence anchored scoring LLM evaluation Hong 2026", "source": "google", "date_range": "2025-2026", "results_found": 6, "results_used": 1}
], "not_searched": [
  "deepwiki LLM evaluation meta-prompting — not sufficient surface coverage for meta-evaluation failure modes",
  "GitHub Issues for eval frameworks — covered by existing llm-as-judge.research.md"
]}
-->
