---
name: Immutable Design Artifacts vs Mutable Execution Plans
description: >
  Engineering processes consistently distinguish between immutable design
  records (supersede to change) and mutable execution plans (revise in-place),
  supporting the pattern of superseding design docs while revising plans.
type: research
sources:
  - https://www.industrialempathy.com/posts/design-docs-at-google/
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
  - https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://peps.python.org/pep-0001/
  - https://www.kubernetes.dev/resources/keps/
  - https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md
  - https://www.tcgen.com/product-development/stage-gate-process/
  - https://simplerqms.com/engineering-change-order/
  - https://praxie.com/plan-of-record-por-software-tools-templates-2/
  - https://github.com/joelparkerhenderson/architecture-decision-record
  - https://icepanel.io/blog/2023-03-29-architecture-decision-records-adrs
  - https://medium.com/@nolomokgosi/basics-of-architecture-decision-records-adr-e09e00c636c6
---

## Search Protocol

| # | Query | Tool | Hits | Useful |
|---|-------|------|------|--------|
| 1 | ADR immutability "architecture decision records" immutable after acceptance | WebSearch | 10 | 3 |
| 2 | "living document" vs "record of decision" software engineering | WebSearch | 0 | 0 |
| 3 | RFC immutable after approval "design document" mutable plan revision | WebSearch | 10 | 2 |
| 4 | Stage-Gate "project plan" revision mid-execution correction vs design freeze | WebSearch | 10 | 2 |
| 5 | agile "project plan" "living document" backlog revision sprint | WebSearch | 10 | 1 |
| 6 | Google design docs immutable after shipping "living document" | WebSearch | 10 | 2 |
| 7 | engineering "work order" revision amendment vs "design specification" | WebSearch | 10 | 2 |
| 8 | "record of decision" immutable vs "execution plan" mutable revision | WebSearch | 10 | 2 |
| 9 | Kubernetes KEP "living document" mutable updated during implementation | WebSearch | 10 | 3 |
| 10 | Google design docs at Google (Malte Ubl) | WebFetch | 1 | 1 |
| 11 | Bruno Scheufler RFCs and ADRs | WebFetch | 0 | 0 (404) |
| 12 | Pragmatic Engineer RFCs and design docs | WebFetch | 1 | 0 |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.industrialempathy.com/posts/design-docs-at-google/ | Design Docs at Google | Malte Ubl | 2020 | T2 | verified |
| 2 | https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html | ADR Process | AWS | 2024 | T1 | verified |
| 3 | https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions | Documenting Architecture Decisions | Michael Nygard / Cognitect | 2011 | T2 | verified |
| 4 | https://peps.python.org/pep-0001/ | PEP 1 – PEP Purpose and Guidelines | Python | 2000 (updated) | T1 | verified |
| 5 | https://www.kubernetes.dev/resources/keps/ | Kubernetes Enhancement Proposals | Kubernetes | current | T1 | verified |
| 6 | https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md | KEP Process | Kubernetes | current | T1 | verified |
| 7 | https://www.tcgen.com/product-development/stage-gate-process/ | Stage-Gate Process | TCGen | 2025 | T2 | verified |
| 8 | https://simplerqms.com/engineering-change-order/ | Engineering Change Order (ECO) | SimplerQMS | current | T3 | verified |
| 9 | https://praxie.com/plan-of-record-por-software-tools-templates-2/ | Plan of Record Template | Praxie | current | T3 | verified |
| 10 | https://github.com/joelparkerhenderson/architecture-decision-record | ADR Template Collection | Joel Parker Henderson | current | T3 | verified |
| 11 | https://icepanel.io/blog/2023-03-29-architecture-decision-records-adrs | Architecture Decision Records (ADRs) | IcePanel | 2023 | T3 | verified |
| 12 | https://medium.com/@nolomokgosi/basics-of-architecture-decision-records-adr-e09e00c636c6 | Basics of ADR | Letlhogonolo Mokgosi | 2024 | T4 | verified |

## Sub-Questions

1. Are ADRs/RFCs/design docs treated as immutable records while project plans/work orders are revised in-place?
2. What patterns exist for "living documents" vs "records of decision" in software engineering?
3. How do Stage-Gate, Agile, and RFC processes handle mid-execution corrections to plans vs designs?
4. Is there an established name for this design-immutable/plan-mutable distinction?

## Findings

### 1. Design Artifacts Are Immutable; Execution Plans Are Mutable

Every system studied distinguishes between design decisions (immutable after acceptance) and execution guidance (revised as conditions change).

| Artifact type | Mutability | Change mechanism | Sources |
|--------------|------------|-----------------|---------|
| ADR | Immutable after acceptance | Supersede with new ADR | [2][3][10][11][12] |
| IETF RFC | Immutable after publication | Errata or new RFC | [4] |
| PEP | Immutable after acceptance | New PEP with `Superseded-By` | [4] |
| Google design doc | "Should" update, practically supplemented | New doc or amendment | [1] |
| Design specification (mfg) | Immutable snapshot; ECO for changes | New revision = new immutable snapshot | [8] |
| KEP | Living document, updated through lifecycle | In-place revision with gate reviews | [5][6] |
| Agile sprint backlog | Mutable within sprint boundaries | Updated during sprint planning | multiple |
| Project plan / Plan of Record | Mutable during execution | In-place revision with accountability | [9] |
| Stage-Gate project plan | Mutable via Recycle decision | Revised and re-enters gate review | [7] |

The pattern is consistent: **artifacts that record "why we decided X" are immutable; artifacts that guide "how to execute X" are mutable** (HIGH — T1+T2+T3 convergence across 7 independent systems).

### 2. Two Document Classes: Records vs. Guides

Two distinct classes emerge, though no single widely-adopted name exists for the distinction:

**Records of decision** (immutable):
- Purpose: preserve the reasoning at a point in time
- Change mechanism: supersede (create new, mark old as superseded)
- Examples: ADRs, RFCs, PEPs, design specifications
- Key property: historical accuracy matters more than currency

**Execution guides** (mutable):
- Purpose: direct ongoing work toward a goal
- Change mechanism: revise in-place (update content, preserve identity)
- Examples: KEPs, sprint backlogs, project plans, work orders
- Key property: currency matters more than historical accuracy

The closest established terminology comes from manufacturing: **design specifications** vs. **work orders**. Design specs are immutable baselines requiring Engineering Change Orders (ECOs) to modify. Work orders are revised through lighter Documentation Change Orders (DCOs) without incrementing revision numbers [8] (HIGH — T3 source but well-established industry practice).

In software, the ADR community uses the language of "immutable documents" [2][3] explicitly. The KEP process uses "living document" [5][6] explicitly. But no source found uses a single term that names the *distinction* between the two classes (MODERATE — absence of terminology confirmed across all sources).

### 3. Mid-Execution Correction Patterns

Each process handles mid-execution corrections differently depending on artifact type:

**Stage-Gate** [7]: Design changes trigger a "Recycle" (return to previous stage, revise, re-enter gate). Project plans are revised at each gate. The distinction is explicit: Recycle addresses design; plan revision addresses execution.

**Agile** [multiple]: The product backlog is a "living document" continuously revised. Sprint backlogs are frozen during a sprint but revised at sprint planning. There are no immutable design artifacts in pure Agile — all planning is iterative.

**KEP** [5][6]: A single KEP tracks a feature through alpha → beta → GA, revised at each stage. KEPs are explicitly "living documents." However, the *design decisions* within a KEP are discussed and agreed before implementation; it's the implementation details and graduation criteria that evolve.

**Google** [1]: Design docs "should" be updated during implementation, but in practice "changes are often isolated into new documents." The article recommends linking amendments to originals. This is a pragmatic middle ground: theoretical mutability, practical supplementation.

**Manufacturing** [8]: Design specs are immutable baselines (ECO creates new revision). Work instructions are revised through lighter DCO process. The two-track system is explicit and enforced by regulatory requirements.

The convergent pattern: **design corrections create new artifacts; execution corrections update existing ones** (HIGH — T1+T2 sources across software and manufacturing).

### 4. No Single Established Name

No source uses a single established term for this distinction. The closest candidates:

- **"Records vs. guides"** — descriptive but not established
- **"Decision records vs. living documents"** — used separately in ADR and KEP communities but never contrasted as a named pair
- **"Design baseline vs. execution plan"** — manufacturing terminology, closest to an established distinction
- **"Immutable vs. mutable artifacts"** — accurate but generic

The distinction is *practiced* universally but *named* nowhere (MODERATE — confirmed absence across 12 sources).

## Challenge

**Counter-argument: Google says design docs should be updated.** True — Malte Ubl [1] recommends updating pre-shipping design docs. But the same article notes this rarely happens in practice, and "changes are often isolated into new documents." Google's actual behavior aligns with supersede-don't-edit even when their stated policy doesn't. The recommendation to update is aspirational; the practice is supplementation.

**Counter-argument: KEPs blur the line.** KEPs are both design decisions and execution plans in one document. They're living documents that get revised. However, KEPs have gate reviews (alpha, beta, GA) that re-validate the design at each stage — they don't allow silent design changes. The mutability is structured, not free-form. This actually supports the pattern: execution details change freely, design decisions change only through formal review.

**Counter-argument: Agile has no immutable artifacts.** In pure Scrum, everything is revisable. But Agile teams using ADRs (a common combination) maintain immutable ADRs alongside mutable backlogs — the distinction re-emerges whenever a team needs both decision traceability and execution flexibility.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | ADRs are immutable after acceptance | attribution | [2][3] | verified — AWS: "treat ADRs as immutable documents after the team accepts or rejects them" |
| 2 | KEPs are "living documents" | attribution | [5] | verified — Kubernetes: "KEPs are living documents" |
| 3 | Google recommends updating design docs pre-shipping | attribution | [1] | verified — "It is strongly recommended to update the design doc" |
| 4 | Google notes changes are "often isolated into new documents" in practice | attribution | [1] | verified — direct quote |
| 5 | Manufacturing distinguishes ECO (design) from DCO (work instructions) | attribution | [8] | verified |
| 6 | No single established name exists for this distinction | comparative | [1-12] | verified (absence confirmed) |
| 7 | Plan of Record is initially immutable then mutable | attribution | [9] | verified — "the plan is immutable, hence the 'of record' title" |

## Recommendation

**Apply the pattern: supersede design docs, revise plans in-place.**

This is well-supported by the evidence:

1. WOS design docs (`type: design`) are records of decision → treat as immutable, supersede to change
2. WOS plans (`type: plan`) are execution guides → revise in-place when scope adjusts mid-flight
3. The write-plan infeasibility check sits at the boundary: it detects when a design decision is wrong (→ supersede the design) vs. when a plan task is impractical (→ revise the plan)

The distinction maps cleanly to the existing WOS artifact types and requires no new concepts — just explicit guidance in the skill instructions about which change mechanism applies to which artifact type.
