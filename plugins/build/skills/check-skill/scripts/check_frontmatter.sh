#!/usr/bin/env bash
#
# check_frontmatter.sh — Deterministic Tier-1 frontmatter checks for
# Claude Code SKILL.md files: required keys, version shape, owner
# presence, description cap.
#
# Required keys:    `name`, `description`, `version`, `owner` present and non-empty.
# Version shape:    matches ^[0-9]+\.[0-9]+\.[0-9]+$ (semver).
# Description cap:  `description` ≤ 1024 chars; combined with `when_to_use` ≤ 1536.
#
# Name slug format and reserved-token checks live in check_identity.sh.
#
# Usage:
#   check_frontmatter.sh <path> [<path> ...]
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
REQUIRED_KEYS=(name description version owner)
DESCRIPTION_CAP=1024
COMBINED_CAP=1536

usage() {
  cat <<'EOF'
check_frontmatter.sh — Frontmatter checks for Claude Code SKILL.md files.

Usage:
  check_frontmatter.sh <path> [<path> ...]

Checks:
  Required keys   `name` / `description` / `version` / `owner` present, non-empty
  Version shape   ^[0-9]+\.[0-9]+\.[0-9]+$ (semver MAJOR.MINOR.PATCH)
  Description cap `description` ≤ 1024 chars (combined with `when_to_use` ≤ 1536)

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

# Read a scalar value (possibly a folded block scalar under `>` or `>-`)
# for a top-level frontmatter key. Returns:
#   stdout: the value (folded whitespace for block scalars)
#   exit 0: key present
#   exit 1: key not present
read_value() {
  local file="$1" key="$2"
  awk -v k="${key}" '
    function strip_quotes(s) {
      if (match(s, /^".*"$/) || match(s, /^'"'"'.*'"'"'$/)) {
        return substr(s, 2, length(s) - 2)
      }
      return s
    }
    BEGIN { in_fm = 0; mode = "none"; acc = ""; found = 0 }
    NR == 1 && /^---[[:space:]]*$/ { in_fm = 1; next }
    in_fm && /^---[[:space:]]*$/ {
      if (found) { print acc }
      exit found ? 0 : 1
    }
    in_fm {
      if (mode == "block") {
        if ($0 ~ /^[A-Za-z_][A-Za-z0-9_-]*:/) {
          print acc
          exit 0
        }
        line = $0
        sub(/^[[:space:]]+/, "", line)
        if (line == "") {
          acc = acc " "
        } else {
          if (acc == "") { acc = line } else { acc = acc " " line }
        }
        next
      }
      pat = "^" k ":[[:space:]]*"
      if (match($0, pat)) {
        val = substr($0, RLENGTH + 1)
        sub(/[[:space:]]+$/, "", val)
        if (val == ">" || val == ">-" || val == "|" || val == "|-") {
          mode = "block"
          acc = ""
          found = 1
          next
        }
        print strip_quotes(val)
        found = 1
        exit 0
      }
    }
    END {
      if (mode == "block") {
        print acc
        exit 0
      }
      exit found ? 0 : 1
    }
  ' "${file}" 2>/dev/null
}

check_required_key() {
  local file="$1" key="$2"
  local val
  if ! val="$(read_value "${file}" "${key}")"; then
    emit_fail "${file}" "Required frontmatter" \
      "missing required key '${key}'" \
      "Add '${key}: <value>' to the frontmatter"
    return 1
  fi
  # Strip trailing whitespace
  val="${val%"${val##*[![:space:]]}"}"
  if [ -z "${val}" ]; then
    emit_fail "${file}" "Required frontmatter" \
      "key '${key}' is present but empty" \
      "Set a non-empty value for '${key}'"
    return 1
  fi
  return 0
}

check_version_shape() {
  local file="$1"
  local val
  val="$(read_value "${file}" "version")" || return 0  # missing = handled elsewhere
  val="${val%"${val##*[![:space:]]}"}"
  [ -n "${val}" ] || return 0
  if ! printf '%s' "${val}" | awk '
    { if ($0 ~ /^[0-9]+\.[0-9]+\.[0-9]+$/) exit 0; else exit 1 }
  '; then
    emit_fail "${file}" "Version shape" \
      "version '${val}' is not semver MAJOR.MINOR.PATCH" \
      "Rewrite as three dot-separated integers (e.g., 1.0.0)"
    return 1
  fi
  return 0
}

char_count() {
  # Byte count is a safe upper bound for the ASCII-heavy description
  # field; multibyte characters would over-count slightly, which is
  # acceptable for a cap check.
  printf '%s' "$1" | wc -c | tr -d ' '
}

check_description_cap() {
  local file="$1"
  local desc when combined
  desc="$(read_value "${file}" "description")" || return 0
  local desc_len
  desc_len="$(char_count "${desc}")"
  local fail=0

  if [ "${desc_len}" -gt "${DESCRIPTION_CAP}" ]; then
    emit_fail "${file}" "Description cap" \
      "description is ${desc_len} chars, exceeds ${DESCRIPTION_CAP}-char cap" \
      "Split trigger phrases into 'when_to_use' (combined cap ${COMBINED_CAP}) rather than compressing"
    fail=1
  fi

  if when="$(read_value "${file}" "when_to_use")"; then
    local when_len combined_len
    when_len="$(char_count "${when}")"
    combined_len=$((desc_len + when_len))
    if [ "${combined_len}" -gt "${COMBINED_CAP}" ]; then
      emit_fail "${file}" "Description cap" \
        "description + when_to_use is ${combined_len} chars, exceeds combined ${COMBINED_CAP}-char cap" \
        "Trim the trigger surface; move long-form guidance into the body (## When to use)"
      fail=1
    fi
  fi

  return "${fail}"
}

check_file() {
  local file="$1"
  local fail=0
  local first
  first="$(head -n 1 "${file}" 2>/dev/null || true)"
  if [ "${first}" != "---" ]; then
    emit_fail "${file}" "Required frontmatter" \
      "file does not begin with YAML frontmatter (---)" \
      "Add a YAML frontmatter block delimited by --- lines at the top of the file"
    return 1
  fi

  local key
  for key in "${REQUIRED_KEYS[@]}"; do
    check_required_key "${file}" "${key}" || fail=1
  done

  check_version_shape    "${file}" || fail=1
  check_description_cap  "${file}" || fail=1

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
