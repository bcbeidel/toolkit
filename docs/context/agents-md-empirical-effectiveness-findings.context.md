---
name: "AGENTS.md Empirical Effectiveness Findings"
description: "Two 2026 studies on AGENTS.md effectiveness conflict in direction but measure different things: ETH Zurich finds accuracy decreases, arXiv 2601.20404 finds runtime efficiency improves — context files may make agents faster but not more correct"
type: context
sources:
  - https://arxiv.org/abs/2602.11988
  - https://arxiv.org/abs/2601.20404
  - https://code.claude.com/docs/en/best-practices
related:
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/context/instruction-file-non-inferable-specificity.context.md
  - docs/context/instruction-file-extraction-techniques.context.md
  - docs/context/instruction-file-authoring-anti-patterns.context.md
---

# AGENTS.md Empirical Effectiveness Findings

Two 2026 preprints study the same intervention — AGENTS.md context files for coding agents — and reach opposite conclusions. They do not contradict each other: they measure different things.

## ETH Zurich (arXiv 2602.11988): Accuracy Decreases, Cost Rises

The ETH Zurich SRI Lab evaluated context files on a dual benchmark (AGENTbench + SWE-bench), spanning approximately 300 tasks. Core findings:

- **LLM-generated context files**: task success −0.5% to −2%, inference cost +20%
- **Human-written context files**: task success +4%, but inference cost +19%

Agents with context files ran more tests, searched more files, and read more files — but did not find the right files any faster. The files induced exploration without improving precision.

The critical exception: when project markdown documentation was stripped from repositories, LLM-generated context files improved task success by +2.7%. This isolates the failure mode as **redundancy with existing docs**, not generation itself. When agents have no other documentation to read, context files fill a genuine gap. When docs already exist, context files that repeat them add noise and cost without accuracy gains.

Recommendation from the paper: human-written context files should describe only minimal requirements — custom tooling, build commands, non-inferable constraints — not architectural overviews agents can derive from existing docs.

## arXiv 2601.20404: Runtime Efficiency Improves

A separate study (10 repos, 124 PRs) measured wall-clock time and token consumption rather than task success. Findings: AGENTS.md files reduced median runtime by 28.64% and output token consumption by 16.58%.

This does not contradict ETH Zurich. The studies measure orthogonal dimensions:

| Study | Metric | Direction |
|---|---|---|
| ETH Zurich 2602.11988 | Task success (accuracy) | Negative (−0.5% to −2%) |
| arXiv 2601.20404 | Runtime, token consumption (efficiency) | Positive (−28.64% runtime) |

A plausible reconciliation: context files help agents find an answer faster by narrowing their search strategy, but that strategy doesn't converge on the *right* answer more often. Speed and correctness are separable.

## Practical Implications

1. Instruction files likely improve agent efficiency (speed, tokens) even when they don't improve accuracy. In cost-sensitive contexts this matters.
2. The accuracy benefit from human-written files (+4%) comes with a 19% cost increase — the net value depends on whether task success is worth the inference spend.
3. The anti-pattern is redundancy with existing project documentation, not the existence of context files. Files that state only non-inferable specifics avoid the ETH Zurich failure mode.
4. Auto-generated context files without human filtering underperform. Human curation is the differentiating step between the −2% and +4% outcomes.
