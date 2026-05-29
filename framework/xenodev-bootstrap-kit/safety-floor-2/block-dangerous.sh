#!/bin/bash
# block-dangerous.sh — Claude Code PreToolUse hook, 阻断危险 Bash 命令 (v3.1 §6)
#
# 注册在 .claude/settings.json:
#   "hooks": { "PreToolUse": [{ "matcher": "Bash", "hooks": [{
#     "type": "command",
#     "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-dangerous.sh"
#   }]}]}
#
# 输入: stdin JSON, 形如 {"tool_input": {"command": "..."}}
# 输出: stdout JSON, hookSpecificOutput.permissionDecision = "allow" | "deny"
#
# 这是**最后一道防线**, 不是唯一防线. 通过的命令仍按 .claude/settings.json
# 的 permissions.allow / permissions.deny 走正常审批流程.
#
# Provenance(已分叉,不再字节级 mirror autodev_pipe):
# Original source: /Users/admin/codes/autodev_pipe/.claude/hooks/block-dangerous.sh
# Mirrored: 2026-05-10 (B2.1 Block A) per ideababy_stroller framework/xenodev-bootstrap-kit/
# **Forked: 2026-05-10 (FU-001)** — line 75 周边改用 python3 json.dumps escape pattern,
#   修原 mirror 输出无效 JSON 当 pattern 含 backslash / quote 的 bug
#   (round-1 实测 7/24 patterns 输出 invalid JSON → Claude consumer json.loads 抛
#   `Invalid \escape` → 实际未拦截 → "Safety Floor 0 漏" 量化承诺被击穿)。
#   24 patterns 不变,仅修输出层。
# **Re-fork: 2026-05-11 (FU-002)** — DANGEROUS_PATTERNS 加固:
#   原 24 字面 regex 不覆盖 dash-dash / option 顺序 / 空白变体(T001 round-5 codex F1
#   实证 `rm -rf -- /` 等 bypass)。改用通用形态 `rm[[:space:]]+-[a-zA-Z]*[rRfF]...`
#   合并 rm 类 5→1、git push 类 4→1,数量 24→17。
# **Re-fork: 2026-05-11 (FU-002 round-1)** — 进一步加固:
#   round-1 codex F1/F2 实证仍 bypass(`rm -r -f /` 多 token、
#   `rm --recursive --force /` long option、`git push --force-with-lease origin main`、
#   `git push origin +main` refspec)。改用 token-agnostic 形态:
#   - rm 类:rm + 任意中间 + 高 risk target(不依赖 option 解析)
#   - git push 类:加 --force-with-lease + refspec (HEAD:main / +main / refs/heads/main)
# **Known limit (FU-002 round-2 codex 实证)**:
#   regex 字符串匹配是 best-effort,不能完全推 shell 语义。已知未拦的 bypass 类:
#   - rm 的 quote/expand 形式:rm -rf "$HOME" / rm -rf ${HOME} / rm -rf ~/ / rm -rf ~/*
#   - git push --force-with-lease=<ref> origin main(force option 带 ref,等号形式)
#   - git push origin +HEAD:main / +refs/heads/main(refspec 复合 + 前缀)
#   FU-003 跟进:hook 重设计为 shlex token-based detection(spec FU-003)。
# 后续政策:本 hook 是 XenoDev fork;upstream 升级 patterns 时 operator 手动 merge 进 fork。

set -euo pipefail

# 从 stdin 读 Claude Code 传入的 hook payload
INPUT="$(cat)"

# 提取要执行的命令. 用 python 而不是 jq 避免依赖.
COMMAND="$(printf '%s' "$INPUT" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get("tool_input", {}).get("command", ""))
except Exception:
    print("")
')"

# 危险模式正则 (grep -E 语法)
# 增减规则时请保留注释, 说明该规则的现实威胁场景.
DANGEROUS_PATTERNS=(
    # rm 类删除高 risk targets(FU-002 round-1 加固:token-agnostic,不解析 option)
    # 形态:rm + (任意中间 token + 空白) + (可选 --) + (空白) + (高 risk target) + word boundary
    # target 集:/ ~ .. $HOME *
    # 关键:用 .* 允许多 short token / long option / dash-dash;末尾 word boundary 防 ./build 误伤
    'rm[[:space:]]+(.*[[:space:]])?(--[[:space:]]+)?(/|~|\.\.|\$HOME|\*)([[:space:]]|$)'
    # git push --force/-f/--force-with-lease 主分支(FU-002 round-1:加 refspec + --force-with-lease)
    # 形态:git push + (任意中间) + force 标志 + (任意中间) + (main|master + 各种 ref 形式)
    'git[[:space:]]+push[[:space:]]+([^|;]*[[:space:]])?(--force(-with-lease)?|-[a-zA-Z]*f[a-zA-Z]*)([[:space:]]+[^|;]*)?[[:space:]]+(origin[[:space:]]+)?(\+?main|\+?master|HEAD:main|HEAD:master|refs/heads/main|refs/heads/master|[^[:space:]]+:main|[^[:space:]]+:master)([[:space:]]|$)'
    # git push +main / +master refspec(无 --force 但用 + 前缀也是 force)
    'git[[:space:]]+push[[:space:]]+([^|;]*[[:space:]])?(origin[[:space:]]+)?\+(main|master)([[:space:]]|$)'
    'git[[:space:]]+reset[[:space:]]+--hard[[:space:]]+.*origin'  # 丢弃本地未推送提交
    'git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f[a-zA-Z]*d'        # 强制清理含未追踪
    'DROP[[:space:]]+DATABASE'                                      # SQL 删库
    'DROP[[:space:]]+TABLE'
    'TRUNCATE[[:space:]]+TABLE'
    'aws[[:space:]]+s3[[:space:]]+rm.*--recursive.*production'      # 删 S3 production 桶
    'aws[[:space:]]+s3[[:space:]]+rb.*--force'                      # 删整个桶
    'kubectl[[:space:]]+delete[[:space:]]+namespace'                # 删 K8s 命名空间
    'terraform[[:space:]]+destroy'                                  # IaC 删基础设施
    ':\(\)\{[[:space:]]*:\|:&[[:space:]]*\};:'                     # fork bomb
    'dd[[:space:]]+if=.*of=/dev/'                                   # 写裸设备
    'mkfs\.'                                                        # 格式化
    'curl.*\|[[:space:]]*bash'                                      # 远程脚本直接执行
    'wget.*\|[[:space:]]*sh'
    'chmod[[:space:]]+-[a-zA-Z]*R[a-zA-Z]*[[:space:]]+777[[:space:]]+/'  # 把根目录权限放开(支持 -Rf 等组合)
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if printf '%s' "$COMMAND" | grep -qE "$pattern"; then
        # 输出 deny JSON (Claude Code Hooks API)
        # 关键:整个 JSON 用 python3 json.dumps 一次性生成,
        #   - escape pattern(防 backslash/quote 破 JSON;原 line 75 bug,FU-001 fix)
        #   - 不依赖 here-doc(防 read-only TMPDIR 环境挂在 temp file 创建,FU-001 round-2 fix)
        python3 -c '
import json, sys
p = sys.argv[1]
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Blocked by safety hook: matched pattern '"'"'{p}'"'"'. If this is intentional, run manually outside Claude Code."
    }
}))
' "$pattern"
        exit 0
    fi
done

# 通过 - 让正常 permission 流程接管(不用 here-doc,见上注)
printf '{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}\n'
