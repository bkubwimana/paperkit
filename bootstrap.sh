#!/usr/bin/env bash
# Install or upgrade paperkit in a paper repository.
#
# Usage: bootstrap.sh TARGET_REPO
#
# Copies .paperkit/ and the phase skills into TARGET_REPO, creates paper/, and
# points the repo's agent instructions at .paperkit/AGENTS.md.
#
# Safe to re-run. Never overwrites files under .paperkit/memory/ (your
# constitution and banned terms) or anything under paper/.

set -euo pipefail

KIT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-}"
if [ -z "$TARGET" ] || [ ! -d "$TARGET" ]; then
    echo "usage: $0 TARGET_REPO (an existing directory)" >&2
    exit 2
fi
TARGET="$(cd -- "$TARGET" && pwd)"
if [ "$TARGET" = "$KIT" ]; then
    echo "refusing to install paperkit into itself" >&2
    exit 2
fi

version="unknown"
if git -C "$KIT" rev-parse --short HEAD >/dev/null 2>&1; then
    version="$(git -C "$KIT" rev-parse --short HEAD)"
fi

echo "paperkit $version -> $TARGET"

# 1. Kit files that are safe to replace on upgrade.
for sub in venues templates scripts; do
    mkdir -p "$TARGET/.paperkit/$sub"
    cp -R "$KIT/.paperkit/$sub/." "$TARGET/.paperkit/$sub/"
done
cp "$KIT/AGENTS.md" "$TARGET/.paperkit/AGENTS.md"
chmod +x "$TARGET"/.paperkit/scripts/bash/*.sh 2>/dev/null || true

# 2. User-owned files: copy only if absent.
mkdir -p "$TARGET/.paperkit/memory"
for f in "$KIT"/.paperkit/memory/*; do
    name="$(basename "$f")"
    if [ -e "$TARGET/.paperkit/memory/$name" ]; then
        echo "  kept      .paperkit/memory/$name"
    else
        cp "$f" "$TARGET/.paperkit/memory/$name"
        echo "  installed .paperkit/memory/$name"
    fi
done

# 3. Phase skills for Claude Code.
mkdir -p "$TARGET/.claude/skills"
for d in "$KIT"/skills/*/; do
    name="$(basename "$d")"
    mkdir -p "$TARGET/.claude/skills/$name"
    cp "$d/SKILL.md" "$TARGET/.claude/skills/$name/SKILL.md"
    echo "  skill     /$name"
done

# 4. Working directory for the artifacts.
mkdir -p "$TARGET/paper"

# 5. Point agent instructions at the kit, without clobbering existing ones.
marker="paperkit: read .paperkit/AGENTS.md"
add_pointer() {
    local file="$1" line="$2"
    if [ -f "$file" ] && grep -qF "$marker" "$file"; then
        echo "  pointer   already in $(basename "$file")"
        return
    fi
    {
        [ -s "$file" ] && printf '\n'
        printf '<!-- %s -->\n%s\n' "$marker" "$line"
    } >> "$file"
    echo "  pointer   added to $(basename "$file")"
}
had_agents=0
[ -f "$TARGET/AGENTS.md" ] && had_agents=1
had_claude=0
[ -f "$TARGET/CLAUDE.md" ] && had_claude=1

add_pointer "$TARGET/AGENTS.md" \
    "Paper writing in this repository follows paperkit. Read \`.paperkit/AGENTS.md\` before editing any paper text, figure or number."

# A new CLAUDE.md must keep loading the repo's own AGENTS.md, or Claude Code
# would see the kit's rules and lose the project's.
if [ $had_claude -eq 0 ] && [ $had_agents -eq 1 ]; then
    printf '@AGENTS.md\n' > "$TARGET/CLAUDE.md"
    echo "  created   CLAUDE.md importing the existing AGENTS.md"
fi
add_pointer "$TARGET/CLAUDE.md" "@.paperkit/AGENTS.md"

echo "$version" > "$TARGET/.paperkit/VERSION"

echo
echo "Done. Next: review .paperkit/memory/constitution.md, then run /paper-venue."
