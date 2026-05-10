#!/usr/bin/env bash
# test-pre-commit-staged-blob.sh — 验 pre-commit-credential.sh 读 staged blob,不读 working tree
#
# 原 bug(codex review B2.2 Block A.5 finding #2):
#   旧实现:if [[ -f "$file" ]] && file -b --mime "$file" | grep -q 'text/' && grep -q 'prod://' "$file"
#   攻击:git add a.md(含 prod://)→ echo '' > a.md → git commit → hook 看 working tree 干净 → PASS
#         但 staged blob 仍含 prod:// → prod:// 进 git 历史
#
# Fix:改读 git show ":$file" → 攻击场景应被 BLOCK
#
# Usage: bash test-pre-commit-staged-blob.sh
# exit 0 if 3 cases all PASS;exit 1 if any FAIL

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SCRIPT="$(cd "$SCRIPT_DIR/.." && pwd)/pre-commit-credential.sh"

if [[ ! -x "$HOOK_SCRIPT" ]]; then
    echo "FAIL: hook not executable: $HOOK_SCRIPT" >&2
    exit 1
fi

# 临时 git repo
TMP_REPO="$(mktemp -d -t pre-commit-test-XXXXXX)"
trap 'rm -rf "$TMP_REPO"' EXIT

cd "$TMP_REPO"
git init -q
git config user.email "test@test.local"
git config user.name "test"

PASS_COUNT=0
FAIL_COUNT=0

# ============================================================
# Case 1:staged blob 含 prod://,working tree 干净 → 应 BLOCK
# ============================================================
echo "Case 1: staged-but-cleaned attack(原 bug 场景)"
echo "prod://my-secret-db" > evil.md
git add evil.md
echo "harmless content" > evil.md  # 清 working tree

# 跑 hook
if bash "$HOOK_SCRIPT" 2>/dev/null; then
    echo "  ❌ FAIL: hook 应 BLOCK 但 PASS 了 — staged blob 仍含 prod:// 但 hook 看 working tree 干净"
    FAIL_COUNT=$((FAIL_COUNT + 1))
else
    echo "  ✅ PASS: hook 正确 BLOCK"
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# 清理 case 1 状态(无 commit,直接清 index + working tree)
git rm -f --cached evil.md >/dev/null 2>&1 || true
rm -f evil.md

# ============================================================
# Case 2:staged blob 干净,working tree 含 prod:// → 应 PASS
# ============================================================
echo ""
echo "Case 2: working tree 含但未 stage(应 PASS — hook 只管 staged)"
echo "harmless" > clean.md
git add clean.md
echo "prod://leaked-but-not-staged" > clean.md  # working tree 改了但没 stage

if bash "$HOOK_SCRIPT" 2>/dev/null; then
    echo "  ✅ PASS: hook 正确 PASS(working tree 内容不该 block commit)"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "  ❌ FAIL: hook 误 BLOCK — working tree 内容不该影响 staged commit"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# 清理 case 2
git rm -f --cached clean.md >/dev/null 2>&1 || true
rm -f clean.md

# ============================================================
# Case 3:staged blob + working tree 都含 prod:// → 应 BLOCK
# ============================================================
echo ""
echo "Case 3: 两端都含 prod:// (回归测;旧逻辑也 catch)"
echo "prod://both" > both.md
git add both.md

if bash "$HOOK_SCRIPT" 2>/dev/null; then
    echo "  ❌ FAIL: hook 应 BLOCK 但 PASS"
    FAIL_COUNT=$((FAIL_COUNT + 1))
else
    echo "  ✅ PASS: hook 正确 BLOCK"
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# 报告
echo ""
echo "================================="
echo "Result: $PASS_COUNT PASS · $FAIL_COUNT FAIL"
echo "================================="
if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
fi
exit 0
