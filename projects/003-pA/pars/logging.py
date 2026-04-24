"""
pars.logging — 统一 logging 配置层（stdlib，不引入 structlog）。

结论：JSON Lines 格式输出到 stderr，stdout 保留给 `claude -p --output-format stream-json`
      的 parser（T008）使用，避免污染 stdout 流解析。

使用方式：
    # CLI 启动时调用一次
    from pars.logging import configure_root
    configure_root()

    # 各模块中
    from pars.logging import get_logger
    logger = get_logger(__name__)
    logger.info("run started", extra={"run_id": run_id})

Env vars：
    PARS_LOG_LEVEL : 日志级别，默认 INFO（支持 DEBUG/INFO/WARNING/ERROR/CRITICAL）
"""

from __future__ import annotations

import json
import logging
import os
import sys
import traceback
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# JSON Formatter
# ---------------------------------------------------------------------------

class _JsonFormatter(logging.Formatter):
    """将 LogRecord 序列化为单行 JSON，输出到 stderr。

    输出字段（固定顺序）：
    - ts      : ISO 8601 UTC 时间戳
    - level   : 日志级别（INFO/WARNING/...）
    - logger  : logger 名称
    - msg     : 消息文本
    - extra   : LogRecord 上的额外字段（由调用方通过 extra={} 传入）
    - exc     : 异常 traceback（若有）
    """

    # 标准 LogRecord 自带的字段，不重复塞进 extra
    _BUILTIN_ATTRS: frozenset[str] = frozenset({
        "args", "created", "exc_info", "exc_text", "filename",
        "funcName", "levelname", "levelno", "lineno", "message",
        "module", "msecs", "msg", "name", "pathname", "process",
        "processName", "relativeCreated", "stack_info", "taskName",
        "thread", "threadName",
    })

    def format(self, record: logging.LogRecord) -> str:
        # 基础消息（安全处理 args 插值异常）
        try:
            message = record.getMessage()
        except Exception:
            message = str(record.msg)

        entry: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": message,
        }

        # 额外字段（调用方 extra={}）
        extras: dict[str, Any] = {
            k: v for k, v in record.__dict__.items()
            if k not in self._BUILTIN_ATTRS
        }
        if extras:
            entry["extra"] = extras

        # 异常信息
        if record.exc_info:
            entry["exc"] = self.formatException(record.exc_info)

        return json.dumps(entry, ensure_ascii=False, default=str)


# ---------------------------------------------------------------------------
# Root logger 配置
# ---------------------------------------------------------------------------

_ROOT_CONFIGURED = False


def configure_root(
    *,
    level: str | None = None,
    force: bool = False,
) -> None:
    """配置 root logger 为 JSON Lines 输出到 stderr。

    参数：
        level  : 日志级别字符串（覆盖 PARS_LOG_LEVEL env var）。
                 优先级：参数 > PARS_LOG_LEVEL env var > INFO（默认）。
        force  : 若 True，即使已配置也重新配置（用于测试）。

    调用约定：
        在 CLI 入口（pars.cli.main）调用一次；不在 module 级自动调用
        （库 import 不应改变 caller 的 logging 配置）。
    """
    global _ROOT_CONFIGURED
    if _ROOT_CONFIGURED and not force:
        return

    # 确定级别
    effective_level_str = (
        level
        or os.environ.get("PARS_LOG_LEVEL", "INFO")
    ).upper()
    effective_level = getattr(logging, effective_level_str, logging.INFO)

    # 创建 stderr handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_JsonFormatter())
    handler.setLevel(effective_level)

    # 配置 root logger
    root = logging.getLogger()
    root.setLevel(effective_level)
    # 清除既有 handler（避免重复输出）
    root.handlers.clear()
    root.addHandler(handler)

    _ROOT_CONFIGURED = True


# ---------------------------------------------------------------------------
# 公开 helper
# ---------------------------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """返回命名 logger。

    若 root logger 尚未配置（如直接 import 而未调用 configure_root），
    自动附加一个最小 stderr handler，确保消息不丢失（告警级别打一次警告）。

    典型用法：
        logger = get_logger(__name__)
        logger.info("started")
        logger.warning("slow", extra={"elapsed_ms": 1500})
    """
    logger = logging.getLogger(name)

    # 若 root 未配置且 root 无任何 handler，临时注入一个最小配置
    # 避免「No handlers could be found」静默丢失日志
    root = logging.getLogger()
    if not root.handlers:
        _bootstrap_stderr_handler(root)

    return logger


def _bootstrap_stderr_handler(root: logging.Logger) -> None:
    """为 root logger 注入最小 stderr JSON handler（bootstrap 场景）。

    不设置 _ROOT_CONFIGURED，让 configure_root() 之后能完整替换。
    """
    level_str = os.environ.get("PARS_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_JsonFormatter())
    handler.setLevel(level)

    root.setLevel(level)
    root.addHandler(handler)
