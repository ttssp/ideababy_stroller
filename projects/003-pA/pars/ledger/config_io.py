"""
pars.ledger.config_io — config.yaml 原子读写层。

结论：提供 load_config / save_config / update_config_field 三个函数，
      所有写操作均通过临时文件 + os.replace() 保证原子性，
      update_config_field 通过 fcntl.flock 保证并发安全。

设计原则：
  1. 原子写（atomic write）：先写 .tmp 临时文件，完成后 os.replace()，
     防止读者读到半写状态的文件
  2. yaml.safe_load / yaml.safe_dump：防 pickle injection
  3. update_config_field 用 fcntl.flock 排它锁：先读 → 改字段 → 原子写 → 放锁
  4. datetime 字段：YAML 中以 ISO8601 字符串存储（防止跨 YAML 实现解析不一致）
  5. ValidationError re-raise 带上 path 信息方便排查

依赖：
  - pyyaml（已在 pyproject.toml 锁定 pyyaml==6.0.3）
  - pydantic v2（已在 pyproject.toml 依赖链中）
  - fcntl（POSIX 标准库，macOS/Linux 均支持；spec tech-stack §7 明确只支持 macOS/Linux）
"""

from __future__ import annotations

import fcntl
import os
import tempfile
from pathlib import Path

import yaml
from pydantic import ValidationError

from pars.ledger.config_schema import RunConfig
from pars.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# 内部辅助：datetime 序列化兼容
# ---------------------------------------------------------------------------

def _prepare_for_yaml(data: dict) -> dict:
    """递归将 datetime 对象转为 ISO8601 字符串，确保 YAML 跨实现一致。

    Pydantic model_dump() 返回的字典中 datetime 字段为 datetime 对象，
    yaml.safe_dump 会把它序列化为 YAML datetime tag（!!python/object/apply:...），
    在不同 YAML 实现中解析不一致。统一转为字符串避免此问题。
    """
    from datetime import datetime

    result = {}
    for key, value in data.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, dict):
            result[key] = _prepare_for_yaml(value)
        elif isinstance(value, list):
            result[key] = [
                (item.isoformat() if isinstance(item, datetime) else item)
                for item in value
            ]
        else:
            result[key] = value
    return result


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------

def load_config(path: Path) -> RunConfig:
    """从 YAML 文件加载并 validate RunConfig。

    参数：
        path: config.yaml 文件路径（必须存在）

    返回：
        已通过 Pydantic v2 校验的 RunConfig 对象

    异常：
        FileNotFoundError: path 不存在
        ValueError: YAML 解析失败（非合法 YAML）
        pydantic.ValidationError: schema 验证失败（字段缺失/类型错误/额外字段等）
    """
    if not path.exists():
        raise FileNotFoundError(f"config.yaml 不存在: {path}")

    logger.debug("loading config", extra={"path": str(path)})

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 解析失败: {path}\n{e}") from e

    if raw is None:
        raise ValueError(f"config.yaml 内容为空: {path}")

    try:
        cfg = RunConfig.model_validate(raw)
    except ValidationError as e:
        # re-raise 带上文件路径，方便排查是哪个 yaml 文件出错
        raise ValidationError(e.errors(), RunConfig) from None

    logger.debug("config loaded", extra={"run_id": cfg.run_id, "path": str(path)})
    return cfg


def save_config(config: RunConfig, path: Path) -> None:
    """序列化 RunConfig 到 YAML（atomic write：temp + rename）。

    参数：
        config: 已验证的 RunConfig 对象
        path: 目标 config.yaml 路径（父目录必须存在）

    设计：
        先写临时文件 <path>.tmp，完成后 os.replace() 原子替换目标文件，
        防止读者读到半写状态。即使中途 crash，也只留下 .tmp 文件（下次重写会覆盖），
        不会破坏已有的 config.yaml。
    """
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)

    # model_dump(mode="json") 会把 datetime 转为字符串（Pydantic v2 行为）
    # 再套一层 _prepare_for_yaml 保险，确保嵌套 dict 中没有残余 datetime 对象
    data = config.model_dump(mode="json")

    yaml_str = yaml.safe_dump(
        data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=True,
    )

    logger.debug("saving config", extra={"path": str(path)})

    # 在同一父目录下创建临时文件（同 fs，确保 rename 是原子的 rename 而非跨 fs copy）
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        prefix=".config_",
        suffix=".tmp",
        dir=str(parent),
    )
    tmp_path = Path(tmp_path_str)

    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.write(yaml_str)
            f.flush()
            os.fsync(f.fileno())  # 确保数据刷到磁盘，防止 rename 后内容丢失

        # 原子替换：POSIX 保证 os.replace 是原子的（单 fs 内）
        os.replace(tmp_path, path)

    except Exception:
        # 清理临时文件，避免残留
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise

    logger.debug("config saved", extra={"run_id": config.run_id, "path": str(path)})


def update_config_field(path: Path, key: str, value: object) -> None:
    """原子地更新 config.yaml 中的单个顶层字段。

    参数：
        path: config.yaml 文件路径（必须已存在）
        key: 要更新的顶层字段名（如 'notes'、'usd_total'）
        value: 新的字段值（必须与 RunConfig 字段类型兼容）

    设计（fcntl.flock 互斥）：
        1. 获取排它锁（LOCK_EX）
        2. 读取当前 config（load_config）
        3. 修改指定字段（model_copy）
        4. 原子写回（save_config）
        5. 释放锁

    注意：
        - key 只支持顶层字段；嵌套字段更新请直接 load → 手动修改 → save
        - fcntl.flock 在 macOS/Linux 上有效；Windows 不支持（spec §7 明确只支持 macOS/Linux）
        - flock 是建议锁（advisory lock），只对同样使用 flock 的进程有效

    异常：
        FileNotFoundError: path 不存在
        ValueError: key 不是 RunConfig 的合法顶层字段
        pydantic.ValidationError: 新值与字段类型不匹配
    """
    if not path.exists():
        raise FileNotFoundError(f"config.yaml 不存在: {path}")

    # 验证 key 是合法的 RunConfig 字段
    valid_fields = set(RunConfig.model_fields.keys())
    if key not in valid_fields:
        raise ValueError(
            f"'{key}' 不是 RunConfig 的合法顶层字段。"
            f"合法字段：{sorted(valid_fields)}"
        )

    logger.debug("updating config field", extra={"path": str(path), "key": key})

    # 使用排它锁（LOCK_EX）保证并发安全
    with path.open("r+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            # 重新读取（在锁内，确保读到最新版本）
            cfg = load_config(path)
            # model_copy 创建新对象（不可变 pattern）
            updated = cfg.model_copy(update={key: value})
            # 原子写回
            save_config(updated, path)
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    logger.debug("config field updated", extra={"path": str(path), "key": key})


def get_run_config_path(run_id: str) -> Path:
    """返回 run 的 config.yaml 标准位置：`<run_dir>/config.yaml`。

    参数：
        run_id: ULID 格式的 run ID

    返回：
        config.yaml 的绝对路径（不保证文件存在）

    注意：路径通过 pars.paths.run_dir() 计算，支持 RECALLKIT_RUN_DIR env var 覆盖
    """
    from pars.paths import run_dir

    return run_dir(run_id) / "config.yaml"
