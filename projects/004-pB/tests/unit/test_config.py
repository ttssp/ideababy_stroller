"""
配置校验测试 — T001
结论: 缺失关键 env var 时必须 fail-fast 抛出 ConfigError
细节:
  - ANTHROPIC_API_KEY 缺失 → ConfigError
  - TELEGRAM_BOT_TOKEN 缺失 → ConfigError
  - 两者都有 → 正常加载
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


def _clear_decision_ledger_modules() -> None:
    """清除 sys.modules 中所有 decision_ledger 相关模块，强制下次 import 重新加载。"""
    for mod_name in list(sys.modules.keys()):
        if "decision_ledger" in mod_name:
            del sys.modules[mod_name]


def test_config_raises_when_anthropic_key_missing() -> None:
    """should raise ConfigError when ANTHROPIC_API_KEY is not set"""
    env_backup = {k: os.environ.pop(k, None) for k in ("ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN")}
    os.environ["TELEGRAM_BOT_TOKEN"] = "123:valid-token"
    os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        _clear_decision_ledger_modules()
        from decision_ledger.config import ConfigError, load_settings

        with pytest.raises(ConfigError):
            load_settings()
    finally:
        for k, v in env_backup.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)


def test_config_raises_when_telegram_token_missing() -> None:
    """should raise ConfigError when TELEGRAM_BOT_TOKEN is not set"""
    env_backup = {k: os.environ.pop(k, None) for k in ("ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN")}
    os.environ["ANTHROPIC_API_KEY"] = "sk-test-key"
    os.environ.pop("TELEGRAM_BOT_TOKEN", None)

    try:
        _clear_decision_ledger_modules()
        from decision_ledger.config import ConfigError, load_settings

        with pytest.raises(ConfigError):
            load_settings()
    finally:
        for k, v in env_backup.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)


def test_config_loads_successfully_when_env_set() -> None:
    """should return settings without error when both keys are provided"""
    env_backup = {
        k: os.environ.pop(k, None)
        for k in ("ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN", "DECISION_LEDGER_HOME")
    }
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"
    os.environ["TELEGRAM_BOT_TOKEN"] = "999:test-token"

    try:
        _clear_decision_ledger_modules()
        from decision_ledger.config import load_settings

        settings = load_settings()
        assert settings.anthropic_api_key == "sk-ant-test"
        assert settings.telegram_bot_token == "999:test-token"
    finally:
        for k, v in env_backup.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)


def test_config_default_home() -> None:
    """should use ~/decision_ledger as default DECISION_LEDGER_HOME"""
    env_backup = {
        k: os.environ.pop(k, None)
        for k in ("ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN", "DECISION_LEDGER_HOME")
    }
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test2"
    os.environ["TELEGRAM_BOT_TOKEN"] = "888:test-token"
    os.environ.pop("DECISION_LEDGER_HOME", None)

    try:
        _clear_decision_ledger_modules()
        from decision_ledger.config import load_settings

        settings = load_settings()
        assert settings.decision_ledger_home == Path("~/decision_ledger").expanduser()
    finally:
        for k, v in env_backup.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)
