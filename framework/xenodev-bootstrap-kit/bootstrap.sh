#!/usr/bin/env bash
# XenoDev bootstrap script
# per ideababy_stroller framework/xenodev-bootstrap-kit/
# Run this in /Users/admin/codes/XenoDev/ AFTER `mkdir XenoDev && cd XenoDev`

set -euo pipefail

IDS_KIT="/Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit"

# === Sanity check: 必须在 XenoDev 目录跑(防 IDS 仓里误跑) ===
CWD="$(pwd)"
if [[ "$CWD" != *"XenoDev"* ]]; then
    echo "ERROR: bootstrap.sh must run inside XenoDev directory."
    echo "       current pwd: $CWD"
    echo "       expected: /Users/admin/codes/XenoDev (or similar)"
    exit 1
fi

if [[ "$CWD" == *"ideababy_stroller"* ]]; then
    echo "ERROR: do NOT run bootstrap.sh inside ideababy_stroller."
    echo "       This script bootstraps a NEW XenoDev repo, not modifies IDS."
    exit 1
fi

# === Check kit source exists ===
if [[ ! -d "$IDS_KIT" ]]; then
    echo "ERROR: IDS bootstrap kit not found at $IDS_KIT"
    echo "       did you clone ideababy_stroller? did the path change?"
    exit 1
fi

echo "→ XenoDev bootstrap starting in $CWD"
echo "→ kit source: $IDS_KIT"
echo

# === Step 1: git init(若未 init)===
if [[ ! -d .git ]]; then
    git init -b main
    echo "✓ Step 1: git init -b main"
else
    echo "✓ Step 1: git already initialized (skipping init)"
fi

# === Step 2: cp 顶级文件 ===
cp "$IDS_KIT/AGENTS.md"            .
cp "$IDS_KIT/CLAUDE.md"            .
cp "$IDS_KIT/README.md.template"   README.md
cp "$IDS_KIT/LICENSE.template"     LICENSE
cp "$IDS_KIT/.gitignore.template"  .gitignore
echo "✓ Step 2: top-level files copied (AGENTS / CLAUDE / README / LICENSE / .gitignore)"

# === Step 3: .claude/ 骨架 ===
mkdir -p .claude/hooks .claude/safety-floor .claude/skills .claude/commands
echo "✓ Step 3: .claude/ skeleton created"

# === Step 4: cp Safety Floor 件 2(block-dangerous.sh)===
cp "$IDS_KIT/safety-floor-2/block-dangerous.sh" .claude/hooks/block-dangerous.sh
chmod +x .claude/hooks/block-dangerous.sh
echo "✓ Step 4: block-dangerous.sh installed (mirror from autodev_pipe)"

# === Step 5: cp Safety Floor 件 1 + 件 3 ===
cp -r "$IDS_KIT/safety-floor-1/" .claude/safety-floor/credential-isolation/
cp -r "$IDS_KIT/safety-floor-3/" .claude/safety-floor/backup-detection/
echo "✓ Step 5: safety floor 件 1 + 件 3 installed"

# === Step 6: cp lib/(workspace-schema + eval-event-log + handback-validator)===
mkdir -p lib
cp -r "$IDS_KIT/workspace-schema/"   lib/workspace-schema/
cp -r "$IDS_KIT/eval-event-log/"     lib/eval-event-log/
cp -r "$IDS_KIT/handback-validator/" lib/handback-validator/
echo "✓ Step 6: lib/ installed (workspace-schema + eval-event-log + handback-validator)"

# === Step 7: 创建 .claude/settings.json 模板(注册 block-dangerous.sh hook)===
if [[ ! -f .claude/settings.json ]]; then
    cat > .claude/settings.json <<'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-dangerous.sh"
          }
        ]
      }
    ]
  }
}
EOF
    echo "✓ Step 7: .claude/settings.json created (block-dangerous.sh hook registered)"
else
    echo "✓ Step 7: .claude/settings.json already exists (skipping)"
fi

# === Step 8: 准备 .eval/ 目录(append-only event log)===
mkdir -p .eval
touch .eval/.keep   # 让 git 看见空目录(.eval/events.jsonl 在 .gitignore 中)
echo "✓ Step 8: .eval/ directory ready"

# === Step 9: 初始 commit ===
git add .
git commit -m "chore: XenoDev bootstrap from ideababy_stroller framework/xenodev-bootstrap-kit/

per discussion/006/forge/v2/stage-forge-006-v2.md verdict
contract_version (mirror): SHARED-CONTRACT v2.0 ACTIVE-but-not-battle-tested
provenance: bootstrap.sh from \$IDS_KIT

Status: ready for B2.2 (first PRD ship + hand-back round-trip)"

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ XenoDev bootstrap complete!"
echo
echo "📋 Next steps:"
echo "  1. 验证 (本目录跑):"
echo "     test -x .claude/hooks/block-dangerous.sh && echo PASS"
echo "     test -d lib/handback-validator && echo PASS"
echo "     git log --oneline | head -1"
echo
echo "  2. 起 B2.2 sub-plan(operator 决定时机):"
echo "     - operator 手补 PRD §Real constraints + §Open questions"
echo "     - cp PRD 进 XenoDev/PRD.md"
echo "     - 起 spec-writer / task-decomposer / parallel-builder skill"
echo "     - 跑首个真 task → ship → hand-back round-trip"
echo
echo "  3. 跨仓引用:"
echo "     - IDS:   /Users/admin/codes/ideababy_stroller (SSOT)"
echo "     - kit 源: \$IDS_KIT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
