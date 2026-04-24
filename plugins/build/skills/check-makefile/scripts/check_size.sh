#!/usr/bin/env bash
#
# check_size.sh — Deterministic Tier-1 size + line-length check for
# Makefiles.
#
# Makefiles rot fast past ~300 non-blank lines — navigation suffers
# and the single-file advantage is lost. This check emits a WARN at
# the threshold. Per-line length is also flagged at >120 chars
# (readability in code review).
#
# Usage:
#   check_size.sh <path> [<path> ...]
#
# Paths may be Makefile / GNUmakefile / *.mk files or directories
# (top-level only).
#
# Exit codes:
#   0   no FAIL findings (WARN exits 0 per the Tier-1 contract)
#   1   one or more FAIL findings (not produced by this script)
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename, head

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly MAX_NON_BLANK_LINES=300
readonly MAX_LINE_LENGTH=120

readonly REQUIRED_CMDS=(awk find basename head)

usage() {
  cat <<'EOF'
check_size.sh — Flag Makefiles exceeding size or line-length thresholds.

Usage:
  check_size.sh <path> [<path> ...]

Arguments:
  <path>   A Makefile / GNUmakefile / *.mk file or directory (top-level).

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
    awk | find | basename | head) printf 'should be preinstalled on any POSIX system' ;;
    *) printf 'see your package manager' ;;
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
  if [[ "${#missing[@]}" -gt 0 ]]; then
    for cmd in "${missing[@]}"; do
      printf '%s: missing required command %q. Install: %s\n' \
        "${PROGNAME}" "${cmd}" "$(install_hint "${cmd}")" >&2
    done
    exit 69
  fi
}

is_makefile() {
  local file="$1"
  local base
  base="$(basename "${file}")"
  case "${base}" in
    Makefile | GNUmakefile) return 0 ;;
    *.mk) return 0 ;;
  esac
  return 1
}

non_blank_count() {
  awk 'NF { count++ } END { print count + 0 }' "$1"
}

check_file() {
  local file="$1"
  local count
  count="$(non_blank_count "${file}")"
  if [[ "${count}" -gt "${MAX_NON_BLANK_LINES}" ]]; then
    printf 'WARN  %s — size: %s non-blank lines (threshold %s)\n' \
      "${file}" "${count}" "${MAX_NON_BLANK_LINES}"
    printf '  Recommendation: Split cohesive sections into included '
    printf '`*.mk` files (e.g., mk/build.mk, mk/test.mk) and include '
    printf 'them from the top-level Makefile.\n'
  fi

  # Per-line length WARN — emit at most 3 per file to avoid noise.
  local emitted=0
  while IFS=: read -r lineno length; do
    if [[ "${emitted}" -ge 3 ]]; then
      break
    fi
    printf 'WARN  %s — line-length: line %s is %s chars (threshold %s)\n' \
      "${file}" "${lineno}" "${length}" "${MAX_LINE_LENGTH}"
    printf '  Recommendation: Break with `\\` continuation or extract the '
    printf 'recipe body into `scripts/<name>.sh`.\n'
    emitted=$((emitted + 1))
  done < <(awk -v max="${MAX_LINE_LENGTH}" '
    length($0) > max { printf "%d:%d\n", NR, length($0) }
  ' "${file}")
}

check_path() {
  local target="$1"
  local file

  if [[ -f "${target}" ]]; then
    if is_makefile "${target}"; then
      check_file "${target}"
    fi
  elif [[ -d "${target}" ]]; then
    while IFS= read -r file; do
      if is_makefile "${file}"; then
        check_file "${file}"
      fi
    done < <(
      find "${target}" -maxdepth 1 -type f \
        \( -name 'Makefile' -o -name 'GNUmakefile' -o -name '*.mk' \) 2>/dev/null
    )
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
}

main() {
  if [[ "$#" -eq 0 ]]; then
    usage >&2
    exit 64
  fi

  case "${1:-}" in
    -h | --help)
      usage
      exit 0
      ;;
  esac

  preflight

  local target
  for target in "$@"; do
    check_path "${target}" || exit "$?"
  done

  exit 0
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
