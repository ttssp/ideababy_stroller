#!/usr/bin/env bash
# T011 .eval/events.jsonl 真路径验证 · O3 量化达标
# per specs/006a-pM/tasks/T011.md(amendment 2026-05-25 对齐 SSOT event_type/复数 enum)
#
# 行为(per spec amendment Outputs):
#   (a) precondition:.eval/events.jsonl 存在 + 非空 → 缺 exit 2
#   (b) wc -l ≥ 5 → 否则 exit 1 + stderr 提示
#   (c) python3 line-by-line json.loads(skip empty line)· 任一行非合法 exit 1 + 列行号
#   (d) 3 类 event_type 覆盖(NEW schema · 复数 enum):
#       operator_interventions / review_failures / handback_drift
#       OLD schema rows(type 字段)只算行数 · 不算 3 类
#       任一缺 exit 1 + 列缺
#   (e) 全过 → echo "O3 quant OK: <wc> events, 3 types covered" + exit 0
#
# 退码:
#   0 = 全过
#   1 = wc < 5 / 行非合法 / 3 类不全
#   2 = .eval/events.jsonl 缺 / 空 / python3 缺

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
# 真路径:支持 EVAL_LOG_DIR env var override(同 T006 writer.sh)· 默认 $REPO_ROOT/.eval
# round 4(codex round 3 P2 修):worktree 内跑(parallel-builder 真路径)时
# REPO_ROOT 是 worktree dir · .eval/events.jsonl 真在 main repo
# 真路径 fallback:git common dir → main repo · 真路径 worktree + main 都齐
EVENTS_FILE="${EVAL_LOG_DIR:-$REPO_ROOT/.eval}/events.jsonl"
if [[ ! -f "$EVENTS_FILE" ]] && [[ -z "${EVAL_LOG_DIR:-}" ]]; then
    # 真路径 fallback(operator 未显式 EVAL_LOG_DIR 时):用 git common dir 找 main repo
    GIT_COMMON=$(git -C "$REPO_ROOT" rev-parse --git-common-dir 2>/dev/null)
    if [[ -n "$GIT_COMMON" ]]; then
        MAIN_REPO=$(cd "$GIT_COMMON/.." && pwd)
        [[ -f "$MAIN_REPO/.eval/events.jsonl" ]] && EVENTS_FILE="$MAIN_REPO/.eval/events.jsonl"
    fi
fi

command -v python3 >/dev/null || { echo "PRECONDITION FAIL: python3 缺(本 runner 依赖)" >&2; exit 2; }

# === (a) precondition ===
if [[ ! -f "$EVENTS_FILE" ]]; then
    echo "PRECONDITION FAIL: .eval/events.jsonl 不存在: $EVENTS_FILE" >&2
    echo "  真路径:跑 T006 wrapper + T008 round-trip + 手 echo JSON | writer.sh 凑数据" >&2
    exit 2
fi

if [[ ! -s "$EVENTS_FILE" ]]; then
    echo "PRECONDITION FAIL: .eval/events.jsonl 空" >&2
    exit 2
fi

# === (b) (c) (d) 真路径校验 · 用 python3 一气 ===
RESULT=$(python3 -c '
import json, sys
events_file = sys.argv[1]
SPEC_ENUM = {"operator_interventions", "review_failures", "handback_drifts", "handback_drift"}  # T104 B-2 backward-compat alias 复数 + 单数兼容
# 真路径"3 类逻辑 group"(2 个 alias 同 group · 不重计 · backward-compat 兼容 OLD v0.1 真历史):
SPEC_GROUPS = {
    "operator_interventions": "operator_interventions",
    "review_failures": "review_failures",
    "handback_drifts": "handback_drifts",
    "handback_drift": "handback_drifts",  # backward-compat alias to plural (T104 B-2 真路径)
}

# (c) line-by-line json.loads · skip empty line
total = 0
malformed = []
event_types = set()    # NEW schema (event_type 字段) 见过的类型
old_count = 0          # OLD schema (type 字段) · 只算行数

with open(events_file) as f:
    for lineno, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception as e:
            malformed.append((lineno, str(e)))
            continue
        total += 1
        # NEW schema (event_type) 优先 · 算 3 类覆盖
        if "event_type" in d:
            event_types.add(d["event_type"])
        elif "type" in d:
            old_count += 1   # OLD schema · 只算行数 不算 3 类覆盖
        # else:无 type/event_type · 算行数不算覆盖

# (c) 任一行非合法 → 报错
if malformed:
    print("FAIL (c): " + str(len(malformed)) + " 行非合法 JSON")
    for lineno, err in malformed[:10]:
        print("  line " + str(lineno) + ": " + err[:100])
    sys.exit(1)

# (b) wc -l ≥ 5
if total < 5:
    print("FAIL (b): wc=" + str(total) + " < 5")
    print("  真路径:跑 T006 wrapper + T008 round-trip + 手 echo JSON | writer.sh 凑数据")
    sys.exit(1)

# (d) 3 类 event_type 覆盖(NEW schema · T104 alias group 真路径)
# 真路径:event_types 映射到 SPEC_GROUPS · 全部 group 必齐
seen_groups = {SPEC_GROUPS[t] for t in event_types if t in SPEC_GROUPS}
all_groups = set(SPEC_GROUPS.values())
missing_groups = all_groups - seen_groups
if missing_groups:
    print("FAIL (d): 3 类 event_type group 覆盖不全 · 缺: " + ", ".join(sorted(missing_groups)))
    print("  见到 group: " + ", ".join(sorted(seen_groups)))
    print("  真路径凑:echo JSON | bash lib/eval-event-log/writer.sh · event_type=" + sorted(missing_groups)[0])
    sys.exit(1)

# (e) 全过
print("O3 quant OK: " + str(total) + " events, 3 types covered (NEW schema · OLD schema 兼容 " + str(old_count) + " 行)")
sys.exit(0)
' "$EVENTS_FILE" 2>&1)
RC=$?

# 真路径输出(stderr if rc != 0 · stdout if rc == 0)
if [[ "$RC" == "0" ]]; then
    echo "$RESULT"
else
    echo "$RESULT" >&2
fi

exit $RC
