---
name: Python Scripts Best Practices
description: Authoring guide for standalone Python 3 scripts — what makes a script load-bearing in production, how to shape the file, the positive patterns that work, and the safety and maintenance posture. Referenced by build-python-script and check-python-script.
---

# Python Scripts Best Practices

## What a Good Python Script Does

A Python script is a single-file program that runs from the shell, does one clear thing, and returns a useful exit code. It reads its inputs explicitly, writes primary data to stdout and diagnostics to stderr, and stays composable in pipelines and automation. The value proposition is narrow: a script earns its place when the work is too small for a package, too repeatable for a one-off notebook, and needs to be honest about success and failure to its caller.

Primitive selection — shell script vs. Python script vs. a proper package — is adjacent to this document. This guide assumes a single-file Python script is the right tool and focuses on making it a *good* one.

## Anatomy

```python
#!/usr/bin/env python3
"""One-line synopsis. Example: ./fetch_rates.py --source usd --out rates.csv"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="…")
    parser.add_argument("--out", type=Path, required=True, help="Output path.")
    args = parser.parse_args(argv)
    try:
        with args.out.open("w", encoding="utf-8") as out:
            ...
        return 0
    except KeyboardInterrupt:
        return 130
    except (FileNotFoundError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

Load-bearing pieces: the shebang and executable bit, the module docstring, the imports at module scope, the `main()` that returns an exit code, and the `__main__` guard that delegates via `sys.exit(main())`. Third-party dependencies are declared in a colocated `requirements.txt` or a PEP 723 `# /// script` block — scripts are expected to be reproducible on a fresh machine.

## Authoring Principles

**Make the entry point explicit.** Start with `#!/usr/bin/env python3`, set the executable bit, and wrap execution in a `main()` function returning an `int`, invoked via `if __name__ == "__main__": sys.exit(main())`. The guard keeps the script importable for testing; the `sys.exit(main())` wiring makes the exit contract honest. A shebang without `chmod +x` is a lie a reader will catch later than they should.

**Document intent at the top.** The first statement is a module docstring that names the script's purpose and shows one example invocation. It is often the only documentation the next reader has. Inside functions, comments explain *why* a non-obvious choice was made; comments that restate what the code does rot alongside the code.

**Parse arguments with `argparse` from the standard library.** Every argument carries a non-empty `help=` string; validation lives in `type=` and `choices=` where applicable. Manual `sys.argv` slicing loses `--help`, usage errors, and typed conversions for no gain. Reach for `click` or `typer` only when subcommands, rich help, or shell completion genuinely require them.

**Treat I/O as a contract.** Primary output goes to stdout; logs, errors, and prompts go to stderr. Specify `encoding="utf-8"` on every text-mode `open()` call — the platform default has produced silent corruption on every production system long enough to have one. Use `pathlib.Path` for filesystem paths and context managers (`with`) for any resource that needs cleanup.

**Fail loud, fail early, return meaningful codes.** Return 0 on success and non-zero on failure. Validate inputs before performing destructive work. Catch specific exceptions where you can recover and let the rest surface with a concise stderr message; reserve full tracebacks for a `--debug` flag. Handle `KeyboardInterrupt` at the top level and exit without a traceback — a script that dumps Python internals on Ctrl+C is user-hostile.

**Prefer the standard library.** `argparse`, `pathlib`, `json`, `csv`, `subprocess`, `logging`, `tempfile`, and `http.client` cover most scripting needs and ship on every Python install. When a third-party dependency earns its place, declare it explicitly — PEP 723 inline metadata or a colocated `requirements.txt` — so the script stays reproducible. Unused imports come out.

**Keep the module scope disciplined.** Imports, constants, class and function definitions, and the `__main__` guard are what belong at the top level. Configuration is passed as arguments, not assigned to module globals. A script that mutates module state at import time resists both testing and reuse.

**Name intent into the code.** Functions and variables state what they represent; numeric and string literals that carry meaning get named constants (`TIMEOUT_SECONDS`, `MAX_RETRIES`, `DEFAULT_PAGE_SIZE`). Single-letter names belong to loop counters and well-established math conventions, not to module scope. Readers spend more time interpreting names than the author spends writing them.

**Keep functions small and single-purpose.** A function does one coherent thing at one level of abstraction. Helper functions make `main()` scannable — the entry point reads as a list of named operations, not a flat wall of logic. When a function sprouts conjunctions in its name (`parse_and_validate_and_write`), it is two functions pretending to be one.

**Eliminate duplication.** Two similar lines is not a problem; three near-identical blocks is. Extract a function and give it a name. Duplication is the easiest bug multiplier to fix at authoring time and the most expensive one to fix after the copies drift.

**Hold the safety posture.** Never pass `shell=True` to subprocess calls, especially with interpolated input. Never use `eval` or `exec` on external input. Use `tempfile` for temporary paths — `/tmp/foo_{pid}` constructions invite races and symlink attacks. Keep paths, credentials, and hostnames out of the script body; read them from arguments or the environment.

**Dress the style.** Format with an automated formatter (`ruff format` or `black`) and leave the line-length debate there. Add type hints to function signatures — they are documentation that doesn't drift and they enable static analysis downstream. Prefer f-strings for formatting; avoid wildcard imports.

## Patterns That Work

These are the positive shapes a durable script tends to take. Each one corresponds to a failure mode the audit rubric catches.

**Stdlib-first dependencies over "grab whatever."** Small surface area is its own feature.

**Explicit exit codes over "it probably worked."** Callers in cron, CI, and Make depend on the contract.

**Stdout for data, stderr for chatter.** One decision that makes scripts composable for years.

**Pathlib over `os.path` strings.** Object-oriented paths remove a class of bugs.

**Context managers over manual close.** Cleanup on exceptions, guaranteed.

**Named constants over magic literals.** A value named `HTTP_TIMEOUT_SECONDS` teaches the reader what it means.

**Small functions over long ones.** Short functions with specific names read as their own commentary.

**Arguments over module globals.** Testable, explicit, and portable across invocations.

**F-strings over `%` or `.format()`.** Clearer to read, faster to execute, harder to mis-quote.

**Specific exceptions over `Exception`.** Catch what you can recover from; surface what you can't.

**PEP 723 or `requirements.txt` over undocumented deps.** The next person to run this is not you.

## Safety

Scripts run with the invoker's privileges and reach the filesystem, the network, and subprocesses. The safety rules are non-negotiable.

- **No `shell=True` on interpolated input.** Pass argument lists; shell injection is trivial and real.
- **No `eval` or `exec` on external input.** Remote-code-execution from a helpful one-liner.
- **Validate inputs before destructive work.** A `--dry-run` flag for anything that deletes or overwrites is cheap insurance.
- **`tempfile` for temporary paths.** Race conditions and symlink attacks are real and easily avoided.
- **No hardcoded credentials, hostnames, or absolute paths.** Arguments or environment variables carry those.
- **Safe parsers for untrusted structured input.** `yaml.safe_load`, not `yaml.load`; JSON over pickle from any untrusted source.

Shell-injection, `eval`/`exec`, and literal `/tmp/` path construction are audited deterministically. The remaining rules rely on author judgment — deterministic detection of "is this input validated enough before the delete?" is infeasible — and live in the authoring rubric and code review.

## Review and Decay

Scripts rot. The platform `python3` moves, third-party APIs change, the shell environment the script assumed goes away. Retire a script when it stops being invoked, when its functionality migrates into a package or service, or when its exit contract can no longer be trusted. Convert to a package when the single file acquires shared state, multiple entry points, or test coverage heavier than the code itself — single-file discipline breaks down past a threshold, and fighting it produces a worse package than starting one would. A neglected script is worse than a missing one — callers trust the exit code they have stopped checking.

---

**Diagnostic when a script misbehaves.** First check the shape: shebang, executable bit, `main()` returning an int, `__main__` guard delegating to it. Then check the contract: does it write data to stdout and diagnostics to stderr? Does it exit non-zero on every failure path? If shape and contract are right, check the scope: is the logic split into small, named functions, or is one function carrying the whole script? Most pathologies live in one of those three places.
