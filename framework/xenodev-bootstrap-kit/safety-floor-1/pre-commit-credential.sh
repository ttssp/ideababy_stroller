#!/usr/bin/env bash
# pre-commit-credential.sh — git pre-commit hook 调用 scan-credentials.sh on staged files
# per ideababy_stroller framework/SHARED-CONTRACT.md §1 第 1 件
#
# 装机:
#   ln -s ../../.claude/safety-floor/credential-isolation/pre-commit-credential.sh .git/hooks/pre-commit
# 或在 lefthook.yml 注册:
#   pre-commit:
#     commands:
#       credential-scan:
#         run: bash .claude/safety-floor/credential-isolation/pre-commit-credential.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAN_SCRIPT="$SCRIPT_DIR/scan-credentials.sh"

if [[ ! -x "$SCAN_SCRIPT" ]]; then
    echo "ERROR: scan-credentials.sh not found or not executable: $SCAN_SCRIPT" >&2
    exit 2
fi

# 取 staged files(每 commit 跑)
STAGED_FILES="$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)"

if [[ -z "$STAGED_FILES" ]]; then
    # 无 staged files(可能是 merge commit / amend 等)— 跳过
    exit 0
fi

# 检测 1:staged file 名匹配 production env / secrets/production
FOUND=0
MATCHED=()

while IFS= read -r file; do
    # filename pattern
    case "$(basename "$file")" in
        .env.production|.env.production.*|.env.prod|.env.prod.*|.env.local)
            FOUND=1
            MATCHED+=("$file (staged: production env file)")
            ;;
    esac
    # path pattern
    case "$file" in
        secrets/production/*|secrets/prod/*)
            FOUND=1
            MATCHED+=("$file (staged: secrets/production/ path)")
            ;;
    esac
    # 文件内含 prod://(只查文本文件,跳过二进制)
    if [[ -f "$file" ]] && file -b --mime "$file" | grep -q 'text/'; then
        if grep -q 'prod://' "$file" 2>/dev/null; then
            FOUND=1
            MATCHED+=("$file (staged: contains prod:// connection string)")
        fi
    fi
done <<< "$STAGED_FILES"

if [[ "$FOUND" == 1 ]]; then
    echo "ERROR: production credentials detected in staged files (Safety Floor 件 1)" >&2
    echo "" >&2
    for entry in "${MATCHED[@]}"; do
        echo "  - $entry" >&2
    done
    echo "" >&2
    echo "Commit BLOCKED. Action:" >&2
    echo "  1. git restore --staged <file>  # unstage 后处理" >&2
    echo "  2. 加到 .gitignore + 不 commit" >&2
    echo "  3. 若是 test fixture,重命名加 .fake 后缀" >&2
    exit 1
fi

# 通过
exit 0
