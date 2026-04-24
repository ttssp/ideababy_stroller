# Demo 剧本 — Qwen2.5-3B-Instruct + gsm8k-100 · 7-Day Operator Rehearsal

**版本**: 0.1.0 · **对应 spec**: specs/003-pA/spec.md §OQ3 + O1/O4
**关联文件**:
- `run_config.yaml` — 完整 RunConfig 参数
- `expected_metrics.md` — 期望指标与判断标准
- `rehearsal_script.sh` — 7 天自动化演练脚本

---

## 0. 剧本说明

本剧本是 RecallKit v0.1 **操作员第一天体验**的标准演练。目的有两个：

1. **验证 O1**：证明操作员能在 7 个自然日内完成 1 个 baseline + 2 个 LoRA 变体 +
   决策记录，整个流程不超过 7 天。
2. **提供 O4 demo**：给其他人一个真实可复现的参考，哪怕最终 LoRA 未提升 baseline
   （诚实负面 demo）也是合法 ship（D20）。

**重要立场**：RecallKit 是决策工具，不是炼丹工具。本剧本的目的是帮你做出
"LoRA 值不值得继续投入"的决策，而不是保证 LoRA 一定提升。

---

## 1. 研究问题（Research Question）

> LoRA r=16 更新 Qwen2.5-3B-Instruct 的 QKV projection 能否在 gsm8k-100 上
> 相比 baseline 提升 >= 5% accuracy？

**为什么选 Qwen2.5-3B-Instruct**：
- 3B 参数，24GB 4090 单卡 QLoRA 可跑（无 OOM 风险）。
- Tongyi Qianwen License 允许非商业研究使用。
- 公开 gsm8k 基准下 Qwen2.5 系列有 ~41% 的已知 baseline，便于对比。

**为什么选 gsm8k-100**：
- 前 100 条训练数据：1h 内训练完 3 个 epoch（H200 约 25-45min）。
- 前 100 条评测数据（5-shot）：约 15-30min 出结果。
- 小数据集更容易过拟合，便于观察 LoRA 超参对 loss 曲线的影响。

---

## 2. Day-by-Day 剧本

### Day 1：Baseline 评测 + LoRA r=16 假设

**目标**：建立 baseline，启动第一个 LoRA 假设。

**操作步骤**：

```bash
# 步骤 1：确认环境就绪
uv sync --frozen
pars --version  # 确认 CLI 可用

# 步骤 2：启动 baseline + LoRA r=16 run
pars sft start \
    --question "LoRA r=16 更新 QKV projection 能否在 gsm8k-100 上提升 >= 5% accuracy?" \
    --base Qwen/Qwen2.5-3B-Instruct \
    --dataset openai/gsm8k \
    --dataset-split "main[:100]" \
    --lora-rank 16 \
    --lora-alpha 32 \
    --lr 2e-4 \
    --epochs 3 \
    --batch-size 2 \
    --max-seq-len 2048 \
    --eval-tasks gsm8k \
    --usd-cap 10.0 \
    --wall-clock-hours-cap 8.0 \
    --gpu-hours-cap 8.0 \
    --name day1-r16
```

**预期耗时**：25-45min（H200）/ 60-90min（RTX 4090）

**完成后检查**：
- `runs/day1-r16/report.md` 是否存在
- `report.md` 中 baseline accuracy 是否在 0.35-0.50 区间
- LoRA accuracy 是否高于 baseline（即使略微高也是信号）

**看什么指标**：
- `gsm8k/acc_norm` — 主要指标，5-shot exact-match accuracy
- `train_loss` — 训练 loss 是否持续下降（如果 loss 震荡，说明 lr 偏高）
- `eval_loss`（若有）— 是否出现过拟合（eval loss 开始上升而 train loss 继续下降）

---

### Day 2：分析 Day 1 结果，发起 LoRA r=32 假设

**目标**：根据 Day 1 结果决定下一步假设。

**典型 Happy Path 场景**：
- Day 1 baseline acc ≈ 0.41，LoRA r=16 acc ≈ 0.45
- 提升 4%，接近但不满足 +5% 目标
- 决策：提升 rank 到 32，增加模型容量

```bash
# 基于 day1-r16 创建 r=32 变体
pars sft retry \
    --from day1-r16 \
    --hypothesis "r=32 相比 r=16 能在 gsm8k-100 上进一步提升 accuracy，" \
                 "因为更高的 rank 给 QKV projection 更多可学习参数" \
    --lora-rank 32 \
    --lora-alpha 64 \
    --name day2-r32
```

**预期耗时**：25-50min（H200，rank 翻倍训练时间增幅约 10-20%）

---

### Day 3：等待 Day 2 完成 + 初步对比

**目标**：对比 day1-r16 和 day2-r32 结果。

```bash
# 查看两个 run 的对比
pars sft compare day1-r16 day2-r32
```

**输出解读**：
- `compare` 输出 config 差异表（rank 16 vs 32）
- `compare` 输出 metric 差异表（acc、loss、wall_clock）
- 如果 r=32 显著优于 r=16：继续 Day 4 探索 lr 调整
- 如果 r=32 无显著差异：看 Day 5 讨论

---

### Day 4：（可选）LoRA r=16 + lr=5e-5 变体

**目标**：验证"lr 偏高导致 Day 1 不稳定"的备选假设。

```bash
# 从 day1-r16 继承 config，只调 lr
pars sft retry \
    --from day1-r16 \
    --hypothesis "lr=5e-5（原 lr=2e-4 的 1/4）能减少震荡，稳定提升 gsm8k-100 accuracy" \
    --lr 5e-5 \
    --name day4-r16-lowlr
```

---

### Day 5：3-way 对比 + 决策记录

**目标**：对比所有变体，产出最终决策报告。

```bash
# 两两对比
pars sft compare day1-r16 day2-r32
pars sft compare day1-r16 day4-r16-lowlr
pars sft compare day2-r32 day4-r16-lowlr
```

**决策框架**（参考期望指标表）：
- 若最佳变体 acc > baseline + 5%：LoRA 有效，值得继续投入更大数据集
- 若最佳变体 acc <= baseline + 2%：LoRA 对此超参组合无效，记录失败归因
- 若 loss 曲线显示过拟合：数据集 100 条太少，建议 v0.2 扩展至 1000 条

---

### Day 6-7：收尾 + 总结

**目标**：完成所有 report.md，产出决策文档。

```bash
# 确认所有 run 有 report.md
pars sft status --run-id day1-r16
pars sft status --run-id day2-r32

# 手动对比生成总结（若 compare 未自动生成 markdown）
pars sft compare day1-r16 day2-r32
```

**最终产出物检查**：
- [ ] `runs/day1-r16/report.md` 含训练曲线 PNG + 分数对比表 + 失败归因
- [ ] `runs/day2-r32/report.md` 同上
- [ ] `runs/*/failure_attribution.md` 若 LoRA 未提升，有具体归因
- [ ] 决策：记录在 `runs/day2-r32/report.md` 的"结论"节

---

## 3. Happy Path 期望

若硬件和依赖版本正常，期望结果：

| 变体 | gsm8k acc（5-shot/100条） | train_loss 趋势 | wall_clock |
|------|---------------------------|-----------------|------------|
| Qwen2.5-3B baseline | ~0.41 | N/A（无训练） | ~15min eval |
| LoRA r=16（day1） | ~0.45-0.50 | 稳定下降 | ~30-45min |
| LoRA r=32（day2） | ~0.46-0.52 | 稳定下降 | ~35-50min |

注：上述数字来自 Qwen 公开 benchmark 数据估算，非实测保证值。实测结果以
`expected_metrics.md` 为准。

---

## 4. 诚实负面 Demo 路径

如果 LoRA 在 gsm8k-100 上未提升（这是**合法的 demo 结果**）：

**判断标准**：
- LoRA acc <= baseline acc + 1%（在统计误差范围内）
- 或 LoRA loss 曲线震荡无收敛趋势

**应该怎么做**：
1. 不要重跑更多次试图"炼丹"出好结果
2. 在 `failure_attribution.md` 诚实记录：
   - 数据集 100 条可能太少，模型看过的数据不足以迁移
   - 或 LoRA rank 设置不当（过小 = 容量不足 / 过大 = 过拟合）
   - 或 gsm8k 需要更多 few-shot examples（5-shot 不够）
3. 这份"诚实负面 demo"本身就是价值：证明 RecallKit 能客观记录失败

**RecallKit 的立场（D20）**：诚实负面 demo = 合法 ship。

---

## 5. 故障排查

### 5.1 GPU OOM（显存不足）

**症状**：`CUDA out of memory` 错误

**处理方案**（按优先级）：
1. 降低 `batch_size` 到 1（最优先）：
   ```bash
   pars sft start ... --batch-size 1
   ```
2. 降低 `max_seq_len` 到 1024：
   ```bash
   pars sft start ... --max-seq-len 1024
   ```
3. 切换到更小模型（R1 缓解路径）：
   ```bash
   pars sft start ... --base Qwen/Qwen2.5-1.5B-Instruct
   ```
4. 若仍 OOM，使用 TinyLlama 1.1B（最保底）：
   ```bash
   pars sft start ... --base TinyLlama/TinyLlama-1.1B-Chat-v1.0
   ```

### 5.2 Proxy 返回 402/429（预算超限）

**症状**：`[ERROR] 402 Budget exceeded` 或 `429 Too Many Requests`

**原因**：`usd_cap` 被触发，proxy 前置拒绝了请求（C20 设计，非 bug）。

**处理**：
```bash
# 查看当前 run 已用预算
pars sft status --run-id day1-r16
# 如确认预算合理，重新启动 run 并提高 usd_cap
pars sft start ... --usd-cap 20.0
```

### 5.3 ReadonlyFailsClosed（.claude/ 只读保护）

**症状**：`[ERROR] .claude/ fail-closed 保护触发`

**原因**：MacFUSE + bindfs 只读 mount 未生效，CLI 拒绝启动（C21 设计）。

**处理**：参考 `docs/demo-reproduction.md §3` 确认 MacFUSE 安装正确。

### 5.4 Training stuck（卡住）

**症状**：GPU util 长时间为 0，进程存在但不写 checkpoint

**原因**：Stuck 状态机检测到 `truly_stuck > 15min`，CLI 已发 SIGINT。

**处理**：
```bash
# 确认 run 状态
pars sft status --run-id day1-r16
# 若误判，手动解锁
pars unlock --run-id day1-r16
# 重新启动（从 checkpoint 续）
pars sft resume --run-id day1-r16
```

### 5.5 HuggingFace 下载失败

**症状**：`ConnectionError` 或 `HTTPError` 访问 HuggingFace

**注意**：公开模型（Qwen2.5-3B-Instruct / openai/gsm8k）无需 `HF_TOKEN`。

**处理**：
1. 检查网络连接：`curl -I https://huggingface.co`
2. 若需要代理，设置环境变量（非 API key 范围，操作员自行配置）
3. 若模型已下载到本地缓存（`~/.cache/huggingface/`），可离线跑

---

## 6. 成功标准（操作员签字）

当以下所有条件满足，本次 demo 演练视为完成：

- [ ] `runs/day1-r16/report.md` 存在且含完整三节（训练曲线/分数对比/失败归因）
- [ ] `runs/day2-r32/report.md` 存在且含完整三节
- [ ] `pars sft compare day1-r16 day2-r32` 可运行并输出对比表
- [ ] 从 `pars sft start` 首次调用到最后一份 `report.md` 落盘，时间 <= 7 自然日
- [ ] 操作员能用文字说出"为什么选/不选继续扩大数据集"

---

_本剧本对应 spec.md O1 + O4，rehearsal 完成后请在 specs/003-pA/STATUS.md 的 O1
验证行填写实测日期和结论。_
