#!/usr/bin/env bash
# T008 round-trip integration test · O1 + PPV P1 真路径主验
# per specs/006a-pM/tasks/T008.md(amendment 2026-05-25 对齐 T007 CLI)
#
# 行为(per spec §"Outputs" amendment):
#   (a) precondition check:gen-handback.sh + HANDOFF.md + IDS dir 真路径
#   (b) gen draft(T007 CLI:--section1/2/3 + --rationale · 不用 --ship/--expected)
#   (c) cp draft → IDS dir(filename ${TS}-006a-pM-${TS}.md · 双 ts 跟 §6.2.1 约束 5 齐)
#   (d) consumer validate 6 约束 PASS
#   (e) cleanup IDS dir 内 T008-test 文件(双质点 glob + ls 预检查 + 数量上限)
#   (f) echo round-trip OK 退 0
#
# 退码:
#   0 = round-trip 全 PASS
#   1 = consumer validate 挂 / cp 挂 / gen 挂
#   2 = precondition fail
#   3 = cleanup 检测到非预期 IDS dir 状态(stderr WARN · 不删 · operator 手 cleanup)

set -uo pipefail   # 不开 -e(要捕中间 RC 真路径)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
GEN="$REPO_ROOT/lib/handback-validator/gen-handback.sh"
VALIDATE="$REPO_ROOT/lib/handback-validator/validate-handback.sh"
HANDOFF="$REPO_ROOT/HANDOFF.md"
IDS_REPO="/Users/admin/codes/ideababy_stroller"
IDS_HANDBACK_DIR="$IDS_REPO/discussion/006/handback"

# === (a) precondition ===
[[ -x "$GEN" ]]      || { echo "PRECONDITION FAIL: gen-handback.sh 不存在或不可执行: $GEN" >&2; exit 2; }
[[ -x "$VALIDATE" ]] || { echo "PRECONDITION FAIL: validate-handback.sh 不存在或不可执行: $VALIDATE" >&2; exit 2; }
[[ -f "$HANDOFF" ]]  || { echo "PRECONDITION FAIL: HANDOFF.md 不存在: $HANDOFF" >&2; exit 2; }
[[ -d "$IDS_HANDBACK_DIR" ]] || { echo "PRECONDITION FAIL: IDS handback dir 不存在: $IDS_HANDBACK_DIR" >&2; exit 2; }
command -v python3 >/dev/null || { echo "PRECONDITION FAIL: python3 缺(cleanup 真路径校验依赖)" >&2; exit 2; }

# === ts 生成(本地 ts 仅用于 task_id 区分本次跑 · IDS final filename 用 gen 真路径
# 算出来的 ts · per §6.2.1 约束 5:filename handback_id 必须 == frontmatter handback_id
# · gen-handback.sh line 169 自己算 ts 写入 frontmatter · caller 必须读 frontmatter
# 真 ts 反推 IDS final filename(否则会撞 ts 不一致 fail 约束 5))===
LOCAL_TS=$(date -u +%Y%m%dT%H%M%SZ)
TASK_ID="T008-test-${LOCAL_TS}"
DRAFT="/tmp/t008-draft-${LOCAL_TS}.md"
# 真路径:IDS_FINAL + HANDBACK_ID + PUBLISHED_SHA 在 gen/publish 后反算 · 提前 declare 防 trap unbound
IDS_FINAL=""
HANDBACK_ID=""
PUBLISHED_SHA=""
PUBLISH_TMP=""

# 初始 trap:只清本地 draft + 临时 tmp(IDS_FINAL/HANDBACK_ID 还没值)· 后续 ln 成功后
# 真路径 re-register trap 加 cleanup_t008_exact(见 line 200+ ln 后)
trap 'rm -f "$DRAFT" "$PUBLISH_TMP" 2>/dev/null' EXIT

# === cleanup helper · round 3(codex round 2 F4 修)真路径双校验 handback_id + SHA ===
# F1+F4 真路径根因:
#   round 1 F1:cleanup 按 prefix 删 · 可能误删 operator/另 runner 的真文件
#   round 1 F1 修:用 handback_id EXACT 匹配
#   round 2 F4(真路径仍漏):若 operator 在发布后真路径修改/替换同 handback_id 文件 ·
#     仍被本 runner 删 → IDS 真 hand-back 或人工修复内容丢失
# round 3 修(double-quality EXACT):
#   - 发布后记 PUBLISHED_SHA(发布到 IDS 时的真 SHA)
#   - cleanup 时双校验 handback_id == expected + 真路径 SHA == PUBLISHED_SHA
#   - 任一不匹配 → fail-closed 不删 + stderr WARN(operator 真路径手 cleanup · 防丢内容)
cleanup_t008_exact() {
    local _ids_final="$1"
    local _expected_handback_id="$2"
    local _expected_sha="${3:-}"

    if [[ -z "$_ids_final" || -z "$_expected_handback_id" ]]; then
        return 0
    fi

    if [[ ! -f "$_ids_final" ]]; then
        return 0
    fi

    # round 5(codex round 4 high 修 · break-cap-by-fix Plan A):
    # F6 真路径仍 path-level TOCTOU(lstat → unlink 之间被替换)· 真路径根因消除:
    #   **改 fail-closed 不自动 unlink** · 只 report + 让 operator 手清
    # 真路径权衡:
    #   - cleanup 不删 = 真路径 race 完全消除(没 unlink 就没 TOCTOU 数据丢失)
    #   - operator 手清 = README + stderr 给出清晰命令 · 跟 hand-back schema 命名一致
    #   - production IDS dir 真路径不会被本 runner 误删任何文件(更安全)
    # F4+F5+F6 全消(从根上不 unlink IDS 文件)· 真消除 race · 改 ship gate 设计
    # 真路径校验仍跑(handback_id + SHA 双校验)· 但只为 sanity check + report ·
    # 不再 unlink · operator 真路径用 stderr 给出的 rm 命令手清

    # 真路径 sanity check(handback_id + SHA 双校验 · 不 unlink)
    local _result
    _result=$(python3 -c '
import os, re, sys, hashlib
p = sys.argv[1]
ids_dir = sys.argv[2]
expected_hbid = sys.argv[3]
expected_sha = sys.argv[4]
real = os.path.realpath(p)
ids_real = os.path.realpath(ids_dir)
if not real.startswith(ids_real + os.sep):
    print("BAD: 路径不在 IDS dir 内 · " + real)
    sys.exit(1)
try:
    with open(real, "rb") as f:
        raw = f.read(1 << 20)
except Exception as e:
    print("BAD: read fail · " + str(e))
    sys.exit(1)
if expected_sha:
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != expected_sha:
        print("BAD: SHA 不匹配 · expected=" + expected_sha[:16] + "... actual=" + actual_sha[:16] + "...")
        sys.exit(1)
content = raw.decode("utf-8", errors="replace")
parts = content.split("---")
if len(parts) < 2:
    print("BAD: no frontmatter")
    sys.exit(1)
m = re.search(r"^handback_id:\s*(\S+)\s*$", parts[1], re.MULTILINE)
if not m:
    print("BAD: 缺 handback_id")
    sys.exit(1)
hbid = m.group(1)
if hbid != expected_hbid:
    print("BAD: handback_id 不匹配 · got=" + hbid + " expected=" + expected_hbid)
    sys.exit(1)
print("OK")
' "$_ids_final" "$IDS_HANDBACK_DIR" "$_expected_handback_id" "$_expected_sha" 2>&1)
    local _rc=$?

    if [[ "$_rc" == "0" ]] && [[ "$_result" == "OK" ]]; then
        # 真路径:sanity check 通过 · 但 fail-closed 设计 不 unlink
        # operator 真路径手清 · README + stderr 给出清晰 rm 命令
        echo "[cleanup] sanity check PASS (handback_id + SHA 双匹配)" >&2
        echo "[cleanup] 真路径 fail-closed 设计 · operator 手清(防 path-level TOCTOU race · per F6+F7+F8 决议):" >&2
        echo "  rm '$_ids_final'" >&2
        echo "[cleanup] 或一次清所有 T008-test*:bash $SCRIPT_DIR/manual-cleanup-t008.sh" >&2
        return 0
    else
        echo "CLEANUP WARN: sanity check fail · 不报清理命令 · $_result" >&2
        return 3
    fi
}

# round 2(codex F1 修):删跑前 batch cleanup · operator 手 cleanup 残留(见 README)
# 这里只 snapshot production 文件数 · 跑完后断言 == before(本 runner 自己 cleanup 自己)
PROD_COUNT_BEFORE=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')
echo "[round-trip] 跑前 IDS dir 文件数 = $PROD_COUNT_BEFORE"

# === (b) gen draft · T007 CLI ===
"$GEN" \
    --feature 006a-pM \
    --task-id "$TASK_ID" \
    --tag drift \
    --severity low \
    --rationale "T008 round-trip integration test(auto · runner=round-trip-006a-pM.sh ts=$LOCAL_TS)" \
    --section1 "T008 round-trip auto test · ts=$LOCAL_TS" \
    --section2 "auto test by tests/integration/round-trip-006a-pM.sh · skip cleanup 会污染 production" \
    --section3 "test 完后 cleanup_t008_safe() 真路径删 T008-test 文件 · production hand-back 一个不少" \
    --out "$DRAFT" 2>/tmp/t008-gen.err
GEN_RC=$?

if [[ "$GEN_RC" != "0" ]]; then
    echo "FAIL [b]: gen-handback.sh exit $GEN_RC · stderr:" >&2
    cat /tmp/t008-gen.err >&2
    rm -f /tmp/t008-gen.err
    exit 1
fi

if [[ ! -f "$DRAFT" ]]; then
    echo "FAIL [b]: gen 退 0 但 draft 文件不存在: $DRAFT" >&2
    exit 1
fi

# === 真路径反算 IDS_FINAL filename · per §6.2.1 约束 5(filename ts == frontmatter handback_id ts)===
# gen-handback.sh line 169 自己算 ts 写 frontmatter handback_id · caller 必须读真 ts 反推 filename
# (bug 2 修:不能用 LOCAL_TS · 因 LOCAL_TS 跟 gen 内 ts 可能相差 1-N 秒)
HANDBACK_ID=$(python3 -c '
import re, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    content = f.read()
parts = content.split("---")
if len(parts) < 2:
    sys.exit(1)
m = re.search(r"^handback_id:\s*(\S+)\s*$", parts[1], re.MULTILINE)
if not m:
    sys.exit(1)
print(m.group(1))
' "$DRAFT" 2>/dev/null)

if [[ -z "$HANDBACK_ID" ]]; then
    echo "FAIL [b]: 解析 draft frontmatter handback_id 失败: $DRAFT" >&2
    exit 1
fi

# 真路径:HANDBACK_ID = ${PRD_FORK_ID}-${TS} (gen line 171)· 抽 ts
GEN_TS="${HANDBACK_ID##*-}"
if [[ -z "$GEN_TS" || "$GEN_TS" == "$HANDBACK_ID" ]]; then
    echo "FAIL [b]: 抽 ts from handback_id 失败: $HANDBACK_ID" >&2
    exit 1
fi
IDS_FINAL="$IDS_HANDBACK_DIR/${GEN_TS}-${HANDBACK_ID}.md"
echo "[round-trip] draft handback_id=$HANDBACK_ID · IDS final=$IDS_FINAL"

# === (c) publish draft → IDS final path · round 2 修 F2 TOCTOU ===
# F2 真路径根因(round 1 codex high):原 check-then-cp 是 TOCTOU
#   if [[ -e $IDS_FINAL ]] ... cp $DRAFT $IDS_FINAL
#   两个并发 runner 都可能 -e 通过然后 cp 撞 · 静默覆盖
# round 2 修:跟 SKILL §6.3 FU-producer-2 一致 · 用 ln(hard link · atomic if-not-exists)
# ln 在 dst 存在时 atomic fail · 无 race · POSIX 保证
# 真路径同设备(IDS dir + /tmp 跨设备),先 cp 到 IDS dir 临时文件 + sha 验等价
# + ln tmp → final · 失败 fail-closed
PUBLISH_TMP="$IDS_HANDBACK_DIR/.t008-tmp.${LOCAL_TS}.$$"

# 真路径 cp draft → IDS dir 临时文件(同设备 · ln 可用)
if ! cp "$DRAFT" "$PUBLISH_TMP"; then
    echo "FAIL [c]: cp draft → publish tmp 失败: $PUBLISH_TMP" >&2
    exit 1
fi

# sha 等价校验(防 cp 半成品)
DRAFT_SHA=$(shasum -a 256 "$DRAFT" | awk '{print $1}')
TMP_SHA=$(shasum -a 256 "$PUBLISH_TMP" | awk '{print $1}')
if [[ "$DRAFT_SHA" != "$TMP_SHA" ]]; then
    echo "FAIL [c]: cp 完后 sha drift · draft=$DRAFT_SHA tmp=$TMP_SHA" >&2
    rm -f "$PUBLISH_TMP"
    exit 1
fi

# ln 原子 reservation(同设备 · POSIX atomic if-not-exists)
if ! ln "$PUBLISH_TMP" "$IDS_FINAL" 2>/dev/null; then
    echo "FAIL [c]: IDS final path ln 撞库(ts collision @ $LOCAL_TS · 间隔 ≥1s 重跑): $IDS_FINAL" >&2
    rm -f "$PUBLISH_TMP"
    exit 1
fi
# ln 成功后真路径删 tmp(只留 final hard link)
rm -f "$PUBLISH_TMP"
PUBLISH_TMP=""   # 真路径:防 trap 再次 rm 报错

# round 3(F4 修):发布后真路径记 PUBLISHED_SHA · cleanup 时双校验防 operator 真路径替换
PUBLISHED_SHA=$(shasum -a 256 "$IDS_FINAL" | awk '{print $1}')

# round 5(F6+F7+F8 决议 Plan A · fail-closed):trap 不再 auto-unlink IDS 文件
# 只 sanity report + 本地 draft 清 · IDS 文件由 operator 真路径手清(防 race)
trap 'cleanup_t008_exact "$IDS_FINAL" "$HANDBACK_ID" "$PUBLISHED_SHA" >/dev/null 2>&1 || true; rm -f "$DRAFT" "$PUBLISH_TMP" 2>/dev/null' EXIT

echo "[round-trip] ln $IDS_FINAL (atomic publish · sha=${PUBLISHED_SHA:0:16}... · 原 draft @ $DRAFT)"

# === (d) consumer validate ===
VALIDATE_OUT=$("$VALIDATE" "$IDS_FINAL" "$IDS_REPO" --mode=consumer 2>&1)
VALIDATE_RC=$?

if [[ "$VALIDATE_RC" != "0" ]]; then
    echo "FAIL [d]: consumer validate exit $VALIDATE_RC · output:" >&2
    echo "$VALIDATE_OUT" >&2
    # 真路径:trap EXIT 会 cleanup IDS_FINAL · 不需手 call
    exit 1
fi

# stderr 真路径含 ✓ all 6 constraints PASS(validator 把 PASS 写 stderr · per T007 学到)
# 这里 VALIDATE_OUT 是合并 stdout + stderr · grep 全 output
if ! echo "$VALIDATE_OUT" | grep -qE "all 6 constraints PASS|consumer.*PASS"; then
    echo "FAIL [d]: consumer validate 退 0 但 output 不含 'all 6 constraints PASS':" >&2
    echo "$VALIDATE_OUT" >&2
    exit 1
fi

echo "[round-trip] consumer validate 6 约束 PASS"

# === (e) cleanup sanity report · round 5 Plan A fail-closed 真路径不 unlink ===
cleanup_t008_exact "$IDS_FINAL" "$HANDBACK_ID" "$PUBLISHED_SHA"
CLEANUP_RC=$?

if [[ "$CLEANUP_RC" != "0" ]]; then
    echo "FAIL [e]: cleanup sanity check 异常 RC=$CLEANUP_RC(handback_id 或 SHA 不匹配)" >&2
    exit 1
fi

# === 跑后 snapshot production 文件数(本 runner 真路径 +1 · 防其他污染)===
PROD_COUNT_AFTER=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')
EXPECTED_AFTER=$((PROD_COUNT_BEFORE + 1))
if [[ "$PROD_COUNT_AFTER" != "$EXPECTED_AFTER" ]]; then
    echo "FAIL [e]: 跑后 IDS dir 文件数异常 · before=$PROD_COUNT_BEFORE after=$PROD_COUNT_AFTER expected=$EXPECTED_AFTER" >&2
    exit 1
fi
echo "[round-trip] 跑后 IDS dir 文件数 = $PROD_COUNT_AFTER(本 runner +1 = $EXPECTED_AFTER · 待 operator 手清)"

# === (f) 全过 · operator 真路径需手清 IDS_FINAL ===
echo "round-trip OK: $IDS_FINAL"
echo ""
echo "==============================================================="
echo "OPERATOR 真路径需手清(防 race · per round 5 F6 Plan A 决议):"
echo "  rm '$IDS_FINAL'"
echo "或一次清所有 T008-test* hand-back:"
echo "  bash $SCRIPT_DIR/manual-cleanup-t008.sh"
echo "==============================================================="
exit 0
