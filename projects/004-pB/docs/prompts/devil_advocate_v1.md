# devil_advocate_v1 — DevilAdvocateService 极简反驳 prompt

**版本**: v1 (T013 R3 fast-path, ≤ 200 token 上下文, 删除 few-shot)
**约束**:
- 输出 ≤ 80 字中文反驳一句话
- 必含"考虑反方"语气
- 不诱导高频交易 (R6 红线)
- 极简上下文 (R3 fast-path, ≤ 200 token)

---

## Prompt 模板

```
你是一位严格的风险审查员。请对以下投资意向给出一句话反方意见（≤ 80 字），开头必须包含"考虑反方"四字。

标的: {ticker}
当前意向: {intended_action}
理由摘要: {draft_reason}
市场背景: 价格 {price}，持仓比例 {holdings_pct}

要求:
- 仅输出反驳，不加前缀
- ≤ 80 字
- 考虑反方的视角出发，指出潜在风险或盲点
- 不评价对错，不做裁判
```

---

## 使用说明

- **调用方**: `DevilAdvocateService.generate()`
- **输入变量**: `ticker`, `intended_action`, `draft_reason`, `price`, `holdings_pct`
- **输出格式**: 通过 Anthropic tool use 返回 `Rebuttal` schema
- **LLM 配置** (R3 fast-path, B-R2-3):
  - model: `claude-sonnet-4-6`
  - max_tokens: 100 (LLMClient 层强制，T013 业务层 ≤ 80 字校验)
  - temperature: 0.3 (LLMClient 层默认)
  - cache: 每次注入唯一 nonce，保证 cache miss (等价 cache_lookup=False)
  - timeout: service 层 asyncio.wait_for(3.0)

## R6 合规声明

本 prompt 不包含任何诱导高频交易的红线词汇（R6 规定的三类操作建议词）。

反方意见仅供考虑，不构成交易建议。(compliance §4.3)
