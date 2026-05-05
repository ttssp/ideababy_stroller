"""
AdvisorWeeklyReport / ParseFailure 域模型 — T002
结论: 咨询师周报解析结果，含 source_id 字段预留 (R8/R20 红线)
细节:
  - source_id 字段: R8/R20 红线，schema 预留，即使 v0.1 只有一个咨询师也不路径依赖
  - structured_json: LLM 解析的结构化结果 (方向/标的/置信度)
  - raw_pdf_path: 原始 PDF 路径，审计追溯用
  - parsed_at: 解析时间戳
  - advisor_week_id: 格式 "YYYY-WNN" (e.g. "2026-W17")
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AdvisorWeeklyReport(BaseModel):
    """咨询师周报解析结果。"""

    model_config = ConfigDict(frozen=True)

    advisor_id: str                     # 咨询师 ID (v0.1 只有一个，但预留 source_id)
    source_id: str                      # R8/R20 红线: 预留，v0.1 = advisor_id，v0.2+ 支持多源
    week_id: str                        # "YYYY-WNN"，e.g. "2026-W17"
    raw_text: str                       # PDF 提取的原始文本
    structured_json: dict[str, Any]     # LLM 结构化输出: {ticker: {direction, confidence, ...}}
    raw_pdf_path: str | None = None     # 原始 PDF 文件路径 (归档/审计用)
    parsed_at: datetime = datetime.now()


class ParseFailure(BaseModel):
    """PDF 解析失败记录 — 入库供 human 重试或手动结构化。"""

    model_config = ConfigDict(frozen=True)

    failure_id: str         # UUID 字符串
    pdf_path: str           # 失败的 PDF 路径
    error_message: str      # 错误信息
    failed_at: datetime = datetime.now()
    advisor_id: str | None = None
