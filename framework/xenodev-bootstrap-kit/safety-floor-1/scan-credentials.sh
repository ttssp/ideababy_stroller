#!/usr/bin/env bash
# scan-credentials.sh — Safety Floor 件 1:凭据隔离检测脚本
# per ideababy_stroller framework/SHARED-CONTRACT.md §1 第 1 件 + §2 件 1
#
# Usage: scan-credentials.sh [<dir>]
#   <dir> 默认 = 当前目录
#   exit 0 if no credentials found (silent)
#   exit 1 if credentials found (stderr lists matched files)
#
# 检测对象(per §1 第 1 件):
# - .env.production* / .env.prod* / .env.local
# - secrets/production/* / secrets/prod/*
# - 文件内含 prod://连接字串

set -euo pipefail

SCAN_DIR="${1:-.}"

if [[ ! -d "$SCAN_DIR" ]]; then
    echo "ERROR: directory not found: $SCAN_DIR" >&2
    exit 2
fi

FOUND=0
MATCHED_FILES=()

# === 检测 1:文件名模式(.env.production* / .env.prod* / .env.local)===
while IFS= read -r -d '' file; do
    FOUND=1
    MATCHED_FILES+=("$file (filename pattern: production env)")
done < <(find "$SCAN_DIR" \
    \( -name '.env.production' -o -name '.env.production.*' \
       -o -name '.env.prod' -o -name '.env.prod.*' \
       -o -name '.env.local' \) \
    -not -name '*.fake' \
    -not -path '*/node_modules/*' \
    -not -path '*/.git/*' \
    -print0 2>/dev/null)

# === 检测 2:secrets/production/* 路径 ===
if [[ -d "$SCAN_DIR/secrets/production" ]]; then
    while IFS= read -r -d '' file; do
        # skip .fake suffix(测试 fixture 用)
        if [[ "$file" != *.fake ]]; then
            FOUND=1
            MATCHED_FILES+=("$file (secrets/production/ path)")
        fi
    done < <(find "$SCAN_DIR/secrets/production" -type f -print0 2>/dev/null)
fi
if [[ -d "$SCAN_DIR/secrets/prod" ]]; then
    while IFS= read -r -d '' file; do
        if [[ "$file" != *.fake ]]; then
            FOUND=1
            MATCHED_FILES+=("$file (secrets/prod/ path)")
        fi
    done < <(find "$SCAN_DIR/secrets/prod" -type f -print0 2>/dev/null)
fi

# === 检测 3:文件内含 prod:// 连接字串 ===
# (只扫文本文件,跳过二进制 / 大文件 / .git / node_modules)
#
# B2.2 Block A.7 codex round 4 finding #1 fix:
# 旧 SKIP_BASENAMES(基名)误 skip 任意位置的 README.md / AGENTS.md / CLAUDE.md →
# docs/README.md 含真 prod:// 不被检测,等于绕过 Safety Floor 件 1。
# 新 SKIP_PATH_SUFFIXES:精确路径(以 suffix 匹配,容纳 IDS 与 XenoDev 两种位置)。
# SKIP_PATHS:相对仓根的精确路径(必须 == 形如 "AGENTS.md" 或 "framework/...");
# 不允许 suffix 通配,防 vendor/lib/AGENTS.md 误 skip。
# 路径形式:相对 SCAN_DIR 的 normalized 路径(用 realpath 后比对)。
declare -a SKIP_PATHS=(
    "framework/xenodev-bootstrap-kit/safety-floor-1/scan-credentials.sh"
    "framework/xenodev-bootstrap-kit/safety-floor-1/pre-commit-credential.sh"
    "framework/xenodev-bootstrap-kit/safety-floor-1/context-loader-filter.md"
    "framework/xenodev-bootstrap-kit/safety-floor-1/README.md"
    "framework/xenodev-bootstrap-kit/AGENTS.md"
    "framework/xenodev-bootstrap-kit/CLAUDE.md"
    "framework/xenodev-bootstrap-kit/README.md.template"
    "framework/SHARED-CONTRACT.md"
    "framework/AUTODEV-PIPE-SYNC-PROPOSAL.md"
    "AGENTS.md"
    "CLAUDE.md"
    ".claude/safety-floor/credential-isolation/scan-credentials.sh"
    ".claude/safety-floor/credential-isolation/pre-commit-credential.sh"
    ".claude/safety-floor/credential-isolation/context-loader-filter.md"
    ".claude/safety-floor/credential-isolation/README.md"
)
# 解析 SCAN_DIR 的 realpath,后续把 file 转 SCAN_DIR-relative 再比对
SCAN_DIR_REAL="$(cd "$SCAN_DIR" 2>/dev/null && pwd -P)"
while IFS= read -r file; do
    # skip .fake / 测试 fixtures 中预期含 prod:// 的位置
    if [[ "$file" == *.fake ]] || [[ "$file" == *test-fixtures* ]]; then
        continue
    fi
    # 把 file 转换成 SCAN_DIR-relative 路径(grep -rIl 输出的是 SCAN_DIR/path 形式)
    file_real="$(cd "$(dirname "$file")" 2>/dev/null && pwd -P)/$(basename "$file")"
    rel="${file_real#$SCAN_DIR_REAL/}"
    # skip 白名单(精确相对路径匹配,不允许 suffix 通配)
    skip=0
    for p in "${SKIP_PATHS[@]}"; do
        if [[ "$rel" == "$p" ]]; then
            skip=1
            break
        fi
    done
    [[ $skip -eq 1 ]] && continue
    FOUND=1
    MATCHED_FILES+=("$file (file content: prod:// connection string)")
done < <(grep -rIl 'prod://' "$SCAN_DIR" \
    --exclude-dir=.git \
    --exclude-dir=node_modules \
    --exclude-dir=.venv \
    --exclude='*.fake' \
    2>/dev/null || true)

# === 输出 ===
if [[ "$FOUND" == 1 ]]; then
    echo "ERROR: production credentials detected in $SCAN_DIR (Safety Floor 件 1 violation)" >&2
    echo "" >&2
    echo "Matched files:" >&2
    for entry in "${MATCHED_FILES[@]}"; do
        echo "  - $entry" >&2
    done
    echo "" >&2
    echo "Action: 移除文件 / 加 .gitignore / 重命名(若是 fixture 加 .fake 后缀)" >&2
    exit 1
fi

# silent on success
exit 0
