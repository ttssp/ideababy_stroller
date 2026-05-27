#!/usr/bin/env bash
# validate-handback.sh — §6.2.1 6 约束主入口(producer + consumer 共用)
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 + §3.1
#
# Usage:
#   validate-handback.sh <handback_file> <source_repo> [--mode=consumer|producer]
#
# Mode(B2.2 Block A friction #4 fix):
#   --mode=consumer (默认):跑全 5 check;<handback_file> 必须在
#     <source_repo>/discussion/<id>/handback/ 路径下(check-5 path 段校验需要)
#   --mode=producer:writer 端写入前自检;跳过 check-5 的 path 段校验
#     (因文件还在 /tmp 等草稿位置,真实路径未知)
#
# 顺序跑 5 个 check script(约束 4 hard-fail 是行为约定,无独立 script):
# - check-1-canonical-path.sh
# - check-2-symlink-reject.sh
# - check-3-repo-identity.sh
# - check-5-id-consistency.sh
# - check-6-id-charset-and-final-path.sh
#
# 任一失败 → 立即 exit 1 + stderr 报哪条约束 + handback_id

set -euo pipefail

HANDBACK_FILE=""
SOURCE_REPO=""
MODE="consumer"

# === Parse args(支持位置 + --mode=XXX flag)===
for arg in "$@"; do
    case "$arg" in
        --mode=consumer) MODE="consumer" ;;
        --mode=producer) MODE="producer" ;;
        --mode=*)
            echo "ERROR: unknown mode: $arg (expected --mode=consumer or --mode=producer)" >&2
            exit 2
            ;;
        *)
            if [[ -z "$HANDBACK_FILE" ]]; then
                HANDBACK_FILE="$arg"
            elif [[ -z "$SOURCE_REPO" ]]; then
                SOURCE_REPO="$arg"
            else
                echo "ERROR: too many positional args (got: $arg)" >&2
                exit 2
            fi
            ;;
    esac
done

if [[ -z "$HANDBACK_FILE" || -z "$SOURCE_REPO" ]]; then
    echo "Usage: validate-handback.sh <handback_file> <source_repo> [--mode=consumer|producer]" >&2
    exit 2
fi

if [[ ! -f "$HANDBACK_FILE" ]]; then
    echo "ERROR: handback file not found: $HANDBACK_FILE" >&2
    exit 2
fi

if [[ ! -d "$SOURCE_REPO" ]]; then
    echo "ERROR: source_repo not a directory: $SOURCE_REPO" >&2
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# === 共享 YAML 解析 helpers(per FU-producer-1 抽离;0 新依赖)===
# 原 inline extract_yaml_field 迁到 _yaml-helpers.sh,signature 从 (field, indent)
# 升 (file, field, indent) — 解耦 $HANDBACK_FILE 隐式依赖,允许 gen-handback.sh 共用。
source "$SCRIPT_DIR/_yaml-helpers.sh"

DISCUSSION_ID="$(extract_yaml_field "$HANDBACK_FILE" discussion_id '')"
PRD_FORK_ID="$(extract_yaml_field "$HANDBACK_FILE" prd_fork_id '')"
HANDBACK_ID="$(extract_yaml_field "$HANDBACK_FILE" handback_id '')"
SOURCE_REPO_FM="$(extract_yaml_field "$HANDBACK_FILE" source_repo '  ')"
HANDBACK_TARGET="$(extract_yaml_field "$HANDBACK_FILE" handback_target '  ')"
EXPECTED_REMOTE="$(extract_yaml_field "$HANDBACK_FILE" expected_remote_url '  ')"
REPO_MARKER="$(extract_yaml_field "$HANDBACK_FILE" repo_marker '  ')"
GIT_HASH="$(extract_yaml_field "$HANDBACK_FILE" git_common_dir_hash '  ')"

# 提 ts(从 handback_id 末尾)
ISO_TS=""
if [[ -n "$HANDBACK_ID" ]]; then
    ISO_TS="$(echo "$HANDBACK_ID" | grep -oE '[0-9]{8}T[0-9]{6}Z$' || true)"
fi

# === 必要字段缺失 = hard-fail ===
# B2.2 Block A friction #1/#3 fix:若所有关键 hand-back 字段全缺,
# 提示可能用错(forward HANDOFF.md 没有 handback_id),给 helpful hint
MISSING=()
for v in DISCUSSION_ID PRD_FORK_ID HANDBACK_ID HANDBACK_TARGET; do
    eval "val=\$$v"
    [[ -z "$val" ]] && MISSING+=("$v")
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo "FAIL · frontmatter 必要字段缺失:${MISSING[*]}" >&2
    echo "  hand-back file: $HANDBACK_FILE" >&2
    echo "  hand-back ID (if any): ${HANDBACK_ID:-<missing>}" >&2
    # 若 handback_id 缺 + workspace.handback_target 存在 → 大概率 forward HANDOFF.md 误用
    if [[ -z "$HANDBACK_ID" && -n "$HANDBACK_TARGET" ]]; then
        echo "" >&2
        echo "  ⚠ 提示:本文件含 workspace.handback_target 但无 handback_id;" >&2
        echo "     可能是 forward HANDOFF.md(plan-start v3.0 产)而非 hand-back 包。" >&2
        echo "     forward HANDOFF.md 不应用本 validator;它由 IDS plan-start 产,XenoDev 消费。" >&2
        echo "     hand-back 包由 XenoDev 在 task ship 后产,frontmatter 必含 handback_id。" >&2
    fi
    exit 1
fi

# === 跑 5 个 check ===
echo "→ Validating $HANDBACK_FILE (handback_id: $HANDBACK_ID, mode: $MODE) against §6.2.1 6 约束..." >&2

# Check 1: canonical-path containment(校验 frontmatter handback_target 字段)
if ! bash "$SCRIPT_DIR/check-1-canonical-path.sh" "$HANDBACK_TARGET" "$SOURCE_REPO" "$DISCUSSION_ID"; then
    echo "→ hand-back ID: $HANDBACK_ID" >&2
    exit 1
fi

# Check 2: symlink reject
if ! bash "$SCRIPT_DIR/check-2-symlink-reject.sh" "$HANDBACK_TARGET" "$SOURCE_REPO"; then
    echo "→ hand-back ID: $HANDBACK_ID" >&2
    exit 1
fi

# Check 3: repo identity (三模式)
if ! bash "$SCRIPT_DIR/check-3-repo-identity.sh" "$SOURCE_REPO" "$EXPECTED_REMOTE" "$REPO_MARKER" "$GIT_HASH"; then
    echo "→ hand-back ID: $HANDBACK_ID" >&2
    exit 1
fi

# Check 5: id consistency
# B2.2 Block A friction #4 fix:producer mode 跳过 check-5 的物理路径段校验
# (producer 写入前文件还在 /tmp,真实路径未知;只能 consumer mode 跑)
if [[ "$MODE" == "consumer" ]]; then
    if ! bash "$SCRIPT_DIR/check-5-id-consistency.sh" "$HANDBACK_FILE" "$DISCUSSION_ID" "$PRD_FORK_ID" "$HANDBACK_ID"; then
        echo "→ hand-back ID: $HANDBACK_ID" >&2
        exit 1
    fi
else
    echo "  ⏭  check-5 skipped (mode=producer; 物理路径段校验只能 consumer 模式跑;frontmatter id 一致性由 check-6 兜底)" >&2
fi

# Check 6: id charset + filename + final-path
if ! bash "$SCRIPT_DIR/check-6-id-charset-and-final-path.sh" "$DISCUSSION_ID" "$PRD_FORK_ID" "$ISO_TS" "$HANDBACK_ID" "$HANDBACK_TARGET" "$SOURCE_REPO"; then
    echo "→ hand-back ID: $HANDBACK_ID" >&2
    exit 1
fi

# === All checks PASS ===
if [[ "$MODE" == "producer" ]]; then
    echo "✓ producer-mode checks PASS for $HANDBACK_ID(check-5 已跳;consumer 端读取后会再跑)" >&2
else
    echo "✓ all 6 constraints PASS for $HANDBACK_ID" >&2
fi
exit 0
