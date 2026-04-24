# RecallKit

**RecallKit 是决策工具，不是 LoRA 炼丹工具。** 它让你在本机单 GPU 上严格顺序地跑
baseline -> LoRA SFT -> eval -> markdown 决策报告，并强制输出含训练曲线、分数对比
和失败归因的可复现记录。诚实的负面 demo（LoRA 未提升）和正面 demo 一样是合法的 ship。

> 本项目处于 alpha 开发阶段（v0.1.0.dev0），API 随时可能变化，不建议在生产环境使用。

---

## 1. Pitch

RecallKit 解决的核心问题：操作员做了一次 LoRA 实验，但不知道这个改动是否真的有效，
因为没有严格的 baseline 对比，没有自动记录的失败归因，也无法与下一次实验做横向比较。

RecallKit 的解决方案：
- 每次实验强制跑 baseline + LoRA SFT + eval，产出含三节（训练曲线/分数对比/失败归因）的
  markdown 报告
- `pars compare runA runB` 做跨实验决策，不凭直觉
- `pars sft retry --from <run-id>` 继承父实验配置，只调你关心的超参
- 诚实负面（LoRA 没提升）= 合法结论，RecallKit 不会帮你掩盖

**RecallKit 不是什么**：
- 不是自动炼丹工具（不自动搜索超参，每次实验都需要操作员主动发起）
- 不是云 GPU 调度器（本机单卡，不集成 Runpod / SageMaker）
- 不是 Web UI（纯 CLI，报告在 markdown 文件里）

---

## 2. Quick Start

```bash
# 1. Clone 并安装依赖
git clone https://github.com/<your-handle>/recallkit.git
cd recallkit
uv sync --frozen

# 2. 安装 CLI
uv tool install .

# 3. 确认 CLI 可用
pars --version
pars sft start --help
```

**前置条件**：
- Python 3.12.x（uv 会自动管理）
- NVIDIA GPU >= 16GB VRAM（见最低配置节）
- CUDA 12.1+
- `export ANTHROPIC_API_KEY=sk-ant-...`（worker 通过 proxy 调用，key 不进 worker 环境）

**无 HF_TOKEN 也能跑**：默认 demo 使用的 `Qwen/Qwen2.5-3B-Instruct` 和 `openai/gsm8k`
均为公开 repo，无需 `HF_TOKEN`。仅在使用 gated 模型时需要（见安全声明节）。

---

## 3. 示例场景（gsm8k-100 + Qwen2.5-3B-Instruct）

完整演练剧本见 [demo/gsm8k-100-qwen3-4b/scenario.md](demo/gsm8k-100-qwen3-4b/scenario.md)。

**核心剧本简版**（7 天内完成）：

```bash
# Day 1: 启动 baseline + LoRA r=16
pars sft start \
    --question "LoRA r=16 能否在 gsm8k-100 上提升 >= 5% accuracy?" \
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
    --name day1-r16

# Day 2: 基于 day1 结果，发起 r=32 变体
pars sft retry \
    --from day1-r16 \
    --hypothesis "r=32 能在 gsm8k-100 上进一步提升" \
    --lora-rank 32 \
    --lora-alpha 64 \
    --name day2-r32

# Day 5: 对比两次实验，做决策
pars sft compare day1-r16 day2-r32
```

**完整演练脚本**：
```bash
# 按天执行（推荐）
bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh day1
bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh day2
bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh compare

# 全流程一次性跑（适合 H200 等快速 GPU）
bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh all
```

**期望指标**：见 [demo/gsm8k-100-qwen3-4b/expected_metrics.md](demo/gsm8k-100-qwen3-4b/expected_metrics.md)。

---

## 4. 架构图

RecallKit v0.1 采用严格顺序的单 worker 执行模型：

```
操作员
  |
  | pars sft start (--question / --base / --dataset / --name)
  v
Orchestrator（pars/orch/orchestrator.py）
  |
  +---> API Proxy（localhost）
  |     - 持有 ANTHROPIC_API_KEY（不注入 worker）
  |     - 预算前置预估（C20：余额不足返回 402，不发上游请求）
  |
  +---> Worker（claude -p headless，git worktree 内）
  |     - 运行 baseline eval（LM Eval Harness）
  |     - 运行 LoRA SFT（Unsloth）
  |     - 运行 SFT 后 eval（LM Eval Harness）
  |     - 产出 report.md + failure_attribution.md
  |
  +---> Run Ledger（runs/<run-id>/）
  |     - config.yaml    RunConfig（操作员输入）
  |     - metrics.jsonl  实时指标流
  |     - report.md      最终决策报告
  |     - failure_attribution.md（若失败）
  |
  +---> Checkpoints（checkpoints/<run-id>/，worktree 外）
        - 支持同机重启续跑（pars sft resume）
        - 不承诺跨机器 resume（C22）

Stuck 状态机（architecture.md §8）
  - 5 秒采样 GPU util / CPU / 磁盘 IO / 网络 IO
  - 仅 truly_stuck > 15min 才发 SIGINT
  - 白名单 4 态：idle / training / downloading / truly_stuck

Budget 控制（双保险）
  - 主：proxy 前置预估拒绝（C20 硬帽）
  - 备：60 秒轮询 SIGINT（wall-clock / GPU hours 上限）
```

**数据流（单 run）**：

```
run_config.yaml -> Orchestrator -> Worker
                                      |
                                      v
                        runs/<id>/metrics.jsonl（实时）
                        runs/<id>/report.md（完成后）
                        checkpoints/<id>/*.safetensors（不入 git）
```

---

## 5. CLI 参考

### pars sft start

启动新的 SFT 训练 run（baseline + LoRA + eval + 决策报告完整循环）。

```bash
pars sft start \
    --question TEXT              # 研究假设（必填）
    --base TEXT                  # HuggingFace base model ID（必填）
    --dataset TEXT               # HuggingFace 数据集 ID（必填）
    --dataset-split TEXT         # 数据集 split（默认 train[:100]）
    --lora-rank INT              # LoRA rank（默认 16）
    --lora-alpha INT             # LoRA alpha（默认 32）
    --lr FLOAT                   # 学习率（默认 2e-4）
    --epochs INT                 # 训练 epoch 数（默认 3）
    --batch-size INT             # per-device batch size（默认 2）
    --max-seq-len INT            # 最大序列长度（默认 2048）
    --eval-tasks TEXT            # lm-eval task 列表，逗号分隔（默认 gsm8k）
    --usd-cap FLOAT              # USD 硬帽（默认 30.0）
    --wall-clock-hours-cap FLOAT # wall-clock 时间上限（小时，默认 12.0）
    --gpu-hours-cap FLOAT        # GPU 小时上限（默认 12.0）
    --name TEXT                  # 覆盖自动生成的 ULID（可选）
```

**退出码**：
- `0` — 完成
- `2` — 配置错误（API key 缺失 / .claude/ 只读保护触发）
- `3` — Stuck 状态机触发 SIGINT
- `4` — 预算超限（USD 或 wall-clock 或 GPU hours）
- `5` — Worker crash

### pars sft resume

从 checkpoint 续跑中断的 SFT run（**仅限同机重启**，跨机器不承诺，C22）。

```bash
pars sft resume \
    --run-id TEXT  # 要续跑的 run ID（必填）
    --yes          # 跳过交互确认（可选）
```

### pars sft retry

基于已有 run 创建新实验（调整超参数后重跑）。

```bash
pars sft retry \
    --from TEXT          # 基于哪个 run ID（必填）
    --hypothesis TEXT    # 新实验假设文本（可选，覆盖原 run 假设）
    --lora-rank INT      # 覆盖 LoRA rank（可选）
    --lora-alpha INT     # 覆盖 LoRA alpha（可选）
    --lr FLOAT           # 覆盖学习率（可选）
    --name TEXT          # 新 run 名称（可选）
```

### pars sft compare

对比两个 run 的 config / metric / 结论，输出 markdown 差异表。

```bash
pars sft compare RUN_ID_A RUN_ID_B
```

### pars sft status

查询 SFT run 的当前状态（训练进度 / stuck 状态 / 已用预算）。

```bash
pars sft status \
    --run-id TEXT  # 指定 run ID（默认显示最近一个 run）
```

### pars unlock

手动清除 stuck_lock 文件（Stuck 状态机误判场景下的人工干预路径）。

```bash
pars unlock \
    --run-id TEXT  # 要解锁的 run ID（必填）
```

---

## 6. 失败处理

### 6.1 Proxy 返回 402（预算超限）

**含义**：USD 硬帽触发，proxy 前置拒绝了该请求（C20 设计，非 bug）。

```
[ERROR] 402 Budget exceeded: estimated cost $0.12, remaining $0.08
```

**处理**：查看 `pars sft status --run-id <id>` 确认已用预算，
若合理则提高 `--usd-cap` 重新启动。

### 6.2 ReadonlyFailsClosed（.claude/ 只读保护触发）

**含义**：MacFUSE + bindfs 只读 mount 未生效，CLI 拒绝启动（C21 设计）。

```
[ERROR] .claude/ fail-closed 保护触发（C21）
```

**处理**：见 [docs/demo-reproduction.md](docs/demo-reproduction.md) §3 MacFUSE 配置节。

### 6.3 Stuck 检测误杀

**含义**：Stuck 状态机误判为真 stuck（通常发生在 LoRA epoch 数据加载长等待期）。

```
[WARN] stuck_lock detected: truly_stuck > 15min, SIGINT sent
```

**处理**：确认是误判后，手动解锁并续跑：

```bash
pars unlock --run-id <id>
pars sft resume --run-id <id>
```

### 6.4 GPU OOM（显存不足）

**症状**：`CUDA out of memory` 错误，run 以 exit_code=5 结束。

**处理方案**（按优先级）：
1. 降低 batch_size：`--batch-size 1`
2. 降低 max_seq_len：`--max-seq-len 1024`
3. 切换更小模型：`--base Qwen/Qwen2.5-1.5B-Instruct`
4. 最保底：`--base TinyLlama/TinyLlama-1.1B-Chat-v1.0`

### 6.5 HuggingFace 下载失败

公开模型无需 HF_TOKEN。若网络问题，检查代理配置或等待 HuggingFace Hub 恢复。
若模型已在本地缓存（`~/.cache/huggingface/`），离线也可跑。

---

## 7. 最低硬件与软件需求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| OS | macOS 14+ / Ubuntu 22.04+ | Ubuntu 22.04 LTS |
| GPU | NVIDIA 16GB+（TinyLlama 1.1B demo） | NVIDIA RTX 4090 24GB（Qwen2.5-3B QLoRA） |
| CUDA | 12.1+ | 12.4 |
| RAM | 32GB | 64GB |
| 磁盘 | 100GB 空余 | 500GB SSD |
| Python | 3.12.x | 3.12.x |
| uv | >= 0.5.0 | 最新 |
| Claude Code CLI | 2026-04-latest | 最新 |
| MacFUSE + bindfs | >= 4.0（macOS C21） | 最新 |

**不支持的配置**（v0.1）：
- Apple Silicon MPS（Unsloth 不支持 MPS，需要 NVIDIA GPU）
- Windows（未测试）
- 多 GPU 并行（v0.1 仅单卡）
- Docker 容器化（非目标，见 non-goals.md）

---

## 8. Reproducibility（可复现性）

### 8.1 Demo 期望指标

见 [demo/gsm8k-100-qwen3-4b/expected_metrics.md](demo/gsm8k-100-qwen3-4b/expected_metrics.md)。

主要期望值（基于公开数据估算，非本机实测保证值）：
- Qwen2.5-3B baseline gsm8k-100（5-shot）: ~0.38-0.44
- LoRA r=16（3 epochs）：提升 ~+3%-+10%
- Wall clock（H200）：~40-50min 完整 run

### 8.2 版本锁定

RecallKit 使用 uv lockfile 锁定所有依赖版本：

```bash
# 安装完全对齐 lockfile 的依赖（不升级任何包）
uv sync --frozen

# 查看关键依赖版本
uv run python -c "import unsloth; print(unsloth.__version__)"
uv run lm_eval --version
```

**若本地指标偏差 >= 10 个百分点**，请检查：
- GPU 型号（不同 GPU 的 4-bit 量化精度有差异）
- CUDA 版本（Unsloth 依赖特定 kernel 版本）
- Unsloth 版本（确认 2024.10+）

### 8.3 H200 远端重跑

若在 H200 上重跑（非跨机 resume，而是远端重跑训练）：
见 [docs/h200-rsync-playbook.md](docs/h200-rsync-playbook.md)。

**重要**：`pars sft resume` 仅支持同机重启，不支持跨机器 resume（C22）。
H200 playbook 只教"将配置 rsync 到 H200 后从零重新训练"。

---

## 9. 安全声明

### 9.1 HF_TOKEN 最小权限

RecallKit 默认 demo（Qwen2.5-3B-Instruct / openai/gsm8k）**无需 HF_TOKEN**，
所有资源均为公开 HuggingFace repo。

若需要访问 gated 模型（如 Meta-Llama-3.1-8B），仅允许使用 **read-only scope**
的 HF_TOKEN，且 token 仅由 orchestrator（非 worker）在下载期间临时持有，
下载完成后立即从环境变量移除。

**严禁**：HF_TOKEN 含 write / private-mirror / write-repo 权限。

### 9.2 Anthropic API Key 隔离

`ANTHROPIC_API_KEY` 仅在 orchestrator 层持有，**不进入 worker 子进程环境**（C15）。
Worker 通过本机 localhost API proxy 调用 Anthropic API，proxy 同时负责预算预估。

```bash
# 正确用法（key 在 host 环境，不传给 worker）
export ANTHROPIC_API_KEY=sk-ant-...
pars sft start ...
```

### 9.3 pip 供应链锁定

Worker 内仅允许安装来自 `requirements-locked.txt` 的包（`--require-hashes` 验证），
禁止任意 `pip install <pkg>`（C17）。

### 9.4 训练数据隐私

RecallKit 将你的训练数据集视为不透明的本地文件，不扫描、不上传、不修改。
所有数据本地存储（C14），不传云。

若你的训练数据含个人信息（PII）且你指示 worker 将样本粘贴到 prompt，
该数据将通过你的 Anthropic 账号 DPA 到达 Anthropic API。
你需要自行评估 GDPR 数据最小化等义务——这是操作员与 Anthropic 的直接关系。

### 9.5 本 demo 使用的 base model license

本 demo 使用 `Qwen/Qwen2.5-3B-Instruct`，遵循 Tongyi Qianwen License Agreement。
运行本 demo 即表示你同意 base model 的条款。RecallKit 本身为 MIT 许可证；
**本仓库不重新分发任何 base model 权重**。

```
This demo uses Qwen2.5-3B-Instruct under Tongyi Qianwen License.
By running this demo you agree to the base model's terms.
RecallKit itself is MIT; base model weights are NOT redistributed by this repo.
```

---

## 10. 操作员责任声明

RecallKit 是研究工具。若你用它训练的模型将在受监管的场景中部署（医疗、金融、
招聘、监控等），你需要自行评估适用的法规（EU AI Act、本地 ML 法规等）并确保
你的下游模型符合合规要求。RecallKit 不会代表你评估或执行任何此类合规义务。

使用 RecallKit 需要 Anthropic API key 并遵守 Anthropic 使用政策。你的 API 用量
计入你的 Anthropic 账号；RecallKit 是调用你配置的 API 的客户端。

---

## 11. License

RecallKit 采用 MIT License。见 [LICENSE](LICENSE)（由 T028 生成）。

```
MIT License

Copyright (c) 2026 RecallKit Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

免责声明：RecallKit 按"现状"提供，不附任何明示或暗示的担保。你对以下事项负责：
1. 遵守你用本工具训练的模型在适用法律法规下的合规义务
2. 在 Anthropic 使用政策和 HuggingFace 服务条款下使用 API
3. 确保你的训练数据符合适用的数据保护法规（GDPR、CCPA 等）

---

## 12. Contributing

RecallKit 是单人 OSS 项目（bus-factor = 1，spec.md C19 明示）。

贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)（由 T028 生成），主要规则：
- 所有 PR 需附测试（TDD 优先，失败测试先于实现）
- 提交信息遵循 Conventional Commits 规范
- 不做 Docker / Web UI / 多 Worker 功能（见 non-goals.md）
- 欢迎：bug fix / 文档改进 / 新 eval task 支持 / 更多 demo 场景

若遇到问题，请先查看故障处理节和 `docs/demo-reproduction.md`，
再开 Issue 并附上相关 `runs/<id>/report.md` 内容。
