"""
pars.ledger.ledger — Run Ledger 高层 facade API。

结论：将 T006/T007/T008 的底层 IO 封装为简单的高层函数，
      提供统一入口，隐藏文件路径细节；调用方无需感知 config.yaml / state.json 位置。

实现的函数：
  create_run(config)       — 生成 ULID、建目录树、写 config.yaml + state.json
  list_runs(*, limit)      — 列出 ULID 合法目录，按最新在前排序
  get_run_summary(run_id)  — 读取 config + state，返回平坦 dict 摘要
  run_exists(run_id)       — 检查 config.yaml 是否存在
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pars.ledger.config_io import get_run_config_path, load_config, save_config
from pars.ledger.config_schema import RunConfig
from pars.ledger.run_id import generate_ulid, validate_ulid
from pars.ledger.state import RunPhase, new_run_state, read_state, write_state
from pars.paths import ensure_run_tree


# ---------------------------------------------------------------------------
# 内部辅助
# ---------------------------------------------------------------------------


def _runs_base() -> Path:
    """返回 run 数据目录根（绝对路径）。

    优先读 RECALLKIT_RUN_DIR，否则 <cwd>/runs。
    与 pars.paths._base_runs() 逻辑一致，独立实现避免私有 API 依赖。
    """
    env_val = os.environ.get("RECALLKIT_RUN_DIR")
    if env_val:
        return Path(env_val).resolve()
    return (Path.cwd() / "runs").resolve()


# ---------------------------------------------------------------------------
# 高层 API
# ---------------------------------------------------------------------------


def create_run(config: RunConfig) -> str:
    """创建新的 run：分配 ULID、建目录树、写 config.yaml + state.json。

    结论：
    - run_id 由此函数生成（使用单调 ULID），调用方传入的 config.run_id 将被忽略并覆盖
    - config.yaml 写入 run_id 和 created_at 字段（原 config 对象不可变，生成副本）
    - state.json 初始 phase = RunPhase.INIT
    - 目录结构：runs/<run_id>/ + runs/<run_id>/artifacts/ + checkpoints/<run_id>/

    Args:
        config: 调用方构造的 RunConfig（run_id 可为 None，此处忽略）

    Returns:
        分配的 26 字符 ULID 字符串
    """
    run_id = generate_ulid()

    # 建目录树（runs/<run_id>/ + artifacts/ + checkpoints/<run_id>/）
    ensure_run_tree(run_id)

    # 填入 run_id 和 created_at，生成带元数据的副本
    filled_config = config.model_copy(
        update={
            "run_id": run_id,
            "created_at": datetime.now(timezone.utc),
        }
    )

    # 写 config.yaml
    config_path = get_run_config_path(run_id)
    save_config(filled_config, config_path)

    # 初始化 state.json（phase = init）
    state = new_run_state(run_id)
    write_state(state, run_id)

    return run_id


def list_runs(*, limit: int | None = None) -> list[str]:
    """列出所有合法 run 的 ULID，按最新在前（字典序降序）排列。

    结论：
    - 仅返回目录名符合 ULID 格式的条目（via validate_ulid）
    - ULID 本身是时间单调递增的 Crockford Base32，字典序 == 时间序
    - runs 根目录不存在时返回空列表（不 raise）
    - limit 为 None 时返回全部；否则截取前 limit 条（即最新的 limit 个）

    Args:
        limit: 返回最多 N 条；None 表示全部

    Returns:
        ULID 字符串列表，最新 run 在前
    """
    base = _runs_base()
    if not base.exists():
        return []

    ulids: list[str] = [
        entry.name
        for entry in base.iterdir()
        if entry.is_dir() and validate_ulid(entry.name)
    ]

    # 字典序降序 = 时间降序（ULID 保证）
    ulids.sort(reverse=True)

    if limit is not None:
        ulids = ulids[:limit]

    return ulids


def get_run_summary(run_id: str) -> dict[str, Any]:
    """读取 run 的 config + state，返回平坦摘要 dict。

    结论：
    - run 不存在（config.yaml 缺失）时 raise FileNotFoundError
    - state.json 缺失时 phase/status 返回 'unknown'
    - 返回字段：run_id, research_question, base_model, phase, status,
                usd_cap, usd_spent，创建时间，基础 budget 信息

    Args:
        run_id: 26 字符 ULID

    Returns:
        dict，包含 run 摘要信息

    Raises:
        FileNotFoundError: config.yaml 不存在时
    """
    config_path = get_run_config_path(run_id)
    if not config_path.exists():
        raise FileNotFoundError(
            f"run {run_id!r} 的 config.yaml 不存在：{config_path}"
        )

    config = load_config(config_path)

    # 读取 state（容错：state.json 缺失时不报错）
    try:
        state = read_state(run_id)
        phase = state.phase.value if isinstance(state.phase, RunPhase) else str(state.phase)
        stuck_state = state.stuck_state
        usd_spent = state.usd_spent
    except (FileNotFoundError, Exception):
        phase = "unknown"
        stuck_state = None
        usd_spent = 0.0

    # 计算 status（简单映射：非 init 且非 completed/failed 视为 running）
    if phase == RunPhase.COMPLETED.value:
        status = "completed"
    elif phase == RunPhase.FAILED.value:
        status = "failed"
    elif phase in (RunPhase.INIT.value, "unknown"):
        status = "pending"
    else:
        status = "running"

    return {
        "run_id": run_id,
        "research_question": config.research_question,
        "base_model": config.base_model,
        "phase": phase,
        "status": status,
        "stuck_state": stuck_state,
        "usd_cap": config.budget.usd_cap,
        "usd_spent": usd_spent,
        "wall_clock_hours_cap": config.budget.wall_clock_hours_cap,
        "gpu_hours_cap": config.budget.gpu_hours_cap,
        "created_at": config.created_at.isoformat() if config.created_at else None,
    }


def run_exists(run_id: str) -> bool:
    """检查指定 run_id 是否存在（以 config.yaml 是否存在为判据）。

    结论：
    - 只检查 config.yaml 存在性，不校验内容合法性
    - 不 raise；有则 True，无则 False

    Args:
        run_id: 26 字符 ULID

    Returns:
        True 若 config.yaml 存在，否则 False
    """
    return get_run_config_path(run_id).exists()
