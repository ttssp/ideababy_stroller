#!/usr/bin/env bash
# dangerous-event-emit.sh — Safety Floor T001 runner wrapper · 接 eval-event-log
# per specs/006a-pM/tasks/T006.md(amendment 2026-05-24 对齐 SSOT writer.sh JSON 接口)
#
# 行为:
#   1. 跑 .claude/hooks/test-fixtures/run-dangerous-24.sh "$@"(透传所有入参,含 --fixture - stdin)
#   2. 捕 RC + stderr 摘要(头 100 字节 · 删 \n \r " \ 防 JSON 注入)
#   3. 构 review_failures event(verdict=PASS|MISS · reviewer=safety-floor · round=0)
#   4. 透传给 lib/eval-event-log/writer.sh(失败只 WARN 不破 RC 透传)
#   5. exit T001 runner 真 RC(Safety Floor 行为不被本 wrapper 改)
#
# 入参:同 T001 runner 透传(含 --fixture - 接 stdin fixture)
# 退码:同 T001 runner(0 = PASS · 1 = MISS · 2 = precondition fail)
# 副作用:.eval/events.jsonl(或 $EVAL_LOG_DIR/events.jsonl)+1 行
#
# Known gotchas(per spec §"Known gotchas"):
#   - 不开 set -e(否则 T001 runner 退非 0 时 wrapper 也死,RC 透传 break)
#   - stderr 摘要必须删 \" 防 JSON 注入(writer.sh 校 schema 不会救字段值非法转义)
#   - EVAL_LOG_DIR env var 由 writer.sh 内部读(line 98 LOG_DIR=${EVAL_LOG_DIR:-.eval})

set -uo pipefail   # 注:不开 -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RUNNER="$REPO_ROOT/.claude/hooks/test-fixtures/run-dangerous-24.sh"
WRITER="$REPO_ROOT/lib/eval-event-log/writer.sh"

# precondition
[[ -x "$RUNNER" ]] || { echo "ERR: T001 runner 缺或不可执行: $RUNNER" >&2; exit 2; }
[[ -x "$WRITER" ]] || { echo "ERR: writer.sh 缺或不可执行: $WRITER" >&2; exit 2; }
command -v python3 >/dev/null || { echo "ERR: python3 缺(writer.sh + 本 wrapper 依赖)" >&2; exit 2; }

# 跑 T001 runner · 透传所有入参 · stderr 捕到临时文件
# round 2 修(codex P1):mktemp 失败时 STDERR_LOG="" 会让 2>"" 报 ambiguous redirect
# 导致 runner 根本不跑 + wrapper 透传错误 RC。回退方案:mktemp 失败 → 不捕 stderr,
# runner stderr 直出 fd 2(operator 仍可见),SUMMARY="" 进 event details。
STDERR_LOG=$(mktemp /tmp/t006-stderr.XXXXXX 2>/dev/null) || STDERR_LOG=""
if [[ -n "$STDERR_LOG" ]]; then
    trap "rm -f $STDERR_LOG" EXIT
fi

# stdin 如果连了管道(eg --fixture - 接 stdin),透传给 runner
if [[ -n "$STDERR_LOG" ]]; then
    bash "$RUNNER" "$@" 2>"$STDERR_LOG"
else
    # mktemp 失败 fallback:stderr 直出 fd 2,SUMMARY 空(per round 2 P1 修)
    bash "$RUNNER" "$@"
fi
RC=$?

# verdict 推断
if [[ "$RC" == "0" ]]; then
    VERDICT=PASS
else
    VERDICT=MISS
fi

# stderr 摘要:头 100 字节 · 删 \n \r " \ 防 JSON 注入
# round 2(codex P1 修):mktemp 失败时 STDERR_LOG="",SUMMARY 空字符串
# round 3(codex P2-1 修):截 100 字节摘要后,把捕到的全 stderr 回放到 fd 2
# 防 CI 跑 wrapper 替代 runner 时 hit-mismatch 等明细丢失(operator 看不到诊断)
if [[ -n "$STDERR_LOG" && -f "$STDERR_LOG" ]]; then
    SUMMARY=$(head -c 100 "$STDERR_LOG" 2>/dev/null | tr -d '\n\r"\\')
    # 全 stderr 回放到 fd 2(operator 可见原 runner 诊断)
    if [[ -s "$STDERR_LOG" ]]; then
        cat "$STDERR_LOG" >&2
    fi
else
    SUMMARY=""
fi

# 构 event JSON(用 python3 严转义 details 字段防奇怪字符)
TS=$(date -u +%Y%m%dT%H%M%SZ)
EVENT=$(python3 -c "
import json, sys
print(json.dumps({
    'ts': sys.argv[1],
    'event_type': 'review_failures',
    'details': 'reviewer=safety-floor round=0 verdict=' + sys.argv[2] + ' summary=' + sys.argv[3],
    'task_id': 'safety-floor'
}))
" "$TS" "$VERDICT" "$SUMMARY")

# stderr 输出 1 行 verdict(operator 可读 · debug 用)
echo "[event-emit] verdict=$VERDICT RC=$RC ts=$TS" >&2

# 透传给 writer.sh · 失败只 WARN(不破 RC 透传 · 不阻 Safety Floor)
# round 3(codex P2-2 修):writer.sh stderr 改走 fd 2 直出(原 2>/tmp/...log
# 在 /tmp 不可写时 redirect 直接失败让 writer 根本没跑 → event 丢)。
# 用 mktemp 兜底也行但加复杂度,直接 fd 2 最稳:writer 失败时 stderr 已经出过了,
# WARN 一行带 EVAL_LOG_DIR hint 给 operator。
#
# round 4(codex round 3 P2-1 修):writer.sh 内默认 LOG_DIR=${EVAL_LOG_DIR:-.eval}
# 用 cwd 解析。wrapper 从子目录跑且未显式设 EVAL_LOG_DIR 时 event 写错位置。
# 这里 default EVAL_LOG_DIR=$REPO_ROOT/.eval 确保 event 始终落本仓 .eval/events.jsonl,
# operator 显式设的 EVAL_LOG_DIR 仍优先(test 隔离场景不破)。
export EVAL_LOG_DIR="${EVAL_LOG_DIR:-$REPO_ROOT/.eval}"
WRITER_OUT=$(echo "$EVENT" | bash "$WRITER" 2>&1)
WRITER_RC=$?
if [[ "$WRITER_RC" != "0" ]]; then
    echo "WARN: writer.sh 失败(EVAL_LOG_DIR=${EVAL_LOG_DIR:-.eval} 可能不可写) RC=$WRITER_RC" >&2
    [[ -n "$WRITER_OUT" ]] && echo "$WRITER_OUT" >&2
fi

exit $RC
