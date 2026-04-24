"""
pars.proxy.audit_log — API 请求审计日志（append-only JSONL）。

结论：
  每次 API 请求（无论成功/失败）写一行 JSONL 到 runs/<id>/artifacts/api_log.jsonl。
  不记录 prompt 原文、不记录 API key（安全 + GDPR）。
  使用 os.O_APPEND + os.fsync 保证原子性（与 metrics.py 同模式）。

JSONL schema（每行字段）：
  ts           : ISO 8601 UTC 时间戳
  endpoint     : 请求路径（如 "/v1/messages"）
  model        : 模型名（如 "claude-sonnet-4-6"）
  input_tokens : 估算/实际 input token 数
  output_tokens: 实际 output token 数（失败时 0）
  duration_ms  : 端到端耗时（毫秒）
  status_code  : HTTP 状态码（200/402/429/5xx）
  estimated_usd: 前置估算 USD 成本
  actual_usd   : 实际计费 USD（失败/拒绝时 0.0）

禁止字段：
  - 任何 prompt/completion 原文
  - ANTHROPIC_API_KEY 或其任何片段
  - 用户 PII
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pars.logging import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# 路径辅助
# ---------------------------------------------------------------------------


def get_audit_log_path(run_id: str) -> Path:
    """返回 runs/<run_id>/artifacts/api_log.jsonl 路径（不创建目录）。"""
    from pars.paths import run_dir

    return run_dir(run_id) / "artifacts" / "api_log.jsonl"


# ---------------------------------------------------------------------------
# 写入
# ---------------------------------------------------------------------------


def append_audit_record(
    *,
    run_id: str,
    endpoint: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    duration_ms: float,
    status_code: int,
    estimated_usd: float,
    actual_usd: float,
    ts: datetime | None = None,
) -> None:
    """向 api_log.jsonl 追加一条审计记录。

    保证：
    - 不记录 prompt 内容（只记 token 计数）
    - 不记录 API key 或其任何片段
    - 使用 O_APPEND + fsync 保证 append 原子性（与 metrics.py 同模式）

    Args:
        run_id:        run 唯一标识
        endpoint:      请求路径（如 "/v1/messages"）
        model:         模型名
        input_tokens:  估算或实际 input token 数
        output_tokens: 实际 output token 数
        duration_ms:   端到端耗时（毫秒）
        status_code:   HTTP 状态码
        estimated_usd: 前置估算 USD 成本
        actual_usd:    实际计费 USD（拒绝/失败时传 0.0）
        ts:            记录时间（默认 datetime.now(UTC)）

    Raises:
        OSError: 磁盘写入失败
    """
    effective_ts = ts if ts is not None else datetime.now(timezone.utc)

    record: dict[str, Any] = {
        "ts": effective_ts.isoformat(),
        "endpoint": endpoint,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "duration_ms": duration_ms,
        "status_code": status_code,
        "estimated_usd": estimated_usd,
        "actual_usd": actual_usd,
    }

    line_bytes = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")

    path = get_audit_log_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    fd = os.open(str(path), os.O_APPEND | os.O_WRONLY | os.O_CREAT, 0o644)
    try:
        os.write(fd, line_bytes)
        os.fsync(fd)
    finally:
        os.close(fd)

    logger.debug(
        "audit log 已追加",
        extra={
            "run_id": run_id,
            "status_code": status_code,
            "model": model,
            "estimated_usd": estimated_usd,
            "actual_usd": actual_usd,
        },
    )
