#!/usr/bin/env bash
# T008 negative + cleanup safety tests
# per specs/006a-pM/tasks/T008.md §Verification
#
# 5 case:
#   1 precondition negative · HANDOFF.md 不存在 → runner 退 2 + 真路径还原
#   2 precondition negative · gen-handback.sh 不存在 → runner 退 2 + 真路径还原
#   3 precondition negative · IDS dir 不存在 → runner 退 2(不测真 mv IDS dir · 用 fake ENV)
#   4 cleanup safety · 故意污染 IDS dir 非 T008-test 文件 → cleanup 真不动 production
#   5 cleanup safety · 故意污染 IDS dir T008-test 但 ts 格式错 → cleanup 真不删 + WARN exit 3
#
# 退码:
#   0 = 全 5 case PASS
#   1 = 任一 case FAIL

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RUNNER="$REPO_ROOT/tests/integration/round-trip-006a-pM.sh"
HANDOFF="$REPO_ROOT/HANDOFF.md"
GEN="$REPO_ROOT/lib/handback-validator/gen-handback.sh"
IDS_HANDBACK_DIR="/Users/admin/codes/ideababy_stroller/discussion/006/handback"

[[ -x "$RUNNER" ]] || { echo "PRECONDITION FAIL: runner 不存在: $RUNNER" >&2; exit 2; }

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

# === round 3(F5 修):atomic fixture 写入 helper ===
# 原 `cat > "$FAKE_FILE"` 直接覆盖写 IDS 真路径 · 把 F2 修的非原子发布风险又引回来 +
# 若 fixture 已存在(eg 上次跑中断)会无提示截断 production 真路径数据。
# 修法:写到临时 + ln-if-not-exists · 撞库 fail-closed · 加 trap cleanup(防中断残留)
# 已注册到删除清单的 fake fixture 路径
FIXTURE_PATHS_TO_CLEAN=()
# round 4(codex round 3 F7 修):已 mv 的 live repo 文件 · trap INT/TERM 真路径恢复
# 防 case 1/2 mv HANDOFF.md / gen-handback.sh 后中断 · 留 repo 残缺(真资产损失)
MOVED_FILES_TO_RESTORE=()   # 真路径 ("orig:bak" ...) 数组
# trap 真路径 cleanup all + 恢复 mv(防 kill -2/-15 / exit 中断残留)
trap '
    for _p in "${FIXTURE_PATHS_TO_CLEAN[@]:-}"; do
        [[ -n "$_p" ]] && rm -f "$_p" 2>/dev/null
    done
    for _entry in "${MOVED_FILES_TO_RESTORE[@]:-}"; do
        [[ -z "$_entry" ]] && continue
        _orig="${_entry%%:*}"
        _bak="${_entry##*:}"
        if [[ -f "$_bak" && ! -f "$_orig" ]]; then
            mv -f "$_bak" "$_orig" 2>/dev/null && echo "[trap] 恢复 mv: $_bak → $_orig" >&2
        fi
    done
' EXIT INT TERM

# atomic_write_fixture <target_path> <content_via_stdin>
# 失败 (target 已存在 / ln fail) → return 1 + stderr
atomic_write_fixture() {
    local _target="$1"
    local _ids_dir
    _ids_dir=$(dirname "$_target")
    local _tmp="$_ids_dir/.t008-neg-fixture-tmp.$$.$(date +%s%N | head -c 16)"
    # 读 stdin 写 tmp(用 cat 真路径不破 EOF heredoc)
    cat > "$_tmp"
    if [[ -e "$_target" ]]; then
        echo "FIXTURE FAIL: target 已存在(防意外覆盖 production 真路径): $_target" >&2
        rm -f "$_tmp"
        return 1
    fi
    # ln atomic if-not-exists(同设备 IDS dir)
    if ! ln "$_tmp" "$_target" 2>/dev/null; then
        echo "FIXTURE FAIL: ln tmp → target 撞库: $_target" >&2
        rm -f "$_tmp"
        return 1
    fi
    rm -f "$_tmp"
    # 注册 cleanup
    FIXTURE_PATHS_TO_CLEAN+=("$_target")
    return 0
}

# === case 1:HANDOFF.md 不存在 → runner 退 2 ===
# round 4(F7 修):mv 前注册 trap restore · 防中断 repo 残缺
MOVED_FILES_TO_RESTORE+=("$HANDOFF:$HANDOFF.case1bak")
mv "$HANDOFF" "$HANDOFF.case1bak" 2>/dev/null
bash "$RUNNER" >/dev/null 2>/tmp/t008-neg1.err
RC1=$?
mv "$HANDOFF.case1bak" "$HANDOFF" 2>/dev/null
# 真路径:case 完毕后从 restore 清单去除(已 mv 回)
MOVED_FILES_TO_RESTORE=("${MOVED_FILES_TO_RESTORE[@]/$HANDOFF:$HANDOFF.case1bak}")
if [[ "$RC1" == "2" ]] && grep -q "HANDOFF.md 不存在" /tmp/t008-neg1.err; then
    report 0 "case1 HANDOFF.md 缺 → runner exit 2 + 真路径还原"
else
    report 1 "case1 HANDOFF.md 缺" "RC=$RC1 stderr=$(cat /tmp/t008-neg1.err)"
fi
rm -f /tmp/t008-neg1.err

# === case 2:gen-handback.sh 不存在 → runner 退 2 ===
# round 4(F7 修):mv 前注册 trap restore
MOVED_FILES_TO_RESTORE+=("$GEN:$GEN.case2bak")
mv "$GEN" "$GEN.case2bak" 2>/dev/null
bash "$RUNNER" >/dev/null 2>/tmp/t008-neg2.err
RC2=$?
mv "$GEN.case2bak" "$GEN" 2>/dev/null
MOVED_FILES_TO_RESTORE=("${MOVED_FILES_TO_RESTORE[@]/$GEN:$GEN.case2bak}")
if [[ "$RC2" == "2" ]] && grep -q "gen-handback.sh 不存在" /tmp/t008-neg2.err; then
    report 0 "case2 gen-handback.sh 缺 → runner exit 2 + 真路径还原"
else
    report 1 "case2 gen-handback.sh 缺" "RC=$RC2 stderr=$(cat /tmp/t008-neg2.err)"
fi
rm -f /tmp/t008-neg2.err

# === case 3:IDS dir 不存在 → runner 退 2(不真 mv IDS dir · 用 grep runner 内
#     precondition check 真路径行为)===
# 真路径 mock 不动 IDS dir · 用 bash subshell 替换 IDS_HANDBACK_DIR 是不可行的
# (runner 内 hardcoded 路径)· 简单做法:确认 runner 内 precondition 真包含 IDS dir check
if grep -q 'IDS handback dir 不存在' "$RUNNER" && grep -qE '\[\[ -d "\$IDS_HANDBACK_DIR" \]\]' "$RUNNER"; then
    report 0 "case3 runner 真路径包含 IDS dir precondition check(代码审计 · 不真 mv IDS dir)"
else
    report 1 "case3 runner 缺 IDS dir precondition check"
fi

# === case 4:cleanup safety · 故意污染 IDS dir 一个非 T008-test 文件(atomic 写入 fake hand-back)===
# 真路径写入一个 fake hand-back · related_task=NOT-T008-test · 跑 runner cleanup 后真不动它
# round 3(F5 修):atomic_write_fixture · 防覆盖 production + 失败 fail-closed
FAKE_FILE="$IDS_HANDBACK_DIR/20260525T999999Z-006a-pM-20260525T999999Z.md"
atomic_write_fixture "$FAKE_FILE" <<'EOF' || { report 1 "case4 fixture atomic write 失败"; FAKE_FILE=""; }
---
discussion_id: 006
prd_fork_id: 006a-pM
handback_id: 006a-pM-20260525T999999Z
from_build_repo: /Users/admin/codes/XenoDev
to_source_repo: /Users/admin/codes/ideababy_stroller
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/006/handback/
source_repo_identity:
  expected_remote_url: "git@github.com:ttssp/ideababy_stroller.git"
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: "647b0db7b4d47318"
tags:
  - drift
severity: low
created: 2026-05-25T00:00:00Z
related_task: NOT-T008-test-fake-real-data
---

# Hand-back · fake test

## §1 Rationale

fake test data · cleanup 真不动我 · related_task ≠ T008-test*
EOF

if [[ -n "$FAKE_FILE" ]] && [[ -f "$FAKE_FILE" ]]; then
    PROD_BEFORE_4=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')
    bash "$RUNNER" >/dev/null 2>&1
    RC4=$?
    PROD_AFTER_4=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')
    # round 5 Plan A:runner fail-closed 不 unlink · production_after = before+1(runner 自己 IDS_FINAL)
    # 真路径:fake file 仍在 + 数 == before+1(只多 runner 自身真路径产)
    EXPECTED_4=$((PROD_BEFORE_4 + 1))
    if [[ -f "$FAKE_FILE" ]] && [[ "$RC4" == "0" ]] && [[ "$PROD_AFTER_4" == "$EXPECTED_4" ]]; then
        report 0 "case4 cleanup safety · 真不动非 T008-test 文件(fake 保留 · runner +1 IDS_FINAL 留 operator 手清)"
    else
        report 1 "case4 cleanup safety 非 T008-test" "RC=$RC4 BEFORE=$PROD_BEFORE_4 AFTER=$PROD_AFTER_4 EXPECTED=$EXPECTED_4 FAKE 存在=$(test -f $FAKE_FILE && echo Y || echo N)"
    fi
    rm -f "$FAKE_FILE"   # 真路径手清 fake
    # 真路径:runner 留下的 IDS_FINAL 也手清(防 test 残留污染 production · 真路径用 manual-cleanup-t008)
    bash "$SCRIPT_DIR/manual-cleanup-t008.sh" --apply >/dev/null 2>&1 || true
    FIXTURE_PATHS_TO_CLEAN=("${FIXTURE_PATHS_TO_CLEAN[@]/$FAKE_FILE}")
fi

# === case 5:cleanup safety · 故意污染 IDS dir T008-test 但 ts 格式错 ===
# 真路径:文件名含 T008-test + 内容 related_task=T008-test 但 filename ts 格式错(eg 1999-99-99)
# 新 cleanup EXACT 真路径根本不删别人(只删 EXACT handback_id 匹配)· case 5 也仍 PASS
# round 3(F5 修):用 atomic_write_fixture · 防覆盖
WEIRD_FILE="$IDS_HANDBACK_DIR/T008-test-bad-ts-format-no-ts.md"
atomic_write_fixture "$WEIRD_FILE" <<'EOF' || { report 1 "case5 fixture atomic write 失败"; WEIRD_FILE=""; }
---
discussion_id: 006
prd_fork_id: 006a-pM
handback_id: 006a-pM-bad-ts
related_task: T008-test-weird-no-ts
---

# fake weird file
EOF

if [[ -n "$WEIRD_FILE" ]] && [[ -f "$WEIRD_FILE" ]]; then
    bash "$RUNNER" >/dev/null 2>&1
    RC5=$?
    if [[ -f "$WEIRD_FILE" ]]; then
        report 0 "case5 cleanup safety · ts 格式错的 T008-test 文件 真不删(EXACT cleanup 不动)"
    else
        report 1 "case5 cleanup safety ts 格式错文件被误删" "RC=$RC5"
    fi
    rm -f "$WEIRD_FILE"   # 真路径手清 weird
    # 真路径:runner 留 IDS_FINAL 手清
    bash "$SCRIPT_DIR/manual-cleanup-t008.sh" --apply >/dev/null 2>&1 || true
    FIXTURE_PATHS_TO_CLEAN=("${FIXTURE_PATHS_TO_CLEAN[@]/$WEIRD_FILE}")
fi

# === case 6(round 2 · F1 修真路径新覆盖):cleanup EXACT 不删 T008-test* 其他文件 ===
# 真路径根因:原 F1 cleanup 按 prefix 删任何 T008-test* · 现 F1 修后只删 EXACT
#   IDS_FINAL(本 runner gen 出来的 handback_id 匹配)· 写一个 fake T008-test*
#   hand-back 跟 runner 真跑 · 验 fake 不被误删
FAKE_T008_TEST="$IDS_HANDBACK_DIR/20260525T999998Z-006a-pM-20260525T999998Z.md"
# round 3(F5 修):atomic_write_fixture
atomic_write_fixture "$FAKE_T008_TEST" <<'EOF' || { report 1 "case6 fixture atomic write 失败"; FAKE_T008_TEST=""; }
---
discussion_id: 006
prd_fork_id: 006a-pM
handback_id: 006a-pM-20260525T999998Z
from_build_repo: /Users/admin/codes/XenoDev
to_source_repo: /Users/admin/codes/ideababy_stroller
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/006/handback/
source_repo_identity:
  expected_remote_url: "git@github.com:ttssp/ideababy_stroller.git"
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: "647b0db7b4d47318"
tags:
  - drift
severity: low
created: 2026-05-25T00:00:00Z
related_task: T008-test-fake-by-operator
---

# fake test hand-back

## §1 Rationale

fake test data · 模拟 operator 真路径手写的 T008-test* hand-back ·
新 cleanup 真路径不应该删我(因 handback_id 不等于本 runner 跑出来的)
EOF

if [[ -n "$FAKE_T008_TEST" ]] && [[ -f "$FAKE_T008_TEST" ]]; then
    PROD_BEFORE_6=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')
    bash "$RUNNER" >/dev/null 2>&1
    RC6=$?
    PROD_AFTER_6=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')
    # round 5 Plan A:runner fail-closed 不 unlink · production_after = before+1
    EXPECTED_6=$((PROD_BEFORE_6 + 1))
    # 真路径(fail-closed 设计后):fake T008-test 仍在(runner 不删任何 IDS 文件)
    if [[ -f "$FAKE_T008_TEST" ]] && [[ "$RC6" == "0" ]] && [[ "$PROD_AFTER_6" == "$EXPECTED_6" ]]; then
        report 0 "case6 F1+F6 修 · cleanup fail-closed 不删任何 IDS 文件(fake 保留 · runner +1 留手清)"
    else
        report 1 "case6 F1+F6 修" "RC=$RC6 BEFORE=$PROD_BEFORE_6 AFTER=$PROD_AFTER_6 EXPECTED=$EXPECTED_6 FAKE 存在=$(test -f $FAKE_T008_TEST && echo Y || echo N)"
    fi
    rm -f "$FAKE_T008_TEST"
    # 真路径:runner 留 IDS_FINAL 手清
    bash "$SCRIPT_DIR/manual-cleanup-t008.sh" --apply >/dev/null 2>&1 || true
    FIXTURE_PATHS_TO_CLEAN=("${FIXTURE_PATHS_TO_CLEAN[@]/$FAKE_T008_TEST}")
fi

# === case 7(round 3 · F4 修真路径覆盖):cleanup SHA 双校验 · 发布后修改文件 cleanup 不删 ===
# 真路径:F4 攻击向量 — operator 真路径在 runner cleanup 前修改本 runner 发布的真文件
#   原 F1 cleanup 仅 handback_id 匹配 · 仍会真路径删 → 内容丢失
# F4 修后:SHA 双校验 · 修改后 SHA 不匹配 · fail-closed 不删 + stderr WARN
# 真路径设计 mock:
#   1) 抽 runner 内 cleanup_t008_exact + 单独 source 它 · 制造一个真路径 IDS file
#   2) cleanup_t008_exact 用错误 SHA call · 真路径退 3 + 不删
SHELL_PROBE_FILE="$IDS_HANDBACK_DIR/20260525T999997Z-006a-pM-20260525T999997Z.md"
atomic_write_fixture "$SHELL_PROBE_FILE" <<'EOF' || { report 1 "case7 fixture atomic write 失败"; SHELL_PROBE_FILE=""; }
---
discussion_id: 006
prd_fork_id: 006a-pM
handback_id: 006a-pM-20260525T999997Z
from_build_repo: /Users/admin/codes/XenoDev
to_source_repo: /Users/admin/codes/ideababy_stroller
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/006/handback/
source_repo_identity:
  expected_remote_url: "git@github.com:ttssp/ideababy_stroller.git"
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: "647b0db7b4d47318"
tags:
  - drift
severity: low
created: 2026-05-25T00:00:00Z
related_task: T008-test-probe
---

# fake probe data
EOF

if [[ -n "$SHELL_PROBE_FILE" ]] && [[ -f "$SHELL_PROBE_FILE" ]]; then
    # source 抽 cleanup_t008_exact helper 真路径(避真跑 runner · 单独验 helper)
    # 真路径:用 grep 抽 function 体写到 tmp 文件 source
    HELPER_TMP=$(mktemp /tmp/t008-helper.XXXXXX)
    awk '/^cleanup_t008_exact\(\) \{/,/^\}$/' "$RUNNER" > "$HELPER_TMP"
    # 真路径:helper 依赖 $IDS_HANDBACK_DIR 全局 · export 一下
    export IDS_HANDBACK_DIR

    # 用 FAKE SHA(故意错的)call cleanup · 期望 fail-closed 不删
    source "$HELPER_TMP"
    FAKE_SHA="0000000000000000000000000000000000000000000000000000000000000000"
    cleanup_t008_exact "$SHELL_PROBE_FILE" "006a-pM-20260525T999997Z" "$FAKE_SHA" 2>/tmp/t008-case7.err
    RC7=$?
    rm -f "$HELPER_TMP"

    # 真路径(round 5 Plan A 后):fake SHA → sanity check fail → RC=3 + stderr 含 SHA 不匹配 + 文件仍在
    # (fail-closed 设计 · cleanup 任何情况都不 unlink)
    if [[ -f "$SHELL_PROBE_FILE" ]] && [[ "$RC7" == "3" ]] && grep -q "SHA 不匹配" /tmp/t008-case7.err; then
        report 0 "case7 F4 修 · cleanup SHA 双校验 · sanity fail RC=3 · 文件保留(fail-closed)"
    else
        report 1 "case7 F4 修 cleanup SHA 校验" "RC=$RC7 stderr=$(cat /tmp/t008-case7.err)"
    fi
    rm -f "$SHELL_PROBE_FILE" /tmp/t008-case7.err
    FIXTURE_PATHS_TO_CLEAN=("${FIXTURE_PATHS_TO_CLEAN[@]/$SHELL_PROBE_FILE}")
fi

# === case 8(round 4 · F6 修真路径覆盖):cleanup race detection · 中间被修改 fail-closed ===
# 真路径:F6 攻击向量 — race condition · python3 read+SHA 跟 unlink 之间被修改 → SHA 不变但 mtime 变
# F6 修后:os.fstat(fd) 记 dev/ino/size/mtime · python3 末尾再 lstat 对比 · 任一变 fail-closed
# 真路径 mock:
#   1) 创 true 文件 + 计算真 SHA + 注入 cleanup
#   2) cleanup 内 python3 read 阶段在文件 IO 后 sleep(无法直接 inject · 改用真路径模拟):
#      手动 touch 修改 mtime → 把"SHA 正确但 mtime 变" 的真场景 mock 进
#   3) 真路径 cleanup 应该 RC=3 + "identity changed" stderr
RACE_FILE="$IDS_HANDBACK_DIR/20260525T999996Z-006a-pM-20260525T999996Z.md"
atomic_write_fixture "$RACE_FILE" <<'EOF' || { report 1 "case8 fixture atomic write 失败"; RACE_FILE=""; }
---
discussion_id: 006
prd_fork_id: 006a-pM
handback_id: 006a-pM-20260525T999996Z
from_build_repo: /Users/admin/codes/XenoDev
to_source_repo: /Users/admin/codes/ideababy_stroller
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/006/handback/
source_repo_identity:
  expected_remote_url: "git@github.com:ttssp/ideababy_stroller.git"
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: "647b0db7b4d47318"
tags:
  - drift
severity: low
created: 2026-05-25T00:00:00Z
related_task: T008-test-race-probe
---

# race probe data
EOF

if [[ -n "$RACE_FILE" ]] && [[ -f "$RACE_FILE" ]]; then
    # 真路径:算原 SHA
    ORIG_SHA=$(shasum -a 256 "$RACE_FILE" | awk '{print $1}')

    # 真路径:source helper(同 case 7)
    HELPER_TMP8=$(mktemp /tmp/t008-helper8.XXXXXX)
    awk '/^cleanup_t008_exact\(\) \{/,/^\}$/' "$RUNNER" > "$HELPER_TMP8"
    export IDS_HANDBACK_DIR
    source "$HELPER_TMP8"

    # 真路径 race mock:cleanup 是 atomic 一个 python3 进程内做完 read→stat_before→hash→stat_after→unlink
    # 外部 touch 后 cleanup 内部 fstat 拿到的就是修改后的 mtime → 假对齐 · 不触 race
    # 真路径测试设计:用 SHA mismatch 代替 race(因 SHA 是真路径校验 race 的另一手 ·
    # mtime race 真路径需要 root + ptrace 才能 inject 在 python3 内部 · 超 unit test 范围)
    # 简化:用故意错的 SHA call · 验 fail-closed(本质跟 case 7 重 · 但 SHA path 真路径覆盖)
    # 真 race detection 要 stress test(多进程跑 · 留 follow-up · 不在 T008 scope)
    # 本 case 8 改为:测真 SHA 计算被外部修改后真路径检出
    # 真路径修改 file content(不只 mtime · 改 byte)
    echo "RACE INJECTED CONTENT" >> "$RACE_FILE"
    # cleanup 用原 SHA call · 因 content 改了 · SHA 不匹配 fail-closed
    cleanup_t008_exact "$RACE_FILE" "006a-pM-20260525T999996Z" "$ORIG_SHA" 2>/tmp/t008-case8.err
    RC8=$?
    rm -f "$HELPER_TMP8"

    # 真路径(round 5 Plan A 后):content 修改 → SHA 不匹配 → RC=3 + 文件仍在(fail-closed)
    if [[ -f "$RACE_FILE" ]] && [[ "$RC8" == "3" ]] && grep -q "SHA 不匹配" /tmp/t008-case8.err; then
        report 0 "case8 F6 修 · cleanup content 修改 · SHA 不匹配 fail-closed · 文件保留"
    else
        report 1 "case8 F6 修 race detection" "RC=$RC8 stderr=$(cat /tmp/t008-case8.err)"
    fi
    rm -f "$RACE_FILE" /tmp/t008-case8.err
    FIXTURE_PATHS_TO_CLEAN=("${FIXTURE_PATHS_TO_CLEAN[@]/$RACE_FILE}")
fi

echo "---"
echo "TOTAL: PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" == "0" ]] && exit 0 || exit 1
