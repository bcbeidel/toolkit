# toolkit

> **Experimental** — This project is under active development. APIs, skill
> interfaces, and document conventions may change without notice.

A Claude Code plugin marketplace for building and maintaining structured project context,
with AI-assisted research, source verification, and quality validation.

For Claude Code users who want reusable tooling for skill authoring, project
documentation, task planning, and structured reasoning — packaged as four
independently installable plugins.

## Prerequisites

- Python 3.9+
- No runtime Python dependencies (stdlib only)
- `gh` CLI (for `work:finish-work` skill)

## Plugins

Four self-contained plugins, each independently installable:

| Plugin | Install | Skills |
|--------|---------|--------|
| `wiki` | `claude plugin install bcbeidel/toolkit --plugin wiki` | `setup`, `research`, `ingest`, `lint` |
| `build` | `claude plugin install bcbeidel/toolkit --plugin build` | 26 skills for creating and auditing Claude Code primitives (skills, rules, hooks, subagents, scripts, configs) |
| `work` | `claude plugin install bcbeidel/toolkit --plugin work` | `scope-work`, `plan-work`, `start-work`, `verify-work`, `finish-work` |
| `consider` | `claude plugin install bcbeidel/toolkit --plugin consider` | 16 mental models + meta |

## Installation

**Knowledge** — build and maintain project context documents:
```bash
claude plugin install bcbeidel/toolkit --plugin wiki
```

**Build tooling** — create, audit, and maintain Claude Code skills and rules:
```bash
claude plugin install bcbeidel/toolkit --plugin build
```

**Full suite** — complete toolkit for AI-assisted project work:
```bash
claude plugin install bcbeidel/toolkit --plugin wiki
claude plugin install bcbeidel/toolkit --plugin build
claude plugin install bcbeidel/toolkit --plugin work
claude plugin install bcbeidel/toolkit --plugin consider
```

## Usage

Once installed, invoke a plugin's skills via the `/plugin:skill-name` syntax
in Claude Code. For example, after installing the `wiki` plugin:

```text
/wiki:setup
```

Expected: Claude Code initializes project context directories and prompts
for any missing metadata.

See each plugin's skill directory for the full skill catalogue
(`plugins/<plugin>/skills/`).

## Security scanning

Every PR that touches `plugins/`, `policy/`, or the scanner pipeline runs
the [Cisco AI Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner)
plus a Claude evaluator and posts a single `Skill Security Audit Report`
comment on the PR. The gate blocks merge on `overall_severity=high` unless
the PR carries the `security-override` label.

The scanner runs in two coupled workflows:

- `.github/workflows/skill-audit-scan.yml` — `pull_request`, `contents: read`
  only, runs against the PR head. Produces a `scan-<plugin>` artifact.
- `.github/workflows/skill-audit-report.yml` — `workflow_run`, checks out
  trusted `main`, posts the comment, enforces the gate.

Detection rules (taxonomy, escalation signals, prohibited extensions) live
in [`policy/skill-scan-policy.yml`](policy/skill-scan-policy.yml). The
SHA256 of that file is recorded as `policy_fingerprint` on every scan.

Run locally before pushing:

```bash
export ANTHROPIC_API_KEY=<key>
make scan PLUGIN=build      # one plugin
make scan-all               # every plugin
make scan-clean             # remove scan-output/
```

`make scan` mirrors the CI workflow: same policy file, same hash-locked
deps in `.github/scripts/requirements.lock`, same `--fail-on-severity high`
threshold. A clean local scan should match what CI produces on the same SHA.

Composition with `/build:check-skill`: that skill audits authorship quality
(structure, completeness, prompt clarity); `skill-audit-*` audits adversarial
content (prompt injection, exfiltration, supply-chain risk). They are
independent, complementary signals.

## Local Development

```bash
pip install -e plugins/wiki -e ".[dev]"

python -m pytest plugins/wiki/tests/ -v

ruff check plugins/
```

## Project Structure

```text
plugins/
  build/       # Skill authoring and auditing
  wiki/        # Project context: setup, research, ingest, lint
    src/wiki/  # Python package
    scripts/   # Shared CLI scripts
    skills/    # Skill definitions
    tests/     # Unit tests
  work/        # Task scoping, planning, execution
  consider/    # Structured mental models
.context/      # Domain knowledge and conventions
.plans/        # Implementation plans
.research/     # Research investigations
.prompts/      # Saved and refined prompts
.claude-plugin/
  marketplace.json
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
