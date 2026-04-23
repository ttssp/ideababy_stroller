#!/usr/bin/env bash
# codex-inbox-init.sh — first-time setup for the Codex inbox/outbox bus.
# Run once after cloning the repo.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

echo "=== Codex Inbox 初始化 ==="

# 1. 确保目录存在
mkdir -p .codex-inbox .codex-outbox
echo "✓ .codex-inbox/ 和 .codex-outbox/ 已就位"

# 2. 创建 latest.md 占位（symlink）
if [[ ! -e .codex-inbox/latest.md ]]; then
  cat > .codex-inbox/latest.md <<'EOF'
# Codex Inbox · placeholder

(no task yet — Claude Code will write here when needed)
EOF
  echo "✓ .codex-inbox/latest.md placeholder created"
fi

# 3. .gitignore 处理（inbox/outbox 内容可以不入 git，README 入 git）
if ! grep -q "^.codex-inbox/" .gitignore 2>/dev/null; then
  cat >> .gitignore <<'EOF'

# Codex inbox/outbox bus (READMEs are tracked, contents are local)
.codex-inbox/*
!.codex-inbox/README.md
.codex-outbox/*
!.codex-outbox/README.md
EOF
  echo "✓ .gitignore 已更新"
fi

# 4. 提示 alias 设置
cat <<'TIP'

=== 下一步：在 Codex 终端配置 alias（一次性）===

在你的 shell 配置文件（~/.zshrc 或 ~/.bashrc）追加：

  # Codex Inbox 快捷
  alias cdx-run='codex "read .codex-inbox/latest.md and execute exactly what it says, then write a corresponding .codex-outbox/<same-filename>.md confirming what you did"'
  alias cdx-peek='ls -lt .codex-inbox/ | head -5 && echo "---" && cat .codex-inbox/latest.md | head -50'

然后 source 一下：
  source ~/.zshrc   # 或 ~/.bashrc

之后每次 Claude Code 说 "Codex 任务已就绪"，你在 Codex 终端只需敲：
  cdx-run

=== 完成 ===
TIP
