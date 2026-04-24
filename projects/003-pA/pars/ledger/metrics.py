"""
pars.ledger.metrics — Metrics JSONL append + 读取工具。

结论:
  metrics.jsonl 是 append-only NDJSON 文件,每行一个 JSON 对象。
  写入端(训练子进程/worker)与读取端(CLI host)可同时操作,
  依赖 POSIX O_APPEND 语义保证单次 write syscall 的原子性。

`metrics.jsonl` 位置:`<run_dir>/metrics.jsonl`

schema(architecture §3 Sequence 约定):
  每行一个 JSON 对象,字段:
  - ts: ISO 8601 UTC timestamp(必)
  - phase: 'baseline' | 'training' | 'evaluating' | 'reporting'(必)
  - kind: 'epoch' | 'step' | 'eval' | 'custom'(必)
  - data: {...}(自由 dict,不 validate;由写入者定义含义)

append-only 保证:
  - 并发写:os.open(O_APPEND | O_WRONLY | O_CREAT) 保证 append 原子性
    (POSIX PIPE_BUF 内,通常 4-64KB)
  - 超过 PIPE_BUF 时不保证原子性,但 metric 单条通常 << 4KB;超过记 warning
  - 写后 os.fsync 保证 crash-safe(电源故障不丢数据)

读接口支持流式(不一次性 load 整个文件)。
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pars.logging import get_logger

logger = get_logger(__name__)

# POSIX 最小保证的 PIPE_BUF(字节)。Linux 通常 65536,macOS 通常 65536。
# 保守取 4096(POSIX 规范最低值)来判断 warning 阈值。
_PIPE_BUF_CONSERVATIVE = 4096

MetricPhase = Literal["baseline", "training", "evaluating", "reporting"]
MetricKind = Literal["epoch", "step", "eval", "custom"]


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MetricRecord:
    """单条 metric 记录,frozen 防止意外修改。

    字段:
        ts:    UTC 感知 datetime
        phase: run 阶段
        kind:  记录类型
        data:  自由 payload dict(不做 schema 校验)
    """

    ts: datetime
    phase: MetricPhase
    kind: MetricKind
    data: dict[str, Any]


# ---------------------------------------------------------------------------
# 路径辅助
# ---------------------------------------------------------------------------


def get_metrics_path(run_id: str) -> Path:
    """返回 run 的 metrics.jsonl 标准位置。

    路径:$RECALLKIT_RUN_DIR/<run_id>/metrics.jsonl
    不创建目录,调用方负责 mkdir。
    """
    from pars.paths import run_dir

    return run_dir(run_id) / "metrics.jsonl"


# ---------------------------------------------------------------------------
# 写接口
# ---------------------------------------------------------------------------


def append_metric(
    run_id: str,
    phase: MetricPhase,
    kind: MetricKind,
    data: dict[str, Any],
    *,
    ts: datetime | None = None,
) -> None:
    """向 metrics.jsonl 追加一条 metric 记录。

    原子性保证:
    - 使用 os.open(O_APPEND | O_WRONLY | O_CREAT) 打开文件
    - 单次 os.write() syscall 写入完整行(含结尾 \\n)
    - POSIX 保证 write() < PIPE_BUF 时原子性(同一文件多写者互不交错)
    - 写后 os.fsync() 确保 crash-safe

    Args:
        run_id: run 唯一标识(ULID);调用方负责确保合法,本函数不校验
        phase:  run 阶段('baseline'|'training'|'evaluating'|'reporting')
        kind:   记录类型('epoch'|'step'|'eval'|'custom')
        data:   任意可 JSON 序列化的 dict;含 set 等不可序列化类型会 raise TypeError
        ts:     显式时间戳;默认 datetime.now(timezone.utc)

    Raises:
        TypeError:  data 包含无法序列化的类型(如 set)
        OSError:    磁盘错误
    """
    effective_ts = ts if ts is not None else datetime.now(timezone.utc)

    record_dict: dict[str, Any] = {
        "ts": effective_ts.isoformat(),
        "phase": phase,
        "kind": kind,
        "data": data,
    }

    # 序列化:不使用 default=str 降级,让 set 等类型直接 raise TypeError
    # 原因:调用方应传入干净的 data,隐式降级会掩盖 bug
    line_bytes = (json.dumps(record_dict, ensure_ascii=False) + "\n").encode("utf-8")

    # 超 PIPE_BUF 保守阈值时 warning(原子性可能失效)
    if len(line_bytes) > _PIPE_BUF_CONSERVATIVE:
        logger.warning(
            "metric record 超过 PIPE_BUF 保守阈值,并发写入原子性不保证(data 过大)",
            extra={
                "run_id": run_id,
                "size_bytes": len(line_bytes),
                "pipe_buf_threshold": _PIPE_BUF_CONSERVATIVE,
            },
        )

    # 确保父目录存在(run 目录可能尚未创建)
    path = get_metrics_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    # 原子 append:O_APPEND 保证多进程/线程 write() 不交错
    fd = os.open(str(path), os.O_APPEND | os.O_WRONLY | os.O_CREAT, 0o644)
    try:
        os.write(fd, line_bytes)
        os.fsync(fd)
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# 读接口
# ---------------------------------------------------------------------------


def _parse_line(line: str, line_no: int) -> MetricRecord | None:
    """将单行 JSON 字符串解析为 MetricRecord。

    解析失败时 log warning 返回 None(由调用方决定是否跳过)。

    结论:
    - 文件末尾可能有不完整行(crash 中断写入),应跳过而非崩溃
    - 字段缺失或类型错误同样跳过,保证读取稳健性
    """
    line = line.strip()
    if not line:
        return None
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as e:
        logger.warning(
            "metrics.jsonl 第 %d 行 JSON 解析失败,跳过",
            line_no,
            extra={"line_preview": line[:80], "error": str(e)},
        )
        return None

    try:
        ts_str: str = obj["ts"]
        phase: MetricPhase = obj["phase"]
        kind: MetricKind = obj["kind"]
        data: dict[str, Any] = obj["data"]
    except (KeyError, TypeError) as e:
        logger.warning(
            "metrics.jsonl 第 %d 行字段缺失,跳过",
            line_no,
            extra={"line_preview": line[:80], "error": str(e)},
        )
        return None

    # 解析 datetime:ISO 8601,fromisoformat 兼容带/不带 tzinfo
    try:
        ts = datetime.fromisoformat(ts_str)
        # 若无 tzinfo,假定 UTC
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError) as e:
        logger.warning(
            "metrics.jsonl 第 %d 行 ts 字段解析失败,跳过",
            line_no,
            extra={"ts_str": ts_str, "error": str(e)},
        )
        return None

    return MetricRecord(ts=ts, phase=phase, kind=kind, data=data)


def read_metrics(
    run_id: str,
    *,
    phase: MetricPhase | None = None,
    kind: MetricKind | None = None,
) -> Iterator[MetricRecord]:
    """流式读 metrics.jsonl,可选按 phase/kind 过滤。

    特性:
    - 文件不存在时返回空 iterator(不 raise)
    - 单行解析失败:log warning 跳过,不中断读取
      (rolling append 文件最后一行可能未完整写入)
    - 逐行 yield,不一次性 load 整个文件(支持大文件)
    - 可同时指定 phase 和 kind 过滤(AND 语义)

    Args:
        run_id: run 唯一标识
        phase:  按 phase 过滤;None 表示不过滤
        kind:   按 kind 过滤;None 表示不过滤

    Yields:
        MetricRecord:通过过滤的记录
    """
    path = get_metrics_path(run_id)
    if not path.exists():
        return

    with open(path, encoding="utf-8") as f:  # noqa: PTH123
        for line_no, line in enumerate(f, 1):
            record = _parse_line(line, line_no)
            if record is None:
                continue
            if phase is not None and record.phase != phase:
                continue
            if kind is not None and record.kind != kind:
                continue
            yield record


# ---------------------------------------------------------------------------
# 聚合工具
# ---------------------------------------------------------------------------


def count_metrics(run_id: str, *, phase: MetricPhase | None = None) -> int:
    """计算 metrics.jsonl 中的记录条数,支持按 phase 过滤。

    特性:
    - 不一次性 load 全部记录(流式计数)
    - 适合 pars status 等轻量查询
    - 文件不存在返回 0

    Args:
        run_id: run 唯一标识
        phase:  按 phase 过滤;None 表示计全部

    Returns:
        记录条数(int)
    """
    return sum(1 for _ in read_metrics(run_id, phase=phase))


def last_metric(
    run_id: str,
    *,
    phase: MetricPhase | None = None,
    kind: MetricKind | None = None,
) -> MetricRecord | None:
    """返回最后一条 metric 记录(可选按 phase/kind 过滤)。

    实现:线性扫描 read_metrics,保留最后一个匹配项。
    metrics 文件通常 << 100MB(每 epoch 1-N 条,小模型任务),
    线性扫描性能可接受,v0.1 不做反向 IO 优化。

    Args:
        run_id: run 唯一标识
        phase:  按 phase 过滤;None 表示不过滤
        kind:   按 kind 过滤;None 表示不过滤

    Returns:
        最后一条匹配的 MetricRecord;文件不存在或无匹配时返回 None
    """
    last: MetricRecord | None = None
    for record in read_metrics(run_id, phase=phase, kind=kind):
        last = record
    return last
