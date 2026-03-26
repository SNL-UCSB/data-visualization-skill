#!/bin/bash
# Install the data-visualization skill for Claude Code
# Usage: ./setup.sh

set -e

SKILL_DIR="${HOME}/.claude/skills/viz"

echo "Installing data-visualization skill to ${SKILL_DIR}..."

mkdir -p "${SKILL_DIR}/reference"

# Copy skill file
cp SKILL.md "${SKILL_DIR}/SKILL.md"

# Copy reference materials
cp reference/before_you_plot.md "${SKILL_DIR}/reference/before_you_plot.md"
cp reference/plot_context_template.md "${SKILL_DIR}/reference/plot_context_template.md"
cp reference/matplotlib_defaults.py "${SKILL_DIR}/reference/matplotlib_defaults.py"

echo "Done. The /viz skill is now available in Claude Code."
echo ""
echo "Usage:"
echo "  /viz brainstorm  — Think through what to visualize"
echo "  /viz plan        — Decide plot type, layout, data source"
echo "  /viz execute     — Generate code, run it, reflect"
