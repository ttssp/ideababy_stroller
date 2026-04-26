#!/usr/bin/env bash
# proxyman_fetch.sh — T006 Q5 RESOLVED
# 结论: 将 Proxyman 捕获的咨询师 PDF 拷贝到 ~/decision_ledger/inbox/
# 细节:
#   - 主入口: human 在 Proxyman 看到 PDF 响应后，手动运行此脚本拖入
#   - 备用: 也可直接把 PDF 文件拖到 ~/decision_ledger/inbox/ 目录
#   - R2: 含 Alfred / Raycast 快捷键绑定示例
#
# 使用方式:
#   ./scripts/proxyman_fetch.sh [PDF 路径]
#   ./scripts/proxyman_fetch.sh ~/Downloads/advisor_2026w17.pdf
#
# R2 快捷键绑定示例:
#
# Alfred Workflow (File Action):
#   1. Alfred Preferences → Workflows → + → File & App → File Action Workflow
#   2. File Action: "Copy to Decision Ledger Inbox"
#   3. Run Script: /bin/bash -c "~/path/to/scripts/proxyman_fetch.sh '{query}'"
#   4. 在 Finder 选中 PDF → Alfred → 选 "Copy to Decision Ledger Inbox"
#
# Raycast Extension / Script Command:
#   1. Raycast → Extensions → Script Commands → + → New Script Command
#   2. Name: "Fetch to Decision Ledger"
#   3. Script Path: /path/to/proxyman_fetch.sh
#   4. Argument: Required (PDF 路径)
#   5. 在 Raycast 搜索 "Fetch to Decision Ledger"，输入 PDF 路径

set -euo pipefail

# ── 配置 ────────────────────────────────────────────────────────────────
INBOX_DIR="${DECISION_LEDGER_HOME:-$HOME/decision_ledger}/inbox"

# ── 帮助信息 ─────────────────────────────────────────────────────────────
usage() {
    echo "用法: $(basename "$0") [PDF 路径]"
    echo ""
    echo "将 PDF 文件复制到 decision_ledger inbox，触发自动解析流程。"
    echo ""
    echo "环境变量:"
    echo "  DECISION_LEDGER_HOME  decision_ledger 根目录 (默认: ~/decision_ledger)"
    echo ""
    echo "示例:"
    echo "  $(basename "$0") ~/Downloads/advisor_2026w17.pdf"
    echo "  $(basename "$0") /tmp/proxyman_response.pdf"
    echo ""
    echo "R2 快捷键: 详见脚本顶部注释 (Alfred / Raycast 示例)"
    exit 0
}

# ── 参数校验 ─────────────────────────────────────────────────────────────
if [[ $# -eq 0 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    usage
fi

PDF_PATH="$1"

if [[ ! -f "$PDF_PATH" ]]; then
    echo "错误: 文件不存在: $PDF_PATH" >&2
    exit 1
fi

if [[ "${PDF_PATH##*.}" != "pdf" && "${PDF_PATH##*.}" != "PDF" ]]; then
    echo "警告: 文件扩展名不是 .pdf，仍然复制: $PDF_PATH" >&2
fi

# ── 创建 inbox 目录 ───────────────────────────────────────────────────────
mkdir -p "$INBOX_DIR"

# ── 复制 PDF 到 inbox ─────────────────────────────────────────────────────
FILENAME=$(basename "$PDF_PATH")
DEST="$INBOX_DIR/$FILENAME"

# 防止文件名冲突：若同名文件已存在，加时间戳前缀
if [[ -f "$DEST" ]]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    DEST="$INBOX_DIR/${TIMESTAMP}_${FILENAME}"
    echo "文件已存在，重命名为: $(basename "$DEST")"
fi

cp "$PDF_PATH" "$DEST"
echo "OK: PDF 已写入 inbox → $DEST"
echo "WatchedFolderWatcher 将在 5s 内检测到并开始解析。"

# ── 可选: Proxyman CLI 集成 ───────────────────────────────────────────────
# TODO: 如需从 Proxyman 直接导出，取消下面注释并自定义:
# proxyman export --flow-id "$PROXYMAN_FLOW_ID" --output "$DEST"
# 参见 Proxyman CLI 文档: https://docs.proxyman.io/cli/introduction
