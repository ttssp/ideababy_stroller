#!/usr/bin/env bash
# lock-deps.sh — 依赖锁文件重生成脚本（T002 · R5 供应链缓解 · C17）
# 用法：bash scripts/lock-deps.sh
# 前提：已安装 uv >= 0.11.0（参考 docs/dependency-policy.md）
# 可重入：多次执行结果幂等（uv lock 会跳过无变更情况）
#
# 产出：
#   uv.lock               — universal lock（跨平台 · macOS arm64 + Linux x86_64 · dev 用）
#   requirements-locked.txt — 含 SHA-256 hash 的 linux-targeted lock（prod 训练机用 · R5 防御）
#
# 说明（ops-decision 2026-04-24）：
#   requirements-locked.txt 中的 linux-only marker 来自 pyproject.toml PEP 508 marker；
#   uv export 会自动排除在当前 lock 中未解析的平台条目，结果等价于 --python-platform linux 效果。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"

cd "${PROJECT_ROOT}"

echo "[lock-deps] 当前目录: ${PROJECT_ROOT}"
echo "[lock-deps] Step 1/3: 生成 universal uv.lock（跨平台 dev lock）..."
uv lock

echo "[lock-deps] Step 2/3: 导出 linux-targeted requirements-locked.txt（含 SHA-256 hash · prod 用）..."
# 导出时 --no-dev 排除开发依赖；
# linux-only marker（sys_platform == 'linux'）在 uv.lock 中已解析为 linux x86_64 条目
# uv export 仅导出 lock 中实际存在的包，mac-only / dev 包自动排除
uv export \
    --format requirements-txt \
    --hashes \
    --no-dev \
    --output-file requirements-locked.txt

echo "[lock-deps] Step 3/3: 校验 hash 完整性..."
HASH_COUNT=$(grep -c -- '--hash=' requirements-locked.txt 2>/dev/null || echo 0)
SHA_COUNT=$(grep -c 'sha256:' requirements-locked.txt 2>/dev/null || echo 0)

if [ "${HASH_COUNT}" -lt 1 ] && [ "${SHA_COUNT}" -lt 1 ]; then
    echo "[lock-deps] ERROR: requirements-locked.txt 中未找到 hash，可能 uv export 参数有误"
    exit 1
fi

echo "[lock-deps] 完成。生成文件概要："
echo "  uv.lock                  — $(wc -l < uv.lock) 行（精确版本 + hash，提交入 git）"
echo "  requirements-locked.txt  — $(wc -l < requirements-locked.txt) 行（pip --require-hashes 格式，提交入 git）"
echo "  sha256 hash 条目数:       ${SHA_COUNT}"
echo ""
echo "[lock-deps] macOS 本地开发安装（跳过 Linux-only 包）："
echo "  uv sync --no-install-package bitsandbytes --no-install-package unsloth"
echo "  详见 docs/dependency-policy.md §4"
