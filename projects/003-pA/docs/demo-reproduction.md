# Demo 复现操作员手册 — Qwen2.5-3B-Instruct + gsm8k-100

**版本**: 0.1.0 · **对应 spec**: specs/003-pA/spec.md O4 + C9
**关联**: demo/gsm8k-100-qwen3-4b/scenario.md（操作员剧本）
         demo/gsm8k-100-qwen3-4b/expected_metrics.md（期望指标）

---

## 0. 文档目的

本手册是 **O4（"他人本机重现"）的操作参考**。目标：

> 另一位操作员（或你在另一台机器上），在不依赖内部路径、私有数据、
> 特定环境变量的情况下，跟着本手册，能产出 `runs/<id>/report.md`，
> 且结果与原 demo 的 `expected_metrics.md` 吻合（误差 < 10%）。

**本手册不覆盖**：
- 跨机器 checkpoint resume（不支持，见 C22）
- Docker 安装（非目标，见 non-goals.md）
- 多 GPU 训练（v0.1 仅单卡）
- 自动超参搜索（非目标）

---

## 1. 前置条件确认

在开始之前，请确认以下条件全部满足：

### 1.1 硬件检查

```bash
# 确认 NVIDIA GPU 可见
nvidia-smi

# 确认显存 >= 16GB（Qwen2.5-3B-Instruct QLoRA 需要 ~20-23GB）
nvidia-smi --query-gpu=name,memory.total --format=csv
```

若显存不足（< 20GB），降级选项：
- Qwen/Qwen2.5-1.5B-Instruct（~12GB，适合 3090 Ti / A5000）
- TinyLlama/TinyLlama-1.1B-Chat-v1.0（~8GB，适合 RTX 2080Ti）

### 1.2 软件依赖

```bash
# Python 版本
python3 --version  # 需要 3.12.x

# CUDA 版本
nvcc --version     # 需要 12.1+
nvidia-smi | grep "CUDA Version"

# uv 版本
uv --version       # 需要 >= 0.5.0
```

若 uv 未安装：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1.3 API Key 准备

```bash
# 确认 ANTHROPIC_API_KEY 已设置（worker 通过 proxy 调用，key 不进 worker 环境）
echo $ANTHROPIC_API_KEY | head -c 20  # 仅显示前 20 字符，不要完整打印

# 若未设置
export ANTHROPIC_API_KEY=sk-ant-...
```

**HF_TOKEN 非必须**：默认 demo 使用的 Qwen2.5-3B-Instruct 和 openai/gsm8k 均为公开 repo。

---

## 2. 安装步骤

### 2.1 Clone 仓库

```bash
git clone https://github.com/<your-handle>/recallkit.git
cd recallkit
```

**注意**：不要 clone 到含特殊字符或空格的路径。

### 2.2 安装依赖

```bash
# 完全锁定版本安装（--frozen 拒绝升级任何包）
uv sync --frozen

# 安装 pars CLI
uv tool install .

# 验证 CLI 可用
pars --version
pars sft start --help
```

### 2.3 确认关键依赖版本

```bash
# 确认 Unsloth 版本（需要 2024.10+）
uv run python -c "import unsloth; print('unsloth:', unsloth.__version__)"

# 确认 lm-eval 版本
uv run lm_eval --version

# 确认 transformers 版本
uv run python -c "import transformers; print('transformers:', transformers.__version__)"
```

记录上述版本号，用于后续与 expected_metrics.md 的复现对比。

---

## 3. MacFUSE + bindfs 只读 mount 配置（C21，macOS）

**macOS 操作员必须完成此步骤。** Linux 操作员见 §3.2。

RecallKit 要求 `.claude/` 目录以只读方式 mount 到 worker worktree，
防止 worker 意外修改 host Claude 配置（C21 fail-closed 设计）。

### 3.1 macOS：MacFUSE + bindfs

```bash
# 安装 MacFUSE（需要 macOS 14+）
brew install --cask macfuse

# 安装 bindfs
brew install bindfs

# 创建只读 mount 点（装机一次）
mkdir -p ~/.recallkit/readonly-claude

# 创建 mount 脚本（装机一次）
cat > ~/.recallkit/mount-readonly.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
CLAUDE_DIR="$HOME/.claude"
MOUNT_POINT="$HOME/.recallkit/readonly-claude"
if ! mount | grep -q "${MOUNT_POINT}"; then
    bindfs --no-allow-other -p a-w "${CLAUDE_DIR}" "${MOUNT_POINT}"
    echo "[OK] .claude/ 以只读方式 mount 到 ${MOUNT_POINT}"
else
    echo "[SKIP] 已 mount，无需重复操作"
fi
EOF
chmod +x ~/.recallkit/mount-readonly.sh

# 执行 mount（每次重启后需要重新 mount）
~/.recallkit/mount-readonly.sh
```

**验证 mount**：
```bash
# 验证 mount 点只读
touch ~/.recallkit/readonly-claude/test.txt 2>&1 | grep "Permission denied"
# 应该输出 "Permission denied" 说明只读 mount 成功
```

### 3.2 Linux：chattr 不可变 flag

```bash
# 对 .claude/ 设置不可变 flag（需要 root）
sudo chattr -R +i ~/.claude/

# 验证
touch ~/.claude/test.txt 2>&1 | grep "Operation not permitted"
```

### 3.3 若两种方法都不可用

CLI 会拒绝启动并打印明确错误：

```
[ERROR] .claude/ fail-closed 保护触发（C21）
OQ5：工作目录 .claude/ 无法以只读模式挂载，拒绝启动。
请检查文件权限或联系管理员。
```

**处理**：确认 MacFUSE（macOS）或 chattr（Linux）是否正确安装。

---

## 4. 跑第一次 Demo

### 4.1 Day 1：启动 baseline + LoRA r=16

```bash
# 使用演练脚本（推荐）
bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh day1

# 或手动运行命令
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

**预期输出**：

```
[OK] run_id=day1-r16
     final_state=completed
     exit_code=0
     report=runs/day1-r16/report.md
```

### 4.2 验证产出文件

```bash
# 确认 report.md 存在且含必要章节
cat runs/day1-r16/report.md | grep -E "^## (训练曲线|分数对比|失败归因)"

# 确认 metrics.jsonl 有数据
wc -l runs/day1-r16/metrics.jsonl

# 确认训练曲线 PNG 存在
ls runs/day1-r16/artifacts/*.png
```

每份 `report.md` 必须含三节：
- `## 训练曲线` — 含 PNG 引用路径
- `## 分数对比` — 含 baseline acc 和 LoRA acc 的对比表
- `## 失败归因` — 即使成功也需要有此节（"无失败"也是合法内容）

### 4.3 Day 2：LoRA r=32 变体

```bash
bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh day2
```

### 4.4 Compare 决策

```bash
bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh compare
```

---

## 5. 指标对比与验收

### 5.1 与期望指标对比

跑完后，将实测值填入 `demo/gsm8k-100-qwen3-4b/expected_metrics.md` 的"实测值"列。

验收标准（O4 人审）：
- baseline acc 在期望区间 0.38-0.44（若明显低于此，检查 GPU / CUDA 版本）
- LoRA acc 高于或等于 baseline（诚实负面 demo 也算通过，见 D20）
- wall_clock 在合理范围内（4090 < 2h 一次完整 run）

### 5.2 指标偏差处理

若本地指标偏差 >= 10 个百分点：

1. 确认 GPU 型号相同（不同 GPU 的 4-bit 量化精度有差异）
2. 确认 CUDA 版本 >= 12.1
3. 确认 Unsloth 版本 >= 2024.10
4. 确认 Python 版本 = 3.12.x（不是 3.11 或 3.13）
5. 若仍偏差，在 `expected_metrics.md` 的备注栏记录实测值和可能原因

---

## 6. 常见问题

### Q: 第一次运行需要下载哪些数据？

- Qwen2.5-3B-Instruct 权重（约 6-8GB）：从 HuggingFace Hub 下载，缓存到 `~/.cache/huggingface/`
- openai/gsm8k 数据集（约 10MB）：同上
- Unsloth 依赖（含 bitsandbytes CUDA kernel）：首次约 2-5min

首次运行通常需要 30-60min 仅用于下载。后续跑相同模型，下载时间可忽略。

### Q: 如何查看当前 run 状态？

```bash
pars sft status --run-id day1-r16
```

### Q: 训练中断后如何续跑？

```bash
# 仅限同机重启（跨机器 resume 不支持，C22）
pars sft resume --run-id day1-r16
```

### Q: 如何在 H200 等远程 GPU 上重跑？

见 [docs/h200-rsync-playbook.md](h200-rsync-playbook.md)。
注意：这是"远端重跑训练"，不是跨机器 resume。

### Q: run 目录在哪？

```
runs/<run-id>/
  config.yaml           RunConfig（操作员输入参数）
  state.json            当前状态（training / completed / failed 等）
  metrics.jsonl         实时指标流（每步追加）
  report.md             最终决策报告（完成后）
  failure_attribution.md（若失败）
  artifacts/
    loss_curve.png      训练曲线 PNG
    pip_freeze.txt      pip freeze 版本快照
```

checkpoint 存在 `checkpoints/<run-id>/`（worktree 外，不入 git）。

---

## 7. O4 验收签字

当以下条件全部满足，操作员在 `specs/003-pA/STATUS.md` O4 行签字：

- [ ] 另一台机器（或回滚 worktree）成功产出 `runs/day1-r16/report.md`
- [ ] `report.md` 含三节（训练曲线/分数对比/失败归因）
- [ ] 实测 baseline acc 与 `expected_metrics.md` 误差 < 10 个百分点
- [ ] 实测 LoRA acc 高于或等于 baseline（或有诚实失败归因）
- [ ] `demo/gsm8k-100-qwen3-4b/expected_metrics.md` 实测值已填写

_本文档不含任何内部路径（如 /Users/admin/...）、私有 checkpoint 链接或内部 run ID。_
