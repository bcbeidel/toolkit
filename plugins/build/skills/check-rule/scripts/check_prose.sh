#!/usr/bin/env bash
#
# check_prose.sh — Deterministic Tier-1 pre-check for rule-file prose.
#
# Flags high-confidence cases for three Tier-2 dimensions:
#   Specificity    — hedged phrasing (prefer, generally, usually, consider,
#                    "where appropriate", "as appropriate", "where it makes sense")
#   Framing        — prohibition-only openers (Don't / Never / Avoid at
#                    the start of the rule statement)
#   Example Realism — synthetic placeholders inside fenced code blocks
#                    (foo+bar pair, myFunction/myClass/…, Widget/SomeClass,
#                    placeholder, example_\w+)
#
# All findings emit at WARN severity. WARN does not exit non-zero —
# these are heuristics with legitimate exceptions (e.g., "Never log PII"
# is a valid prohibition-only rule). Tier-2 remains the judgment layer.
#
# Usage:
#   check_prose.sh <path> [<path> ...]
#
# Paths may be files or directories (recursively scanned for *.md).
#
# Exit codes:
#   0   always (WARN findings are heuristics, not failures)
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename)

usage() {
  cat <<'EOF'
check_prose.sh — Prose pre-check for Claude Code rule files.

Usage:
  check_prose.sh <path> [<path> ...]

Pre-checks (WARN only):
  Hedges                  prefer / generally / usually / consider / "where appropriate"
  Prohibition-only opener Don't / Never / Avoid at rule-statement start
  Synthetic placeholders  foo+bar pair, myFunction/myClass family,
                          Widget/SomeClass, placeholder, example_*

All patterns have legitimate exceptions. WARN flags candidates;
Tier-2 LLM evaluation remains the judgment layer.

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   always
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

scan_file() {
  local file="$1"
  awk '
    BEGIN { in_fm = 0; in_code = 0 }

    # Frontmatter skip (between first two --- markers).
    NR == 1 && /^---$/ { in_fm = 1; next }
    in_fm && /^---$/ { in_fm = 0; next }
    in_fm { next }

    # Code-block toggle (``` lines switch in_code state).
    /^```/ { in_code = !in_code; next }

    # ----- INSIDE CODE BLOCK: synthetic-placeholder checks -----
    in_code {
      if (tolower($0) ~ /(^|[^A-Za-z_])foo([^A-Za-z_]|$)/ &&
          tolower($0) ~ /(^|[^A-Za-z_])bar([^A-Za-z_]|$)/) {
        printf "WARN  %s — prose: synthetic identifier (foo/bar) in code example at line %d\n", FILENAME, NR
        printf "  Recommendation: Replace with real code from the codebase (actual table names, function names, module paths)\n"
      }
      if ($0 ~ /(^|[^A-Za-z_])(myFunction|myClass|myObject|myVariable|myComponent)([^A-Za-z_]|$)/) {
        printf "WARN  %s — prose: placeholder identifier (my*) in code example at line %d\n", FILENAME, NR
        printf "  Recommendation: Replace with real code from the codebase (actual table names, function names, module paths)\n"
      }
      if ($0 ~ /(^|[^A-Za-z_])(Widget|MyWidget|SomeClass|SomeThing)([^A-Za-z_]|$)/) {
        printf "WARN  %s — prose: placeholder class (Widget/SomeClass) in code example at line %d\n", FILENAME, NR
        printf "  Recommendation: Replace with real code from the codebase (actual table names, function names, module paths)\n"
      }
      if ($0 ~ /(^|[^A-Za-z_])(placeholder|example_[A-Za-z_]+)([^A-Za-z_]|$)/) {
        printf "WARN  %s — prose: placeholder token in code example at line %d\n", FILENAME, NR
        printf "  Recommendation: Replace with real code from the codebase (actual table names, function names, module paths)\n"
      }
      next
    }

    # ----- OUTSIDE CODE BLOCK: hedge check -----
    {
      lc = tolower($0)
      if (match(lc, /(^|[^A-Za-z_])(prefer|generally|usually|consider)([^A-Za-z_]|$)/)) {
        word = substr(lc, RSTART, RLENGTH)
        gsub(/^[^A-Za-z_]+/, "", word)
        gsub(/[^A-Za-z_]+$/, "", word)
        printf "WARN  %s — prose: hedged phrasing \"%s\" at line %d\n", FILENAME, word, NR
        printf "  Recommendation: State the rule directly; if there are exceptions, list them in a **Exception:** line\n"
      }
      if (lc ~ /where appropriate/ || lc ~ /as appropriate/ || lc ~ /where it makes sense/) {
        printf "WARN  %s — prose: hedged phrase at line %d\n", FILENAME, NR
        printf "  Recommendation: Replace with a specific condition or remove the hedge\n"
      }
    }

    # ----- OUTSIDE CODE BLOCK: prohibition-only opener -----
    {
      stripped = $0
      sub(/^[[:space:]]*/,       "", stripped)
      sub(/^#+[[:space:]]+/,     "", stripped)
      sub(/^[*-][[:space:]]+/,   "", stripped)
      sub(/^>[[:space:]]+/,      "", stripped)
      sub(/^\*\*[[:space:]]*/,   "", stripped)
      if (match(stripped, /^(Don['\''\047]t|Never|Avoid)([[:space:]]|$)/)) {
        word = substr(stripped, RSTART, RLENGTH)
        gsub(/[[:space:]]+$/, "", word)
        printf "WARN  %s — prose: prohibition-only opener \"%s\" at line %d\n", FILENAME, word, NR
        printf "  Recommendation: Restate as a positive action (\"Use X\") unless no clean positive counterpart exists\n"
      }
    }
  ' "${file}" 2>/dev/null || true
}

scan_path() {
  local target="$1"
  local file

  if [ -f "${target}" ]; then
    scan_file "${target}"
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      scan_file "${file}"
    done < <(find "${target}" -type f -name '*.md' 2>/dev/null)
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
  local arg_err=0
  for target in "$@"; do
    scan_path "${target}" || arg_err=1
  done

  if [ "${arg_err}" -ne 0 ]; then
    exit 64
  fi
  exit 0
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
