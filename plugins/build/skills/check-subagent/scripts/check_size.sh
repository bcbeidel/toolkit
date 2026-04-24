#!/usr/bin/env bash
#
# check_size.sh — Deterministic Tier-1 body-size check for subagent
# definitions.
#
# Measures the character count of the markdown body (everything after
# the frontmatter block). Soft WARN at ≥6,000 chars (~1,500 tokens);
# hard FAIL at ≥12,000 chars (~3,000 tokens). Thresholds derived from
# the ensemble synthesis.
#
# Usage:
#   check_size.sh <path> [<path> ...]

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly SOFT_THRESHOLD=6000
readonly HARD_THRESHOLD=12000

readonly REQUIRED_CMDS=(awk basename find wc)

usage() {
  cat <<'EOF'
check_size.sh — Flag subagent definitions with oversized prompt bodies.

Usage:
  check_size.sh <path> [<path> ...]
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

emit_warn() {
  printf 'WARN  %s — %s: %s\n' "$1" "$2" "$3"
  printf '  Recommendation: %s\n' "$4"
}

# Print the body (everything after the closing --- of frontmatter).
# If no frontmatter, prints the entire file.
body_text() {
  awk '
    BEGIN { in_body = 0; fm_count = 0 }
    in_body { print; next }
    /^---[[:space:]]*$/ {
      fm_count++
      if (NR == 1 && fm_count == 1) { in_fm = 1; next }
      if (in_fm && fm_count == 2)   { in_fm = 0; in_body = 1; next }
    }
    !in_fm && NR == 1 {
      # No leading ---; whole file is body
      in_body = 1
      print
    }
    in_fm { next }
  ' "$1"
}

check_file() {
  local file="$1"
  case "${file}" in
    *.md) ;;
    *) return ;;
  esac

  local body_chars
  body_chars="$(body_text "${file}" | wc -c | awk '{print $1}')"

  local rec_hard="Split the workflow — at this size the prompt competes"
  rec_hard+=" with task context. Consider two subagents or moving"
  rec_hard+=" reference material into a linked file."

  local rec_soft="Trim the body — target <=1,500 tokens. Remove"
  rec_soft+=" expansions, collapse redundant examples, move reference"
  rec_soft+=" material into references/."

  if [[ "${body_chars}" -ge "${HARD_THRESHOLD}" ]]; then
    emit_fail "${file}" "size-hard" \
      "body is ${body_chars} chars (>=${HARD_THRESHOLD}, ~3,000 tokens)" \
      "${rec_hard}"
  elif [[ "${body_chars}" -ge "${SOFT_THRESHOLD}" ]]; then
    emit_warn "${file}" "size-soft" \
      "body is ${body_chars} chars (>=${SOFT_THRESHOLD}, ~1,500 tokens)" \
      "${rec_soft}"
  fi
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
