#!/usr/bin/env bash
# T104 B-2 enum 全复数测试
# - V1 positive: writer 接受新复数 handback_drifts
# - V2 positive: writer 仍接受 OLD 单数 handback_drift(reader 兼容路径 · backward-compat 不破)
# - V3 positive: reader 读 OLD events.jsonl(单数)能 surface 出 event
# - V4 negative: writer 拒未知 event_type
# - V5 schema: event-schema.json 真路径 grep handback_drifts ≥ 1

set -uo pipefail

# worktree 真路径:用 $PWD (caller cd 到 worktree 真路径) · 不硬绑主仓
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "[test-T104] REPO=$REPO"

TMPDIR=$(mktemp -d -t t104-enum.XXXXXX)
trap "rm -rf $TMPDIR" EXIT

PASS_CNT=0
FAIL_CNT=0
report() {
  local rc="$1" msg="$2" detail="${3:-}"
  if [ "$rc" -eq 0 ]; then
    echo "  PASS: $msg"
    PASS_CNT=$((PASS_CNT + 1))
  else
    echo "  FAIL: $msg"
    [ -n "$detail" ] && echo "    detail: $detail"
    FAIL_CNT=$((FAIL_CNT + 1))
  fi
}

# === V1: writer 接受新复数 handback_drifts ===
echo "=== V1: writer 新复数 handback_drifts ==="
TS=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$TMPDIR/v1"
cd "$TMPDIR/v1"
OUT=$(bash $REPO/lib/eval-event-log/writer.sh "{\"ts\":\"$TS\",\"event_type\":\"handback_drifts\",\"details\":\"v1 test new plural\"}" 2>&1)
RC=$?
if [ $RC -eq 0 ] && [ -f .eval/events.jsonl ] && grep -q 'handback_drifts' .eval/events.jsonl; then
  report 0 "V1 writer accepts plural handback_drifts"
else
  report 1 "V1 writer plural" "rc=$RC · out=$OUT"
fi
cd "$REPO"

# === V2: writer 拒新写 OLD 单数 handback_drift(只 reader 兼容历史 · 防新 caller 写 OLD)===
echo "=== V2: writer reject OLD 单数 handback_drift on new write ==="
TS=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$TMPDIR/v2"
cd "$TMPDIR/v2"
OUT=$(bash $REPO/lib/eval-event-log/writer.sh "{\"ts\":\"$TS\",\"event_type\":\"handback_drift\",\"details\":\"v2 reject new OLD write\"}" 2>&1)
RC=$?
# writer 拒 OLD 单数(per codex R1 P1:不让新 caller 写 OLD enum · 真路径迁移)
if [ $RC -ne 0 ]; then
  report 0 "V2 writer 拒 OLD 单数 handback_drift 新写(只 reader 兼容 OLD)"
else
  report 1 "V2 writer OLD reject" "rc=$RC · out=$OUT (期望非 0)"
fi
cd "$REPO"

# === V3: reader 读 OLD events.jsonl 能 filter handback_drifts 时也捞出单数 ===
echo "=== V3: reader OLD events read ==="
mkdir -p "$TMPDIR/v3/.eval"
# 真路径 fixture(per codex R1 P1):3 种 OLD/NEW · v0.1 真实历史是 type 字段(per .eval/events.jsonl 实证)
cat > "$TMPDIR/v3/.eval/events.jsonl" <<'EOF'
{"ts":"20260510T140000Z","type":"handback_drift","details":"OLD type-field singular (v0.1 真历史)"}
{"ts":"20260510T150000Z","event_type":"handback_drift","details":"OLD event_type-field singular"}
{"ts":"20260511T140000Z","event_type":"handback_drifts","details":"NEW plural"}
EOF
cd "$TMPDIR/v3"
# 读所有 event 真路径(backward-compat fixture)
ALL=$(bash $REPO/lib/eval-event-log/reader.sh 2>&1)
COUNT_ALL=$(echo "$ALL" | grep -cE 'handback_drift')  # backward-compat alias regex
if [ "$COUNT_ALL" -eq 3 ]; then
  report 0 "V3 reader 读 3 种 fixture 全 3 行(OLD type · OLD event_type · NEW plural)"
else
  report 1 "V3 reader 3 种" "count=$COUNT_ALL · out=$ALL"
fi
# filter --type handback_drifts:期望真路径捞 3 种(OLD type · OLD event_type · NEW)backward-compat alias 等价
PLURAL=$(bash $REPO/lib/eval-event-log/reader.sh --type handback_drifts 2>&1)
COUNT_P=$(echo "$PLURAL" | grep -cE 'handback_drift')  # backward-compat alias regex
if [ "$COUNT_P" -eq 3 ]; then
  report 0 "V3b filter handback_drifts → 3 行 (兼容 OLD type + OLD event_type + NEW alias)"
else
  report 1 "V3b filter alias 3 种" "count=$COUNT_P · out=$PLURAL"
fi
cd "$REPO"

# === V4: writer 拒未知 event_type ===
echo "=== V4: writer reject unknown event_type ==="
TS=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$TMPDIR/v4"
cd "$TMPDIR/v4"
OUT=$(bash $REPO/lib/eval-event-log/writer.sh "{\"ts\":\"$TS\",\"event_type\":\"unknown_evt\",\"details\":\"v4 unknown\"}" 2>&1)
RC=$?
if [ $RC -ne 0 ]; then
  report 0 "V4 writer 拒 unknown event_type"
else
  report 1 "V4 writer unknown" "rc=$RC · out=$OUT"
fi
cd "$REPO"

# === V5: event-schema.json 真路径 grep handback_drifts ≥ 1 ===
echo "=== V5: schema 含 handback_drifts ==="
SCH=$REPO/lib/eval-event-log/event-schema.json
SCH_PLURAL=$(grep -c '"handback_drifts"' "$SCH")
if [ "$SCH_PLURAL" -ge 1 ]; then
  report 0 "V5 event-schema.json 含 handback_drifts ($SCH_PLURAL 次)"
else
  report 1 "V5 schema plural" "count=$SCH_PLURAL"
fi

# === Summary ===
echo ""
echo "=== Summary ==="
echo "PASS: $PASS_CNT"
echo "FAIL: $FAIL_CNT"
[ "$FAIL_CNT" -eq 0 ]
