#!/usr/bin/env bash
# snapshot.sh — Safety Floor 件 3:取 backup 配置 snapshot
# per ideababy_stroller framework/SHARED-CONTRACT.md §1 第 3 件 + §2 件 3
#
# 原理:周期性 snapshot 关键 backup 配置(IAM rules / API tokens / restore policies),
# 在下一次 snapshot 时与本次 diff,警告 backup destruction patterns(eg "同一 credential
# 被 grant 删除主存 + 备份的权限")。
#
# Usage: snapshot.sh <output-dir>
#   写入 <output-dir>/snapshot-<ISO ts>.json
#   exit 0 if snapshot taken; exit 1 if scope is empty (no backup config to snapshot)
#
# 单人本地 dev 场景 v0.1 简化:扫 .git 配置 + .claude/settings*.json + 任何 *.backup* 文件;
# 真正生产级 backup config(IAM / cloud) v0.2 加(per stage doc OUT v0.1 不实装阈值)

set -euo pipefail

OUTPUT_DIR="${1:-.snapshots}"

if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir -p "$OUTPUT_DIR"
fi

TS="$(date -u +%Y%m%dT%H%M%SZ)"
SNAPSHOT_FILE="$OUTPUT_DIR/snapshot-$TS.json"

# === 收集 snapshot 内容 ===
# v0.1 简化版本:
# - .git/config(remote URL / hooks)
# - .claude/settings*.json(permissions / hooks)
# - 任何 *.backup* / *.bak / *.snapshot 文件路径(不读内容,只录存在)

PWD_REAL="$(pwd)"

GIT_CONFIG=""
if [[ -f .git/config ]]; then
    GIT_CONFIG="$(cat .git/config 2>/dev/null | base64 | tr -d '\n')"
fi

CLAUDE_SETTINGS=""
if [[ -f .claude/settings.json ]]; then
    CLAUDE_SETTINGS="$(cat .claude/settings.json 2>/dev/null | base64 | tr -d '\n')"
fi

BACKUP_FILES="$(find . -maxdepth 4 \
    \( -name '*.backup' -o -name '*.bak' -o -name '*.snapshot' \) \
    -not -path '*/node_modules/*' \
    -not -path '*/.git/*' \
    2>/dev/null | sort | head -50 || true)"

# === 写入 snapshot JSON ===
cat > "$SNAPSHOT_FILE" <<EOF
{
  "ts": "$TS",
  "pwd": "$PWD_REAL",
  "scope_version": "v0.1-local-dev",
  "git_config_b64": "$GIT_CONFIG",
  "claude_settings_b64": "$CLAUDE_SETTINGS",
  "backup_file_paths": [
$(echo "$BACKUP_FILES" | sed 's/.*/    "&",/' | sed '$ s/,$//')
  ]
}
EOF

# 若空 scope(单人 dev 仓全空) — 报告但不 fail
if [[ -z "$GIT_CONFIG" && -z "$CLAUDE_SETTINGS" && -z "$BACKUP_FILES" ]]; then
    echo "WARNING: empty backup-relevant scope at $PWD_REAL — snapshot is essentially empty" >&2
    echo "         (single-developer / new repo — this is normal at v0.1)" >&2
fi

echo "✓ snapshot taken: $SNAPSHOT_FILE"
exit 0
