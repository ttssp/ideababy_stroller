#!/usr/bin/env bash
# writer.sh — Eval event log append-only writer
# per ideababy_stroller framework/SHARED-CONTRACT.md §"模块 B" + IN-5 + stage doc L255/L329
#
# Usage:
#   writer.sh '<json-event>'
#   echo '<json-event>' | writer.sh
#
# Behavior:
#   - 校验 event JSON against event-schema.json(用 python jsonschema 若可用,
#     退化为 grep + python json 校验若无 jsonschema)
#   - 校验通过 → append 一行 JSON(JSONL 格式)到 .eval/events.jsonl(相对当前目录)
#   - 校验失败 → exit 1 + stderr 报哪个字段失败
#
# scope OUT(per stage doc OUT-2 + v0.2 note 2):
#   - ❌ 不实装 scoring 算法
#   - ❌ 不算阈值(N 真 idea / X% intervention rate)
#   - ❌ 不出 verdict
#   - 只产 raw event log,留 v0.2 决定算法

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA="$SCRIPT_DIR/event-schema.json"

# === 输入:命令行 arg 或 stdin ===
if [[ $# -gt 0 ]]; then
    EVENT_JSON="$1"
else
    EVENT_JSON="$(cat)"
fi

if [[ -z "$EVENT_JSON" ]]; then
    echo "ERROR: empty event JSON" >&2
    exit 1
fi

# === 校验 JSON 格式合法 ===
if ! echo "$EVENT_JSON" | python3 -c 'import json, sys; json.load(sys.stdin)' 2>/dev/null; then
    echo "ERROR: invalid JSON: $EVENT_JSON" >&2
    exit 1
fi

# === 校验 schema(必需字段 + event_type enum + ts pattern)===
# 用 python3 -c 一行;EVENT_JSON 通过 stdin 传(防 shell quote 复杂度)
VALIDATE_RESULT="$(printf '%s' "$EVENT_JSON" | python3 -c '
import json, sys, re

REQUIRED = ["ts", "event_type", "details"]
ENUM_EVENT_TYPE = ["review_failures", "operator_interventions", "handback_drift"]
TS_PATTERN = r"^[0-9]{8}T[0-9]{6}Z$"
DETAILS_MAX = 500

try:
    e = json.load(sys.stdin)
except Exception as ex:
    print("ERROR: invalid JSON: " + str(ex))
    sys.exit(1)

errors = []

for f in REQUIRED:
    if f not in e or e[f] is None or e[f] == "":
        errors.append("required field missing or empty: " + f)

if "event_type" in e and e["event_type"] not in ENUM_EVENT_TYPE:
    errors.append("event_type not in enum " + str(ENUM_EVENT_TYPE) + ": got " + str(e["event_type"]))

if "ts" in e and not re.match(TS_PATTERN, str(e.get("ts", ""))):
    errors.append("ts not matching pattern " + TS_PATTERN + ": got " + str(e["ts"]))

if "details" in e and len(str(e["details"])) > DETAILS_MAX:
    errors.append("details exceeds " + str(DETAILS_MAX) + " chars: got " + str(len(str(e["details"]))))

if errors:
    for err in errors:
        print("  - " + err)
    sys.exit(1)

print("OK")
' 2>&1)"
VALIDATE_RC=$?

if [[ "$VALIDATE_RC" != "0" ]]; then
    echo "ERROR: event schema validation failed:" >&2
    echo "$VALIDATE_RESULT" >&2
    exit 1
fi

# === Append-only 写入 .eval/events.jsonl ===
LOG_DIR="${EVAL_LOG_DIR:-.eval}"
LOG_FILE="$LOG_DIR/events.jsonl"

mkdir -p "$LOG_DIR"

# 每行一 JSON event(JSONL 格式;append-only,不修改既有行)
echo "$EVENT_JSON" >> "$LOG_FILE"

# silent on success
exit 0
