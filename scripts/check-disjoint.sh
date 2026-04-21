#!/usr/bin/env bash
# check-disjoint.sh — Verify that parallel-kickoff candidate tasks have disjoint file_domain.
# Usage: ./scripts/check-disjoint.sh <idea-number> T003 T004 T008
# Exit 0 = safe to parallelize; exit 1 = collision detected.

set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <idea-number> <task-id> <task-id> [<task-id>...]"
  echo "Example: $0 001 T003 T004 T008"
  exit 2
fi

IDEA="$1"
shift
TASKS=("$@")

# Find the spec directory
SPEC_DIR=$(find specs -maxdepth 1 -type d -name "${IDEA}-*" | head -1)
if [[ -z "$SPEC_DIR" ]]; then
  echo "Error: no specs/${IDEA}-* directory found"
  exit 2
fi

echo "Checking file_domain disjointness for tasks in ${SPEC_DIR}:"
echo "  Tasks: ${TASKS[*]}"
echo ""

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Extract each task's file_domain into a per-task file
for tid in "${TASKS[@]}"; do
  TFILE="${SPEC_DIR}/tasks/${tid}.md"
  if [[ ! -f "$TFILE" ]]; then
    echo "✗ Task file not found: $TFILE"
    exit 2
  fi
  # Parse the file_domain: bullet list under the "file_domain:" key
  awk '
    /^\*\*file_domain\*\*:/ { inlist=1; next }
    /^---$/ && inlist { inlist=0 }
    inlist && /^  - / { sub(/^  - /, ""); print }
  ' "$TFILE" > "${TMPDIR}/${tid}.txt"

  if [[ ! -s "${TMPDIR}/${tid}.txt" ]]; then
    echo "⚠ Task $tid has no file_domain declared — unsafe to parallelize"
    exit 1
  fi

  echo "  $tid touches:"
  sed 's/^/    /' "${TMPDIR}/${tid}.txt"
done
echo ""

# Build a combined list: "<pattern>\t<task>"
> "${TMPDIR}/all.txt"
for tid in "${TASKS[@]}"; do
  while IFS= read -r line; do
    printf "%s\t%s\n" "$line" "$tid" >> "${TMPDIR}/all.txt"
  done < "${TMPDIR}/${tid}.txt"
done

# Find patterns claimed by >1 task
COLLISIONS=$(awk -F'\t' '{ counts[$1]++; tasks[$1] = tasks[$1] " " $2 }
                        END { for (p in counts) if (counts[p] > 1) print p "|" tasks[p] }' \
              "${TMPDIR}/all.txt")

if [[ -n "$COLLISIONS" ]]; then
  echo "✗ COLLISION DETECTED"
  echo ""
  echo "$COLLISIONS" | while IFS='|' read -r pattern tasks; do
    echo "  Pattern '$pattern' claimed by tasks:$tasks"
  done
  echo ""
  echo "Resolution options:"
  echo "  1. Split the tasks further so domains are disjoint"
  echo "  2. Sequentialize these tasks (run one after another, not in parallel)"
  echo "  3. If the collision is a shared-infrastructure file (e.g. package.json),"
  echo "     move its modification into a dedicated Phase-0 task that others depend on."
  exit 1
fi

echo "✓ No collisions. Tasks are safe to parallelize."
exit 0
