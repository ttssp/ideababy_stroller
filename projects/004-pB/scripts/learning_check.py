"""
learning_check.py — T019 (R3 简化版)
结论: CLI 入口，触发季度学习检查抽题
细节:
  - 命令: python -m scripts.learning_check --quarter 2026-Q2
  - 从 learning_checklist.yaml 随机抽 7 题写入 DB
  - 打印抽取的题目列表，供 human 在浏览器答题
  - 无 LLM 调用 (R3 cut)

用法:
  uv run python -m scripts.learning_check --quarter 2026-Q2
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any

# 确保项目根目录在 sys.path，使 scripts 可作为模块运行
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def run_start_quarter(
    quarter_id: str,
    svc: Any,
) -> list[dict[str, str]]:
    """触发季度抽题，返回 7 个概念列表。

    结论: 仅调用 service 的 start_quarter，无 LLM 调用 (R3 cut).
    参数:
      quarter_id: 季度标识 (e.g. "2026-Q2")
      svc: LearningCheckService 实例
    返回:
      7 个概念的 list
    """
    questions: list[dict[str, str]] = await svc.start_quarter(quarter_id)
    return questions


async def _main(quarter_id: str) -> None:
    """CLI 主流程。"""
    from decision_ledger.repository.base import AsyncConnectionPool
    from decision_ledger.repository.learning_quarter_repository import LearningQuarterRepository
    from decision_ledger.services.learning_check_service import LearningCheckService

    db_url = os.environ.get("DECISION_LEDGER_DB_URL", "")
    if db_url.startswith("sqlite:///"):
        db_path = db_url[len("sqlite:///"):]
    else:
        db_path = str(_PROJECT_ROOT / "db.sqlite")

    pool = AsyncConnectionPool(db_path)
    await pool.initialize()

    try:
        repo = LearningQuarterRepository(pool=pool)
        svc = LearningCheckService(repo=repo)

        logger.info("开始季度 %s 抽题...", quarter_id)
        questions = await run_start_quarter(quarter_id=quarter_id, svc=svc)

        print(f"\n季度 {quarter_id} 学习检查题目 (共 {len(questions)} 题):")
        print("=" * 60)
        for i, q in enumerate(questions, 1):
            print(f"\n[{i}] 概念 ID: {q['id']}")
            print(f"    题目: {q['concept']}")
        print("\n" + "=" * 60)
        print(f"请访问浏览器 /learning/{quarter_id} 提交答案")

    finally:
        await pool.close()


def main() -> None:
    """CLI 入口点。"""
    parser = argparse.ArgumentParser(
        description="季度学习检查 — 从 checklist.yaml 随机抽 7 题",
        prog="python -m scripts.learning_check",
    )
    parser.add_argument(
        "--quarter",
        required=True,
        help='季度标识，格式 YYYY-QN，例如 "2026-Q2"',
    )

    args = parser.parse_args()
    asyncio.run(_main(args.quarter))


if __name__ == "__main__":
    main()
