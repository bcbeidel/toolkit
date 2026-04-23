#!/usr/bin/env bash
#
# emit_shape_hints.sh — Keyword sniff for Claude Code rule files.
#
# Emits informational HINT lines (not findings) that /build:check-rule
# Tier-2 uses as context for judgment-based rule detection.
#
# Keywords detected (case-insensitive, body only — frontmatter ignored):
#   compliant       a compliant example or section is present
#   non-compliant   a non-compliant example or section is present
#   violation       enforcement language
#   exception       named exception policy
#   failure         failure-cost discussion
#   code-blocks     fenced code blocks (```)
#
# Usage:
#   emit_shape_hints.sh <path> [<path> ...]
#
# Paths may be files or directories (recursively scanned for *.md).
#
# Output format:
#   HINT  <path> — shape hints: compliant, non-compliant, exception, code-blocks
#
# Files with no signals emit nothing — the absence of hints is itself
# informative to the Tier-2 evaluator (no judgment-based shape detected).
#
# Exit codes:
#   0   always (hints never fail the build)
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename)

usage() {
  cat <<'EOF'
emit_shape_hints.sh — Keyword sniff for Claude Code rule files.

Usage:
  emit_shape_hints.sh <path> [<path> ...]

Output:
  HINT  <path> — shape hints: <comma-separated signals>

Signals:
  compliant, non-compliant, violation, exception, failure, code-blocks

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   always (hints never fail the build)
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    awk|find|basename) printf 'should be preinstalled on any POSIX system' ;;
    *)                 printf 'see your package manager' ;;
  esac
}

preflight() {
  local missing=()
  local cmd
  for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
      missing+=("${cmd}")
    fi
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    for cmd in "${missing[@]}"; do
      printf '%s: missing required command %q. Install: %s\n' \
        "${PROGNAME}" "${cmd}" "$(install_hint "${cmd}")" >&2
    done
    exit 69
  fi
}

scan_file() {
  local file="$1"
  awk '
    BEGIN { in_fm = 0; comp = 0; noncomp = 0; vio = 0; exc = 0; fail = 0; cb = 0 }

    NR == 1 && /^---$/ { in_fm = 1; next }
    in_fm && /^---$/ { in_fm = 0; next }
    in_fm { next }

    {
      line = tolower($0)
      if (line ~ /non-?compliant|non compliant/) noncomp = 1
      # "compliant" alone: strip non-compliant variants, then check.
      temp = line
      gsub(/non-?compliant|non compliant/, "", temp)
      if (temp ~ /compliant/) comp = 1
      if (line ~ /violation/) vio = 1
      if (line ~ /exception/) exc = 1
      if (line ~ /failure/)   fail = 1
    }
    /^```/ { cb = 1 }

    END {
      hints = ""
      if (comp)    hints = (hints == "" ? "compliant"     : hints ", compliant")
      if (noncomp) hints = (hints == "" ? "non-compliant" : hints ", non-compliant")
      if (vio)     hints = (hints == "" ? "violation"     : hints ", violation")
      if (exc)     hints = (hints == "" ? "exception"     : hints ", exception")
      if (fail)    hints = (hints == "" ? "failure"       : hints ", failure")
      if (cb)      hints = (hints == "" ? "code-blocks"   : hints ", code-blocks")
      if (hints != "") {
        printf "HINT  %s — shape hints: %s\n", FILENAME, hints
      }
    }
  ' "${file}" 2>/dev/null || true
}

scan_path() {
  local target="$1"
  local file

  if [ -f "${target}" ]; then
    scan_file "${target}"
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      scan_file "${file}"
    done < <(find "${target}" -type f -name '*.md' 2>/dev/null)
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
}

main() {
  if [ "$#" -eq 0 ]; then
    usage >&2
    exit 64
  fi

  case "${1:-}" in
    -h|--help) usage; exit 0 ;;
  esac

  preflight

  local target
  local arg_err=0
  for target in "$@"; do
    scan_path "${target}" || arg_err=1
  done

  if [ "${arg_err}" -ne 0 ]; then
    exit 64
  fi
  exit 0
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
