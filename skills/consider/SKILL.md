---
name: consider
description: >
  This skill should be used when the user wants to "think through",
  "analyze", "consider", "evaluate", "reason about", "break down",
  "prioritize", or apply structured thinking to a problem. Each model
  is a separate sub-skill invoked as /wos:consider:{model-name}.
argument-hint: "{model-name} [topic to analyze]"
user-invocable: true
---

# Consider Skill

Apply structured mental models to problems. Each model is a sub-skill in its
own directory — adding a new model requires creating a `<model-name>/SKILL.md` file.

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

Invoke any model with a topic:

```
/wos:consider:first-principles how to design a caching system
/wos:consider:inversion how to make our product successful
/wos:consider:pareto where to focus testing effort
```

If no topic is provided, apply the model to the current discussion context.
