#!/usr/bin/env bash
# check-no-hardcoded-env.sh — 防再漂移守卫(forge v6 · KG-26/27 verdict)
#
# 结论:拦"把某台机器的环境形态(用户绝对家目录 / codex 散写版本号)当默认值/可执行路径写死"的硬编码。
# 命中 = 非零退出(可作 pre-commit hook / 手动 gate)。轻量,不上重 CI(K binding④ 双机非发行)。
#
# 自身可移植:用 git rev-parse 定位仓根,不重蹈硬编码(否则守卫自己就是下一个 KG-26)。
# allowlist:注释里的历史记录 / 本守卫自身 / 明确标注的示例,不算硬编码(见 ALLOWLIST_RE)。

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT" || exit 2

# 待拦模式:
#   1. 任何用户绝对家目录当路径用:/Users/<name>/ 或 /home/<name>/(mac + linux 都拦 —— 本机 /home/ys 也不该写死进框架)
#   2. codex 散写版本号:codex/<x.y.z>/(应走 glob *+sort -V,不钉死具体版本)
HARDCODE_RE='(/Users/[a-zA-Z0-9_.-]+/|/home/[a-zA-Z0-9_.-]+/|codex/[0-9]+\.[0-9]+\.[0-9]+/)'

# allowlist(这些命中不算违规 —— 它们是"明确标注的示例/警告/历史",不是"当默认值/可执行路径写死"):
#   - 警告类:"绝不硬编码" / "不硬编码" / "mac 路径"
#   - 示例类:"示例" / "如 /"(illustrative,后面必跟"按本机实际填"语境)/ "如本机" / "e.g." / "<...-repo-root>" 占位符
#   - operator 自填类:"operator 自填" / "默认 <...>"(占位符包裹的默认)
#   - 历史注释类:"旧 v" / "原为" / "已淘汰" / "provenance"
#   - 本守卫脚本自身
ALLOWLIST_RE='(绝不硬编码|不硬编码|mac 路径|示例|如 /|如本机|e\.g\.|repo-root>|operator 自填|旧 v[0-9]|原为|已淘汰|provenance|per FU|check-no-hardcoded-env)'

# 扫描范围(forge v6 P0 · 分阶段收窄):
#   本守卫**当前只 gate P0 已根治的可执行治理文件** —— 即"值真流进产物 / 被当默认值执行"的运行时路径。
#   ⚠ 全框架 mac 硬编码面远大于此(~45 文件:test-fixtures 用 mac 路径当测试数据 / MANIFEST·AUDIT 历史文档 /
#     bootstrap-kit skills/ 的 XenoDev SKILL 拷贝 / integration test 的 IDS_ROOT)。那批是**分批清扫的后续**
#     (v0.2 note · 逐类判断:fixture 改了会不会破测试 / 历史文档要不要动),不在本 P0 gate 射程,防误伤。
#   扩大 gate 面 = 后续单独 PR + 逐文件核。
SCAN_PATHS=(
    .claude/commands/plan-start.md
    .claude/commands/handback-review.md
    framework/SHARED-CONTRACT.md
    framework/xenodev-bootstrap-kit/handback-validator/gen-handback.sh
    framework/xenodev-bootstrap-kit/handback-validator/templates/handback.template.md
)
# 只扫存在的文件(有的可能后续才纳入)
EXISTING=()
for p in "${SCAN_PATHS[@]}"; do [[ -e "$p" ]] && EXISTING+=("$p"); done

MATCHES=$(grep -rnE "$HARDCODE_RE" "${EXISTING[@]}" 2>/dev/null \
    | grep -vE "$ALLOWLIST_RE" \
    || true)

if [[ -n "$MATCHES" ]]; then
    echo "❌ check-no-hardcoded-env: 发现硬编码机器环境形态(用户家目录绝对路径 / 散写 codex 版本号):" >&2
    echo "$MATCHES" >&2
    echo "" >&2
    echo "修法(forge v6 KG-26/27):路径用 git rev-parse/realpath 或 \$XENODEV_REPO 推断;" >&2
    echo "  codex 版本用 glob 'codex/*/scripts' + sort -V resolver。若是有意示例/历史注释 → 加进 ALLOWLIST_RE。" >&2
    exit 1
fi

echo "✅ check-no-hardcoded-env: 无当默认值/可执行路径用的硬编码机器环境形态(扫 .claude/ + framework/)"
exit 0
