"""
grade_learning.py — T019 (R3 简化版)
结论: CLI 评分脚本，用 LLMClient 比对 human 答案 vs yaml 标准答案
细节:
  - 命令: python -m scripts.grade_learning --quarter 2026-Q2
  - 从 DB 读取当前季度答案
  - 从 learning_checklist.yaml 读取标准答案
  - asyncio.gather 并发调用 LLMClient 评分 (每题 0-10 分)
  - 均分 >= 7.0 视为通过 (O4 verification)
  - 打印总分 + 通过/未通过状态
  - 写入 scores_json + finalized=1 到 DB
  - 可选: 追加 release_log.jsonl

提示: LLM 调用只在此脚本，service 路径零 LLM 调用 (R3 cut)

用法:
  uv run python -m scripts.grade_learning --quarter 2026-Q2
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from pydantic import BaseModel

# 确保项目根目录在 sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ── LLM 评分 Schema ─────────────────────────────────────────────────────────


class GradeResult(BaseModel):
    """LLM 评分返回 Schema (grade_learning_v1 prompt).

    结论: score=0-10 整数，brief_reason ≤ 20 字 (内部记录，不展示给 human).
    """

    score: int  # 0-10
    brief_reason: str  # ≤ 20 字，说明扣分主因或满分原因


# ── 评分 Prompt 渲染 ─────────────────────────────────────────────────────────

_GRADE_PROMPT_TEMPLATE = """\
你是一位学习评估专家。请评估以下投资决策系统学习检查答案的质量。

## 评分规则
- 评分范围: 0-10 整数
- 10分: 完全掌握核心概念，答案准确且有深度
- 7-9分: 基本掌握，主旨正确，细节可能不完整
- 4-6分: 部分理解，有明显缺漏或误解
- 1-3分: 极少掌握，答案偏离核心概念
- 0分: 未作答或完全错误

## 评分要求
- 主旨匹配优先：不强求逐字对照，只要核心概念准确即可得高分
- 宽容理解：允许不同的表达方式，重点是理解深度
- 只输出 JSON，不输出任何解释文字

## 待评估内容

概念: {concept}

标准答案:
{standard_answer}

Human 答案:
{human_answer}
"""


def _render_grade_prompt(
    concept: str,
    standard_answer: str,
    human_answer: str,
) -> str:
    """渲染评分 prompt。

    结论: 简单字符串替换，不用 Jinja2 (避免依赖引入).
    """
    return _GRADE_PROMPT_TEMPLATE.format(
        concept=concept,
        standard_answer=standard_answer,
        human_answer=human_answer,
    )


# ── 核心评分函数 ─────────────────────────────────────────────────────────────


async def _grade_single(
    *,
    question: dict[str, str],
    human_answer: str,
    llm_client: Any,
    quarter_id: str,
) -> tuple[str, int]:
    """评估单题，返回 (concept_id, score)。

    结论: 无答案时 score=0; LLM 失败时 score=0 (宽松降级，不中断整体评分).
    """
    concept_id = question["id"]
    concept = question["concept"]
    standard_answer = question["standard_answer"]

    if not human_answer.strip():
        logger.warning("概念 %s 无答案，score=0", concept_id)
        return concept_id, 0

    prompt = _render_grade_prompt(
        concept=concept,
        standard_answer=standard_answer,
        human_answer=human_answer,
    )

    try:
        result: GradeResult = await llm_client.call(
            prompt=prompt,
            template_version="grade_learning_v1",
            cache_key_extras={
                "advisor_week_id": quarter_id,
                "ticker": concept_id,
            },
            schema=GradeResult,
        )
        score = max(0, min(10, result.score))  # 强制 clamp 0-10
        logger.info("概念 %s 评分: %d/10 (%s)", concept_id, score, result.brief_reason)
        return concept_id, score
    except Exception as exc:
        logger.error("概念 %s 评分失败: %s，score=0", concept_id, exc)
        return concept_id, 0


async def grade_quarter(
    *,
    quarter_id: str,
    svc: Any,
    llm_client: Any,
) -> float:
    """评估整个季度，返回均分。

    结论: 并发评分 (asyncio.gather) + 保存结果到 DB.
    参数:
      quarter_id: 季度标识
      svc: LearningCheckService 实例
      llm_client: LLMClient 实例
    返回:
      均分 (0.0-10.0)
    """
    # 读取季度数据
    quarter = await svc.get_quarter(quarter_id)
    if quarter is None:
        raise ValueError(
            f"季度 {quarter_id} 不存在，请先运行 learning_check.py --quarter {quarter_id}"
        )

    questions: list[dict[str, str]] = json.loads(quarter["questions_json"])
    answers: dict[str, str] = json.loads(quarter.get("answers_json", "{}"))

    if not questions:
        raise ValueError(f"季度 {quarter_id} 无题目，数据可能损坏")

    logger.info("开始评分季度 %s，共 %d 题", quarter_id, len(questions))

    # 并发评分
    tasks = [
        _grade_single(
            question=q,
            human_answer=answers.get(q["id"], ""),
            llm_client=llm_client,
            quarter_id=quarter_id,
        )
        for q in questions
    ]
    results: list[tuple[str, int]] = await asyncio.gather(*tasks)

    scores = dict(results)

    # 保存评分结果
    avg: float = await svc.save_scores(quarter_id, scores, finalized=True)

    return avg


# ── CLI 入口 ─────────────────────────────────────────────────────────────────


class _FakeUsageWriter:
    """mock LLMUsageWriter (避免 DB 依赖时使用)。"""

    async def insert(self, usage: Any) -> None:
        pass

    async def monthly_total_cost(self) -> Decimal:
        return Decimal("0.0")


async def _main(quarter_id: str) -> None:
    """CLI 主流程。"""
    from decision_ledger.llm.client import LLMClient
    from decision_ledger.repository.base import AsyncConnectionPool
    from decision_ledger.repository.learning_quarter_repository import LearningQuarterRepository
    from decision_ledger.services.learning_check_service import LearningCheckService

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY 未设置，使用 mock 模式")

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

        llm_client = LLMClient(
            api_key=api_key or "mock-key",
            usage_writer=_FakeUsageWriter(),
        )

        avg = await grade_quarter(
            quarter_id=quarter_id,
            svc=svc,
            llm_client=llm_client,
        )

        passing = svc.is_passing(avg)
        print("\n" + "=" * 60)
        print(f"季度 {quarter_id} 学习检查评分完成")
        print(f"均分: {avg:.2f} / 10")
        print(f"结论: {'通过 ✓' if passing else '未通过 ✗'} (通过线: 7.0/10)")
        print("=" * 60 + "\n")

        # 追加 release_log.jsonl
        log_path = _PROJECT_ROOT / "release_log.jsonl"
        entry = {
            "event": "learning_grade",
            "quarter_id": quarter_id,
            "average_score": round(avg, 2),
            "passing": passing,
            "graded_at": datetime.now(tz=UTC).isoformat(),
        }
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        logger.info("评分记录已追加到 release_log.jsonl")

    finally:
        await pool.close()


def main() -> None:
    """CLI 入口点。"""
    parser = argparse.ArgumentParser(
        description="季度学习检查评分 — LLM 比对 human 答案 vs 标准答案",
        prog="python -m scripts.grade_learning",
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
