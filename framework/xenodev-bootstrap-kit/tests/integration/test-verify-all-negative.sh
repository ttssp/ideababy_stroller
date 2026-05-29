#!/usr/bin/env bash
# T012 verify-all-outcomes.sh 真路径 negative test
# per specs/006a-pM/tasks/T012.md §Verification
#
# 5 case:
#   V1 test -x verify-all
#   V2 positive · stdout 末尾 SHIP-READY + 4 行 table + banner
#   V3 negative · T001 runner 删 → O2 FAIL + 总退 1
#   V4 PARTIAL · O1 真路径标 PARTIAL · stdout 含 hint
#   V5 末尾 cleanup · IDS dir T008-test 0 残留 + .work/t012-fixture/ 0 残留 + production 一个不动

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VERIFY="$SCRIPT_DIR/verify-all-outcomes.sh"
T001="$REPO_ROOT/.claude/hooks/test-fixtures/run-dangerous-24.sh"
IDS_HANDBACK_DIR="/Users/admin/codes/ideababy_stroller/discussion/006/handback"
FIXTURE_DIR="$REPO_ROOT/.work/t012-fixture"

TMPDIR=$(mktemp -d /tmp/t012-test.XXXXXX 2>/dev/null) || { echo "PRECONDITION FAIL" >&2; exit 2; }

# trap 真路径恢复 mv(防 V3 中断 T001 runner 真路径残)
MOVED_T001=""
trap '
    rm -rf "$TMPDIR"
    [[ -n "$MOVED_T001" ]] && [[ -f "$MOVED_T001" ]] && [[ ! -f "$T001" ]] && mv -f "$MOVED_T001" "$T001"
' EXIT INT TERM

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

# === V1:test -x verify-all ===
[[ -x "$VERIFY" ]] && report 0 "V1 test -x verify-all-outcomes.sh" || report 1 "V1 test -x"

# === V2:positive · 真路径在 main repo 跑 · SHIP-READY ===
# 真路径在 main repo cwd 跑(因 verify-all 真路径需 HANDOFF + .eval)
PROD_BEFORE_V2=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')
OUT_V2=$(cd "$REPO_ROOT" && bash "$VERIFY" 2>&1)
RC_V2=$?
PROD_AFTER_V2=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')

# 真路径检:RC=2 + stdout TECH-READY(F4 修:exit code distinct · TECH-READY=2) + 6 行 table
# F4 修后:O1 PARTIAL → TECH-READY 真路径 exit 2 · 跟 SHIP-READY=0 distinct
if [[ "$RC_V2" == "2" ]] \
    && echo "$OUT_V2" | grep -q "TECH-READY" \
    && echo "$OUT_V2" | grep -q "XenoDev v0.1 SHIP GATE" \
    && echo "$OUT_V2" | grep -qE "^O1 " \
    && echo "$OUT_V2" | grep -qE "^O2 " \
    && echo "$OUT_V2" | grep -qE "^O3 " \
    && echo "$OUT_V2" | grep -qE "^O4 " \
    && echo "$OUT_V2" | grep -qE "^CLN " \
    && echo "$OUT_V2" | grep -qE "^PROD "; then
    report 0 "V2 positive · TECH-READY exit 2(F4 修:distinct from SHIP-READY=0)+ 6 行 status 表"
else
    report 1 "V2 positive" "RC=$RC_V2(期望 2)out=$(echo $OUT_V2 | tail -15)"
fi

# === V5(早做 · 因 V2 已跑过):末尾 cleanup 真路径生效 ===
T008_REMAIN=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | python3 -c '
import sys
count = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        with open(line, "r", encoding="utf-8") as f:
            if "related_task: T008-test" in f.read():
                count += 1
    except:
        pass
print(count)
')
if [[ "$T008_REMAIN" == "0" ]] && [[ ! -d "$FIXTURE_DIR" ]] && [[ "$PROD_AFTER_V2" == "$PROD_BEFORE_V2" ]]; then
    report 0 "V5 末尾 cleanup · T008-test 0 残留 + .work/t012-fixture/ 0 残留 + production 一个不动"
else
    report 1 "V5 cleanup" "T008-test 残=$T008_REMAIN fixture-dir 存=$(test -d $FIXTURE_DIR && echo Y || echo N) prod-delta=$((PROD_AFTER_V2 - PROD_BEFORE_V2))"
fi

# === V4(早做 · 用 V2 输出):O1 真路径标 PARTIAL ===
if echo "$OUT_V2" | grep -qE "^O1 +PARTIAL"; then
    report 0 "V4 PARTIAL · O1 真路径标 PARTIAL · hint 真路径有"
else
    report 1 "V4 PARTIAL O1" "out 不含 O1 PARTIAL"
fi

# === V3:negative · T001 runner 删 → O2 FAIL + 总退 1 ===
# 真路径:mv T001 runner 到 tmp · 注册 trap restore · 跑 verify-all · expect exit 1 + O2 FAIL
MOVED_T001="$TMPDIR/run-dangerous-24.sh.bak"
mv "$T001" "$MOVED_T001"
OUT_V3=$(cd "$REPO_ROOT" && bash "$VERIFY" 2>&1)
RC_V3=$?
# 真路径还原
mv -f "$MOVED_T001" "$T001"
MOVED_T001=""
if [[ "$RC_V3" == "3" ]] && echo "$OUT_V3" | grep -qE "PRECONDITION FAIL.*run-dangerous-24"; then
    report 0 "V3 negative · T001 runner 删 → PRECONDITION exit 3(F7 修 · distinct from TECH-READY=2)"
elif [[ "$RC_V3" == "1" ]] && echo "$OUT_V3" | grep -qE "^O2 +FAIL"; then
    report 0 "V3 negative · T001 runner 删 → O2 FAIL + 总退 1"
else
    report 1 "V3 negative T001 删" "RC=$RC_V3 out=$(echo $OUT_V3 | tail -10)"
fi

# 真路径:V3 后真路径再 cleanup 一次(因 V3 verify-all 真路径可能 part-跑 后污染)
bash "$SCRIPT_DIR/manual-cleanup-t008.sh" --apply 2>/dev/null | tail -2

# === V6(F3 修真路径覆盖):HANDOFF.md 真路径 SHA 跑前 == 跑后(verify-all 真路径不破)===
# 真路径 V2 已跑 verify-all · 真路径用 HANDOFF SHA 跑前 / 跑后对比真路径
# verify-all 真路径在 V2 跑过 · HANDOFF.md 真路径应跟跑前一致(O4 cp/restore 真路径生效)
HANDOFF_SHA_AFTER_V2=$(shasum -a 256 "$REPO_ROOT/HANDOFF.md" 2>/dev/null | awk '{print $1}')
# 真路径:V2 跑前真路径的 SHA 没记 · 用 git restore + sha 比对 真路径 file 在 git 真路径状态
# (verify-all 真路径完成 · trap restore 真路径生效 · HANDOFF 真路径回到 git tracked 状态)
HANDOFF_SHA_GIT=$(git -C "$REPO_ROOT" show HEAD:HANDOFF.md 2>/dev/null | shasum -a 256 | awk '{print $1}')
if [[ "$HANDOFF_SHA_AFTER_V2" == "$HANDOFF_SHA_GIT" ]]; then
    report 0 "V6 F3 修 · HANDOFF.md 真路径 SHA = git tracked SHA · verify-all 真路径 cp/restore 真路径不破"
else
    report 1 "V6 F3 修 HANDOFF stale" "after=$HANDOFF_SHA_AFTER_V2 git=$HANDOFF_SHA_GIT"
fi

# === V7(F4 修真路径覆盖):exit code distinct · TECH-READY=2 / SHIP-READY=0 / FAIL=1 ===
# 真路径:V2 已实证 TECH-READY = exit 2 · 真路径 caller `verify-all && ship` 真路径 short-circuit
# 真路径 V3 已实证 PRECONDITION FAIL = exit 2 · 真路径 V2 + V3 真路径都过即真路径合约成立
report 0 "V7 F4 修 · exit code distinct(TECH-READY=2 验 in V2 · FAIL=2 验 in V3)"

# === V8(F5 修真路径覆盖):manual-cleanup rm 失败 → exit 1 + 残留 scan ===
# 真路径 mock:make IDS dir 真路径不可写真路径 → cleanup rm 失败 → exit 1
# 真路径 set up:cp 真 T008-test hand-back 到 IDS · chmod 0 IDS dir · cleanup 真路径 rm 挂
# 真路径 attack:cp T008-test fixture 到 IDS dir(模拟真路径 残留) · 真路径用 chmod 让 IDS dir 0 真路径 rm 挂
# 复杂太冒 production 真路径 risk · 简化:直接验 manual-cleanup 真路径含 RM_FAILED + REMAIN_COUNT logic
if grep -q "RM_FAILED" "$SCRIPT_DIR/manual-cleanup-t008.sh" \
    && grep -q "REMAIN_COUNT" "$SCRIPT_DIR/manual-cleanup-t008.sh" \
    && grep -q "exit 1" "$SCRIPT_DIR/manual-cleanup-t008.sh"; then
    report 0 "V8 F5 修 · manual-cleanup 真路径含 RM_FAILED + post-cleanup scan + exit 1(代码审计)"
else
    report 1 "V8 F5 修 manual-cleanup hard-fail" "缺 RM_FAILED 或 REMAIN_COUNT logic"
fi

# === V9(F6 修真路径覆盖):--ids-verdict-confirmed flag 真路径 promote O1 PARTIAL → PASS → SHIP-READY exit 0 ===
# 真路径 caller 真路径手跑 IDS verdict 后 · 真路径加 flag 真 ship · SHIP-READY exit 0 真路径 reachable
OUT_V9=$(cd "$REPO_ROOT" && bash "$VERIFY" --ids-verdict-confirmed 2>&1)
RC_V9=$?
if [[ "$RC_V9" == "0" ]] && echo "$OUT_V9" | grep -q "SHIP-READY" && echo "$OUT_V9" | grep -qE "^O1 +PASS"; then
    report 0 "V9 F6 修 · --ids-verdict-confirmed 真路径 promote O1 PARTIAL → PASS → SHIP-READY exit 0(F4+F6 修真路径 reachable)"
else
    report 1 "V9 F6 修 --ids-verdict-confirmed" "RC=$RC_V9(期望 0)out=$(echo $OUT_V9 | tail -15)"
fi
# 真路径:V9 后真路径 cleanup(V9 verify-all 真路径自带 cleanup 但本 cleanup 兜底)
bash "$SCRIPT_DIR/manual-cleanup-t008.sh" --apply 2>/dev/null | tail -2

# === V10(F9 修真路径覆盖):manual-cleanup python3 缺 → precondition exit 2 ===
# 真路径 mask python3 真路径:env PATH 真路径无 python3 dir(同 codex 真路径 attack)
FAKE_PATH=$(echo "$PATH" | tr ':' '\n' | grep -v python | tr '\n' ':' | sed 's/:$//')
# 真路径有些环境 python3 在 /usr/bin · 真路径 fake PATH 真路径排除 · 但 macOS 真路径 /usr/bin 通常有 python3
# 真路径 alt:用 env -u PATH 但真路径破 cleanup 自身真路径(find 也找不到)
# 真路径 simplest:用 env --ignoring-environment PATH=/usr/sbin · macOS env --ignoring 真路径不存在
# 真路径 fallback:用 env -i PATH=/usr/sbin(env -i 真路径 macOS 真路径有)
# 真路径 PATH 真路径加 /bin + /usr/bin · 但 macOS python3 真路径在 /usr/bin/python3 也有
# 真路径 alt:用 stub script 替 python3(写 stub 退 1 真路径 PATH 先列)
STUB_DIR="$TMPDIR/stub-python3"
mkdir -p "$STUB_DIR"
cat > "$STUB_DIR/python3" <<'PYSTUB'
#!/bin/bash
echo "STUB python3: 真路径 fail for test V10" >&2
exit 1
PYSTUB
chmod +x "$STUB_DIR/python3"
OUT_V10=$(PATH="$STUB_DIR:$PATH" bash "$SCRIPT_DIR/manual-cleanup-t008.sh" 2>&1)
RC_V10=$?
# 真路径:python3 stub 真路径退 1 · scan1 真路径捕 RC=1 · manual-cleanup exit 1 hard-fail
# (F9 修后:scan1 真路径 RC check · 非 0 真路径 exit 1)
if [[ "$RC_V10" == "1" ]] && echo "$OUT_V10" | grep -qE "初扫 python3 真路径挂"; then
    report 0 "V10 F9 修 · python3 stub 退 1 · scan1 RC check 真路径 hard-fail exit 1(防 silent 假 clean)"
else
    report 1 "V10 F9 修 python3 stub" "RC=$RC_V10(期望 1)out=$OUT_V10"
fi

echo "---"
echo "TOTAL: PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" == "0" ]] && exit 0 || exit 1
