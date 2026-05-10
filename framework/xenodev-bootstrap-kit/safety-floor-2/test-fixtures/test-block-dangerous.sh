#!/usr/bin/env bash
# test-block-dangerous.sh — 验 block-dangerous.sh 拦截 codex round 3 bypass + 回归
#
# Usage: bash test-block-dangerous.sh
# exit 0 if all PASS;1 if any FAIL

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$(cd "$SCRIPT_DIR/.." && pwd)/block-dangerous.sh"

if [[ ! -x "$HOOK" ]]; then
    echo "FAIL: hook not executable: $HOOK" >&2
    exit 1
fi

PASS_COUNT=0
FAIL_COUNT=0

# expect_decision: deny 或 allow
run_case() {
    local name="$1" expect="$2" cmd="$3"
    local payload
    payload=$(printf '{"tool_input":{"command":%s}}' "$(printf '%s' "$cmd" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")
    local out
    out="$(printf '%s' "$payload" | bash "$HOOK" 2>/dev/null)"
    local got
    if printf '%s' "$out" | grep -q '"permissionDecision":[[:space:]]*"deny"'; then
        got="deny"
    elif printf '%s' "$out" | grep -q '"permissionDecision":[[:space:]]*"allow"'; then
        got="allow"
    else
        got="unknown"
    fi
    if [[ "$got" == "$expect" ]]; then
        echo "  ✅ PASS: $name"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "  ❌ FAIL: $name (expected=$expect got=$got cmd=$cmd)"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

echo "=== codex round 3 finding #1 bypass scenarios (must DENY)==="
run_case "force-push 参数顺序: --force 在 main 后" deny "git push origin main --force"
run_case "force-push 参数顺序: -f 在 master 后" deny "git push origin master -f"
run_case "force-push 受保护分支 release-1" deny "git push origin release-1 --force"
run_case "force-push 受保护分支 production" deny "git push --force origin production"
run_case "小写 SQL drop table" deny "drop table users;"
run_case "小写 SQL drop database" deny "drop database mydb"
run_case "混合大小写 SQL" deny "Drop TaBle x"

echo ""
echo "=== 回归(旧 case 仍 DENY)==="
run_case "rm -rf /" deny "rm -rf /"
run_case "DROP DATABASE prod (大写)" deny "DROP DATABASE prod"
run_case "kubectl delete namespace" deny "kubectl delete namespace foo"
run_case "terraform destroy" deny "terraform destroy"
run_case "fork bomb" deny ":(){ :|:& };:"
run_case "git push --force main(原顺序)" deny "git push --force origin main"
run_case "git reset --hard origin" deny "git reset --hard origin/main"

echo ""
echo "=== 新增云提供商危险命令(must DENY)==="
run_case "aws rds delete-db-instance" deny "aws rds delete-db-instance --db-instance-identifier prod"
run_case "aws rds delete-db-cluster" deny "aws rds delete-db-cluster --db-cluster-identifier prod"
run_case "gcloud sql instances delete" deny "gcloud sql instances delete prod-db"
run_case "az sql db delete" deny "az sql db delete -n prod -g rg --server srv"

echo ""
echo "=== 安全命令(must ALLOW)==="
run_case "ls -la" allow "ls -la"
run_case "git status" allow "git status"
run_case "git push origin feature-branch" allow "git push origin feature-branch"
run_case "drop tableware (无关词)" allow "echo drop tableware"
run_case "rm -rf /tmp/local" allow "rm -rf /tmp/local-junk"
run_case "rm -rf node_modules" allow "rm -rf node_modules"

echo ""
echo "================================="
echo "Result: $PASS_COUNT PASS · $FAIL_COUNT FAIL"
echo "================================="
[[ $FAIL_COUNT -gt 0 ]] && exit 1
exit 0
