---
name: "Validation Architecture: Three Layers"
description: "Three-layer validation model (structural, semantic, quality) derived from compiler and linter patterns, with severity calibration principles and agent-specific quality considerations"
metadata:
  type: reference
  sources:
    - https://doc.rust-lang.org/rustc/lints/levels.html
    - https://doc.rust-lang.org/stable/clippy/lints.html
    - https://eslint.org/docs/latest/rules/
    - https://gcc.gnu.org/onlinedocs/gccint/Guidelines-for-Diagnostics.html
    - https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-rules/rules
  related:
    - docs/research/validation-architecture.md
    - docs/context/tool-design-for-llms.md
    - docs/context/feedback-loop-design.md
---

Validation systems across compilers, linters, and CI pipelines converge on the
same architectural separation: **errors are non-negotiable, lints are
configurable**. This distinction is not about mechanism (deterministic vs.
heuristic) but about what happens when a check fails -- does work stop, or does
the user decide?

## Three Validation Layers

Synthesizing patterns from Rust's compiler, Clippy, ESLint, Pylint, SonarQube,
and CI pipeline quality gates, three layers emerge. Each layer assumes the
previous one passed.

**Layer 1 -- Structural (fail severity).** Parse-time checks with zero false
positives. Frontmatter parses correctly, required fields exist, file paths
resolve, URLs are reachable. These are expressible as "X exists" or "X matches
pattern." If structural validation fails, the document is invalid and further
checks are meaningless.

**Layer 2 -- Semantic (warn severity).** Deterministic execution of convention
checks with low false-positive rates. Word count within thresholds, index files
in sync with directory contents, research documents have sources, draft markers
present. These are expressible as "X satisfies constraint." The document works
but violates a convention.

**Layer 3 -- Quality (warn/advisory severity).** Heuristic checks with higher
false-positive tolerance. Instruction density, ALL-CAPS directive counts,
naming conventions, content substance. These involve subjective criteria or
pattern matching with inherent ambiguity. For agent-produced content, this
layer should also target LLM-specific failure modes: boilerplate inflation,
circular definitions, and structure mimicry (correct format, vacuous content).

## Severity Calibration

Two principles govern severity assignment:

**Categorize by what checks detect, not how they work.** Clippy groups 800+
lints by category (correctness, style, complexity) with default severity tied
to category. ESLint classifies rules as "problem," "suggestion," or "layout."
The check's category determines its default severity. A word count threshold
executes deterministically but embeds a heuristic judgment -- its layer
assignment depends on its semantic role, not its computational method.

**False-positive cost scales with severity.** SonarQube targets zero false
positives for bugs but tolerates 20% for vulnerabilities. Clippy's correctness
category is deny-by-default; style is warn-by-default. A false `fail` blocks
work; a false `warn` wastes attention. Heuristic checks should almost never be
fail severity because their inherent uncertainty makes false positives
inevitable.

## Design Constraints

**Binary warn/fail works when combined with categories.** Real-world tools use
more severity levels (Rust has six, Pylint has five), but binary severity is
adequate when checks are explicitly categorized. The category communicates what
kind of problem was found; severity communicates whether to stop.

**Thresholds need configurability and rationale.** Every tool that went
maximally strict added escape hatches. GCC documents that high warning levels
produce noise for "perfectly legitimate code." TypeScript decomposed `strict`
into individual flags. Thresholds set once and never revisited drift toward
either noise (too strict) or irrelevance (too lenient).

**Agent-specific quality checks are a gap.** Checks designed for human
developers miss LLM failure modes. Agents produce well-structured but
potentially vacuous content. The quality layer needs checks tuned to
agent output patterns -- detecting generated boilerplate, circular definitions
("X is defined as X"), and source hallucination -- alongside traditional
code-oriented quality checks.

## Takeaway

The compiler pipeline principle applies directly: run structural checks first,
semantic checks second, quality checks last. Each layer filters out documents
that would produce false positives in later layers. Severity is a property of
the check-in-context, not the check alone -- the same check (unused variable,
word count) can warrant different severity in different contexts.
