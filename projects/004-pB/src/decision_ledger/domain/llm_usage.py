"""
LLMUsage 域模型 — T002
结论: LLM 调用成本日志，每次 API 调用后写入
细节:
  - 架构 §10 M4: 防日志格式漂移，所有字段在此定义
  - cost_usd: 实时估算 (input_tokens × 价格 + output_tokens × 价格)
  - cache_hit: D21 监控，命中率目标 ≥ 95%
  - prompt_template_version: 版本化 prompt，e.g. "conflict_v1"
  - latency_ms: R2 Q11 监控，draft 阶段 latency 分布
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LLMUsage(BaseModel):
    """LLM API 调用记录 — 成本监控 + cache 命中率监控。"""

    model_config = ConfigDict(frozen=True)

    # call_id: UUID 字符串
    # service: 调用方,如 "ConflictReportAssembler" / "AdvisorStrategy.analyze"
    # model: 模型 ID,如 "claude-sonnet-4-6"
    # prompt_template_version: prompt 版本,如 "conflict_v1"
    call_id: str
    service: str
    model: str
    prompt_template_version: str
    prompt_tokens: int
    output_tokens: int
    cost_usd: float                        # 实时估算
    cache_hit: bool                        # D21 命中率监控
    latency_ms: int                        # R2 Q11 latency 监控 (毫秒)
    created_at: datetime = datetime.now()
