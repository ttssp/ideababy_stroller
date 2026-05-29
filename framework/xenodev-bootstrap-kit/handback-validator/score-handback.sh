#!/usr/bin/env bash
# score-handback.sh — operator 真路径打 score 进 hand-back frontmatter
# per specs/006a-pM/tasks/T009.md(amendment 2026-05-25 · SSOT writer.sh JSON 接口)
#
# 用法:
#   bash score-handback.sh <handback-file> <score 0-10> [--rationale "<text>"]
#
# 行为:
#   (a) 校验 file 存在 + score 0-10 整数 · 违反 exit 2
#   (b) python3 line-by-line 替换 3 字段(operator_score / _at / _rationale)
#   (c) score < 7 → writer.sh JSON 输入 emit operator_interventions event
#   (d) 打印 frontmatter diff 摘要 + stderr summary
#
# 退码:
#   0 = 全过 + 字段真路径更新
#   1 = python3 替换失败 / writer.sh emit 失败(非阻塞 · 只 WARN)
#   2 = 入参非法 / file 不存在 / frontmatter 缺 3 字段

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WRITER="$REPO_ROOT/lib/eval-event-log/writer.sh"

usage() {
    cat <<'EOF' >&2
Usage: score-handback.sh <handback-file> <score 0-10> [--rationale "<text>"]

Score a hand-back. Updates frontmatter 3 fields:
  operator_score: <score>
  operator_score_at: <ISO ts>
  operator_score_rationale: <rationale | "(none)">

If score < 7, emits operator_interventions event to .eval/events.jsonl (writer.sh).

Exit codes:
  0 = success
  1 = python3 replace fail / writer.sh emit fail
  2 = invalid args / file 缺 / frontmatter 缺 operator_score 字段
EOF
}

# === Parse args ===
HANDBACK_FILE=""
SCORE=""
RATIONALE="(none)"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --rationale)
            # round 3(codex round 2 P3 修):check $# 足 防 --rationale 末尾真路径 $2 unbound
            if [[ $# -lt 2 ]]; then
                echo "ERR: --rationale 缺值(真路径需 1 个 text 参数)" >&2
                usage
                exit 2
            fi
            RATIONALE="$2"
            shift 2
            ;;
        --help|-h) usage; exit 0 ;;
        -*) echo "ERR: unknown option: $1" >&2; usage; exit 2 ;;
        *)
            if [[ -z "$HANDBACK_FILE" ]]; then
                HANDBACK_FILE="$1"
            elif [[ -z "$SCORE" ]]; then
                SCORE="$1"
            else
                echo "ERR: 多余位置参数: $1" >&2
                usage
                exit 2
            fi
            shift
            ;;
    esac
done

# === (a) 入参校验 ===
if [[ -z "$HANDBACK_FILE" || -z "$SCORE" ]]; then
    echo "ERR: 缺 handback-file 或 score" >&2
    usage
    exit 2
fi

if [[ ! -f "$HANDBACK_FILE" ]]; then
    echo "ERR: handback file 不存在: $HANDBACK_FILE" >&2
    exit 2
fi

# score 真路径 0-10 整数(regex match · `0|1|...|9|10`)
if ! [[ "$SCORE" =~ ^(10|[0-9])$ ]]; then
    echo "ERR: score 必须 0-10 整数 · got: '$SCORE'" >&2
    exit 2
fi

# === 真路径 ts 算(ISO + compact)===
SCORE_AT_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EVENT_TS=$(date -u +%Y%m%dT%H%M%SZ)
HANDBACK_BASENAME=$(basename "$HANDBACK_FILE")

# === (b) python3 line-by-line 替换 frontmatter 3 字段 ===
# 真路径设计:
#   - 真路径只在 frontmatter (--- ... ---) 内替换 · 不动 body
#   - 真路径检 3 字段都存在 · 任一缺 → exit 2
#   - 真路径 idempotent:已 score 过的 hand-back 再 score 真路径覆盖(不要求 null 初值)
REPLACE_RESULT=$(SCORE="$SCORE" SCORE_AT="$SCORE_AT_ISO" RATIONALE="$RATIONALE" \
HANDBACK="$HANDBACK_FILE" \
python3 -c '
import os, sys, io, re
hb = os.environ["HANDBACK"]
score = os.environ["SCORE"]
score_at = os.environ["SCORE_AT"]
rationale = os.environ["RATIONALE"]

with io.open(hb, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 真路径找 frontmatter 边界(2 个 --- 真路径行)
fm_start = None
fm_end = None
for i, line in enumerate(lines):
    s = line.strip()
    if s == "---":
        if fm_start is None:
            fm_start = i
        else:
            fm_end = i
            break
if fm_start is None or fm_end is None:
    print("BAD: frontmatter 边界(--- 2 行)未找到")
    sys.exit(1)

# 真路径检 3 字段在 frontmatter 内
needed = {"operator_score", "operator_score_at", "operator_score_rationale"}
seen = set()
for i in range(fm_start + 1, fm_end):
    s = lines[i].strip()
    for field in needed:
        if s.startswith(field + ":"):
            seen.add(field)
missing = needed - seen
if missing:
    print("BAD: frontmatter 缺字段(老版本 hand-back 或非 hand-back · per T009 amendment 用 gen-handback.sh 真路径产新): " + ", ".join(sorted(missing)))
    sys.exit(2)

# 真路径替换 3 字段(line-by-line · 只动 frontmatter 内 · 不动 body)
for i in range(fm_start + 1, fm_end):
    s = lines[i]
    if s.startswith("operator_score:"):
        lines[i] = "operator_score: " + score + "\n"
    elif s.startswith("operator_score_at:"):
        lines[i] = "operator_score_at: " + score_at + "\n"
    elif s.startswith("operator_score_rationale:"):
        # 真路径转义 rationale 防 yaml 注入:
        # round 2(codex round 1 F1 修):用 yaml double-quoted scalar 真路径包
        # 防 yaml 特殊字符破:`:`(map key 边界)/ `#`(注释)/ `\n`(多行)/ ``、`{`、`[` 等
        # 真路径只需 escape `\` 和 `"` 即可(其他特殊字符在 double-quoted scalar 内真路径无效)
        r = rationale
        if any(ord(c) < 0x20 and c not in ("\t",) for c in r):
            print("BAD: rationale 含控制字符(防 yaml 注入)")
            sys.exit(2)
        if len(r) > 200:
            r = r[:200]
        # YAML double-quoted scalar 真路径 escape:`\` → `\\` · `"` → `\"`
        r_escaped = r.replace("\\", "\\\\").replace("\"", "\\\"")
        lines[i] = "operator_score_rationale: \"" + r_escaped + "\"\n"

with io.open(hb, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("OK")
' 2>&1)
REPLACE_RC=$?

if [[ "$REPLACE_RC" != "0" ]]; then
    echo "ERR: frontmatter 替换失败 · $REPLACE_RESULT" >&2
    # 真路径:python3 sys.exit(2) = input invalid(缺字段 / rationale 含控制字符 / 含双引号)→ exit 2
    # python3 sys.exit(1) = unexpected error(frontmatter 边界没找到)→ exit 1
    if [[ "$REPLACE_RC" == "2" ]]; then
        exit 2
    fi
    exit 1
fi

# === (c) score < 7 → writer.sh emit operator_interventions event ===
EVENT_EMITTED="no"
if [[ "$SCORE" -lt 7 ]]; then
    # 真路径拼 details(SSOT details free text · max 500 chars)
    # 拼:intervention=low_score_handback target=<basename> score=<n> rationale=<前 100 chars>
    R_SHORT="$RATIONALE"
    [[ ${#R_SHORT} -gt 100 ]] && R_SHORT="${R_SHORT:0:100}"
    DETAILS="intervention=low_score_handback target=${HANDBACK_BASENAME} score=${SCORE} rationale=${R_SHORT}"
    # 真路径用 python3 严转义 JSON(防 details 含特殊字符破)
    EVENT=$(python3 -c '
import json, sys
print(json.dumps({
    "ts": sys.argv[1],
    "event_type": "operator_interventions",
    "task_id": "score-handback",
    "details": sys.argv[2]
}))
' "$EVENT_TS" "$DETAILS")

    # round 2(codex round 1 F2 修):export EVAL_LOG_DIR=$REPO_ROOT/.eval
    # 真路径同 T006 round 4 学到 — writer.sh 内默认用 cwd · operator 从非 repo root
    # 跑会写错位置 · operator 显式 EVAL_LOG_DIR 仍优先(test 隔离不破)
    export EVAL_LOG_DIR="${EVAL_LOG_DIR:-$REPO_ROOT/.eval}"

    # 真路径 emit(失败 WARN 不阻 · 同 T006 wrapper 真路径设计)
    if echo "$EVENT" | bash "$WRITER" 2>/dev/null; then
        EVENT_EMITTED="yes"
    else
        echo "WARN: writer.sh emit operator_interventions event 失败(EVAL_LOG_DIR=$EVAL_LOG_DIR 可能不可写)" >&2
        # 真路径不退 1 · 不阻 score 更新(operator 已打分了)
    fi
fi

# === (d) print summary ===
echo "[score-handback] hand-back: $HANDBACK_FILE"
echo "[score-handback] operator_score: $SCORE / 10"
echo "[score-handback] operator_score_at: $SCORE_AT_ISO"
echo "[score-handback] operator_score_rationale: $RATIONALE"
if [[ "$SCORE" -lt 7 ]]; then
    if [[ "$EVENT_EMITTED" == "yes" ]]; then
        echo "[score-handback] LOW SCORE(< 7)· 真路径 emit operator_interventions event"
    else
        echo "[score-handback] LOW SCORE(< 7)· event emit 失败(见 WARN · operator 真路径手 emit)"
    fi
fi

exit 0
