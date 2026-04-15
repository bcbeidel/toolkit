#!/usr/bin/env bash
# Check whether all task checkboxes in a plan are complete.
# Usage: bash check_tasks_complete.sh <file>
# Exit 0: all tasks complete. Exit 1: prints open task count and lines.

set -euo pipefail

file="${1:-}"
if [[ -z "$file" ]]; then
    echo "Usage: check_tasks_complete.sh <file>" >&2
    exit 1
fi

if [[ ! -f "$file" ]]; then
    echo "FAIL: file not found: $file" >&2
    exit 1
fi

open_tasks=$(grep -c "^- \[ \]" "$file" || true)

if [[ "$open_tasks" -eq 0 ]]; then
    echo "OK: all tasks complete"
    exit 0
fi

echo "INCOMPLETE: $open_tasks open task(s) remain"
grep "^- \[ \]" "$file"
exit 1
