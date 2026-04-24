#!/usr/bin/env bash
#
# check_location.sh — Deterministic Tier-1 location + extension check
# for Claude Code subagent definitions.
#
# Subagents must live under an agents/ directory (.claude/agents/,
# ~/.claude/agents/, or plugins/<plugin>/agents/) with a .md extension.
# Files outside these paths are invisible to the Claude Code router.
#
# Usage:
#   check_location.sh <path> [<path> ...]
#
# Paths may be .md files or directories (top-level only).
#
# Exit codes:
#   0   no FAIL findings
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly REQUIRED_CMDS=(basename find)

usage() {
  cat <<'EOF'
check_location.sh — Flag subagent files outside agents/ directories or with wrong extension.

Usage:
  check_location.sh <path> [<path> ...]

Arguments:
  <path>   A .md file or directory to scan (top-level files only).

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no FAIL findings
  1   one or more FAIL findings
  64  usage error
  69  missing dependency
EOF
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
      printf '%s: missing required command %q\n' "${PROGNAME}" "${cmd}" >&2
    done
    exit 69
  fi
}

fail_count=0

emit_fail() {
  fail_count=$((fail_count + 1))
  printf 'FAIL  %s — %s: %s\n' "$1" "$2" "$3"
  printf '  Recommendation: %s\n' "$4"
}

check_file() {
  local file="$1"

  # location-ext: must be .md
  case "${file}" in
    *.md) ;;
    *)
      emit_fail "${file}" "location-ext" \
        "extension is not .md" \
        "Rename to <name>.md — Claude Code only loads .md files from agents/ directories."
      ;;
  esac

  # location-dir: must contain an agents/ segment in its path
  case "${file}" in
    */.claude/agents/* | */agents/* | .claude/agents/* | agents/*)
      # OK — includes .claude/agents/, plugins/<plugin>/agents/, ~/.claude/agents/
      ;;
    *)
      local rec="Move to .claude/agents/ (project),"
      rec+=" ~/.claude/agents/ (user), or plugins/<plugin>/agents/"
      rec+=" (plugin scope)."
      emit_fail "${file}" "location-dir" \
        "file is not under an agents/ directory" "${rec}"
      ;;
  esac
}

check_path() {
  local target="$1"
  local file

  if [[ -f "${target}" ]]; then
    check_file "${target}"
  elif [[ -d "${target}" ]]; then
    while IFS= read -r file; do
      check_file "${file}"
    done < <(find "${target}" -maxdepth 1 -type f -name '*.md' 2>/dev/null)
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

  [[ "${fail_count}" -eq 0 ]] && exit 0 || exit 1
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
