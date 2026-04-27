"""
conflict_narrative.py — T017 D3 / D22
结论: 把 ConflictReport → 3 行叙事版 (Telegram 用)，顺序按 rendered_order_seed 随机 (R2 D22)
细节:
  - build_narrative(): 返回 3 行字符串，每行对应一个 signal
  - 顺序由 rendered_order_seed % 3! (6 种) 决定，不固定 advisor 第一 (R10 约束)
  - 每行格式: "[source_id] ({direction} {confidence:.0%}): {rationale_plain}"
  - divergence_root_cause 附在末尾作第 4 行注释（仅在 has_divergence=True 时）
  - 输出为纯文本，供 Telegram send_message 直接使用
"""

from __future__ import annotations

from itertools import permutations

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.strategy_signal import StrategySignal

# ── 6 种排列顺序 (3! = 6) ──────────────────────────────────────────────────────
# 结论: 预计算所有排列，用 rendered_order_seed % 6 取下标，确保顺序确定性
_THREE_PERMUTATIONS: list[tuple[int, int, int]] = [
    (p[0], p[1], p[2]) for p in permutations(range(3))
]
assert len(_THREE_PERMUTATIONS) == 6, "排列数应为 6"


def _format_signal_line(signal: StrategySignal) -> str:
    """将单个 StrategySignal 格式化为一行叙事文本。

    结论: 格式 "[source_id] ({direction} {confidence:.0%}): {rationale_plain}"
    细节: confidence 用百分比显示，保持可读性
    """
    return (
        f"[{signal.source_id}] ({signal.direction} {signal.confidence:.0%}): "
        f"{signal.rationale_plain}"
    )


def build_narrative(report: ConflictReport) -> str:
    """构建 ConflictReport 的三行叙事版。

    结论: 顺序由 rendered_order_seed % 6 决定（R2 D22，不固定 advisor 第一）。
    细节:
      - signals 取前 3 条（不变量 #2 保证 ≥ 3）
      - has_divergence=True 时追加第 4 行根因注释
      - 返回 \n 分隔的字符串

    参数:
        report: ConflictReport 实例

    返回:
        3（或 4）行叙事字符串
    """
    signals = report.signals[:3]  # 取前 3 条
    perm_idx = report.rendered_order_seed % len(_THREE_PERMUTATIONS)
    order = _THREE_PERMUTATIONS[perm_idx]

    # 三路信号各一行，严格三行（D3 三列对应 Telegram 三行）
    lines: list[str] = [
        _format_signal_line(signals[order[0]]),
        _format_signal_line(signals[order[1]]),
        _format_signal_line(signals[order[2]]),
    ]

    # 有分歧时，根因追加在最后一行末尾（保持三行结构）
    if report.has_divergence and report.divergence_root_cause:
        lines[-1] = lines[-1] + f" | 分歧: {report.divergence_root_cause}"

    return "\n".join(lines)
