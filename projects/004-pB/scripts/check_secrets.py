#!/usr/bin/env python3
"""
pre-commit 敏感内容检测钩子 — T001
结论: 扫描 staged 文件，发现敏感字符串/路径即拒绝提交
细节:
  - 检测 Anthropic API key 前缀: sk-ant-
  - 检测 Telegram bot token 格式: bot[0-9]+: 或 [0-9]+:[A-Za-z0-9_-]{35,}
  - 检测 inbox/ 路径字样（版权内容）
  - 检测 db.sqlite 字样（F3 修复后已统一为 data.sqlite, 此 hook 防回退）
  - 二进制文件跳过
  - 退出码 0 = 通过, 1 = 拦截
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ── 检测规则 ─────────────────────────────────────────────
# 结论: 每条规则含 (name, pattern, 说明)，命中任一即拒绝
RULES: list[tuple[str, re.Pattern[str], str]] = [
    (
        "anthropic_api_key",
        re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"),
        "疑似 Anthropic API key (sk-ant-...)",
    ),
    (
        "telegram_bot_token",
        re.compile(r"\bbot[0-9]{6,}:[A-Za-z0-9_\-]{30,}", re.IGNORECASE),
        "疑似 Telegram Bot Token (bot{id}:{token})",
    ),
    (
        "telegram_token_raw",
        re.compile(r"\b[0-9]{7,}:[A-Za-z0-9_\-]{35,}\b"),
        "疑似 Telegram Bot Token ({id}:{token} 格式)",
    ),
    (
        "inbox_path",
        re.compile(r"\binbox/"),
        "路径包含 inbox/（咨询师 PDF 目录，版权敏感）",
    ),
    (
        "legacy_db_sqlite",
        re.compile(r"\bdb\.sqlite"),
        "包含 db.sqlite（F3 修复后已统一为 data.sqlite, 此命中说明回退到旧路径）",
    ),
]

# ── 豁免文件（这些文件本身就是示例/文档，允许含占位字样）────
EXEMPT_SUFFIXES = {
    ".example",
    ".md",
}
EXEMPT_NAMES = {
    ".env.example",
    "check_secrets.py",  # 此脚本自身含检测字符串
    "CLAUDE.md",
    "AGENTS.md",
}


def is_binary(path: Path) -> bool:
    """结论: 检测文件是否为二进制，二进制跳过。"""
    try:
        with path.open("rb") as f:
            chunk = f.read(8192)
            return b"\x00" in chunk
    except OSError:
        return False


def check_file(path: Path) -> list[str]:
    """扫描单个文件，返回命中的违规描述列表（空 = 通过）。"""
    violations: list[str] = []

    # 豁免检查
    if path.name in EXEMPT_NAMES:
        return []
    if path.suffix in EXEMPT_SUFFIXES:
        return []
    if is_binary(path):
        return []

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        # 无法读取的文件不阻塞提交，但记录警告
        print(f"  ⚠ 无法读取 {path}: {e}", file=sys.stderr)
        return []

    for _rule_name, pattern, description in RULES:
        if pattern.search(content):
            violations.append(f"  命中规则 [{_rule_name}]: {description}")

    return violations


def main() -> int:
    """主入口：接受 pre-commit 传入的 staged 文件路径列表。"""
    files = sys.argv[1:]
    if not files:
        return 0

    found_any = False
    for file_path_str in files:
        path = Path(file_path_str)
        if not path.exists():
            continue

        violations = check_file(path)
        if violations:
            found_any = True
            print(f"\n[BLOCKED] {path}", file=sys.stderr)
            for v in violations:
                print(v, file=sys.stderr)

    if found_any:
        print(
            "\n❌ pre-commit 拦截: 检测到敏感内容，请从文件中移除后重新 commit。",
            file=sys.stderr,
        )
        print(
            "   提示: .env 文件应已 gitignored，不应出现在 staged 列表中。",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
