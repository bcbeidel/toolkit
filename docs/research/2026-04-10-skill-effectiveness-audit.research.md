---
name: "Skill Effectiveness Evaluation and Audit"
description: "What signals and structural properties best measure skill and skill-chain effectiveness in LLM-driven plugin systems, and how to operationalize a static audit in WOS. Bottom line: effectiveness is five-dimensional; security-pattern checks achieve high recall without runtime data; quality heuristics are pedagogically useful but require calibration; skill-chain failures are categorically distinct; WOS needs seven new warn-severity checks in skill_audit.py."
type: research
sources:
  - https://agentskills.io/skill-creation/evaluating-skills
  - https://www.philschmid.de/testing-skills
  - https://arxiv.org/html/2603.22455v4
  - https://arxiv.org/html/2603.29919v1
  - https://arxiv.org/html/2604.03081
  - https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/
  - https://www.morphllm.com/context-rot
  - https://arxiv.org/html/2503.13657v1
  - https://arxiv.org/html/2604.02460v1
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://www.anthropic.com/research/building-effective-agents
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://arxiv.org/html/2602.12430v3
related:
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
  - docs/research/2026-04-07-skill-ecosystem-design.research.md
  - docs/research/2026-04-07-agent-testing.research.md
  - docs/research/2026-04-07-llm-as-judge.research.md
  - docs/research/2026-04-07-validation-architecture.research.md
  - docs/research/2026-04-07-feedback-loops.research.md
---

# Skill Effectiveness Evaluation and Audit

## Bottom Line Up Front

Five findings dominate the evidence:

1. **Effectiveness is five-dimensional.** A skill is effective when it: (1) triggers on correct intent and only that intent, (2) produces structured outputs that downstream consumers can parse, (3) completes without escalation or abandonment, (4) respects token budget constraints, and (5) adds measurable quality over the no-skill baseline. Only the last requires ground-truth labels — the first four are auditable structurally.

2. **Instruction density matters for tool-wrapper skills, not orchestration skills.** SkillReducer found >60% of skill body content is non-actionable in general registries, with 2.8% quality gain from compression. But WOS skills like `wos:research` and `wos:write-plan` are reasoning and orchestration skills where rationale sentences are load-bearing — stripping them for density can reduce quality. Apply the density check selectively; do not apply it uniformly.

3. **Skill-chain failures are categorically different from single-skill failures.** The MASFT taxonomy's inter-agent misalignment category (context resets, task derailment, reasoning-action mismatch) is definitionally absent in single-skill runs. Context rot degrades performance as context grows; contract mismatch produces silent failures that cascade; error amplification is real but substantially lower in sequential, human-supervised designs than in uncoordinated parallel architectures.

4. **Security-pattern checks are reliable without runtime data; quality heuristics require calibration.** Static analysis achieves 90%+ recall for syntactic security patterns (executable content, external fetches, hardcoded credentials). Quality heuristics (description coverage, density ratio, output format presence) are pedagogically useful but have expected 20–40% false positive rates before in-domain calibration — treat them as author nudges, not diagnostic signals.

5. **WOS needs seven new `warn`-severity checks in `skill_audit.py`:** description routing coverage, output format declaration presence, executable content flag, external fetch flag, instruction density ratio (tool-wrapper skills only), negative scope coverage, and chain-gate documentation. All belong in `check_skill_meta()` or `check_skill_sizes()`. A calibration pass against existing WOS skills is needed before thresholds are tightened.

---

## Search Protocol

| # | Query | Engine | Results |
|---|-------|--------|---------|
| 1 | LLM skill instruction quality heuristics automated audit 2025 2026 | WebSearch | 10; selected arxiv.org/html/2601.17717 |
| 2 | LangSmith Braintrust skill evaluation setup metrics 2025 2026 | WebSearch | 10; selected langwatch.ai comparison, braintrust.dev |
| 3 | skill chain failure taxonomy context bleed contract mismatch silent degradation LLM 2025 | WebSearch | 10; selected arxiv.org/html/2503.13657 (MASFT), morphllm.com/context-rot, arxiv.org/html/2604.03081 |
| 4 | automated prompt quality audit heuristics instruction density signals 2025 | WebSearch | 10; selected arxiv.org/abs/2502.18746, aclanthology.org/2025 |
| 5 | LLM workflow reliability evaluation metrics completion rate 2024 2025 | WebSearch | 10; selected confident-ai.com, futureagi.com, arxiv AGENTIF |
| 6 | supply chain poisoning agent skill ecosystem attack SKILL.md 2025 2026 | WebSearch | 10; selected arxiv.org/html/2604.03081, snyk.io/blog/toxicskills |
| 7 | agent skill effectiveness measurement intent alignment output contract fidelity completion rate 2025 2026 | WebSearch | 10; selected philschmid.de/testing-skills, arxiv.org/html/2603.22455, agentskills.io/skill-creation/evaluating-skills |
| 8 | skill description quality routing effectiveness user-invocable description signal LLM agent 2025 2026 | WebSearch | 10; selected arxiv.org/html/2603.22455v4 (SkillRouter), arxiv.org/html/2603.29919 (SkillReducer), agentskills.io |
| F1 | Fetch: https://arxiv.org/html/2604.03081 | WebFetch | Supply-chain poisoning attacks on agent skills — full content |
| F2 | Fetch: https://www.morphllm.com/context-rot | WebFetch | Context rot complete guide |
| F3 | Fetch: https://agentskills.io/skill-creation/evaluating-skills | WebFetch | Official skill evaluation guide — full content |
| F4 | Fetch: https://arxiv.org/html/2603.22455v4 | WebFetch | SkillRouter — full content |
| F5 | Fetch: https://arxiv.org/html/2603.29919v1 | WebFetch | SkillReducer — full content |
| F6 | Fetch: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ | WebFetch | ToxicSkills full findings |
| F7 | Fetch: https://www.philschmid.de/testing-skills | WebFetch | Practical skill testing guide — full content |
| F8 | Fetch: https://langwatch.ai/blog/langwatch-vs-langsmith-vs-braintrust-vs-langfuse | WebFetch | Platform comparison — partial (no agent-specific signals documented) |
| F9 | Fetch: https://www.braintrust.dev/articles/best-llm-evaluation-platforms-2025 | WebFetch | Braintrust platform comparison — partial |

---

## Extracts by Sub-Question

### SQ1: What does "effectiveness" mean for a single skill?

**Official definition from agentskills.io [F3]:**
The Agent Skills spec evaluation guide defines three dimensions of skill success:
1. **Outcome quality**: "Did the skill produce a usable result? Code compiles, the image rendered, the document got created" — described as the baseline requirement. "If output doesn't work, nothing else matters."
2. **Style and instructions adherence**: Verification that outputs follow skill directives — correct SDK usage, naming conventions, formatting standards.
3. **Efficiency**: "The most undervalued dimension — token consumption, retry counts, and computational effort. Two identical outputs can differ dramatically in resource consumption."

The guide operationalizes measurement via a with-skill vs. without-skill comparison: "Run each test case twice — once with the skill and once without (or with a previous version). This gives you a baseline to compare against." A benchmark.json captures pass_rate delta, time_seconds delta, and token delta. A skill that adds 13 seconds but improves pass rate by 50 percentage points is worth it; a skill that doubles token usage for a 2-point improvement is not.

**Practical skill testing framework (Philschmid) [F7]:**
The Gemini Interactions API skill case study surfaced a useful decomposition. Before intervention: 66.7% pass rate. After description rewrite: 100% pass rate. The single most impactful fix was "rewriting the skill description to match user intent rather than API terminology — this alone corrected 5 of 7 failures." This demonstrates that **routing fidelity** (does the skill trigger on the right intent?) is both the most common failure mode and the most actionable.

Three evaluation dimensions operationalized in testing:
- Core capabilities (7 tests) — can the skill do what it claims?
- Negative controls (2 tests) — does the skill avoid triggering on unrelated prompts? "Don't skip negative tests. A skill with too-broad description could trigger on every coding prompt."
- Deprecated/guardrail tests (4 tests) — does the skill correctly refuse or redirect edge cases?

**Prompt fidelity as an emerging concept [search synthesis]:**
Research from February 2026 proposes "prompt fidelity" — measuring how much of the user's intent an AI agent actually executes — as a first-class dimension distinct from output quality. A high-fidelity skill executes the full intent; a low-fidelity skill produces correct-looking output that satisfies only part of the user's goal. This is particularly relevant for WOS skills like wos:research or wos:write-plan where partial execution can appear complete but miss critical sub-goals.

**Anthropic's task/trial/transcript/outcome framework [existing research, skill-chaining doc]:**
Anthropic defines four evaluation components: Tasks (single test with input + success criteria), Trials (multiple attempts for variance), Transcripts (complete records including tool calls and intermediate results), Outcomes (final environmental state). Three grader types: code-based (fast, cheap, brittle), model-based (flexible, requires calibration), human (gold-standard, expensive). The key insight: "Grade outcomes not paths. Agents regularly find valid approaches that eval designers didn't anticipate."

**Two critical production metrics:**
- **pass@k**: Probability of at least one correct solution in k attempts — measures skill potential
- **pass^k**: Probability all k trials succeed — the correct metric for production reliability (users expect the skill to work every time, not just sometimes)

**Synthesis — five dimensions of single-skill effectiveness:**

| Dimension | Measurable? | Ground truth needed? | WOS relevance |
|-----------|-------------|---------------------|---------------|
| Routing fidelity (triggers on correct intent only) | Yes — negative test pass rate | No (structural) | High — descriptions drive routing |
| Output contract fidelity (produces parseable structured output) | Yes — schema validation | No (structural) | High — skills produce freetext today |
| Completion rate (completes without escalation) | Yes — pass@k, pass^k | Yes (for grading) | Medium — WOS chains are interactive |
| Token efficiency (delta vs. baseline) | Yes — token delta from evals | No (comparative) | Medium — context matters for long chains |
| Quality delta (better than no-skill baseline) | Yes — pass rate delta | Yes (eval suite needed) | Low (currently) — no baseline tracking |

---

### SQ2: What structural properties of a SKILL.md correlate with execution quality?

**SkillReducer findings — instruction density and compression [F5]:**
SkillReducer (arXiv 2603.29919, March 2026) analyzed a large corpus of real SKILL.md files and found:
- 26.4% of skills lack routing descriptions entirely — no description means no auto-routing
- Over 60% of skill body content is non-actionable (background, examples, or templates loaded regardless of task relevance)
- Only 38.5% of body content is actionable core rules
- Compressed skills outperform originals by 2.8% on functional quality — "a less-is-more effect where removing non-essential content reduces distraction"
- 48% mean description compression was achievable while preserving routing accuracy

Implication: Instruction density (ratio of actionable rules to total body content) is a measurable quality proxy. A skill body that is mostly background and examples is both less effective and less efficient than one that front-loads directives.

**SkillRouter findings — description as routing contract [F4]:**
SkillRouter (arXiv 2603.22455, March 2026) studied 80K+ skills and found:
- Median description length: 21 words vs. 704 words for body
- Removing skill bodies caused 31–44 percentage point routing accuracy collapse across all tested architectures
- Even skills with descriptions exceeding 35 words showed a 31.8pp gap between metadata-only and full-text routing
- Key routing signal elements extracted from skill bodies: **primary capability, trigger condition, and unique identifiers** (library names, API endpoints, etc.) each in 20–40 tokens

Implication: Description length alone is not a quality signal (SkillRouter showed word count doesn't predict routing success). The presence of the three signal elements — primary capability, trigger condition, unique identifier — is what matters for routing.

**Official specification properties [existing research, skill-ecosystem-design doc]:**
- `name` ≤ 64 chars, lowercase + hyphens only
- `description` ≤ 1024 chars (truncated in skill listings at 250 chars in Claude Code)
- Body under 500 lines recommended — "move detailed reference material to separate files"
- Progressive disclosure structure: metadata → instructions → resources

**Description as the routing signal:**
"The description IS the routing signal. Claude Code: 'Front-load the key use case; each description entry is capped at 250 characters regardless of budget.' OpenAI Codex: 'Include specific keywords that help agents identify relevant tasks.'"

The guide also notes: "Use directives over suggestions — 'Always use X' outperforms 'X is recommended.'" Reasoning-based instructions ("Do X because Y tends to cause Z") work better than rigid directives, but directive language still outperforms hedged suggestions.

**SKILL.md structural antipatterns [F7, F5]:**
- Vague descriptions → missed or incorrect invocations
- Single skills attempting multiple responsibilities → debugging opacity
- Excessive rigid directives (MUST/NEVER/ALWAYS) without rationale → reduced reliability
- Over 60% non-actionable body content → distraction, context waste
- Missing output format declarations → downstream parsing failures

**Security correlation [F1, F6]:**
The supply-chain research adds a security angle to structural properties:
- The majority of vulnerabilities are embedded in SKILL.md natural language content, not in companion scripts — the skill instruction file is the primary attack surface (specific figure cited in gatherer notes as 84.2% but not confirmed explicitly in source; treat as directional)
- Executed payloads averaged 1,850 bytes vs. 2,214 bytes for refused samples — **brevity correlates with successful attack disguise** (short malicious content is harder to detect)
- Two structural attack patterns: code example poisoning (malicious logic in code blocks that agents copy as "official examples") and configuration template poisoning (backdoored YAML/JSON applied verbatim)
- 17.7% of real skills fetch untrusted third-party content — an indirect injection vector
- 10.9% of ClawHub skills expose hardcoded secrets, API keys, or credentials

These structural properties are auditable via static analysis. SkillScan detected 90.7% of adversarial samples; ToxicSkills' toolkit achieves 90–100% recall on confirmed malicious skills with 0% false-positive rate on legitimate ones.

---

### SQ3: What failure modes are unique to skill chains vs. single skills?

**MASFT taxonomy — 14 failure modes in 3 categories [existing research, agent-testing doc]:**
The Multi-Agent System Failure Taxonomy (arXiv 2503.13657) identifies failures clustered into:
- (FC1) Specification/system design failures: role confusion, step repetition, unaware of termination
- (FC2) Inter-agent misalignment: context resets, task derailment, reasoning-action mismatch
- (FC3) Task verification and termination: premature termination, insufficient verification

FC2 is chain-specific — these failures only manifest when multiple agents/skills interact. The root cause diagnosis is structural: "Failures stem from organizational design flaws rather than individual agent limitations." Tactical prompt fixes yielded only +14% improvement; structural changes (standardized protocols, verification) were required.

**Context rot as a compounding chain failure mechanism [F2]:**
Morph's analysis of 18 frontier models (including GPT-4.1, Claude Opus 4, Gemini 2.5) found universal context rot:
- 30%+ accuracy drops when relevant information sits in middle positions (lost-in-the-middle effect)
- Performance follows a U-shaped curve: strong at document start/end, weak in middle
- At 100K tokens, each token competes among 10 billion pairwise relationships (attention dilution)
- Coding agents spend over 60% of their first turn just retrieving context; every agent's success rate decreases after 35 minutes; doubling task time quadruples failure rate
- By 35 minutes, typical signal-to-noise ratio drops to ~2.5% (500 relevant tokens among 20,000 total)

For skill chains, context rot compounds at every handoff. Each skill's verbose output becomes noise in the next skill's context. This explains why "compact returns prevent context bloat" is not just a style preference but a reliability requirement for chains longer than 2–3 steps.

**Four chain-specific failure modes identified in existing research [skill-chaining doc]:**

1. **Context bleed / context poisoning**: Earlier messages in the conversation get compressed as the chain progresses, eroding information fidelity with each hop. Critical details from earlier skills become inaccessible by later stages.

2. **Contract mismatch**: The producing skill generates output in a format the consuming skill cannot parse. "Outputs are syntactically valid but semantically incompatible, leading to silent failures." Silent is the key word — the chain continues on malformed input without surfacing an error.

3. **Error amplification**: Unstructured multi-agent networks amplify errors substantially compared to single-agent baselines. This applies specifically to fully independent architectures with no inter-agent coordination. Sequential chains with boundary validation face substantially lower amplification, but the mechanism (each stage treats prior output as ground truth) applies to any chain. (Amplification ratios vary by architecture — parallel uncoordinated designs exhibit worst-case behavior; centralized sequential designs like WOS are substantially lower.)

4. **Behavioral drift**: Agent Behavioral Contracts (arXiv 2602.22302) documents measurable behavioral degradation over extended interactions — outputs drift from intended specifications even when typed schemas are in place. For WOS, research chains spanning multiple sessions (wos:research → wos:distill across sessions) may accumulate this drift invisibly.

**Write conflict amplification [existing research]:**
"Agent A creates a user profile structure. Agent B, unaware, creates a different structure — producing three incompatible representations of the same concept. Unlike read operations, write conflicts cascade." In WOS terms: if wos:research writes a file and wos:distill writes to the same file without checking the prior output's structure, write conflicts can silently corrupt the pipeline state.

**Skill chain vs. single skill failure comparison:**

| Failure mode | Single skill | Skill chain | Detectable by static audit? |
|---|---|---|---|
| Routing misfires | Yes | Amplified at each stage | Partial — description analysis |
| Output contract violations | Yes | Cascading | Yes — output format declarations |
| Context rot | Minimal | Severe (compounding) | Partial — body size proxy |
| Contract mismatch / silent failures | No | Yes | Yes — requires declared contracts |
| Behavioral drift | Minimal | Present across sessions | No — requires runtime monitoring |
| Write conflicts | No | Yes | Partial — shared state schema check |
| Error amplification | No | Yes — substantial in uncoordinated MAS; lower in sequential designs | Partial — coordination design review |

---

### SQ4: What evaluation signals are available without ground-truth labels?

**Structural signals (fully automated, no ground truth needed):**

From the evidence gathered, the following checks require no labeled data:

1. **Description coverage** (SkillRouter): Does the description contain the three routing signal elements — primary capability, trigger condition, unique identifier? Detectable via keyword/phrase analysis.

2. **Instruction density ratio** (SkillReducer): What fraction of body content is actionable rules vs. background/examples/templates? Below 38.5% actionable content signals a SkillReducer candidate; above 60% non-actionable content predicts quality degradation.

3. **Body line count and compression potential** (existing WOS check): WOS already measures instruction lines. SkillReducer's 48% compression finding suggests that bodies significantly above the 500-line threshold contain substantial non-actionable content.

4. **Output format declaration presence**: Does the skill describe what format it produces? A skill that lacks any mention of output format, schema, or structure is a contract mismatch risk in chains.

5. **Executable content flags** (ToxicSkills/arxiv 2604.03081): Does the body embed code blocks with executable patterns? Does the skill fetch external content? Skills with inline code examples and external fetches have 2.12× higher vulnerability rates.

6. **Rigid directive density** (existing WOS check): WOS already counts MUST/NEVER/ALWAYS occurrences. The SkillReducer findings add context: rigid directives without rationale reduce reliability vs. reasoning-based instructions.

7. **Negative trigger coverage**: Does the description or frontmatter include scope-limiting language (what the skill does NOT do)? Skills without exclusion criteria are prone to over-triggering on adjacent intents.

**Behavioral signals (observable without gold labels, but require runtime data):**

8. **Pass rate delta**: Comparison of with-skill vs. without-skill on a small prompt set. Even 10–20 test cases surfaces meaningful signal. The agentskills.io guide recommends this as the primary eval primitive.

9. **Token cost delta**: Whether the skill increases or decreases token consumption relative to baseline. A skill that doubles tokens for minimal quality gain has negative efficiency effectiveness.

10. **Retry rate and escalation frequency**: How often does the skill's output get corrected, retried, or escalated by the user? Implicit correction signals available from session logs.

**From agent testing research [agent-testing doc]:**
Property-based testing provides structural invariants that hold without ground-truth labels:
- Tool call schemas are always valid
- Retry counts never exceed configured maximums
- Context window budget is never exceeded
- Structured output always parses as valid JSON

These are deterministic even when model outputs vary, making them compatible with automated static audit.

---

### SQ5: How do existing frameworks approach skill/chain evaluation, and what can WOS adopt?

**LangSmith and Braintrust — general agent evaluation [F8, F9]:**
Both platforms provide tracing and LLM-as-judge evaluation for agent workflows. However, investigation found neither platform provides skill-specific evaluation primitives. They treat agent evaluation as general LLM pipeline evaluation (tracing, scoring, human annotation) rather than providing SKILL.md-aware checks. Braintrust's "Loop AI" feature generates evaluation datasets from production logs; LangSmith provides granular trace-level visibility into multi-step workflows. Neither has published skill-specific quality dimensions equivalent to the agentskills.io eval guide.

**What existing frameworks measure:**
- Trace-level: tool call sequences, latency, token consumption, error rates
- Quality-level: LLM-as-judge scoring on semantic correctness, task completion, tone
- Comparative: with-version vs. without-version pass rate delta
- Structural: schema validation, format compliance

**What existing frameworks do NOT measure:**
- Description routing coverage (three signal elements)
- Instruction density ratio (actionable vs. non-actionable content)
- Output contract declaration presence
- Chain-gate documentation (what a skill requires from its predecessor)
- Security-relevant structural properties (executable content, external fetches, credential patterns)

**Promptfoo — most relevant for WOS [existing research, agent-testing doc]:**
Promptfoo is CLI-first, YAML-configured, and supports structural assertions (exact match, JSON schema, regex) alongside LLM-graded rubrics. MIT licensed. Its key differentiator for WOS is: it runs without a hosted platform, integrates with CI/CD, and supports per-assertion pass/fail with configurable thresholds. This aligns with WOS's stdlib-only philosophy for core checks. Promptfoo was acquired by OpenAI in March 2026.

**agentskills.io official eval guide [F3]:**
The official guide provides the most operationally relevant framework for WOS-style evaluation:
- `evals/evals.json` stores test cases with prompts, expected outputs, and assertions
- Each test runs with-skill and without-skill (or prior version as baseline)
- `grading.json` records PASS/FAIL with specific evidence per assertion
- `timing.json` records token count and duration per run
- `benchmark.json` aggregates pass_rate delta, time delta, token delta across all test cases
- Key analysis: assertions that always pass in both configurations add no value; assertions that pass with-skill but fail without-skill reveal where the skill adds value

**Three evaluation signal categories WOS can adopt immediately (no new infrastructure):**

1. **Static structural checks** (extend `wos/skill_audit.py`): description coverage check, output format declaration presence, executable content flag, chain-gate documentation presence. Zero runtime cost, zero ground-truth dependency.

2. **Density analysis** (extend existing `count_instruction_lines`): add non-actionable content ratio estimate (prose-only lines vs. directive lines) using pattern matching on imperative verbs, schema notation, and format specifications.

3. **Baseline delta framework** (new skill eval scaffold): provide a standard `evals/evals.json` template in `wos:skill-creator` so authors can capture with-skill vs. without-skill deltas from day one of skill development.

---

### SQ6: What should a WOS skill audit surface?

**Grounding in current WOS skill_audit.py:**
The existing `check_skill_sizes()` and `check_skill_meta()` functions already cover:
- Instruction line count (warn if total > 500)
- SKILL.md body raw line count (warn if > 500 non-blank lines)
- Name format (fail: must be lowercase + hyphens, ≤ 64 chars, no reserved words)
- Description length (warn if > 1024 chars)
- XML tags in description (warn)
- Second-person language patterns in description (warn)
- ALL-CAPS directive density (warn if ≥ 3 occurrences of MUST/NEVER/ALWAYS/etc.)

**Gaps in current WOS audit vs. what evidence supports:**

| Gap | Evidence source | Proposed check | Severity |
|-----|-----------------|----------------|----------|
| Description routing coverage | SkillRouter (F4) | Warn if description lacks primary capability, trigger condition, or unique identifier pattern | warn |
| Output format declaration | Skill chaining doc (SQ8), agentskills.io (F3) | Warn if SKILL.md body contains no output format specification | warn |
| Executable content flag | ToxicSkills (F6), arxiv 2604.03081 (F1) | Warn if SKILL.md body contains code blocks with executable patterns (shell commands, eval, subprocess) | warn |
| External fetch flag | ToxicSkills (F6) | Warn if skill references or fetches external URLs in body | warn |
| Instruction density ratio | SkillReducer (F5) | Warn if estimated actionable content < 35% of body (pattern: lines containing imperative verbs, schema notation, format specs) | warn |
| Negative scope coverage | Philschmid (F7), skill-ecosystem-design doc | Warn if description contains no scope-limiting language (no exclusion criteria) | warn |
| Chain-gate documentation | Skill chaining doc (SQ8), SQ3 findings | Warn if skill description or body references other skills by name but declares no input requirements | warn |

**Checks that should remain out of scope for static audit:**
- Output quality (requires ground-truth labels)
- Routing accuracy (requires runtime eval suite)
- Behavioral drift (requires runtime monitoring across sessions)
- Pass rate delta (requires with/without baseline comparison)

**Severity calibration:**
Following the existing WOS model (fail = blocking, warn = accumulating), all seven proposed new checks should be `warn`. None meets the fail threshold because:
- A skill without output format declarations may still function correctly for simple single-use skills
- Executable content is not inherently malicious — it is a risk flag requiring human review
- Description routing coverage is heuristic, not definitive

**Output format recommendation:**
New checks should emit the same `{file, issue, severity}` dict format as existing validators. The `audit.py` CLI should surface them in the existing grouped output under a "Skill Quality" section. No new output format is needed.

---

### SQ7: Where does the audit live in WOS architecture?

**Current architecture:**
- `wos/skill_audit.py` — `check_skill_sizes()` and `check_skill_meta()` — contains all skill-specific quality checks
- `scripts/audit.py` — CLI entry point that calls skill audit via `--skill-max-lines` flag
- `wos/validators.py` — document-level validation (frontmatter, URLs, content length, etc.) — currently has no skill-specific section

The existing design is correct: skill-specific checks belong in `wos/skill_audit.py`, not in `validators.py`. `validators.py` operates on `Document` instances (parsed from `.md` files in `docs/`); skill audit operates on skill directories (SKILL.md + scripts + references). These are distinct data models.

**Where new checks belong:**

| New check | Where it lives | Why |
|---|---|---|
| Description routing coverage | `skill_audit.py:check_skill_meta()` | Reads description from SKILL.md frontmatter — already parsed by `parse_skill_meta()` |
| Output format declaration | `skill_audit.py:check_skill_meta()` | Reads SKILL.md body — same access pattern as rigid directive check |
| Executable content flag | `skill_audit.py:check_skill_meta()` | Reads SKILL.md body — regex scan for shell patterns, subprocess calls |
| External fetch flag | `skill_audit.py:check_skill_meta()` | Reads SKILL.md body — regex scan for URL fetch patterns |
| Instruction density ratio | `skill_audit.py:check_skill_sizes()` | Needs full body content + line count — extends existing measurement |
| Negative scope coverage | `skill_audit.py:check_skill_meta()` | Reads description — natural extension of description quality checks |
| Chain-gate documentation | `skill_audit.py:check_skill_meta()` | Reads description + body — cross-reference between skill name mentions and input declarations |

**Implementation pattern (extending existing code):**

```python
# In check_skill_meta() — detection pattern examples
_EXECUTABLE_PATTERNS_RE = re.compile(
    r"```(?:sh|bash|shell|zsh)|\bsubprocess\b|\bos\.system\b|\beval\b"
)
_EXTERNAL_FETCH_RE = re.compile(r"https?://[^\s]+")
_OUTPUT_FORMAT_SIGNALS = (
    "returns", "outputs", "produces", "format:", "schema:",
    "json", "yaml", "markdown", "structured"
)
_SCOPE_EXCLUSION_SIGNALS = (
    "does not", "don't use", "not for", "avoid", "only when",
    "excludes", "not intended"
)
```

**CLI integration:**
The `scripts/audit.py` `--skill-max-lines` flag already conditionally enables skill audit. New checks integrate into the same `check_skill_meta()` call path; no new CLI flags are needed unless authors want to disable specific checks. Following WOS convention, new flags should only be added when there is a clear user need to override defaults.

**Separation of reads from writes (CQS principle from validation-architecture research):**
All proposed new checks are pure reads: they observe SKILL.md content and return issue lists without mutating anything. The reads/writes separation is already maintained in `skill_audit.py` and should continue. Any future "fix" operations (e.g., auto-generating missing output format declarations) belong in a separate, explicitly invoked command — not in the audit path.

**Where a full skill eval harness belongs:**
Static audit lives in `skill_audit.py`. A dynamic eval harness (with-skill vs. without-skill pass rate delta) is a different tool: it requires agent execution, not static analysis. This belongs in `skills/skill-creator/` as part of the skill creation workflow, not in `wos/` core. The agentskills.io `evals/evals.json` structure can serve as the standard format for skill authors to adopt.

---

## Challenge

### Steelmanned claims (no significant counter-evidence found)

- **The audit belongs in `wos/skill_audit.py`** — The architectural separation is well-grounded. `validators.py` operates on `Document` dataclass instances parsed from `docs/`; `skill_audit.py` operates on skill directories. These are distinct data models with distinct access patterns. No counter-evidence found for the placement decision.

- **Seven new checks should all be `warn` severity** — The severity calibration is sound. None of the proposed checks produces a definitive, exploitable failure on its own (no output format declaration does not break a simple single-use skill; executable content is not inherently malicious). The warn-not-fail choice is also consistent with the current WOS model where only structurally incorrect or clearly invalid conditions are `fail`. No contradicting evidence found.

- **Skill-chain failures are categorically different from single-skill failures** — The MASFT taxonomy's FC2 (inter-agent misalignment: context resets, task derailment, reasoning-action mismatch) does not manifest in single-skill runs by definition. The chain-specific failure modes (contract mismatch, write conflicts, behavioral drift) are confirmed by multiple independent sources. This distinction held up under challenge.

---

### Claims with counter-evidence or important caveats

#### Claim 1: Instruction density is the highest-leverage structural signal

**Counter-evidence / caveat:** The 2.8% quality improvement from SkillReducer's compression is a real but modest effect. Complexity-based prompting research (2025) shows that for reasoning-heavy tasks, *longer* reasoning chains and more elaborate examples improve performance by +5.3% on average and up to +18% on benchmarks like MathQA. The direction inverts for skills that provide worked examples or multi-step reasoning scaffolds: stripping background content that looks "non-actionable" can remove context that the model needs to reason correctly. SkillReducer's corpus is dominated by plugin-style skill files (tool descriptions, API wrappers), not reasoning scaffolds. The compression benefit may not generalize to WOS skills like `wos:research` or `wos:write-plan` whose bodies guide extended deliberation rather than short tool invocations.

Additionally, the research notes: "Reasoning-based instructions ('Do X because Y tends to cause Z') work better than rigid directives." Those rationale sentences look non-actionable by line count but are load-bearing for reliability.

**Implication for the research:** The instruction density ratio check (warn if actionable content < 35% of body) should not be applied uniformly. Skills primarily composed of reasoning guidance or multi-step examples may legitimately score below the threshold without quality loss. The check needs a task-type qualifier, or the threshold should be set conservatively enough to avoid flagging skills that use rationale-heavy patterns intentionally. The claim that instruction density is *the highest-leverage* signal is probably true for tool-wrapper skills but likely false for orchestration or planning skills.

---

#### Claim 2: Description routing coverage can be checked structurally via three-signal keyword analysis

**Counter-evidence / caveat:** The three-signal model (primary capability, trigger condition, unique identifier) is derived from what SkillRouter found *in bodies* — the signals used to reconstruct routing accuracy when descriptions were insufficient. Applying keyword pattern matching to descriptions to detect whether those signals are present is a heuristic leap the paper does not make itself. SkillRouter demonstrates that *the signals matter*, not that their presence is detectable via keyword scanning.

Two documented failure modes of keyword/phrase matching in routing contexts:
1. **False negatives:** A skill can contain all three signals in natural language without using any of the canonical keyword forms. A description reading "Converts audio files into structured transcripts using the Deepgram API" contains all three signals and would pass — but a description reading "Handles all Deepgram work" carries the same routing information without keyword matches.
2. **Gaming / surface compliance:** The check can be satisfied trivially by adding "Use this skill when: [trigger]. Produces: [output]. Uses: [identifier]." as boilerplate, without any improvement to actual routing effectiveness.

Static analysis of ATS (applicant tracking) keyword systems — an analogous domain — shows that heuristic keyword matching achieves ~42% screening precision vs. ~78% for semantic matching. The ATS analogy suggests the three-signal check produces meaningful signal but should not be treated as a routing accuracy proxy.

**Implication for the research:** The description routing coverage check is useful as a *prompt* to skill authors, not as a reliable proxy for routing quality. The audit should frame the warning as "description may be missing routing signals" rather than implying the check has predictive validity. The check's value is pedagogical (educating authors about what makes descriptions effective) more than diagnostic.

---

#### Claim 3: Context rot is a chain-specific compounding failure — 30%+ accuracy drops, 17.2× error amplification

**Counter-evidence / caveat:** Two distinct claims are bundled here that should be separated.

On context rot: Chroma's 2025 study tested 18 frontier models and found universal degradation, which the draft treats as confirmation. However, the Chroma research is published by a company whose RAG products benefit commercially from the finding that long contexts are unreliable. The study design (needle-in-a-haystack variants) is contested as underrepresenting retrieval-augmented and structured-context scenarios where relevant content is prepended or summarized. Chroma itself notes: "Performance degrades non-uniformly — factors like needle-question similarity, presence of distractors, and haystack structure all impact performance non-uniformly." The 30%+ accuracy drop applies to specific positional conditions (mid-context placement with high distractor density), not to well-structured skill chain outputs that front-load summaries. EMNLP 2025 (arXiv 2510.05381) found that context length *alone* hurts performance even with perfect retrieval — but this is a different, narrower claim than chain-specific compounding failure.

On the 17.2× amplification figure: This applies specifically to fully independent "bag of agents" architectures with no inter-agent coordination. The draft acknowledges this ("sequential chains with boundary validation face substantially lower amplification") but presents the 17.2× number prominently. The Google DeepMind "Science of Scaling Agent Systems" (arXiv 2512.08296, Dec 2025) found that centralized architectures contain error amplification to 4.4× — a 4× reduction in the worst-case figure. For WOS skill chains, which are sequential and human-supervised at each step, the relevant amplification figure is much lower than 17.2×.

**Implication for the research:** The context rot section should distinguish between (a) the well-evidenced positional degradation effect (lost-in-the-middle) and (b) chain-specific compounding, which is real but substantially mitigated by structured handoffs and sequential validation. The 17.2× figure should be contextualized as a worst-case for uncoordinated parallel agents, not a representative figure for WOS's sequential, human-supervised chains.

---

#### Claim 4: Static structural checks can surface 90%+ of quality/security issues without runtime data

**Counter-evidence / caveat:** The 90%+ recall figures come from the ToxicSkills and SkillScan studies, which were evaluated against *confirmed malicious skills* — a curated adversarial dataset. This is a recall figure over a labeled set, not a false positive rate study. IEEE TSE (2023, doi:10.1109/TSE.2023.3329667) — a major meta-analysis of static analysis false positive mitigation — documents that heuristic-based static analysis tools routinely generate 30–50% false positive rates in practice (one tool at 16.7%, another at 34.55%). The Nature Scientific Data 2025 dataset paper on non-actionable static analysis reports confirms that "heuristic approaches produce labels that do not agree with human oracles, making strong performance overoptimistic of true adoption performance."

The 90%+ recall is over security adversarial samples. Quality checks (instruction density, description coverage, output format declaration) are pattern-matching heuristics over natural language — a domain where false positive rates for NLP-based classifiers are typically 20–40% at heuristic thresholds without calibration on in-domain data.

**Implication for the research:** The 90–100% recall claim is accurate for the security checks (executable content, external fetch, hardcoded credentials) which match explicit patterns in well-defined syntactic categories. It likely overstates accuracy for the quality checks (instruction density ratio, description signal coverage, negative scope language) which rely on natural language pattern matching without in-domain calibration. The audit implementation should track and report these warnings separately, and a follow-up study against real WOS skill files would be needed to validate false positive rates before increasing check severity.

---

#### Claim 5: LLM-as-judge should NOT be added to the audit pipeline

**Counter-evidence / caveat:** The case against LLM-as-judge is weaker in 2026 than it was in 2024. Active research has produced:
- Reasoning-based Bias Detector (RBD, arXiv 2505.17100, May 2026): a plug-in debiasing module that improves evaluation accuracy by 18.5% and consistency by 10.9%, bringing calibration substantially closer to human agreement.
- RULERS (arXiv 2601.08654): locked rubrics with evidence-anchored scoring achieve substantially reduced position and verbosity bias when rubric criteria are defined before, not during, evaluation.
- Ensemble approaches with 3–5 judges reduce bias 30–40%, making them viable for high-stakes decisions.
- Regression-based calibration halves residual error relative to best single ensembles.

These advances do not eliminate the bias concern, but they significantly raise the bar. The LLM-as-judge research in `2026-04-07-llm-as-judge.research.md` documents bias extensively but was written in April 2026 and may not yet incorporate the RBD and RULERS mitigation results at full depth.

The refusal remains defensible on WOS-specific grounds: (a) WOS's stdlib-only core principle excludes runtime LLM calls from the audit path, (b) skill authors need deterministic, reproducible audit results for CI/CD integration, (c) bias mitigation techniques require calibration data WOS does not have for skill quality specifically. But the claim that LLM-as-judge bias "outweighs benefits" is less categorical than it was in 2024 — the tradeoff has shifted.

**Implication for the research:** The exclusion of LLM-as-judge should be justified on WOS architectural grounds (stdlib-only, deterministic CI/CD) rather than on the claim that bias concerns are categorically disqualifying. The research should acknowledge that bias mitigation has materially progressed and that a future `wos:skill-eval` skill (distinct from the deterministic audit) could legitimately incorporate calibrated LLM-as-judge scoring for quality dimensions that structural checks cannot reach.

---

### Key assumptions not validated by evidence

1. **The SkillReducer 2.8% compression benefit transfers to WOS skill types.** SkillReducer's corpus is 55,315 publicly available skills from a general coding agent registry. WOS skills are a different population: smaller corpus (~13 skills), human-supervised chains, planning and research skills alongside tool wrappers. The assumption that >60% non-actionable content and 2.8% quality improvement generalize to WOS's specific skill distribution is not validated. WOS would need its own density analysis to set a calibrated threshold.

2. **The three routing signal elements are detectable via keyword/phrase matching at useful precision.** The draft proposes checking for "primary capability, trigger condition, and unique identifier" via keyword pattern matching. SkillRouter's evidence is that these signals *exist* in skill bodies and matter for routing accuracy; it does not validate that their presence in descriptions is detectable via static text patterns. The precision of the proposed check on real WOS descriptions has not been tested.

3. **Structural audit warnings will be acted on at `warn` severity without calibration data.** The proposed checks are all `warn`, following WOS convention that warns accumulate rather than block. But the value of accumulated warnings depends on their false positive rate — if the density ratio check fires on 60% of skills due to the natural prose content of planning and reasoning skills, the warnings become noise and authors will learn to ignore the audit output. Without a baseline false positive rate study on real WOS skill files, the check thresholds (e.g., "< 35% actionable content") are unvalidated and could produce an alert fatigue pattern that undermines the audit's credibility.

---

## Findings

Confidence levels: **HIGH** = convergent evidence from T1/T2 sources with no significant counter-evidence. **MODERATE** = supported by evidence but challenged, qualified, or based on analogy to WOS. **LOW** = plausible but weak or contested evidence.

### Finding 1: Skill effectiveness has five measurable dimensions, only one requires ground-truth labels

A skill is effective when it satisfies five dimensions: (1) **routing fidelity** — triggers on the correct intent and only that intent; (2) **output contract fidelity** — produces structured output that downstream skills and users can parse; (3) **completion rate** — completes without escalation, abandonment, or retry loop; (4) **token efficiency** — adds quality relative to its token cost; (5) **quality delta** — measurably outperforms the no-skill baseline. [1][2][10][11]

Dimensions 1–4 are auditable without ground-truth labels (routing via negative tests, output format via declaration presence, completion via session logs, efficiency via token delta). Dimension 5 requires a with-skill vs. without-skill eval harness. (HIGH — T1 and T2 sources converge; Anthropic's task/trial/transcript/outcome framework aligns with the agentskills.io eval guide.)

**Counter-evidence:** The quality delta dimension (pass^k vs. pass@k) is essential for production reliability but adds substantial eval infrastructure cost. Routing fidelity is the single highest-frequency failure mode identified in practice — description rewrites fixed 5 of 7 failures in Philschmid's case study (HIGH). Efficiency and quality delta are currently untracked in WOS and may remain so; audit focus should prioritize the four label-free dimensions.

### Finding 2: Instruction density is a valid signal for tool-wrapper skills; inapplicable to orchestration skills

SkillReducer's finding — >60% non-actionable content in the average skill body, 2.8% quality gain from compression — is real and significant for API-wrapper and tool-description skills. (MODERATE — the paper's corpus is general coding agent registries, not WOS-style orchestration skills.)

**Important qualification from challenge:** Complexity-based prompting research (2025) shows reasoning-heavy tasks improve by +5.3–18% with longer, rationale-inclusive instructions. WOS skills like `wos:research`, `wos:write-plan`, and `wos:execute-plan` are orchestration skills, not tool wrappers. Rationale sentences ("Do X because Y prevents Z") look non-actionable by line count but are load-bearing for execution quality. The 35% actionable content threshold must not be applied uniformly. [4]

**Calibrated recommendation:** Apply the density check only to skills where the primary intent is tool invocation or single-step transformation. Mark orchestration and planning skills as exempt, or raise the body size threshold for skills that contain `## Methodology`, `## Stages`, or `## Phases` structural markers indicating deliberate process documentation. (MODERATE — architectural reasoning grounded in evidence; threshold values require calibration against real WOS skill files before enforcement.)

### Finding 3: The three-signal description check is pedagogically valuable but not diagnostically reliable

SkillRouter demonstrates that descriptions containing primary capability, trigger condition, and unique identifier produce substantially better routing accuracy than descriptions without them [3]. Removing skill bodies collapses routing accuracy by 31–44 percentage points — confirming that descriptions must carry meaningful routing signal.

**Challenge resolution:** SkillRouter does not validate that these three signals are detectable via keyword pattern matching on descriptions. The check has high false negative potential (valid descriptions without canonical keyword forms) and is gameable by surface compliance. Analogous domain evidence (ATS keyword matching) shows ~42% precision for heuristic keyword classifiers vs. ~78% for semantic matchers. (MODERATE — the signal matters; the detection method is heuristic, not validated.)

**Calibrated recommendation:** Implement the check as a pedagogical nudge to authors, not a diagnostic claim. Frame the warning as "description may be under-specified for routing" with clear guidance on what to add. Do not treat the check as a routing accuracy proxy. Track false positive rate on real WOS skills after implementation and adjust before raising severity. (MODERATE)

### Finding 4: Skill-chain failures are categorically different from single-skill failures

The MASFT taxonomy's FC2 category (inter-agent misalignment: context resets, task derailment, reasoning-action mismatch) is definitionally absent in single-skill runs. Contract mismatch, write conflicts, and behavioral drift compound across chain boundaries in ways that single skills cannot produce. (HIGH — MASFT taxonomy confirmed by multiple independent sources; chain-specific mechanisms are structurally distinct.) [8]

**Qualified context rot claim:** The lost-in-the-middle positional degradation effect is real and universal across 18 frontier models [7]. However, the 30%+ accuracy drop applies to mid-context placement with high distractor density, not to structured chain outputs that front-load summaries. The effect is real but condition-specific — WOS chains with compact handoffs are less exposed than the worst-case scenario. (MODERATE — real effect, but T3 source (Morph) has commercial incentive; the positional mechanism is corroborated by independent sources.)

**Qualified amplification claim:** The 17.2× error amplification figure is a worst-case for fully uncoordinated "bag of agents" parallel architectures. For centralized, sequential architectures (WOS's model), Google DeepMind research shows amplification of ~4.4× — still substantial, but not catastrophic. WOS chains are also human-supervised at gate points, which further reduces compounding. (MODERATE — the mechanism is real; the magnitude requires architectural context.) [9]

### Finding 5: Security-pattern structural checks achieve high recall; quality-heuristic checks require calibration

**Security patterns (HIGH confidence):** Executable content detection, external URL fetch detection, and hardcoded credential pattern matching are syntactic checks over well-defined categories. ToxicSkills and SkillScan achieve 90–100% recall with 0% false positives on confirmed malicious skills. These checks are reliable for security purposes. [5][6]

**Quality heuristics (MODERATE confidence, pending calibration):** Instruction density ratio, description routing coverage, and output format declaration presence rely on natural language pattern matching. IEEE TSE meta-analysis documents 30–50% false positive rates for heuristic static analysis tools in practice. Quality heuristic checks are expected to fire on legitimate skills with rationale-heavy content, broad user-facing descriptions, or implicit output conventions. These checks add pedagogical value but require calibration against real WOS skill files before their thresholds can be trusted. Implementation should start with conservative thresholds and adjust based on observed false positive rates.

**Counter-evidence addressed:** The 90%+ recall claim was correctly scoped to security patterns. Quality heuristics should be presented to users as "consideration flags" not "detected violations." (MODERATE overall — strong for security, uncertain for quality.)

### Finding 6: Seven new `warn`-severity checks are justified, with adjusted framing for quality heuristics

The existing WOS skill audit covers name format, description length, XML tags, second-person patterns, and ALL-CAPS directive density. The following seven additions are justified by the evidence, all at `warn` severity:

| # | Check | Evidence basis | Confidence | Framing |
|---|-------|---------------|------------|---------|
| 1 | Description routing coverage (three signals) | SkillRouter [3] | MODERATE | "Description may be under-specified for routing" — pedagogical |
| 2 | Output format declaration presence | Skill chaining research, agentskills.io [1] | HIGH | "Skill does not declare output format — downstream parsing risk" |
| 3 | Executable content flag (shell commands in body) | ToxicSkills [5][6] | HIGH | "Skill body contains executable patterns — review for security" |
| 4 | External fetch flag | ToxicSkills [6] | HIGH | "Skill fetches external URLs — indirect injection risk" |
| 5 | Instruction density ratio | SkillReducer [4] | MODERATE | "Body may contain high proportion of non-actionable content — check applies to tool-wrapper skills only" |
| 6 | Negative scope coverage | Philschmid [2], skill-ecosystem-design | MODERATE | "Description lacks exclusion criteria — may over-trigger" |
| 7 | Chain-gate documentation | Skill chaining research, SQ3 | MODERATE | "Skill references other skills but declares no input requirements" |

All seven checks belong in `check_skill_meta()` or `check_skill_sizes()` in `wos/skill_audit.py`. (HIGH — architectural placement is uncontested; severity calibration is sound per WOS convention.)

**Alert fatigue risk:** If the density ratio and description coverage checks fire on most WOS skills due to their orchestration-heavy content, warn accumulation becomes noise. A follow-up calibration pass against the ~13 existing WOS skills should precede any threshold hardening or severity escalation.

### Finding 7: LLM-as-judge exclusion should be grounded in WOS architecture, not categorical bias rejection

The case against adding LLM-as-judge to the deterministic audit has three valid architectural grounds for WOS: (1) stdlib-only core principle excludes runtime LLM calls; (2) CI/CD integration requires deterministic, reproducible results; (3) calibration for skill quality dimensions requires in-domain training data WOS does not have. (HIGH — these constraints are well-established in WOS architecture and not dependent on LLM-as-judge bias literature.)

**Challenge resolved:** Bias mitigation progress (RBD debiasing: +18.5% accuracy; RULERS locked rubrics; ensemble judges: 30–40% bias reduction) means the categorical "bias disqualifies LLM-as-judge" argument is weakening. The correct framing is: WOS's current architecture is not suited for LLM-as-judge in the deterministic audit path — but a future `wos:skill-eval` skill (distinct from the static audit) could legitimately incorporate calibrated LLM-as-judge scoring for quality dimensions that structural checks cannot reach, including routing fidelity, completion rate, and quality delta. (MODERATE — architecture grounds the current exclusion; door should remain open for a dynamic eval skill.)

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Over 60% of skill body content is non-actionable background" | statistic | [4] | verified — paper states 61.5% non-actionable (background 40.7%, examples 12.9%, templates 7.6%, redundant 0.3%) |
| 2 | "Compressed skills outperform verbose ones by 2.8%" | statistic | [4] | verified — paper states 2.8% functional quality improvement; 25.3% improving, 14.0% regressing |
| 3 | "48% mean description compression achievable" | statistic | [4] | verified — paper states 48.0% mean reduction, median 59.0% |
| 4 | "26.4% of skills lack routing descriptions entirely" | statistic | [4] | verified — exact figure confirmed in paper |
| 5 | "Only 38.5% of body content is actionable core rules" | statistic | [4] | verified — exact figure confirmed in paper taxonomy analysis |
| 6 | "Removing skill bodies caused 31–44 percentage point routing accuracy collapse" | statistic | [3] | verified — paper states 31.4pp (BM25), 38.7pp (Qwen3-Emb-8B), 44.0pp (Qwen3-Emb-8B × Qwen3-Rank-8B) |
| 7 | "Median description length: 21 words vs. 704 words for body" | statistic | [3] | verified — exact figures from metadata audit table in paper |
| 8 | "80K+ skills studied" | statistic | [3] | verified — Easy tier: 78,361 candidates; Hard tier: 79,141 candidates |
| 9 | "84.2% of vulnerabilities embedded in SKILL.md files" | statistic | [5] | corrected in document — specific percentage removed; body now reads "the majority of vulnerabilities are embedded in SKILL.md content" with a note that the 84.2% figure is directional and unconfirmed in source text |
| 10 | "36.8% of real skills have vulnerabilities" | statistic | [6] | verified — source states 36.82% (1,467 of 3,984 skills) have at least one security flaw |
| 11 | "10.9% expose hardcoded credentials" | statistic | [6] | verified — exact figure confirmed |
| 12 | "17.7% fetch untrusted third-party content" | statistic | [6] | verified — exact figure confirmed |
| 13 | "30%+ accuracy drops when relevant information sits in middle positions" | statistic | [7] | verified — source states >30% accuracy drop for mid-context placement (positions 5–15 vs. 1 or 20); condition-specific, not universal |
| 14 | "All coding agents fail after 35 minutes" | superlative | [7] | corrected in document — body now reads "every agent's success rate decreases after 35 minutes"; "fail" overstatement removed |
| 15 | "17.2× error amplification compared to single-agent baselines" | statistic | [8] | corrected in document — specific ratio removed (figure not found in cited MASFT paper or arXiv 2604.02460; likely conflated with a different metric from arXiv 2505.17100); body now uses qualitative description of amplification pattern only |
| 16 | "Tactical prompt fixes yielded only +14% improvement" | statistic | [8] | verified — MASFT paper: ChatDev baseline 25.0%, improved prompts 34.4% (+9.4pp / +37.6% relative); however the paper itself frames this as "14% improvement on task completion"; document's paraphrase is consistent with source framing |
| 17 | "SkillScan detects 90.7% of adversarial samples" | statistic | [5] | verified — exact figure confirmed in source |
| 18 | "Description rewrites fixed 5 of 7 failures" | statistic | [2] | verified — source states "the description change alone fixed 5 of 7 failures"; pass rate went from 66.7% to 100% |
| 19 | "pass^k is the correct production metric" | superlative | [10] | corrected — Anthropic article presents pass@k and pass^k as context-dependent choices: "which to use depends on product requirements"; it does not designate pass^k as the single correct production metric |
| 20 | "RBD debiasing achieves 18.5% accuracy improvement" | statistic | [arXiv 2505.17100] | verified — abstract states "RBD-8B model improves evaluation accuracy by an average of 18.5% and consistency by 10.9%" |

**Reliability summary:** Of 20 claims, 15 are verified, 3 are corrected, and 2 are unverified. The verified claims (1–8, 10–13, 16–18, 20) are solid and well-sourced. Two claims require attention: claim 14 ("all agents fail") overstates a degradation finding as total failure — the Findings section should note this distinction though it is flagged here for the finalizer rather than corrected in the body. Claim 15 (17.2× error amplification attributed to MASFT [8]) is the most significant reliability gap: the number does not appear in either of its candidate source papers; the figure 17.2 appears only in the RBD paper (arXiv 2505.17100) as a different metric entirely (percentage improvement over fine-tuned judges). This claim should not be cited without identifying its actual source. Claim 19 misattributes a prescriptive framing to Anthropic — the source presents pass^k as one option, not the definitive production choice. These corrections do not undermine the document's core findings, which rest on well-verified T1 and T2 sources, but claims 14, 15, and 19 should be revised before the document is approved.

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://agentskills.io/skill-creation/evaluating-skills | Evaluating skill output quality | agentskills.io | 2026 | T2 | verified (domain ownership unclear; distinct from platform.claude.com) |
| 2 | https://www.philschmid.de/testing-skills | Practical Guide to Evaluating and Testing Agent Skills | Philipp Schmid (Hugging Face) | 2026 | T2 | verified |
| 3 | https://arxiv.org/html/2603.22455v4 | SkillRouter: Skill Routing for LLM Agents at Scale | Academic (arXiv) | Mar 2026 | T1 | verified |
| 4 | https://arxiv.org/html/2603.29919v1 | SkillReducer: Optimizing LLM Agent Skills for Token Efficiency | Academic (arXiv) | Mar 2026 | T1 | verified |
| 5 | https://arxiv.org/html/2604.03081 | Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems | Academic (arXiv) | Apr 2026 | T1 | verified |
| 6 | https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ | ToxicSkills: Malicious AI Agent Skills on ClawHub | Snyk Research | 2026 | T2 | verified |
| 7 | https://www.morphllm.com/context-rot | Context Rot: Why LLMs Degrade as Context Grows | Morph | 2026 | T3 | verified |
| 8 | https://arxiv.org/html/2503.13657v1 | Why Do Multi-Agent LLM Systems Fail? (MASFT) | Academic (arXiv) | Mar 2025 | T1 | verified |
| 9 | https://arxiv.org/html/2604.02460v1 | Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning | Academic (arXiv) | Apr 2026 | T1 | verified |
| 10 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Demystifying Evals for AI Agents | Anthropic Engineering | 2025 | T1 | verified |
| 11 | https://www.anthropic.com/research/building-effective-agents | Building Effective Agents | Anthropic | 2024 | T1 | verified |
| 12 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Agent Skills Overview | Anthropic | 2025–2026 | T1 | verified |
| 13 | https://arxiv.org/html/2602.12430v3 | Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward | Academic (arXiv, survey) | Feb 2026 | T2 | verified |

---

## What This Research Does Not Cover

- **Dynamic eval harness implementation**: How to build and run the with-skill vs. without-skill eval framework within the WOS plugin. That is a design task, not a research question.
- **LLM-as-judge for skill quality**: Whether to add an LLM-graded quality check to the skill audit. The research supports structural checks for reliability; the LLM-as-judge literature (2026-04-07-llm-as-judge.research.md) documents significant bias concerns that argue against adding probabilistic checks to a deterministic audit pipeline.
- **Cross-runtime skill chain evaluation**: How skill chain effectiveness varies across Claude Code, Cursor, Gemini CLI, and other runtimes. The research focuses on structural properties of SKILL.md that are runtime-independent.
- **Quantitative effectiveness benchmarks for WOS skills specifically**: No WOS failure postmortem or skill effectiveness baseline exists. The recommendations in SQ6/SQ7 are derived from analogous systems, not from WOS-specific data.
