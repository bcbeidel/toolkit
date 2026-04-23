#!/usr/bin/env bash
#
# check_prose.sh — Tier-1 prose pre-checks for Claude Code SKILL.md
# files: hedging/filler words, absolute-path references outside code.
#
# Hedging words (case-insensitive whole-word): etc., maybe, probably,
# somehow, generally, sometimes, TBD, ???.
#
# Absolute-path references: `/home/…`, `~/…`, Windows drive-letter
# paths (`C:\…`), and multi-component backslash paths (`foo\bar`).
#
# Both checks emit WARN — these are heuristics that Tier-2's
# Clarity & Consistency dimension refines.
#
# Usage:
#   check_prose.sh <path> [<path> ...]
#
# Exit codes:
#   0   always (WARN only)
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename)

# Whole-word hedges. Matched case-insensitively outside fenced blocks.
HEDGES=(etc maybe probably somehow generally sometimes TBD)

usage() {
  cat <<'EOF'
check_prose.sh — Prose pre-checks for Claude Code SKILL.md files.

Usage:
  check_prose.sh <path> [<path> ...]

Checks:
  Hedges             whole-word matches for etc., maybe, probably,
                     somehow, generally, sometimes, TBD, ??? outside
                     fenced code blocks
  Absolute paths     /home/..., ~/..., C:\... drive-letter paths, or
                     multi-component backslash paths outside code

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   always (WARN only; no FAILs emitted)
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    awk|find|basename) printf 'should be preinstalled on any POSIX system' ;;
    *)                 printf 'see your package manager' ;;
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

emit_warn() {
  local path="$1" check="$2" detail="$3" rec="$4"
  printf 'WARN  %s — %s: %s\n' "${path}" "${check}" "${detail}"
  printf '  Recommendation: %s\n' "${rec}"
}

check_hedges() {
  local file="$1"
  local hedge_list
  # Join with | for awk regex. Also include ??? literal (not a word).
  hedge_list="$(printf '%s|' "${HEDGES[@]}")"
  hedge_list="${hedge_list%|}"
  local hits
  hits="$(awk -v hedges="${hedge_list}" '
    BEGIN {
      IGNORECASE = 1
      in_fence = 0
    }
    {
      if ($0 ~ /^[[:space:]]*```/ || $0 ~ /^[[:space:]]*~~~/) {
        in_fence = !in_fence
        next
      }
      if (in_fence) { next }
      line = $0
      # Strip inline code spans — words inside backticks are often
      # documentation of the very patterns this script looks for.
      gsub(/`[^`]*`/, "", line)
      # Literal ??? check (not a word; separate).
      if (index(line, "???") > 0) {
        print NR "\t???"
      }
      # Whole-word hedge check. Split into tokens on non-letter boundaries.
      n = split(line, toks, /[^A-Za-z]+/)
      for (i = 1; i <= n; i++) {
        t = tolower(toks[i])
        if (t == "") continue
        m = 1
        split(hedges, hl, "|")
        for (j in hl) {
          if (t == tolower(hl[j])) {
            print NR "\t" hl[j]
            break
          }
        }
      }
    }
  ' "${file}")"
  [ -n "${hits}" ] || return 0
  local row line_no word
  while IFS= read -r row; do
    [ -n "${row}" ] || continue
    line_no="${row%%$'\t'*}"
    word="${row##*$'\t'}"
    emit_warn "${file}" "Hedges" \
      "line ${line_no} contains hedge '${word}'" \
      "Replace with direct phrasing or delete the hedge"
  done <<<"${hits}"
  return 0
}

check_absolute_paths() {
  local file="$1"
  local hits
  hits="$(awk '
    BEGIN { in_fence = 0 }
    {
      if ($0 ~ /^[[:space:]]*```/ || $0 ~ /^[[:space:]]*~~~/) {
        in_fence = !in_fence
        next
      }
      if (in_fence) { next }
      # Skip lines in inline-code-only form (bare backtick segments
      # frequently contain relative paths; we only flag the prose).
      # Strip inline code spans `...` before pattern matching.
      line = $0
      gsub(/`[^`]*`/, "", line)

      # /home/ or /Users/ (POSIX absolute path starting at a user dir)
      if (match(line, /(^|[^A-Za-z0-9_])\/home\//) || match(line, /(^|[^A-Za-z0-9_])\/Users\//)) {
        print NR "\tPOSIX absolute path (/home/ or /Users/)"
      }
      # ~/ tilde home
      else if (match(line, /(^|[[:space:]])~\//)) {
        print NR "\tTilde home path (~/)"
      }
      # Windows drive letter: C:\ or C:/ style path
      else if (match(line, /(^|[^A-Za-z0-9_])[A-Za-z]:\\/) || match(line, /(^|[^A-Za-z0-9_])[A-Za-z]:\//)) {
        print NR "\tWindows drive-letter path"
      }
      # Multi-component backslash path: word\word\word (3+ components)
      else if (match(line, /[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+/)) {
        print NR "\tBackslash path (3+ components)"
      }
    }
  ' "${file}")"
  [ -n "${hits}" ] || return 0
  local row line_no detail
  while IFS= read -r row; do
    [ -n "${row}" ] || continue
    line_no="${row%%$'\t'*}"
    detail="${row##*$'\t'}"
    emit_warn "${file}" "Absolute path" \
      "line ${line_no}: ${detail}" \
      "Convert to a relative path or an environment variable"
  done <<<"${hits}"
  return 0
}

check_file() {
  local file="$1"
  check_hedges "${file}"
  check_absolute_paths "${file}"
  return 0
}

check_path() {
  local target="$1"
  local file
  if [ -f "${target}" ]; then
    check_file "${target}"
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      check_file "${file}"
    done < <(
      find "${target}" -type f -name 'SKILL.md' \
        -not -path '*/_shared/*' \
        2>/dev/null
    )
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
  return 0
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
    check_path "${target}" || exit 64
  done
  exit 0
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
