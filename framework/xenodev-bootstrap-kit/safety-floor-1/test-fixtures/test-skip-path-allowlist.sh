#!/usr/bin/env bash
# test-skip-path-allowlist.sh — 验 round 4 finding #1 fix:
# basename-skip → path-allowlist。任意位置的 user-written README/AGENTS/CLAUDE
# 含 prod:// 必须被检测。

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$(cd "$SCRIPT_DIR/.." && pwd)/pre-commit-credential.sh"
SCAN="$(cd "$SCRIPT_DIR/.." && pwd)/scan-credentials.sh"

PASS_COUNT=0
FAIL_COUNT=0

TMP_REPO="$(mktemp -d -t skip-allowlist-XXXXXX)"
trap 'rm -rf "$TMP_REPO"' EXIT

cd "$TMP_REPO"
git init -q
git config user.email "test@test.local"
git config user.name "test"

echo "=== pre-commit hook(staged blob 扫)==="

# Case 1:docs/README.md 含 prod:// 必须 BLOCK
mkdir -p docs
echo "prod://my-real-db" > docs/README.md
git add docs/README.md
if bash "$HOOK" 2>/dev/null; then
    echo "  FAIL: docs/README.md 含 prod:// 应 BLOCK 但 PASS"
    FAIL_COUNT=$((FAIL_COUNT + 1))
else
    echo "  PASS: docs/README.md 含 prod:// 正确 BLOCK"
    PASS_COUNT=$((PASS_COUNT + 1))
fi
git rm -f --cached docs/README.md >/dev/null 2>&1
rm -rf docs

# Case 2:notes/AGENTS.md 含 prod:// 必须 BLOCK
mkdir -p notes
echo "prod://notes-leak" > notes/AGENTS.md
git add notes/AGENTS.md
if bash "$HOOK" 2>/dev/null; then
    echo "  FAIL: notes/AGENTS.md 应 BLOCK 但 PASS"
    FAIL_COUNT=$((FAIL_COUNT + 1))
else
    echo "  PASS: notes/AGENTS.md 正确 BLOCK"
    PASS_COUNT=$((PASS_COUNT + 1))
fi
git rm -f --cached notes/AGENTS.md >/dev/null 2>&1
rm -rf notes

# Case 3:vendor/lib/CLAUDE.md 含 prod:// 必须 BLOCK
mkdir -p vendor/lib
echo "prod://vendor-leak" > vendor/lib/CLAUDE.md
git add vendor/lib/CLAUDE.md
if bash "$HOOK" 2>/dev/null; then
    echo "  FAIL: vendor/lib/CLAUDE.md 应 BLOCK"
    FAIL_COUNT=$((FAIL_COUNT + 1))
else
    echo "  PASS: vendor/lib/CLAUDE.md 正确 BLOCK"
    PASS_COUNT=$((PASS_COUNT + 1))
fi
git rm -f --cached vendor/lib/CLAUDE.md >/dev/null 2>&1
rm -rf vendor

# Case 4:.claude/safety-floor/credential-isolation/README.md 应 PASS(白名单)
mkdir -p .claude/safety-floor/credential-isolation
echo "本规则检测 prod:// 字串" > .claude/safety-floor/credential-isolation/README.md
git add .claude/safety-floor/credential-isolation/README.md
if bash "$HOOK" 2>/dev/null; then
    echo "  PASS: .claude/safety-floor/credential-isolation/README.md (白名单) 正确 ALLOW"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "  FAIL: 白名单 README 应 ALLOW"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi
git rm -f --cached .claude/safety-floor/credential-isolation/README.md >/dev/null 2>&1
rm -rf .claude

echo ""
echo "=== scan-credentials.sh(全仓扫)==="

# Case 5:全仓扫 docs/README.md 含 prod:// 应 FAIL
mkdir -p docs
echo "prod://leak" > docs/README.md
if bash "$SCAN" "$TMP_REPO" 2>/dev/null; then
    echo "  FAIL: 全仓扫 docs/README.md 应 FAIL"
    FAIL_COUNT=$((FAIL_COUNT + 1))
else
    echo "  PASS: 全仓扫 docs/README.md 正确 FAIL"
    PASS_COUNT=$((PASS_COUNT + 1))
fi
rm -rf docs

# Case 6:仅白名单文件含 prod://,全仓扫应 PASS
mkdir -p .claude/safety-floor/credential-isolation
echo "本规则定义 prod:// 模式" > .claude/safety-floor/credential-isolation/README.md
if bash "$SCAN" "$TMP_REPO" 2>/dev/null; then
    echo "  PASS: 全仓扫白名单文件正确 PASS"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "  FAIL: 全仓扫白名单文件应 PASS"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi
rm -rf .claude

echo ""
echo "================================="
echo "Result: $PASS_COUNT PASS - $FAIL_COUNT FAIL"
echo "================================="
[[ $FAIL_COUNT -gt 0 ]] && exit 1
exit 0
