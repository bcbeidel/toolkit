---
name: "Validation Architecture: Separating Structure from Quality"
description: "Three-layer validation model (structural/semantic/quality) derived from compiler phases, linter categories, and CI quality gates, with severity calibration patterns and agent-specific considerations"
metadata:
  type: research
  sources:
    - https://doc.rust-lang.org/rustc/lints/levels.html
    - https://doc.rust-lang.org/stable/clippy/lints.html
    - https://eslint.org/docs/latest/rules/
    - https://gcc.gnu.org/onlinedocs/gccint/Guidelines-for-Diagnostics.html
    - https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html
    - https://docs.astral.sh/ruff/linter/
    - https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-rules/rules
    - https://www.typescriptlang.org/tsconfig/strict.html
    - https://greatexpectations.io/blog/exploring-data-quality-schema-validation/
    - https://www.infoq.com/articles/pipeline-quality-gates/
    - https://cs.lmu.edu/~ray/notes/compilerarchitecture/
    - https://rustc-dev-guide.rust-lang.org/diagnostics.html
  related:
    - docs/research/tool-design-for-llms.md
    - docs/research/prompt-engineering.md
    - docs/context/validation-architecture.md
---

## Summary

Technical investigation of validation architecture patterns drawn from 12 verified
sources (9 T1 official documentation, 3 T4 expert practitioner) covering compilers
(Rust, GCC), linters (Clippy, ESLint, Pylint, Ruff), quality platforms (SonarQube),
type systems (TypeScript), data validation (Great Expectations), and CI pipelines.

18 searches across Google, 12 sources used.

**Key findings:**

- **Errors are non-negotiable; lints are configurable.** Every tool examined draws this
  same line. Compilers separate hard errors (compilation fails) from lints (advisory,
  user-overridable). The separation exists because the same check may be appropriate
  in one context and irrelevant in another (HIGH).
- **Checks are grouped by what they detect, not how.** Linters organize by category
  (correctness vs. style vs. performance), not by mechanism (deterministic vs.
  heuristic). Default severity is tied to the category (HIGH).
- **Real-world tools use more than two severity levels.** Rust has 6 lint levels,
  Pylint has 5 categories, SonarQube crosses type with severity for two dimensions.
  Binary warn/fail is too coarse for most validation needs (HIGH).
- **Three validation layers emerge from synthesis:** structural (parse-time, fail
  severity), semantic (consistency checks, warn severity), and quality assessment
  (judgment, warn/advisory severity). Each layer assumes the previous passed (HIGH).
- **Heuristic checks should almost never be fail severity.** The cost of a false
  positive scales with severity. SonarQube targets zero false positives for bugs
  but tolerates 20% for vulnerabilities. Uncertain checks need lower severity (HIGH).

## Detailed Analysis

### How compilers, linters, and CI pipelines separate deterministic from heuristic checks

Every tool examined draws the same fundamental line: **errors are non-negotiable, lints are configurable** (HIGH -- T1 sources [1][2][4][12] converge).

Rust's compiler makes the distinction architecturally explicit: errors prevent compilation; lints are advisory with configurable severity [1][12]. GCC follows the same pattern -- errors halt compilation, warnings continue, and `-Werror` can promote warnings to errors [4]. This separation exists because the same code might be acceptable in one context and unacceptable in another. Rust's `--cap-lints allow` mechanism, used by Cargo for dependencies, is the clearest expression: your strictness standards should not apply to code you don't control [1].

Linters extend this pattern with **categorical organization**. Clippy groups ~800 lints into categories (correctness, suspicious, complexity, perf, style, pedantic, restriction) with default severity tied to the category [2]. ESLint classifies rules as "problem," "suggestion," or "layout," with stylistic rules separated into an entirely different plugin (@stylistic/eslint-plugin) [3]. Pylint uses five categories (Fatal, Error, Warning, Convention, Refactor) with bit-encoded exit codes [5]. The consistent pattern across all tools: **checks are grouped by what they detect (correctness vs. style vs. performance), not by how they detect it (deterministic vs. heuristic)** (HIGH -- all linter sources converge).

CI pipelines add a **temporal dimension**: fast deterministic checks run first (lint, type check), slower integration tests run mid-pipeline, and heuristic quality gates (performance benchmarks, coverage thresholds) run last [10]. The ordering principle is: cheapest and most deterministic first, most expensive and most judgment-dependent last (MODERATE -- T4 source, but consistent with compiler phase ordering from T1/T4 sources [4][11]).

**Counter-evidence:** The clean separation breaks down in practice. GCC acknowledges that "the highest warning levels produce diagnostic messages for perfectly legitimate, reasonable code" [4] -- high-severity warnings can still be false positives. SonarQube targets "zero false positives" for bugs and code smells [7], but achieves only ">80% true positive rate" for vulnerabilities. The deterministic/heuristic boundary is not a clean line but a gradient (MODERATE).

### Severity models across validation systems

Real-world tools consistently use **more than two severity levels**, and the most sophisticated tools add orthogonal dimensions (HIGH -- all sources converge).

**Linear severity models (single dimension):**

| Tool | Levels | Notes |
|------|--------|-------|
| Rust/rustc | 6: allow, expect, warn, force-warn, deny, forbid | [1] Most granular; `forbid` prevents override |
| GCC | 3: error, warning, note | [4] Plus `-Werror` promotion |
| ESLint | 3: off (0), warn (1), error (2) | [3] Per-rule configurable |
| Pylint | 5: Fatal, Error, Warning, Convention, Refactor | [5] Bit-encoded exit codes |

**Multi-dimensional severity models:**

| Tool | Dimensions | Notes |
|------|-----------|-------|
| SonarQube | Type (Bug/Vulnerability/Smell) x Severity (Blocker to Info) | [7] Two-dimensional |
| Clippy | Category (correctness to restriction) x Level (deny/warn/off) | [2] Category determines default level |
| TypeScript | Flag bundle (strict = 8 individual flags) | [8] Decomposable strictness |

Two patterns emerge for **calibrating severity**:

1. **The Rust pattern -- configurable with caps.** Start with reasonable defaults, let users override up or down, provide cap mechanisms for dependency contexts [1]. New checks enter as warnings and may be promoted over time (HIGH).

2. **The TypeScript pattern -- decomposable bundles.** Group related checks into a "strict" bundle that can be adopted incrementally. Individual flags within the bundle can be toggled independently [8]. This enables gradual adoption (MODERATE -- single source, but well-documented pattern).

The key insight: **severity should be a property of the check-in-context, not the check alone**. The same check (e.g., unused variable) can be a hard error in production code and silenced in test code [1][4] (HIGH -- T1 sources converge).

### Validation layer organization for agent-produced content

Synthesizing compiler phases [11][12], linter categories [2][3][5], CI pipeline stages [10], and data validation frameworks [9], a three-layer model emerges:

**Layer 1: Structural Validation (Parse-time)**
- Deterministic, fast, zero false positives
- Analogous to: lexical/syntactic analysis, JSON Schema validation
- Examples: frontmatter parses correctly, required fields present, file paths exist on disk, URLs reachable
- Severity: fail (if it fails, the document is structurally invalid)
- All checks expressible as "X exists / X matches pattern / X is reachable"

**Layer 2: Semantic Validation (Consistency checks)**
- Deterministic execution of heuristic criteria, fast, low false-positive rate
- Analogous to: semantic analysis, type checking, Pylint Convention/Refactor checks
- Examples: word count within thresholds, index files in sync with directory contents, research documents have sources, draft markers present
- Severity: warn (the document works but violates a convention or exceeds a guideline)
- All checks expressible as "X is within threshold / X satisfies constraint"

**Layer 3: Quality Assessment (Judgment)**
- Heuristic, potentially slow, higher false-positive tolerance
- Analogous to: Clippy pedantic/restriction lints, SonarQube code smell detection, LLM-as-judge
- Examples: instruction density too high, ALL-CAPS directive count, naming convention adherence, content substance assessment
- Severity: warn (advisory; requires human or agent judgment to resolve)
- Checks involve subjective criteria or pattern matching with inherent ambiguity

This maps to the existing WOS validator architecture: `check_frontmatter` and `check_related_paths` are Layer 1; `check_content` and `check_draft_markers` are Layer 2; `check_skill_sizes` (instruction density, ALL-CAPS density) straddles Layers 2 and 3 (HIGH -- synthesis of multiple T1 sources with direct codebase mapping).

**The compiler pipeline principle applies:** each layer assumes the previous layer passed. Don't check word count if frontmatter didn't parse. Don't assess quality if required fields are missing [11] (MODERATE -- T4 source, but architecturally sound).

**For agent-produced content specifically,** the quality layer needs additional checks targeting LLM failure modes:
- Circular definitions (defining X as "X is...")
- Boilerplate inflation (word count met but substance absent)
- Source hallucination (URLs that look plausible but don't exist -- partially caught by Layer 1 URL checks)
- Structure mimicry (correct headings/format but vacuous content beneath)

These are inherently heuristic and may require LLM-as-judge evaluation rather than deterministic checks [9] (MODERATE -- synthesized from data quality patterns, not directly evidenced for agent content).

### Counter-evidence: when the separation fails

**The threshold boundary problem.** A check like "content must be 100-800 words" executes deterministically but embeds a heuristic judgment in its threshold. The layer assignment depends on the semantic role of the check, not its computational method. For a context file, word count is a quality guideline (warn). For YAML frontmatter requiring a `name` field, presence is structural (fail). The same mechanism (threshold comparison) serves both layers (HIGH -- derived from examining all tools).

**The strictness fatigue problem.** GCC documents that high warning levels produce noise for "perfectly legitimate code" [4]. TypeScript had to decompose `strict` into individual flags because blanket strictness was too disruptive for migration [8]. Clippy's pedantic category expects "frequent `#[allow]`" usage [2]. Every tool that went maximally strict had to add escape hatches. For agent-produced content: if the quality layer generates too many warnings, agents will either ignore them or waste context window addressing non-issues (MODERATE -- T1 sources for the pattern, inference for agent behavior).

**The two-dimension problem.** SonarQube discovered that a single severity axis is insufficient -- you need both "what kind of problem" (bug vs. smell vs. vulnerability) and "how bad" (blocker vs. minor) [7]. For document validation, a check that finds "no sources on a research document" is both a structural problem (missing required data) and a quality problem (incomplete research). A single severity axis forces you to pick one framing (HIGH -- T1 source).

**The false-positive cost asymmetry.** SonarQube targets zero false positives for bugs but tolerates 20% false positives for vulnerabilities [7]. Clippy's correctness category is deny-by-default (zero tolerance) while style is warn-by-default (tolerance expected) [2]. The cost of a false positive scales with severity: a false `fail` blocks work; a false `warn` wastes attention. Heuristic checks should almost never be `fail` severity -- their inherent uncertainty makes false positives inevitable (HIGH -- all linter sources converge).

## Challenge

### Assumptions Check

1. **Assumption: The compiler phase model maps cleanly to document validation.**
   Challenge: Compilers process a formal language with a grammar; documents are semi-structured (YAML frontmatter + free-text markdown). The "lexical to syntactic to semantic" pipeline assumes each phase produces a well-defined intermediate representation. Document validation may not have clean phase boundaries -- a "word count" check is simultaneously structural (is there content?) and qualitative (is there enough?).
   Assessment: Partially valid. The mapping holds for parse-level checks (frontmatter parsing, required fields) but gets fuzzy for quality checks that span multiple concerns.

2. **Assumption: Deterministic and heuristic checks are cleanly separable.**
   Challenge: Some checks appear deterministic but embed judgment. "Content must be 100-800 words" is deterministic in execution but heuristic in its threshold choice. URL reachability is deterministic at check time but non-deterministic across time (URLs go stale). The boundary between "structure" and "quality" is itself a design choice, not a natural law.
   Assessment: Valid concern. The separation is useful as an organizing principle but should not be treated as a binary classification. Some checks will sit at the boundary.

3. **Assumption: Severity should be binary (warn/fail).**
   Challenge: Every real-world tool examined uses more than two levels. Rust has six lint levels. Pylint has five categories. SonarQube crosses type with severity for a two-dimensional model. Binary severity may be too coarse for a validation system that needs to guide agent behavior without blocking it.
   Assessment: Strong counter-evidence. The current warn/fail model may need at least one additional level or an orthogonal dimension (check category).

4. **Assumption: All heuristic checks belong at the same validation layer.**
   Challenge: "Word count > 800" is a simple threshold check (fast, deterministic execution). "Instruction density is too high" requires pattern analysis (fast but with higher false-positive rate). Both are "quality" checks but differ in reliability characteristics.
   Assessment: Valid. Heuristic checks should be subdivided by execution characteristics: threshold-based (fast, deterministic execution of heuristic criteria) vs. pattern-based (fast, higher ambiguity).

### Premortem

If a validation architecture based on this research fails, the most likely causes:

1. **Over-stratification.** Too many validation layers create confusion about which layer owns which check. Developers (or agents) stop trusting the system when they can't predict where a check will fire. Mitigation: limit to 3 layers maximum.

2. **Severity inflation.** Checks start as warnings, get promoted to errors after incidents, and eventually everything is a hard failure. The system becomes unusable. Mitigation: require explicit justification for severity promotion; make demotion equally easy.

3. **Threshold drift.** Heuristic thresholds (word counts, line limits, density scores) are set once and never revisited. They become either too strict (noise) or too lenient (miss real issues). Mitigation: make thresholds configurable and document their rationale.

4. **Agent-specific blindness.** Patterns designed for human developers may not catch agent-specific failure modes (e.g., agents produce well-structured but vacuous content). The quality layer needs checks tuned to LLM output patterns, not just human coding patterns. Mitigation: include agent-specific checks (e.g., detecting generated boilerplate, circular definitions).

## Evidence

### Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|-----------|------|--------|------|
| 1 | https://doc.rust-lang.org/rustc/lints/levels.html | Lint Levels - The rustc book | Rust Project | 2024 | verified | T1 |
| 2 | https://doc.rust-lang.org/stable/clippy/lints.html | Clippy's Lints | Rust Project | 2024 | verified | T1 |
| 3 | https://eslint.org/docs/latest/rules/ | Rules Reference - ESLint | ESLint / OpenJS Foundation | 2024 | verified | T1 |
| 4 | https://gcc.gnu.org/onlinedocs/gccint/Guidelines-for-Diagnostics.html | Guidelines for Diagnostics | GCC Project / FSF | 2024 | verified | T1 |
| 5 | https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html | Messages overview - Pylint | Pylint / PyCQA | 2024 | verified | T1 |
| 6 | https://docs.astral.sh/ruff/linter/ | The Ruff Linter | Astral / Charlie Marsh | 2024 | verified | T1 |
| 7 | https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-rules/rules | SonarQube rules | SonarSource | 2024 | verified | T1 |
| 8 | https://www.typescriptlang.org/tsconfig/strict.html | TSConfig Option: strict | TypeScript / Microsoft | 2024 | verified | T1 |
| 9 | https://greatexpectations.io/blog/exploring-data-quality-schema-validation/ | Exploring data quality: schema validation | Great Expectations | 2024 | verified | T4 |
| 10 | https://www.infoq.com/articles/pipeline-quality-gates/ | The Importance of Pipeline Quality Gates | InfoQ | 2024 | verified | T4 |
| 11 | https://cs.lmu.edu/~ray/notes/compilerarchitecture/ | Compiler Architecture | Ray Toal / LMU | 2024 | verified | T4 |
| 12 | https://rustc-dev-guide.rust-lang.org/diagnostics.html | Errors and lints - Rust Compiler Development Guide | Rust Project | 2024 | verified | T1 |

### Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Rust lints have six levels: allow, expect, warn, force-warn, deny, forbid | statistic | [1] | verified |
| 2 | Clippy groups ~800 lints into categories | statistic | [2] | corrected (source says ~795-801; findings updated from "700+" to "~800") |
| 3 | ESLint classifies rules as "problem," "suggestion," or "layout" | attribution | [3] | verified |
| 4 | GCC: "the highest warning levels produce diagnostic messages for perfectly legitimate, reasonable code" | quote | [4] | verified |
| 5 | Pylint uses five message categories with bit-encoded exit codes: Fatal (1), Error (2), Warning (4), Convention (8), Refactor (16) | statistic | [5] | verified |
| 6 | SonarQube targets "zero false positives" for bugs and code smells | quote | [7] | verified |
| 7 | SonarQube achieves ">80% true positive rate" for vulnerabilities | statistic | [7] | verified |
| 8 | TypeScript strict mode is a bundle of 8 individual flags | statistic | [8] | verified |
| 9 | Clippy correctness category is the only deny-by-default category | attribution | [2] | verified |
| 10 | ESLint stylistic rules were separated into @stylistic/eslint-plugin | attribution | [3] | verified |

### Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| compiler phases validation architecture deterministic vs heuristic checks separation | google | all | 10 | 1 |
| ESLint rule categories error warning stylistic architecture design | google | all | 10 | 1 |
| Rust compiler error levels lint warn deny forbid architecture | google | all | 10 | 3 |
| GCC warning levels -Wall -Werror compiler diagnostic severity architecture | google | all | 10 | 1 |
| CI pipeline validation stages gate checks quality gates pattern | google | all | 10 | 1 |
| pylint message categories convention refactor warning error fatal design | google | all | 10 | 1 |
| Clippy Rust lint categories correctness style complexity perf | google | all | 10 | 1 |
| SonarQube rule types bug vulnerability code smell severity blocker critical | google | all | 10 | 1 |
| validation layer architecture parse-time vs semantic vs quality checks | google | all | 10 | 1 |
| JSON Schema validation ajv structural type checking vs semantic validation | google | all | 10 | 0 |
| linter false positive rate heuristic check problem configurable severity | google | all | 10 | 0 |
| Mypy Python type checker error codes categories | google | all | 10 | 0 |
| great expectations data validation deterministic vs statistical checks | google | all | 10 | 1 |
| TypeScript compiler strictness levels strict mode tsconfig | google | all | 10 | 1 |
| ruff Python linter rule categories preview stable severity | google | all | 10 | 1 |
| shift left testing validation fast feedback deterministic checks | google | all | 10 | 0 |
| content validation agent-produced LLM output structured document quality | google | all | 10 | 0 |
| validation architecture anti-patterns over-validation strictness fatigue | google | all | 10 | 0 |

18 searches across Google, 180 found, 12 used. Not searched: academic databases (ACM DL, IEEE Xplore -- authenticated access required), compiler textbooks (Dragon Book, Engineering a Compiler -- not web-accessible).

## Takeaways

**For WOS validation architecture:**

1. **Keep three layers, not more.** Structural (fail), semantic (warn), quality (warn). The compiler pipeline principle -- each layer assumes the previous passed -- keeps the architecture predictable.

2. **Categorize checks by what they detect, add severity as a second dimension.** Follow the Clippy/SonarQube pattern: the check's category (structural, semantic, quality) determines its default severity. Allow per-check override for project-specific needs.

3. **Binary warn/fail is adequate if combined with check categories.** The current WOS model works because it already separates categories implicitly (frontmatter checks fail, content checks warn). Making categories explicit would be more valuable than adding severity levels.

4. **Make thresholds configurable with documented rationale.** Every threshold (word counts, line limits, density scores) should have CLI flags and config file options. Follow the Rust/Ruff pattern: reasonable defaults, easy overrides.

5. **Agent-specific quality checks are a gap.** Current checks catch structural and convention issues. Checks for LLM-specific failure modes (boilerplate, circular definitions, structure mimicry) would strengthen the quality layer.

**Limitations:** All sources are from code-oriented tools. Document validation is a less-explored domain with fewer established patterns. The three-layer model is synthesized, not directly evidenced in any single source. Agent-specific validation patterns are nascent -- no established frameworks exist yet.

**Follow-ups:** Design the check category taxonomy for WOS. Evaluate whether `check_source_urls` belongs in Layer 1 (structural -- URL exists) or Layer 2 (semantic -- source supports claims). Prototype an agent-specific quality check (e.g., circular definition detector).
