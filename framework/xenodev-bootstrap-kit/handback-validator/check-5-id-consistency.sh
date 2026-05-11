#!/usr/bin/env bash
# check-5-id-consistency.sh — §6.2.1 约束 5:id consistency check(三处一致)
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 约束 5
#
# Usage: check-5-id-consistency.sh <handback_file_path> <fm_discussion_id> <fm_prd_fork_id> <fm_handback_id>
#
# 校验三处 id 严格一致:
# 1. 物理路径中 discussion/<X>/handback/ 的 <X>
# 2. 文件名 <ts>-<handback_id>.md 中 handback_id 解出的 prd_fork_id 前缀的 discussion_id 部分
# 3. frontmatter discussion_id / prd_fork_id / handback_id derived 公式
#
# exit 0 if PASS
# exit 1 if FAIL + stderr 报哪处不一致

set -euo pipefail

FILE_PATH="${1:-}"
FM_DISCUSSION_ID="${2:-}"
FM_PRD_FORK_ID="${3:-}"
FM_HANDBACK_ID="${4:-}"

if [[ -z "$FILE_PATH" || -z "$FM_DISCUSSION_ID" || -z "$FM_PRD_FORK_ID" || -z "$FM_HANDBACK_ID" ]]; then
    echo "Usage: check-5-id-consistency.sh <file_path> <fm_discussion_id> <fm_prd_fork_id> <fm_handback_id>" >&2
    exit 2
fi

ERRORS=()

# === 检查 1: 物理路径中 discussion/<X>/handback/ 的 <X> ===
# 路径形如 .../discussion/008/handback/<ts>-<handback_id>.md
# 同时接受绝对路径(/...) 与相对路径(discussion/...) — regex 允许 ^ 或 / 前缀
# B2.2 Block F fix(2026-05-11):/handback-review consumer 模式可能传相对路径,
# 原 regex 要求 `/discussion/` 前必有 `/` 会 false-positive。
PATH_DISCUSSION_ID="$(echo "$FILE_PATH" | sed -nE 's|^(.*/)?discussion/([^/]+)/handback/.*|\2|p')"
if [[ -z "$PATH_DISCUSSION_ID" ]]; then
    ERRORS+=("path discussion_id: cannot extract from path $FILE_PATH (path must contain discussion/<X>/handback/, with optional path prefix)")
elif [[ "$PATH_DISCUSSION_ID" != "$FM_DISCUSSION_ID" ]]; then
    ERRORS+=("path discussion_id ($PATH_DISCUSSION_ID) != frontmatter discussion_id ($FM_DISCUSSION_ID)")
fi

# === 检查 2: 文件名 <ts>-<handback_id>.md 中 handback_id 的 prd_fork_id 前缀 ===
FILE_NAME="$(basename "$FILE_PATH")"
# 文件名格式: <ISO ts>-<handback_id>.md  例: 20260520T103015Z-008a-pA-20260520T103015Z.md
# handback_id == <prd_fork_id>-<ISO ts>
# 所以 handback_id 中前面是 prd_fork_id (如 008a-pA),后面是 ts
FILE_HANDBACK_ID="$(echo "$FILE_NAME" | sed -nE 's|^[0-9]{8}T[0-9]{6}Z-(.+)\.md$|\1|p')"
if [[ -z "$FILE_HANDBACK_ID" ]]; then
    ERRORS+=("filename: cannot extract handback_id from $FILE_NAME (expected format: <ISO ts>-<handback_id>.md)")
elif [[ "$FILE_HANDBACK_ID" != "$FM_HANDBACK_ID" ]]; then
    ERRORS+=("filename handback_id ($FILE_HANDBACK_ID) != frontmatter handback_id ($FM_HANDBACK_ID)")
fi

# === 检查 3: frontmatter handback_id == prd_fork_id + "-" + ts ===
# handback_id 应严格等于 prd_fork_id + "-" + <ISO ts>
# ts 在 handback_id 末尾(从尾巴 reverse 解析,因 prd_fork_id 含 "-")
EXPECTED_TS_PATTERN='^[0-9]{8}T[0-9]{6}Z$'
HBID_TS="$(echo "$FM_HANDBACK_ID" | grep -oE "${EXPECTED_TS_PATTERN#^}" | tail -1 || true)"
if [[ -z "$HBID_TS" ]]; then
    ERRORS+=("frontmatter handback_id ($FM_HANDBACK_ID) does not contain ISO ts at end (expected pattern $EXPECTED_TS_PATTERN)")
else
    EXPECTED_HBID="${FM_PRD_FORK_ID}-${HBID_TS}"
    if [[ "$FM_HANDBACK_ID" != "$EXPECTED_HBID" ]]; then
        ERRORS+=("frontmatter handback_id ($FM_HANDBACK_ID) != derived prd_fork_id ($FM_PRD_FORK_ID) + '-' + ts ($HBID_TS) = $EXPECTED_HBID")
    fi
fi

# === 检查 4: prd_fork_id 前缀 == discussion_id ===
# prd_fork_id 形如 008a-pA;前 3 位 (008) 应 == discussion_id
PRD_FORK_PREFIX="${FM_PRD_FORK_ID:0:3}"
if [[ "$PRD_FORK_PREFIX" != "$FM_DISCUSSION_ID" ]]; then
    ERRORS+=("frontmatter prd_fork_id prefix ($PRD_FORK_PREFIX from $FM_PRD_FORK_ID) != frontmatter discussion_id ($FM_DISCUSSION_ID)")
fi

# === 输出 ===
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "FAIL · §6.2.1 约束 5 (id consistency check, 三处 id 不一致):" >&2
    for err in "${ERRORS[@]}"; do
        echo "  - $err" >&2
    done
    echo "  问题:hand-back 包 id 不一致 → corruption-of-corpus 失效模式" >&2
    exit 1
fi

exit 0
