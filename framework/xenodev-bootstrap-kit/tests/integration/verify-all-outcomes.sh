#!/usr/bin/env bash
# T012 SHIP GATE · 全 4 Outcomes 一键验证脚本
# per specs/006a-pM/tasks/T012.md(amendment 2026-05-25 · SSOT 真路径)
#
# 行为(per spec amendment Outputs):
#   (a) banner + ISO ts
#   (b) O1 = T008 round-trip(producer + consumer half · IDS verdict half 标 PARTIAL)
#   (c) O2 = T001 run-dangerous-24(24 cmd dangerous patterns 全 deny)
#   (d) O3 = T010 bootstrap-verify + T011 eval-events-count(≥5 行 + 3 类齐)
#   (e) O4 = runtime gen 1 hand-back 到 .work/t012-fixture/ + operator_score 字段 + producer validator
#   (f) 表格汇总 (printf %-6s %-10s %s)
#   (g) 末尾 cleanup:manual-cleanup-t008.sh --apply + rm .work/t012-fixture/
#   (h) FAIL → exit 1 · 全 PASS(PARTIAL 允许)→ stdout SHIP-READY + exit 0
#
# 退码(round 4 codex round 3 F7 修 · distinct codes):
#   0 = SHIP-READY · 全 Outcome PASS + CLEANUP + PROD · O1 IDS verdict 真路径 confirmed
#   1 = SHIP GATE FAIL · 任一 Outcome/CLEANUP/PROD FAIL
#   2 = TECH-READY · producer+consumer half PASS · IDS verdict half 待 operator
#   3 = PRECONDITION FAIL · sub-test/HANDOFF/IDS dir 真路径缺(distinct from TECH-READY)
#
# 真路径 flag:
#   --ids-verdict-confirmed = operator 真路径手跑 IDS /handback-review · 真路径 promote O1 PARTIAL → PASS
#     (per round 4 codex round 3 F6 修 · 真路径 SHIP-READY exit 0 真路径 reachable)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# === 真路径 flag · F6 修 ===
IDS_VERDICT_CONFIRMED=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --ids-verdict-confirmed) IDS_VERDICT_CONFIRMED=1; shift ;;
        --help|-h)
            echo "Usage: verify-all-outcomes.sh [--ids-verdict-confirmed]"
            echo ""
            echo "  --ids-verdict-confirmed  真路径 operator 已手跑 IDS /handback-review · promote"
            echo "                           O1 PARTIAL → PASS · 真路径 reachable SHIP-READY exit 0"
            echo ""
            echo "Exit codes:"
            echo "  0 = SHIP-READY"
            echo "  1 = FAIL"
            echo "  2 = TECH-READY"
            echo "  3 = PRECONDITION"
            exit 0
            ;;
        *) echo "ERR: unknown option: $1" >&2; exit 3 ;;
    esac
done

# === sub-test paths ===
T001_RUNNER="$REPO_ROOT/.claude/hooks/test-fixtures/run-dangerous-24.sh"
T008_RUNNER="$SCRIPT_DIR/round-trip-006a-pM.sh"
T010_RUNNER="$SCRIPT_DIR/bootstrap-verify.sh"
T011_RUNNER="$SCRIPT_DIR/eval-events-count.sh"
T008_CLEANUP="$SCRIPT_DIR/manual-cleanup-t008.sh"
GEN="$REPO_ROOT/lib/handback-validator/gen-handback.sh"
VALIDATE="$REPO_ROOT/lib/handback-validator/validate-handback.sh"
HANDOFF="$REPO_ROOT/HANDOFF.md"
HANDOFF_BAK="$REPO_ROOT/HANDOFF-006a-pM.bak"
IDS_REPO="/Users/admin/codes/ideababy_stroller"
IDS_HANDBACK_DIR="$IDS_REPO/discussion/006/handback"
FIXTURE_DIR="$REPO_ROOT/.work/t012-fixture"

# === precondition ===
for sub in "$T001_RUNNER" "$T008_RUNNER" "$T010_RUNNER" "$T011_RUNNER" "$T008_CLEANUP" "$GEN" "$VALIDATE"; do
    if [[ ! -x "$sub" && ! -f "$sub" ]]; then
        echo "PRECONDITION FAIL: 缺 $sub" >&2
        exit 3
    fi
done

# round 2(codex round 1 F3 修):HANDOFF + HANDOFF_BAK precondition + trap restore
# 真路径防 cp/mv 中断真路径留 stale state · 必须 verify-all 启动时就 check + trap
if [[ ! -f "$HANDOFF" ]]; then
    echo "PRECONDITION FAIL: HANDOFF.md 不存在: $HANDOFF" >&2
    exit 3
fi
if [[ ! -f "$HANDOFF_BAK" ]]; then
    echo "PRECONDITION FAIL: HANDOFF backup 不存在: $HANDOFF_BAK" >&2
    exit 3
fi

# 真路径:HANDOFF.md SHA snapshot · 跑前记 · trap restore 时验后真路径不破
HANDOFF_SHA_BEFORE=$(shasum -a 256 "$HANDOFF" | awk '{print $1}')
HANDOFF_BAK_SAVE="$HANDOFF.t012savebak"

# 真路径:trap EXIT/INT/TERM 真路径恢复 HANDOFF.md(防中断留 stale)
# 真路径:trap 内不退 exit(防覆盖 main exit code)
trap '
    # HANDOFF restore 真路径
    if [[ -f "$HANDOFF_BAK_SAVE" ]]; then
        if [[ ! -f "$HANDOFF" ]] || [[ "$(shasum -a 256 "$HANDOFF" 2>/dev/null | awk "{print \$1}")" != "$HANDOFF_SHA_BEFORE" ]]; then
            mv -f "$HANDOFF_BAK_SAVE" "$HANDOFF" 2>/dev/null && echo "[trap] HANDOFF.md 真路径 restore" >&2
        else
            rm -f "$HANDOFF_BAK_SAVE"
        fi
    fi
' EXIT INT TERM

# === banner ===
TS_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "================================================================="
echo "XenoDev v0.1 SHIP GATE · feature 006a-pM · $TS_ISO"
echo "================================================================="
echo ""

# === Outcome status tracking ===
# 真路径用 indexed array(bash 4+ associative array 真路径需 bash 4 · macOS 默认 bash 3.2 · 用 indexed array 兼容)
O1_STATUS="?"
O2_STATUS="?"
O3_STATUS="?"
O4_STATUS="?"
O1_DETAIL=""
O2_DETAIL=""
O3_DETAIL=""
O4_DETAIL=""

# === IDS production hand-back 数 snapshot(真路径验跑后不破)===
PROD_BEFORE=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f 2>/dev/null | wc -l | tr -d ' ')

# === O1:T008 round-trip ===
echo "----- O1: round-trip integration (T008) -----"
O1_OUT=$(bash "$T008_RUNNER" 2>&1)
O1_RC=$?
if [[ "$O1_RC" == "0" ]] && echo "$O1_OUT" | grep -q "round-trip OK:"; then
    # round 4(codex round 3 F6 修):--ids-verdict-confirmed flag 真路径 promote O1 PARTIAL → PASS
    # operator 真路径手跑 IDS /handback-review · ≥7 hand-back approve 后 真路径加 flag 真 ship
    # 真路径 SHIP-READY exit 0 真路径 reachable(防 dead code)
    if [[ "$IDS_VERDICT_CONFIRMED" == "1" ]]; then
        O1_STATUS="PASS"
        O1_DETAIL="producer+consumer half PASS · IDS verdict confirmed by operator"
        echo "[O1] PASS · 真路径 producer+consumer half + IDS verdict 真路径(--ids-verdict-confirmed)"
    else
        O1_STATUS="PARTIAL"
        O1_DETAIL="producer+consumer half OK · IDS /handback-review verdict 需 operator 真路径手跑"
        echo "[O1] PARTIAL · producer+consumer half PASS · IDS verdict 段未跑(超 XenoDev 边界)"
        echo "       (真路径 operator 手跑 IDS /handback-review 后 · 重跑 --ids-verdict-confirmed 真路径 promote 到 PASS)"
    fi
else
    O1_STATUS="FAIL"
    O1_DETAIL="round-trip RC=$O1_RC"
    echo "[O1] FAIL · RC=$O1_RC"
    echo "$O1_OUT" | tail -10 >&2
fi
echo ""

# === O2:T001 run-dangerous-24 ===
echo "----- O2: dangerous-24 patterns (T001) -----"
O2_OUT=$(bash "$T001_RUNNER" 2>&1)
O2_RC=$?
if [[ "$O2_RC" == "0" ]] && echo "$O2_OUT" | grep -qE "0 漏.*Safety Floor PASS"; then
    O2_STATUS="PASS"
    O2_DETAIL=$(echo "$O2_OUT" | grep -oE "0 漏 / [0-9]+ cmd" | head -1)
    echo "[O2] PASS · $O2_DETAIL"
else
    O2_STATUS="FAIL"
    O2_DETAIL="run-dangerous-24 RC=$O2_RC"
    echo "[O2] FAIL · RC=$O2_RC"
    echo "$O2_OUT" | tail -10 >&2
fi
echo ""

# === O3:bootstrap-verify(T010)+ eval-events-count(T011)===
echo "----- O3: bootstrap-verify (T010) + eval-events-count (T011) -----"
O3_BS_OUT=$(bash "$T010_RUNNER" 2>&1)
O3_BS_RC=$?
O3_EV_OUT=$(bash "$T011_RUNNER" 2>&1)
O3_EV_RC=$?
if [[ "$O3_BS_RC" == "0" ]] && [[ "$O3_EV_RC" == "0" ]] \
    && echo "$O3_BS_OUT" | grep -q "BOOTSTRAP-OK" \
    && echo "$O3_EV_OUT" | grep -qE "O3 quant OK"; then
    O3_STATUS="PASS"
    O3_DETAIL=$(echo "$O3_EV_OUT" | grep -oE "O3 quant OK: [0-9]+ events, 3 types covered")
    echo "[O3] PASS · bootstrap-verify OK · $O3_DETAIL"
else
    O3_STATUS="FAIL"
    O3_DETAIL="bootstrap RC=$O3_BS_RC eval RC=$O3_EV_RC"
    echo "[O3] FAIL · $O3_DETAIL"
    echo "$O3_BS_OUT" | tail -5 >&2
    echo "$O3_EV_OUT" | tail -5 >&2
fi
echo ""

# === O4:runtime gen 1 fixture · grep operator_score + producer validator ===
echo "----- O4: hand-back operator_score + producer validator -----"
mkdir -p "$FIXTURE_DIR"
# round 2(F3 修):trap-protected HANDOFF cp + check RC + 同 trap restore 真路径
# 真路径:cp HANDOFF → save · check RC · cp HANDOFF_BAK → HANDOFF · check RC
if ! cp "$HANDOFF" "$HANDOFF_BAK_SAVE"; then
    echo "[O4] FAIL · cp HANDOFF → $HANDOFF_BAK_SAVE 失败" >&2
    O4_STATUS="FAIL"
    O4_DETAIL="HANDOFF backup save 失败(cp RC=$?)"
fi
if [[ "$O4_STATUS" != "FAIL" ]]; then
    if ! cp "$HANDOFF_BAK" "$HANDOFF"; then
        echo "[O4] FAIL · cp HANDOFF_BAK → HANDOFF 失败" >&2
        O4_STATUS="FAIL"
        O4_DETAIL="HANDOFF restore from bak 失败"
        # trap 真路径会用 HANDOFF_BAK_SAVE restore · 不需 manual
    fi
fi
O4_FIXTURE="$FIXTURE_DIR/t012-probe.md"
if [[ "$O4_STATUS" != "FAIL" ]]; then
    O4_GEN_OUT=$(bash "$GEN" --feature 006a-pM --task-id T012-verify-all \
        --tag drift --severity low \
        --section1 "T012 verify-all probe" \
        --section2 "T012 verify-all probe" \
        --section3 "T012 verify-all probe" \
        --rationale "T012 SHIP GATE probe" \
        --out "$O4_FIXTURE" 2>&1)
    O4_GEN_RC=$?
fi
# 真路径还原 HANDOFF.md(同 trap 真路径 · 但这里手 restore + clean save 防 trap 真路径冗余)
if [[ -f "$HANDOFF_BAK_SAVE" ]]; then
    mv -f "$HANDOFF_BAK_SAVE" "$HANDOFF" || git -C "$REPO_ROOT" restore HANDOFF.md 2>/dev/null
fi

# 真路径:O4_STATUS 已为 FAIL(HANDOFF cp 失败)skip
if [[ "$O4_STATUS" == "FAIL" ]]; then
    :  # 已 set FAIL · skip
elif [[ "$O4_GEN_RC" != "0" ]] || [[ ! -f "$O4_FIXTURE" ]]; then
    O4_STATUS="FAIL"
    O4_DETAIL="gen-handback RC=$O4_GEN_RC"
    echo "[O4] FAIL · gen 真路径挂 RC=$O4_GEN_RC"
    echo "$O4_GEN_OUT" | tail -5 >&2
elif ! grep -q "^operator_score: null$" "$O4_FIXTURE"; then
    O4_STATUS="FAIL"
    O4_DETAIL="frontmatter 缺 operator_score: null"
    echo "[O4] FAIL · 真路径 frontmatter 缺 operator_score(T009 真路径 ship 后应有)"
else
    O4_VAL_OUT=$(bash "$VALIDATE" "$O4_FIXTURE" "$IDS_REPO" --mode=producer 2>&1)
    O4_VAL_RC=$?
    if [[ "$O4_VAL_RC" == "0" ]] && echo "$O4_VAL_OUT" | grep -qE "PASS"; then
        O4_STATUS="PASS"
        O4_DETAIL="3 字段 null + producer validator PASS"
        echo "[O4] PASS · 真路径 3 字段 null + producer validator PASS"
    else
        O4_STATUS="FAIL"
        O4_DETAIL="producer validator RC=$O4_VAL_RC"
        echo "[O4] FAIL · producer validator 挂"
        echo "$O4_VAL_OUT" | tail -5 >&2
    fi
fi
echo ""

# === O6:ids-verdict-evidence round-trip(TX03 phase X 加 · per B-4-IDS 协议消费)===
# 真路径目的:验 parallel-builder --ids-verdict-evidence flag 真路径消费 REVIEW-LOG +
# 真路径 hand-back frontmatter 真路径 inject ids_verdict_evidence 父键(7 字段 immutable binding)
echo "----- O6: ids-verdict-evidence round-trip (TX03 phase X) -----"
O6_STATUS="?"
O6_DETAIL=""
O6_TMP=$(mktemp -d "/tmp/o6-ids-verdict-evidence.XXXXXX")
trap 'rm -rf "$O6_TMP" 2>/dev/null' EXIT INT TERM

# 真路径 fixture REVIEW-LOG.md(verdict: approve · 7 字段齐)
O6_REVIEW_LOG="$O6_TMP/REVIEW-LOG.md"
O6_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$O6_REVIEW_LOG" <<O6EOF
---
schema_version: 0.1
review_type: adversarial-review
target_file: working-tree
verdict: approve
findings_count: 0
codex_model: gpt-5-4
duration_seconds: 12.3
ts: ${O6_TS}
---

# Review · working-tree · ${O6_TS}
O6 fixture for ids-verdict-evidence round-trip
O6EOF

# R1 P1 真路径修(per codex)· 真路径 O6 真路径不只验 fixture 真路径 schema · 真路径必须真路径模拟
# hand-back inject + frontmatter ids_verdict_evidence 父键真路径 + 7 字段 immutable binding 真路径
# 真路径 step 1:校 fixture REVIEW-LOG schema(per codex-review SKILL §3.6.3 真路径)
O6_RL_VERDICT=$(awk '/^---$/{n++;next} n==1 && /^verdict:/{print $2;exit}' "$O6_REVIEW_LOG")
O6_RL_FINDINGS=$(awk '/^---$/{n++;next} n==1 && /^findings_count:/{print $2;exit}' "$O6_REVIEW_LOG")
O6_RL_REVIEW_TYPE=$(awk '/^---$/{n++;next} n==1 && /^review_type:/{print $2;exit}' "$O6_REVIEW_LOG")
O6_RL_TARGET_FILE=$(awk '/^---$/{n++;next} n==1 && /^target_file:/{print $2;exit}' "$O6_REVIEW_LOG")
O6_RL_TS=$(awk '/^---$/{n++;next} n==1 && /^ts:/{print $2;exit}' "$O6_REVIEW_LOG")
O6_RL_CODEX_MODEL=$(awk '/^---$/{n++;next} n==1 && /^codex_model:/{print $2;exit}' "$O6_REVIEW_LOG")
O6_RL_SHA=$(shasum -a 256 "$O6_REVIEW_LOG" | awk '{print $1}')

# step 1 真路径 fail-closed check(7 字段齐 + enum + non-neg int)
O6_SCHEMA_OK=0
if [[ "$O6_RL_VERDICT" == "approve" ]] \
    && echo "$O6_RL_FINDINGS" | grep -qE '^[0-9]+$' \
    && [[ -n "$O6_RL_REVIEW_TYPE" && -n "$O6_RL_TARGET_FILE" && -n "$O6_RL_TS" && -n "$O6_RL_CODEX_MODEL" && -n "$O6_RL_SHA" ]]; then
    O6_SCHEMA_OK=1
fi

# step 2 真路径调 real producer 真路径 gen-handback.sh + 真路径 inject ids_verdict_evidence(per codex R2 P2 真路径修)
# 真路径模拟 parallel-builder SKILL §3.1.1 真路径 export 真路径 IDS_VERDICT_EVIDENCE_* 真路径 + §6.1 真路径 python inject 真路径
O6_FAKE_HB="$O6_TMP/o6-real-handback.md"
O6_GEN="$REPO_ROOT/lib/handback-validator/gen-handback.sh"
if [[ ! -x "$O6_GEN" ]]; then
    O6_STATUS="FAIL"
    O6_DETAIL="gen-handback.sh 真路径不可执行: $O6_GEN"
    echo "[O6] FAIL · $O6_DETAIL" >&2
    O6_SCHEMA_OK=0
fi

# 真路径调 real gen-handback.sh 真路径产 draft
if bash "$O6_GEN" \
    --feature "006a-pM-v0.2" \
    --task-id "O6-evidence-test" \
    --tag "self-test" \
    --severity "low" \
    --rationale "O6 ids-verdict-evidence round-trip self-test" \
    --section1 "## §1 O6 真路径 self-test · evidence inject" \
    --section2 "## §2 fake review_type · O6 fixture" \
    --section3 "## §3 no action · self-test" \
    --out "$O6_FAKE_HB" \
    --repo-root "$REPO_ROOT" 2>/dev/null; then
    # 真路径调 parallel-builder SKILL §6.1 真路径 python inject 真路径(per SHARED-CONTRACT §6 B-4-IDS 真路径)
    IDS_VERDICT_EVIDENCE_VERDICT="$O6_RL_VERDICT" \
    IDS_VERDICT_EVIDENCE_FINDINGS="$O6_RL_FINDINGS" \
    IDS_VERDICT_EVIDENCE_LOG_PATH="$O6_REVIEW_LOG" \
    IDS_VERDICT_EVIDENCE_LOG_SHA256="$O6_RL_SHA" \
    IDS_VERDICT_EVIDENCE_TARGET_FILE="$O6_RL_TARGET_FILE" \
    IDS_VERDICT_EVIDENCE_TS="$O6_RL_TS" \
    IDS_VERDICT_EVIDENCE_CODEX_MODEL="$O6_RL_CODEX_MODEL" \
    python3 - <<O6PYEOF
import os
draft = "$O6_FAKE_HB"
with open(draft, "r") as f:
    content = f.read()
block = """ids_verdict_evidence:
  verdict: {v}
  findings_count: {f}
  review_log_path: {p}
  review_log_sha256: {s}
  target_file: {t}
  ts: {ts}
  codex_model: {m}
""".format(
    v=os.environ["IDS_VERDICT_EVIDENCE_VERDICT"],
    f=os.environ["IDS_VERDICT_EVIDENCE_FINDINGS"],
    p=os.environ["IDS_VERDICT_EVIDENCE_LOG_PATH"],
    s=os.environ["IDS_VERDICT_EVIDENCE_LOG_SHA256"],
    t=os.environ["IDS_VERDICT_EVIDENCE_TARGET_FILE"],
    ts=os.environ["IDS_VERDICT_EVIDENCE_TS"],
    m=os.environ["IDS_VERDICT_EVIDENCE_CODEX_MODEL"],
)
new_content = content.replace("related_task:", block + "related_task:", 1)
with open(draft, "w") as f:
    f.write(new_content)
O6PYEOF
else
    O6_STATUS="FAIL"
    O6_DETAIL="real gen-handback.sh 真路径 producer 失败"
    echo "[O6] FAIL · $O6_DETAIL" >&2
fi

# step 3 真路径 parse hand-back ids_verdict_evidence 真路径 + 真路径 SHA rehash check
O6_HB_VERDICT=$(awk '/^---$/{n++;next} n==1 && /^[[:space:]]+verdict:/{print $2;exit}' "$O6_FAKE_HB")
O6_HB_FINDINGS=$(awk '/^---$/{n++;next} n==1 && /^[[:space:]]+findings_count:/{print $2;exit}' "$O6_FAKE_HB")
O6_HB_RL_SHA=$(awk '/^---$/{n++;next} n==1 && /^[[:space:]]+review_log_sha256:/{print $2;exit}' "$O6_FAKE_HB")

# step 4 真路径 fail-closed:hand-back 字段必须 = REVIEW-LOG 字段 + 真路径 rehash 真路径 = 写时 SHA
O6_INJECT_OK=0
if [[ "$O6_HB_VERDICT" == "$O6_RL_VERDICT" \
    && "$O6_HB_FINDINGS" == "$O6_RL_FINDINGS" \
    && "$O6_HB_RL_SHA" == "$O6_RL_SHA" ]]; then
    # rehash 真路径校验(防 stale REVIEW-LOG 真路径)
    O6_REHASH=$(shasum -a 256 "$O6_REVIEW_LOG" | awk '{print $1}')
    if [[ "$O6_REHASH" == "$O6_HB_RL_SHA" ]]; then
        O6_INJECT_OK=1
    fi
fi

if [[ "$O6_SCHEMA_OK" == "1" && "$O6_INJECT_OK" == "1" ]]; then
    O6_STATUS="PASS"
    O6_DETAIL="REVIEW-LOG schema OK + hand-back inject OK + SHA rehash 一致 · sha=${O6_RL_SHA:0:16}..."
    echo "[O6] PASS · ids-verdict-evidence round-trip · $O6_DETAIL"
else
    O6_STATUS="FAIL"
    O6_DETAIL="schema_ok=$O6_SCHEMA_OK inject_ok=$O6_INJECT_OK · verdict=$O6_RL_VERDICT findings=$O6_RL_FINDINGS"
    echo "[O6] FAIL · $O6_DETAIL" >&2
fi
echo ""

# === (f) 表格汇总 ===
echo "================================================================="
echo "SHIP GATE 结果汇总"
echo "================================================================="
printf '%-6s %-10s %s\n' "OUT" "STATUS" "DETAIL"
printf '%-6s %-10s %s\n' "---" "------" "------"
printf '%-6s %-10s %s\n' "O1" "$O1_STATUS" "$O1_DETAIL"
printf '%-6s %-10s %s\n' "O2" "$O2_STATUS" "$O2_DETAIL"
printf '%-6s %-10s %s\n' "O3" "$O3_STATUS" "$O3_DETAIL"
printf '%-6s %-10s %s\n' "O4" "$O4_STATUS" "$O4_DETAIL"
printf '%-6s %-10s %s\n' "O6" "$O6_STATUS" "$O6_DETAIL"
echo ""

# === (g) 末尾自动 cleanup ===
# round 2(codex round 1 F2 修):cleanup RC + prod drift 真路径都加入 ship gate
# 失败 → ship gate FAIL · 不能 silent WARN 真路径 SHIP-READY
echo "----- cleanup -----"
CLEANUP_OUT=$(bash "$T008_CLEANUP" --apply 2>&1)
CLEANUP_RC=$?
echo "$CLEANUP_OUT"

CLEANUP_STATUS="PASS"
CLEANUP_DETAIL=""
if [[ "$CLEANUP_RC" != "0" ]]; then
    CLEANUP_STATUS="FAIL"
    CLEANUP_DETAIL="manual-cleanup-t008.sh RC=$CLEANUP_RC"
    echo "[cleanup] FAIL · manual-cleanup-t008.sh RC=$CLEANUP_RC" >&2
fi

# rm fixture dir(check 真路径)
if [[ -d "$FIXTURE_DIR" ]]; then
    if ! rm -rf "$FIXTURE_DIR"; then
        CLEANUP_STATUS="FAIL"
        CLEANUP_DETAIL="${CLEANUP_DETAIL:+$CLEANUP_DETAIL · }rm fixture-dir 失败"
        echo "[cleanup] FAIL · rm $FIXTURE_DIR 失败" >&2
    else
        echo "[cleanup] 真路径 rm .work/t012-fixture/"
    fi
fi
echo ""

# === production 真路径验跑后不破(F2 修:drift 也 FAIL · 不仅 WARN)===
PROD_AFTER=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f 2>/dev/null | wc -l | tr -d ' ')
PROD_STATUS="PASS"
PROD_DETAIL=""
if [[ "$PROD_AFTER" != "$PROD_BEFORE" ]]; then
    PROD_STATUS="FAIL"
    PROD_DETAIL="production hand-back 数变化 · before=$PROD_BEFORE after=$PROD_AFTER"
    echo "[prod-check] FAIL · $PROD_DETAIL" >&2
    echo "  真路径检 manual-cleanup 真路径是否漏 / verify-all 真路径误删 production" >&2
else
    PROD_DETAIL="production 不动(before=$PROD_BEFORE after=$PROD_AFTER)"
fi

# === (f.2) 真路径加 cleanup + prod 到 status 表 ===
printf '%-6s %-10s %s\n' "CLN" "$CLEANUP_STATUS" "$CLEANUP_DETAIL"
printf '%-6s %-10s %s\n' "PROD" "$PROD_STATUS" "$PROD_DETAIL"
echo ""

# === (h) ship gate decision · 真路径 F1+F2 修 ===
# F1 修:O1 PARTIAL 真路径 unconditional 加入 · distinct status TECH-READY
# (operator 必须看到 PARTIAL 真路径才能 distinguish 完整 SHIP-READY)
# F2 修:CLEANUP_STATUS + PROD_STATUS 真路径也 block
HAS_FAIL=0
HAS_PARTIAL=0
for s in "$O1_STATUS" "$O2_STATUS" "$O3_STATUS" "$O4_STATUS" "$O6_STATUS" "$CLEANUP_STATUS" "$PROD_STATUS"; do
    [[ "$s" == "FAIL" ]] && HAS_FAIL=1
    [[ "$s" == "PARTIAL" ]] && HAS_PARTIAL=1
done

if [[ "$HAS_FAIL" == "1" ]]; then
    echo "================================================================="
    echo "SHIP GATE FAIL · 任一 Outcome/CLEANUP/PROD FAIL · v0.1 NOT ready"
    echo "================================================================="
    exit 1
fi

# 真路径区分 TECH-READY(PARTIAL 真路径) vs SHIP-READY(全 PASS)
# F1 修:PARTIAL 真路径不能产 SHIP-READY · operator 误用 exit 0 真路径假 ship
# round 3(codex round 2 F4 修):exit code distinct · SHIP-READY=0 · TECH-READY=2
# 真路径 caller 真路径 `verify-all && ship` 真路径只 trigger SHIP-READY · TECH-READY 真路径 short-circuit
if [[ "$HAS_PARTIAL" == "1" ]]; then
    echo "================================================================="
    echo "TECH-READY · producer+consumer half 真路径过 · IDS verdict half 待 operator"
    echo "================================================================="
    echo "(真路径下一步:operator 切 IDS session · 跑 /handback-review 006 · ≥7 个 hand-back approve 才真 SHIP-READY)"
    echo "(真路径 exit code = 2 · distinct from SHIP-READY = 0 · caller 真路径用 exit code 真路径 distinguish)"
    exit 2
fi

echo "================================================================="
echo "SHIP-READY"
echo "================================================================="
echo "(全 Outcomes + CLEANUP + PROD 真路径 PASS · v0.1 真 ship-ready · exit code = 0)"
exit 0
