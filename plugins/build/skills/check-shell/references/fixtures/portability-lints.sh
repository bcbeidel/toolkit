#!/usr/bin/env bash
#
# Fixture: Portability lints for /build:check-shell.
#
# Target declaration: bash-3.2-portable (so bash-4+ features flag P1).
# Each planted lint is preceded by a `# LINT:` comment naming the lint.
# This fixture is not intended to run; it exists so check-shell can
# demonstrate detection of every Portability-group lint.

set -Eeuo pipefail

# LINT: P1 target-shell feature mismatch — declare -A requires bash 4+
declare -A map
map[key]="value"

# LINT: P1 target-shell feature mismatch — mapfile requires bash 4+
mapfile -t lines < /etc/hosts

# LINT: P2 mktemp -t without portable fallback
tmpfile="$(mktemp -t myscript.XXXXXX)"
rm -f "${tmpfile}"

# LINT: P3 POSIX-sh target uses bash-only features
# (This fixture declares bash but also demonstrates the posix-sh violation
# pattern — `[[ ]]` would flag if the target were posix-sh.)
if [[ "${HOME}" == "/root" ]]; then
  :
fi
