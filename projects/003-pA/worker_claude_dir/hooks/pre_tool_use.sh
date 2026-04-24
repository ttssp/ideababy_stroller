#!/usr/bin/env bash
# worker pre_tool_use hook · T012 stub, T014 扩展
# 职责：拦截危险 Bash 命令（deny 清单）——读取 Claude Code hook JSON 协议 stdin
# C21 / R6：配合 fail-closed 只读分离，提供 hooks 层第三道防线
#
# Hook 协议（Claude Code 2026-04-latest）：
#   stdin: JSON {"tool":{"name":"<ToolName>"},"input":{"command":"<bash cmd>",...}}
#   exit 0  → 允许
#   exit 2  → deny（Claude Code 将报 PermissionError 给 worker）
#
# T014 将扩展本脚本，加入完整正则 deny 清单。
# 本版本（T012 stub）实现最小可工作的拒绝逻辑。

set -euo pipefail

# 读取 stdin（Claude Code hook 协议 JSON）
INPUT="$(cat)"

# 提取工具名和命令（使用 python3 解析 JSON，避免依赖 jq）
TOOL_NAME=$(echo "$INPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('tool', {}).get('name', data.get('tool_name', 'unknown')))
" 2>/dev/null || echo "unknown")

COMMAND=$(echo "$INPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
# 兼容 tool/input 嵌套和扁平结构
cmd = data.get('input', {}).get('command', data.get('command', ''))
print(cmd)
" 2>/dev/null || echo "")

echo "[pre_tool_use] tool=${TOOL_NAME} command=${COMMAND:0:80}" >&2

# 仅当工具为 Bash 时检查命令
if [[ "$TOOL_NAME" == "Bash" ]]; then
    # deny 模式列表（T014 会扩展）
    # 危险命令正则匹配（bash ERE 语法）
    DENY_PATTERNS=(
        'rm[[:space:]]+-rf'          # rm -rf 任意路径
        'rm[[:space:]]+-fr'          # rm -fr 变体
        'curl[[:space:]]'            # 外部 curl 请求
        'wget[[:space:]]'            # 外部 wget 请求
        'cat[[:space:]].*\.env'      # cat .env 文件
        'chmod[[:space:]]'           # chmod 改权限（绕过只读）
        'chflags[[:space:]]'         # chflags（macOS immutable flag）
        'chattr[[:space:]]'          # chattr（Linux immutable flag）
        'sudo[[:space:]]'            # sudo 提权
    )

    for PATTERN in "${DENY_PATTERNS[@]}"; do
        if echo "$COMMAND" | grep -qE "$PATTERN"; then
            echo "[pre_tool_use] DENIED: command matches deny pattern '${PATTERN}'" >&2
            exit 2
        fi
    done
fi

# 未命中任何 deny 规则 → 放行
exit 0
