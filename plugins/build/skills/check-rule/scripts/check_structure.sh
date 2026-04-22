#!/usr/bin/env bash
#
# check_structure.sh — Deterministic Tier-1 structural checks for
# Claude Code rule files: location, extension, frontmatter shape.
#
# Location: rule files must live under .claude/rules/ or ~/.claude/rules/.
# Extension: rule files must end in .md (not .mdx, .markdown, or .X.md).
# Frontmatter shape: only `paths:` is a documented top-level key;
#   unknown keys emit INFO findings.
#
# Usage:
#   check_structure.sh <path> [<path> ...]
#
# Paths may be files or directories (recursively scanned for
# .md/.mdx/.markdown — the non-.md extensions are scanned so the
# extension check can catch misnamed rule files).
#
# Exit codes:
#   0   no FAIL findings (INFO-only runs also return 0)
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

usage() {
  cat <<'EOF'
check_structure.sh — Structural checks for Claude Code rule files.

Usage:
  check_structure.sh <path> [<path> ...]

Checks:
  Location          must be under .claude/rules/ or ~/.claude/rules/
  Extension         must end in .md (not .mdx, .markdown, or .X.md)
  Frontmatter shape only `paths:` is a documented top-level key

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

abspath() {
  local file="$1"
  local dir
  dir="$(cd "$(dirname "${file}")" 2>/dev/null && pwd)" || {
    printf '%s' "${file}"
    return
  }
  printf '%s/%s' "${dir}" "$(basename "${file}")"
}

emit_fail() {
  local path="$1" check="$2" detail="$3" rec="$4"
  printf 'FAIL  %s — %s: %s\n' "${path}" "${check}" "${detail}"
  printf '  Recommendation: %s\n' "${rec}"
}

emit_info() {
  local path="$1" check="$2" detail="$3" rec="$4"
  printf 'INFO  %s — %s: %s\n' "${path}" "${check}" "${detail}"
  printf '  Recommendation: %s\n' "${rec}"
}

check_location() {
  local file="$1"
  local abs
  abs="$(abspath "${file}")"
  case "${abs}" in
    */.claude/rules/*) return 0 ;;
    *)
      emit_fail "${file}" "Location" \
        "file not under .claude/rules/ or ~/.claude/rules/" \
        "Move the file to .claude/rules/<name>.md"
      return 1
      ;;
  esac
}

check_extension() {
  local file="$1"
  local base stem ext
  base="$(basename "${file}")"
  case "${base}" in
    *.md)
      stem="${base%.md}"
      case "${stem}" in
        *.*)
          emit_fail "${file}" "Extension" \
            "double extension .${stem##*.}.md" \
            "Rename to <name>.md (remove the inner extension segment)"
          return 1
          ;;
        *) return 0 ;;
      esac
      ;;
    *.mdx|*.markdown)
      ext="${base##*.}"
      emit_fail "${file}" "Extension" \
        "file extension is .${ext}, expected .md" \
        "Rename to <name>.md"
      return 1
      ;;
    *)
      emit_fail "${file}" "Extension" \
        "file has no .md extension" \
        "Rename to <name>.md"
      return 1
      ;;
  esac
}

check_frontmatter_shape() {
  local file="$1"
  local first
  first="$(head -n 1 "${file}" 2>/dev/null || true)"
  if [ "${first}" != "---" ]; then
    # No frontmatter — always-on rule, valid.
    return 0
  fi

  local hit line key
  while IFS= read -r hit; do
    line="${hit%%:*}"
    key="${hit#*:}"
    emit_info "${file}" "Frontmatter shape" \
      "unknown top-level key '${key}' at line ${line}" \
      "Remove the key, or move its content into the body"
  done < <(
    awk '
      BEGIN { in_fm = 0 }
      NR == 1 && /^---$/ { in_fm = 1; next }
      in_fm && /^---$/ { exit }
      in_fm && /^[A-Za-z_][A-Za-z0-9_-]*:/ {
        match($0, /^[A-Za-z_][A-Za-z0-9_-]*/)
        key = substr($0, RSTART, RLENGTH)
        if (key != "paths") {
          print NR ":" key
        }
      }
    ' "${file}" 2>/dev/null || true
  )
}

check_file() {
  local file="$1"
  local fail=0

  check_location "${file}"          || fail=1
  check_extension "${file}"         || fail=1
  check_frontmatter_shape "${file}"  # INFO only; no exit-code effect

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
      find "${target}" -type f \
        \( -name '*.md' -o -name '*.mdx' -o -name '*.markdown' \) \
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

  local any=0
  local target
  for target in "$@"; do
    check_path "${target}" || any=1
  done

  exit "${any}"
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
