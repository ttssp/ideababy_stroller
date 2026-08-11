#!/usr/bin/env bash
# check-7-topology-selfattest.sh — §6.3.1 拓扑自证三字段(current_idea / worktree / baseline)
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.3.1(forge 006 v8 簇② 落 IDS 权威侧)
#
# Usage: check-7-topology-selfattest.sh <handback_file> <fm_prd_fork_id> <fm_working_repo>
#
# 校验(全部 warn 型 · 不阻断):
#   1. 三字段是否存在(老包无此三字段 = 正常 · 只提示)
#   2. worktree == workspace.working_repo(不等 = 自证字段本身失真)
#   3. current_idea == prd_fork_id(不等 = 混线嫌疑)
#   4. baseline 形状 ^[0-9a-f]{7,40}$
#
# **本 check 永远 exit 0** —— warn 型起步,理由见 §6.3.1「校验强度」段:
#   (a) 与 CLAUDE.md「Session-per-idea worktree 规约」P0 warn 型同构;
#   (b) 三字段 2026-08-10 才补进 schema,存量 40+ 包全无,硬 reject 会把既有语料判 corruption。
# === warn 分型(forge 006 v10 · 2026-08-11)===
#   warn_class: **temporary**
#   registry:   framework/warn-registry/registry.jsonl → `WARN-check7-topology-selfattest`
#   owner:      IDS handback-validator owner
#   due_event:  forge:006:phase0(已接线 · 见 .claude/commands/expert-forge.md Step 0.7)
#
# 🔴 **原判据「worktree mismatch 复发 ≥2 次即升 hard-fail」已被 v10 作废** ——
# 「复发 ≥N 次」不是升级机制:无计数者、无消费点、无执行者。实证:CLAUDE.md 的同形判据
# 在第 2 次就达成,达成后仍复发到第 4 次。
#
# 取而代之:到 due_event 时**必须三态裁决**(承 RFC 1589)——
#   convert(升 §6.2.1 第 7 约束)/ revert(移除机制)/ defer(具名签署 + 理由 + 新 due_event)
#   或改判 soft advisory(须补 no_upgrade_plan + rationale)。
# **被遗忘的 defer 不是 defer,是缺席。**
#
# ⚠ 裁决时须一并处理存量 40+ 无三字段老包的追溯性执法边界,
#   按 v10「存量与新增分域」条款(forward 硬拦 / 历史只读不追溯)处理。

set -euo pipefail

HANDBACK_FILE="${1:-}"
FM_PRD_FORK_ID="${2:-}"
FM_WORKING_REPO="${3:-}"

if [[ -z "$HANDBACK_FILE" ]]; then
    echo "Usage: check-7-topology-selfattest.sh <handback_file> <fm_prd_fork_id> <fm_working_repo>" >&2
    exit 2
fi

if [[ ! -f "$HANDBACK_FILE" ]]; then
    echo "ERROR: handback file not found: $HANDBACK_FILE" >&2
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_yaml-helpers.sh"

CURRENT_IDEA="$(extract_yaml_field "$HANDBACK_FILE" current_idea '')"
WORKTREE="$(extract_yaml_field "$HANDBACK_FILE" worktree '')"
BASELINE="$(extract_yaml_field "$HANDBACK_FILE" baseline '')"

WARNINGS=()

# === 1. 三字段存在性(老包无 = 正常)===
MISSING=()
[[ -z "$CURRENT_IDEA" ]] && MISSING+=("current_idea")
[[ -z "$WORKTREE" ]]     && MISSING+=("worktree")
[[ -z "$BASELINE" ]]     && MISSING+=("baseline")

if [[ ${#MISSING[@]} -eq 3 ]]; then
    echo "  ⏭  check-7 skipped:§6.3.1 拓扑自证三字段全缺(2026-08-10 前的老包属正常)" >&2
    exit 0
fi

if [[ ${#MISSING[@]} -gt 0 ]]; then
    WARNINGS+=("§6.3.1 三字段部分缺失:${MISSING[*]}(部分填写比全不填更可疑 —— producer 可能只 backfill 了好填的那几个)")
fi

# === 2. worktree == workspace.working_repo(自证字段核心判据)===
if [[ -n "$WORKTREE" && -n "$FM_WORKING_REPO" ]]; then
    if [[ "$WORKTREE" != "$FM_WORKING_REPO" ]]; then
        WARNINGS+=("worktree 字段与 workspace.working_repo 不一致 —— 拓扑自证失真:
       worktree            = $WORKTREE
       workspace.working_repo = $FM_WORKING_REPO
     该字段的唯一意义是自证「本产物出自哪根分支拓扑」;填成 idea 主 worktree 的常量,
     会恰好在分支真的分叉了的场景(per-task 专用 worktree)失真。见 §6.3.1。")
    fi
fi

# === 3. current_idea == prd_fork_id(混线嫌疑)===
if [[ -n "$CURRENT_IDEA" && -n "$FM_PRD_FORK_ID" ]]; then
    if [[ "$CURRENT_IDEA" != "$FM_PRD_FORK_ID" ]]; then
        WARNINGS+=("current_idea ($CURRENT_IDEA) != prd_fork_id ($FM_PRD_FORK_ID) —— 混线嫌疑(session working on 的 idea 与本包归属 fork 不同)")
    fi
fi

# === 4. baseline 形状 ===
if [[ -n "$BASELINE" ]]; then
    if [[ ! "$BASELINE" =~ ^[0-9a-f]{7,40}$ ]]; then
        WARNINGS+=("baseline ($BASELINE) 不是 git sha 形状(期望 ^[0-9a-f]{7,40}\$)")
    fi
fi

# === 输出 ===
if [[ ${#WARNINGS[@]} -eq 0 ]]; then
    echo "  ✓ check-7 (§6.3.1 拓扑自证三字段) PASS" >&2
    exit 0
fi

echo "  ⚠ check-7 (§6.3.1 拓扑自证三字段) WARN ×${#WARNINGS[@]} —— warn 型,不阻断:" >&2
for w in "${WARNINGS[@]}"; do
    echo "     · $w" >&2
done
echo "     升级 hard-fail 判据见 SHARED-CONTRACT §6.3.1「校验强度」段。" >&2
exit 0
