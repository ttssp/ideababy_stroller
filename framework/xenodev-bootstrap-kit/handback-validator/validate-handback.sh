#!/usr/bin/env bash
# validate-handback.sh — §6.2.1 6 约束主入口(producer + consumer 共用)
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 + §3.1
#
# Usage: validate-handback.sh <handback_file> <source_repo>
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

HANDBACK_FILE="${1:-}"
SOURCE_REPO="${2:-}"

if [[ -z "$HANDBACK_FILE" || -z "$SOURCE_REPO" ]]; then
    echo "Usage: validate-handback.sh <handback_file> <source_repo>" >&2
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

# === 提取 frontmatter 字段(用 sed + grep 替代 gawk-only match)===
extract_yaml_field() {
    local field="$1"
    local indent="$2"  # 顶级 = "", workspace 子段 = "  "
    # 取 frontmatter(第一个 ---)到第二个 --- 之间)
    # 然后 grep 出 "^<indent><field>:" 那行,提 value,strip quotes
    awk '/^---$/{if(++c==1) next; if(c==2) exit} c==1' "$HANDBACK_FILE" \
        | grep -E "^${indent}${field}:[[:space:]]" \
        | head -1 \
        | sed -E "s/^${indent}${field}:[[:space:]]*//" \
        | sed 's/^"\(.*\)"$/\1/' \
        | sed "s/^'\(.*\)'$/\1/"
}

DISCUSSION_ID="$(extract_yaml_field discussion_id '')"
PRD_FORK_ID="$(extract_yaml_field prd_fork_id '')"
HANDBACK_ID="$(extract_yaml_field handback_id '')"
SOURCE_REPO_FM="$(extract_yaml_field source_repo '  ')"
HANDBACK_TARGET="$(extract_yaml_field handback_target '  ')"
EXPECTED_REMOTE="$(extract_yaml_field expected_remote_url '  ')"
REPO_MARKER="$(extract_yaml_field repo_marker '  ')"
GIT_HASH="$(extract_yaml_field git_common_dir_hash '  ')"

# 提 ts(从 handback_id 末尾)
ISO_TS=""
if [[ -n "$HANDBACK_ID" ]]; then
    ISO_TS="$(echo "$HANDBACK_ID" | grep -oE '[0-9]{8}T[0-9]{6}Z$' || true)"
fi

# === 必要字段缺失 = hard-fail ===
MISSING=()
for v in DISCUSSION_ID PRD_FORK_ID HANDBACK_ID HANDBACK_TARGET; do
    eval "val=\$$v"
    [[ -z "$val" ]] && MISSING+=("$v")
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo "FAIL · frontmatter 必要字段缺失:${MISSING[*]}" >&2
    echo "  hand-back file: $HANDBACK_FILE" >&2
    echo "  hand-back ID (if any): ${HANDBACK_ID:-<missing>}" >&2
    exit 1
fi

# === 跑 5 个 check ===
echo "→ Validating $HANDBACK_FILE (handback_id: $HANDBACK_ID) against §6.2.1 6 约束..." >&2

# Check 1: canonical-path containment
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
if ! bash "$SCRIPT_DIR/check-5-id-consistency.sh" "$HANDBACK_FILE" "$DISCUSSION_ID" "$PRD_FORK_ID" "$HANDBACK_ID"; then
    echo "→ hand-back ID: $HANDBACK_ID" >&2
    exit 1
fi

# Check 6: id charset + filename + final-path
if ! bash "$SCRIPT_DIR/check-6-id-charset-and-final-path.sh" "$DISCUSSION_ID" "$PRD_FORK_ID" "$ISO_TS" "$HANDBACK_ID" "$HANDBACK_TARGET" "$SOURCE_REPO"; then
    echo "→ hand-back ID: $HANDBACK_ID" >&2
    exit 1
fi

# === All 6 PASS ===
echo "✓ all 6 constraints PASS for $HANDBACK_ID" >&2
exit 0
