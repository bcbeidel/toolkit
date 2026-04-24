#!/usr/bin/env bash
#
# check_structure.sh — Deterministic Tier-1 body-structure check for
# subagent definitions.
#
# Checks:
#   no-headings    body has no ## heading (WARN)
#   scope-absent   no heading matching Scope / In scope / Out of scope (INFO)
#
# Usage:
#   check_structure.sh <path> [<path> ...]

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk basename find)

usage() {
  cat <<'EOF'
check_structure.sh — Audit body heading structure.

Usage:
  check_structure.sh <path> [<path> ...]
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
  if [ "${#missing[@]}" -gt 0 ]; then
    for cmd in "${missing[@]}"; do
      printf '%s: missing required command %q\n' "${PROGNAME}" "${cmd}" >&2
    done
    exit 69
  fi
}

FAIL_COUNT=0

emit_warn() {
  printf 'WARN  %s — %s: %s\n' "$1" "$2" "$3"
  printf '  Recommendation: %s\n' "$4"
}

emit_info() {
  printf 'INFO  %s — %s: %s\n' "$1" "$2" "$3"
  printf '  Recommendation: %s\n' "$4"
}

# Walk headings in the body (post-frontmatter). Emits one heading line per match.
body_headings() {
  awk '
    /^---[[:space:]]*$/ {
      if (++fm_count == 1 && NR == 1) { in_fm = 1; next }
      if (in_fm && fm_count == 2)      { in_fm = 0; next }
    }
    in_fm { next }
    /^##[ \t]/ { print }
  ' "$1"
}

check_file() {
  local file="$1"
  case "${file}" in
    *.md) ;;
    *) return ;;
  esac

  local headings
  headings="$(body_headings "${file}")"

  if [ -z "${headings}" ]; then
    emit_warn "${file}" "no-headings" \
      "body has no ## headings" \
      "Add section headings (Scope, Process/Workflow, Output, Failure behavior). Pattern-match peer subagents for consistency."
    return
  fi

  # Scope detection — match any of: Scope, In scope, Out of scope, Scope & Constraints.
  if ! printf '%s\n' "${headings}" | awk '
    /^##[[:space:]]+(Scope|In scope|Out of scope)/ { found = 1 }
    /^##[[:space:]]+Scope[[:space:]]*&[[:space:]]*Constraints/ { found = 1 }
    END { exit (found ? 0 : 1) }
  '; then
    emit_info "${file}" "scope-absent" \
      "no Scope / In scope / Out of scope section" \
      "Add a ## Scope section naming what the agent handles and what it refuses."
  fi
}

check_path() {
  local target="$1"
  local file

  if [ -f "${target}" ]; then
    check_file "${target}"
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      check_file "${file}"
    done < <(find "${target}" -maxdepth 1 -type f -name '*.md' 2>/dev/null)
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

  [ "${FAIL_COUNT}" -eq 0 ] && exit 0 || exit 1
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
