#!/usr/bin/env bash
# LINT: D1 missing top-of-file header
# (No structured purpose/usage/exit-codes/dependencies block after
# the shebang — just this comment, which does not satisfy D1.)

set -Eeuo pipefail

PROGNAME="some-other-name"
# LINT: D4 filename ≠ PROGNAME drift
# (File is documentation-lints.sh; PROGNAME is hardcoded to
# "some-other-name".)

usage() {
  # LINT: D5 unquoted heredoc in help / usage function
  cat <<EOF
${PROGNAME} — usage
  (this heredoc performs variable expansion because it is not quoted;
  compare with <<'EOF' to prevent that.)
EOF
}

fetch_data() {
  # LINT: D3 bare TODO without attribution
  # TODO: handle the retry case
  :
}

if ! curl -fsS https://example.invalid/ >/dev/null; then
  # LINT: D6 error message not going to stderr
  echo "Error: fetch failed"
  # LINT: D2 undocumented non-zero exit code
  exit 42
fi

usage
fetch_data
