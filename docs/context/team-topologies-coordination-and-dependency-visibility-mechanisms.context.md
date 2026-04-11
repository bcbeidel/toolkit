---
name: Team Topologies Coordination and Dependency Visibility Mechanisms
description: Team Topologies defines four team types with prescribed interaction modes to reduce coordination overhead structurally — RAID logs and PI Planning are the operational dependency-tracking mechanisms that make inter-team dependencies visible and owned.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.atlassian.com/devops/frameworks/team-topologies
  - https://asana.com/resources/raid-log
  - https://framework.scaledagile.com/pi-planning
  - https://agilemania.com/kanban-for-risk-management-and-dependency-tracking
related:
  - docs/context/agile-methodology-selection-by-context-and-hybrid-principle-commitment.context.md
  - docs/context/okr-co-creation-cascade-failure-and-structural-discipline.context.md
  - docs/context/platform-engineering-as-load-reduction-discipline.context.md
  - docs/context/flow-metrics-and-monte-carlo-simulation-stability-precondition.context.md
---
# Team Topologies Coordination and Dependency Visibility Mechanisms

## Key Insight

Effective coordination in multi-team engineering organizations is primarily a structural problem, not a communication problem. Team Topologies addresses it structurally: define team types and interaction modes to minimize coordination overhead by design rather than managing it reactively. The dependency-tracking mechanisms (RAID logs, PI Planning) make dependencies visible and owned — the specific tool matters less than consistent use.

## The Four Team Types (Team Topologies framework, Skelton & Pais)

**Stream-aligned teams**: Focused on a single, impactful stream of work (a product, service, or user journey). Empowered to build and deliver value as quickly and independently as possible without handoffs. This is the primary team type; the other three exist to support stream-aligned teams.

**Platform teams**: Provide internal platforms — reliable, self-service capabilities that stream-aligned teams consume. Their product is developer experience. Goal: reduce cognitive load on stream-aligned teams by abstracting infrastructure complexity.

**Enabling teams**: Temporarily work with stream-aligned teams to help them acquire capabilities (new technology, practices, architectures). Time-limited engagement; aim to be unnecessary after knowledge transfer completes.

**Complicated-subsystem teams**: Own technically complex subsystems that require deep specialist knowledge. Used sparingly; most teams should be stream-aligned.

**Prescribed interaction modes**: Collaboration (teams work closely for a defined period), X-as-a-Service (stream-aligned team consumes platform team's service without collaboration), Facilitating (enabling team works alongside stream-aligned team to build capability). Prescribing interaction modes prevents ad-hoc, high-overhead coordination patterns.

## Evidence Caveat

Team Topologies evidence is largely anecdotal and case-study based — not controlled research. The framework is compelling as a lens, but the specific taxonomy should not be treated as empirically validated. Evidence is MODERATE confidence for Team Topologies as a useful structural framework; LOW confidence in it as a universal answer for all engineering contexts. R&D and research-heavy organizations may not map cleanly to the stream-aligned model.

## Dependency Tracking Mechanisms

**RAID logs**: Canonical lightweight mechanism. RAID = Risks, Assumptions, Issues, Dependencies. Each quadrant has an owner and a resolution path. Works because it categorizes what's being tracked explicitly and is reviewed continuously rather than filed once. The tool is secondary — a shared spreadsheet used consistently outperforms dedicated software used inconsistently.

**SAFe PI Planning**: High-ceremony complement for large organizations. A 2-day cross-team event producing committed team objectives and a program board showing feature delivery dates and inter-team dependency chains for an 8–12 week increment. SAFe's own reported statistics (30–40% predictability improvement, 20–35% time-to-market reduction) are self-reported by the framework vendor with no independent replication — treat as directional motivation, not precise benchmarks.

**Kanban-based risk boards**: Alternative for organizations that want dependency visibility inside their existing workflow tools. Treat risks and dependencies as work items with visual workflow stages (identified → assessed → mitigated → resolved). Makes risk work visible alongside delivery work rather than isolated in a separate register.

## The Coordination Principle That Generalizes

Any mechanism that makes dependencies visible and owned outperforms unstructured verbal coordination. The three anti-patterns are: (a) dependencies discovered at release time rather than during planning, (b) dependencies tracked without owners, and (c) dependency lists maintained outside the workflow where teams are already operating.

## Takeaway

Structure team boundaries to minimize coordination by design (Team Topologies provides the vocabulary). Then make remaining dependencies visible and owned through lightweight persistent artifacts (RAID logs) or high-ceremony alignment events (PI Planning) depending on organizational scale. More meetings do not solve structural coordination problems — structure does.
