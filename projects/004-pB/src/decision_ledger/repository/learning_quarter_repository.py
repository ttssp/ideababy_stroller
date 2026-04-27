"""
LearningQuarterRepository — T019 (R3 简化版)
结论: 季度学习检查数据存储，对应 learning_quarters 表
细节:
  - insert_quarter: 插入新季度记录 (questions_json)
  - get_quarter: 按 quarter_id 查询
  - update_answers: 更新 answers_json
  - update_scores: 更新 scores_json + finalized
"""

from __future__ import annotations

import json
import logging
from typing import Any

from decision_ledger.repository.base import AsyncConnectionPool

logger = logging.getLogger(__name__)


class LearningQuarterRepository:
    """学习季度数据访问层 (T019 R3)。

    对应表: learning_quarters
    """

    def __init__(self, pool: AsyncConnectionPool) -> None:
        """注入 AsyncConnectionPool。"""
        self._pool = pool

    async def insert_quarter(
        self,
        quarter_id: str,
        generated_at: str,
        questions: list[dict[str, str]],
    ) -> None:
        """插入新季度记录 (写路径)。

        结论: INSERT OR IGNORE 实现幂等，同一 quarter_id 重复调用不报错.
        参数:
          quarter_id: 季度标识 (e.g. "2026-Q2")
          generated_at: ISO 8601 UTC 字符串
          questions: 7 个概念 list (已序列化为 JSON)
        """
        questions_json = json.dumps(questions, ensure_ascii=False)
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT OR IGNORE INTO learning_quarters
                    (quarter_id, generated_at, questions_json, answers_json, scores_json, finalized)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (quarter_id, generated_at, questions_json, "{}", "{}", 0),
            )
            await conn.commit()
        logger.debug("learning_quarter 插入: quarter_id=%s", quarter_id)

    async def get_quarter(self, quarter_id: str) -> dict[str, Any] | None:
        """按 quarter_id 查询季度记录 (读路径)。

        结论: 不存在时返回 None.
        """
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM learning_quarters WHERE quarter_id = ?",
                (quarter_id,),
            )
            row = await cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    async def update_answers(
        self,
        quarter_id: str,
        answers: dict[str, str],
    ) -> None:
        """更新 answers_json (写路径)。

        结论: 仅更新 answers_json，不触碰其他字段.
        参数:
          quarter_id: 季度标识
          answers: {concept_id: answer_text}
        """
        answers_json = json.dumps(answers, ensure_ascii=False)
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE learning_quarters
                SET answers_json = ?
                WHERE quarter_id = ?
                """,
                (answers_json, quarter_id),
            )
            await conn.commit()
        logger.debug("learning_quarter 答案更新: quarter_id=%s", quarter_id)

    async def update_scores(
        self,
        quarter_id: str,
        scores: dict[str, int],
        *,
        finalized: int = 1,
    ) -> None:
        """更新 scores_json + finalized (写路径)。

        结论: grade_learning.py 评分完成后调用，同时标记 finalized.
        参数:
          quarter_id: 季度标识
          scores: {concept_id: score(0-10)}
          finalized: 1=评分完成, 0=未完成
        """
        scores_json = json.dumps(scores, ensure_ascii=False)
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE learning_quarters
                SET scores_json = ?, finalized = ?
                WHERE quarter_id = ?
                """,
                (scores_json, finalized, quarter_id),
            )
            await conn.commit()
        logger.debug(
            "learning_quarter 评分更新: quarter_id=%s finalized=%d", quarter_id, finalized
        )
