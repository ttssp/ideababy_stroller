#!/usr/bin/env bash
# verify-bootstrap.sh · T302 OQ-2=选建 smoke test(per spec.md §5.3 wave 3)
# 结论先:接 fixture path 真路径 · 逐文件 SHA dual-verify(source = bootstrap-kit/<rel> vs target = fixture/<rel>)
# fail-closed:任一 SHA mismatch / file missing → exit 非 0 + stderr 列 drift
# stdout 含 "SHA dual-verify PASS" 字面真路径(per spec verify line 52)
#
# 真路径与 verify-ppv-p1.sh O1 段不重叠:
# - verify-bootstrap.sh 真路径 = bootstrap.sh 立刻反馈(MANIFEST 不一定已写)
# - verify-ppv-p1.sh O1 真路径 = MANIFEST-driven 全 lifecycle 校验
#
# Usage:
#   bash verify-bootstrap.sh <fixture-path>
#
# 退码:
#   0 = 全 PASS
#   1 = drift detected / fixture invalid
#   2 = arg error

set -uo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: bash verify-bootstrap.sh <fixture-path>" >&2
    exit 2
fi

FIXTURE_PATH="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IDS_KIT="$SCRIPT_DIR"

if [[ ! -d "$FIXTURE_PATH" ]]; then
    echo "ERROR: fixture path 真路径不存在: $FIXTURE_PATH" >&2
    exit 1
fi

if [[ ! -d "$IDS_KIT" ]]; then
    echo "ERROR: bootstrap-kit source 真路径不存在: $IDS_KIT" >&2
    exit 1
fi

# === source→target mapping(与 bootstrap.sh fixture mode 真路径严格一致) ===
TOP_FILES=(
    "AGENTS.md:AGENTS.md"
    "CLAUDE.md:CLAUDE.md"
)
SUBTREE_MAP=(
    "skills:.claude/skills"
    "hooks/wrappers:.claude/hooks/wrappers"
    "hooks/test-fixtures:.claude/hooks/test-fixtures"
    "safety-floor-1:.claude/safety-floor/credential-isolation"
    "safety-floor-3:.claude/safety-floor/backup-detection"
    "handback-validator:lib/handback-validator"
    "eval-event-log:lib/eval-event-log"
    "workspace-schema:lib/workspace-schema"
    "tests/integration:tests/integration"
)
SINGLE_FILES=(
    "safety-floor-2/block-dangerous.sh:.claude/hooks/block-dangerous.sh"
)

VERIFIED=0
DRIFT=0
MISSING=0

verify_file() {
    local src="$1" tgt="$2"
    if [[ ! -f "$src" ]]; then
        echo "ERROR: source 真路径缺失: $src" >&2
        MISSING=$((MISSING + 1))
        return 1
    fi
    if [[ ! -f "$tgt" ]]; then
        echo "DRIFT[missing-target]: $tgt(source=$src)" >&2
        DRIFT=$((DRIFT + 1))
        return 1
    fi
    local src_sha tgt_sha
    src_sha=$(shasum -a 256 "$src" | awk '{print $1}')
    tgt_sha=$(shasum -a 256 "$tgt" | awk '{print $1}')
    if [[ "$src_sha" != "$tgt_sha" ]]; then
        echo "DRIFT[sha-mismatch]: $tgt" >&2
        echo "  source SHA: $src_sha" >&2
        echo "  target SHA: $tgt_sha" >&2
        DRIFT=$((DRIFT + 1))
        return 1
    fi
    VERIFIED=$((VERIFIED + 1))
    return 0
}

# === top files ===
for pair in "${TOP_FILES[@]}"; do
    src_rel="${pair%%:*}"
    tgt_rel="${pair##*:}"
    verify_file "$IDS_KIT/$src_rel" "$FIXTURE_PATH/$tgt_rel" || true
done

# === single files ===
for pair in "${SINGLE_FILES[@]}"; do
    src_rel="${pair%%:*}"
    tgt_rel="${pair##*:}"
    verify_file "$IDS_KIT/$src_rel" "$FIXTURE_PATH/$tgt_rel" || true
done

# === subtrees(逐文件 SHA verify)===
for pair in "${SUBTREE_MAP[@]}"; do
    src_rel="${pair%%:*}"
    tgt_rel="${pair##*:}"
    SRC_DIR="$IDS_KIT/$src_rel"
    TGT_DIR="$FIXTURE_PATH/$tgt_rel"
    if [[ ! -d "$SRC_DIR" ]]; then
        echo "ERROR: subtree source 真路径缺: $SRC_DIR" >&2
        MISSING=$((MISSING + 1))
        continue
    fi
    if [[ ! -d "$TGT_DIR" ]]; then
        echo "DRIFT[missing-subtree]: $TGT_DIR" >&2
        DRIFT=$((DRIFT + 1))
        continue
    fi
    while IFS= read -r src_file; do
        rel="${src_file#$SRC_DIR/}"
        tgt_file="$TGT_DIR/$rel"
        verify_file "$src_file" "$tgt_file" || true
    done < <(find "$SRC_DIR" -type f)
done

# === Result ===
if [[ "$DRIFT" -gt 0 || "$MISSING" -gt 0 ]]; then
    echo "[verify-bootstrap] FAIL · verified=$VERIFIED · drift=$DRIFT · missing=$MISSING" >&2
    exit 1
fi

echo "[verify-bootstrap] $VERIFIED files OK · SHA dual-verify PASS · fixture=$FIXTURE_PATH"
exit 0
