#!/usr/bin/env bash
# Shared helpers for paperkit scripts.

# Print the directory that contains .paperkit/, searching upward from $1 or $PWD.
find_paperkit_root() {
    local dir="${1:-$(pwd)}"
    dir="$(cd -- "$dir" 2>/dev/null && pwd)" || return 1
    local prev=""
    while true; do
        if [ -d "$dir/.paperkit" ]; then
            echo "$dir"
            return 0
        fi
        if [ "$dir" = "/" ] || [ "$dir" = "$prev" ]; then
            return 1
        fi
        prev="$dir"
        dir="$(dirname "$dir")"
    done
}

# Escape a string for inclusion in a JSON string literal.
json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    printf '%s' "$s"
}

# Print a JSON array from the arguments.
json_array() {
    local first=1 item
    printf '['
    for item in "$@"; do
        [ $first -eq 1 ] || printf ','
        printf '"%s"' "$(json_escape "$item")"
        first=0
    done
    printf ']'
}
