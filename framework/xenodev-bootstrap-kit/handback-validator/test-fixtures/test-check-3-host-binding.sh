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
    local dir="$1" remote="$2" claude_marker="${3:-}"
    mkdir -p "$dir"
    (cd "$dir" && git init -q) || return 1
    if [[ -n "$remote" ]]; then
        (cd "$dir" && git remote add origin "$remote") || return 1
    fi
    if [[ -n "$claude_marker" ]]; then
        printf '%s\n' "$claude_marker" > "$dir/CLAUDE.md"
    fi
}

TMP_BASE="$(mktemp -d -t check3-test-XXXXXX)"
trap 'rm -rf "$TMP_BASE"' EXIT

run_case() {
    local name="$1" expected_exit="$2" actual_remote="$3" expected_remote="$4" \
          repo_marker="${5:-}" claude_content="${6:-}"
    local repo_dir="$TMP_BASE/$(printf '%s' "$name" | tr ' /' '_')"
    make_repo "$repo_dir" "$actual_remote" "$claude_content"
    set +e
    bash "$CHECK_SCRIPT" "$repo_dir" "$expected_remote" "$repo_marker" "" >/dev/null 2>&1
    local got=$?
    set -e
    if [[ "$got" == "$expected_exit" ]]; then
        echo "  ✅ PASS: $name (exit=$got)"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "  ❌ FAIL: $name (expected exit=$expected_exit, got=$got)"
        echo "      actual_remote=$actual_remote"
        echo "      expected_remote=$expected_remote"
        echo "      repo_marker=$repo_marker  claude=$claude_content"
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

echo ""
echo "=== fail-closed 优先级链 (codex round 3 finding #2 攻击场景)==="

# 攻击场景:remote mismatch 但 marker 匹配 → 旧版 PASS,新版必须 FAIL
run_case "remote mismatch + marker matches (无 fall through)" 1 \
    "https://evil.example/ttssp/ideababy_stroller.git" \
    "git@github.com:ttssp/ideababy_stroller.git" \
    "# Idea Incubator" \
    "# Idea Incubator — Project C"

# 攻击场景:有 remote + producer 故意把 expected_remote_url 留空 (downgrade)→ 必须 FAIL
run_case "downgrade attack: actual有remote + expected空 + marker匹配" 1 \
    "git@github.com:attacker/repo.git" \
    "" \
    "# Idea Incubator" \
    "# Idea Incubator — fake"

# 合法场景:都无 remote + marker 匹配 → PASS
run_case "都无 remote + marker 匹配 (合法 no-remote 模式)" 0 \
    "" \
    "" \
    "# Idea Incubator" \
    "# Idea Incubator — Project C"

# 攻击场景:三字段全空 → FAIL(无 ground truth)
run_case "三字段全空 (无 ground truth)" 1 \
    "git@github.com:ttssp/ideababy_stroller.git" \
    "" \
    "" \
    ""

# 报告
echo ""
echo "================================="
echo "Result: $PASS_COUNT PASS · $FAIL_COUNT FAIL"
echo "================================="
if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
fi
exit 0
