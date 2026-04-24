#!/usr/bin/env bash
# pre_tool_use.sh · T014 加固版 · R6 · SLA §1.4 · architecture §6
#
# 职责：拦截 Claude Code 工具调用，执行 deny 清单（第三道防线）
#       第一道：fail-closed .claude/ 只读 mount（T012 · bindfs/chflags）
#       第二道：settings.json permissions.deny 规则（Claude Code 原生）
#       第三道（本文件）：bash 正则 deny，覆盖 architecture §6 完整清单
#
# Hook 协议（Claude Code 2026-04-latest）：
#   stdin: JSON {"tool":{"name":"<ToolName>"},"input":{"command":"<bash cmd>",...}}
#   exit 0  → 允许（allow）
#   exit 2  → deny（Claude Code 向 worker 报 PermissionError）
#
# 开发规则：
#   - 每条 deny 规则带来源注释（architecture §6 / SLA §1.4）
#   - deny 时 echo "[pre_tool_use] DENY: <reason>: $COMMAND" >&2
#   - 最后 exit 0（allow，未命中任何 deny 规则）
#   - bash -n 语法检查必须通过
#
# 关联：T012（stub）→ T014（加固）→ T023（下游依赖）

set -euo pipefail

# ---------------------------------------------------------------------------
# 读取 stdin JSON（Claude Code hook 协议）
# ---------------------------------------------------------------------------
INPUT="$(cat)"

# 提取工具名（支持 tool.name 嵌套格式）
TOOL_NAME=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('tool', {}).get('name', data.get('tool_name', 'unknown')))
except Exception:
    print('unknown')
" 2>/dev/null || echo "unknown")

# 提取 Bash 命令（兼容 tool/input 嵌套和扁平结构）
COMMAND=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    cmd = (data.get('input') or {}).get('command', data.get('command', ''))
    print(cmd)
except Exception:
    print('')
" 2>/dev/null || echo "")

# 提取文件路径（Edit / Write 工具使用）
FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    path = (data.get('input') or {}).get('path', '')
    print(path)
except Exception:
    print('')
" 2>/dev/null || echo "")

echo "[pre_tool_use] tool=${TOOL_NAME} command=${COMMAND:0:80}" >&2

# ---------------------------------------------------------------------------
# Edit / Write 工具：拦截对 .claude/** 目录的写操作
# architecture §6：hooks deny Write(.claude/**) / Edit(.claude/**)
# SLA §1.4：host .claude/ 在 worker 视角只读
# ---------------------------------------------------------------------------
if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
    if [[ "$FILE_PATH" =~ (^|/)\.claude(/|$) ]]; then
        echo "[pre_tool_use] DENY: .claude/ write forbidden (architecture §6 hooks 层第三道防线): ${FILE_PATH}" >&2
        exit 2
    fi
    # 非 .claude/ 路径的 Edit/Write → 放行
    exit 0
fi

# ---------------------------------------------------------------------------
# 仅当工具为 Bash 时检查命令
# ---------------------------------------------------------------------------
if [[ "$TOOL_NAME" != "Bash" ]]; then
    # 非 Bash 工具（Read、Glob 等）→ 放行
    exit 0
fi

# ==========================================================================
# Bash 工具 deny 清单（bash ERE 正则，[[ "$COMMAND" =~ <pattern> ]]）
# 来源：architecture §6 + SLA §1.4 + T014.md §Outputs
# ==========================================================================

# --------------------------------------------------------------------------
# 组 1：rm -rf / rm -fr / rm -r -f 变体
# architecture §6：deny rm -rf:*  SLA §1.4 第4条
# --------------------------------------------------------------------------

# rm -rf / rm -rF / rm -Rf / rm -RF（flags 紧凑，含大写变体）
# deny `rm` + 空格 + 连字符 + 含 r/R 和 f/F 的 flags（顺序任意）
if [[ "$COMMAND" =~ (^|[[:space:];|&])rm[[:space:]]+-[rRfF]*[rR][rRfF]*[fF][^[:space:]]* ]] || \
   [[ "$COMMAND" =~ (^|[[:space:];|&])rm[[:space:]]+-[rRfF]*[fF][rRfF]*[rR][^[:space:]]* ]]; then
    echo "[pre_tool_use] DENY: rm -rf/-fr 变体 (architecture §6 · T014): ${COMMAND}" >&2
    exit 2
fi

# rm -r -f 分离 flags 变体（两个独立 flag 组合）
if [[ "$COMMAND" =~ (^|[[:space:];|&])rm[[:space:]]+-[rRfF]*[rR][[:space:]]+-[rRfF]*[fF] ]] || \
   [[ "$COMMAND" =~ (^|[[:space:];|&])rm[[:space:]]+-[rRfF]*[fF][[:space:]]+-[rRfF]*[rR] ]]; then
    echo "[pre_tool_use] DENY: rm -r -f 分离 flags 变体 (architecture §6 · T014): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 2：curl / wget / httpie — deny 外部地址，allow localhost / 127.0.0.1
# architecture §6 + SLA §1.4：deny curl:* 但 allow 本地 proxy 通信
# T010 proxy 通信走 http://127.0.0.1:PORT 或 http://localhost:PORT
# --------------------------------------------------------------------------

# curl：deny 非 localhost/127.0.0.1 目标
if [[ "$COMMAND" =~ (^|[[:space:];|&])curl[[:space:]] ]]; then
    # 先检查是否是本地地址（localhost 或 127.0.0.1）→ 放行
    if [[ "$COMMAND" =~ curl[[:space:]].*https?://(localhost|127\.0\.0\.1)(:[0-9]+)?(/|[[:space:]]|$) ]]; then
        : # localhost / 127.0.0.1 → 继续检查其他规则（不在此处 exit）
    else
        echo "[pre_tool_use] DENY: curl 外部请求（非 localhost/127.0.0.1）(architecture §6): ${COMMAND}" >&2
        exit 2
    fi
fi

# wget：全部 deny（不应有合法的 wget 外部下载场景）
if [[ "$COMMAND" =~ (^|[[:space:];|&])wget[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: wget 外部请求 (architecture §6 · SLA §1.4): ${COMMAND}" >&2
    exit 2
fi

# httpie (http / https CLI 工具)：全部 deny
if [[ "$COMMAND" =~ (^|[[:space:];|&])(http|https)[[:space:]]+[A-Z]*(GET|POST|PUT|DELETE|PATCH|HEAD) ]] || \
   [[ "$COMMAND" =~ (^|[[:space:];|&])httpie[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: httpie 外部请求 (architecture §6): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 3：cat 敏感凭证文件（.env / .key / .pem / ~/.aws/*）
# SLA §1.4：不读 .env / ~/.aws/credentials / 其它 credential 文件
# --------------------------------------------------------------------------

# cat .env（各种形式：.env / .env.local / .env.production 等）
if [[ "$COMMAND" =~ (^|[[:space:];|&])cat[[:space:]].*\.env([^[:alnum:]]|$) ]]; then
    echo "[pre_tool_use] DENY: cat .env 文件（凭证泄露防护）(SLA §1.4): ${COMMAND}" >&2
    exit 2
fi

# cat *.key 私钥文件
if [[ "$COMMAND" =~ (^|[[:space:];|&])cat[[:space:]].*\.key([^[:alnum:]]|$) ]]; then
    echo "[pre_tool_use] DENY: cat *.key 私钥文件 (SLA §1.4): ${COMMAND}" >&2
    exit 2
fi

# cat *.pem 证书文件
if [[ "$COMMAND" =~ (^|[[:space:];|&])cat[[:space:]].*\.pem([^[:alnum:]]|$) ]]; then
    echo "[pre_tool_use] DENY: cat *.pem 证书文件 (SLA §1.4): ${COMMAND}" >&2
    exit 2
fi

# cat ~/.aws/* AWS 凭证目录
if [[ "$COMMAND" =~ (^|[[:space:];|&])cat[[:space:]].*~/\.aws/ ]]; then
    echo "[pre_tool_use] DENY: cat ~/.aws/* AWS 凭证 (SLA §1.4): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 4：chmod / chflags / chattr — deny 权限修改（防止绕过只读保护）
# architecture §6 · SLA §1.4：deny Bash(chmod:*) / Bash(chflags:*) / Bash(chattr:*)
# --------------------------------------------------------------------------

if [[ "$COMMAND" =~ (^|[[:space:];|&])chmod[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: chmod（防止绕过 .claude/ 只读保护）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

if [[ "$COMMAND" =~ (^|[[:space:];|&])chflags[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: chflags（macOS immutable flag 修改防护）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

if [[ "$COMMAND" =~ (^|[[:space:];|&])chattr[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: chattr（Linux immutable flag 修改防护）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 5：sudo / su - — deny 提权
# architecture §6 · SLA §1.4：deny sudo / su -
# --------------------------------------------------------------------------

if [[ "$COMMAND" =~ (^|[[:space:];|&])sudo[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: sudo（提权禁止）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

# su - 或 su -（切换 root）
if [[ "$COMMAND" =~ (^|[[:space:];|&])su[[:space:]]+-( |$) ]] || \
   [[ "$COMMAND" =~ (^|[[:space:];|&])su[[:space:]]+-[[:alnum:]] ]]; then
    echo "[pre_tool_use] DENY: su - 切换 root（提权禁止）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 6：ssh / scp / rsync 外部地址
# architecture §6：deny ssh/scp/rsync 外部（C9 rsync 是用户行为，不进 worker）
# --------------------------------------------------------------------------

if [[ "$COMMAND" =~ (^|[[:space:];|&])ssh[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: ssh 外部连接（worker 禁止远程访问）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

if [[ "$COMMAND" =~ (^|[[:space:];|&])scp[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: scp 外部文件传输（worker 禁止远程访问）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

if [[ "$COMMAND" =~ (^|[[:space:];|&])rsync[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: rsync 外部同步（worker 禁止远程访问）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 7：nc / netcat / socat — deny 网络工具
# architecture §6：deny nc/netcat/socat
# --------------------------------------------------------------------------

# nc（netcat 短命令）—— 匹配 "nc " 开头或命令链中的 nc
if [[ "$COMMAND" =~ (^|[[:space:];|&])nc[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: nc（netcat，网络工具禁止）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

if [[ "$COMMAND" =~ (^|[[:space:];|&])netcat[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: netcat（网络工具禁止）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

if [[ "$COMMAND" =~ (^|[[:space:];|&])socat[[:space:]] ]]; then
    echo "[pre_tool_use] DENY: socat（socket relay 工具禁止）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 8：dd 危险写操作（写块设备 / /dev/random / /dev/urandom to disk）
# architecture §6：deny dd if=/dev/random of=/dev/sda 类
# --------------------------------------------------------------------------

# 匹配 dd 含 "of=/dev/" 目标（写到块设备）
if [[ "$COMMAND" =~ (^|[[:space:];|&])dd[[:space:]].*of=/dev/ ]]; then
    echo "[pre_tool_use] DENY: dd 写块设备（覆盖磁盘操作禁止）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

# --------------------------------------------------------------------------
# 组 9：Bash 命令中写 .claude/ 路径（shell 重定向到 .claude/）
# architecture §6：hooks 层第三道防线，兜底 settings.json deny 层
# --------------------------------------------------------------------------

# 检测 Bash 命令中含 ">.claude/" 或 ">> .claude/" 或 "> .claude/" 等 shell 重定向
if [[ "$COMMAND" =~ (>|>>)[[:space:]]*\.claude/ ]]; then
    echo "[pre_tool_use] DENY: shell 重定向写 .claude/（hooks 层第三道防线）(architecture §6): ${COMMAND}" >&2
    exit 2
fi

# ==========================================================================
# 未命中任何 deny 规则 → 放行
# ==========================================================================
exit 0
