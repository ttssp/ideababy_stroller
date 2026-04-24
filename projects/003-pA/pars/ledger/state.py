"""
pars.ledger.state — state.json 读写 + run lifecycle 状态机。

结论：state.json 是 resume（C13）的核心载体，每次 phase 切换和 stuck/budget
      事件都必须先更新 state，再继续执行，确保断电/kill 后仍可 resume。

state.json 文件位置：runs/<run_id>/state.json

### Phase 合法转移表（VALID_TRANSITIONS）

来源：spec §4 D13 + T007 known gotchas。"* → failed" 表示任意 phase 均可失败。
"lora_train → lora_train" 支持 resume 重入。

```
init          → baseline | lora_train | failed
baseline      → lora_train | eval | failed
lora_train    → lora_train | eval | failed   (lora_train→lora_train = resume 重入)
eval          → report | failed
report        → completed | failed
completed     → (终态，无出边)
failed        → (终态，无出边)
```

### 并发安全

update_state 使用 fcntl.flock（POSIX 独占锁），防止 worker 与 CLI `pars status`
同时写 state.json。v0.1 只有 1 worker 顺序执行，锁主要防 worker 与 CLI 并发。
atomic write = 先写 .tmp 文件，flock 内 rename 覆盖，保证读到的永远是完整 JSON。
"""

from __future__ import annotations

import fcntl
import json
import os
import tempfile
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from pars.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Phase 枚举
# ---------------------------------------------------------------------------


class RunPhase(StrEnum):
    """run 的生命周期阶段（有限状态机节点）。

    顺序：init → baseline → lora_train → eval → report → completed
    任意阶段均可跳转 failed。
    """

    INIT = "init"
    BASELINE = "baseline"
    LORA_TRAIN = "lora_train"
    EVAL = "eval"
    REPORT = "report"
    COMPLETED = "completed"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# 合法转移表
# ---------------------------------------------------------------------------

#: VALID_TRANSITIONS[src] = {dest, ...}
#: 终态（completed / failed）出边为空集，update_state 会拒绝
VALID_TRANSITIONS: dict[str, set[str]] = {
    RunPhase.INIT: {RunPhase.BASELINE, RunPhase.LORA_TRAIN, RunPhase.FAILED},
    RunPhase.BASELINE: {RunPhase.LORA_TRAIN, RunPhase.EVAL, RunPhase.FAILED},
    RunPhase.LORA_TRAIN: {RunPhase.LORA_TRAIN, RunPhase.EVAL, RunPhase.FAILED},
    RunPhase.EVAL: {RunPhase.REPORT, RunPhase.FAILED},
    RunPhase.REPORT: {RunPhase.COMPLETED, RunPhase.FAILED},
    RunPhase.COMPLETED: set(),
    RunPhase.FAILED: set(),
}


# ---------------------------------------------------------------------------
# Pydantic 数据模型
# ---------------------------------------------------------------------------


class RunState(BaseModel):
    """state.json 的完整 schema。

    设计原则：
    - extra="forbid"：未知字段直接报错，防止调用方传入拼错的字段名
    - 所有时间均为 UTC datetime（tzinfo 非空）
    - T019（resume 主逻辑）和 T017（stuck 探测）通过 update_state 写入各自字段
    - T018（budget 计量）负责更新 usd_spent / wall_clock_elapsed_s / gpu_hours_used
    """

    model_config = ConfigDict(extra="forbid")

    run_id: str
    phase: RunPhase
    current_script: str | None = None
    """当前正在执行的脚本文件名（baseline_script.py / lora_script.py / eval_script.py）"""
    checkpoint_path: str | None = None
    """最新 checkpoint 的绝对路径，供 resume 使用"""
    last_epoch_completed: int | None = None
    """已完成的最后一个 epoch 编号（0-based），None 表示尚未开始"""
    stuck_state: str = "idle"
    """Stuck 状态机节点：idle | training | downloading | truly_stuck（见 architecture §8）"""
    stuck_restart_count: int = 0
    """Stuck 触发后 SIGINT+restart 的累计次数"""
    needs_human_review: bool = False
    """熔断信号：True 时 CLI 打印警告并阻止自动 resume（T017 写入）"""
    usd_spent: float = 0.0
    """截至当前的 API 累计消费（USD）；proxy 前置账本，T018 更新"""
    wall_clock_elapsed_s: float = 0.0
    """run 启动至今的 wall-clock 秒数；T018 更新"""
    gpu_hours_used: float = 0.0
    """GPU 使用小时数；T018 更新"""
    last_update: datetime
    """最后一次 write_state 的 UTC 时间戳"""

    @field_validator("stuck_state")
    @classmethod
    def _validate_stuck_state(cls, v: str) -> str:
        allowed = {"idle", "training", "downloading", "truly_stuck"}
        if v not in allowed:
            raise ValueError(f"stuck_state 必须是 {allowed!r}，got {v!r}")
        return v

    @field_validator("last_update", mode="before")
    @classmethod
    def _ensure_utc(cls, v: Any) -> Any:
        """将无时区 datetime 自动标记为 UTC，便于 JSON 反序列化。"""
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


# ---------------------------------------------------------------------------
# 路径辅助
# ---------------------------------------------------------------------------


def _state_path(run_id: str) -> Path:
    """返回 runs/<run_id>/state.json 的绝对路径（不创建目录）。"""
    from pars.paths import run_dir

    return run_dir(run_id) / "state.json"


# ---------------------------------------------------------------------------
# 序列化辅助
# ---------------------------------------------------------------------------

_DT_FMT = "%Y-%m-%dT%H:%M:%S.%f+00:00"


def _to_json_str(state: RunState) -> str:
    """序列化 RunState → JSON 字符串（datetime 保持 ISO 8601 UTC 格式）。"""
    data = state.model_dump()
    # datetime 序列化
    for key in ("last_update",):
        if isinstance(data.get(key), datetime):
            dt: datetime = data[key].astimezone(timezone.utc)
            data[key] = dt.strftime(_DT_FMT)
    # Enum 序列化
    if isinstance(data.get("phase"), RunPhase):
        data["phase"] = data["phase"].value
    return json.dumps(data, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 读写 API
# ---------------------------------------------------------------------------


def read_state(run_id: str) -> RunState:
    """从 state.json 加载 RunState。

    Raises：
        FileNotFoundError : state.json 不存在
        pydantic.ValidationError : JSON 内容不符合 RunState schema
        json.JSONDecodeError : 文件内容不是合法 JSON
    """
    path = _state_path(run_id)
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    return RunState.model_validate(data)


def write_state(state: RunState, run_id: str) -> None:
    """将 RunState 写入 state.json（atomic write：temp file + rename）。

    原子性保证：
    1. 先写同目录的 .tmp 文件
    2. os.replace（POSIX atomic rename）覆盖 state.json
    确保读到的永远是完整 JSON（不会读到半截文件）。

    参数：
        state  : 要持久化的 RunState
        run_id : 用于定位 state.json 路径
    """
    path = _state_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    json_str = _to_json_str(state)

    # 写 .tmp（与目标同目录，确保 rename 是 same-device atomic）
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, prefix=".state_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json_str)
        os.replace(tmp_path, path)
    except Exception:
        # 清理 tmp，避免残留
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    logger.debug("state written", extra={"run_id": run_id, "phase": state.phase.value})


def update_state(run_id: str, **kwargs: Any) -> RunState:
    """原子读 → 校验 → 改 → 写，返回新 state。

    支持部分更新：只传要修改的字段。phase 字段有合法转移校验。
    使用 fcntl.flock 防止并发写（worker 与 CLI 同时执行时互斥）。

    参数：
        run_id : run 标识
        **kwargs : 要更新的字段（键值对）

    返回：
        更新后的 RunState

    Raises：
        FileNotFoundError : state.json 不存在
        ValueError : phase 转移非法（如 completed → lora_train）
        pydantic.ValidationError : 更新字段值非法
    """
    path = _state_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    lock_path = path.parent / ".state.lock"
    with open(lock_path, "w") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            state = read_state(run_id)

            # phase 转移合法性校验
            if "phase" in kwargs:
                new_phase = RunPhase(kwargs["phase"])
                current_phase = state.phase
                allowed = VALID_TRANSITIONS.get(current_phase, set())
                if new_phase not in allowed:
                    raise ValueError(
                        f"非法 phase 转移：{current_phase.value!r} → {new_phase.value!r}。"
                        f"合法目标：{sorted(p.value for p in allowed)!r}"
                    )

            # 合并更新（Pydantic model_copy + update）
            updated_data = state.model_dump()
            updated_data.update(kwargs)
            updated_data["last_update"] = datetime.now(timezone.utc)

            new_state = RunState.model_validate(updated_data)
            write_state(new_state, run_id)
            return new_state
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# 便捷工厂
# ---------------------------------------------------------------------------


def new_run_state(run_id: str) -> RunState:
    """创建一个全新 run 的初始 RunState（phase=init）。

    不写磁盘，调用方负责调用 write_state 持久化。
    """
    now = datetime.now(timezone.utc)
    return RunState(
        run_id=run_id,
        phase=RunPhase.INIT,
        last_update=now,
    )
