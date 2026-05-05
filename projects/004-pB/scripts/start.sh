#!/usr/bin/env bash
# scripts/start.sh — 启动脚本
# 结论: 封装日常启动命令，绑定 127.0.0.1（架构不变量 #7）
# 细节:
#   - 检查 .env 存在（首次运行提醒）
#   - 检查 DECISION_LEDGER_HOME 目录（自动创建）
#   - 用 uv run 在虚拟环境中启动
#   - 不接受 0.0.0.0 绑定（架构不变量 #7）

set -euo pipefail

# ── 脚本所在目录（相对路径安全）──────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

# ── .env 检查 ─────────────────────────────────────────────
if [[ ! -f ".env" ]]; then
    echo "❌ 找不到 .env 文件。请先执行:"
    echo "   cp .env.example .env"
    echo "   # 然后填入 ANTHROPIC_API_KEY 和 TELEGRAM_BOT_TOKEN"
    exit 1
fi

# ── DECISION_LEDGER_HOME 创建 ────────────────────────────
DL_HOME="${DECISION_LEDGER_HOME:-${HOME}/decision_ledger}"
mkdir -p "${DL_HOME}/inbox"
mkdir -p "${DL_HOME}/llm_cache"
mkdir -p "${DL_HOME}/backups"
mkdir -p "${DL_HOME}/logs"

echo "✅ 数据目录: ${DL_HOME}"
echo "✅ 启动决策账本 (bind=127.0.0.1:8000)..."
echo "   浏览器打开: http://localhost:8000"
echo "   Ctrl+C 停止"
echo ""

# 结论: 永远绑定 127.0.0.1，不接 0.0.0.0（架构不变量 #7）
exec uv run python -m decision_ledger.main
