# Prompt 版本化规范

## 目录结构

```
docs/prompts/
├── README.md              # 本文件：规范说明
├── conflict_v1.md         # conflict advisor prompt 版本 1
├── conflict_v2.md         # conflict advisor prompt 版本 2（内容变更后递增）
└── ...
```

## 命名规范

格式: `<name>_v<N>.md`

- `<name>`: prompt 功能名称（小写字母、下划线），如 `conflict`、`advisor`
- `<N>`: 正整数版本号，从 1 开始，每次内容变更递增

## 版本号规则（关键，勿跳过）

**任何 prompt 内容变更都必须递增版本号 N。**

原因：版本号是 LLM 文件缓存的 key 组成部分（D11 规范）。
若 prompt 内容改变但版本号不变，缓存会继续返回旧 prompt 的结果，产生污染。

正确工作流：
1. 编辑 `conflict_v1.md` → 创建 `conflict_v2.md`（保留 v1 用于 diff）
2. 更新调用代码：`PromptTemplate.load("conflict", "2")`
3. 运行 `LLMCache.invalidate("conflict_v1")` 清除旧缓存（可选，会自动过期）

## 使用方式

```python
from decision_ledger.llm.prompts import PromptTemplate

# 加载 docs/prompts/conflict_v1.md
template = PromptTemplate.load("conflict", "1")

# 填充变量（str.format 语法）
prompt = template.format(ticker="TSM", week_id="2026-W17", ...)

# template_version 用于 LLMClient.call(template_version=...)
# 格式: "conflict_v1"
print(template.template_version)  # → "conflict_v1"
```

## Prompt 文件格式

使用 `{variable_name}` 占位符：

```markdown
# 周期冲突分析

分析 {ticker} 在 {week_id} 的周期冲突情况：

市场数据:
{market_context}

请分析：
...
```

## 禁止事项

- 不得修改已有版本的 prompt 内容（应创建新版本）
- 不得跳版本号（如从 v1 跳到 v3）
- 不得在 prompt 文件中硬编码机密信息

## 与 LLM 缓存的关系

缓存键 = `sha256(advisor_week_id | ticker | template_version | model)`

其中 `template_version` 格式为 `<name>_v<N>`（如 `conflict_v1`）。
版本号变更 → 缓存自动失效（旧 key 不匹配新 key）。
