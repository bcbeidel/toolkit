#!/usr/bin/env bash
#
# check_structure.sh — Deterministic Tier-1 structure checks for
# Claude Code SKILL.md files: required H2 sections, Steps as a
# numbered ordered list, Examples containing a fenced code block.
#
# Required sections: `## When to use`, `## Prerequisites`, `## Steps`,
#                    `## Failure modes`, `## Examples` — all five present.
# Steps shape:       `## Steps` is a Markdown ordered list starting at
#                    1 with sequential (1..N) increments.
# Examples content:  `## Examples` contains at least one fenced code
#                    block (``` or ~~~).
#
# Usage:
#   check_structure.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename, head

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename head)
REQUIRED_SECTIONS=("When to use" "Prerequisites" "Steps" "Failure modes" "Examples")

usage() {
  cat <<'EOF'
check_structure.sh — Structure checks for Claude Code SKILL.md files.

Usage:
  check_structure.sh <path> [<path> ...]

Checks:
  Required sections  `## When to use` / `## Prerequisites` / `## Steps`
                     / `## Failure modes` / `## Examples` all present
  Steps shape        Markdown ordered list starting at 1; sequential
                     increments 1..N
  Examples content   at least one fenced code block (``` or ~~~)

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
    awk|find|basename|head) printf 'should be preinstalled on any POSIX system' ;;
    *)                      printf 'see your package manager' ;;
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

# Strip frontmatter and print remaining body lines with line numbers
# (body line numbers, starting at 1 after the closing ---).
body_with_nums() {
  local file="$1"
  awk '
    BEGIN { in_fm = 0; past_fm = 0; body_nr = 0 }
    NR == 1 && /^---[[:space:]]*$/ { in_fm = 1; next }
    in_fm && /^---[[:space:]]*$/ { in_fm = 0; past_fm = 1; next }
    in_fm { next }
    !in_fm && !past_fm { past_fm = 1 }
    { body_nr++; print body_nr "\t" $0 }
  ' "${file}"
}

check_required_sections() {
  local file="$1"
  local body missing=""
  local section
  body="$(body_with_nums "${file}")"
  for section in "${REQUIRED_SECTIONS[@]}"; do
    # Match `## Section` at start of a body line, optional trailing spaces.
    if ! printf '%s\n' "${body}" | awk -v s="${section}" '
      BEGIN { FS = "\t"; pat = "^## " s "[[:space:]]*$" }
      $2 ~ pat { found = 1; exit 0 }
      END { exit found ? 0 : 1 }
    '; then
      if [ -n "${missing}" ]; then
        missing="${missing}, ## ${section}"
      else
        missing="## ${section}"
      fi
    fi
  done
  if [ -n "${missing}" ]; then
    emit_fail "${file}" "Required sections" \
      "missing section(s): ${missing}" \
      "Add the missing H2 section(s) with real content (not placeholder headings)"
    return 1
  fi
  return 0
}

check_steps_shape() {
  local file="$1"
  # Extract the `## Steps` section (lines until the next `## ` heading
  # or end of file). Then check that the first list-shaped line is an
  # ordered list item starting at 1 and that subsequent ordered-list
  # items increment sequentially.
  local section
  section="$(awk '
    BEGIN { in_sec = 0 }
    /^## / {
      if (in_sec) { exit }
      if ($0 ~ /^## Steps[[:space:]]*$/) { in_sec = 1; next }
    }
    in_sec { print }
  ' "${file}" 2>/dev/null)"

  if [ -z "${section}" ]; then
    # Steps section missing — already flagged by check_required_sections.
    return 0
  fi

  # Find list items — lines matching /^[0-9]+\.\s/ or /^\s*[-*+]\s/.
  # Ordered items appear first => ordered list. Unordered items first => not ordered.
  local first_list_line
  first_list_line="$(printf '%s\n' "${section}" | awk '
    /^[[:space:]]*[-*+][[:space:]]+/ { print "UL:" $0; exit }
    /^[0-9]+\.[[:space:]]+/ { print "OL:" $0; exit }
  ')"

  if [ -z "${first_list_line}" ]; then
    emit_fail "${file}" "Steps shape" \
      "## Steps contains no Markdown list (ordered or unordered)" \
      "Write Steps as a numbered ordered list, one atomic action per step, starting at 1"
    return 1
  fi

  case "${first_list_line}" in
    UL:*)
      emit_fail "${file}" "Steps shape" \
        "## Steps begins with an unordered list; expected an ordered list (1. 2. 3. ...)" \
        "Convert to a numbered ordered list starting at 1 with sequential increments"
      return 1
      ;;
    OL:*)
      ;;
  esac

  # Validate ordered-list numbering: first number must be 1; subsequent
  # ordered-list top-level items must increment by 1.
  local nums
  nums="$(printf '%s\n' "${section}" | awk '
    /^[0-9]+\.[[:space:]]+/ {
      match($0, /^[0-9]+/)
      print substr($0, RSTART, RLENGTH)
    }
  ')"
  local first_num
  first_num="$(printf '%s\n' "${nums}" | head -n 1)"
  if [ "${first_num}" != "1" ]; then
    emit_fail "${file}" "Steps shape" \
      "## Steps ordered list starts at ${first_num}, not 1" \
      "Renumber the ordered list to start at 1"
    return 1
  fi
  local expect=1 n
  local non_seq=""
  while IFS= read -r n; do
    [ -n "${n}" ] || continue
    if [ "${n}" != "${expect}" ]; then
      non_seq="${non_seq}${non_seq:+, }${n}"
    fi
    expect=$((n + 1))
  done <<<"${nums}"
  if [ -n "${non_seq}" ]; then
    emit_warn "${file}" "Steps shape" \
      "## Steps ordered list has non-sequential numbering (unexpected: ${non_seq})" \
      "Renumber sequentially 1..N"
    # WARN does not flip the FAIL exit; swallow.
  fi
  return 0
}

check_examples_fenced() {
  local file="$1"
  # Extract the Examples section body; then look for a fenced block marker.
  local section
  section="$(awk '
    BEGIN { in_sec = 0 }
    /^## / {
      if (in_sec) { exit }
      if ($0 ~ /^## Examples[[:space:]]*$/) { in_sec = 1; next }
    }
    in_sec { print }
  ' "${file}" 2>/dev/null)"

  if [ -z "${section}" ]; then
    return 0  # already flagged by check_required_sections
  fi

  if printf '%s\n' "${section}" | awk '
    /^[[:space:]]*```/ { found = 1; exit }
    /^[[:space:]]*~~~/ { found = 1; exit }
    END { exit found ? 0 : 1 }
  '; then
    return 0
  fi

  emit_warn "${file}" "Examples content" \
    "## Examples contains no fenced code block" \
    "Add at least one fenced block (\`\`\`) showing inputs, outputs, and side effects"
  return 0
}

check_file() {
  local file="$1"
  local fail=0
  check_required_sections "${file}" || fail=1
  check_steps_shape       "${file}" || fail=1
  check_examples_fenced   "${file}"  # WARN only
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
