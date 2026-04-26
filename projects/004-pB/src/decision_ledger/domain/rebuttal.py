"""
Rebuttal 域模型 — T002
结论: Devil's advocate 服务的输出，一句话粗糙反驳 ≤ 80 字
细节:
  - rebuttal_text: 必填非空，≤ 80 字 (DevilAdvocateService max_tokens ≤ 100 保证)
  - invoked_at: 调用时间戳字符串 (ISO 8601)
  - 不可变 (frozen) — 一旦 LLM 生成即归档
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class Rebuttal(BaseModel):
    """Devil's advocate 输出 — 一句话反驳，不超过 80 字。"""

    model_config = ConfigDict(frozen=True)

    rebuttal_text: str   # ≤ 80 字，DevilAdvocateService fast-path 保证简短
    invoked_at: str      # ISO 8601 时间戳字符串

    @field_validator("rebuttal_text")
    @classmethod
    def _validate_rebuttal_text(cls, v: str) -> str:
        """结论: rebuttal_text 必须非空且不超过 80 字符。"""
        if not v or not v.strip():
            raise ValueError("rebuttal_text 不能为空")
        if len(v) > 80:
            raise ValueError(
                f"rebuttal_text 不能超过 80 字符，当前 {len(v)} 字符 (DevilAdvocateService 约束)"
            )
        return v
