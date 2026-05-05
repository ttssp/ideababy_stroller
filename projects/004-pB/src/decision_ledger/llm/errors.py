"""
LLM 层自定义异常 — T005
结论: 明确异常边界，防止业务层处理错误类型
细节:
  - LLMUnavailableError: 5 次 retry 全失败或 fallback 也失败 (TECH-7)
  - LLMSchemaError: tool-use 返回数据不符合 pydantic schema (SEC-4)
"""

from __future__ import annotations


class LLMUnavailableError(Exception):
    """
    LLM 不可用 — 5 次 retry 全部失败，且 fallback 也失败。
    上层 (worker / advisor) 决定写 parse_failures 还是 503。
    """

    def __init__(self, message: str, attempts: int = 0) -> None:
        super().__init__(message)
        self.attempts = attempts


class LLMSchemaError(Exception):
    """
    tool-use 返回数据与期望 pydantic schema 不匹配 (SEC-4 mitigation)。
    不接受 free-form text，任何 schema violation 都会触发此异常。
    上层决定写 parse_failures 还是重试。
    """

    def __init__(self, message: str, raw_data: object = None) -> None:
        super().__init__(message)
        self.raw_data = raw_data
