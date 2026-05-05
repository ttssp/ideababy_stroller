"""
PostMortemService 单元测试 — T018
结论: 验证时间约束校验逻辑（executed_at >= pre_commit_at; result_pct_after_7d 7天限制）
细节:
  - executed_at < pre_commit_at → PostMortemValidationError (422)
  - result_pct_after_7d 在决策不到 7 天时填写 → PostMortemValidationError (422)
  - hold/wait 决策 executed_at 留空 → 合法 (R11: 不动允许复盘)
  - result_pct_after_30d 无时间限制 (30天窗口比7d宽松，测试场景是决策后第3天填30d)
    注: 规格只限制 7d 字段，30d 字段无限制
  - 全空回填也合法（允许只填 notes）
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from decision_ledger.services.post_mortem_service import (
    PostMortemService,
    PostMortemValidationError,
)


class TestExecutedAtConstraint:
    """executed_at >= pre_commit_at 校验。"""

    def test_should_raise_when_executed_at_before_pre_commit_at(self) -> None:
        """结论: executed_at < pre_commit_at → PostMortemValidationError。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        executed_at = datetime(2026, 4, 19, 10, 0, 0, tzinfo=UTC)  # 早一天

        with pytest.raises(PostMortemValidationError, match="executed_at"):
            svc.validate(
                pre_commit_at=pre_commit_at,
                executed_at=executed_at,
                result_pct_after_7d=None,
                result_pct_after_30d=None,
                retrospective_notes=None,
                now=pre_commit_at + timedelta(days=10),
            )

    def test_should_pass_when_executed_at_equals_pre_commit_at(self) -> None:
        """结论: executed_at == pre_commit_at → 合法（边界值）。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        executed_at = pre_commit_at  # 同一时刻

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=executed_at,
            result_pct_after_7d=None,
            result_pct_after_30d=None,
            retrospective_notes=None,
            now=pre_commit_at + timedelta(days=10),
        )

    def test_should_pass_when_executed_at_after_pre_commit_at(self) -> None:
        """结论: executed_at > pre_commit_at → 合法。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        executed_at = pre_commit_at + timedelta(hours=2)

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=executed_at,
            result_pct_after_7d=None,
            result_pct_after_30d=None,
            retrospective_notes=None,
            now=pre_commit_at + timedelta(days=10),
        )

    def test_should_pass_when_executed_at_is_none(self) -> None:
        """结论: executed_at 为 None → 合法（hold/wait 决策不填 R11）。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=None,
            result_pct_after_7d=None,
            result_pct_after_30d=None,
            retrospective_notes=None,
            now=pre_commit_at + timedelta(days=10),
        )


class TestResult7dConstraint:
    """result_pct_after_7d 仅在决策 7 天后允许填。"""

    def test_should_raise_when_result_7d_filled_before_7_days(self) -> None:
        """结论: 决策后不到 7 天填 result_pct_after_7d → PostMortemValidationError。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        # 现在是第 3 天（仅过了 3 天）
        now = pre_commit_at + timedelta(days=3)

        with pytest.raises(PostMortemValidationError, match="result_pct_after_7d"):
            svc.validate(
                pre_commit_at=pre_commit_at,
                executed_at=None,
                result_pct_after_7d=5.2,  # 填了 7d 数据
                result_pct_after_30d=None,
                retrospective_notes=None,
                now=now,
            )

    def test_should_raise_when_result_7d_filled_at_exactly_6_days(self) -> None:
        """结论: 第 6 天填 result_pct_after_7d → 不允许（< 7 天）。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        now = pre_commit_at + timedelta(days=6, hours=23, minutes=59)

        with pytest.raises(PostMortemValidationError, match="result_pct_after_7d"):
            svc.validate(
                pre_commit_at=pre_commit_at,
                executed_at=None,
                result_pct_after_7d=3.1,
                result_pct_after_30d=None,
                retrospective_notes=None,
                now=now,
            )

    def test_should_pass_when_result_7d_filled_after_7_days(self) -> None:
        """结论: 决策后恰好 7 天 → 允许填 result_pct_after_7d。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        now = pre_commit_at + timedelta(days=7)

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=None,
            result_pct_after_7d=5.2,
            result_pct_after_30d=None,
            retrospective_notes=None,
            now=now,
        )

    def test_should_pass_when_result_7d_is_none_before_7_days(self) -> None:
        """结论: 7 天内不填 result_pct_after_7d → 合法（不填是允许的）。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        now = pre_commit_at + timedelta(days=3)

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=None,
            result_pct_after_7d=None,  # 不填
            result_pct_after_30d=None,
            retrospective_notes="观察中",
            now=now,
        )

    def test_should_pass_when_only_notes_filled_before_7_days(self) -> None:
        """结论: 只填 retrospective_notes（不填 7d/30d 数据）→ 合法。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        now = pre_commit_at + timedelta(days=1)

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=None,
            result_pct_after_7d=None,
            result_pct_after_30d=None,
            retrospective_notes="复盘笔记",
            now=now,
        )


class TestHoldWaitScenario:
    """R11: hold/wait 决策允许 post_mortem（executed_at 留空）。"""

    def test_should_pass_when_hold_decision_fills_notes_only(self) -> None:
        """结论: hold 决策填 retrospective_notes 不填 executed_at → 合法 (R11)。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        now = pre_commit_at + timedelta(days=14)

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=None,          # hold → 无执行时间
            result_pct_after_7d=1.5,   # 7天后填收益
            result_pct_after_30d=None,
            retrospective_notes="持有观察，基本面未变化",
            now=now,
        )

    def test_should_pass_when_all_fields_none(self) -> None:
        """结论: 全空回填 → 合法（仅触发保存，不含任何数据）。"""
        svc = PostMortemService()
        pre_commit_at = datetime(2026, 4, 20, 10, 0, 0, tzinfo=UTC)
        now = pre_commit_at + timedelta(days=30)

        # 不应抛出异常
        svc.validate(
            pre_commit_at=pre_commit_at,
            executed_at=None,
            result_pct_after_7d=None,
            result_pct_after_30d=None,
            retrospective_notes=None,
            now=now,
        )
