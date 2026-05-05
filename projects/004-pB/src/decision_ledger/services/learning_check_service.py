"""
LearningCheckService — T019 (R3 简化版)
结论: 季度学习检查服务，human 手编 master checklist，agent 仅按 checklist 抽问
细节:
  - start_quarter(quarter_id): 从 learning_checklist.yaml 随机抽 7 个概念，入 learning_quarters
  - save_answers(quarter_id, answers): 保存 human 答案
  - get_quarter(quarter_id): 查询季度数据
  - compute_average_score(scores): 计算均分
  - is_passing(average_score): 均分 >= 7.0 视为通过 (O4 verification)

R3 真砍约束:
  - 不调 LLM (service 路径零 LLM 调用)
  - 仅抽题 + 存储 + 评分计算
  - 评分 LLM 只在 scripts/grade_learning.py 调用
  - 不做 nav UI 提醒
"""

from __future__ import annotations

import logging
import random
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

# 默认 checklist 路径 (项目 docs 目录)
_DEFAULT_CHECKLIST_PATH = Path(__file__).resolve().parents[3] / "docs" / "learning_checklist.yaml"

# 每季度抽题数量
_SAMPLE_SIZE = 7


class LearningCheckService:
    """季度学习检查服务 (R3 简化版，零 LLM 调用)。

    架构约束 (R3):
      - 无 LLM 调用: 抽题仅随机抽 yaml，评分委托给 grade_learning.py 脚本
      - 不依赖 LLMClient: __init__ 只接受 repo + checklist_path
    """

    def __init__(
        self,
        repo: Any,
        checklist_path: Path | None = None,
    ) -> None:
        """
        结论: 仅注入 LearningQuarterRepository + checklist 路径，无 LLM 依赖 (R3 cut).
        参数:
          repo: LearningQuarterRepository 实例 (duck typing)
          checklist_path: learning_checklist.yaml 路径 (None 时用默认路径)
        """
        self._repo = repo
        self._checklist_path = checklist_path or _DEFAULT_CHECKLIST_PATH

    # ── checklist 解析 ────────────────────────────────────────────────────────

    def _load_checklist(self) -> list[dict[str, str]]:
        """从 yaml 加载 master checklist 概念列表。

        结论: 每次调用重新读文件 (yaml 小文件，无需缓存).
        返回: list of {id, concept, standard_answer}
        Raises:
          FileNotFoundError: yaml 文件不存在
          ValueError: 概念数量 < 7
        """
        path = self._checklist_path
        if not path.exists():
            raise FileNotFoundError(f"learning_checklist.yaml 不存在: {path}")

        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)

        concepts: list[dict[str, str]] = data.get("concepts", [])

        if len(concepts) < _SAMPLE_SIZE:
            raise ValueError(
                f"至少需要 {_SAMPLE_SIZE} 个概念，当前 yaml 只有 {len(concepts)} 个"
            )

        return concepts

    # ── 季度抽题 ──────────────────────────────────────────────────────────────

    async def start_quarter(self, quarter_id: str) -> list[dict[str, str]]:
        """从 master checklist 随机抽 7 个概念，写入 learning_quarters 表。

        结论: 不调 LLM，纯随机抽样 (R3 cut).
        参数:
          quarter_id: 季度标识 (e.g. "2026-Q2")
        返回:
          7 个概念的 list，每项含 {id, concept, standard_answer}
        Raises:
          FileNotFoundError: checklist yaml 不存在
          ValueError: checklist 概念数量不足
        """
        concepts = self._load_checklist()
        sampled = random.sample(concepts, _SAMPLE_SIZE)

        generated_at = datetime.now(tz=UTC).isoformat()

        await self._repo.insert_quarter(
            quarter_id=quarter_id,
            generated_at=generated_at,
            questions=sampled,
        )

        logger.info("季度 %s 抽题完成，共 %d 题", quarter_id, len(sampled))
        return sampled

    # ── 答案管理 ─────────────────────────────────────────────────────────────

    async def save_answers(self, quarter_id: str, answers: dict[str, str]) -> None:
        """保存 human 提交的答案到 learning_quarters.answers_json。

        结论: 纯 DB 写入，不调 LLM.
        参数:
          quarter_id: 季度标识
          answers: {concept_id: answer_text} 字典
        """
        await self._repo.update_answers(quarter_id, answers)
        logger.info("季度 %s 答案已保存，共 %d 条", quarter_id, len(answers))

    # ── 季度查询 ─────────────────────────────────────────────────────────────

    async def get_quarter(self, quarter_id: str) -> dict[str, Any] | None:
        """查询季度数据。

        结论: 不存在时返回 None，由调用方处理.
        参数:
          quarter_id: 季度标识
        返回:
          含 quarter_id/generated_at/questions_json/answers_json/scores_json/finalized 的 dict，
          或 None (不存在)
        """
        return await self._repo.get_quarter(quarter_id)  # type: ignore[no-any-return]

    # ── 评分计算 ─────────────────────────────────────────────────────────────

    def compute_average_score(self, scores: dict[str, int]) -> float:
        """计算均分 (0.0-10.0)。

        结论: 空 scores 返回 0.0; 否则返回所有分数的算术平均值.
        参数:
          scores: {concept_id: score(0-10)} 字典
        返回:
          float 均分
        """
        if not scores:
            return 0.0
        return sum(scores.values()) / len(scores)

    def is_passing(self, average_score: float) -> bool:
        """判断季度学习检查是否通过 (O4 verification)。

        结论: 均分 >= 7.0 视为通过.
        参数:
          average_score: 均分 (0.0-10.0)
        返回:
          True=通过, False=未通过
        """
        return average_score >= 7.0

    # ── 评分写入 ─────────────────────────────────────────────────────────────

    async def save_scores(
        self,
        quarter_id: str,
        scores: dict[str, int],
        *,
        finalized: bool = True,
    ) -> float:
        """保存 LLM 评分结果，返回均分。

        结论: 由 grade_learning.py 脚本调用，不在 web 请求路径调用.
        参数:
          quarter_id: 季度标识
          scores: {concept_id: score(0-10)} 字典
          finalized: 是否标记为已完成 (默认 True)
        返回:
          均分 float
        """
        await self._repo.update_scores(
            quarter_id,
            scores,
            finalized=1 if finalized else 0,
        )
        avg = self.compute_average_score(scores)
        logger.info(
            "季度 %s 评分已保存 | 均分=%.2f | 通过=%s",
            quarter_id,
            avg,
            self.is_passing(avg),
        )
        return avg
