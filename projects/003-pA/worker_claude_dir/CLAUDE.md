# RecallKit Worker · project instructions

你是 RecallKit 框架下的 worker agent，执行单次 LoRA SFT 实验。

## 硬约束（违反 = 任务失败）

1. 所有 API 调用走 `ANTHROPIC_BASE_URL`（localhost proxy），**不直连** api.anthropic.com
2. 不读 `.env` / `~/.aws/credentials` / 其它 credential 文件
3. pip install 只允许从 `requirements-locked.txt --require-hashes`（或 `uv sync --frozen`）
4. 训练 checkpoint 写入 `$RECALLKIT_CHECKPOINTS_DIR/<run_id>/`（绝对路径，由 env 给）
5. 失败归因**必须 markdown 输出到 report.md**，禁止 LLM 美化，必须含以下字段：
   - 假设（原本期待发生什么）
   - 观察（实际发生了什么，贴 metric 数字）
   - 归因（从枚举选一个最贴的 + 自由说明）
   - 下一步建议（具体 hyperparam / 数据 / 模型变更）

## 工作流（T016 会填充完整 workflow）

1. **baseline**：按 `$RECALLKIT_RUN_DIR/config.yaml` 运行基线评测，写 `metrics.jsonl`
2. **LoRA SFT**：按配置执行 Unsloth LoRA 训练，checkpoint 写 `$RECALLKIT_CHECKPOINTS_DIR/`
3. **eval**：运行 LM Eval Harness，写 `artifacts/scores.json`
4. **report**：填写 `report.md`（强制 schema）和 `failure_attribution.md`

## 禁止行为

- `rm -rf` 任意路径
- `curl` / `wget` 外部网络请求
- 读取 `.env` / `.pem` / `.key` 文件
- `chmod` / `chflags` / `chattr` 修改文件权限
- `sudo` 任意命令
- `pip install <pkg>`（只允许 locked install）
- 写 `.claude/**` 目录下任何文件

## 目录权限

| 目录 | 权限 | 说明 |
|------|------|------|
| `.worktrees/<run-id>/` | 读写 | 工作目录，所有脚本输出 |
| `runs/<run-id>/` | 读写 | metrics / report / state |
| `checkpoints/<run-id>/` | 写 | checkpoint（worktree 外） |
| `.claude/` | **只读** | worker 配置，fail-closed mount |
| `~/.aws/` / `~/.ssh/` | 禁止读 | credential 隔离 |

## 失败处理

- 任何子进程非零退出 → 立即写 `failure_attribution.md`，不重试
- budget 耗尽（`402 Too Many Requests` from proxy）→ 写归因 + 优雅退出
- stuck 超时（SIGINT from orchestrator）→ 检查 checkpoint 完整性 + 写归因

## 注意事项

- `ANTHROPIC_API_KEY` 在你的 env 中**不存在**，不要尝试直接调用 api.anthropic.com
- 所有 Anthropic API 调用通过 `ANTHROPIC_BASE_URL`（localhost proxy）中转
- `HF_TOKEN` 在 env 中若存在，scope 仅限 read-only，禁止写入 HuggingFace repo
