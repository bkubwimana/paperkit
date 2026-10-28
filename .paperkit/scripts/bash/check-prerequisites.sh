#!/usr/bin/env bash
# Check that the artifacts a paperkit phase depends on exist.
#
# Usage: check-prerequisites.sh --phase <venue|claims|outline|figures|review|check>
#
# Prints one JSON object. Exit 0 when the phase may run, 1 when a required
# artifact is missing, 2 on usage error.

set -u
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
. "$SCRIPT_DIR/common.sh"

phase=""
while [ $# -gt 0 ]; do
    case "$1" in
        --phase) phase="${2:-}"; shift 2 ;;
        -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

case "$phase" in
    venue)   required=(constitution);                 recommended=() ;;
    claims)  required=(constitution venue);           recommended=() ;;
    outline) required=(constitution venue claims);    recommended=() ;;
    figures) required=(constitution claims);          recommended=(outline) ;;
    review)  required=(constitution venue claims);    recommended=(figures outline) ;;
    check)   required=(constitution venue claims);    recommended=(figures outline) ;;
    *) echo "usage: $0 --phase <venue|claims|outline|figures|review|check>" >&2; exit 2 ;;
esac

root="$(find_paperkit_root)" || {
    printf '{"ok":false,"error":"no .paperkit directory found above %s"}\n' "$(json_escape "$PWD")"
    exit 1
}

path_for() {
    case "$1" in
        constitution) echo "$root/.paperkit/memory/constitution.md" ;;
        venue)        echo "$root/paper/venue.md" ;;
        claims)       echo "$root/paper/claims.md" ;;
        outline)      echo "$root/paper/outline.md" ;;
        figures)      echo "$root/paper/figures.md" ;;
    esac
}

missing=()
for a in "${required[@]}"; do
    [ -f "$(path_for "$a")" ] || missing+=("$a")
done
warnings=()
for a in "${recommended[@]+"${recommended[@]}"}"; do
    [ -f "$(path_for "$a")" ] || warnings+=("$a")
done

mkdir -p "$root/paper"

ok=true
[ ${#missing[@]} -eq 0 ] || ok=false

printf '{"ok":%s,"phase":"%s","root":"%s","paper_dir":"%s",' \
    "$ok" "$phase" "$(json_escape "$root")" "$(json_escape "$root/paper")"
printf '"constitution":"%s","venue":"%s","claims":"%s","outline":"%s","figures":"%s",' \
    "$(json_escape "$(path_for constitution)")" "$(json_escape "$(path_for venue)")" \
    "$(json_escape "$(path_for claims)")" "$(json_escape "$(path_for outline)")" \
    "$(json_escape "$(path_for figures)")"
printf '"missing":%s,"recommended_missing":%s}\n' \
    "$(json_array "${missing[@]+"${missing[@]}"}")" \
    "$(json_array "${warnings[@]+"${warnings[@]}"}")"

[ "$ok" = true ] && exit 0
exit 1
