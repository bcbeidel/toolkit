#!/usr/bin/env bash
#
# Fixture: Safety lints for /build:check-shell.
#
# Target declaration: bash-3.2-portable. Each planted lint is preceded
# by a `# LINT:` comment naming the lint. This fixture is not intended
# to run correctly; it exists so check-shell can demonstrate detection
# of every Safety-group lint.

# (intentionally no `set -Eeuo pipefail` — so we can plant unsafe
# patterns without aborting if this ever does execute)

VAR="value with spaces"

# LINT: S1 unquoted variable expansion
echo $VAR

# LINT: S2 for f in $(ls ...) instead of glob
for f in $(ls *.md); do
  echo "$f"
done

# LINT: S3 clobbering redirect (cat file | cmd > file)
cat /etc/hosts | sed 's/localhost/local/' > /tmp/unused-safety-fixture

# LINT: S4 while | read pipeline variable loss
count=0
echo "line1
line2" | while read -r line; do
  count=$((count + 1))
done
# count is still 0 here — classic subshell variable loss

# LINT: S5 unscoped IFS= without restore
IFS=,
read -r a b c <<< "1,2,3"
# IFS not restored; leaks into downstream commands

# LINT: S6 find | xargs without -print0 / -0
find /tmp -name '*.tmp' | xargs rm -f

# LINT: S7 cd X; Y without || guard
cd /nonexistent-safety-fixture-dir
rm -rf ./some-subdir

# LINT: S8 [[ ]] with > on numerics (string comparison, not numeric)
a=9
b=10
if [[ $a > $b ]]; then
  echo "9 > 10 (string comparison says yes)"
fi

# LINT: S9 mktemp before cleanup trap
tmpfile="$(mktemp)"
trap 'rm -f "${tmpfile}"' EXIT

# LINT: S10 function-local variable without `local`
do_thing() {
  result="leaked-to-global"
  echo "${result}"
}
do_thing
