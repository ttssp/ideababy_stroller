"""
pars.stuck.stuck_lock — stuck_lock 文件读写（原子写 + 幂等删除）。

结论：
- stuck_lock 是"锁标记文件"，存在即表示进程被 circuit breaker 锁定
- 写入采用 tempfile + rename 保证原子性（避免读到半写文件）
- has_stuck_lock() 是纯存在性检查，无 I/O 副作用
- clear_stuck_lock() 幂等（文件不存在不抛异常）
- read_stuck_lock() 文件不存在时抛 FileNotFoundError（由调用方决策）

文件路径：$RECALLKIT_RUN_DIR/<run_id>/stuck_lock
文件内容：JSON { reason, restart_count, created_at（ISO 8601 UTC） }
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from pars.logging import get_logger
from pars.paths import run_dir

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------


class StuckLockData(BaseModel):
    """stuck_lock 文件内容的强类型模型。"""

    reason: str
    restart_count: int
    created_at: str  # ISO 8601 UTC, e.g. "2024-01-01T00:00:00+00:00"


# ---------------------------------------------------------------------------
# 内部辅助
# ---------------------------------------------------------------------------


def _lock_path(run_id: str) -> Path:
    """返回 stuck_lock 文件的绝对路径（不创建目录）。"""
    return run_dir(run_id) / "stuck_lock"


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------


def write_stuck_lock(run_id: str, reason: str, restart_count: int) -> None:
    """原子写入 stuck_lock 文件（tempfile + rename）。

    参数：
        run_id        : run 标识符
        reason        : 锁定原因（通常 "circuit_breaker_tripped"）
        restart_count : 当前 stuck_restart_count

    原子性保证：
    1. 先写到同目录下的临时文件（.tmp 扩展）
    2. 再 rename 到 stuck_lock（同目录 rename 是 POSIX 原子操作）
    """
    lock_file = _lock_path(run_id)
    data = StuckLockData(
        reason=reason,
        restart_count=restart_count,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    payload = data.model_dump_json(indent=2)

    # tempfile 写到目标文件的同目录，确保 rename 是同文件系统（原子）
    dir_path = lock_file.parent
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=dir_path,
            suffix=".tmp",
            delete=False,
            encoding="utf-8",
        ) as tmp_f:
            tmp_path = Path(tmp_f.name)
            tmp_f.write(payload)

        # POSIX 原子 rename：目标路径若存在则直接替换（覆盖）
        tmp_path.rename(lock_file)
        logger.info(
            "stuck_lock 写入成功",
            extra={"run_id": run_id, "reason": reason, "restart_count": restart_count},
        )
    except Exception as exc:
        logger.error("write_stuck_lock: 写入失败", exc_info=exc, extra={"run_id": run_id})
        raise


def has_stuck_lock(run_id: str) -> bool:
    """检查 stuck_lock 文件是否存在（存在 = 进程被锁定）。

    纯存在性检查，不读取文件内容。

    返回：
        True  : stuck_lock 文件存在
        False : 文件不存在
    """
    return _lock_path(run_id).exists()


def read_stuck_lock(run_id: str) -> StuckLockData:
    """读取并反序列化 stuck_lock 文件。

    文件不存在时抛 FileNotFoundError（由调用方决策是否继续）。

    返回：
        StuckLockData : 反序列化后的锁数据

    抛出：
        FileNotFoundError : 文件不存在
        json.JSONDecodeError : 文件内容不合法 JSON
        pydantic.ValidationError : 字段类型不匹配
    """
    lock_file = _lock_path(run_id)
    if not lock_file.exists():
        raise FileNotFoundError(f"stuck_lock 不存在: {lock_file}")
    content = lock_file.read_text(encoding="utf-8")
    raw = json.loads(content)
    return StuckLockData(**raw)


def clear_stuck_lock(run_id: str) -> None:
    """删除 stuck_lock 文件（幂等，文件不存在不抛异常）。

    用于 `pars unlock` 命令：人工确认后解锁，让 orchestrator 可以继续。
    """
    lock_file = _lock_path(run_id)
    try:
        lock_file.unlink()
        logger.info("stuck_lock 已清除", extra={"run_id": run_id})
    except FileNotFoundError:
        # 幂等：文件不存在时静默忽略
        logger.debug("clear_stuck_lock: 文件不存在（幂等忽略）", extra={"run_id": run_id})
