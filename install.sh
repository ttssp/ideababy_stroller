#!/usr/bin/env bash
# install.sh — One-shot bootstrap for Idea Incubator.
# Run from the repo root after extracting the tarball.

set -euo pipefail

echo "=== Idea Incubator — install ==="

# --- 1. Ensure AGENTS.md symlink for Codex ---
if [[ ! -e AGENTS.md ]]; then
  ln -s CLAUDE.md AGENTS.md
  echo "✓ Created AGENTS.md → CLAUDE.md symlink"
else
  echo "• AGENTS.md already exists, skipping symlink"
fi

# --- 2. Make scripts executable ---
if [[ -d scripts ]]; then
  chmod +x scripts/*.sh 2>/dev/null || true
  echo "✓ scripts/ made executable"
fi

# --- 3. Verify prerequisites ---
echo ""
echo "=== Checking prerequisites ==="
check() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "  ✓ $1: $(command -v "$1")"
  else
    echo "  ✗ $1: NOT FOUND"
    MISSING=1
  fi
}
MISSING=0
check git
check rg
check node
check claude
check codex
check gh

if [[ "$MISSING" == "1" ]]; then
  echo ""
  echo "⚠ Some tools are missing. See PLAYBOOK.md §0.2 for install commands."
fi

# --- 4. Git init if needed ---
if [[ ! -d .git ]]; then
  read -p "Initialize git repo here? [y/N] " answer
  if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    git init
    git add -A
    git commit -m "chore: bootstrap idea-incubator skeleton" || true
    echo "✓ Git repo initialized"
  fi
fi

# --- 5. Reminder about plugins ---
cat <<'EOF'

=== Next steps ===

1. Install codex-plugin-cc (run inside Claude Code):
     claude
     > /plugin marketplace add openai/codex-plugin-cc
     > /plugin install codex@openai-codex
     > /codex:setup   # verifies Codex is reachable

2. (Optional) Enable agent teams:
     export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

3. Read PLAYBOOK.md top to bottom once.

4. Start your first idea:
     claude
     > /propose

Done. Good luck — now go pick an idea worth betting on.
EOF
