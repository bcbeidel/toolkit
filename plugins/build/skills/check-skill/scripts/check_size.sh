#!/usr/bin/env bash
#
# check_size.sh — Deterministic Tier-1 size checks for Claude Code
# SKILL.md files: non-blank line count and maximum line length.
#
# Line count:   non-blank line count is WARN at ≥300, FAIL at ≥400.
# Line length:  any line (outside fenced code blocks and bare URLs)
#               exceeding 120 chars emits a WARN.
#
# Usage:
#   check_size.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings
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
WARN_LINES=300
FAIL_LINES=400
MAX_LINE_LEN=120

usage() {
  cat <<EOF
check_size.sh — Size checks for Claude Code SKILL.md files.

Usage:
  check_size.sh <path> [<path> ...]

Checks:
  Line count   WARN at ≥${WARN_LINES} non-blank lines, FAIL at ≥${FAIL_LINES}
  Line length  WARN on any line > ${MAX_LINE_LEN} chars (fenced blocks and
               bare URLs are excluded)

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

count_non_blank() {
  awk 'NF { n++ } END { print n + 0 }' "$1"
}

check_line_count() {
  local file="$1"
  local n
  n="$(count_non_blank "${file}")"
  if [ "${n}" -ge "${FAIL_LINES}" ]; then
    emit_fail "${file}" "Body length" \
      "${n} non-blank lines exceeds hard ceiling of ${FAIL_LINES}" \
      "Move reference material, long examples, or complex scripts into sibling files"
    return 1
  elif [ "${n}" -ge "${WARN_LINES}" ]; then
    emit_warn "${file}" "Body length" \
      "${n} non-blank lines exceeds guidance ${WARN_LINES}" \
      "Consider moving long embedded content into sibling references/ or scripts/ files"
  fi
  return 0
}

check_line_length() {
  local file="$1"
  # Emit one WARN per overlong line, skipping fenced blocks and
  # single-token lines that are bare URLs.
  local lines
  lines="$(awk -v max="${MAX_LINE_LEN}" '
    BEGIN { in_fence = 0 }
    {
      if ($0 ~ /^[[:space:]]*```/) { in_fence = !in_fence; next }
      if ($0 ~ /^[[:space:]]*~~~/) { in_fence = !in_fence; next }
      if (in_fence) { next }
      # Skip lines that are just a bare URL (one token, starts with http).
      if (NF == 1 && $1 ~ /^https?:\/\//) { next }
      if (length($0) > max) {
        printf "%d\t%d\n", NR, length($0)
      }
    }
  ' "${file}")"
  [ -n "${lines}" ] || return 0
  local row line_no len
  while IFS= read -r row; do
    line_no="${row%%$'\t'*}"
    len="${row##*$'\t'}"
    emit_warn "${file}" "Line length" \
      "line ${line_no} is ${len} chars (> ${MAX_LINE_LEN})" \
      "Wrap the line at a natural clause boundary"
  done <<<"${lines}"
  return 0
}

check_file() {
  local file="$1"
  local fail=0
  check_line_count  "${file}" || fail=1
  check_line_length "${file}"  # WARN only
  return "${fail}"
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
    done < <(
      find "${target}" -type f -name 'SKILL.md' \
        -not -path '*/_shared/*' \
        2>/dev/null
    )
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
  local any=0 target
  for target in "$@"; do
    check_path "${target}" || any=1
  done
  exit "${any}"
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
