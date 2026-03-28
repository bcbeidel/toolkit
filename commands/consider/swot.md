---
description: Map strengths, weaknesses, opportunities, and threats systematically
metadata:
  argument-hint: "[project, product, team, or strategy to evaluate]"
---

<objective>
Create a structured inventory of internal capabilities (strengths/weaknesses)
and external factors (opportunities/threats). Use the map to identify
strategic options that leverage strengths against opportunities while
defending weaknesses against threats.
</objective>

<process>
1. Define the subject being analyzed (project, product, team, strategy)
2. List internal strengths — what do we do well? What advantages exist?
3. List internal weaknesses — what could improve? What are we missing?
4. List external opportunities — what trends, changes, or gaps can we exploit?
5. List external threats — what risks, competitors, or changes endanger us?
6. Cross-reference: match strengths to opportunities (offensive strategies)
7. Cross-reference: match weaknesses to threats (defensive priorities)
</process>

<output_format>
## SWOT Analysis: [Topic]

### Internal
| Strengths | Weaknesses |
|-----------|-----------|
| [S1] | [W1] |
| [S2] | [W2] |

### External
| Opportunities | Threats |
|--------------|---------|
| [O1] | [T1] |
| [O2] | [T2] |

### Strategic Options
- **Leverage (S+O):** [Use strength X to capture opportunity Y]
- **Defend (W+T):** [Address weakness X before threat Y materializes]
- **Improve (W+O):** [Fix weakness X to unlock opportunity Y]

### Priority Action
[Single most important action based on the analysis]
</output_format>

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

