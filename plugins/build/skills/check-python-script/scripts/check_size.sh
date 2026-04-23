#!/usr/bin/env bash
#
# check_size.sh — Deterministic Tier-1 size check for Python scripts.
#
# Single-file scripts past ~500 non-blank lines are an anti-pattern —
# the convention is to graduate to a proper package. This check emits
# a WARN at the threshold; no FAIL, since line count is a heuristic.
#
# Usage:
#   check_size.sh <path> [<path> ...]
#
# Paths may be .py files or directories (top-level .py only; scripts
# are single-file by definition — no recursion into subpackages).
#
# Exit codes:
#   0   no FAIL findings (WARN findings exit 0 per the Tier-1 contract)
#   1   one or more FAIL findings (not produced by this script)
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename, wc

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

# Threshold lives here so it is trivial to locate and adjust.
MAX_NON_BLANK_LINES=500

REQUIRED_CMDS=(awk find basename wc)

usage() {
  cat <<'EOF'
check_size.sh — Flag Python scripts exceeding the size threshold.

Usage:
  check_size.sh <path> [<path> ...]

Arguments:
  <path>   A .py file or directory to scan (top-level .py only).

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no FAIL findings
  1   one or more FAIL findings (not produced by this script)
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    awk|find|basename|wc) printf 'should be preinstalled on any POSIX system' ;;
    *)                    printf 'see your package manager' ;;
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

# Count non-blank lines — blank = empty or whitespace-only.
non_blank_count() {
  awk 'NF { count++ } END { print count + 0 }' "$1"
}

check_file() {
  local file="$1"
  local count
  count="$(non_blank_count "${file}")"
  if [ "${count}" -gt "${MAX_NON_BLANK_LINES}" ]; then
    printf 'WARN  %s — size: %s non-blank lines (threshold %s)\n' \
      "${file}" "${count}" "${MAX_NON_BLANK_LINES}"
    printf '  Recommendation: Extract cohesive sections into helper '
    printf 'functions, or convert to a package (pyproject.toml + src/<pkg>/).\n'
  fi
}

check_path() {
  local target="$1"
  local file

  if [ -f "${target}" ]; then
    case "${target}" in
      *.py) check_file "${target}" ;;
    esac
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      check_file "${file}"
    done < <(find "${target}" -maxdepth 1 -type f -name '*.py' 2>/dev/null)
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
  for target in "$@"; do
    check_path "${target}" || exit "$?"
  done

  exit 0
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
