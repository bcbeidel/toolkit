#!/usr/bin/env bash
# PostToolUse hook: runs after Write/Edit/MultiEdit on *SKILL.md files.
# Reads hook input from stdin (JSON), extracts the file path, and reports
# it for awareness. Exit 0 always — informational only.
set -euo pipefail

input=$(cat)
file=$(echo "$input" | python3 -c "
import json, sys
d = json.load(sys.stdin)
# tool_input is nested under the hook payload
ti = d.get('tool_input', d)
print(ti.get('file_path', ti.get('path', '')))
" 2>/dev/null || true)

if [[ -n "$file" ]]; then
  echo "skill-lint: $file edited — run /build:check-skill to audit quality" >&2
fi

exit 0
