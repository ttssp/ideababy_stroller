#!/usr/bin/env bash
# check-2-symlink-reject.sh — §6.2.1 约束 2:symlink reject
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 约束 2
#
# Usage: check-2-symlink-reject.sh <handback_target> <source_repo>
#
# 校验:从 source_repo 起到 handback_target 路径上的任意一段不能是 symlink
#       (例外:source_repo 自身可以是 symlink — operator dev workflow 决定)
#
# exit 0 if PASS
# exit 1 if FAIL + stderr 报哪段是 symlink

set -euo pipefail

HANDBACK_TARGET="${1:-}"
SOURCE_REPO="${2:-}"

if [[ -z "$HANDBACK_TARGET" || -z "$SOURCE_REPO" ]]; then
    echo "Usage: check-2-symlink-reject.sh <handback_target> <source_repo>" >&2
    exit 2
fi

# 先 canonicalize source_repo(允许 source_repo 自身是 symlink)
SOURCE_REAL="$(realpath "$SOURCE_REPO" 2>/dev/null || echo "$SOURCE_REPO")"

# 取 handback_target 的相对部分(source_repo 之下的部分)
# 期望 handback_target 形如 <SOURCE_REAL>/discussion/<id>/handback[/...]
RELATIVE="${HANDBACK_TARGET#"$SOURCE_REPO"}"
RELATIVE="${RELATIVE#"$SOURCE_REAL"}"
RELATIVE="${RELATIVE#/}"  # strip leading /

if [[ -z "$RELATIVE" ]]; then
    # handback_target == source_repo,异常但不算 symlink 失败
    exit 0
fi

# 检查 SOURCE_REAL 之下的每一段是否是 symlink
CURRENT="$SOURCE_REAL"
IFS='/' read -ra SEGMENTS <<< "$RELATIVE"

for seg in "${SEGMENTS[@]}"; do
    [[ -z "$seg" ]] && continue
    CURRENT="$CURRENT/$seg"
    if [[ -L "$CURRENT" ]]; then
        echo "FAIL · §6.2.1 约束 2 (symlink reject):" >&2
        echo "  symlink found at: $CURRENT" >&2
        echo "  source_repo (canonicalized): $SOURCE_REAL" >&2
        echo "  handback_target: $HANDBACK_TARGET" >&2
        echo "  问题:source_repo 之下路径段不能是 symlink(防 confused-deputy / Dropbox-conflict 攻击)" >&2
        echo "  例外:source_repo 自身可以是 symlink(operator dev workflow 决定),不在本检查范围" >&2
        exit 1
    fi
done

exit 0
