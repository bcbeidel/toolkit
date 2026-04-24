#!/usr/bin/env bash
#
# check_tools.sh — Deterministic Tier-1 tool-allowlist checks for
# subagent definitions.
#
# Checks:
#   tools-omitted         tools key absent — spec defaults to full grant (WARN)
#   tools-wildcard        tools contains *, all, or all_tools (FAIL)
#   agent-listed          Agent listed in tools for a subagent-scope definition (WARN)
#   parallel-write-risk   background: true + Write/Edit without isolation: worktree (WARN)
#
# Usage:
#   check_tools.sh <path> [<path> ...]

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly REQUIRED_CMDS=(awk basename find)

usage() {
  cat <<'EOF'
check_tools.sh — Audit subagent tools allowlist hygiene.

Usage:
  check_tools.sh <path> [<path> ...]
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

extract_frontmatter() {
  awk '
    /^---[[:space:]]*$/ {
      if (++count == 1) { inside = 1; next }
      if (count == 2)   { exit }
    }
    inside { print }
  ' "$1"
}

# Emit tool-list items one per line. Handles block-list and flow-list forms.
tools_list() {
  printf '%s\n' "$1" | awk '
    /^tools:/ {
      if ($0 ~ /\[/) {
        line = $0
        sub(/^tools:[[:space:]]*\[/, "", line)
        sub(/\].*$/, "", line)
        n = split(line, items, /,/)
        for (i = 1; i <= n; i++) {
          gsub(/^[[:space:]]+|[[:space:]]+$/, "", items[i])
          gsub(/^"|"$|^'\''|'\''$/, "", items[i])
          if (items[i] != "") print items[i]
        }
      } else {
        in_tools = 1
      }
      next
    }
    in_tools && /^[^ \t-]/ { in_tools = 0 }
    in_tools && /^[[:space:]]*-[[:space:]]/ {
      item = $0
      sub(/^[[:space:]]*-[[:space:]]*/, "", item)
      gsub(/^"|"$|^'\''|'\''$/, "", item)
      gsub(/[[:space:]]+$/, "", item)
      if (item != "") print item
    }
  '
}

has_key() {
  printf '%s\n' "$1" | awk -v k="$2" '
    $0 ~ "^" k ":" { found = 1 }
    END { exit (found ? 0 : 1) }
  '
}

# Top-level scalar value; empty if missing. Simpler than get_scalar in
# check_frontmatter.sh — tools.sh only needs scalar truthiness for
# background / isolation.
get_scalar_value() {
  printf '%s\n' "$1" | awk -v k="$2" '
    $0 ~ "^" k ":[[:space:]]*" {
      val = $0
      sub("^" k ":[[:space:]]*", "", val)
      gsub(/^"|"$|^'\''|'\''$/, "", val)
      gsub(/[[:space:]]+$/, "", val)
      print val
      exit
    }
  '
}

check_file() {
  local file="$1"
  case "${file}" in
    *.md) ;;
    *) return ;;
  esac

  local fm
  fm="$(extract_frontmatter "${file}")"
  [[ -z "${fm}" ]] && return

  # tools-omitted
  if ! has_key "${fm}" "tools"; then
    emit_warn "${file}" "tools-omitted" \
      "tools key absent — Claude Code grants the full tool set by default" \
      "Add an explicit tools list declaring the minimum set the workflow needs."
    return
  fi

  local tools
  tools="$(tools_list "${fm}")"

  # tools-wildcard
  local item
  while IFS= read -r item; do
    [[ -z "${item}" ]] && continue
    case "${item}" in
      '*' | all | all_tools | ALL)
        emit_fail "${file}" "tools-wildcard" \
          "tools contains wildcard entry '${item}'" \
          "Replace wildcard with an enumerated list of the tools the workflow actually uses."
        ;;
    esac
  done <<<"${tools}"

  # agent-listed — flag for all subagent-scope definitions. The
  # platform filters Agent out at invocation; listing it is a no-op.
  # The caveat about main-thread `claude --agent <name>` runs is noted
  # in the recommendation text but cannot be detected from the file
  # alone.
  while IFS= read -r item; do
    if [[ "${item}" = "Agent" ]]; then
      local msg="Agent listed in tools — filtered at platform"
      msg+=" level for subagents, has no effect"
      local rec="Remove Agent from tools. (If this definition"
      rec+=" runs as main thread via 'claude --agent', move it"
      rec+=" out of agents/.)"
      emit_warn "${file}" "agent-listed" "${msg}" "${rec}"
    fi
  done <<<"${tools}"

  # parallel-write-risk
  local background isolation
  background="$(get_scalar_value "${fm}" "background")"
  isolation="$(get_scalar_value "${fm}" "isolation")"
  if [[ "${background}" = "true" ]]; then
    local has_write=0
    while IFS= read -r item; do
      case "${item}" in
        Write | Edit) has_write=1 ;;
      esac
    done <<<"${tools}"
    if [[ "${has_write}" -eq 1 ]] && [[ "${isolation}" != "worktree" ]]; then
      emit_warn "${file}" "parallel-write-risk" \
        "background: true with Write/Edit granted but isolation: worktree absent" \
        "Add 'isolation: worktree' — parallel writes on shared files conflict without it."
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
