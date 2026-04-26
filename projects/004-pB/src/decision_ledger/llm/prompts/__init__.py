"""
Prompt 模板加载 — T005
结论: PromptTemplate.load() 从 docs/prompts/ 读取版本化 prompt 文件
细节:
  - 文件命名规范: <name>_v<N>.md，如 conflict_v1.md
  - 版本号 N 在任何 prompt 内容变更时必须递增 (D11: cache key 含 version)
  - load() 返回 str，调用方负责填充变量 (str.format_map 或模板引擎)
  - 默认搜索路径: 相对于项目根的 docs/prompts/ 目录
  - FileNotFoundError 时给出有用错误信息，包含期望路径
"""

from __future__ import annotations

from pathlib import Path

# 默认 prompt 目录（相对于此文件的 ../../../../docs/prompts/）
_DEFAULT_PROMPT_DIR = Path(__file__).parent.parent.parent.parent.parent / "docs" / "prompts"


class PromptTemplate:
    """
    版本化 Prompt 模板加载器。

    命名规范: docs/prompts/<name>_v<N>.md
    版本号规则:
      - 任何 prompt 内容变更 → N 递增
      - 版本号是 LLM cache key 的组成部分 (D11)
      - 不递增版本号而修改 prompt = cache 污染 bug

    用法:
        template = PromptTemplate.load("conflict", "1")
        prompt = template.format(ticker="TSM", week="2026-W17")
    """

    def __init__(self, content: str, name: str, version: str) -> None:
        self.content = content
        self.name = name
        self.version = version

    @classmethod
    def load(
        cls,
        name: str,
        version: str,
        prompt_dir: Path | None = None,
    ) -> PromptTemplate:
        """
        从 docs/prompts/<name>_v<version>.md 加载 prompt 模板。

        Args:
            name: prompt 名称，如 "conflict"
            version: 版本号，如 "1"（不含 v 前缀）
            prompt_dir: 自定义 prompt 目录（测试用），默认 docs/prompts/

        Returns:
            PromptTemplate 实例

        Raises:
            FileNotFoundError: prompt 文件不存在，错误信息含期望路径
        """
        search_dir = prompt_dir or _DEFAULT_PROMPT_DIR
        filename = f"{name}_v{version}.md"
        filepath = search_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(
                f"Prompt 模板不存在: {filepath}\n"
                f"命名规范: docs/prompts/<name>_v<N>.md\n"
                f"请检查名称 '{name}' 和版本 '{version}' 是否正确。"
            )

        content = filepath.read_text(encoding="utf-8")
        return cls(content=content, name=name, version=version)

    def format(self, **kwargs: str) -> str:
        """
        填充 prompt 模板变量。
        使用 str.format_map 语法: {ticker}, {week_id} 等。

        Raises:
            KeyError: 模板含未提供的变量
        """
        return self.content.format_map(kwargs)

    @property
    def template_version(self) -> str:
        """
        返回 cache key 用的版本字符串 (格式: <name>_v<version>)。
        用于 LLMClient.call(template_version=...) 参数。
        """
        return f"{self.name}_v{self.version}"
