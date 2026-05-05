"""
PostMortemService — T018
结论: post-mortem 回填校验服务，执行时间约束检查
细节:
  - validate(): 校验 4 字段的时间约束
    * executed_at >= pre_commit_at (若填写)
    * result_pct_after_7d 仅在决策 7 天后允许填（避免假数据）
  - R11: executed_at 留空允许（hold/wait 不动允许复盘）
  - 不含 nudge 逻辑（R3 砍掉, v0.2+）
"""

from __future__ import annotations

from datetime import UTC, datetime


class PostMortemValidationError(ValueError):
    """post-mortem 校验失败，对应 HTTP 422。

    结论: 继承 ValueError 便于上层路由 catch 后返回 422。
    """

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"[{field}] {message}")


class PostMortemService:
    """post-mortem 回填校验服务。

    结论: 无状态纯校验，不含 DB 操作（由路由层持 repo）。
    """

    def validate(
        self,
        *,
        pre_commit_at: datetime,
        executed_at: datetime | None,
        result_pct_after_7d: float | None,
        result_pct_after_30d: float | None,
        retrospective_notes: str | None,
        now: datetime | None = None,
    ) -> None:
        """校验 post-mortem 回填数据的时间约束。

        参数:
          pre_commit_at: 决策提交时间（来自 Decision 域对象）
          executed_at: 实际执行时间（hold/wait 可为 None）
          result_pct_after_7d: 7 天后收益百分比（仅 7 天后可填）
          result_pct_after_30d: 30 天后收益百分比（无时间限制）
          retrospective_notes: 复盘笔记（无时间限制）
          now: 当前时间（默认 datetime.now(UTC)，测试可注入）

        抛出:
          PostMortemValidationError: 任一约束违反时
        """
        if now is None:
            now = datetime.now(tz=UTC)

        # 约束1: executed_at >= pre_commit_at (若填写)
        if executed_at is not None:
            # 确保时区一致比较
            exec_at = self._ensure_utc(executed_at)
            pre_at = self._ensure_utc(pre_commit_at)
            if exec_at < pre_at:
                raise PostMortemValidationError(
                    field="executed_at",
                    message=(
                        f"executed_at ({exec_at.isoformat()}) 不能早于 "
                        f"pre_commit_at ({pre_at.isoformat()})"
                    ),
                )

        # 约束2: result_pct_after_7d 仅在决策 7 天后允许填
        if result_pct_after_7d is not None:
            pre_at = self._ensure_utc(pre_commit_at)
            now_utc = self._ensure_utc(now)
            days_elapsed = (now_utc - pre_at).total_seconds() / 86400.0
            if days_elapsed < 7.0:
                raise PostMortemValidationError(
                    field="result_pct_after_7d",
                    message=(
                        f"result_pct_after_7d 仅在决策 7 天后允许填写，"
                        f"当前仅过了 {days_elapsed:.1f} 天"
                    ),
                )

    @staticmethod
    def _ensure_utc(dt: datetime) -> datetime:
        """确保 datetime 有 UTC 时区信息。

        结论: naive datetime 默认视为 UTC（DB 存储约定）。
        """
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)
        return dt
