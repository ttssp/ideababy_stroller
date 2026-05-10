#!/usr/bin/env bash
# reader.sh — Eval event log query API
# per ideababy_stroller framework/SHARED-CONTRACT.md §"模块 B" + IN-5
#
# Usage:
#   reader.sh                                       # 列全部 events
#   reader.sh --type review_failures               # filter by event_type
#   reader.sh --discussion 008                     # filter by discussion_id
#   reader.sh --since 20260501T000000Z             # filter by ts >= since
#   reader.sh --type review_failures --since ...   # 组合
#   reader.sh --count                              # 只输出 count
#
# scope OUT:
#   - ❌ 不算 scoring(per OUT-2)
#   - ❌ 不算阈值
#   - 只 raw filter / count

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${EVAL_LOG_DIR:-.eval}"
LOG_FILE="$LOG_DIR/events.jsonl"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "ERROR: log file not found: $LOG_FILE" >&2
    echo "       (run writer.sh to append events first)" >&2
    exit 1
fi

# === Parse args ===
FILTER_TYPE=""
FILTER_DISCUSSION=""
FILTER_SINCE=""
COUNT_ONLY=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --type) FILTER_TYPE="$2"; shift 2 ;;
        --discussion) FILTER_DISCUSSION="$2"; shift 2 ;;
        --since) FILTER_SINCE="$2"; shift 2 ;;
        --count) COUNT_ONLY=1; shift ;;
        *)
            echo "ERROR: unknown arg: $1" >&2
            echo "Usage: reader.sh [--type T] [--discussion ID] [--since TS] [--count]" >&2
            exit 2
            ;;
    esac
done

# === Filter via python(避免 jq 依赖)===
RESULT="$(python3 <<PYEOF
import json, sys

filter_type = "$FILTER_TYPE"
filter_discussion = "$FILTER_DISCUSSION"
filter_since = "$FILTER_SINCE"
count_only = $COUNT_ONLY

count = 0
matched = []

with open("$LOG_FILE", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except Exception:
            continue  # skip malformed line
        # apply filters
        if filter_type and e.get("event_type") != filter_type:
            continue
        if filter_discussion and e.get("discussion_id") != filter_discussion:
            continue
        if filter_since and e.get("ts", "") < filter_since:
            continue
        count += 1
        if not count_only:
            matched.append(line)

if count_only:
    print(count)
else:
    for m in matched:
        print(m)
PYEOF
)"

echo "$RESULT"
exit 0
