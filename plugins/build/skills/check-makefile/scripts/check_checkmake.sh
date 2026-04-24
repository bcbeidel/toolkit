#!/usr/bin/env bash
#
# check_checkmake.sh — Tier-1 wrapper around `checkmake`.
#
# `checkmake` (https://github.com/mrtazz/checkmake) catches Make-idiom
# mistakes that regex checks miss: mixed phony / file-target
# prerequisites, expanded timestamps, oversize recipe bodies, and
# more. This wrapper invokes it against each target file and maps
# non-zero findings to WARN lines in the standard Tier-1 lint format.
#
# When `checkmake` is absent, emit a single INFO line and exit 0 —
# the tool is optional and degrades gracefully.
#
# Usage:
#   check_checkmake.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings (WARN/INFO exits 0)
#   1   one or more FAIL findings (not produced by this script)
#   64  usage error
#   69  missing required dependency (awk, find, basename)

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly REQUIRED_CMDS=(awk find basename)

usage() {
  cat <<'EOF'
check_checkmake.sh — Wrap `checkmake` for Tier-1 Makefile audits.

Usage:
  check_checkmake.sh <path> [<path> ...]

Arguments:
  <path>   A Makefile / GNUmakefile / *.mk file or directory (top-level).

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no FAIL findings (INFO on missing `checkmake` exits 0)
  1   one or more FAIL findings (not produced by this script)
  64  usage error
  69  missing required dependency
EOF
}

install_hint() {
  case "${1}" in
    awk | find | basename) printf 'should be preinstalled on any POSIX system' ;;
    checkmake)
      printf '`brew install checkmake` (macOS) '
      printf 'or `go install github.com/mrtazz/checkmake@latest`'
      ;;
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

emit_tool_missing() {
  printf 'INFO  — checkmake: tool not installed; coverage reduced\n'
  printf '  Recommendation: Install `checkmake` to extend Tier-1 '
  printf 'coverage (%s).\n' "$(install_hint checkmake)"
}

check_file() {
  local file="$1"
  local output
  if ! output="$(checkmake "${file}" 2>&1)"; then
    # checkmake emits lines like "rulename: detail"; convert each to a WARN.
    while IFS= read -r line; do
      [[ -z "${line}" ]] && continue
      # Strip any leading filename prefix some builds add.
      local stripped="${line#"${file}":}"
      printf 'WARN  %s — checkmake: %s\n' "${file}" "${stripped}"
      printf '  Recommendation: See `checkmake --list-rules` for the '
      printf 'rule reference; fixes vary by rule (MIXDEPS, '
      printf 'TIMESTAMP_EXPANDED, MIN_PHONY, MAX_BODY_LENGTH).\n'
    done <<<"${output}"
  fi
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

  if ! command -v checkmake >/dev/null 2>&1; then
    emit_tool_missing
    exit 0
  fi

  local target
  for target in "$@"; do
    check_path "${target}" || exit "$?"
  done

  exit 0
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
