#!/usr/bin/env bash
#
# check_identity.sh — Deterministic Tier-1 identity checks for Claude
# Code SKILL.md files: filename case, directory basename, name slug
# format, reserved tokens, uniqueness across the audited set.
#
# Filename:         file must be named exactly SKILL.md (case-sensitive).
# Directory match:  parent directory basename must equal frontmatter `name`.
# Name slug:        `name` matches ^[a-z0-9]+(-[a-z0-9]+)*$, ≤64 chars.
# Reserved tokens:  `name` must not contain `anthropic` or `claude`.
# Uniqueness:       no two audited skills may share the same `name`.
#
# Usage:
#   check_identity.sh <path> [<path> ...]
#
# Paths may be files (SKILL.md or variant) or directories (scanned
# recursively for SKILL.md / Skill.md / skill.md — wrong-case variants
# are picked up so the filename check can flag them).
#
# Exit codes:
#   0   no FAIL findings
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename, dirname

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename dirname)

usage() {
  cat <<'EOF'
check_identity.sh — Identity checks for Claude Code SKILL.md files.

Usage:
  check_identity.sh <path> [<path> ...]

Checks:
  Filename          must be exactly SKILL.md (case-sensitive)
  Directory match   parent directory basename == frontmatter `name`
  Name slug         ^[a-z0-9]+(-[a-z0-9]+)*$, ≤64 characters
  Reserved tokens   `name` must not contain `anthropic` or `claude`
  Uniqueness        no two audited skills share the same `name`

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
    awk|find|basename|dirname) printf 'should be preinstalled on any POSIX system' ;;
    *)                         printf 'see your package manager' ;;
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

# Extract a scalar string value for the given top-level frontmatter key.
# Echoes the value (without surrounding quotes) or nothing if absent.
# Only handles single-line scalars — folded block scalars are the
# description cap's concern, not identity.
read_scalar() {
  local file="$1" key="$2"
  awk -v k="${key}" '
    BEGIN { in_fm = 0 }
    NR == 1 && /^---[[:space:]]*$/ { in_fm = 1; next }
    in_fm && /^---[[:space:]]*$/ { exit }
    in_fm {
      pat = "^" k ":[[:space:]]*"
      if (match($0, pat)) {
        val = substr($0, RLENGTH + 1)
        sub(/[[:space:]]+$/, "", val)
        if (match(val, /^".*"$/) || match(val, /^'"'"'.*'"'"'$/)) {
          val = substr(val, 2, length(val) - 2)
        }
        print val
        exit
      }
    }
  ' "${file}" 2>/dev/null || true
}

check_filename() {
  local file="$1"
  local base
  base="$(basename "${file}")"
  if [ "${base}" = "SKILL.md" ]; then
    return 0
  fi
  emit_fail "${file}" "Filename" \
    "file is named '${base}', expected 'SKILL.md' (case-sensitive)" \
    "Rename to SKILL.md — Claude Code's skill loader matches the filename exactly"
  return 1
}

check_directory_match() {
  local file="$1" name="$2"
  local dir_base
  dir_base="$(basename "$(dirname "${file}")")"
  if [ "${dir_base}" = "${name}" ]; then
    return 0
  fi
  emit_fail "${file}" "Directory basename" \
    "parent directory '${dir_base}' does not match frontmatter name '${name}'" \
    "Rename the directory to '${name}/' or update the name field to '${dir_base}'"
  return 1
}

check_name_slug() {
  local file="$1" name="$2"
  local fail=0
  local len=${#name}
  if [ "${len}" -gt 64 ]; then
    emit_fail "${file}" "Name slug" \
      "name '${name}' is ${len} chars, exceeds 64-char cap" \
      "Shorten the name while preserving meaning; move detail to description"
    fail=1
  fi
  # Kebab-case: ^[a-z0-9]+(-[a-z0-9]+)*$
  case "${name}" in
    ""|-*|*-) ;;
    *) ;;
  esac
  if ! printf '%s' "${name}" | awk '
    { if ($0 ~ /^[a-z0-9]+(-[a-z0-9]+)*$/) exit 0; else exit 1 }
  '; then
    emit_fail "${file}" "Name slug" \
      "name '${name}' is not lowercase kebab-case (^[a-z0-9]+(-[a-z0-9]+)*\$)" \
      "Rewrite as lowercase kebab-case (e.g., my-skill-name)"
    fail=1
  fi
  return "${fail}"
}

check_reserved_tokens() {
  local file="$1" name="$2"
  case "${name}" in
    *anthropic*|*claude*)
      emit_fail "${file}" "Reserved name token" \
        "name '${name}' contains a platform-reserved token (anthropic / claude)" \
        "Rename without the reserved token — these collide with platform namespaces"
      return 1
      ;;
  esac
  return 0
}

check_file() {
  local file="$1"
  local fail=0

  check_filename "${file}" || fail=1

  local name
  name="$(read_scalar "${file}" "name")"
  if [ -z "${name}" ]; then
    # Missing name is check_frontmatter.sh's concern; skip name-based
    # checks to avoid duplicate findings.
    return "${fail}"
  fi

  check_directory_match "${file}" "${name}"  || fail=1
  check_name_slug       "${file}" "${name}"  || fail=1
  check_reserved_tokens "${file}" "${name}"  || fail=1

  # Record name for uniqueness check; caller aggregates.
  printf '%s\t%s\n' "${name}" "${file}" >>"${UNIQ_LOG}"

  return "${fail}"
}

check_uniqueness() {
  # Groups names appearing more than once and emits a FAIL per file.
  if [ ! -s "${UNIQ_LOG}" ]; then
    return 0
  fi
  local dup_names
  dup_names="$(awk -F'\t' '{print $1}' "${UNIQ_LOG}" | sort | uniq -d)"
  if [ -z "${dup_names}" ]; then
    return 0
  fi
  local any=0 name file others
  while IFS= read -r name; do
    [ -n "${name}" ] || continue
    others="$(awk -F'\t' -v n="${name}" '$1 == n { print $2 }' "${UNIQ_LOG}" | paste -sd ',' -)"
    while IFS= read -r file; do
      emit_fail "${file}" "Name uniqueness" \
        "name '${name}' collides with another audited skill (matches: ${others})" \
        "Rename one of the colliding skills to a distinct, more specific name"
      any=1
    done < <(awk -F'\t' -v n="${name}" '$1 == n { print $2 }' "${UNIQ_LOG}")
  done <<<"${dup_names}"
  return "${any}"
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
      find "${target}" -type f \
        \( -name 'SKILL.md' -o -name 'Skill.md' -o -name 'skill.md' \) \
        -not -path '*/_shared/*' \
        2>/dev/null
    )
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
  return "${any}"
}

UNIQ_LOG=""

cleanup() {
  [ -n "${UNIQ_LOG}" ] && [ -f "${UNIQ_LOG}" ] && rm -f "${UNIQ_LOG}"
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

  UNIQ_LOG="$(mktemp -t check_identity.XXXXXX)"
  trap cleanup EXIT INT TERM

  local any=0
  local target
  for target in "$@"; do
    check_path "${target}" || any=1
  done

  check_uniqueness || any=1

  exit "${any}"
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
