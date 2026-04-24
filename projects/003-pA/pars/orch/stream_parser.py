"""claude -p --output-format stream-json 输出解析。

结论:
  Claude Code headless 模式输出 NDJSON(每行一个 JSON 对象)。
  我们关心三类事件:
    - message:    assistant 消息,含 usage(input_tokens / output_tokens)
    - tool_use:   工具调用请求(stuck detector 的 activity 信号)
    - tool_result: 工具调用结果
    - error:      运行时错误(记 state.error)

  其余类型(ping / message_start / message_delta / content_block_* 等)
  统一以 event_type 原样透传,不丢弃(让下游决定是否处理)。

损坏行:跳过 + log warning,不抛异常(容错 parse)。

claude -p --output-format stream-json 实际输出格式(2026-04 版):
  {"type": "system", "subtype": "init", ...}
  {"type": "assistant", "message": {"id": "...", "role": "assistant",
    "content": [...], "usage": {...}}, ...}
  {"type": "tool_use", "name": "...", "id": "...", "input": {...}}
  {"type": "tool_result", "tool_use_id": "...", "content": "..."}
  {"type": "result", "subtype": "success|error", ...}

注意:外层 type 字段是事件类型,"message" 子字段才是真正的 assistant message。
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from pars.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ClaudeEvent:
    """单个 claude -p stream-json 事件。

    字段:
        event_type: 事件类型字符串(来自 JSON 的 "type" 字段)
                    已知值: "assistant", "tool_use", "tool_result", "error",
                             "system", "result", 以及 claude 可能新增的其他类型
        raw:        原始解析后的 dict(完整保留,供下游读取细节)
    """

    event_type: str
    raw: dict[str, Any]

    @property
    def usage(self) -> dict[str, Any] | None:
        """提取 usage 信息(input_tokens / output_tokens)。

        仅 event_type == "assistant" 时有效:
            raw["message"]["usage"] = {"input_tokens": N, "output_tokens": N}
        其他类型返回 None。
        """
        if self.event_type == "assistant":
            message = self.raw.get("message", {})
            if isinstance(message, dict):
                return message.get("usage") or None
        return None

    @property
    def tool_name(self) -> str | None:
        """仅 tool_use 事件有效,返回工具名称。"""
        if self.event_type == "tool_use":
            return self.raw.get("name")
        return None

    @property
    def error_info(self) -> dict[str, Any] | str | None:
        """仅 error / result(subtype=error) 事件有效,返回错误信息。"""
        if self.event_type == "error":
            return self.raw.get("error") or self.raw
        if self.event_type == "result" and self.raw.get("subtype") == "error":
            return self.raw
        return None

    @property
    def is_success_result(self) -> bool:
        """result 事件且 subtype == success 时返回 True。"""
        return self.event_type == "result" and self.raw.get("subtype") == "success"


def parse_stream(lines: Iterator[str]) -> Iterator[ClaudeEvent]:
    """逐行解析 claude -p --output-format stream-json 输出。

    容错行为:
    - 空行:跳过(不是 NDJSON 错误)
    - JSON 解析失败:log warning + 跳过
    - 缺少 "type" 字段:log warning + 跳过
    - 合法 JSON 但 type 未知:透传(不过滤),让下游决定

    Args:
        lines: 可迭代的字符串行(如 subprocess.stdout 按行读取)

    Yields:
        ClaudeEvent 实例
    """
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            logger.warning(
                "stream_parser: JSON 解析失败,跳过该行",
                extra={"line_preview": line[:200], "error": str(exc)},
            )
            continue

        if not isinstance(data, dict):
            logger.warning(
                "stream_parser: 解析结果不是 dict,跳过",
                extra={"type": type(data).__name__, "line_preview": line[:200]},
            )
            continue

        event_type = data.get("type")
        if event_type is None:
            logger.warning(
                "stream_parser: 事件缺少 'type' 字段,跳过",
                extra={"keys": list(data.keys()), "line_preview": line[:200]},
            )
            continue

        yield ClaudeEvent(event_type=str(event_type), raw=data)
