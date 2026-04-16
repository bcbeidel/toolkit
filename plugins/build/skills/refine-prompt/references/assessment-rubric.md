# Assessment Rubric

Three dimensions, each scored 1-5. Use the examples below as anchors.

## Clarity (Is the intent unambiguous?)

| Score | Description | Example |
|-------|-------------|---------|
| 1 | Vague or ambiguous; multiple interpretations possible | "Make it better" |
| 2 | General direction clear but key terms undefined | "Optimize the performance" |
| 3 | Intent clear but some ambiguity in scope or terms | "Improve the API response time" |
| 4 | Specific and unambiguous; minor clarifications possible | "Reduce P95 API latency for the /users endpoint" |
| 5 | Crystal clear; no reasonable misinterpretation possible | "Reduce P95 latency for GET /users from 800ms to under 200ms by adding Redis caching" |

## Structure (Is it organized and scannable?)

| Score | Description | Example |
|-------|-------------|---------|
| 1 | Wall of text, no organization | Single paragraph mixing instructions, context, and constraints |
| 2 | Some separation but no clear sections | Loosely ordered sentences with line breaks |
| 3 | Logical flow but not scannable | Numbered steps without headers or grouping |
| 4 | Well-organized with clear sections | Headers or XML tags separating context, task, and output format |
| 5 | Optimally structured for the model | XML-tagged sections, clear hierarchy, scannable at every level |

## Completeness (Does it specify what success looks like?)

| Score | Description | Example |
|-------|-------------|---------|
| 1 | No output format, no criteria, no constraints | "Write some tests" |
| 2 | Output format OR criteria mentioned, not both | "Write unit tests" (format implied, no criteria) |
| 3 | Output format and basic criteria present | "Write pytest tests that cover the happy path" |
| 4 | Format, criteria, and constraints specified | "Write pytest tests covering happy path and error cases, assert specific return values" |
| 5 | Format, criteria, constraints, and edge cases | "Write pytest tests: happy path, invalid input, empty input, concurrent access. Each test asserts specific return values. Use tmp_path for file operations." |

## Scoring Guidelines

- Score each dimension independently
- Use the examples as anchors, not exact matches
- A prompt scoring 4+ on all dimensions is well-formed — do not refine
- A score of 3 means "acceptable but improvable" — refine if a technique
  condition is met
- A score of 1-2 means "needs work" — techniques will almost certainly apply
