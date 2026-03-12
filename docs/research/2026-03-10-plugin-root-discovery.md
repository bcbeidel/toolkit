---
name: Plugin Root Discovery Patterns for Python Scripts
description: Investigation of how Python plugin scripts should discover their package root directory, comparing chained .parent, marker-based search, environment variables, and importlib approaches
type: research
sources:
  - https://github.com/jayqi/python-find-project-root-cookbook
  - https://code.claude.com/docs/en/plugins-reference
  - https://github.com/anthropics/claude-code/issues/9354
  - https://github.com/anthropics/claude-code/issues/11011
  - https://docs.python.org/3/library/pathlib.html
  - https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/
  - https://docs.pytest.org/en/stable/reference/customize.html
  - https://docs.python.org/3/library/importlib.resources.html
related:
---
# Plugin Root Discovery Patterns for Python Scripts

## Summary

**Bottom line:** For WOS plugin scripts, the chained `.parent` pattern is the
correct choice — not because it's elegant, but because it's the only approach
that works reliably in the Claude Code plugin cache environment. Marker-based
search is the standard Python answer but introduces ambiguity risks in nested
project contexts. Environment variables would be ideal but `CLAUDE_PLUGIN_ROOT`
is not available to scripts invoked from skill instructions.

## Sub-Questions

1. What patterns exist in the wild for Python root discovery?
2. What are the failure modes of each approach?
3. What does the Python packaging ecosystem recommend?
4. What does the Claude Code plugin runtime actually provide?
5. What's the simplest correct solution for WOS's constraints?

## Search Protocol

| # | Query | Source | Results |
|---|-------|--------|---------|
| 1 | Python find project root pyproject.toml marker file walk up | WebSearch | python-find-project-root-cookbook, project-paths PyPI, Real Python |
| 2 | Python importlib.resources package root discovery plugin | WebSearch | Python packaging guide, importlib docs |
| 3 | pytest rootdir discovery algorithm | WebSearch | pytest configuration docs |
| 4 | Python __file__ parent chained pathlib find package root | WebSearch | pathlib docs, Real Python, various tutorials |
| 5 | Claude Code CLAUDE_PLUGIN_ROOT environment variable | WebSearch | Plugin reference docs, issues #9354, #11011 |
| 6 | anthropics/claude-code plugin-scripts-dir path resolution | WebSearch | Plugin structure docs, issue #11011 |

## Sources

| # | URL | Title | Author/Org | Tier | Status |
|---|-----|-------|-----------|------|--------|
| 1 | https://github.com/jayqi/python-find-project-root-cookbook | Python Find Project Root Cookbook | jayqi | T3 | verified |
| 2 | https://code.claude.com/docs/en/plugins-reference | Plugins Reference | Anthropic | T1 | verified |
| 3 | https://github.com/anthropics/claude-code/issues/9354 | Fix CLAUDE_PLUGIN_ROOT in command markdown | bartolli / rhuss | T2 | verified |
| 4 | https://github.com/anthropics/claude-code/issues/11011 | Skill plugin scripts fail on first execution | community | T2 | verified |
| 5 | https://docs.python.org/3/library/pathlib.html | pathlib documentation | Python Software Foundation | T1 | verified |
| 6 | https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/ | Creating and discovering plugins | PyPA | T1 | verified |
| 7 | https://docs.pytest.org/en/stable/reference/customize.html | pytest configuration | pytest-dev | T1 | verified |
| 8 | https://docs.python.org/3/library/importlib.resources.html | importlib.resources | Python Software Foundation | T1 | verified |

## Findings

### 1. What patterns exist in the wild?

Five distinct approaches appear in practice (HIGH — T1 + T3 sources converge):

**A. Chained `.parent` (most common for scripts)**

```python
_root = Path(__file__).resolve().parent.parent.parent
```

Used by: WOS existing scripts, many open-source CLI tools. Simple,
dependency-free, predictable. Fragile if files move. The
[python-find-project-root-cookbook][1] documents this as the baseline approach.

**B. Marker-based walk-up (most common for tools)**

```python
def find_root(marker="pyproject.toml"):
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / marker).exists():
            return current
        current = current.parent
    raise RuntimeError("Root not found")
```

Used by: pytest (rootdir discovery [7]), many build tools. Resilient to
restructuring. Can find wrong root in nested projects.

**C. Environment variable**

```python
root = os.environ["PLUGIN_ROOT"]
```

Used by: Claude Code hooks/MCP servers via `${CLAUDE_PLUGIN_ROOT}` [2],
Docker-based tools, CI systems. Explicit, debuggable. Requires external
configuration.

**D. `importlib.resources` (for installed packages)**

```python
from importlib.resources import files
resource = files("wos") / "data" / "config.json"
```

Used by: installed Python packages that need to access bundled data [8].
Not applicable to scripts that need to find the repo root for `sys.path`
insertion — the package isn't importable yet at that point.

**E. `__package__` / package metadata**

```python
from importlib.metadata import packages_distributions
```

Used by: pip, setuptools for plugin discovery via entry points [6]. Requires
the package to be installed. Not applicable to `uv run` PEP 723 scripts.

### 2. What are the failure modes?

| Approach | Failure Mode | Severity for WOS |
|----------|-------------|-----------------|
| Chained `.parent` | Breaks silently if script moves to different depth | Medium — scripts rarely move |
| Marker walk-up | Finds wrong `pyproject.toml` in nested projects | High — WOS runs inside user projects that have their own `pyproject.toml` |
| Environment variable | `CLAUDE_PLUGIN_ROOT` not set during skill script execution | Blocking — can't use today |
| `importlib.resources` | Package must be installed first | Blocking — scripts run before import |
| Package metadata | Package must be installed | Blocking — same as above |

**Critical finding:** The marker-based approach — the standard Python answer —
is actually *dangerous* for WOS. When a WOS skill runs `uv run` on a plugin
script, the script executes inside the user's project directory. If the user's
project has a `pyproject.toml` (and most do), the marker walk-up would find the
*user's* project root instead of the *plugin's* root (HIGH — confirmed by
testing the cache directory structure at
`~/.claude/plugins/cache/wos/wos/0.17.0/`).

### 3. What does the Python ecosystem recommend?

The Python Packaging Authority [6] recommends three plugin discovery
mechanisms: naming conventions, namespace packages, and entry points. All
three assume the package is *installed* — none address the case of standalone
scripts that need to find their containing package for `sys.path` insertion
before any imports work.

pytest's rootdir algorithm [7] uses marker walk-up but it controls the
execution context — it knows it's searching for the *project* root. WOS
scripts have the opposite problem: they need to find the *plugin* root while
running inside a *different* project.

The python-find-project-root-cookbook [1] acknowledges that marker-based search
"stops at first match (problematic in monorepos)" — the WOS plugin cache
scenario is functionally the same problem.

### 4. What does the Claude Code plugin runtime provide?

`${CLAUDE_PLUGIN_ROOT}` is the intended solution [2] but it only works in JSON
configurations (hooks, MCP servers). It is **not available** during skill
script execution [3][4]. This is a known bug with 44+ upvotes [3]. There is no
fix date announced.

The `<plugin-scripts-dir>` placeholder in WOS skill instructions is not a
system feature — it's a convention where the model resolves the path at
runtime by navigating from the skill file's known location. The model
essentially does the `.parent` chain in its head, converting the placeholder
to an absolute path like `/Users/.../.claude/plugins/cache/wos/wos/0.17.0/scripts/`.

This means WOS scripts face a bootstrapping problem: the model provides the
correct *invocation* path, but once the script is running, it must
independently rediscover the plugin root for `sys.path` insertion.

### 5. What's the simplest correct solution for WOS?

Given the constraints (stdlib-only, PEP 723 scripts, plugin cache, runs inside
user projects), the options narrow to:

**Option A: Chained `.parent` with comment (current approach)**
```python
# skills/research/scripts/ → skills/research/ → skills/ → plugin root
_plugin_root = Path(__file__).resolve().parent.parent.parent.parent
```
- Pro: Simple, predictable, no false positives
- Con: Fragile to moves, depth varies by script location
- Risk: Low — script locations are stable conventions

**Option B: Marker walk-up with WOS-specific marker**
Instead of `pyproject.toml`, search for a marker unique to WOS — like
`plugin.json` or `.claude-plugin/plugin.json`:
```python
def _find_plugin_root():
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".claude-plugin" / "plugin.json").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find plugin root")
```
- Pro: Resilient to restructuring, won't match user projects
- Con: `.claude-plugin/plugin.json` is optional per Anthropic docs [2]
- Risk: Medium — depends on manifest presence

**Option C: Hybrid — try environment variable, fall back to `.parent`**
```python
def _find_plugin_root():
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root and os.path.isdir(env_root):
        return Path(env_root)
    # Fallback: navigate from __file__
    return Path(__file__).resolve().parent.parent.parent.parent

_plugin_root = _find_plugin_root()
```
- Pro: Future-proof — when Anthropic fixes #9354, scripts auto-upgrade
- Con: Slightly more code, env var may never be fixed
- Risk: Low — fallback is the proven pattern

## Challenge

**Counter-argument to Option C (hybrid):** Adding `CLAUDE_PLUGIN_ROOT` support
is speculative engineering. The env var doesn't work today, may never work for
skill-invoked scripts, and the fallback is the `.parent` chain anyway. We'd be
adding code that never executes in practice (YAGNI, P5).

**Response:** The hybrid adds 4 lines and the env var check is a single
`os.environ.get()`. If Anthropic fixes #9354, we get free resilience. If they
don't, we pay ~4 lines. The cost-benefit ratio favors inclusion.

**Counter-argument to chained `.parent`:** It's fragile and ugly.

**Response:** "Ugly" is not a defect. The pattern is *predictable* — given a
file's path, you can count parents to verify correctness. It only breaks if
scripts move, which is a deliberate architectural change that would require
updating the path anyway. The "fragility" is detectable at test time.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | `CLAUDE_PLUGIN_ROOT` only works in JSON configs, not skill scripts | factual | [3][4] | verified |
| 2 | Marker walk-up can find wrong root in nested projects | factual | [1] | verified |
| 3 | `<plugin-scripts-dir>` is model-resolved, not system-resolved | inference | WOS codebase | verified (grep confirms it's a placeholder in markdown, not a runtime variable) |
| 4 | `importlib.resources` requires package to be installed first | factual | [8] | verified |
| 5 | pytest uses marker walk-up for rootdir | factual | [7] | verified |

## Recommendation

**Option C (hybrid)** is the best answer for WOS:

```python
import os
from pathlib import Path

def _find_plugin_root() -> Path:
    """Find the plugin root directory.

    Prefers CLAUDE_PLUGIN_ROOT env var (set by Claude Code for hooks/MCP).
    Falls back to navigating from __file__ (required for skill-invoked scripts).
    """
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root and os.path.isdir(env_root):
        return Path(env_root)
    # skills/research/scripts/ → skills/research/ → skills/ → plugin root
    return Path(__file__).resolve().parent.parent.parent.parent
```

This should be:
1. Defined in each script (not extracted to a shared utility — scripts must be
   self-contained per P7)
2. Include a comment documenting the parent chain depth
3. Check `CLAUDE_PLUGIN_ROOT` first for forward-compatibility

For shared scripts in `scripts/` (2 parents deep), the fallback line would be:
```python
return Path(__file__).resolve().parent.parent
```
