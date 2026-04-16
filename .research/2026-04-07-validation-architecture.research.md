---
name: "Validation Architecture & Structural Checks"
description: "Composable validation pipelines work best when deterministic structural checks gate expensive LLM-quality checks, with a two-to-four level severity model and reads-only query functions cleanly separated from mutating fix operations."
type: research
sources:
  - https://www.hebbia.com/blog/evaluating-ai-agents-a-hybrid-deterministic-and-rubric-based-framework
  - https://eslint.org/docs/latest/contribute/architecture/
  - https://arxiv.org/html/2601.18827
  - https://github.com/mlflow/mlflow/issues/20827
  - https://docs.greatexpectations.io/docs/reference/api/core/expectationsuitevalidationresult_class/
  - https://openai.github.io/openai-agents-python/guardrails/
  - https://fsharpforfunandprofit.com/rop/
  - https://arxiv.org/html/2603.07019
  - https://semgrep.dev/docs/kb/rules/understand-severities
  - https://rustc-dev-guide.rust-lang.org/diagnostics.html
  - https://oneuptime.com/blog/post/2026-01-25-data-validation-framework-python/view
  - https://dev.to/teppana88/how-i-validate-quality-when-ai-agents-write-my-code-481c
  - https://www.guardrailsai.com/docs/getting_started/quickstart
  - https://martinfowler.com/bliki/CQRS.html
  - https://www.javacodegeeks.com/2025/12/the-cqrs-pattern-separating-reads-from-writes-for-scalable-architectures.html
  - https://arxiv.org/html/2510.03469v1
  - https://blog.logrocket.com/what-is-railway-oriented-programming/
  - https://docs.greatexpectations.io/docs/cloud/expectations/expectations_overview/
  - https://khalilstemmler.com/articles/oop-design-principles/command-query-separation/
related:
---

## Summary

Validation for agent/LLM developer tools is best structured as a two-tier pipeline: deterministic structural checks (schema, field presence, format) run first and gate expensive LLM-quality checks, which assess semantic properties like coherence and completeness. The dominant severity models across mature tooling (Rust, ESLint, Great Expectations, Semgrep) converge on three-to-four levels (error/fail, warn, info/note) with the fail tier blocking execution and warn tier accumulating for report. Reads-vs-writes separation (CQS/CQRS) directly maps onto validation architecture: query functions observe and return issue lists without side effects; fix/mutate operations are explicit, separate commands.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.hebbia.com/blog/evaluating-ai-agents-a-hybrid-deterministic-and-rubric-based-framework | Evaluating AI Agents: A Hybrid Deterministic and Rubric-Based Framework | Hebbia | 2025 | T4 | verified |
| 2 | https://eslint.org/docs/latest/contribute/architecture/ | ESLint Architecture | ESLint | 2025 | T1 | verified |
| 3 | https://arxiv.org/html/2601.18827 | Automated Structural Testing of LLM-Based Agents | arXiv | Jan 2026 | T3 | verified |
| 4 | https://github.com/mlflow/mlflow/issues/20827 | Built-in Tier 1 Deterministic Scorers (Feature Request) | MLflow / GitHub | 2025 | T1 | verified |
| 5 | https://docs.greatexpectations.io/docs/reference/api/core/expectationsuitevalidationresult_class/ | ExpectationSuiteValidationResult | Great Expectations | 2025 | T1 | verified |
| 6 | https://openai.github.io/openai-agents-python/guardrails/ | Guardrails — OpenAI Agents SDK | OpenAI | 2025 | T1 | verified |
| 7 | https://fsharpforfunandprofit.com/rop/ | Railway Oriented Programming | F# for Fun and Profit | 2013 (foundational) | T4 | verified |
| 8 | https://arxiv.org/html/2603.07019 | AutoChecklist: Composable Pipelines for Checklist Generation and Scoring with LLM-as-a-Judge | arXiv / U. Chicago | Mar 2026 | T3 | verified |
| 9 | https://semgrep.dev/docs/kb/rules/understand-severities | How Does Semgrep Assign Severity Levels? | Semgrep | 2025 | T1 | verified |
| 10 | https://rustc-dev-guide.rust-lang.org/diagnostics.html | Errors and Lints — Rust Compiler Development Guide | Rust Project | 2025 | T1 | verified |
| 11 | https://oneuptime.com/blog/post/2026-01-25-data-validation-framework-python/view | How to Build a Data Validation Framework in Python | OneUptime | Jan 2026 | T4 | verified |
| 12 | https://dev.to/teppana88/how-i-validate-quality-when-ai-agents-write-my-code-481c | How I Validate Quality When AI Agents Write My Code | Teppana88 / DEV Community | 2025 | T5 | verified |
| 13 | https://www.guardrailsai.com/docs/getting_started/quickstart | Guardrails AI Quickstart | Guardrails AI | 2025 | T1 | verified |
| 14 | https://martinfowler.com/bliki/CQRS.html | CQRS | Martin Fowler | 2011 (foundational) | T3 | verified |
| 15 | https://www.javacodegeeks.com/2025/12/the-cqrs-pattern-separating-reads-from-writes-for-scalable-architectures.html | The CQRS Pattern: Separating Reads from Writes for Scalable Architectures | Java Code Geeks | Dec 2025 | T4 | verified |
| 16 | https://arxiv.org/html/2510.03469v1 | Bridging LLM Planning Agents and Formal Methods: A Case Study in Plan Verification | arXiv | Oct 2025 | T3 | verified |
| 17 | https://blog.logrocket.com/what-is-railway-oriented-programming/ | What is Railway Oriented Programming? | LogRocket | 2025 | T4 | verified |
| 18 | https://docs.greatexpectations.io/docs/cloud/expectations/expectations_overview/ | Expectations Overview | Great Expectations | 2025 | T1 | verified |
| 19 | https://khalilstemmler.com/articles/oop-design-principles/command-query-separation/ | Command Query Separation | Khalil Stemmler | 2019 (foundational) | T4 | verified |

## Extracts

### Sub-question 1: How should validation be separated into structural (deterministic) and quality (LLM-driven) checks?

The clearest production framing comes from Hebbia's hybrid framework [1]: "Deterministic checks handle verifiable properties of agent outputs such as schema validation, required field presence, data type correctness, and formatting compliance to produce fast, reliable, and consistent results," while "rubric-based evaluations by LLMs assess... properties like coherence, completeness, and domain-appropriateness." The key implementation consequence is that Tier 1 should gate Tier 2: "If JsonValidity fails, there's no point calling openai:/gpt-4 to judge 'correctness' on garbage output."

The MLflow feature request [4] formalizes this into an eight-scorer Tier 1 set (ExactMatch, JsonValidity, RegexMatch, ContainsKeywords, LengthBound, IsNotEmpty, LatencyThreshold, NumericBound) designed to be "Free — no LLM API calls, Instant — microseconds, not seconds, Reproducible — identical results every run." The proposed `gate=True` mechanism short-circuits Tier 2 evaluation on structural failure, with explicit cost savings: "At 1,000 eval rows × 5 LLM judges × $0.01/call, even a 20% structural failure rate saves $100/run."

The arxiv structural testing paper [3] makes the separation concrete for agent testing: structural assertions verify "tool invocations, parameter passing, execution sequences, and state transitions" via OpenTelemetry traces — deliberately bypassing semantic evaluation. The paper notes: "no need to test the agent's text response, since we test if right tools were invoked." This bypasses the "LLM-as-judge" reliability problem for properties that can be checked deterministically.

For LLM planning agents, the formal methods case study [16] confirms that "a robust design paradigm involves using LLMs to translate natural language into structured representations, followed by classical deterministic AI techniques for reasoning, leveraging LLM strengths in translation and structuring while using deterministic methods for verification guarantees."

The separation pattern is also present in LLM output validation tooling. Guardrails AI [13] implements a two-path design: structural validation via Pydantic BaseModel schema enforcement; semantic validation through installable validators (PII detection, regex matching, toxicity scoring). The Guard composes both, executing validators sequentially and surfacing a `validation_passed` boolean.

### Sub-question 2: What patterns exist for composable validation pipelines (check functions returning issue lists)?

**ESLint rule model [2]:** ESLint's architecture is the canonical composable linting design. Rules are stateless — they "inspect AST nodes and report warnings only, with no direct file system access or asynchronous operations permitted." Rules attach to events in an AST traversal and emit issues into a shared result list. The CLI, CLIEngine, and Linter are layered: CLI handles I/O; Linter performs verification with no file system access. This separation makes the core independently testable and programmatically embeddable.

**Composable validator interface [11]:** A common Python pattern uses an abstract base class where each rule implements `validate(value, context) -> Optional[ValidationError]`. Results merge via accumulation: `ValidationResult(errors=self.errors + other.errors)`. This enables validators to compose into suites with a single `is_valid` flag derived from all sub-results.

**AutoChecklist Generator → Refiner → Scorer [8]:** The 2026 AutoChecklist library formalizes composable LLM evaluation pipelines. "Any generator can be paired with any scorer, and refiners compose in sequence." Five generator strategies (Direct, Contrastive, Inductive, Deductive, Interactive) pair with three scoring modes (pass rate, weighted, normalized). New configurations register via Markdown prompt templates alone, without modifying library code. This demonstrates that quality-check pipelines can be as composable as structural-check pipelines.

**Railway Oriented Programming / error accumulation [7, 17]:** ROP provides the theoretical foundation for validation pipelines that collect all errors rather than failing fast. The `Sequence` method enables "Success([values]) or Failure with SubErrors containing each individual failure." The `&&&` operator runs validators in parallel on the same input, useful for checking multiple fields simultaneously. ROP's constraint is that the composition pattern is uniform — "basically only one way to write the code" — which enforces consistency across a pipeline.

**Multi-agent gate pipeline [12]:** Practical multi-agent validation uses sequential independent gates (requirements → architecture → implementation → code validator → multi-agent review → CI → human → deployment), each with distinct responsibilities. Parallel specialization runs four agents simultaneously on the same artifact with different foci (architecture compliance, bugs, security, E2E tests). Confidence scoring (>= 75 threshold) filters noise before reporting.

**Great Expectations ExpectationSuite [5, 18]:** GX organizes checks as declarative Expectations composed into Suites. The `ExpectationSuiteValidationResult` container collects individual `ExpectationValidationResult` instances, aggregates statistics, and exposes a `get_max_severity_failure()` method for gating decisions. Each Expectation carries a severity (critical, warning, info), and the suite can trigger downstream Actions based on the maximum severity encountered.

### Sub-question 3: How do reads-vs-writes separation patterns (CQS/CQRS) apply to agent validation systems?

**CQS foundation [19, 14]:** Bertrand Meyer's original CQS principle — "every method should either be a command that performs an action, or a query that returns data to the caller, but not both" — maps directly onto validation design. Validators are pure queries: they observe state and return issue lists without mutating anything. Fix operations are separate commands. Fowler's CQRS bliki [14] extends this to services: "you can use a different model to update information than the model you use to read information."

**Direct mapping to validation [15]:** In CQRS-influenced validation, the write side "focus[es] on enforcing business rules and maintaining consistency," while the read/query side optimizes for speed. For developer tools, this means audit functions are read-only reporters — they can be memoized, parallelized, and run in CI without side effects. Fix functions are explicit commands that change state and require separate invocation.

**Agent-specific application [3, 4]:** Structural testing of LLM agents via OpenTelemetry traces is inherently a query operation: the test framework observes trace data (spans, attributes, sequences) and asserts against it without modifying agent behavior. The MLflow Tier 1 scorer design aligns: scorers are pure functions returning `Feedback` objects with human-readable rationale, never mutating the system under evaluation.

**AI SQL agent pattern [from web search]:** Production AI SQL agents enforce CQS at the guardrail level: "every LLM-generated query must be treated as untrusted input and validated before execution, introducing deterministic, server-side guardrails that enforce read-only access, block dangerous operations, and apply role-based rules regardless of what the model generates." This implements CQS as a safety invariant, not just a design preference.

**OpenAI Agents SDK guardrails [6]:** Input and output guardrails are stateless validators that examine data and return a `GuardrailFunctionOutput` with a `tripwire_triggered` boolean. They do not modify the agent state — they observe and report, with the orchestrator handling mutation (halting execution) when the tripwire fires. Tool guardrails extend this to the tool boundary: validating input before invocation and output after, without the guardrail itself causing side effects.

### Sub-question 4: What severity models (warn/fail, multi-level) work best for developer-facing validation?

**Rust's four-tier model [10]:** The Rust compiler's diagnostic system is the most granular reference implementation: Error (blocks compilation), Warning (informational but actionable), Note (contextual support for errors/warnings), Help (actionable fix suggestions). The lint subsystem adds a configurable layer — Forbid/Deny/Warn/Allow — separating policy decisions from hard errors. This prevents "warning fatigue" by reserving warnings for situations "where the user _should_ take action" or code that is "very likely to be incorrect."

**Great Expectations three-tier model [5, 18]:** GX uses Critical > Warning > Info with explicit ordering. Execution failures always escalate to Critical regardless of configured severity. The `get_max_severity_failure()` method enables threshold-based gating: downstream systems can block on Critical, report on Warning, and log Info. Default severity is Warning for generated expectations; Critical if unspecified.

**Semgrep's four-tier model [9]:** Semgrep defines Critical, High, Medium, Low (with deprecated ERROR/WARNING/INFO mapping to High/Medium/Low). Supply Chain severity derives from external CVSS scores rather than author judgment. A separate "confidence" dimension (distinct from severity) captures the rule's accuracy/false-positive characteristics, preventing conflation of "how bad is this?" with "how certain are we?"

**Hebbia's required/additional binary [1]:** For LLM quality evaluation, Hebbia uses a two-level model: Required criteria (SLAs that must pass) and Additional criteria (aspirational quality above the minimum). This avoids the problem of trying to assign numeric severity to LLM judgment outputs and creates a clear "pass/fail on contract" vs. "measure quality improvement" distinction.

**Agent multi-gate confidence scoring [12]:** In multi-agent validation pipelines, a confidence score (0–100) with a threshold (>= 75 to report) replaces traditional severity levels. This addresses the non-determinism of LLM-based checks: "No evidence, no report" prevents LLM validators from blocking on speculation.

**Practical convergence:** Across mature tools, the effective minimum is a two-level model (fail/warn) where fail blocks execution and warn accumulates for report. The warn level is the escape hatch that prevents alert fatigue from opinionated or heuristic checks. Multi-level models (3–4 tiers) add an info/note tier for context-only diagnostics and optionally a separate "confidence" dimension. Conflating severity (impact) with confidence (certainty) is a common design error that Semgrep explicitly avoids.

## Search Protocol

| # | Query | Engine | Results |
|---|-------|--------|---------|
| 1 | composable validation pipeline patterns check functions returning issue lists 2025 | WebSearch | 10 results; arxiv AutoChecklist, Databricks expectations, ETL patterns |
| 2 | CQS CQRS command query separation validation agent systems 2025 | WebSearch | 10 results; Fowler CQRS bliki, cosmicpython, Wikipedia, kurrent.io |
| 3 | linting tool severity model warn error fail developer tools design 2025 | WebSearch | 10 results; Rust diagnostics, Android lint, Baeldung, ESLint |
| 4 | LLM agent validation architecture structural vs semantic checks 2025 | WebSearch | 10 results; arxiv structural testing, Hebbia hybrid framework, Berkeley tech report |
| 5 | ESLint plugin architecture rule severity composable validator design pattern | WebSearch | 10 results; ESLint architecture docs, plugin boundaries, hexagonal architecture |
| 6 | read-only query vs mutating command separation validation developer tooling agent 2025 | WebSearch | 10 results; CQRS patterns, AI SQL agent validation, Confluent CQRS |
| 7 | deterministic structural checks vs LLM quality checks hybrid validation architecture 2025 2026 | WebSearch | 10 results; MLflow issue #20827, Hebbia, Rethinking Testing for LLM Apps |
| 8 | pytest ruff mypy validation pipeline architecture multi-severity linting 2025 | WebSearch | 10 results; Ruff architecture, pytest-ruff, LSP aggregator pattern |
| 9 | Great Expectations "expectation suite" validation result severity level architecture 2025 | WebSearch | 10 results; GX API docs, trivago hybrid environments, DataCamp tutorial |
| 10 | OpenTelemetry agent validation structural invariants trace assertions 2025 | WebSearch | 10 results; arxiv structural testing of LLM agents, OpenTelemetry AI agent observability |
| 11 | Semgrep rule architecture check registry composable validation severity 2025 | WebSearch | 10 results; Semgrep severity KB, rule syntax, policy management |
| 12 | "validation as code" agent framework "structural check" "quality check" separation pattern 2025 2026 | WebSearch | 10 results; DEV Community AI agent validation, InfoQ PDCA, qodo code quality |
| 13 | railway oriented programming validation "error accumulation" "collect all errors" pipeline 2025 | WebSearch | 10 results; F# for Fun and Profit ROP, LogRocket, Kotlin Baeldung |
| 14 | agent guardrails OpenAI SDK input validation output validation architecture pattern 2025 | WebSearch | 10 results; OpenAI Agents SDK guardrails docs, Towards Data Science guardrails, appsecsanta |
| 15 | AutoChecklist composable LLM judge pipeline generator scorer 2025 arxiv | WebSearch | 10 results; arxiv 2603.07019, Langfuse LLM-as-Judge, evidentlyai guide |
| 16 | Guardrails AI validation framework structural semantic check NLP output 2025 | WebSearch | 10 results; guardrails-ai GitHub, guardrailsai.com docs, patronus.ai |
| 17 | Pydantic v2 validation pipeline composable validators severity levels architecture 2025 | WebSearch | 10 results; Pydantic validators docs, PydanticAI bixtech, experimental pipeline API |
| 18 | WebFetch: Hebbia hybrid evaluation blog | WebFetch | Full content extracted; hybrid tier architecture, required/additional severity model |
| 19 | WebFetch: ESLint architecture docs | WebFetch | Full content extracted; rule visitor pattern, layered pipeline CLI→Linter |
| 20 | WebFetch: arxiv 2601.18827 structural testing of LLM agents | WebFetch | Full content extracted; trace-based assertions, structural vs. semantic separation |
| 21 | WebFetch: MLflow issue #20827 Tier 1 scorers | WebFetch | Full content extracted; 8 built-in scorers, gate mechanism, cost rationale |
| 22 | WebFetch: Great Expectations ValidationResult class API | WebFetch | Full content extracted; CRITICAL > WARNING > INFO ordering, get_max_severity_failure |
| 23 | WebFetch: OpenAI Agents SDK guardrails | WebFetch | Full content extracted; tripwire mechanism, parallel vs. blocking modes, tool guardrails |
| 24 | WebFetch: F# for Fun and Profit ROP | WebFetch | Full content extracted; error accumulation, &&& operator, Kleisli composition |
| 25 | WebFetch: arxiv 2603.07019 AutoChecklist | WebFetch | Full content extracted; Generator→Refiner→Scorer pipeline, five strategies, unified scorer |
| 26 | WebFetch: Semgrep severity KB | WebFetch | Full content extracted; Critical/High/Medium/Low, confidence vs. severity distinction |
| 27 | WebFetch: Rust compiler diagnostics guide | WebFetch | Full content extracted; 4-tier diagnostic model, lint pass structure, "warning fatigue" avoidance |
| 28 | WebFetch: OneUptime Python validation framework | WebFetch | Full content extracted; ValidationRule ABC, ERROR/WARNING/INFO tiers, merge pattern |
| 29 | WebFetch: DEV Community AI agent validation | WebFetch | Full content extracted; multi-gate pipeline, confidence threshold filtering, parallel specialization |
| 30 | WebFetch: Guardrails AI quickstart | WebFetch | Full content extracted; validator composition via Guard, structural vs. semantic path |

## Challenge

### Claims Examined

| # | Claim | Challenge | Verdict |
|---|-------|-----------|---------|
| 1 | "Deterministic checks handle verifiable properties… structural checks gate expensive LLM-quality checks" — structural checks always run first and gate LLM checks | In content-routing and intent-triage architectures, a lightweight LLM classifier must run *before* structural validation to determine which schema or rule set to apply. Leanware's 2025 LLM guardrails guide describes risk-based routing: "dynamically adjusting guardrail intensity based on query characteristics," where the router is itself an LLM call preceding any structural check. Guardrails AI documentation confirms fast LLM validators (toxicity, PII) run on input *before* structured-output schema enforcement on the response. The draft's framing is correct for single-schema pipelines but does not generalise to multi-schema or routing contexts. | qualified |
| 2 | CQS/CQRS "maps directly onto validation design… validators are pure queries… fix operations are separate commands" | Two qualifications erode the clean mapping. First, practical validators routinely produce audit-log side effects. Ploeh (2015) acknowledges this directly: "A Query may cause a side-effect to happen (such as an audit record being written), but that side-effect doesn't concern the client." He concludes CQS "applies at the source code level" but "all applications must have a boundary where… CQS doesn't apply." Second, CQRS is broadly acknowledged as overkill for simple domains — "CQRS is overkill for 90% of backends" (The Atomic Architect, 2025) — with Netflix cited as having abandoned it in favour of simpler architectures. For developer-tool validators that neither face high-concurrency write/read scale nor distributed teams, projecting CQRS framing onto a local list-returning function provides conceptual clarity but no structural enforcement: nothing in Python or other common validator implementations prevents a "query" function from mutating state. | qualified |
| 3 | "Across mature tools, the effective minimum is a two-level model (fail/warn)… the warn level is the escape hatch that prevents alert fatigue" | In practice, the warn tier is itself a known source of alert fatigue rather than a remedy for it. Thomas Junghans's widely-cited ESLint piece states: "Warnings are overlooked and bloat your terminal. Either use the `error` or `off` severity for all rules." The ESLint team's own GitHub discussions show persistent community pressure to treat `warn` as equivalent to `error` (via `--max-warnings 0`) because warnings accumulate without being addressed. The draft presents warn as the solution to alert fatigue, but real-world evidence from ESLint's own ecosystem shows warn creates a second fatigue problem — a category of issues developers are conditioned to ignore. The claim stands as design intent; it is qualified because the mechanism that is supposed to prevent fatigue is empirically the same mechanism that causes it if not actively enforced. | qualified |
| 4 | Severity models from traditional tools (Rust, ESLint, Semgrep) are transferable to LLM-based validation | Traditional severity tiers assume deterministic, reproducible checks: the same input always produces the same severity output. LLM-as-a-judge systems violate this assumption. A 2025 arXiv paper ("Validating LLM-as-a-Judge Systems under Rating Indeterminacy," arXiv 2503.05965) finds that "differences in how humans and LLMs resolve rating indeterminacy… can heavily bias LLM-as-a-judge validation" and that standard forced-choice severity assignment selects judge systems that perform "as much as 31% worse" than alternative methods. The same evaluation run on the same artifact can yield different severity labels across invocations. The draft acknowledges non-determinism in the confidence-score discussion (Section 4) but treats the severity frameworks as directly portable; the evidence indicates they require structural adaptation (e.g., multi-sample aggregation, soft thresholds) before applying to LLM-based checks. | qualified |

### Gaps Identified

- **Ordering under multi-schema routing:** The draft assumes a single known schema governs what "structural" means. In systems where a lightweight model first classifies input type (and thus selects which schema to validate against), the two-tier ordering inverts for that first step. No source in the draft addresses this case.
- **Enforcement mechanism for the warn tier:** The draft recommends warn as an alert-fatigue escape valve but does not address how to prevent warn accumulation from becoming its own fatigue source. Tools like `--max-warnings 0` (ESLint), dbt's `warn_if` / `error_if` thresholds, and Rust's `#[deny(warnings)]` gate exist for this; none are discussed.
- **Stateful validators and invalidation caching:** Both the CQS and composability sections assume validators are stateless functions. Real pipelines often cache validation results for performance, but a cached result may be stale if upstream state changes. Neither ROP nor the ESLint rule model addresses cache invalidation for long-running pipelines.
- **Team and project scale sensitivity:** The CQRS framing is designed for distributed, high-concurrency systems. For single-process developer tools (the domain of this research), applying CQRS vocabulary to local list-returning functions may add conceptual weight without structural benefit. This scale mismatch is not discussed.
- **LLM judge calibration for severity assignment:** The draft notes Semgrep's confidence-vs-severity distinction but does not address how to calibrate an LLM judge's severity outputs to align with a fixed severity taxonomy. The arXiv 2503.05965 finding that forced-choice severity rating is systematically biased implies calibration is non-trivial.

### Additional Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| A1 | https://medium.com/@tangiblej/you-might-as-well-not-use-eslints-warning-severity-warnings-will-get-ignored-38d52848238e | You might as well not use ESLint's Warning Severity | Thomas Junghans / Medium | 2023 | T5 | confirmed |
| A2 | https://arxiv.org/abs/2503.05965 | Validating LLM-as-a-Judge Systems under Rating Indeterminacy | arXiv | Mar 2025 | T3 | confirmed |
| A3 | https://blog.ploeh.dk/2015/09/23/applications-and-their-side-effects/ | Applications and their side effects | Mark Seemann (ploeh) | 2015 (foundational) | T4 | confirmed |
| A4 | https://medium.com/@the_atomic_architect/cqrs-is-overkill-for-90-of-backends-here-is-the-10-worth-it-ae805296d1ce | CQRS Is Overkill For 90% Of Backends | The Atomic Architect / Medium | 2025 | T5 | confirmed |
| A5 | https://python.useinstructor.com/blog/2025/05/20/understanding-semantic-validation-with-structured-outputs/ | Understanding Semantic Validation with Structured Outputs | Instructor / useinstructor.com | May 2025 | T4 | confirmed |
| A6 | https://www.leanware.co/insights/llm-guardrails | LLM Guardrails: Strategies & Best Practices in 2025 | Leanware | 2025 | T4 | confirmed |

## Findings

### How should validation be separated into structural (deterministic) and quality (LLM-driven) checks?

Structural checks should gate LLM-quality checks in single-schema pipelines. Multiple sources converge on a two-tier architecture: deterministic checks (schema validation, field presence, format, type correctness) run first and short-circuit LLM-quality evaluation on structural failure [1][4][16]. The cost argument is concrete — MLflow's analysis shows even a 20% structural failure rate at 1,000 rows × 5 LLM judges × $0.01/call saves $100/run [4]. The arXiv structural testing paper confirms the separation at the testing layer: structural assertions via OpenTelemetry traces verify tool invocations and parameter passing without touching semantic content [3]. (HIGH — T1 + T3 + T4 sources converge)

The ordering inverts in multi-schema routing contexts. When a lightweight LLM classifier must determine which schema applies before validation can begin, the LLM call necessarily precedes structural checks — this is the standard pattern for content-routing and intent-triage pipelines [A6][13]. The two-tier model holds; only the execution order flips for that routing step. (MODERATE — T4 sources only)

**Counter-evidence:** The challenge found no sources that dispute the two-tier separation itself. The qualification is scope: the pattern is for single-schema output validation, not for systems that must classify input type before any schema applies.

Canonical implementations: Guardrails AI [13] (Pydantic BaseModel for structural, installable validators for semantic); OpenAI Agents SDK [6] (input guardrails gate output guardrails); ESLint [2] (parse-error short-circuit before rule-level checks).

### What patterns exist for composable validation pipelines?

The canonical pattern across all mature tools is **stateless check functions returning issue lists, composed via a shared result accumulator** [2][11][7]. Three convergent implementations:

1. **ESLint rule model [2]**: Stateless rules attach to AST traversal events and emit issues into a shared result list. No direct file system access or async operations permitted. The CLI, CLIEngine, and Linter are layered — CLI handles I/O; Linter performs verification. This makes the core independently testable and embeddable. (HIGH — T1 official docs)

2. **Python ABC accumulator pattern [11]**: `validate(value, context) -> Optional[ValidationError]`, merged via `ValidationResult(errors=self.errors + other.errors)`. Each rule is independently testable; suites compose via accumulation. (MODERATE — T4 vendor blog, no peer review)

3. **Railway Oriented Programming [7][17]**: Provides the theoretical foundation for "collect all errors" rather than fail-fast. The `Sequence` method collects all individual failures; `&&&` runs validators in parallel on the same input. ROP's constraint — one uniform composition pattern — enforces consistency at scale. (MODERATE — T4 foundational, widely cited)

LLM-based quality checks can be equally composable. AutoChecklist (Mar 2026 arXiv) [8] shows: Generator → Refiner → Scorer, where any generator pairs with any scorer, refiners compose in sequence, new configurations register via Markdown prompt templates without modifying library code. (MODERATE — T3 preprint, not peer-reviewed)

### How do CQS/CQRS apply to agent validation systems?

**The conceptual mapping is sound; the practical scope is narrow.** Validators should be pure query functions — observe and return issue lists, no mutation. Fix operations are separate explicit commands [14][19]. The OpenAI Agents SDK [6] implements this cleanly: `GuardrailFunctionOutput` observes and reports; the orchestrator handles mutation (halting execution) when the tripwire fires.

The mapping holds as design vocabulary and as a naming/organizational convention. It breaks at two real-world boundaries:

- **Audit log side effects**: Validators that write audit records technically violate pure CQS, but Ploeh (2015) [A3] classifies these as "ignorable" side effects that don't concern the caller. The pragmatic rule: validators should not mutate the artifact under validation, but may emit observability data. (MODERATE — T4 foundational only)
- **CQRS is overkill for local tools**: CQRS was designed for distributed, high-concurrency systems with separate read/write stores. For single-process developer tools, applying CQRS vocabulary to list-returning functions provides useful conceptual framing but no structural enforcement — nothing in Python prevents a "query" function from mutating state [A4]. The framing is a design convention, not a constraint. (HIGH — consistent practitioner consensus across T4/T5)

### What severity models work best for developer-facing validation?

**For deterministic validators: 3 tiers (fail / warn / info) with explicit warn enforcement.** For LLM-based quality checks: required/additional binary or confidence-threshold scoring.

Mature deterministic tools converge on 3–4 tiers: Rust uses Error / Warning / Note / Help [10]; Great Expectations uses Critical / Warning / Info [5][18]; Semgrep uses Critical / High / Medium / Low [9]. The minimum viable model is fail (blocks execution) + warn (accumulates for report). The info/note tier adds context-only diagnostics that don't require action. (HIGH — T1 sources converge)

**Critical design distinction: severity ≠ confidence.** Semgrep [9] explicitly separates severity (how bad is this?) from confidence (how certain are we?). Conflating these produces false positives in the blocking tier — a high-severity but low-confidence finding that blocks CI erodes trust in the entire system.

**The warn tier trap**: The warn level is the intended escape valve for alert fatigue, but is itself a documented source of fatigue in practice. Thomas Junghans's widely-cited ESLint analysis [A1] finds warnings are routinely ignored, recommending `error` or `off` only. The mitigation is active enforcement: `--max-warnings 0` (ESLint), `#[deny(warnings)]` (Rust), `warn_if`/`error_if` thresholds (dbt). Without enforcement, warn becomes a category developers are conditioned to ignore. (HIGH — T1 ESLint ecosystem + T5 practitioner evidence)

For LLM-based quality checks, traditional severity tiers don't transfer directly. arXiv 2503.05965 [A2] finds forced-choice severity assignment by LLM judges is systematically biased, selecting judge systems performing up to 31% worse than alternatives. Recommended approach: Hebbia's required/additional binary [1] (required criteria are SLAs that must pass; additional criteria measure quality improvement) or confidence-threshold scoring [12] rather than severity tiers. (MODERATE — T3 preprint + T4 vendor)

## Takeaways

1. **Structure gates quality.** Structural (deterministic) checks run first and gate LLM-quality checks. The ordering inverts only in multi-schema routing contexts where an LLM classifier must first determine which schema applies.

2. **Composability pattern: stateless + accumulator.** Each check function is stateless, takes input, returns issues. Compose by merging issue lists. ESLint is the canonical reference; Railway Oriented Programming provides the theoretical foundation for collecting all errors rather than failing fast.

3. **CQS as convention, not constraint.** Validators-as-pure-queries is sound design vocabulary and worth enforcing through code review, but Python provides no structural mechanism. The practical rule: validators must not mutate the artifact under validation; emitting audit/observability data is acceptable.

4. **Warn tiers need enforcement or they become noise.** Use fail + warn + info (3 tiers) for deterministic checks. Never let warns accumulate without a threshold gate (`--max-warnings 0` or equivalent). Keep severity and confidence as separate dimensions.

5. **LLM-based quality checks need different severity models.** Traditional tiered severity doesn't transfer to non-deterministic checks — forced-choice severity assignment by LLM judges is systematically biased. Use required/additional binary or confidence-threshold scoring instead.

## Claims

| # | Claim | Type | Source | CoVe Question | CoVe Answer | Status |
|---|-------|------|--------|--------------|-------------|--------|
| 1 | MLflow's analysis: "At 1,000 eval rows × 5 LLM judges × $0.01/call, even a 20% structural failure rate saves $100/run" | Quoted statistic | [4] MLflow GitHub issue #20827 | Does the arithmetic hold? 1000 × 5 × $0.01 = $50/run total; 20% failure rate saves $50 × 0.20 = $10, not $100. | The arithmetic does not hold as written. $50 total × 20% saved = $10/run, or to reach $100 saved requires either 10,000 rows, 100% failure rate, or $0.10/call. The quoted figure appears to contain an error originating in the source document itself. The document cites this figure verbatim from [4]; the error is in the source, not the document's transcription. | human-review |
| 2 | MLflow Tier 1 proposed scorer set is exactly eight: ExactMatch, JsonValidity, RegexMatch, ContainsKeywords, LengthBound, IsNotEmpty, LatencyThreshold, NumericBound | Named attribution / count | [4] MLflow GitHub issue #20827 | Does the document support exactly these eight named scorers? | The Extracts section lists these eight scorers by name as the proposed "Tier 1 set" attributed to MLflow issue #20827 (source [4]). The count and names are internally consistent with the source reference. Not independently verifiable without external access, but no internal contradiction. | human-review |
| 3 | AutoChecklist offers "five generator strategies (Direct, Contrastive, Inductive, Deductive, Interactive)" paired with "three scoring modes (pass rate, weighted, normalized)" | Named attribution / count | [8] arXiv 2603.07019 | Are exactly these five strategy names and three scoring modes stated in the Extracts section from source [8]? | The Extracts section (Sub-question 2) lists these five generator strategies and three scoring modes verbatim attributed to arXiv 2603.07019. They are internally consistent across both the Extracts and Findings sections. No independent verification possible from within the document, but there is no internal contradiction. | human-review |
| 4 | AutoChecklist is attributed to "arXiv / U. Chicago" and dated "Mar 2026" | Named attribution / date | [8] arXiv 2603.07019 | Does the Sources table attribute [8] to U. Chicago and Mar 2026? | The Sources table (row 8) attributes arXiv 2603.07019 to "arXiv / U. Chicago, Mar 2026." The Findings section repeats "Mar 2026 arXiv [8]." The attribution is internally consistent. The arXiv ID 2603.07019 encodes March (03) 2026, consistent with the stated date. | verified |
| 5 | ROP's `&&&` operator "runs validators in parallel on the same input" | Specific technical claim | [7] F# for Fun and Profit ROP | Does the Extracts section from [7] describe `&&&` as enabling parallel validation on the same input? | The Extracts section (Sub-question 2, ROP paragraph) states: "The `&&&` operator runs validators in parallel on the same input, useful for checking multiple fields simultaneously." This is internally consistent. The original ROP source is F# functional composition — "parallel" here means logical parallel application, not concurrent execution threads. The document does not clarify this distinction, which could mislead readers expecting concurrent execution. | human-review |
| 6 | Rust's diagnostic system has four tiers: "Error (blocks compilation), Warning (informational but actionable), Note (contextual support for errors/warnings), Help (actionable fix suggestions)" | Named attribution / superlative ("most granular reference implementation") | [10] Rust compiler dev guide | Does the Findings section call Rust's model "the most granular reference implementation"? | The Findings section (Sub-question 4) states "Rust's four-tier model [10]: The Rust compiler's diagnostic system is the most granular reference implementation." This is a superlative comparative claim. The document examines four severity models (Rust, GX, Semgrep, Hebbia) and Semgrep also has four tiers (Critical/High/Medium/Low) plus a separate confidence dimension — arguably making Semgrep's model equally or more granular. The "most granular" superlative is not rigorously defended. | human-review |
| 7 | Great Expectations: "Default severity is Warning for generated expectations; Critical if unspecified" | Specific factual claim | [5][18] GX docs | Does the document's Extracts section state this default behavior for GX severity? | The Extracts section (Sub-question 4) states: "Default severity is Warning for generated expectations; Critical if unspecified." This creates a logical tension: if the default is Warning when generated, what scenario produces the "if unspecified" Critical default? These two defaults appear contradictory. The GX source docs [5][18] are listed as verified in the Sources table but the internal logic of this claim is inconsistent. | human-review |
| 8 | Semgrep's deprecated severity levels: "ERROR/WARNING/INFO mapping to High/Medium/Low" | Specific factual claim | [9] Semgrep severity KB | Does the document's Extracts section attribute this deprecated mapping to [9]? | The Extracts section (Sub-question 4) states: "Semgrep defines Critical, High, Medium, Low (with deprecated ERROR/WARNING/INFO mapping to High/Medium/Low)." This is internally consistent across Extracts and Findings. Source [9] is listed as T1 official docs with status "verified." The claim is traceable to the cited source. | verified |
| 9 | ESLint rules are "stateless — they inspect AST nodes and report warnings only, with no direct file system access or asynchronous operations permitted" | Quoted attribution | [2] ESLint architecture docs | Does the document attribute this exact constraint to [2] ESLint architecture docs? | The Extracts section (Sub-question 2) quotes this description directly and attributes it to [2]. The Findings section repeats the attribution. Source [2] is listed as T1 official docs with status "verified." The claim is internally consistent and traceable to the cited source. | verified |
| 10 | arXiv 2503.05965 finds forced-choice severity assignment selects judge systems performing "up to 31% worse than alternatives" | Quoted statistic | [A2] arXiv 2503.05965 | Does the document consistently state the "31% worse" figure and attribute it to [A2]? | The Challenge section and Findings section both cite this figure. Challenge: "selecting judge systems that perform 'as much as 31% worse' than alternative methods." Findings: "judge systems performing up to 31% worse than alternatives." The figure is internally consistent across both sections and attributed to [A2]. The source is listed as T3 status "confirmed" in the Additional Sources table. | verified |
| 11 | CQS is attributed to "Bertrand Meyer's original CQS principle" with the formulation "every method should either be a command that performs an action, or a query that returns data to the caller, but not both" | Named attribution | [19] Khalil Stemmler article | Does the document attribute this CQS formulation to Bertrand Meyer via source [19]? | The Extracts section (Sub-question 3) quotes this formulation and attributes it to CQS foundation [19, 14]. Source [19] is Khalil Stemmler's article on Command Query Separation, not a primary Meyer source. Stemmler's article is a secondary source that cites Meyer. The attribution in the document says "Bertrand Meyer's original CQS principle" but sources it via a T4 practitioner blog, not Meyer's original "Object Oriented Software Construction." The attribution is correct in naming Meyer but the sourcing chain passes through a secondary source. | human-review |
| 12 | Multi-agent confidence scoring uses ">= 75 threshold" to filter noise before reporting | Specific numeric claim | [12] DEV Community AI agent validation | Does the document consistently attribute this threshold to [12] and cite it in Findings? | The Extracts section (Sub-question 2) states "Confidence scoring (>= 75 threshold) filters noise before reporting" attributed to [12]. The Findings section (Sub-question 4) states "a confidence score (0–100) with a threshold (>= 75 to report)" also citing [12]. The figure is internally consistent across both sections. Source [12] is a T5 practitioner blog (DEV Community), meaning this threshold reflects one practitioner's implementation choice, not an industry standard. The document does not flag this provenance limitation. | human-review |
