#!/usr/bin/env bash
# worker pre_pip_install hook · T012 stub, T015 扩展
# 职责：仅放行 requirements-locked.txt --require-hashes 的 pip install
# C17 / R5：供应链锁定；防止 worker 随意安装未锁定依赖
#
# Hook 协议：同 pre_tool_use.sh（stdin JSON）
# T015 将完善 allowlist 详细逻辑。

set -euo pipefail

echo "[pre_pip_install] checking requirements-locked.txt..." >&2

# 读取 stdin（Claude Code hook 协议 JSON）
INPUT="$(cat)"

COMMAND=$(echo "$INPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
cmd = data.get('input', {}).get('command', data.get('command', ''))
print(cmd)
" 2>/dev/null || echo "")

# 仅检查包含 pip install 的命令
if echo "$COMMAND" | grep -qE '(pip install|pip3 install|python -m pip install)'; then
    # allowlist（T015 会扩展）
    # 目前仅允许：pip install -r requirements-locked.txt --require-hashes
    #            uv pip install -r requirements-locked.txt --require-hashes
    #            uv sync --frozen
    ALLOWED_PATTERNS=(
        '^pip install -r requirements-locked\.txt --require-hashes'
        '^uv pip install -r requirements-locked\.txt --require-hashes'
        '^uv sync --frozen'
    )

    MATCHED=0
    for PATTERN in "${ALLOWED_PATTERNS[@]}"; do
        # 去掉命令前后空白再匹配
        TRIMMED=$(echo "$COMMAND" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        if echo "$TRIMMED" | grep -qE "$PATTERN"; then
            MATCHED=1
            break
        fi
    done

    if [[ "$MATCHED" -eq 0 ]]; then
        echo "[pre_pip_install] DENIED: pip install must use requirements-locked.txt --require-hashes" >&2
        echo "[pre_pip_install] command was: ${COMMAND:0:120}" >&2
        exit 2
    fi
fi

# T015 will enforce --require-hashes + locked file (full implementation)
exit 0
