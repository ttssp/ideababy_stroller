"""
pars.report.failure_prompt — 给 worker 的失败归因 prompt 模板。

结论：D16 缓解中 worker-facing 侧。若不给 worker 明确的 prompt 引导，
      worker 会输出"可能是数据问题，也许超参有问题"（崩塌模式）；
      本模块通过 Jinja2 模板 + 禁用词列表 + 示例对比消除这种倾向。

字段来源：
  - tasks/T020.md — failure_prompt.py 的契约和禁用词列表
  - architecture.md §9 — failure_attribution.md 半结构化格式和归因枚举

导出：
  - FAILURE_PROMPT_TEMPLATE : str — Jinja2 模板原始字符串（中文为主）
  - render_failure_prompt(run_id, baseline_score, lora_final_score) -> str
"""

from __future__ import annotations

from jinja2 import Environment, Undefined


# ---------------------------------------------------------------------------
# Jinja2 模板：给 worker 的失败归因写作引导
# ---------------------------------------------------------------------------

FAILURE_PROMPT_TEMPLATE: str = """\
# 失败归因写作要求 · Run {{ run_id }}

你是 RecallKit LoRA 微调 worker，需要分析本次训练为何未达到基线提升目标，
并填写结构化的 failure_attribution.md 报告。

---

## 核心数据参考

| 指标 | 数值 |
|------|------|
| Baseline 分数 | {{ baseline_score }} |
| LoRA 最终分数 | {{ lora_final_score }} |
| 分数差距 | {{ "%.4f"|format(lora_final_score - baseline_score) }} |

---

## 必须填写的字段

按以下格式逐项填写（缺一不可）：

```markdown
# Failure attribution · {{ run_id }}

## 必填字段
- **假设**：[你原本期望发生什么？含具体目标 metric 值，≥20 字符]
- **观察**：[实际发生了什么？必须引用具体 metric 数字，如 accuracy=0.41, loss=1.23, epoch 3 等，≥30 字符]
- **归因**：
  - [x] [从下方归因枚举中选一或多项，打 x 勾选]
- **下一步建议**：[可执行的具体改动，如 "将 lr=2e-4 改为 lr=5e-5" 或 "增加 epoch=5"]

## 自由叙述（可选，但鼓励）
[reasoning chain、异常发现、新假设]
```

---

## 归因枚举（必选一项以上）

请从以下枚举中选择最符合的归因类别，在 `[ ]` 中填入 `x`：

| 枚举值 | 中文描述 | 适用场景 |
|--------|----------|----------|
| DATA_FORMAT | 数据格式错误 | 具体哪条/哪种格式不符合预期 |
| LR_TOO_HIGH | 学习率太大 | loss 曲线震荡、不收敛或初期下降后反弹 |
| LR_TOO_LOW | 学习率太小 | loss 长时间不下降、训练缓慢无进展 |
| DIST_DRIFT | 训练/eval 分布漂移 | eval 集与训练集来自不同分布 |
| BASELINE_STRONG | 基线本身够强 | LoRA 的提升空间有限，基线已接近天花板 |
| EPOCH_NOT_ENOUGH | 训练 epoch 不足 | loss 仍在下降但 epoch 已到上限 |
| LORA_RANK_LOW | LoRA rank 不足 | 模型容量不足以捕捉任务模式 |
| OOM | 显存 OOM 导致 batch 太小 | 实际 batch_size 小于预期，训练不稳定 |
| OTHER | 其他原因 | **必须**在 causes_detail 中详细说明 |

---

## 禁止使用的措辞（黑名单）

以下措辞**禁止**出现在 observation 和 causes_detail 中：

- **可能是** — 你在猜测，而非分析。请引用具体数字。
- **也许** — 同上。模糊推断不是归因。
- **大概** — 同上。请给出可验证的观察。
- **不确定** — 如不确定，请选 OTHER 并说明需要哪些额外信息。

如果你的 observation 或 next_steps 中包含以上词汇，schema validator 将拒绝报告。

---

## 示例对比（参考）

### 不合格示例（Bad）— 会被 schema gate 拒绝

```markdown
- **假设**：希望效果变好
- **观察**：LoRA 训练完成后评测结果比预期差，可能是数据问题，也许超参有问题
- **归因**：
  - [x] 其他
- **下一步建议**：继续尝试调超参，也许可以改改数据
```

**为什么拒绝：**
- observation 无数字（违反规则1）
- next_steps 无具体关键词（违反规则2）
- OTHER 未填 causes_detail（违反规则3）
- 使用了禁用词（可能是、也许）

---

### 合格示例（Good）— 通过 schema gate

```markdown
- **假设**：预计 LoRA rank=8 微调后 gsm8k 准确率从 baseline 0.45 提升至 0.55 以上
- **观察**：LoRA final epoch accuracy=0.41，低于 baseline 0.45；loss 曲线在 epoch 2 出现拐点后反弹至 1.45，判断为 lr 过大导致梯度震荡
- **归因**：
  - [x] 学习率太大 / LR_TOO_HIGH
- **下一步建议**：将 lr=2e-4 降低至 lr=5e-5，同时将 warmup_steps=100 以稳定初期训练；epoch=3 观察 loss 收敛趋势
```

**为什么合格：**
- observation 含具体数字（0.41, 0.45, epoch 2, 1.45）
- next_steps 含明确的 hyperparam 变更（lr=, warmup_steps=, epoch=）
- 无禁用词

---

## 注意事项

1. **observation 必须含数字** — 引用 `accuracy=`、`loss=`、`epoch N`、`grad_norm` 等可验证事实
2. **next_steps 必须可执行** — 每项应含具体的 hyperparam 赋值或数据/模型变更
3. **OTHER 需要详细叙述** — 选 OTHER 后必须在 `causes_detail` 或自由叙述中说明原因
4. **schema validator 是 strict gate** — 不合格的报告会被 O2 gate 拒绝，需重写后才能归档
"""


# ---------------------------------------------------------------------------
# 渲染函数：将模板填入实际运行数据
# ---------------------------------------------------------------------------

# 配置 Jinja2 Environment（使用 StrictUndefined 防止变量未定义时静默失败）
_JINJA2_ENV = Environment(
    undefined=Undefined,
    autoescape=False,
    keep_trailing_newline=True,
)


def render_failure_prompt(
    run_id: str,
    baseline_score: float,
    lora_final_score: float,
) -> str:
    """渲染 worker 失败归因 prompt，填入运行特定数据。

    结论：给 worker 提供个性化的 prompt，含本次 run 的实际 baseline 和 lora 分数，
          减少 worker 在归因时需要查找的上下文。

    参数：
        run_id          : 本次 run 的 ULID（如 01KPZSDEE8VWSDS83ZS9WHKWES）
        baseline_score  : 基线模型在 eval 上的得分（浮点数，如 0.45）
        lora_final_score: LoRA 微调后 final epoch 在 eval 上的得分（如 0.41）

    返回：
        str — 渲染后的 prompt 全文，直接可作为 LLM system prompt 或 user message 使用
    """
    template = _JINJA2_ENV.from_string(FAILURE_PROMPT_TEMPLATE)
    return template.render(
        run_id=run_id,
        baseline_score=baseline_score,
        lora_final_score=lora_final_score,
    )
