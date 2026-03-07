---
description: Apply structured mental models to think through problems. Use when the user wants to "analyze", "evaluate", "think through", "decide between", "weigh tradeoffs", or needs a framework for a decision.
argument-hint: "{model-name} [topic to analyze]"
---

Apply structured mental models to problems. If a specific model was requested,
invoke the matching `/consider:{model-name}` command. If no model was specified,
help the user choose by presenting the options below.

## Available Models

| Model | When to use |
|-------|------------|
| `first-principles` | Break down assumptions, rebuild from fundamentals |
| `occams-razor` | Find the simplest explanation that fits all facts |
| `inversion` | Solve problems backwards, identify failure modes |
| `second-order` | Think through consequences of consequences |
| `eisenhower-matrix` | Prioritize by urgency and importance |
| `opportunity-cost` | Analyze what you give up by choosing this option |
| `via-negativa` | Improve by removing rather than adding |
| `pareto` | Apply 80/20 rule to find leverage points |
| `5-whys` | Drill to root cause by asking why repeatedly |
| `swot` | Map strengths, weaknesses, opportunities, threats |
| `10-10-10` | Evaluate decisions across three time horizons |
| `one-thing` | Identify the single highest-leverage action |
| `circle-of-competence` | Scope decisions, know what you don't know |
| `map-vs-territory` | Recognize model limitations, check assumptions |
| `reversibility` | Assess decision risk — one-way vs two-way doors |
| `hanlons-razor` | Interpret behavior charitably, avoid conspiracy thinking |

## Usage

```
/consider:first-principles how to design a caching system
/consider:inversion how to make our product successful
/consider:pareto where to focus testing effort
```

If no model is specified, ask the user what they want to think through, then
suggest 2-3 models that would be most relevant to their problem.
