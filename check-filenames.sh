#!/usr/bin/env bash
# Verify that file names are safe to commit and to check out on Windows.
#
# Flags, per path component:
#   - illegal characters:  < > : " / \ | ? *  and ASCII control chars
#   - a trailing space or dot (Windows silently strips these)
#   - reserved device names: CON PRN AUX NUL COM1-9 LPT1-9 (any extension)
#
# By default it checks the files staged for commit (so it works as a
# pre-commit hook). Pass --all to check every tracked file instead.
#
# Exit status: 0 = all clean, 1 = at least one bad name.

set -euo pipefail

mode="staged"
[ "${1:-}" = "--all" ] && mode="all"

bad=0
count=0
report() { printf '  %s\n    -> %s\n' "$1" "$2"; bad=1; }

check_path() {
  path="$1"
  [ -z "$path" ] && return
  count=$((count + 1))
  # Check each path component (directory names count too).
  oldIFS="$IFS"; IFS='/'
  set -- $path
  IFS="$oldIFS"
  for comp in "$@"; do
    [ -z "$comp" ] && continue
    case "$comp" in
      *[\<\>:\"\\\|\?\*]*)  report "$path" "illegal character in '$comp' (one of < > : \" \\ | ? *)";;
      *' ')                 report "$path" "'$comp' ends with a space";;
      *.)                   report "$path" "'$comp' ends with a dot";;
    esac
    # Control characters (ASCII 0x01-0x1F).
    if printf '%s' "$comp" | LC_ALL=C grep -q '[[:cntrl:]]'; then
      report "$path" "control character in '$comp'"
    fi
    # Reserved device names (case-insensitive), with or without extension.
    stem=$(printf '%s' "${comp%%.*}" | tr '[:lower:]' '[:upper:]')
    case "$stem" in
      CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]) report "$path" "'$comp' uses a Windows reserved name";;
    esac
  done
}

# Read NUL-separated paths (bash 3.2 compatible).
if [ "$mode" = "all" ]; then
  src() { git ls-files -z; }
else
  # Added/Copied/Modified/Renamed staged paths.
  src() { git diff --cached --name-only --diff-filter=ACMR -z; }
fi

while IFS= read -r -d '' path; do
  check_path "$path"
done < <(src)

if [ "$bad" -ne 0 ]; then
  echo "Windows/git-unfriendly file names found:" >&2
  echo "Rename them (use 'git mv') before committing." >&2
  exit 1
fi

echo "File names OK (${count} ${mode} files checked)."
