"""
MonthlyReviewService — T015 (R3 简化版)
结论: 月度 review 聚合服务，纯 SQL 聚合，不调 LLM (R3 cut)
细节:
  - generate(month_id): 聚合本月数据 → dict for template (R3: 无 LLM 调用)
    * month_id 格式: "YYYY-MM" (e.g. "2026-04")
    * SQL 聚合: decisions 按 status='committed' filter (R2: draft 不算)
  - 4 section 内容:
    (1) calibration: 校准证据 SQL 聚合
        - total_committed: 本月 committed 决策总数
        - inactive_count: hold+wait 不动决策数
        - inactive_ratio: 不动占比
        - would_have_acted_count: would_have_acted_without_agent=1 的决策数
    (2) matrix_snapshot: 错位矩阵月末快照 (复用 matrix_service)
    (3) risk_snapshot: 静态 4 行风险表 (OP-1/OP-2/TECH-2/O10)
    (4) benchmark_placeholder: 12 月对标 placeholder 文字 (Q1 mitigation)
  - R3 砍掉: LLM 摘要 / PNG 图表 / 自定义模板 / audience 参数
  - R2 M5: generate() 签名不含 audience 参数
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from decision_ledger.repository.base import AsyncConnectionPool

logger = logging.getLogger(__name__)

# ── 静态风险快照 (R3: 4 行静态文本, 无颜色) ──────────────────────────────────
# 结论: OP-1/OP-2/TECH-2/O10 的简短描述，不做颜色 class，不做动态更新
_STATIC_RISK_SNAPSHOT: list[dict[str, str]] = [
    {
        "id": "OP-1",
        "description": "过度交易风险: agent 可能推高决策频率，偏离纪律目标",
    },
    {
        "id": "OP-2",
        "description": "过度依赖风险: operator 对 AI 建议过度信赖，弱化主观判断",
    },
    {
        "id": "TECH-2",
        "description": "模型漂移风险: LLM 行为不稳定，建议质量可能退化",
    },
    {
        "id": "O10",
        "description": "告警疲劳风险: 频繁失败告警导致重要信号被忽略",
    },
]

# ── 月份 ID 转日期范围 ───────────────────────────────────────────────────────


def _month_id_to_date_range(month_id: str) -> tuple[str, str]:
    """将 YYYY-MM 格式转为月份的起止时间 ISO 字符串。

    结论: 月初 00:00:00 → 月末 23:59:59 (UTC)。
    细节:
      - 使用 datetime 构造月初/月末，适配 SQL BETWEEN 查询
      - 避免使用 calendar 模块，手动计算月末
    """
    year, month = map(int, month_id.split("-"))
    # 月初
    start = datetime(year, month, 1, 0, 0, 0, tzinfo=UTC)
    # 月末: 下个月月初减 1 秒
    if month == 12:
        next_month_start = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=UTC)
    else:
        next_month_start = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=UTC)

    from datetime import timedelta

    end = next_month_start - timedelta(seconds=1)

    return start.isoformat(), end.isoformat()


class MonthlyReviewService:
    """月度 review 聚合服务 — R3 简化版。

    结论: 纯 SQL 聚合，不调 LLM，generate 签名不含 audience (R2 M5)。
    细节:
      - 依赖 pool 直接执行 SQL，不走 Repository 层
      - 所有 4 section 数据在同一 generate() 调用中聚合完成
    """

    def __init__(
        self,
        pool: AsyncConnectionPool,
    ) -> None:
        self._pool = pool

    async def generate(self, month_id: str) -> dict[str, Any]:
        """生成月度 review 数据字典（供模板渲染）。

        结论: 聚合 4 section 数据，纯 SQL，不调 LLM (R3 cut)。
        参数:
          month_id: "YYYY-MM" 格式 (e.g. "2026-04")
        返回: dict 含以下 key:
          - month_id: str
          - calibration: dict  (校准证据聚合)
          - matrix_snapshot: list  (错位矩阵月末快照行列表)
          - risk_snapshot: list  (静态 4 行风险表)
          - benchmark_placeholder: str  (12 月对标 placeholder 文字)
        """
        logger.info("monthly_review generate 开始 | month_id=%s", month_id)
        start_iso, end_iso = _month_id_to_date_range(month_id)

        # ── Section 1: 校准证据聚合 ────────────────────────────────────────────
        calibration = await self._aggregate_calibration(start_iso, end_iso)

        # ── Section 2: 错位矩阵月末快照 ───────────────────────────────────────
        matrix_snapshot = await self._get_matrix_snapshot()

        # ── Section 3: 静态风险快照 ───────────────────────────────────────────
        risk_snapshot = list(_STATIC_RISK_SNAPSHOT)

        # ── Section 4: 12 月对标 placeholder ─────────────────────────────────
        month_count = await self._count_months_with_data(month_id)
        benchmark_placeholder = _build_benchmark_placeholder(month_count)

        return {
            "month_id": month_id,
            "calibration": calibration,
            "matrix_snapshot": matrix_snapshot,
            "risk_snapshot": risk_snapshot,
            "benchmark_placeholder": benchmark_placeholder,
        }

    # ── 私有方法 ──────────────────────────────────────────────────────────────

    async def _aggregate_calibration(
        self, start_iso: str, end_iso: str
    ) -> dict[str, Any]:
        """聚合本月校准证据 (committed decisions only, R2)。

        结论: 统计总数 / 不动占比 / would_have_acted count，只计 committed。
        """
        async with self._pool.connection() as conn:
            # 总 committed 决策数
            cursor = await conn.execute(
                """
                SELECT
                    COUNT(*) as total_committed,
                    SUM(
                        CASE WHEN action IN ('hold', 'wait') THEN 1 ELSE 0 END
                    ) as inactive_count,
                    SUM(
                        CASE WHEN would_have_acted_without_agent = 1 THEN 1 ELSE 0 END
                    ) as would_have_acted_count
                FROM decisions
                WHERE status = 'committed'
                  AND pre_commit_at >= ?
                  AND pre_commit_at <= ?
                """,
                (start_iso, end_iso),
            )
            row = await cursor.fetchone()

        if row is None:
            total_committed = 0
            inactive_count = 0
            would_have_acted_count = 0
        else:
            total_committed = int(row["total_committed"] or 0)
            inactive_count = int(row["inactive_count"] or 0)
            would_have_acted_count = int(row["would_have_acted_count"] or 0)

        inactive_ratio = (inactive_count / total_committed) if total_committed > 0 else 0.0

        return {
            "total_committed": total_committed,
            "inactive_count": inactive_count,
            "inactive_ratio": inactive_ratio,
            "would_have_acted_count": would_have_acted_count,
        }

    async def _get_matrix_snapshot(self) -> list[dict[str, Any]]:
        """获取错位矩阵月末快照 (复用 MatrixService 逻辑, 空 signals 快照)。

        结论: R3 简化版直接返回空 list (矩阵快照在 template 中通过 iframe 嵌入)。
        细节:
          - T011 矩阵 partial 已通过 template include 嵌入，此处不重复 build
          - 供 template 判断是否显示 "暂无快照数据" 占位文字
        """
        return []

    async def _count_months_with_data(self, current_month_id: str) -> int:
        """统计截至当前月份有决策数据的月份数 (Q1: 12 月对标样本量判断)。

        结论: 按 YYYY-MM 分组统计 committed 决策月份数。
        细节:
          - 使用 substr(pre_commit_at, 1, 7) 提取年月 (ISO 字符串前 7 位)
          - 只计 committed 决策所在月份 (R2 一致性)
        """
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT COUNT(DISTINCT substr(pre_commit_at, 1, 7)) as month_count
                FROM decisions
                WHERE status = 'committed'
                  AND substr(pre_commit_at, 1, 7) <= ?
                """,
                (current_month_id,),
            )
            row = await cursor.fetchone()

        if row is None or row["month_count"] is None:
            return 0
        return int(row["month_count"])


def _build_benchmark_placeholder(month_count: int) -> str:
    """构建 12 月对标 placeholder 文字 (Q1 mitigation)。

    结论: 样本不足 12 个月时, 显示"样本 N 个月，暂不出年化"而非误导性数字。
    细节:
      - Q1 默认假设: 12 个月以下不出年化对标
      - 精确数字等运营 12 个月后由 human 手算 (O9)
    """
    if month_count < 12:
        return (
            f"样本 {month_count} 个月，暂不出年化对标 (Q1: 需满 12 个月才出年化 alpha 估算)"
        )
    return (
        f"已积累 {month_count} 个月数据，年化对标请参阅运营报告 (O9: human 手算)"
    )
