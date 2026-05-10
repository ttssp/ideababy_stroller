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

# === Step 6.5: cp framework SSOT mirror(SHARED-CONTRACT.md 字节级 mirror + provenance 文件)===
# B2.2 Block D friction F3 fix(006a-pM session 实证):
# AGENTS.md §4 + CLAUDE.md §"跨仓引用" 写 "framework/SHARED-CONTRACT.md 是 IDS SSOT 字节级 mirror",
# 但 bootstrap.sh 之前不带 framework/ 目录 → 每个 XenoDev session 首跑都重发现 mirror 缺位。
# 本 Step 在 bootstrap 时就落 mirror + 校验 + 落 provenance,避免重复 friction。
IDS_FRAMEWORK_DIR="$(cd "$IDS_KIT/.." && pwd)"
IDS_REPO_ROOT="$(cd "$IDS_FRAMEWORK_DIR/.." && pwd)"
SSOT_SRC="$IDS_FRAMEWORK_DIR/SHARED-CONTRACT.md"
if [[ ! -f "$SSOT_SRC" ]]; then
    echo "ERROR: Step 6.5 IDS SSOT not found: $SSOT_SRC"
    exit 1
fi
mkdir -p framework
cp "$SSOT_SRC" framework/SHARED-CONTRACT.md
# 字节级校验
SSOT_BYTES="$(wc -c < "$SSOT_SRC" | tr -d ' ')"
MIRROR_BYTES="$(wc -c < framework/SHARED-CONTRACT.md | tr -d ' ')"
SSOT_SHA="$(shasum -a 256 "$SSOT_SRC" | awk '{print $1}')"
MIRROR_SHA="$(shasum -a 256 framework/SHARED-CONTRACT.md | awk '{print $1}')"
if [[ "$SSOT_BYTES" != "$MIRROR_BYTES" || "$SSOT_SHA" != "$MIRROR_SHA" ]]; then
    echo "ERROR: Step 6.5 mirror integrity check FAILED"
    echo "  SSOT bytes=$SSOT_BYTES sha=$SSOT_SHA"
    echo "  mirror bytes=$MIRROR_BYTES sha=$MIRROR_SHA"
    exit 1
fi
# 落 MIRROR-PROVENANCE.md(per 006a-pM friction-report D2 闭环范式)
cat > framework/MIRROR-PROVENANCE.md <<EOF
# framework/ mirror provenance

> framework/ 下的文件是 ideababy_stroller(IDS · SSOT)的**只读字节级 mirror**。XenoDev 不修改这些文件;只在 IDS 改后由 operator 重新 cp。

## Mirror 列表

| 文件 | IDS 源路径 | mirror bootstrap 时 sha256 | bytes |
|---|---|---|---|
| SHARED-CONTRACT.md | $SSOT_SRC | $MIRROR_SHA | $MIRROR_BYTES |

## 校验命令(operator 任意时点跑,验是否 drift)

\`\`\`bash
diff -q $SSOT_SRC framework/SHARED-CONTRACT.md
shasum -a 256 framework/SHARED-CONTRACT.md
# 期望 sha256: $MIRROR_SHA
\`\`\`

## 重 cp 触发条件

- IDS \`framework/SHARED-CONTRACT.md\` 改了(operator 在 IDS commit 后通知 / XenoDev session 跑 \`diff -q\` 发现 drift)
- 重 cp 命令:\`cp $SSOT_SRC framework/SHARED-CONTRACT.md && shasum -a 256 framework/SHARED-CONTRACT.md\`

## 失败处置

- diff 不一致 = drift → operator 决:从 IDS 重 cp(若 IDS 是真新版本)/ 不动(若 XenoDev 仍按旧 contract 跑且无 break)
- bootstrap 时 sha 不一致 = bootstrap.sh bug → 报 IDS

## bootstrap 时点

- 时间:$(date -u +%Y-%m-%dT%H:%M:%SZ)
- IDS 仓:$IDS_REPO_ROOT
EOF
echo "✓ Step 6.5: framework/SHARED-CONTRACT.md mirror installed (sha256: ${MIRROR_SHA:0:16}... · $MIRROR_BYTES bytes) + MIRROR-PROVENANCE.md"

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

# === Step 8.5: 装 pre-commit credential hook(初始 commit 前必装,防 prod:// 进首 commit)===
# B2.2 Block A.6 codex round 3 finding #3 fix:
# 旧版本先 git commit,再让 operator 手装 hook → 首 commit 不受 Safety Floor 件 1 保护。
# 新版本:bootstrap.sh 自己装 hook(symlink 到 .git/hooks/pre-commit)+ 跑一次 scan-credentials.sh,
#       任一失败 → 整个 bootstrap exit 1,不创建首 commit。
HOOK_TARGET=".git/hooks/pre-commit"
HOOK_SOURCE=".claude/safety-floor/credential-isolation/pre-commit-credential.sh"
if [[ -f "$HOOK_TARGET" || -L "$HOOK_TARGET" ]]; then
    echo "  ⚠ $HOOK_TARGET already exists (overwriting; 旧 hook 备份到 ${HOOK_TARGET}.bak)"
    mv "$HOOK_TARGET" "${HOOK_TARGET}.bak"
fi
# 用相对路径 symlink(可移植性优于绝对路径)
ln -s "../../$HOOK_SOURCE" "$HOOK_TARGET"
chmod +x "$HOOK_SOURCE"  # 确保 hook 可执行
if [[ ! -x "$HOOK_TARGET" ]]; then
    echo "ERROR: Step 8.5 装 pre-commit hook 失败: $HOOK_TARGET 不可执行"
    exit 1
fi
echo "✓ Step 8.5: pre-commit credential hook installed (symlink → $HOOK_SOURCE)"

# 立即跑一次 full scan-credentials.sh 在所有待 commit 文件上(不只 staged):
# 这是 first-commit 保护(此时 staged 为空,也无 working tree 改动 — 跑全仓 scan)
SCAN_SCRIPT=".claude/safety-floor/credential-isolation/scan-credentials.sh"
if [[ -x "$SCAN_SCRIPT" ]]; then
    if ! bash "$SCAN_SCRIPT" . >/dev/null 2>&1; then
        echo "ERROR: Step 8.5 scan-credentials.sh 在 bootstrap 工作区发现凭据,bootstrap 中止"
        echo "       检查 stderr 输出:"
        bash "$SCAN_SCRIPT" . >&2 || true
        exit 1
    fi
    echo "✓ Step 8.5: scan-credentials.sh PASS (无 prod credential)"
else
    echo "ERROR: Step 8.5 scan-credentials.sh not found / not executable: $SCAN_SCRIPT"
    exit 1
fi

# === Step 9: 初始 commit(此时 hook 已装且 PASS,commit 受 Safety Floor 保护)===
git add .
git commit -m "chore: XenoDev bootstrap from ideababy_stroller framework/xenodev-bootstrap-kit/

per discussion/006/forge/v2/stage-forge-006-v2.md verdict
contract_version (mirror): SHARED-CONTRACT v2.0 ACTIVE-but-not-battle-tested
provenance: bootstrap.sh from \$IDS_KIT
pre-commit hook (credential): installed (Step 8.5)

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
