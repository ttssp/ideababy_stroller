"""
bot.py — T017 Telegram bot 主类
结论: DecisionLedgerBot 封装 python-telegram-bot v21 Application，提供:
  - is_allowed_chat(): 白名单验证 (compliance §3.2 + LEG-2)
  - send_alert(): 发送告警消息给白名单 chat (T020 接口)
  - push_event(): 发送 event 触发 push（v0.1 被动触发，non-goals A1）
  - start_polling(): 启动 long-polling（作为 asyncio task 注册到 plugin registry）
细节:
  - pool=None 时 graceful 降级（测试模式）
  - _application=None 时 send_alert/push_event 记录 warning 不抛出
  - 通过 register_startup_task 注册到 main.py plugin registry，不修改 main.py
  - long-polling 网络断开后自动重连 ≤ 1 min (SLA §1.1, python-telegram-bot 内置)
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any

from decision_ledger.plugin import register_startup_task

if TYPE_CHECKING:
    from decision_ledger.domain.alert import Alert
    from decision_ledger.repository.base import AsyncConnectionPool

logger = logging.getLogger(__name__)


class DecisionLedgerBot:
    """Telegram bot 主类 — long-polling + send_alert + push_event。

    结论: 封装 Application，独立管理生命周期，通过 plugin registry 注入。
    细节:
      - token: TELEGRAM_BOT_TOKEN env var
      - allowed_chat_id: TELEGRAM_CHAT_ID env var（单白名单）
      - pool: AsyncConnectionPool（rate_limiter 使用）
    """

    def __init__(
        self,
        token: str,
        allowed_chat_id: str,
        pool: AsyncConnectionPool | None,
    ) -> None:
        self._token = token
        self._allowed_chat_id = allowed_chat_id
        self._pool = pool
        self._application: Any | None = None  # telegram.ext.Application，启动后设置

    # ── 白名单验证 ────────────────────────────────────────────────────────────
    def is_allowed_chat(self, chat_id: str) -> bool:
        """检查 chat_id 是否在白名单内（compliance §3.2 + LEG-2）。

        结论: 字符串精确匹配，非白名单直接拒绝，不做模糊匹配。
        """
        return str(chat_id) == str(self._allowed_chat_id)

    # ── T020 接口 send_alert() ────────────────────────────────────────────────
    async def send_alert(self, alert: Alert) -> None:
        """发送告警消息给白名单 chat (T020 调用接口)。

        结论: application 未初始化时 graceful 降级（log warning）。
        细节:
          - 消息格式: [{severity}] {alert_type}: {body}
          - 失败不抛出（OP-3 mitigation，告警系统不应因推送失败崩溃）
        """
        if self._application is None:
            logger.warning(
                "send_alert: application 未初始化，告警未推送 | alert_id=%s",
                alert.alert_id,
            )
            return

        text = f"[{alert.severity.upper()}] {alert.alert_type}: {alert.body}"
        try:
            await self._application.bot.send_message(
                chat_id=self._allowed_chat_id,
                text=text,
            )
            logger.info("send_alert: 推送成功 | alert_id=%s", alert.alert_id)
        except Exception:
            logger.exception("send_alert: 推送失败 | alert_id=%s", alert.alert_id)

    # ── event push 接口 ───────────────────────────────────────────────────────
    async def push_event(
        self,
        payload: dict[str, Any],
        reference_time: Any | None = None,
    ) -> bool:
        """发送 event 触发 push（v0.1 被动触发）。

        结论: 先过 rate_limiter，再推送到白名单 chat。
        细节:
          - payload: {"ticker": "AAPL", "event_type": "earnings", "market": "US"}
          - 未过 rate_limit 返回 False（不推送）
          - application 未初始化时 graceful log
        """
        ticker = payload.get("ticker", "UNKNOWN")
        market = payload.get("market", "US")
        event_type = payload.get("event_type", "event")

        # rate limit 检查
        if self._pool is not None:
            from decision_ledger.telegram.rate_limiter import RateLimiter

            rl = RateLimiter(self._pool)
            kwargs: dict[str, Any] = {"push_type": "event"}
            if reference_time is not None:
                kwargs["reference_time"] = reference_time
            allowed = await rl.try_push(self._allowed_chat_id, **kwargs)
            if not allowed:
                logger.info("push_event: rate limit 超限，跳过推送 | ticker=%s", ticker)
                return False

        if self._application is None:
            logger.warning("push_event: application 未初始化 | ticker=%s", ticker)
            return False

        # per-market session 检查
        from decision_ledger.telegram.market_session import is_in_session

        if not is_in_session(market):
            logger.info(
                "push_event: %s 市场当前不在 session 内，跳过推送 | ticker=%s",
                market,
                ticker,
            )
            return False

        text = f"Event 提醒 [{event_type}] — {ticker} ({market})"
        try:
            await self._application.bot.send_message(
                chat_id=self._allowed_chat_id,
                text=text,
            )
            logger.info("push_event: 推送成功 | ticker=%s", ticker)
            return True
        except Exception:
            logger.exception("push_event: 推送失败 | ticker=%s", ticker)
            return False

    # ── 周报 push（T014 scheduler 触发）─────────────────────────────────────
    async def push_weekly_review(
        self,
        week_id: str,
        reference_time: Any | None = None,
    ) -> bool:
        """推送周度 review 摘要（由 T014 scheduler 触发）。

        结论: 先过 rate_limiter，再调 WeeklyReviewService 生成内容推送。
        """
        # rate limit 检查
        if self._pool is not None:
            from decision_ledger.telegram.rate_limiter import RateLimiter

            rl = RateLimiter(self._pool)
            kwargs: dict[str, Any] = {"push_type": "weekly"}
            if reference_time is not None:
                kwargs["reference_time"] = reference_time
            allowed = await rl.try_push(self._allowed_chat_id, **kwargs)
            if not allowed:
                logger.info(
                    "push_weekly_review: rate limit 超限，跳过推送 | week_id=%s",
                    week_id,
                )
                return False

        if self._application is None:
            logger.warning("push_weekly_review: application 未初始化 | week_id=%s", week_id)
            return False

        if self._pool is None:
            logger.warning("push_weekly_review: pool 未初始化，无法生成周报 | week_id=%s", week_id)
            return False

        try:
            from decision_ledger.services.weekly_review_service import WeeklyReviewService
            from decision_ledger.telegram.handlers import _format_weekly_summary

            service = WeeklyReviewService(pool=self._pool, llm_client=None)
            data = await service.generate(week_id)
            text = _format_weekly_summary(week_id, data)
            await self._application.bot.send_message(
                chat_id=self._allowed_chat_id,
                text=text,
            )
            logger.info("push_weekly_review: 推送成功 | week_id=%s", week_id)
            return True
        except Exception:
            logger.exception("push_weekly_review: 推送失败 | week_id=%s", week_id)
            return False

    # ── long-polling 启动 ──────────────────────────────────────────────────────
    async def start_polling(self) -> None:
        """启动 long-polling（作为 asyncio task 由 plugin registry 管理）。

        结论: 构建 Application，注册 handlers，启动 polling。
        细节:
          - 自动重连：python-telegram-bot v21 内置，断线重连 ≤ 1 min (SLA §1.1)
          - 使用 run_polling() 替代旧版 updater（v21 Application 模式）
          - 任何初始化异常 log 后不抛出（防止 main 崩溃）
        """
        try:
            import asyncio

            from telegram.ext import (
                Application,
                CommandHandler,
            )

            from decision_ledger.telegram.handlers import (
                handle_help,
                handle_start,
                handle_ticker,
                handle_weekly,
            )

            builder = Application.builder().token(self._token)
            application = builder.build()

            # 注入 bot_instance 和 pool 到 bot_data
            application.bot_data["bot_instance"] = self
            application.bot_data["pool"] = self._pool

            # 注册 command handlers
            application.add_handler(CommandHandler("start", handle_start))
            application.add_handler(CommandHandler("help", handle_help))
            application.add_handler(CommandHandler("weekly", handle_weekly))
            application.add_handler(CommandHandler("ticker", handle_ticker))

            self._application = application
            logger.info(
                "Telegram bot 启动 long-polling | allowed_chat_id=%s",
                self._allowed_chat_id,
            )

            # 初始化 + 开始 polling (阻塞直到取消)
            await application.initialize()
            await application.start()
            await application.updater.start_polling(  # type: ignore[union-attr]
                drop_pending_updates=True,
            )

            # 等待取消信号（asyncio task 被 cancel 时退出）
            try:
                await asyncio.get_event_loop().create_future()  # 永远等待
            except asyncio.CancelledError:
                logger.info("Telegram bot polling 收到取消信号，正在停止...")

        except Exception:
            logger.exception("Telegram bot start_polling 异常")
        finally:
            if self._application is not None:
                try:
                    await self._application.updater.stop()
                    await self._application.stop()
                    await self._application.shutdown()
                    logger.info("Telegram bot 已停止")
                except Exception:
                    logger.exception("Telegram bot 停止时异常")


# ── Plugin registry 注册（模块导入副作用）───────────────────────────────────
# 结论: 延迟初始化——实际 bot 实例在 main.py 启动时由 _create_bot_startup_task 创建
# 细节: 不在模块加载时实例化 Bot（需要 env var），而是注册一个 factory


def _create_bot_startup_task() -> Any:
    """创建并注册 bot long-polling startup task。

    结论: 从 env var 读取配置，构建 DecisionLedgerBot，返回 start_polling coroutine。
    """

    async def _bot_startup() -> None:
        """Bot 启动任务（由 main.py lifespan 执行）。"""
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

        if not token or not chat_id:
            logger.warning(
                "Telegram bot 未配置 (TELEGRAM_BOT_TOKEN=%s, TELEGRAM_CHAT_ID=%s)，跳过启动",
                bool(token),
                bool(chat_id),
            )
            return

        # pool 从全局 app state 获取（若已初始化）
        pool = None
        try:
            from decision_ledger.repository.base import AsyncConnectionPool

            db_path = os.environ.get("DECISION_LEDGER_DB_URL", "")
            if db_path.startswith("sqlite:///"):
                db_path = db_path[len("sqlite:///"):]
            if db_path:
                pool = AsyncConnectionPool(db_path)
                await pool.initialize()
        except Exception:
            logger.exception("Telegram bot: pool 初始化失败，rate_limiter 将跳过 DB 检查")

        bot = DecisionLedgerBot(
            token=token,
            allowed_chat_id=chat_id,
            pool=pool,
        )
        await bot.start_polling()

    return _bot_startup


register_startup_task(_create_bot_startup_task())
