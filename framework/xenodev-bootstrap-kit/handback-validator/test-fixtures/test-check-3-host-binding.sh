#!/usr/bin/env bash
# test-check-3-host-binding.sh — 验 check-3-repo-identity.sh 保留 host 比对
#
# 原 bug(codex review B2.2 Block A.5 finding #3):
#   normalize 删了 host → git@github.com:owner/repo.git == https://evil.example/owner/repo.git
#   攻击者起 evil.example/<owner>/<repo>.git 同名 fork → 通过约束 3 → 写假 hand-back
#
# Fix:normalize 保留 host,统一为 host[:port]/path/repo 形式
#
# Usage: bash test-check-3-host-binding.sh
# exit 0 if all cases PASS;exit 1 if any FAIL

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_SCRIPT="$(cd "$SCRIPT_DIR/.." && pwd)/check-3-repo-identity.sh"

if [[ ! -x "$CHECK_SCRIPT" ]]; then
    echo "FAIL: check script not executable: $CHECK_SCRIPT" >&2
    exit 1
fi

PASS_COUNT=0
FAIL_COUNT=0

# 临时 git repo 工厂
make_repo() {
    local dir="$1" remote="$2"
    mkdir -p "$dir"
    (cd "$dir" && git init -q && git remote add origin "$remote") || return 1
}

TMP_BASE="$(mktemp -d -t check3-test-XXXXXX)"
trap 'rm -rf "$TMP_BASE"' EXIT

run_case() {
    local name="$1" expected_exit="$2" actual_remote="$3" expected_remote="$4"
    local repo_dir="$TMP_BASE/$(printf '%s' "$name" | tr ' /' '_')"
    make_repo "$repo_dir" "$actual_remote"
    set +e
    bash "$CHECK_SCRIPT" "$repo_dir" "$expected_remote" "" "" >/dev/null 2>&1
    local got=$?
    set -e
    if [[ "$got" == "$expected_exit" ]]; then
        echo "  ✅ PASS: $name (exit=$got)"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "  ❌ FAIL: $name (expected exit=$expected_exit, got=$got)"
        echo "      actual_remote=$actual_remote"
        echo "      expected_remote=$expected_remote"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

echo "=== 正向(应 PASS, exit 0)==="
run_case "scp-form 完全相等" 0 \
    "git@github.com:ttssp/ideababy_stroller.git" \
    "git@github.com:ttssp/ideababy_stroller.git"

run_case "https 完全相等" 0 \
    "https://github.com/ttssp/ideababy_stroller.git" \
    "https://github.com/ttssp/ideababy_stroller.git"

run_case "scp 与 https 同 host 同 owner repo (跨形式等价)" 0 \
    "git@github.com:ttssp/ideababy_stroller.git" \
    "https://github.com/ttssp/ideababy_stroller.git"

run_case "trailing .git 缺一可"  0 \
    "https://github.com/ttssp/ideababy_stroller" \
    "https://github.com/ttssp/ideababy_stroller.git"

run_case "大小写 host"  0 \
    "git@GitHub.com:ttssp/ideababy_stroller.git" \
    "git@github.com:ttssp/ideababy_stroller.git"

echo ""
echo "=== 负向(应 FAIL, exit 1 — 这是 finding #3 攻击场景)==="
run_case "同 owner/repo 不同 host (攻击场景)" 1 \
    "https://evil.example/ttssp/ideababy_stroller.git" \
    "git@github.com:ttssp/ideababy_stroller.git"

run_case "不同 owner" 1 \
    "git@github.com:attacker/ideababy_stroller.git" \
    "git@github.com:ttssp/ideababy_stroller.git"

run_case "不同 repo" 1 \
    "git@github.com:ttssp/other_repo.git" \
    "git@github.com:ttssp/ideababy_stroller.git"

run_case "host 子域名也算不同 (gitlab vs github)" 1 \
    "git@gitlab.com:ttssp/ideababy_stroller.git" \
    "git@github.com:ttssp/ideababy_stroller.git"

# 报告
echo ""
echo "================================="
echo "Result: $PASS_COUNT PASS · $FAIL_COUNT FAIL"
echo "================================="
if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
fi
exit 0
