#!/usr/bin/env bash
# validate-verdict-evidence.sh — verdict-evidence **syntax-only precheck**(可执行入口)
#
# ⚠️⚠️ 这**不是** full consumer validator · 是 shallow 语法预检 ⚠️⚠️
#   只校验 ids_verdict_evidence 7 字段齐全 + verdict enum + findings_count 整数。
#   **不验** review_log_path 可达 / review_log_sha256 binding / target_file·ts·codex_model
#   与 REVIEW-LOG 一致(那些是 producer-side full 校验 · 在 scripts/verify-ppv-p2.sh)。
#   → 本工具**接受语法合法但未经证伪的 evidence metadata**(伪造/stale 的 path/sha 也过)。
#   per codex adversarial-review F2(job review-mptsfdjm-ztrfbm):勿把本工具当 THE consumer
#   validator 用 · 它只挡"字段缺/enum 错/findings 非整数"这类语法错。完整 consumer-side
#   binding 验证是 post-P0 backlog(见 .work/IDS-handoff-006-forge-v4-P0.md §4.5)。
# Provenance:idea 006 forge v4 · P0 原子波 · source 共享 verdict-evidence-lib.sh。
#
# ⚠️ 为什么不做 full(高危约束 · forge v4 一手验证):
#   真 hand-back 的 review_log_path 是 XenoDev repo-relative(eg
#   .claude/skills/codex-review/REVIEW-LOG.md)· IDS consumer 本地无此文件 ·
#   若照搬 producer 的 rehash / path-fail-closed → 100% 误拒合法包。
#   故本预检只 verify_evidence_required(path 不可达不 fail-closed)。
#
# Usage:
#   validate-verdict-evidence.sh <handback_file> [--mode=consumer]
#
# Mode:
#   --mode=consumer(默认):shallow syntax-precheck · 只 required(7 字段齐 + enum + int)
#   --mode=producer:**拒**(exit 2 · per codex round-3 F2)· 本 wrapper 不做 producer full
#     校验 · 别拿它冒充 producer validator;producer full 链在 scripts/verify-ppv-p2.sh。
#
# 退码:0 = syntax-precheck PASS · 1 = FAIL(stderr 报因) · 2 = usage / 文件不存在 / --mode=producer

set -euo pipefail

HANDBACK_FILE=""
MODE="consumer"

# === Parse args(支持位置 + --mode=XXX flag · 抄 validate-handback.sh:29-49)===
for arg in "$@"; do
    case "$arg" in
        --help|-h)
            # 仿同目录 gen-handback.sh / score-handback.sh · print 头部 usage 注释块(line 2-28)
            sed -n '2,28p' "$0"
            exit 0
            ;;
        --mode=consumer) MODE="consumer" ;;
        --mode=producer)
            # per codex adversarial-review(round 3 F2):拒 --mode=producer · 消除假动作。
            # 本 wrapper 是 consumer-side syntax-precheck · 不做 producer full 校验(path/sha/
            # field consistency)。producer full 链在 scripts/verify-ppv-p2.sh · 别拿本工具冒充。
            echo "ERROR: --mode=producer 本 wrapper 不支持 · 本工具是 consumer-side syntax-precheck(只验字段齐+enum+int)·" >&2
            echo "  producer full 校验(rehash/consistency/freshness)在 scripts/verify-ppv-p2.sh · 用那个" >&2
            exit 2
            ;;
        --mode=*)
            echo "ERROR: unknown mode: $arg (expected --mode=consumer)" >&2
            exit 2
            ;;
        *)
            if [[ -z "$HANDBACK_FILE" ]]; then
                HANDBACK_FILE="$arg"
            else
                echo "ERROR: too many positional args (got: $arg)" >&2
                exit 2
            fi
            ;;
    esac
done

if [[ -z "$HANDBACK_FILE" ]]; then
    echo "Usage: validate-verdict-evidence.sh <handback_file> [--mode=consumer]" >&2
    exit 2
fi

if [[ ! -f "$HANDBACK_FILE" ]]; then
    echo "ERROR: handback file not found: $HANDBACK_FILE" >&2
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# === 共享 verdict-evidence 解析 + verify lib(与 verify-ppv-p2.sh 同一件)===
source "$SCRIPT_DIR/verdict-evidence-lib.sh"

echo "→ verdict-evidence syntax-precheck on $HANDBACK_FILE (mode: $MODE · shallow=required-only · 非 full consumer 验证) ..." >&2

# consumer shallow:只 required(verdict/findings 无条件 + 5 字段 gate 在父键存在时)
# · path 不可达不 fail-closed(不调 rehash/consistency/freshness)
if verify_evidence_required "$HANDBACK_FILE" "$MODE"; then
    echo "✓ verdict-evidence syntax-precheck PASS ($HANDBACK_FILE · mode=$MODE · 仅语法 · 未验 binding)" >&2
    exit 0
else
    echo "→ verdict-evidence FAIL ($HANDBACK_FILE)" >&2
    exit 1
fi
