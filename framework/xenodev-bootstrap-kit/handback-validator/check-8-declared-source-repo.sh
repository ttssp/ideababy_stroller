#!/usr/bin/env bash
# check-8-declared-source-repo.sh — §6.2.1 约束 1 的**声明侧**投影
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 约束 1
#
# Usage: check-8-declared-source-repo.sh <fm_source_repo> <fm_handback_target> <discussion_id> <runtime_source_repo>
#
# 为什么需要本 check(HANDBACK-LOG 第 45 条 · consumer 侧实证):
#   §6.2.1 约束 1 的公式是 handback_target ⊂ source_repo + "/discussion/<id>/handback/"。
#   check-1 把这条公式作用在**运行时传入的** source_repo 上(= consumer 的 `realpath .`),
#   那个值永远自洽,于是公式实际上从未校验过**包里声明的** workspace.source_repo。
#   validate-handback.sh:76 抽出的 SOURCE_REPO_FM 曾是一个**从未被使用的死变量**。
#   实证:hand-back 001-radar-pA-20260811T024101Z 声明 source_repo=/Users/admin/...(mac 旧路径,
#   Ubuntu 上不存在)而 handback_target=/home/ys/...,两者按约束 1 自身的公式互相矛盾,
#   却 7 个 check 全 PASS。⇒ 自证字段存在但不被验 = 自证等于零(与 XD-47 / KG-B16 同族)。
#
# 校验(全部 warn 型 · 不阻断):
#   1. workspace.source_repo 是否存在(缺 = warn;老包可能没这字段)
#   2. **声明内部自洽**:handback_target 落在 source_repo + "/discussion/<id>/handback" 之下
#      —— 即把约束 1 的公式作用在声明值上(纯词法比较,不碰文件系统:
#         声明的 source_repo 是**产源主机**的路径,在 consumer 主机上做 realpath 无意义)
#   3. 声明的 source_repo 与运行时 source_repo 一致(不等 = 包自述的写回目标仓 ≠ 实际消费仓)
#
# **本 check 永远 exit 0** —— warn 型起步,与 check-7 同构,理由:
#   (a) 存量语料里 20/41 个 001 包带 mac 旧路径,硬 reject 会把既有语料整体判 corruption;
#   (b) 该字段此前从未被校验过,producer 侧无任何机会被提示,直接硬拦属追溯性执法。
# 升级为 hard-fail 的判据:本 warn 上线后声明不自洽仍复发 ≥2 次,
# 或出现一次因 source_repo 声明失真导致的跨仓误写/误决议。

set -euo pipefail

FM_SOURCE_REPO="${1:-}"
FM_HANDBACK_TARGET="${2:-}"
DISCUSSION_ID="${3:-}"
RUNTIME_SOURCE_REPO="${4:-}"

if [[ -z "$DISCUSSION_ID" ]]; then
    echo "Usage: check-8-declared-source-repo.sh <fm_source_repo> <fm_handback_target> <discussion_id> <runtime_source_repo>" >&2
    exit 2
fi

# 纯词法归一:去尾部 `/`、折叠重复 `/`。**不碰文件系统** —— 声明值是产源主机路径。
# 不做 `..` 折叠:含 `..` 的声明本身就该被 warn 出来,而不是被悄悄normalize 掉。
lexical_norm() {
    local p="$1"
    p="$(printf '%s' "$p" | sed -e 's|//*|/|g' -e 's|/*$||')"
    printf '%s' "$p"
}

WARNINGS=()

# === 1. 声明存在性 ===
if [[ -z "$FM_SOURCE_REPO" ]]; then
    echo "  ⏭  check-8 skipped:frontmatter 无 workspace.source_repo 字段" >&2
    exit 0
fi

SRC_NORM="$(lexical_norm "$FM_SOURCE_REPO")"
TGT_NORM="$(lexical_norm "$FM_HANDBACK_TARGET")"

# `..` / 非绝对路径 = 声明形状本身可疑
if [[ "$SRC_NORM" != /* ]]; then
    WARNINGS+=("workspace.source_repo 不是绝对路径:[$FM_SOURCE_REPO]")
fi
if [[ "$SRC_NORM" == *".."* ]]; then
    WARNINGS+=("workspace.source_repo 含 '..' 段:[$FM_SOURCE_REPO](声明侧不做 normalize,原样报出)")
fi

# === 2. 声明内部自洽(约束 1 公式作用在声明值上)===
if [[ -n "$TGT_NORM" ]]; then
    EXPECTED_PREFIX="${SRC_NORM}/discussion/${DISCUSSION_ID}/handback"
    if [[ "$TGT_NORM" != "$EXPECTED_PREFIX" && "$TGT_NORM" != "$EXPECTED_PREFIX/"* ]]; then
        WARNINGS+=("声明内部不自洽 —— workspace.handback_target 不在 workspace.source_repo 之下:
       workspace.source_repo     = $FM_SOURCE_REPO
       workspace.handback_target = $FM_HANDBACK_TARGET
       约束 1 公式要求的前缀        = $EXPECTED_PREFIX
     这两个字段按 §6.2.1 约束 1 自身的公式是结构耦合的;不自洽 = 包的自证拓扑失真。")
    fi
fi

# === 3. 声明 vs 运行时 ===
if [[ -n "$RUNTIME_SOURCE_REPO" ]]; then
    RUNTIME_NORM="$(lexical_norm "$RUNTIME_SOURCE_REPO")"
    if [[ "$SRC_NORM" != "$RUNTIME_NORM" ]]; then
        WARNINGS+=("声明的 source_repo 与运行时消费仓不同:
       declared (包内) = $FM_SOURCE_REPO
       runtime  (本机) = $RUNTIME_SOURCE_REPO
     常见真因:producer 侧从陈旧的指令文档/模板里抄了 IDS 仓路径,而非从运行时解析
     (gen-handback.sh 的 --source-repo / \$IDS_REPO / sibling 优先级链)。")
    fi
fi

if [[ ${#WARNINGS[@]} -eq 0 ]]; then
    echo "  ✓ check-8 (§6.2.1 约束 1 声明侧投影) PASS" >&2
    exit 0
fi

echo "  ⚠ check-8 (§6.2.1 约束 1 声明侧投影) WARN — 不阻断,但请修 producer 侧:" >&2
for w in "${WARNINGS[@]}"; do
    echo "    · $w" >&2
done
exit 0
