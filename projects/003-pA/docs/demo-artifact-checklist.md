# Demo Artifact 分发检查清单 — compliance §4.4

**版本**: 0.1.0 · **对应 spec**: specs/003-pA/compliance.md §4.4
**关联**: demo/gsm8k-100-qwen3-4b/

---

## 用途

本清单用于在 **分发 demo artifact** 之前（如合并到 main branch、发布 release、
向他人分享演练包）确认所有合规要求已满足。

合规要求来源：`specs/003-pA/compliance.md §4.4`（Demo artifact 分发检查）。

**何时使用**：
- 将 demo/ 目录提交到 public repo 之前
- 向 O4 操作员（他人）发送演练包之前
- 发布 RecallKit v0.1.0 正式版 release 之前

---

## §4.4.1 数据集与模型 HF Repo 合规

| 检查项 | 标准 | 状态 |
|--------|------|------|
| base model repo ID 为公开 repo | `Qwen/Qwen2.5-3B-Instruct` 是公开 HF repo，无需 HF_TOKEN | [ ] |
| dataset repo ID 为公开 repo | `openai/gsm8k` 是公开 HF repo，无需 HF_TOKEN | [ ] |
| 无私有或内部 HF repo ID | 检查 run_config.yaml 和所有 .md 文件中的 HF ID | [ ] |
| 降级模型备选均为公开 repo | `Qwen/Qwen2.5-1.5B-Instruct` + `TinyLlama/TinyLlama-1.1B-Chat-v1.0` 均为公开 repo | [ ] |

**验证命令**：
```bash
# 确认公开 repo 无需 token 即可访问
curl -s "https://huggingface.co/api/models/Qwen/Qwen2.5-3B-Instruct" | grep '"private"' | grep 'false'
curl -s "https://huggingface.co/api/datasets/openai/gsm8k" | grep '"private"' | grep 'false'
```

---

## §4.4.2 隐私与路径合规

| 检查项 | 标准 | 状态 |
|--------|------|------|
| 无个人身份信息（PII）在 expected_metrics.md | 无用户名、机器名、email 等信息 | [ ] |
| 无硬编码本地路径（如 /Users/admin/...）在所有 demo/ 文档 | 所有路径均为相对路径或 `~/<path>` 格式 | [ ] |
| 无内部路径在 docs/demo-reproduction.md | 文件中不含 /Users/admin/ 等私有路径 | [ ] |
| 无内部 run ID（如公司内部实验 run ID）在文档中 | demo 中的 run ID（day1-r16、day2-r32 等）均为通用名称 | [ ] |

**验证命令**：
```bash
# 扫描所有 demo/ 和 docs/ 文件，确认无内部路径
rg '/Users/' projects/003-pA/demo/ projects/003-pA/docs/ && echo "FAIL: 发现内部路径" || echo "OK: 无内部路径"

# 扫描是否有 email 或用户名
rg '@' projects/003-pA/demo/ projects/003-pA/docs/ | grep -v '@h200-host' && echo "WARN: 请检查" || echo "OK"
```

---

## §4.4.3 Git 仓库内容合规

| 检查项 | 标准 | 状态 |
|--------|------|------|
| `.safetensors` 文件不在 git 中 | LoRA adapter 权重不入 git | [ ] |
| `.bin` 模型文件不在 git 中 | 基础模型权重不入 git | [ ] |
| `checkpoints/` 目录在 .gitignore | `checkpoints/<run-id>/` 不入 git | [ ] |
| `runs/` 目录的实测数据不入 git | 训练产出（metrics.jsonl、state.json、artifacts/）不入 git | [ ] |
| `.env` 文件不在 git 中 | API key 等敏感配置不入 git | [ ] |

**验证命令**（在 recallkit/ 仓库根目录执行）：
```bash
# 确认 .gitignore 覆盖关键路径
grep -E '(safetensors|\.bin|checkpoints/|runs/|\.env)' .gitignore | head -10

# 确认 git 中无模型权重文件
git ls-files -- '*.safetensors' '*.bin' | head -5 && echo "FAIL: 发现权重文件" || echo "OK"
```

---

## §4.4.4 基础模型许可证合规

| 模型 | 许可证 | 商业使用 | 要求 |
|------|--------|----------|------|
| Qwen2.5-3B-Instruct | Tongyi Qianwen License | 允许（满足条件） | 保留许可证声明；不可将模型 API 服务化 |
| Qwen2.5-1.5B-Instruct | Tongyi Qianwen License | 允许（满足条件） | 同上 |
| TinyLlama-1.1B | Apache 2.0 | 允许 | 保留 Apache 2.0 声明 |

| 检查项 | 标准 | 状态 |
|--------|------|------|
| README.md 含基础模型许可证声明 | 链接到 Qwen 许可证 + Apache 2.0 | [ ] |
| 不以 API 服务化方式分发微调后的 Qwen | v0.1 无推理 API，不涉及 | [ ] |
| LoRA adapter 若发布，附带原始模型许可证声明 | v0.1 不分发 adapter，标记为待办 | [ ] |

**验证命令**（在 recallkit/ 仓库根目录执行）：
```bash
# 确认 README.md 含许可证相关链接
grep -i 'tongyi\|license\|apache\|许可' README.md
```

---

## §4.4.5 LLaMA 变体许可证合规（若使用）

本 demo 的默认模型链（Qwen2.5-3B → Qwen2.5-1.5B → TinyLlama）**不含 LLaMA 变体**，
无需 Meta LLaMA License 检查。

若将来需要使用 LLaMA 变体：

| 检查项 | 标准 |
|--------|------|
| Meta LLaMA Community License Agreement 已接受 | 操作员已在 HF 页面接受 |
| HF_TOKEN 已配置（LLaMA 模型为 gated repo） | `export HF_TOKEN=hf_...` |
| README 含 LLaMA 许可证声明链接 | 链接到 meta-llama/Meta-Llama-3 |
| 微调模型不得用于 Meta 禁止的用途 | 参考 Meta LLaMA Use Policy |

---

## §4.4.6 LoRA Adapter 分发说明

**v0.1.0 不分发微调后的 LoRA adapter 权重。**

若未来版本需要分发 LoRA adapter（如作为 HuggingFace Hub 上的 model card），
需补充以下检查：

| 检查项 | 标准 |
|--------|------|
| adapter 配套 README 含基础模型声明 | 明确 "base model: Qwen/Qwen2.5-3B-Instruct" |
| adapter 许可证与基础模型许可证兼容 | Tongyi Qianwen License 下发布 |
| 无训练数据 PII 泄漏（membership inference 风险） | 确认 gsm8k 是公开数据集，无用户隐私数据 |
| 不含基础模型全量权重（仅 LoRA delta） | adapter 仅含 delta，不含合并后权重 |
| model card 含 gsm8k eval 结果 | 与 expected_metrics.md 对齐 |

---

## §4.4.7 metrics 数据合规

| 检查项 | 标准 | 状态 |
|--------|------|------|
| metrics.jsonl 不含 PII | 每行仅含 step、loss、acc 等数值指标 | [ ] |
| metrics.jsonl 不含内部路径 | 无 /Users/admin/... 等路径 | [ ] |
| expected_metrics.md "实测值" 列空白（初始状态）| 操作员实测后才填入，初始为 "—" | [ ] |
| 不将真实 run 数据伪装为 expected_metrics | 期望值来源在文件开头声明 | [ ] |

---

## 使用方法

### 分发前核查流程

1. 逐条确认上述 [ ] 项目，全部打勾后方可分发。
2. 若有任何 FAIL，先解决再重新核查。
3. 核查完成后，在 `specs/003-pA/STATUS.md` 的 C-compliance 行记录检查日期。

### 自动化扫描（辅助，非替代）

```bash
# 一键扫描常见问题（在 recallkit/ 仓库根目录执行）
echo "=== 内部路径扫描 ==="
rg '/Users/|/home/[a-z]' demo/ docs/ && echo "FAIL: 发现潜在内部路径" || echo "OK"

echo "=== git 中的权重文件扫描 ==="
git ls-files -- '*.safetensors' '*.bin' && echo "FAIL: 发现权重文件" || echo "OK"

echo "=== .gitignore 覆盖检查 ==="
grep "checkpoints/" .gitignore && echo "OK" || echo "WARN: checkpoints/ 可能未在 .gitignore 中"

echo "=== runs/ gitignore 检查 ==="
grep "^runs/" .gitignore && echo "OK" || echo "WARN: runs/ 可能未在 .gitignore 中"
```

### 负责人

本清单的**最终判断**由操作员（人类）完成。自动化扫描仅作辅助参考。
合规决策不由 AI agent 代替操作员做出。

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 0.1.0 | 2026-04-24 | 初稿，对应 compliance.md §4.4 |

---

_本文档对应 specs/003-pA/compliance.md §4.4（Demo artifact 分发检查）。_
_RecallKit v0.1.0.dev0 · 核查完成后请在 specs/003-pA/STATUS.md 记录。_
