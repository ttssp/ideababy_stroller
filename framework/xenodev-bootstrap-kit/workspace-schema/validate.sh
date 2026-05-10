#!/usr/bin/env bash
# validate.sh — workspace 4 字段校验
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2 + workspace-schema.json
#
# Usage: validate.sh <handoff-or-handback-file.md>
#   exit 0 if 4 fields all present + all values absolute paths
#   exit 1 if invalid + stderr lists which field failed
#
# 单人 dev 环境无 npm install 假设 → 退化为 grep + bash 校验,不强依赖 ajv

set -euo pipefail

FILE="${1:-}"

if [[ -z "$FILE" ]]; then
    echo "Usage: validate.sh <file.md>" >&2
    exit 2
fi

if [[ ! -f "$FILE" ]]; then
    echo "ERROR: file not found: $FILE" >&2
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTRACT="$SCRIPT_DIR/extract.sh"

if [[ ! -x "$EXTRACT" ]]; then
    echo "ERROR: extract.sh not found or not executable: $EXTRACT" >&2
    exit 2
fi

# 提取 workspace 块
WS_BLOCK="$(bash "$EXTRACT" "$FILE" 2>&1)"
EXTRACT_RC=$?
if [[ "$EXTRACT_RC" != "0" ]]; then
    echo "$WS_BLOCK" >&2
    exit 1
fi

# 4 必填字段
REQUIRED=("source_repo" "build_repo" "working_repo" "handback_target")

ERRORS=()

for field in "${REQUIRED[@]}"; do
    # 提取值(YAML "key: value" 格式;value 可能 quoted 也可能不 quoted)
    # 关键:用 || true 防 grep 不匹配时 set -e + pipefail 杀脚本
    VAL="$(echo "$WS_BLOCK" | { grep -E "^[[:space:]]+${field}:[[:space:]]" || true; } | sed -E "s/^[[:space:]]+${field}:[[:space:]]+//" | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/" | head -1)"

    if [[ -z "$VAL" ]]; then
        ERRORS+=("$field: missing or empty")
        continue
    fi

    # 必须 absolute path(以 / 开头)
    if [[ "$VAL" != /* ]]; then
        ERRORS+=("$field: not absolute path (got: $VAL)")
        continue
    fi
done

# === 输出 ===
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "ERROR: workspace 4 字段校验失败 in $FILE" >&2
    for err in "${ERRORS[@]}"; do
        echo "  - $err" >&2
    done
    exit 1
fi

# silent on success
exit 0
