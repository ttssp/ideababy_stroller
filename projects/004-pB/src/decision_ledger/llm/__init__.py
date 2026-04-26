"""
LLM 抽象层 — T005
结论: 所有 LLM 调用必须经过此层 (架构不变量 §9.8)
细节:
  - LLMClient: 统一 async 接口，封装 cache / retry / usage / structured output
  - cache: 文件缓存，键 = sha256(advisor_week_id + ticker + prompt_template_version + model)
  - retry: 5 次指数退避 + jitter，失败后 fallback Sonnet → Haiku
  - usage: 记账每次调用 token 数 + cost (LLMUsageWriter Protocol 解耦 T003)
  - prompts: PromptTemplate 版本化 prompt 加载
"""

from decision_ledger.llm.client import LLMClient
from decision_ledger.llm.errors import LLMSchemaError, LLMUnavailableError
from decision_ledger.llm.usage import LLMUsageWriter

__all__ = [
    "LLMClient",
    "LLMSchemaError",
    "LLMUnavailableError",
    "LLMUsageWriter",
]
