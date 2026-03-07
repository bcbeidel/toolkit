# Consider Command Examples & Research Density Reduction — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add worked examples to all 16 consider command models (#126), then reduce research skill instruction density without losing behavioral intent (#124).

**Architecture:** Two independent changes on one branch. #126 adds `<example>` blocks to command files in `commands/consider/`. #124 merges and deduplicates reference files in `skills/research/references/`, then updates SKILL.md references.

**Tech Stack:** Markdown editing, pytest for validation, `wc -w` for word count measurement.

**Branch:** `feat/124-126-research-density-and-examples`
**Design:** `docs/plans/2026-03-06-research-density-and-examples-design.md`

---

## Part 1: Consider Command Worked Examples (#126)

Each task adds an `<example>` block to one consider command file. The example is placed between `</output_format>` and `<success_criteria>`, is ~10-15 lines, uses a scenario matching the model's natural sweet spot, and demonstrates the depth/specificity from `<success_criteria>`.

### Task 1: Add example to first-principles.md

**Files:**
- Modify: `commands/consider/first-principles.md`

**Step 1: Add `<example>` block**

Insert between `</output_format>` (line 41) and `<success_criteria>` (line 43):

```markdown
<example>
## First-Principles Analysis: Monolith vs Microservices

### Problem Statement
Our team assumes we need microservices because we're scaling, but deploys are slow and coordination costs are high.

### Assumptions Identified
- Microservices improve scalability — convention (monoliths scale vertically too)
- Independent deploys are faster — convention (coordination overhead can negate this)
- Our team is big enough to own separate services — unverified (we have 4 engineers)
- Network calls between services are negligible — unverified (latency adds up)

### Fundamental Truths
1. We need to deploy changes without breaking unrelated features
2. Our current bottleneck is deploy pipeline speed, not runtime scaling
3. Four engineers cannot maintain more than 2-3 independent services effectively

### Rebuilt Reasoning
A modular monolith with clear internal boundaries gives us deploy isolation (via feature flags and targeted rollouts) without the coordination cost of service boundaries. Split only when a module's scaling needs diverge measurably from the rest.

### Key Insight
The assumption "scaling = microservices" skipped the question "what are we actually scaling?" Our bottleneck is deploy speed, not request throughput — a problem microservices make worse, not better.
</example>
```

**Step 2: Verify file structure**

Read the file and confirm: frontmatter → `<objective>` → `<process>` → `<output_format>` → `<example>` → `<success_criteria>`.

### Task 2: Add example to 5-whys.md

**Files:**
- Modify: `commands/consider/5-whys.md`

**Step 1: Add `<example>` block**

Insert between `</output_format>` (line 43) and `<success_criteria>` (line 45). Scenario: debugging a CI pipeline failure.

```markdown
<example>
## 5 Whys Analysis: CI Builds Failing Intermittently

### Problem Statement
Integration tests fail roughly 20% of the time on CI but pass locally.

### Why Chain
1. Why? Tests depend on a shared database that sometimes has stale data from previous runs.
2. Why? Test teardown doesn't reset the database — it relies on transactions that sometimes don't roll back.
3. Why? Two test suites run in parallel and share a single test database instance.
4. Why? The CI config was copied from a project that ran tests sequentially.
5. Why? No one reviewed the CI config when we added the second test suite six months ago.

### Root Cause
CI infrastructure was never updated when test parallelism was introduced. The shared database assumption held for sequential runs but breaks under concurrency.

### Verification
Giving each parallel suite its own database instance would eliminate the shared-state race condition, preventing the intermittent failures.

### Action
Create per-suite database instances in CI using a template database that's cloned at suite start and destroyed at suite end.
</example>
```

### Task 3: Add example to eisenhower-matrix.md

**Files:**
- Modify: `commands/consider/eisenhower-matrix.md`

**Step 1: Add `<example>` block**

Insert between `</output_format>` and `<success_criteria>`. Scenario: a tech lead's weekly priorities.

```markdown
<example>
## Eisenhower Matrix: Sprint Planning Priorities

### Items to Prioritize
1. Fix production login bug (users locked out)
2. Write Q2 architecture proposal (due in 3 weeks)
3. Review 4 pending pull requests
4. Update team wiki with onboarding docs
5. Respond to vendor demo scheduling emails
6. Refactor auth module (tech debt)

### Matrix

|  | Urgent | Not Urgent |
|--|--------|-----------|
| **Important** | Q1: Fix login bug | Q2: Architecture proposal, Refactor auth |
| **Not Important** | Q3: Vendor emails, PR reviews | Q4: Wiki updates |

### Quadrant Assignments
- **Q1 (Do Now):** Fix production login bug — users are blocked, revenue impact
- **Q2 (Schedule):** Architecture proposal (block 2hrs Thursday), Auth refactor (next sprint)
- **Q3 (Delegate):** Vendor emails (admin can schedule), PR reviews (assign to senior dev)
- **Q4 (Eliminate):** Wiki updates — onboarding isn't happening this quarter

### Key Insight
PR reviews feel urgent because notifications pile up, but they're not important enough to displace the architecture proposal. Batching reviews to end-of-day prevents them from fragmenting deep work on Q2 items.
</example>
```

### Task 4: Add example to inversion.md

**Files:**
- Modify: `commands/consider/inversion.md`

**Step 1: Add `<example>` block**

Scenario: launching a developer platform.

```markdown
<example>
## Inversion Analysis: Developer Platform Launch

### Desired Outcome
Launch an internal developer platform adopted by 80% of engineering teams within 6 months.

### Guaranteed Failure Modes
1. Build without talking to teams about their actual pain points — likelihood: high, severity: high
2. Require migration from existing tools on day one — likelihood: medium, severity: high
3. No documentation or onboarding path — likelihood: medium, severity: medium
4. Platform team operates in isolation, slow to fix bugs — likelihood: medium, severity: high
5. Mandate adoption top-down without demonstrating value — likelihood: high, severity: medium
6. Over-engineer for future scale instead of solving current problems — likelihood: medium, severity: medium

### Avoidance Strategies
| Failure Mode | Avoidance Strategy |
|-------------|-------------------|
| Build without input | Interview 5 teams before writing code; co-design with 2 pilot teams |
| Forced migration | Run alongside existing tools; migrate incrementally when platform proves faster |
| No docs | Onboarding guide ships with v1; pilot teams write the first tutorials |
| Slow bug response | Dedicated on-call rotation; SLA of 1 business day for blocking issues |
| Top-down mandate | Demo wins from pilot teams; let adoption spread organically before any mandates |
| Over-engineering | Ship MVP for the top 3 pain points only; add capabilities based on demand |

### Positive Plan
Start with pilot teams, solve their top 3 pain points, ship fast bug fixes, let results drive adoption. Documentation and incremental migration from day one.

### Blind Spots
We haven't considered what happens if pilot teams' pain points diverge significantly — the platform might fragment into team-specific solutions rather than a shared one.
</example>
```

### Task 5: Add example to occams-razor.md

**Files:**
- Modify: `commands/consider/occams-razor.md`

**Step 1: Add `<example>` block**

Scenario: diagnosing why API response times increased.

```markdown
<example>
## Occam's Razor Analysis: API Response Time Increase

### Observations to Explain
- P95 latency increased from 200ms to 800ms last Tuesday
- No code deployments that day
- Database CPU is normal
- Only affects the /search endpoint
- Traffic volume unchanged

### Candidate Explanations
| Explanation | Assumptions | Fits all facts? |
|-------------|------------|----------------|
| Search index corrupted | 1 (index can silently corrupt) | Yes |
| Upstream provider slowed down | 1 (provider had an incident) | Yes — /search calls external API |
| DNS resolution intermittent | 2 (DNS issue + only affects one endpoint) | Partial — why only /search? |
| Memory leak in search service | 2 (leak exists + triggered Tuesday) | Partial — would worsen over time |

### Simplest Sufficient Explanation
Upstream search provider experienced degradation. This requires only one assumption (provider incident), explains why only /search is affected (it's the only endpoint calling that provider), and fits the Tuesday timing without needing a code change.

### Distinguishing Evidence
Check the provider's status page for Tuesday incidents. If clean, run `curl` directly against the provider API to measure current latency. If provider is fast, re-examine the search index.
</example>
```

### Task 6: Add example to second-order.md

**Files:**
- Modify: `commands/consider/second-order.md`

**Step 1: Add `<example>` block**

Scenario: introducing mandatory code review.

```markdown
<example>
## Second-Order Analysis: Mandatory Code Review Policy

### Proposed Action
Require two approvals on every pull request before merge.

### Consequence Chain
- **1st order:** PRs take longer to merge (reviewers must be available)
  - **2nd order:** Developers batch smaller changes into larger PRs to reduce review overhead
    - **3rd order:** Larger PRs get superficial reviews — reviewers skim instead of reading carefully
- **1st order:** More eyes on code catches bugs earlier
  - **2nd order:** Developers rely on reviewers as a safety net, writing less carefully
- **1st order:** Junior developers get feedback and learn faster
  - **2nd order:** Senior developers spend significant time reviewing, reducing their own output
    - **3rd order:** Seniors become bottlenecks; review queues grow; teams start rubber-stamping

### Feedback Loops
- Larger PRs → worse reviews → more bugs slip through → pressure to add more reviewers → even longer queues (amplifying)
- Junior learning → better code quality over time → reviews get faster (dampening, but slow)

### Unintended Consequences
- Review bottlenecks create a two-class system: people who review and people who wait. Resentment builds.
- Two-approval rule optimizes for risk avoidance but penalizes the 90% of changes that are low-risk.

### Revised Assessment
Keep mandatory review but with one approval, not two. Add a "trivial" label for changes under 20 lines that need only one reviewer. This preserves the learning and bug-catching benefits while avoiding the bottleneck spiral.
</example>
```

### Task 7: Add example to swot.md

**Files:**
- Modify: `commands/consider/swot.md`

**Step 1: Add `<example>` block**

Scenario: evaluating an open-source project's competitive position.

```markdown
<example>
## SWOT Analysis: Open-Source CLI Tool Competitive Position

### Internal
| Strengths | Weaknesses |
|-----------|-----------|
| Zero dependencies — easy install | No GUI — limits non-technical adoption |
| Fast execution (stdlib only) | Small maintainer team (2 active) |
| Clear documentation and examples | No plugin ecosystem yet |

### External
| Opportunities | Threats |
|--------------|---------|
| Growing demand for CLI-first developer tools | Well-funded competitor launching similar tool |
| Conference talk accepted — visibility boost | Key maintainer may leave in 6 months |
| Integration request from popular IDE plugin | AI-assisted alternatives reducing need for CLI tools |

### Strategic Options
- **Leverage (S+O):** Zero-dep install + IDE integration request = ship an IDE adapter that wraps the CLI, capturing both audiences
- **Defend (W+T):** Small team + competitor launch = focus on what competitor can't easily copy (simplicity, no vendor lock-in)
- **Improve (W+O):** No plugins + conference visibility = announce plugin API at conference to attract contributors

### Priority Action
Ship the IDE adapter integration — it leverages the core strength (simple CLI) to reach a new audience (IDE users) at exactly the moment visibility is growing (conference).
</example>
```

### Task 8: Add example to 10-10-10.md

**Files:**
- Modify: `commands/consider/10-10-10.md`

**Step 1: Add `<example>` block**

Scenario: whether to rewrite a legacy system.

```markdown
<example>
## 10-10-10 Analysis: Rewrite Legacy Billing System

### Decision
Option A: Rewrite the billing system from scratch in a modern stack.
Option B: Incrementally refactor the existing system module by module.

### Time Horizon Assessment
| Option | 10 Minutes | 10 Months | 10 Years |
|--------|-----------|-----------|---------|
| A (Rewrite) | Exciting — fresh start, modern tools | Painful — 6 months in, still not shipped, maintaining two systems | Either transformative (if it ships) or a cautionary tale (if it stalls) |
| B (Refactor) | Frustrating — same old codebase | Steady progress — 3 modules modernized, billing still works | Fully modernized system, no big-bang risk, but took longer |

### Divergence Points
10-minute excitement for the rewrite masks the 10-month reality: rewrites routinely take 2-3x estimated time, and the team must maintain the old system in parallel. The refactor feels worse now but avoids the dual-maintenance trap.

### Dominant Time Horizon
10 months — this is a business-critical system. The risk of a stalled rewrite leaving the team maintaining two billing systems for a year outweighs the long-term elegance argument.

### Decision
Incremental refactor (Option B). The 10-month horizon reveals that the rewrite's main appeal is emotional (fresh start) rather than practical. Refactoring delivers value continuously without betting on a single high-risk cutover.
</example>
```

### Task 9: Add example to one-thing.md

**Files:**
- Modify: `commands/consider/one-thing.md`

**Step 1: Add `<example>` block**

Scenario: improving developer onboarding.

```markdown
<example>
## One Thing Analysis: Improving Developer Onboarding

### Goal
Reduce time-to-first-commit for new engineers from 2 weeks to 3 days.

### Candidate Actions
| Action | Domino Effect | Makes others easier? |
|--------|-------------|---------------------|
| Write comprehensive onboarding docs | New hires self-serve answers | Partially — still need environment to work |
| Fix the dev environment setup script | New hires have working code on day 1 | Yes — unblocks everything downstream |
| Assign onboarding buddies | New hires get personalized help | Partially — buddies still fight the broken setup |
| Create a "first task" ticket template | Clear first contribution path | Partially — useless if environment isn't working |
| Record architecture walkthrough video | Context available on-demand | No — doesn't unblock the setup bottleneck |

### The One Thing
Fix the dev environment setup script. Every other onboarding improvement assumes the new hire has a working environment. A broken setup script means buddies spend their time debugging Docker instead of teaching architecture, docs describe a system the new hire can't run, and first tasks can't be attempted.

### Definition of Done
A new hire can run `make setup` on a fresh laptop and have all services running with seed data in under 30 minutes. Tested by having someone outside the team follow the instructions.

### Say No To
Pause the architecture video project and the onboarding doc rewrite until setup works. Both are wasted effort if people can't run the code.
</example>
```

### Task 10: Add example to opportunity-cost.md

**Files:**
- Modify: `commands/consider/opportunity-cost.md`

**Step 1: Add `<example>` block**

Scenario: build vs buy for authentication.

```markdown
<example>
## Opportunity Cost Analysis: Build vs Buy Authentication

### Decision
Whether to build a custom auth system or use Auth0.

### Options
| Option | Direct Value | Direct Cost | Key Tradeoff |
|--------|-------------|-------------|-------------|
| A: Build custom | Full control, no vendor dependency | 3 engineer-months, ongoing maintenance | Time to market vs control |
| B: Auth0 | Ships in 1 week, managed security patches | $1,200/month, vendor lock-in | Cost vs speed |
| Do nothing | No cost | Users can't log in — not viable | — |

### Opportunity Cost
If we build custom, we forgo 3 engineer-months of product work. At our current pace, that's the entire notifications feature our top 5 customers are waiting for. The opportunity cost isn't $0 — it's the revenue risk of delaying notifications by a quarter.

### Hidden Costs
- Custom auth requires ongoing security patching — not a one-time build
- Auth0 lock-in means switching later requires re-implementing session management
- Custom auth expertise leaves with the engineer who built it

### Verdict
Auth0 justified. The opportunity cost of building (delayed notifications = revenue risk) exceeds Auth0's dollar cost by roughly 10x. Revisit only if we outgrow Auth0's pricing tier or need auth behavior they can't support.
</example>
```

### Task 11: Add example to via-negativa.md

**Files:**
- Modify: `commands/consider/via-negativa.md`

**Step 1: Add `<example>` block**

Scenario: simplifying a deployment pipeline.

```markdown
<example>
## Via Negativa Analysis: Deployment Pipeline

### Current State
Deployment pipeline has 12 steps: lint, unit test, integration test, build Docker image, push to registry, deploy to staging, run smoke tests, wait for manual approval, deploy to canary, monitor for 30 minutes, deploy to production, run production smoke tests.

### Removal Candidates
| Element | Remove? | What improves | What breaks |
|---------|---------|--------------|-------------|
| Manual approval gate | Yes | Deploy time drops 2-4 hours (waiting for approver) | Nothing — canary + smoke tests catch issues automatically |
| Separate lint step | Yes | 2 min saved — linting runs in IDE and pre-commit hooks already | Nothing — issues caught earlier in workflow |
| Staging environment | Yes | Eliminates a flaky environment that causes 30% of pipeline failures | Need canary to be reliable (it already is) |
| 30-min canary monitor | No | — | Removing loses the safety net for slow-burn issues |
| Integration tests | No | — | Only place we catch cross-service contract breaks |

### Recommended Removals
1. Manual approval gate — replaced by automated canary monitoring, which is more consistent than a human glancing at dashboards
2. Separate lint step — redundant with pre-commit hooks; lint errors haven't reached CI in 4 months
3. Staging environment — flaky environment causes more failed deploys than it prevents; canary on production traffic is a better signal

### Simplified Version
9 steps: unit test, integration test, build, push, deploy canary, monitor 30 min, deploy production, smoke test. Still catches regressions, still has gradual rollout, but 30% faster and no flaky staging.

### What NOT to Remove
The 30-minute canary monitor looks like wasted time but caught a memory leak last month that smoke tests missed. It's load-bearing.
</example>
```

### Task 12: Add example to pareto.md

**Files:**
- Modify: `commands/consider/pareto.md`

**Step 1: Add `<example>` block**

Scenario: reducing customer support ticket volume.

```markdown
<example>
## Pareto Analysis: Reducing Support Ticket Volume

### Outcome to Optimize
Reduce monthly support tickets from 500 to under 200.

### Input-to-Outcome Mapping
| Input | Est. Contribution | Cumulative |
|-------|------------------|-----------|
| Password reset issues | 35% | 35% |
| Confusing billing page | 25% | 60% |
| API error messages unclear | 15% | 75% |
| Feature requests misfiled as bugs | 10% | 85% |
| Onboarding confusion | 8% | 93% |
| Account deletion requests | 4% | 97% |
| Other | 3% | 100% |

### Vital Few (the 20%)
- Password resets: add self-service reset flow (currently requires support ticket to trigger)
- Billing page: redesign the plan comparison table — 80% of billing tickets ask "what's the difference between plans?"

### Trivial Many (candidates for reduction)
- Feature requests as bugs: not worth building a routing system for 10% of volume
- Account deletion: low volume, legally required to handle manually anyway

### Recommended Focus Shift
Two changes (self-service password reset + billing page redesign) would eliminate ~60% of tickets. Everything else combined is less impactful than either of these alone. Start with password reset — it's a weekend project with the highest single-category impact.
</example>
```

### Task 13: Add example to reversibility.md

**Files:**
- Modify: `commands/consider/reversibility.md`

**Step 1: Add `<example>` block**

Scenario: choosing a database for a new service.

```markdown
<example>
## Reversibility Analysis: Choosing a Database for the Events Service

### Decision
Use PostgreSQL vs DynamoDB for a new event-sourcing service.

### Classification: One-Way Door

### Reversibility Assessment
- **Can it be undone?** Partially — data can be migrated, but schema design and query patterns are deeply coupled
- **Cost to reverse:** High — rewriting data access layer, migrating data, revalidating correctness
- **Time to reverse:** Months (data migration + regression testing + gradual cutover)
- **Blast radius:** Team — affects the events team and all downstream consumers of the event stream

### If One-Way Door
- **What makes it irreversible:** Query patterns, schema design, and operational tooling all become database-specific within weeks. After 6 months of production data, migration becomes a project in itself.
- **Ways to reduce commitment:** Start with a repository abstraction layer so business logic doesn't call database APIs directly. Build for PostgreSQL first (team knows it), but keep the option to swap the storage backend if DynamoDB's scaling becomes necessary.
- **Recommendation:** Analyze thoroughly. Default to PostgreSQL (known quantity, team expertise, adequate for projected scale). Revisit DynamoDB only if event volume exceeds 50K/sec — a threshold we're unlikely to hit in year one.
</example>
```

### Task 14: Add example to circle-of-competence.md

**Files:**
- Modify: `commands/consider/circle-of-competence.md`

**Step 1: Add `<example>` block**

Scenario: a backend team evaluating whether to build a mobile app.

```markdown
<example>
## Circle of Competence: Should Our Backend Team Build the Mobile App?

### Domain
Deciding whether our team of 3 backend engineers should build the iOS/Android app ourselves or hire specialists.

### Inside (know well)
- REST API design and backend infrastructure
- PostgreSQL performance tuning and data modeling
- CI/CD pipelines and production monitoring
- Python and Go ecosystem

### Edge (familiar but not deep)
- React Native (one engineer did a tutorial project)
- Mobile app architecture patterns (read about MVVM, never shipped it)
- App Store submission process (know it exists, never done it)

### Outside (don't know)
- iOS/Android platform-specific performance optimization
- Mobile-specific UX patterns (gesture navigation, offline-first)
- App Store review guidelines and rejection recovery
- Push notification infrastructure at scale

### Decision Requirements
Building the mobile app requires deep knowledge in all three zones. API integration is inside our circle, but the entire frontend layer — UI, platform APIs, store submission — is outside it.

### Strategy
Bring in outside expertise. Hire or contract a mobile developer for the app shell and platform integration. Our team owns the API layer and backend (inside our circle). The mobile specialist handles what we'd spend months learning poorly. Review architecture decisions together so knowledge transfers over time.
</example>
```

### Task 15: Add example to map-vs-territory.md

**Files:**
- Modify: `commands/consider/map-vs-territory.md`

**Step 1: Add `<example>` block**

Scenario: a sprint velocity estimate.

```markdown
<example>
## Map vs Territory: Sprint Velocity Predictions

### The Map (current model)
"Our team velocity is 40 story points per sprint, so this 120-point epic will take 3 sprints."

### Where Map Matches Territory
- Average velocity over the last 6 sprints is genuinely ~40 points
- Team composition hasn't changed recently
- The work is in a familiar domain (same service, similar features)

### Where Map Simplifies
- Velocity averages hide variance (actual range: 28-52 points) — risk: medium
- Story points assume uniform complexity, but this epic has an unfamiliar integration — risk: high
- "3 sprints" assumes no interruptions (production incidents, unplanned work) — risk: medium

### Where Map Is Blank
- The epic depends on an external team's API that isn't built yet — risk: high
- Two engineers have PTO overlapping in sprint 2 — risk: medium
- We've never estimated an epic this large as a single block before — risk: low

### Highest-Risk Gap
The external API dependency. Our velocity model assumes all work is within our control. If the external team delivers late, sprint 2 stalls regardless of our capacity.

### Reality Check
Ask the external team for their delivery date and confidence level. If they can't commit, re-sequence the epic to pull forward work that doesn't depend on their API. Adjust the estimate to 4-5 sprints to account for the dependency and PTO gaps.
</example>
```

### Task 16: Add example to hanlons-razor.md

**Files:**
- Modify: `commands/consider/hanlons-razor.md`

**Step 1: Add `<example>` block**

Scenario: a colleague seems to be blocking your PR.

```markdown
<example>
## Hanlon's Razor: PR Sitting Unreviewed for a Week

### Situation
You submitted a PR 7 days ago, pinged the assigned reviewer twice, and got no response. The reviewer has been merging other PRs during this time.

### Uncharitable Interpretation
The reviewer is deliberately ignoring your PR because they disagree with your approach and want to passively block it rather than give direct feedback.

### Charitable Alternatives
1. They're prioritizing PRs for the release deadline this week and yours isn't on the critical path — plausibility: high
2. They saw the PR, noted it was large (400+ lines), and keep deferring it for a time block they haven't found — plausibility: high
3. Your notification got buried — Slack/email volume means pings are easily missed — plausibility: medium

### Distinguishing Evidence
Check whether the PRs they've been reviewing are smaller or release-critical. Ask directly: "Is this a good time, or should I find another reviewer?" Their response will distinguish between "busy" and "avoiding."

### Most Likely Explanation
PR size + competing priorities. A 400-line PR requires 30-60 minutes of focused review. During a release crunch, that time block doesn't exist. The other merged PRs were likely small and fast.

### Appropriate Response
Break the PR into 2-3 smaller PRs if possible. Message the reviewer offering to walk through the changes in 15 minutes to reduce their review burden. If still no response after the offer, reassign to a different reviewer without resentment.
</example>
```

### Task 17: Commit all consider command examples

**Step 1: Verify all 16 files have examples**

```bash
for f in commands/consider/*.md; do grep -l '<example>' "$f" || echo "MISSING: $f"; done
```

Expected: all 16 files listed, no "MISSING" lines.

**Step 2: Run tests**

```bash
uv run python -m pytest tests/ -v
```

Expected: all tests pass.

**Step 3: Commit**

```bash
git add commands/consider/
git commit -m "feat: add worked examples to all 16 consider command models (#126)"
```

---

## Part 2: Research Skill Instruction Density Reduction (#124)

**Principles for this part:**
- Each reference file should be small, discrete, and cover one concern
- Files must be mutually exclusive (no duplicated procedures across files)
- SKILL.md is the entry point — it should follow instructional design best practices (primacy, ordering, no lost-in-the-middle)
- Trim each file individually: "would the model do the wrong thing without this?"
- File count may go up, down, or stay the same — it's not a goal
- The research skill's write-to-disk phase gates mean references load on demand, not all at once
- **Deterministic stays in code, reasoning stays in skills.** Instructions that tell the model to run Python scripts (`audit.py`, `reindex.py`, `check_url.py`) are deterministic enforcement anchors — never trim these. Only trim duplicated reasoning/judgment instructions where the same procedure appears in multiple files.

### Task 18: Measure baseline word counts

**Step 1: Record before counts**

```bash
for f in skills/research/SKILL.md skills/research/references/*.md; do wc -w "$f"; done
wc -w skills/research/SKILL.md skills/research/references/*.md | tail -1
```

Expected baseline: ~5,805 total words across 9 files.

Record the output — this is the "before" measurement.

### Task 19: Review python-utilities.md (deterministic tooling reference)

**Files:**
- Review: `skills/research/references/python-utilities.md` (223 words)

**Rationale:** `python-utilities.md` documents the deterministic Python tooling
(`audit.py`, `reindex.py`, `check_url.py`, Document model). Even though these
commands also appear in `research-workflow.md` Phase 6, this file serves as a
dedicated reference that anchors the model to **running the actual tools**.
Per the principle "structure in code, quality in skills" — deterministic tool
references are load-bearing. **Keep this file.**

**Step 1: Apply density test**

- Validate a Single Document section: **KEEP** — deterministic tool reference
- Validate Entire Project section: **EVALUATE** — is this used during research?
  If not, it may be extraneous to this skill (but harmless at 2 lines).
- Regenerate Index Files section: **KEEP** — deterministic tool reference
- Document Model table: **KEEP** — quick reference for frontmatter fields

**Step 2: Trim only if a section is truly extraneous**

If "Validate Entire Project" is never referenced by the research workflow or
SKILL.md, it can be removed. Otherwise leave the file as-is — it's already
223 words and serves a clear purpose.

### Task 20: Make claim-verification.md MECE with research-workflow.md

**Files:**
- Modify: `skills/research/references/claim-verification.md`

**Rationale:** `claim-verification.md` and `research-workflow.md` both describe
the Phase 5.5a/5.5b procedure. The workflow owns the procedure (step-by-step
execution). The reference should own the lookup data (types, formats, statuses,
edge cases). Currently they overlap — make them MECE.

**Step 1: Identify what each file should own**

`research-workflow.md` owns (KEEP as-is):
- Phase 5.5a procedure steps 1-4
- Phase 5.5b procedure steps 1-5
- Gate conditions

`claim-verification.md` should own (reference lookup only):
- Claim Types table (4 types) — **KEEP, unique**
- Claims Table Format — **KEEP, unique**
- Resolution Statuses table (5 statuses) — **KEEP, unique**
- Verification Questions by Type — **KEEP, extracted from the procedure as a quick-reference** (currently buried in procedure steps)
- Contradiction Resolution flowchart — **KEEP, unique**
- human-review Triggers — **KEEP, unique**

`claim-verification.md` should NOT contain:
- Phase 5.5a procedure (duplicates workflow)
- Phase 5.5b procedure (duplicates workflow)

**Step 2: Rewrite claim-verification.md as reference lookup**

The resulting file:

```markdown
# Claim Verification Reference

Lookup reference for claim types, table format, resolution statuses, and edge
cases. The step-by-step verification procedure lives in `research-workflow.md`
Phases 5.5a and 5.5b.

## Claim Types (4)

Register these claim types — they map to observed fabrication failure modes.

| Type | Definition | Example |
|------|-----------|---------|
| quote | Verbatim text attributed to a person/source | "Software is eating the world" — Andreessen |
| statistic | Specific number, percentage, or quantity | "30+ integrations available" |
| attribution | Action or role attributed to a person/org | "Chesky founded Airbnb" |
| superlative | Claim of primacy, extremity, or uniqueness | "the first company to achieve..." |

General observations, trend descriptions, and methodology notes do NOT need
registration. Only register claims that assert a specific, verifiable fact.

## Claims Table Format

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Software is eating the world" | quote | [1] | unverified |
| 2 | 30+ integrations | statistic | [3] | unverified |

- `Source` references map to the numbered Sources table (e.g., `[1]` = first source)
- All claims start as `unverified`
- Claims without a citeable source should still be registered with source marked `—`

## Resolution Statuses (5)

| Status | Meaning |
|--------|---------|
| verified | Passed CoVe self-check AND citation re-verification confirmed source support |
| corrected | Didn't match source; updated to match (note original claim in parentheses) |
| removed | Not found in source; claim removed from document body |
| unverifiable | Source couldn't be fetched (403/timeout); claim kept but flagged in document |
| human-review | Ambiguous automated result, or uncited claim that CoVe couldn't confirm |

## Verification Questions by Type

When generating CoVe verification questions, use these type-specific patterns:
- quote: "What exact words did [person] say about [topic]?"
- statistic: "What is the actual number for [metric]?"
- attribution: "What role did [person] play in [event]?"
- superlative: "Which [entity] was actually the first/largest/most [claim]?"

## Contradiction Resolution

When CoVe contradicts a claim:

CoVe contradicts claim
  → Does the claim have a cited source?
    → YES: Escalate to Phase 5.5b (citation re-verification)
           Source confirms CoVe answer → corrected, update claim, note diff
           Source confirms original claim → verified
           Source is ambiguous → human-review
           Source can't be fetched → human-review
    → NO: human-review

The source is always the tiebreaker between the draft and CoVe. When there
is no source, escalate to the human.

## human-review Triggers

These cases always get `human-review` regardless of CoVe/citation results:
- Direct quotes attributed to named individuals (highest fabrication risk)
- Statistics where the source contains a nearby but different number
- Attributions where the source describes a different role or action
- Any claim with no cited source that CoVe contradicts
```

**Step 3: Verify workflow references**

Confirm `research-workflow.md` Phases 5.5a and 5.5b still reference
`claim-verification.md` for types/formats/statuses. These references remain
accurate since we kept that content — we only removed the duplicated procedure.

### Task 21: Trim source-verification.md

**Files:**
- Modify: `skills/research/references/source-verification.md`

**Rationale:** `source-verification.md` (188 words) is a discrete concern
(mechanical URL checking) separate from `source-evaluation.md` (quality
assessment). Keep them as separate files. But trim: the "When to Run" section
duplicates what `research-workflow.md` Phase 3 already specifies.

**Step 1: Apply density test**

- "When to Run" section (lines 7-9): **TRIM** — workflow Phase 3 already
  specifies "after Phase 2, before SIFT evaluation"
- "How to Run" section: **KEEP** — the `uv run` command and result fields
  are mechanical reference
- "What to Do with Results" section: **KEEP** — drop/keep decision logic
  is a judgment call the model needs

**Step 2: Remove the "When to Run" section**

Remove lines 7-9 ("After Phase 2... before entering the SIFT pipeline.").
The intro line ("Mechanical URL verification...") already provides sufficient
context.

### Task 22: Trim source-evaluation.md

**Files:**
- Modify: `skills/research/references/source-evaluation.md`

**Rationale:** `source-evaluation.md` (334 words) is already fairly lean.
Apply density test to each section.

**Step 1: Apply density test**

- Source Hierarchy (6 tiers with examples): **KEEP** — model needs tier
  definitions to classify sources correctly
- Authority Annotation Format: **KEEP** — shows where annotations go
  (frontmatter vs body), which is a non-obvious convention
- Red Flags: **KEEP** — these are judgment calls (circular sourcing,
  survivorship bias) that the model wouldn't reliably catch without prompting

**Conclusion:** No cuts. This file is already concise and MECE.

### Task 23: Trim research-workflow.md

**Files:**
- Modify: `skills/research/references/research-workflow.md`

**Rationale:** `research-workflow.md` (2,052 words) is the largest reference.
It's the procedural backbone — phase-by-phase execution. Apply density test
to each phase, looking for content that either duplicates other references
or that the model handles correctly without prompting.

**Step 1: Apply density test per phase**

- **Resuming After Context Reset** (lines 10-23): **KEEP** — this is unique
  and critical for the write-to-disk design
- **Phase 1: Frame** (lines 25-46): Review the source diversity note (lines
  41-46). **TRIM if redundant** — check whether this duplicates content in
  SKILL.md or sift-framework.md
- **Phase 2: Gather** (lines 48-130): The search protocol JSON format and
  the inline HTML comment explanation (lines 120-128) are verbose.
  **EVALUATE** — is the 9-line explanation of why the protocol lives in an
  HTML comment necessary? The model would place it there if told to; the
  "why" may be extraneous instruction.
- **Phase 3: Verify & Evaluate** (lines 132-183): This phase contains both
  URL verification (deterministic — runs `check_url.py`) and SIFT evaluation
  (model reasoning). **PROTECT all `uv run` commands and tool invocation
  instructions** — these are deterministic enforcement anchors, not candidates
  for trimming. Only evaluate whether the SIFT evaluation prose duplicates
  what's already in `sift-framework.md`. If the inline SIFT steps are just
  pointers ("see `references/sift-framework.md`"), they're fine. If they
  restate the full SIFT procedure, that's reasoning duplication — trim.
- **Phase 5.5a/5.5b** (lines 235-278): These reference `claim-verification.md`
  and provide the procedure. After Task 20 made claim-verification.md a
  lookup-only reference, the workflow correctly owns the procedure. **KEEP.**
- **Phase 6: Finalize** (lines 280-345): The search protocol formatting
  instructions (lines 292-307) are detailed. **KEEP** — this is a mechanical
  format the model needs to produce correctly.
- **Quality Checklist** (lines 328-345): **KEEP** — this is the final
  gate and uses recency position (end of file) per best practices.

**Step 2: Make targeted trims**

For each section flagged above, make the specific edit. Do NOT rewrite
sections that passed the density test. Only touch what's flagged.

**Step 3: Verify all cross-references**

After trimming, grep for all `references/` paths in the file and confirm
each target file exists.

### Task 24: Audit SKILL.md against instructional design best practices

**Files:**
- Modify: `skills/research/SKILL.md`

**Rationale:** SKILL.md is the entry point that loads first. Per instructional
design research: critical constraints should be at the beginning (primacy),
output format and quality criteria at the end (recency), and supporting detail
in the middle. Check current structure against this.

**Step 1: Assess current SKILL.md structure**

Current order (806 words):
1. Frontmatter (lines 1-21)
2. Intro paragraph (lines 23-28)
3. Mode Detection table (lines 30-47)
4. Workflow reference pointer (lines 49-52)
5. Phase Gates table (lines 54-68) — **critical constraints**
6. Common Deviations (lines 71-84) — **critical constraints**
7. Output Document Format (lines 86-101)
8. Document Standards (lines 107-108)
9. Key Rules (lines 110-134) — **critical constraints**

**Step 2: Check for issues**

Evaluate:
- **Primacy:** Are the most critical instructions first? Phase Gates (item 5)
  and Common Deviations (item 6) are critical but come after Mode Detection.
  Mode Detection is important but less critical — getting the mode wrong is
  recoverable; skipping phase gates is not.
- **Redundancy:** "Common Deviations" (lines 71-84) and "Key Rules" (lines
  110-134) — do they overlap? Both say "don't skip phases" in different words.
  Check whether they can be consolidated without losing distinct value.
- **Lost-in-the-middle:** "Document Standards" (line 107-108) is a one-liner
  pointing to AGENTS.md, sandwiched between two important sections. It's easy
  to miss. Evaluate whether it adds value or is extraneous.
- **Reference duplication:** Do any "Key Rules" restate what's already in a
  reference file? If a rule says "SIFT every source, see sift-framework.md",
  the rule is a pointer, not a duplicate — that's fine. But if it restates
  the SIFT procedure, that's duplication.

**Step 3: Restructure if warranted**

Only restructure if the audit found concrete issues. Possible changes:
- Move Phase Gates earlier (before Mode Detection) if primacy matters more
- Consolidate Common Deviations into Key Rules if they overlap
- Remove Document Standards line if it's extraneous

**Do NOT restructure for aesthetic reasons.** Only change what the density test
or primacy/recency analysis identifies as a problem.

### Task 25: Trim remaining references (sift-framework, challenge-phase, research-modes)

**Files:**
- Review: `skills/research/references/sift-framework.md` (443 words)
- Review: `skills/research/references/challenge-phase.md` (461 words)
- Review: `skills/research/references/research-modes.md` (565 words)

**Rationale:** Apply the density test to each file individually. These are
already reasonably sized. Only trim if specific sections fail the test.

**Step 1: sift-framework.md**

- SIFT steps (S, I, F, T) with agent actions: **KEEP** — model needs these
- SIFT Intensity by Mode table: **CHECK** — does `research-modes.md` already
  have this? If duplicated, keep it in one place only (whichever is more
  natural). If both files have mode-specific tables, that's not MECE.

**Step 2: challenge-phase.md**

- Assumptions Check procedure: **KEEP** — unique
- ACH procedure with anti-anchoring step: **KEEP** — unique and non-obvious
- Premortem procedure: **KEEP** — unique
- Output format examples: **KEEP** — model needs format reference

**Step 3: research-modes.md**

- Mode Matrix table: **CHECK for MECE** — does SKILL.md's Mode Detection
  table duplicate information? SKILL.md maps question patterns → modes.
  research-modes.md maps modes → parameters (sources, rigor, etc.). These
  are complementary (MECE), not duplicated, if they don't repeat the same
  columns.
- Mode Descriptions (8 descriptions): **EVALUATE** — are all descriptions
  necessary? Or would the model behave correctly with just the Mode Matrix
  table? If descriptions are just prose restatements of the table, trim them.

**Step 4: Make targeted trims**

Only edit files where specific sections failed the density test or MECE check.

### Task 26: Measure after word counts and run tests

**Step 1: Measure after counts**

```bash
for f in skills/research/SKILL.md skills/research/references/*.md; do wc -w "$f"; done
wc -w skills/research/SKILL.md skills/research/references/*.md | tail -1
```

Compare to baseline (5,805 words). Report the delta.

**Step 2: Run tests**

```bash
uv run python -m pytest tests/ -v
```

Expected: all tests pass.

**Step 3: Verify skill audit passes**

```bash
uv run python -m pytest tests/test_skill_audit.py -v
```

### Task 27: Commit research skill density reduction

**Step 1: Review all changes**

```bash
git diff --stat
git diff
```

Verify:
- No behavioral content silently dropped — every removal justified
- All `references/` paths in SKILL.md and research-workflow.md point to existing files
- Phase gate structure in SKILL.md unchanged (or improved per primacy audit)
- Reference files are MECE — no procedure appears in two files
- All deterministic tool invocations (`uv run` commands for `audit.py`, `reindex.py`, `check_url.py`) preserved

**Step 2: Commit**

```bash
git add skills/research/
git commit -m "refactor: reduce research skill instruction density (#124)

Make claim-verification.md MECE with workflow (lookup only, no procedure).
Trim duplicated reasoning across references.
Audit SKILL.md structure per instructional design best practices.
Preserve all deterministic tool invocations (audit, reindex, check_url).

Before: 5,805 words across 9 files
After: [X] words across [Y] files
Removals justified: [summary]"
```

---

## Part 3: Final Verification

### Task 28: Run full test suite and update design doc

**Step 1: Full test suite**

```bash
uv run python -m pytest tests/ -v
```

**Step 2: Update design doc with results**

Edit `docs/plans/2026-03-06-research-density-and-examples-design.md` to add a Results section with:
- Before/after word counts for #124
- Summary of what was trimmed and why
- Confirmation all 16 consider models have examples for #126
- Test results

**Step 3: Commit**

```bash
git add docs/plans/
git commit -m "docs: update design doc with implementation results"
```
