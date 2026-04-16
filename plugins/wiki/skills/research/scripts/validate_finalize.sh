#!/usr/bin/env bash
# Validate a research document is ready to finalize.
# Usage: bash validate_finalize.sh <file>
# Exit 0: OK. Exit 1: prints which check failed.

set -euo pipefail

file="${1:-}"
if [[ -z "$file" ]]; then
    echo "Usage: validate_finalize.sh <file>" >&2
    exit 1
fi

if [[ ! -f "$file" ]]; then
    echo "FAIL: file not found: $file" >&2
    exit 1
fi

fail=0

if ! grep -q "^name:" "$file"; then
    echo "MISSING: name field in frontmatter"
    fail=1
fi

if ! grep -q "^description:" "$file"; then
    echo "MISSING: description field in frontmatter"
    fail=1
fi

if ! grep -q "^type: research" "$file"; then
    echo "MISSING: type: research in frontmatter"
    fail=1
fi

if ! grep -q "https\?://" "$file"; then
    echo "MISSING: no URLs found in sources block"
    fail=1
fi

if grep -q "<!-- DRAFT -->" "$file"; then
    echo "FAIL: <!-- DRAFT --> marker still present — run finalizer first"
    fail=1
fi

if [[ "$fail" -eq 0 ]]; then
    echo "OK: research document valid"
fi

exit "$fail"
