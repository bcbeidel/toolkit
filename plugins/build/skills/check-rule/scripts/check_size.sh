#!/usr/bin/env bash
#
# check_size.sh — Deterministic Tier-1 file-size check for Claude Code
# rule files. Counts non-blank lines; emits WARN at >200 and FAIL at >500.
#
# A "non-blank" line contains at least one non-whitespace character.
# Blank lines are excluded so formatting padding doesn't push a file
# past threshold.
#
# Usage:
#   check_size.sh <path> [<path> ...]
#
# Paths may be files or directories (recursively scanned for *.md).
#
# Exit codes:
#   0   no FAIL findings (WARN-only runs return 0)
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename)

WARN_THRESHOLD=200
FAIL_THRESHOLD=500

usage() {
  cat <<'EOF'
check_size.sh — File-size check for Claude Code rule files.

Usage:
  check_size.sh <path> [<path> ...]

Thresholds:
  WARN  > 200 non-blank lines  ("prefer short" soft cap)
  FAIL  > 500 non-blank lines  (document-not-rule hard cap)

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no FAIL findings
  1   one or more FAIL findings
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

emit_fail() {
  local path="$1" check="$2" detail="$3" rec="$4"
  printf 'FAIL  %s — %s: %s\n' "${path}" "${check}" "${detail}"
  printf '  Recommendation: %s\n' "${rec}"
}

emit_warn() {
  local path="$1" check="$2" detail="$3" rec="$4"
  printf 'WARN  %s — %s: %s\n' "${path}" "${check}" "${detail}"
  printf '  Recommendation: %s\n' "${rec}"
}

count_nonblank() {
  local file="$1"
  awk 'NF > 0 { n++ } END { print n+0 }' "${file}" 2>/dev/null || printf '0'
}

check_file() {
  local file="$1"
  local count
  count="$(count_nonblank "${file}")"

  if [ "${count}" -gt "${FAIL_THRESHOLD}" ]; then
    emit_fail "${file}" "file size" \
      "${count} non-blank lines exceeds ${FAIL_THRESHOLD}-line hard cap" \
      "Split into rules and move long-form rationale to .context/<name>.md or a CLAUDE.md section"
    return 1
  elif [ "${count}" -gt "${WARN_THRESHOLD}" ]; then
    emit_warn "${file}" "file size" \
      "${count} non-blank lines exceeds ${WARN_THRESHOLD}-line soft cap" \
      "Split into topic files (e.g., testing-unit.md + testing-integration.md)"
  fi
  return 0
}

check_path() {
  local target="$1"
  local any=0
  local file

  if [ -f "${target}" ]; then
    check_file "${target}" || any=1
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      check_file "${file}" || any=1
    done < <(find "${target}" -type f -name '*.md' 2>/dev/null)
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
  return "${any}"
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

  local any=0
  local target
  for target in "$@"; do
    check_path "${target}" || any=1
  done

  exit "${any}"
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
