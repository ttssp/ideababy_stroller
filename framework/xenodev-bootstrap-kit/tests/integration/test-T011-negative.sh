#!/usr/bin/env bash
# T011 negative + verification tests
# per specs/006a-pM/tasks/T011.md §Verification
#
# 5 case:
#   V1 test -x runner
#   V2 positive · stdout 含 "O3 quant OK: <N> events, 3 types covered"
#   V3 negative · .eval/events.jsonl 缺 → runner exit 2
#   V4 negative · < 5 行 → runner exit 1
#   V5 negative · 某行非合法 JSON → runner exit 1
#   V6 negative · handback_drift 类删完 → runner exit 1 + 列缺类型

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RUNNER="$SCRIPT_DIR/eval-events-count.sh"
# round 2(codex round 1 P2 修):real events 路径不再 hardcode 真路径 ·
# 用 EVAL_LOG_DIR override 或 REPO_ROOT 推断 · 防 CI/clone/worktree 跑挂
# worktree 内 REPO_ROOT 真路径不是 main repo(没 .eval/) · operator 应 export
# EVAL_LOG_DIR 或 cd 到 main repo · 真路径 fallback 用 git common dir
EVAL_DIR="${EVAL_LOG_DIR:-$REPO_ROOT/.eval}"
# 真路径:检 events.jsonl 真路径(非 dir · 因 worktree 内 .eval dir 真路径含 .keep 但
# events.jsonl 不真路径 untracked) · 不在 → fallback 用 git common dir 找 main repo
if [[ ! -f "$EVAL_DIR/events.jsonl" ]]; then
    GIT_COMMON=$(git -C "$REPO_ROOT" rev-parse --git-common-dir 2>/dev/null)
    if [[ -n "$GIT_COMMON" ]]; then
        MAIN_REPO=$(cd "$GIT_COMMON/.." && pwd)
        [[ -f "$MAIN_REPO/.eval/events.jsonl" ]] && EVAL_DIR="$MAIN_REPO/.eval"
    fi
fi
REAL_EVENTS="$EVAL_DIR/events.jsonl"

[[ -x "$RUNNER" ]] || { echo "PRECONDITION FAIL: runner 不存在: $RUNNER" >&2; exit 2; }
if [[ ! -f "$REAL_EVENTS" ]]; then
    echo "PRECONDITION FAIL: real events 不存在: $REAL_EVENTS" >&2
    echo "  真路径:export EVAL_LOG_DIR=<path/to/main-repo/.eval> 或 cd 到 main repo 跑" >&2
    exit 2
fi

TMPDIR=$(mktemp -d /tmp/t011-test.XXXXXX 2>/dev/null) || {
    echo "PRECONDITION FAIL: mktemp -d 失败" >&2
    exit 2
}
trap 'rm -rf "$TMPDIR"' EXIT

PASS=0
FAIL=0
report() {
    local rc=$1 name=$2 detail=${3:-}
    if [[ "$rc" == "0" ]]; then
        echo "PASS: $name"
        PASS=$((PASS+1))
    else
        echo "FAIL: $name${detail:+ — $detail}"
        FAIL=$((FAIL+1))
    fi
}

# === V1:test -x runner ===
[[ -x "$RUNNER" ]] && report 0 "V1 test -x runner" || report 1 "V1 test -x runner"

# === V2:positive · 真路径跑(用 round 1 解出的 EVAL_DIR · 防 hardcode)===
OUT_V2=$(EVAL_LOG_DIR="$EVAL_DIR" bash "$RUNNER" 2>&1)
RC_V2=$?
if [[ "$RC_V2" == "0" ]] && echo "$OUT_V2" | grep -qE "O3 quant OK: [0-9]+ events, 3 types covered"; then
    report 0 "V2 positive · stdout 含 O3 quant OK + N events + 3 types covered"
else
    report 1 "V2 positive" "RC=$RC_V2 out=$OUT_V2"
fi

# === V3:negative · events.jsonl 缺 → runner exit 2 ===
# 真路径:用临时空 EVAL_LOG_DIR(不真 mv 真文件 · 真路径 isolated)
mkdir -p "$TMPDIR/no-events"
OUT_V3=$(EVAL_LOG_DIR="$TMPDIR/no-events" bash "$RUNNER" 2>&1)
RC_V3=$?
if [[ "$RC_V3" == "2" ]] && echo "$OUT_V3" | grep -q "不存在"; then
    report 0 "V3 negative · events.jsonl 缺 → exit 2 + 真路径还原"
else
    report 1 "V3 negative events 缺" "RC=$RC_V3 out=$OUT_V3"
fi

# === V4:negative · < 5 行 → runner exit 1 ===
mkdir -p "$TMPDIR/short-events"
head -3 "$REAL_EVENTS" > "$TMPDIR/short-events/events.jsonl"
OUT_V4=$(EVAL_LOG_DIR="$TMPDIR/short-events" bash "$RUNNER" 2>&1)
RC_V4=$?
if [[ "$RC_V4" == "1" ]] && echo "$OUT_V4" | grep -q "< 5"; then
    report 0 "V4 negative · < 5 行 → exit 1 + 列 wc"
else
    report 1 "V4 negative < 5 行" "RC=$RC_V4 out=$OUT_V4"
fi

# === V5:negative · 某行非合法 JSON → runner exit 1 ===
mkdir -p "$TMPDIR/malformed-events"
{ head -10 "$REAL_EVENTS"; echo "INVALID JSON NOT PARSEABLE"; tail -10 "$REAL_EVENTS"; } > "$TMPDIR/malformed-events/events.jsonl"
OUT_V5=$(EVAL_LOG_DIR="$TMPDIR/malformed-events" bash "$RUNNER" 2>&1)
RC_V5=$?
if [[ "$RC_V5" == "1" ]] && echo "$OUT_V5" | grep -qE "非合法 JSON|line [0-9]+"; then
    report 0 "V5 negative · 非合法 JSON → exit 1 + 列行号"
else
    report 1 "V5 negative non-JSON" "RC=$RC_V5 out=$OUT_V5"
fi

# === V6:negative · handback_drift 删完 → runner exit 1 + 列缺 ===
mkdir -p "$TMPDIR/missing-type-events"
grep -v "handback_drift" "$REAL_EVENTS" > "$TMPDIR/missing-type-events/events.jsonl"
# 真路径:验证 grep -v 真删了 + 仍 ≥ 5 行 + 全合法
TYPED_COUNT=$(wc -l < "$TMPDIR/missing-type-events/events.jsonl" | tr -d ' ')
if [[ "$TYPED_COUNT" -lt 5 ]]; then
    report 1 "V6 setup" "grep -v handback_drift 后 < 5 行 · $TYPED_COUNT"
else
    OUT_V6=$(EVAL_LOG_DIR="$TMPDIR/missing-type-events" bash "$RUNNER" 2>&1)
    RC_V6=$?
    if [[ "$RC_V6" == "1" ]] && echo "$OUT_V6" | grep -q "handback_drift"; then
        report 0 "V6 negative · handback_drift 删完 → exit 1 + 列缺 handback_drift"
    else
        report 1 "V6 negative 缺 type" "RC=$RC_V6 out=$OUT_V6"
    fi
fi

echo "---"
echo "TOTAL: PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" == "0" ]] && exit 0 || exit 1
