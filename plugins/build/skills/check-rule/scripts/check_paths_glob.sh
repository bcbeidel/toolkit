#!/usr/bin/env bash
#
# check_paths_glob.sh — Validate the `paths:` globs in Claude Code
# rule file frontmatter.
#
# Checks each glob entry for:
#   - empty pattern
#   - unbalanced braces {...}
#   - unbalanced brackets [...]
#   - control characters
#
# Supports inline list  (paths: ["a", "b"])
# and block list        (paths:\n  - "a"\n  - "b").
#
# Limitations (documented, not supported):
#   - Multi-line inline arrays (paths: [\n  "a"\n])
#   - Inline entries containing literal commas inside string values
#   - Escaped braces/brackets (\{, \[) are counted as unbalanced
#
# Files without frontmatter or without a paths: key are skipped.
#
# Usage:
#   check_paths_glob.sh <path> [<path> ...]
#
# Exit codes:
#   0   no findings
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename, head, tr, grep

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename head tr grep)

usage() {
  cat <<'EOF'
check_paths_glob.sh — Validate paths: globs in rule file frontmatter.

Usage:
  check_paths_glob.sh <path> [<path> ...]

Checks:
  empty-pattern        a paths entry is empty or whitespace-only
  unbalanced-braces    mismatched {...} in a glob
  unbalanced-brackets  mismatched [...] in a glob
  control-character    non-printable characters in a glob

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no findings
  1   one or more FAIL findings
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    awk|find|basename|head|tr|grep) printf 'should be preinstalled on any POSIX system' ;;
    *)                              printf 'see your package manager' ;;
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

count_char() {
  local str="$1" char="$2"
  local stripped
  stripped="$(printf '%s' "${str}" | tr -d "${char}")"
  printf '%s' "$(( ${#str} - ${#stripped} ))"
}

validate_glob() {
  local file="$1" line="$2" entry="$3"
  local fail=0
  local trimmed

  trimmed="$(printf '%s' "${entry}" | tr -d '[:space:]')"
  if [ -z "${trimmed}" ]; then
    emit_fail "${file}" "paths glob validity" \
      "empty pattern at line ${line}" \
      "Remove the empty entry or replace with a valid glob"
    return 1
  fi

  if printf '%s' "${entry}" | LC_ALL=C grep -qE '[[:cntrl:]]'; then
    emit_fail "${file}" "paths glob validity" \
      "control character in pattern at line ${line}" \
      "Remove non-printable characters from the pattern"
    fail=1
  fi

  if [ "$(count_char "${entry}" '{')" != "$(count_char "${entry}" '}')" ]; then
    emit_fail "${file}" "paths glob validity" \
      "unclosed brace in \"${entry}\" at line ${line}" \
      "Close the brace (e.g., \"src/**/*.{ts,tsx}\")"
    fail=1
  fi

  if [ "$(count_char "${entry}" '[')" != "$(count_char "${entry}" ']')" ]; then
    emit_fail "${file}" "paths glob validity" \
      "unclosed bracket in \"${entry}\" at line ${line}" \
      "Close the bracket (e.g., \"src/**/*.[ch]\")"
    fail=1
  fi

  return "${fail}"
}

extract_paths_entries() {
  local file="$1"
  awk '
    function split_top(content, items,   i, ch, depth, start, n, len) {
      n = 0
      depth = 0
      start = 1
      len = length(content)
      for (i = 1; i <= len; i++) {
        ch = substr(content, i, 1)
        if (ch == "{" || ch == "[") depth++
        else if (ch == "}" || ch == "]") depth--
        else if (ch == "," && depth == 0) {
          n++
          items[n] = substr(content, start, i - start)
          start = i + 1
        }
      }
      if (start <= len) {
        n++
        items[n] = substr(content, start)
      }
      return n
    }

    function strip_quotes(s) {
      if (match(s, /^"[^"]*"$/) || match(s, /^\047[^\047]*\047$/)) {
        s = substr(s, 2, length(s) - 2)
      }
      return s
    }

    BEGIN { in_fm=0; in_block=0 }

    NR==1 && /^---$/ { in_fm=1; next }
    in_fm && /^---$/ { exit }
    !in_fm { next }

    /^paths:[[:space:]]*\[/ {
      if (match($0, /\[.*\]/)) {
        content = substr($0, RSTART+1, RLENGTH-2)
        n = split_top(content, items)
        for (i=1; i<=n; i++) {
          entry = items[i]
          sub(/^[[:space:]]+/, "", entry)
          sub(/[[:space:]]+$/, "", entry)
          entry = strip_quotes(entry)
          print NR "\t" entry
        }
      }
      in_block = 0
      next
    }

    /^paths:[[:space:]]*$/ {
      in_block = 1
      next
    }

    in_block && /^[[:space:]]+-[[:space:]]+/ {
      entry = $0
      sub(/^[[:space:]]+-[[:space:]]+/, "", entry)
      sub(/[[:space:]]+$/, "", entry)
      entry = strip_quotes(entry)
      print NR "\t" entry
      next
    }

    in_block && /^[[:space:]]*$/ { next }
    in_block { in_block = 0 }
  ' "${file}" 2>/dev/null || true
}

check_file() {
  local file="$1"
  local fail=0
  local hit line entry

  while IFS= read -r hit; do
    line="${hit%%$'\t'*}"
    entry="${hit#*$'\t'}"
    validate_glob "${file}" "${line}" "${entry}" || fail=1
  done < <(extract_paths_entries "${file}")

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
    done < <(find "${target}" -type f -name '*.md' 2>/dev/null)
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
