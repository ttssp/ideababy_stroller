#!/usr/bin/env bash
# check-6-id-charset-and-final-path.sh — §6.2.1 约束 6
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 约束 6
#
# Usage: check-6.sh <discussion_id> <prd_fork_id> <iso_ts> <handback_id> <handback_target_dir> <source_repo>
#
# 校验:
# 1. id 字符集 regex(reject / \ .. 控制字符 绝对路径前缀)
# 2. filename basename 校验(自身不含 separator)
# 3. final-path containment(realpath 二次校验,防 prd_fork_id 含 / 或 .. 时 filename 把目录 prefix 拆破)
#
# exit 0 if PASS
# exit 1 if FAIL + stderr 报哪条失败

set -euo pipefail

DISCUSSION_ID="${1:-}"
PRD_FORK_ID="${2:-}"
ISO_TS="${3:-}"
HANDBACK_ID="${4:-}"
TARGET_DIR="${5:-}"
SOURCE_REPO="${6:-}"

if [[ -z "$DISCUSSION_ID" || -z "$PRD_FORK_ID" || -z "$ISO_TS" || -z "$HANDBACK_ID" || -z "$TARGET_DIR" || -z "$SOURCE_REPO" ]]; then
    echo "Usage: check-6.sh <discussion_id> <prd_fork_id> <iso_ts> <handback_id> <target_dir> <source_repo>" >&2
    exit 2
fi

ERRORS=()

# === 1.1 · discussion_id 字符集 ===
if ! [[ "$DISCUSSION_ID" =~ ^[0-9]{3}$ ]]; then
    ERRORS+=("discussion_id ($DISCUSSION_ID) not matching ^[0-9]{3}\$")
fi

# === 1.2 · prd_fork_id 字符集 ===
if ! [[ "$PRD_FORK_ID" =~ ^[0-9]{3}[a-z]?(-p[A-Z])?$ ]]; then
    ERRORS+=("prd_fork_id ($PRD_FORK_ID) not matching ^[0-9]{3}[a-z]?(-p[A-Z])?\$")
fi

# === 1.3 · iso_ts 字符集 ===
if ! [[ "$ISO_TS" =~ ^[0-9]{8}T[0-9]{6}Z$ ]]; then
    ERRORS+=("iso_ts ($ISO_TS) not matching ^[0-9]{8}T[0-9]{6}Z\$ (UTC, 无毫秒)")
fi

# === 1.4 · handback_id 严格等于 prd_fork_id + "-" + iso_ts ===
EXPECTED_HBID="${PRD_FORK_ID}-${ISO_TS}"
if [[ "$HANDBACK_ID" != "$EXPECTED_HBID" ]]; then
    ERRORS+=("handback_id ($HANDBACK_ID) != derived ($EXPECTED_HBID)")
fi

# === 1.5 · 三 token 不含危险字符(/ \ .. 控制字符 绝对路径前缀)===
for token_name in "discussion_id" "prd_fork_id" "iso_ts"; do
    case "$token_name" in
        discussion_id) val="$DISCUSSION_ID" ;;
        prd_fork_id) val="$PRD_FORK_ID" ;;
        iso_ts) val="$ISO_TS" ;;
    esac

    # 检 / \ .. 绝对路径前缀
    if [[ "$val" == */* || "$val" == *\\* || "$val" == *..* || "$val" == /* ]]; then
        ERRORS+=("$token_name ($val) contains forbidden chars (/, \\, .., or absolute path prefix)")
    fi

    # 检控制字符(\x00-\x1f \x7f)— 用 tr 兼容 BSD grep
    # tr 删除非控制字符;若 result 非空 = 有控制字符
    if [[ -n "$(printf '%s' "$val" | LC_ALL=C tr -d '\11\12\15\40-\176' )" ]]; then
        ERRORS+=("$token_name ($val) contains control characters")
    fi
done

# === 2 · filename basename 校验 ===
FILENAME="${ISO_TS}-${HANDBACK_ID}.md"
EXPECTED_BASENAME="$(basename "$FILENAME")"
if [[ "$FILENAME" != "$EXPECTED_BASENAME" ]]; then
    ERRORS+=("filename ($FILENAME) basename mismatch (basename = $EXPECTED_BASENAME) — contains separator")
fi

# === 3 · final-path containment(写入前最后一道)===
FULL_PATH="${TARGET_DIR%/}/$FILENAME"
FULL_REAL="$(realpath -m "$FULL_PATH" 2>/dev/null || python3 -c "import os, sys; print(os.path.normpath(os.path.abspath(sys.argv[1])))" "$FULL_PATH")"
SOURCE_REAL="$(realpath -m "$SOURCE_REPO" 2>/dev/null || python3 -c "import os, sys; print(os.path.normpath(os.path.abspath(sys.argv[1])))" "$SOURCE_REPO")"
EXPECTED_PREFIX="${SOURCE_REAL}/discussion/${DISCUSSION_ID}/handback"

if [[ "$FULL_REAL" != "$EXPECTED_PREFIX" && "$FULL_REAL" != "$EXPECTED_PREFIX/"* ]]; then
    ERRORS+=("final-path containment FAIL: full_path realpath ($FULL_REAL) not under expected prefix ($EXPECTED_PREFIX)")
fi

# === 输出 ===
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "FAIL · §6.2.1 约束 6 (id charset + filename basename + final-path containment):" >&2
    for err in "${ERRORS[@]}"; do
        echo "  - $err" >&2
    done
    echo "  问题:OWASP path traversal 防御失败 — id 含 / 或 .. 可能让 filename 拆破目录 prefix 逃逸" >&2
    exit 1
fi

exit 0
