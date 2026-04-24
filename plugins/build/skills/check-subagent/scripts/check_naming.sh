#!/usr/bin/env bash
#
# check_naming.sh — Deterministic Tier-1 naming checks for subagent
# definitions.
#
# Checks:
#   name-kebab         `name` matches ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ (WARN)
#   name-stem-match    filename stem equals `name` (FAIL)
#   generic-filename   filename is a generic placeholder (HINT)
#
# Usage:
#   check_naming.sh <path> [<path> ...]

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly REQUIRED_CMDS=(awk basename find)

usage() {
  cat <<'EOF'
check_naming.sh — Audit subagent name field and filename.

Usage:
  check_naming.sh <path> [<path> ...]
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

emit_hint() {
  printf 'HINT  %s — %s: %s\n' "$1" "$2" "$3"
  printf '  Recommendation: %s\n' "$4"
}

extract_name() {
  awk '
    /^---[[:space:]]*$/ {
      if (++count == 1) { inside = 1; next }
      if (count == 2)   { exit }
    }
    inside && /^name:[[:space:]]*/ {
      val = $0
      sub(/^name:[[:space:]]*/, "", val)
      if (val ~ /^".*"$/) { val = substr(val, 2, length(val) - 2) }
      else if (val ~ /^'\''.*'\''$/) { val = substr(val, 2, length(val) - 2) }
      print val
      exit
    }
  ' "$1"
}

is_generic_stem() {
  case "$1" in
    agent | agents | helper | default | subagent | test | example) return 0 ;;
  esac
  return 1
}

check_file() {
  local file="$1"
  case "${file}" in
    *.md) ;;
    *) return ;;
  esac

  local stem
  stem="$(basename "${file}" .md)"

  if is_generic_stem "${stem}"; then
    local rec="Rename to describe the agent's primary role"
    rec+=" (e.g., typescript-linter.md, migration-reviewer.md)."
    emit_hint "${file}" "generic-filename" \
      "filename stem '${stem}' is a generic placeholder" "${rec}"
  fi

  local name
  name="$(extract_name "${file}")"

  # name-kebab — only check when name is present (check_frontmatter handles missing)
  if [[ -n "${name}" ]]; then
    if ! printf '%s' "${name}" | awk '
      /^[a-z][a-z0-9]*(-[a-z0-9]+)*$/ { exit 0 }
      { exit 1 }
    '; then
      local rec="Convert to kebab-case (lowercase + hyphens):"
      rec+=" e.g., typescript-linter, not TypeScriptLinter."
      emit_warn "${file}" "name-kebab" \
        "name '${name}' is not kebab-case" "${rec}"
    fi

    # name-stem-match
    if [[ "${name}" != "${stem}" ]]; then
      emit_fail "${file}" "name-stem-match" \
        "filename stem '${stem}' does not equal name '${name}'" \
        "Rename the file to ${name}.md, or change name: to match the filename stem."
    fi
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
