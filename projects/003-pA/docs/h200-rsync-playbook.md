# H200 远端 GPU 重跑训练 Playbook — C9 + C22

**版本**: 0.1.0 · **对应 spec**: specs/003-pA/spec.md C9 / C22 / R10
**关联**: demo/gsm8k-100-qwen3-4b/scenario.md

---

## 重要声明（请先读此节）

**`pars sft resume` 不支持跨机器恢复（C22）。**

本 Playbook 教你如何把训练任务从本地机器（如 RTX 4090）迁移到远端 GPU（如 H200）重新运行，
或者将 H200 上的产出结果同步回本地审阅。

**这不是 "跨机器 resume"**，而是：

- **远端重跑（Re-run on remote）**：在 H200 上重新跑一个完整 run，
  从头开始训练（不续接本地 checkpoint）。
- **产出同步（Artifact sync）**：把 H200 上生成的 `runs/<run-id>/`
  rsync 回本地，用于审阅 `report.md`、`metrics.jsonl` 等文件。

如需同机恢复训练（如 4090 上中断后续跑），见：
```bash
pars sft resume --run-id <run-id>   # 仅限同一台机器
```

---

## 0. 适用场景

| 场景 | 本 Playbook 是否适用 |
|------|----------------------|
| 本地 4090 + 希望在 H200 跑更快 | **是** — 见 §1-3 |
| 本地跑到一半，想在远端继续 | **否** — C22 明确不支持，需重跑 |
| 把 H200 的 report.md 拉回本地 | **是** — 见 §4 |
| 自动化 CI/CD 触发远端训练 | 不在 v0.1 范围 |

---

## 1. 前置条件

### 1.1 本地机器

```bash
# 确认 rsync 可用（macOS/Linux 预装）
rsync --version

# 确认 SSH 可以免密连接到 H200
ssh user@h200-host "nvidia-smi | head -5"
```

若 SSH 未配置免密：

```bash
ssh-keygen -t ed25519 -C "recallkit-h200"
ssh-copy-id user@h200-host
```

### 1.2 远端 H200

```bash
# 确认 RecallKit 已在 H200 安装（方式同本地）
ssh user@h200-host "pars --version"

# 确认 H200 显存充足
ssh user@h200-host "nvidia-smi --query-gpu=name,memory.total --format=csv"
# 期望：NVIDIA H200, 80000 MiB（或 SXM 变体）
```

---

## 2. 把 RunConfig 推送到 H200

不需要推送 checkpoint，只需要把 run 配置文件（或等效 CLI 参数）传过去。

### 2.1 方式 A：rsync 整个 repo（推荐）

```bash
# 仅推送代码和配置，不推送 runs/（含 checkpoint）
rsync -avz --exclude='.git' \
          --exclude='runs/' \
          --exclude='checkpoints/' \
          --exclude='__pycache__/' \
          --exclude='*.pyc' \
          --exclude='.venv/' \
          /path/to/recallkit/ \
          user@h200-host:/remote/path/recallkit/
```

### 2.2 方式 B：只推送 run_config.yaml

```bash
# 若 H200 已有代码，只需同步配置
rsync -avz \
    /path/to/recallkit/demo/gsm8k-100-qwen3-4b/run_config.yaml \
    user@h200-host:/remote/path/recallkit/demo/gsm8k-100-qwen3-4b/
```

---

## 3. 在 H200 上重跑训练

### 3.1 SSH 进入 H200 执行

```bash
# 进入 H200
ssh user@h200-host

# 确认环境就绪
cd /remote/path/recallkit
uv sync --frozen
pars --version

# 设置 API Key（不要硬编码在脚本中）
export ANTHROPIC_API_KEY=sk-ant-...

# 运行 day1 demo（与本地命令完全相同）
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
    --name day1-r16-h200
```

**建议**：run name 加 `-h200` 后缀，区分本地跑和远端跑，避免混淆。

### 3.2 后台运行（nohup）

若 SSH 连接不稳定，建议后台运行：

```bash
# 后台运行，日志写到文件
nohup pars sft start \
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
    --name day1-r16-h200 \
    > ~/recallkit-day1.log 2>&1 &

# 记录 PID
echo $! > ~/recallkit-day1.pid
echo "PID: $(cat ~/recallkit-day1.pid)"
```

### 3.3 监控进度

```bash
# 方式 A：实时查看日志（保持 SSH 连接）
tail -f ~/recallkit-day1.log

# 方式 B：通过 pars status 查询（重连 SSH 后）
ssh user@h200-host "cd /remote/path/recallkit && pars sft status --run-id day1-r16-h200"

# 方式 C：查看 metrics.jsonl（实时追加）
ssh user@h200-host "tail -20 /remote/path/recallkit/runs/day1-r16-h200/metrics.jsonl"
```

---

## 4. 将产出结果同步回本地

训练完成后，把 H200 上的 `runs/<run-id>/` 同步回本地审阅。

### 4.1 同步 report 和 metrics（不含 checkpoint）

```bash
# 只同步 run 产出（不含 checkpoints/，避免拉取数十GB权重）
rsync -avz \
    --exclude='checkpoints/' \
    user@h200-host:/remote/path/recallkit/runs/day1-r16-h200/ \
    ./runs/day1-r16-h200/

# 验证关键文件
ls -lh ./runs/day1-r16-h200/
# 期望看到：config.yaml  state.json  metrics.jsonl  report.md  artifacts/
```

### 4.2 同步 artifacts（含训练曲线 PNG）

```bash
rsync -avz \
    user@h200-host:/remote/path/recallkit/runs/day1-r16-h200/artifacts/ \
    ./runs/day1-r16-h200/artifacts/

# 确认 PNG 存在
ls ./runs/day1-r16-h200/artifacts/*.png
```

### 4.3 若需要同步 LoRA 适配器权重（用于本地推理）

```bash
# 警告：LoRA adapter 大小约 200MB-2GB，视 rank 而定
# 不要用 git 管理这些文件（见 .gitignore）
rsync -avz \
    user@h200-host:/remote/path/recallkit/checkpoints/day1-r16-h200/ \
    ./checkpoints/day1-r16-h200/

# 本地使用 LoRA adapter 推理（需要 transformers + peft）
# 见 docs/local-inference.md（T029 范围，非本 Playbook 内容）
```

---

## 5. 注意事项与已知限制

### 5.1 机器指纹与 resume 限制（C22）

RecallKit 的 checkpoint 路径与状态锁文件（`state.json`）绑定在具体机器的文件系统路径上。

**跨机 resume 的具体问题**：
- `state.json` 中的 checkpoint 路径是绝对路径（`/remote/path/recallkit/checkpoints/...`），
  在本地机器上无效。
- 状态锁文件（`runs/<id>/.lock`）是基于 PID 的，跨机器无意义。
- Unsloth 的 4-bit 量化 kernel 对 GPU 架构敏感，H200（Hopper）和 4090（Ada Lovelace）
  的 kernel 编译结果不兼容。

**唯一支持的跨机场景**：从头重跑（re-run），不是续接（resume）。

### 5.2 GPU 型号差异对指标的影响

4-bit 量化（bitsandbytes）在不同 GPU 上的精度略有差异：

| GPU | 架构 | 量化精度 |
|-----|------|----------|
| H200 | Hopper (sm_90) | 最高精度 |
| A100 | Ampere (sm_80) | 与 H200 接近 |
| RTX 4090 | Ada Lovelace (sm_89) | 略低，但差异 < 1% |
| RTX 3090 | Ampere (sm_86) | 与 A100 接近 |

若 H200 上的 baseline acc 与 4090 测出的结果相差 > 3%，属正常现象，
在 `expected_metrics.md` 的备注栏记录即可（不算复现失败）。

### 5.3 HuggingFace 下载缓存

H200 上首次运行需要下载模型权重（约 6-8GB）。若 H200 没有外网或速度慢：

```bash
# 方式 A：从本地 4090 rsync 缓存
rsync -avz ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct/ \
    user@h200-host:~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct/

# 方式 B：设置 H200 从本地 scp
# 见 HuggingFace 官方文档：HF_HOME 环境变量
```

### 5.4 API Key 隔离

```bash
# 在 H200 上设置（session 级别，不持久化到 .bashrc）
export ANTHROPIC_API_KEY=sk-ant-...

# 不要写入 .bashrc 或任何版本控制的文件
# 不要使用 echo $ANTHROPIC_API_KEY 将完整 key 打印到日志
```

---

## 6. 完整工作流示例（4090 本地 → H200 重跑）

```
本地 4090                           H200
──────────────────────────          ──────────────────────────
                                    
1. 写 run_config.yaml               
   (本地 demo/ 目录)                 
                                    
2. rsync repo 到 H200  ─────────>  3. 收到代码 + 配置
                                    
                                   4. uv sync --frozen
                                    
                                   5. pars sft start ... --name day1-r16-h200
                                      （H200 训练约 25-45min）
                                    
                                   6. report.md 生成
                                    
7. rsync runs/ 回本地  <─────────  
                                    
8. 本地审阅 report.md
   pars sft compare day1-r16 day1-r16-h200
```

---

## 7. 故障排查

### Q: SSH 连接中断，训练是否还在继续？

若使用 `nohup` 后台运行（见 §3.2），是的，训练在 H200 上继续。
重新 SSH 进入后，通过 `pars sft status` 或 `tail -f ~/recallkit-day1.log` 查看。

### Q: rsync 时 "Permission denied" 报错？

```bash
# 确认远端目录权限
ssh user@h200-host "ls -la /remote/path/recallkit/runs/"

# 若 runs/ 目录不存在，先创建
ssh user@h200-host "mkdir -p /remote/path/recallkit/runs/"
```

### Q: H200 上 pars 命令找不到？

```bash
# 确认 uv tool install 已经完成
ssh user@h200-host "which pars || echo 'pars not found'"

# 若未安装
ssh user@h200-host "cd /remote/path/recallkit && uv tool install ."
```

### Q: 怎么知道 H200 上的 run 完成了？

```bash
# state.json 中 final_state = "completed" 表示成功
ssh user@h200-host "cat /remote/path/recallkit/runs/day1-r16-h200/state.json | grep final_state"

# 或用 pars status
ssh user@h200-host "cd /remote/path/recallkit && pars sft status --run-id day1-r16-h200"
```

---

_本 Playbook 对应 spec.md C9（checkpoint 管理）+ C22（跨机 resume 明确不支持）。_
_文档版本与 RecallKit v0.1.0.dev0 对应。_
