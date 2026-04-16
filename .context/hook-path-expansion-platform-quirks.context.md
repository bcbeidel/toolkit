---
name: "Hook Path Expansion Platform Quirks"
description: "Tilde (~) in Windsurf working_directory and $HOME in Claude Code command fields both fail silently; absolute paths are required on both platforms"
type: context
sources:
  - https://docs.windsurf.com/windsurf/cascade/hooks
  - https://code.claude.com/docs/en/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-windsurf-model-and-constraints.context.md
  - docs/context/hook-cross-platform-payload-nonportability.context.md
---

Two platforms have documented path expansion failures that cause silent hook load or execution errors: Windsurf does not expand `~` in `working_directory`, and Claude Code does not expand `$HOME` in command fields. Both failures are silent — the hook appears configured but does not behave as intended.

**Windsurf: `~` not expanded in `working_directory`**

The Windsurf hook configuration supports an optional `working_directory` field per hook entry. Using a tilde shorthand fails silently:

```json
{
  "hooks": {
    "pre_run_command": [{
      "command": "/usr/local/bin/my-hook.sh",
      "working_directory": "~/my-scripts"
    }]
  }
}
```

The `~/my-scripts` path is passed literally and is not resolved to the user's home directory. The hook may fail to locate its working directory or silently use the wrong path. Use absolute paths:

```json
"working_directory": "/Users/username/my-scripts"
```

**Claude Code: `$HOME` not expanded in command fields**

Claude Code hook command strings do not expand `$HOME`. A command like `$HOME/.local/bin/my-hook.sh` will not resolve correctly. As with Windsurf, this failure is silent — the hook configuration is accepted, but the command fails at execution time because the path is not resolved.

**Pattern**

Both failures are instances of the same class: hook configuration systems that accept path strings but do not apply shell-level variable or tilde expansion to those strings at load time. The shell expansion that developers expect from interactive use is not guaranteed in configuration file contexts. The safe pattern on both platforms: use absolute paths with no shell variables in hook command and working directory fields.
