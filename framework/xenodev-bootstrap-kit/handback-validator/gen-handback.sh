#!/usr/bin/env bash
# gen-handback.sh — 产 hand-back .md 草稿,严格对齐 §6.3 schema + 强制 SSOT
# per FU-producer-1 spec + round 1 codex findings(F1/F2/F3/F4):
#   - 三字段 source_repo_identity(expected_remote_url / repo_marker / git_common_dir_hash)
#     必读 HANDOFF.md 真值,不接受 CLI override(防绕 SSOT)
#   - 缺任一字段 fail-closed,exit 1
#   - 复用 _yaml-helpers.sh 解析 frontmatter(0 新依赖)
#   - F1 修(round 1):CLI scalar allowlist 校验 + source_repo_identity 块在所有
#     用户输入字段之前 + 生成后断言三字段等于 HANDOFF 抽取值
#   - F2 修:frontmatter schema 严格对齐 test-fixtures/valid/<ts>-008a-pA-<ts>.md
#     (workspace 4 字段含 working_repo / created / related_task)
#   - F3 修:handback_target 撞库检测 → exit 1 让 caller 重 gen TS
#
# Usage:
#   bash gen-handback.sh \
#     --feature <fork-id> --task-id <TID> \
#     --tag <tag>[,<tag>...] --severity <low|medium|high> \
#     --rationale "<text>" \
#     --out <draft.md> \
#     [--repo-root <path>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_yaml-helpers.sh"

# === Parse args ===
FEATURE=""
TASK_ID=""
TAG=""
SEVERITY=""
RATIONALE=""
SECTION1=""
SECTION2=""
SECTION3=""
OUT=""
REPO_ROOT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --feature) FEATURE="$2"; shift 2 ;;
        --task-id|--task) TASK_ID="$2"; shift 2 ;;
        --tag) TAG="$2"; shift 2 ;;
        --severity) SEVERITY="$2"; shift 2 ;;
        --rationale) RATIONALE="$2"; shift 2 ;;
        --section1) SECTION1="$2"; shift 2 ;;
        --section2) SECTION2="$2"; shift 2 ;;
        --section3) SECTION3="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --help|-h)
            sed -n '2,18p' "$0"
            exit 0
            ;;
        *)
            echo "ERR: unknown option: $1" >&2
            echo "  gen-handback.sh 不接受 source_repo_identity 三字段 CLI override" >&2
            echo "  per SSOT 契约,三字段从 HANDOFF.md 读真值。--help 查 usage。" >&2
            exit 2
            ;;
    esac
done

# === T007:@<path> 形式从文件读 section 内容(避命令行 length 限制 + 允许 \n)===
# round 2(codex P1 修):@<path> 加 path traversal + denylist + allowlist:
#   - 拒 absolute path(必须相对 repo root · 防 @/etc/passwd)
#   - 拒 .. 逃逸(realpath 后必须仍在 REPO_ROOT 内 · 防 ../../etc/passwd)
#   - 拒 symlink 指向 REPO_ROOT 外(防 symlink 逃逸)
#   - 拒 .env.production* / .env.prod* / secrets/production/* / secrets/prod/*
#     等 Safety Floor 件 1 凭据隔离路径(per CLAUDE.md 硬约束)
# section 是真 markdown · 允许 \n;但 NUL / 控制字符仍拒(防 YAML 注入)
# round 3:python3 stderr capture file(mktemp fallback /dev/null 保证 cat 不破)
TMPDIR_T007_PYERR=$(mktemp /tmp/t007-py.XXXXXX 2>/dev/null) || TMPDIR_T007_PYERR=/dev/null
# T207(R4 P3)真路径合并:本 EXIT trap 既清 TMPDIR_T007_PYERR 又清 RESERVED(reservation)
# 防 line 370 trap 覆盖丢 T007 临时文件(per codex R4 P3)· 改 single cleanup_all 兜底
# RESERVED 是 T207 default reservation 占位 · 仅在 default 模式置值 · 成功路径前 unset
# R5 P2 真路径加固:无论 partial 与否都清(成功路径 unset RESERVED 由 line 539 负责)·
# 防 sed 写一半 fail 留 partial draft 挡下次重试(per codex R5 P2)
RESERVED=""
cleanup_all() {
    # 件 1:清 T007 python stderr 临时文件
    if [[ "$TMPDIR_T007_PYERR" != "/dev/null" ]]; then
        rm -f "$TMPDIR_T007_PYERR"
    fi
    # 件 2:清 T207 default reservation(成功路径已 unset RESERVED · 这里见到 = fail 路径 · 不论 partial 一律清)
    if [[ -n "$RESERVED" && -f "$RESERVED" ]]; then
        rm -f "$RESERVED"
    fi
}
trap cleanup_all EXIT

# round 4(codex round 3 medium 修):section body 控制字符校验抽 helper · 让 rationale
# backward-compat 路径(SECTION1=$RATIONALE)也走同校验 · 防绕过 ESC/0x01 等控制字符
# round 4 strong-fix(case 25 fail 真路径):原 `grep -qE $'[\x00-\x08...]'` 在某些
# grep 版本上 bash $'...' 字面 `[` 被误认 brackets not balanced → grep 退非 0 →
# `if !` 走 fail-open 路径直接放过控制字符 = bug 真路径(case 25 RC=0 而期望非 0)
# 改 python3 真路径校验(BSD/GNU 跨平台 100% · 不靠 grep regex 兼容性)
# **定义必须在 expand_section_at_file 之前**(bash function call 时查找:expand 内
# 调用 validate · validate 必须先 declare)
validate_section_body() {
    local val="$1" name="$2"
    local _has_ctrl
    _has_ctrl=$(printf '%s' "$val" | python3 -c '
import sys
s = sys.stdin.read()
# round 5(codex round 4 P2 修):用 allowlist 真路径 — 只允许 \t (0x09) + \n (0x0a)
# 其它 0x00-0x1f 全 C0 控制字符(含 0x0d CR 真攻击向量:clean\rhidden 终端覆盖隐藏)
# 都拒(原 round 4 用 deny set 漏 0x0d)
for c in s:
    o = ord(c)
    if o < 0x20 and o not in (0x09, 0x0a):
        sys.stdout.write("BAD: byte 0x{:02x} at pos\n".format(o))
        sys.exit(0)
sys.stdout.write("OK\n")
' 2>/dev/null)
    if [[ "$_has_ctrl" != "OK"* ]]; then
        echo "ERR: --${name} 含 NUL 或控制字符(0x00-0x1f 除 \\t \\n);拒(防 YAML 注入 / hand-back 正文污染) · 真因: $_has_ctrl" >&2
        exit 2
    fi
}

expand_section_at_file() {
    local val="$1" name="$2"
    if [[ "${val:0:1}" == "@" ]]; then
        local path="${val:1}"
        # F1.a:拒 absolute path
        if [[ "${path:0:1}" == "/" ]]; then
            echo "ERR: --${name} @<path> 拒 absolute path(防 path traversal · 必须相对 REPO_ROOT): $path" >&2
            exit 2
        fi
        # 推算 REPO_ROOT(若 sed line 172 还没推算,这里 fallback)
        local _repo_root="${REPO_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
        # round 3(codex round 2 high 修):F1.b/c 合并进同 python3 块 · 用 lower() 真路径
        # case-insensitive 比对 denylist · 防 macOS HFS+/APFS 大小写不敏感文件系统下
        # @.ENV.PRODUCTION.fake 绕过 bash regex(原 line 99 大小写敏感 grep 漏)
        # 同时加更严格的 component-boundary 匹配防 `--env.productionfake` 类误命中
        local resolved
        local _py_err
        resolved=$(cd "$_repo_root" 2>/dev/null && python3 -c '
import os, sys
p = sys.argv[1]
try:
    real = os.path.realpath(p)
    root = os.path.realpath(os.getcwd())
except Exception as ex:
    sys.stderr.write("realpath 失败: " + str(ex) + "\n")
    sys.exit(2)
# F1.b 真路径:逃逸 REPO_ROOT 直接拒
if not (real == root or real.startswith(root + os.sep)):
    sys.stderr.write("path traversal: " + real + " 不在 REPO_ROOT(" + root + ")内\n")
    sys.exit(1)
# F1.c 真路径(round 3 修 · round 4 强化):case-insensitive + Unicode normalize 比对
# Safety Floor 件 1 凭据路径 · 防 .Env.Production / .ｅnv.production(fullwidth)/
# .env．production(fullwidth dot)/ 零宽字符 等绕过(per codex round 3 high)
# 用 unicodedata.normalize("NFKC") + casefold() 把同形/大小写都规范化后再 match
import unicodedata
def _normalize(s):
    # NFKC 把 fullwidth/half-width 等同形字符规范化 + casefold 比 lower() 严
    # 同时去除 0x00-0x1f 控制字符 + 零宽字符(防 .e​env.production 之类)
    s = unicodedata.normalize("NFKC", s)
    # 删零宽字符 + 各种控制字符(BOM/ZWJ/ZWNJ 等)
    s = "".join(c for c in s if unicodedata.category(c) not in ("Cc", "Cf"))
    return s.casefold()
real_canon = _normalize(real)
# 拒任何子组件以 .env.production / .env.prod 起头(eg /a/b/.env.production.bak)
# 拒任何子路径含 /secrets/production/ 或 /secrets/prod/(以 sep 边界匹配)
for forbidden_prefix in [".env.production", ".env.prod"]:
    for comp in real_canon.split(os.sep):
        if comp.startswith(forbidden_prefix):
            sys.stderr.write("Safety Floor 件 1 凭据 denylist: 路径含 " + forbidden_prefix + "* component(canon=" + real_canon + ")· raw real: " + real + "\n")
            sys.exit(3)
for forbidden_substr in [os.sep + "secrets" + os.sep + "production" + os.sep,
                         os.sep + "secrets" + os.sep + "prod" + os.sep]:
    if forbidden_substr in real_canon or real_canon.endswith(forbidden_substr.rstrip(os.sep)):
        sys.stderr.write("Safety Floor 件 1 凭据 denylist: 路径含 " + forbidden_substr.strip(os.sep) + " 目录(canon=" + real_canon + ")· raw real: " + real + "\n")
        sys.exit(3)
print(real)
' "$path" 2>"$TMPDIR_T007_PYERR")
        local _py_rc=$?
        _py_err=$(cat "$TMPDIR_T007_PYERR" 2>/dev/null || true)
        if [[ "$_py_rc" != "0" ]]; then
            if [[ "$_py_rc" == "3" ]]; then
                echo "ERR: --${name} @<path> 拒 Safety Floor 件 1 凭据路径(per CLAUDE.md 三件硬约束之一):" >&2
            elif [[ "$_py_rc" == "1" ]]; then
                echo "ERR: --${name} @<path> path traversal 拒(必须在 REPO_ROOT 内):" >&2
            else
                echo "ERR: --${name} @<path> realpath 失败:" >&2
            fi
            echo "  $_py_err" >&2
            exit 2
        fi
        # 真路径检查
        if [[ ! -f "$resolved" ]]; then
            echo "ERR: --${name} file not found: $path (resolved: $resolved)" >&2
            exit 2
        fi
        # 读文件内容
        val="$(cat "$resolved")"
    fi
    # 拒 NUL + 控制字符 0x01-0x08 + 0x0b + 0x0c + 0x0e-0x1f(允许 \t = 0x09 / \n = 0x0a)
    # round 4(codex round 3 medium 修):抽 helper validate_section_body 单独跑 ·
    # 防 --rationale backward-compat 路径绕过校验(下面统一跑)
    validate_section_body "$val" "$name"
    printf '%s' "$val"
}
[[ -n "$SECTION1" ]] && SECTION1="$(expand_section_at_file "$SECTION1" "section1")"
[[ -n "$SECTION2" ]] && SECTION2="$(expand_section_at_file "$SECTION2" "section2")"
[[ -n "$SECTION3" ]] && SECTION3="$(expand_section_at_file "$SECTION3" "section3")"

# === T007:必须传 --section1 或 --rationale 之一(否则 hand-back §1 空 → 无意义)===
# 显式 check 防 case 3 backward-compat 兜底 false-PASS:
# caller 没传任何 §1 内容时硬挂 + stderr 列缺哪些 flag
if [[ -z "$SECTION1" && -z "$RATIONALE" ]]; then
    echo "ERR: 必须传 --section1 或 --rationale 之一(否则 hand-back §1 内容空)" >&2
    exit 2
fi

# T103 OQ-1=a 真路径修(per FU-producer-1 Case F regression · 2026-05-28):
# 原 dquote reject 真路径包在 `if template 含 {{RATIONALE}}` 内 ·
# T007 ship 后 template 无 placeholder · 整段 skip · F1 YAML inject 防护漏。
# 真路径区分两条 case:
#   - 走 --rationale CLI(无 --section1)→ RATIONALE 兜底 SECTION1 进 body · 仍 reject dquote(F1)
#   - 走 --section1 CLI(显式真传)→ SECTION1 是 markdown body · 允许合法 dquote(T007 case13)
# NUL / 控制字符 reject 已由 line 240 validate_section_body 真路径(python allowlist)cover ·
# 此处只补 dquote 真路径(validate_section_body 无 dquote 拒 · 因 SECTION1 body 允许 markdown dquote)
RATIONALE_FIRSTLINE_T103="${RATIONALE%%$'\n'*}"
if [[ -z "$SECTION1" && -n "$RATIONALE" && "$RATIONALE" != "(none)" ]]; then
    # 走 backward-compat 路径(RATIONALE 兜底 SECTION1 · 进 body 但仍属 CLI 真路径)
    if [[ "$RATIONALE_FIRSTLINE_T103" == *'"'* ]]; then
        echo "ERR: --rationale 含双引号;拒 (防 frontmatter quote 闭合提前)。用单引号或转义" >&2
        exit 2
    fi
fi

# === T007:backward-compat:旧 caller 只传 --rationale 不传 sections ===
# 自动:rationale → §1 · §2/§3 用占位文本(per T007 amendment 兜底)
if [[ -z "$SECTION1" && -n "$RATIONALE" ]]; then
    SECTION1="$RATIONALE"
fi
if [[ -z "$SECTION2" ]]; then
    SECTION2="(待补 · per T007 amendment · operator 跑 gen-handback 时未传 --section2)"
fi
if [[ -z "$SECTION3" ]]; then
    SECTION3="(待补 · per T007 amendment · operator 跑 gen-handback 时未传 --section3)"
fi
# RATIONALE 兜底防 line 59 必填校验挂(backward-compat:RATIONALE 是 T004 原有必填)
[[ -z "$RATIONALE" ]] && RATIONALE="$SECTION1"

# round 4(codex round 3 medium 修):rationale backward-compat / 默认占位字符串都进
# 最终 SECTION1/2/3 · 这里统一跑 validate_section_body 防绕过(原 expand_section_at_file
# 只跑了 @file/直传 直接传的 section · rationale fallback 和 default placeholder 跳过)
validate_section_body "$SECTION1" "section1 (final · 含 rationale backward-compat 兜底)"
validate_section_body "$SECTION2" "section2 (final · 含 default placeholder)"
validate_section_body "$SECTION3" "section3 (final · 含 default placeholder)"

# === 必填校验(amendment 后 SECTION1 必有 · RATIONALE backward-compat 已兜底)===
# 注:OUT 不在必填列表 — T207(C-2)default 兜底在下方 HANDOFF 读 PRD_FORK_ID 后真路径计算
for var_name in FEATURE TASK_ID TAG SEVERITY RATIONALE SECTION1 SECTION2 SECTION3; do
    eval "val=\${$var_name:-}"
    if [[ -z "$val" ]]; then
        echo "ERR: required arg --${var_name,,} missing" >&2
        exit 2
    fi
done

# === F1 修:CLI scalar allowlist 校验(防 YAML 注入)===
# FEATURE / TASK_ID:严格字母数字横线下划线点(allowlist 字符集)
validate_scalar_safe() {
    local val="$1" name="$2" pattern="$3"
    if [[ ! "$val" =~ $pattern ]]; then
        echo "ERR: --${name} value contains illegal chars or pattern. Got: [$val]. Allowed regex: $pattern" >&2
        exit 2
    fi
}
validate_scalar_safe "$FEATURE" "feature" '^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$'
validate_scalar_safe "$TASK_ID"  "task-id" '^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$'

# TAG:enum + 允许逗号分隔
case "$TAG" in
    drift|prd-revision-trigger|practice-stats|spec-gap-fix|feature|spec-gap|self-test|redesign)
        :  # OK
        ;;
    *)
        # 允许多个 tag 逗号分隔,每个都必须在 enum 内
        IFS=',' read -ra TAGS_ARR <<< "$TAG"
        for t in "${TAGS_ARR[@]}"; do
            t_trim=$(echo "$t" | sed -E 's/^[[:space:]]+//;s/[[:space:]]+$//')
            case "$t_trim" in
                drift|prd-revision-trigger|practice-stats|spec-gap-fix|feature|spec-gap|self-test|redesign)
                    : ;;
                *)
                    echo "ERR: --tag '$t_trim' not in enum {drift, prd-revision-trigger, practice-stats, spec-gap-fix, feature, spec-gap, self-test, redesign}" >&2
                    exit 2
                    ;;
            esac
        done
        ;;
esac

# SEVERITY:enum {low, medium, high}
case "$SEVERITY" in
    low|medium|high) : ;;
    *)
        echo "ERR: --severity '$SEVERITY' not in enum {low, medium, high}" >&2
        exit 2
        ;;
esac

# RATIONALE 处理:
# T007 template 已无 {{RATIONALE}}(改为 {{SECTION1/2/3}} body 占位)· RATIONALE 仅作
# backward-compat 兜底 SECTION1 用 · 不进 frontmatter · 真校验在 expand_section_at_file
# 已做(NUL + 控制字符拒 · markdown 双引号合法不破)
# round 2(codex P2-3 修):section1 含合法 markdown 双引号不被原 RATIONALE 严校验误拒。
# round 2 strong-fix(case 2 fail 真路径):RATIONALE 不论 template 是否有 {{RATIONALE}}
# 都截到首行(SECTION1 = multi-line 时不能让 RATIONALE 也跟着 multi-line · 否则
# sed -e "s|{{RATIONALE}}|...|g" 在 BSD sed 报 "unescaped newline inside substitute
# pattern" · 即使 template 无 {{RATIONALE}} 占位 sed 这行仍跑)
TEMPLATE_CHECK="$SCRIPT_DIR/templates/handback.template.md"
RATIONALE_FIRSTLINE="${RATIONALE%%$'\n'*}"
# T103 OQ-1=a:dquote check 在更早的 SECTION1 兜底前真路径做(line 197 之后)·
# 此处保留 RATIONALE_FIRSTLINE 截首行 sed 兼容(原 round-2 strong-fix 防 BSD sed unescaped newline)
# 不论 template 是否有 {{RATIONALE}},RATIONALE 都强制截首行(防 sed 破)
# T007 template 无 {{RATIONALE}} 时 sed 跑这行 -e 是 no-op,但 RATIONALE 多行仍会让
# sed 自身报 "unescaped newline" → 整个 sed 链失败 · 必须截首行
RATIONALE="$RATIONALE_FIRSTLINE"

# === REPO_ROOT 推断(若未传)===
if [[ -z "$REPO_ROOT" ]]; then
    REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

HANDOFF="$REPO_ROOT/HANDOFF.md"
if [[ ! -f "$HANDOFF" ]]; then
    echo "ERR: HANDOFF.md not found at $HANDOFF" >&2
    exit 1
fi

# === 三字段强制读 HANDOFF.md(per FU-producer-1 SSOT 契约)===
EXPECTED_REMOTE_URL=$(require_yaml_field "$HANDOFF" expected_remote_url '  ') || exit 1
REPO_MARKER=$(require_yaml_field "$HANDOFF" repo_marker '  ') || exit 1
GIT_COMMON_DIR_HASH=$(require_yaml_field "$HANDOFF" git_common_dir_hash '  ') || exit 1

# === F1 防御:三字段值本身也要做最小安全校验(防 HANDOFF 被污染)===
# 不允许字段值含换行 / 控制字符 / 双引号(会破 frontmatter quote)
# FU-T207-1 修(per codex T209 review P2):原 `grep -qE $'[\x00-\x08\x0a-\x1f]|"'` 真路径
# bash $'...' 字面 `[` 真路径在某些 grep(macOS BSD grep)被误认 brackets not balanced →
# grep 退 2 → `if ! grep -qE` 当"未匹配"接 → 真路径 fail-open · 污染值进 frontmatter
# 与 line 100 validate_section_body 同模式 · 用 python3 allowlist 真路径校验跨平台 100%
for ssot_field in EXPECTED_REMOTE_URL REPO_MARKER GIT_COMMON_DIR_HASH; do
    eval "ssot_val=\$$ssot_field"
    _check_result=$(printf '%s' "$ssot_val" | python3 -c '
import sys
s = sys.stdin.read()
# 拒 0x00-0x1f 控制字符(除 \t \n)+ 拒双引号(防 frontmatter quote 提前闭合)
for c in s:
    o = ord(c)
    if o < 0x20 and o not in (0x09, 0x0a):
        sys.stdout.write("BAD: ctrl byte 0x{:02x}".format(o))
        sys.exit(0)
    if c == "\"":
        sys.stdout.write("BAD: double quote")
        sys.exit(0)
sys.stdout.write("OK")
' 2>/dev/null)
    if [[ "$_check_result" != "OK" ]]; then
        # bash 3.2 compat:用 tr 真路径 lowercase 真路径(${var,,} 是 bash 4+ · macOS 默认 3.2 真路径)
        _field_lower=$(printf '%s' "$ssot_field" | tr '[:upper:]' '[:lower:]')
        echo "ERR: HANDOFF.md source_repo_identity.${_field_lower} 字段含控制字符或双引号: [$ssot_val] · 真因: $_check_result" >&2
        exit 1
    fi
done

# === 从 HANDOFF.md 拿 discussion_id + prd_fork_id ===
DISCUSSION_ID=$(extract_yaml_field "$HANDOFF" discussion_id '')
[[ -z "$DISCUSSION_ID" ]] && DISCUSSION_ID=$(extract_yaml_field "$HANDOFF" discussion_id '  ')
PRD_FORK_ID=$(extract_yaml_field "$HANDOFF" prd_fork_id '')
[[ -z "$PRD_FORK_ID" ]] && PRD_FORK_ID=$(extract_yaml_field "$HANDOFF" prd_fork_id '  ')
[[ -z "$PRD_FORK_ID" ]] && PRD_FORK_ID="$FEATURE"

if [[ -z "$DISCUSSION_ID" || -z "$PRD_FORK_ID" ]]; then
    echo "ERR: HANDOFF.md 缺 discussion_id 或 prd_fork_id" >&2
    exit 1
fi

# discussion_id / prd_fork_id 也做 allowlist
validate_scalar_safe "$DISCUSSION_ID" "discussion_id (from HANDOFF)" '^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$'
validate_scalar_safe "$PRD_FORK_ID"   "prd_fork_id (from HANDOFF)"   '^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$'

# === T207(C-2)· --out default 计算 + 防 silent overwrite ===
# 结论先:OUT 未传 → default = <PRD_FORK_ID>-<TASK_ID>-handback.md(用 HANDOFF SSOT 真值 · 防 caller 传错 --feature 时 default 名漂移 · per codex R1 P2)
# explicit --out 优先 default(本块 OUT 非空时跳过 · 显式不变)
# default 已存在 → hard-fail · 用 noclobber 原子占位防 TOCTOU 竞态(per codex R2 P2)
# 真路径:并发同 task-id 两进程 check-then-write 会都过 [[ -e ]] check 然后第二个 silent overwrite
# 修法:用 ( set -o noclobber; > "$OUT" ) — open(O_CREAT|O_EXCL) 原子占位 · race-free
# reservation cleanup(per codex R3 P2):中途 fail 留空 file 会挡下次重试 · 必须清
# R4 P3 真路径修:本 trap 已并入 line 73 cleanup_all(防覆盖丢 TMPDIR_T007_PYERR)·
# 这里只赋 RESERVED · 不重 trap · cleanup_all 真路径会处理 0-byte 占位
if [[ -z "$OUT" ]]; then
    OUT="${PRD_FORK_ID}-${TASK_ID}-handback.md"
    # noclobber 原子占位 reservation(若 OUT 已存在 · open 失败 · 子 shell 退非 0)
    if ! ( set -o noclobber; : > "$OUT" ) 2>/dev/null; then
        echo "ERR: default --out 路径已存在,hard-fail 防 silent overwrite: $OUT" >&2
        echo "  Caller 选项:(1) 显式传 --out <new-path> 走 explicit · (2) rm 旧文件后重跑" >&2
        echo "  per CLAUDE.md SHARED-CONTRACT §6.2.1 hard-fail 哲学 · 不缓冲 / 不静默 / 不 retry" >&2
        echo "  注:并发同 task-id 时本 reservation 原子 · 后到进程 race 拒(per codex R2 P2)" >&2
        exit 1
    fi
    # 占位真路径 reserve 成功 · 注册 cleanup · 后续 sed/python 写 OUT 是 overwrite 自己占位的空 file(non-race)
    RESERVED="$OUT"
fi

# === 拼 handback_id + ts + final path ===
# F2 修(round 2):handback_target 是**目录**(末尾 /),FINAL_PATH 是**文件**;
#   契约 fixture(test-fixtures/valid/<ts>-008a-pA-<ts>.md)workspace.handback_target
#   是 dir 路径,check-6 把它当 TARGET_DIR 再 append filename。之前 r1 写成 file
#   路径会让 check-6 拼出 <file>.md/<file>.md broken path。
# F4 修(round 2):created 用 ISO 8601 RFC3339(契约要求),TS 留作 compact id/filename。
TS=$(date -u +%Y%m%dT%H%M%SZ)
CREATED_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HANDBACK_ID="${PRD_FORK_ID}-${TS}"
BASE="${TS}-${HANDBACK_ID}.md"
HANDBACK_TARGET_DIR="/Users/admin/codes/ideababy_stroller/discussion/${DISCUSSION_ID}/handback/"
FINAL_PATH="${HANDBACK_TARGET_DIR}${BASE}"

# === F3 修(round 2 降为 advisory):FINAL_PATH 撞库 advisory check ===
# 注:真原子 reservation 在 SKILL §6.3 的 `ln "$DRAFT" "$TGT"`(ln 在 dst 存在
# 时 atomic fail,无 race)。本处仅 advisory warn — 帮 caller 提前发现同秒
# collision,不替代 ln 原子语义。
if [[ -e "$FINAL_PATH" ]]; then
    echo "ERR: FINAL_PATH already exists (advisory check; ts collision @ $TS): $FINAL_PATH" >&2
    echo "  Caller should wait ≥1s and retry,或确认 SKILL §6.3 ln reservation 流程。" >&2
    exit 1
fi

# === 输出 dir 预创 ===
OUT_DIR="$(dirname "$OUT")"
mkdir -p "$OUT_DIR"

# === T004:template-based 生成(替代 inline here-doc · per spec §"Outputs")===
# template SSOT:templates/handback.template.md · 字段顺序 + YAML 缩进同 fixture
# 替换分隔符用 `|`(因 EXPECTED_REMOTE_URL 含 `:` `/` `@`,用 `/` 会冲突)
# 替换顺序无关(占位符全 `{{VAR}}` 形态,无套娃)
#
# T004 round 2(codex P2 finding):sed replacement 必须 escape `\`/`&`/分隔符 `|`
# 否则 rationale 含 `A & B` → `&` 展开成匹配的 `{{RATIONALE}}` 全占位符
# rationale 含 `A | B` → sed 表达式破坏 "bad flag in substitute command"
# 修法:写 escape_sed_replacement() helper · 入参 raw → 输出 sed-safe
TEMPLATE="$SCRIPT_DIR/templates/handback.template.md"
if [[ ! -f "$TEMPLATE" ]]; then
    echo "ERR: template not found: $TEMPLATE" >&2
    echo "  T004 ship 后 SSOT 是 lib/handback-validator/templates/handback.template.md" >&2
    exit 1
fi

# sed replacement escape helper(POSIX sed BRE):
# - `\` 先 escape(必须最先,后续 escape 会引入新 \)
# - `&` escape(replacement 里 `&` = 整个匹配)
# - `|` escape(本脚本用 `|` 作分隔符)
# 用 bash parameter expansion ${var//pattern/replacement}(0 fork · 0 子 shell)
escape_sed_replacement() {
    local s="$1"
    s="${s//\\/\\\\}"   # \ → \\
    s="${s//&/\\&}"     # & → \&
    s="${s//|/\\|}"     # | → \|
    printf '%s' "$s"
}

# escape 所有 replacement 值(SSOT 三字段 + user input + 推算字段)
E_DISCUSSION_ID=$(escape_sed_replacement "$DISCUSSION_ID")
E_PRD_FORK_ID=$(escape_sed_replacement "$PRD_FORK_ID")
E_HANDBACK_ID=$(escape_sed_replacement "$HANDBACK_ID")
E_REPO_ROOT=$(escape_sed_replacement "$REPO_ROOT")
E_HANDBACK_TARGET_DIR=$(escape_sed_replacement "$HANDBACK_TARGET_DIR")
E_EXPECTED_REMOTE_URL=$(escape_sed_replacement "$EXPECTED_REMOTE_URL")
E_REPO_MARKER=$(escape_sed_replacement "$REPO_MARKER")
E_GIT_COMMON_DIR_HASH=$(escape_sed_replacement "$GIT_COMMON_DIR_HASH")
E_TAG=$(escape_sed_replacement "$TAG")
E_SEVERITY=$(escape_sed_replacement "$SEVERITY")
E_CREATED_ISO=$(escape_sed_replacement "$CREATED_ISO")
E_TASK_ID=$(escape_sed_replacement "$TASK_ID")
E_FEATURE=$(escape_sed_replacement "$FEATURE")
E_RATIONALE=$(escape_sed_replacement "$RATIONALE")

# sed 替换(BSD sed + GNU sed 兼容写法 · 用 `|` 分隔避字符冲突)
# T007 amendment:sed 只替换 frontmatter + 单行字段;{{SECTION1/2/3}} multi-line
# markdown body 由后续 python3 sub 处理(防 sed 不能放 \n)
# {{RATIONALE}} 保留 backward-compat:T004 template 仍可能有这个占位 · 取 RATIONALE_FIRSTLINE
sed \
    -e "s|{{DISCUSSION_ID}}|${E_DISCUSSION_ID}|g" \
    -e "s|{{PRD_FORK_ID}}|${E_PRD_FORK_ID}|g" \
    -e "s|{{HANDBACK_ID}}|${E_HANDBACK_ID}|g" \
    -e "s|{{REPO_ROOT}}|${E_REPO_ROOT}|g" \
    -e "s|{{HANDBACK_TARGET_DIR}}|${E_HANDBACK_TARGET_DIR}|g" \
    -e "s|{{EXPECTED_REMOTE_URL}}|${E_EXPECTED_REMOTE_URL}|g" \
    -e "s|{{REPO_MARKER}}|${E_REPO_MARKER}|g" \
    -e "s|{{GIT_COMMON_DIR_HASH}}|${E_GIT_COMMON_DIR_HASH}|g" \
    -e "s|{{TAG}}|${E_TAG}|g" \
    -e "s|{{SEVERITY}}|${E_SEVERITY}|g" \
    -e "s|{{CREATED_ISO}}|${E_CREATED_ISO}|g" \
    -e "s|{{TASK_ID}}|${E_TASK_ID}|g" \
    -e "s|{{FEATURE}}|${E_FEATURE}|g" \
    -e "s|{{RATIONALE}}|${E_RATIONALE}|g" \
    "$TEMPLATE" > "$OUT"

# T007:python3 sub 替换 {{SECTION1/2/3}}(multi-line markdown body)
# round 2(codex P2-2 修):**单次替换 防套娃** — 原顺序替换 section1 → 2 → 3,
# 若 section1 内容含字面 `{{SECTION2}}`,第二步会再次替换 section1 内已插入的字面 →
# operator 写的 markdown 被篡改。修法:用 re.sub + dict lookup 单次扫描整个 content,
# 每个 `{{SECTIONn}}` placeholder 只匹配 1 次(原模板里的),section 内容里的字面
# `{{SECTION...}}` 不会再被处理。
# round 2(codex P2-4 修):{{TAGS_BLOCK}} 真渲 yaml array · CSV --tag drift,feature
# → `  - drift\n  - feature`(非 1 string · 防 multi-tag false-PASS)
# 入参通过 env var(避命令行 length 限制 + 避 shell quote 复杂度)
SECTION1_VAL="$SECTION1" SECTION2_VAL="$SECTION2" SECTION3_VAL="$SECTION3" TAG_VAL="$TAG" \
python3 -c '
import os, sys, io, re
out_path = sys.argv[1]
with io.open(out_path, "r", encoding="utf-8") as f:
    content = f.read()
# {{TAGS_BLOCK}} 渲成多行 yaml list("  - tag1\n  - tag2"...)
raw_tag = os.environ.get("TAG_VAL", "")
tags = [t.strip() for t in raw_tag.split(",") if t.strip()]
tags_block = "\n".join("  - " + t for t in tags)
# 单次 regex 替换:SECTION1/2/3 + TAGS_BLOCK · section 内容里的字面不被二次处理
section_map = {
    "SECTION1": os.environ.get("SECTION1_VAL", ""),
    "SECTION2": os.environ.get("SECTION2_VAL", ""),
    "SECTION3": os.environ.get("SECTION3_VAL", ""),
    "TAGS_BLOCK": tags_block,
}
def _sub(m):
    key = m.group(1)
    return section_map.get(key, m.group(0))
content = re.sub(r"\{\{(SECTION[123]|TAGS_BLOCK)\}\}", _sub, content)
with io.open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
' "$OUT"

# === F1 修:post-gen 断言 SSOT 三字段不被覆盖 ===
# 重读 $OUT,断言三字段等于 HANDOFF 抽取值(防 user input 注入 YAML 提前出现)
POST_URL=$(extract_yaml_field "$OUT" expected_remote_url '  ')
POST_MARKER=$(extract_yaml_field "$OUT" repo_marker '  ')
POST_HASH=$(extract_yaml_field "$OUT" git_common_dir_hash '  ')

if [[ "$POST_URL" != "$EXPECTED_REMOTE_URL" ]]; then
    echo "ERR: post-gen 断言失败 — expected_remote_url 在 frontmatter 被覆盖" >&2
    echo "  SSOT(HANDOFF): [$EXPECTED_REMOTE_URL]" >&2
    echo "  生成文件:        [$POST_URL]" >&2
    rm -f "$OUT"
    exit 1
fi
if [[ "$POST_MARKER" != "$REPO_MARKER" ]]; then
    echo "ERR: post-gen 断言失败 — repo_marker 在 frontmatter 被覆盖" >&2
    rm -f "$OUT"
    exit 1
fi
if [[ "$POST_HASH" != "$GIT_COMMON_DIR_HASH" ]]; then
    echo "ERR: post-gen 断言失败 — git_common_dir_hash 在 frontmatter 被覆盖" >&2
    rm -f "$OUT"
    exit 1
fi

# T207(C-2)· 真路径输出 OUT 路径到 stdout(verification 真路径 grep 命中 + caller publish 链消费 OUT path)
echo "draft: $OUT"
# T207(R5 P2)· success 路径前 unset RESERVED · 让 cleanup_all 不误清成功生成的 default OUT
RESERVED=""
exit 0
