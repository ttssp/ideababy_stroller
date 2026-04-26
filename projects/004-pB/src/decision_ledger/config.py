"""
配置加载 — T001
结论: 用 pydantic-settings 从 .env 加载配置，缺失关键变量 fail-fast
细节:
  - ANTHROPIC_API_KEY 和 TELEGRAM_BOT_TOKEN 必填，空值即 ConfigError
  - DECISION_LEDGER_HOME 默认 ~/decision_ledger
  - DECISION_LEDGER_TEST_MODE 默认 "strict"（架构不变量 #15）
  - 模块级 _settings 单例，避免重复加载
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigError(RuntimeError):
    """配置校验失败的专用异常，调用方可精确 catch。"""


class Settings(BaseSettings):
    """系统配置模型 — 仅在此处定义所有 env var。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # 未知字段忽略，避免 CI / 本地 env 差异导致校验失败
        extra="ignore",
    )

    # ── 必填 ──────────────────────────────────────────────
    anthropic_api_key: Annotated[str, Field(min_length=1)] = ""
    telegram_bot_token: Annotated[str, Field(min_length=1)] = ""

    # ── 可选，有合理默认 ───────────────────────────────────
    decision_ledger_home: Path = Field(
        default_factory=lambda: Path("~/decision_ledger").expanduser()
    )

    # strict mode 控制（架构不变量 #15: CI 默认 strict）
    decision_ledger_test_mode: str = Field(
        default="strict",
        alias="DECISION_LEDGER_TEST_MODE",
    )

    @field_validator("anthropic_api_key", mode="before")
    @classmethod
    def _validate_anthropic_key(cls, v: object) -> object:
        """结论: 禁止空 API key — 防止 API 调用时才爆炸。"""
        if not v or str(v).strip() == "":
            raise ValueError("ANTHROPIC_API_KEY 不能为空")
        return v

    @field_validator("telegram_bot_token", mode="before")
    @classmethod
    def _validate_telegram_token(cls, v: object) -> object:
        """结论: 禁止空 Token — Telegram bot 启动即需要。"""
        if not v or str(v).strip() == "":
            raise ValueError("TELEGRAM_BOT_TOKEN 不能为空")
        return v


def load_settings() -> Settings:
    """加载并校验配置，失败时抛出 ConfigError。

    结论: 调用方永远只调这个函数，不直接实例化 Settings。
    细节: ValidationError 被包成 ConfigError，统一错误面。
    """
    from pydantic import ValidationError  # 延迟 import 避免循环

    # 从 env 读取，支持空字符串触发 validator 失败
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")

    try:
        settings = Settings(
            anthropic_api_key=anthropic_key,
            telegram_bot_token=telegram_token,
        )
    except ValidationError as exc:
        # 提取第一条错误信息，给调用方友好提示
        first_err = exc.errors()[0]
        field = first_err.get("loc", ("unknown",))[0]
        msg = first_err.get("msg", str(exc))
        raise ConfigError(f"配置校验失败 [{field}]: {msg}") from exc

    return settings
