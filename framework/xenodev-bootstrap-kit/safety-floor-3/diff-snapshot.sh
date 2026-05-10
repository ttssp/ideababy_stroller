#!/usr/bin/env bash
# diff-snapshot.sh — Safety Floor 件 3:比对两次 snapshot,报警 backup destruction patterns
# per ideababy_stroller framework/SHARED-CONTRACT.md §1 第 3 件 + §2 件 3
#
# Usage: diff-snapshot.sh <snapshot-A.json> <snapshot-B.json>
#   exit 0 if no destruction pattern detected
#   exit 1 if destruction pattern detected (stderr lists pattern + recommendation)
#
# v0.1 检测 4 类破坏模式:
# 1. backup 文件突然消失(有 → 无)
# 2. .git/config 中 push policy 变宽松(eg 加了 force push)
# 3. .claude/settings.json permissions.deny 减少(防御能力变弱)
# 4. snapshot 间隔 > 30 天(operator 长时间未跑 → 防 snapshot 本身失效)

set -euo pipefail

A="${1:-}"
B="${2:-}"

if [[ -z "$A" || -z "$B" ]]; then
    echo "Usage: diff-snapshot.sh <snapshot-A.json> <snapshot-B.json>" >&2
    exit 2
fi

if [[ ! -f "$A" ]]; then
    echo "ERROR: snapshot A not found: $A" >&2
    exit 2
fi
if [[ ! -f "$B" ]]; then
    echo "ERROR: snapshot B not found: $B" >&2
    exit 2
fi

# 用 python 读 JSON(避免 jq 依赖)
EXTRACT='
import json, sys, base64
try:
    d = json.load(sys.stdin)
    print("TS=" + d.get("ts", ""))
    print("PWD=" + d.get("pwd", ""))
    print("GIT=" + d.get("git_config_b64", ""))
    print("CLAUDE=" + d.get("claude_settings_b64", ""))
    print("BACKUPS=" + ",".join(d.get("backup_file_paths", [])))
except Exception as e:
    print("ERROR: " + str(e), file=sys.stderr)
    sys.exit(1)
'

A_DATA="$(python3 -c "$EXTRACT" < "$A")"
B_DATA="$(python3 -c "$EXTRACT" < "$B")"

A_TS="$(echo "$A_DATA" | grep '^TS=' | cut -d= -f2-)"
B_TS="$(echo "$B_DATA" | grep '^TS=' | cut -d= -f2-)"
A_GIT="$(echo "$A_DATA" | grep '^GIT=' | cut -d= -f2-)"
B_GIT="$(echo "$B_DATA" | grep '^GIT=' | cut -d= -f2-)"
A_CLAUDE="$(echo "$A_DATA" | grep '^CLAUDE=' | cut -d= -f2-)"
B_CLAUDE="$(echo "$B_DATA" | grep '^CLAUDE=' | cut -d= -f2-)"
A_BACKUPS="$(echo "$A_DATA" | grep '^BACKUPS=' | cut -d= -f2-)"
B_BACKUPS="$(echo "$B_DATA" | grep '^BACKUPS=' | cut -d= -f2-)"

ALERTS=()

# === 检测 1:backup 文件突然消失 ===
if [[ -n "$A_BACKUPS" && -z "$B_BACKUPS" ]]; then
    ALERTS+=("CRITICAL: backup files in A ($A_BACKUPS) all disappeared in B")
fi

# === 检测 2:.git/config 变化(可能 push policy 变宽松)===
if [[ "$A_GIT" != "$B_GIT" && -n "$A_GIT" && -n "$B_GIT" ]]; then
    A_GIT_TXT="$(echo "$A_GIT" | base64 -d 2>/dev/null || echo '')"
    B_GIT_TXT="$(echo "$B_GIT" | base64 -d 2>/dev/null || echo '')"
    # 简化检测:B 含 'push.*force' 但 A 不含
    if echo "$B_GIT_TXT" | grep -qE 'push.*force|forcePush' && ! echo "$A_GIT_TXT" | grep -qE 'push.*force|forcePush'; then
        ALERTS+=("WARNING: B contains push --force config but A did not — push policy widened")
    fi
fi

# === 检测 3:.claude/settings.json permissions.deny 减少 ===
if [[ -n "$A_CLAUDE" && -n "$B_CLAUDE" ]]; then
    A_CLAUDE_TXT="$(echo "$A_CLAUDE" | base64 -d 2>/dev/null || echo '')"
    B_CLAUDE_TXT="$(echo "$B_CLAUDE" | base64 -d 2>/dev/null || echo '')"
    A_DENY_COUNT="$(echo "$A_CLAUDE_TXT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get("permissions",{}).get("deny",[])))' 2>/dev/null || echo 0)"
    B_DENY_COUNT="$(echo "$B_CLAUDE_TXT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get("permissions",{}).get("deny",[])))' 2>/dev/null || echo 0)"
    if [[ "$B_DENY_COUNT" -lt "$A_DENY_COUNT" ]]; then
        ALERTS+=("WARNING: permissions.deny count A=$A_DENY_COUNT > B=$B_DENY_COUNT — defense capability weakened")
    fi
fi

# === 检测 4:snapshot 间隔 > 30 天 ===
# (TS 格式 20260510T120000Z;转 epoch 比较)
A_EPOCH="$(date -j -u -f '%Y%m%dT%H%M%SZ' "$A_TS" '+%s' 2>/dev/null || echo 0)"
B_EPOCH="$(date -j -u -f '%Y%m%dT%H%M%SZ' "$B_TS" '+%s' 2>/dev/null || echo 0)"
if [[ "$A_EPOCH" -gt 0 && "$B_EPOCH" -gt 0 ]]; then
    DIFF_DAYS="$(( (B_EPOCH - A_EPOCH) / 86400 ))"
    if [[ "$DIFF_DAYS" -gt 30 ]]; then
        ALERTS+=("INFO: snapshot interval = $DIFF_DAYS days (> 30) — recommend more frequent snapshots")
    fi
fi

# === 输出 ===
if [[ ${#ALERTS[@]} -gt 0 ]]; then
    echo "Backup destruction pattern detection: ${#ALERTS[@]} alert(s) for $A vs $B" >&2
    for alert in "${ALERTS[@]}"; do
        echo "  - $alert" >&2
    done
    echo "" >&2
    echo "Action: 检查 ${#ALERTS[@]} 条 alert,确认是 operator 主动改 vs 异常" >&2
    # CRITICAL 项 → exit 1;WARNING/INFO → exit 0(报警但不 block)
    if printf '%s\n' "${ALERTS[@]}" | grep -q '^CRITICAL'; then
        exit 1
    fi
fi

exit 0
