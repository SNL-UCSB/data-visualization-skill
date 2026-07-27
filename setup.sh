#!/bin/bash
# Install the data-visualization skill for Claude Code
# Usage: ./setup.sh

set -e

SKILL_DIR="${HOME}/.claude/skills/viz"

echo "Installing data-visualization skill to ${SKILL_DIR}..."

mkdir -p "${SKILL_DIR}/reference"

# Copy skill file
cp SKILL.md "${SKILL_DIR}/SKILL.md"

# Copy ALL reference materials (copy the directory contents, not a hand-maintained list —
# an enumerated list silently goes stale whenever a reference file is added, which is how the
# installed copy and this repo drift apart).
cp -R reference/. "${SKILL_DIR}/reference/"

echo "Done. The /viz skill is now available in Claude Code."
echo ""
echo "Usage:"
echo "  /viz brainstorm  — Think through what to visualize"
echo "  /viz plan        — Decide plot type, layout, data source"
echo "  /viz execute     — Generate code, run it, reflect"
