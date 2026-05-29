#!/usr/bin/env bash
# T008 manual cleanup · 真路径删 IDS dir 内本 runner 留下的 T008-test* hand-back
# per round 5 F6 Plan A 决议:round-trip runner 改 fail-closed 不自动 unlink ·
# operator 真路径用本 script 手清(防 path-level TOCTOU race · 真路径根因消除)
#
# 真路径:
#   1) 用户 dry-run 看会删什么:bash manual-cleanup-t008.sh
#   2) 真删:bash manual-cleanup-t008.sh --apply
#
# 退码:
#   0 = dry-run 列出或真删完
#   1 = 真删失败
#   2 = precondition fail

set -uo pipefail

IDS_HANDBACK_DIR="/Users/admin/codes/ideababy_stroller/discussion/006/handback"
[[ -d "$IDS_HANDBACK_DIR" ]] || { echo "PRECONDITION FAIL: IDS handback dir 不存在: $IDS_HANDBACK_DIR" >&2; exit 2; }

# round 5(codex T012 round 4 F9 修):python3 precondition 必须真路径在首扫前
# 防 python3 缺/挂 → CANDIDATES 空 → 假"IDS dir clean" exit 0 → 真 T008-test 残留
command -v python3 >/dev/null 2>&1 || { echo "PRECONDITION FAIL: python3 缺(manual-cleanup 真路径依赖)" >&2; exit 2; }

APPLY="0"
[[ "${1:-}" == "--apply" ]] && APPLY="1"

# 真路径筛 T008-test* hand-back · python3 真路径校 frontmatter related_task
# round 5 F9 修:scan stderr 真路径捕 + RC 真路径 check · 非 0 exit 1 hard-fail
SCAN1_STDERR=$(mktemp /tmp/t008-cleanup-scan1-err.XXXXXX 2>/dev/null) || SCAN1_STDERR=/dev/stderr
trap '[[ "$SCAN1_STDERR" != "/dev/stderr" ]] && rm -f "$SCAN1_STDERR"' EXIT

CANDIDATES=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f 2>/dev/null | python3 -c '
import os, re, sys
ids_dir = sys.argv[1]
ids_real = os.path.realpath(ids_dir)
for line in sys.stdin:
    p = line.strip()
    if not p:
        continue
    real = os.path.realpath(p)
    if not real.startswith(ids_real + os.sep):
        continue
    basename = os.path.basename(real)
    if not basename.endswith(".md"):
        continue
    try:
        with open(real, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        sys.stderr.write("WARN: read fail " + p + ": " + str(e) + "\n")
        continue
    parts = content.split("---")
    if len(parts) < 2:
        continue
    m = re.search(r"^related_task:\s*(\S+)\s*$", parts[1], re.MULTILINE)
    if m and m.group(1).startswith("T008-test"):
        print(real)
' "$IDS_HANDBACK_DIR" 2>"$SCAN1_STDERR")
SCAN1_RC=$?

# F9 修:scan1 RC 真路径 check · 非 0 hard-fail(防 silent 假 clean)
if [[ "$SCAN1_RC" != "0" ]]; then
    echo "[manual-cleanup-t008] FAIL · 初扫 python3 真路径挂 RC=$SCAN1_RC" >&2
    [[ -s "$SCAN1_STDERR" ]] && cat "$SCAN1_STDERR" >&2
    exit 1
fi
# stderr WARN 真路径透传(防 silent · 即使 RC=0)
[[ -s "$SCAN1_STDERR" ]] && cat "$SCAN1_STDERR" >&2

if [[ -z "$CANDIDATES" ]]; then
    echo "[manual-cleanup-t008] 无 T008-test* hand-back 残留 · IDS dir 干净"
    exit 0
fi

COUNT=$(echo "$CANDIDATES" | wc -l | tr -d ' ')
echo "[manual-cleanup-t008] 找到 $COUNT 个 T008-test* hand-back:"
echo "$CANDIDATES" | sed 's/^/  /'

if [[ "$APPLY" == "0" ]]; then
    echo ""
    echo "DRY-RUN 模式 · 真删请加 --apply:"
    echo "  bash $0 --apply"
    exit 0
fi

# 真删
# round 5(codex T012 round 2 F5 修):rm 失败累积 → exit 1(原 silent exit 0)
# + post-cleanup scan 真路径 zero T008-test 残留 verify(不靠 PROD count)
DELETED=0
RM_FAILED=0
while IFS= read -r _f; do
    [[ -z "$_f" ]] && continue
    if rm -f "$_f"; then
        DELETED=$((DELETED + 1))
        echo "[manual-cleanup-t008] 删: $_f"
    else
        echo "[manual-cleanup-t008] 删失败: $_f" >&2
        RM_FAILED=$((RM_FAILED + 1))
    fi
done <<< "$CANDIDATES"

echo "[manual-cleanup-t008] 真路径删完 $DELETED 个 T008-test* hand-back"

# round 5 F5 修:post-cleanup scan · 真路径 zero T008-test 残留 verify
# round 6(codex T012 round 3 F8 修):
#   - python3 precondition check(避免 silent missing python3 → REMAINING 空 false-PASS)
#   - 真路径 python3 stderr 真路径不 suppress(防 silent error → REMAINING 空 false-PASS)
#   - python3 真路径 exit code 真路径 check · 非 0 exit 1 hard-fail
command -v python3 >/dev/null 2>&1 || { echo "[manual-cleanup-t008] FAIL · python3 缺(post-cleanup scan 真路径依赖)" >&2; exit 1; }

SCAN_STDERR=$(mktemp /tmp/t008-cleanup-scan-err.XXXXXX 2>/dev/null) || SCAN_STDERR=/dev/stderr
trap '[[ "$SCAN_STDERR" != "/dev/stderr" ]] && rm -f "$SCAN_STDERR"' EXIT

REMAINING=$(find "$IDS_HANDBACK_DIR" -maxdepth 1 -name '*.md' -type f 2>/dev/null | python3 -c '
import os, re, sys
for line in sys.stdin:
    p = line.strip()
    if not p:
        continue
    try:
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        sys.stderr.write("WARN: read fail " + p + ": " + str(e) + "\n")
        continue
    parts = content.split("---")
    if len(parts) < 2:
        continue
    m = re.search(r"^related_task:\s*(\S+)\s*$", parts[1], re.MULTILINE)
    if m and m.group(1).startswith("T008-test"):
        print(p)
' 2>"$SCAN_STDERR")
SCAN_RC=$?

# 真路径:python3 scan 真路径 RC check + stderr 真路径透传
if [[ "$SCAN_RC" != "0" ]]; then
    echo "[manual-cleanup-t008] FAIL · post-cleanup scan python3 真路径挂 RC=$SCAN_RC" >&2
    [[ -s "$SCAN_STDERR" ]] && cat "$SCAN_STDERR" >&2
    exit 1
fi
# 真路径:即使 scan rc=0 但 stderr 真路径有 WARN · 也打 stderr(不阻 ship · 但 operator 真路径可见)
[[ -s "$SCAN_STDERR" ]] && cat "$SCAN_STDERR" >&2

# 真路径:REMAINING 空真路径 wc -l = 0(不像 grep -c · 不会因 0 match exit 1)
if [[ -z "$REMAINING" ]]; then
    REMAIN_COUNT=0
else
    REMAIN_COUNT=$(printf '%s\n' "$REMAINING" | wc -l | tr -d ' \n')
fi

if [[ "$RM_FAILED" -gt "0" ]] || [[ "$REMAIN_COUNT" != "0" ]]; then
    echo "[manual-cleanup-t008] FAIL · rm_failed=$RM_FAILED · 残留 T008-test 数=$REMAIN_COUNT" >&2
    [[ "$REMAIN_COUNT" != "0" ]] && echo "$REMAINING" | sed 's/^/  残留: /' >&2
    exit 1
fi

exit 0
