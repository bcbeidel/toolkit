#!/usr/bin/env bash
#
# check_collision.sh — Tier-3 description-collision check for subagent
# definitions.
#
# Computes pairwise token-set Jaccard similarity across every .md file
# in the audit scope. Flags any pair with similarity >=0.6 as a WARN —
# overlapping descriptions produce non-deterministic routing because
# the main agent has no basis to pick between two agents claiming the
# same trigger surface.
#
# Single-file scope is a no-op (nothing to compare against).
#
# Usage:
#   check_collision.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings (WARN exits 0 per the Tier-1 contract)
#   1   one or more FAIL findings (not produced by this script)
#   64  usage error
#   69  missing dependency

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

THRESHOLD=60   # Jaccard * 100; >=60 => flag

REQUIRED_CMDS=(awk basename find tr)

usage() {
  cat <<'EOF'
check_collision.sh — Flag subagent pairs with colliding descriptions.

Usage:
  check_collision.sh <path> [<path> ...]
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

# Emit the description value for a single .md file, or empty string if
# no description is present / parseable.
extract_description() {
  awk '
    BEGIN { in_fm = 0; folded = 0; literal = 0; val = "" }
    /^---[[:space:]]*$/ {
      if (++fm_count == 1) { in_fm = 1; next }
      if (fm_count == 2)   { exit }
    }
    !in_fm { next }
    (folded || literal) && /^[^ \t]/ { folded = 0; literal = 0 }
    (folded || literal) && /^[ \t]+/ {
      line = $0
      sub(/^[ \t]+/, "", line)
      if (val == "") { val = line } else { val = val (folded ? " " : "\n") line }
      next
    }
    /^description:[ \t]*/ {
      rest = $0
      sub(/^description:[ \t]*/, "", rest)
      if (rest == ">" || rest == ">-") { folded = 1; next }
      if (rest == "|" || rest == "|-") { literal = 1; next }
      if (rest ~ /^".*"$/) { rest = substr(rest, 2, length(rest) - 2) }
      else if (rest ~ /^'\''.*'\''$/) { rest = substr(rest, 2, length(rest) - 2) }
      val = rest
    }
    END { print val }
  ' "$1"
}

# Tokenize a string: lowercase, split on non-alphanumeric, drop stopwords
# and very short tokens. Print one token per line (deduplicated via sort/uniq
# is handled by awk dedupe below).
tokenize() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | awk '
    BEGIN {
      split("the a an and or but of to for in on at by with as is are be use when not", s, " ")
      for (i in s) stop[s[i]] = 1
    }
    {
      n = split($0, tok, /[^a-z0-9]+/)
      for (i = 1; i <= n; i++) {
        if (length(tok[i]) < 3) continue
        if (tok[i] in stop) continue
        if (!(tok[i] in seen)) {
          seen[tok[i]] = 1
          print tok[i]
        }
      }
    }
  '
}

# Compute Jaccard similarity * 100 (integer) between two token sets.
# Inputs: two files, each with one token per line, already deduplicated.
jaccard_pct() {
  local a="$1" b="$2"
  awk '
    NR == FNR { set1[$0] = 1; n1++; next }
    {
      set2[$0] = 1; n2++
      if ($0 in set1) inter++
    }
    END {
      if (n1 == 0 && n2 == 0) { print 0; exit }
      union = n1 + n2 - inter
      if (union == 0) { print 0; exit }
      printf "%d\n", int(100 * inter / union)
    }
  ' "$a" "$b"
}

emit_warn() {
  printf 'WARN  %s — description-collision: %s (similarity %s%%)\n' "$1" "$2" "$3"
  printf '  Recommendation: Differentiate the descriptions (each naming a distinct trigger surface + exclusion + return), or merge into one subagent.\n'
}

# Collect all target files into an array.
gather_files() {
  local target file
  for target in "$@"; do
    if [ -f "${target}" ]; then
      case "${target}" in
        *.md) printf '%s\n' "${target}" ;;
      esac
    elif [ -d "${target}" ]; then
      find "${target}" -maxdepth 1 -type f -name '*.md' 2>/dev/null
    fi
  done
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

  # Collect files
  local files=()
  while IFS= read -r f; do
    [ -n "${f}" ] && files+=("${f}")
  done < <(gather_files "$@")

  if [ "${#files[@]}" -lt 2 ]; then
    # Nothing to compare; Tier-3 is a no-op.
    exit 0
  fi

  # Tokenize each file's description into a temp file (paired arrays).
  local tmpdir
  tmpdir="$(mktemp -d)"
  trap 'rm -rf "${tmpdir}"' EXIT

  local i tok_file desc
  for i in "${!files[@]}"; do
    desc="$(extract_description "${files[$i]}")"
    tok_file="${tmpdir}/tok.${i}"
    if [ -n "${desc}" ]; then
      tokenize "${desc}" > "${tok_file}"
    else
      : > "${tok_file}"
    fi
  done

  # Pairwise comparison
  local j pct
  for i in "${!files[@]}"; do
    for j in "${!files[@]}"; do
      if [ "${j}" -le "${i}" ]; then continue; fi
      # Skip pairs where either description is missing
      if [ ! -s "${tmpdir}/tok.${i}" ] || [ ! -s "${tmpdir}/tok.${j}" ]; then
        continue
      fi
      pct="$(jaccard_pct "${tmpdir}/tok.${i}" "${tmpdir}/tok.${j}")"
      if [ "${pct}" -ge "${THRESHOLD}" ]; then
        emit_warn "${files[$i]}" "collides with $(basename "${files[$j]}")" "${pct}"
      fi
    done
  done

  exit 0
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
