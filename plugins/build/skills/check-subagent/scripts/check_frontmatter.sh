#!/usr/bin/env bash
#
# check_frontmatter.sh — Deterministic Tier-1 frontmatter checks for
# Claude Code subagent definitions.
#
# Checks:
#   fm-delimiter         file begins with a ---...--- YAML block
#   fm-name              `name` key present and non-empty
#   fm-description       `description` key present and non-empty
#   fm-description-length  `description` ≤1,024 characters
#   plugin-noop          plugin-scoped files do not set permissionMode / hooks / mcpServers
#   memory-expansion     memory: set alongside narrow tools omitting Read/Write/Edit
#
# Usage:
#   check_frontmatter.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings (WARN ok)
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk basename find)

usage() {
  cat <<'EOF'
check_frontmatter.sh — Audit subagent frontmatter shape.

Usage:
  check_frontmatter.sh <path> [<path> ...]
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

emit_fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  printf 'FAIL  %s — %s: %s\n' "$1" "$2" "$3"
  printf '  Recommendation: %s\n' "$4"
}

emit_warn() {
  printf 'WARN  %s — %s: %s\n' "$1" "$2" "$3"
  printf '  Recommendation: %s\n' "$4"
}

# Extract the frontmatter block (between the first pair of --- lines).
# Emits nothing if no block found.
extract_frontmatter() {
  awk '
    /^---[[:space:]]*$/ {
      if (++count == 1) { inside = 1; next }
      if (count == 2)   { exit }
    }
    inside { print }
  ' "$1"
}

# Get a top-level scalar value for `key`. Handles:
#   key: value
#   key: "value"
#   key: 'value'
#   key: >           (folded scalar, next indented lines concatenated with spaces)
#     continuation
#   key: |           (literal scalar, next indented lines kept as-is)
# Returns empty string if key missing.
get_scalar() {
  local fm="$1"
  local key="$2"
  printf '%s\n' "${fm}" | awk -v k="${key}" '
    BEGIN { val = ""; folded = 0; literal = 0 }
    # Stop folded/literal collection on a non-indented line
    (folded || literal) && /^[^ \t]/ { folded = 0; literal = 0 }
    # Continuation line for folded/literal
    (folded || literal) && /^[ \t]+/ {
      line = $0
      sub(/^[ \t]+/, "", line)
      if (val == "") { val = line } else { val = val (folded ? " " : "\n") line }
      next
    }
    # Match `key:` at column 0
    $0 ~ "^" k ":[ \t]*" {
      rest = $0
      sub("^" k ":[ \t]*", "", rest)
      if (rest == ">" || rest == ">-") { folded = 1; next }
      if (rest == "|" || rest == "|-") { literal = 1; next }
      # Strip surrounding quotes if present
      if (rest ~ /^".*"$/) { rest = substr(rest, 2, length(rest) - 2) }
      else if (rest ~ /^'\''.*'\''$/) { rest = substr(rest, 2, length(rest) - 2) }
      val = rest
    }
    END { print val }
  '
}

# Check whether a top-level scalar/block key is present in the frontmatter
# (even if its value is empty). Used for plugin-noop and memory detection.
has_key() {
  local fm="$1"
  local key="$2"
  printf '%s\n' "${fm}" | awk -v k="${key}" '
    $0 ~ "^" k ":" { found = 1 }
    END { exit (found ? 0 : 1) }
  '
}

# Return 0 if tools: list contains the given tool name, 1 otherwise.
# Supports block-list (- Tool) and flow-list ([Tool, Tool]) forms.
tools_contains() {
  local fm="$1"
  local needle="$2"
  printf '%s\n' "${fm}" | awk -v needle="${needle}" '
    BEGIN { in_tools = 0; hit = 0 }
    /^tools:/ {
      # Flow form on same line: tools: [A, B]
      if ($0 ~ /\[/) {
        line = $0
        sub(/^tools:[ \t]*\[/, "", line)
        sub(/\].*$/, "", line)
        n = split(line, items, /,/)
        for (i = 1; i <= n; i++) {
          gsub(/^[ \t]+|[ \t]+$/, "", items[i])
          gsub(/^"|"$|^'\''|'\''$/, "", items[i])
          if (items[i] == needle) { hit = 1 }
        }
        in_tools = 0
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
      if (item == needle) { hit = 1 }
    }
    END { exit (hit ? 0 : 1) }
  '
}

# Is this path plugin-scoped (under plugins/<plugin>/agents/)?
is_plugin_path() {
  case "$1" in
    *plugins/*/agents/*) return 0 ;;
  esac
  return 1
}

check_file() {
  local file="$1"

  # Must be an .md file to have frontmatter
  case "${file}" in
    *.md) ;;
    *) return ;;
  esac

  local fm
  fm="$(extract_frontmatter "${file}")"

  if [ -z "${fm}" ]; then
    emit_fail "${file}" "fm-delimiter" \
      "no ---delimited YAML frontmatter block at file head" \
      "Add a frontmatter block as the first lines of the file (see subagents-best-practices.md Anatomy)."
    return
  fi

  local name description
  name="$(get_scalar "${fm}" "name")"
  description="$(get_scalar "${fm}" "description")"

  # fm-name
  if [ -z "${name}" ]; then
    emit_fail "${file}" "fm-name" \
      "name key missing or empty" \
      "Add 'name: <kebab-case-slug>' to the frontmatter, matching the filename stem."
  fi

  # fm-description
  if [ -z "${description}" ]; then
    emit_fail "${file}" "fm-description" \
      "description key missing or empty" \
      "Add a routing-rule description: verb-phrase + trigger conditions + exclusion + returns."
  else
    # fm-description-length
    local dlen="${#description}"
    if [ "${dlen}" -gt 1024 ]; then
      emit_fail "${file}" "fm-description-length" \
        "description is ${dlen} characters (>1,024 — Claude Code silently truncates)" \
        "Shorten to <=1,024 chars; move overflow detail into body sections (Scope, Workflow)."
    fi
  fi

  # plugin-noop: plugin-scoped files setting fields the runtime ignores
  if is_plugin_path "${file}"; then
    local noop_key
    for noop_key in permissionMode hooks mcpServers; do
      if has_key "${fm}" "${noop_key}"; then
        emit_warn "${file}" "plugin-noop" \
          "${noop_key} set in a plugin-scoped definition — silently ignored by Claude Code" \
          "Remove ${noop_key}; plugin subagents have this field stripped at load time."
      fi
    done
  fi

  # memory-expansion: memory: set + tools: set + tools omits any of Read/Write/Edit
  if has_key "${fm}" "memory" && has_key "${fm}" "tools"; then
    local missing=()
    local t
    for t in Read Write Edit; do
      if ! tools_contains "${fm}" "${t}"; then
        missing+=("${t}")
      fi
    done
    if [ "${#missing[@]}" -gt 0 ]; then
      emit_warn "${file}" "memory-expansion" \
        "memory: enabled — runtime auto-grants Read/Write/Edit; tools list is missing: ${missing[*]}" \
        "Either remove memory: (if not needed), or add Read/Write/Edit to tools to match runtime behavior."
    fi
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
