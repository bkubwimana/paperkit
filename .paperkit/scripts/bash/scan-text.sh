#!/usr/bin/env bash
# Scan the paper source for placeholders and banned vocabulary.
#
# Usage: scan-text.sh [--ext .tex,.bib] [ROOT]
# ROOT defaults to the directory containing .paperkit/.

set -u
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
. "$SCRIPT_DIR/common.sh"

ext=".tex"
root=""
while [ $# -gt 0 ]; do
    case "$1" in
        --ext) ext="${2:-.tex}"; shift 2 ;;
        -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
        *) root="$1"; shift ;;
    esac
done

if [ -z "$root" ]; then
    root="$(find_paperkit_root)" || { echo "no .paperkit directory found" >&2; exit 2; }
fi

py="$(command -v python3 || command -v python)" || { echo "python3 not found" >&2; exit 2; }
exec "$py" "$SCRIPT_DIR/scan_text.py" "$root" --ext "$ext"
