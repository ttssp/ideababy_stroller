"""
handlers.py — T017 Telegram command handlers
结论: 注册 /start /weekly /ticker /help 四个只读命令 handler
细节:
  - 所有 handler 前置白名单检查（compliance §3.2 + LEG-2）：非白名单 chat_id 直接 ignore
  - /weekly: 调 WeeklyReviewService 获取当周摘要，推送给用户
  - /ticker <SYMBOL>: 查最新 ConflictReport 生成叙事版，推送给用户
  - /start /help: 返回命令列表说明
  - handler 全部 async，符合 python-telegram-bot v21 Application 模式
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from telegram import Update
from telegram.ext import ContextTypes

if TYPE_CHECKING:
    from decision_ledger.telegram.bot import DecisionLedgerBot

logger = logging.getLogger(__name__)

# ── 帮助文本 ──────────────────────────────────────────────────────────────────
_HELP_TEXT = (
    "决策账本 Bot 命令列表:\n"
    "/start — 启动并显示帮助\n"
    "/weekly — 获取本周投资决策摘要\n"
    "/ticker <SYMBOL> — 查看指定 ticker 的三路冲突叙事 (例: /ticker AAPL)\n"
    "/help — 显示帮助信息\n"
    "\n"
    "提示: 本 bot 仅供只读查询，决策录入请使用 Web 界面。"
)


def _get_chat_id(update: Update) -> str | None:
    """安全获取 chat_id 字符串，若无效返回 None。"""
    if update.effective_chat is None:
        return None
    return str(update.effective_chat.id)


def _is_allowed(update: Update, bot: DecisionLedgerBot) -> bool:
    """检查 chat_id 是否在白名单内（compliance §3.2 + LEG-2）。"""
    chat_id = _get_chat_id(update)
    if chat_id is None:
        return False
    return bot.is_allowed_chat(chat_id)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /start 命令 — 显示帮助信息。

    结论: 前置白名单检查，非白名单直接 ignore（不回复）。
    """
    bot_instance: DecisionLedgerBot | None = context.application.bot_data.get("bot_instance")
    if bot_instance is None or not _is_allowed(update, bot_instance):
        logger.info("handle_start: 非白名单 chat_id，ignore | chat=%s", _get_chat_id(update))
        return

    if update.message is None:
        return
    await update.message.reply_text(_HELP_TEXT)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /help 命令 — 显示命令列表。

    结论: 与 /start 相同内容，前置白名单检查。
    """
    bot_instance: DecisionLedgerBot | None = context.application.bot_data.get("bot_instance")
    if bot_instance is None or not _is_allowed(update, bot_instance):
        logger.info("handle_help: 非白名单 chat_id，ignore | chat=%s", _get_chat_id(update))
        return

    if update.message is None:
        return
    await update.message.reply_text(_HELP_TEXT)


async def handle_weekly(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /weekly 命令 — 返回本周决策摘要。

    结论: 前置白名单检查，调 WeeklyReviewService.generate() 生成摘要文本。
    细节:
      - pool / llm_client 从 bot_data 获取（启动时注入）
      - 失败时返回友好错误提示，不抛出（OP-3 mitigation）
    """
    bot_instance: DecisionLedgerBot | None = context.application.bot_data.get("bot_instance")
    if bot_instance is None or not _is_allowed(update, bot_instance):
        logger.info("handle_weekly: 非白名单 chat_id，ignore | chat=%s", _get_chat_id(update))
        return

    if update.message is None:
        return

    pool: Any = context.application.bot_data.get("pool")
    if pool is None:
        await update.message.reply_text("系统初始化中，请稍后重试。")
        return

    try:
        from decision_ledger.services.weekly_review_service import WeeklyReviewService

        service = WeeklyReviewService(pool=pool, llm_client=None)
        now = datetime.now(tz=UTC)
        week_id = now.strftime("%G-W%V")
        data = await service.generate(week_id)

        text = _format_weekly_summary(week_id, data)
        await update.message.reply_text(text)
    except Exception:
        logger.exception("handle_weekly: 生成周报失败")
        await update.message.reply_text("生成周报时出错，请稍后重试。")


async def handle_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /ticker <SYMBOL> 命令 — 返回 ticker 的三路冲突叙事。

    结论: 前置白名单检查，查最新 ConflictReport 生成叙事版。
    细节:
      - 参数解析失败时返回用法提示
      - 无 ConflictReport 时返回提示
    """
    bot_instance: DecisionLedgerBot | None = context.application.bot_data.get("bot_instance")
    if bot_instance is None or not _is_allowed(update, bot_instance):
        logger.info("handle_ticker: 非白名单 chat_id，ignore | chat=%s", _get_chat_id(update))
        return

    if update.message is None:
        return

    # 解析 ticker symbol
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("用法: /ticker <SYMBOL>  (例: /ticker AAPL)")
        return

    symbol = context.args[0].upper()
    pool: Any = context.application.bot_data.get("pool")

    if pool is None:
        await update.message.reply_text("系统初始化中，请稍后重试。")
        return

    try:
        from decision_ledger.repository.conflict_repo import ConflictRepository
        from decision_ledger.telegram.conflict_narrative import build_narrative

        repo = ConflictRepository(pool)
        # 获取最近 20 条冲突报告，按 ticker 过滤取最新一条
        recent = await repo.list_recent(limit=20)
        # 按 signals 中包含该 ticker 的 report 过滤
        matching = [
            r for r in recent
            if any(s.ticker.upper() == symbol for s in r.signals)
        ]

        if not matching:
            await update.message.reply_text(f"{symbol} 暂无冲突报告数据。")
            return

        report = matching[0]  # 最新一条（list_recent 已按 created_at DESC 排序）
        narrative = build_narrative(report)
        await update.message.reply_text(f"三路冲突叙事 — {symbol}:\n\n{narrative}")
    except Exception:
        logger.exception("handle_ticker: 查询 %s 冲突报告失败", symbol)
        await update.message.reply_text(f"查询 {symbol} 时出错，请稍后重试。")


def _format_weekly_summary(week_id: str, data: dict[str, Any]) -> str:
    """将周报数据格式化为 Telegram 可发送的文本。

    结论: 简洁格式，包含总决策数 + hold/wait 占比 + LLM 摘要（若有）。
    """
    total = data.get("total", 0)
    hold_wait_count = data.get("hold_wait_count", 0)
    hold_wait_ratio = data.get("hold_wait_ratio", 0.0)
    llm_summary = data.get("llm_summary")

    lines = [
        f"本周决策周报 ({week_id})",
        f"总决策数: {total}",
        f"不动专区 (hold/wait): {hold_wait_count} ({hold_wait_ratio:.1%})",
    ]

    if llm_summary:
        lines.append(f"\n摘要: {llm_summary}")

    return "\n".join(lines)
