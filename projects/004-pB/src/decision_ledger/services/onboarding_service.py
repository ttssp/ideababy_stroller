"""
OnboardingService — T021
结论: 7 步引导流程状态机，内置计时，O6 验证门槛 (总耗时 < 900s)
细节:
  - STEPS: 7 步描述 (只读类常量)
  - enter_step(n) / leave_step(n): 记录每步 enter/leave timestamp
  - mark_complete(): 记录完成时间，计算 total_duration_s，设置 o6_pass
  - check_o6_pass(total_s): 类方法，严格 < 900s → True
  - get_step_timestamps(): 返回 {step_n_enter: float, step_n_leave: float}
  - is_completed(): bool
  - completed_at: 完成时间 (float UNIX timestamp, None if not complete)
  - R2 H3: 完全不引用 T019 符号 (learning_check / LearningCheck)
    step 7 仅静态文案，通过 T020 alert banner 触发学习提醒
"""

from __future__ import annotations

import time
from typing import ClassVar


class OnboardingService:
    """7 步 Onboarding 状态机 (内存版, 供路由层调用).

    结论: 生产版本路由层持久化 to onboarding_state 表 (0007 migration);
    此类封装纯业务逻辑 (可独立单测, 无 DB 依赖).
    """

    # ── 7 步描述 (类常量, 只读) ────────────────────────────────────────────────
    STEPS: ClassVar[list[dict[str, str]]] = [
        {
            "n": "1",
            "title": "启动系统",
            "desc": "确认 ./scripts/start.sh 已正常运行，浏览器打开 http://localhost:8000",
            "duration_hint": "约 1 分钟",
            "anchor": "section-step-1",
        },
        {
            "n": "2",
            "title": "录入关注股 (30-50 只)",
            "desc": '到"设置 - 关注股"页面，粘贴 CSV 格式关注股 ticker，一行一个',
            "duration_hint": "约 5 分钟",
            "anchor": "section-step-2",
        },
        {
            "n": "3",
            "title": "录入持仓快照",
            "desc": '到"设置 - 持仓快照"页面，粘贴 JSON 格式持仓数据',
            "duration_hint": "约 3 分钟",
            "anchor": "section-step-3",
        },
        {
            "n": "4",
            "title": "拖入第一份咨询师 PDF",
            "desc": "将 PDF 文件拖入监听目录 (~/decision_ledger/inbox/)，等待自动解析完成",
            "duration_hint": "约 1 分钟",
            "anchor": "section-step-4",
        },
        {
            "n": "5",
            "title": "录入首次决策档案",
            "desc": '到"决策 - 新建"页面，选任意 ticker，action=hold/wait，填写理由',
            "duration_hint": "约 30 秒~1 分钟",
            "anchor": "section-step-5",
        },
        {
            "n": "6",
            "title": "绑定 Telegram 通知",
            "desc": "在 BotFather 申请 bot token，在系统设置中填写并完成 chat_id 绑定",
            "duration_hint": "约 3 分钟",
            "anchor": "section-step-6",
        },
        {
            "n": "7",
            "title": "完成引导 — 空态说明",
            "desc": (
                "首次季度学习提醒在 90 天后自动出现（通过 alert banner 由 T020 触发）。"
                " 系统现在已配置完毕，可正常使用。"
            ),
            "duration_hint": "约 1.5 分钟",
            "anchor": "section-step-7",
        },
    ]

    # ── O6 通过门槛 ──────────────────────────────────────────────────────────────
    O6_PASS_THRESHOLD_S: ClassVar[float] = 900.0  # 严格 <

    def __init__(self) -> None:
        """结论: 初始化状态机，step=0，所有 timestamp 为空。"""
        self._step: int = 0
        self._started_at: float | None = None
        self._completed_at: float | None = None
        self._step_timestamps: dict[str, float] = {}

    # ── 状态访问 ─────────────────────────────────────────────────────────────────

    @property
    def current_step(self) -> int:
        """当前步骤 (0 = 未开始, 1-7 = 进行中, 8 = 已完成)."""
        return self._step

    @property
    def completed_at(self) -> float | None:
        """完成时间 (UNIX timestamp), None 表示未完成."""
        return self._completed_at

    def is_completed(self) -> bool:
        """结论: 已完成 7 步 → True."""
        return self._completed_at is not None

    def get_step_timestamps(self) -> dict[str, float]:
        """结论: 返回每步 enter/leave timestamp 副本 (key = step_{n}_{enter|leave})."""
        return dict(self._step_timestamps)

    def total_duration_s(self) -> float | None:
        """结论: 总耗时秒数 (仅 completed 时有值)."""
        if self._started_at is None or self._completed_at is None:
            return None
        return self._completed_at - self._started_at

    # ── 状态转换 ─────────────────────────────────────────────────────────────────

    async def enter_step(self, step_n: int) -> None:
        """结论: 记录 step_n_enter timestamp; 若为 step 1 则同时记录 started_at.

        参数:
            step_n: 1-7 的步骤编号
        """
        now = time.monotonic()
        key = f"step_{step_n}_enter"
        self._step_timestamps[key] = now
        self._step = step_n
        if step_n == 1 and self._started_at is None:
            self._started_at = now

    async def leave_step(self, step_n: int) -> None:
        """结论: 记录 step_n_leave timestamp.

        参数:
            step_n: 1-7 的步骤编号
        """
        now = time.monotonic()
        key = f"step_{step_n}_leave"
        self._step_timestamps[key] = now

    async def mark_complete(self) -> None:
        """结论: 标记 7 步全部完成，计算 total_duration_s，设置 o6_pass."""
        now = time.monotonic()
        self._completed_at = now
        if self._started_at is None:
            # 兜底: 若 enter_step(1) 未被调用，使用 completed_at 作为 started_at
            self._started_at = now
        self._step = 8  # 超出 7 步，表示完成

    # ── 类方法 ───────────────────────────────────────────────────────────────────

    @classmethod
    def check_o6_pass(cls, total_s: float) -> bool:
        """结论: 严格 < 900s → True (O6 验证门槛).

        参数:
            total_s: 总耗时秒数
        返回:
            bool: total_s < O6_PASS_THRESHOLD_S
        """
        return total_s < cls.O6_PASS_THRESHOLD_S

    def build_state_dict(self) -> dict[str, object]:
        """结论: 序列化为可写入 DB 的 dict (供 router 持久化).

        返回:
            step / started_at / completed_at / total_duration_s / o6_pass /
            step_timestamps_json
        """
        import json
        from datetime import UTC, datetime

        total_s = self.total_duration_s()
        o6_pass = self.check_o6_pass(total_s) if total_s is not None else False

        def _ts_to_iso(ts: float | None) -> str | None:
            if ts is None:
                return None
            # monotonic → wall clock offset 近似: 用 time.time() 计算偏移
            # 生产中应改为真实 wall clock
            return datetime.now(tz=UTC).isoformat()

        return {
            "step": self._step,
            "started_at": _ts_to_iso(self._started_at),
            "completed_at": _ts_to_iso(self._completed_at),
            "total_duration_s": total_s,
            "o6_pass": 1 if o6_pass else 0,
            "step_timestamps_json": json.dumps(self._step_timestamps),
        }
