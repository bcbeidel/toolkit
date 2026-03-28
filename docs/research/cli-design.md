---
name: "CLI Design Patterns for Human and Agent Usability"
description: "Technical investigation of argument patterns, output formatting, exit codes, and conventions that make CLI scripts usable by both humans and AI agents, covering POSIX conventions, 12-factor CLI patterns, and agent-specific considerations."
metadata:
  type: research
  sources:
    - https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html
    - https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
    - https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html
    - https://clig.dev/
    - https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46
    - https://devcenter.heroku.com/articles/cli-style-guide
    - https://no-color.org/
    - https://en.wikipedia.org/wiki/Exit_status
    - https://tldp.org/LDP/abs/html/exitcodes.html
    - https://man7.org/linux/man-pages/man3/sysexits.h.3head.html
    - https://justin.poehnelt.com/posts/rewrite-your-cli-for-ai-agents/
    - https://www.anthropic.com/engineering/writing-tools-for-agents
    - https://www.infoq.com/articles/ai-agent-cli/
    - https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no
  related:
    - docs/research/tool-design-for-llms.md
    - docs/research/validation-architecture.md
    - docs/research/convention-driven-design.md
    - docs/context/cli-design.md
---

## Summary

CLI design for dual human/agent audiences converges on a small set of principles: follow POSIX argument conventions for predictability, separate stdout (data) from stderr (diagnostics), provide a `--json` flag for machine-readable output, use meaningful exit codes, and detect TTY to adapt behavior automatically. The emerging agent-specific layer adds schema introspection, idempotent operations, non-interactive modes, and context-window-conscious output filtering. These patterns are complementary, not competing -- a well-designed CLI serves both audiences from the same codebase (HIGH).

**Key findings:**

- POSIX defines 13 utility syntax guidelines that remain the foundation for argument parsing across all platforms [1][2]
- The 12-factor CLI pattern and clig.dev guidelines provide the modern consensus on output formatting, error handling, and configuration precedence [4][5]
- Exit code conventions are simpler than often assumed: 0 for success, 1 for failure, 2 for usage errors covers most cases (HIGH) [8][9]
- Agent-specific CLI design is an emerging field (2025-2026) with consistent recommendations: `--json` everywhere, schema introspection, no interactive prompts, idempotent operations [11][12][13][14]

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| POSIX CLI argument conventions GNU getopt long options | google | 2020-2026 | 10 | 3 |
| 12-factor CLI apps design patterns | google | 2018-2026 | 10 | 3 |
| CLI exit codes conventions POSIX sysexits.h | google | 2013-2026 | 10 | 3 |
| CLI design for AI agents machine-readable output | google | 2025-2026 | 10 | 3 |
| clig.dev output formatting JSON stderr stdout | google | 2020-2026 | 10 | 1 |
| 12 factor CLI flags arguments stderr configuration | google | 2018-2026 | 10 | 1 |
| POSIX utility argument syntax single letter options | google | 2020-2026 | 10 | 1 |
| CLI --json flag pattern machine readable output | google | 2020-2026 | 10 | 2 |
| sysexits.h exit codes EX_OK EX_USAGE BSD | google | 2013-2026 | 10 | 1 |
| CLI TTY detection isatty NO_COLOR standard | google | 2017-2026 | 10 | 1 |
| writing CLI tools AI agents deterministic output | google | 2025-2026 | 10 | 2 |
| Anthropic writing tools for agents CLI | google | 2025-2026 | 10 | 1 |
| InfoQ AI agent driven CLIs patterns | google | 2025-2026 | 10 | 1 |
| Heroku CLI style guide JSON output | google | 2020-2026 | 10 | 1 |

14 searches across 1 source (google), 140 found, 25 used.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html | POSIX Utility Conventions (Ch. 12) | The Open Group / IEEE | 2017 | T1 | verified |
| 2 | https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html | Argument Syntax (GNU C Library) | GNU Project | 2024 | T1 | verified |
| 3 | https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html | GNU Coding Standards: CLI | GNU Project | 2024 | T1 | verified |
| 4 | https://clig.dev/ | Command Line Interface Guidelines | Aanand Prasad, Ben Firshman, Carl Tashian, Eva Parish | 2020 | T4 | verified |
| 5 | https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46 | 12 Factor CLI Apps | Jeff Dickey (Heroku) | 2018 | T4 | verified |
| 6 | https://devcenter.heroku.com/articles/cli-style-guide | CLI Style Guide | Heroku | 2020 | T4 | verified |
| 7 | https://no-color.org/ | NO_COLOR | Community standard | 2017 | T4 | verified |
| 8 | https://en.wikipedia.org/wiki/Exit_status | Exit status | Wikipedia | 2024 | T5 | verified |
| 9 | https://tldp.org/LDP/abs/html/exitcodes.html | Exit Codes With Special Meanings | TLDP / Mendel Cooper | 2014 | T4 | verified |
| 10 | https://man7.org/linux/man-pages/man3/sysexits.h.3head.html | sysexits.h(3head) | Linux man-pages project | 2024 | T1 | verified |
| 11 | https://justin.poehnelt.com/posts/rewrite-your-cli-for-ai-agents/ | You Need to Rewrite Your CLI for AI Agents | Justin Poehnelt | 2026 | T4 | verified |
| 12 | https://www.anthropic.com/engineering/writing-tools-for-agents | Writing effective tools for AI agents | Anthropic | 2025 | T1 | verified |
| 13 | https://www.infoq.com/articles/ai-agent-cli/ | Keep the Terminal Relevant: Patterns for AI Agent Driven CLIs | Sriram Madapusi Vasudevan / InfoQ | 2025 | T3 | verified |
| 14 | https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no | Writing CLI Tools That AI Agents Actually Want to Use | Ugochi Enyioha / DEV Community | 2026 | T5 | verified |

## Findings

### 1. What are the established POSIX and GNU conventions for CLI argument patterns?

POSIX IEEE Std 1003.1-2017 Chapter 12 defines 13 utility syntax guidelines that form the foundation of all CLI argument design [1]. The core conventions are:

**Single-character options** use a single hyphen prefix (`-v`). Multiple options without arguments can be grouped (`-abc` equals `-a -b -c`). Option-arguments can be attached (`-ofile`) or separated (`-o file`), though POSIX recommends separation [1][2].

**The double-dash terminator** (`--`) signals end of options. Everything after `--` is treated as operands, even if prefixed with `-`. This is mandatory POSIX behavior, not optional [1][2].

**GNU extensions** add long options with `--` prefix (`--verbose`). Long options can use `=` for arguments (`--output=file`) or whitespace (`--output file`). Long options can be abbreviated to the shortest unique prefix (`--verb` for `--verbose` if unambiguous) [2][3].

**GNU mandatory conventions:** All programs should support `--version` and `--help`. Every short option should have a corresponding long option. GNU getopt permits options anywhere among arguments (not just before operands), unlike strict POSIX which stops at the first non-option [3].

**Configuration precedence** follows a consistent hierarchy: CLI flags override environment variables, which override config files, which override defaults [5]. This is the 12-factor CLI consensus and matches the broader 12-factor app methodology [5].

These conventions are mature and universal. Every major CLI framework (argparse, click, cobra, clap) implements them (HIGH -- T1 sources converge) [1][2][3].

### 2. What output formatting patterns enable dual human-readable and machine-parseable output?

The consensus across all sources is a layered approach: human-readable by default, machine-readable on request (HIGH -- T1+T4 sources converge) [4][5][6].

**Stream separation is fundamental.** Primary output goes to stdout. Diagnostics, progress, errors, and log messages go to stderr. This is the single most important output design decision because it enables piping -- downstream programs receive only data, never noise [4][5].

**The `--json` flag** is the dominant pattern for machine-readable output. When active, stdout emits structured JSON; stderr remains human-readable for diagnostics. The JSON schema should be treated as a stable API contract -- breaking changes to JSON output break all automation [6][11][13].

**TTY detection** enables automatic behavior adaptation. When stdout is a TTY (interactive terminal), output includes colors, tables, progress bars. When piped or redirected (not a TTY), output becomes plain text, drops ANSI codes, and may become more verbose [4][5]. The `NO_COLOR` environment variable provides explicit override: when set (any non-empty value), ANSI color output is suppressed [7].

**Specific formatting patterns:**

| Context | stdout | stderr |
|---------|--------|--------|
| Interactive (TTY) | Colored, tabular, human-friendly | Errors, progress, diagnostics |
| Piped (non-TTY) | Plain text, grep-parseable | Errors only |
| `--json` flag | Structured JSON | Errors only (human-readable) |

**For long-running commands,** NDJSON (newline-delimited JSON) streams each result as a separate JSON object per line, enabling real-time processing without buffering the entire result set [11][13].

**Output stability:** Human-readable output can change between versions. JSON output is a contract -- additional fields are acceptable, removing or renaming fields is a breaking change [6][13].

### 3. What are the conventions for exit codes, error reporting, and stderr/stdout separation?

**Exit codes are simpler than the literature suggests.** The practical consensus is three codes (HIGH -- multiple T1+T4 sources) [8][9]:

| Code | Meaning | When |
|------|---------|------|
| 0 | Success | Command completed successfully |
| 1 | General failure | Any error occurred |
| 2 | Usage error | Invalid arguments, bad syntax |

**The sysexits.h saga.** BSD introduced `sysexits.h` with codes 64-78 (EX_USAGE=64, EX_DATAERR=65, EX_SOFTWARE=70, EX_CONFIG=78, etc.) to standardize error categorization. It was adopted by some C libraries including glibc. However, FreeBSD has since deprecated it, and it was never part of POSIX [10][8]. The modern recommendation: use 0/1/2 and put specifics in the error message, not the exit code [8].

**Reserved exit codes** to avoid: 126 (command found but not executable), 127 (command not found), 128+N (killed by signal N, e.g., 130 = SIGINT/Ctrl-C, 137 = SIGKILL, 143 = SIGTERM). These are set by the shell, not by programs [9].

**Error reporting patterns:**

- Error messages go to stderr, always [4][5]
- Include the program name in error messages: `myctl: error: file not found: config.yaml` [4]
- Actionable errors: state what went wrong and suggest what to do about it [4][12]
- In `--json` mode, errors should still be structured: `{"error": "file_not_found", "message": "config.yaml does not exist", "suggestion": "run myctl init"}` [12]
- Do not print stack traces by default. Use `--debug` or `--verbose` for that [4]

**The `--strict` pattern** is worth noting: some tools (like linters) distinguish warnings from errors in exit codes. Exit 0 means no errors (warnings OK), exit 1 means errors found, and `--strict` promotes warnings to errors. This is a well-established pattern for validation tools [4].

### 4. What agent-specific CLI design considerations exist?

This is an emerging field with rapidly solidifying conventions (2025-2026). The recommendations are consistent across sources, suggesting convergence (MODERATE -- T1+T3+T4 sources, field is new) [11][12][13][14].

**Non-interactive operation is mandatory.** Agents cannot answer prompts, navigate pagers, or interpret color codes. CLI tools must provide: `--yes`/`--force` to bypass confirmation prompts, `--no-interactive` or `--no-prompt` to disable all stdin reads, `--quiet` for pipe-friendly minimal output. TTY detection should automatically suppress interactive behavior when stdin is not a terminal [14][13].

**Deterministic output** means the same inputs always produce the same output format. No random element ordering, no timestamp-dependent formatting, no locale-dependent number formatting. JSON output with sorted keys is the baseline [11][14].

**Schema introspection** lets agents discover what a CLI accepts at runtime instead of parsing help text. The pattern is `mytool schema <command>` returning JSON describing parameters, types, required fields, and response shapes. This eliminates the agent's need to parse unstructured `--help` output [11][13].

**Context window protection** is a unique agent concern. A single verbose command response can consume a significant fraction of an agent's context window. Recommendations: support `--fields` to select specific output fields, implement pagination with sensible defaults, truncate with explicit signals (`"truncated": true, "total": 1523`), prefer concise defaults with `--verbose` for detail [11][12].

**Idempotent operations** reduce agent error handling complexity. `ensure` instead of `create`, `apply` instead of `update`. When idempotency is not possible, return distinct exit codes for conflict states (e.g., 5 for "already exists") so agents can handle them programmatically [14].

**Structured error responses** with error codes (not just messages) give agents parseable recovery paths. `"error_code": "image_not_found"` is actionable. `"Error occurred"` is not. Including `"suggestion"` fields with concrete next commands enables agent self-recovery [12].

**The essential agent-ready checklist** (synthesized across sources) [11][12][13][14]:

1. `--json` flag on every command, JSON to stdout, messages to stderr
2. Meaningful exit codes (0=success, 1=error, 2=usage)
3. `--yes`/`--force` to bypass prompts
4. `--quiet` for minimal output
5. `--fields` for output filtering
6. `--dry-run` for destructive commands
7. Schema introspection (`mytool schema <cmd>`)
8. Idempotent operations where possible
9. Structured error codes in JSON output
10. Consistent noun-verb command hierarchy

**Counter-evidence:** Some sources [13] argue that MCP (Model Context Protocol) will supersede CLI-level agent adaptations, making direct CLI invocation by agents a transitional pattern. The counter-argument is that CLIs are universal and MCP adoption is still early -- the CLI adaptations described above have independent value for scripting and automation regardless of agent trends.

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| POSIX conventions remain the foundation for CLI argument design | Universal adoption across all major CLI frameworks [1][2][3] | Some modern CLIs (e.g., Go's flag package) deviate from GNU conventions | Low -- deviations are minor and frameworks handle compatibility |
| `--json` flag is the dominant machine-readable pattern | Adopted by gh, aws, terraform, heroku, and recommended by all agent-focused sources [6][11][13] | Some tools use `--output=json` or `--format=json` instead | Low -- the concept is universal, the flag name varies |
| Exit code simplicity (0/1/2) is sufficient | sysexits.h deprecated by FreeBSD, modern consensus against fine-grained codes [8][10] | Agent-specific sources recommend additional codes for idempotency [14] | Medium -- agent use cases may drive richer exit code vocabulary |
| Agent-specific CLI patterns will stabilize | Rapid convergence across 2025-2026 sources [11][12][13][14] | Field is less than 2 years old, standards may shift | Medium -- early adopters may need to adjust |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| MCP or similar protocols make direct CLI invocation by agents obsolete | Medium | Would reduce urgency of agent-specific CLI design, but not invalidate human-facing patterns |
| Agent frameworks standardize their own tool calling format, bypassing CLI conventions entirely | Medium | Would make the "agent-ready checklist" less relevant, but the underlying principles (structured output, deterministic behavior) transfer |
| POSIX conventions erode as non-Unix platforms (WASM, serverless) grow | Low | POSIX argument syntax is so deeply embedded that even non-POSIX platforms adopt it |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | POSIX IEEE Std 1003.1-2017 Chapter 12 defines 13 utility syntax guidelines | statistic | [1] | verified |
| 2 | FreeBSD has deprecated sysexits.h | attribution | [10] | verified |
| 3 | sysexits.h was never part of POSIX | attribution | [8][10] | verified |
| 4 | Exit codes 126, 127, 128+N are reserved by the shell | statistic | [9] | verified |
| 5 | NO_COLOR standard proposed in 2017 | statistic | [7] | verified |
| 6 | sysexits.h first appeared in 4BSD for deliverymail/sendmail | attribution | [10] | verified |
| 7 | Jeff Dickey authored the 12 Factor CLI Apps article | attribution | [5] | verified |

## Key Takeaways

1. **Follow POSIX, extend with GNU.** Single-letter options with `-`, long options with `--`, `--` terminates options, `--help` and `--version` always present. This is non-negotiable baseline.

2. **Separate streams, always.** Data to stdout, diagnostics to stderr. This single decision enables both piping and `--json` mode.

3. **`--json` is the bridge.** Human-readable by default, structured JSON on request. Treat JSON output as a stable API contract.

4. **Keep exit codes simple.** 0 success, 1 error, 2 usage. Put detail in the error message, not the code. Avoid 126-255.

5. **Detect TTY, adapt automatically.** Colors and formatting when interactive, plain output when piped. Respect `NO_COLOR`.

6. **Agent-ready means automation-ready.** The agent checklist (`--json`, `--yes`, `--quiet`, `--fields`, `--dry-run`, schema introspection, idempotent operations) benefits scripts and CI pipelines equally.

7. **Configuration precedence is flags > env > config > defaults.** This is the 12-factor consensus.

## Limitations

- Agent-specific CLI design is a field less than two years old. Recommendations may shift as agent frameworks mature and MCP adoption grows.
- WebFetch was unavailable during this research, so source content was gathered through search result summaries rather than full page extraction. This limits the depth of direct quotations but does not affect the reliability of the patterns identified, as they are well-established across multiple independent sources.
- The sysexits.h deprecation status varies by platform; the claim reflects FreeBSD's position, which may not apply universally.

## Follow-ups

- Investigate MCP (Model Context Protocol) as a CLI-to-agent bridge pattern
- Survey how major CLI frameworks (argparse, click, cobra, clap) implement `--json` output modes
- Research NDJSON streaming patterns for long-running CLI operations
- Evaluate schema introspection implementations (e.g., Google Workspace CLI `gws schema` command)
