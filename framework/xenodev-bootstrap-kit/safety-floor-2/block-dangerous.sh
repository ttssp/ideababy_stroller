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
# Mirror provenance:
# Source: /Users/admin/codes/autodev_pipe/.claude/hooks/block-dangerous.sh
# Mirrored: 2026-05-10 (B2.1 Block A) per ideababy_stroller framework/xenodev-bootstrap-kit/
# Reason: per stage-forge-006-v2.md M5 step 2 "cp block-dangerous.sh from V4 (纯工业共识,无定制)"
# 改动:本 mirror 与源完全一致(byte-for-byte);未来若需 XenoDev 定制 dangerous patterns,
# 在 XenoDev 仓内 fork 后修改,不要改本 mirror(本 mirror 始终保持与 autodev_pipe 同步)。

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
    'rm -rf /'                          # 删根
    'rm -rf \*'                         # 删当前目录所有内容
    'rm -rf ~'                          # 删 home
    'rm -rf \.\.'                       # 跳出删父目录
    'rm -rf \$HOME'                     # 删 home 变量形式
    'git push --force.*main'            # force push 主分支
    'git push --force.*master'
    'git push -f.*main'
    'git push -f.*master'
    'git reset --hard.*origin'          # 丢弃本地未推送的提交
    'git clean -[a-zA-Z]*f[a-zA-Z]*d'   # 强制清理含未追踪
    'DROP DATABASE'                     # SQL 删库
    'DROP TABLE'
    'TRUNCATE TABLE'
    'aws s3 rm.*--recursive.*production' # 删 S3 production 桶
    'aws s3 rb.*--force'                 # 删整个桶
    'kubectl delete namespace'           # 删 K8s 命名空间
    'terraform destroy'                  # IaC 删基础设施
    ':\(\)\{ :\|:& \};:'                # fork bomb
    'dd if=.*of=/dev/'                   # 写裸设备
    'mkfs\.'                             # 格式化
    'curl.*\| *bash'                     # 远程脚本直接执行
    'wget.*\| *sh'
    'chmod -R 777 /'                     # 把根目录权限放开
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if printf '%s' "$COMMAND" | grep -qE "$pattern"; then
        # 输出 deny JSON (Claude Code Hooks API)
        cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Blocked by safety hook: matched pattern '$pattern'. If this is intentional, run manually outside Claude Code."
  }
}
EOF
        exit 0
    fi
done

# 通过 - 让正常 permission 流程接管
cat <<'EOF'
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
EOF
