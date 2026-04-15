#!/usr/bin/env bash
# Validate a plan document has all required sections and a status field.
# Usage: bash validate_plan.sh <file>
# Exit 0: OK. Exit 1: prints MISSING: for each failed check.

set -euo pipefail

file="${1:-}"
if [[ -z "$file" ]]; then
    echo "Usage: validate_plan.sh <file>" >&2
    exit 1
fi

if [[ ! -f "$file" ]]; then
    echo "FAIL: file not found: $file" >&2
    exit 1
fi

fail=0

if ! grep -qi "^## *Goal" "$file"; then
    echo "MISSING: Goal section"
    fail=1
fi

if ! grep -qi "^## *Scope" "$file"; then
    echo "MISSING: Scope section"
    fail=1
fi

if ! grep -qi "^## *Approach" "$file"; then
    echo "MISSING: Approach section"
    fail=1
fi

if ! grep -qi "^## *File Changes" "$file"; then
    echo "MISSING: File Changes section"
    fail=1
fi

if ! grep -qi "^## *Tasks" "$file"; then
    echo "MISSING: Tasks section"
    fail=1
fi

if ! grep -qi "^## *Validation" "$file"; then
    echo "MISSING: Validation section"
    fail=1
fi

if ! grep -q "^status:" "$file"; then
    echo "MISSING: status field in frontmatter"
    fail=1
fi

if [[ "$fail" -eq 0 ]]; then
    echo "OK: plan structure valid"
fi

exit "$fail"
