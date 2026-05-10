#!/usr/bin/env bash
# check-1-canonical-path.sh — §6.2.1 约束 1:canonical-path containment
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 约束 1
#
# Usage: check-1-canonical-path.sh <handback_target> <source_repo> <discussion_id>
#
# 校验:realpath(handback_target) 必须严格落在
#       realpath(source_repo) + "/discussion/" + <discussion_id> + "/handback/" 之下
#
# exit 0 if PASS
# exit 1 if FAIL + stderr 报具体逃逸

set -euo pipefail

HANDBACK_TARGET="${1:-}"
SOURCE_REPO="${2:-}"
DISCUSSION_ID="${3:-}"

if [[ -z "$HANDBACK_TARGET" || -z "$SOURCE_REPO" || -z "$DISCUSSION_ID" ]]; then
    echo "Usage: check-1-canonical-path.sh <handback_target> <source_repo> <discussion_id>" >&2
    exit 2
fi

# realpath HANDBACK_TARGET(若文件不存在用 realpath -m / --no-symlinks fallback)
HANDBACK_REAL="$(realpath -m "$HANDBACK_TARGET" 2>/dev/null || python3 -c "import os, sys; print(os.path.normpath(os.path.abspath(sys.argv[1])))" "$HANDBACK_TARGET")"
SOURCE_REAL="$(realpath -m "$SOURCE_REPO" 2>/dev/null || python3 -c "import os, sys; print(os.path.normpath(os.path.abspath(sys.argv[1])))" "$SOURCE_REPO")"

EXPECTED_PREFIX="${SOURCE_REAL}/discussion/${DISCUSSION_ID}/handback"

# 严格 prefix 比较:HANDBACK_REAL 必须 == EXPECTED_PREFIX 或 == EXPECTED_PREFIX + "/..."
if [[ "$HANDBACK_REAL" == "$EXPECTED_PREFIX" || "$HANDBACK_REAL" == "$EXPECTED_PREFIX/"* ]]; then
    exit 0
fi

echo "FAIL · §6.2.1 约束 1 (canonical-path containment):" >&2
echo "  handback_target realpath:   $HANDBACK_REAL" >&2
echo "  expected prefix:            $EXPECTED_PREFIX" >&2
echo "  source_repo realpath:       $SOURCE_REAL" >&2
echo "  discussion_id:              $DISCUSSION_ID" >&2
echo "  问题:handback_target 不在 source_repo/discussion/<id>/handback/ 之下(path traversal 防御)" >&2
exit 1
