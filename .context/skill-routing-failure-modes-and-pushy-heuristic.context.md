---
name: "Skill Routing Failure Modes and the Pushy Heuristic"
description: "Undertriggering and overtriggering are the two opposing routing failure modes; the 'pushy description' is Anthropic's documented workaround for undertriggering, with unquantified overtriggering risk"
type: concept
confidence: moderate
created: 2026-04-11
updated: 2026-04-11
sources:
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html
  - https://gorilla.cs.berkeley.edu/leaderboard.html
  - https://arxiv.org/abs/2512.07497
  - https://arxiv.org/html/2510.02554v1
related:
  - docs/context/skill-progressive-loading-and-routing.context.md
  - docs/context/tool-description-quality-and-consolidation.context.md
  - docs/research/2026-04-11-skill-description-routing.research.md
---

Routing failures in skill ecosystems divide into two types with opposite causes. Knowing which failure is occurring determines the fix.

**Undertriggering** — Claude fails to invoke the skill when a matching request is made. The skill exists but is invisible to the routing mechanism. Common causes: the description uses technical vocabulary that doesn't match how users naturally phrase requests; the description focuses on capability rather than trigger conditions. Fix: add keywords users would naturally say; make the trigger clause explicit.

**Overtriggering** — Claude invokes the skill when it shouldn't. Common forms: a skill fires on requests intended for a different skill (ambiguous overlap); a skill fires when the task context makes invocation incorrect (e.g., re-authenticating when authentication already completed; substituting data when no match exists). Fix: make the description more specific and narrow the trigger scope. Hard fix: `disable-model-invocation: true` removes the skill from context entirely (explicit `/skill-name` invocation only).

Empirical examples of both failure modes appear in the Berkeley Function Calling Leaderboard V3 (S7): undertriggering — models fail to check fuel level before deciding on a route, omitting a necessary prerequisite call; overtriggering — models re-authenticate users who are already authenticated. The KAMI benchmark (S12) documents tool avoidance (undertriggering) as a model-specific pattern: Granite 4 Small consistently avoided Python execution for CSV tasks and tried to eyeball values manually instead. BFCL V4 (S8) formalizes overtriggering measurement as IrrelAcc — the fraction of no-tool-needed queries where the model correctly abstains — tested across 875 entries.

**The pushy description heuristic.** Anthropic's documentation identifies undertriggering as the default bias: "Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful." The documented workaround is to make descriptions assertive: include explicit imperative clauses such as "Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics..." This is prescriptive practitioner guidance from Anthropic (S1), not an experimentally ablated fix.

**The overtriggering risk from pushy language is unquantified.** Adversarial research (ToolTweak, S14) demonstrates that assertive wording and subjective cues in descriptions raise a tool's selection rate from ~20% to 81% within a task-matched 5-tool slate. This shows pushy language has causal force on routing. However, ToolTweak measured selection rates within relevant query sets, not false-positive rates on off-topic queries. Whether assertive descriptions increase activation when the user's intent has no relation to the skill — the real overtriggering risk — was not studied. The risk is real but unquantified (MODERATE confidence).

**Practical guidance for skill authors:**
- Start with neutral, specific language. If undertriggering is observed, add explicit trigger keywords.
- Scope trigger clauses tightly — list the specific contexts and phrases that should activate the skill.
- If a pushy description causes overtriggering, narrow the trigger clause before reaching for `disable-model-invocation: true`.
- Monitor routing in real scenarios and iterate. Routing failures are almost always description quality problems, not library size problems.
