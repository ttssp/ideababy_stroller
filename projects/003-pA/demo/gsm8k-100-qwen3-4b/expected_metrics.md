# 期望指标 — Qwen2.5-3B-Instruct + gsm8k-100 Demo

**状态**: 基于公开数据预估（T027 实测前的参考值）
**更新时间**: 2026-04-24（初稿，操作员实测后更新）
**数据来源**:
- Qwen 官方发布的 gsm8k benchmark 报告（2024Q4）
- Unsloth 社区测试（4090 24GB QLoRA 场景）
- LM Eval Harness gsm8k 5-shot 标准评测结果

---

## 0. 重要声明

**请先读此节再看数字。**

1. 下表数字来自 Qwen 官方发布报告和社区测试估算，**不是本机实测结果**。
2. 操作员在实际跑完后，应将"实测结果"一列填入对应表格，留档复现参考。
3. 若你本地跑出的 baseline accuracy 偏差 >= 10 个百分点（例如期望 0.41，
   实测 0.30 或 0.55），请检查：
   - GPU 型号（4090 vs A100 量化精度略有差异）
   - CUDA 版本（建议 12.1+，Unsloth 依赖 CUDA kernel）
   - Unsloth 版本（确认 `uv run python -c "import unsloth; print(unsloth.__version__)"` 在 2024.10+）
   - 是否使用了 4-bit 量化（`load_in_4bit=True`，显存节约但精度略降）
4. gsm8k-100（前 100 条）与 gsm8k 全集（1319 条 test）结果有差异属正常，
   小样本评测噪声较大（1 条 = 1% 的准确率变化）。

---

## 1. Baseline 期望指标

**场景**：Qwen2.5-3B-Instruct，无 LoRA，直接 5-shot eval on gsm8k-100

| 指标 | 期望值（估算） | 实测值（操作员填入） |
|------|---------------|---------------------|
| `gsm8k/acc_norm` (5-shot, 100条) | 0.38 - 0.44 | — |
| `gsm8k/exact_match` | 0.38 - 0.44 | — |
| Eval wall_clock | ~15-20min (H200) / ~25-40min (4090) | — |
| GPU 显存峰值 | ~18-22GB (4bit QLoRA 加载) | — |
| API USD 消耗 | < $0.10（仅 worker LLM 调用） | — |

**注**：官方 Qwen2.5-3B-Instruct 在 gsm8k 全集 0-shot 约 75%，5-shot 约 79%。
此处 100 条小样本评测噪声大，期望 acc 偏低（0.38-0.44 为保守估算，实测可能更高）。

---

## 2. LoRA SFT 期望指标（r=16，day1）

**场景**：Qwen2.5-3B-Instruct + LoRA r=16/alpha=32，
        gsm8k-100 训练 3 epochs，lr=2e-4，batch_size=2

| 指标 | 期望值（估算） | 实测值（操作员填入） |
|------|---------------|---------------------|
| `gsm8k/acc_norm` (5-shot, 100条 eval) | 0.44 - 0.52 | — |
| 相对 baseline 提升 | +3% - +10% | — |
| 最终 train_loss | 0.5 - 1.2 | — |
| loss 曲线趋势 | 单调下降（若震荡，lr 偏高） | — |
| Training wall_clock | ~25-35min (H200) / ~60-90min (4090) | — |
| GPU 显存峰值（训练中） | ~20-23GB (4bit QLoRA) | — |
| API USD 消耗 | $0.50 - $1.20 | — |

**对 +5% 目标的判断**：
- acc >= 0.46（即 baseline ~0.41 + 5%）：假设成立，LoRA 有效
- acc < 0.46 但趋势向上：可能 epoch 不足，或需要更多训练数据
- acc <= baseline：失败，见失败归因节

---

## 3. LoRA SFT 期望指标（r=32，day2）

**场景**：Qwen2.5-3B-Instruct + LoRA r=32/alpha=64，
        其余参数同 day1

| 指标 | 期望值（估算） | 实测值（操作员填入） |
|------|---------------|---------------------|
| `gsm8k/acc_norm` (5-shot, 100条 eval) | 0.45 - 0.55 | — |
| 相对 r=16 提升 | +1% - +5%（边际递减） | — |
| Training wall_clock | ~30-40min (H200) / ~70-100min (4090) | — |
| GPU 显存峰值 | ~21-24GB（rank 翻倍显存略增） | — |
| API USD 消耗 | $0.50 - $1.50 | — |

**预期规律**：rank 翻倍通常给模型更多容量，但在 100 条小数据集下容易过拟合。
若 r=32 的 eval loss 早于 r=16 上升，说明过拟合，r=16 更合适。

---

## 4. 完整演练（3 个 run）汇总

**3 次 run 对比决策段落**（操作员实测后填写）：

```
run_id      | variant          | baseline_acc | lora_acc | delta | wall_clock | usd
------------|------------------|-------------|---------|-------|------------|------
day1-r16    | r=16/lr=2e-4     |  —          |  —      |  —    |  —         |  —
day2-r32    | r=32/lr=2e-4     |  —          |  —      |  —    |  —         |  —
day4-lowlr  | r=16/lr=5e-5     |  —          |  —      |  —    |  —         |  —
```

**决策建议框架**：

- delta >= +5%：LoRA 假设成立。建议 v0.2 阶段扩大训练数据至 gsm8k 全量（7473条）。
- +2% <= delta < +5%：LoRA 有边际效果，但样本量不足以确认。可额外跑一次 5-epoch 验证。
- delta < +2%：LoRA 在 100 条数据规模下无统计意义的提升。建议先扩大数据再继续炼丹。
- delta < 0：LoRA 造成退步，训练过拟合或超参设置问题。见失败归因。

---

## 5. 失败归因候选（若 LoRA 未提升）

以下是最常见的失败原因（供 worker 和操作员参考）：

| 失败模式 | 信号 | 根本原因 | 建议下一步 |
|----------|------|----------|------------|
| 过拟合 | eval_loss 上升，train_loss 下降 | 100 条太少，模型记住了训练集 | 增加数据量（>=1000条），或用早停 |
| 欠拟合 | loss 居高不下，acc 无变化 | lr 太低，或 epoch 不足 | 提高 lr 到 5e-4，或增加 epoch 到 5 |
| 收敛不稳定 | loss 震荡，无单调趋势 | lr 太高（2e-4 对 3B 可能偏高） | 降低 lr 到 5e-5，或 linear warmup |
| 评测噪声 | acc 波动 ±5%，无规律 | 100 条 eval 噪声大（1条=1%） | 增加 eval 样本量或重复 3 次 eval 取均值 |
| 任务不匹配 | SFT 数据格式与 gsm8k 格式不符 | 训练时的 answer format 与 eval 时不一致 | 检查 lora_script.py 的 data formatting |

---

## 6. 硬件参考配置

| 配置 | Baseline Eval | LoRA SFT（r=16，3 epochs） | 总 wall_clock |
|------|--------------|---------------------------|--------------|
| H200 80GB（单卡） | ~15min | ~25-35min | ~40-50min |
| RTX 4090 24GB（单卡） | ~25-40min | ~60-90min | ~85-130min |
| RTX 3090 24GB（单卡） | ~35-50min | ~80-120min | ~115-170min |
| RTX 2080Ti 11GB（单卡） | OOM 风险，需降模型 | 建议换 Qwen2.5-1.5B | N/A |

注：H200 数字基于 Unsloth 官方 benchmark 估算，非 RecallKit 实测数据。

---

## 7. 版本锁定与复现说明

为确保他人能复现本 demo 指标，以下版本信息必须在实测时记录：

| 软件 | 版本（操作员填入） |
|------|------------------|
| Python | — |
| CUDA | — |
| Unsloth | — |
| transformers | — |
| peft | — |
| lm-eval | — |
| GPU 型号 | — |
| RecallKit | 0.1.0.dev0 |

操作员实测后，请运行 `uv run pip freeze > runs/day1-r16/artifacts/pip_freeze.txt`
并将关键版本号填入上表。

---

_指标预估来源：Qwen 官方技术报告（2024）、Unsloth GitHub benchmark（2025-Q1）、
LM Eval Harness gsm8k 标准评测。实测数值以 `runs/<run-id>/report.md` 为准。_
