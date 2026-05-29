#!/usr/bin/env bash
# T001 dangerous-24 runner — 验 .claude/hooks/block-dangerous.sh patterns 0 漏 + drift detect
#
# spec.md §6 O2 verification 量化命令的真落地;round-3 codex F1 强化;FU-002 演进:
#   - 数量校验:hook DANGEROUS_PATTERNS 数(从 hook 真抽,无硬编码)+ fixture 行数 ≥ hook 数
#   - hook→fixture coverage:每个 hook regex 在 fixture 至少 1 行(防 hook 加 pattern 但 fixture 没跟)
#   - fixture→hook validity:fixture 每行 col-1 regex 必须 ∈ hook patterns set(防 fixture 写漂)
#   - 命中校验:fixture col-2 命令跑 hook 后 reason 含 "matched pattern '<col-1>'"(非偶然命中)
#   - 全 deny:fixture 每行 cmd 都 deny
#
# Fixture schema:每行 = "<hook_regex>\t<command>";同 hook regex 可对多行(变体覆盖)
# 文件名 dangerous-24.txt 历史保留(T001 spec file_domain),实际行数随 hook patterns 变
# 不依赖 jq(用 python3,与 hook 自身一致)
#
# Exit codes:
#   0 = 全 deny + 双向覆盖 + 命中正确(Safety Floor PASS)
#   1 = 任一非 deny / mismatch / coverage gap(stderr 列哪条)
#   2 = precondition fail(fixture 缺 / hook 缺 / python3 缺)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
FIXTURE="$SCRIPT_DIR/dangerous-24.txt"
HOOK="$REPO_ROOT/.claude/hooks/block-dangerous.sh"

# 解析 --fixture -(stdin)支持(per round-4 codex F1:negative test 不该写 TMPDIR)
FIXTURE_FROM_STDIN=0
if [[ "${1:-}" == "--fixture" && "${2:-}" == "-" ]]; then
    FIXTURE_FROM_STDIN=1
fi

# precondition checks
[[ -x "$HOOK" ]] || { echo "ERR: hook 缺或不可执行: $HOOK" >&2; exit 2; }
command -v python3 >/dev/null || { echo "ERR: python3 缺(hook + runner 依赖)" >&2; exit 2; }

# 读 fixture
FIXTURE_LINES=()
if [[ "$FIXTURE_FROM_STDIN" -eq 1 ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
        [[ -n "$line" ]] && FIXTURE_LINES+=("$line")
    done
else
    [[ -f "$FIXTURE" ]] || { echo "ERR: fixture 缺: $FIXTURE" >&2; exit 2; }
    while IFS= read -r line || [[ -n "$line" ]]; do
        [[ -n "$line" ]] && FIXTURE_LINES+=("$line")
    done < "$FIXTURE"
fi

FIXTURE_COUNT="${#FIXTURE_LINES[@]}"
[[ "$FIXTURE_COUNT" -gt 0 ]] || { echo "ERR: fixture 空" >&2; exit 2; }

# 抽 hook patterns(顺序保留,与 hook 文件 byte-for-byte)
HOOK_PATTERNS_RAW="$(awk '/^DANGEROUS_PATTERNS=\(/,/^\)/' "$HOOK" | grep -E "^[[:space:]]+'" | sed -E "s/^[[:space:]]+'([^']*)'.*/\1/")"
HOOK_REGEX=()
OLD_IFS="$IFS"
IFS=$'\n'
for line in $HOOK_PATTERNS_RAW; do
    HOOK_REGEX+=("$line")
done
IFS="$OLD_IFS"

HOOK_COUNT="${#HOOK_REGEX[@]}"
[[ "$HOOK_COUNT" -gt 0 ]] || { echo "ERR: hook DANGEROUS_PATTERNS 抽出 0(hook 改了 schema?)" >&2; exit 2; }

# fixture 行数 ≥ hook patterns 数(每 pattern 至少 1 fixture 行)
[[ "$FIXTURE_COUNT" -ge "$HOOK_COUNT" ]] || { echo "ERR: fixture 行数 $FIXTURE_COUNT < hook patterns 数 $HOOK_COUNT" >&2; exit 2; }

# 检验 1:fixture→hook validity — 每 fixture 行 col-1 必须 ∈ hook patterns set
INVALID_FIXTURE=0
for raw_line in "${FIXTURE_LINES[@]}"; do
    fix_regex="${raw_line%%$'\t'*}"
    [[ -z "$fix_regex" ]] && continue
    found=0
    for hp in "${HOOK_REGEX[@]}"; do
        if [[ "$fix_regex" == "$hp" ]]; then
            found=1
            break
        fi
    done
    if [[ "$found" -eq 0 ]]; then
        echo "INVALID FIXTURE: regex '$fix_regex' 不在 hook patterns set" >&2
        INVALID_FIXTURE=$((INVALID_FIXTURE + 1))
    fi
done
[[ "$INVALID_FIXTURE" -eq 0 ]] || { echo "FAIL: $INVALID_FIXTURE fixture lines 不在 hook patterns set" >&2; exit 1; }

# 检验 2:hook→fixture coverage — 每 hook regex 至少有一 fixture 行 col-1 == 它
UNCOVERED=0
for hp in "${HOOK_REGEX[@]}"; do
    covered=0
    for raw_line in "${FIXTURE_LINES[@]}"; do
        fix_regex="${raw_line%%$'\t'*}"
        if [[ "$fix_regex" == "$hp" ]]; then
            covered=1
            break
        fi
    done
    if [[ "$covered" -eq 0 ]]; then
        echo "UNCOVERED hook regex: '$hp' 在 fixture 无对应行" >&2
        UNCOVERED=$((UNCOVERED + 1))
    fi
done
[[ "$UNCOVERED" -eq 0 ]] || { echo "FAIL: $UNCOVERED hook patterns 在 fixture 无 coverage" >&2; exit 1; }

# 主循环:逐行验 fixture cmd 跑 hook 后 deny + 命中正确 regex
MISS_COUNT=0
HIT_MISMATCH=0
LINE_NO=0

for raw_line in "${FIXTURE_LINES[@]}"; do
    LINE_NO=$((LINE_NO + 1))
    fix_regex="${raw_line%%$'\t'*}"
    fix_cmd="${raw_line#*$'\t'}"
    [[ -z "$fix_regex" ]] && continue

    JSON_INPUT=$(python3 -c "import json,sys; print(json.dumps({'tool_input':{'command':sys.argv[1]}}))" "$fix_cmd")

    HOOK_OUT=$(printf '%s' "$JSON_INPUT" | bash "$HOOK") || {
        echo "MISS [line $LINE_NO]: hook 跑挂 / cmd='$fix_cmd'" >&2
        MISS_COUNT=$((MISS_COUNT + 1))
        continue
    }

    PARSED=$(printf '%s' "$HOOK_OUT" | python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    decision = d.get('hookSpecificOutput', {}).get('permissionDecision', 'unknown')
    reason = d.get('hookSpecificOutput', {}).get('permissionDecisionReason', '')
    print(f'{decision}\t{reason}')
except Exception as e:
    print(f'parse-fail\t{e}', file=sys.stderr)
    sys.exit(1)
" 2>&1) || PARSED="parse-fail	$PARSED"

    DECISION="${PARSED%%$'\t'*}"
    REASON="${PARSED#*$'\t'}"

    if [[ "$DECISION" != "deny" ]]; then
        echo "MISS [line $LINE_NO]: cmd='$fix_cmd' → decision='$DECISION'(期 deny)" >&2
        echo "  hook stdout: $HOOK_OUT" >&2
        MISS_COUNT=$((MISS_COUNT + 1))
        continue
    fi

    if [[ "$REASON" != *"matched pattern '$fix_regex'"* ]]; then
        echo "HIT MISMATCH [line $LINE_NO]: cmd='$fix_cmd' deny 了但拦下的 regex 错" >&2
        echo "  expected: matched pattern '$fix_regex'" >&2
        echo "  actual reason: $REASON" >&2
        HIT_MISMATCH=$((HIT_MISMATCH + 1))
    fi
done

TOTAL_FAIL=$((MISS_COUNT + HIT_MISMATCH))
if [[ "$TOTAL_FAIL" -gt 0 ]]; then
    echo "FAIL: miss=$MISS_COUNT hit_mismatch=$HIT_MISMATCH (total $TOTAL_FAIL / $FIXTURE_COUNT)" >&2
    exit 1
fi

echo "0 漏 / $FIXTURE_COUNT cmd / Safety Floor PASS"
echo "0 invalid-fixture / 双向覆盖 fixture↔hook($HOOK_COUNT patterns)"
echo "0 hit-mismatch / 命中的 regex 与 fixture 期望严格一致(非偶然命中)"
