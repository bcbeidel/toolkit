# Model Landscape Reference

Data as of April 2026. Benchmark gaps have a 12-18 month shelf life —
revisit when this data feels stale.

## Task-Type to Model Mapping

Use this table to select the primary recommendation based on task type.
"Leader" is the top-performing model on external benchmarks. "Value" offers
the best quality-per-dollar. "Budget" is the cheapest viable option.

| Task Type | Leader | Value | Budget |
|-----------|--------|-------|--------|
| Coding: function completion | Saturated — any frontier | Claude Sonnet 4.6 ($3/M) | DeepSeek V3.2 ($0.26/M) |
| Coding: bug fixing / SWE | Claude Opus 4.5/4.6 (SWE-bench 80.8%) | Gemini 3.1 Pro ($1.25/M) | DeepSeek V3.2 (73%, $0.26/M) |
| Coding: agentic multi-file | GPT-5.4 / Claude Opus 4.6 (Terminal-Bench ~82%) | Claude Sonnet 4.6 (59.1%) | DeepSeek V3.2 (39.6%) |
| Reasoning: scientific (PhD-level) | Gemini 3.1 Pro (GPQA 94.1%) | Gemini 2.5 Flash ($0.30/M, 82.8%) | DeepSeek R1-0528 ($0.45/M, 81%) |
| Reasoning: mathematical | GPT-5.4 (MATH-500 99%, USAMO 95%) | o4-mini ($1.10/M, 97.6%) | DeepSeek R1 ($0.55/M, 97.3%) |
| Reasoning: abstract / novel | Gemini 3.1 Pro (ARC-AGI-2 77.1%) | GPT-5.4 (73.3%) | No budget option — open-weight absent |
| Creative writing | Claude Opus 4.6 (Arena blind test 4/8 wins) | Claude Sonnet 4.6 | — |
| Multilingual / translation | Gemini 3.1 Pro (100+ languages, MMMLU 91.8%) | Gemini 2.5 Flash | Qwen 3.5 (CJK specialist) |
| Instruction following | Qwen3.5 397B (IFBench 78.8%) | Gemini 3 Flash (78.0%) | — |
| Long-context processing | Llama 4 Scout (10M context) | Gemini 2.5 Pro/Flash (1M) | — |
| Cost-optimized production | DeepSeek V3.2 ($0.26/M input, 73% SWE-bench) | GPT-4o-mini ($0.15/M) | — |
| Vision / multimodal | Gemini 3 Pro (Arena Vision ELO 1286) | Gemini 2.5 Flash | — |

## Pricing Quick Reference

Prices are per million tokens (input / output).

### Proprietary Models

| Model | Input | Output | Context | Speed | Provider |
|-------|-------|--------|---------|-------|----------|
| Claude Opus 4.6/4.7 | $5.00 | $25.00 | 1M | Moderate | Anthropic |
| Claude Sonnet 4.6 | $3.00 | $15.00 | 1M | Fast | Anthropic |
| Claude Haiku 4.5 | $1.00 | $5.00 | 200K | Fastest | Anthropic |
| GPT-5.4 | $2.50 | $15.00 | — | — | OpenAI |
| o3 | $2.00 | $8.00 | 200K | Medium-Slow | OpenAI |
| o4-mini | $1.10 | $4.40 | 200K | Medium | OpenAI |
| GPT-4o | $2.50 | $10.00 | 128K | Fast | OpenAI |
| GPT-4o-mini | $0.15 | $0.60 | 128K | Very fast | OpenAI |
| Gemini 3.1 Pro | $1.25 | $5.00 | 1M | Slow (25s TTFT) | Google |
| Gemini 2.5 Pro | $1.25 | $10.00 | 1M | Slow | Google |
| Gemini 2.5 Flash | $0.30 | $2.50 | 1M | Fast (0.7s TTFT) | Google |

### Open-Weight Models (API pricing)

| Model | Input | Output | Context | Provider |
|-------|-------|--------|---------|----------|
| DeepSeek V3.2 | $0.26 | $0.38 | 128K | DeepSeek |
| DeepSeek R1-0528 | $0.45 | $2.15 | 64K | DeepSeek |
| Qwen3.5 397B | $0.39 | $2.34 | 128K+ | Alibaba |
| Llama 4 Maverick | $0.27 | $0.85 | 1M | Meta (via Together) |
| Llama 4 Scout | $0.18 | $0.59 | 10M | Meta (via Together) |
| Mistral Large 3 | $0.50 | $1.50 | 256K | Mistral |

## Effort Controls by Provider

All three major providers offer semantic effort parameters. Tune effort
after selecting the model — this is the second layer of the cost stack.

| Provider | Parameter | Values | Default | Scope |
|----------|-----------|--------|---------|-------|
| Anthropic | `effort` | low / medium / high / xhigh / max | high | All tokens (text, tools, thinking) |
| OpenAI | `reasoning_effort` | low / medium / high | medium | Reasoning tokens only |
| Google | `thinkingLevel` (3.x) | minimal / low / medium / high | — | Thinking tokens |
| Google | `thinkingBudget` (2.5) | 0-32768 (numeric) | -1 (dynamic) | Thinking tokens |

### Effort Guidance

- **Low effort**: Simple Q&A, formatting, classification, translation.
  Saves 2-5x tokens. May skip thinking entirely on simple queries.
- **Medium effort**: Most professional tasks, content creation, standard
  coding. Good balance of quality and cost.
- **High effort**: Complex reasoning, multi-step analysis, important
  coding tasks. Default for intelligence-sensitive work.
- **Max/xhigh effort**: Frontier problems, security review, research
  synthesis. Reserve for genuinely hard problems — adds significant cost
  for relatively small quality gains on most workloads.

## Key Benchmark Notes

**Saturated (do not use for differentiation):**
MMLU (>88% at frontier), HumanEval (>92%), SWE-bench Verified (6 models
within 0.8 pts), MATH-500 (97-99%), AIME 2025 (multiple at 99-100%).

**Still differentiating:**
GPQA Diamond, SWE-bench Pro, Terminal-Bench 2.0, ARC-AGI-2, FrontierMath,
Chatbot Arena ELO.

**Caveats:**
- Benchmark scores vary 2-17 points for the same model across evaluation
  protocols. Treat rankings as ordinal (who leads), not cardinal (by how much).
- ARC-AGI-2: all 14 leaderboard scores are self-reported, 0 independently
  verified.
- Terminal-Bench scores depend on agent scaffold — swapping scaffolds
  causes ~22% score change vs ~1% for swapping top models.

## The Crossover Point

A smaller model with high effort can outperform a larger model with low
effort — up to a point. Research (Snell et al. ICLR 2025) shows a 7B
model with compute-optimal inference can match a 14x larger model. But
once accuracy saturates, the larger model wins regardless of effort.

**Rule of thumb:** If the cheaper model achieves >70% of the frontier
score on the relevant benchmark, try it with high effort before upgrading
to the next tier. If it scores <50%, skip straight to the frontier.
