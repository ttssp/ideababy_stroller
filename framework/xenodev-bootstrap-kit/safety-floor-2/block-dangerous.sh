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
#
# B2.2 Block A.6 codex round 3 finding #1 fix(2026-05-10):
# 反向 fork — autodev_pipe 上游 patterns 自身存在 bypass(参数顺序 + 大小写),
# 不是定制需求,而是 mirror 源对 declared Safety Floor 的实现 bug。修在 IDS
# 这一份 mirror,operator 后续可决定是否同步回 autodev_pipe 上游(详见
# discussion/006/b2-2/CODEX-REVIEW-ROUND3.md Park 决策重论证)。
# 修改点:
#   1. force-push 改 case-insensitive + 接受任意参数顺序(--force 在 main 前后都拦)
#   2. force-push 加 release-* / production 受保护分支
#   3. SQL DROP/TRUNCATE 改 case-insensitive
#   4. aws rds delete-db-* / GCP-Azure 删除 资源 等价命令(仅加最小必要,非完备)
#   5. 加 normalize 步骤:case-fold + 折叠多空格,匹配前统一

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

# Normalize:case-fold + 折叠空白,统一匹配输入(防大小写 / 多空格 bypass)
NORMALIZED="$(printf '%s' "$COMMAND" | tr '[:upper:]' '[:lower:]' | tr -s '[:space:]' ' ')"

# === 危险模式 ===
# 注:
# - 模式按 NORMALIZED(小写 + 折叠空白)匹配;字面匹配处保留 -E 用 ERE
# - force-push 用语义匹配(出现 git push + --force/-f + 受保护分支),不依赖参数顺序
# - SQL 用 -i 等效(已对 NORMALIZED 跑,DROP TABLE → drop table 仍 hit)

DANGEROUS_PATTERNS=(
    'rm -rf /( |$)'                     # 删根($ 或空格;不含 /tmp/...)
    'rm -rf \*'                         # 删当前目录所有内容
    'rm -rf ~( |$)'                     # 删 home
    'rm -rf \.\.( |$)'                  # 跳出删父目录
    'rm -rf \$home'                     # 删 home 变量形式(NORMALIZED 已小写)
    'git reset --hard.*origin'          # 丢弃本地未推送的提交
    'git clean -[a-z]*f[a-z]*d'         # 强制清理含未追踪
    'drop database( |;|$)'              # SQL 删库(词边界,防 mydatabase)
    'drop table( |;|$)'                 # SQL 删表(词边界,防 tableware)
    'truncate table( |;|$)'             # SQL 清表
    'aws s3 rm.*--recursive.*production' # 删 S3 production 桶
    'aws s3 rb.*--force'                 # 删整个桶
    'aws rds delete-db-instance'         # AWS RDS 删 DB 实例
    'aws rds delete-db-cluster'          # AWS RDS 删 DB 集群
    'aws rds delete-db-snapshot'         # AWS RDS 删 snapshot
    'gcloud sql instances delete'        # GCP Cloud SQL 删实例
    'gcloud compute disks delete'        # GCP 删盘
    'az sql db delete'                   # Azure SQL 删 DB
    'az storage account delete'          # Azure 删 storage 账号
    'kubectl delete namespace'           # 删 K8s 命名空间
    'terraform destroy'                  # IaC 删基础设施
    ':\(\)\{ :\|:& \};:'                # fork bomb
    'dd if=.*of=/dev/'                   # 写裸设备
    'mkfs\.'                             # 格式化
    'curl.*\| *bash'                     # 远程脚本直接执行
    'wget.*\| *sh'
    'chmod -r 777 /( |$)'               # 把根目录权限放开(词边界)
)

# === 字面 / 语义复合匹配:force-push 受保护分支(参数顺序无关)===
# 受保护分支:main / master / production / release-*
# bash regex 不支持 \b 词边界,用 [^a-z0-9_-] 或字符串首尾代替
#
# B2.2 Block A.7 codex round 4 finding #2 fix:
# Round 3 fix 只覆盖 --force / -f,漏 --force-with-lease / --force-if-includes / +ref:ref refspec。
# attack model(系统化列举 git "覆盖远程" 全部语法,不只 codex 给的 specific case):
#   1. --force (+ -f 短形)
#   2. --force-with-lease[=...] / --force-if-includes
#   3. +<branch>:<branch> refspec(简写 +<branch> 也算)
# 任一形式 + 受保护分支 → DENY。
has_force_indicator() {
    local cmd="$1"
    # 1. --force / -f 独立 token
    [[ "$cmd" =~ (^|[[:space:]])(--force|-f)([[:space:]]|=|$) ]] && return 0
    # 2. --force-with-lease / --force-if-includes(可带 = 后缀)
    [[ "$cmd" =~ (^|[[:space:]])--force-with-lease([[:space:]]|=|$) ]] && return 0
    [[ "$cmd" =~ (^|[[:space:]])--force-if-includes([[:space:]]|=|$) ]] && return 0
    # 3. +<branch>:<branch> 或 +<branch> refspec(覆盖远程)
    if printf '%s' "$cmd" | grep -qE '(^|[[:space:]])\+(main|master|production|release-[a-z0-9._-]+)(:|[[:space:]]|$)'; then
        return 0
    fi
    return 1
}

is_force_push_protected() {
    local cmd="$1"
    # 必须是 git push
    [[ "$cmd" =~ git[[:space:]]+push ]] || return 1
    # 必须含某种 force 指示符
    has_force_indicator "$cmd" || return 1
    # 必须含受保护分支名(若 force 走 +refspec 路径,refspec 已含分支,直接 DENY)
    if printf '%s' "$cmd" | grep -qE '(^|[[:space:]])\+(main|master|production|release-[a-z0-9._-]+)(:|[[:space:]]|$)'; then
        return 0
    fi
    if printf '%s' "$cmd" | grep -qE '(^|[^a-z0-9_-])(main|master|production)([^a-z0-9_-]|$)'; then
        return 0
    fi
    if printf '%s' "$cmd" | grep -qE '(^|[^a-z0-9_-])release-[a-z0-9._-]+'; then
        return 0
    fi
    return 1
}

if is_force_push_protected "$NORMALIZED"; then
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Blocked by safety hook: force-push to protected branch (main/master/production/release-*). If this is intentional, run manually outside Claude Code."
  }
}
EOF
    exit 0
fi

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if printf '%s' "$NORMALIZED" | grep -qE "$pattern"; then
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
