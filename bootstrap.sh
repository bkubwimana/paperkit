#!/usr/bin/env bash
# Compatibility wrapper: set up or upgrade paperkit in a paper repository
# without installing the pk CLI. Prefer `uv tool install` and `pk init`.
#
# Usage: bootstrap.sh TARGET_REPO [pk init options]

set -euo pipefail

KIT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-}"
if [ -z "$TARGET" ] || [ ! -d "$TARGET" ]; then
    echo "usage: $0 TARGET_REPO [pk init options]" >&2
    exit 2
fi
shift

py="$(command -v python3 || command -v python)" || { echo "python3 not found" >&2; exit 2; }
export PYTHONPATH="$KIT/src${PYTHONPATH:+:$PYTHONPATH}"

if [ -f "$TARGET/.paperkit/manifest.json" ] || [ -d "$TARGET/.paperkit" ]; then
    cd "$TARGET"
    exec "$py" -m paperkit upgrade "$@"
fi
exec "$py" -m paperkit init "$TARGET" "$@"
